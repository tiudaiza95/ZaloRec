import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import json
import wave

from recording_library import (
    prepare_audio_for_gemini,
    format_call_minutes,
    filter_records,
    transcribe_with_gemini,
    delete_recording,
    trim_audio,
    read_json,
    atomic_json
)
from recording_names import caller_from_title
from main import resolve_device
from audio_engine import AudioSession
import queue


class Release30Tests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_wav(self, name, duration_sec=3.0):
        p = self.dir / name
        with wave.open(str(p), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b'\x00\x00' * int(16000 * duration_sec))
        return p

    def test_prepare_audio_downsamples_wav(self):
        wav = self._create_wav('large_speech.wav', duration_sec=5.0)
        prepared_path, is_temp = prepare_audio_for_gemini(wav)
        self.assertTrue(is_temp)
        self.assertTrue(prepared_path.is_file())
        self.assertEqual(prepared_path.suffix.lower(), '.mp3')
        # Clean up temp
        prepared_path.unlink(missing_ok=True)

    def test_prepare_audio_small_mp3_passthrough(self):
        mp3 = self.dir / 'small.mp3'
        mp3.write_bytes(b'ID3\x03\x00\x00\x00\x00\x00\x00' + b'\x00' * 1000)
        prepared_path, is_temp = prepare_audio_for_gemini(mp3)
        self.assertFalse(is_temp)
        self.assertEqual(prepared_path, mp3)

    def test_format_call_minutes(self):
        wav = self._create_wav('call_sample.wav', 1.0)
        sidecar = wav.with_suffix('.wav.json')
        sidecar.write_text(json.dumps({
            'caller_name': 'Nguyễn Văn A',
            'started_at': '2026-11-04T10:00:00',
            'ended_at': '2026-11-04T10:15:30',
            'duration': 930.0,
            'summary': '📌 Hẹn ký hợp đồng vào thứ Sáu tuần này.\n✅ Cần chuẩn bị bản cứng.',
            'transcription': 'Alo, chào anh Nam...',
            'timestamps': [{'time': 60, 'label': 'Thảo luận giá'}],
            'note': 'Khách hàng VIP'
        }, ensure_ascii=False), encoding='utf-8')

        minutes = format_call_minutes(wav)
        self.assertIn('Nguyễn Văn A', minutes)
        self.assertIn('Hẹn ký hợp đồng', minutes)
        self.assertIn('Khách hàng VIP', minutes)
        self.assertIn('Thảo luận giá', minutes)
        self.assertIn('Alo, chào anh Nam', minutes)

    def test_fulltext_search_in_filter_records(self):
        records = [
            {
                'name': 'Zalo_01.mp3',
                'timestamp': '2026-11-04T08:00:00',
                'duration': 120,
                'metadata': {
                    'caller_name': 'Trần Thị B',
                    'note': 'Hỏi về đơn hàng số 123',
                    'summary': '📌 Bàn về tiến độ giao hàng',
                    'transcription': 'Đơn hàng sẽ giao vào chiều nay'
                }
            },
            {
                'name': 'Zalo_02.mp3',
                'timestamp': '2026-11-04T09:00:00',
                'duration': 300,
                'metadata': {
                    'caller_name': 'Lê Văn C',
                    'note': '',
                    'summary': '📌 Đàm phán hợp đồng cung cấp linh kiện',
                    'transcription': 'Chúng tôi đồng ý mức chiết khấu 15%'
                }
            }
        ]

        # Search by caller name
        res = filter_records(records, query='Trần Thị B')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'Zalo_01.mp3')

        # Search by summary keyword
        res = filter_records(records, query='hợp đồng')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'Zalo_02.mp3')

        # Search by transcript keyword
        res = filter_records(records, query='chiết khấu')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'Zalo_02.mp3')

        # Search accent-insensitive
        res = filter_records(records, query='chiet khau')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], 'Zalo_02.mp3')

    def test_transcribe_with_gemini_cleans_temporary_compressed_file(self):
        wav = self._create_wav('to_transcribe.wav', duration_sec=2.0)
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_resp = MagicMock()
            mock_resp.read.return_value = json.dumps({
                'candidates': [{
                    'content': {
                        'parts': [{'text': 'Đã nhận dạng thành công'}]
                    }
                }]
            }).encode('utf-8')
            mock_urlopen.return_value.__enter__.return_value = mock_resp

            result = transcribe_with_gemini('test_key', wav, task='transcribe')
            self.assertEqual(result, 'Đã nhận dạng thành công')

            # Ensure no lingering ~gemini_opt_ temp files in folder
            temp_files = list(self.dir.glob('~gemini_opt_*'))
            self.assertEqual(len(temp_files), 0)


    def test_delete_recording(self):
        wav = self._create_wav('to_delete.wav', duration_sec=1.0)
        sidecar = wav.with_suffix('.wav.json')
        sidecar.write_text('{"caller_name": "Test"}', encoding='utf-8')
        self.assertTrue(wav.is_file())
        self.assertTrue(sidecar.is_file())

        self.assertTrue(delete_recording(wav))
        self.assertFalse(wav.exists())
        self.assertFalse(sidecar.exists())

    def test_trim_audio_preserves_metadata(self):
        wav = self._create_wav('original.wav', duration_sec=10.0)
        sidecar = wav.with_suffix('.wav.json')
        atomic_json(sidecar, {
            'caller_name': 'Đại gia',
            'started_at': '2026-11-04T12:00:00',
            'timestamps': [
                {'time': 2.0, 'label': 'Trước cắt'},
                {'time': 6.0, 'label': 'Quan trọng'},
                {'time': 9.5, 'label': 'Sau cắt'}
            ],
            'note': 'Ghi chú gốc'
        })
        cut_file = self.dir / 'cut.wav'
        trim_audio(wav, 4.0, 8.0, cut_file)
        self.assertTrue(cut_file.is_file())
        cut_meta = read_json(cut_file.with_suffix('.wav.json'))
        self.assertEqual(cut_meta.get('caller_name'), 'Đại gia')
        self.assertEqual(cut_meta.get('duration'), 4.0)
        self.assertIn('Cắt từ original.wav [4s - 8s]', cut_meta.get('note', ''))
        self.assertIn('Ghi chú gốc', cut_meta.get('note', ''))
        # Timestamp at 6.0 should become 2.0 (6.0 - 4.0)
        ts = cut_meta.get('timestamps', [])
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0]['time'], 2.0)
        self.assertEqual(ts[0]['label'], 'Quan trọng')

    def test_caller_from_title_with_call_window(self):
        # Dedicated call window (e.g. ZaloCall.exe) with contact name only
        title = 'Trần Văn Mạnh - Zalo'
        self.assertEqual(caller_from_title(title, is_call_window=True), 'Trần Văn Mạnh')
        title2 = 'Nguyễn Thị Hoa'
        self.assertEqual(caller_from_title(title2, is_call_window=True), 'Nguyễn Thị Hoa')
        # Without is_call_window=True, plain names are not assumed to be calls
        self.assertEqual(caller_from_title(title2, is_call_window=False), '')

    def test_resolve_device_fallback(self):
        devices = [
            {'name': 'Default Speaker', 'index': 0},
            {'name': 'Headphones USB', 'index': 3}
        ]
        # Exact match
        self.assertEqual(resolve_device(devices, 'Headphones USB  [#3]', fallback_index=0), 3)
        # Unplugged device falls back to fallback_index
        self.assertEqual(resolve_device(devices, 'Bluetooth Headset  [#5]', fallback_index=0), 0)

    def test_audio_session_live_bookmark(self):
        q = queue.Queue()
        session = AudioSession(q)
        session.add_bookmark(25.4, 'Bàn giá cả')
        session.add_bookmark(65.1, 'Chốt hợp đồng')
        self.assertEqual(len(session._live_bookmarks), 2)
        self.assertEqual(session._live_bookmarks[0]['time'], 25.4)
        self.assertEqual(session._live_bookmarks[0]['label'], 'Bàn giá cả')


if __name__ == '__main__':
    unittest.main()

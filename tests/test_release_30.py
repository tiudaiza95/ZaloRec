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
    transcribe_with_gemini
)


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


if __name__ == '__main__':
    unittest.main()

import json
import queue
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from audio_player import AudioPlayer
from recording_library import (
    atomic_json,
    prepare_audio_for_gemini,
    rename_recording,
    transcribe_with_gemini,
)


class AuditFixesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_rename_recording_strips_duplicate_extension(self):
        f = self.dir / 'OldName.mp3'
        f.write_bytes(b'dummy')
        sidecar = f.with_suffix('.mp3.json')
        sidecar.write_text('{}', encoding='utf-8')

        # User accidentally includes .mp3 in new name
        dest = rename_recording(f, 'Renamed_Call.mp3')
        self.assertEqual(dest.name, 'Renamed_Call.mp3')
        self.assertTrue(dest.is_file())
        self.assertTrue(dest.with_suffix('.mp3.json').is_file())
        self.assertFalse(f.exists())

    def test_audio_player_status_safe_fallback(self):
        # Mock command returning invalid or empty string for position
        player = AudioPlayer(command=lambda cmd: '' if 'position' in cmd else 'playing')
        player.path = self.dir / 'test.mp3'
        mode, pos = player.status()
        self.assertEqual(mode, 'playing')
        self.assertEqual(pos, 0)

    def test_audio_player_set_volume_safe_exception_handling(self):
        def bad_command(cmd):
            if 'setaudio' in cmd:
                raise RuntimeError('Unsupported MCI command')
            return 'ok'

        player = AudioPlayer(command=bad_command)
        player.path = self.dir / 'test.mp3'
        # Should not raise exception
        player.set_volume(50)
        self.assertEqual(player.volume, 50)

    def test_audio_player_close_resets_even_on_error(self):
        def failing_close(cmd):
            if 'close' in cmd:
                raise RuntimeError('MCI close error')
            return 'ok'

        player = AudioPlayer(command=failing_close)
        player.path = self.dir / 'test.mp3'
        player.length = 5000
        player.close()
        self.assertIsNone(player.path)
        self.assertEqual(player.length, 0)

    def test_prepare_audio_metadata_duration_and_bitrate(self):
        # MP3 file > 18MB mock
        mp3 = self.dir / 'large.mp3'
        mp3.write_bytes(b'\x00' * (19 * 1024 * 1024))
        sidecar = mp3.with_suffix('.mp3.json')
        atomic_json(sidecar, {'duration': 7200.0})  # 120 minutes (> 6000s)

        with patch('subprocess.run') as mock_run, patch('audio_engine.find_ffmpeg', return_value='ffmpeg.exe'):
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_run.return_value = mock_proc

            # Create the expected output file when ffmpeg is mocked
            def fake_run(cmd, **kwargs):
                out_file = Path(cmd[-1])
                out_file.write_bytes(b'compressed_audio')
                return mock_proc

            mock_run.side_effect = fake_run

            out_path, is_temp = prepare_audio_for_gemini(mp3)
            self.assertTrue(is_temp)
            # Verify 16k bitrate was used for > 6000s (120 mins)
            called_cmd = mock_run.call_args[0][0]
            self.assertIn('16k', called_cmd)
            out_path.unlink(missing_ok=True)

    def test_gemini_api_handles_safety_blocked_response(self):
        mp3 = self.dir / 'sample.mp3'
        mp3.write_bytes(b'ID3\x03' + b'\x00' * 500)

        with patch('urllib.request.urlopen') as mock_url:
            mock_resp = MagicMock()
            mock_resp.read.return_value = json.dumps({
                'candidates': [{
                    'finishReason': 'SAFETY',
                    'index': 0
                }]
            }).encode('utf-8')
            mock_url.return_value.__enter__.return_value = mock_resp

            with self.assertRaises(RuntimeError) as ctx:
                transcribe_with_gemini('test_key', mp3)
            self.assertIn('SAFETY', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()

"""AL-HUDA production-oriented background Azan service foundation.

Keeps scheduling/playback isolated so UI screens can control it without
embedding Android-specific code throughout the app.
"""
from __future__ import annotations
from typing import Optional

class AzanService:
    def __init__(self, audio_path: Optional[str] = None):
        self.audio_path = audio_path
        self._player = None
        self._playing = False

    @property
    def is_playing(self) -> bool:
        return self._playing

    def play(self, audio_path: Optional[str] = None) -> bool:
        path = audio_path or self.audio_path
        if not path:
            return False
        try:
            from kivy.core.audio import SoundLoader
            if self._player:
                self.stop()
            self._player = SoundLoader.load(path)
            if not self._player:
                return False
            self._player.play()
            self._playing = True
            return True
        except Exception:
            self._player = None
            self._playing = False
            return False

    def stop(self) -> None:
        if self._player:
            try:
                self._player.stop()
            except Exception:
                pass
        self._playing = False

    def pause(self) -> None:
        if self._player:
            try:
                self._player.stop()
            except Exception:
                pass
        self._playing = False

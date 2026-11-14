import pygame, time

class Audio_Manager():
    def __init__(self):
        self.BACKGROUND_MUSIC = {
            "clickarea_default": {"path": "assets/audios/bgms/lobby.mp3", "volume": 0.75, "last_position": 0.0},
            "clickarea_rush": {"path": "assets/audios/bgms/rush.mp3", "volume": 0.75, "last_position": 0.0},
            "brown_square_boss": {"path": "assets/audios/bgms/paint_the_world_purple.mp3", "volume": 0.75, "last_position": 0.0},
        }

        self.current_track = None
        self.start_offset = 0.0

    def play_sound(self, sound, volume = 1):
        sound.set_volume(volume)
        sound.play()


    #time.monotonic() used to calculate the amount of milliseconds elapsed since the last time position update.
    def get_current_position(self):
        if not self.current_track:
            return 0.0

        track = self.BACKGROUND_MUSIC[self.current_track]

        if not pygame.mixer.music.get_busy():
            return track["last_position"]

        elapsed = time.monotonic() - track["last_position_time"]
        return track["last_position"] + elapsed

    def play_bgm(self, track_key, loops=-1, start=0.0, fade_ms=2000, resume=True):
        if self.current_track == track_key and not pygame.mixer.music.get_busy() and resume:
            pygame.mixer.music.unpause()
            return

        if self.current_track and self.current_track != track_key:
            track = self.BACKGROUND_MUSIC[self.current_track]
            track["last_position"] = self.get_current_position()
            track["last_position_time"] = time.monotonic()

        track = self.BACKGROUND_MUSIC[track_key]
        self.current_track = track_key

        if resume:
            pos = track["last_position"]
        else:
            pos = start
            track["last_position"] = pos

        track["last_position_time"] = time.monotonic()

        pygame.mixer.music.load(track["path"])
        pygame.mixer.music.set_volume(track["volume"])
        pygame.mixer.music.play(loops=loops, start=pos, fade_ms=fade_ms)

    def pause_bgm(self, fadeout_ms=750):
        if self.current_track:
            track = self.BACKGROUND_MUSIC[self.current_track]
            track["last_position"] = self.get_current_position()
            track["last_position_time"] = time.monotonic()
            pygame.mixer.music.fadeout(fadeout_ms)

    def resume_bgm(self):
        if self.current_track:
            track = self.BACKGROUND_MUSIC[self.current_track]
            pos = track["last_position"]
            track["last_position_time"] = time.monotonic()

            pygame.mixer.music.load(track["path"])
            pygame.mixer.music.set_volume(track["volume"])
            pygame.mixer.music.play(loops=-1, start=pos, fade_ms=400)


    def reset_track_position(self, track_key):
        self.BACKGROUND_MUSIC[track_key]["last_position"] = 0.0

import pyxel as px
from constants import (FPS, MUSIC_CHANNEL_0, MUSIC_CHANNEL_1, SOUND_CHANNEL)

class Audio:
    music_start_frame = 0
    music_paused_frame = 0
    music_is_paused = False
    music_current_index = 0
    music_current_loop_setting = True

    @classmethod
    def start_music(cls, index, do_loop):
        cls.music_start_frame = px.frame_count
        cls.music_is_paused = False
        cls.music_current_index = index
        cls.music_current_loop_setting = do_loop
        px.playm(index, loop=do_loop)

    @classmethod
    def resume_music(cls):
        if not cls.music_is_paused:
            return
        cls.music_is_paused = False
        paused_frames = px.frame_count - cls.music_paused_frame
        cls.music_start_frame += paused_frames
        px.playm(cls.music_current_index, 
                 sec=(px.frame_count - cls.music_start_frame) / FPS, 
                 loop=cls.music_current_loop_setting)
        # print("Resumed music, music frames: " +
        #       f"{ px.frame_count - cls.music_start_frame }")

    @classmethod
    def pause_music(cls):
        if cls.music_is_paused:
            return
        cls.music_is_paused = True
        cls.music_paused_frame = px.frame_count
        px.stop(MUSIC_CHANNEL_0)
        px.stop(MUSIC_CHANNEL_1)
        # print("Paused music, music frames: " +
        #       f"{ px.frame_count - cls.music_start_frame }")

    @classmethod
    def stop_music(cls):
        cls.music_is_paused = False
        px.stop(MUSIC_CHANNEL_0)
        px.stop(MUSIC_CHANNEL_1)
        
    @classmethod
    def stop_sfx(cls):
        px.stop(SOUND_CHANNEL)


from itertools import filterfalse
import pyxel as px
from player import Player
from bubble import Bubble
from harpoon import Harpoon
import hud
from utils import draw_centred_label, stop_music
import vars
from constants import (SCORE_SEC_REMAINING_BONUS, MAX_STAGE_NUMBER, 
                       SOUND_CHANNEL, SND_STAGE_CLEAR, MUS_GAMEPLAY,)
import stage_data

MAX_GET_READY_FRAMES = 120
MAX_TIME_UP_FRAMES = 120
MAX_GAME_OVER_FRAMES = 180
MAX_PLAYER_DEAD_FRAMES = 120
MAX_STAGE_CLEAR_FRAMES = 180

STATE_PLAY = 0
STATE_PAUSED = 1
STATE_TIME_UP = 2
STATE_GAME_OVER = 3
STATE_GET_READY = 4
STATE_PLAYER_DEAD = 5
STATE_STAGE_CLEAR = 6
STATE_GAME_COMPLETE = 7

class Stage:
   def __init__(self, app, number):
      self.app = app
      self.number = number
      self.music_pause_pos = 0
      self.reset()

   def reset(self):
      self.music_pause_pos = 0

      Bubble.reset()

      self.bubbles = []
      self.bubble_pops = []
      self.player = Player(self)
      self.harpoon = Harpoon(self)
      self.score_labels = []

      self.time_secs = 0
      self.time_frame_cnt = 0
      self.set_state(STATE_GET_READY)

      self.add_max_velocity_x = 0

      data = stage_data.DATA[self.number]
      for b in data["bubbles"]:
         Bubble(self, b[0], b[1])
      self.time_secs = data["time_secs"]
      self.add_max_velocity_x = data.get("add_max_velocity_x", 0)

   def set_state(self, new_state):
      self.state = new_state

   def update_state_get_ready(self):
      self.time_frame_cnt += 1
      if self.time_frame_cnt == MAX_GET_READY_FRAMES:
         self.time_frame_cnt = 0
         self.set_state(STATE_PLAY)
         px.playm(MUS_GAMEPLAY, self.music_pause_pos, loop=True)

   def update_state_stage_clear(self):
      self.time_frame_cnt += 1
      if self.time_frame_cnt == MAX_STAGE_CLEAR_FRAMES:
         self.time_frame_cnt = 0
         if vars.stage_number < MAX_STAGE_NUMBER - 1:
            self.app.go_to_next_stage()
         else:
            self.set_state(STATE_GAME_COMPLETE)
            stop_music()

   def update_state_game_complete(self):
      self.time_frame_cnt += 1
      if self.time_frame_cnt > 180:
         if vars.pressed_shoot:
            self.app.go_to_main_menu()

   def update_state_time_up(self):
      self.player.animate()
      self.time_frame_cnt += 1
      if self.time_frame_cnt == MAX_TIME_UP_FRAMES:
         self.time_frame_cnt = 0
         if vars.lives_remaining > 0:
            self.reset()
         else:
            self.set_state(STATE_GAME_OVER)

   def update_state_player_dead(self):
      self.player.animate()
      self.time_frame_cnt += 1
      if self.time_frame_cnt == MAX_PLAYER_DEAD_FRAMES:
         self.time_frame_cnt = 0
         if vars.lives_remaining > 0:
            self.reset()
         else:
            self.set_state(STATE_GAME_OVER)

   def update_state_game_over(self):
      self.player.animate()

      if vars.pressed_shoot:
         self.app.go_to_main_menu()
         return

      self.time_frame_cnt += 1
      if self.time_frame_cnt == MAX_GAME_OVER_FRAMES:
         self.time_frame_cnt = 0
         self.app.go_to_main_menu()

   def update_state_paused(self):
      if vars.pressed_pause:
         self.set_state(STATE_PLAY)
         px.playm(MUS_GAMEPLAY, self.music_pause_pos, loop=True)
         return
      
   def update_state_play(self):
      if vars.pressed_pause:
         self.set_state(STATE_PAUSED)
         self.music_pause_pos = stop_music()
         return

      self.time_frame_cnt += 1
      if self.time_frame_cnt == 60:
         self.time_frame_cnt = 0
         self.time_secs -= 1
         if self.time_secs == 0:
            self.player.kill()
            self.set_state(STATE_TIME_UP)
            stop_music()
            return

      self.player.update()
      self.harpoon.update()

      for b in self.score_labels:
         b.update()
      self.score_labels[:] = filterfalse(lambda x: x.remove, self.score_labels)

      for b in self.bubbles:
         b.update()
      self.bubbles[:] = filterfalse(lambda x: x.remove, self.bubbles)

      if self.player.is_dead():
         self.set_state(STATE_PLAYER_DEAD)
         self.bubble_pops = []
         self.score_labels = []
         stop_music()
      elif len(self.bubbles) == 0:
         px.play(SOUND_CHANNEL, SND_STAGE_CLEAR)
         self.set_state(STATE_STAGE_CLEAR)
         stop_music()
         vars.add_score(self.time_secs * SCORE_SEC_REMAINING_BONUS)
         self.bubble_pops = []
         self.score_labels = []

      for b in self.bubble_pops:
         b.update()
      self.bubble_pops[:] = filterfalse(lambda x: x.remove, self.bubble_pops)
   
   def update(self):
      # if px.btnp(px.KEY_R):
      #    self.reset()
      #    return
      
      if self.state == STATE_GET_READY:
            self.update_state_get_ready()
      elif self.state == STATE_PLAY:
            self.update_state_play()
      elif self.state == STATE_PAUSED:
            self.update_state_paused()
      elif self.state == STATE_TIME_UP:
            self.update_state_time_up()
      elif self.state == STATE_GAME_OVER:
            self.update_state_game_over()
      elif self.state == STATE_PLAYER_DEAD:
            self.update_state_player_dead()
      elif self.state == STATE_STAGE_CLEAR:
            self.update_state_stage_clear()
      elif self.state == STATE_GAME_COMPLETE:
            self.update_state_game_complete()
         
   
   def draw(self):
      for b in self.score_labels:
         b.draw()

      self.harpoon.draw()
      for b in self.bubbles:
         b.draw()
      for b in self.bubble_pops:
         b.draw()

      self.player.draw()

      hud.draw(self.time_secs)

      if self.state == STATE_GET_READY:
         draw_centred_label(32, f"STAGE {self.number + 1}")
         draw_centred_label(56, "GET READY")
      elif self.state == STATE_PAUSED:
         draw_centred_label(56, "PAUSED")
      elif self.state == STATE_TIME_UP:
         draw_centred_label(56, "TIME UP")
      elif self.state == STATE_GAME_OVER:
         draw_centred_label(56, "GAME OVER")
      elif self.state == STATE_STAGE_CLEAR:
         draw_centred_label(32, f"STAGE {self.number + 1} CLEAR")
         draw_centred_label(56, "TIME BONUS")
         draw_centred_label(72, f"{self.time_secs * SCORE_SEC_REMAINING_BONUS}")
      elif self.state == STATE_GAME_COMPLETE:
         draw_centred_label(32, f"GAME COMPLETE")
         draw_centred_label(56, "FINAL SCORE")
         draw_centred_label(72, f"{vars.score:06}")
   
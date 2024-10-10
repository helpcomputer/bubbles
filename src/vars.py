
import pyxel as px
from constants import MAX_SCORE

score = 0
hi_score = 0
lives_remaining = 3
stage_number = 0

move_up = False
move_down = False
move_left = False
move_right = False
pressed_shoot = False
pressed_pause = False

def reset():
   global score, hi_score, lives_remaining, stage_number
   score = 0
   lives_remaining = 3
   stage_number = 0

def update_input():
   global move_up, move_down, move_left, move_right, pressed_shoot, pressed_pause
   move_up = move_down = move_left = move_right = pressed_shoot = pressed_pause = False
   if px.btn(px.KEY_A) or px.btn(px.KEY_LEFT) or px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT):
      move_left = True
   elif px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT) or px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT):
      move_right = True

   if px.btn(px.KEY_W) or px.btn(px.KEY_UP) or px.btn(px.GAMEPAD1_BUTTON_DPAD_UP):
      move_up = True
   elif px.btn(px.KEY_S) or px.btn(px.KEY_DOWN) or px.btn(px.GAMEPAD1_BUTTON_DPAD_DOWN):
      move_down = True

   if px.btnp(px.KEY_SPACE) or px.btnp(px.KEY_B) or px.btnp(px.GAMEPAD1_BUTTON_A):
      pressed_shoot = True

   if px.btnp(px.KEY_P) or px.btnp(px.KEY_PAUSE) or px.btnp(px.GAMEPAD1_BUTTON_START):
      pressed_pause = True

def remove_life():
   global lives_remaining
   lives_remaining = max(0, lives_remaining - 1)

def add_score(add):
   global score, hi_score
   score = min(MAX_SCORE, score + add)
   hi_score = max(hi_score, score)

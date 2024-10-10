
import pyxel as px
from constants import APP_WIDTH, COLLIDE_BOTTOM, BORDER_WIDTH, SOUND_CHANNEL, SND_DIED
import vars

STATE_IDLE = 0
STATE_RUN = 1
STATE_DEAD = 2

MOVE_SPEED = 1.5

FRAMES = {
   STATE_IDLE : ( 0, ),
   STATE_RUN : ( 8, 16, 24, 16, ),
   STATE_DEAD : ( 40, 48 ),
}
FRAME_TIME = 4

class Player:
   def __init__(self, stage):
      self.stage = stage
      self.x = APP_WIDTH // 2 - 4
      self.y = COLLIDE_BOTTOM - 8

      self.state = STATE_IDLE
      self.facing = 1
      self.anim_frame = 0
      self.anim_frame_time = 0
      self.u = 0

   def is_dead(self):
      return self.state == STATE_DEAD

   def kill(self):
      vars.remove_life()
      self.update_state(STATE_DEAD)
      px.play(SOUND_CHANNEL, SND_DIED)

   def animate(self):
      self.anim_frame_time += 1
      if self.anim_frame_time == FRAME_TIME:
         self.anim_frame_time = 0
         self.anim_frame += 1
         if self.anim_frame == len(FRAMES[self.state]):
            self.anim_frame = 0
         self.u = FRAMES[self.state][self.anim_frame]

   def update_state(self, new_state):
      if new_state == self.state:
         if self.state != STATE_IDLE:
            self.animate()
         return
      
      self.state = new_state
      self.anim_frame = 0
      self.anim_frame_time = 0
      self.u = FRAMES[self.state][0]
      if self.state != STATE_RUN:
         self.facing = 1

   def move(self):
      move_x = 0
      if vars.move_left:
         move_x = -1
      elif vars.move_right:
         move_x = 1

      if move_x != 0:
         self.x = max(BORDER_WIDTH, min(APP_WIDTH - BORDER_WIDTH - 8, self.x + move_x * MOVE_SPEED))
         self.update_state(STATE_RUN)
         self.facing = move_x
      else:
         self.update_state(STATE_IDLE)

   def shoot(self):
      if vars.pressed_shoot and not self.stage.harpoon.active:
         self.stage.harpoon.shoot(self.x)
         self.update_state(STATE_IDLE)

   def update(self):
      self.move()
      self.shoot()
   
   def draw(self):
      px.blt(self.x, self.y, 0, self.u, 120, 8 * self.facing, 8, px.COLOR_GREEN)


import pyxel as px
from constants import COLLIDE_BOTTOM, COLLIDE_TOP, APP_HEIGHT, SOUND_CHANNEL, SND_SHOOT

WIDTH = 8
MOVE_SPEED = 2
START_Y = COLLIDE_BOTTOM - 8

class Harpoon:
   def __init__(self, stage):
      self.stage = stage
      self.x = 0
      self.y = START_Y
      self.active = False

   def get_height(self):
      return APP_HEIGHT - (self.y + 8)

   def update(self):
      if not self.active:
         return

      self.y -= MOVE_SPEED
      if self.y <= COLLIDE_TOP:
         self.active = False

   def shoot(self, x):
      self.x = x
      self.y = START_Y
      self.active = True
      px.play(SOUND_CHANNEL, SND_SHOOT)

   def draw(self):
      if not self.active:
         return

      # Draw head
      px.blt(self.x, self.y, 0, 32, 112, 8, 8, px.COLOR_BLACK)

      # Draw chain
      height = self.get_height() - 8
      y = 0
      while y < height:
         if height - y >= 8:
            px.blt(self.x, self.y + 8 + y, 0, 32, 120, 8, 8, px.COLOR_BLACK)
         else:
            px.blt(self.x, self.y + 8 + y, 0, 32, 120, 8, height - y, px.COLOR_BLACK)
         y += 8
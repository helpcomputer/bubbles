
import pyxel as px
from constants import COLLIDE_BOTTOM, COLLIDE_LEFT, COLLIDE_RIGHT, COLLIDE_TOP, BubbleType, SCORE_BUBBLES, SOUND_CHANNEL, SND_POP
from utils import rect_overlap
from bubble_pop import BubblePop
import vars
from score_label import ScoreLabel

DATA = {
   BubbleType.TINY : {
      "size" : 8,
      "u" : 72,
      "max_velocity_y" : 0.9,
   },
   BubbleType.SMALL : {
      "size" : 16,
      "u" : 56,
      "max_velocity_y" : 1.1,
   },
   BubbleType.MEDIUM : {
      "size" : 24,
      "u" : 32,
      "max_velocity_y" : 1.3,
   },
   BubbleType.LARGE : {
      "size" : 32,
      "u" : 0,
      "max_velocity_y" : 1.5,
   },
}

GRAVITY = 0.015
MAX_VELOCITY_X = 0.7
SPLIT_VELOCITY_Y = -0.6

MAX_MULTIPLIER = 8

class Bubble:
   next_x_dir = -1
   multiplier = 1
   last_type_popped = None

   @classmethod
   def reset(cls):
      cls.next_x_dir = -1
      cls.multiplier = 1
      cls.last_type_popped = None

   @classmethod
   def killed_type(cls, stage, x, y, type):
      score = SCORE_BUBBLES[type]
      if type == cls.last_type_popped:
         cls.multiplier = min(MAX_MULTIPLIER, cls.multiplier * 2)
         score *= cls.multiplier
         ScoreLabel(stage, x - 4, y - 3, score)
      else:
         cls.multiplier = 1
         cls.last_type_popped = type
      vars.add_score(score)

   def __init__(self, stage, cen_x, cen_y, type=None, vy=0):
      self.stage = stage
      self.type = type or BubbleType.LARGE

      for k, v in DATA[self.type].items():
         setattr(self, k, v)

      self.x = cen_x - self.size // 2 # left
      self.y = cen_y - self.size // 2 # top

      self.vx = (MAX_VELOCITY_X + self.stage.add_max_velocity_x) * Bubble.next_x_dir
      Bubble.next_x_dir *= -1

      self.vy = min(self.max_velocity_y, max(-self.max_velocity_y, vy))
      self.remove = False

      self.stage.bubbles.append(self)

   def move_x(self):
      self.x += self.vx
      if self.vx > 0:
         if self.x + self.size >= COLLIDE_RIGHT:
            self.x = COLLIDE_RIGHT - self.size
            self.vx = -self.vx
      elif self.vx < 0:
         if self.x <= COLLIDE_LEFT:
            self.x = COLLIDE_LEFT
            self.vx = -self.vx

   def move_y(self):
      self.vy = min(self.max_velocity_y, max(-self.max_velocity_y, self.vy + GRAVITY))
      self.y += self.vy
      if self.vy > 0:
         if self.y + self.size >= COLLIDE_BOTTOM:
            self.y = COLLIDE_BOTTOM - self.size
            self.vy = -self.max_velocity_y
      elif self.vy < 0: # Shouldn't ever reach the top but just in case.
         if self.y <= COLLIDE_TOP:
            self.y = COLLIDE_TOP
            self.vy = 0

   def player_collide_check(self):
      player = self.stage.player
      if player.is_dead():
         return
      
      # Bubbles are circles but rect collisions are accurate enough and favour the player.
      if rect_overlap(player.x + 2, player.y + 2, 4, 6, 
                      self.x + (self.size // 2) - 4, self.y, 8, self.size):
         player.kill()

   def harpoon_collide_check(self):
      harp = self.stage.harpoon
      if not harp.active:
         return
      
      # Bubbles are circles but rect collisions are accurate enough and favour the player.
      if rect_overlap(harp.x, harp.y, 8, harp.get_height(), 
                      self.x, self.y, self.size, self.size):
         self.do_pop()
         Bubble.killed_type(self.stage, self.x + self.size // 2, self.y + self.size // 2, self.type)
         harp.active = False
      
   def do_pop(self):
      px.play(SOUND_CHANNEL, SND_POP)
      self.remove = True
      BubblePop(self.stage, self.x, self.y, self.type)
      if self.type == BubbleType.TINY:
         return
      
      # Split bubble
      next_type = self.type - 1
      cen_x = self.x + self.size // 2
      cen_y = self.y + self.size // 2
      Bubble(self.stage, cen_x, cen_y, next_type, SPLIT_VELOCITY_Y)
      Bubble(self.stage, cen_x, cen_y, next_type, SPLIT_VELOCITY_Y)

   def update(self):
      self.move_x()
      self.move_y()
      self.harpoon_collide_check()
      if not self.remove:
         self.player_collide_check()
   
   def draw(self):
      px.blt(self.x, self.y, 
             0, 
             self.u, 0, 
             self.size, self.size, 
             px.COLOR_BLACK)


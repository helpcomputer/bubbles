
import pyxel as px
from constants import BubbleType

DATA = {
   BubbleType.TINY : {
      "uv_wh" : [99, 32, 16, 13],
      "offset_x" : -4,
      "offset_y" : -2,
   },
   BubbleType.SMALL : {
      "uv_wh" : [79, 32, 20, 22],
      "offset_x" : -2,
      "offset_y" : -3,
   },
   BubbleType.MEDIUM : {
      "uv_wh" : [46, 32, 31, 32],
      "offset_x" : -3,
      "offset_y" : -4,
   },
   BubbleType.LARGE : {
      "uv_wh" : [0, 32, 44, 44],
      "offset_x" : -6,
      "offset_y" : -6,
   },
}

LIFETIME_FRAMES = 5

class BubblePop:
   def __init__(self, stage, bubble_x, bubble_y, bubble_type):
      self.stage = stage
      self.type = bubble_type

      for k, v in DATA[self.type].items():
         setattr(self, k, v)

      self.x = bubble_x + self.offset_x
      self.y = bubble_y + self.offset_y
      self.lifetime = LIFETIME_FRAMES
      self.remove = False

      self.stage.bubble_pops.append(self)

   def update(self):
      self.lifetime -= 1
      if self.lifetime == 0:
         self.remove = True
   
   def draw(self):
      px.blt(self.x, self.y, 0, 
             self.uv_wh[0], 
             self.uv_wh[1], 
             self.uv_wh[2], 
             self.uv_wh[3], 
             px.COLOR_BLACK)


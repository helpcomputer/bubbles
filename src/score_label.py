
import pyxel as px
from utils import get_str_width

LIFETIME = 120 # 2 secs

class ScoreLabel:
   def __init__(self, stage, x, y, score):
      self.stage = stage
      self.x = x
      self.y = y
      self.str = f"{score}"
      self.width = get_str_width(self.str)
      self.lifetime = LIFETIME
      self.remove = False

      self.stage.score_labels.append(self)

   def update(self):
      self.lifetime -= 1
      if self.lifetime == 0:
         self.remove = True

   def draw(self):
      px.rect(self.x, self.y, self.width, px.FONT_HEIGHT, px.COLOR_DARK_BLUE)
      px.text(self.x, self.y, self.str, px.COLOR_YELLOW)

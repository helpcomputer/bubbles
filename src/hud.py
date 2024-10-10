
import pyxel as px
import vars
from utils import text

def draw(time_secs):
   text(5, 5, f"SC:{vars.score:06}", px.COLOR_WHITE)
   text(87, 5, f"HI:{vars.hi_score:06}", px.COLOR_WHITE)
   text(58, 5, f"{time_secs:03}", px.COLOR_WHITE)

   # lives
   for x in range(vars.lives_remaining):
      px.blt(4 + x * 8, 120, 0, 0, 120, 8, 8, px.COLOR_GREEN)

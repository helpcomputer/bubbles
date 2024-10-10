
import pyxel as px
from utils import draw_label
import hud
import vars

OPTION_PLAY = 0
OPTION_EXIT = 1
OPTION_MAX = 2

OPTIONS = {
   OPTION_PLAY : {
      "name" : "PLAY",
   },
   OPTION_EXIT : {
      "name" : "EXIT",
   },
}

OPTIONS_ANCHOR_X = 40
OPTIONS_ANCHOR_Y = 64
OPTIONS_SPACING_Y = 16

class MainMenu:
   def __init__(self, app):
      self.app = app
      self.selected_index = OPTION_PLAY

   def select(self):
      if self.selected_index == OPTION_PLAY:
         self.app.go_to_play()
      elif self.selected_index == OPTION_EXIT:
         self.app.go_to_exit()
   
   def update(self):
      if vars.move_up:
         self.selected_index = max(0, self.selected_index - 1)
      elif vars.move_down:
         self.selected_index = min(OPTION_MAX - 1, self.selected_index + 1)

      if vars.pressed_shoot:
         self.select()
   
   def draw(self):
      # draw title
      y = (px.frame_count * 4 % 360)
      for i in range(7):
         yy = px.cos(y + i * 60) * 8
         px.blt(8 + i * 16, 24 + yy, 0, 
                i * 16, 80, 
                16, 17, 
                px.COLOR_GREEN)

      y = OPTIONS_ANCHOR_Y - 4
      for v in OPTIONS.values():
         draw_label(OPTIONS_ANCHOR_X + 16, y, f"{v['name']}")
         y += 16

      # Draw cursor
      y = OPTIONS_ANCHOR_Y - 4
      x = 4 - ((px.frame_count % 32) // 8)
      px.blt(OPTIONS_ANCHOR_X + x, y + self.selected_index * OPTIONS_SPACING_Y, 0, 0, 112, 8, 8, px.COLOR_BLACK)

      hud.draw(0)

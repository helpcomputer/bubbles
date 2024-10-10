
import pyxel as px

from constants import APP_WIDTH, APP_HEIGHT, MAX_STAGE_NUMBER
from stage import Stage
from main_menu import MainMenu
import vars

STATE_MAIN_MENU = 0
STATE_PLAY = 1

class App:
   def __init__(self):
      px.init(APP_WIDTH, APP_HEIGHT, "Bubbles", fps=60, display_scale=3, capture_scale=1)
      px.load("assets\my_resource.pyxres")

      self.state = STATE_MAIN_MENU
      self.main_menu = MainMenu(self)
      self.stage = None

      px.run(self.update, self.draw)

   def go_to_main_menu(self):
      self.state = STATE_MAIN_MENU

   def go_to_next_stage(self):
      vars.stage_number = min(MAX_STAGE_NUMBER, vars.stage_number + 1)
      self.stage = Stage(self, vars.stage_number)

   def go_to_play(self):
      vars.reset()
      self.state = STATE_PLAY
      self.stage = Stage(self, vars.stage_number)

   def go_to_exit(self):
      px.quit()

   def update(self):
      vars.update_input()

      if self.state == STATE_MAIN_MENU:
         self.main_menu.update()
      elif self.state == STATE_PLAY:
         self.stage.update()
   
   def draw(self):
      # Draw background
      px.bltm(0, 0, 0, 0, 0, 128, 128)

      if self.state == STATE_MAIN_MENU:
         self.main_menu.draw()
      elif self.state == STATE_PLAY:
         self.stage.draw()

if __name__ == "__main__":
   App()

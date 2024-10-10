
import pyxel as px
from constants import APP_WIDTH

def rect_overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and \
            x1 + w1 > x2 and \
            y1 < y2 + h2 and \
            y1 + h1 > y2

def text(x, y, str, col):
    px.text(x + 1, y + 1, str, px.COLOR_BLACK)
    px.text(x, y, str, col)

def draw_label(x, y, str, text_col=px.COLOR_WHITE, bg_col=px.COLOR_PINK):
   str_w = (len(str) * px.FONT_WIDTH)
   px.rect(x - 8 + 1, y + 1, str_w + 16, 8, px.COLOR_DARK_BLUE)
   px.rect(x - 8, y, str_w + 16, 8, bg_col)
   text(x, y + 1, str, text_col)

def draw_centred_label(y, str, text_col=px.COLOR_WHITE, bg_col=px.COLOR_PINK):
   x = (APP_WIDTH // 2) - (get_str_width(str) // 2)
   draw_label(x, y, str, text_col, bg_col)

def get_str_width(str):
    return len(str) * px.FONT_WIDTH
from settings import*
from module.behaviors import*

p.font.init()

class Text(BEHAVIORS):
    def __init__(self, text='', color=BLUE, size=24, x=0, y=0):
        self.text = text
        self.color = color
        self.size = size
        self.rect = p.Rect(x,y,12,12)
        self.image = p.font.SysFont('verdana', self.size).render(self.text, True, self.color)


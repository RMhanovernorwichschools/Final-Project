from ggame import App, RectangleAsset, CircleAsset, Sprite, LineStyle, Color

black = Color(0, 1)
noline = LineStyle(0, black)

class ShooterTest(App):
    def __init__(self):
        super().__init__()
        ShooterTest.listenMouseEvent('click', self.mouseClick)
    
    def mouseClick(self, event):
        char=Char(event.x,event.y)
        
class Char(Sprite):
    asset=RectangleAsset(15,15,noline, black)
    def __init__(self, x,y):
        super().__init__(Char.asset)
        self.x=x
        self.y=y

myapp=ShooterTest()
myapp.run()

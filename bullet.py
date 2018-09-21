from ggame import App, RectangleAsset, CircleAsset, Sprite, LineStyle, Color

black = Color(0, 1)
noline = LineStyle(0, black)

class ShooterTest(App):
    def __init__(self):
        super().__init__()
        char=Char()
        
class Char(Sprite):
    asset=RectangleAsset(15,15,noline, black)
    def __init__(self):
        super().__init__()

myapp=ShooterTest()
ShooterTest.run()

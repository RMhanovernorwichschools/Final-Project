from ggame import App, RectangleAsset, CircleAsset, Sprite, LineStyle, Color

black = Color(0, 1)
noline = LineStyle(0, black)

class ShooterTest(App):
    def __init__(self):
        super().__init__()
        char=Char((0,0))
        
class Char(Sprite):
    asset=RectangleAsset(15,15,noline, black)
    def __init__(self, posititon):
        super().__init__(Char.asset)

myapp=ShooterTest()
ShooterTest.run()

from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame

class Game(App):
    def __init__(self):
        super().__init__()
        m = ImageAsset("Map Base.jpg")
        am=Sprite(m)

myapp=Game()
myapp.run()
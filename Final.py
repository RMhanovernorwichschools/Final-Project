from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame

class Game(App):
    def __init__(self):
        super().__init__()
        m = ImageAsset("images/Map Base.png")
        Sprite(m)

myapp=Game()
myapp.run()
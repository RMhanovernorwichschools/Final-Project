from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame

class Game(App):
    def __init__(self):
        super().__init__()
        m = ImageAsset("Map Base.jpg")
        am=Sprite(m)

myapp=App()

m = ImageAsset("Map Base.jpg")
am=Sprite(m)
am.scale=5

myapp.run()
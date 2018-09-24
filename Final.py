from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame

class Game(App):
    asset = ImageAsset("images/Map Base.png")
     def __init__(self):
        super().__init__(Game.asset)
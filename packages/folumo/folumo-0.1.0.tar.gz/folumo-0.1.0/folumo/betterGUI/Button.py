import sdl2

from folumo.betterGUI import itemBase


class Button(itemBase):
    def __init__(self, screenID: str = "/default/"):
        super().__init__(screenID)

        self.w, self.h = 50, 50
        self.color = (255, 255, 255)

    def _renderObj(self) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, self.w, self.h, 32, sdl2.SDL_PIXELFORMAT_RGBA32)
        print(123)

        if surface:
            sdl2.SDL_FillRect(surface, None, sdl2.SDL_MapRGBA(surface.contents.format, *self.color))

            return surface, (self.x, self.y)
        else:
            print("Failed to create surface:", sdl2.SDL_GetError())
            return None, (0, 0)

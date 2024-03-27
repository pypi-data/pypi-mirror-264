import sdl2
import sdl2.ext
from .screen import data
from PIL import Image
imgCatch = {}


class itemBase:
    def __init__(self, screenID: str = "/default/", getEvent: bool = False):
        self.screenID = screenID
        self.x, self.y = 0, 0

        self.render = False
        self.getEvent = getEvent

        data["root"].addItemToScreen(self.screenID, self)

    def show(self):
        self.render = True

    def hide(self):
        self.render = False

    def update(self) -> None:
        return None

    def _renderObjEvent(self, event: sdl2.SDL_Event = None) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        if event:
            return None, (0, 0)

        return None, (0, 0)

    def renderObjEvent(self, event: sdl2.SDL_Event = None) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        if self.render:
            return self._renderObjEvent(event)

        return None, (0, 0)

    def _renderObj(self) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        return None, (0, 0)

    def renderObj(self) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        if self.render:
            return self._renderObj()

        return None, (0, 0)


class rect(itemBase):
    def __init__(self, screenID: str = "/default/", x: int = 0, y: int = 0, w: int = 50, h: int = 50,
                 color=(255, 255, 255, 255)):
        super().__init__(screenID)
        self.screenID = screenID

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color

    def update(self, screenID: str = None, x: int = None, y: int = None, w: int = None, h: int = None, color=None) -> None:
        if screenID is not None:
            self.screenID = screenID

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if w is not None:
            self.w = w

        if h is not None:
            self.h = h

        if color is not None:
            self.color = color

        return None

    def _renderObj(self) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, self.w, self.h, 32, sdl2.SDL_PIXELFORMAT_RGBA32)

        if surface:
            sdl2.SDL_FillRect(surface, None, sdl2.SDL_MapRGBA(surface.contents.format, *self.color))

            return surface, (self.x, self.y)
        else:
            print("Failed to create surface:", sdl2.SDL_GetError())
            return None, (0, 0)


class image(itemBase):
    def __init__(self, screenID: str = "/default/", imgPath: str = None, x: int = 0, y: int = 0):
        super().__init__(screenID)
        self.imgPath = imgPath
        self.x = x
        self.y = y
        self.LocalImg: sdl2.surface.SDL_Surface | None = None

        if self.imgPath is not None:
            if self.imgPath in imgCatch:
                self.LocalImg = imgCatch[self.imgPath]
            else:
                img = Image.open(self.imgPath)
                self.LocalImg = sdl2.ext.pillow_to_surface(img)
                imgCatch[self.imgPath] = self.LocalImg

    def resize(self, newW: int = 64, newH: int = 64) -> None:
        if self.LocalImg is None:
            return

        tmp_surf = sdl2.SDL_CreateRGBSurface(0, newW, newH, 32, 0, 0, 0, 0)

        _re = sdl2.SDL_Rect(0, 0, newW, newH)
        sdl2.SDL_BlitScaled(self.LocalImg, None, tmp_surf.contents, _re)

        self.LocalImg = tmp_surf

    def _renderObj(self) -> tuple[sdl2.surface.SDL_Surface, tuple[int, int]] | tuple[None, tuple[int, int]]:
        surface = sdl2.SDL_CreateRGBSurface(0, self.LocalImg.w, self.LocalImg.h, 32, 0, 0, 0, 0)

        if surface:
            if self.LocalImg is not None:
                _re = sdl2.SDL_Rect(*(0, 0), surface.contents.w, surface.contents.h)
                sdl2.SDL_BlitSurface(self.LocalImg, None, surface, _re)
            return surface, (self.x, self.y)
        else:
            print("Failed to create surface:", sdl2.SDL_GetError())
            return None, (0, 0)

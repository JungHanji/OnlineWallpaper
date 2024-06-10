from src.downloader.utils import *
from src.downloader.image import *

class Page:
    def __init__(self, url: str, settings: dict) -> None:
        self.category = "none"
        self.url = url
        self.settings = settings

        self.isImagesLoaded: bool = False
        self.prevUrl: str = "none"

        self.defaultResolution = self.settings["default-resolution"]

    def setCategory(self, category: str) -> None:
        if category != "all":
            self.url = self.settings["catalog-url"] + category
        else:
            self.url = self.settings["main-url"] + "all/page1"
        
        self.category: str = category

    def loadImages(self) -> list[Image]:

        if self.prevUrl == self.url and self.isImagesLoaded:
            return self.images
        
        data = request("GET", self.url).text
        out: list[tuple[list[str], str, str, tuple[int, int], tuple[int, int]]] = []
        ref: str = ""

        for line in data.splitlines():
            line = line.strip()

            if 'a class="wallpapers__link"' in line:
                ref: str = line[
                    smartindex(line, 'href="'):
                    smartindex(line, '"', 
                        smartindex(line, 'href="')
                    ) - 1
                ]

            if '<img class="wallpapers__image"' in line:
                prev_ref: str = line[
                    smartindex(line, 'src="'):
                    smartindex(line, '"', 
                        smartindex(line, 'src="')
                    ) - 1
                ]

                tags: str = line[
                    smartindex(line, 'alt="Превью обои '):
                    smartindex(line, '"', 
                        smartindex(line, 'alt="')
                    ) - 1
                ]

                resolution: tuple[int, int] = (0, 0)
                presolution: tuple[int, int] = (0, 0)

                ref = ref[ref.index('/', 1)+1:]
                nref = ref.replace('/', '_')
                
                res = prev_ref[prev_ref.rindex('_')+1:prev_ref.rindex('.')]
                presolution = (int(res[:res.index('x')]), int(res[res.index('x')+1:]))

                if ref == nref:
                    nref += f"_{self.defaultResolution}"
                    resolution = (int(self.defaultResolution[:self.defaultResolution.index('x')]), int(self.defaultResolution[self.defaultResolution.index('x')+1:]))
                else:
                    res = ref.split('/')[-1]
                    resolution = (int(res[:res.index('x')]), int(res[res.index('x')+1:]))

                out.append((tags.split(','), prev_ref, self.settings["download-url"]+nref+'.jpg', resolution, presolution))
        self.images: list[Image] = [Image(i[0], i[1], i[2], i[3], i[4]) for i in out]
        
        self.isImagesLoaded = True
        self.prevUrl = self.url
        return self.images
    
    def getHTMLdata(self) -> str:
        return request("GET", self.url).text
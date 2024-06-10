from src.downloader.utils import *
from src.downloader.page import *

class Site:
    def __init__(self, settings: dict) -> None:
        self.url = settings["main-url"]
        self.pages: list[Page] = []
        self.settings: dict = settings

        self.mainPage = Page("", settings)
        self.mainPage.setCategory("all")
        self.lastQuery = "none"
    
    def getPageBySearch(self, query: str, resolution: str = "none", page: int = 1) -> Page:
        
        if resolution == "none":
            self.lastQuery = f"Query: {query}; Resolution: Default; Asked resolution: None"
            return Page(self.settings["main-url"]+f"search/?order=&page={page}&query={query}", self.settings)

        getxyres = lambda res: (int(res[:res.index('x')]), int(res[res.index('x')+1:]))
        
        xres, yres = getxyres(resolution)
        mxres, myres = xres, yres

        if not resolution in self.settings["resolutions"]:
            closest_res = None
            closest_diff = float('inf')
            for mres in self.settings["resolutions"]:
                tmpx, tmpy = getxyres(mres)
                diff = abs(xres - tmpx) + abs(yres - tmpy)
                if diff < closest_diff or (diff == closest_diff and (tmpx > mxres or tmpy > myres)):
                    closest_diff = diff
                    closest_res = (tmpx, tmpy)
            if closest_res:
                mxres, myres = closest_res
        
        self.lastQuery = f"Query: {query}; Resolution: {mxres}x{myres}; Asked resolution: {resolution}"    
        return Page(self.settings["main-url"]+f"search/?order=&page={page}&query={query}&size={mxres}x{myres}", self.settings)
    
    def getPageByCategory(self, category: str) -> Page:
        tmp = Page("", self.settings)
        tmp.setCategory(category)
        
        return tmp
    
    def getDefaultImages(self) -> list[Image]:
        return self.mainPage.loadImages()
    
    def getCategoryMaxPages(self, category: str) -> int:
        data = self.getPageByCategory(category).getHTMLdata()

        lines = data[
            smartindex(data, '<li class="pager__item pager__item_last-page">'):
            smartindex(data, "</li>",
                smartindex(data, '<li class="pager__item pager__item_last-page">')
            )
        ].splitlines()

        tmp = lines[1][
            smartindex(lines[1], '<a class="pager__link" href="/catalog/'):
            smartindex(lines[1], '"', 
                smartindex(lines[1], '<a class="pager__link" href="/catalog/')
            ) - 1
        ]

        return int(tmp[
            smartindex(tmp, "page"):
        ])
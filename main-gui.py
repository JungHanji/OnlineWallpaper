from colorama import init, Fore
from random import randint
import src.downloader.msite as wpm
import dearpygui.dearpygui as dpg
import json
import os
init()

def registrate_image(image: wpm.Image, tag: int = 0):
    while True:
        try:
            data = image.data("preview")
            break
        except KeyboardInterrupt:
            break
        except:
            print(f"{Fore.RED}[ERROR] Connection error while trying to fetch an image ({image.prev_url})... trting again...{Fore.RESET} (Ctrl + C to stop)")
    
    data = [float(item) / 255 for sublist in data for item in sublist]
    
    with dpg.texture_registry():
        dpg.add_static_texture(
            width=image.preview_resolution[0],
            height=image.preview_resolution[1],
            default_value=data,
            tag=f"prev{tag}"
        )

def registrate_image_file(tag: str, index: int):
    width, height, channels, data = dpg.load_image(f"./assets/wallpapers/preview{index}.jpg")
    with dpg.texture_registry():
        dpg.add_static_texture(
            default_value=data,
            width=width,
            height=height,
            tag=tag
        )

def setwallpaper_callback(sender, keyword, user_data: tuple[wpm.Image, int]):
    print(f"{Fore.BLUE}[WALLPAPER INFO] Setting wallpaper {Fore.RESET}")
    config = json.load(open(f"{os.environ.get('HOME')}/.config/onlineWallpaper/config.json"))
    name = user_data[0].save(f"{config["wallpaperDir"]}/{user_data[0].main_url[user_data[0].main_url.rindex('/')+1:]}")

    with open(config["configPath"], "w") as conf:
        data: str = config["config"]
        data = data.replace("{wallpaperDir}", config["wallpaperDir"])
        data = data.replace("{wallpaperFile}", name)
        conf.write(data)

    print(f"{Fore.BLUE}[WALLPAPER INFO] Setted {name} as main wallpaper in config {Fore.RESET}")

    commands: str = config["permanentSet"]
    for line in commands.splitlines():
        data = line.replace("{wallpaperDir}", config["wallpaperDir"])
        data = data.replace("{wallpaperFile}", name)
        os.system(data)
    
    print(f"{Fore.BLUE}[WALLPAPER INFO] Setted {name} as main wallpaper at monitors {Fore.RESET}")

def img_callback(sender, keyword, user_data: tuple[wpm.Image, int]):
    with dpg.window(label = "Wallpaper view", width=500, height=300):
        dpg.add_text(f"Wallpaper with tags: {', '.join([tag for tag in user_data[0].tags])}")
        dpg.add_text(f"Wallpaper resolution: {user_data[0].resolution[0]}x{user_data[0].resolution[1]}")
        dpg.add_image(texture_tag=f"prev{user_data[1]}")
        dpg.add_button(
            label="Set as main wallpaper",
            callback=setwallpaper_callback,
            user_data=user_data
        )

def reset_settings(sender):
    data = {
        "config": "preload = {wallpaperDir}/{wallpaperFile}\nwallpaper = ,{wallpaperDir}/{wallpaperFile}\nsplash = false",
        "wallpaperDir": f"{os.environ.get('HOME')}/wallpapers",
        "configPath": f"{os.environ.get('HOME')}/.config/hypr/hyprpaper.conf",
        "permanentSet": "hyprctl hyprpaper unload all\nhyprctl hyprpaper preload {wallpaperDir}/{wallpaperFile}\nhyprctl hyprpaper wallpaper \",{wallpaperDir}/{wallpaperFile}\"",
    }

    with open(f"{os.environ.get('HOME')}/.config/onlineWallpaper/config.json", 'w') as file:
        json.dump(data, file)

def settings_callback(sender):
    data = {}
    
    def setall():
        print(f"{Fore.LIGHTGREEN_EX}[INFO] Writing info to config file {Fore.RESET}")
        with open(f"{os.environ.get('HOME')}/.config/onlineWallpaper/config.json", 'w') as file:
            json.dump(data, file)
        
    with dpg.window(label="Settings", width=500, height=300, on_close = setall):
        if not os.path.exists(f"{os.environ.get('HOME')}/.config/onlineWallpaper/config.json"):
            print(f"{Fore.LIGHTGREEN_EX}[INFO] Config file is not found - generating new one {Fore.RESET}")
            os.makedirs(f"{os.environ.get('HOME')}/.config/onlineWallpaper", exist_ok=True)

            config = dpg.add_input_text(
                multiline = True,
                default_value="preload = {wallpaperDir}/{wallpaperFile}\nwallpaper = ,{wallpaperDir}/{wallpaperFile}\nsplash = false",
                label = "Wallpaper config command"
            )

            configPath = dpg.add_input_text(
                default_value=f"{os.environ.get('HOME')}/.config/hypr/hyprpaper.conf",
                label="Default path to config file"
            )

            wallpaperDir = dpg.add_input_text(
                default_value=f"{os.environ.get('HOME')}/wallpapers",
                label = "Default dir to wallpapers"
            )

            permanentSet = dpg.add_input_text(
                multiline=True,
                default_value="hyprctl hyprpaper unload all\nhyprctl hyprpaper preload {wallpaperDir}/{wallpaperFile}\nhyprctl hyprpaper wallpaper \",{wallpaperDir}/{wallpaperFile}\"",
                label = "Commands for permanent set of wallpaper"
            )

            data = {
                "config": dpg.get_value(config),
                "wallpaperDir": dpg.get_value(wallpaperDir),
                "configPath": dpg.get_value(configPath),
                "permanentSet": dpg.get_value(permanentSet)
            }
        else:
            print(f"{Fore.LIGHTGREEN_EX}[INFO] Config file is found. Setting settings to file's values  {Fore.RESET}")
            data = json.load(open(f"{os.environ.get('HOME')}/.config/onlineWallpaper/config.json"))

            config = dpg.add_input_text(
                multiline = True,
                default_value=data["config"],
                label = "Wallpaper config command"
            )

            configPath = dpg.add_input_text(
                default_value=data["configPath"],
                label="Default path to config file"
            )

            wallpaperDir = dpg.add_input_text(
                default_value=data["wallpaperDir"],
                label = "Default dir to wallpapers"
            )

            permanentSet = dpg.add_input_text(
                multiline=True,
                default_value=data["permanentSet"],
                label = "Commands for permanent set of wallpaper"
            )

def load_font():
    big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
    big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
    remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
    alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
    with dpg.font_registry():
        with dpg.font("./assets/fonts/MagnetTrial-Light.ttf", 13) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
            for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
                dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
                dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
                biglet += 1  # choose next letter
            dpg.bind_font(default_font)

def search_callback(sender, keyword, user_data: (None | int), is_init_page: (bool) = False):
    npage = 1 if user_data == None else user_data

    print(f"{Fore.CYAN}[SEARCH] Searching images by text '{dpg.get_value('search')}', and page: {npage} (resolution: {mainResolution}) {Fore.RESET}")
    if not is_init_page: 
        page = site.getPageBySearch(dpg.get_value('search'), mainResolution, npage)
    else:
        page = wpm.Page(site.settings["main-url"] + f"all/page{npage}", site.settings)
    imgs: list[wpm.Image] = page.loadImages()
    print(f"{Fore.CYAN}[SEARCH] Serached images ({len(imgs)}) by {site.lastQuery} {Fore.RESET}")
    regimgs = registrate_images(imgs)
    print(f"{Fore.CYAN}[SEARCH] Registrated new images, showing page {Fore.RESET}")

    show_page(regimgs, npage, page.getMaxPagesCurrCat())

def page_decr(sender, keyword, user_data: tuple[int, int, bool]):
    page = user_data[0]
    if page >= 1:
        page -= 1
    search_callback(0, 0, page, user_data[2])
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Page decrimented {Fore.RESET}")

def page_incr(sender, keyword, user_data: tuple[int, int, bool]):
    page = user_data[0]
    if page < user_data[1]:
        page += 1
    search_callback(0, 0, page, user_data[2])
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Page incremented {Fore.RESET}")

def page_max(sender, keyword, user_data: tuple[int, int, bool]):
    search_callback(0, 0, user_data[1], user_data[2])
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Page setted to max page {Fore.RESET}")

def page_min(sender, keyword, user_data: tuple[int, int, bool]):
    search_callback(0, 0, user_data[1], user_data[2])
    print(f"{Fore.LIGHTGREEN_EX}[INFO] Page setted to min page {Fore.RESET}")

def show_page(regimgs: list[tuple[wpm.Image, int]], currentPage: int, maxPages: int):
    print(f"{Fore.YELLOW}[PAGE] Entered page, current page num: {currentPage}, maximum: {maxPages} {Fore.RESET}")
    if dpg.does_item_exist("$imgsTable"):
        dpg.delete_item("$imgsTable")

    if dpg.does_item_exist("$scrollTable"):
        dpg.delete_item("$scrollTable")

    # Удаление контейнера таблицы, если он существует
    if dpg.does_item_exist("$imgsTableContainer"):
        dpg.delete_item("$imgsTableContainer")
    print(f"{Fore.YELLOW}[PAGE] Deleted all tables {Fore.RESET}")
    # Пересоздание контейнера и таблицы внутри окна
    if dpg.does_item_exist("$mainWindow"):
        with dpg.child_window(parent="$mainWindow", tag="$imgsTableContainer"):
            with dpg.table(tag="$imgsTable", header_row=False):
                columns, rows = 3, len(regimgs) // 3 + (len(regimgs) % 3 > 0)
                [dpg.add_table_column() for _ in range(columns)]

                index = 0
                for i in range(rows):
                    with dpg.table_row():
                        for j in range(columns):
                            if index < len(regimgs):
                                img = regimgs[index][0]
                                dpg.add_image_button(
                                    texture_tag=f'prev{regimgs[index][1]}',
                                    label=', '.join(img.tags),
                                    callback=img_callback,
                                    user_data=regimgs[index],
                                    tag=f"imgbuttonprev{regimgs[index][1]}"
                                )
                                index += 1
                print(f"{Fore.YELLOW}[PAGE] showed all button-images {Fore.RESET}")

            with dpg.table(tag="$scrollTable", header_row=False):
                [dpg.add_table_column() for i in range(5)]
                with dpg.table_row():
                    dpg.add_button(label="1", user_data=(currentPage, maxPages, False), callback=page_min)
                    dpg.add_button(label="<-", user_data=(currentPage, maxPages, False), callback=page_decr)
                    dpg.add_text(default_value=f"{currentPage}")
                    dpg.add_button(label="->", user_data=(currentPage, maxPages, False), callback=page_incr)
                    dpg.add_button(label=f"{maxPages}", user_data=(currentPage, maxPages, False), callback=page_max)

def first_page(regimgs: list[tuple[wpm.Image, int]], currentPage: int, maxPages: int):
    with dpg.window(tag="$mainWindow"):
        with dpg.menu_bar():
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label = "Edit...", callback=settings_callback)
                dpg.add_menu_item(label="Reset to defaults", callback=reset_settings)
        
        dpg.add_combo(settings["resolutions"], label = "Choose resolution", default_value=settings["default-resolution"], callback=resolution_callback)

        dpg.add_input_text(hint = "Enter search text", tag="search")
        dpg.add_button(label="Search", callback=search_callback)
        
        with dpg.table(tag="$imgsTable", header_row=False):
            columns, rows = 3, len(regimgs) // 3 + (len(regimgs) % 3 > 0)
            [dpg.add_table_column() for _ in range(columns)]

            index = 0
            for i in range(rows):
                with dpg.table_row():
                    for j in range(columns):
                        if index < len(regimgs):
                            img = regimgs[index][0]
                            dpg.add_image_button(
                                texture_tag=f'prev{regimgs[index][1]}',
                                label=', '.join(img.tags),
                                callback=img_callback,
                                user_data=regimgs[index],
                                tag=f"imgbuttonprev{regimgs[index][1]}"
                            )
                            index += 1

        with dpg.table(tag="$scrollTable", header_row=False):
            [dpg.add_table_column() for i in range(5)]
            with dpg.table_row():
                dpg.add_button(label="1", user_data=(currentPage, maxPages, True), callback=page_min)
                dpg.add_button(label="<-", user_data=(currentPage, maxPages, True), callback=page_decr)
                dpg.add_text(default_value=f"{currentPage}")
                dpg.add_button(label="->", user_data=(currentPage, maxPages, True), callback=page_incr)
                dpg.add_button(label=f"{maxPages}", user_data=(currentPage, maxPages, True), callback=page_max)

def registrate_images(imgs: list[wpm.Image]) -> list[tuple[wpm.Image, int]]:
    unique_int: int = randint(0, 100000000)
    regimgs: list[tuple[wpm.Image, int]] = [(img, unique_int + i) for i, img in enumerate(imgs)]

    for tp in regimgs:
        registrate_image(tp[0], tp[1])
    
    return regimgs

def resolution_callback(sender, keyword, user_data):
    global mainResolution
    mainResolution = keyword        
        

if __name__ == '__main__':
    
    
    settings = wpm.load(open(f"{os.environ.get('HOME')}/.config/onlineWallpaper/settings.json"))
    # settings = wpm.load(open("./assets/settings.json"))
    mainResolution = settings["default-resolution"]

    site = wpm.Site(settings)
    dpg.create_context()
    load_font()        

    print(f"{Fore.GREEN}[INIT] Getting default images {Fore.RESET}")
    regimgs = registrate_images(site.getDefaultImages())
    print(f"{Fore.GREEN}[INIT] Registrated default images ({len(regimgs)}) {Fore.RESET}")
    first_page(regimgs, 1, site.mainPage.getMaxPagesCurrCat())
    print(f"{Fore.LIGHTGREEN_EX}[INFO] First page displayed {Fore.RESET}")

    dpg.create_viewport(title='Online wallpapers', clear_color = [200, 200, 200, 255])
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("$mainWindow", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
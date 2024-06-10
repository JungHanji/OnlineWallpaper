from uu import encode
import dearpygui.dearpygui as dpg
import src.downloader.msite as wpm
import dearpygui.demo as demo
default_font: (int | str) = 0

def registrate_image(image: wpm.Image, tag: int = 0):
    data = image.data("preview")
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
    print(f"Setting {user_data[0].main_url} as main wallpaper...")

def img_callback(sender, keyword, user_data: tuple[wpm.Image, int]):
    strr = ""
    with open("file.txt", 'w', encoding="utf-8") as f:
        f.write(f"Wallpaper with tags: {', '.join([tag for tag in user_data[0].tags])}")
    with open("file.txt", 'r', encoding="utf-8") as f:
        strr = f.read()

    with dpg.window(label = "Wallpaper view", width=500, height=300):
        dpg.add_text(strr)
        dpg.add_text(f"Wallpaper resolution: {user_data[0].resolution[0]}x{user_data[0].resolution[1]}")
        dpg.add_image(texture_tag=f"prev{user_data[1]}")
        dpg.add_button(
            label="Set as main wallpaper",
            callback=setwallpaper_callback,
            user_data=user_data
        )

def search_callback(sender, keyword, user_data):
    print(f"Search: {dpg.get_value("search")}")

if __name__ == '__main__':
    
    settings = wpm.load(open("./assets/settings.json"))
    site = wpm.Site(settings)
    imgs: list[wpm.Image] = site.getDefaultImages()
    regimgs: list[tuple[wpm.Image, int]] = [(img, i) for i, img in enumerate(imgs)]

    dpg.create_context()

    big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
    big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
    small_let_end = 0x00FF  # small "я" in cyrillic alphabet
    remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
    alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
    alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped
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

    for tp in regimgs:
        registrate_image(tp[0], tp[1])
        
    with dpg.window(tag="$mainWindow"):
        dpg.add_input_text(hint = "Enter search text", tag="search")
        dpg.add_button(label="Search", callback=search_callback)

        with dpg.table(header_row=False):
            columns, rows = 3, len(regimgs) // 3
            [dpg.add_table_column() for i in range(columns)]

            index: int = 0
            for i in range(0, rows):
                with dpg.table_row():
                    for j in range(0, columns):
                        img = regimgs[index][0]
                        dpg.add_image_button(
                            texture_tag = f'prev{regimgs[index][1]}',
                            label = ', '.join(img.tags),
                            callback = img_callback,
                            user_data = regimgs[index]
                        )
                        index += 1

    dpg.create_viewport(
        title='Online wallpapers',
        clear_color = [200, 200, 200, 255]
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # demo.show_demo()
    # dpg.show_font_manager()
    dpg.set_primary_window("$mainWindow", True)
    dpg.start_dearpygui()
    
    dpg.destroy_context()
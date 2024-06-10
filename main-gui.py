import dearpygui.dearpygui as dpg
import src.downloader.msite as wpm

def registrate_image(image: wpm.Image, tag: int = 0):
    data = image.data("preview")
    
    # Flatten the list of tuples
    data = [item for sublist in data for item in sublist]
    
    # Ensure data is a list of floats
    if not all(isinstance(i, float) for i in data):
        data = [float(i) for i in data]
    
    # Normalize data if necessary
    max_value = max(data)
    if max_value > 1.0:
        data = [i / max_value for i in data]

    with dpg.texture_registry():
        dpg.add_raw_texture(
            width=image.resolution[0],
            height=image.resolution[1],
            default_value=data,
            tag=tag,
            format=dpg.mvFormat_Float_rgb
        )

def img_callback(sender, keyword, user_data):
    print(sender, keyword, user_data)

def search_callback(sender, keyword, user_data):
    print(f"Search: {dpg.get_value("search")}")


if __name__ == '__main__':
    
    settings = wpm.load(open("./assets/settings.json"))
    site = wpm.Site(settings)
    imgs: list[wpm.Image] = site.getDefaultImages()
    regimgs: list[tuple[wpm.Image, int]] = [(img, i) for i, img in enumerate(imgs)]

    dpg.create_context()

    print("registration...")

    for tp in regimgs:
        print(f"-> {tp[1]+1}/{len(regimgs)} registration: {tp[0].prev_url}")
        registrate_image(tp[0], tp[1])

    print("registrated...")

    with dpg.window(tag="Primary Window"):
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
                        index += 1
                        dpg.add_image_button(
                            texture_tag = index,
                            label = ', '.join(img.tags),
                            callback = img_callback,
                            user_data = img
                        )

    dpg.create_viewport(
        title='Online wallpapers', 
        width=600, 
        height=600, 
        clear_color = [200, 200, 200, 255]
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
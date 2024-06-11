import dearpygui.demo as demo
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Online wallpapers', clear_color = [200, 200, 200, 255])
dpg.setup_dearpygui()
dpg.show_viewport()
demo.show_demo()
dpg.start_dearpygui()
dpg.destroy_context()
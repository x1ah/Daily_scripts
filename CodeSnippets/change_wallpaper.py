#!/usr/bin/env python
# encoding: utf-8

import os
import random

WALLPAPER_PATH = "/home/x1ah/Pictures/desktop_pictures/"
WALLPAPER_SET_COMMAND = ("gsettings set org.gnome.desktop.background "
                         "picture-uri {pic_path}")


def random_picture(path):
    """
    :path: wallpaper picture's absolute path
    return random picture's absolute path of the wallpaper path.
    """
    all_pics = os.listdir(path)
    pic = random.choice(all_pics)
    pic_abspath = os.path.join(path, pic)
    return pic_abspath

change_wallpaper = lambda pic_path: os.system(
    WALLPAPER_SET_COMMAND.format(pic_path=pic_path)
)


def run():
    pic_path = random_picture(WALLPAPER_PATH)
    change_wallpaper(pic_path)

if __name__ == "__main__":
    run()

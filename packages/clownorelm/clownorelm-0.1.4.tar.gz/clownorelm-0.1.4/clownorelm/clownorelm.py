import os
from ascii_magic import AsciiArt
from importlib import resources as il_resources

def register():
    with il_resources.as_file(il_resources.files('clownorelm') / 'resources' / 'mellow_corn_label.jpeg') as img_path:
        my_art = AsciiArt.from_image(img_path)
        my_art.to_terminal(columns=130)

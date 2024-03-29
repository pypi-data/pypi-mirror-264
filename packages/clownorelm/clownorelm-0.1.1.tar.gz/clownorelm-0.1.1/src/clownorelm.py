import os
from ascii_magic import AsciiArt
import pkg_resources

def register():
    img_path = 'resources/mellow_corn_label.jpeg'  # always use slash
    img_file = pkg_resources.resource_filename(__name__, img_path)

    my_art = AsciiArt.from_image(img_file)
    my_art.to_terminal(columns=130)

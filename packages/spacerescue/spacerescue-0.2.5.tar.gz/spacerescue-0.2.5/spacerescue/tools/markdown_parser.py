import os
import re

from spacerescue.resources import SCENE_RESOURCES


class MarkdownParser:

    def __init__(self, columns: int, font_size: int):
        self.columns = columns
        self.font_size = font_size

    def parse_string(self, text: str) -> list[str]:
        buffer = []
        line = ""
        for word in re.split(r"[^\S\r\n]+|\n", text):
            if word == "":
                buffer.append(line)
                buffer.append("")
                line = ""
            elif word == "*":
                buffer.append(line)
                line = word.replace("_", " ") + " "
            elif word.startswith("!"):
                caption, image_path = MarkdownParser.accept_image(word)
                self._load_image(caption, image_path, buffer)
            elif len(line + " " + word) >= self.columns:
                buffer.append(line)
                line = word + " "
            else:
                line += word + " "
        buffer.append(line)
        return buffer

    @staticmethod
    def accept_image(word: str):
        m = re.match(r"!\[(.+)\]\((.+)\)", word)
        assert m is not None
        return m.group(1), m.group(2)

    def _load_image(self, caption: str, image_path: str, buffer):

        # If image not found, replace by the caption

        if not os.path.exists(image_path):
            buffer.append(caption)
            return

        texture = SCENE_RESOURCES.load_texture_from_path(image_path)

        # Add place hoder for the image in the text

        buffer.append(f"![{caption}]({image_path})")
        for i in range(1, texture.height // self.font_size):
            buffer.append("")

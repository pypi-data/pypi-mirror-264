import pyray as pr

from spacerescue.resources import SCENE_RESOURCES
from spacerescue.render.widget import Widget
from spacerescue.core.math import clamp
from spacerescue.tools.markdown_parser import MarkdownParser


class MarkdownBox(Widget):

    FONT_SPACING = 2
    FONT_SIZE = 28
    FONT_CHAR_WIDTH = (FONT_SIZE + FONT_SPACING) / 2
    FONT_COLOR = pr.Color(255, 255, 255, 255)
    FOOTER_SIZE = FONT_SIZE + FONT_SPACING
    BG_COLOR = pr.Color(64, 191, 182, 192)
    SCANLINE_COLOR = pr.Color(255, 255, 255, 96)

    def __init__(
        self,
        id: str,
        position: pr.Vector2,
        size: pr.Vector2,
        buffers: list[str],
        caption: str = "",
        first_buffer: int = 0,
        border_size: int = 10,
    ):
        super().__init__(id, self._get_inner_bound(position, size))
        self.caption = caption
        self.buffers = [
            MarkdownParser(self.size_in_chars.x, MarkdownBox.FONT_SIZE).parse_string(b)
            for b in buffers
        ]
        self.buffer_text = self.buffers[first_buffer]
        self.buffer_line = 0
        self.border_size = border_size

        self.scanline = SCENE_RESOURCES.load_texture("scanline")
        pr.set_texture_wrap(self.scanline, pr.TextureWrap.TEXTURE_WRAP_REPEAT)
        self.font = SCENE_RESOURCES.load_font("mono_font28")

    def update(self):
        pos = pr.get_mouse_position()
        if pr.check_collision_point_rec(pos, self.bound):
            for i in range(0, 10):
                if pr.is_key_pressed(pr.KeyboardKey.KEY_F1 + i) and i < len(
                    self.buffers
                ):
                    self.buffer_text = self.buffers[i]
                    self.buffer_line = 0

            if (
                pr.is_key_pressed(pr.KeyboardKey.KEY_UP)
                or pr.get_mouse_wheel_move() > 0
            ):
                self.buffer_line = clamp(
                    self.buffer_line - 1,
                    0,
                    len(self.buffer_text) - self.size_in_chars.y - 1,
                )

            if (
                pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN)
                or pr.get_mouse_wheel_move() < 0
            ):
                self.buffer_line = clamp(
                    self.buffer_line + 1,
                    0,
                    len(self.buffer_text) - self.size_in_chars.y - 1,
                )

    def draw(self):
        outer_bound = self._get_outer_bound()

        pr.draw_rectangle_rec(outer_bound, MarkdownBox.BG_COLOR)
        
        pr.begin_scissor_mode(
            int(self.bound.x),
            int(self.bound.y),
            int(self.bound.width),
            int(self.bound.height),
        )
        for i in range(-int(self.size_in_chars.y), int(self.size_in_chars.y)):
            j = int(self.buffer_line + i)
            if 0 <= j < len(self.buffer_text):
                pos = pr.Vector2(
                    self.bound.x,
                    self.bound.y + i * MarkdownBox.FONT_SIZE,
                )
                text = self.buffer_text[j]
                if text.startswith("!"):
                    _, image_path = MarkdownParser.accept_image(text)
                    self._draw_image(image_path, pos)
                else:
                    pr.draw_text_ex(
                        self.font,
                        text,
                        pos,
                        MarkdownBox.FONT_SIZE,
                        MarkdownBox.FONT_SPACING,
                        MarkdownBox.FONT_COLOR,
                    )
        pr.end_scissor_mode()

        pr.draw_text_ex(
            self.font,
            self.caption,
            pr.Vector2(
                self.bound.x,
                self.bound.y + self.bound.height + MarkdownBox.FONT_SPACING,
            ),
            MarkdownBox.FONT_SIZE,
            MarkdownBox.FONT_SPACING,
            MarkdownBox.FONT_COLOR,
        )

        pr.draw_texture_pro(
            self.scanline,
            pr.Rectangle(0, 0, outer_bound.width, outer_bound.height),
            outer_bound,
            pr.vector2_zero(),
            0.0,
            MarkdownBox.SCANLINE_COLOR,
        )

    def _get_inner_bound(self, position: pr.Vector2, size: pr.Vector2) -> pr.Rectangle:
        self.size_in_chars = pr.Vector2(
            size.x // MarkdownBox.FONT_CHAR_WIDTH,
            size.y // MarkdownBox.FONT_SIZE,
        )
        return pr.Rectangle(position.x, position.y, size.x, size.y)

    def _get_outer_bound(self) -> pr.Rectangle:
        if len(self.caption) > 0:
            return pr.Rectangle(
                int(self.bound.x - self.border_size),
                int(self.bound.y - self.border_size),
                int(self.bound.width + self.border_size * 2),
                int(self.bound.height + self.border_size * 2 + MarkdownBox.FOOTER_SIZE),
            )
        else:
            return pr.Rectangle(
                int(self.bound.x - self.border_size),
                int(self.bound.y - self.border_size),
                int(self.bound.width + self.border_size * 2),
                int(self.bound.height + self.border_size * 2),
            )

    def _draw_image(self, image_path: str, pos: pr.Vector2):
        texture = SCENE_RESOURCES.load_texture_from_path(image_path)
        pr.draw_texture_pro(
            texture,
            pr.Rectangle(
                0,
                0,
                texture.width,
                texture.height,
            ),
            pr.Rectangle(
                int(pos.x),
                int(pos.y),
                texture.width,
                texture.height,
            ),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,  # type: ignore
        )

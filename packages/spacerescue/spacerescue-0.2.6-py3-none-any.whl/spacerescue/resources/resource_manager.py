from __future__ import annotations
from functools import cache

import pyray as pr

from spacerescue import resources
from spacerescue.tools.util import (
    load_lines,
    load_res_lines,
    load_res_yaml,
    load_yaml,
    wait_while_true,
)


class CacheEntry:

    def __init__(self, type, value):
        self.type = type
        self.value = value


class ResourceManager:

    PATHS = load_res_yaml(resources, "resource_manager.yml")

    @cache
    @staticmethod
    def get_instance(name: str = "singleton") -> ResourceManager:
        return ResourceManager()

    def __init__(self):
        self.cache: dict[str, CacheEntry] = {}

    def unload_all(self):
        for entry in self.cache.values():
            if entry.type == "music":
                pr.unload_music_stream(entry.value)
            elif entry.type == "sound":
                wait_while_true(lambda: pr.is_sound_playing(entry.value))
                pr.unload_sound(entry.value)
            elif entry.type == "font":
                pr.unload_font(entry.value)
            elif entry.type == "image":
                pr.unload_image(entry.value)
            elif entry.type == "texture":
                pr.unload_texture(entry.value)
            elif entry.type == "model":
                pr.unload_model(entry.value)
            elif entry.type == "shader":
                pr.unload_shader(entry.value)
        self.cache = {}

    def load_yaml(self, name: str):
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("yaml", load_yaml(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "yaml"
        return entry.value

    def load_res_yaml(self, name: str):
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry(
                "yaml", load_res_yaml(resources, *ResourceManager.PATHS[name])
            )
            self.cache[name] = entry
        assert entry.type == "yaml"
        return entry.value

    def load_lines(self, name: str) -> list[str]:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("lines", load_lines(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "lines"
        return entry.value

    def load_res_lines(self, name: str) -> list[str]:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry(
                "lines", load_res_lines(resources, *ResourceManager.PATHS[name])
            )
            self.cache[name] = entry
        assert entry.type == "lines"
        return entry.value

    def load_music(self, name: str) -> pr.Music:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry(
                "music", pr.load_music_stream(*ResourceManager.PATHS[name])
            )
            self.cache[name] = entry
        assert entry.type == "music"
        return entry.value

    def load_sound(self, name: str) -> pr.Sound:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("sound", pr.load_sound(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "sound"
        return entry.value

    def load_font(self, name: str) -> pr.Font:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("font", pr.load_font_ex(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "font"
        return entry.value
    
    def load_image(self, name: str) -> pr.Image:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("image", pr.load_image(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "image"
        return entry.value

    def load_texture(self, name: str) -> pr.Texture:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("texture", pr.load_texture(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "texture"
        return entry.value

    def load_texture_from_path(self, path: str) -> pr.Texture:
        entry = self.cache.get(path)
        if entry is None:
            entry = CacheEntry("texture", pr.load_texture(path))
            self.cache[path] = entry
        assert entry.type == "texture"
        return entry.value

    def load_model(self, name: str) -> pr.Model:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("model", pr.load_model(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "model"
        return entry.value

    def load_shader(self, name: str) -> pr.Shader:
        entry = self.cache.get(name)
        if entry is None:
            entry = CacheEntry("shader", pr.load_shader(*ResourceManager.PATHS[name]))
            self.cache[name] = entry
        assert entry.type == "shader"
        return entry.value

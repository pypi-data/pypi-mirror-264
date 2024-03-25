import logging
import pyray as pr

from spacerescue.tools.simple_allocator import SimpleAllocator

MAX_LIGHTS = 4
LIGHT_DIRECTIONAL = 0
LIGHT_POINT = 1

LIGHT_LOC_ENABLED = 0
LIGHT_LOC_TYPE = 1
LIGHT_LOC_POSITION = 2
LIGHT_LOC_TARGET = 3
LIGHT_LOC_COLOR = 4

_light_allocator = SimpleAllocator(MAX_LIGHTS)


class Light:
    """struct"""

    def __init__(
        self,
        handle: int,
        type: int,
        position: pr.Vector3,
        target: pr.Vector3,
        color: pr.Color,
        shader
    ):
        self.handle = handle
        self.enabled = True
        self.type = type
        self.position = position
        self.target = target
        self.color = color
        self.locs = [0] * 5
        self.shader = shader


def create_light(
    type: int,
    position: pr.Vector3,
    target: pr.Vector3,
    color: pr.Color,
    shader: pr.Shader,
) -> Light:
    
    h = _light_allocator.alloc()
    light = Light(h, type, position, target, color, shader)
    light.locs[LIGHT_LOC_ENABLED] = pr.get_shader_location(
        shader, f"lights[{h}].enabled"
    )
    light.locs[LIGHT_LOC_TYPE] = pr.get_shader_location(shader, f"lights[{h}].type")
    light.locs[LIGHT_LOC_POSITION] = pr.get_shader_location(
        shader, f"lights[{h}].position"
    )
    light.locs[LIGHT_LOC_TARGET] = pr.get_shader_location(shader, f"lights[{h}].target")
    light.locs[LIGHT_LOC_COLOR] = pr.get_shader_location(shader, f"lights[{h}].color")
    light_update_values(light)
    logging.info(f"INFO: LIGHT: [ID {h}] Light created successfully")
    return light


def delete_light(light: Light):
    _light_allocator.free(light.handle)
    logging.info(f"INFO: LIGHT: [ID {light.handle}] Light deleted successfully")


def light_update_values(light: Light):
    pr.set_shader_value(
        light.shader,
        light.locs[LIGHT_LOC_ENABLED],
        1 if light.enabled else 0,
        pr.ShaderUniformDataType.SHADER_UNIFORM_INT,
    )
    pr.set_shader_value(
        light.shader,
        light.locs[LIGHT_LOC_TYPE],
        light.type,
        pr.ShaderUniformDataType.SHADER_UNIFORM_INT,
    )
    pr.set_shader_value(
        light.shader,
        light.locs[LIGHT_LOC_POSITION],
        light.position,
        pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3,
    )
    pr.set_shader_value(
        light.shader,
        light.locs[LIGHT_LOC_TARGET],
        light.target,
        pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3,
    )
    pr.set_shader_value(
        light.shader,
        light.locs[LIGHT_LOC_COLOR],
        pr.color_normalize(light.color),
        pr.ShaderUniformDataType.SHADER_UNIFORM_VEC4,
    )

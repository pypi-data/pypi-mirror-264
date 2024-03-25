import pyray as pr


REQUEST_FOR_EXIT = False


def window_request_close():
    global REQUEST_FOR_EXIT
    REQUEST_FOR_EXIT = True


def window_should_close():
    global REQUEST_FOR_EXIT
    return REQUEST_FOR_EXIT or pr.window_should_close()


def is_skip_key():
    return pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE) or pr.is_mouse_button_pressed(
        pr.MouseButton.MOUSE_BUTTON_LEFT
    )

import pyray as pr

from spacerescue.resources import (
    GLOBAL_RESOURCES,
    SCENE_RESOURCES,
    STRING_BACK,
    STRING_LEARNING_FAILURE,
    STRING_LEARNING_SUCCESS,
    STRING_TRAINING,
    STRING_TRAINING_SUCCESS,
)
from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.gameplay.challenge import CodeChallenge
from spacerescue.gameplay.game_scene import (
    GameScene,
    GameSceneEnd,
    GameSceneNext,
    GameSceneResult,
    GameSubScene,
)
from spacerescue.gameplay.scenes.computer_console import ComputerConsole
from spacerescue.physic.simulation.drone import Drone
from spacerescue.physic.simulation.world import World
from spacerescue.render.animators.open_horizontal import OpenHorizontal
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.widgets.button import Button
from spacerescue.render.widgets.markdown_box import MarkdownBox
from spacerescue.render.widgets.message_box import MessageBox
from spacerescue.render.widgets.progress_box import ProgressBox
from spacerescue.render.widgets.screen import Screen


class SimulatorConsole(ComputerConsole):
    def update(self) -> GameSceneResult:
        if self.state == 4:
            self.state = 0
            return GameSceneNext(SimulatorBench(self, self.challenge).enter())
        else:
            return super().update()


class SimulatorBench(GameSubScene):

    SIMULATION_SPEED = 1
    BORDER_SIZE = 55
    DISTANCE_WIN = 214

    def __init__(self, scene: GameScene, challenge: CodeChallenge):
        super().__init__(scene)
        self.challenge = challenge
        self.brain = self.challenge.get_answer()

    def enter(self):
        super().enter()
        pr.stop_music_stream(GLOBAL_RESOURCES.load_music("music"))
        self._build_ui()
        self.state = 0

    def update_simulation(self, dt: float, training: bool):
        for i in range(SimulatorBench.SIMULATION_SPEED):
            dt = 1/10
            self.world.update(dt)
            for drone in self.drones:
                if self.world.check_collision(drone):
                    self.destroyed_drones.append(drone)
                    self.drones.remove(drone)
                drone.update(dt, training)

    def update_training_results(self):
        if len(self.drones) == 0:
            self._reboot_simulation(True)
            self.state = 1
        elif self.world.score >= 214:
            self._notify_training_success()
            self.state = 4

    def update_learning_results(self):
        if len(self.drones) == 0:
            self._notify_learning_failure()
            self.state = 4
        elif self.world.score >= 214:
            self._notify_learning_success()
            self.state = 4

    def update_input(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_ADD):
            SimulatorBench.SIMULATION_SPEED = min(
                SimulatorBench.SIMULATION_SPEED + 1, 10
            )
        if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_SUBTRACT):
            SimulatorBench.SIMULATION_SPEED = max(
                SimulatorBench.SIMULATION_SPEED - 1, 1
            )

    def update(self):
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self._boot_simulation(True)
                    self.state = 1

            case 1:
                dt = pr.get_frame_time()
                self.update_simulation(dt, True)
                self.update_training_results()
                self.update_input()
                for button in self.buttons:
                    button.update()

            case 2:
                dt = pr.get_frame_time()
                self.update_simulation(dt, False)
                self.update_learning_results()
                self.update_input()
                for button in self.buttons:
                    button.update()

            case 4:
                if self.message_box is not None:
                    self.message_box.update()
                else:
                    self._reboot_simulation(True)
                    self.state = 1

            case 5:
                return GameSceneEnd(self.scene)

            case 6:
                self.leave()
                return GameSceneEnd(self.scene)

        return super().update()

    def draw_simulation(self):
        bound = pr.Rectangle(
            int(self.world.bound.x - SimulatorConsole.BORDER_SIZE),
            int(self.world.bound.y - SimulatorConsole.BORDER_SIZE),
            int(self.world.bound.width + SimulatorConsole.BORDER_SIZE * 2),
            int(self.world.bound.height + SimulatorConsole.BORDER_SIZE * 2),
        )

        pr.begin_scissor_mode(
            int(self.world.bound.x),
            int(self.world.bound.y),
            int(self.world.bound.width),
            int(self.world.bound.height),
        )
        self.world.draw()
        for drone in self.drones:
            drone.draw()
        pr.end_scissor_mode()

        mode = STRING_TRAINING if self.state == 1 else ""
        pr.draw_text(
            f"[+/-]: x{SimulatorBench.SIMULATION_SPEED}\t{mode}",
            int(self.world.bound.x + 5),
            int(self.world.bound.y + self.world.bound.height - 25),
            20,
            pr.WHITE,  # type: ignore
        )

        pr.draw_texture_pro(
            self.scanline,
            pr.Rectangle(0, 0, bound.width, bound.height),
            bound,
            pr.vector2_zero(),
            0.0,
            pr.WHITE,  # type: ignore
        )

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(MarkdownBox.BG_COLOR)
        if self.state >= 1:
            self.draw_simulation()
        self.screen.draw()
        if self.state >= 1:
            for button in self.buttons:
                button.draw()
        if self.state == 4 and self.message_box is not None:
            self.message_box.draw()
        if self.state == 0:
            self.fade_in.draw()
        pr.end_drawing()

    def _build_ui(self):
        self.scanline = SCENE_RESOURCES.load_texture("scanline")
        self.fade_in = FadeScr(0.5)
        self.screen = Screen("widget", "console")
        self.message_box = None
        self.buttons = [
            Button(
                "button_back",
                pr.Vector2(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 45),
                pr.Vector2(200, 38),
                STRING_BACK,
                Button.RED,
                self._button_is_clicked,
            ),
        ]

    def _notify_training_success(self):
        mb = MessageBox(
            "mb_training_success",
            pr.Vector2(500, 300),
            STRING_TRAINING_SUCCESS,
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)

    def _notify_learning_success(self):
        mb = MessageBox(
            "mb_learning_success",
            pr.Vector2(500, 300),
            STRING_LEARNING_SUCCESS,
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)

    def _notify_learning_failure(self):
        mb = MessageBox(
            "mb_learning_failure",
            pr.Vector2(500, 300),
            STRING_LEARNING_FAILURE,
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)

    def _button_is_clicked(self, button: Button):
        if button.id == "button_back":
            self.state = 5

    def _message_box_is_closed(self, message_box: MessageBox):
        self.message_box = None
        match message_box.id:
            case "mb_training_success":
                self._reboot_simulation(False)
                self.state = 2

            case "mb_learning_success":
                self.challenge.on_good_answer()
                self.state = 6

    def _boot_simulation(self, training: bool):
        self._create_world()
        self._spawn_entities(training)

    def _reboot_simulation(self, training: bool):
        assert self.brain is not None
        self.brain.fit(self.destroyed_drones)
        self._boot_simulation(training)

    def _create_world(self):
        self.world = World(
            220,
            136,
            SCREEN_WIDTH - 354,
            SCREEN_HEIGHT - 240,
        )

    def _spawn_entities(self, training: bool):
        assert self.brain is not None
        self.drones: list[Drone] = self.brain.get_drones(
            self.world, World.ORIGIN, training
        )
        self.destroyed_drones: list[Drone] = []

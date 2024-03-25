from spacerescue.resources.resource_manager import ResourceManager


GLOBAL_RESOURCES = ResourceManager.get_instance()
STATE_RESOURCES = ResourceManager.get_instance("state")
SCENE_RESOURCES = ResourceManager.get_instance("scene")

STRING_COMMIT = "COMMIT"
STRING_QUIT = "QUIT"
STRING_COPY_ID = "COPY ID"
STRING_MUSIC_ONOFF = "MUSIC ON/OFF"
STRING_START = "START"
STRING_EXIT = "EXIT"
STRING_OK = "OK"
STRING_BACK = "BACK"
STRING_TRAINING = "TRAINING ..."

STRING_MISSION_CAPTION = "\n     [F1: HELP] [F2: MISSION]             [ID: {}]"
STRING_CODE_UNDER_VALIDATION = "Code under validation, wait a minute ..."

STRING_ANSWER_IS_CORRECT = """Congratulation!

Your answer is correct!

Ready for the next challenge?"""

STRING_ANSER_IS_INCORRECT = """Your answer is incorrect!

{reason}

Your crew really needs you.
Please try again and good luck."""

STRING_ALL_CHALLENGES_UNLOCKED = """All the challenges are unlocked!

Did you really save the crew?"""

STRING_ONE_CHALLENGE_UNLOCKED = """Congratulation!

One Challenge unlocked!"""

STRING_TRAINING_SUCCESS = """Congratulation!

Your drone successfully reachs the target.

Now let try for real!"""

STRING_LEARNING_SUCCESS = """Congratulation!

Your drone successfully reachs the target.

Ready for the next challenge?"""

STRING_LEARNING_FAILURE = """Halas!

Your drone could not reach the target.

Please train more and good luck."""

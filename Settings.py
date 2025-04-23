# WORLD SETTINGS


class Settings:
    # Screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # World parameters
    GRAVITY = 0.5
    TIME_STEP = 0.01
    DAMPENING = 0.85

    @classmethod
    def update_settings(cls, gravity, time_step, dampening):
        cls.GRAVITY = gravity
        cls.TIME_STEP = time_step
        cls.DAMPENING = dampening




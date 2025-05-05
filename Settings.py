# WORLD SETTINGS


class Settings:
    # Screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # World parameters
    GRAVITY = 0.5
    TIME_STEP = 0.01
    DAMPENING = 0.85
    FPS = 60

    @classmethod
    def update_settings(self, gravity, time_step, dampening):
        self.GRAVITY = gravity
        self.TIME_STEP = time_step
        self.DAMPENING = dampening

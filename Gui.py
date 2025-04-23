import imgui
import pygame
from Settings import Settings
from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import *
from Body import *

class Gui:
    def __init__(self):
        imgui.create_context()
        self.impl = PygameRenderer()
        
        self.gravity = Settings.GRAVITY
        self.time_step = Settings.TIME_STEP
        self.dampening = Settings.DAMPENING

        self.num_bodies = 50
        
        ####    FLAGS    ####
        self.show_custom_window = True
        self.generate_bodies = False
        self.demo_figure_8_pattern = False
        self.demo_Mini_solar_system = False


    def process_event(self, event):
        self.impl.process_event(event)

        io = imgui.get_io()
        return not io.want_capture_mouse and not io.want_capture_keyboard


    def process_input(self):
        self.impl.process_inputs()

    def update_settings(self):
        Settings.GRAVITY = self.gravity
        Settings.TIME_STEP = self.time_step
        Settings.DAMPENING = self.dampening
        print(f"gravity:{Settings.GRAVITY}, time_step:{Settings.TIME_STEP}, damp:{Settings.DAMPENING}")


    def render(self):
        glUseProgram(0)
        glBindVertexArray(0)

        io = imgui.get_io()
        io.display_size = pygame.display.get_surface().get_size()

        imgui.new_frame()

        if self.show_custom_window:
            is_expand, self.show_custom_window = imgui.begin("Custom window", True)
            if is_expand:
                imgui.columns(2, "settings_columns", border=True)
                imgui.text("Simulation Controls")
                #imgui.separator()

                # Button to trigger reset
                if imgui.button("Randomize Bodies"):
                    self.generate_bodies = True

                changed, self.num_bodies = imgui.slider_int("Bodies", self.num_bodies, 0, 200)

                imgui.text(" ")

                if imgui.button("3 body problem"):
                    self.demo_figure_8_pattern = True

                if imgui.button("Mini solar system"):
                    self.demo_Mini_solar_system = True

                imgui.next_column()
                imgui.text("World Settings")

                changed, self.gravity = imgui.slider_float("Gravity", self.gravity, 0.0, 5.0)
                changed, self.time_step = imgui.slider_float("Time Step", self.time_step, 0.001, 0.5, format="%.4f")
                changed, self.dampening = imgui.slider_float("Dampening", self.dampening, 0.0, 1.0)

                imgui.columns(1)

            imgui.end()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        imgui.render()
        self.impl.render(imgui.get_draw_data())

        glEnable(GL_DEPTH_TEST)



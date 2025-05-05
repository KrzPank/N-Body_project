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

        self.new_body_pos = glm.vec3(0.0)
        self.new_body_vel = glm.vec3(0.0)
        self.new_body_r = 5.0
        self.new_body_mass = 1.0
        self.new_body_color = glm.vec3(0.0)

        self.bodies = []

        self.num_bodies = 50
        
        ####    FLAGS    ####
        self.show_settings_window = True
        self.show_custom_window = False
        self.generate_bodies = False
        self.demo_figure_8_pattern = False
        self.demo_Mini_solar_system = False
        self.add_custom_body = False
        self.demo_earth_moon = False


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
        #print(f"gravity:{Settings.GRAVITY}, time_step:{Settings.TIME_STEP}, damp:{Settings.DAMPENING}")


    def render(self):
        glUseProgram(0)
        glBindVertexArray(0)

        io = imgui.get_io()
        io.display_size = pygame.display.get_surface().get_size()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("Menu", True):

                clicked_settings_window, selected = imgui.menu_item("Settings Window", None, self.show_settings_window, True)
                if clicked_settings_window:
                    self.show_settings_window = not self.show_settings_window

                clicked_custom_window, selected = imgui.menu_item("Custom Window", None, self.show_custom_window, True)
                if clicked_custom_window:
                    self.show_custom_window = not self.show_custom_window

                imgui.end_menu()
            imgui.end_main_menu_bar()


        if self.show_settings_window:
            is_expand, self.show_settings_window = imgui.begin("Settings Window", True)
            if is_expand:
                imgui.columns(2, "settings_columns", border=True)
                imgui.text("Simulation Controls")

                # Button to trigger reset
                if imgui.button("Randomize Bodies"):
                    self.generate_bodies = True

                changed, self.num_bodies = imgui.slider_int("Bodies", self.num_bodies, 0, 200)

                imgui.text(" ")

                if imgui.button("3 body problem"):
                    self.demo_figure_8_pattern = True

                if imgui.button("Mini solar system"):
                    self.demo_Mini_solar_system = True
                
                if imgui.button("Earth Moon"):
                    self.demo_earth_moon = True

                imgui.next_column()
                imgui.text("World Settings")

                #changed, self.gravity = imgui.slider_float("Gravity", self.gravity, 0.0, 5.0)
                #changed, self.time_step = imgui.slider_float("Time Step", self.time_step, 0.0000, 0.3, format="%.4f")
                
                changed, self.gravity = imgui.input_float("Gravity", self.gravity, 0.01)
                changed, self.time_step = imgui.input_float("Time Step", self.time_step, 0.0005,  format="%.4f")

                changed, self.dampening = imgui.slider_float("Dampening", self.dampening, 0.0, 1.0)

                if self.gravity < 0:
                    self.gravity = 0

                if self.time_step < 0:
                    self.time_step = 0

                imgui.columns(1)

            imgui.end()


        if self.show_custom_window:
            is_expand, self.show_custom_window = imgui.begin("Custom Window", True)
            if is_expand:
                imgui.text("Create New Body")

                changed, self.new_body_pos = imgui.input_float3("Position (x,y,z)", *self.new_body_pos)
                changed, self.new_body_vel = imgui.input_float3("Velocity (x,y,z)", *self.new_body_vel)
                changed, self.new_body_r = imgui.input_float("Radius", self.new_body_r, 0.1, 10.0)
                changed, self.new_body_mass = imgui.input_float("Mass", self.new_body_mass, 0.1, 1000.0)

                changed, self.new_body_color = imgui.color_edit3("Color", *self.new_body_color)

                
                if imgui.button("Add Body"):
                    new_body = Body(
                        position=glm.vec3(*self.new_body_pos),
                        velocity=glm.vec3(*self.new_body_vel),
                        r=self.new_body_r,
                        mass=self.new_body_mass,
                        color=glm.vec3(*self.new_body_color)
                    )
                    self.bodies.append(new_body)
                    print(f"Added new body: {new_body}")
                    self.add_custom_body = True

            imgui.end()

        glDisable(GL_DEPTH_TEST)

        imgui.render()
        self.impl.render(imgui.get_draw_data())

        glEnable(GL_DEPTH_TEST)

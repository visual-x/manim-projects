from manim import *

CAR1_COLOR = BLUE_D
CAR2_COLOR = ORANGE
NEON_GREEN = "#00f700"


def parameter_to_color(y_value, min, max, colors):
    alpha = inverse_interpolate(min, max, y_value)
    index, sub_alpha = integer_interpolate(0, len(colors) - 1, alpha)

    return interpolate_color(colors[index], colors[index + 1], sub_alpha)

def get_street(radius = 3, thickness = 0.5):
    asphalt = Annulus(
        inner_radius = radius - thickness, outer_radius = radius + thickness, 
        color = GREY, fill_opacity = 0.5, stroke_width = 1
    )
    circle = Circle(radius = radius, color = LIGHT_GREY, stroke_width = 3)
    marks = DashedVMobject(circle, num_dashes = 50)

    street = VGroup(asphalt, marks)
    street.start = circle.get_start()
    street.dline = circle

    return street

def get_car(main_color, height = 1):
    car = SVGMobject("Car_Oben")
    car.set(height = height)
    car.set_color(DARK_GREY)
    car[2].set_color(main_color)
    car[9].set_color(YELLOW)
    car[10].set_color(YELLOW)
    car[11].set_color(RED)
    car[12].set_color(RED)

    car.center = car.get_center()

    # lights 
    front_left  = get_front_lights().next_to(car[9], UP, buff = -0.05)
    front_right = get_front_lights().next_to(car[10], UP, buff = -0.05)

    back_left  = get_back_lights().next_to(car[11], DOWN, buff = -0.03)
    back_right = get_back_lights().next_to(car[12], DOWN, buff = -0.03)

    car.add_to_back(front_left, front_right, back_left, back_right)

    return car

def get_front_lights(inner_rad = 1, outer_rad = 2):
    light = AnnularSector(
        inner_radius=inner_rad, outer_radius=outer_rad,
        angle = 8*DEGREES, start_angle = 86*DEGREES, 
        fill_opacity = [0.3,0], color = YELLOW
    )
    return light

def get_back_lights():
    light = AnnularSector(
        inner_radius=0.05, outer_radius=0.1,
        angle = -180*DEGREES, start_angle = 0, 
        fill_opacity = [0,0.3,0], color = RED
    )
    return light



class Physics(Scene):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street()
        self.start_point = self.street.start

        self.rotating_cars()


    def rotating_cars(self):
        street, start_point = self.street, self.start_point

        car1 = get_car(main_color = CAR1_COLOR)
        car1.shift(start_point + car1.center)
        car1.save_state()

        car2 = get_car(main_color = CAR2_COLOR)
        car2.shift(start_point + car2.center)
        car2.save_state()

        self.add(street, car2, car1)
        self.wait(2)

        self.play(
            Rotating(car2, radians = 60*DEGREES, about_point = street.get_center(), run_time=4, rate_func = smooth), 
        )
        self.wait(2)


        def update_car(mob, dt):
            mob.rotate(0.25 * dt * PI, about_point = street.get_center())
        car1.add_updater(update_car)
        car2.add_updater(update_car)
        self.wait(16) # 4 Sekunden noch bis zur Vollrotation


class Intro(Scene):
    def construct(self):
        self.x_min = 0
        self.x_max = 4*np.pi

        self.axes = NumberPlane(
            x_range = [self.x_min, self.x_max], y_range = [-3, 3, np.pi/4],
            x_length = config["frame_width"] - 1, 
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.origin = self.axes.c2p(0,0)

        self.a_val = ValueTracker(1)
        self.b_val = ValueTracker(1)
        self.c_val = ValueTracker(0)
        self.d_val = ValueTracker(0)

        a_val, b_val, c_val, d_val = self.a_val, self.b_val, self.c_val, self.d_val

        arrows = always_redraw(lambda: self.get_arrows(
                a_val.get_value(), b_val.get_value(), c_val.get_value(), d_val.get_value(), nums = 41, 
                buff = 0, max_tip_length_to_length_ratio = 0.15
            ).set_color_by_gradient(RED, GREEN, YELLOW, BLUE)
        )

        func = MathTex("f(x)", "=", "a", "\\cdot", "\\sin", "\\big(", "b", "\\cdot", "(", "x", "+", "c", ")","\\big)", "+", "d")\
            .scale(1.5)\
            .to_edge(UP, buff = 1)
        func[2].set_color(RED)
        func[6].set_color(BLUE)
        func[11].set_color(YELLOW)
        func[-1].set_color(GREEN)

        a, b, c, d = func[2].copy(), func[6].copy(), func[11].copy(), func[-1].copy()
        func.set_fill(opacity = 0.5)

        self.play(
            AnimationGroup(
                FadeIn(a, shift = 5*UP, scale = 5),
                FadeIn(b, shift = 5*LEFT, scale = 5), 
                lag_ratio = 0.25 
            ), 
            run_time = 2
        )

        self.play(
            *[GrowArrow(arrow) for arrow in arrows], 
            run_time = 1.5
        )
        self.add(arrows)

        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.6)).set_value(2),
            b_val.animate(rate_func = squish_rate_func(smooth, 0.4, 1.0)).set_value(0.5),
            run_time = 3
        )
        self.play(Write(func))
        self.play(
            Transform(b, c, path_arc = PI/3),
            Transform(a, d, path_arc = PI/3),
            run_time = 1.5
        )
        self.wait()

        self.play(
            c_val.animate.set_value(+5*PI),
            run_time = 3
        )
        arrows.clear_updaters()
        self.play(ApplyMethod(arrows.shift, 2*DOWN), run_time = 2)
        self.wait(3)


        mobs = Group(*self.mobjects)
        self.play(mobs.animate.scale_about_point(5, ORIGIN), rate_func = running_start, run_time = 2)


    # functions
    def sin_par(self, x, a, b, c, d):
        return a * np.sin(b*(x - c)) + d

    def get_arrows(self, a, b, c, d, nums = 41, **kwargs):
        arrows = VGroup()
        for x in np.linspace(self.x_min, self.x_max, nums):
            start = self.axes.c2p(x, 0)
            end = self.axes.c2p(x, a * np.sin(b*(x + c)) + d)
            arrow = Arrow(start, end, **kwargs)
            arrows.add(arrow)

        return arrows


class FromCarsToGraphs(MovingCameraScene):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)                                   # POSITION street

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/6], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)             # POSITION axes
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo = 0.50
        self.phase = 60*DEGREES


        self.setup_scene(animate = True)
        self.similar_difference()
        self.camera_to_street()
        self.car2_to_start_position()
        self.draw_sine_curves_for_both_cars()
        self.introduce_parameter()

    def setup_scene(self, animate = False):
        street, axes= self.street, self.axes

        start_point = street[1][0].get_start()  #   street[1] --> DashedLine --> street[1][0] --> first segment
        car1 =  get_car(main_color = CAR1_COLOR, height = self.car_height)
        car1.shift(start_point + car1.center)

        car2 = get_car(main_color = CAR2_COLOR, height = self.car_height)
        car2.shift(start_point - car2.center)

        x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()
        axis_ticks = self.get_axis_ticks([PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3, 2*PI])

        if animate is True:
            car1.shift(2*DOWN)
            car2.shift(2*DOWN)
            self.play(
                AnimationGroup(
                    FadeIn(car1, shift = LEFT), 
                    FadeIn(car2, shift = RIGHT), 
                    lag_ratio = 0.2
                ),
                run_time = 2
            )
            self.play(
                AnimationGroup(
                    Create(axes, lag_ratio = 0.05),
                    Create(axis_ticks, lag_ratio = 0.05),
                    FadeIn(x_numbers, shift = 0.5*UP, lag_ratio = 0.05), 
                    FadeIn(y_numbers, shift = 0.5*DOWN, lag_ratio = 0.05), 
                    DrawBorderThenFill(street), 
                    car1.animate(rate_func = lambda t: smooth(t)).shift(2*UP),
                    car2.animate(rate_func = lambda t: smooth(t)).shift(2*UP),
                    lag_ratio = 0.15
                ),
                run_time = 4
            )
        self.add(street, car1, car2, axes, axis_ticks, x_numbers, y_numbers)

        self.car1, self.car2, self.start_point = car1, car2, start_point

    def similar_difference(self):
        car1 = self.get_car_side_view(car_width = 2, main_color = CAR1_COLOR)\
            .shift(3*DOWN + 2.5*LEFT)
        car2 = self.get_car_side_view(car_width = 2, main_color = CAR2_COLOR)\
            .shift(3*DOWN + 2.5*RIGHT)

        def rotate_wheel_clockwise(mob, dt):
            mob.rotate(-dt* TAU)

        car1[0].add_updater(rotate_wheel_clockwise)
        car1[1].add_updater(rotate_wheel_clockwise)
        car2[0].add_updater(rotate_wheel_clockwise)
        car2[1].add_updater(rotate_wheel_clockwise)

        self.wait()
        self.play(
            FadeIn(car1, shift = 3*RIGHT), 
            FadeIn(car2, shift = 3*RIGHT), 
            rate_func = linear, run_time = 3
        )
        for wheel in car1[0], car1[1], car2[0], car2[1]:
            wheel.clear_updaters()
        self.wait()

        equals = MathTex("=", font_size = 72)\
            .move_to(midpoint(car1.get_right(), car2.get_left()))

        self.play(Write(equals))
        self.wait(2)

        self.car1_side, self.car2_side, self.equals = car1, car2, equals

    def camera_to_street(self):
        frame = self.camera.frame
        frame.save_state()

        self.play(
            frame.animate.move_to(self.street).set(height = self.street.height + 1), 
            run_time = 3
        )
        self.wait()

    def car2_to_start_position(self):
        car1, car2, street = self.car1, self.car2, self.street

        self.play(Rotating(car2, radians = self.phase, about_point=street.get_center(), run_time = 2))
        self.wait()

        car1_line = always_redraw(lambda: 
            Line(street.get_center(), car1[-23:-1].get_center())\
                .set_stroke(opacity = [0,1])\
                .set_color([CAR1_COLOR, WHITE])
        )
        car2_line = always_redraw(lambda: 
                Line(street.get_center(), car2[-23:-1].get_center())\
                    .set_stroke(opacity = [1,0])\
                    .set_color([WHITE, CAR2_COLOR])
        )

        cars_angle = Arc(radius = 1.5, start_angle = 0, angle = self.phase, arc_center = street.get_center())\
            .set_color([CAR1_COLOR, CAR2_COLOR])


        self.play(
            Create(VGroup(car1_line, car2_line)), 
            run_time = 2
        )
        self.bring_to_front(car1, car2)
        self.wait(0.5)
        self.play(Create(cars_angle), run_time = 2)
        self.bring_to_front(car1, car2)
        self.wait(2)


        rotate_group = VGroup(cars_angle, car1, car2)
        self.play(
            Rotating(rotate_group, radians = TAU, about_point = street.get_center(), run_time = 8),
            Restore(self.renderer.camera.frame, rate_func = squish_rate_func(smooth, 0.25, 1), run_time = 8)
        )


        self.cars_angle_group = VGroup(cars_angle, car1_line, car2_line)
        self.play(FadeOut(self.cars_angle_group))
        self.wait()

    def draw_sine_curves_for_both_cars(self):
        street, car1, car2, axes = self.street, self.car1, self.car2, self.axes

        dot1 = Dot(self.start_point, color = CAR1_COLOR)
        dot2 = Dot(car2[-23:-1].get_center(), color = CAR2_COLOR)
        self.play(
            AnimationGroup(
                dot1.animate.move_to(self.origin),
                dot2.animate.move_to(axes.c2p(0, np.sin(self.phase))),
                lag_ratio = 0.4
            ),
            run_time = 3
        )
        self.wait()

        # CAR 1
        self.t_offset = 0
        def update_car1(mob, dt):
            self.t_offset += 0.5 * dt
            mob.rotate(self.velo * dt, about_point = street.get_center())

        def get_car1_to_graph_line():
            x = self.t_offset
            y = np.sin(x)
            return DashedLine(car1[4:].get_center(), axes.c2p(x,y), color=CAR1_COLOR)

        sin = VGroup()
        sin.add(Line(self.origin, self.origin, color = CAR1_COLOR))
        def get_curve():
            last_line = sin[-1]
            x = self.t_offset
            y = np.sin(x)
            new_line = Line(last_line.get_end(), axes.c2p(x,y), color = CAR1_COLOR)
            sin.add(new_line)
            return sin

        car1.add_updater(update_car1)
        car1_to_graph_line = always_redraw(get_car1_to_graph_line)
        sin1_curve = always_redraw(get_curve)

        # CAR 2
        def update_car2(mob, dt):
            # self.t_offset += 0.5 * dt
            mob.rotate(self.velo * dt, about_point = street.get_center())

        def get_car2_to_graph_line():
            x = self.t_offset
            y = np.sin(x + self.phase)
            return DashedLine(car2[4:].get_center(), axes.c2p(x,y), color=CAR2_COLOR)

        sin2 = VGroup()
        sin2.add(Line(axes.c2p(0, np.sin(self.phase)), axes.c2p(0, np.sin(self.phase)), color = CAR2_COLOR))
        def get_curve():
            last_line = sin2[-1]
            x = self.t_offset
            y = np.sin(x + self.phase)
            new_line = Line(last_line.get_end(), axes.c2p(x,y), color = CAR2_COLOR)
            sin2.add(new_line)
            return sin2

        car2.add_updater(update_car2)
        car2_to_graph_line = always_redraw(get_car2_to_graph_line)
        sin2_curve = always_redraw(get_curve)


        self.add(car1_to_graph_line, sin1_curve, car2_to_graph_line, sin2_curve)
        self.wait(4*PI)

        final_graph1 = axes.get_graph(lambda x: np.sin(x), x_range=[0, TAU], color = CAR1_COLOR)
        final_graph2 = axes.get_graph(lambda x: np.sin(x + self.phase), x_range=[0, TAU], color = CAR2_COLOR)

        car1.suspend_updating()
        car2.suspend_updating()
        self.remove(car1_to_graph_line, sin1_curve, car2_to_graph_line, sin2_curve, dot1, dot2)
        self.add(final_graph1, final_graph2)
        self.wait(2)


        self.graph1, self.graph2 = final_graph1, final_graph2

    def introduce_parameter(self):

        func_sin = MathTex("y", "=", "\\sin", "(", "x", ")", font_size = 80)\
            .set_color(CAR1_COLOR)\
            .shift(4*LEFT + 3*UP)
        func_sin[:2].set_color(GREY)

        func_sinc = MathTex("y", "=", "\\sin", "(", "x", "+", "\\pi/3", ")", font_size = 80)\
            .set_color(CAR2_COLOR)\
            .shift(2.5*RIGHT + 3*UP)
        func_sinc[:2].set_color(GREY)
        func_sinc[-3:-1].set_color(NEON_GREEN)


        self.play(ApplyWave(self.graph1, amplitude = 0.15))
        self.play(Write(func_sin))
        self.wait()

        self.play(
            ApplyMethod(self.graph2.shift, self.phase * self.axes.x_axis.unit_size * RIGHT),
            rate_func = there_and_back_with_pause, run_time = 6
        )
        self.wait()

        diff_val = ValueTracker(0)
        diff = always_redraw(lambda:
            Line(
                start = self.axes.c2p(diff_val.get_value(), np.sin(diff_val.get_value() + self.phase)),
                end = self.axes.c2p(diff_val.get_value() + self.phase, np.sin(diff_val.get_value() + self.phase)),
                color = NEON_GREEN, stroke_width = 8
            )
        )
        self.play(FadeIn(diff, shift = UP))
        self.play(diff_val.animate.set_value(5*PI/3), run_time = 4)
        self.play(diff_val.animate.set_value(2*PI/3), run_time = 2.5)
        self.wait()

        diff.clear_updaters()
        cars_angle = self.cars_angle_group[0].set_color(NEON_GREEN)
        self.play(ReplacementTransform(diff, cars_angle), run_time = 4)
        self.bring_to_front(self.car1, self.car2)
        self.wait()


        sin_copy = func_sin.copy()
        self.play(
            sin_copy.animate.move_to(func_sinc, aligned_edge = LEFT), 
            run_time = 2
        )

        def rotate_about_street(mob, dt):
            mob.rotate(self.velo * dt, about_point = self.street.get_center())

        self.car1.resume_updating()
        self.car2.resume_updating()
        cars_angle.add_updater(rotate_about_street)
        self.wait()

        self.play(
            Transform(sin_copy[:4], func_sinc[0:4]), 
            Transform(sin_copy[-1], func_sinc[-1]),
            run_time = 2
        )
        self.wait(2)

        self.play(Write(func_sinc[5:-1]))
        self.wait(3)

        # 4*PI - 5 left for full return

        self.play(Circumscribe(func_sinc, color = NEON_GREEN, run_time = 3, time_width = 0.75))
        self.wait(4*PI - 12)
        self.car1.clear_updaters()
        self.car2.clear_updaters()
        cars_angle.clear_updaters()
        self.wait()


        c_tex = MathTex("\\text{Parameter }", "c", font_size = 60)
        c_tex.move_to(self.axes.c2p(4*PI/3, 1))
        c_tex[-1].set_color(NEON_GREEN)

        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = NEON_GREEN) for mob in [func_sinc, func_sinc[-3:-1], c_tex[-1]]
        ])
        self.play(Create(sur_rects[0]), run_time = 2)
        self.wait()
        self.play(Transform(sur_rects[0], sur_rects[1]))
        self.wait(3)

        self.play(
            Write(c_tex[0]), 
            TransformFromCopy(func_sinc[-3:-1], c_tex[1]),
        )
        self.play(Transform(sur_rects[0], sur_rects[2]))
        self.wait(3)




        def rotate_wheel_clockwise(mob, dt):
            mob.rotate(-dt* TAU)

        self.car1_side[0].add_updater(rotate_wheel_clockwise)
        self.car1_side[1].add_updater(rotate_wheel_clockwise)
        self.car2_side[0].add_updater(rotate_wheel_clockwise)
        self.car2_side[1].add_updater(rotate_wheel_clockwise)
        translation_group = VGroup(self.car1_side, self.equals, self.car2_side)
        self.play(
            translation_group.animate(rate_func = double_smooth).shift(24 * RIGHT), 
            self.renderer.camera.frame.animate().shift(18*RIGHT), 
            run_time = 4
        )


    # functions
    def get_x_axis_numbers(self):
        x_axis_nums = [np.pi/2, np.pi, 3/2*np.pi, 2*np.pi]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                ["\\pi/2", "\\pi", "3\\pi/2", "2\\pi"], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_y_axis_numbers(self):
        y_axis_nums = [-1,0,1]
        y_axis_coords = VGroup(*[
            MathTex(num, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for num in y_axis_nums
        ])
        return y_axis_coords

    def get_axis_ticks(self, numbers, sw = 3, length = 0.2, **kwargs):
        ticks = VGroup()
        for num in numbers:
            tick = Line(UP, DOWN, stroke_width = sw)
            tick.set_length(length)
            tick.move_to(self.axes.c2p(num, 0))
            ticks.add(tick)

        return ticks

    def get_car_side_view(self, car_width = 1.5, main_color = RED):
        car = SVGMobject("Car")
        car.set_color(main_color)
        car.set(width = car_width)

        car[0].set_color(GREY)
        car[1].set_color(GREY)
        car[-3].set_color(RED)
        car[-2].set_color(YELLOW)
        car[-1].set_color(YELLOW)

        front_lights = self.get_front_lights().next_to(car[-2], RIGHT, buff = 0, aligned_edge=UP)
        back_lights = self.get_back_lights().next_to(car[-3], LEFT, buff = 0)
        car.add(front_lights, back_lights)

        car.main_color = main_color

        return car

    def get_front_lights(self, inner_rad = 0.25, outer_rad = 1):
        light = AnnularSector(
            inner_radius=inner_rad, outer_radius=outer_rad,
            angle = 15*DEGREES, start_angle = -15*DEGREES, 
            fill_opacity = [0.3,0], color = YELLOW
        )
        return light

    def get_back_lights(self):
        light = AnnularSector(
            inner_radius=0.05, outer_radius=0.3,
            angle = -120*DEGREES, start_angle = -120*DEGREES, 
            fill_opacity = [0,0.3,0], color = RED
        )
        return light


class ParameterInfluence(Scene):
    def construct(self):
        self.x_min = -9*PI/4
        self.x_max = 9*PI/4

        self.axes_kwargs = {
            "x_range": [self.x_min, self.x_max, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": config["frame_width"] - 1, "y_length": 3.25, "color": GREY,
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 0}
        }
        self.axes = NumberPlane(**self.axes_kwargs).shift(1.5*DOWN).add_background_rectangle()
        self.origin = self.axes.c2p(0,0)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.c_val = ValueTracker(0)
        self.colors = [PINK, BLUE, GREEN_D, ORANGE, PURPLE]

        self.setup_scene()

    def setup_scene(self):
        axes, c_val = self.axes, self.c_val

        axes_ticks = self.get_axes_ticks([-5*PI/2, -2*PI, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, 2*PI, 5*PI/2])
        axes_numbers = self.get_axes_numbers()

        # Parameter Line
        c_line = self.c_line = self.get_c_line(
            x_min = self.x_min, x_max = self.x_max, x_step = PI/12, line_length = config["frame_width"] - 1, 
            numbers_with_elongated_ticks = [-2*PI, -3/2*PI, -5*PI/4, -PI, -3*PI/4, -PI/2, -PI/4, 0, PI/4, PI/2, 3*PI/4, PI, 5*PI/4, 3*PI/2, 2*PI]
        )
        c_line_numbers = self.get_c_line_numbers(font_size = 36)
        c_break = DashedLine(5*UP, 5*DOWN, color = RED, stroke_opacity = 0.5)
        c_dot = self.c_dot = always_redraw(lambda: self.get_c_dot(radius = 0.10))


        # Eequation
        func = MathTex("f(x)", "=", "\\sin", "(", "x", "param", ")")\
            .scale(1.4)\
            .next_to(c_line, DOWN, buff = 1.5)\
            .add_background_rectangle()
        func[6].set_stroke(width = 0).set_fill(opacity = 0)

        c_dec_func = self.c_dec_func = DecimalNumber(c_val.get_value(), num_decimal_places=2, include_sign=True)
        c_dec_func.scale(1.4).move_to(func[6]).align_to(func[5], DOWN)
        c_dec_func.add_updater(lambda dec:
            dec.set_value(c_val.get_value()).set_color(parameter_to_color(c_val.get_value(), -TAU, TAU, self.colors))
        )

        c_dec_line = always_redraw(lambda: self.get_parameter_to_num_line())


        # Graphen
        graph_bg = always_redraw(lambda: axes.get_graph(
            lambda x: np.sin(x), x_range = [self.x_min, self.x_max],
            color = parameter_to_color(c_val.get_value(), -TAU, TAU, self.colors), stroke_opacity = 0.45
        ))
        graph_per = always_redraw(lambda: axes.get_graph(
            lambda x: np.sin(x + c_val.get_value()), x_range = [-c_val.get_value(), -c_val.get_value() + 2*PI],
            color = parameter_to_color(c_val.get_value(), -TAU, TAU, self.colors)
        ))


        # Animations
        self.play(
            AnimationGroup(
                FadeIn(c_break, shift = 5*DOWN), 
                Create(axes), 
                *[GrowFromCenter(tick) for tick in axes_ticks],
                FadeIn(axes_numbers, shift = 0.5*UP, lag_ratio = 0.25),
                Create(func), 
                Write(c_dec_func), 
                Create(c_line), 
                FadeIn(c_line_numbers, shift = 0.5*DOWN, lag_ratio = 0.15),
                GrowFromCenter(c_dot),
                Create(c_dec_line), 
                lag_ratio = 0.15
            ), 
            run_time = 4
        )
        self.wait()

        self.play(Circumscribe(c_line_numbers[4], color = BLUE_D, fade_out = True, run_time = 3))
        self.wait()

        self.play(
            FadeIn(graph_bg), 
            Create(graph_per), 
            run_time = 4
        )
        self.wait()


        # ADDED ANIMATIONS
        trans_arrow = always_redraw(lambda: Arrow(self.origin, axes.c2p(-c_val.get_value(), 0), buff = 0, color = NEON_GREEN))
        prop_pos = Tex("Verschiebung nach links").next_to(c_line.n2p(PI), UP).shift(RIGHT)
        prop_neg = Tex("Verschiebung nach rechts").next_to(c_line.n2p(-PI), UP).shift(LEFT)

        equals_neg_sin = MathTex("=", "-", "\\sin", "(", "x", ")").scale(1.4).next_to(func, RIGHT)
        equals_cos = MathTex("=", "\\cos", "(", "x", ")").scale(1.4).next_to(func, RIGHT)
        equals_sin = MathTex("=", "\\sin", "(", "x", ")").scale(1.4).next_to(func, RIGHT)

        added_anims = [
            AnimationGroup(
                FadeIn(trans_arrow, shift = 2*UP),
                Write(prop_pos),
                lag_ratio = 0.25, run_time = 2.5
            ),
            FadeIn(equals_neg_sin, shift = 4*LEFT, run_time = 2), 
            ReplacementTransform(equals_neg_sin, equals_cos, run_time = 2),
            Write(prop_neg, run_time = 2),
            Write(equals_sin, run_time = 2)
        ]

        # LOOP THROUGH DIFFERENT VALUES FOR C
        c_values = [+PI/3, PI, PI/2, -3*PI/4, -2*PI]
        for i, c in enumerate(c_values):
            self.play(c_val.animate.set_value(c), run_time = 6)
            self.wait()
            self.play(added_anims[i])
            self.wait()
            if i == 2:
                self.wait()
                self.play(FadeOut(equals_cos, shift = 4*RIGHT))
                self.wait()
            if i == 4:
                self.play(FadeOut(equals_sin), run_time = 2)
                self.wait()
        self.wait()


        self.play(c_val.animate(rate_func = linear).set_value(2*PI), run_time = 20)
        self.wait(5)



    # functions
    def get_axes_ticks(self, numbers, tick_length = 0.2):
        ticks = VGroup()
        for num in numbers:
            tick = Line(UP, DOWN)\
                .set_length(tick_length)\
                .move_to(self.axes.c2p(num, 0))
            ticks.add(tick)

        return ticks

    def get_axes_numbers(self):
        numbers = [-TAU, -PI, PI, TAU]
        strings = ["-2\\pi", "-\\pi", "\\pi", "2\\pi"]

        axes_numbers = VGroup()
        for num, string in zip(numbers, strings):
            tex = MathTex(string, font_size = 36, color = GREY)
            tex.next_to(self.axes.c2p(num, 0), DOWN)
            axes_numbers.add(tex)
        return axes_numbers

    def get_c_line(self, x_min, x_max, x_step, line_length, **kwargs):
        c_line = NumberLine(x_range = [x_min, x_max, x_step], length = line_length, include_numbers = False, **kwargs)\
            .shift(2.75*UP)
        return c_line

    def get_c_line_numbers(self, **kwargs):
        nums = [-2*PI, -3*PI/2, -PI, -PI/2, 0, PI/2, PI, 3*PI/2, 2*PI]
        texs = ["-2\\pi", "-\\frac{3}{2}\\pi", "-\\pi", "-\\frac{1}{2}\\pi", "0", "\\frac{1}{2}\\pi", "\\pi", "\\frac{3}{2}\\pi", "2\\pi"]
        num_texs = VGroup()
        for num, latex in zip(nums, texs):
            tex = MathTex(latex, **kwargs)
            tex.next_to(self.c_line.n2p(num), DOWN, buff = 0.35)
            num_texs.add(tex)

        for i in [1,3]:
            num_texs[i][0][1:4].scale(0.6)
            num_texs[i].shift(0.2*UP)
        for i in [5,7]:
            num_texs[i][0][0:3].scale(0.6)
            num_texs[i].shift(0.2*UP)

        return num_texs

    def get_parameter_to_num_line(self):
        start_pos = 1.75*RIGHT + 1.15*UP
        line = Line(
            start_pos, 
            self.c_dot.get_center(), 
            color = parameter_to_color(self.c_val.get_value(), -TAU, TAU, self.colors)
        )
        line.set_stroke(opacity = [0,1,0])
        return line

    def get_c_dot(self, **kwargs):
        c_line, c_val = self.c_line, self.c_val
        c_dot = Dot(
            point = c_line.n2p(c_val.get_value()), 
            color = parameter_to_color(c_val.get_value(), -TAU, TAU, self.colors), 
            **kwargs
        )
        c_dot.set_sheen(-0.3, DR)
        c_dot.set_stroke(width = 1, color = WHITE)

        return c_dot


class DifferentPhases(FromCarsToGraphs):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)                                   # POSITION street

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/6], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)             # POSITION axes
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo = 0.50
        self.start_phase = 90*DEGREES
        self.phase = ValueTracker(self.start_phase)


        self.setup_scene(animate = False)
        self.add_2nd_car_items()
        self.shift_graph_with_parameter()

    def add_2nd_car_items(self):
        c_line = self.c_line = self.get_c_line(
            -2*PI, 2*PI, PI/3, line_length=config["frame_width"] - 2, 
            numbers_with_elongated_ticks = []
        )
        c_line.to_edge(UP, buff = 1.5)
        c_numbers = self.get_c_line_numbers(font_size = 36, color = GREY)
        c_dot = always_redraw(lambda: self.get_c_dot())
        sin_graph = self.axes.get_graph(lambda x: np.sin(x), x_range=[0, TAU], color = CAR1_COLOR)

        self.add(sin_graph)
        self.add(c_line, c_numbers, c_dot)
        self.bring_to_front(self.car2)

        all_mobs = Group(*self.mobjects)
        self.play(FadeIn(all_mobs), run_time = 3)
        self.wait()

        self.play(Rotating(self.car2, radians = self.start_phase, about_point=self.street.get_center(), run_time = 3))

    def shift_graph_with_parameter(self):
        street, axes, phase = self.street, self.axes, self.phase

        graph = always_redraw(lambda: axes.get_graph(lambda x: np.sin(x + phase.get_value()), x_range=[0, TAU], color = CAR2_COLOR))

        car1_line = Line(street.get_center(), street.get_center() + 1.5*RIGHT).set_stroke(opacity = [0,1]).set_color([CAR1_COLOR, WHITE])
        car2_line = always_redraw(lambda: 
                Line(street.get_center(), street.get_center() + 1.5*np.sin(phase.get_value())*UP + 1.5*np.cos(phase.get_value())*RIGHT)\
                    .set_stroke(opacity = [1,0])\
                    .set_color([WHITE, CAR2_COLOR])
        )
        cars_angle = always_redraw(lambda: 
            Arc(radius = 1.5, start_angle = 0, angle = phase.get_value(), arc_center = street.get_center())\
                .set_color(NEON_GREEN)
        )

        self.play(
            LaggedStartMap(FadeIn, VGroup(cars_angle, car1_line, car2_line), lag_ratio = 0.2),
            Create(graph), 
            run_time = 2
        )
        self.bring_to_front(self.car1, self.car2)
        self.wait()


        phase_line = always_redraw(lambda: self.get_phase_line())
        self.play(
            TransformFromCopy(cars_angle, phase_line), 
            run_time = 3
        )
        self.wait()


        self.play(
            phase.animate(rate_func = linear).set_value(TAU),
            Rotating(self.car2, radians = 3*TAU/4, about_point = street.get_center(), run_time = 15, rate_func = linear),
            run_time = 12
        )
        self.wait()

        phase.set_value(0)
        self.wait()

        self.play(
            phase.animate(rate_func = linear).set_value(-TAU),
            Rotating(self.car2, radians = -TAU, about_point = street.get_center(), run_time = 15, rate_func = linear),
            run_time = 16
        )
        self.wait(3)


    # functions
    def get_c_line(self, x_min, x_max, x_step, line_length, **kwargs):
        c_line = NumberLine(x_range = [x_min, x_max, x_step], length = line_length, include_numbers = False, **kwargs)\
            .shift(2.75*UP)
        return c_line

    def get_c_line_numbers(self, **kwargs):
        nums = [-TAU, -PI, 0, PI, TAU]
        texs = ["-2\\pi", "-\\pi", "0", "\\pi", "2\\pi"]
        num_texs = VGroup()
        for num, latex in zip(nums, texs):
            tex = MathTex(latex, **kwargs)
            tex.next_to(self.c_line.n2p(num), UP, buff = 0.35)
            num_texs.add(tex)

        return num_texs

    def get_phase_line(self):
        c_line, phase = self.c_line, self.phase

        line = Line(
            c_line.n2p(0), 
            c_line.n2p(phase.get_value()),
        )
        line.set_color(NEON_GREEN)
        line.set_fill(opacity = 0.75)

        return line

    def get_c_dot(self, **kwargs):
        c_line, phase = self.c_line, self.phase
        c_dot = Dot(
            point = c_line.n2p(phase.get_value()),
            radius = 0.12,
            color = NEON_GREEN, 
            **kwargs
        )
        c_dot.set_fill(opacity = 0.75)
        c_dot.set_sheen(-0.3, DR)

        return c_dot


class Pendulum(Scene):
    def construct(self):
        self.anchor_point = 3*UP + 4*LEFT
        self.radius = 2
        self.weight_radius = 0.2
        self.angle = np.pi/6

        self.swing_kwargs = {"about_point" : self.anchor_point, "run_time" : 1.7, "rate_func" : self.swing_rate_func}

        self.draw_pendulum()
        self.show_oscillation()

    def draw_pendulum(self):
        pendulum = self.get_pendulum()
        ceiling = self.get_ceiling()

        self.play(
            Create(ceiling),
            Create(pendulum.line)
        )
        self.play(DrawBorderThenFill(pendulum.weight, run_time = 1))
        self.wait()

        self.pendulum = pendulum

    def show_oscillation(self):
        trajectory_dots = self.get_trajectory_dots()

        self.play(
            Create(trajectory_dots, run_time = self.swing_kwargs["run_time"]),
            Rotate(mobject = self.pendulum, angle = -2*self.angle, **self.swing_kwargs),
        )

        for m in 2, -2, 2, -2, 2, -2, 2, -2, 2:
            self.play(Rotate(self.pendulum, m*self.angle, **self.swing_kwargs))
        self.wait()

        self.play(
            ShrinkToCenter(Group(*self.mobjects), rate_func = running_start)
        )


    # functions
    def get_pendulum(self):
        line = Line(
            self.anchor_point, self.anchor_point + self.radius*DOWN,
            color = WHITE, stroke_width = 2
        )
        weight = Circle(
            radius = self.weight_radius,
            fill_color = GREY, fill_opacity = 1,
            stroke_width = 0, sheen_factor = 1,
        )
        weight.move_to(line.get_end())
        result = VGroup(line, weight)
        result.rotate(
            self.angle, 
            about_point = self.anchor_point
        )
        result.line = line
        result.weight = weight

        return result

    def get_ceiling(self):
        line = Line(0.75*LEFT, 0.75*RIGHT, color = GREY)
        line.move_to(self.anchor_point)
        return line

    def get_trajectory_dots(self, n_dots = 40, color = YELLOW):
        proportions = self.swing_rate_func(
            np.linspace(0, 1, n_dots)
        )
        angles = -2*self.angle*proportions
        angle_to_point = lambda a : np.cos(a)*RIGHT + np.sin(a)*UP
        dots = VGroup(*[
            Dot(angle_to_point(angle), radius = 0.005)
            for angle in angles
        ])
            
        dots.set_color(color)
        dots.scale(self.radius)
        dots.rotate(-np.pi/2 + self.angle, about_point = ORIGIN)
        dots.shift(4*LEFT + 2.1*UP)
        return dots

    def swing_rate_func(self, t):
        return (1-np.cos(np.pi*t))/2.0


class Thumbnail(Scene):
    def construct(self):
        tex = MathTex("\\sin", "(", "x", "+", "c", ")")
        tex.scale(3.5)
        tex.to_edge(UP)
        tex.set_color_by_tex_to_color_map({"\\sin": CAR2_COLOR, "(": CAR2_COLOR, ")": CAR2_COLOR, "x": CAR1_COLOR, "+": NEON_GREEN, "c": NEON_GREEN})

        self.add(tex)


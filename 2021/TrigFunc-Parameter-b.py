from manim import *

CAR1_COLOR = RED
CAR2_COLOR = GREEN

CMARK_TEX = "\\ding{51}"
XMARK_TEX = "\\ding{55}"


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
        self.b_val = ValueTracker(2)
        self.c_val = ValueTracker(0)
        self.d_val = ValueTracker(0)

        a_val, b_val, c_val, d_val = self.a_val, self.b_val, self.c_val, self.d_val

        arrows = always_redraw(lambda: self.get_arrows(
                a_val.get_value(), b_val.get_value(), c_val.get_value(), d_val.get_value(), nums = 61, 
                buff = 0, max_tip_length_to_length_ratio = 0.15
            ).set_color_by_gradient(RED, GREEN, YELLOW, BLUE)
        )

        func = MathTex("f(x)", "=", "a", "\\cdot", "\\sin", "\\big(", "b", "\\cdot", "(", "x", "+", "c", ")","\\big)", "+", "d")
        func.scale(1.5)
        func.to_edge(UP, buff = 1)
        for i, color in zip([2, 6, 11, -1], [RED, BLUE, YELLOW, GREEN]):
            func[i].set_color(color)
        func.save_state()
        func.center().scale(1.25)

        a_copy, b_copy = func[2].copy(), func[6].copy() 

        self.play(FadeIn(a_copy), run_time = 1.5)
        self.play(Transform(a_copy, b_copy, path_arc = np.pi/3))
        self.play(Circumscribe(b_copy, color = BLUE, fade_out=True))
        self.play(Write(func))
        self.remove(a_copy)
        self.wait()

        self.play(Restore(func))


        self.play(
            *[GrowArrow(arrow) for arrow in arrows], 
            run_time = 1.5
        )
        self.add(arrows)


        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.4)).set_value(2),
            c_val.animate(rate_func = squish_rate_func(smooth, 0.3, 0.7)).set_value(3*PI/2),
            d_val.animate(rate_func = squish_rate_func(smooth, 0.6, 1.0)).set_value(-1),
            run_time = 8
        )
        self.wait()

        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.6, 1.0)).set_value(1),
            c_val.animate(rate_func = squish_rate_func(smooth, 0.3, 0.7)).set_value(0),
            d_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.4)).set_value(0),
            run_time = 3
        )
        self.wait()

        car = self.get_car()\
            .to_edge(DOWN)\
            .shift(10*LEFT)

        def rotate_wheel(mob, dt):
            mob.rotate(-dt * TAU)

        car[0].add_updater(rotate_wheel)
        car[1].add_updater(rotate_wheel)
        self.add(car)

        self.play(
            car.animate(rate_func = linear).shift(20*RIGHT),
            b_val.animate(rate_func = there_and_back).set_value(0),
            run_time = 10
        )
        self.wait()

    # functions
    def sin_par(self, x, a, b, c, d):
        return a * np.sin(b*(x - c)) + d

    def get_arrows(self, a, b, c, d, nums = 61, **kwargs):
        arrows = VGroup()
        for x in np.linspace(self.x_min, self.x_max, nums):
            start = self.axes.c2p(x, 0)
            end = self.axes.c2p(x, a * np.sin(b*(x + c)) + d)
            arrow = Arrow(start, end, **kwargs)
            arrows.add(arrow)

        return arrows

    def get_car(self):
        car = SVGMobject("Car")
        car.set_color(BLUE)
        car.set(width = 2.5)

        car[0].set_color(GREY)
        car[1].set_color(GREY)
        car[-3].set_color(RED)
        car[-2].set_color(YELLOW)
        car[-1].set_color(YELLOW)

        front_lights = self.get_front_lights()\
            .next_to(car[-2], RIGHT, buff = 0, aligned_edge=UP)

        back_lights = self.get_back_lights()\
            .next_to(car[-3], LEFT, buff = 0)

        car.add(front_lights, back_lights)

        return car

    def get_front_lights(self, inner_rad = 0.5, outer_rad = 2):
        light = AnnularSector(
            inner_radius=inner_rad, outer_radius=outer_rad,
            angle = 15*DEGREES, start_angle = -15*DEGREES, 
            fill_opacity = [0.3,0], color = YELLOW
        )
        return light

    def get_back_lights(self):
        light = AnnularSector(
            inner_radius=0.05, outer_radius=0.3,
            angle = -180*DEGREES, start_angle = -90*DEGREES, 
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
        self.car_to_parameter()


    def rotating_cars(self):
        street, start_point = self.street, self.start_point

        car1 = get_car(main_color = CAR1_COLOR)
        car1.shift(start_point + car1.center)
        car1.save_state()


        self.play(
            AnimationGroup(
                DrawBorderThenFill(street), 
                # car1.animate(rate_func = lambda t: linear(t)).shift(2*UP),
                FadeIn(car1, shift = 2*UP),
                lag_ratio = 0.15
            ),
            run_time = 3
        )
        self.wait()

        def update_car1(mob, dt):
            mob.rotate(0.25 * dt * PI, about_point = street.get_center())
        car1.add_updater(update_car1)
        self.wait(4) # 4 Sekunden noch bis zur Vollrotation


        def update_dot(mob, dt):
            mob.rotate(0.125 * dt * PI, about_point = street.get_center())
        dot = Dot(point = street.dline.point_from_proportion(0.5), color = CAR1_COLOR)
        dot.add_updater(update_dot)

        circle = Circle(radius = 3, color = LIGHT_GREY, stroke_width = 3)
        self.add(dot)
        self.play(
            Transform(car1, dot),
            Transform(street, circle),
            rate_func = lambda t: there_and_back_with_pause(t, pause_ratio = 1/3), 
            run_time = 8
        )

        dot.remove_updater(update_dot)
        self.remove(dot)
        self.wait(4)            # Full Rotation done, well
        self.wait(self.dt)      # actually had to add this one for a full 360° rotation, dont know why


        car2 = get_car(main_color = CAR2_COLOR)
        car3 = get_car(main_color = YELLOW)
        car4 = get_car(main_color = BLUE)
        for car in car2, car3, car4:
            car.shift(start_point + car.center)
            car.save_state()

        def update_car2(mob, dt):
            mob.rotate(0.50 * dt * PI, about_point = street.get_center())
        def update_car3(mob, dt):
            mob.rotate(0.75 * dt * PI, about_point = street.get_center())
        def update_car4(mob, dt):
            mob.rotate(1.00 * dt * PI, about_point = street.get_center())

        self.add(car2, car3, car4)
        self.bring_to_front(car1)

        car2.add_updater(update_car2)
        car3.add_updater(update_car3)
        car4.add_updater(update_car4)
        self.wait(8)

        car1.remove_updater(update_car1)
        car2.remove_updater(update_car2)
        car3.remove_updater(update_car3)
        car4.remove_updater(update_car4)

        car1.restore()
        car2.restore()
        car3.restore()
        car4.restore()


        self.wait(3)
        self.car1, self.car2, self.car3, self.car4 = car1, car2, car3, car4

    def car_to_parameter(self):
        car1, car2, car3, car4 = self.car1, self.car2, self.car3, self.car4

        funcs = VGroup(*[
            MathTex("f(x)", "=", "\\sin", "(", str(b), "\\cdot", "x", ")", font_size = 60)
            for b in [1,4,3,2]
        ])
        for func, color in zip(funcs, [RED, BLUE, YELLOW, GREEN]):
            func[4].set_color(color)

        self.play(
            FadeIn(VGroup(funcs[0][:4], funcs[0][5:]), run_time = 1),
            FadeIn(funcs[0][4], shift = UP)
        )
        self.play(
            GrowFromPoint(car1, funcs[0][4].get_center(), rate_func = lambda t: smooth(1-t), run_time = 2)
        )
        self.wait()

        cars = [car1, car4, car3, car2]

        for i in range(1, len(funcs)):
            self.play(
                FadeOut(funcs[i-1][4], shift = UP), 
                FadeIn(funcs[i][4], shift = UP)
            )
            self.play(
                GrowFromPoint(cars[i], funcs[i][4].get_center(), rate_func = lambda t: smooth(1-t), run_time = 2)
            )
        self.wait()


        mobs = Group(*self.mobjects)
        self.play(
            *[FadeOut(mob) for mob in mobs]
        )


class FromCarsToGraphs(Scene):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)                                   # POSITION street

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)             # POSITION axes
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50
        self.velo2 = 1.00


        self.setup_scene(animate = True)
        self.draw_sine_curve_with_car1()
        self.infos_about_car1()
        self.infos_about_car2()
        self.draw_curve_for_car2_with_twice_speed()

    def setup_scene(self, animate = False):
        street, axes= self.street, self.axes

        start_point = street[1][0].get_start()  #   street[1] --> DashedLine --> street[1][0] --> first segment
        car1 =  get_car(main_color = CAR1_COLOR, height = self.car_height)
        car1.shift(start_point + car1.center)

        x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        self.add(street, car1, axes, x_numbers, y_numbers)
        if animate is True:
            car1.shift(2*DOWN)
            self.play(
                AnimationGroup(
                    Create(axes, lag_ratio = 0.05),
                    FadeIn(x_numbers, shift = 0.5*UP, lag_ratio = 0.05), 
                    FadeIn(y_numbers, shift = 0.5*DOWN, lag_ratio = 0.05), 
                    DrawBorderThenFill(street), 
                    car1.animate(rate_func = lambda t: linear(t)).shift(2*UP),
                    lag_ratio = 0.15
                ), 
                run_time = 3
            )
        self.wait()

        self.car1, self.start_point = car1, start_point

    def draw_sine_curve_with_car1(self):
        street, car1, axes = self.street, self.car1, self.axes

        dot = Dot(self.start_point, color = CAR1_COLOR)
        self.play(dot.animate.move_to(self.origin), run_time = 3)
        self.wait()

        self.t_offset = 0
        def update_car1(mob, dt):
            self.t_offset += 0.5 * dt
            mob.rotate(self.velo1 * dt, about_point = street.get_center())

        def get_car_to_graph_line():
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
        car_to_graph_line = always_redraw(get_car_to_graph_line)
        sin_curve = always_redraw(get_curve)
        self.add(car_to_graph_line, sin_curve)
        self.wait(4*PI)

        final_graph = axes.get_graph(lambda x: np.sin(x), x_range=[0, TAU], color = CAR1_COLOR)

        car1.suspend_updating()
        self.remove(car_to_graph_line, sin_curve)
        self.add(final_graph)
        self.wait(2)

    def infos_about_car1(self):
        axes = self.axes 

        car1_side = self.get_car_side_view(car_width = 1.5, main_color = RED)
        car1_side.to_corner(UL).shift(RIGHT)

        arrow = DoubleArrow(axes.c2p(0,1.5), axes.c2p(2*PI, 1.5), color = GREY, buff = 0)

        num_of_rot = MathTex("1", "\\ \\text{Umdrehung}")
        num_of_rot.next_to(arrow, UP, buff = 0)
        num_of_rot[0].set_color(car1_side.main_color)
        num_of_rot[1].set_color(arrow.get_color())

        self.play(FadeIn(car1_side, shift = 3*RIGHT), run_time = 2)
        self.play(GrowFromCenter(arrow))
        self.play(Write(num_of_rot))
        self.wait(2)

        func = MathTex("f(x)", "=", "\\sin", "(", "1", "\\cdot", "x", ")")
        func.next_to(num_of_rot, UP)
        func[4].set_color(car1_side.main_color)

        self.play(Write(func))
        self.play(
            *[Circumscribe(mob, run_time = 3, fade_out=True, color = car1_side.main_color) for mob in [num_of_rot[0], func[4]]]
        )
        self.wait(2)

    def infos_about_car2(self):
        axes = self.axes

        car2 = get_car(main_color = CAR2_COLOR, height = self.car_height)
        car2.shift(self.start_point + car2.center)
        car2.shift(2*DOWN)

        dot = Dot(self.start_point, color = CAR2_COLOR)

        self.play(DrawBorderThenFill(car2), run_time = 2)
        self.play(
            car2.animate.shift(2*UP),
            dot.animate.move_to(self.origin),
            run_time = 2
        )
        self.wait()


        car2_side = self.get_car_side_view(car_width = 1.5, main_color = GREEN)
        car2_side.to_corner(DL).shift(RIGHT)

        arrow = DoubleArrow(axes.c2p(0, -1.5), axes.c2p(2*PI, -1.5), color = GREY, buff = 0)

        num_of_rot = MathTex("2", "\\ \\text{Umdrehungen}")
        num_of_rot.next_to(arrow, DOWN, buff = 0)
        num_of_rot[0].set_color(car2_side.main_color)
        num_of_rot[1].set_color(arrow.get_color())


        self.play(FadeIn(car2_side, shift = 3*RIGHT), run_time = 2)
        self.play(GrowFromCenter(arrow))
        self.play(Write(num_of_rot))
        self.wait()

        self.car2, self.car2_side, self.arrow2, self.num_of_rot2 = car2, car2_side, arrow, num_of_rot

    def draw_curve_for_car2_with_twice_speed(self):
        street, car1, car2, axes = self.street, self.car1, self.car2, self.axes

        self.t_offset = 0
        def update_car2(mob, dt):
            self.t_offset += 0.5*dt                                                 # Change: 0.5 removed
            mob.rotate(self.velo2 * dt, about_point = street.get_center())

        def get_car_to_graph_line():
            x = 0.5*self.t_offset
            y = np.sin(2*x)
            return DashedLine(car2[4:].get_center(), axes.c2p(x,y), color=CAR2_COLOR)

        sin2 = VGroup()
        sin2.add(Line(self.origin, self.origin, color = CAR2_COLOR))
        def get_curve():
            last_line = sin2[-1]
            x = 0.5*self.t_offset
            y = np.sin(2*x)
            new_line = Line(last_line.get_end(), axes.c2p(x,y), color = CAR2_COLOR)
            sin2.add(new_line)

            return sin2

        car2.add_updater(update_car2)
        car1.resume_updating()
        car_to_graph_line = always_redraw(get_car_to_graph_line)
        sin2_curve = always_redraw(get_curve)
        self.add(car_to_graph_line, sin2_curve)
        self.wait(4*PI)

        final_graph = axes.get_graph(lambda x: np.sin(2*x), x_range=[0, TAU], color = CAR2_COLOR)

        car1.suspend_updating()
        self.remove(car_to_graph_line, sin2_curve)
        self.add(final_graph)
        self.wait(self.dt)
        car2.suspend_updating()
        self.wait(2)

        func = MathTex("f(x)", "=", "\\sin", "(", "2", "\\cdot", "x", ")")
        func.next_to(self.num_of_rot2, DOWN)
        func[4].set_color(self.car2_side.main_color)

        self.play(Write(func))
        self.wait()

        self.play(
            *[Circumscribe(mob, run_time = 4, fade_out=True, color = self.car2_side.main_color) for mob in [self.num_of_rot2[0], func[4]]]
        )
        self.wait(3)


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


class GraphsAtDifferentVelos(Scene):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50

        self.par = 2
        self.velo2 = self.par * self.velo1
        self.car2_color = PURPLE

        self.setup_scene()
        self.let_them_drive()

    def setup_scene(self):
        street, axes= self.street, self.axes

        start_point = street[1][0].get_start()  #   street[1] --> DashedLine --> street[1][0] --> first segment
        car1 = get_car(main_color = CAR1_COLOR, height = self.car_height)
        car1.shift(start_point + car1.center)

        car2 = get_car(main_color = self.car2_color, height = self.car_height)
        car2.shift(start_point + car2.center)
        x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        self.add(street, car1, car2, axes, x_numbers, y_numbers)
        self.wait(2)
        self.car1, self.car2, self.start_point = car1, car2, start_point

    def let_them_drive(self):
        street, car1, car2, axes = self.street, self.car1, self.car2, self.axes

        # Updater for both cars
        self.t_offset = 0
        def update_car1(mob, dt):
            self.t_offset += 0.5 * dt
            mob.rotate(self.velo1 * dt, about_point = street.get_center())

        def update_car2(mob, dt):
            self.t_offset += 0.5 * dt
            mob.rotate(self.velo2 * dt, about_point = street.get_center())

        # Updater for both car_graph_lines
        def get_car1_to_graph_line():
            x = 0.5 * self.t_offset
            y = np.sin(x)
            return DashedLine(car1[4:].get_center(), axes.c2p(x,y), color=CAR1_COLOR)

        def get_car2_to_graph_line():
            x = 0.5 * self.t_offset
            y = np.sin(self.par*x)
            return DashedLine(car2[4:].get_center(), axes.c2p(x,y), color=self.car2_color)

        # both Curves
        sin_ref = VGroup()
        sin_ref.add(Line(self.origin, self.origin, color = CAR1_COLOR))
        def get_ref_curve():
            last_line = sin_ref[-1]
            x = 0.5 * self.t_offset
            y = np.sin(x)
            new_line = Line(last_line.get_end(), axes.c2p(x,y), color = CAR1_COLOR)
            sin_ref.add(new_line)

            return sin_ref

        sin_par = VGroup()
        sin_par.add(Line(self.origin, self.origin, color = self.car2_color))
        def get_par_curve():
            last_line = sin_par[-1]
            x = 0.5 * self.t_offset
            y = np.sin(self.par*x)
            new_line = Line(last_line.get_end(), axes.c2p(x,y), color = self.car2_color)
            sin_par.add(new_line)

            return sin_par


        car1.add_updater(update_car1)
        car2.add_updater(update_car2)
        car1_to_graph_line = always_redraw(get_car1_to_graph_line)
        car2_to_graph_line = always_redraw(get_car2_to_graph_line)
        sin_ref_curve = always_redraw(get_ref_curve)
        sin_par_curve = always_redraw(get_par_curve)
        self.add(car1_to_graph_line, car2_to_graph_line, sin_ref_curve, sin_par_curve)
        self.wait(4*PI)


        graph_ref = axes.get_graph(lambda x: np.sin(x), x_range = [0, 2*PI], color = CAR1_COLOR)
        graph_par = axes.get_graph(lambda x: np.sin(self.par *x), x_range = [0, 2*PI], color = self.car2_color)


        car1.remove_updater(update_car1)
        self.wait(2*self.dt)
        car2.remove_updater(update_car2)
        self.remove(car1_to_graph_line, car2_to_graph_line, sin_ref_curve, sin_par_curve)
        self.add(graph_ref, graph_par)
        self.wait(3)


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


class Graph05TimesSpeed(GraphsAtDifferentVelos):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50

        self.par = 0.5
        self.velo2 = self.par * self.velo1
        self.car2_color = parameter_to_color(0.5, -2, 4, [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE])

        self.setup_scene()
        self.let_them_drive()


class Graph3TimesSpeed(GraphsAtDifferentVelos):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50
        self.car2_color = YELLOW

        self.par = 3
        self.velo2 = self.par * self.velo1

        self.setup_scene()
        self.let_them_drive()


class Graph4TimesSpeed(GraphsAtDifferentVelos):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50

        self.par = 4
        self.velo2 = self.par * self.velo1
        self.car2_color = BLUE

        self.setup_scene()
        self.let_them_drive()


class Graph8TimesSpeed(GraphsAtDifferentVelos):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50

        self.par = 8
        self.velo2 = self.par * self.velo1

        self.setup_scene()
        self.let_them_drive()


class GraphNegative2TimesSpeed(GraphsAtDifferentVelos):
    def construct(self):
        self.fps = 60
        self.dt = 1/self.fps

        self.street = get_street(radius = 1.5, thickness = 0.25)
        self.street.to_edge(LEFT)

        self.axes_kwargs = {
            "x_range": [0, 9*np.pi/4, 0.5], "y_range": [-1.25, 1.25, np.pi/4], 
            "x_length": 8, "y_length": 3.75, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.next_to(self.street, RIGHT, buff = 1)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.car_height = 0.5
        self.velo1 = 0.50

        self.par = -2
        self.velo2 = self.par * self.velo1
        self.car2_color = PURPLE

        self.setup_scene()
        self.let_them_drive()


class ParameterInfluence(Scene):
    def construct(self):

        self.axes_kwargs = {
            "x_range": [-3*PI/2, 9*PI/2, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 0}
        }
        self.axes = NumberPlane(**self.axes_kwargs).shift(UP)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.x_min = -3*PI/2
        self.x_max = 9*PI/2
        self.b_val = ValueTracker(1)

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]

        self.setup_scene(animate = True)
        self.b_is_bigger_than_1()
        self.clarify_parameter_influence()


    def setup_scene(self, animate = False):
        axes, b_val = self.axes, self.b_val

        axes_ticks = self.get_ticks()
        x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()
        b_line = self.b_line = self.get_b_line()
        b_arrow = always_redraw(lambda: self.get_b_arrow())

        func = MathTex("f(x)", "=", "\\sin", "(", "parai", "\\cdot", "x", ")")\
            .scale(1.4)\
            .to_edge(UP)\
            .shift(RIGHT)
        func[4].set_stroke(width = 0).set_fill(opacity = 0)

        b_dec_func = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)
        b_dec_func.scale(1.4).move_to(func[4]).align_to(func[5:7], DOWN)
        b_dec_func.add_updater(lambda dec:
            dec.set_value(b_val.get_value()).set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
        )

        b_tex_line = MathTex("b", "=")
        b_tex_line.add_updater(lambda btex: btex.next_to(b_arrow, UP).shift(0.5*LEFT))
        b_dec_line = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)
        b_dec_line.add_updater(lambda dec: 
            dec.set_value(b_val.get_value())\
                .next_to(b_tex_line, RIGHT, aligned_edge = DOWN)\
                .set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
        )


        graph_ref_bg = axes.get_graph(
            lambda x: np.sin(x), 
            x_range = [self.x_min, self.x_max], 
            color = CAR1_COLOR, stroke_opacity = 0.3
        )
        graph_par_bg = always_redraw(lambda: axes.get_graph(
            lambda x: np.sin(b_val.get_value() * x), 
            x_range = [self.x_min, self.x_max], 
            color = parameter_to_color(b_val.get_value(), -2, 4, self.colors), 
            stroke_opacity = 0.3
        ))
        graph_par_2pi = always_redraw(lambda: axes.get_graph(
            lambda x: np.sin(b_val.get_value() * x), 
            x_range = [0, 2*PI],
            color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
        ))
        graph_par_per = always_redraw(lambda: axes.get_graph(
            lambda x: np.sin(b_val.get_value() * x), 
            x_range = [0, 2*PI/abs(b_val.get_value())], 
            color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
        ))

        self.add(axes, axes_ticks, x_numbers, y_numbers)
        self.add(graph_ref_bg, graph_par_bg, graph_par_2pi)
        self.add(func, b_dec_func)
        self.add(b_line, b_arrow, b_tex_line, b_dec_line)

        if animate is True:
            self.play(
                AnimationGroup(
                    Create(axes), 
                    FadeIn(axes_ticks, shift = 0.5*UP, lag_ratio = 0.1),
                    FadeIn(x_numbers),
                    FadeIn(y_numbers, shift = 0.5*RIGHT), 
                    Create(VGroup(graph_ref_bg, graph_par_bg)), 
                    Create(graph_par_2pi), 
                    Create(func), 
                    FadeIn(b_dec_func, shift = 0.5*UP),
                    Create(VGroup(b_line, b_arrow, b_tex_line, b_dec_line), lag_ratio = 0.1),
                    lag_ratio = 0.1
                ),
                run_time = 4
            )
            self.wait()

        self.graph_par_2pi, self.graph_par_per = graph_par_2pi, graph_par_per
        self.b_dec_line = b_dec_line
        self.b_dec_func, self.func = b_dec_func, func

    def b_is_bigger_than_1(self):
        b_val = self.b_val

        self.play(b_val.animate.set_value(2), run_time = 4)
        dlines2 = self.get_vert_dlines(2)
        self.play(FadeIn(dlines2, shift = UP))
        self.wait()
        self.play(dlines2.animate.shift(self.axes.x_axis.unit_size * PI * RIGHT))
        self.wait()


        dlines4 = self.get_vert_dlines(4)
        self.play(
            b_val.animate(run_time = 4).set_value(4),
            ReplacementTransform(dlines2, dlines4, run_time = 4), 
        )
        for x in range(3):
            self.play(dlines4.animate.shift(self.axes.x_axis.unit_size * PI/2 * RIGHT))
        self.wait(3)

        self.play(
            FadeOut(dlines4, run_time = 1),
            b_val.animate(run_time = 4).set_value(1),
        )
        self.wait()

    def clarify_parameter_influence(self):
        b_val = self.b_val

        cases_math = VGroup(*[
            MathTex(*tex, color = DARK_GREY) for tex in [["b", ">", "1", ":"], ["0", "<", "b", "<", "1", ":"], ["b", "<", "0", ":"]]
        ])
        cases_math.arrange_submobjects(DOWN, buff = 0.5, aligned_edge = RIGHT)
        cases_math.to_corner(DR)
        cases_math.shift(4*LEFT + 0.5*UP)

        text1 = Tex("Stauchung")
        text2 = Tex("Streckung")
        text3 = Tex("zusätzliche", "\\\\ Spiegelung")
        for text, math in zip([text1, text2, text3], cases_math):
            text.next_to(math, RIGHT, aligned_edge = UP)
            text.set_color(DARK_GREY)

        def update_bval_bigger_1(mob):
            if abs(b_val.get_value()) > 1:
                mob.set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
            else:
                mob.set_color(DARK_GREY)

        def update_bval_between01(mob):
            if 0 < abs(b_val.get_value()) < 1:
                mob.set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
            else:
                mob.set_color(DARK_GREY)

        def update_bval_neg(mob):
            if b_val.get_value() < 0:
                mob.set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
            else:
                mob.set_color(DARK_GREY)

        cases_math[0].add_updater(update_bval_bigger_1)
        cases_math[1].add_updater(update_bval_between01)
        cases_math[2].add_updater(update_bval_neg)
        text1.add_updater(update_bval_bigger_1)
        text2.add_updater(update_bval_between01)
        text3.add_updater(update_bval_neg)


        b_values = [1.5, 3, 1, 0.5, 0.25, 0, -0.25, -2, -1, 1]
        for b in b_values:
            self.play(b_val.animate.set_value(b), run_time = 3)
            self.wait()

            if b == 1.5:
                self.play(Write(cases_math[0]))
                self.play(Write(text1))
                self.wait()

            if b == 0.5:
                self.play(Write(cases_math[1]))
                self.play(Write(text2))
                self.wait()

            if b == -0.25:
                self.play(Write(cases_math[2]))
                self.play(Write(text3))
                self.wait()

        self.wait()


        # self.play(b_val.animate.set_value(1), run_time = 4)
        # self.wait(2)

        # self.play(b_val.animate.set_value(0.5), run_time = 4)
        # self.wait(2)

        # self.play(b_val.animate.set_value(0.1), rate_func = linear, run_time = 2)
        # b_val.set_value(-0.1)
        # self.wait()
        # self.play(b_val.animate.set_value(-2), rate_func = linear, run_time = 2)
        # self.wait(2)


    # functions
    def get_ticks(self):
        ticks = VGroup()
        for x in [-PI, -1/2*PI, PI/2, PI, 3/2*PI, 2*PI, 5/2*PI, 3*PI, 7/2*PI, 4*PI]:
            tick = Line(DOWN, UP, color = LIGHT_GREY)
            tick.set_length(0.15)
            tick.move_to(self.axes.c2p(x, 0))
            ticks.add(tick)

        return ticks

    def get_x_axis_numbers(self):
        x_axis_nums = [-PI, -1/2*PI, PI/2, PI, 3/2*PI, 2*PI, 5/2*PI, 3*PI, 7/2*PI, 4*PI]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                ["-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi", "5\\pi/2", "3\\pi", "7\\pi/2", "4\\pi"], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_y_axis_numbers(self):
        y_axis_nums = [-1,1]
        y_axis_coords = VGroup(*[
            MathTex(num, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for num in y_axis_nums
        ])
        return y_axis_coords

    def get_b_line(self):
        b_line = NumberLine(x_range = [-2, 4], length = 5.5, include_numbers = True)\
            .to_edge(LEFT, buff = 1)\
            .shift(3*DOWN)
        return b_line

    def get_p_line(self):
        p_line = NumberLine(x_range = [0, 4*PI, PI/2], length = 5.5)\
            .to_edge(RIGHT, buff = 1)\
            .shift(3*DOWN)
        
        return p_line

    def get_p_line_numbers(self):
        p_line_nums = [0, PI, 2*PI, 3*PI, 4*PI]
        p_line_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 36)\
                .next_to(self.p_line.n2p(num), DOWN)
            for tex, num in zip(
                ["0", "\\pi", "2\\pi", "3\\pi", "4\\pi"],
                p_line_nums
            )
        ])

        return p_line_coords

    def get_b_arrow(self):
        b_line, b_val = self.b_line, self.b_val
        b_arrow = Arrow(
            b_line.n2p(b_val.get_value()) + 0.60*UP, 
            b_line.n2p(b_val.get_value()),
            buff = 0, 
            color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
        )
        return b_arrow

    def get_p_arrow(self):
        p_line, b_val = self.p_line, self.b_val
        p_arrow = Arrow(
            p_line.n2p(2*PI/abs(b_val.get_value())) + 0.60*UP, 
            p_line.n2p(2*PI/abs(b_val.get_value())), 
            buff = 0, 
            color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
        )
        return p_arrow

    def get_vert_dlines(self, num):
        axes = self.axes
        width = 2*PI / num

        dline1 = DashedLine(axes.c2p(0, 1), axes.c2p(0,-1.35), color = WHITE)
        dline2 = DashedLine(axes.c2p(width, 1), axes.c2p(width, -1.35), color = WHITE)

        dlines = VGroup(dline1, dline2)
        return dlines


class PropertiesList(Scene):
    def construct(self):
        funcs = VGroup(*[
            MathTex(*tex, font_size = 60) for tex in [
                ["y", "=", "\\sin(x)"], 
                ["y", "=", "\\sin", "(", "b", "\\cdot", "x", ")"]
            ]
        ])
        funcs.arrange_submobjects(RIGHT, buff = 5)
        funcs.to_edge(UP, buff = 1)
        funcs[1][4].set_color(BLUE)

        ulines = VGroup(*[
            Underline(mob, color = color) for mob, color in zip([funcs[0], funcs[1]], [RED, BLUE])
        ])

        properties1 = VGroup(*[
            Tex(tex) for tex in [
                "Definitionsbereich", 
                "Wertebereich",
                "Nullstellen", 
                "Periode", 
            ]
        ])

        properties1.arrange_submobjects(DOWN, buff = 0.75, aligned_edge = LEFT)
        properties1.next_to(funcs[0], DOWN, buff = 1)

        properties2 = properties1.copy()
        properties2.arrange_submobjects(DOWN, buff = 0.75, aligned_edge = RIGHT)
        properties2.next_to(funcs[1], DOWN, buff = 1)
        properties2[:2].set_color(RED)
        properties2[2:].set_color(GREEN)

        self.play(
            FadeIn(funcs, shift = DOWN, lag_ratio = 0.5),
            Create(ulines, lag_ratio = 0.5),
            run_time = 2
        )
        self.play(FadeIn(properties1, shift = RIGHT, lag_ratio = 0.5), run_time = 2)
        self.wait(2)

        self.play(
            AnimationGroup(
                *[Transform(properties1[index], properties2[index]) for index in range(len(properties1))], 
                lag_ratio = 0.5
            ),
            run_time = 3
        )
        self.wait()


        sur_rect = SurroundingRectangle(properties1[2:], color = BLUE)
        self.play(FadeIn(sur_rect, scale = 1.5))
        self.wait()


        frame = ScreenRectangle(height = 4, color = GREY, stroke_width = 2)\
            .to_edge(LEFT)\
            .shift(DOWN)
        frame_title = Tex("Nächstes Video")\
            .next_to(frame, UP)

        self.play(Write(frame_title))
        self.play(TransformFromCopy(sur_rect, frame), run_time = 1.5)
        self.wait(3)


class Period(ParameterInfluence):
    def construct(self):
        self.axes_kwargs = {
            "x_range": [-3*PI/2, 9*PI/2, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 0}
        }
        self.axes = NumberPlane(**self.axes_kwargs).shift(UP)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.x_min = -3*PI/2
        self.x_max = 9*PI/2
        self.b_val = ValueTracker(1)

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]

        self.setup_scene(animate = False)
        self.remove(self.graph_par_2pi)
        self.add(self.graph_par_per)
        self.wait()
        self.add_period_infos()


    def add_period_infos(self):
        axes, b_val = self.axes, self.b_val


        p_line = self.p_line = self.get_p_line()
        p_line_nums = self.get_p_line_numbers()
        p_arrow = always_redraw(lambda: self.get_p_arrow())
        p_tex_line = MathTex("p")
        p_tex_line.add_updater(lambda ptex: ptex.next_to(p_arrow, UP))

        self.play(
            LaggedStartMap(
                Create, VGroup(p_line, p_line_nums, p_arrow, p_tex_line), lag_ratio = 0.15
            ),
            run_time = 3
        )
        self.wait(2)


        arrow_period = always_redraw(lambda: 
            DoubleArrow(axes.c2p(0, -1.25), axes.c2p(2*PI/abs(b_val.get_value()), -1.25), buff = 0, color = GREY, stroke_width = 3)
        )

        per_tex = MathTex("p", "\\approx")\
            .scale(0.8)\
            .add_updater(lambda p: p.next_to(arrow_period, DOWN, buff = 0.2))

        per_dec = DecimalNumber(2*np.pi / abs(b_val.get_value()))\
            .scale(0.8)\
            .add_updater(lambda dec: dec.set_value(2*np.pi / abs(b_val.get_value())).next_to(per_tex, RIGHT).shift(0.1*UP))
        per_end_line = always_redraw(lambda: DashedLine(arrow_period.get_end(), axes.c2p(2*np.pi / abs(b_val.get_value()), 0), color = GREY, stroke_width = 3))


        self.play(
            GrowFromCenter(arrow_period), 
            FadeIn(VGroup(per_tex, per_dec), shift = 0.5*UP), 
        )
        self.play(Create(per_end_line))
        self.play(
            Circumscribe(per_dec, color = YELLOW, run_time = 3),
            Circumscribe(p_line_nums[2], color = YELLOW, run_time = 3),
        )
        self.wait()


        b_values = [2, 0.5, -2, -1]
        for b in b_values:
            self.play(b_val.animate.set_value(b), run_time = 4)
            self.wait()

            if b == 2:
                graph_copy = self.graph_par_per.copy()
                graph_copy.clear_updaters()
                self.play(
                    ApplyMethod(graph_copy.shift, PI * axes.x_axis.unit_size * RIGHT, path_arc = 2, rate_func = there_and_back), 
                    run_time = 4
                )
                self.remove(graph_copy)
                self.wait()
                self.play(
                    Circumscribe(per_dec, color = YELLOW, run_time = 3),
                    Circumscribe(p_line_nums[1], color = YELLOW, run_time = 3),
                )
                self.wait()

            if b == 0.5:
                self.play(
                    Circumscribe(per_dec, color = YELLOW, run_time = 3),
                    Circumscribe(p_line_nums[-1], color = YELLOW, run_time = 3),
                )
                self.wait(3)

                periode_final = MathTex("p", "=", "{2", "\\pi", "\\over", "\\vert b\\vert", "}", font_size = 60)
                periode_final.to_edge(UP).shift(5*LEFT)
                periode_final.add_background_rectangle()
                self.add(periode_final)
                b_val.set_value(-0.5)
                self.wait(3)

                self.play(Circumscribe(self.b_dec_line, color = YELLOW, run_time = 3))
                self.play(ApplyWave(self.graph_par_per), run_time = 2)
                self.wait()
                self.play(
                    Circumscribe(per_dec, color = YELLOW, run_time = 3),
                    Circumscribe(p_line_nums[-1], color = YELLOW, run_time = 3),
                )

        self.wait(3)


class PeriodGeneralize(Scene):
    def construct(self):
        color1 = parameter_to_color(2.0, -2, 4, [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE])
        color2 = parameter_to_color(0.5, -2, 4, [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE])
        funcs = VGroup(*[
            MathTex(*tex, font_size = 60) for tex in [
                ["y", "=", "\\sin", "(", "2", "\\cdot", "x", ")"], 
                ["y", "=", "\\sin", "(", "0.5", "\\cdot", "x", ")"]
            ]
        ])
        funcs[0][4].set_color(color1)
        funcs[1][4].set_color(color2)

        funcs.arrange_submobjects(RIGHT, buff = 4)
        funcs.to_edge(UP, buff = 1)
        u_lines = VGroup(*[
            Underline(mob, color = color) for mob, color in zip(
                [funcs[0], funcs[1]], 
                [color1, color2]
            )
        ])

        self.play(
            Write(funcs), 
            Create(u_lines), 
        )
        self.wait()

        p1 = MathTex("p", "=", "{2", "\\pi", "\\over", "2}", "=", "\\pi", font_size = 60)
        p1.next_to(funcs[0], DOWN, buff = 1)
        p1[-3].set_color(color1)

        self.play(Write(p1[:5]))
        self.play(TransformFromCopy(funcs[0][4], p1[-3], path_arc = 2), run_time = 2)
        self.play(Write(p1[-2:]))
        self.wait()


        p2_start = MathTex("p", "=", "2", "\\pi", "\\cdot", "2", font_size = 60)
        p2_start.next_to(funcs[1], DOWN, buff = 1)
        self.play(Write(p2_start))
        self.wait(2)

        p2_final = MathTex("p", "=", "{2", "\\pi", "\\over", "0.5}", "=", "4\\pi", font_size = 60)
        p2_final.next_to(funcs[1], DOWN, buff = 1)
        p2_final[-3].set_color(color2)

        self.play(Transform(p2_start, p2_final[:5]))
        self.play(TransformFromCopy(funcs[1][4], p2_final[-3], path_arc = 2), run_time = 2)
        self.play(Write(p2_final[-2:]))
        self.wait(3)


        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = YELLOW) for mob in [p1[:-2], p2_final[:-2]]
        ])
        self.play(Create(sur_rects, lag_ratio = 0.4), run_time = 2)
        self.wait()

        periode_start = MathTex("p", "=", "{2", "\\pi", "\\over", "b", "}", font_size = 60)
        periode_final = MathTex("p", "=", "{2", "\\pi", "\\over", "\\vert b\\vert", "}", font_size = 60)
        for tex in periode_start, periode_final:
            tex.shift(2*DOWN)
        rect_final1 = SurroundingRectangle(periode_final, color = RED, buff = 0.5)
        rect_final2 = rect_final1.copy()

        self.play(
            Transform(sur_rects[0], rect_final1), 
            Transform(sur_rects[1], rect_final2), 
            run_time = 2
        )
        self.play(Write(periode_start))
        self.wait(2)

        self.play(ReplacementTransform(periode_start, periode_final))
        self.wait(3)


        periode_final.generate_target()
        periode_final.target.to_edge(UP).shift(5*LEFT)

        other_stuff = Group(*[x for x in self.mobjects if x != periode_final])
        self.play(
            FadeOut(other_stuff), 
            MoveToTarget(periode_final), 
            run_time = 3
        )
        self.wait(3)


class Thumbnail(Scene):
    def construct(self):
        radius = 2
        street = get_street(radius = radius, thickness=0.375)
        street.shift(3.5*LEFT)



        def par_func(b, t):
            return np.array([(radius + 1 + 0.25*np.cos(b * t))*np.cos(t), (radius + 1 + 0.25*np.cos(b * t))*np.sin(t), 0])

        graphs_parametric = VGroup(*[
            ParametricFunction(lambda t: par_func(b, t), t_range = np.array([0, TAU]), color = color, stroke_opacity = 0.5)
            for b, color in zip([4, 6, 8, 10], [RED, GREEN, YELLOW, BLUE])
        ])
        graphs_parametric.shift(3.5*LEFT)


        def par_func_inner(t, r):
            return np.array([(r + 0.05*np.cos(20 * t))*np.cos(t), (r + 0.05*np.cos(20 * t))*np.sin(t), 0])

        graphs_inner = VGroup(*[
            ParametricFunction(lambda t: par_func_inner(t, r), t_range = np.array([0, TAU]), color = color, stroke_opacity = 0.5)
            for r, color in zip([0.333, 0.666, 1, 1.3333], [GREY_B, GREY_C, GREY_D, GREY_E])
        ])
        graphs_inner.shift(3.5*LEFT)


        cars = VGroup(*[
            get_car(main_color = color, height = 1).move_to(street.dline.point_from_proportion(prop)).rotate(angle)
            for color, prop, angle in zip([RED, GREEN, YELLOW, BLUE], [0, 0.25, 0.5, 0.75], [0, PI/2, PI, 3*PI/2])
        ])
        cars.shift(3.5*LEFT)

        func_tex = MathTex("\\sin", "(", "b", "\\cdot", "x", ")")\
            .scale(3)\
            .set_color(LIGHT_GREY)\
            .add_background_rectangle()\
            .to_corner(UR)\
            .shift(0.5*LEFT)
        func_tex[3].set_color([GREEN, YELLOW, BLUE, BLUE])

        def func(b, t):
            return np.array([t, np.sin(b*t), 0])
        graphs = VGroup(*[
            ParametricFunction(lambda t: func(b, t), t_range = np.array([0, TAU]), color = color).scale(0.75).stretch_to_fit_height(1)
            for b, color in zip([1, 2, 3, 4], [RED, GREEN, YELLOW, BLUE])
        ])
        graphs.arrange_submobjects(DOWN)
        graphs.next_to(func_tex, DOWN)


        self.add(street, graphs_inner, graphs_parametric, cars, graphs, func_tex)




# SECOND VIDEO

class IntroDrawing(Scene):
    def construct(self):
        func = MathTex("f(x)", "=", "\\sin", "(", "b", "\\cdot", "x", ")", font_size = 90)
        func[4].set_color(RED)
        
        frame = ScreenRectangle(height = 5.75, stroke_width = 3, color = GREY)\
            .to_edge(DOWN)

        self.play(Write(func), run_time = 1.5)
        self.wait()

        self.play(func.animate.to_edge(UP), run_time = 2)
        self.play(Create(frame), run_time = 3)
        self.wait(3)


class HowToDrawGraphs(ParameterInfluence, MovingCameraScene):
    def construct(self):
        self.axes_kwargs = {
            "x_range": [-3*PI/2, 9*PI/2, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.x_min = -3*PI/2
        self.x_max = 9*PI/2
        self.b_val = ValueTracker(2)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]


        self.scene_setup()
        self.period_from_parameter()
        self.zoom_in()
        self.mid_and_extrema()
        self.shift_frame()
        self.draw_next_period()
        self.zoom_out_draw_curve()


    def scene_setup(self):
        axes, b_val = self.axes, self.b_val

        axes_ticks = self.get_ticks()
        x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        func = MathTex("f(x)", "=", "\\sin", "(", "parai", "\\cdot", "x", ")")\
            .scale(1.4)\
            .to_edge(UP)\
            .shift(RIGHT)
        func[4].set_stroke(width = 0).set_fill(opacity = 0)

        b_dec_func = self.b_dec_func = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)
        b_dec_func.scale(1.4).move_to(func[4]).align_to(func[5:7], DOWN)
        b_dec_func.add_updater(lambda dec:
            dec.set_value(b_val.get_value()).set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
        )

        self.play(
            AnimationGroup(
                Create(axes),
                FadeIn(axes_ticks, shift = 0.5*UP, lag_ratio = 0.1),
                FadeIn(x_numbers, shift = 0.5*RIGHT, lag_ratio = 0.1), 
                FadeIn(y_numbers, shift = RIGHT),
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.play(
            AnimationGroup(
                Create(func), 
                FadeIn(b_dec_func, shift = 0.5*DOWN),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()

        self.play(Circumscribe(b_dec_func, color = YELLOW, run_time = 2, fade_out = True))
        b_dec_func.suspend_updating()
        b_val.set_value(1)
        self.wait()

        self.x_numbers = x_numbers

    def period_from_parameter(self):
        b_val, axes = self.b_val, self.axes

        x_mark0 = always_redraw(lambda: 
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=parameter_to_color(b_val.get_value(), -2, 4, self.colors))\
                .move_to(self.origin)
        )
        x_mark1 = always_redraw(lambda: 
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=parameter_to_color(b_val.get_value(), -2, 4, self.colors))\
                .move_to(axes.c2p(2*PI / b_val.get_value(), 0))
        )

        # BRACE & P-TEX
        brace = always_redraw(lambda: Brace(Line(x_mark0.get_center(), x_mark1.get_center()), UP, color = GREY))

        p_tex = MathTex("p", "\\approx")
        p_tex.add_updater(lambda p: p.next_to(brace, UP, buff = 0.2))

        p_dec = DecimalNumber(2*PI / abs(b_val.get_value()))
        p_dec.add_updater(lambda dec: dec.set_value(2*PI / abs(b_val.get_value())).next_to(p_tex, RIGHT).shift(0.1*UP))

        # p_bg = BackgroundRectangle(VGroup(p_tex, p_dec), buff = 0.1)
        # p_bg.add_updater(lambda bg: bg.next_to(brace, UP, buff = 0.2))

        self.play(
            LaggedStartMap(DrawBorderThenFill, VGroup(x_mark0, x_mark1), lag_ratio = 0.35), 
            run_time = 1.5
        )
        self.play(Create(brace))
        self.play(Write(p_tex), Write(p_dec))

        graph_b = self.get_graph_b(stroke_opacity = 0.5)
        self.play(Create(graph_b), run_time = 3)
        self.bring_to_front(brace, p_tex, p_dec)
        self.wait()

        self.play(Circumscribe(VGroup(p_tex, p_dec), color = YELLOW, run_time = 3))
        self.wait()

        b_values = [1.75, 0.5, 2, 2*PI/3, PI/5, 1]
        for b in b_values:
            self.play(b_val.animate.set_value(b), run_time = 3)
            self.wait()
        self.wait()


        p_dec.clear_updaters()
        self.play(
            AnimationGroup(
                Uncreate(brace),
                Unwrite(p_dec),
                Unwrite(p_tex),
                Uncreate(graph_b), 
                lag_ratio = 0.25
            ),
            run_time = 1.5
        )
        self.remove(p_dec)
        self.wait()
        self.play(Circumscribe(x_mark0, shape = Circle, time_width = 0.75))
        self.play(DrawBorderThenFill(x_mark0))
        self.wait()

        self.play(Circumscribe(x_mark1, shape = Circle, time_width = 0.75, run_time = 2))
        self.wait()


        p_eq = MathTex("p", "=", "{2", "\\pi", "\\over", "\\vert", "b", "\\vert}")\
            .scale(1.5)\
            .to_edge(DOWN)\
            .set_color_by_tex_to_color_map({"b": parameter_to_color(2, -2, 4, self.colors)})
        self.play(FadeIn(p_eq, shift = 3*UP), run_time = 3)
        self.play(Indicate(p_eq), run_time = 2)
        self.wait()

        tex_p = Tex("Periode")\
            .scale(1.4)\
            .next_to(p_eq, LEFT)
        tex_b = Tex("Parameter")\
            .scale(1.4)\
            .next_to(p_eq[-1], RIGHT)
        arc = ArcBetweenPoints(tex_b.get_top(), tex_p.get_top(), angle = TAU/2).add_tip()
        self.play(FadeIn(tex_p, shift = 3*RIGHT))
        self.wait(0.5)
        self.play(FadeIn(tex_b, shift=3*LEFT))
        self.play(Create(arc), run_time = 2)
        self.wait(2)

        self.play(LaggedStartMap(FadeOut, VGroup(arc, tex_b, tex_p), lag_ratio = 0.25), run_time = 2)
        self.wait()

        p_eq_calc = MathTex("=", "{2", "\\pi", "\\over", "\\vert", "2", "\\vert}")
        p_eq_calc.scale(1.5).next_to(p_eq, RIGHT)
        p_eq_calc[-2].set_color(parameter_to_color(2, -2, 4, self.colors))
        self.play(TransformFromCopy(p_eq[1:], p_eq_calc), run_time = 2)
        self.wait()

        p_eq_result = MathTex("=", "\\pi")\
            .scale(1.5).next_to(p_eq_calc, RIGHT)
        self.play(Write(p_eq_result))
        self.wait()

        pi_axes = self.x_numbers[3].copy()
        self.play(
            b_val.animate.set_value(2),
            ReplacementTransform(p_eq_result[-1].copy(), pi_axes, path_arc = 1),
            run_time = 3
        )
        self.remove(pi_axes)
        self.wait(2)


        self.p_eq, self.p_eq_calc, self.p_eq_result = p_eq, p_eq_calc, p_eq_result
        self.x_mark0, self.x_mark1 = x_mark0, x_mark1

    def zoom_in(self):
        frame = self.frame = self.renderer.camera.frame
        frame.save_state()

        self.play(
            frame.animate.set(height = self.axes.height + 0.2).move_to(self.axes.c2p(PI/2, 0)), 
            FadeOut(VGroup(self.p_eq, self.p_eq_calc, self.p_eq_result), shift = DOWN, lag_ratio = 0.1), 
            run_time = 5
        )
        self.wait(2)

    def mid_and_extrema(self):
        axes, x_mark0, x_mark1= self.axes, self.x_mark0, self.x_mark1

        target_point = axes.c2p(PI/2, 0)
        x_mark05_0 = x_mark0.copy().move_to(target_point)
        x_mark05_1 = x_mark1.copy().move_to(target_point)

        self.play(
            FocusOn(target_point, run_time = 1.5),
            TransformFromCopy(x_mark0, x_mark05_0, run_time = 3), 
            TransformFromCopy(x_mark1, x_mark05_1, run_time = 3),
        )
        self.remove(x_mark05_1)
        self.wait()


        # EXTREMA
        x_mark25 = x_mark0.copy().move_to(axes.c2p(PI/4, 1))
        x_mark75 = x_mark0.copy().move_to(axes.c2p(3*PI/4, -1))

        arrows = VGroup(*[
            Arrow(
                axes.c2p(x, 0), axes.c2p(x, np.sin(2*x)), color = RED, buff = 0, 
                stroke_opacity = 0.5, stroke_width = 4, tip_length = 0.15, tip_style = {"fill_opacity": 0.5})
            for x in [PI/4, 3*PI/4]
        ])

        self.play(GrowArrow(arrows[0]), run_time = 3)
        self.play(DrawBorderThenFill(x_mark25, run_time = 1.5))
        self.wait()


        self.play(GrowArrow(arrows[1]), run_time = 3)
        self.play(DrawBorderThenFill(x_mark75, run_time = 1.5))
        self.wait()

        self.play(
            *[GrowArrow(arrows[index], rate_func = lambda t: smooth(1-5)) for index in [0,1]],
            # GrowArrow(arrows[0], rate_func = lambda t: smooth(1-t)),
            # GrowArrow(arrows[1], rate_func = lambda t: smooth(1-t)),
            run_time = 2 
        )

        graph_b = self.get_graph_b()
        self.play(Create(graph_b), run_time = 4)
        self.wait(3)


        self.x_mark25, self.x_mark05, self.x_mark75 = x_mark25, x_mark05_0, x_mark75

    def shift_frame(self):
        self.play(
            self.frame.animate.move_to(self.axes.c2p(PI, 0)), 
            run_time = 3
        )
        self.wait(2)

    def draw_next_period(self):
        new_x_marks = self.get_period_x_marks()
        self.add(new_x_marks)

        self.play(
            ApplyMethod(new_x_marks.shift, self.axes.x_axis.unit_size * RIGHT * PI, path_arc = -1),
            run_time = 4
        )

        arrows = VGroup(*[
            Arrow(
                start = self.axes.c2p(x, np.sin(self.b_val.get_value() * x)), 
                end = self.axes.c2p(x + PI, np.sin(self.b_val.get_value() * x)), 
                buff = 0, color = RED, 
                stroke_width = 4, tip_length = 0.175
            )
            for x in [PI/4, 3*PI/4, PI]
        ])
        self.play(
            AnimationGroup(
                *[GrowArrow(arrow) for arrow in arrows],
                lag_ratio = 0.3
            ), 
            run_time = 5
        )
        self.wait(0.5)
        self.play(*[FadeOut(arrow) for arrow in arrows])
        self.wait()

        new_graph = self.axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), 
            x_range = [PI, 2*PI], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )
        self.play(Create(new_graph), run_time = 3)
        self.wait(3)

    def zoom_out_draw_curve(self):
        graph_left = self.axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), 
            x_range = [self.x_min, 0], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )
        graph_right = self.axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), 
            x_range = [2*PI, self.x_max], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )


        period = MathTex("p", "=", "{2\\pi", "\\over", "\\vert", "b", "\\vert}", "=", "\\pi")\
            .scale(1.25)\
            .to_edge(UL)\
            .set_color_by_tex_to_color_map({"b": parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)})
        period[-1].set_color(RED)

        brace = Brace(
            Line(self.axes.c2p(0, -1.35), self.axes.c2p(PI, -1.35)), 
            DOWN, color = RED
        )
        brace_tex = brace.get_tex("p").set_color(RED).scale(1.25)

        self.add(period, brace, brace_tex)

        self.play(
            AnimationGroup(
                Restore(self.frame),
                Create(graph_left), 
                Create(graph_right),
                lag_ratio = 0.25
            ),
            run_time = 5
        )
        self.wait(3)

    # functions
    def get_graph_b(self, **kwargs):
        graph_b = always_redraw(lambda: 
            self.axes.get_graph(
                lambda x: np.sin(self.b_val.get_value() * x),
                x_range=[0, 2*PI/abs(self.b_val.get_value())],
                color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors), 
                **kwargs
            )
        )

        return graph_b

    def get_period_x_marks(self):
        x_marks = VGroup(*[
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=parameter_to_color(self.b_val.get_value(), -2, 4, self.colors))\
                .move_to(self.axes.c2p(x, np.sin(self.b_val.get_value() * x)))
            for x in np.linspace(0, PI, 5)
        ])

        return x_marks


class HowToDrawGraphs2(ParameterInfluence, MovingCameraScene):
    def construct(self):
        self.axes_kwargs = {
            "x_range": [-3*PI/2, 9*PI/2, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)


        self.x_min = -4*PI/3 - 0.5
        self.x_max = 10*PI/3 + 0.5
        self.new_axes_kwargs = {
            "x_range": [self.x_min, self.x_max, 0.5], "y_range": [-1.25, 1.25, PI/3], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.new_axes = NumberPlane(**self.new_axes_kwargs)
        self.new_axes.x_axis.add_tip(tip_length = 0.25)
        self.new_axes.y_axis.add_tip(tip_length = 0.25)

        self.b_val = ValueTracker(2)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]

        self.setup_from_old_scene()
        self.new_parameter_new_period()
        self.switch_axes()
        self.drawing_curve()
        self.add_marks_for_full_graph()


    def setup_from_old_scene(self):
        b_val = self.b_val

        self.axes_ticks = self.get_ticks()
        self.x_numbers, self.y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        func = self.func = MathTex("f(x)", "=", "\\sin", "(", "parai", "\\cdot", "x", ")")\
            .scale(1.4)\
            .to_edge(UP)\
            .shift(RIGHT)
        func[4].set_stroke(width = 0).set_fill(opacity = 0)

        b_dec_func = self.b_dec_func = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)\
            .scale(1.4)\
            .move_to(func[4])\
            .align_to(func[5:7], DOWN)\
            .add_updater(lambda dec:
                dec.set_value(b_val.get_value()).set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
            )

        period = self.period = MathTex("p", "=", "{2\\pi", "\\over", "\\vert", "b", "\\vert}")\
            .scale(1.25)\
            .to_edge(UL)\
            .set_color_by_tex_to_color_map({"b": parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)})

        self.add(self.axes, self.axes_ticks, self.x_numbers, self.y_numbers)
        self.add(func, b_dec_func, period)
        self.wait(3)

    def new_parameter_new_period(self):
        b_val = self.b_val

        self.play(
            b_val.animate.set_value(-0.75),
            FadeToColor(self.period[-2], parameter_to_color(-0.75, -2, 4, self.colors)),
            run_time = 5
        )
        self.wait()

        new_b = MathTex("b", "=", "-", "\\frac{3}{4}")\
            .next_to(self.new_axes, DOWN, buff = 0.5)\
            .shift(3*LEFT)
        new_per = MathTex("p", "=", "{2\\pi", "\\over", "\\vert", "-\\frac{3}{4}", "\\vert}")\
            .next_to(new_b, RIGHT, buff = 1.5)\
            .set_color_by_tex_to_color_map({"-\\frac{3}{4}": parameter_to_color(b_val.get_value(), -2, 4, self.colors)})

        self.play(Write(new_b))
        self.wait()

        self.play(Circumscribe(self.period, color = RED, run_time = 3))
        self.wait(2)
        self.play(Write(new_per), run_time = 1.5)
        self.wait(2)

        new_per1 = MathTex("p", "=", "{2\\pi", "\\over", "\\frac{3}{4}", "}")\
            .next_to(new_b, RIGHT, buff = 1.5)\
            .set_color_by_tex_to_color_map({"\\frac{3}{4}": parameter_to_color(b_val.get_value(), -2, 4, self.colors)})

        self.play(ReplacementTransform(new_per[2:], new_per1[2:]))
        self.wait()

        new_per2 = MathTex("=", "2\\pi", "\\cdot", "\\frac{4}{3}")\
            .next_to(new_per1, RIGHT)\
            .set_color_by_tex_to_color_map({"-\\frac{3}{4}": parameter_to_color(b_val.get_value(), -2, 4, self.colors)})

        self.play(Write(new_per2[0]))
        self.wait()
        self.play(Write(new_per2[1]))
        self.wait(0.5)
        self.play(Write(new_per2[2]))
        self.wait(0.5)
        self.play(Write(new_per2[3:]))
        self.wait()

        new_per_final = MathTex("=", "\\frac{8\\pi}{3}")\
            .next_to(new_per2, RIGHT)
        self.play(Write(new_per_final[0]))
        self.wait()
        self.play(Write(new_per_final[1]))
        self.wait(0.5)
        self.play(Circumscribe(new_per_final[1], color = RED, fade_out = True, run_time = 3))
        self.wait(2)


        self.play(ApplyWave(self.x_numbers), run_time = 3)
        self.wait()

        self.fadeout_group = VGroup(
            new_b, new_per[:2], new_per1[2:], new_per2, new_per_final
        )

    def switch_axes(self):
        new_x_numbers = self.get_new_x_numbers()
        new_axes_ticks = self.get_new_ticks()
        self.play(
            ReplacementTransform(self.axes, self.new_axes),
            ReplacementTransform(self.x_numbers, new_x_numbers),
            ReplacementTransform(self.axes_ticks, new_axes_ticks),
            self.y_numbers.animate.shift(0.8*self.new_axes.x_axis.unit_size * RIGHT),
        )
        self.wait(1)

        new_per = MathTex("=", "\\frac{8\\pi}{3}")\
            .scale(1.25)\
            .next_to(self.period, RIGHT)
        self.play(
            FadeOut(self.fadeout_group), 
            Write(new_per),
            run_time = 2
        )
        self.wait(2)

    def drawing_curve(self):
        p_num = self.p_num = ValueTracker(1)
        p_arrow = always_redraw(lambda: self.get_period_double_arrow())
        p_texs = VGroup(*[
            MathTex(frac, "\\cdot", "p").move_to(self.new_axes.c2p(x, -1.95))
            for frac, x in zip(
                ["1", "\\frac{1}{2}", "\\frac{1}{4}", "\\frac{3}{4}"], 
                [4*PI/3, 2*PI/3, PI/3, PI]
            )
        ])
        for tex in p_texs[1:]:
            tex[0].scale(0.75, about_point = tex[0].get_right())

        x_marks = self.get_x_marks([0, 2*PI/3, 4*PI/3, 2*PI, 8*PI/3])

        self.play(
            Create(p_arrow),
            Write(p_texs[0]),
            AnimationGroup(*[FocusOn(x) for x in [x_marks[0], x_marks[-1]]], lag_ratio = 0.5),
            AnimationGroup(*[DrawBorderThenFill(x) for x in [x_marks[0], x_marks[-1]]], lag_ratio = 0.5), 
            run_time = 3
        )
        self.wait()

        self.play(
            ApplyMethod(x_marks[0].copy().move_to, x_marks[2], path_arc = -PI/2, remover = True),
            ApplyMethod(x_marks[4].copy().move_to, x_marks[2], path_arc = +PI/2, remover = True),
            p_num.animate.set_value(0.5),
            Transform(p_texs[0], p_texs[1]),
            run_time = 4
        )
        self.add(x_marks[2])
        self.wait(2)


        # Tiefpunkt da negatives Vorzeichen
        x_mark_x_axis = Tex(XMARK_TEX, tex_template = self.myTemplate, color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors))\
            .move_to(self.new_axes.c2p(2*PI/3, 0))

        self.play(
            ApplyMethod(x_marks[0].copy().move_to, x_mark_x_axis, path_arc = -PI/2, remover = True),
            ApplyMethod(x_marks[2].copy().move_to, x_mark_x_axis, path_arc = +PI/2, remover = True),
            p_num.animate.set_value(0.25),
            Transform(p_texs[0], p_texs[2]),
            run_time = 4
        )
        self.add(x_mark_x_axis)

        self.play(x_mark_x_axis.animate.move_to(self.new_axes.c2p(2*PI/3, 1)), run_time = 2)
        self.wait()


        sign_arrow = Arrow(self.func[4].get_left() + DOWN + 0.7*RIGHT, self.func[4].get_left() + 0.2*RIGHT, buff = 0, color = PINK)
        sign_tex = Tex("Spiegelung an \\\\ der $x$-Achse", color = PINK)\
            .next_to(sign_arrow.get_start(), RIGHT, aligned_edge=UP)
        self.play(GrowArrow(sign_arrow), run_time = 2)
        self.wait(0.5)
        self.play(Write(sign_tex), run_time = 2)
        self.wait(2)

        self.play(x_mark_x_axis.animate.move_to(self.new_axes.c2p(2*PI/3, -1)), run_time = 4)
        self.remove(x_mark_x_axis)
        self.add(x_marks[1])
        self.wait()


        self.play(
            GrowArrow(sign_arrow, rate_func = lambda t: smooth(1-t)), 
            FadeOut(sign_tex),
            run_time = 2
        )
        self.wait()

        # Hochpunkt
        x_mark_x_axis = Tex(XMARK_TEX, tex_template = self.myTemplate, color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors))\
            .move_to(self.new_axes.c2p(2*PI, 0))

        self.play(
            ApplyMethod(x_marks[2].copy().move_to, x_mark_x_axis, path_arc = -PI/2, remover = True),
            ApplyMethod(x_marks[4].copy().move_to, x_mark_x_axis, path_arc = +PI/2, remover = True),
            p_num.animate.set_value(0.75),
            Transform(p_texs[0], p_texs[3]),
            run_time = 4
        )
        self.add(x_mark_x_axis)

        self.play(x_mark_x_axis.animate.move_to(self.new_axes.c2p(2*PI, 1)), run_time = 3)
        self.remove(x_mark_x_axis)
        self.add(x_marks[3])
        self.wait(2)


        # Draw Graph
        graph = self.new_axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), x_range = [0, 8*PI/3], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )

        self.play(
            Create(graph),
            FadeOut(p_arrow),
            FadeOut(p_texs[0]),
            run_time = 5
        )
        self.wait(3)

    def add_marks_for_full_graph(self):
        new_x_marks = self.get_x_marks([-4*PI/3, -2*PI/3, 10*PI/3])
        arrows = VGroup(*[
            Arrow(
                start = self.new_axes.c2p(x, np.sin(self.b_val.get_value() * x)), 
                end = self.new_axes.c2p(x + k*8*PI/3, np.sin(self.b_val.get_value() * x)),
                buff = 0.25, color = BLUE, stroke_width = 6, tip_length = 0.25
            )
            for x, k in zip([4*PI/3, 2*PI, 2*PI/3], [-1, -1, 1])
        ])
        self.play(
            AnimationGroup(
                *[GrowArrow(arrow) for arrow in arrows], 
                lag_ratio = 0.5
            ), 
            run_time = 4
        )
        self.play(
            AnimationGroup(*[FocusOn(x) for x in new_x_marks], lag_ratio = 0.5), 
            AnimationGroup(*[DrawBorderThenFill(x) for x in new_x_marks], lag_ratio = 0.5), 
            run_time = 3
        )
        self.wait()

        full_graph = self.new_axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), x_range = [self.x_min, self.x_max], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )
        self.play(
            Create(full_graph, run_time = 5),
            AnimationGroup(*[GrowArrow(arrow, rate_func = lambda t: smooth(1-t)) for arrow in arrows], lag_ratio = 0.5, run_time = 3)
        )
        self.wait(3)



    # functions
    def get_new_ticks(self):
        ticks = VGroup()
        for x in [-PI, -2/3*PI, -1/3*PI, PI/3, 2/3*PI, PI, 4/3*PI, 5/3*PI, 2*PI, 7/3*PI, 8/3*PI, 3*PI]:
            tick = Line(DOWN, UP, color = LIGHT_GREY)
            tick.set_length(0.15)
            tick.move_to(self.new_axes.c2p(x, 0))
            ticks.add(tick)

        return ticks

    def get_new_x_numbers(self):
        x_axis_nums = [-PI, -2/3*PI, -1/3*PI, PI/3, 2/3*PI, PI, 4/3*PI, 5/3*PI, 2*PI, 7/3*PI, 8/3*PI, 3*PI]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.new_axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                ["-\\pi", "-2\\pi/3", "-\\pi/3", "\\pi/3", "2\\pi/3", "\\pi", "4\\pi/3", "5\\pi/3", "2\\pi", "7\\pi/3", "8\\pi/3", "3\\pi"], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_period_double_arrow(self):
        arrow = DoubleArrow(
            start = self.new_axes.c2p(0,-1.5), end = self.new_axes.c2p(self.p_num.get_value() * 8*PI/3, -1.5), 
            buff = 0, color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )
        return arrow

    def get_x_marks(self, numbers):
        x_marks = VGroup(*[
            Tex(XMARK_TEX, tex_template = self.myTemplate, color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors))\
                .move_to(self.new_axes.c2p(x, np.sin(self.b_val.get_value() * x)))
            for x in numbers# [0, 2*PI/3, 4*PI/3, 2*PI, 8*PI/3]
        ])

        return x_marks


class ParameterToPeriodViceVersa(Scene):
    def construct(self):
        colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]

        color_b = parameter_to_color(-0.75, -2, 4, colors)
        color_p = BLUE
        pos_b = 2.5*LEFT
        pos_p = 2.5*RIGHT

        bp = VGroup(*[
            MathTex(tex, font_size = 120, color = color).move_to(pos, aligned_edge=edge) 
                for tex, color, pos, edge in zip(["b", "p"], [color_b, color_p], [pos_b, pos_p], [RIGHT, LEFT])
        ])

        arrow_b = ArcBetweenPoints(pos_b, pos_p, angle = -75*DEGREES)\
            .set_color([color_p, color_b])\
            .add_tip()
        arrow_p = ArcBetweenPoints(pos_p, pos_b, angle = -75*DEGREES)\
            .set_color([color_b, color_p])\
            .add_tip()

        arrows = VGroup(arrow_b, arrow_p).arrange_submobjects(DOWN, buff = 1.5)

        texts = VGroup(*[
            Tex(tex).next_to(arrow, direction, buff = 0.5) for tex, arrow, direction in zip(
                ["Zeichnen des\\\\Graphen", "Ablesen der \\\\Funktionsgleichung"], arrows, [UP, DOWN]
            )
        ])


        self.add(texts[0])
        self.wait(2)

        self.play(DrawBorderThenFill(bp[0]), run_time = 1.5)
        self.play(Create(arrows[0]), run_time = 2)
        self.play(Write(bp[1]))
        self.wait()

        per_eq = MathTex("p", "=", "{2\\pi", "\\over", "\\vert", "b", "\\vert}", font_size = 60)\
            .set_color_by_tex_to_color_map({"b": color_b, "p": color_p, "2\\pi": WHITE})
        self.play(Write(per_eq))
        self.wait(0.5)

        self.play(Circumscribe(per_eq, color = GREEN, fade_out=True, run_time = 3))
        self.wait(2)


        self.play(Create(arrows[1]), run_time = 3)
        self.play(Write(texts[1]), run_time = 2)
        self.wait()


        self.play(Flash(per_eq[0], color = GREEN))
        self.wait()
        self.play(Flash(per_eq[-2], color = GREEN))
        self.wait(3)


        disappear_first = Group(*[x for x in self.mobjects if x != per_eq])
        self.play(
            AnimationGroup(
                ShrinkToCenter(disappear_first, rate_func = smooth), 
                ShrinkToCenter(per_eq, rate_func = running_start),
                lag_ratio = 0.3
            ),
            run_time = 1.5
        )
        self.wait()


class ReadEquation(ParameterInfluence):
    def construct(self):
        self.axes_kwargs = {
            "x_range": [-3*PI/2, 9*PI/2, 0.5], "y_range": [-1.25, 1.25, PI/4], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}, 
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.x_min = -3*PI/2
        self.x_max = 9*PI/2
        self.b_val = ValueTracker(4/5)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]


        self.scene_setup()
        self.first_example()


    def scene_setup(self):
        axes, b_val = self.axes, self.b_val

        axes_ticks = self.get_ticks()
        self.x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        func = self.func = MathTex("f(x)", "=", "\\sin", "(", "parai", "\\cdot", "x", ")")\
            .scale(1.4)\
            .to_edge(UP, buff = 0.25)
        func[4].set_stroke(width = 0).set_fill(opacity = 0)

        b_dec_func = self.b_dec_func = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)
        b_dec_func.scale(1.4).move_to(func[4]).align_to(func[5:7], DOWN)
        b_dec_func.add_updater(lambda dec:
            dec.set_value(b_val.get_value()).set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
        )

        graph = self.graph = always_redraw(lambda: 
            axes.get_graph(
                lambda x: np.sin(b_val.get_value() * x), x_range = [self.x_min, self.x_max], 
                color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
            )
        )

        starting_mobs = Group(axes, axes_ticks, self.x_numbers, y_numbers, graph, func)
        self.add(starting_mobs)
        self.wait(3)

    def first_example(self):
        dot = Dot()
        path = self.axes.get_graph(lambda x: np.sin(0.8*x), x_range = [0,5*PI/2])
        self.play(MoveAlongPath(dot, path), run_time = 3)
        self.bring_to_front(self.x_numbers)

        p_arrow = self.get_p_arrow(color = GREEN_D)
        self.play(
            FadeOut(dot),
            Create(p_arrow), 
            run_time = 1.5
        )
        self.wait()

        self.play(Circumscribe(self.x_numbers[6], run_time = 3))
        
        per1 = MathTex("p", "=", "{5", "\\pi", "\\over", "2}", font_size = 60)\
            .next_to(self.func, DOWN, buff = 0.5)
        self.play(Write(per1))
        self.wait()

        per2 = MathTex("{2", "\\pi", "\\over", "b}", "=", "{5", "\\pi", "\\over", "2}", font_size = 60)\
            .move_to(per1, aligned_edge=RIGHT)

        self.play(TransformMatchingTex(per1, per2), run_time = 2.5)
        self.wait()

        self.play(Indicate(per2[3]), run_time = 2)
        self.wait()

        per3 = MathTex("{2", "\\over", "b}", "=", "{5", "\\over", "2}", font_size = 60)\
            .move_to(per2)
        self.play(
            *[FadeToColor(per2[i], color = GREY_D) for i in [1, 6]], 
            run_time = 2
        )
        self.play(TransformMatchingTex(per2, per3), run_time = 3)
        self.wait()

        per4 = MathTex("{4", "\\over", "b}", "=", "5", font_size = 60)\
            .move_to(per3, aligned_edge=LEFT)
        self.play(TransformMatchingTex(per3, per4, fade_transform_mismatches = True), run_time = 3)
        self.wait()

        per5 = MathTex("{4", "\\over", "5}", "=", "b", font_size = 60)\
            .move_to(per4, aligned_edge=LEFT)
        self.play(TransformMatchingTex(per4, per5, fade_transform_mismatches = True), run_time = 2.5)
        self.wait(0.5)

        self.play(Circumscribe(per5, color = YELLOW, fade_out = True, run_time = 3))
        self.play(
            Write(self.b_dec_func), run_time = 2
        )
        self.wait(3)



    # functions 
    def get_p_arrow(self, color):
        p = 2*PI/abs(self.b_val.get_value())
        arrow = DoubleArrow(
            start = self.axes.c2p(0, 0), end = self.axes.c2p(p, 0),
            buff = 0, color = color, tip_length = 0.25
        )

        return arrow


class ReadEquation2(ParameterInfluence):
    def construct(self):
        self.axes_kwargs = {
            "x_range": [-3*PI/2, 10*PI/3, 0.5], "y_range": [-1.25, 1.25, PI/3], 
            "x_length": 13, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}, 
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(UP)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)
        self.origin = self.axes.c2p(0,0)

        self.x_min = -3*PI/2
        self.x_max = 10*PI/3
        self.b_val = ValueTracker(-3/2)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]


        self.scene_setup()
        self.from_per_to_b()


    def scene_setup(self):
        axes, b_val = self.axes, self.b_val

        axes_ticks = self.get_ticks()
        self.x_numbers, y_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        func = self.func = MathTex("f(x)", "=", "\\sin", "(", "parai", "\\cdot", "x", ")")\
            .scale(1.4)\
            .to_edge(DOWN, buff = 0.25)
        func[4].set_stroke(width = 0).set_fill(opacity = 0)

        b_dec_func = self.b_dec_func = DecimalNumber(b_val.get_value(), num_decimal_places=2, include_sign=True)
        b_dec_func.scale(1.4).move_to(func[4]).align_to(func[5:7], DOWN)
        b_dec_func.add_updater(lambda dec:
            dec.set_value(b_val.get_value()).set_color(parameter_to_color(b_val.get_value(), -2, 4, self.colors))
        )

        graph = self.graph = axes.get_graph(
                lambda x: np.sin(b_val.get_value() * x), x_range = [self.x_min, self.x_max], 
                color = parameter_to_color(b_val.get_value(), -2, 4, self.colors)
        )

        starting_mobs = Group(axes, axes_ticks, self.x_numbers, y_numbers, func)
        self.add(starting_mobs)
        self.wait(2)
        self.play(Create(graph), run_time = 3)
        self.wait(2)

    def from_per_to_b(self):
        dot = Dot()
        path = self.axes.get_graph(lambda x: np.sin(self.b_val.get_value()*x), x_range = [0, 4*PI/3])
        self.play(MoveAlongPath(dot, path), run_time = 3)

        p_arrow = self.get_p_arrow(color = GREEN_D)
        self.play(
            FadeOut(dot),
            Create(p_arrow), 
            run_time = 1.5
        )
        self.wait()

        # Hopping to 4*PI/3
        dot = Dot(point = self.origin)
        self.play(FocusOn(dot), GrowFromCenter(dot), run_time = 2)
        for k in range(4):
            self.play(
                ApplyMethod(dot.shift, PI/3*self.axes.x_axis.unit_size * RIGHT, path_arc = -PI/2), 
                run_time = 1.5
            )
        self.wait()


        per1 = MathTex("p", "=", "{4", "\\pi", "\\over", "3}", font_size = 60)\
            .next_to(self.func, UP, buff = 0.75)
        self.play(Write(per1))
        self.wait()

        per2 = MathTex("{2", "\\pi", "\\over", "b}", "=", "{4", "\\pi", "\\over", "3}", font_size = 60)\
            .move_to(per1, aligned_edge=RIGHT)

        self.play(TransformMatchingTex(per1, per2), run_time = 2.5)
        self.wait()

        self.play(Indicate(per2[3]), run_time = 2)
        self.wait()

        per3 = MathTex("{2", "\\over", "b}", "=", "{4", "\\over", "3}", font_size = 60)\
            .move_to(per2)
        self.play(
            *[FadeToColor(per2[i], color = GREY_D) for i in [1, 6]], 
            run_time = 2
        )
        self.play(TransformMatchingTex(per2, per3), run_time = 3)
        self.wait()

        per4 = MathTex("{6", "\\over", "b}", "=", "4", font_size = 60)\
            .move_to(per3, aligned_edge=LEFT)
        self.play(TransformMatchingTex(per3, per4, fade_transform_mismatches = True), run_time = 3)
        self.wait()

        per5 = MathTex("{6", "\\over", "4}", "=", "b", font_size = 60)\
            .move_to(per4, aligned_edge=LEFT)
        self.play(TransformMatchingTex(per4, per5, fade_transform_mismatches = True), run_time = 2.5)
        self.wait(0.5)

        per6 = MathTex("{3", "\\over", "2}", "=", "b", font_size = 60)\
            .move_to(per5)
        self.play(TransformMatchingTex(per5, per6, fade_transform_mismatches = True), run_time = 2.5)
        self.wait(0.5)

        self.play(Circumscribe(per6, color = YELLOW, fade_out = True, run_time = 3))
        self.wait()


        new_graph = self.axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), x_range = [0,PI/3], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )
        self.add(new_graph)
        self.play(self.graph.animate.set_stroke(opacity = 0.25), run_time = 1.5)
        self.play(ApplyWave(new_graph))
        self.wait()

        self.play(Write(self.b_dec_func), run_time = 2)
        self.wait(3)



    # functions
    def get_ticks(self):
        ticks = VGroup()
        for x in [-PI, PI, 2*PI, 3*PI]:
            tick = Line(DOWN, UP, color = LIGHT_GREY)
            tick.set_length(0.15)
            tick.move_to(self.axes.c2p(x, 0))
            ticks.add(tick)

        return ticks

    def get_x_axis_numbers(self):
        x_axis_nums = [-PI, PI, 2*PI, 3*PI]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                ["-\\pi", "\\pi", "2\\pi", "3\\pi"], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_y_axis_numbers(self):
        y_axis_nums = [-1,1]
        y_axis_coords = VGroup(*[
            MathTex(num, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for num in y_axis_nums
        ])
        return y_axis_coords

    def get_p_arrow(self, color):
        p = 2*PI/abs(self.b_val.get_value())
        arrow = DoubleArrow(
            start = self.axes.c2p(0, 0), end = self.axes.c2p(p, 0),
            buff = 0, color = color, tip_length = 0.25
        )

        return arrow


class ThumbnailDrawing(HowToDrawGraphs2):
    def construct(self):
        self.x_min = -2*PI/3 - 0.5
        self.x_max = 10*PI/3 + 0.5
        self.new_axes_kwargs = {
            "x_range": [self.x_min, self.x_max, 0.5], "y_range": [-1.25, 1.25, PI/3], 
            "x_length": 11, "y_length": 3.75, 
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.new_axes = NumberPlane(**self.new_axes_kwargs)\
            .to_edge(DOWN)
        self.new_axes.x_axis.add_tip(tip_length = 0.25)
        self.new_axes.y_axis.add_tip(tip_length = 0.25)

        self.b_val = ValueTracker(-0.75)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.colors = [PURPLE, ORANGE, WHITE, RED, GREEN, YELLOW, BLUE]

        ###########################################################################
        x_ticks = self.get_new_ticks()
        x_numbers = self.get_new_x_numbers()
        x_marks = self.get_x_marks([0, 2*PI/3, 4*PI/3, 2*PI, 8*PI/3])

        graph = self.new_axes.get_graph(
            lambda x: np.sin(self.b_val.get_value() * x), x_range = [self.x_min, 3*PI + PI/3], 
            color = parameter_to_color(self.b_val.get_value(), -2, 4, self.colors)
        )

        func = MathTex("\\sin", "(", "b", "\\cdot", "x", ")", font_size = 80).shift(3*LEFT + 2*UP)
        peri = MathTex("p", "=", "{2\\pi", "\\over", "\\vert", "b", "\\vert}", font_size = 80).shift(3*RIGHT + 2*UP)

        for tex in func, peri:
            tex.set_color_by_tex_to_color_map({"b": BLUE})

        self.add(self.new_axes, x_numbers, x_ticks, x_marks, graph, func, peri)
        self.wait()





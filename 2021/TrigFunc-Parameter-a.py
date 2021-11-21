from manim import *
import random

def height_to_color(y_value, min, max, colors):
    alpha = inverse_interpolate(min, max, y_value)
    index, sub_alpha = integer_interpolate(0, len(colors) - 1, alpha)

    return interpolate_color(colors[index], colors[index + 1], sub_alpha)


CMARK_TEX = "\\ding{51}"
XMARK_TEX = "\\ding{55}"


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

        self.play(
            *[GrowArrow(arrow) for arrow in arrows], 
            run_time = 1.5
        )
        self.add(arrows)

        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.4, 1.0)).set_value(2),
            c_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.6)).set_value(PI/2),
            run_time = 3
        )
        self.play(c_val.animate.set_value(-2*PI), run_time = 3)
        self.play(
            b_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.6)).set_value(-2),
            d_val.animate(rate_func = squish_rate_func(smooth, 0.3, 0.9)).set_value(-2),
            Write(func, rate_func = squish_rate_func(smooth, 0.75, 1.0)),
            run_time = 3
        )
        self.wait()

        self.play(
            AnimationGroup(
                *[Circumscribe(mob, color = rect_color, time_width = 0.5, fade_out = True, ) 
                for mob, rect_color in zip([func[2], func[6], func[11], func[-1]], [RED, BLUE, YELLOW, GREEN])], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait(0.5)


        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.4, 1.0)).set_value(-3),
            b_val.animate(rate_func = squish_rate_func(smooth, 0.2, 0.8)).set_value(1.5),
            c_val.animate(rate_func = squish_rate_func(smooth, 0.2, 0.8)).set_value(PI/3),
            d_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.6)).set_value(-1),
            run_time = 3
        )

        self.play(
            a_val.animate(rate_func = squish_rate_func(smooth, 0.4, 1.0)).set_value(-1.5),
            b_val.animate(rate_func = squish_rate_func(smooth, 0.2, 0.8)).set_value(-0.5),
            c_val.animate(rate_func = squish_rate_func(smooth, 0.2, 0.8)).set_value(0),
            d_val.animate(rate_func = squish_rate_func(smooth, 0.0, 0.6)).set_value(0),
            run_time = 3
        )

        self.play(Circumscribe(func[2], color = RED, fade_out=True, run_time = 2))
        self.play(
            a_val.animate(run_time = 2).set_value(1.5),
        )
        self.wait()


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


class StandardApproach(Scene):
    def construct(self):
        self.x_values = np.linspace(0, 2*np.pi, 9)
        self.sin_values = [round(np.sin(x), 2) for x in self.x_values]
        self.sin_values[-1] = 0.00
        self.sin2_values = [2*x for x in self.sin_values]

        axes = self.axes = NumberPlane(
            x_range = [0, 9*PI/4, 1], y_range = [-2, 2, PI/4],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        axes.to_edge(DOWN)
        self.origin = axes.c2p(0,0)
        axes.x_axis.add_tip(tip_length = 0.25)
        axes.y_axis.add_tip(tip_length = 0.25)

        self.x_axis_label = MathTex("x", color = GREY, font_size = 24).next_to(axes.x_axis, UP, aligned_edge=RIGHT)
        self.y_axis_label = MathTex("y", color = GREY, font_size = 24).next_to(axes.y_axis, UP)

        self.x_axis_numbers =  self.get_x_axis_numbers() 
        self.y_axis_numbers = self.get_y_axis_numbers()

        self.colors = [PINK, YELLOW, GREEN, RED, BLUE]

        self.table()
        self.graphs()
        self.multiply_each_with_2()
        self.show_different_graphs()


    def table(self):
        x_values, sin_values, sin2_values = self.x_values, self.sin_values, self.sin2_values

        x_strings = [
            "0", "\\frac{1}{4}\\pi", "\\frac{1}{2}\\pi", "\\frac{3}{4}\\pi", "\\pi", 
            "\\frac{5}{4}\\pi", "\\frac{3}{2}\\pi", "\\frac{7}{4}\\pi", "2\\pi"
        ]

        x_texs = VGroup(*[MathTex(x_str, font_size = 40) for x_str in x_strings])\
            .arrange_submobjects(RIGHT, buff = 0.8)\
            .to_corner(UR)\
            .shift(0.35*LEFT)


        sin_texs = VGroup(*[MathTex(str(sin), font_size = 40) for sin in sin_values])
        sin_texs.next_to(x_texs, DOWN, buff = 0.5)

        sin2_texs = VGroup(*[MathTex(str(sin2), font_size = 40) for sin2 in sin2_values])
        sin2_texs.next_to(sin_texs, DOWN, buff = 0.5)

        for x, sin, sin2 in zip(x_texs, sin_texs, sin2_texs):
            sin.align_to(x, RIGHT)
            sin2.align_to(x, RIGHT)


        x_label = MathTex("x", font_size = 40).next_to(x_texs, LEFT, buff = 0.85)
        sin_label = MathTex("\\sin", "(x)", font_size = 40).next_to(sin_texs, LEFT).align_to(x_label, RIGHT)
        sin2_label = MathTex("2", "\\cdot", "\\sin", "(x)", font_size = 40).next_to(sin2_texs, LEFT).align_to(sin_label, RIGHT)
        for label in sin_label, sin2_label:
            label.set_color_by_tex_to_color_map({"2": BLUE, "\\sin": RED})


        self.play(
            Write(x_label),
            FadeIn(x_texs, shift = 0.5*DOWN, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()
        self.play(
            LaggedStartMap(
                Create, VGroup(self.axes, self.x_axis_label, self.y_axis_label, self.x_axis_numbers, self.y_axis_numbers), lag_ratio = 0.2
            ),
            run_time = 4
        )
        self.wait()
        self.play(FocusOn(sin2_label[0]), run_time = 1.5)
        self.play(FadeIn(sin2_label[0], shift = 0.5*UP))
        self.play(
            Write(sin_label), 
            Write(sin2_label[1:])
        )
        self.wait()


        self.play(
            AnimationGroup(*[Write(tex) for tex in sin_texs], lag_ratio = 0.2),
            run_time = 2
        )
        self.play(
            AnimationGroup(*[Write(tex) for tex in sin2_texs], lag_ratio = 0.2),
            run_time = 2
        )
        self.wait()

        self.x_texs, self.sin_texs, self.sin2_texs = x_texs, sin_texs, sin2_texs
        self.sin2_label = sin2_label

    def graphs(self):
        x_values, sin_values, sin2_values = self.x_values, self.sin_values, self.sin2_values
        x_texs, sin_texs, sin2_texs = self.x_texs, self.sin_texs, self.sin2_texs
        axes = self.axes

        dots_axis = VGroup(*[Dot(axes.c2p(x_val, 0), radius = 0.06) for x_val in x_values])
        dots_sin  = VGroup(*[Dot(axes.c2p(x_val, sin_val),  radius = 0.06, color = RED)  for x_val, sin_val in  zip(x_values, sin_values)])
        dots_sin2 = VGroup(*[Dot(axes.c2p(x_val, sin2_val), radius = 0.06, color = BLUE) for x_val, sin2_val in zip(x_values, sin2_values)])

        graph_sin  = axes.get_graph(lambda x: np.sin(x), x_range = [0, 2*np.pi], color = RED)
        graph_sin2 = axes.get_graph(lambda x: 2*np.sin(x), x_range = [0, 2*np.pi], color = BLUE)

        self.play(
            AnimationGroup(
                *[Transform(tex.copy(), dot) for tex, dot in zip(x_texs, dots_axis)], 
                lag_ratio = 0.2
            ),
            run_time = 3
        )

        self.play(
            AnimationGroup(*[Indicate(sin_tex, color = RED) for sin_tex in sin_texs],lag_ratio = 0.2),
            run_time = 2
        )
        self.play(
            AnimationGroup(*[ReplacementTransform(dot, dot_sin) for dot, dot_sin in zip(dots_axis, dots_sin)], lag_ratio = 0.2),
            run_time = 3
        )
        self.play(Create(graph_sin), run_time = 2)
        self.wait()

        self.play(
            AnimationGroup(*[Indicate(sin2_tex, color = BLUE) for sin2_tex in sin2_texs],lag_ratio = 0.2),
            run_time = 2
        )
        self.play(
            AnimationGroup(*[ReplacementTransform(dot1, dot2) for dot1, dot2 in zip(dots_sin, dots_sin2)], lag_ratio = 0.2),
            run_time = 2
        )
        self.play(Create(graph_sin2), run_time = 2)
        self.wait(2)

        graph_copy = graph_sin.copy()
        self.play(
            Transform(graph_copy, graph_sin2.copy()), run_time = 3
        )
        self.remove(graph_copy)

        self.dots_sin2, self.graph_sin2 = dots_sin2, graph_sin2

    def multiply_each_with_2(self):
        arcs = VGroup(*[
            ArcBetweenPoints(sin_tex.get_right() + 0.1*RIGHT, sin2_tex.get_right() + 0.1*RIGHT, angle = -60*DEGREES)\
                .set_color(YELLOW)\
                .add_tip(tip_length = 0.15)
            for sin_tex, sin2_tex in zip(self.sin_texs, self.sin2_texs) 
        ])

        mults = VGroup(*[
            MathTex("\\cdot", "2", color = BLUE, font_size = 30).next_to(arc, buff = 0.1)
            for x, arc in zip(range(len(arcs)), arcs)
        ])

        # show multiplication at x = pi/2
        self.play(Indicate(self.sin_texs[2], color = YELLOW))
        self.play(Create(arcs[2]))
        self.play(Write(mults[2]))
        self.play(Indicate(self.sin2_texs[2], color = BLUE))
        self.wait()

        # all the others
        self.play(
            Create(arcs, lag_ratio = 0.1),
            AnimationGroup(*[Indicate(tex) for tex in [*self.sin_texs[:2], *self.sin_texs[3:]]]),
            run_time = 2
        )
        self.play(
            AnimationGroup(*[Write(two) for two in [mults[:2], mults[3:]]], lag_ratio = 0.1),
            AnimationGroup(*[Indicate(tex, color = BLUE) for tex in [self.sin2_texs[:2], self.sin2_texs[3:]]]),
            run_time = 2
        )
        self.wait(3)

        # self.remove(*arcs, *mults)
        # self.wait()
        self.arcs, self.mults = arcs, mults

    def show_different_graphs(self):
        a_values = [0.5, 1.5, -1, -2, 0.25, -0.5]

        old_dec = self.sin2_label[0]
        old_sin2_texs = self.sin2_texs
        old_dots = self.dots_sin2
        old_graph = self.graph_sin2
        old_mults = self.mults

        for a_value in a_values:
            new_dec = MathTex(str(a_value), color = height_to_color(a_value, -2, 2, self.colors), font_size = 40)
            new_dec.move_to(old_dec, aligned_edge = RIGHT)

            self.play(
                FadeOut(old_dec, shift = UP), 
                FadeIn(new_dec, shift = UP)
            )

            new_mults = VGroup(*[
                MathTex("\\cdot", str(a_value), color = height_to_color(a_value, -2, 2, self.colors), font_size = 30)\
                    .next_to(arc, buff = 0.1)
                for x, arc in zip(range(len(self.arcs)), self.arcs)
            ])
            self.play(ReplacementTransform(old_mults, new_mults))

            new_values = [round(a_value * np.sin(x), 2) for x in self.x_values]
            new_values[-1] = 0.00
            new_texs = VGroup(*[MathTex(str(sin2), font_size = 40) for sin2 in new_values])
            new_texs.next_to(self.sin_texs, DOWN, buff = 0.5)

            for x, new_sin2 in zip(self.x_texs, new_texs):
                new_sin2.align_to(x, RIGHT)
                new_sin2.align_to(x, RIGHT)

            self.play(ReplacementTransform(old_sin2_texs, new_texs))

            new_dots = VGroup(*[
                Dot(self.axes.c2p(x_val, sin2_val), radius = 0.06, color = height_to_color(a_value, -2, 2, self.colors)) 
                for x_val, sin2_val in zip(self.x_values, new_values)
            ])
            new_graph = self.axes.get_graph(
                lambda x: a_value * np.sin(x), x_range = [0, 2*np.pi], color = height_to_color(a_value, -2, 2, self.colors)
            )

            self.play(
                ReplacementTransform(old_graph, new_graph), 
                ReplacementTransform(old_dots, new_dots),
                run_time = 2
            )
            self.wait()

            old_dec, old_mults, old_sin2_texs, old_dots, old_graph = new_dec, new_mults, new_texs, new_dots, new_graph

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
        y_axis_nums = list(range(-2,3))
        y_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for tex, num in zip(
                [-2,-1,0,1,2], 
                y_axis_nums
            )
        ])
        return y_axis_coords


class LookingForGeneralUnderstanding(Scene):
    def construct(self):
        self.axes_kwargs = {
            "x_length": 5.5, "y_length": 5.5 * 9/16, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }

        self.colors = [YELLOW, GREEN, RED, BLUE]

        self.titles_table_setup()
        self.left_side()
        self.righ_side()
        self.parabola()
        self.trig_func()
        self.expo_func()

    # setup
    def titles_table_setup(self):
        his = self.his = Tex("How it started:", font_size = 60)
        hig = self.hig = Tex("How it's going:", font_size = 60)

        titles = VGroup(his, hig)\
            .arrange_submobjects(RIGHT, buff = 2.5, aligned_edge = UP)\
            .to_edge(UP)

        line_config = {"stroke_width": 3, "color": GREY}
        hline = Line(6.5*LEFT, 6.5*RIGHT, **line_config).shift(2.75*UP)
        vline = Line(3.5*UP, 3.5*DOWN, **line_config)

        self.add(his, hig, hline, vline)

    def left_side(self):
        axes = self.axes_left = NumberPlane(x_range = [-4, 4, 4], y_range = [-5, 25, 1], **self.axes_kwargs)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)

        for mob in axes, frame:
            mob.next_to(self.his.get_top(), DOWN, buff = 1.5)

        a_left = ValueTracker(1)
        graph1 = axes.get_graph(lambda x: x**2, x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: a_left.get_value() * x**2, 
            x_range = [-2.5, 2.5], 
            color = height_to_color(a_left.get_value(), -1.5, 2.5, self.colors)
        ))

        func = MathTex("f(x)", "=", "para", "\\cdot", "x^2", font_size = 60)
        func.next_to(self.his.get_top(), DOWN, buff = 5.5)
        func[2].set_color(BLACK).set_fill(opacity = 0)

        a_dec = DecimalNumber(a_left.get_value(), num_decimal_places=1, include_sign=True, font_size = 60)\
            .next_to(func[3:], LEFT, aligned_edge=DOWN)\
            .shift(0.05*DOWN)\
            .add_updater(lambda dec: dec.set_value(a_left.get_value()).set_color(height_to_color(a_left.get_value(), -1.5, 2.5, self.colors)))

        self.add(frame, axes, graph1, graph2, func, a_dec)

        self.a_left, self.graph2_left = a_left, graph2

    def righ_side(self):
        axes = self.axes_right = NumberPlane(x_range = [-4, 4, 1], y_range = [-4, 4, 1], **self.axes_kwargs)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)

        for mob in axes, frame:
            mob.next_to(self.hig.get_top(), DOWN, buff = 1.5)


        a_right = ValueTracker(1)
        graph1 = axes.get_graph(lambda x: np.sin(x), x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: a_right.get_value() * np.sin(x), 
            x_range = [-4, 4], 
            color = height_to_color(a_right.get_value(), -1.5, 2.5, self.colors)
        ))


        self.add(frame, axes, graph1, graph2)
        self.a_right, self.graph1_right, self.graph2_right = a_right, graph1, graph2

    # animations
    def parabola(self):
        a_left = self.a_left
        self.wait(1)
        for val, rt in zip([4,-0.5,1], [2,1.5,1]):
            self.play(a_left.animate.set_value(val), run_time = rt)
            self.wait()
        self.wait()

    def trig_func(self):
        a_left, a_right = self.a_left, self.a_right

        func = MathTex("f(x)", "=", "para", "\\cdot", "\\sin(x)", font_size = 60)
        func.next_to(self.hig.get_top(), DOWN, buff = 5.5)
        func[2].set_color(BLACK).set_fill(opacity = 0)

        a_dec = DecimalNumber(a_right.get_value(), num_decimal_places=1, include_sign=True, font_size = 60)\
            .next_to(func[3:], LEFT, aligned_edge=DOWN)\
            .add_updater(lambda dec: dec.set_value(a_right.get_value()).set_color(height_to_color(a_right.get_value(), -1.5, 2.5, self.colors)))

        func.shift(0.09*DOWN)

        self.play(
            Write(func), 
            FadeIn(a_dec, shift = DOWN),
        )

        for val, rt in zip([4,-0.5,1], [4,3,1.5]):
            self.play(
                a_left.animate.set_value(val),
                a_right.animate.set_value(val),
                run_time = rt
            )
            self.wait()
        self.remove(self.graph2_right)

        self.func = func

    def expo_func(self):
        a_left, a_right, axes_right = self.a_left, self.a_right, self.axes_right

        graph1 = axes_right.get_graph(lambda x: np.exp(-x**2), x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes_right.get_graph(
            lambda x: a_right.get_value() * np.exp(-x**2), 
            x_range = [-4, 4], 
            color = height_to_color(a_right.get_value(), -1.5, 2.5, self.colors)
        ))

        func = MathTex("f(x)", "=", "para", "\\cdot", "e^{x^2}", font_size = 60)
        func.move_to(self.func, aligned_edge=LEFT)
        func[2].set_color(BLACK).set_fill(opacity = 0)

        self.play(
            ReplacementTransform(self.graph1_right, graph1), 
            ReplacementTransform(self.func, func),
        )
        self.add(graph2)

        for val, rt in zip([4,-0.5,1], [4,3,1.5]):
            self.play(
                a_left.animate.set_value(val),
                a_right.animate.set_value(val),
                run_time = rt
            )
            self.wait()
        self.wait()


class ScaleGraph(Scene):
    def construct(self):
        self.axes = NumberPlane(
            x_range = [0, 9*np.pi/4, 1], y_range = [-3, 3, np.pi/4],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.axes.to_edge(RIGHT)
        self.origin = self.axes.c2p(0,0)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        x_axis_label = MathTex("x", color = LIGHT_GREY, font_size = 30).next_to(self.axes.x_axis, UP, aligned_edge=RIGHT)
        y_axis_label = MathTex("y", color = LIGHT_GREY, font_size = 30).next_to(self.axes.y_axis, UP)

        self.x_axis_numbers, self.y_axis_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()
        self.add(self.axes, self.x_axis_numbers, self.y_axis_numbers, x_axis_label, y_axis_label)
        self.wait()

        self.a_val = ValueTracker(2)
        self.x_min = 0
        self.x_max = 2*np.pi

        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]
        self.arrow_kwargs = {
            "buff": 0, "max_tip_length_to_length_ratio": 0.2, "color": height_to_color(self.a_val.get_value(), -3, 3, self.colors),
            "stroke_opacity": 0.5, "tip_style": {"fill_opacity": 0.5}
        }

        self.create_sin_ref()
        self.show_dot_on_normal_sine()
        self.multiply_with_2()
        self.repeat_with_more_dots()
        self.clarify_parameter_influence()

    def create_sin_ref(self):
        axes = self.axes

        dots, traces = VGroup(), VGroup()
        x_values = np.linspace(0, 2*PI, 100)
        for x in x_values:
            dot = Dot(point = axes.x_axis.n2p(x), radius = 0.03, fill_opacity = 0)
            trace = TracedPath(dot.get_center, dissipating_time = 0.2, stroke_opacity = [0.2, 1, 0.2])
            dots.add(dot)
            traces.add(trace)

        self.add(traces)
        for dot, x in zip(dots, x_values):
            dot.generate_target()
            dot.target.move_to(axes.c2p(x, self.sin_ref(x)))

        tex_ref = MathTex("f", "(", "x", ")", "=", "\\sin", "(", "x", ")")\
            .move_to(4*LEFT + 3*UP)
        uline_ref = Underline(tex_ref, color = RED)

        sin_ref_graph = self.axes.get_graph(lambda x: self.sin_ref(x), x_range = [self.x_min, self.x_max], color = RED)

        self.play(
            Write(tex_ref),
            Create(uline_ref)
        )
        self.play(
            AnimationGroup(*[MoveToTarget(dot) for dot in dots], lag_ratio = 0.05),
            Create(sin_ref_graph),
            run_time = 2
        )
        self.wait()

        self.sin_ref_graph, self.func_eq, self.func_uline = sin_ref_graph, tex_ref, uline_ref

    def show_dot_on_normal_sine(self):
        axes = self.axes
        dot = Dot(self.origin, radius = 0.06)
        self.play(
            FocusOn(self.origin),
            FadeIn(dot, shift = UP + LEFT), 
            run_time = 1.5
        )
        self.play(dot.animate.move_to(axes.c2p(np.pi/2, 0)), run_time = 1.5)
        self.play(Circumscribe(self.x_axis_numbers[0], color = YELLOW, run_time = 2))
        self.wait()

        target = axes.c2p(np.pi/2, 1)
        trace = TracedPath(dot.get_center, dissipating_time = 0.6, stroke_color = YELLOW, stroke_width = 8, stroke_opacity = [0,1,0])
        self.add(trace)

        self.play(dot.animate.move_to(target), run_time = 2)

        dot2 = dot.copy()
        dot2.set_fill(opacity = 0)
        trace2 = TracedPath(dot2.get_center, dissipating_time = 0.6, stroke_color = RED, stroke_width = 8, stroke_opacity = [0,1,0])
        self.add(trace2)
        self.play(dot2.animate.move_to(axes.c2p(0,1)), run_time = 2)
        self.wait()

        func_pi2_eq = MathTex("\\sin", "(", "\\pi/2", ")", "=", "1")\
            .next_to(self.func_eq, DOWN, buff = 0.75)
        self.play(Write(func_pi2_eq))
        self.wait(2)


        self.dot, self.trace, self.target, self.func_pi2_eq = dot, trace, target, func_pi2_eq

    def multiply_with_2(self):
        a_val, axes = self.a_val, self.axes

        #                  0    1    2    3    4       5      6         7      8    9   10
        tex_par = MathTex("g", "(", "x", ")", "=", "para", "\\cdot", "\\sin", "(", "x", ")")
        tex_par.move_to(4 * LEFT + 2.5 * DOWN)
        tex_par[5].set_color(BLACK).set_fill(opacity = 0)
        
        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign = True)
        a_dec.next_to(tex_par[6:8], LEFT, aligned_edge = DOWN)
        a_dec.add_updater(lambda a: a.set_value(a_val.get_value()).set_color(height_to_color(a_val.get_value(), -3, 3, self.colors)))

        uline = Underline(tex_par, color = height_to_color(a_val.get_value(), -3, 3, self.colors))
        uline.add_updater(lambda line: line.set_color(height_to_color(a_val.get_value(), -3, 3, self.colors)))

        self.play(
            Write(tex_par),
            Create(uline),
            FadeIn(a_dec, shift = 3*DOWN)
        )
        self.remove(self.trace)
        self.dot.move_to(axes.c2p(np.pi/2, 0))
        self.add(self.trace)
        self.wait()

        # Arrows for sine and parameter
        start1 = tex_par[7:].get_top()
        start2 = tex_par[5].get_top()
        arrow_sin = Arrow(start1, start1 + UP, color = RED, max_tip_length_to_length_ratio=0.2)
        arrow_dec = Arrow(start2, start2 + UP, color = GREY, max_tip_length_to_length_ratio=0.2).shift(0.15*UP)

        height_scalar = a_dec.copy().next_to(arrow_dec, UP)
        cdot = tex_par[6].copy().next_to(height_scalar, RIGHT)
        height = self.height = MathTex("1").next_to(arrow_sin, UP)

        self.play(FocusOn(self.dot, run_time = 1))
        self.play(self.dot.animate.move_to(self.target), run_time = 2)
        self.wait()
        self.play(GrowArrow(arrow_sin))
        self.play(TransformFromCopy(self.func_pi2_eq[-1], height, path_arc = np.pi/2), run_time = 2.5)
        self.wait()


        self.play(
            GrowArrow(arrow_dec),
            FadeIn(cdot, shift = UP),
            TransformFromCopy(a_dec, height_scalar, path_arc = np.pi/2), 
            run_time = 2
        )
        self.wait()

        # Arrow for dot on graph
        self.play(FocusOn(self.dot, run_time = 1))


        arrow_dot = always_redraw(lambda: Arrow(
            start = axes.c2p(np.pi/2,0), end = self.dot.get_center(), 
            buff = 0, max_tip_length_to_length_ratio = 0.2, 
            color = height_to_color(a_val.get_value(), -3, 3, self.colors), 
            stroke_opacity = 0.5, tip_style = {"fill_opacity": 0.5}
        ))
        self.play(GrowArrow(arrow_dot), run_time = 2)
        self.play(self.dot.animate.move_to(axes.c2p(np.pi/2, 2)), run_time = 3)
        self.wait(2)



        self.arrow_dot = arrow_dot
        self.tex_par = tex_par
        self.explain_group = VGroup(arrow_sin, arrow_dec, cdot, height_scalar, height, self.func_pi2_eq)

    def repeat_with_more_dots(self):
        axes, a_val = self.axes, self.a_val

        x_values = self.x_values = np.linspace(0, 2*np.pi, 21)
        dots1 = self.get_dots(1)
        dots2 = self.get_dots(2)


        # arrows for sin and 2*sin
        arrows1 = self.get_arrows(1, **self.arrow_kwargs) 
        arrows2 = self.get_arrows(a_val.get_value(), **self.arrow_kwargs)

        self.play(
            LaggedStartMap(FadeIn, dots1, shift = DOWN, lag_ratio = 0.2), 
            LaggedStartMap(GrowArrow, arrows1, lag_ratio = 0.2),
            run_time = 4
        )
        self.wait()

        for dot, x in zip(dots1, x_values):
            dot.generate_target()
            dot.target.move_to(axes.c2p(x, 2*self.sin_ref(x)))

        self.play(
            *[Transform(dot1, dot2) for dot1, dot2 in zip(dots1, dots2)],
            *[Transform(arrow1, arrow2) for arrow1, arrow2 in zip(arrows1, arrows2)],
            FadeOut(self.arrow_dot),
            run_time = 5
        )
        self.remove(self.dot)
        self.wait(2)


        # multilication at x = 3pi/2
        sample_arrow = arrows1[15]
        sample_arrow.save_state()

        self.play(
            sample_arrow.animate.scale_about_point(0.5, axes.c2p(3/2*np.pi, 0)), 
            run_time = 3
        )
        self.wait(0.25)
        func_3pi2_eq = MathTex("\\sin", "(", "3", "\\pi", "/", "2", ")", "=", "-1")\
            .next_to(self.func_pi2_eq, DOWN, buff = 0.5)
        self.play(Write(func_3pi2_eq))
        self.wait()

        new_height = MathTex("-1").move_to(self.height)

        grow_obj = func_3pi2_eq[-1].copy()
        self.play(
            GrowFromPoint(grow_obj, self.height.get_center(), rate_func = lambda t: smooth(1-t)),
            Transform(self.height, new_height),
        )
        self.remove(new_height)
        self.wait()

        self.play(Restore(sample_arrow), run_time = 3)
        self.wait(2)

        self.explain_group.add(func_3pi2_eq)

        # Graph 2 * sin(x)
        sin_par_graph = always_redraw(
            lambda: self.axes.get_graph(
                lambda x: self.sin_par(self.a_val.get_value(), x), 
                x_range = [self.x_min, self.x_max], 
                color = height_to_color(self.a_val.get_value(), -3, 3, self.colors)
            )
        )

        self.play(
            Create(sin_par_graph),
            FadeOut(dots1, lag_ratio = 0.2),
            FadeOut(arrows1, lag_ratio = 0.2), 
            FadeOut(self.explain_group, lag_ratio = 0.2),
            run_time = 3
        )
        self.wait()

        old_graph = self.sin_ref_graph.copy()
        new_graph = sin_par_graph.copy()
        self.play(Transform(old_graph, new_graph), run_time = 2)
        self.remove(old_graph)
        self.wait(3)

    def clarify_parameter_influence(self):
        a_val = self.a_val

        num_line = self.get_num_line()
        par_arrow = always_redraw(lambda: Arrow(
                start = self.tex_par[5].get_top() + 0.25*UP, end = num_line.n2p(a_val.get_value()), buff = 0, 
                color = height_to_color(a_val.get_value(), -3, 3, self.colors), 
                stroke_opacity = 0.5, tip_style = {"fill_opacity": 0.5}
        ))

        func_group = VGroup(self.func_eq, self.func_uline)
        func_group.generate_target()
        func_group.target.to_edge(UP).shift(1.5*RIGHT)

        self.play(
            Create(num_line), 
            GrowArrow(par_arrow), 
            MoveToTarget(func_group, path_arc = 30*DEGREES),
            run_time = 3
        )
        self.wait()


        brace_r = Brace(Line(num_line.n2p(1), num_line.n2p(3.5)), UP)
        brace_m = Brace(Line(num_line.n2p(0), num_line.n2p(1)), UP)
        brace_l = Brace(Line(num_line.n2p(-3.5), num_line.n2p(0)), UP)

        fs = 48
        text_r = Tex("Streckung", font_size = fs)
        text_m = Tex("Stauchung", font_size = fs)
        text_l = Tex("zusätzliche\\\\", "Spiegelung", font_size = fs)
        for mob, brace in zip([text_r, text_m, text_l], [brace_r, brace_m, brace_l]):
            mob.rotate(45*DEGREES)
            mob.next_to(brace, UP)

        self.play(FadeIn(VGroup(brace_r, brace_m, brace_l), shift = DOWN, lag_ratio = 0.5), run_time = 2)
        self.wait()

        def update_aval_bigger_1(mob):
            if abs(a_val.get_value()) > 1:
                mob.set_color(height_to_color(a_val.get_value(), -3, 3, self.colors))
            else:
                mob.set_color(DARK_GREY)

        def update_aval_between01(mob):
            if 0 < abs(a_val.get_value()) < 1:
                mob.set_color(height_to_color(a_val.get_value(), -3, 3, self.colors))
            else:
                mob.set_color(DARK_GREY)

        def update_aval_neg(mob):
            if a_val.get_value() < 0:
                mob.set_color(height_to_color(a_val.get_value(), -3, 3, self.colors))
            else:
                mob.set_color(DARK_GREY)


        brace_r.add_updater(update_aval_bigger_1)
        brace_m.add_updater(update_aval_between01)
        brace_l.add_updater(update_aval_neg)
        text_r.add_updater(update_aval_bigger_1)
        text_m.add_updater(update_aval_between01)
        text_l.add_updater(update_aval_neg)

        a_values = [3, 1.5, 2.3, 1, 0.5, 0.9, 0.3, 0, -0.5, -2, -1, -3]
        for a_value in a_values:
            self.play(a_val.animate.set_value(a_value), run_time = 3)
            self.wait()

            if a_value == 3:
                self.play(Write(text_r))
                self.wait()

            if a_value == 0.5:
                self.play(Write(text_m))
                self.wait()

            if a_value == -0.5:
                self.play(Write(text_l))
                self.wait()

                dots_ori, dots_pos, dots_neg = self.get_dots(1), self.get_dots(0.5), self.get_dots(-0.5)
                arrows_ori, arrows_pos, arrows_neg = self.get_arrows( 1.0, **self.arrow_kwargs), self.get_arrows( 0.5, **self.arrow_kwargs), self.get_arrows(-0.5, **self.arrow_kwargs)

                self.play(
                    FadeIn(dots_ori, shift = 0.5*DOWN, lag_ratio = 0.2), 
                    LaggedStartMap(GrowArrow, arrows_ori, lag_ratio = 0.2), 
                    run_time = 2
                )
                self.play(
                    Transform(dots_ori, dots_pos), 
                    Transform(arrows_ori, arrows_pos), 
                    run_time = 3
                )
                self.wait()
                self.play(
                    Transform(dots_ori, dots_neg), 
                    Transform(arrows_ori, arrows_neg), 
                    run_time = 4
                )
                self.wait()

                self.play(
                    FadeOut(dots_ori, lag_ratio = 0.2), 
                    FadeOut(arrows_ori, lag_ratio = 0.2), 
                    run_time = 2
                )
                self.wait()
        self.wait(3)

        self.play(a_val.animate.set_value(+3), rate_func = lambda t: linear(t), run_time = 10)
        self.play(a_val.animate.set_value(-3), rate_func = lambda t: linear(t), run_time = 10)
        self.wait(3)



    # functions
    def sin_par(self, a, x):
        return a * np.sin(x)

    def sin_ref(self, x):
        return self.sin_par(1, x)

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
        y_axis_nums = list(range(-2,3))
        y_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for tex, num in zip(
                [-2,-1,0,1,2], 
                y_axis_nums
            )
        ])
        return y_axis_coords

    def get_dots(self, stretch_value, num = 21, **kwargs):
        dots = VGroup()
        for x in np.linspace(self.x_min, self.x_max, num):
            dot = Dot(point = self.axes.c2p(x, stretch_value * self.sin_ref(x)), radius = 0.06, **kwargs)
            dots.add(dot)

        return dots

    def get_arrows(self, stretch_value, num = 21, **kwargs):
        arrows = VGroup()
        for x in np.linspace(self.x_min, self.x_max, num):
            start = self.axes.c2p(x, 0)
            end = self.axes.c2p(x, stretch_value * self.sin_ref(x))
            arrow = Arrow(start, end, **kwargs)
            arrows.add(arrow)

        return arrows

    def get_num_line(self):
        num_line = NumberLine(
            x_range = [-3,3, 0.5], length = 5, 
            include_numbers=True, numbers_to_exclude = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5],
            decimal_number_config={"num_decimal_places": 0})
        num_line.move_to(4*LEFT + 0.25*DOWN)

        return num_line


class Properties(MovingCameraScene):
    def construct(self):
        self.axes = NumberPlane(
            x_range = [-20*np.pi/4, 20*np.pi/4, 1], y_range = [-3, 3, np.pi/4],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.axes.to_edge(UP)
        self.origin = self.axes.c2p(0,0)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]
        self.a_val = ValueTracker(1)
        self.x_min, self.x_max = -5*np.pi, 5*np.pi

        # Graphs
        self.graph_ref = self.axes.get_graph(lambda x: self.sin_ref(x), x_range = [self.x_min, self.x_max], color = RED)
        self.graph_par = always_redraw(
            lambda: self.axes.get_graph(
                lambda x: self.sin_par(self.a_val.get_value(), x), x_range = [self.x_min, self.x_max], 
                color = height_to_color(self.a_val.get_value(), -3, 3, self.colors)
            )
        )


        self.nst_nums = [k * np.pi for k in range(-5, 6)]

        self.setup_scene()
        self.zeros()
        self.domain()
        self.periode()
        self.image()


    def setup_scene(self):
        x_axis_label = MathTex("x", color = LIGHT_GREY, font_size = 30).next_to(self.axes.x_axis, RIGHT)
        y_axis_label = MathTex("y", color = LIGHT_GREY, font_size = 30).next_to(self.axes.y_axis, UP)
        self.x_axis_numbers, self.y_axis_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()

        self.add(self.axes, self.x_axis_numbers, self.y_axis_numbers, x_axis_label, y_axis_label)
        self.remove(self.x_axis_numbers[10])
        self.wait()

        #                   0    1    2    3    4       5      6         7      8    9   10
        func_tex = MathTex("f", "(", "x", ")", "=", "para", "\\cdot", "\\sin", "(", "x", ")", font_size = 60)
        func_tex.move_to(4 * LEFT + 2.5 * DOWN)
        func_tex.to_edge(DOWN)
        func_tex[5].set_color(BLACK).set_fill(opacity = 0)
        
        a_dec = DecimalNumber(self.a_val.get_value(), num_decimal_places=1, include_sign = True)
        a_dec.scale(1.25)
        a_dec.next_to(func_tex[6:8], LEFT, aligned_edge = DOWN)
        a_dec.add_updater(lambda a: a.set_value(self.a_val.get_value()).set_color(height_to_color(self.a_val.get_value(), -3, 3, self.colors)))


        self.play(
            Create(self.graph_ref, run_time = 3), 
            Write(func_tex, run_time = 1), 
            FadeIn(a_dec, shift = DOWN, run_time = 2)
        )
        self.add(self.graph_par)


        self.func_tex = func_tex

    def zeros(self):
        a_val = self.a_val

        prop = Tex("Nullstellen", font_size = 60).next_to(self.func_tex, RIGHT, buff = 1)

        pins = self.get_zeros_pins(self.nst_nums, height = 0.35)
        for pin in pins:
            pin.save_state()
            pin.move_to(1*LEFT + 2*UP)
        self.play(
            Write(prop),
            DrawBorderThenFill(pins[0])
        )
        self.add(pins[1:])

        self.play(LaggedStartMap(Restore, pins, lag_ratio = 0.2), run_time = 3)
        self.wait()

        a_values = [-1, 2, -3, 0.5]
        for val in a_values:
            self.play(a_val.animate.set_value(val))
            self.wait()
        self.wait(3)

        self.prop, self.pins = prop, pins

    def domain(self):
        a_val = self.a_val
        self.camera.frame.save_state()
        camera_pos = self.camera.frame.get_center()
        prop = Tex("Definitionsbereich", font_size = 60).next_to(self.func_tex, RIGHT, buff = 1)
        self.play(Transform(self.prop, prop))
        self.wait()

        target_points = [
            self.axes.c2p(3*np.pi, 0), 
            self.axes.c2p(-4*np.pi, 0),
            self.axes.c2p(0*np.pi, 0), 
            camera_pos
        ] 
        a_values = [-1, 2, -3, 0.5]
        for val, target_point in zip(a_values, target_points):
            self.play(a_val.animate.set_value(val))
            self.play(self.camera.frame.animate.move_to(target_point))
            self.wait()
        self.wait(3)

    def periode(self):
        a_val, axes = self.a_val, self.axes
        prop = Tex("Periode", font_size = 60).next_to(self.func_tex, RIGHT, buff = 1)
        self.play(Transform(self.prop, prop))
        self.wait()


        arrow_a = DoubleArrow(start = axes.c2p(0, 1.5), end = axes.c2p(2*np.pi, 1.5), buff = 0, color = WHITE)
        per_tex = MathTex("p", "=", "2", "\\cdot", "\\pi", "\\approx", "6.28")\
            .next_to(arrow_a, UP, buff = 0)
        self.play(
            GrowFromCenter(arrow_a), 
            FadeIn(per_tex, shift = 0.25*UP)
        )
        self.play(Circumscribe(per_tex, run_time = 2))
        self.wait()

        self.play(LaggedStartMap(ApplyWave, self.pins, lag_ratio = 0.2), run_time = 3)
        self.wait()

        b_val = ValueTracker(1)
        graph_b = always_redraw(lambda: axes.get_graph(lambda x: np.sin(b_val.get_value() * x), x_range=[self.x_min, self.x_max], color = BLUE_E))
        arrow_b = always_redraw(lambda:DoubleArrow(start = axes.c2p(0, -1.5), end = axes.c2p(2*np.pi/b_val.get_value(), -1.5), buff = 0, color = WHITE))

        per_tex2 = MathTex("p", "\\approx")
        per_tex2.add_updater(lambda p: p.next_to(arrow_b, DOWN, buff = 0.2))
        dec_p = DecimalNumber(2*np.pi / b_val.get_value())
        dec_p.add_updater(lambda dec: dec.set_value(2*np.pi / b_val.get_value()).next_to(per_tex2, RIGHT).shift(0.1*UP))

        self.add(graph_b, arrow_b, per_tex2, dec_p)
        self.bring_to_front(self.graph_ref, self.graph_par, self.pins)

        for val in [4, 2, 1]:
            self.play(b_val.animate.set_value(val), run_time = 3)
            self.wait()
        self.wait()
        self.remove(graph_b, arrow_b, per_tex2, dec_p)
        self.wait(0.5)

        self.play(a_val.animate.set_value(-2), run_time = 4)
        self.play(a_val.animate.set_value(1), run_time = 4)
        self.wait()

        self.play(FadeOut(VGroup(arrow_a, per_tex), shift = 2*UP), run_time = 2)

    def image(self):
        a_val, axes = self.a_val, self.axes
        prop = Tex("Wertebereich", font_size = 60).next_to(self.func_tex, RIGHT, buff = 1)
        self.play(Transform(self.prop, prop))
        self.wait()

        rect = always_redraw(lambda: self.get_image_rect())
        arrow_max = always_redraw(lambda: self.get_image_arrow())
        arrow_min = always_redraw(lambda: self.get_image_arrow(max = False))

        max_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign=True)
        max_dec.add_updater(lambda dec: dec\
            .set_value(abs(a_val.get_value()))\
            .next_to(arrow_max.get_start(), LEFT)\
            .set_color(height_to_color(a_val.get_value(), -3, 3, self.colors))
        )

        min_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign=True)
        min_dec.add_updater(lambda dec: dec\
            .set_value(-1*abs(a_val.get_value()))\
            .next_to(arrow_min.get_start(), RIGHT)\
            .set_color(height_to_color(a_val.get_value(), -3, 3, self.colors))
        )


        # dot projection
        x = 5*np.pi/4
        dot = Dot(point = axes.c2p(x, self.sin_ref(x)))
        dot.generate_target()
        dot.target.move_to(axes.c2p(0, axes.p2c(dot.get_center())[1]))

        self.play(FocusOn(dot), GrowFromCenter(dot))
        self.play(MoveToTarget(dot), run_time = 5)
        self.wait()
        self.play(FadeOut(dot))

        self.repeat_with_all_dots()

        # upper and lower bound
        self.play(GrowArrow(arrow_max))
        self.play(Write(max_dec))
        self.wait() 

        self.play(GrowArrow(arrow_min))
        self.play(Write(min_dec))
        self.wait()

        # creating the image_rectangle
        self.play(
            FadeOut(self.dots, run_time = 2),
            Create(rect, run_time = 3)
        )
        self.bring_to_front(self.graph_ref, self.graph_par, self.pins)
        self.wait()

        self.play(a_val.animate.set_value(2), run_time = 6)
        self.wait()

        #              0      1           2            3       4      5      6      7
        tex = MathTex("y", "\\in", "\\mathbb{R},\\ ", "-2", "\\leq", "y", "\\leq", "2")
        tex.set_color_by_tex_to_color_map({"-2": BLUE, "2": BLUE})
        tex.to_edge(UP)
        tex.shift(3*RIGHT)

        self.play(Write(tex[:3]))
        self.wait()
        self.play(Write(tex[3:]))
        self.wait(3)

        self.play(
            FadeOut(tex), 
            FadeOut(self.prop),
            run_time = 2
        )
        self.wait()

        for val in [-3, 1.5, -2.25, 0.5]:
            self.play(a_val.animate.set_value(val), run_time = 4)
            self.wait()
        self.wait()

    def repeat_with_all_dots(self):
        props = list(np.linspace(0, 1, 200))
        dots_init = VGroup(*[Dot(point = self.graph_ref.point_from_proportion(x), radius = 0.04) for x in props])
        self.play(
            AnimationGroup(
                *[GrowFromCenter(dot) for dot in dots_init], 
                lag_ratio = 0.1
            ), 
            run_time = 2.5
        )

        random.shuffle(props)
        dots = self.dots = VGroup(*[Dot(point = self.graph_ref.point_from_proportion(x), radius = 0.04) for x in props])
        self.add(dots)
        self.remove(*dots_init)
        self.wait()

        for dot in dots:
            y_coord = self.axes.p2c(dot.get_center())[1]
            dot.generate_target()
            dot.target.move_to(self.axes.c2p(0, y_coord))

        self.play(
            AnimationGroup(
                *[MoveToTarget(dot, rate_func = rate_functions.ease_in_sine) for dot in dots], 
                lag_ratio = 0.2
            ), 
            run_time = 6
        )
        self.wait(2)

    # functions

    def sin_par(self, a, x):
        return a * np.sin(x)

    def sin_ref(self, x):
        return self.sin_par(1, x)

    def get_x_axis_numbers(self):
        x_axis_nums = [k * np.pi/2 for k in range(-10, 12)]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                [
                    "-5\\pi", "-9\\pi/2",
                    "-4\\pi", "-7\\pi/2", "-3\\pi", "-5\\pi/2",
                    "-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2",
                    "0",
                    "\\pi/2", "\\pi", "3\\pi/2", "2\\pi", 
                    "5\\pi/2", "3\\pi", "7\\pi/2", "4\\pi",
                    "9\\pi/2", "5\\pi"
                ], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_y_axis_numbers(self):
        y_axis_nums = [-2,-1,1,2]
        y_axis_coords = VGroup(*[
            MathTex(num, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for num in y_axis_nums
        ])
        return y_axis_coords

    def get_pin(self, height):
        pin = SVGMobject("pin")
        pin.set(height = height)
        return pin

    def get_zeros_pins(self, x_values, height):
        pins = VGroup()
        for x in x_values:
            pin = self.get_pin(height)
            pin.next_to(self.axes.c2p(x,0), UP, buff = 0, aligned_edge=RIGHT)
            pins.add(pin)

        return pins

    def get_image_rect(self):
        axes, a_val, x_min, x_max = self.axes, self.a_val, self.x_min, self.x_max
        rect = VMobject()
        rect.set_points_as_corners([
            axes.c2p(x_min, -a_val.get_value()),
            axes.c2p(x_max, -a_val.get_value()),
            axes.c2p(x_max, +a_val.get_value()),
            axes.c2p(x_min, +a_val.get_value()),
            axes.c2p(x_min, -a_val.get_value()),
        ])
        rect.set_fill(color = height_to_color(self.a_val.get_value(), -3, 3, self.colors), opacity = 0.25)
        rect.set_stroke(width = 0)

        return rect

    def get_image_arrow(self, max = True):
        factor = 1
        if max is not True:
            factor = -1
        
        axes, a_val = self.axes, self.a_val
        arrow = Arrow(
            start = axes.c2p(-1*factor * np.pi/4,  factor * abs(a_val.get_value())) + 0.5*factor*UP, 
            end = axes.c2p(0, factor * abs(a_val.get_value())), 
            buff = 0, color = WHITE
        )
        return arrow


class Thumbnail(ScaleGraph):
    def construct(self):
        self.axes = NumberPlane(
            x_range = [0, 9*np.pi/4, 1], y_range = [-3, 3, np.pi/4],
            x_length = config["frame_width"] - 2, 
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 0}
        )
        self.origin = self.axes.c2p(0,0)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        x_axis_label = MathTex("x", color = LIGHT_GREY, font_size = 30).next_to(self.axes.x_axis, UP, aligned_edge=RIGHT)
        y_axis_label = MathTex("y", color = LIGHT_GREY, font_size = 30).next_to(self.axes.y_axis, UP)

        self.x_axis_numbers, self.y_axis_numbers = self.get_x_axis_numbers(), self.get_y_axis_numbers()
        self.add(self.axes, self.x_axis_numbers, self.y_axis_numbers, x_axis_label, y_axis_label)
        self.wait()

        self.a_val = ValueTracker(2)
        self.x_min = 0
        self.x_max = 2*np.pi
        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]


        sin_ref_graph = self.axes.get_graph(lambda x: self.sin_ref(x), x_range = [self.x_min, self.x_max], stroke_width = 7, color = RED)
        sin_par_graph2 = self.axes.get_graph(lambda x: self.sin_par(2, x), x_range = [self.x_min, self.x_max], stroke_width = 7, color = BLUE)
        
        additional_graphs = VGroup(*[
            self.axes.get_graph(
                lambda x: self.sin_par(a, x), 
                x_range = [self.x_min, self.x_max], 
                stroke_width = 4, color = color, 
                stroke_opacity = 0.5
            )
            for a, color in zip([0.5, 1.5, 2.5, 3], [GREEN, PURPLE, PINK, YELLOW])
        ])

        x_values = self.x_values = np.linspace(0, 2*np.pi, 21)
        dots1 = self.get_dots(1, color = RED, stroke_color = WHITE, stroke_width = 2)
        dots2 = self.get_dots(2, color = BLUE, stroke_color = WHITE, stroke_width = 2)


        # arrows for sin and 2*sin
        self.arrow_kwargs = {
            "buff": 0, "max_tip_length_to_length_ratio": 0.2, "color": height_to_color(self.a_val.get_value(), -3, 3, self.colors),
            "stroke_opacity": 0.65, "tip_style": {"fill_opacity": 0.65}
        }
        arrows2 = self.get_arrows(self.a_val.get_value(), **self.arrow_kwargs)

        self.add(arrows2, additional_graphs, sin_ref_graph, sin_par_graph2, dots1, dots2)


        # func1 = MathTex("y", "=", "\\sin", "(x)", font_size = 120)\
        #     .set_color(GREY)\
        #     .add_background_rectangle()\
        #     .move_to(self.axes.c2p(PI/2, -2.25))\
        #     .shift(0.4*RIGHT)

        func2 = MathTex("y", "=", "a", "\\cdot", "\\sin", "(x)", font_size = 120)\
            .set_color(GREY)\
            .add_background_rectangle()\
            .move_to(self.axes.c2p(3*PI/2, +2.25))\
            .shift(RIGHT)
        
        # func1[-2].set_color(RED)
        func2[5].set_color(RED)
        func2[3].set_color(BLUE)

        self.add(func2)

        lines = VGroup()
        for angle in np.arange(0, TAU, TAU / 8):
            line = Line(ORIGIN, 0.75 * RIGHT)
            line.shift(0.75 * RIGHT)
            line.rotate(angle, about_point=ORIGIN)
            line.add_tip(at_start = True, tip_length = 0.15)
            lines.add(line)
        lines.set_color(YELLOW)
        lines.set_stroke(width=4)
        lines.move_to(func2[3])

        self.add(lines)
        self.remove(lines[0], lines[4])




class TwoPossibleTasks(Scene):
    def construct(self):
        given_and_sought = VGroup(*[
            Tex(tex, color = color, font_size = 60) for tex, color in zip(
                ["gegeben", "gesucht"], 
                [YELLOW_E, BLUE_E]
            )
        ])
        given_and_sought.arrange_submobjects(RIGHT, buff = 3)
        given_and_sought.to_edge(UP)

        one_two = VGroup(*[
            self.get_number_coin(num, col)
            for num, col in zip(["1", "2"], [GREY, GREY])
        ])
        one_two.arrange_submobjects(DOWN, buff = 2)
        one_two.to_edge(LEFT)

        grid_mobs = self.get_grid_mobs()

        self.play(
            DrawBorderThenFill(one_two, lag_ratio = 0.2), 
            run_time = 2
        )
        self.play(
            LaggedStartMap(FadeIn, VGroup(*given_and_sought), shift = DOWN, lag_ratio = 0.2), 
            run_time = 2
        )
        self.wait()
        self.play(
            AnimationGroup(*[Write(mob) for mob in grid_mobs[1]], lag_ratio = 0.15), 
            run_time = 1.5
        )
        self.play(Create(grid_mobs[0]))
        self.wait(2)



        self.play(TransformFromCopy(grid_mobs[0], grid_mobs[-1]), run_time = 1.5)
        self.play(
            AnimationGroup(*[Write(mob) for mob in grid_mobs[2]], lag_ratio = 0.15), 
            run_time = 1.5
        )
        self.wait(3)



        rect = Rectangle(width = 15, height = 9/16 * 15)\
            .set_fill(color = BLACK, opacity = 1)\
            .set_stroke(color = [BLUE, YELLOW], width = 5)

        self.play(GrowFromCenter(rect))
        self.wait()


    # functions
    def get_number_coin(self, number, color):
        coin = VGroup()
        circ = Circle()\
            .set_fill(color, 0.3)\
            .set_stroke(WHITE, 1)\
            .set(height = 1)
        label = MathTex(number)\
            .set(height = 0.5 * circ.height)\
            .move_to(circ)
        coin.add(circ, label)
        coin.symbol = number
        return coin

    def get_grid_mobs(self):
        graph1 = FunctionGraph(lambda x: 4 * np.sin(x), x_range = [0, 5*np.pi], color = YELLOW)
        graph1.set(height = 2)

        eq1_part1 = MathTex("a", "=", "\\ ???")
        eq1_arrow = Arrow(UP, ORIGIN, buff = 0, color = GREY)
        eq1_part2 = MathTex("f(x)", "=", "a", "\\cdot", "\\sin", "(x)")
        for tex in eq1_part1, eq1_part2:
            tex.set_color_by_tex_to_color_map({"a": RED, "???": RED, "\\sin": BLUE})
        eq1 = VGroup(eq1_part1, eq1_arrow, eq1_part2)
        eq1.arrange_submobjects(DOWN)


        graph2 = FunctionGraph(lambda x: -1.5 * np.sin(x), x_range = [0, 5*np.pi], color = BLUE)
        graph2.set(width = graph1.width)


        eq2_part1 = MathTex("a", "=", "2.5")
        eq2_arrow = Arrow(UP, ORIGIN, buff = 0, color = GREY)
        eq2_part2 = MathTex("f(x)", "=", "2.5", "\\cdot", "\\sin", "(x)")
        for tex in eq2_part1, eq2_part2:
            tex.set_color_by_tex_to_color_map({"2.5": RED, "\\sin": YELLOW})

        eq2 = VGroup(eq2_part1, eq2_arrow, eq2_part2)
        eq2.arrange_submobjects(DOWN)

        mobs = VGroup(eq2, graph2, graph1, eq1)\
            .arrange_in_grid(2,2, buff = 1)\
            .center()\
            .to_edge(DOWN)

        return mobs


class HowToDrawGraphs(Scene):
    def construct(self):
        axes = self.axes = NumberPlane(
            x_range = [-np.pi, 11/4*np.pi, 1], y_range = [-3.99, 3.99, 1/4*np.pi], 
            x_length = config["frame_width"] - 2, y_length = config["frame_height"] - 2, 
            background_line_style = {"stroke_color": BLUE_E, "stroke_width": 1}, 
        )
        axes.to_edge(DOWN)
        axes.x_axis.add_tip(tip_length = 0.25)
        axes.y_axis.add_tip(tip_length = 0.25)

        self.x_axis_label = MathTex("x", color = GREY, font_size = 40).next_to(axes.x_axis, UP, aligned_edge=RIGHT)
        self.y_axis_label = MathTex("y", color = GREY, font_size = 40).next_to(axes.y_axis, UP)
        self.x_axis_numbers = self.get_x_axis_numbers()
        self.y_axis_numbers = self.get_y_axis_numbers()
        self.origin = axes.c2p(0,0)

        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]

        self.a_val = ValueTracker(2.5)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.setup_scene()
        self.pin_down_and_scale()
        self.scaling()
        self.different_types()
        self.second_example()


    def setup_scene(self):
        a_val = self.a_val

        starting_mobs = VGroup(
            self.axes, self.x_axis_label, self.y_axis_label, self.x_axis_numbers, self.y_axis_numbers
        )
        self.play(GrowFromCenter(starting_mobs))
        self.wait()

        #               0    1    2    3    4     5         6        7      8    9   10
        func = MathTex("f", "(", "x", ")", "=", "para", "\\cdot", "\\sin", "(", "x", ")")\
            .scale(1.25)\
            .to_edge(UP)\
            .shift(RIGHT)
        black_out = func.get_parts_by_tex("para")
        black_out.set_color(BLACK).set_fill(opacity = 0)

        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign=True)\
            .scale(1.25)\
            .next_to(func[6:8], LEFT)\
            .set_color(height_to_color(a_val.get_value(), -4, 4, self.colors))
        a_dec.add_updater(lambda a: 
            a.set_value(a_val.get_value()).set_color(height_to_color(a_val.get_value(), -4, 4, self.colors))
        )

        self.play(
            Write(func), 
            FadeIn(a_dec, shift = DOWN)
        )
        self.wait(2)
        a_dec.suspend_updating()


        self.func, self.a_dec = func, a_dec

    def pin_down_and_scale(self):
        a_val, a_dec, axes = self.a_val, self.a_dec, self.axes

        pin_x_coords = [k*np.pi for k in range(-1, 3)]
        pins = VGroup()
        for k in pin_x_coords:
            pin = self.get_pin(height = 0.4)
            pin.next_to(axes.c2p(k, 0), UP, buff = 0, aligned_edge = RIGHT)
            pin.save_state()
            pin.move_to(2.5*UP)
            pins.add(pin)

        self.play(
            AnimationGroup(*[
                Restore(pin) for pin in pins
            ], lag_ratio = 0.2),
            run_time = 3
        )
        self.wait()


        a_val.set_value(1)
        graph = always_redraw(lambda: self.axes.get_graph(
            lambda x: a_val.get_value() * np.sin(x), 
            color = height_to_color(a_val.get_value(), -4, 4, self.colors)
        ))
        self.play(Create(graph), run_time = 2)
        self.wait()
        self.play(a_val.animate.set_value(4), rate_func = double_smooth, run_time = 1.5)
        self.play(a_val.animate.set_value(1), rate_func = smooth, run_time = 1.5)
        self.play(a_val.animate.set_value(-2), rate_func = there_and_back, run_time = 2)
        self.wait()

        self.play(*[FocusOn(pin.get_corner(DR)) for pin in pins])
        self.wait()

        self.graph, self.pins = graph, pins

    def scaling(self):
        axes, pins, a_val, graph = self.axes, self.pins, self.a_val, self.graph

        dots_mid = VGroup(*[
            Dot(point = axes.c2p(x,0), color = RED)
            for x in [-PI/2, PI/2, 3*PI/2, 5*PI/2]
        ])

        self.play(
            *[FocusOn(dot) for dot in dots_mid], 
            *[GrowFromCenter(dot) for dot in dots_mid]
        )

        dots_sin = VGroup(*[
            Dot(point = axes.c2p(x, np.sin(x)), color = RED)
            for x in [-PI/2, PI/2, 3*PI/2, 5*PI/2]
        ])

        arrows_ref = self.get_arrows(a=1)
        arrows_par = self.get_arrows(a=2.5)

        self.play(
            FadeOut(dots_mid[1], target_position = dots_sin[1].get_center()),
            GrowArrow(arrows_ref[1]), 
            run_time = 2
        )
        self.wait()
        self.play(
            FadeOut(dots_mid[2], target_position = dots_sin[2].get_center()),
            GrowArrow(arrows_ref[2]), 
            run_time = 2
        )
        self.wait()

        self.play(
            *[FadeOut(dots_mid[index], target_position = dots_sin[index].get_center()) for index in [0, -1]],
            *[GrowArrow(arrows_ref[index]) for index in [0, -1]], 
            run_time = 2
        )
        self.wait()

        self.play(Circumscribe(self.a_dec, time_width = 0.75, run_time = 2))
        self.wait()

        self.play(
            AnimationGroup(
                *[ReplacementTransform(arrows_ref[index], arrows_par[index]) for index in [1,2]], 
                lag_ratio = 0.75
            ),
            run_time = 5
        )
        self.wait()
        self.play(
             *[ReplacementTransform(arrows_ref[index], arrows_par[index]) for index in [0,-1]],
             run_time = 2
        )
        self.wait()

        x_marks = self.x_marks = VGroup(*[
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=height_to_color(2.5, -4, 4, self.colors))\
                .move_to(axes.c2p(x, 2.5*np.sin(x)))
            for x in [-PI/2, PI/2, 3*PI/2, 5*PI/2]
        ])
        self.play(DrawBorderThenFill(x_marks), lag_ratio = 0.3, run_time = 3)
        self.play(
            *[GrowArrow(arrow, rate_func = lambda t: smooth(1-t)) for arrow in arrows_par],
            Uncreate(self.graph),
            lag_ratio = 0.2, run_time = 3
        )
        self.wait()

    def different_types(self):
        axes, a_val = self.axes, self.a_val

        graph = axes.get_graph(lambda x: 2.5*np.sin(x), color = height_to_color(2.5, -4, 4, self.colors))
        self.play(Create(graph), run_time = 6)
        self.wait()

        false1 = VMobject()
        false1.set_points_as_corners([
            *[axes.c2p(x, 2.5*np.sin(x)) for x in [-PI, -PI/2, 0, PI/2, PI, 3*PI/2, 2*PI, 5*PI/2]],
            axes.c2p(11*PI/4, 1.25), 
        ])
        false1.set_color(height_to_color(2.5, -4, 4, self.colors))

        self.play(Transform(graph, false1), rate_func = there_and_back_with_pause, run_time = 4)
        self.wait(3)


        self.play(
            AnimationGroup(
                Uncreate(graph), 
                *[FadeOut(x_mark) for x_mark in self.x_marks], 
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()

    def second_example(self):
        a_dec, a_val, axes = self.a_dec, self.a_val, self.axes
        
        a_val.set_value(2.5)
        a_dec.resume_updating()
        self.play(Circumscribe(a_dec, time_width = 0.75, run_time = 2))
        self.play(a_val.animate.set_value(-3.2), run_time = 2)

        arrows_ref = self.get_arrows(a=1)
        arrows_par = self.get_arrows(a=-3.2)

        self.play(
            FocusOn(arrows_ref[1]),
            *[GrowArrow(arrow) for arrow in arrows_ref],
            run_time = 3
        )
        self.wait()

        self.play(ReplacementTransform(arrows_ref[1], arrows_par[1]), run_time = 4)
        self.wait()

        self.play(
            AnimationGroup(
                *[ReplacementTransform(arrows_ref[index], arrows_par[index]) for index in [0,2,3]], 
                lag_ratio = 0.75
            ),
            run_time = 2
        )
        self.wait()

        x_marks = self.x_marks = VGroup(*[
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=height_to_color(-3.2, -4, 4, self.colors))\
                .move_to(axes.c2p(x, -3.2*np.sin(x)))
            for x in [-PI/2, PI/2, 3*PI/2, 5*PI/2]
        ])
        self.play(
            DrawBorderThenFill(x_marks), 
            FadeOut(arrows_par),
            lag_ratio = 0.3, run_time = 3
        )
        self.wait()

        graph = axes.get_graph(lambda x: -3.2*np.sin(x), color = height_to_color(-3.2, -4, 4, self.colors))
        self.play(Create(graph), run_time = 6)
        self.wait(3)


    # functions
    def get_x_axis_numbers(self):
        x_axis_nums = [-np.pi, -np.pi/2, np.pi/2, np.pi, 3/2*np.pi, 2*np.pi, 5*np.pi/2]
        x_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24)\
                .add_background_rectangle()\
                .next_to(self.axes.c2p(num, 0), DOWN)
            for tex, num in zip(
                ["-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi", "5\\pi/2"], 
                x_axis_nums
            )
        ])
        return x_axis_coords

    def get_y_axis_numbers(self):
        y_axis_nums = [-3,-2,-1,1,2,3]
        y_axis_coords = VGroup(*[
            MathTex(num, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for num in y_axis_nums
        ])
        return y_axis_coords

    def get_pin(self, height):
        pin = SVGMobject("pin")
        pin.set(height = height)

        return pin

    def get_arrows(self, a, **kwargs):
        axes, a_val = self.axes, self.a_val
        arrows = VGroup(*[
            Arrow(
                axes.c2p(x, 0), 
                axes.c2p(x, a * np.sin(x)), 
                buff = 0, color = height_to_color(a, -4, 4, self.colors),
                **kwargs
            )
            for x in [-PI/2, PI/2, 3*PI/2, 5*PI/2]
        ])

        return arrows


class LastVideo(Scene):
    def construct(self):
        frame = ScreenRectangle(height = 6.5)\
            .to_edge(DOWN)\
            .set_color([GREY, YELLOW_A, BLUE_A])

        title = Tex("Letztes Video")\
            .scale(1.5)\
            .next_to(frame, UP)

        self.play(
            Write(title),
            Create(frame, run_time = 2), 
        )
        self.wait(3)


class ReadEquation(HowToDrawGraphs):
    def construct(self):
        axes = self.axes = NumberPlane(
            x_range = [-np.pi, 11/4*np.pi, 1], y_range = [-3.99, 3.99, 1/4*np.pi], 
            x_length = config["frame_width"] - 2, y_length = config["frame_height"] - 2, 
            background_line_style = {"stroke_color": BLUE_E, "stroke_width": 1}, 
        )
        axes.to_edge(DOWN)
        axes.x_axis.add_tip(tip_length = 0.25)
        axes.y_axis.add_tip(tip_length = 0.25)

        self.x_axis_label = MathTex("x", color = GREY, font_size = 40).next_to(axes.x_axis, UP, aligned_edge=RIGHT)
        self.y_axis_label = MathTex("y", color = GREY, font_size = 40).next_to(axes.y_axis, UP)
        self.x_axis_numbers = self.get_x_axis_numbers()
        self.y_axis_numbers = self.get_y_axis_numbers()
        self.origin = axes.c2p(0,0)

        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]
        self.a_val = ValueTracker(1.5)


        self.setup_scene()
        self.func_tex()
        self.from_arrows_to_func()
        self.triangle_rotation()


    def setup_scene(self):
        a_val = self.a_val

        self.graph = always_redraw(lambda: 
            self.axes.get_graph(
                lambda x: a_val.get_value() * np.sin(x), 
                x_range = [-np.pi, 11/4*np.pi],
                color = height_to_color(a_val.get_value(), -4, 4, self.colors)
            )
        )
        starting_mobs = VGroup(
            self.axes, self.x_axis_label, self.y_axis_label, self.x_axis_numbers, self.y_axis_numbers
        )
        self.play(
            Create(starting_mobs, lag_ratio = 0.2), 
            Create(self.graph),
            run_time = 3
        )
        self.wait()

    def func_tex(self):
        a_val = self.a_val

        #               0    1    2    3    4     5         6        7      8    9   10
        func = MathTex("f", "(", "x", ")", "=", "para", "\\cdot", "\\sin", "(", "x", ")")\
            .scale(1.25)\
            .to_edge(UP)\
            .shift(RIGHT)
        black_out = func.get_parts_by_tex("para")
        black_out.set_color(BLACK).set_fill(opacity = 0)

        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign=True)\
            .scale(1.25)\
            .next_to(func[6:8], LEFT)\
            .set_color(height_to_color(a_val.get_value(), -4, 4, self.colors))
        a_dec.add_updater(lambda a: 
            a.set_value(a_val.get_value()).set_color(height_to_color(a_val.get_value(), -4, 4, self.colors))
        )

        self.play(
            Write(func), 
        )
        self.wait(2)

        self.a_dec = a_dec

    def from_arrows_to_func(self):
        arrows = always_redraw(lambda: 
            self.get_arrows(a = self.a_val.get_value(), stroke_opacity = 0.6, tip_style = {"fill_opacity": 0.6})
        )

        self.play(
            Create(arrows, lag_ratio = 0.25), 
            FocusOn(arrows[1]),
            run_time = 3
        )
        self.wait(3)

        brace = always_redraw(lambda: 
            Brace(arrows[1], RIGHT, buff = 0.1, color = GREY)
        )
        brace_tex = brace.get_tex("=", "+", "1.5").add_background_rectangle()

        self.play(Create(brace), run_time = 1.5)
        self.play(FadeIn(brace_tex, shift = 2*LEFT), run_time = 1.5)
        self.wait()

        self.play(
            GrowFromPoint(brace_tex, point = self.a_dec.get_center(), rate_func = lambda t: smooth(1-t), run_time = 2),
            Write(self.a_dec, run_time = 1.5),
        )
        self.wait()


        self.a_dec.suspend_updating()
        self.play(self.a_val.animate.set_value(-2.8), run_time = 2)
        self.wait(3)


        brace_tex = brace.get_tex("=", "-", "2.8").add_background_rectangle()
        self.play(FadeIn(brace_tex, shift = 2*LEFT), run_time = 1.5)
        self.wait()


        self.graph.clear_updaters()
        brace.clear_updaters()
        arrows.clear_updaters()
        self.a_dec.resume_updating()
        self.a_val.set_value(1.5)
        self.play(
            GrowFromPoint(brace_tex, point = self.a_dec.get_center(), rate_func = lambda t: smooth(1-t), run_time = 2),
            self.a_val.animate.set_value(-2.8)
        )
        self.wait(3)

    def triangle_rotation(self):
        triangle = Triangle()\
            .set_color(color = [RED, BLUE, YELLOW])\
            .set_stroke(width = 5)\
            .set_fill(color = BLACK, opacity = 1)

        def update_triangle(mob, dt):
            mob.rotate(270*DEGREES * dt, about_point = ORIGIN)

        triangle.add_updater(update_triangle)
        self.play(GrowFromPoint(triangle, 5*UP))
        self.wait()

        self.play(triangle.animate.scale(50))
        self.wait()


class Thumbnail2(HowToDrawGraphs):
    def construct(self):
        axes = self.axes = NumberPlane(
            x_range = [-np.pi/4, 9/4*np.pi, 1], y_range = [-2.49, 2.49, 1/4*np.pi], 
            x_length = config["frame_width"] - 6, y_length = config["frame_height"]/2, 
            background_line_style = {"stroke_color": BLUE_E, "stroke_width": 1}, 
        )
        axes.to_edge(DOWN)
        axes.x_axis.add_tip(tip_length = 0.25)
        axes.y_axis.add_tip(tip_length = 0.25)

        self.x_axis_label = MathTex("x", color = GREY, font_size = 40).next_to(axes.x_axis, UP, aligned_edge=RIGHT)
        self.y_axis_label = MathTex("y", color = GREY, font_size = 40).next_to(axes.y_axis, UP)
        self.x_axis_numbers = self.get_x_axis_numbers()
        self.y_axis_numbers = self.get_y_axis_numbers()
        self.origin = axes.c2p(0,0)

        self.colors = [GREEN, YELLOW_E, YELLOW, WHITE, RED, BLUE, BLUE_E]

        self.a_val = ValueTracker(2.5)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.add(self.axes, self.x_axis_label, self.y_axis_label, self.x_axis_numbers, self.y_axis_numbers)
        self.remove(self.x_axis_numbers[0], self.x_axis_numbers[1], self.x_axis_numbers[-1], self.y_axis_numbers[0], self.y_axis_numbers[-1])


        #               0    1    2    3    4     5         6        7      8    9   10
        func = MathTex("f", "(", "x", ")", "=", "para", "\\cdot", "\\sin", "(", "x", ")")\
            .scale(2)\
            .to_edge(UP)
        black_out = func.get_parts_by_tex("para")
        black_out.set_color(BLACK).set_fill(opacity = 0)

        a_val = self.a_val
        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=1, include_sign=True)\
            .scale(2)\
            .next_to(func[6:8], LEFT)\
            .set_color(YELLOW)
        a_dec.add_updater(lambda a: 
            a.set_value(a_val.get_value()).set_color(YELLOW)
        )

        pin_x_coords = [k*np.pi for k in range(0, 3)]
        pins = VGroup()
        for k in pin_x_coords:
            pin = self.get_pin(height = 0.6)
            pin.next_to(axes.c2p(k, 0), UP, buff = 0, aligned_edge = RIGHT)
            pins.add(pin)

        x_marks = VGroup(*[
            Tex(XMARK_TEX, tex_template = self.myTemplate, color=YELLOW)\
                .set_fill(opacity = 0)\
                .set_stroke(width = 2, color = YELLOW)
                .move_to(axes.c2p(x, 2.5*np.sin(x)))
            for x in [PI/2, 3*PI/2]
        ])

        graph = axes.get_graph(lambda x: 2.5*np.sin(x), x_range=[0, TAU], color = YELLOW)

        self.add(pins, x_marks, func, a_dec, graph)


        arrow1 = Arc(radius = 3.25, start_angle = 40*DEGREES, angle = -80*DEGREES)\
            .add_tip()\
            .set_color(BLUE_E)\
            .to_edge(RIGHT, buff = 1)\
            .set_stroke(width = 10)\
            .set_fill(opacity = 0)

        arrow2 = arrow1.copy()\
            .rotate(180*DEGREES)\
            .set_color(GREEN_E)\
            .to_edge(LEFT, buff = 1)

        self.add(arrow1, arrow2)



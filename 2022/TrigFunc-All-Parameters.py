from pickle import FALSE
from manim import *


XMARK_TEX = "\\ding{55}"


# SCENE FOR DETERMINE SINE-EQUATIONS

class Explanation(Scene):
    def construct(self):

        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 2, 2, PI/2, 1

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/4)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/4], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings, font_size = 30)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY, font_size = 30)


        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.setup_scene(animate = True)
        self.getting_startet_cd()
        self.period_and_b()
        self.parameter_a()
        self.write_equation()


    def setup_scene(self, animate = True):
        num_lines, num_decimals, num_dots = self.num_lines, self.num_decimals, self.num_dots
        axes = self.axes

        graph_stat = self.graph_stat = axes.get_graph(
            lambda x: self.sin_func(x, self.a_stat, self.b_stat, self.c_stat, self.d_stat), 
            x_range = [-TAU, TAU], color = YELLOW
        )
        graph_stat_per = self.graph_stat_per = axes.get_graph(
            lambda x: self.sin_func(x, self.a_stat, self.b_stat, self.c_stat, self.d_stat), 
            x_range = [-self.c_stat, -self.c_stat + TAU/abs(self.b_stat)], color = YELLOW
        )

        if animate is True:
            self.play(
                AnimationGroup(
                    FadeIn(num_decimals, shift = DOWN, lag_ratio = 0.2),
                    Create(num_lines, lag_ratio = 0.2), 
                    FadeIn(num_dots, shift = UP, lag_ratio = 0.2), 
                    lag_ratio = 0.3
                ), 
                LaggedStartMap(Create, VGroup(axes, self.y_ticks, self.y_nums, self.x_ticks, self.x_nums), lag_ratio = 0.3),
                run_time = 3
            )
            self.wait(0.5)
            self.play(Create(graph_stat), run_time = 3)
            self.wait(0.5)
            self.play(ApplyWave(graph_stat), run_time = 2)
            self.wait()

            self.add(graph_stat_per)
            self.play(graph_stat.animate.set_stroke(opacity = 0.35), run_time = 3)
            dot = Dot(point = graph_stat_per.point_from_proportion(0), color = RED, fill_opacity = 0.75)
            trace = TracedPath(dot.get_center, dissipating_time = 0.2, stroke_width = 6, stroke_opacity = [0.2, 1, 0.2], stroke_color = RED)
            self.add(trace)
            self.play(MoveAlongPath(dot, graph_stat_per), run_time = 5)
            self.play(FadeOut(dot))
            self.wait()

        graph_stat.set_stroke(opacity = 0.35)
        self.add(num_lines, num_dots, num_decimals)
        self.add(axes, self.y_ticks, self.y_nums, self.x_ticks, self.x_nums)
        self.add(graph_stat, graph_stat_per)
        self.wait()

    def getting_startet_cd(self):
        a_val, b_val, c_val, d_val = self.a_val, self.b_val, self.c_val, self.d_val
        axes = self.axes

        graph = self.graph = always_redraw(lambda: axes.get_graph(
            lambda x: self.sin_func(x, a_val.get_value(), b_val.get_value(), c_val.get_value(), d_val.get_value()), 
            x_range = [-c_val.get_value(), -c_val.get_value() + TAU/abs(b_val.get_value())], color = BLUE
        ))

        graph2 = axes.get_graph(lambda x: self.sin_func(x, 1, 1, 0, 0), x_range = [0, TAU], color = BLUE)
        graph2.save_state()

        self.play(Create(graph), run_time = 3)
        self.wait()
        self.play(Transform(graph2, self.graph_stat_per), run_time = 3)
        self.wait()
        self.play(Restore(graph2), run_time = 2)
        self.remove(graph2)

        x_mark_stat = self.get_x_period_start(x_color = YELLOW)\
            .move_to(axes.c2p(-self.c_stat, self.d_stat))
        x_mark_par = always_redraw(lambda: self.get_x_period_start())

        self.x_mark_stat, self.x_mark_par = x_mark_stat, x_mark_par

        self.play(FadeIn(x_mark_par, shift = UP, scale = 2), run_time = 2)
        self.wait()

        self.play(FadeIn(x_mark_stat, shift = RIGHT, scale = 2), run_time = 2)
        self.wait()

        self.play(
            x_mark_par.animate(rate_func = there_and_back_with_pause).move_to(x_mark_stat), 
            run_time = 6
        )
        self.wait()


        # Mit Parameter c nach links verschieben
        c_arrow = Arrow(axes.c2p(0,0), axes.c2p(-self.c_stat, 0), color = self.num_dots[2].get_color(), buff = 0)
        d_arrow = Arrow(axes.c2p(-self.c_stat, 0), axes.c2p(-self.c_stat, self.d_stat), color = self.num_dots[3].get_color(), buff = 0)

        self.play(
            GrowArrow(c_arrow), 
            c_val.animate.set_value(self.c_stat), 
            run_time = 4
        )
        self.wait()

        c_sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = self.colors[2]) for mob in 
            [VGroup(self.num_lines[2], self.num_decimals[2]), self.x_nums[3], self.num_decimals[2][1]]
        ])
        self.play(
            Create(c_sur_rects[0]),
            FadeOut(c_arrow),
            run_time = 3
        )
        self.wait()

        self.play(FadeIn(c_sur_rects[1], scale = 3), run_time = 3)
        self.wait()

        self.play(Transform(c_sur_rects[0], c_sur_rects[2]), run_time = 3)
        self.wait()

        self.play(FadeOut(VGroup(c_sur_rects[0], c_sur_rects[1])), run_time = 2)
        self.wait()

        # Mit Parameter d nach oben verschieben
        self.play(
            GrowArrow(d_arrow), 
            d_val.animate.set_value(self.d_stat),
            run_time = 4 
        )
        self.wait()
        d_sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = self.colors[3]) for mob in 
            [VGroup(self.num_lines[3], self.num_decimals[3]), self.num_decimals[3][1]]
        ])
        self.play(Create(d_sur_rects[0]), run_time = 3)
        self.wait()

        self.play(Transform(d_sur_rects[0], d_sur_rects[1]), run_time = 3)
        self.wait()

        self.play(FadeOut(VGroup(d_sur_rects[0], d_arrow), lag_ratio = 0.25), run_time = 2)
        self.wait(2)

    def period_and_b(self):
        arrow_par = self.get_period_arrow(TAU, -3, self.graph)
        arrow_stat = self.get_period_arrow(PI, -2, self.graph_stat_per)

        self.play(TransformFromCopy(self.graph, arrow_par), run_time = 1.5)
        self.wait(0.5)
        self.play(TransformFromCopy(self.graph_stat_per, arrow_stat), run_time = 1.5)
        self.wait()

        arrow_par2 = self.get_period_arrow(PI, -3, self.graph)
        self.play(
            Transform(arrow_par, arrow_par2),
            self.b_val.animate.set_value(self.b_stat),
            rate_func = there_and_back_with_pause, run_time = 5
        )
        self.wait()


        p_tex1 = MathTex("p")\
            .next_to(arrow_stat, UP, buff = 0.05)\
            .add_background_rectangle(buff = 0.2)
        p_tex2 = MathTex("p", "=", "\\pi")\
            .next_to(arrow_stat, UP, buff = 0.05)\
            .add_background_rectangle(buff = 0.2)

        p_gen1 = MathTex("p", "=", "{2\\pi", "\\over", "b")\
            .move_to(self.axes.c2p(-5*PI/4, -2))\
            .add_background_rectangle()
        p_gen2 = MathTex("b", "=", "{2\\pi", "\\over", "p")\
            .move_to(p_gen1)\
            .add_background_rectangle()

        self.play(
            FadeIn(p_tex1[0]), 
            Write(p_tex1[1])
        )
        self.wait()

        # Periode als 2PI / b
        self.play(
            FadeIn(p_gen1[0], run_time = 1),
            TransformFromCopy(p_tex1[1], p_gen1[1], run_time = 2),
        )
        self.play(Write(p_gen1[2:]))
        self.play(Circumscribe(p_gen1[1:], color = YELLOW, fadeout = True, run_time = 2))
        self.wait()

        self.play(
            ReplacementTransform(p_gen1[0], p_gen2[0]),
            ReplacementTransform(p_gen1[1:], p_gen2[1:]),
            run_time = 3
        )
        self.wait()

        sur_rects = VGroup(*[
            SurroundingRectangle(num, color = color) for num, color in zip([self.x_nums[3], self.x_nums[4]], [GREEN_A, GREEN_E])
        ])
        self.play(LaggedStartMap(Create, sur_rects, lag_ratio = 0.25), run_time = 3)
        self.wait()

        # calculate period
        bg = Rectangle(height = 2, width = 4.5, stroke_width = 0)
        bg.set_fill(color = BLACK, opacity = 0.75)
        bg.shift(4.25*LEFT + 1*UP)

        p_calc = MathTex("p", "=", "\\pi/2", "-", "\\big(", "-", "\\pi/2", "\\big)")\
            .next_to(bg.get_bottom(), UP)

        self.play(FadeIn(bg))
        self.play(Write(p_calc[:2]))
        self.wait()

        text = Tex("Ende ", "$-$", " Anfang").next_to(bg.get_top(), DOWN)
        text[0].set_color(GREEN_E)
        text[2].set_color(GREEN_A)

        self.play(ShowIncreasingSubsets(text), run_time = 2)
        self.wait()

        self.play(ReplacementTransform(sur_rects[1], p_calc[2]), run_time = 3)
        self.wait()

        self.play(ReplacementTransform(text[1].copy(), p_calc[3]), run_time = 2)
        self.wait()

        self.play(ReplacementTransform(sur_rects[0], p_calc[4:]), run_time = 3)
        self.wait()


        self.play(FocusOn(p_tex1))

        self.play(
            ReplacementTransform(p_tex1[0], p_tex2[0]),
            ReplacementTransform(p_tex1[1], p_tex2[1:]),
            run_time = 1.5
        )

        self.play(Flash(p_tex2[-1], color = GREEN), run_time = 2)
        self.wait()

        # fadeout p calculation
        self.play(
            FadeOut(VGroup(bg, text, p_calc), run_time = 1.5)
        )
        self.wait()

        # p = pi in zweiter Gleichung ersetzen
        pi = p_tex2[-1].copy()
        pi.generate_target()
        pi.target.move_to(p_gen2[-1])

        self.play(
            MoveToTarget(pi), 
            FadeOut(p_gen2[-1], shift = DOWN), 
            run_time = 3
        )
        self.wait()

        self.play(
            self.b_val.animate.set_value(self.b_stat), 
            run_time = 4
        )
        self.wait()


        self.play(FadeOut(VGroup(arrow_par, arrow_stat, p_tex2[1:], p_tex2[0], p_gen2[1:], p_gen2[0], pi)))
        self.wait()

    def parameter_a(self):
        axes, a_val, = self.axes, self.a_val
        arrows_sin = VGroup(*[
            Arrow(
                axes.c2p(-self.c_stat + factor * TAU/abs(self.b_stat), self.d_stat), 
                axes.c2p(-self.c_stat + factor * TAU/abs(self.b_stat), self.d_stat + direc * 1), 
                buff = 1, color = BLUE
            )
            for factor, direc in zip([1/4, 3/4], [1, -1])
        ])

        arrows_a = VGroup(*[
            Arrow(
                axes.c2p(-self.c_stat + factor * TAU/abs(self.b_stat), self.d_stat), 
                axes.c2p(-self.c_stat + factor * TAU/abs(self.b_stat), self.d_stat + direc * self.a_stat), 
                buff = 1, color = YELLOW
            )
            for factor, direc in zip([1/4, 3/4], [1, -1])
        ])


        self.play(Create(arrows_sin, lag_ratio = 0.25), run_time = 3)
        self.wait()

        self.play(
            Transform(arrows_sin[0], arrows_a[0]), 
            Transform(arrows_sin[1], arrows_a[1]), 
            run_time = 3
        )
        self.wait()


        self.play(Circumscribe(VGroup(self.num_lines[0], self.num_decimals[0]), fade_out = True, color = self.colors[0], run_time = 4))
        self.wait()

        self.play(
            self.a_val.animate.set_value(self.a_stat),
            FadeOut(arrows_sin),
            FadeOut(self.x_mark_stat), 
            FadeOut(self.x_mark_par),
            run_time = 3
        )
        self.wait(3)

    def write_equation(self):
        #               0    1    2      3          4        5      6       7      8    9   10      11     12      13     14   15
        func = MathTex("y", "=", "2", "\\cdot", "\\sin", "\\big(", "2", "\\cdot", "(", "x", "+", "\\pi/2", ")", "\\big)", "+", "1")
        func.scale(1.75)
        func.to_edge(DOWN, buff = 1)
        for i in 2,6,11, 15:
            func[i].set_color(BLACK)

        bg = BackgroundRectangle(func, buff = 0.2)

        self.play(Create(bg), run_time = 2)
        self.wait()

        self.play(Create(func), run_time = 2)
        self.wait()


        par_num = range(0, len(self.num_decimals))
        func_index = [2, 6, 11, 15]

        for parameter, index in zip(par_num, func_index):
            #                                       1: means not taking sign
            value = self.num_decimals[parameter][1][1:].copy()
            value.generate_target()
            value.target.move_to(func[index]).fade(1)

            self.play(
                MoveToTarget(value), 
                FadeToColor(func[index], WHITE),
                run_time = 2
            )
        self.wait()
        self.play(Circumscribe(func, color = BLUE, fade_out=True, run_time = 4))
        self.wait(3)




    # graph functions
    def sin_func(self, x, a, b, c, d):
        return a*np.sin(b*(x + c)) + d

    def get_x_axis_ticks(self, numbers, tick_length = 0.2):
        ticks = VGroup()
        for num in numbers:
            tick = Line(UP, DOWN, color = LIGHT_GREY)\
                .set_length(tick_length)\
                .move_to(self.axes.c2p(num, 0))
            ticks.add(tick)
        return ticks

    def get_x_axis_numbers(self, numbers, strings, **kwargs):
        axis_numbers = VGroup()
        for num, string in zip(numbers, strings):
            tex = MathTex(string, color = LIGHT_GREY, **kwargs)
            tex.scale(5/8)
            tex.next_to(self.axes.c2p(num, 0), DOWN)
            axis_numbers.add(tex)
        return axis_numbers

    def get_y_axis_ticks(self, numbers, tick_length = 0.2, **kwargs):
        ticks = VGroup()
        for y in numbers:
            tick = Line(LEFT, RIGHT, color = LIGHT_GREY, **kwargs)\
                .set_length(tick_length)\
                .move_to(self.axes.c2p(0, y))
            ticks.add(tick)
        return ticks

    def get_y_axis_numbers(self, numbers, **kwargs):
        axis_numbers = VGroup()
        for y in numbers:
            num = MathTex(str(y), **kwargs)
            num.scale(5/8)
            num.next_to(self.axes.c2p(0, y), LEFT)
            axis_numbers.add(num)
        return axis_numbers

    def get_x_period_start(self, x_color = BLUE):
        xmark = Tex(XMARK_TEX, tex_template = self.myTemplate, color = x_color)\
            .move_to(self.axes.c2p(-self.c_val.get_value(), self.d_val.get_value()))

        return xmark

    def get_period_arrow(self, length, axes_height, graph):
        axes, b_stat, c_stat = self.axes, self.b_stat, self.c_stat
        arrow = DoubleArrow(
            start = axes.c2p(-c_stat, axes_height), end = axes.c2p(-c_stat + length, axes_height), 
            color = graph.get_color(), buff = 0
        )
        return arrow

    # numberlines functions
    def get_num_line(self, x_min, x_max, x_step, line_length = config["frame_width"]/5, **kwargs):
        num_line = NumberLine(
            x_range = [x_min, x_max, x_step], length = line_length, color = WHITE,
            label_direction = DOWN, decimal_number_config = {"num_decimal_places": 0, "color": LIGHT_GREY}, font_size = 30,
            **kwargs
        )
        return num_line

    def get_c_line_texs(self, numbers, strings):
        texs = VGroup()
        for num, string in zip(numbers, strings):
            tex = MathTex(string, color = LIGHT_GREY, font_size = 30)
            tex.next_to(self.num_lines[2].n2p(num), DOWN)
            texs.add(tex)
        return texs

    def get_num_line_dot(self, num_line, val_tracker, dot_color):
        dot = always_redraw(lambda: Dot(point = num_line.n2p(val_tracker.get_value()), color = dot_color)\
            .set_sheen(-0.3, DR)\
            .set_stroke(width = 1, color = WHITE)
        )
        return dot

    def get_tex_dec(self, val_tracker, val_tex, num_line, val_color):
        tex = MathTex(val_tex, "=")
        tex[0].set_color(val_color)
        dec = always_redraw(lambda: DecimalNumber(val_tracker.get_value(), include_sign=True).next_to(tex, RIGHT, aligned_edge=DOWN))

        result = VGroup(tex, dec)
        result.next_to(num_line, UP)

        return result


class Intro(Explanation):
    def construct(self):
        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 1.5, 3/4, 2*PI/3, 2

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/3)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/3], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        # self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        # self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_tick_numbers = [-TAU, -5*PI/3, -4*PI/3, -PI, -2*PI/3, -PI/3, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3, TAU]
        self.x_tick_strings = ["-2\\pi", "-5\\pi/3", "-4\\pi/3", "-\\pi", "-2\\pi/3", "-\\pi/3", "\\pi/3", "2\\pi/3", "\\pi", "4\\pi/3", "5\\pi/3", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY)


        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.setup_scene(animate = True)
        self.wait()
        self.transform_sine_curve()


    def transform_sine_curve(self):
        axes = self.axes
        a_val, b_val, c_val, d_val = self.a_val, self.b_val, self.c_val, self.d_val 
        a_stat, b_stat, c_stat, d_stat = self.a_stat, self.b_stat, self.c_stat, self.d_stat

        graph = self.graph = always_redraw(lambda: axes.get_graph(
            lambda x: self.sin_func(x, a_val.get_value(), b_val.get_value(), c_val.get_value(), d_val.get_value()), 
            x_range = [-c_val.get_value(), -c_val.get_value() + TAU/abs(b_val.get_value())], color = BLUE
        ))

        mid_line = Line(LEFT, RIGHT)
        mid_line.set_length((2*TAU + 1.5)*axes.x_axis.unit_size)
        mid_line.move_to(axes.c2p(0, d_stat))
        dashed_line = DashedVMobject(mid_line)

        self.play(
            Create(graph),
            Create(dashed_line),
            run_time = 1.5
        )
        self.wait()

        index_list = reversed(range(0, len(self.num_lines)))
        tracker_stat_list = reversed([a_stat, b_stat, c_stat, d_stat])

        for index, stat_value in zip(index_list, tracker_stat_list):
            self.play(
                Circumscribe(VGroup(self.num_decimals[index], self.num_lines[index]), color = self.colors[index], run_time = 2), 
                self.tracker_list[index].animate(run_time = 2).set_value(stat_value), 
            )
            self.wait(0.75)
        self.wait()


class Fast2(Intro):
    def construct(self):
        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 3, 3/2, -PI/3, -1

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-3, 3, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/3)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/3], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        # self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        # self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_tick_numbers = [-TAU, -PI, PI/3, PI, 5*PI/3, TAU]
        self.x_tick_strings = ["-2\\pi", "-\\pi", "\\pi/3", "\\pi", "5\\pi/3", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings, font_size = 30)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY, font_size = 30)

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.setup_scene(animate = True)
        self.wait()
        self.transform_sine_curve()
        self.parameter_b()
        self.parameter_a()
        self.write_equation()


    def transform_sine_curve(self):
        axes = self.axes
        a_val, b_val, c_val, d_val = self.a_val, self.b_val, self.c_val, self.d_val 
        a_stat, b_stat, c_stat, d_stat = self.a_stat, self.b_stat, self.c_stat, self.d_stat

        graph = self.graph = always_redraw(lambda: axes.get_graph(
            lambda x: self.sin_func(x, a_val.get_value(), b_val.get_value(), c_val.get_value(), d_val.get_value()), 
            x_range = [-c_val.get_value(), -c_val.get_value() + TAU/abs(b_val.get_value())], color = BLUE
        ))

        mid_line = Line(LEFT, RIGHT)
        mid_line.set_length((2*TAU + 1.5)*axes.x_axis.unit_size)
        mid_line.move_to(axes.c2p(0, d_stat))
        dashed_line = DashedVMobject(mid_line)

        self.play(
            Create(graph),
            Create(dashed_line),
            run_time = 1.5
        )
        self.wait()


        for index, stat_value in zip([3,2], [d_stat, c_stat]):
            self.play(
                Circumscribe(VGroup(self.num_decimals[index], self.num_lines[index]), color = self.colors[index], run_time = 2), 
                self.tracker_list[index].animate(run_time = 2).set_value(stat_value), 
            )
            self.wait(0.75)
        self.wait()

        self.play(
            Circumscribe(VGroup(self.num_decimals[1], self.num_lines[1]), color = self.colors[1], run_time = 2),
        )

    def parameter_b(self):
        end_start_rects = VGroup(*[
            SurroundingRectangle(mob, color = rect_color) 
            for mob, rect_color in zip([self.x_nums[2], self.x_nums[4]], [RED_A, RED_E])
        ])

        bg = Rectangle(height = 2, width = 5.5, stroke_width = 0)
        bg.set_fill(color = BLACK, opacity = 0.75)
        bg.shift(4.25*LEFT + 1*UP)

        p_calc = MathTex("p", "=", "5\\pi/3", "-", "\\pi/3", "=", "4\\pi/3")\
            .next_to(bg.get_bottom(), UP)

        end_start_text = Tex("Ende ", "$-$", " Anfang").next_to(bg.get_top(), DOWN)
        end_start_text[0].set_color(RED_E)
        end_start_text[2].set_color(RED_A)

        self.play(
            FocusOn(self.x_nums[2]),
            FocusOn(self.x_nums[4]), 
            Create(end_start_rects, lag_ratio = 0.15),
            run_time = 2
        )
        self.play(
            FadeIn(bg), 
            Write(end_start_text),
        )
        self.wait()

        self.play(Write(p_calc[:-2]))
        self.wait()
        self.play(Write(p_calc[-2:]))
        self.wait()

        bg2 = Rectangle(height = 2, width = 4.5, stroke_width = 0)
        bg2.set_fill(color = BLACK, opacity = 0.75)
        bg2.shift(4.25*LEFT + 2*DOWN)

        b_calc0 = MathTex("b", "=", "{2\\pi", "\\over", "p}")\
            .move_to(bg2)
        b_calc1 = MathTex("b", "=", "{2\\pi", "\\over", "4\\pi/3}")\
            .move_to(bg2)
        b_calc2 = MathTex("b", "=", "2\\pi", "\\cdot", "\\frac{3}{4\\pi}")\
            .move_to(b_calc1, aligned_edge=LEFT)
        
        b_final = MathTex("=", "\\frac{3}{2}")\
            .next_to(b_calc2, RIGHT)

        self.play(
            FadeOut(end_start_rects),
            FadeIn(bg2), 
            Write(b_calc0)
        )
        self.wait(0.5)
        self.play(ReplacementTransform(b_calc0, b_calc1))
        self.wait()
        self.play(TransformMatchingShapes(b_calc1, b_calc2))
        self.wait()

        self.play(
            bg2.animate.shift(0.75*RIGHT),
            Write(b_final)
        )
        self.wait()

        self.play(
            Circumscribe(VGroup(self.num_decimals[1], self.num_lines[1]), color = self.colors[1], run_time = 4), 
            self.tracker_list[1].animate(run_time = 4).set_value(self.b_stat), 
        )
        self.wait()


        self.play(
            FadeOut(VGroup(bg2, b_final, b_calc2, bg, p_calc, end_start_text), lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()

    def parameter_a(self):
        arrows1 = self.get_arrows_a(height = 1)
        arrows2 = self.get_arrows_a(height = 2)
        arrows3 = self.get_arrows_a(height = 3)
        self.play(
            LaggedStartMap(GrowArrow, arrows1, lag_ratio = 0.15), 
            run_time = 2
        )
        self.wait()

        self.play(
            Transform(arrows1, arrows2), 
            self.tracker_list[0].animate.set_value(2), 
            run_time = 2
        )
        self.play(
            Transform(arrows1, arrows3), 
            self.tracker_list[0].animate.set_value(self.a_stat), 
            run_time = 2
        )
        self.wait()

        self.play(
            FadeOut(arrows1, run_time = 2),
            Circumscribe(VGroup(self.num_decimals[0], self.num_lines[0]), color = self.colors[0], run_time = 4), 
        )
        self.wait()

    def write_equation(self):
        #               0    1    2      3          4        5      6       7      8    9   10      11     12      13     14   15
        func = MathTex("y", "=", "3", "\\cdot", "\\sin", "\\big(", "1.5", "\\cdot", "(", "x", "-", "\\pi/3", ")", "\\big)", "-", "1")
        func.scale(1.75)
        func.next_to(self.axes.get_top(), DOWN, buff = 0)
        func.shift(0.2*DOWN)
        for i in 2,6,11, 15:
            func[i].set_color(BLACK)

        bg = BackgroundRectangle(func, buff = 0.2)
        self.play(Create(bg), Create(func), run_time = 2)


        par_num = range(0, len(self.num_decimals))
        func_index = [2, 6, 11, 15]

        for parameter, index in zip(par_num, func_index):
            #                                       1: means not taking sign
            value = self.num_decimals[parameter][1][1:].copy()
            value.generate_target()
            value.target.move_to(func[index]).fade(1)

            self.play(
                MoveToTarget(value), 
                FadeToColor(func[index], WHITE),
                run_time = 1
            )
        self.wait()
        self.play(Circumscribe(func, color = BLUE, fade_out=True, run_time = 4))
        self.wait(3)

    # functions
    def get_arrows_a(self, height):
        axes, b_stat, c_stat, d_stat = self.axes, self.b_stat, self.c_stat, self.d_stat
        return VGroup(*[
            Arrow(start, end, color = BLUE, buff = 0)
            for start, end in zip(
                [axes.c2p(-c_stat + 1/4 * 2*PI/b_stat, d_stat), axes.c2p(-c_stat + 3/4 * 2*PI/b_stat, d_stat)], 
                [axes.c2p(-c_stat + 1/4 * 2*PI/b_stat, d_stat + height), axes.c2p(-c_stat + 3/4 * 2*PI/b_stat, d_stat - height)], 
            )
        ])


class Fast3(Intro):
    def construct(self):
        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 2, 2, -PI/2, -1

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/2)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/2], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        # self.x_tick_numbers = [-TAU, -5*PI/3, -4*PI/3, -PI, -2*PI/3, -PI/3, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3, TAU]
        # self.x_tick_strings = ["-2\\pi", "-5\\pi/3", "-4\\pi/3", "-\\pi", "-2\\pi/3", "-\\pi/3", "\\pi/3", "2\\pi/3", "\\pi", "4\\pi/3", "5\\pi/3", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings, font_size = 30)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY, font_size = 30)


        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.setup_scene(animate = True)
        self.wait()
        self.transform_sine_curve()
        self.write_equation()

    def write_equation(self):
        #               0    1    2      3          4        5      6       7      8    9   10      11     12      13     14   15
        func = MathTex("y", "=", "2", "\\cdot", "\\sin", "\\big(", "2", "\\cdot", "(", "x", "-", "\\pi/2", ")", "\\big)", "-", "1")
        func.scale(1.75)
        func.next_to(self.axes.get_top(), DOWN, buff = 0)
        func.shift(0.2*DOWN)
        for i in 2,6,11, 15:
            func[i].set_color(BLACK)

        bg = BackgroundRectangle(func, buff = 0.2)
        self.play(Create(bg), Create(func), run_time = 2)


        par_num = range(0, len(self.num_decimals))
        func_index = [2, 6, 11, 15]

        for parameter, index in zip(par_num, func_index):
            #                                       1: means not taking sign
            value = self.num_decimals[parameter][1][1:].copy()
            value.generate_target()
            value.target.move_to(func[index]).fade(1)

            self.play(
                MoveToTarget(value), 
                FadeToColor(func[index], WHITE),
                run_time = 1
            )
        self.wait()
        self.play(Circumscribe(func, color = BLUE, fade_out=True, run_time = 4))
        self.wait(3)


class Fast4(Intro):
    def construct(self):
        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 0.5, 0.75, PI, 2

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/2)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/3], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        # self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        # self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_tick_numbers = [-TAU, -5*PI/3, -4*PI/3, -PI, -2*PI/3, -PI/3, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3, TAU]
        self.x_tick_strings = ["-2\\pi", "-5\\pi/3", "-4\\pi/3", "-\\pi", "-2\\pi/3", "-\\pi/3", "\\pi/3", "2\\pi/3", "\\pi", "4\\pi/3", "5\\pi/3", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings, font_size = 30)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY, font_size = 30)


        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.setup_scene(animate = False)
        self.wait()
        self.transform_sine_curve()
        self.write_equation()

    def write_equation(self):
        #               0    1          2            3          4        5           6             7      8    9   10     11    12      13     14   15
        func = MathTex("y", "=", "\\frac{1}{2}", "\\cdot", "\\sin", "\\left(", "\\frac{3}{4}", "\\cdot", "(", "x", "+", "\\pi", ")", "\\right)", "+", "2")
        func.scale(1.75)
        func.next_to(self.axes.get_bottom(), UP, buff = 0)
        func.shift(0.2*UP)
        for i in 2,6,11, 15:
            func[i].set_color(BLACK)

        bg = BackgroundRectangle(func, buff = 0.2)
        self.play(Create(bg), Create(func), run_time = 2)


        par_num = range(0, len(self.num_decimals))
        func_index = [2, 6, 11, 15]

        for parameter, index in zip(par_num, func_index):
            #                                       1: means not taking sign
            value = self.num_decimals[parameter][1][1:].copy()
            value.generate_target()
            value.target.move_to(func[index]).fade(1)

            self.play(
                MoveToTarget(value), 
                FadeToColor(func[index], WHITE),
                run_time = 1
            )
        self.wait()
        self.play(Circumscribe(func, color = BLUE, fade_out=True, run_time = 4))
        self.wait(3)


class Fast5(Intro):
    def construct(self):
        # NUM_LINES STUFF
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 1.5, 1, 2*PI/3, -1.5

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        a_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)
        b_line = self.get_num_line(-2, 2, 1.0, include_numbers = True, numbers_to_exclude = [-1.5, -0.5, 0.5, 1.5])
        c_line = self.get_num_line(-PI, PI, PI/3)
        d_line = self.get_num_line(-2, 2, 1.0, include_numbers = True)

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]
        num_line_list = [a_line, b_line, c_line, d_line]

        self.num_lines = VGroup(a_line, b_line, c_line, d_line)\
            .arrange_submobjects(RIGHT, buff = 0.5, aligned_edge = UP)\
            .to_edge(UP, buff = 0.75)
        c_line_texs = self.get_c_line_texs([-PI, 0, PI], ["-\\pi", "0", "\\pi"])
        self.num_lines[2].add(c_line_texs)

        num_decimals = VGroup(*[
            self.get_tex_dec(val_tracker, val_tex, num_line, color) 
            for val_tracker, val_tex, num_line, color in zip(tracker_list, ["a", "b", "c", "d"], num_line_list, self.colors)
        ])

        num_dots = VGroup(*[
            self.get_num_line_dot(num_line, val_tra, color) for num_line, val_tra, color in zip(num_line_list, tracker_list, self.colors)
        ])
        self.num_decimals, self.num_dots = num_decimals, num_dots

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-4, 4, PI/3], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": LIGHT_GREY},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        # self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        # self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_tick_numbers = [-TAU, -5*PI/3, -4*PI/3, -PI, -2*PI/3, -PI/3, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3, TAU]
        self.x_tick_strings = ["-2\\pi", "-5\\pi/3", "-4\\pi/3", "-\\pi", "-2\\pi/3", "-\\pi/3", "\\pi/3", "2\\pi/3", "\\pi", "4\\pi/3", "5\\pi/3", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings, font_size = 30)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-3,-2,-1,1,2,3], color = LIGHT_GREY, font_size = 30)


        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")


        self.setup_scene(animate = True)
        self.wait()
        self.transform_sine_curve()
        self.write_equation()


    def write_equation(self):
        #               0    1     2       3          4        5       6       7      8    9   10     11    12      13     14   15
        func = MathTex("y", "=", "1.5", "\\cdot", "\\sin", "\\left(", "1", "\\cdot", "(", "x", "+", "2\\pi/3", ")", "\\right)", "-", "1.5")
        func.scale(1.75)
        func.next_to(self.axes.get_top(), DOWN, buff = 0)
        func.shift(0.2*DOWN)
        for i in 2,6,11, 15:
            func[i].set_color(BLACK)

        bg = BackgroundRectangle(func, buff = 0.2)
        self.play(Create(bg), Create(func), run_time = 2)


        par_num = range(0, len(self.num_decimals))
        func_index = [2, 6, 11, 15]

        for parameter, index in zip(par_num, func_index):
            #                                       1: means not taking sign
            value = self.num_decimals[parameter][1][1:].copy()
            value.generate_target()
            value.target.move_to(func[index]).fade(1)

            self.play(
                MoveToTarget(value), 
                FadeToColor(func[index], WHITE),
                run_time = 1
            )
        self.wait()
        self.play(Circumscribe(func, color = BLUE, fade_out=True, run_time = 4))
        self.wait(3)


class Thumbnail(Explanation):
    def construct(self):
        self.colors = [GOLD, MAROON, PINK, GREEN]

        self.a_stat, self.b_stat, self.c_stat, self.d_stat = 3, 2/3, 3*PI/2, 2

        a_val = self.a_val = ValueTracker(1)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(0)
        d_val = self.d_val = ValueTracker(0)
        self.a_val, self.b_val, self.c_val, self.d_val = a_val, b_val, c_val, d_val

        tracker_list = self.tracker_list = [a_val, b_val, c_val, d_val]

        # AXES STUFF
        self.axes_kwargs = {
            "x_range": [-TAU - 0.75, TAU + 0.75, 1], "y_range": [-3, 5, PI/4], 
            "x_length": config["frame_width"] - 1, "y_length": config["frame_height"] - 2,
            "axis_config": {"stroke_color": WHITE},
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 0}
        }
        self.axes = NumberPlane(**self.axes_kwargs)
        self.axes.to_edge(DOWN, buff = 0.5)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.x_tick_numbers = [-TAU, -3*PI/2, -PI, -PI/2, PI/2, PI, 3*PI/2, TAU]
        self.x_tick_strings = ["-2\\pi", "-3\\pi/2", "-\\pi", "-\\pi/2", "\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]
        self.x_ticks = self.get_x_axis_ticks(self.x_tick_numbers)
        self.x_nums = self.get_x_axis_numbers(self.x_tick_numbers, self.x_tick_strings)
        self.y_ticks = self.get_y_axis_ticks([-3,-2,-1,1,2,3])
        self.y_nums = self.get_y_axis_numbers([-2,-1,1,2,3,4], color = LIGHT_GREY)


        graph_stat = self.graph_stat = self.axes.get_graph(
            lambda x: self.sin_func(x, self.a_stat, self.b_stat, self.c_stat, self.d_stat), 
            x_range = [-TAU, TAU], color = BLUE, stroke_opacity = 0.35, stroke_width = 8
        )
        graph_stat_per = self.graph_stat_per = self.axes.get_graph(
            lambda x: self.sin_func(x, self.a_stat, self.b_stat, self.c_stat, self.d_stat), 
            x_range = [-self.c_stat, -self.c_stat + TAU/abs(self.b_stat)], color = BLUE, stroke_width = 8
        )

        title = Tex("Ablesen von \\\\Funktionsgleichungen")
        title.add_background_rectangle()
        title.set(width = 5.5)
        title.move_to(1.5*UP + 3.5*RIGHT)

        #               0    1     2       3        4        5       6       7      8    9   10   11   12      13       14    15
        func = MathTex("y", "=", "a", "\\cdot", "\\sin", "\\left(", "b", "\\cdot", "(", "x", "+", "c", ")", "\\right)", "+", "d")
        func.set(width = self.axes.width - 1)
        func.to_edge(UP, buff = 0.1)

        func_index = [2, 6, 11, 15]
        for i, color in zip(func_index, self.colors):
            func[i].set_color(color)

        arrows_a = VGroup(*[
            Arrow(
                self.axes.c2p(-self.c_stat + prop * 2*PI/self.b_stat, self.d_stat), 
                self.axes.c2p(-self.c_stat + prop * 2*PI/self.b_stat, self.d_stat + factor * self.a_stat), 
                color = self.colors[0], buff = 0
            )
            for prop, factor in zip([1/4, 3/4], [1, -1])
        ])
        arrow_c = Arrow(self.axes.c2p(0,0), self.axes.c2p(-self.c_stat, 0), color = self.colors[2], buff = 0)
        arrow_d = Arrow(self.axes.c2p(-self.c_stat, 0), self.axes.c2p(-self.c_stat, self.d_stat), color = self.colors[3], buff = 0)
        arrow_p = DoubleArrow(self.axes.c2p(-self.c_stat, -2), self.axes.c2p(-self.c_stat + TAU/self.b_stat, -2), color = self.colors[1], buff = 0)


        a = MathTex("a", color = arrows_a[0].get_color())
        p = MathTex("p", color = arrow_p.get_color())
        c = MathTex("c", color = arrow_c.get_color())
        d = MathTex("d", color = arrow_d.get_color())
        for mob in a, p, c, d:
            mob.scale(1.5)
            mob.add_background_rectangle(opacity = 1, buff = 0.1)
        a.next_to(arrows_a[0], RIGHT, buff = 0.1)
        p.next_to(arrow_p, DOWN, buff = 0.1)
        c.next_to(arrow_c, UP, buff = 0.1)
        d.next_to(arrow_d, RIGHT, buff = 0.1)


        mid_line = DashedLine(
            self.axes.c2p(-TAU - 0.75, self.d_stat), self.axes.c2p(TAU + 0.75, self.d_stat), dash_length = 0.5
        )

        self.add(self.axes, self.y_ticks, self.y_nums, self.x_ticks, self.x_nums)
        self.add(graph_stat, graph_stat_per)
        self.add(func, title)
        self.add(arrows_a, arrow_p, arrow_c, arrow_d)
        self.add(a, p, c, d)
        self.add(mid_line)
        self.wait()




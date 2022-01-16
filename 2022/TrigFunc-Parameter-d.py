from manim import *

XMARK_TEX = "\\ding{55}"

def p2c(y_value, min, max, colors):
    alpha = inverse_interpolate(min, max, y_value)
    index, sub_alpha = integer_interpolate(0, len(colors) - 1, alpha)

    return interpolate_color(colors[index], colors[index + 1], sub_alpha)


class Intro(Scene):
    def construct(self):

        scr = VGroup(*[ScreenRectangle(height = 3, stroke_width = 3, stroke_color = GREY) for x in range(4)])
        scr.arrange_in_grid(2,2)
        scr.to_edge(DOWN, buff = 0.4)

        func = MathTex("f(x)", "=", "a", "\\cdot", "\\sin", "\\big(", "b", "\\cdot", "(", "x", "+", "c", ")","\\big)", "+", "d", font_size = 80)
        func.to_edge(UP, buff = 0.3)
        func[2].set_color(RED)
        func[6].set_color(BLUE)
        func[11].set_color(YELLOW)
        func[-1].set_color(GREEN)

        self.play(
            Create(scr[:-1], lag_ratio = 0.2, run_time = 3), 
            Write(func, run_time = 1), 
        )
        self.wait()

        abcd = VGroup(*[func[index].copy() for index in [2, 6, 11, -1]])
        for alph, rect, direc in zip(abcd, scr, [LEFT, RIGHT, LEFT, RIGHT]):
            alph.generate_target()
            alph.target.next_to(rect, direc)

        self.play(
            LaggedStart(*[MoveToTarget(alph) for alph in abcd[:-1]], lag_ratio = 0.2), 
            run_time = 3
        )
        self.wait()


        sur = SurroundingRectangle(abcd[-1], color = GREEN)
        self.play(Create(sur), run_time = 2)
        self.wait(0.5)
        self.play(FadeOut(sur, scale = 2))
        self.wait()


        self.play(
            MoveToTarget(abcd[-1]), 
            Create(scr[-1]), 
            run_time = 2
        )
        self.wait(3)


        group = Group(*self.mobjects)
        self.play(FadeOut(group, scale = 5), run_time = 1.5)
        self.wait()


class TableToGraph(Scene):
    def construct(self):
        self.x_values = np.linspace(0, 2*np.pi, 9)
        self.sin_values = [round(np.sin(x), 2) for x in self.x_values]
        self.sin_values[-1] = 0.00
        self.sind_values = [x + 2 for x in self.sin_values]

        axes = self.axes = NumberPlane(
            x_range = [0, 9*PI/4, 1], y_range = [-4, 4, PI/4],
            x_length = config["frame_width"] * 2/5, y_length = 7,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        axes.to_edge(RIGHT)
        self.origin = axes.c2p(0,0)
        axes.x_axis.add_tip(tip_length = 0.25)
        axes.y_axis.add_tip(tip_length = 0.25)

        self.x_axis_label = MathTex("x", color = GREY, font_size = 24).next_to(axes.x_axis, UP, buff = 0.1, aligned_edge=RIGHT)
        self.y_axis_label = MathTex("y", color = GREY, font_size = 24).next_to(axes.y_axis, UP, buff = 0.1)

        self.x_axis_numbers =  self.get_x_axis_numbers() 
        self.y_axis_numbers = self.get_y_axis_numbers()

        self.colors = [PINK, YELLOW, GREEN, RED, BLUE]

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.build_table_and_sin_graph()
        self.get_idea_for_new_parameter()
        self.explain_parameter()


    def build_table_and_sin_graph(self):
        x_values, sin_values, sind_values = self.x_values, self.sin_values, self.sind_values
        axes = self.axes

        x_strings = [
            "0", "\\frac{1}{4}\\pi", "\\frac{1}{2}\\pi", "\\frac{3}{4}\\pi", "\\pi", 
            "\\frac{5}{4}\\pi", "\\frac{3}{2}\\pi", "\\frac{7}{4}\\pi", "2\\pi"
        ]

        x_texs = VGroup(*[MathTex(x_str, font_size = 36) for x_str in x_strings])
        for index in [1,2,3,5,6,7]:
            x_texs[index][0][:3].scale(0.65)
        sin_texs = VGroup(*[MathTex(str(sin), font_size = 36) for sin in sin_values])
        sind_texs = VGroup(*[MathTex(str(sind), font_size = 36) for sind in sind_values])


        table = VGroup(*x_texs, *sin_texs, *sind_texs)\
            .arrange_in_grid(rows = len(x_texs), cols = 3, col_widths=[1, 2, 3], flow_order = "dr")\
            .to_edge(LEFT, buff = 1)\
            .shift(0.5*DOWN)


        x_label = MathTex("x", font_size = 40).next_to(table[0], UP, buff = 0.6)
        sin_label = MathTex("\\sin", "(x)", font_size = 40).next_to(table[9], UP, buff = 0.5)
        sind_label = MathTex("\\sin", "(x)", "+", "2", font_size = 40).next_to(table[18], UP, buff = 0.5)
        for label in sin_label, sind_label:
            label.set_color_by_tex_to_color_map({"+": YELLOW, "2": YELLOW, "\\sin": RED})


        self.play(
            Write(x_label),
            FadeIn(x_texs, shift = 0.5*DOWN, lag_ratio = 0.1),
            run_time = 2
        )
        self.wait()

        # Create sin_values and transform dots_x into dots_sin
        dots_axis = VGroup(*[Dot(axes.c2p(x_val, 0), radius = 0.06) for x_val in x_values])
        self.play(
            LaggedStartMap(
                Create, VGroup(axes, self.x_axis_label, self.y_axis_label, self.x_axis_numbers, self.y_axis_numbers), 
                lag_ratio = 0.2, run_time = 2
            ),
            AnimationGroup(
                *[Transform(tex.copy(), dot) for tex, dot in zip(x_texs, dots_axis)], 
                lag_ratio = 0.2, run_time = 3
            ),
        )
        self.wait()

        self.play(
            FocusOn(sin_label, run_time = 1),
            Write(sin_label, rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 2)
        )
        self.play(AnimationGroup(*[Write(tex) for tex in sin_texs], lag_ratio = 0.2, run_time = 2))
        self.wait()

        dots_sin  = VGroup(*[Dot(axes.c2p(x_val, sin_val),  radius = 0.06, color = RED)  for x_val, sin_val in  zip(x_values, sin_values)])
        dots_sin2 = dots_sin.copy()
        graph_sin  = axes.get_graph(lambda x: np.sin(x), x_range = [0, 2*np.pi], color = RED)

        self.play(
            AnimationGroup(
                *[ReplacementTransform(tex.copy(), dot) for tex, dot in zip(sin_texs, dots_sin)], 
                lag_ratio = 0.2, run_time = 3
            ),
        )
        self.add(dots_sin2)

        self.play(
            TransformFromCopy(dots_axis, dots_sin.copy()),
            Create(graph_sin), 
            run_time = 2
        )
        self.remove(dots_sin2)
        self.wait()


        self.x_texs, self.sin_texs, self.sind_texs = x_texs, sin_texs, sind_texs
        self.sin_label, self.sind_label = sin_label, sind_label
        self.graph_sin, self.dots_sin = graph_sin, dots_sin

    def get_idea_for_new_parameter(self):
        sind_label = self.sind_label

        zero_zero_rect = SurroundingRectangle(VGroup(self.x_texs[0], self.sin_texs[0]), color = RED)
        self.play(FadeIn(zero_zero_rect, scale = 5), run_time = 2)
        self.wait()

        xmark = Tex(XMARK_TEX, tex_template = self.myTemplate, color = RED)
        xmark.move_to(self.origin)

        self.play(ReplacementTransform(zero_zero_rect, xmark))
        self.wait()

        trans_group = VGroup(self.graph_sin, self.dots_sin, xmark)
        for c in [-PI, 3*PI/2, -PI/2]:
            self.play(
                trans_group.animate.shift(c * self.axes.x_axis.unit_size * RIGHT), run_time = 1.5
            )
            self.wait(0.5)
        self.wait()


        trans_group2 = trans_group.copy().set_color(BLUE)
        self.add(trans_group2)
        self.bring_to_front(trans_group)
        for d in [1, -3, 4]:
            self.play(
                trans_group2.animate.shift(d * self.axes.y_axis.unit_size * UP), run_time = 1.5
            )
            self.wait(0.5)
        self.wait()

    def explain_parameter(self):
        sin_texs = self.sin_texs
        dots_sind = self.dots_sind = VGroup(*[
            Dot(self.axes.c2p(x_val, sind_val), radius = 0.06, color = BLUE) 
            for x_val, sind_val in zip(self.x_values, self.sind_values)
        ])



        graph_arrows = self.get_graph_arrows()
        table_arrows = self.table_arrows = self.get_table_arrows()
        multiplicators = self.get_multiplicators(number = 2)


        sur_rect_input = SurroundingRectangle(sin_texs[2])
        self.play(Flash(self.dots_sin[2]), run_time = 2)
        self.play(Create(sur_rect_input), run_time = 1.5)
        self.wait()

        self.play(GrowFromEdge(graph_arrows[2], DOWN), run_time = 2)
        self.play(Flash(dots_sind[2]), run_time = 2)
        self.wait()

        sur_rect_output = SurroundingRectangle(self.sind_texs[2])
        self.play(ReplacementTransform(sur_rect_input, sur_rect_output, path_arc = np.pi/3), run_time = 1)
        self.play(Write(self.sind_texs[2]))
        self.wait()

        self.play(
            GrowFromEdge(table_arrows[2], LEFT, run_time = 2),
            Write(multiplicators[2]), 
            Uncreate(sur_rect_output)
        )
        self.wait()


        # Adding all other arrows and multiplicators
        self.play(
            AnimationGroup(
                *[GrowFromEdge(graph_arrows[index], DOWN) for index in range(len(graph_arrows)) if index != 2], 
                *[GrowFromEdge(table_arrows[index], LEFT) for index in range(len(graph_arrows)) if index != 2],
                *[Write(multiplicators[index]) for index in range(len(graph_arrows)) if index != 2],
                *[FadeIn(self.sind_texs[index]) for index in range(len(graph_arrows)) if index != 2],
                lag_ratio = 0.1
            ),
            run_time = 8
        )
        self.wait()


        # Write equation
        self.play(
            AnimationGroup(
                *[Indicate(number, color = YELLOW, scale_factor = 1.5) for number in multiplicators], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )

        self.play(
            TransformFromCopy(self.sin_label[:2], self.sind_label[:2], path_arc = np.pi/3), 
            run_time = 2
        )
        self.play(FadeIn(self.sind_label[2:], shift = 2*LEFT), run_time = 2)
        self.play(Circumscribe(self.sind_label, color = BLUE, fade_out=True, run_time = 3))
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
        y_axis_nums = list(range(-3,4))
        y_axis_coords = VGroup(*[
            MathTex(tex, color = LIGHT_GREY, font_size = 24).next_to(self.axes.y_axis.n2p(num), LEFT)
            for tex, num in zip(
                [-3,-2,-1,0,1,2,3], 
                y_axis_nums
            )
        ])
        return y_axis_coords

    def get_graph_arrows(self):

        graph_arrows = VGroup(*[
            Line(start.get_center(), end.get_center(), buff = 0).set_color([RED, BLUE])
            for start, end in zip(self.dots_sin, self.dots_sind)
        ])
        for line in graph_arrows:
            line.add_tip(tip_length = 0.2)      # adding a tip
            line[1].set_color(BLUE)             # color the tip

        return graph_arrows

    def get_table_arrows(self):
        table_arrows = VGroup(*[
            Line(ORIGIN, RIGHT, buff = 0).set_color([BLUE, RED])
            for _ in range(len(self.sin_texs))
        ])

        for arrow, tex in zip(table_arrows, self.sin_texs):
            arrow.add_tip(tip_length = 0.2)
            arrow[1].set_color(BLUE)
            arrow.next_to(tex, RIGHT, buff = 0.5)

        table_arrows.shift(0.1*RIGHT)
        for arrow in table_arrows[1:]:
            arrow.align_to(table_arrows[0], LEFT)

        return table_arrows

    def get_multiplicators(self, number, font_size = 24):
        mults = VGroup()
        if number > 0:
            sign = "+"
        else:
            sign = "-"
        for arrow in self.table_arrows:
            mult = MathTex(sign, str(abs(number)), font_size = 24, color = YELLOW)
            mult.next_to(arrow, UP, buff = 0)
            mults.add(mult)

        return mults


class DifferentFunctions(Scene):
    def construct(self):
        self.axes_kwargs = {
            "x_length": 5, "y_length": 5 * 9/16, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 1}
        }
        self.part_buff = 0.75
        self.colors = [BLUE, RED, YELLOW, GREEN]
        self.d_val = ValueTracker(0)

        self.starting_mobs = VGroup()
        self.titles = VGroup()

        self.linear()
        self.quadratic()
        self.power()
        self.trig()
        self.play_animations()

    def linear(self):
        axes = NumberPlane(x_range = [-4, 4, 4], y_range = [-10, 20, 1], **self.axes_kwargs)
        axes.to_corner(UL, buff = self.part_buff)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)
        frame.move_to(axes)

        title = Tex("Lineare Funktionen")
        title.next_to(frame, UP, buff = 0.1)

        graph1 = axes.get_graph(lambda x: x, x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: x + self.d_val.get_value(), 
            x_range = [-4,4], 
            color = p2c(self.d_val.get_value(), -5, 10, self.colors)
        ))

        self.starting_mobs.add(axes, frame, graph2, graph1)
        self.titles.add(title)

    def quadratic(self):
        axes = NumberPlane(x_range = [-4, 4, 4], y_range = [-10, 20, 1], **self.axes_kwargs)
        axes.to_corner(UR, buff = self.part_buff)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)
        frame.move_to(axes)

        title = Tex("Quadratische Funktionen")
        title.next_to(frame, UP, buff = 0.1)

        graph1 = axes.get_graph(lambda x: 1/2 * x**2, x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: 1/2 * x**2 + self.d_val.get_value(), 
            x_range = [-4,4], 
            color = p2c(self.d_val.get_value(), -5, 10, self.colors)
        ))

        self.starting_mobs.add(axes, frame, graph2, graph1)
        self.titles.add(title)

    def power(self):
        axes = NumberPlane(x_range = [-4, 4, 4], y_range = [-10, 20, 1], **self.axes_kwargs)
        axes.to_corner(DL, buff = self.part_buff)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)
        frame.move_to(axes)

        title = Tex("Potenzfunktionen")
        title.next_to(frame, DOWN, buff = 0.1)

        graph1 = axes.get_graph(lambda x: 3*np.sqrt(x), x_range = [0, 4, 0.05], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: 3*np.sqrt(x) + self.d_val.get_value(), 
            x_range = [0, 4, 0.05],
            color = p2c(self.d_val.get_value(), -5, 10, self.colors)
        ))

        self.starting_mobs.add(axes, frame, graph2, graph1)
        self.titles.add(title)

    def trig(self):
        axes = NumberPlane(x_range = [-4, 4, 4], y_range = [-10, 20, 1], **self.axes_kwargs)
        axes.to_corner(DR, buff = self.part_buff)
        frame = ScreenRectangle(height = axes.height, color = GREY, stroke_width = 2)
        frame.move_to(axes)

        title = Tex("Trigonometr. Funktionen")
        title.next_to(frame, DOWN, buff = 0.1)

        graph1 = axes.get_graph(lambda x: 5*np.sin(1.75*x), x_range = [-4, 4], color = RED)
        graph2 = always_redraw(lambda: axes.get_graph(
            lambda x: 5*np.sin(1.75*x) + self.d_val.get_value(), 
            x_range = [-4,4], 
            color = p2c(self.d_val.get_value(), -5, 10, self.colors)
        ))

        self.starting_mobs.add(axes, frame, graph2, graph1)
        self.titles.add(title)

    def play_animations(self):
        self.play(Create(self.starting_mobs, lag_ratio = 0.1), run_time = 3)
        self.wait()

        self.play(
            AnimationGroup(*[Write(title) for title in self.titles], lag_ratio = 0.25),
            run_time = 3
        )
        self.wait()

        eq = MathTex("g(x)", "=", "f(x)", "+", "d", font_size = 90)
        eq[0].add_updater(lambda mob: mob.set_color(p2c(self.d_val.get_value(), -5, 10, self.colors)))
        eq[3].add_updater(lambda mob: mob.set_color(p2c(self.d_val.get_value(), -5, 10, self.colors)))
        eq[4].add_updater(lambda mob: mob.set_color(p2c(self.d_val.get_value(), -5, 10, self.colors)))
        eq[2].set_color(RED)
        eq.add_background_rectangle(buff = 0.2, stroke_width = 1, stroke_opacity = 0.5)

        self.play(
            FadeIn(eq[0]), 
            Write(eq[1:]),
        )
        self.wait()

        ds = [10, -5, 12, 5]
        for d in ds:
            self.play(self.d_val.animate.set_value(d), run_time = 3)
            self.wait()

        par_tex = Tex("Parameter ", "$d$")\
            .rotate(90*DEGREES)\
            .set_fill(opacity = 0)\
            .set_stroke(width = 0.75, opacity = 0.75, color = GREY)\
            .set(height = 4, color = GREY)\
            .move_to(np.array([-1.06481703, 0, 0]))

        d_copy = eq[-1].copy()
        self.play(Transform(d_copy, par_tex[-1]), run_time = 2)
        self.wait(2)


class ParameterInfluence(Scene):
    def construct(self):
        self.x_min = 0
        self.x_max = 2*PI

        self.axes_kwargs = {
            "x_range": [self.x_min - 0.25, self.x_max + 0.5, 1], "y_range": [-4.25, 4.25, PI/4], 
            "x_length": config["frame_width"] * 2/5, "y_length": 7,
            "background_line_style": {"stroke_color": GREY_D, "stroke_width": 1}
        }
        self.axes = NumberPlane(**self.axes_kwargs).to_edge(RIGHT, buff = 1.5)
        self.origin = self.axes.c2p(0,0)
        self.axes.x_axis.add_tip(tip_length = 0.25)
        self.axes.y_axis.add_tip(tip_length = 0.25)

        self.d_val = ValueTracker(0)
        self.colors = [PINK, BLUE, RED, YELLOW, GREEN]


        self.setup_scene()


    def setup_scene(self):
        axes, d_val = self.axes, self.d_val

        x_axis_ticks = self.get_x_axis_ticks([PI/2, PI, 3/2*PI, TAU])
        x_axis_numbers = self.get_x_axis_numbers(font_size = 30)
        y_axis_ticks = self.get_y_axis_ticks(-4, 4)
        y_axis_numbers = self.get_y_axis_numbers(-4, 3, font_size = 30)

        graph_ref = axes.get_graph(lambda x: np.sin(x), x_range = [self.x_min, self.x_max], color = RED, stroke_opacity = 0.5)
        graph = always_redraw(lambda: axes.get_graph(
                lambda x: np.sin(x) + d_val.get_value(), x_range = [self.x_min, self.x_max], 
                color = p2c(d_val.get_value(), -3, 3, self.colors)
            )
        )

        graph_tex = always_redraw(lambda: MathTex("\\sin", "(", "x", ")")\
            .add_background_rectangle()\
            .next_to(graph.point_from_proportion(1), RIGHT + UP)\
            .shift(LEFT)
        )
        d_graph_dec = always_redraw(lambda: DecimalNumber(d_val.get_value(), num_decimal_places=1, include_sign=True)\
            .next_to(graph_tex, RIGHT, buff = 0.1)\
            .set_color(p2c(d_val.get_value(), -3, 3, self.colors))
        )

        d_line = self.d_line = self.get_d_line(
            -4.25, 4.25, x_step = 0.5, line_length = self.axes_kwargs["y_length"],
            numbers_to_exclude = [-3.5 + k for k in range(8)]
        )
        d_dot = self.d_dot = always_redraw(lambda: self.get_d_dot())
        d_par_line = always_redraw(lambda: self.get_dot_to_axes_line())

        par_tex = Tex("Parameter ", "$d$")\
            .rotate(90*DEGREES)\
            .set_fill(opacity = 0)\
            .set_stroke(width = 0.75, opacity = 0.75)\
            .set(height = 4, color = GREY)\
            .move_to(midpoint(d_line.get_center(), axes.y_axis.get_center()))

        brace_up = Brace(Line(d_line.n2p(0), d_line.n2p(+4.25)), LEFT, buff = 0.75)
        brace_down = Brace(Line(d_line.n2p(0), d_line.n2p(-4.25)), LEFT, buff = 0.75)

        def update_d_pos(mob):
            mob.set_color(p2c(d_val.get_value(), -3, 3, self.colors))
            if d_val.get_value() <= 0:
                mob.set_color(DARK_GREY)
        def update_d_neg(mob):
            mob.set_color(p2c(d_val.get_value(), -3, 3, self.colors))
            if d_val.get_value() >= 0:
                mob.set_color(DARK_GREY)

        brace_up.add_updater(update_d_pos)
        brace_down.add_updater(update_d_neg)

        brace_text_up = Tex("Verschiebung\\\\", "nach oben")\
            .next_to(brace_up, LEFT)
        brace_text_down = Tex("Verschiebung\\\\", "nach unten")\
            .next_to(brace_down, LEFT)

        def update_tex_pos(mob):
            mob.set_color(WHITE)
            if d_val.get_value() <= 0:
                mob.set_color(DARK_GREY)
        def update_tex_neg(mob):
            mob.set_color(WHITE)
            if d_val.get_value() >= 0:
                mob.set_color(DARK_GREY)
            
        brace_text_up.add_updater(update_tex_pos)
        brace_text_down.add_updater(update_tex_neg)

        # ANIMATIONS
        self.add(par_tex[-1])
        self.wait(2)

        self.play(
            LaggedStartMap(Create, VGroup(axes, x_axis_ticks, x_axis_numbers, y_axis_ticks, y_axis_numbers), lag_ratio = 0.25),
            Create(par_tex[:-1]),
            FadeIn(d_line, shift = 3*RIGHT, lag_ratio = 0.1),
            run_time = 2
        )
        self.wait()

        self.play(
            LaggedStartMap(FadeIn, VGroup(d_par_line, d_dot), shift = 3*RIGHT, lag_ratio = 0.35),
            run_time = 3
        )
        self.play(Create(graph), run_time = 2.5)
        self.play(
            Create(graph_tex),
            FadeIn(d_graph_dec, shift = DOWN)
        )
        self.add(graph_ref)
        self.bring_to_front(graph)
        self.wait()

        # d bigger than 0
        self.play(d_val.animate.set_value(3), run_time = 4)
        self.play(
            Create(brace_up),
            Write(brace_text_up)
        )
        self.wait()

        self.play(d_val.animate.set_value(0.5), rate_func = double_smooth, run_time = 3)
        self.wait()

        # d smaller than 0
        self.play(d_val.animate.set_value(-3), run_time = 3)
        self.play(
            Create(brace_down),
            Write(brace_text_down)
        )
        self.wait()

        self.play(d_val.animate.set_value(+3), rate_func = linear, run_time = 9)
        self.play(d_val.animate.set_value(-3), rate_func = linear, run_time = 9)
        self.wait(3)


    # functions
    def get_x_axis_ticks(self, numbers, tick_length = 0.2):
        ticks = VGroup()
        for num in numbers:
            tick = Line(UP, DOWN)\
                .set_length(tick_length)\
                .move_to(self.axes.c2p(num, 0))
            ticks.add(tick)
        return ticks

    def get_x_axis_numbers(self, **kwargs):
        numbers = [PI/2, PI, 3*PI/2, TAU]
        strings = ["\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]

        axis_numbers = VGroup()
        for num, string in zip(numbers, strings):
            tex = MathTex(string, color = GREY, **kwargs)
            tex.next_to(self.axes.c2p(num, 0), DOWN)
            axis_numbers.add(tex)
        return axis_numbers

    def get_y_axis_ticks(self, start, end, tick_length = 0.2):
        ticks = VGroup()
        for y in range(start, end + 1):
            tick = Line(LEFT, RIGHT)\
                .set_length(tick_length)\
                .move_to(self.axes.c2p(0, y))
            ticks.add(tick)
        return ticks

    def get_y_axis_numbers(self, start, end, **kwargs):
        axis_numbers = VGroup()
        for y in range(start, end + 1):
            num = MathTex(str(y), color = GREY, **kwargs)
            num.next_to(self.axes.c2p(0, y), LEFT)
            axis_numbers.add(num)
        return axis_numbers

    def get_d_line(self, x_min, x_max, x_step, line_length, **kwargs):
        d_line = NumberLine(
            x_range = [x_min, x_max, x_step], length = line_length, rotation = PI/2, color = WHITE,
            include_numbers = True, label_direction = LEFT, decimal_number_config = {"num_decimal_places": 0, "color": GREY}, font_size = 30,
            **kwargs
        )
        d_line.shift(2*LEFT)
        return d_line

    def get_d_dot(self, **kwargs):
        d_line, d_val = self.d_line, self.d_val
        d_dot = Dot(
            point = d_line.n2p(d_val.get_value()), 
            color = p2c(d_val.get_value(), -3, 3, self.colors), 
            **kwargs
        )
        d_dot.set_sheen(-0.3, DR)
        d_dot.set_stroke(width = 1, color = WHITE)

        return d_dot

    def get_dot_to_axes_line(self):
        line = Line(
            self.d_dot.get_center(),
            self.axes.c2p(0, self.d_val.get_value()),
            color = p2c(self.d_val.get_value(), -3, 3, self.colors)
        )
        line.set_stroke(opacity = [0,1,0])
        return line





class Thumbnail(Scene):
    def construct(self):
        x_min, x_max = -3*PI, 3*PI
        axes = Axes(x_range = [x_min, x_max])

        sin_graph = axes.get_graph(lambda x: np.sin(x), x_range = [x_min, x_max], stroke_width = 8)\
            .set_color([RED, RED_E, RED])
        sind_graph = axes.get_graph(lambda x: np.sin(x) + 3, x_range = [x_min, x_max], stroke_width = 8)\
            .set_color([BLUE, BLUE_E, BLUE])

        dots_sin, dots_sind = VGroup(), VGroup()
        for x in np.linspace(0, 1, 21):
            dot_sin  = Dot(point = sin_graph.point_from_proportion(x),  color = sin_graph.get_color(),  radius = 0.1)
            dot_sind = Dot(point = sind_graph.point_from_proportion(x), color = sind_graph.get_color(), radius = 0.1)

            dot_sin.set_stroke(width = 1, color = BLACK).set_sheen(-0.3, DR)
            dot_sind.set_stroke(width = 1, color = BLACK).set_sheen(-0.3, DR)

            dots_sin.add(dot_sin)
            dots_sind.add(dot_sind)


        arrows = VGroup(*[
            Line(start.get_center(), end.get_center(), buff = 0.1).set_color([RED, BLUE])
            for start, end in zip(dots_sin, dots_sind)
        ])
        for line in arrows:
            line.add_tip(tip_length = 0.2)      # adding a tip
            line[1].set_color(BLUE)             # color the tip


        eq = MathTex("\\sin", "(", "x", ")", "+", "d", font_size = 160)\
            .to_edge(DOWN, buff = 1)
        eq[0].set_color(RED)
        eq[1:4].set_color(LIGHT_GREY)
        eq[4:].set_color(BLUE)


        self.add(sin_graph, sind_graph, dots_sin, dots_sind, arrows, eq)

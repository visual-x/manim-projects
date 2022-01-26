from manim import *
from BinomHelpers import *


class OpinionPoll(Scene):
    def construct(self):
        map = self.get_german_map()

        pins = VGroup(*[SVGMobject(SVG_DIR + "pin", height = 0.25) for _ in range(6)])
        pins.arrange(RIGHT)
        pins[0].move_to(3.4*LEFT + 2.5*UP)
        pins[1].move_to(4*LEFT + 1.85*UP)
        pins[2].move_to(3*LEFT + 1*UP)
        pins[3].move_to(5.5*LEFT + 0.25*UP)
        pins[4].move_to(3.75*LEFT + 1.25*DOWN)
        pins[5].move_to(5*LEFT + 2*DOWN)


        self.play(Write(map), run_time = 3)
        self.play(LaggedStartMap(FadeIn, pins, shift = DOWN, lag_ratio = 0.1), run_time = 2)
        self.wait()

        data0 = np.zeros(6)
        data = np.array([0.4, 0.28, 0.13, 0.09, 0.06, 0.04])
        histo0 = Histogram(data0, width = 5, height = 4, bar_colors = [PURPLE, MAROON, ORANGE], include_x_labels = False)
        histo = Histogram(data, width = 5, height = 4, bar_colors = [PURPLE, MAROON, ORANGE], include_x_labels = False)

        for h in histo0, histo:
            h.shift(2.5*RIGHT)

        title = Tex("Hate it or love it", font_size = 64)
        title.scale(1.25)
        title.next_to(histo, UP, aligned_edge=RIGHT)
        title.set_color_by_gradient(PURPLE, MAROON, ORANGE)

        self.play(
            FadeIn(histo.axes),
            ReplacementTransform(histo0.bars, histo.bars, lag_ratio = 0.1), 
            run_time = 3
        )
        self.play(Write(title))

        subject = Tex("Stochastik", color = YELLOW_E)
        subject.rotate(90*DEGREES)
        subject.set(width = histo.bars[0].width - 0.3)
        subject.next_to(histo.bars[0].get_bottom(), UP, buff = 0.2)

        self.play(FadeIn(subject, shift = 3*UP), run_time = 1)
        self.wait()


        # Bruchrechnung --> Baumdiagramm --> Pfadregeln

        histo_group = VGroup(title, histo, subject)
        tree = BinomTree(width = 5, height = 6, num_events = 3, cx_font_size = 16)
        tree.to_edge(LEFT)

        pfad = [1,5,12] # [[1,5,13], [1,5,12], [1,4,11], [1,4,10], [0,3,9], [0,3,8], [0,2,7], [0,2,6]]
        prob_all = tree.get_pfad_prob(texp = "0.75", texq = "0.25", use_prob_values=True)

        prob_pfad = VGroup(*[prob_all[x] for x in pfad])

        mult = MathTex("0.75", "\\cdot", "0.75", "\\cdot", "0.25")
        mult.move_to(tree)

        self.play(
            histo_group.animate.to_edge(RIGHT), 
            Unwrite(map),
            LaggedStartMap(ShrinkToCenter, pins, lag_ratio = 0.1),
            FadeIn(mult, shift = 5*RIGHT, rate_func = squish_rate_func(smooth, 0.5, 1)),
            run_time = 2.5
        )
        self.wait(0.5)
        self.play(
            ReplacementTransform(mult, prob_pfad),
            FadeIn(tree.cx_marks, lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait(0.5)


        pfad_list = [[1,5,13], [1,5,12], [1,4,11], [1,4,10], [0,3,9], [0,3,8], [0,2,7], [0,2,6]]
        pfade = VGroup(*[tree.get_pfad(numbers) for numbers in pfad_list])
        moving_dots = VGroup(*[Dot(point = tree.lines[0].get_start()).set_fill(opacity = 0) for _ in range(8)])
        traces = VGroup(*[
            TracedPath(dot.get_center, dissipating_time=0.75, stroke_opacity=[0, 1, 0], 
            stroke_color = YELLOW_D, stroke_width = 6)
            for dot in moving_dots
        ])
        self.add(traces)
        self.play(
            AnimationGroup(
                *[MoveAlongPath(dot, pfad, run_time = 2.5) for dot, pfad in zip(moving_dots, pfade)], 
                lag_ratio = 0.1
            ),
        )
        for trace in traces:
            trace.clear_updaters()
        self.bring_to_back(tree)
        self.play(FadeOut(traces))
        self.wait()

    # functions
    def get_german_map(self):
        map = SVGMobject(SVG_DIR + "germany_map", height = config["frame_height"] - 2)
        map.to_edge(LEFT)
        map.set_fill(BLUE, 0.75)
        map.set_stroke(width = 2, color = YELLOW)

        return map


class CodingScene(Scene):
    def construct(self):

        question = Tex("Wie programmiert \\\\man den Zufall?")
        question.scale(2)
        self.play(Write(question))
        self.wait()

        self.play(FadeOut(question, shift = 2*DOWN))


        code = '''
        self.play(
            AnimationGroup(*[
                MoveAlongPath(dot, pfad, run_time = 5) 
                for dot, pfad in zip(moving_dots, pfade)
            ], lag_ratio = 0.1), 
            run_time = 5
            )
        self.wait()
'''
        rendered_code = Code(code=code, tab_width=4, background="window", language="Python", font="Monospace")
        self.play(Write(rendered_code))
        self.wait(3)


        self.play(
            rendered_code.animate.scale(0.8).to_edge(UP, buff = 0.2), 
            run_time = 2
        )
        self.wait(3)


class CodingScene2(Scene):
    def construct(self):
        code = '''
        choices = get_die_faces()

        def shuffle_die(mob):
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            mob.become(new_mob)

        for k in range(len(dices)):
            self.play(UpdateFromFunc(first_die, shuffle_die))
            first_die.become(choices[dice_values[k] - 1])
            self.play(TransformFromCopy(first_die, dices[k]))
            counter += 1
            num.set_value(counter)
'''

        rendered_code = Code(code=code, tab_width=4, background="window", language="Python", font="Monospace")
        self.play(Write(rendered_code), run_time = 1.5)
        self.wait(3)


class RiseHistoFromGround(HistoScene):
    def construct(self):
        n = 10
        p = 0.7
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo_0 = self.get_histogram(n, p, zeros = True, **histo_kwargs)
        histo = self.get_histogram(n, p, zeros = False, **histo_kwargs)

        for mob in histo_0, histo:
            mob.center().to_edge(UP)

        title = Tex("Binomialverteilung")\
            .set_color_by_gradient(*histo_kwargs["bar_colors"])\
            .set_fill(color = WHITE, opacity = 0.3)\
            .set_stroke(width = 1.5)\
            .set(width = config["frame_width"] - 3)\
            .to_edge(DOWN)

        self.play(
            DrawBorderThenFill(title, rate_func = squish_rate_func(smooth, 0.6, 1)),
            FadeIn(histo.axes),
            ReplacementTransform(histo_0.bars, histo.bars, lag_ratio = 0.2),
            run_time = 5
        )
        self.wait()
        self.remove(histo_0)


        p_val = ValueTracker(0.7)
        histo.p_val = p_val
        histo.n = n
        self.play(
            p_val.animate.set_value(0.25),
            UpdateFromFunc(histo, self.update_histogram), 
            run_time = 4
        )
        self.wait()

    # functions
    def update_histogram(self, hist):
        new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
        new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)


class AskForAbo(Scene):
    def construct(self):
        title = Tex("Wie wäre es denn mit einem...", " Abo", "???")
        title.set(width = 12)
        title.to_edge(UL)

        wheel = self.wheel = self.get_wheel()
        wheel.scale(1.25)
        wheel.shift(4*RIGHT)

        self.play(
            AnimationGroup(
                Write(title[0]),
                DrawBorderThenFill(wheel), 
                lag_ratio = 0.4
            ),
            run_time = 3
        )
        self.wait()


        succ = wheel.succ[0].copy().scale(0.5)
        fail = wheel.fail[0].copy().scale(0.5)
        sf = VGroup(succ, fail)
        sf.arrange(DOWN, buff = 1)
        sf.move_to(5*LEFT)

        yes = Tex("Ja, warum nicht!").scale(1.25).next_to(succ, RIGHT)
        no = Tex("Ähm nope, Danke!").scale(1.25).next_to(fail, RIGHT)

        self.play(
            FadeIn(title[1:], shift = UP, scale = 0.1),
            LaggedStartMap(GrowFromCenter, sf, lag_ratio = 0.25), 
            LaggedStartMap(FadeIn, VGroup(yes, no), shift = 2*LEFT, lag_ratio = 0.25),
            run_time = 1.5
        )
        self.wait()

        self.rotate_arrow(deg_angle = -(7*360 - 110), run_time = 8)
        self.wait()

    # functions 
    def get_wheel(self):
        colors = [BLUE, ORANGE, BLUE, BLUE, BLUE]
        sectors = VGroup()
        for i in range(5):
            sector = Sector(
                outer_radius = 1.8, angle = 72*DEGREES, start_angle = i * 72*DEGREES - 36*DEGREES, 
                color = colors[i], fill_opacity = 0.75
            )
            sector.set_stroke(width = 1, color = WHITE)
            sectors.add(sector)

        dot = Dot(color = WHITE).set_stroke(width = 1, color = BLACK)
        arrow = Arrow(1.35*DOWN, 1.35*UP, stroke_width = 8, color = BLACK).move_to(dot)
        arrow.rotate(-10*DEGREES)
        arrow.set_stroke(width = 10)

        wheel = VGroup(sectors, arrow, dot)
        wheel.arrow = arrow
        wheel.succ = VGroup(sectors[0], sectors[2], sectors[3], sectors[4])
        wheel.fail = VGroup(sectors[1])

        return wheel

    def rotate_arrow(self, deg_angle, added_anims = None, **kwargs):
        wheel = self.wheel

        if added_anims is None:
            added_anims = []

        self.play(
            Rotate(
                wheel.arrow, 
                angle = deg_angle*DEGREES, 
                about_point = wheel.get_center(), 
                rate_func = slow_into,
                **kwargs
            ),
            *added_anims
        )


class Thumbnail(HistoScene):
    def construct(self):
        n = 10
        p = 0.7
        p_val = ValueTracker(p)
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo = self.get_histogram(n, p, zeros = False, **histo_kwargs)
        histo.center()
        histo.to_edge(DOWN)

        title = Tex("Binomialverteilung")
        title.set(width = histo.width)
        title.set_color_by_gradient(RED, GREEN, BLUE, YELLOW)
        title.to_corner(UL)

        trailer = Tex("Trailer")
        trailer.to_edge(UP).shift(0.65*RIGHT)

        # for x in [0,1,2,3,4,6]:
        #     histo.bars[x].set_fill(opacity = 0.2)

        p6 = MathTex("P", "(", "X", "=", "6", ")")
        p6[-2].set_color(C_COLOR)
        p6.rotate(90*DEGREES)
        p6.set(height = histo.bars[6].height - 0.25)
        p6.next_to(histo.bars[6].get_bottom(), UP, buff = 0.1)

        binom5 = get_binom_formula(10, 0.7, 6)[7:]
        binom5.next_to(histo.bars[6].get_corner(UL), UL)


        carrow = CurvedArrow(binom5.get_bottom() + 0.1*DOWN, histo.bars[6].get_left() + 0.5*UP, angle = TAU / 8, stroke_width = 3)


        self.add(histo, title, trailer)
        self.add(p6, binom5)
        self.add(carrow)












class CasNoCas(Scene):
    def construct(self):
        title = Tex("Wir schreiben den Test ... ")
        title.scale(2.5)
        title.shift(UP)

        origin = Tex("mit Cas", color = RED)
        origin.scale(2.5)

        def update_tex(mob):
            value = random.uniform(0,1)
            if value < 0.5:
                tex = Tex("mit CAS", font_size = 72, color = RED)
            else:
                tex = Tex("ohne CAS", font_size = 72, color = GREEN)
            tex.scale(2.5)
            mob.become(tex)

        self.play(
            Write(title), 
            FadeIn(origin, shift = 2*UP), 
        )
        self.wait() 

        self.play(
            UpdateFromFunc(origin, update_tex), 
            run_time = 5
        )
        self.wait()


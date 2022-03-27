from manim import *
from BinomHelpers import *


class UrnProblem(Scene):
    def construct(self):

        title = Tex("Ziehen aus einer Urne")
        title.to_corner(UL)
        uline = Line()
        uline.reverse_direction()
        uline.set(width = title.width + 0.25)
        uline.next_to(title, DOWN)
        subtitle = Tex("Mit Zurücklegen")
        subtitle.scale(0.75)
        subtitle.set_color(GREY)
        subtitle.next_to(title, DOWN, buff = 0.5, aligned_edge=LEFT)

        urn = self.urn = self.get_urn(total_balls = 5, stroke_color = WHITE)
        urn.to_edge(LEFT)

        sf = VGroup(*[
            Tex(m, color = m_color, tex_template = myTemplate).scale(1.15)
            for m, m_color in zip([CMARK_TEX, XMARK_TEX], [C_COLOR, X_COLOR])
        ])
        sf.arrange(RIGHT, buff = 3)
        sf.next_to(title, RIGHT, buff = 1)

        sf_arrows = VGroup(*[Arrow(ORIGIN, RIGHT, buff = 0) for _ in range(len(sf))])
        sf_balls = VGroup(*[urn.balls[k].copy() for k in [1,0]])
        for mark, arrow, ball in zip(sf, sf_arrows, sf_balls):
            arrow.next_to(mark, RIGHT)
            ball.next_to(arrow, RIGHT)



        lines = VGroup(*[Line(color = GREY).set_length(0.75) for _ in range(6)])
        lines.arrange(RIGHT, buff = 0.5)
        lines.next_to(urn.body, RIGHT, buff = 1.5)
        nums = VGroup()
        for x, line in enumerate(lines):
            num = MathTex(str(x + 1))
            num.scale(0.65)
            num.next_to(line, DOWN, buff = 0.1)
            nums.add(num)

        balls = urn.balls
        balls.save_state()

        balls.arrange(RIGHT, buff = 0.5)
        balls.shift(1.5*UP)

        self.play(
            Write(title), 
            Create(uline),
            FadeIn(subtitle, shift = 3*RIGHT),
            Create(urn.body),
            Create(balls, lag_ratio = 0.1),
            DrawBorderThenFill(sf, lag_ratio = 0.1),
            *[GrowArrow(arrow) for arrow in sf_arrows],
            *[GrowFromCenter(ball) for ball in sf_balls],
            FadeIn(lines, shift = DOWN, lag_ratio = 0.1),
            FadeIn(nums, lag_ratio = 0.1),
            run_time = 2
        )
        self.play(
            Restore(balls, path_arc = 60*DEGREES), 
            run_time = 3
        )
        self.play(FadeOut(balls))
        self.wait()

        marks = VGroup()
        for k in range(len(lines)):
            random_num = random.randrange(len(list(range(5))))

            if random_num == 1 or random_num == 3:
                mark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
            else:
                mark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
            mark.next_to(lines[k], DOWN, buff = 0.75)
            marks.add(mark)

            ball = urn.balls[random_num].copy()
            ball.move_to(urn.get_center())

            start = ball.get_center()
            target = lines[k].get_center() + 0.5*UP
            ball.move_to(target)
            self.play(
                GrowFromPoint(ball, start, path_arc = (-160 + 10*k)*DEGREES),
                GrowFromCenter(mark, rate_func = squish_rate_func(smooth, 0.4, 1)),
                run_time = 2
            )
        self.wait()

        brace = Brace(marks, DOWN, color = GREY)
        key_words_strings = ["genau", "mindestens", "mehr als", "höchstens"]
        key_words = VGroup(*[Tex(tex).set_color(PINK) for tex in key_words_strings])
        two_succs = Tex("2", " Erfolge")
        two_succs.scale(1.4)
        two_succs[0].set_color(C_COLOR)

        for word in key_words:
            word.scale(1.4)
            word.next_to(two_succs, LEFT, aligned_edge=UP)
        key_words[0].shift(0.15*DOWN)

        group = VGroup(key_words, two_succs)
        group.next_to(brace, DOWN)

        exclamation_mark = Tex("!")
        question_mark = Tex("?")

        for mark in exclamation_mark, question_mark:
            mark.scale(4)\
                .set_fill(color = GREY, opacity = 0.5)\
                .set_stroke(width = 1)\
                .set_color_by_gradient([RED, BLUE, GREEN, YELLOW])\
                .next_to(two_succs, RIGHT, buff = 0.5)

        self.play(
            Create(brace), 
            LaggedStart(
                FadeIn(key_words[0], shift = 3*RIGHT), 
                FadeIn(two_succs, shift = 3*LEFT), 
                lag_ratio = 0.3
            ), 
            run_time = 2
        )
        self.play(
            DrawBorderThenFill(exclamation_mark, run_time = 1.5),
            Circumscribe(VGroup(two_succs, key_words[0]), color = BLUE, run_time = 3)
        )
        self.wait()


        added_anim = [ReplacementTransform(exclamation_mark, question_mark)]
        old_key_word = key_words[0]
        for k in range(1, len(key_words)):
            self.play(
                Transform(old_key_word, key_words[k]), 
                *added_anim
            )
            added_anim = []
            self.wait()
        self.wait()


    # functions
    def get_urn(self, total_balls, **kwargs):
        ellipse = Ellipse(width = 1, height = 0.35)
        arc = ArcBetweenPoints(ellipse.get_left(), ellipse.get_right(), angle = 3*TAU/4)

        urn = VGroup(ellipse, arc)
        urn.set_style(**kwargs)
        urn.scale(2)
        urn.rotate(-30*DEGREES)

        balls = self.place_balls_in_urn(total_balls)
        balls.shift(0.6*DOWN)

        urn.add(balls)
        urn.balls = balls
        urn.body = urn

        return urn

    def place_balls_in_urn(self, total_balls, main_color = YELLOW, ball_radius = 0.25):
        balls = VGroup()
        for num in range(total_balls):
            ball = Circle(radius = ball_radius, stroke_width = 1, stroke_color = WHITE, fill_color = GREY, fill_opacity = 1)
            ball.set_sheen(0.6, UR)
            balls.add(ball)

        for ball in balls[1], balls[3]:
            ball.set_color(main_color)

        balls.arrange_in_grid(2,3)
        balls.flip(axis = RIGHT)

        return balls


class ExactVsAtMost(HistoScene):
    def construct(self):
        self.n, self.p = 6, 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] / 3, "height": config["frame_height"] * 3/5,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 1, "y_tick_num": 4,
            "bar_colors": [BLUE, GREEN, YELLOW]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(LEFT)

        histo_cdf = self.histo_cdf = self.get_histogram_cdf(self.n, self.p, **self.histo_kwargs)
        histo_cdf.to_edge(RIGHT)

        titles = self.titles = VGroup(*[Tex(tex).scale(1.25) for tex in ["Einzelwkt.", "Summierte Wkt."]])
        for title, hist in zip(titles, [histo, histo_cdf]):
            title.next_to(hist, UP, buff = 0.5)

        self.bernoulli_formula()
        self.ask_about_at_most()
        self.expand_bernoullis()


    def bernoulli_formula(self):
        histo, titles = self.histo, self.titles


        histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        histo_0.to_edge(LEFT)

        # left histo its title + bernoulli-formula
        self.play(
            ReplacementTransform(histo_0.bars, histo.bars, lag_ratio = 0.1, run_time = 3),
            LaggedStartMap(FadeIn, VGroup(histo.axes, titles[0]), lag_ratio = 0.2, run_time = 2),
        )

        arrow = CurvedArrow(histo.bars[2].get_top() + 0.2*UP, LEFT + 0.85*UP, angle = -60*DEGREES, color = histo.bars[2].get_color())
        binom2 = self.binom2 = get_binom_formula(self.n, self.p, 2)
        binom2.next_to(arrow.get_end(), RIGHT)
        binom2[3].set_color(PINK)

        brace = Brace(binom2[2:5], UP, color = GREY)
        brace_tex = brace.get_text("genau\\\\", "2", " Erfolge")
        brace_tex[0].set_color(PINK)
        brace_tex[1].set_color(C_COLOR)

        self.play(Create(arrow))
        self.play(
            Write(binom2), 
            Create(brace),
            Write(brace_tex)
        )
        self.wait()

        # explain formula
        arrow_l = Arrow(binom2[8].get_top(), binom2[8].get_top() + 2*RIGHT + UP, buff = 0.1).set_color(BLUE_E)
        length = Tex("Länge der \\\\", "Bernoulli-Kette").next_to(arrow_l.get_end(), UP)
        self.play(
            GrowArrow(arrow_l), 
            FadeIn(length, shift = 3*LEFT)
        )
        self.wait(0.5)

        arrow_p = Arrow(binom2[12].get_bottom() + 0.1*DOWN, 5*RIGHT + DOWN).set_color(BLUE_E)
        succ_prob = Tex("Erfolgswahr-\\\\scheinlichkeit").next_to(arrow_p.get_end(), DOWN)
        self.play(
            GrowArrow(arrow_p), 
            FadeIn(succ_prob, shift = 3*LEFT)
        )
        self.wait()

        # probability
        self.highlight_single_bar(histo, 2, run_time = 3)


        prob = round(scipy.stats.binom.pmf(2, self.n, self.p), 4)
        prob_tex = MathTex("\\approx", str(prob))
        prob_tex.next_to(binom2, DOWN, buff = 0.5)
        prob_tex.align_to(binom2[6:], LEFT)
        hline = DashedLine(start = histo.axes.c2p(0, prob), end = histo.axes.c2p(7, prob))
        self.play(
            FadeIn(hline, target_position=histo.axes.x_axis),
            LaggedStartMap(FadeOut, VGroup(arrow_l, length, arrow_p, succ_prob), lag_ratio = 0.1),
            run_time = 1.5
        )
        self.play(Write(prob_tex))
        self.wait()

        self.play(
            FadeOut(hline), 
            FadeOut(prob_tex, shift = 3*RIGHT)
        )
        self.wait()

    def ask_about_at_most(self):
        histo, binom2 = self.histo, self.binom2
        kum_binom = MathTex("P", "\\big(", "X", "\\leq", "2", "\\big)", "=")
        kum_binom.next_to(binom2, DOWN, buff = 1, aligned_edge=LEFT)
        kum_binom[3].set_color(PINK)
        kum_binom[4].set_color(C_COLOR)

        parts = VGroup(*[MathTex("P", "\\big(", "X", "=", str(num), "\\big)") for num in reversed(range(3))])
        parts.arrange(DOWN, buff = 0.35, aligned_edge = LEFT)
        parts.next_to(kum_binom, RIGHT, buff = 1, aligned_edge=UP)

        pluses = VGroup(*[MathTex("+").set_color(PINK) for _ in range(2)])
        for plus, part in zip(pluses, [parts[1][0], parts[2][0]]):
            plus.next_to(part, LEFT)


        brace = Brace(kum_binom[2:5], DOWN, color = GREY)
        brace_tex = brace.get_text("höchstens\\\\", "2", " Erfolge")
        brace_tex[0].set_color(PINK)
        brace_tex[1].set_color(C_COLOR)

        self.play(Write(brace_tex))
        self.wait()

        kum_binom_ask = MathTex("P", "\\big(", "X", "\\ ??\\ ", "2", "\\big)", "=")
        kum_binom_ask.next_to(kum_binom.get_left(), RIGHT, buff = 0)
        kum_binom_ask[3].set_color(PINK)
        kum_binom_ask[4].set_color(C_COLOR)
        brace_ask = Brace(kum_binom_ask[2:5], DOWN, color = GREY)

        self.play(
            Write(kum_binom_ask), 
            Create(brace_ask)
        )
        self.wait(3)

        # Switch Scene --> AtMostMeaning
        self.wait()
        self.play(
            ReplacementTransform(brace_ask, brace), 
            ReplacementTransform(kum_binom_ask, kum_binom)
        )
        self.play(Circumscribe(kum_binom[3], color = YELLOW_D, run_time = 3))
        self.wait()


        self.play(Write(parts[0]))
        self.play(ApplyWave(histo.bars[2], run_time = 1.5))

        for x in range(len(pluses)):
            self.highlight_group_of_bars(histo, 1-x, 2, run_time = 2)
            self.play(
                FadeIn(pluses[x]),
                Write(parts[x + 1])
            )
            self.wait(0.5)
        self.wait()

        self.kum_binom, self.parts, self.pluses = kum_binom, parts, pluses

    def expand_bernoullis(self):
        histo = self.histo
        stay = VGroup(histo, self.kum_binom, self.parts, self.pluses)
        self.add(stay)
        fadeout_group = Group(*[x for x in self.mobjects if x != stay])

        self.play(
            FadeOut(fadeout_group), 
            stay[1:].animate.shift(3*UP + 0.5*LEFT), 
            run_time = 3
        )
        self.wait()

        # Highlight 
        self.play(
            LaggedStart(
                *[ApplyWave(histo.bars[x]) for x in range(3)], 
                lag_ratio = 0.2
            ), 
            run_time = 2
        )
        parts_copy = self.parts.copy()
        for part, bar in zip(parts_copy, [histo.bars[2], histo.bars[1], histo.bars[0]]):
            part.generate_target()
            part.target.rotate(90*DEGREES).scale(0.75).next_to(bar.get_top(), UP).match_color(bar)
        self.play(
            LaggedStart(*[
                MoveToTarget(part, path_arc = 90*DEGREES) for part in parts_copy
            ], lag_ratio = 0.2), 
            run_time = 3
        )
        self.wait()


        # transform P(...) into Bernoullis
        binoms = VGroup(*[
            get_binom_formula(self.n, self.p, k) for k in reversed(range(3))
        ])
        binoms.arrange(DOWN)
        binoms.align_to(self.kum_binom, LEFT)
        binoms.shift(0.25*RIGHT + 0.5*UP)

        new_pluses = VGroup(*[MathTex("+").set_color(PINK) for _ in range(2)])
        for plus, binom in zip(new_pluses, binoms[1:]):
            plus.next_to(binom[7:], LEFT)

        # self.add(*[eq[7:] for eq in binoms])
        self.play(
            LaggedStart(
                *[Transform(eq1, eq2[7:]) for eq1, eq2 in zip(self.parts, binoms)], 
                lag_ratio = 0.1
            ),
            LaggedStart(
                *[Transform(plus, new_plus) for plus, new_plus in zip(self.pluses, new_pluses)], 
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait()

        for k, part in zip(reversed(range(3)), histo.bars[:3]):
            circums = [Circumscribe(binoms[k][7:], color = part.get_color(), time_width = 0.75, run_time = 2)]
            self.highlight_single_bar(histo, 2-k, added_anims = circums, run_time = 2)
            self.wait(0.5)

        self.highlight_group_of_bars(histo, 0, 2)
        self.wait()

        result_num = get_binom_cdf_result(self.n, self.p, 2)
        result = MathTex("\\approx", str(result_num))
        result.next_to(binoms, DOWN, buff = 0.5)
        result.align_to(self.kum_binom[6], LEFT)

        self.play(FadeIn(result, shift = 3*LEFT, scale = 4), run_time = 1.5)
        self.wait(3)


class BreathAnalyser(Scene):
    def construct(self):
        self.drive_under_alc()
        self.boundaries()
        self.ddad()
        self.at_most()


    def drive_under_alc(self):
        axes = Axes(x_range = [0, 6], y_range = [0,2.5])

        parabola = axes.get_graph(lambda x: 3/8*x + 1, x_range = [-1, 6])
        sin_para = axes.get_graph(lambda x: 3/8*x + 1 + 0.05 * np.exp(-1/10*(x-3)**2) *np.sin(5*x), x_range = [-1, 6])

        car = self.get_car(main_color = "#A6FF00")
        car.move_to(parabola.point_from_proportion(0))
        car2 = car.copy()
        car2.save_state()
        car.save_state()

        def update_car_par(mob, alpha):
            mob.restore()
            angle = self.get_pending(parabola, alpha)
            mob.move_to(parabola.point_from_proportion(alpha))
            mob.rotate(angle - TAU/4, about_point=mob.get_center())

        def update_car_sin(mob, alpha):
            mob.restore()
            angle = self.get_pending(sin_para, alpha)
            mob.move_to(sin_para.point_from_proportion(alpha))
            mob.rotate(angle - TAU/4, about_point=mob.get_center())

        self.play(
            UpdateFromAlphaFunc(car2, update_car_sin), 
            rate_func = linear, run_time = 5
        )
        self.wait()

    def boundaries(self):
        alk_val = self.alk_val = ValueTracker(0)
        analyser = self.get_breath_analyser()
        analyser.scale(1.25)
        analyser.to_corner(UR, buff = 0.75)

        bound_rect = self.bound_rect = Rectangle(height = 0.75, width = 8, color = WHITE, stroke_width = 1)
        drunk_rect = self.drunk_rect = self.get_drunk_rect()
        for rect in bound_rect, drunk_rect:
            rect.shift(LEFT + 2*DOWN)

        bound_line = self.bound_line = Line(bound_rect.get_corner(DL), bound_rect.get_corner(DR))
        permil = Tex("Alkoholgehalt\\\\", "im Blut in ", "$\\permil$")
        permil.next_to(bound_rect, RIGHT)
        ticks = VGroup()
        nums = VGroup()
        for x in np.linspace(0, 1, 9):
            tick = Line(UP, DOWN, stroke_width = 1)
            tick.set_length(0.2)
            tick.next_to(bound_line.point_from_proportion(x), DOWN, buff = 0)
            ticks.add(tick)

            num = MathTex(str(round(0.8 * x, 1)))
            num.scale(0.8)
            num.next_to(tick, DOWN)
            nums.add(num)

        def update_drunk(mob):
            rect = self.get_drunk_rect()
            rect.next_to(bound_rect.get_left(), RIGHT, buff = 0)
            mob.become(rect) 

        self.play(
            LaggedStartMap(Create, analyser, lag_ratio = 0.1),
            Create(bound_rect),
            LaggedStartMap(FadeIn, ticks, shift = 0.5*UP, lag_ratio = 0.1),
            LaggedStartMap(FadeIn, nums, shift = 0.5*RIGHT, lag_ratio = 0.1),
            Write(permil),
            run_time = 2
        )
        self.add(drunk_rect)
        self.wait()

        self.play(
            UpdateFromFunc(drunk_rect, self.update_drunk),
            alk_val.animate.set_value(0.7), 
            run_time = 5
        )
        self.wait()

        self.play(
            UpdateFromFunc(drunk_rect, self.update_drunk),
            alk_val.animate.set_value(0.49999),
            run_time = 3
        )
        self.wait()

    def ddad(self):
        t1 = Text("DON'T", font = "Bahnschrift")
        t2 = Text("DRINK", font = "Bahnschrift")
        t3 = Text("AND", font = "Bahnschrift")
        t4 = Text("DRIVE", font = "Bahnschrift")

        ddad = VGroup()
        for t in t1, t2, t3, t4:
            t.scale(1.75)
            ddad.add(t)

        ddad.arrange(DOWN, aligned_edge = LEFT)
        ddad.to_edge(UP, buff = 0.75)
        ddad.shift(2*LEFT)

        self.play(
            ShowIncreasingSubsets(ddad),
            UpdateFromFunc(self.drunk_rect, self.update_drunk),
            self.alk_val.animate.set_value(0.0), 
            run_time = 5
        )
        self.wait()

        self.play(
            LaggedStart(
                *[FadeOut(part, shift = direc) for part, direc in zip(ddad, 2*[4*LEFT, 4*RIGHT])], 
                lag_ratio = 0.1
            ),
            UpdateFromFunc(self.drunk_rect, self.update_drunk),
            self.alk_val.animate.set_value(0.5),
            run_time = 1.5
        )
        self.wait()

    def at_most(self):
        text1 = Tex("Fahren darf, wer...")
        text1.scale(1.75)
        text1.to_corner(UL)

        text2 = Tex("...", "höchstens ", "$0{,}5 \\permil$", " hat")
        text2.scale(1.75)
        text2.shift(LEFT + 0.5*UP)
        text2[1].set_color(PINK)

        self.play(Write(text1), run_time = 0.8)
        self.wait(0.5)

        self.play(Write(text2), run_time = 0.8)
        self.wait()

        vline = DashedLine(Line(LEFT, 3*RIGHT), color = PINK)
        vline.rotate(90*DEGREES)
        vline.next_to(self.bound_line.point_from_proportion(5/8), UP, buff = 0)
        self.play(TransformFromCopy(text2[1], vline))
        self.wait()

        upper_bound = Tex("Obergrenze")
        upper_bound.set_color_by_gradient(PINK, WHITE)
        upper_bound.next_to(vline, RIGHT, aligned_edge=UP)
        self.play(FadeIn(upper_bound, shift = 2*LEFT))
        self.wait()

        for value in [0.4, 0.1, 0.3, 0.2, 0.4999]:
            self.play(
                UpdateFromFunc(self.drunk_rect, self.update_drunk),
                self.alk_val.animate.set_value(value), 
                run_time = 2
            )
            if value == 0.2:
                lt = Tex("kleiner als")
                lt.next_to(text2[1], UP, buff = 0.5).shift(2*LEFT)
                self.play(GrowFromPoint(lt, text2[1]), run_time = 2)
            if value == 0.4999:
                oder = Tex("oder")
                oder.set_color(YELLOW_D)
                oder.next_to(lt, RIGHT, buff = 0.5, aligned_edge=DOWN)
                self.play(FadeIn(oder, shift = DOWN))
                self.wait(0.5)

                gt = Tex("gleich")
                gt.next_to(oder, RIGHT, buff = 0.5, aligned_edge=UP)
                self.play(GrowFromPoint(gt, text2[1]), run_time = 2)
                self.wait()
            self.wait()
        self.wait()


        width = self.bound_rect.width
        start = self.bound_rect.get_corner(UL)
        bound_line = Line(start, start + 5/8 * width * RIGHT)
        brace = Brace(bound_line, UP, color = GREY)

        lt = MathTex("\\leq", "0{,}5")
        lt.scale(1.5)
        lt.next_to(brace, UP)
        lt[0].set_color(PINK)

        self.play(
            FadeIn(lt[0], scale = 5), 
            Create(brace)
        )
        self.play(FadeIn(lt[1], shift = 2*LEFT))
        self.wait(3)




    # functions
    def get_car(self, main_color, height = 1.5):
        car = SVGMobject(SVG_DIR + "Car_Oben")
        car.set(height = height)
        car.set_color(DARK_GREY)
        car[2].set_color(main_color)
        car[9].set_color(YELLOW)
        car[10].set_color(YELLOW)
        car[11].set_color(RED)
        car[12].set_color(RED)

        car.center = car.get_center()

        # lights 
        front_left  = self.get_front_lights().next_to(car[9], UP, buff = -0.05)
        front_right = self.get_front_lights().next_to(car[10], UP, buff = -0.05)

        back_left  = self.get_back_lights().next_to(car[11], DOWN, buff = -0.03)
        back_right = self.get_back_lights().next_to(car[12], DOWN, buff = -0.03)

        car.add_to_back(front_left, front_right, back_left, back_right)

        return car

    def get_front_lights(self, inner_rad = 1, outer_rad = 2):
        light = AnnularSector(
            inner_radius=inner_rad, outer_radius=outer_rad,
            angle = 8*DEGREES, start_angle = 86*DEGREES, 
            fill_opacity = [0.3,0], color = YELLOW
        )
        return light

    def get_back_lights(self):
        light = AnnularSector(
            inner_radius=0.05, outer_radius=0.15,
            angle = -180*DEGREES, start_angle = 0, 
            fill_opacity = [0,0.3,0], color = RED
        )
        return light

    def get_pending(self, path, prop, dx=0.001):
        if prop < 1:
            coord_i = path.point_from_proportion(prop)
            coord_f = path.point_from_proportion(prop+dx)
        else:
            coord_i = path.point_from_proportion(prop-dx)
            coord_f = path.point_from_proportion(prop)
        line = Line(coord_i, coord_f)
        angle = line.get_angle()
        return angle

    def get_breath_analyser(self):
        big_rect = Rectangle(height = 3, width = 2, stroke_width = 3, color = LIGHT_GREY)
        small_rect = Rectangle(height = 0.6, width = 1.75, stroke_width = 3, color = LIGHT_GREY)
        small_rect.next_to(big_rect.get_top(), DOWN)

        dec = DecimalNumber(0, num_decimal_places=2, unit = "\\permil", edge_to_fix=RIGHT)
        dec.next_to(small_rect.get_right(), LEFT, buff = 0.1)
        dec.add_updater(lambda dec: dec.set_value(self.alk_val.get_value()))
        dec.add_updater(
            lambda dec: dec.set_color(
                self.alc_to_color(self.alk_val.get_value(), 0, 0.5, [WHITE, GREEN_A, GREEN])) 
                if self.alk_val.get_value() <= 0.5 
                else dec.set_color(RED)
        )

        name = Tex("Drunk-Meter")
        name.set(width = big_rect.width - 0.2)
        name.next_to(big_rect.get_bottom(), UP, buff = 1)

        analyser = VGroup(big_rect, small_rect, name, dec)
        return analyser

    def alc_to_color(self, alk_val, min, max, colors):
        alpha = inverse_interpolate(min, max, alk_val)
        index, sub_alpha = integer_interpolate(0, len(colors) - 1, alpha)

        return interpolate_color(colors[index], colors[index + 1], sub_alpha)

    def get_drunk_rect(self):
        rect = Rectangle(
            height = 0.75, width = self.alk_val.get_value()/0.7 * 7, 
            color = WHITE, stroke_width = 0
        )
        if self.alk_val.get_value() <= 0.5:
            rect.set_fill(self.alc_to_color(self.alk_val.get_value(), 0, 0.5, [WHITE, GREEN_A, GREEN]), opacity = 1)
        else:
            rect.set_fill(RED, opacity = 1)

        return rect

    def update_drunk(self, mob):
        rect = self.get_drunk_rect()
        rect.next_to(self.bound_rect.get_left(), RIGHT, buff = 0)
        mob.become(rect) 


class TransformPMFtoCDF(HistoScene):
    def construct(self):
        self.n, self.p = 6, 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] / 3, "height": config["frame_height"] * 0.55,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 1, "y_tick_num": 4,
            "bar_colors": [BLUE, GREEN, YELLOW]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(LEFT).shift(0.5*UP)

        histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        histo_0.to_edge(LEFT).shift(0.5*UP)

        histo_cdf = self.histo_cdf = self.get_histogram_cdf(self.n, self.p, **self.histo_kwargs)
        histo_cdf.to_edge(RIGHT).shift(0.5*UP)

        titles = self.titles = VGroup(*[Tex(tex) for tex in ["Einzelwahrscheinlichkeit", "Summierte Wkt."]])
        for title, hist in zip(titles, [histo, histo_cdf]):
            title.next_to(hist, UP)


        self.add(histo.axes, histo_cdf.axes, titles[0])
        self.play(
            ReplacementTransform(histo_0.bars, histo.bars),
            run_time = 3
        )
        self.wait()


        calcs = VGroup()
        for k in range(7):
            calc = self.get_calculation(k)
            calc.next_to(5.75*LEFT + 3*DOWN, RIGHT, buff = 0)
            calcs.add(calc)
        calc0 = MathTex("P", "\\big(", "X", "\\leq", "0", "\\big)", "=", "P", "\\big(", "X", "=", "0", "\\big)")
        calc1 = MathTex("P", "\\big(", "X", "\\leq", "1", "\\big)", "=", "P", "\\big(", "X", "=", "0", "\\big)", "+", "P", "\\big(", "X", "=", "1", "\\big)")
        calc2 = MathTex("P", "\\big(", "X", "\\leq", "2", "\\big)", "=", "P", "\\big(", "X", "=", "0", "\\big)", "+", "P", "\\big(", "X", "=", "1", "\\big)", "+", "P", "\\big(", "X", "=", "2", "\\big)")
        for calc in calc0, calc1, calc2:
            calc[3].set_color(PINK)
            calc[4].set_color(C_COLOR)
            calc[-2].set_color(C_COLOR)
            calc.next_to(5.75*LEFT + 3*DOWN, RIGHT, buff = 0)

        calcs[0] = calc0
        calcs[1] = calc1
        calcs[2] = calc2

        eq = calcs[0].copy()
        eq.set_stroke(color = BLACK)
        self.add(eq)

        for x in range(1, len(histo.bars) + 1):
            if x == 4:
                self.play(Indicate(histo.bars[3], color = RED), run_time = 2.5)
                self.wait(0.5)
            cum = VGroup(*[histo.bars[k].copy() for k in range(x)])
            cum.generate_target()
            cum.target.arrange_submobjects(UP, buff = 0).next_to(histo_cdf.axes.c2p(x - 0.5,0), UP, buff = 0)
            self.play(
                MoveToTarget(cum, path_arc = -120*DEGREES, lag_ratio = 0.15, rate_func = rate_functions.ease_in_out_sine, run_time = 3),
                Transform(eq, calcs[x - 1])
            )
            self.wait(0.5)
            if x == 4:
                self.play(Indicate(cum, color = RED, lag_ratio = 0.2), run_time = 3.5)
                self.wait()

        self.play(FadeIn(self.titles[1], shift = 3*LEFT, scale = 0.1))
        self.wait()

        cumulus = Tex("lat.: ", "cumulus", " - ", "Anhäufen")
        cumulus.move_to(2.85*LEFT + 2*UP)
        self.play(FadeIn(cumulus[2:], shift = LEFT))
        self.play(Write(cumulus[:2]))
        self.wait()

        new_title = Tex("kumulierte Wkt.")
        new_title.move_to(self.titles[1])
        self.play(Transform(self.titles[1], new_title))
        self.play(Circumscribe(self.titles[1], color = PINK, run_time = 3))
        self.wait(3)


    # functions
    def get_calculation(self, k):
        result = MathTex(
            "P", "\\big(", "X", "\\leq", str(k), "\\big)", "=",
            "P", "\\big(", "X", "=", 0, "\\big)", "+",
            "P", "\\big(", "X", "=", 1, "\\big)", "+", 
            "\\ldots", "+", 
            "P", "\\big(", "X", "=", str(k), "\\big)", 
        )
        result[3].set_color(PINK)
        result[4].set_color(C_COLOR)
        result[-2].set_color(C_COLOR)

        return result


class Definition(HistoScene):
    def construct(self):
        self.n = 25
        self.p = 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] * 0.8, "height": config["frame_height"] * 0.3,
            "x_tick_freq": 1, "x_label_freq": 2, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW]
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.center().to_edge(DOWN)

        par_values = self.par_values = VGroup(*[MathTex(*tex) for tex in [["n", "=", "25"], ["p", "=", "0.4"]]])
        par_values.arrange(DOWN, aligned_edge = LEFT)
        par_values.add_background_rectangle(buff = 0.2, stroke_width = 1, stroke_opacity = 1, stroke_color = WHITE)
        par_values.next_to(histo.get_corner(UR), DL, buff = 0.35)


        self.generalize()
        self.show_specific_examples()



    def generalize(self):
        histo, histo_0, par_values = self.histo, self.histo_0, self.par_values

        n, p, k = "n", "p", "k"
        summands = get_binom_cdf_summands(k)
        summands.to_edge(UP)

        sum_eq = get_binom_cdf_sum_notation(n, p, k)
        sum_eq.next_to(summands, DOWN)
        sum_eq.align_to(summands[6:], LEFT)


        self.play(
            FadeIn(histo.axes),
            ReplacementTransform(histo_0.bars, histo.bars),
            FadeIn(par_values[0]), 
            FadeIn(par_values[1], shift = 2*RIGHT), 
            FadeIn(par_values[2], shift = 2*LEFT), 
            Write(summands, rate_func = squish_rate_func(smooth, 0.4, 1)),
            run_time = 3
        )
        self.wait()

        self.play(Circumscribe(summands[7:], color = YELLOW_D, time_width = 0.75, run_time = 3))
        self.wait()


        # transform + into sum symbol
        self.play(
            LaggedStart(
                *[GrowFromPoint(summands[i].copy(), sum_eq[1], rate_func = lambda t: smooth(1-t)) for i in [13, 20, 22]], 
                lag_ratio = 0.2
            ),
            DrawBorderThenFill(sum_eq[1]),
            Write(sum_eq[0]),
            run_time = 3
        )
        self.wait()

        # lower bound
        self.play(
            GrowFromPoint(summands[11].copy(), sum_eq[-2], rate_func = lambda t: smooth(1-t)), 
            Write(sum_eq[-2]), 
            run_time = 3
        )
        # upper bound
        self.play(
            GrowFromPoint(summands[27].copy(), sum_eq[-1], rate_func = lambda t: smooth(1-t)), 
            Write(sum_eq[-1]), 
            run_time = 3
        )
        self.wait()

        # add P(X = i)
        probs_i = MathTex("P", "\\big(", "X", "=", "i", "\\big)")
        probs_i[-2].set_color(C_COLOR)
        probs_i.next_to(sum_eq[1], RIGHT)
        
        self.play(
            *[
                Circumscribe(summands[start:finish], color = YELLOW_D, run_time = 2) 
                for start, finish in zip([7, 14, 23], [13, 20, 29])
            ]
        )
        self.play(Write(probs_i))
        self.wait()

        self.play(
            LaggedStart(
                *[
                    Indicate(summands[start:finish], color = YELLOW_D, run_time = 2) 
                    for start, finish in zip([7, 14, 23], [13, 20, 29])
                ], 
                lag_ratio = 0.2
            ), 
            run_time = 2
        )

        brace = Brace(probs_i, DOWN, color = GREY)
        brace_tex = brace.get_text("Bernoulli", "$-$", "Formel")
        self.play(
            Create(brace), 
            FadeIn(brace_tex, shift = 3*LEFT)
        )
        self.wait()

        # Transform probs_i into bernoulli-term
        new_brace = Brace(sum_eq[2:-2], DOWN, color = GREY)
        new_brace_tex = new_brace.get_text("Bernoulli", "$-$", "Formel")
        self.play(
            ReplacementTransform(probs_i, sum_eq[2:-2]), 
            Transform(brace, new_brace), 
            Transform(brace_tex, new_brace_tex)
        )
        self.wait()

        self.play(
            *[FadeOut(mob) for mob in [brace, brace_tex]]
        )
        self.wait()


        # mathcal notation
        mathcal = get_binom_cdf_mathcal(n, p, k)
        mathcal.next_to(sum_eq, DOWN, buff = 0.35)
        mathcal.align_to(sum_eq, LEFT)

        # = F
        self.play(Write(mathcal[0]))
        self.play(FadeIn(mathcal[1], shift = 3*LEFT, scale = 0.1), run_time = 1.5)
        self.wait()

        # ( .... )
        self.play(
            FadeIn(mathcal[2]),
            FadeIn(mathcal[8]),
        )
        self.wait(0.5)

        self.play(FadeIn(mathcal[3:5], shift = UP, scale = 0.1))
        self.wait()
        self.play(FadeIn(mathcal[5:7], shift = UP, scale = 0.1))
        self.wait()
        self.play(FadeIn(mathcal[7], shift = UP, scale = 0.1))
        self.add(mathcal)
        self.wait()


        self.summands, self.sum_eq, self.mathcal = summands, sum_eq, mathcal

    def show_specific_examples(self):
        histo = self.histo
        summands, sum_eq, mathcal = self.summands, self.sum_eq, self.mathcal

        # self.play(
        #     FocusOn(summands[4]),
        #     FocusOn(summands[-2]),
        # )

        black_result = MathTex("\\approx", str(get_binom_cdf_result(25, 0.4, 12)))
        black_result.next_to(mathcal, RIGHT, buff = 0.5)
        black_result.set_color(BLACK)
        black_result.shift(2 * RIGHT)
        self.add(black_result)

        n = "25"
        p = "0.4"
        k_values = [12, 7,10]
        k_strings = [str(k) for k in k_values]

        for k_str, k_val in zip(k_strings, k_values):
            summand = get_binom_cdf_summands(k_str)
            summand.to_edge(UP)

            sum = get_binom_cdf_sum_notation(n, p, k_str)
            sum.next_to(summand, DOWN)
            sum.align_to(summand[6:], LEFT)

            mathc = get_binom_cdf_mathcal(n, p, k_str)
            mathc.next_to(sum, DOWN, buff = 0.35)
            mathc.align_to(sum, LEFT)

            result = MathTex("\\approx", str(get_binom_cdf_result(25, 0.4, k_val)))
            result.next_to(mathc, RIGHT, buff = 0.5)


            self.play(Transform(mathcal, mathc))
            self.wait(0.5)

            self.play(Transform(sum_eq, sum))
            self.wait(0.5)
            self.play(Transform(summands, summand))
            self.wait()
            self.highlight_group_of_bars(histo, 0, k_val, run_time = 3)
            self.wait()

            self.play(Transform(black_result, result))
            self.play(Circumscribe(result, color = BLUE, fade_out=True, run_time = 2))
            self.wait()

            if k_val == 12:
                self.play(
                    AnimationGroup(     # lift  bars[:13]  up and down
                        *[histo.bars[k].animate(rate_func = there_and_back).shift(0.5*UP) for k in range(13)], 
                        lag_ratio = 0.05
                    ),
                    run_time = 3
                )
                self.play(
                    LaggedStart(        # indicate  corresponding  texs P(X = i)
                        *[Indicate(summands[start:finish], color = YELLOW_D, run_time = 2) 
                            for start, finish in zip([7, 14, 23], [13, 20, 29])], 
                        lag_ratio = 0.2
                    ), 
                    run_time = 2
                )
                self.wait()

                self.play(
                    AnimationGroup(     # lift  bars[13:]  up and down
                        *[histo.bars[k].animate(rate_func = there_and_back).shift(0.5*UP) for k in range(13, 26)], 
                        lag_ratio = 0.05
                    ),
                    run_time = 3
                )
                self.wait()
        self.wait(3)


class TablesForCalculations(MovingCameraScene):
    def construct(self):
        n, p, k = "25", "0.4", "10"
        summands = get_binom_cdf_summands(k)
        summands.to_edge(UP)

        self.add(summands)
        self.wait(2)

        binoms = VGroup(*[get_binom_formula(25, 0.4, k) for k in range(11)])
        binoms.arrange(DOWN, buff = 0.35)
        binoms.next_to(summands[0], RIGHT, buff = 0, aligned_edge = UP)
        binoms.shift(DOWN)

        pluses = VGroup(*[MathTex("+").set_color(PINK) for _ in range(10)])
        for plus, binom in zip(pluses, binoms[1:]):
            plus.move_to(binom[6])

        succ_nums = VGroup()
        for k, binom in zip(range(11), binoms):
            desc = Tex(str(k), " Erfolge")
            desc[0].set_color(C_COLOR)
            desc.next_to(binom[0], RIGHT)
            desc.shift(9*RIGHT)

            succ_nums.add(desc)


        # Transform P(X = 0) into bernoulli and Write 1 Erfolge
        self.play(ReplacementTransform(summands[7:13].copy(), binoms[0][7:]))
        self.play(Write(succ_nums[0]))
        self.wait()

        # Transform + into + AND P(X = 1) into bernoulli
        self.play(ReplacementTransform(summands[13].copy(), pluses[0]))
        self.wait()
        self.play(ReplacementTransform(summands[14:20].copy(), binoms[1][7:]))
        self.play(Write(succ_nums[1]))
        self.wait()

        # Transform + into + 
        self.play(ReplacementTransform(summands[20].copy(), pluses[1]))
        self.wait()

        # Write bernoulli P(X = 2)
        self.play(
            Write(binoms[2][7:]), 
            FadeIn(succ_nums[2], shift = LEFT)
        )
        self.wait()


        # Show The Rest
        self.play(
            ShowIncreasingSubsets(VGroup(*[binom[7:] for binom in binoms[3:]])),
            ShowIncreasingSubsets(pluses[2:]),
            ShowIncreasingSubsets(succ_nums[3:]), 
            self.renderer.camera.frame.animate.shift(10.5*DOWN),
            run_time = 8
        )
        self.wait(3)

        self.play(
            self.renderer.camera.frame.animate.shift(10.5*UP),
            run_time = 3
        )
        self.wait()


class Thumbnail(HistoScene):
    def construct(self):
        self.n, self.p = 6, 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] / 2.5, "height": config["frame_height"] * 0.55,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 1, "y_tick_num": 4,
            "bar_colors": [RED, YELLOW], "include_h_lines": False # BLUE, GREEN, YELLOW
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.center().shift(3.75*LEFT + UP)

        histo_cdf = self.histo_cdf = self.get_histogram_cdf(self.n, self.p, **self.histo_kwargs)
        histo_cdf.center().shift(3*RIGHT + UP)

        self.add(histo.bars)

        # Stack bars on top of each other
        cums = VGroup()
        for x in range(1, len(histo.bars) + 1):
            cum = VGroup(*[histo.bars[k].copy() for k in range(x)])
            cum.generate_target()
            cum.target.arrange_submobjects(UP, buff = 0).next_to(histo_cdf.axes.c2p(x - 0.5,0), UP, buff = 0)
            self.play(MoveToTarget(cum))
            cums.add(cum)

        # highlight bars left and right
        histo.bars.set_fill(opacity = 0.15)
        histo.bars[3].set_fill(opacity = 0.6)
        for cum in cums:
            cum.set_fill(opacity = 0.15)
        cums[3].set_fill(opacity = 0.6)

        # title
        title = Tex("Kumulierte")
        title.set(width = config["frame_width"] - 5)
        title.to_edge(UL)
        title.set_color_by_gradient(BLUE, GREEN, YELLOW)# histo.bars[0].get_color(), histo.bars[3].get_color())
        title.set_stroke(color = WHITE, width = 1)

        subtitle = Tex("Wahrscheinlichkeit")
        subtitle.set(width = title.width - 3)
        subtitle.next_to(title, DOWN)

        self.add(title, subtitle)

        # equations & texts
        eq1 = get_binom_formula(self.n, self.p, 3)[:6]
        eq1[3].set_color(PINK)
        eq1.scale(2)
        eq1.next_to(histo.axes.x_labels[3], DOWN, buff = 0)

        text1 = Tex("genau")\
            .scale(1.35)\
            .set_color(GREY)\
            .next_to(eq1, DOWN)

        eq2 = get_binom_cdf_summands(3)[:6]
        eq2.scale(2)
        eq2.next_to(histo_cdf.axes.x_labels[3], DOWN, buff = 0)

        text2 = Tex("höchstens")\
            .scale(1.35)\
            .set_color(GREY)\
            .next_to(eq2, DOWN)

        self.add(eq1, eq2, text1, text2)


class TableTest(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.15,
            zoomed_display_height= 1.5,
            zoomed_display_width= 4.5,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                "default_frame_stroke_color": RED,
            },
            zoomed_camera_image_mobject_config={
                "stroke_width": 3,
                "stroke_color": BLUE_E,
                "buff": 0,
            },
            zoomed_camera_frame_starting_position = 0.08 * LEFT,
            **kwargs
        )

    def construct(self):
        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_50_2")
        table.set(height = config["frame_height"] - 0.5)
        table.shift(1.5*LEFT)

        npk_group = self.npk_group = self.get_npk_group(25, 0.4, 10)

        cum_eq = 3.375*UP
        cum_name = 3.375*UP + 3.5*LEFT

        self.play(
            FadeIn(table), 
            FadeIn(npk_group, shift = RIGHT, lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait()

        self.activate_zooming(animate=True)
        self.wait()

        zf = self.zf = self.zoomed_camera.frame
        zd = self.zoomed_display

        # Zoom on different positions
        positions = [2.04*LEFT + 2.53*UP, 2.42*LEFT + 0.5*DOWN, 0.84*LEFT + 1.25*UP]

        for pos in positions:
            self.play(zf.animate.move_to(pos), run_time = 2)
            self.wait()
        self.wait()

        # Zoom on eq with sum notation
        self.play(zf.animate.move_to(cum_eq).scale(2.5), run_time = 3)
        self.wait()

        n, p, k = "n", "p", "k"
        sum_eq = get_binom_cdf_sum_notation(n, p, k)
        sum_eq.next_to(zd, DOWN, buff = 1)
        sum_eq.shift(0.5*LEFT)
        self.play(Write(sum_eq[1:]))
        self.wait()

        # # Zoom on name 
        self.play(zf.animate.move_to(cum_name), run_time = 2)
        self.play(zf.animate(rate_func = double_smooth).shift(1.5 * RIGHT), run_time = 6)
        self.wait()






        self.find_block()
        self.find_result()


    def find_block(self):
        # Square n = 25
        square = Square(side_length = 0.25, color = BLUE)
        square.move_to(3.375*UP + 1.53*LEFT)
        self.play(Create(square), run_time = 3)
        self.wait()

        self.play(
            square.animate.move_to(3.82*LEFT + 1.74*DOWN), 
            self.zf.animate.move_to(3.82*LEFT + 1.74*DOWN).scale(1/2.5), 
            run_time = 3
        )
        self.play(Uncreate(square))
        self.wait()

        # search in this block
        rect_above, rect_below = self.highlight_block(pos_above = 0.44*DOWN + 1.5*LEFT, pos_below = 3.05*DOWN + 1.5*LEFT)
        self.play(
            LaggedStart(
                FadeIn(rect_above, shift = 4*RIGHT), 
                FadeIn(rect_below, shift = 4*LEFT), 
                lag_ratio = 0.2
            ),
            run_time = 3
        )

        brace = BraceBetweenPoints(rect_above.get_corner(DL), rect_below.get_corner(UL))
        n_value = self.npk_group[0]
        n_value.generate_target()
        n_value.target.next_to(brace, LEFT)
        self.play(
            Create(brace), 
            MoveToTarget(n_value), 
            run_time = 2
        )
        self.wait()

        self.play(FadeOut(rect_above), FadeOut(rect_below))
        self.wait()

    def find_result(self):
        rects_boundary = self.highlight_row_col(0.065*LEFT)

        self.play(Circumscribe(self.npk_group[1], color = YELLOW_D, time_width = 0.75, run_time = 2))

        # find probability
        p_rect = Rectangle(width = self.table.width - 1.2, height = 0.25, color = YELLOW_D)
        p_rect.next_to(self.table.get_top(), DOWN, buff = 0.58)
        self.play(
            Create(p_rect), 
            self.zf.animate.move_to(p_rect.get_left()),
            run_time = 3
        )
        self.wait()

        p_rect_final = Rectangle(width = 0.4, height = 0.25, color = YELLOW_D)
        p_rect_final.move_to(p_rect.get_y()*UP + 0.065*LEFT)
        self.play(
            Transform(p_rect, p_rect_final), 
            self.zf.animate.move_to(p_rect_final.get_center()),
            run_time = 3
        )
        self.wait()

        # add rect_boundary
        self.play(
            LaggedStartMap(GrowFromCenter, rects_boundary, lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()

        new_rects_boundary = self.highlight_row_col(2.42*LEFT + 0.5*DOWN)
        self.play(
            Transform(rects_boundary, new_rects_boundary),
            self.zf.animate.move_to(2.42*LEFT + 0.5*DOWN),
            run_time = 3
        )
        self.wait()


    # functions 
    def get_npk_group(self, n, p, k):
        group = VGroup(
            MathTex("n", "=", str(n)),
            MathTex("p", "=", str(p)),
            MathTex("k", "=", str(k))
        )
        group.arrange(DOWN, buff = 0.35)
        group.to_corner(UL)

        for k, col in zip([1,2], [YELLOW_D, C_COLOR]):
            group[k][0].set_color(col)

        return group

    def highlight_block(self, pos_above, pos_below):
        width = self.table.width
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]

        rect_kwargs = {"width": width, "stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}

        rect_above = Rectangle(height = top - pos_above[1], **rect_kwargs)
        rect_above.next_to(pos_above, UP, buff = 0)

        rect_below = Rectangle(height = bottom - pos_below[1], **rect_kwargs)
        rect_below.next_to(pos_below, DOWN, buff = 0)

        return rect_above, rect_below

    def highlight_row_col(self, pos):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]
        left = self.table.get_left()[0]
        right = self.table.get_right()[0]

        width, height = 0.4, 0.1

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}

        rect_ul = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ul.next_to(self.table.get_corner(UL), DR, buff = 0)

        rect_ur = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ur.next_to(self.table.get_corner(UR), DL, buff = 0)

        rect_dl = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dl.next_to(self.table.get_corner(DL), UR, buff = 0)

        rect_dr = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dr.next_to(self.table.get_corner(DR), UL, buff = 0)

        return VGroup(rect_ul, rect_ur, rect_dl, rect_dr)











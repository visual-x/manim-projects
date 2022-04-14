from manim import *
from BinomHelpers import *


class VirusSpreading(Scene):
    def construct(self):
        virus = self.get_virus()
        height = 3
        virus.set(height = height)

        self.play(DrawBorderThenFill(virus))

        viruses = VGroup(virus)

        for x in range(8):
            height *= 0.8
            anims = []
            new_viruses = VGroup()
            for virus in viruses:
                children = [virus.copy(), virus.copy()]
                for child in children:
                    child.set(height = height)
                    child.set_color(interpolate_color(RED_E, GREY_D, 0.7 * random.random()))
                    child.shift([
                        (random.random() - 0.5) * 3,
                        (random.random() - 0.5) * 3,
                        0,
                    ])
                    anims.append(TransformFromCopy(virus, child))
                    new_viruses.add(child)
            new_viruses.center()
            self.remove(*viruses)
            self.play(*anims, run_time=0.5)
            viruses.set(submobjects = list(new_viruses))
        self.wait()

        # Eliminate
        for virus in viruses:
            virus.generate_target()
            virus.target.scale(3)
            virus.target.set_color(WHITE)
            virus.target.set_opacity(0)

        self.play(LaggedStartMap(
            MoveToTarget, viruses,
            run_time = 8,
            lag_ratio = 3 / len(viruses)
        ))


    # functions 
    def get_virus(self, height = 2):
        ball = Circle(radius = 1)
        ball.set_stroke(width = 5, color = RED)

        symbol = Star(color = RED, start_angle = -36*DEGREES)

        ball_center = ball.get_center()
        angles = np.linspace(0, TAU, 8, endpoint=False)
        for x, angle in enumerate(angles):
            tick = Line(color = GREY)
            tick.set_length(0.3)
            tick.next_to(ball.get_start(), RIGHT, buff = 0)

            symbol_copy = symbol.copy()

            symbol_copy.set(height = 0.3)
            symbol_copy.next_to(tick, RIGHT, buff = 0)

            tick.set_color(RED)
            tick.rotate(angle, about_point = ball_center)
            symbol_copy.rotate(angle, about_point = ball_center)

            ball.add(tick, symbol_copy)

        ball.set(height = height)
        ball.ball = ball

        return ball


class Intro(Scene):
    def construct(self):
        rabbit = self.get_rabbit(ill = True)
        rabbit.move_to(4*LEFT)

        medicin = self.get_medicin()
        medicin.scale(0.5)
        medicin.to_edge(DOWN)

        self.play(
            FadeIn(rabbit, shift = 4*RIGHT),
            FadeIn(medicin, shift = 2*DOWN),
            rate_func = linear, run_time = 2
        )
        rabbit_ill = rabbit.copy()
        self.add(rabbit_ill)

        rab_med = medicin.copy()
        rab_med.generate_target()
        rab_med.target.scale(0.2).fade(darkness = 1).move_to(rabbit.virus.get_center() + 4*RIGHT)

        self.play(
            MoveToTarget(rab_med, path_arc = -150*DEGREES),
            rabbit.animate(rate_func = linear).shift(4*RIGHT), 
            run_time = 2
        )


        virus = rabbit.virus
        virus.generate_target()
        virus.target.shift(4*RIGHT).scale(3).set_color(GREY).set_opacity(0)
        self.play(
            rabbit.animate(rate_func = linear).shift(4*RIGHT), 
            MoveToTarget(virus, rate_func = linear), 
            run_time = 2
        )
        rabbit_healthy = rabbit.copy()
        self.add(rabbit_healthy)
        self.play(
            FadeOut(rabbit, shift = 4*RIGHT), rate_func = linear, run_time = 2
        )


        arrow = Arrow(1.5*LEFT, 1.5*RIGHT, color = BLUE_E, buff = 0)
        text1 = Tex("Heilung bei").next_to(arrow, UP, buff = 0.1)
        text2 = Tex("mindestens $70\\%$").next_to(arrow, DOWN, buff = 0.1)
        self.play(
            GrowArrow(arrow), 
            AnimationGroup(
                FadeIn(text1, shift = DOWN), 
                FadeIn(text2, shift = UP),
                lag_ratio = 0.2
            ),
            run_time = 2
        )
        self.play(Circumscribe(VGroup(text1, text2, arrow), color = C_COLOR, time_width = 0.75, run_time = 2))
        self.wait()

        true_or_false = Tex("Aber stimmt das auch?")\
            .next_to(text1, UP, buff = 1)
        self.play(FadeIn(true_or_false, lag_ratio = 0.1), run_time = 2)
        self.wait()


        # 20 ill rabbits
        scale_group = VGroup(rabbit_ill, text1, arrow, text2, rabbit_healthy)
        scale_group.generate_target()
        scale_group.target.scale(0.35).to_edge(UP)

        rabbits_ill = VGroup(*[self.get_rabbit(ill = True).scale(0.35) for x in range(20)])
        rabbits_ill.arrange_in_grid(2,10)
        rabbits_ill.center()

        self.play(
            MoveToTarget(scale_group),
            LaggedStartMap(FadeIn, rabbits_ill, lag_ratio = 0.1),
            FadeOut(true_or_false, shift = 4*UP),
            run_time = 2
        )
        total = Integer(20)\
            .scale(2.5)\
            .set_color(RED)\
            .next_to(scale_group, LEFT, buff = 2)

        self.play(FadeIn(total, shift = 2*RIGHT))
        self.wait()

        # feed rabbits with medicin
        medicins = VGroup(*[self.get_medicin().scale(0.5).to_edge(DOWN) for x in range(20)])
        for med, rab in zip(medicins, rabbits_ill):
            med.generate_target()
            med.target.scale(0.2).fade(darkness = 1).move_to(rab.get_center())

        self.play(LaggedStartMap(MoveToTarget, medicins, lag_ratio = 0.1), run_time = 3)

        # 12 rabbits are healthy after taking medicin
        sick_list = 8*[True] + 12*[False]
        random.shuffle(sick_list)
        rabbits_after = VGroup(*[self.get_rabbit(ill = tof).scale(0.35) for x, tof in zip(range(20), sick_list)])
        rabbits_after.arrange_in_grid(2,10)
        rabbits_after.center()

        for before, after in zip(rabbits_ill, rabbits_after):
            before.generate_target()
            before.target.become(after)


        health_val = ValueTracker(20)
        health_dec = Integer(health_val.get_value())\
            .scale(2.5)\
            .set_color(BLUE_E)\
            .next_to(scale_group, RIGHT, buff = 2)\
            .add_updater(lambda dec: dec.set_value(health_val.get_value()))

        self.add(health_dec)
        self.play(
            LaggedStartMap(MoveToTarget, rabbits_ill, lag_ratio = 0.1),
            health_val.animate.set_value(12), 
            run_time = 5
        )
        self.wait()


        # does 12 out 20 mean that its true?
        out_of = Tex(" von ").scale(2.5).shift(0.5*DOWN)
        self.play(
            FadeOut(medicin, shift = 2*DOWN),
            rabbits_ill.animate.scale(0.65).to_edge(DOWN), 
            health_dec.animate.next_to(out_of, LEFT, buff = 0.5, aligned_edge = DOWN), 
            total.animate.next_to(out_of, RIGHT, buff = 0.5, aligned_edge = DOWN),
            Write(out_of),
            run_time = 3
        )
        self.wait()

        self.play(
            FadeOut(rabbits_ill, shift = DOWN),
            VGroup(health_dec, out_of, total).animate.shift(2*DOWN),
            scale_group.animate.scale(2.5).shift(DOWN),
            run_time = 3
        )
        self.wait(3)


    # functions
    def get_rabbit(self, ill):
        rabbit = SVGMobject(SVG_DIR + "Rabbit")
        rabbit.scale(2)
        rabbit.set_fill(color = "#dea85f")
        rabbit.set_stroke(width = 2, color = WHITE)

        if ill is True:
            virus = Star(color = RED, fill_color = RED, fill_opacity = 1)
            virus.set_fill(RED, 1)
            virus.set_stroke(width = 1, color = WHITE)
            virus.set(height = 1)
            virus.move_to(rabbit)
            virus.shift(0.75*DOWN)
            rabbit.add(virus)
            rabbit.virus = virus

        return rabbit

    def get_medicin(self):
        arc_l = Arc(start_angle = 90*DEGREES, angle = TAU/2)
        rect_l = Rectangle(height = arc_l.height, width = 1.5)
        rect_r = Rectangle(height = arc_l.height, width = 1.5)
        arc_r = Arc(start_angle = -90*DEGREES, angle = TAU/2)

        result = VGroup(arc_l, rect_l, rect_r, arc_r)
        result.arrange(RIGHT, buff = 0)
        for mob in result:
            mob.set_stroke(color = BLUE_E, width = 1)
            mob.set_fill(color = BLUE_E, opacity = 1)

        name = Tex("Heilmittel")
        name.scale(2)
        result.add(name)


        return result


class ReasonsWhyItsFalse(Intro):
    def construct(self):
        rabbits_ill = self.rabbits_ill = VGroup(*[self.get_rabbit(ill = True) for _ in range(161)])
        rabbits_ill.arrange_in_grid(10, 23)
        rabbits_ill.set(width = config["frame_width"] - 0.5)
        rabbits_ill.to_edge(UP)



        self.different_samples()
        self.more_than_70_percent()


    def different_samples(self):
        rabbits_ill = self.rabbits_ill

        self.play(
            LaggedStartMap(DrawBorderThenFill, rabbits_ill, lag_ratio = 0.01), 
            run_time = 3
        )

        sample_text = Tex("Stichprobe")\
            .to_edge(DOWN)\
            .shift(1*UP + 3*LEFT)
        sample_val = ValueTracker(0)
        sample_int = self.sample_int = Integer(sample_val.get_value(), edge_to_fix = RIGHT)\
            .scale(2)\
            .set_color(RED)\
            .next_to(sample_text, DOWN)\
            .add_updater(lambda int: int.set_value(sample_val.get_value()))

        succ_text = Tex("geheilt")\
            .to_edge(DOWN)\
            .shift(1*UP + 3*RIGHT)
        succ_val = ValueTracker(0)
        succ_int = self.succ_int = Integer(succ_val.get_value(), edge_to_fix = RIGHT)\
            .scale(2)\
            .set_color(BLUE_E)\
            .next_to(succ_text, DOWN)\
            .add_updater(lambda int: int.set_value(succ_val.get_value()))


        bottom_group = VGroup(sample_text, sample_int, succ_text, succ_int)

        self.add(sample_int)
        self.play(
            LaggedStart(
                rabbits_ill[:26].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
                rabbits_ill[36:49].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
                rabbits_ill[59:].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
                lag_ratio = 0.05
            ),
            Write(sample_text, rate_func = squish_rate_func(smooth, 0, 0.4)),
            sample_val.animate.set_value(20),
            run_time = 3
        )
        self.wait()

        medicin = self.get_medicin()
        medicin.scale(0.3)
        medicin.move_to(bottom_group)
        self.play(FadeIn(medicin, shift = 2*RIGHT))
        self.play(FadeOut(medicin, shift = 2*RIGHT))

        self.add(succ_int)
        self.play(
            Write(succ_text),
            succ_val.animate.set_value(12)
        )
        self.wait()


        # highlight 12 different rabbits
        hl = [3, 17, 19, 24, 37, 56, 66, 74, 75, 80, 92, 106, 114, 119, 124, 131, 140, 142, 145, 159]
        self.play(
            rabbits_ill[26:36].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
            rabbits_ill[49:59].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
            LaggedStart(*[rabbits_ill[x].animate.set_fill(opacity = 1).set_stroke(opacity = 1) for x in hl], lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()


        highlights = [
            hl,
            [9, 11, 21, 35, 42, 48, 52, 70, 81, 85, 93, 101, 109, 113, 118, 125, 134, 143, 147, 154],
            [4,  7, 15, 25, 36, 44, 50, 64, 82, 89, 97, 102, 105, 110, 115, 120, 132, 139, 144, 158],
            [0,  5, 22, 31, 32, 40, 48, 52, 69, 75, 88,  93, 101, 108, 119, 123, 129, 136, 148, 149],
        ]
        values = [9, 18, 12]
        for index, k in enumerate(values):
            self.play(
                succ_val.animate.set_value(k),
                LaggedStart(*[rabbits_ill[x].animate.set_fill(opacity = 1).set_stroke(opacity = 1) for x in highlights[index + 1]], lag_ratio = 0.1),
                LaggedStart(*[rabbits_ill[x].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3) for x in highlights[index]], lag_ratio = 0.1),
                run_time = 2.5
            )
            self.wait(0.5)
        self.wait()

    def more_than_70_percent(self):
        text = Tex("Heilung bei\\\\", "mindestens ", "$70\\%$")
        text[1:].set_color(BLUE)
        text.move_to(self.rabbits_ill)

        self.play(
            FadeOut(self.rabbits_ill[:81], shift = 5*LEFT),
            FadeOut(self.rabbits_ill[81:], shift = 5*RIGHT),
            GrowFromCenter(text),
            run_time = 2
        )
        self.play(Circumscribe(text[1:], color = YELLOW_D, run_time = 2))
        self.play(text.animate.to_edge(UP), run_time = 2)
        self.wait()

        calc1 = MathTex("20", "\\cdot", "70\\%").scale(2)
        calc2 = MathTex("20", "\\cdot", "0.7").scale(2)
        calc2.move_to(calc1, aligned_edge=LEFT)


        self.play(
            AnimationGroup(
                TransformFromCopy(self.sample_int, calc1[0]),
                Write(calc1[1]),
                TransformFromCopy(text[-1], calc1[-1]),
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait(0.5)

        result = MathTex("=", "14").scale(2)
        result.next_to(calc1)
        self.play(Transform(calc1, calc2), run_time = 0.8)
        self.play(Write(result))
        self.wait()

        more_than_14 = VGroup()
        scale_vals = [0.8 - t*0.15 for t in [1,2,3,4]]
        colors = [GREY_A, GREY_B, GREY_C, GREY_D, GREY_E]
        for x, scl, col in zip(range(15, 20), scale_vals, colors):
            num = MathTex(str(x))
            num.scale(2)
            num.scale(scl)
            num.set_color(col)
            more_than_14.add(num)
        more_than_14.arrange(RIGHT, aligned_edge = DOWN)
        more_than_14.next_to(result, RIGHT, aligned_edge=DOWN)
        self.play(ShowIncreasingSubsets(more_than_14), run_time = 3)
        self.wait()

        self.play(LaggedStartMap(FadeOut, more_than_14, shift = RIGHT, lag_ratio = 0.1), run_time = 2)
        self.wait(0.5)

        arrow = CurvedArrow(self.succ_int.get_right() + 0.1*RIGHT, result.get_corner(DR) + 0.1*DR, color = YELLOW_D)
        self.play(Create(arrow), run_time = 2)
        self.wait()


        sur_rect = SurroundingRectangle(text, color = RED)
        cross = Cross(text)
        self.play(Create(sur_rect), run_time = 2.5)
        self.wait()
        self.play(Transform(sur_rect, cross))
        self.wait(3)


class Spoiler(Scene):
    def construct(self):
        spoiler = Tex("Spoiler")\
            .set_color(YELLOW_D)\
            .to_corner(UL)
        uline = Underline(spoiler, color = YELLOW_D)

        self.play(
            LaggedStart(
                FadeIn(spoiler, shift = DOWN, scale = 4), 
                Create(uline), 
                lag_ratio = 0.1
            ),
            run_time = 0.75
        )
        uline.reverse_direction()

        words = ["Nope.", "Die", "Argumentation", "ist", "falsch."]
        texs = VGroup(*[Tex(word) for word in words])
        texs.arrange(DOWN, aligned_edge = LEFT)
        texs.next_to(spoiler, DOWN, aligned_edge=LEFT)
        texs.shift(0.5*RIGHT)

        self.play(
            Uncreate(uline),
            ShowIncreasingSubsets(texs, rate_func = linear, run_time = 1.75)
        )
        self.wait()

        self.play(
            FadeOut(spoiler, shift = UP, scale = 4),
            LaggedStartMap(FadeOut, texs, shift = 2*LEFT)
        )


class ConnectToBernoulli(Intro, HistoScene):
    def construct(self):

        self.bernoulli()
        self.expected_value()
        self.histo()

    def bernoulli(self):
        rabbit0 = self.get_rabbit(ill = True)
        rabbit_ill = rabbit0.copy()
        rabbit_healthy = self.get_rabbit(ill = False)

        for r in rabbit0, rabbit_ill, rabbit_healthy:
            r.set(height = 1.5)
        rabbit0.to_edge(UP)

        medicin = self.get_medicin()
        medicin.scale(0.3)
        medicin.next_to(rabbit0, RIGHT, buff = 1.5)

        succ_fail = VGroup(rabbit_healthy, rabbit_ill)
        succ_fail.arrange(RIGHT, buff = 3)
        succ_fail.next_to(rabbit0, DOWN, buff = 2)

        arrows = VGroup(*[
            Arrow(rabbit0.get_corner(corner), rabbit.get_top(), color = GREY)
            for corner, rabbit in zip([DL, DR], succ_fail)
        ])

        succ_fail_symbols = VGroup(*[
            Tex(tex, tex_template = myTemplate, color = t_color).scale(2).next_to(r, DOWN)
            for tex, t_color, r in zip([CMARK_TEX, XMARK_TEX], [C_COLOR, X_COLOR], succ_fail)
        ])

        self.add(rabbit0, medicin)
        self.wait()

        # Bernoulli - Experiment
        bexp = Tex("Bernoulli", "-", "Experiment").to_corner(UL)
        self.play(
            FadeOut(medicin, scale = 0.2, target_position = rabbit0.virus),
            Write(bexp),
            run_time = 2
        )
        self.play(
            GrowArrow(arrows[0]), 
            GrowFromPoint(succ_fail[0], rabbit0.get_corner(DL)),
        )
        self.play(
            GrowArrow(arrows[1]), 
            GrowFromPoint(succ_fail[1], rabbit0.get_corner(DR)),
        )
        self.wait(0.5)

        self.play(LaggedStartMap(FadeIn, succ_fail_symbols, shift = UP, lag_ratio = 0.2))
        self.wait()


        # # feed rabbits with medicin
        cac_bools = [True] + [False] + 2*[False] + 2*[True] + [False] + [True] + 3*[False] + [True] + 3*[False] + [True] + [False] + 2*[True] + [False]
        cac_group = get_checks_and_crosses(cac_bools)

        neg_bools = [not elem for elem in cac_bools]
        rabbits_group = VGroup(*[self.get_rabbit(ill = bools).scale(0.35) for bools in neg_bools])
        rabbits_group.arrange_in_grid(2,10)
        rabbits_group[10:].shift(DOWN)
        rabbits_group.center()

        for cac, rabbit in zip(cac_group, rabbits_group):
            cac.next_to(rabbit, DOWN)

        self.play(
            ReplacementTransform(succ_fail[0], rabbits_group[0]),
            ReplacementTransform(succ_fail[1], rabbits_group[1]),
            ReplacementTransform(succ_fail_symbols[0], cac_group[0]),
            ReplacementTransform(succ_fail_symbols[1], cac_group[1]),
            FadeOut(rabbit0, shift = 3*UP),
            FadeOut(arrows, shift = 3*UP),
            run_time = 2
        )
        btrail = Tex("Bernoulli", "-", "Kette").to_corner(UL)
        self.play(
            LaggedStart(
                ShowIncreasingSubsets(rabbits_group[2:]), 
                ShowIncreasingSubsets(cac_group[2:]),
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(ReplacementTransform(bexp, btrail))
        self.wait()


        zv = MathTex("X", "-", "\\#").scale(1.5).to_edge(UP).shift(0.75*LEFT)
        zv[2].set_color(C_COLOR)
        zv_r = self.get_rabbit(ill = False)
        zv_r.match_height(zv)
        zv_r.next_to(zv, RIGHT, buff = 0)
        zv.add(zv_r)

        self.play(Write(zv[:2]))
        self.wait(0.5)
        self.play(FadeIn(zv[2:], shift = 2*LEFT))
        self.wait()

        zvinfo = self.zvinfo = MathTex("X", "\\sim", "\\mathcal{B}", "(", "20", ",", "0.7", ")")
        zvinfo.scale(1.5)
        zvinfo.to_corner(UR)

        self.play(FadeIn(zvinfo[:3], lag_ratio = 0.1), run_time = 2)
        self.wait(0.5)
        self.play(
            GrowFromCenter(zvinfo[3]),
            GrowFromCenter(zvinfo[-1]),
        )
        self.play(
            LaggedStartMap(FadeIn, zvinfo[4:-1], shift = UP, lag_ratio = 0.25), 
            run_time = 2.5
        )
        self.wait()

        self.play(
            LaggedStartMap(FadeOut, rabbits_group, lag_ratio = 0.1), 
            LaggedStartMap(FadeOut, cac_group, lag_ratio = 0.1),
            run_time = 2 
        )
        self.wait()


        top_group = VGroup(btrail, zv, zvinfo)
        self.fade_out_top_group = [FadeOut(top_group, shift = 3*UP)]

    def expected_value(self):
        old_calc = MathTex("20", "\\cdot", "0.7", "=", "14")
        old_calc.scale(2)
        self.play(FadeIn(old_calc, lag_ratio = 0.1), run_time = 2)
        self.wait()

        brace = Brace(old_calc[-1], UP, color = GREY)

        interpret1 = brace.get_text("$70\\%$ der \\\\Stichprobe")
        interpret2 = brace.get_text("Erwartungswert \\\\", "von $X$")
        interpret3 = brace.get_text("Im ", "Durchschnitt\\\\", "14 geheilte Hasen")

        self.play(
            Create(brace), 
            Write(interpret1)
        )
        self.wait()

        ntex = MathTex("n", color = RED)\
            .scale(1.5)\
            .next_to(old_calc[0], DOWN)
        ptex = MathTex("p", color = YELLOW_D)\
            .scale(1.5)\
            .next_to(old_calc[2], DOWN)


        self.play(
            FadeToColor(self.zvinfo[-4], ntex.get_color()),
            FadeToColor(self.zvinfo[-2], ptex.get_color()),
        )
        self.play(LaggedStartMap(FadeIn, VGroup(ntex, ptex), shift = DOWN, lag_ratio = 0.1), run_time = 2)
        self.wait()

        ex = MathTex("E", "(", "X", ")", "=")
        ex.scale(2)
        ex.next_to(old_calc, LEFT, buff = 0.35)

        self.play(Transform(interpret1, interpret2))
        self.play(Write(ex))
        self.wait()

        self.play(Transform(interpret1, interpret3))
        self.wait()


        # show other outcomes
        uline = Underline(interpret1[1], color = BLUE)
        self.play(Create(uline))
        uline.reverse_points()

        numbers = VGroup(*[MathTex(num).scale(1.25) for num in range(8,21)])
        numbers.arrange(DOWN)
        numbers.next_to(old_calc, RIGHT, buff = 2)

        for number in numbers:
            y_num = number.get_y()
            number.scale(np.exp(-0.2*y_num**2))

        sur_rects = VGroup(*[SurroundingRectangle(number, color = BLUE_E) for number in numbers])
        rect = sur_rects[6]

        self.play(
            Uncreate(uline), 
            LaggedStartMap(FadeIn, numbers, lag_ratio = 0.5), 
            Create(rect)
        )

        for k in [7, 8, 4]:
            self.play(Transform(rect, sur_rects[k]))
            self.wait(0.25)

        self.play(FadeOut(rect, scale = 4))
        self.wait()


        center_group = VGroup(ex, old_calc, ntex, ptex, brace, interpret1)
        self.fadeout_center_group = [FadeOut(center_group, shift = 5*RIGHT)]
        self.numbers = numbers

    def histo(self):
        histo_numbers = self.numbers
        # add histo
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] / 4,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": False,
        }

        n, p = 20, 0.7
        histo0 = self.get_histogram(n, p, zeros = True, **histo_kwargs)
        histo = self.get_histogram(n, p, **histo_kwargs)

        for hist in histo0, histo:
            hist.center()
            hist.to_edge(DOWN, buff = 0.85)

        for number, bar in zip(histo_numbers, histo.bars[8:]):
            number.generate_target()
            number.target.scale(0.9).next_to(bar, DOWN)

        self.play(
            FadeIn(histo.axes),
            ReplacementTransform(histo0.bars, histo.bars),
            LaggedStartMap(MoveToTarget, histo_numbers, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()

        self.highlight_single_bar(histo, 14, run_time = 2)
        self.wait()
        self.highlight_single_bar(histo, 12, run_time = 2)
        self.wait(2)


        rabbits_healthy = VGroup(*[self.get_rabbit(ill = False).set(height = 1) for x in range(14)])
        rabbits_healthy.arrange(RIGHT)
        rabbits_healthy.shift(2.5*UP)
        numbers = VGroup(*[MathTex(num).next_to(rab, DOWN) for num, rab in zip(range(1,15), rabbits_healthy)])

        self.play(
            histo.bars[14].animate.set_fill(opacity = histo.bar_style.get("fill_opacity")),
            histo.bars[12].animate.set_fill(opacity = 0.15),
            AnimationGroup(
                *self.fade_out_top_group,
                *self.fadeout_center_group,
                FadeIn(rabbits_healthy, lag_ratio = 0.1),
                ShowIncreasingSubsets(numbers),
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()

        texts_str = [
            ["kann passieren"],
            ["Pech gehabt"],
            ["kleine Pechsträhne"],
            ["mhhhh..."],
            ["unwahrscheinlich"],
            ["fast unmöglich"],
            ["wtf"],
            ["lost"]
        ]
        texts = VGroup(*[
            Tex(*text).scale(0.8) 
            for text in texts_str
        ])
        arrows = VGroup(*[
            CurvedArrow(numbers[-1].get_bottom(), numbers[-1 - k].get_bottom(), angle = -TAU / 6, color = BLUE_E) 
            for k in range(1, len(texts) + 1)
        ])
        for text, arrow in zip(texts, arrows):
            text.next_to(arrow, DOWN)

        for k in range(len(texts)):
            self.play(
                rabbits_healthy[13 - k].animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
                histo.bars[13 - k].animate.set_fill(opacity = histo.bar_style.get("fill_opacity")),
                histo.bars[13 - k + 1].animate.set_fill(opacity = 0.15),
                FadeToColor(numbers[13 - k], GREY),
                Transform(arrows[0], arrows[k]),
                Transform(texts[0], texts[k]),
                run_time = 1
            )
            self.wait()
        self.wait(3)

        je_desto = Tex("Je ", "größer", " die Abweichung \\\\ vom Erwartungswert, desto \\\\", "unwahrscheinlicher die\\\\", "Aussage der Firma", ".")
        je_desto.move_to(histo.axes.c2p(6, 0.17))
        self.play(Write(je_desto[:3]))
        self.wait()
        self.play(Write(je_desto[3:]))
        self.wait()

        je_desto2 = Tex("Je ", "signifikanter", " die Abweichung \\\\ vom Erwartungswert, desto \\\\", "unwahrscheinlicher die\\\\", "Nullhypothese", ".")
        je_desto2[1].set_color(BLUE_E)
        je_desto2[-2].set_color(RED_E)
        je_desto2.move_to(histo.axes.c2p(6, 0.17))
        self.play(Transform(je_desto, je_desto2))
        self.wait(3)

        null = je_desto2[4].copy()
        null.generate_target()
        null.target.scale(1.5).set_color(RED).move_to(-0.01681196*DOWN)

        self.play(
            LaggedStartMap(FadeOut, Group(*self.mobjects), lag_ratio = 0.1),
            MoveToTarget(null),
            run_time = 3
        )


class Hypothesen(Intro, HistoScene):
    def construct(self):


        self.zero_vs_alter()
        self.significance_level()
        self.play_with_alpha()

    def zero_vs_alter(self):
        hypo_info = Tex("Aussage der Firma", color = LIGHT_GREY)
        hypo_label = Tex("Nullhypothese", color = RED)
        hypo = MathTex("H_0", ":", "p", "\\geq", "0.7")
        hypo[0].set_color(hypo_label.get_color())

        hypo_group = VGroup(hypo_info, hypo_label, hypo)\
            .arrange(DOWN)\
            .to_corner(UL)\
            .shift(RIGHT)\
            .save_state()\
            .center()\
            .scale(1.5)

        alter_info = Tex("Gegenteil der Aussage", color = LIGHT_GREY)
        alter_label = Tex("Alternative", color = GREEN)
        alter = MathTex("H_1", ":", "p", "<", "0.7")
        alter[0].set_color(alter_label.get_color())

        alter_group = VGroup(alter_info, alter_label, alter)\
            .arrange(DOWN)\
            .to_corner(UR)\
            .shift(LEFT)\
            .save_state()\
            .center()\
            .scale(1.5)

        # Nullhypothese 
        self.add(hypo_label)
        self.wait()

        self.play(Write(hypo[:2]))
        self.wait()

        self.play(GrowFromPoint(hypo_info, hypo_label))
        self.wait()

        self.play(ShowIncreasingSubsets(hypo[2:], rate_func = linear), run_time = 1.5)
        self.play(Circumscribe(hypo, color = YELLOW_D, run_time = 2))
        self.wait()

        # leftsided test
        health_val = self.health_val = ValueTracker(0)

        def update_rabbits(group):
            group[0:int(health_val.get_value() + 0.5) + 1].set_fill(opacity = 1)
            group[int(health_val.get_value() + 0.5) + 1:].set_fill(opacity = 0.2)


        rabbits = VGroup(*[self.get_rabbit(ill = False).scale(0.25) for x in range(21)])
        rabbits.arrange(RIGHT)
        rabbits.set(width = config["frame_width"] - 0.5)
        rabbits.shift(DOWN)
        rabbits.set_fill(opacity = 0.2)

        numbers = VGroup()
        for num, rabbit in zip(range(len(rabbits)), rabbits):
            number = MathTex(str(num))
            number.scale(0.5)
            number.next_to(rabbit, DOWN, buff = 0.1)
            numbers.add(number)

        rabbits[14].set_stroke(color = BLUE)
        numbers[14].set_color(BLUE)


        text = Tex("linksseitiger Hypothesentest")
        text.next_to(rabbits[:14], UP, aligned_edge=RIGHT)

        ew = Tex("Erwartungswert", color = BLUE)
        ew.next_to(rabbits[14:], DOWN, buff = 0.5, aligned_edge = LEFT)

        self.play(
            Restore(hypo_group),
            LaggedStartMap(FadeIn, rabbits, lag_ratio = 0.1), 
            LaggedStartMap(FadeIn, numbers, shift = UP, lag_ratio = 0.1),
            run_time = 3
        )
        self.play(
            health_val.animate.set_value(12),
            UpdateFromFunc(rabbits, update_rabbits),
            run_time = 4
        )
        self.play(FadeIn(ew, lag_ratio = 0.2))
        self.wait()

        for k in [8,10,12]:
            self.play(
                health_val.animate.set_value(k), 
                UpdateFromFunc(rabbits, update_rabbits),
            )

        self.play(Write(text), run_time = 0.75)
        self.wait()

        group = VGroup(text, ew, rabbits, numbers)

        # Alternative
        self.play(
            AnimationGroup(
                group.animate(run_time = 3).shift(1.65*DOWN), 
                Write(alter_info, run_time = 0.75),
                lag_ratio = 0.5
            ),
        )
        self.wait()

        self.play(GrowFromPoint(alter_label, alter_info))
        self.play(Write(alter[:2]))
        self.wait()

        self.play(ShowIncreasingSubsets(alter[2:], rate_func = linear), run_time = 1.5)
        self.play(Circumscribe(alter, color = YELLOW_D, run_time = 2))
        self.wait()

        self.play(Restore(alter_group), run_time = 2)
        self.play(LaggedStartMap(FadeOut, group, shift = 2*DOWN, lag_ratio = 0.1), run_time = 2)
        self.wait()


        self.hypo_group, self.alter_group = hypo_group, alter_group

    def significance_level(self):
        self.width_val = ValueTracker(0.01)

        bar_border = self.bar_border = Rectangle(height = 0.75, width = 10, color = WHITE, stroke_width = 1)
        bar_border.shift(3*DOWN)
        bar_change = always_redraw(lambda: self.get_bar_change())

        brace_left = always_redraw(lambda: BraceBetweenPoints(bar_border.get_corner(UL), bar_change.get_corner(UR), UP, color = GREY))
        brace_right = always_redraw(lambda: BraceBetweenPoints(bar_change.get_corner(UR), bar_border.get_corner(UR), UP, color = GREY))

        dec_con = always_redraw(lambda: Integer(self.width_val.get_value(), unit = "\\%").next_to(brace_left, UP))

        safe_and_error = VGroup(*[Tex(tex, color = t_color) for tex, t_color in zip(["Sicherheit", "Irrtum"], [YELLOW_D, TEAL])])
        safe_and_error.arrange(RIGHT, buff = 2)
        safe_and_error.set_y(bar_change.get_y())

        self.add(bar_border, bar_change, brace_left, dec_con)
        self.play(
            self.width_val.animate.set_value(100),
            Write(safe_and_error[0], rate_func = squish_rate_func(smooth, 0, 0.5)),
            run_time = 3
        )
        self.wait()



        bar_error = always_redraw(lambda: self.get_bar_error())
        self.add(brace_right, bar_error)
        safe_and_error[1].next_to(bar_error, RIGHT)
        self.play(
            self.width_val.animate.set_value(95), 
            run_time = 2
        )
        self.wait()

        dec_sig = always_redraw(lambda: Integer(100 - self.width_val.get_value(), unit = "\\%").next_to(brace_right, UP))
        dec_sig.suspend_updating()
        self.play(FadeIn(dec_sig, shift = DOWN))
        dec_sig.resume_updating()
        self.play(Circumscribe(dec_sig, color = TEAL, time_width = 0.75, fade_out = True, run_time = 2))
        self.play(Write(safe_and_error[1]))
        self.wait()


        name = Tex("Signifikanzniveau ", "$\\alpha$").scale(1.5)
        self.play(FadeIn(name, lag_ratio = 0.1))
        self.wait()


        # histogram
        n, p = 20, 0.7
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] / 3,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }
        histo0 = self.get_histogram(n, p, zeros = True, **histo_kwargs)
        histo = self.histo = self.get_histogram(n, p, **histo_kwargs)
        for hist in histo, histo0:
            hist.center()
            hist.to_edge(DOWN)

        for mob in bar_change, bar_error, dec_con, brace_left, brace_right, dec_sig:
            mob.clear_updaters()

        alpha_name = name[0]
        alpha_label = name[1]
        alpha_label.generate_target()
        alpha_label.target.set_color(YELLOW_D).center().to_edge(UP).shift(0.75*DL + 0.5*LEFT)
        self.alpha_dec = dec_sig
        equal = MathTex("=").scale(1.5).set_color(YELLOW_D).next_to(alpha_label.target, RIGHT)
        self.play(
            Create(histo.axes), 
            ReplacementTransform(histo0.bars, histo.bars, lag_ratio = 0.1), 
            LaggedStartMap(FadeOut, safe_and_error, lag_ratio = 0.1), 
            LaggedStartMap(FadeOut, VGroup(bar_border, bar_change, brace_left, dec_con, bar_error, brace_right)),
            alpha_name.animate.scale(2/3).to_edge(UP),
            MoveToTarget(alpha_label),
            Write(equal),
            self.alpha_dec.animate.scale(1.5).set_color(YELLOW_D).next_to(equal, RIGHT).shift(0.05*UP),
            self.hypo_group.animate.to_corner(UL).shift(UP + 0.5*LEFT),
            self.alter_group.animate.to_corner(UR).shift(UP + 0.6*RIGHT), 
            run_time = 3
        )
        self.wait()

    def play_with_alpha(self):
        histo, alpha_dec = self.histo, self.alpha_dec

        # alpha = 0.05 --> k_l = 10
        alpha_val = self.alpha_val = ValueTracker(5)
        alpha_dec.add_updater(lambda dec: dec.set_value(alpha_val.get_value()))

        reject_name = Tex("Ablehnungsbereich ", "$\\overline{\\text{A}}$", color = PINK)\
            .scale(1.15)\
            .shift(2.5*LEFT + 1.5*UP)
        reject_info = Tex("Menge aller Erfolgszahlen, ", "bei der\\\\", "die Nullhypothese abgelehnt wird", tex_environment="flushleft")\
            .next_to(reject_name, DOWN, aligned_edge=LEFT)

        for x in range(21):
            histo.bars[x].set_fill(opacity = 0.15)
            histo.bars[x].save_state()
            histo.bars[x].set_fill(opacity = 0.6)

        self.play(Write(reject_name), run_time = 0.75)
        self.play(
            LaggedStart(*[histo.bars[x].animate.set_fill(opacity = 0.15) for x in range(11, 21)], lag_ratio = 0.1), 
            LaggedStart(*[histo.bars[x].animate.set_fill(color = PINK) for x in range(0, 11)], lag_ratio = 0.1),
            run_time = 2
        )
        self.wait()


        self.play(Write(reject_info[0]), run_time = 0.75)
        self.wait(0.5)
        self.play(Write(reject_info[1:]))
        self.wait()



        reject_set = MathTex("\\overline{\\text{A}}", "=", "\\{", "0", ",", "1", ",", "\\ldots", ",", "\\}")\
            .next_to(reject_info, DOWN, aligned_edge = LEFT)\
            .shift(0.5*RIGHT)
        reject_set[-1].shift(0.4*RIGHT)

        upper_val = self.upper_val = ValueTracker(10)
        upper_dec = Integer(upper_val.get_value(), edge_to_fix = RIGHT)

        upper_dec.next_to(reject_set[3:-1], RIGHT, buff = 0.1, aligned_edge = UP)

        self.play(
            Write(reject_set), 
            Write(upper_dec, rate_func = squish_rate_func(smooth, 0.5, 1))
        )
        upper_dec.add_updater(lambda dec: dec.set_value(upper_val.get_value()))

        # alpha = 0.15 --> k_l = 11
        self.change_alpha_animation(15, 11, run_time = 4)


        # alpha = 0.20 --> k_l = 12
        self.change_alpha_animation(20, 12, run_time = 2)
        self.wait(2)

        # alpha = 0.01 --> k_l = 8
        self.change_alpha_animation(15, 11, run_time = 1)
        self.change_alpha_animation(10, 10, run_time = 1)
        self.change_alpha_animation(5, 10, run_time = 1)
        self.change_alpha_animation(2, 9, run_time = 0.6)
        self.change_alpha_animation(1, 8, run_time = 0.4)
        self.wait(3)

        self.change_alpha_animation(5, 10, run_time = 1)
        self.play(*[Restore(bar) for bar in histo.bars[11:]])
        self.wait(2)

    # functions 
    def get_bar_change(self):
        bar =  Rectangle(
            width = self.width_val.get_value() / 10,
            height = 0.75, color = WHITE, stroke_width = 0, fill_color = YELLOW_D, fill_opacity = 0.5
        )
        bar.next_to(self.bar_border.get_left(), RIGHT, aligned_edge = LEFT, buff = 0)
        return bar

    def get_bar_error(self):
        bar = Rectangle(
            width = 10 - self.width_val.get_value() / 10,
            height = 0.75, color = WHITE, stroke_width = 0, fill_color = TEAL, fill_opacity = 0.5
        )
        bar.next_to(self.bar_border.get_right(), LEFT, aligned_edge=RIGHT, buff = 0)
        return bar

    def change_alpha_animation(self, alpha, upper, **kwargs):
        alpha_val, upper_val, histo = self.alpha_val, self.upper_val, self.histo
        self.play(
            alpha_val.animate.set_value(alpha),
            upper_val.animate.set_value(upper),
            LaggedStart(*[histo.bars[x].animate.set_fill(opacity = 0.15) for x in range(upper + 1, 21)], lag_ratio = 0.1), 
            LaggedStart(*[histo.bars[x].animate.set_fill(opacity = 0.6, color = PINK) for x in range(0, upper + 1)], lag_ratio = 0.1),
            rate_func = linear, **kwargs
        )


class CalcRejectSet(HistoScene, MovingCameraScene):
    def construct(self):
        self.n, self.p = 20, 0.7

        self.setup_old_scene()
        self.geometric_idea()
        self.calculation()
        self.look_into_table()

    def setup_old_scene(self):
        old_histo_kwargs = {
            "width": config["frame_width"] - 2,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }
        new_histo_kwargs = {"height": config["frame_height"] - 2, **old_histo_kwargs}

        histo_old = self.get_histogram(self.n, self.p, height = config["frame_height"] / 3, **old_histo_kwargs)
        histo = self.histo = self.get_histogram(self.n, self.p, **new_histo_kwargs)

        for hist in histo_old, histo:
            hist.center().to_edge(DOWN)
            hist.bars[11:].set_fill(opacity = 0.15)
            hist.bars[:11].set_fill(color = PINK)

        self.add(histo_old)
        self.wait(2)
        self.play(ReplacementTransform(histo_old, histo), run_time = 3)
        self.wait()

    def geometric_idea(self):
        histo = self.histo

        self.alpha_val = ValueTracker(0.05)
        alpha_line = DashedLine(
            start = histo.axes.c2p(0, self.alpha_val.get_value()), 
            end = histo.axes.c2p(21, self.alpha_val.get_value()),
            color = YELLOW_D, stroke_width = 2
        )
        alpha_dec = DecimalNumber(self.alpha_val.get_value(), edge_to_fix = RIGHT)\
            .scale(0.75)\
            .next_to(alpha_line, LEFT)\
            .set_color(alpha_line.get_color())
        self.play(
            Create(alpha_line),
            FadeIn(alpha_dec, shift = RIGHT),
        )
        alpha_dec.add_updater(lambda dec: dec.set_value(self.alpha_val.get_value()).next_to(alpha_line, LEFT))
        self.wait()

        # group first 11 bars ( 0 -- 10 )
        first_10_bars = self.first_10_bars = VGroup(*[histo.bars[x].copy() for x in range(11)])
        self.play(first_10_bars.animate.shift(2*UP), run_time = 2)

        first_10_bars.generate_target()
        first_10_bars.target.arrange(DOWN, buff = 0).set_x(histo.axes.x_labels[5].get_x())
        self.play(MoveToTarget(first_10_bars), run_time = 3)
        self.play(first_10_bars.animate.next_to(histo.bars[5].get_bottom(), UP, buff = 0), run_time = 3)
        self.wait()

        # zoom in 
        self.renderer.camera.frame.save_state()
        self.play(
            self.renderer.camera.frame.animate.scale(1/3).move_to(first_10_bars),
            run_time = 3
        )
        brace_kum = Brace(first_10_bars, LEFT, color = GREY)
        brace_label = brace_kum.get_tex(str(get_binom_cdf_result(self.n, self.p, 10)))
        for mob in brace_kum, brace_label:
            mob.save_state()

        self.play(Create(brace_kum))
        self.play(FadeIn(brace_label, lag_ratio = 0.1), run_time = 1.5)
        self.play(Circumscribe(brace_label, color = PINK, time_width = 1, run_time = 2))
        self.wait()

        self.play(
            Restore(self.renderer.camera.frame), 
            run_time = 3
        )
        self.wait()

        # one more healthy rabbit
        eleven = histo.bars[11].copy()
        eleven.generate_target()
        eleven.target.set_fill(opacity = 0.6, color = PINK).next_to(histo.bars[5].get_bottom(), UP, buff = 0)

        first_10_bars.save_state()
        first_10_bars.generate_target()
        first_10_bars.target.next_to(eleven.target, UP, buff = 0)

        brace_11 = Brace(VGroup(eleven.target, first_10_bars.target), LEFT, color = GREY)
        brace_label_11 = brace_11.get_tex(str(get_binom_cdf_result(self.n, self.p, 11)))

        self.play(
            *[MoveToTarget(mob) for mob in [eleven, first_10_bars]],
            Transform(brace_kum, brace_11),
            Transform(brace_label, brace_label_11),
            rate_func = lambda t: there_and_back_with_pause(t, pause_ratio = 1/3),
            run_time = 4
        )
        self.remove(eleven)
        self.wait()

        # what about 9 rabbits???
        first_9 = first_10_bars[:10]
        first_9.generate_target()
        first_9.target.next_to(histo.bars[5].get_bottom(), UP, buff = 0)

        self.wait()
        brace_9 = Brace(first_9.target, LEFT, color = GREY)
        brace_label_9 = brace_9.get_tex(str(get_binom_cdf_result(self.n, self.p, 9)))

        self.play(
            MoveToTarget(first_9),
            first_10_bars[10].animate.next_to(histo.bars[10].get_bottom(), UP, buff = 0),
            Transform(brace_kum, brace_9), 
            Transform(brace_label, brace_label_9),
            run_time = 3
        )
        self.wait(0.5)
        self.play(Circumscribe(brace_label_9, color = YELLOW_D, time_width = 0.75, run_time = 2))
        self.wait()

        self.play(
            *[Restore(mob) for mob in [brace_kum, brace_label, first_10_bars]],
            run_time = 2
        )
        self.wait()

        self.brace_label, self.brace_kum = brace_label, brace_kum 

    def calculation(self):
        text = Tex(
            "10 ", "geheilte Hasen ", " zu haben ist die\\\\", "größtmögliche Erfolgszahl,", " bei der\\\\", "die ",
            "summierte Wahrscheinlichkeit \\\\", "kleiner oder gleich ", "0.05", " ist",
            tex_environment="flushleft"
        )
        text.to_edge(UP)
        text.shift(1.5*LEFT)

        self.play(Write(text[:4]))
        self.wait(0.5)
        uline = Underline(text[3], color = BLUE)
        self.play(Create(uline))
        uline.reverse_points()
        self.play(Uncreate(uline))

        self.play(FadeIn(text[4:], lag_ratio = 0.1), run_time = 2)
        self.play(Indicate(text[7:9]), run_time = 2)
        self.wait(2)

        #                       0      1       2       3     4      5         6         7
        eq = self.eq = MathTex("P", "\\big(", "X", "\\leq", "g", "\\big)", "\\leq", "0.05")
        eq.scale(1.5)
        eq.set_color_by_tex_to_color_map({"0.05": YELLOW_D, "g": PINK, "\\big": WHITE})
        eq.next_to(text, DOWN, buff = 0.75)
        eq.shift(0.5*LEFT)

        self.play(FadeIn(eq[4], shift = UP))
        self.wait()
        self.play(
            LaggedStart(
                *[FadeIn(eq[index], shift = UP) for index in [0,1,2,3,5]],
                lag_ratio = 0.2
            )
        )
        self.wait()
        self.play(GrowFromCenter(eq[6]))
        self.wait(0.5)
        self.play(FadeIn(eq[-1], shift = DOWN))
        self.play(Circumscribe(eq, color = BLUE, time_width = 0.75, run_time = 2))
        self.wait()


        self.play(
            FadeOut(text, shift = 5*UP), 
            eq.animate.to_edge(UP), 
            run_time = 3
        )
        self.wait()

        brace = Brace(eq[:6], DOWN, color = GREY)
        brace_texts = VGroup(*[
            Tex(tex).next_to(brace, DOWN) 
            for tex in ["vorgegebene Tabellen", "Tabellen Tafelwerk", "Taschenrechner"]
        ])
        self.play(
            Create(brace),
            Write(brace_texts[0]), 
            run_time = 0.75
        )
        self.wait(0.5)
        self.play(Transform(brace_texts[0], brace_texts[1]))
        self.wait(0.5)
        self.play(Transform(brace_texts[0], brace_texts[2]))
        self.wait()

        self.play(
            FadeOut(brace_texts[0]), 
            FadeOut(brace)
        )

    def look_into_table(self):

        k_values = VGroup(*[Integer(x).scale(0.85) for x in reversed(range(8, 14))])
        k_values.arrange(DOWN, aligned_edge = LEFT)
        k_values.shift(2*LEFT + 0.5*UP)

        k_probs = VGroup(*[
            MathTex(str(get_binom_cdf_result(self.n, self.p, k.get_value())))\
                .match_height(k)\
                .next_to(k.get_left(), RIGHT, buff = 0, aligned_edge=LEFT)\
                .shift(2*LEFT)
            for k in k_values
        ])

        n = Integer(20, color = GREY).scale(0.85).rotate(90*DEGREES).next_to(k_values, RIGHT)
        p = DecimalNumber(0.70, color = GREY).scale(0.85).next_to(k_probs, UP)

        self.play(Write(n), run_time = 0.5)
        self.play(Write(p), run_time = 0.5)
        self.wait()

        self.play(LaggedStartMap(FadeIn, k_values, shift = LEFT, lag_ratio = 0.15), run_time = 2)
        self.wait()

        self.play(LaggedStartMap(FadeIn, k_probs, shift = RIGHT, lag_ratio = 0.15), run_time = 2)
        self.wait()


        rects = VGroup(*[
            SurroundingRectangle(VGroup(k_values[index], k_probs[index]), color = BLUE)
            for index in range(len(k_values))
        ])
        self.play(
            Circumscribe(self.brace_label, color = BLUE, run_time = 2.5),
            Create(rects[3], run_time = 2.5)
        )
        self.wait()


        g_eq = MathTex("g", "=", "10")
        g_eq[0].set_color(PINK)
        g_eq.scale(1.5)
        g_eq.next_to(self.eq, DOWN, buff = 1)
        g_eq.align_to(self.eq[4], LEFT)

        self.play(
            AnimationGroup(
                FadeOut(n, shift = RIGHT),
                FadeOut(p, shift = LEFT), 
                FadeOut(k_values, shift = RIGHT), 
                FadeOut(k_probs, shift = LEFT), 
                FadeOut(rects[3], scale =3),
                FadeOut(self.brace_kum), 
                FadeOut(self.brace_label), 
                FadeOut(self.first_10_bars), 
                FadeIn(g_eq, shift = 2*DOWN, scale = 1.5), 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(Circumscribe(g_eq, color = BLUE, time_width = 0.75, run_time = 3))
        self.wait()


class Interpretation(Intro):
    def construct(self):

        self.rule()
        self.result_for_12_healed_rabbits()

    def rule(self):
        reject_name = Tex("Ablehnungsbereich", color = PINK).to_edge(UP)
        reject = self.reject = MathTex("\\overline{\\text{A}}", "=", "\\{", "0", ",", "1", ",", "\\ldots", ",", "10", "\\}").next_to(reject_name, DOWN)

        hypo_group = self.get_hypo_group()
        alter_group = self.get_alter_group()

        rule, rule_name = self.get_rule_and_name()

        # write hypos, reject and rule
        self.play(
            LaggedStartMap(FadeIn, VGroup(reject_name, rule_name), shift = DOWN, lag_ratio = 0.5),
            run_time = 2
        )
        self.play(
                LaggedStart(
                FadeIn(hypo_group, shift = 3*RIGHT), 
                FadeIn(alter_group, shift = 3*LEFT), 
                lag_ratio = 0.25
            ),
            run_time = 2
        )
        self.wait()

        self.play(
            Write(reject[:3]), 
            Write(reject[-1]),
            run_time = 0.75
        )
        self.wait()

        self.play(FadeIn(reject[3:-1], shift = UP, lag_ratio = 0.2), run_time = 2)
        self.wait()


        # write down decision rule
        health_val = self.health_val = ValueTracker(0)

        def update_rabbits(group):
            group[0:int(health_val.get_value() + 0.5)].set_fill(opacity = 1)
            group[int(health_val.get_value() + 0.5):].set_fill(opacity = 0.2)

        rabbits = self.rabbits = self.get_rabbits()
        rabbits.set_fill(opacity = 0.2)

        def update_health_int(mob):
            if health_val.get_value() < 10.5:
                mob.set_color(C_COLOR)
            else:
                mob.set_color(X_COLOR)
            mob.set_value(health_val.get_value())
            return mob

        health_int = self.health_int = Integer(health_val.get_value(), edge_to_fix = ORIGIN)\
            .scale(2.5)\
            .move_to(rabbits)\
            .add_updater(update_health_int)


        self.play(LaggedStartMap(FadeIn, rabbits, lag_ratio = 0.1), run_time = 2)
        self.add(health_int)
        self.play(
            Write(rule[:4]),
            health_val.animate.set_value(10),
            UpdateFromFunc(rabbits, update_rabbits)
        )
        self.wait()

        self.play(Write(rule[4:]))
        self.wait(0.25)

        hypo_rect = self.hypo_rect = SurroundingRectangle(hypo_group, color = X_COLOR).save_state()
        alter_rect = SurroundingRectangle(alter_group, color = C_COLOR)
        cross_hypo = self.cross_hypo = Cross(hypo_group, stroke_color = RED)
        cross_alter = self.cross_alter = Cross(alter_group, stroke_color = GREEN)

        self.play(
            LaggedStart(
                Create(hypo_rect), 
                GrowFromCenter(cross_hypo), 
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait(2)


        self.play(Transform(hypo_rect, alter_rect), run_time = 3)
        self.wait()

    def result_for_12_healed_rabbits(self):
        health_val, rabbits = self.health_val, self.rabbits
        def update_rabbits(group):
            group[0:int(health_val.get_value() + 0.5)].set_fill(opacity = 1)
            group[int(health_val.get_value() + 0.5):].set_fill(opacity = 0.2)

        self.play(
            LaggedStart(*[FocusOn(rabbits[index]) for index in [10, 11]], lag_ratio = 0.1),
            run_time = 1.5
        )
        self.play(
            health_val.animate.set_value(12),
            UpdateFromFunc(rabbits, update_rabbits),
            run_time = 3
        )
        not_in_A = MathTex("12", "\\notin", "\\overline{\\text{A}}")\
            .next_to(self.reject, DOWN)
        self.play(
            TransformFromCopy(self.health_int, not_in_A[0]), 
            Write(not_in_A[1:], rate_func = squish_rate_func(smooth, 0.5, 1)), 
            run_time = 2
        )
        self.wait()

        self.play(
            ShrinkToCenter(self.cross_hypo),
            Restore(self.hypo_rect), 
            run_time = 3
        )
        self.wait()

        def update_rabbits(group):
            group[0:int(health_val.get_value() + 0.5)].set_fill(opacity = 1)
            group[int(health_val.get_value() + 0.5):].set_fill(opacity = 0.2)

        self.health_val.set_value(0)
        self.play(
            self.health_val.animate.set_value(12), 
            UpdateFromFunc(self.rabbits, update_rabbits), 
            run_time = 3
        )
        self.wait()

        tex_not = Tex("nicht").next_to(self.health_int, UP)
        tex_sign = Tex("signifikant").scale(0.8).next_to(self.health_int, DOWN)
        self.play(
            LaggedStart(
                FadeIn(tex_not, shift = DOWN), 
                FadeIn(tex_sign, shift = UP),
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()

        self.play(GrowFromCenter(self.cross_alter), run_time = 2)
        self.wait(3)

    # functions
    def get_rule_and_name(self):
        rule = Tex(
            "Werden in einer Stichprobe ", "höchstens ", "10 Hasen\\\\", 
            "geheilt,", " so ist die ", "Nullhypothese", " abzulehnen", ".", 
        )
        rule_name = Tex("Entscheidungsregel", color = BLUE)
        rule_name.next_to(rule, UP)

        return rule, rule_name

    def get_hypo_group(self):
        hypo_info = Tex("Firmenaussage", color = LIGHT_GREY)
        hypo_label = Tex("Nullhypothese", color = RED)
        hypo = MathTex("H_0", ":", "p", "\\geq", "0.7")
        hypo[0].set_color(hypo_label.get_color())

        hypo_group = VGroup(hypo_info, hypo_label, hypo)\
            .arrange(DOWN)\
            .to_corner(UL)

        return hypo_group

    def get_alter_group(self):
        alter_info = Tex("Gegenteil", color = LIGHT_GREY)
        alter_label = Tex("Alternative", color = GREEN)
        alter = MathTex("H_1", ":", "p", "<", "0.7")
        alter[0].set_color(alter_label.get_color())

        alter_group = VGroup(alter_info, alter_label, alter)\
            .arrange(DOWN)\
            .to_corner(UR)

        return alter_group

    def get_rabbits(self):
        rabbits = VGroup(*[self.get_rabbit(ill = False).scale(0.25) for x in range(20)])
        rabbits.arrange_in_grid(2,10)
        rabbits.to_edge(DOWN)
        rabbits[:5].shift(LEFT)
        rabbits[5:10].shift(RIGHT)
        rabbits[10:15].shift(LEFT)
        rabbits[15:].shift(RIGHT)

        rabbits[:10].set_stroke(color = PINK)
        rabbits[13].set_stroke(color = BLUE)

        return rabbits


class Thumbnail(Intro, HistoScene):
    def construct(self):

        cac_bools = 12*[True] + 8*[False]
        random.shuffle(cac_bools)
        cac_group = get_checks_and_crosses(cac_bools).scale(0.8)

        neg_bools = [not elem for elem in cac_bools]
        rabbits_group = VGroup(*[self.get_rabbit(ill = bools).scale(0.25) for bools in neg_bools])
        rabbits_group.arrange_in_grid(2,10, buff = 0.45)
        rabbits_group[:10].to_edge(UP, buff = 0.1)
        rabbits_group[10:].to_edge(DOWN, buff = 0.1)

        for cac, rabbit in zip(cac_group, rabbits_group):
            cac.next_to(rabbit, DOWN)

        for cac, rabbit in zip(cac_group[10:], rabbits_group[10:]):
            cac.next_to(rabbit, UP)

        self.add(rabbits_group, cac_group)


        arrow = Arrow(2.75*LEFT, 2.75*RIGHT, color = BLUE_E, buff = 0).shift(0.5*UP)
        medicin = self.get_medicin().scale(0.5).next_to(arrow, UP)
        text2 = Tex("mindestens $70\\%$").scale(1.4).next_to(arrow, DOWN, buff = 0.1)
        self.add(arrow, medicin,  text2)


        rabbit_ill = self.get_rabbit(ill = True).scale(0.6).next_to(arrow, LEFT, buff = 1)
        rabbit_hea = self.get_rabbit(ill = False).scale(0.6).next_to(arrow, RIGHT, buff = 1)
        self.add(rabbit_ill, rabbit_hea)


        twelve = Integer(12).set_color(GREEN)
        von = Tex("von").set_color(GREY)
        twenty = Integer(20).set_color(RED)
        ratio = VGroup(twelve, von, twenty)
        ratio.scale(3.5)
        ratio.arrange(RIGHT, buff = 0.5, aligned_edge = DOWN)
        ratio.shift(1.35*DOWN)
        self.add(ratio)







# ###############################################
class Price(Scene):
    def construct(self):
        price_flag = self.get_price_flag()
        price_flag.to_edge(UP)
        price_flag.save_state()

        price_flag.banner.center()
        price_flag.texts.center()

        self.play(
            Create(price_flag.banner), 
            Write(price_flag.texts), 
            run_time = 2
        )
        self.play(
            Restore(price_flag),
            *[Create(pole) for pole in price_flag.poles],
            run_time = 2
        )
        self.wait()


        wheel = self.get_wheel()
        self.add(wheel)




    def get_price_flag(self):
        text1 = Tex("Hauptgewinn", color = YELLOW_D)
        text2 = Tex("bei jedem").scale(0.7)
        text3 = Tex("25.", " Versuch", color = TEAL)

        texts = VGroup(text1, text2, text3)
        for text in texts:
            text.scale(1.5)
        texts.arrange(RIGHT, aligned_edge = UP, buff = 0.5)

        banner = SurroundingRectangle(texts, color = GREY)

        pole_left = Line(ORIGIN, 3.5*UP, color = GREY)\
            .next_to(banner.get_corner(DL), DOWN, buff = 0)
        pole_right = Line(ORIGIN, 3.5*UP, color = GREY)\
            .next_to(banner.get_corner(DR), DOWN, buff = 0)
        poles = VGroup(pole_left, pole_right)

        result = VGroup(banner, texts, poles)
        result.banner = banner
        result.texts = texts
        result.poles = poles

        return result

    def get_wheel(self):
        succ_sector = Sector(outer_radius = 1.5, angle = 14.4*DEGREES, start_angle = 30*DEGREES)\
            .set_fill(color = YELLOW_D, opacity = 1)\
            .set_stroke(width = 1)
        fail_sector = Sector(outer_radius = 1.5, angle = 345.6*DEGREES, start_angle =  44.4*DEGREES)\
            .set_fill(color = GREY, opacity = 1)\
            .set_stroke(width = 1)
        dot = Dot()
        arrow = Arrow(DOWN, UP, stroke_width = 8, color = BLACK).move_to(dot)

        wheel = VGroup(succ_sector, fail_sector, arrow, dot)
        wheel.arrow = arrow
        wheel.s_sector = succ_sector
        wheel.f_sector = fail_sector

        return wheel





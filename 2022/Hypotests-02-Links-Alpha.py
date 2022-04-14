from manim import *
from BinomHelpers import *
import math 



def get_chip():
    body = RoundedRectangle(corner_radius = 0.1, width = 1, height = 1, stroke_opacity = 0, fill_color = "#036B00", fill_opacity = 1)
    middle = RoundedRectangle(corner_radius = 0.075, width = 0.7, height = 0.7, stroke_opacity = 0, fill_color = GREY, fill_opacity = 1)
    top = RoundedRectangle(corner_radius = 0.05, width = 0.35, height = 0.35, stroke_opacity = 0, fill_color = "#EF9926", fill_opacity = 1)

    nipples = VGroup(*[get_nipples() for x in range(4)])
    for nipple_group, angle, direction in zip(nipples, [0, 90, 0, 90], [UP, RIGHT, DOWN, LEFT]):
        nipple_group.set(width = body.width - 0.15)
        nipple_group.rotate(angle*DEGREES)
        nipple_group.next_to(body.get_edge_center(direction), direction, buff = 0)

    return VGroup(body, middle, top, nipples)

def get_nipples():
    nipple = Rectangle(width = 0.25, height = 0.45, stroke_opacity = 0, fill_color = "#EF9926", fill_opacity = 1)

    nipples = VGroup()
    for x in range(7):
        nip = nipple.copy()
        nipples.add(nip)
    nipples.arrange(RIGHT)

    return nipples


class Intro(Scene):
    def construct(self):
        self.smarties()
        self.produce_chips()
        self.order_chips()
        self.ask_for_number()


    def smarties(self):
        smartwatch = self.get_smartwatch().scale(3)
        logo = self.get_logo()
        logo.set(width = smartwatch[5].width - 0.2)
        logo.move_to(smartwatch[5])
        logo.shift(0.2*UP)

        self.play(Create(smartwatch), run_time = 2)
        watch_vx = Tex("gucken")
        watch_vx.next_to(logo, DOWN)
        self.play(
            FadeIn(logo, lag_ratio = 0.1), 
            FadeIn(watch_vx, shift = 0.5*UP)
        )
        self.wait()

        smartphone = self.get_smartphone().scale(3)
        watch_rect = ScreenRectangle(color = GREY, stroke_width = 2)
        watch_rect.scale_to_fit_width(width = smartphone[4].width - 0.1)
        watch_rect.move_to(smartphone[4]).shift(1.25*UP)

        comment_vx = Tex("und\\\\fleißig\\\\kommentieren")
        comment_vx.set(width = smartphone[4].width - 0.1)
        comment_vx.shift(DOWN)

        self.play(
            ReplacementTransform(smartwatch, smartphone),
            logo.animate.scale(0.2).next_to(watch_rect.get_corner(UR), DOWN, buff = 0.05, aligned_edge = RIGHT).shift(0.05*LEFT),
            Create(watch_rect),
            ReplacementTransform(watch_vx, comment_vx, rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 1.5)
        )
        self.bring_to_front(watch_rect, logo)
        self.wait()


        def scale_fade(group, alpha):
            group.restore()
            group.scale(1 + 4*alpha)
            group.fade(alpha**2)


        chip = self.chip = get_chip().scale(3)
        scale_group = VGroup(smartphone, logo, watch_rect, comment_vx)
        scale_group.save_state()
        self.play(
            UpdateFromAlphaFunc(scale_group, scale_fade),
            FadeIn(chip, scale=0.05, rate_func = squish_rate_func(smooth, 0.3, 1)), 
            run_time = 2
        )

    def produce_chips(self):
        chip_text = Tex("Computerchip")\
            .scale(2)\
            .next_to(self.chip, UP)
        self.play(FadeIn(chip_text, shift = 3*RIGHT))
        self.wait()

        prob_val = ValueTracker(0)
        prob_dec = Integer(prob_val.get_value(), unit = "\\%", edge_to_fix = LEFT)\
            .scale(4)\
            .to_edge(LEFT, buff = 0.75)\
            .add_updater(lambda dec: dec.set_value(prob_val.get_value()))

        cmark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        cmark.set(height = prob_dec.height)
        cmark.to_edge(RIGHT, buff = 0.75)

        arrow = Arrow(LEFT, RIGHT, color = C_COLOR)
        arrow.next_to(cmark, LEFT)

        self.play(
            FadeIn(prob_dec, run_time = 1),
            prob_val.animate(run_time = 2).set_value(97),
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arrow),
            FadeIn(cmark, shift = 2*RIGHT)
        )
        self.wait()

        self.fadeout_anims = [
            FadeOut(chip_text, shift = 3*UP),
            FadeOut(cmark, shift = 3*RIGHT),
            FadeOut(arrow, shift = 3*RIGHT),
            prob_dec.animate.scale(0.25).center(),
        ]

    def order_chips(self):
        chips = VGroup(*[get_chip() for x in range(300)])
        chips.arrange_in_grid(12, 25)
        chips.set(width = config["frame_width"] - 0.5)
        chips[:150].to_edge(UP)
        chips[150:].to_edge(DOWN)

        self.chip.generate_target()
        self.chip.target.match_width(chips[0]).move_to(chips[0])

        self.play(
            MoveToTarget(self.chip),
            LaggedStart(*self.fadeout_anims, lag_ratio = 0.1, rate_func = squish_rate_func(smooth, 0, 0.5)),
            LaggedStartMap(FadeIn, chips[1:], lag_ratio = 0.05),
            run_time = 4
        )
        self.add(chips)

        total_tex = MathTex("300").to_edge(LEFT).shift(RIGHT)

        self.play(
            FadeIn(total_tex, shift = 2*RIGHT, rate_func = squish_rate_func(smooth, 0.5, 1)),
            run_time = 2
        )
        self.wait(3)

        self.chips = chips

    def ask_for_number(self):
        val = ValueTracker(300)
        dec = Integer(val.get_value(), edge_to_fix = RIGHT)\
            .to_edge(RIGHT)\
            .shift(LEFT)\
            .add_updater(lambda dec: dec.set_value(val.get_value()))

        def update_chips(group):
            group[0:int(val.get_value() + 0.5)].set_fill(opacity = 1)
            group[int(val.get_value() + 0.5):].set_fill(opacity = 0.2)

        self.add(dec)
        self.play(
            UpdateFromFunc(self.chips, update_chips), 
            val.animate.set_value(250), 
            run_time = 3
        )
        self.wait()

        self.play(
            UpdateFromFunc(self.chips, update_chips), 
            val.animate.set_value(280), 
            run_time = 2
        )
        self.play(
            UpdateFromFunc(self.chips, update_chips), 
            val.animate.set_value(290), 
            run_time = 2
        )
        self.wait(2)

    # functions
    def get_smartphone(self):
        sp = SVGMobject(SVG_DIR + "smartphone")
        sp[:4].set_color(RED_A)
        sp[4].set_fill(color = "#2D2D2D", opacity = 1)
        sp[5:8].set_color(GREY_A)
        sp[8].set_color(RED_A)

        return sp

    def get_smartwatch(self):
        sw = SVGMobject(SVG_DIR + "smartwatch")
        sw[:4].set_fill(color = GREEN_B, opacity = 1)
        sw[4].set_fill(color = GREY, opacity = 1)
        sw[5].set_fill(color = "#2D2D2D", opacity = 1)

        return sw

    def get_logo(self):
        logo = SVGMobject(SVG_DIR + "VisualX-ausgeschrieben")
        logo[:6].set_color(WHITE)
        logo[6:8].set_color(BLUE)
        logo[8:10].set_color(RED)
        logo[-2:].set_color(YELLOW)
        return logo


class LeftSidedTest(HistoScene):
    def construct(self):
        histo_kwargs = {
            "width": config["frame_width"] - 4.5, "height": config["frame_height"] / 2,
            "x_tick_freq": 20, "x_label_freq": 20, "y_max_value": 0.15, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }

        self.n, self.p = 300, 0.97
        histo0 = self.get_histogram(self.n, self.p, zeros = True, **histo_kwargs)
        histo = self.histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        for hist in histo0, histo:
            hist.center()
            hist.to_corner(DL, buff = 0.85)
            hist.shift(LEFT)

        x_label = Tex("Anzahl der funktionsfähigen Chips", color = GREY).next_to(histo, DOWN)
        y_label = Tex("Vertrauenslevel")

        gauss = histo.axes.get_graph(lambda x: self.get_gaussian(x, self.n, self.p), x_range=[0,300])


        delivery = Tex("Lieferung mit").to_corner(UR, buff = 0.5)
        delivery3 = Tex("Chips").next_to(delivery, DOWN, buff = 0.5, aligned_edge=RIGHT)
        delivery2 = Tex("300").scale(2).next_to(delivery3, LEFT, aligned_edge=DOWN)


        pieces = Tex("funktionsfähig").to_corner(UR, buff = 0.5).shift(2*DOWN)
        pieces_unit = Tex("Stück").next_to(pieces, DOWN, buff = 0.5, aligned_edge=RIGHT)

        pieces_val = ValueTracker(0)
        pieces_num = Integer(pieces_val.get_value(), edge_to_fix = RIGHT)\
            .scale(2)\
            .next_to(pieces_unit, LEFT, aligned_edge=DOWN)\
            .add_updater(lambda dec: dec.set_value(pieces_val.get_value()))

        self.play(
            Create(histo.axes.x_axis),
            LaggedStartMap(FadeIn, histo.axes.x_labels, shift = DOWN),
            Write(x_label),
            LaggedStart(*[FadeIn(mob, shift = 2*RIGHT) for mob in [delivery, delivery2, delivery3]], lag_ratio = 0.1), 
            LaggedStart(*[FadeIn(mob, shift = 2*LEFT) for mob in [pieces, pieces_num, pieces_unit]], lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()


        moving_dot = always_redraw(
            lambda: Dot(
                point = histo.axes.c2p(pieces_val.get_value(), 1/6*self.get_errorfunc(pieces_val.get_value())), 
                color = RED, stroke_width = 1, stroke_color = WHITE,
                )
            )
        moving_vline = always_redraw(
            lambda: histo.axes.get_vertical_line(moving_dot.get_center(), line_func = DashedLine, color = YELLOW_D)
        )
        errorfunc = always_redraw(
            lambda: histo.axes.get_graph(
                lambda x: 1/6*self.get_errorfunc(x), 
                x_range = [0, pieces_val.get_value()], 
                color = RED, stroke_width = 3
            )
        )
        self.add(moving_dot, moving_vline, errorfunc)
        self.wait()


        self.play(pieces_val.animate(rate_func = linear).set_value(250), run_time = 7)
        self.play(pieces_val.animate(rate_func = linear).set_value(280), run_time = 2)
        self.play(pieces_val.animate(rate_func = linear).set_value(300), run_time = 6)
        self.wait()

        errorfunc.clear_updaters()
        self.play(pieces_val.animate(rate_func = smooth).set_value(285), run_time = 4)
        self.wait(3)


    def get_gaussian(self, x, n, p):
        mu = n*p
        sigma = np.sqrt(mu * (1-p))

        return 1/np.sqrt(2*np.pi*sigma**2) * np.exp(-(x - mu)**2/(2*sigma**2))

    def get_errorfunc(self, x):
        mu = self.n*self.p
        sigma = np.sqrt(mu * (1-self.p))

        return 1/2*(1 + math.erf((x-mu)/(np.sqrt(2) * sigma)))


class BuildUpTest(HistoScene):
    def construct(self):

        self.zufallsvariable()
        self.hypothesen()
        self.histogram()
        self.expected_value()
        self.signifikanzniveau()
        self.reject_set()


    def zufallsvariable(self):

        zv = self.zv = MathTex("X", "\\sim", "\\mathcal{B}", "(", "300", ",", "0.97", ")").scale(2)
        zv_info = Tex("$X$", "$-$", "Anzahl funktionsfähige Chips").next_to(zv, UP, aligned_edge=LEFT)

        arrow_n = Arrow(DL, UR, color = GREY).next_to(zv[4].get_bottom(), DOWN, aligned_edge = RIGHT)
        arrow_p = Arrow(DR, UL, color = GREY).next_to(zv[6].get_bottom(), DOWN, aligned_edge = LEFT)

        tex_n = MathTex("n", color = BLUE).next_to(arrow_n.point_from_proportion(0.5), LEFT)
        tex_p = MathTex("p", color = YELLOW_D).next_to(arrow_p.point_from_proportion(0.5), RIGHT)

        text_n = Tex("Stichprobenumfang", color = BLUE).next_to(arrow_n.get_start(), DOWN).shift(LEFT)
        text_p = Tex("Erfolgswahrscheinlichkeit", color = YELLOW_D).next_to(arrow_p.get_start(), DOWN)

        uline_n = Underline(text_n, color = text_n.get_color())
        uline_p = Underline(text_p, color = text_p.get_color())

        self.play(Write(zv))
        self.play(Write(zv_info), run_time = 0.75)
        self.wait(0.5)

        self.play(
            *[GrowArrow(arrow) for arrow in [arrow_p, arrow_n]], 
            FadeIn(tex_n, shift = RIGHT), 
            FadeIn(tex_p, shift = LEFT),
            run_time = 1.5
        )
        self.wait(0.5)

        self.play(
            FadeIn(text_n, lag_ratio = 0.1),
            Create(uline_n),
            FadeToColor(zv[4], BLUE)
        )
        uline_n.reverse_direction()
        self.play(Uncreate(uline_n), run_time = 0.5)

        self.play(
            FadeIn(text_p, lag_ratio = 0.1),
            Create(uline_p),
            FadeToColor(zv[6], YELLOW_D)
        )
        uline_p.reverse_direction()
        self.play(Uncreate(uline_p), run_time = 0.5)
        self.wait()

        zv_group = VGroup(zv, zv_info)
        fadeout_group = VGroup(text_n, tex_n, arrow_n, text_p, tex_p, arrow_p)
        self.play(
            zv_group.animate.scale(0.5).to_edge(UP),
            LaggedStartMap(FadeOut, fadeout_group, shift = 2*DOWN, lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()

    def hypothesen(self):
        hypo_group = self.get_hypo_group().scale(2)
        alter_group = self.get_alter_group().scale(2)

        for group, corner in zip([hypo_group, alter_group], [UL, UR]):
            self.play(
                LaggedStart(
                    Write(group[1]), 
                    Write(group[2][:2]), 
                    lag_ratio = 0.75
                )
            )
            self.play(FadeIn(group[0], shift = 3*RIGHT))
            self.wait()

            self.play(FadeIn(group[2][2:], lag_ratio = 0.1), run_time = 2)
            self.play(Circumscribe(group[1:], color = group[1].get_color(), run_time = 2))
            self.wait()

            info = group[0]
            group.remove(group[0])
            group.generate_target()
            group.target.scale(0.5).to_corner(corner)

            self.play(
                FadeOut(info),
                MoveToTarget(group), 
                run_time = 1.5
            )

    def histogram(self):
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] / 2,
            "x_tick_freq": 20, "x_label_freq": 20, "y_max_value": 0.15, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }

        n, p = 300, 0.97
        histo0 = self.get_histogram(n, p, zeros = True, **histo_kwargs)
        histo = self.histo = self.get_histogram(n, p, **histo_kwargs)
        for hist in histo0, histo:
            hist.center()
            hist.to_edge(DOWN)

        self.transform_zeros_into_histo(histo, width= config["frame_width"] - 2, height= config["frame_height"] / 4, run_time = 5)
        self.wait()

        # makes bars bigger
        bars = histo.bars[275:]
        bars.generate_target()
        bars.target.stretch_to_fit_width(9).set_x(0)

        self.play(
            MoveToTarget(bars),
            run_time = 3
        )
        ticks = VGroup()
        for bar in bars:
            tick = Line(UP, DOWN, stroke_width = 2)
            tick.set_length(0.2)
            tick.move_to(bar.get_corner(DR))
            ticks.add(tick)

        new_x_axis = Line(histo.axes.c2p(0,0), ticks[-1].get_center(), stroke_width = 2)
        new_x_labels = VGroup()
        for x, bar in zip([275, 280, 285, 290, 295, 300], bars[::5]):
            label = MathTex(str(x)).scale(0.75)
            label.next_to(bar, DOWN)
            new_x_labels.add(label)

        self.play(
            FadeOut(histo.bars[:275]),
            Transform(histo.axes.x_axis, new_x_axis),
            Transform(histo.axes.x_labels[1:], new_x_labels),
            Create(ticks, lag_ratio = 0.1),
        )
        self.wait()


        self.bars = bars

        # animations for later
        self.fade_out_histo_stuff = [
            FadeOut(histo.axes.y_axis),
            *[FadeOut(mob, shift = 5*RIGHT) for mob in [ticks, histo.axes.x_axis, histo.axes.x_labels]],
            LaggedStartMap(FadeOut, bars[11:], shift = 3*DOWN, lag_ratio = 0.05),
            bars[:11].animate.move_to(3.5*RIGHT + 0.25*UP),
        ]

    def expected_value(self):
        ex1 = MathTex("E", "(", "X", ")", "=", "n", "\\cdot", "p")\
            .shift(4.25*RIGHT + 0.5*UP)\
            .set_color_by_tex_to_color_map({"n": BLUE, "p": YELLOW_D})
        ex2 = MathTex("=", "300", "\\cdot", "0.97")\
            .set_color_by_tex_to_color_map({"300": BLUE, "0.97": YELLOW_D})
        ex3 = MathTex("=", "291")
        ex3[1].set_color(self.histo.bars[291].get_color())

        for ex in ex2, ex3:
            ex.next_to(ex1[4], DOWN, buff = 0.5, aligned_edge=LEFT)

        self.play(Write(ex1[:5]))
        self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeIn(ex1[5], shift = DOWN),
                GrowFromCenter(ex1[6]),
                FadeIn(ex1[7], shift = UP),
                lag_ratio = 0.2
            ),
            run_time = 2
        )
        self.wait()

        self.play(
            LaggedStart(
                Write(ex2[0]),
                TransformFromCopy(self.zv[4], ex2[1]),
                GrowFromCenter(ex2[2]),
                TransformFromCopy(self.zv[6], ex2[3]),
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait()

        self.play(Transform(ex2, ex3))

        arrow = CurvedArrow(ex1[:4].get_top() + 0.1*UP, self.histo.bars[291].get_top() + 0.1*UP, color = GREY)
        self.play(
            Circumscribe(ex3[1], color = MAROON, run_time = 2),
            Create(arrow)
        )
        self.wait(2)


        # animations for later
        exp_val_group = VGroup(ex1, ex2)
        exp_val_group.generate_target()
        exp_val_group.target.arrange(RIGHT).move_to(3.383499653*LEFT + 2*DOWN).set_color(GREY)

        self.expected_value_anims = [
            FadeOut(arrow), 
            MoveToTarget(exp_val_group)
        ]

    def signifikanzniveau(self):
        sig = Tex("Signifikanzniveau", color = YELLOW_D)
        sig.move_to(3.27460591*LEFT + 1.47982562*UP)

        five = Tex("$5\\%$", color = YELLOW_D)
        five.move_to(0.0702210139*LEFT + 1.5283935*UP)
        self.add(sig, five)
        self.wait(2)

        alpha = MathTex("\\alpha")
        equals = MathTex("=")
        zerozerofive = MathTex("0.05")

        sig_group = VGroup(alpha, equals, zerozerofive)
        sig_group.arrange(RIGHT)
        sig_group.move_to(2.5*LEFT + 1.5*UP)

        self.play(
            AnimationGroup(
                ReplacementTransform(sig, alpha), 
                GrowFromCenter(equals), 
                ReplacementTransform(five, zerozerofive), 
                lag_ratio = 0.2
            ), 
            run_time = 2
        )
        self.wait()

        eq_term = MathTex("P", "\\big(", "X", "\\leq", "g", "\\big)", "\\leq", "0.05")
        eq_term.next_to(sig_group, DOWN, aligned_edge = RIGHT)
        eq_term[3].set_color(PINK)

        sur_rect = SurroundingRectangle(eq_term, color = LIGHT_PINK, stroke_width = 2)
        self.play(FadeIn(eq_term[:6], shift = 1.5*RIGHT))
        self.wait()

        self.play(FadeIn(eq_term[6:], shift = 1.5*LEFT))
        self.play(Create(sur_rect), run_time = 2)
        self.wait()


        # sample values
        k_values = range(284,288)
        k_texs = VGroup(*[Integer(k) for k in k_values])\
            .arrange(DOWN)\
            .next_to(eq_term[4], DOWN, buff = 0.75)
        prob_texs = VGroup()
        for k, k_tex in zip(k_values, k_texs):
            prob_tex = MathTex(get_binom_cdf_result(300, 0.97, k))
            prob_tex.next_to(k_tex, RIGHT, buff = 1)
            prob_tex.align_to(eq_term[-1], LEFT)
            prob_texs.add(prob_tex)

        self.play(LaggedStartMap(FadeIn, k_texs, shift = 1.5*RIGHT, lag_ratio = 0.1), run_time = 2)
        self.wait()

        arrow = Arrow(ORIGIN, 0.75*RIGHT, buff = 0, color = TEAL, stroke_width = 2, tip_length = 0.2)
        arrow.next_to(k_texs[-1], LEFT)
        self.play(GrowArrow(arrow))


        for x, k in enumerate(k_texs):
            self.play(
                LaggedStart(*[bar.animate.set_fill(opacity = 0.60) for bar in self.bars[:13 - x]]), 
                LaggedStart(*[bar.animate.set_fill(opacity = 0.15) for bar in self.bars[13 - x:]]), 
                arrow.animate.next_to(k_texs[3 - x], LEFT)
            )
            self.play(Write(prob_texs[3 - x]))
            self.wait()

        sur_rect2 = SurroundingRectangle(prob_texs[1], color = LIGHT_PINK, stroke_width = 2)
        arrow.generate_target()
        arrow.target.next_to(k_texs[1], LEFT)

        g = eq_term[4].copy().next_to(arrow.target, LEFT)
        self.play(
            MoveToTarget(arrow),
            LaggedStart(*[k_texs[x].animate.set_color(DARK_GREY) for x in [0,2,3]]),
            LaggedStart(*[prob_texs[x].animate.set_color(DARK_GREY) for x in [0,2,3]]),
            TransformFromCopy(eq_term[4], g),
            LaggedStart(*[bar.animate.set_fill(opacity = 0.60) for bar in self.bars[:11]]),
            LaggedStart(*[bar.animate.set_fill(opacity = 0.15) for bar in self.bars[11:]]),
            Create(sur_rect2),
            run_time = 2
        )
        self.wait(2)


        arrow = Arrow(ORIGIN, RIGHT, buff = 0, color = TEAL)
        arrow.next_to(sur_rect2, RIGHT)
        self.play(GrowArrow(arrow))

        prob = MathTex("\\alpha", "=", "P", "\\big(", "X", "\\leq", "285", ")")
        prob[0].set_color(YELLOW_D)
        prob[5].set_color(PINK)
        prob.next_to(arrow, RIGHT)

        prob_back = BackgroundRectangle(prob, buff = 0.15)
        self.play(
            FadeIn(prob_back),
            Write(prob)
        )
        self.wait(0.5)

        sur_rect3 = SurroundingRectangle(prob[2:], color = LIGHT_PINK, stroke_width = 2)
        self.play(ReplacementTransform(sur_rect2.copy(), sur_rect3), run_time = 2)
        self.wait(3)

        self.remove(prob, prob_back, arrow, sur_rect3)
        self.wait()


        # animations for later
        self.significance_anims = [
            *[FadeOut(k_texs[x]) for x in [0,2,3]],
            *[FadeOut(prob_texs[x]) for x in [0,2,3]],
        ]

    def reject_set(self):

        self.play(
            # *self.fade_out_histo_stuff,
            *self.expected_value_anims,
            *self.significance_anims,
            run_time = 4
        )
        self.wait()

        set_title = Tex("Ablehnungsbereich")
        set_title.move_to(4.5*RIGHT + 1.5*UP)

        set = MathTex("\\overline{\\text{A}}", "=", "\\lbrace", "0", ",", "1", ",", "\\ldots", ",", "285", "\\rbrace")
        set[0].set_color(self.histo.bars[285].get_color())
        set.next_to(set_title, DOWN, aligned_edge=LEFT)


        self.play(Write(set_title))
        self.play(Write(set[0:3]))

        self.play(
            AnimationGroup(
                TransformFromCopy(self.histo.axes.x_labels[0], set[3]),
                Write(set[4:9]),
                TransformFromCopy(self.histo.axes.x_labels[-16], set[9]),
                Write(set[-1]),
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()



        rule_title = Tex("Entscheidungsregel").set_color(self.bars[10].get_color())
        rule_title.next_to(set_title, DOWN, aligned_edge = LEFT)
        rule_title.shift(DOWN)

        self.play(FadeIn(rule_title, shift = 2*LEFT))
        self.wait()

        rule11 = Tex("$285$", " oder weniger").next_to(rule_title, DOWN, aligned_edge = RIGHT)
        rule12 = Tex("$H_0$\\\\", " verwerfen").next_to(rule11, DOWN)
        rule12[0].set_color(RED)

        rule21 = Tex("mehr als ", "$285$").next_to(rule_title, DOWN, aligned_edge = RIGHT)
        rule22 = Tex("$H_0$\\\\", "nicht ", "verwerfen").next_to(rule21, DOWN)
        rule22[0].set_color(RED)

        self.play(Write(rule11))
        self.wait()

        self.play(
            LaggedStart(
                FadeIn(rule12[0], shift = RIGHT), 
                FadeIn(rule12[1], shift = LEFT)
            ),
            LaggedStart(*[bar.animate(rate_func = there_and_back).shift(0.25*UP) for bar in self.bars[:11]]),
            run_time = 2
        )
        self.wait() 


        self.play(
            Transform(rule11[0], rule21[1], path_arc = PI),
            Transform(rule11[1], rule21[0], path_arc = PI),
            LaggedStart(*[bar.animate.set_fill(opacity = 0.40, color = TEAL) for bar in self.bars[11:]], run_time = 2), 
            FadeToColor(rule_title, TEAL)
        )
        self.wait()
        self.play(ReplacementTransform(rule12, rule22))

        uline = Underline(rule22[1], color = YELLOW_D)
        self.play(Create(uline))
        uline.reverse_direction()
        self.play(Uncreate(uline))
        self.wait(3)

    # functions

    def get_hypo_group(self):
        hypo_info = Tex("Firmenaussage", color = LIGHT_GREY)
        hypo_label = Tex("Nullhypothese", color = RED)
        hypo = MathTex("H_0", ":", "p", "=", "0.97")
        hypo[0].set_color(hypo_label.get_color())

        hypo_group = VGroup(hypo_info, hypo_label, hypo)
        hypo_group.arrange(DOWN)

        return hypo_group

    def get_alter_group(self):
        alter_info = Tex("Gegenteil", color = LIGHT_GREY)
        alter_label = Tex("Alternative", color = GREEN)
        alter = MathTex("H_1", ":", "p", "\\neq", "0.97")
        alter[0].set_color(alter_label.get_color())

        alter_group = VGroup(alter_info, alter_label, alter)
        alter_group.arrange(DOWN)

        return alter_group


class DeviationFromEX(Scene):
    def construct(self):

        chips = VGroup(*[get_chip() for x in range(300)])
        chips.arrange_in_grid(12, 25)
        chips.set(width = config["frame_width"] - 0.5)
        chips[:150].to_edge(UP)
        chips[150:].to_edge(DOWN)

        ex_rect = SurroundingRectangle(chips[290], color = BLUE, buff = 0.05, stroke_width = 3)

        prob = MathTex("97\\%")
        total = MathTex("300").to_edge(LEFT).shift(RIGHT)

        val = ValueTracker(300)
        dec = Integer(val.get_value(), edge_to_fix = RIGHT)\
            .to_edge(RIGHT)\
            .shift(LEFT)\
            .add_updater(lambda dec: dec.set_value(val.get_value()))

        def update_chips(group):
            group[0:int(val.get_value() + 0.5)].set_fill(opacity = 1)
            group[int(val.get_value() + 0.5):].set_fill(opacity = 0.2)

        self.add(chips, prob, total, dec)
        self.wait(2)


        self.play(
            UpdateFromFunc(chips, update_chips), 
            val.animate.set_value(291), 
            run_time = 3
        )
        self.play(Create(ex_rect))
        self.wait()

        self.play(
            UpdateFromFunc(chips, update_chips, rate_func = linear), 
            val.animate(rate_func = linear).set_value(280), 
            run_time = 6
        )
        self.wait()
        self.play(
            UpdateFromFunc(chips, update_chips), 
            val.animate.set_value(285), 
            run_time = 3
        )
        self.wait(3)


class Task(Scene):
    def construct(self):
        task = Tex(
            "Eine Firma stellt Computer-Chips her und behauptet, dass \\\\97$\\%$ der Chips funktionsfähig sind.\\\\",
            "Ein Großabnehmer bestellt 300 dieser Chips und möchte mit \\\\", "einem ", "Signifikanzniveau", " von ", "$5\\%$",
            " entscheiden, ", "ob er eine \\\\ Bestellung annehmen sollte.\\\\",
            "Bestimme den ", "Ablehnungsbereich", " und formuliere \\\\die ", "Entscheidungsregel.",
            tex_environment="flushleft"
        )
        task.to_corner(UL)
        task[8:].shift(0.5*DOWN)

        self.play(FadeIn(task[0], lag_ratio = 0.1), run_time = 1.5)
        self.wait()
        self.play(FadeIn(task[1:8], lag_ratio = 0.1), run_time = 2)
        self.wait()

        self.play(Write(task[8:]))
        self.wait()

        self.play(
            FadeToColor(task[3], YELLOW_D, lag_ratio = 0.1),
            FadeToColor(task[5], YELLOW_D, lag_ratio = 0.1),
            run_time = 2
        )
        self.wait(3)


class DecisionRule(Scene):
    def construct(self):
        title = Tex("Entscheidungsregel")\
            .scale(1.25)\
            .to_corner(UL)\
            .set_color(TEAL)


        rule1 = Tex(
            "Befinden sich unter den 300 bestellten ", "genau 285 oder weniger\\\\", 
            " funktionsfähige Chips,", " so liegt eine signifikante Abweichung\\\\", 
            "vom Erwartungswert $291$ vor.", 
            tex_environment="flushleft"
        )
        rule1.next_to(title, DOWN, aligned_edge = LEFT)

        arrow1 = Arrow(ORIGIN, RIGHT, buff = 0, stroke_width = 2, color = TEAL)\
            .next_to(rule1, DOWN, aligned_edge=LEFT)\
            .shift(RIGHT)

        dec1 = Tex("Die Nullhypothese sollte verworfen,\\\\", "die Lieferung abgelehnt werden.", tex_environment="flushleft")
        dec1.next_to(arrow1, RIGHT, buff=1, aligned_edge=UL)


        rule2 = Tex(
            "Befinden sich jedoch ", "mehr als 285", " funktionsfähige Chips in \\\\der Lieferung,", 
            " so ist die Nullhypothese nicht zu verwerfen.",
            tex_environment="flushleft"
        )
        rule2.next_to(rule1, DOWN, buff=2, aligned_edge = LEFT)

        arrow2 = arrow1.copy()\
            .next_to(rule2, DOWN, aligned_edge = LEFT)\
            .shift(RIGHT)
        dec2 = Tex("In diesem Fall sollte die Lieferung \\\\angenommen werden.", tex_environment="flushleft")
        dec2.next_to(arrow2, RIGHT, buff = 1, aligned_edge = UL)


        self.add(title, rule1, arrow1, dec1)
        self.add(rule2, arrow2, dec2)

        self.play(
            LaggedStartMap(FadeIn, Group(*self.mobjects), shift = 5*LEFT, lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait(3)


        self.play(
            LaggedStartMap(FadeOut, Group(*self.mobjects), shift = 5*LEFT, lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait()


class CountIncomingChips(Scene):
    def construct(self):

        count_tex = Tex("Anzahl funktions-\\\\ fähige Chips")
        decision = Tex("Entscheidung")
        for mob, corner in zip([count_tex, decision], [UL, UR]):
            mob.scale(1.15)
            mob.to_corner(corner)
            self.add(mob)


        def update_dec(DecimalMob):
            if count_val.get_value() > 285:
                DecimalMob.set_color(X_COLOR)
            else:
                DecimalMob.set_color(C_COLOR)
            DecimalMob.set_value(count_val.get_value())

        count_val = ValueTracker(0)
        count_dec = Integer(count_val.get_value(), edge_to_fix = ORIGIN)\
            .scale(1.5)\
            .next_to(count_tex, DOWN)\
            .add_updater(update_dec)\
            .update()

        rule_block = self.get_rule_block()
        self.add(rule_block)
        self.add(count_dec)



        count_values = [290, 285, 287, 271]
        for value in count_values:
            count_val.set_value(0)
            if value > 285:
                path = FunctionGraph(lambda x:  1.75*sigmoid(4*x), x_range = [-2.5,2.5])
                outcome_text = Tex("Lieferung\\\\", "annehmen")
            else:
                path = FunctionGraph(lambda x: -1.75*sigmoid(4*x), x_range = [-2.5,2.5])
                outcome_text = Tex("Lieferung\\\\", "ablehnen")

            chip = get_chip()
            chip.move_to(path.point_from_proportion(0))
            self.play(
                FadeIn(chip, shift = 2*RIGHT, rate_func = linear), 
                count_val.animate(rate_func = squish_rate_func(smooth, 0.5, 1)).set_value(value),
            )
            self.play(Circumscribe(count_dec, color = count_dec.get_color(), time_width = 0.85, run_time = 1))

            outcome_text[1].set_color(count_dec.get_color())
            outcome_text.next_to(path.point_from_proportion(1), RIGHT, buff = 0.5)

            chip.save_state()
            def update_chip_along_path(mob, alpha):
                mob.restore()
                mob.move_to(path.point_from_proportion(alpha))
                mob.fade(alpha**4)

            self.play(
                UpdateFromAlphaFunc(chip, update_chip_along_path),
                FadeIn(outcome_text, rate_func = there_and_back_with_pause),
                run_time = 1.5
            )

        path = FunctionGraph(lambda x: -1.75*sigmoid(4*x), x_range = [-2.5,2.5], color = GREY)
        dpath = DashedVMobject(path, num_dashes = 25, color = GREY)
        chip = get_chip().move_to(path.point_from_proportion(0))
        outcome_text = Tex("Lieferung\\\\", "ablehnen").next_to(path.point_from_proportion(1), RIGHT, buff = 0.5)

        self.play(
            ShowIncreasingSubsets(dpath),
            FadeIn(chip, shift = 2*RIGHT, rate_func = linear),
            Write(outcome_text, rate_func = squish_rate_func(smooth, 0.6, 1)), 
            run_time = 3
        )
        self.wait()

        self.play(Circumscribe(count_dec, color = count_dec.get_color(), run_time = 2))
        self.wait()


        self.play(count_val.animate(rate_func = linear).set_value(280))
        self.play(count_val.animate(rate_func = linear).set_value(283), run_time = 2)
        self.play(count_val.animate(rate_func = linear).set_value(285), run_time = 2)
        self.wait()

    # functions
    def get_rule_block(self):
        rule_title = Tex("Entscheidungsregel", color = TEAL)
        rule_title.to_edge(DOWN)

        vline = Line(6*LEFT, 6*RIGHT, color = GREY)
        vline.shift(2.5*DOWN)

        rule11 = Tex("$285$", " oder weniger").next_to(rule_title, LEFT, buff = 1.00, aligned_edge = UP).shift(0.35*UP)
        rule12 = Tex("$H_0$", " verwerfen").next_to(rule11, DOWN, aligned_edge = UP)
        rule12[0].set_color(RED)

        rule21 = Tex("mehr als ", "$285$").next_to(rule_title, RIGHT, buff = 1.35, aligned_edge = UP).shift(0.35*UP)
        rule22 = Tex("$H_0$", " nicht verwefen").next_to(rule21, DOWN, aligned_edge = UP)
        rule22[0].set_color(RED)

        rule_group = VGroup(vline, rule_title, rule11, rule12, rule21, rule22)
        rule_group.add_background_rectangle(opacity = 0.85, buff = 0.1)

        return rule_group


class WhatIf(MovingCameraScene):
    def construct(self):


        chips = VGroup(*[get_chip() for x in range(2700)])
        chips.arrange_in_grid(36, 75)
        chips.set(width = 3*(config["frame_width"] - 0.5))

        self.add(chips)


        rule_title = Tex("Entscheidungsregel", color = TEAL)
        rule_title.to_edge(DOWN)

        vline = Line(6*LEFT, 6*RIGHT, color = GREY)
        vline.shift(2.5*DOWN)


        rule11 = Tex("$285$", " oder weniger").next_to(rule_title, LEFT, buff = 1.00, aligned_edge = UP).shift(0.35*UP)
        rule12 = Tex("$H_0$", " verwerfen").next_to(rule11, DOWN, aligned_edge = UP)
        rule12[0].set_color(RED)

        rule21 = Tex("mehr als ", "$285$").next_to(rule_title, RIGHT, buff = 1.35, aligned_edge = UP).shift(0.35*UP)
        rule22 = Tex("$H_0$", " nicht verwefen").next_to(rule21, DOWN, aligned_edge = UP)
        rule22[0].set_color(RED)

        rule_group = VGroup(vline, rule_title, rule11, rule12, rule21, rule22)
        rule_group.add_background_rectangle(opacity = 0.85, buff = 0.1)

        self.add(rule_group[0], rule_group[1:])
        self.wait()


        # self.renderer.camera.frame.scale(3)
        self.play(
            self.renderer.camera.frame.animate(rate_func = linear).scale(3),
            run_time = 15
        )
        self.wait()


class AlphaError(HistoScene):
    def construct(self):

        self.build_table()
        self.connect_to_reject_set()

    def build_table(self):

        title_up = Tex("In der Grundgesamtheit gilt die")
        header = VGroup(*[Tex(*tex) for tex in [["Nullhypothese ", "$H_0$"], ["Alternative ", "$H_1$"]]])
        header.arrange(RIGHT, buff = 1)
        header.next_to(title_up, DOWN)
        for tex in header:
            tex.set_color_by_tex_to_color_map({"$H_0$": X_COLOR, "$H_1$": C_COLOR})

        title_left = Tex("Entscheidung aufgrund \\\\der Stichprobe")\
            .rotate(90*DEGREES)\
            .next_to(header, DOWN)\
            .shift(8*LEFT)

        lefties = VGroup(*[Tex(*tex) for tex in [["$H_0$\\\\", "(", "$H_0$", " nicht verwerfen)"], ["$H_1$\\\\", "(", "$H_0$", " verwerfen)"]]])
        for tex in lefties:
            tex[1:].scale(0.5)
            tex.set_color_by_tex_to_color_map({"$H_0$": X_COLOR, "$H_1$": C_COLOR})

        lefties.arrange(DOWN, buff = 1.5)
        lefties.next_to(title_left, RIGHT, buff = 0.5)


        table = VGroup(title_up, header, title_left, lefties)
        table.center()

        def update_dec(DecimalMob):
            if count_val.get_value() > 285:
                DecimalMob.set_color(X_COLOR)
            else:
                DecimalMob.set_color(C_COLOR)
            DecimalMob.set_value(count_val.get_value())

        count_val = self.count_val = ValueTracker(0)
        count_dec = Integer(count_val.get_value(), edge_to_fix = ORIGIN)\
            .scale(1.5)\
            .next_to(title_left, UP)\
            .to_edge(UP)\
            .add_updater(update_dec)\
            .update()

        # Grundgesamtheit und Nullhypothese
        self.play(FadeIn(title_up, lag_ratio = 0.1), run_time = 2)
        self.wait()
        self.play(Write(header[0]))
        self.wait()

        arrow = Arrow(ORIGIN, DOWN, buff = 0 , color = TEAL)
        arrow.next_to(header[0], DOWN)
        statement = MathTex("p", "=", "0.97")
        statement.next_to(arrow, DOWN)
        self.play(GrowArrow(arrow))
        self.play(FadeIn(statement, shift = 2*LEFT))
        self.wait()

        self.play(
            FadeOut(statement, shift = 2*LEFT), 
            FadeOut(arrow, shift = 2*RIGHT)
        )
        self.wait()

        # Stichprobe und H_0
        self.add(count_dec)
        self.play(
            FadeIn(title_left, shift = RIGHT, lag_ratio = 0.1),
            count_val.animate.set_value(290),
            run_time = 2
        )
        self.play(Circumscribe(count_dec, color = count_dec.get_color(), time_width = 0.75, run_time = 2))
        self.wait()

        self.play(Write(lefties[0]), run_time = 0.75)
        self.wait()

        # Create check for H_0 / H_0
        check = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        check.scale(2.5)
        check.next_to(header[0], DOWN)
        check.set_y(lefties[0].get_y())

        check_c1 = check.copy()#.move_to(header[0])
        check_c2 = check.copy()#.move_to(lefties[0])

        self.play(
            FadeIn(check_c1, target_position=header[0]),
            FadeIn(check_c2, target_position=lefties[0]),
            run_time = 2.5
        )
        self.remove(check_c1, check_c2)
        self.add(check)
        self.wait(2)


        # Stichprobe und H_1 aus H_0 transformieren
        self.play(count_val.animate.set_value(283))
        self.play(
            AnimationGroup(
                TransformFromCopy(lefties[0][0], lefties[1][0]), 
                TransformFromCopy(lefties[0][1:], lefties[1][1:]),
                lag_ratio = 0.2
            ),
            run_time = 2
        )
        self.play(Circumscribe(count_dec, color = count_dec.get_color(), time_width = 0.75, run_time = 2))
        self.wait()

        # Create Cross for H_0 / H_1
        cross = Tex(XMARK_TEX, color = YELLOW_D, tex_template = myTemplate)
        cross.scale(2.5)
        cross.next_to(header[0], DOWN)
        cross.set_y(lefties[1:].get_y())

        self.play(GrowFromCenter(cross), run_time = 2)
        self.wait()

        uline = Underline(header[0], color = RED)
        self.play(Create(uline))
        uline.reverse_direction()
        self.play(Uncreate(uline))
        self.wait()

        # name error 
        name1 = Tex("$\\alpha-$", "Fehler", color = YELLOW_D).next_to(cross, DOWN)
        name2 = Tex("Fehler ", "1. Art", color = YELLOW_D).next_to(cross, DOWN)

        self.play(Write(name1))
        self.wait()
        self.play(Transform(name1, name2))
        self.wait(3)

        # ask for prob
        carrow = CurvedArrow(name1.get_corner(UR) + 0.1*UR, name1.get_corner(UR) + 2.5*RIGHT + 2*UP, color = GREY, angle = 60*DEGREES)
        question = Tex("Wie wahrscheinlich\\\\ ist das denn bitte?").next_to(carrow.get_end(), UP)

        self.play(Create(carrow))
        self.play(Write(question))
        self.wait(2)

        self.play(
            FadeOut(question, shift = 3*RIGHT), 
            FadeOut(carrow),
        )
        self.wait(0.5)

        self.error_name, self.header, self.lefties, self.cross = name1, header, lefties, cross

    def connect_to_reject_set(self):
        set_title = Tex("Ablehnungsbereich")
        set_title.next_to(self.error_name, RIGHT, buff = 1)

        set = MathTex("\\overline{\\text{A}}", "=", "\\lbrace", "0", ",", "1", ",", "\\ldots", ",", "285", "\\rbrace")
        set[0].set_color(YELLOW_D)
        set.next_to(set_title, UP, aligned_edge=LEFT)

        self.play(Write(set_title))
        self.wait()

        self.count_val.set_value(0)
        self.play(self.count_val.animate.set_value(285), run_time = 4)
        self.play(Write(set))
        self.wait()


        # histogram stuff
        histo_kwargs = {
            "width": config["frame_width"] / 3, "height": config["frame_height"] / 4,
            "x_tick_freq": 20, "x_label_freq": 20, "y_max_value": 0.15, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }

        n, p = 300, 0.97
        histo0 = self.get_histogram(n, p, zeros = True, **histo_kwargs)
        histo = self.histo = self.get_histogram(n, p, **histo_kwargs)
        for hist in histo0, histo:
            hist.center()
            hist.to_edge(RIGHT)

        bars0 = histo0.bars[275:]
        bars = histo.bars[275:]

        for bar_group in bars0, bars:
            bar_group.stretch_to_fit_width(config["frame_width"] / 3).stretch_to_fit_height(config["frame_height"] / 3).set_x(4.25).shift(0.5*UP)
            bar_group[:11].set_fill(color = YELLOW_D, opacity = 0.6)
            bar_group[11:].set_fill(color = C_COLOR, opacity = 0.6)

        bars0.move_to(bars.get_bottom())

        new_x_axis = Line(bars[0].get_corner(DL) + 1.1*LEFT, bars[-1].get_corner(DR), stroke_width = 2, color = WHITE)
        new_x_labels = VGroup()
        for x, bar in zip([275, 280, 285, 290, 295, 300], bars[::5]):
            label = MathTex(str(x)).scale(0.75)
            label.next_to(bar, DOWN)
            new_x_labels.add(label)

        self.play(
            Create(new_x_axis), 
            LaggedStartMap(FadeIn, new_x_labels),
            run_time = 2
        )
        self.play(ReplacementTransform(bars0[10], bars[10]), run_time = 2)
        self.wait()

        self.play(ReplacementTransform(bars0[9], bars[9]), run_time = 2)
        self.wait()

        self.play(
            LaggedStart(*[ReplacementTransform(bars0[k], bars[k]) for k in reversed(range(9))]),
            run_time = 4
        )
        self.wait()

        # brace and prob
        zero_til = MathTex("0", "\\ldots")\
            .match_height(new_x_labels[0])\
            .next_to(new_x_labels[0], LEFT)

        self.play(Write(zero_til))
        self.wait()

        brace_line = Line(new_x_axis.get_left(), bars[10].get_corner(DR))
        brace = Brace(brace_line, UP, buff = 0.55, color = GREY)

        prob = MathTex("\\alpha", "=", "P", "\\big(", "X", "\\leq", "285", ")", "=")
        prob[0].set_color(YELLOW_D)
        prob[5].set_color(PINK)
        prob.next_to(brace, UP)
        prob.shift(RIGHT)

        self.play(
            Create(brace),
            FadeIn(prob[0], shift=DOWN)
        )
        self.play(Write(prob[1:8]))
        sur_rect = SurroundingRectangle(prob[:8], LIGHT_PINK)
        brain = SVGMobject(SVG_DIR + "BrainBulb")\
            .scale(0.65)\
            .next_to(prob, UP)

        brain_text = Tex("clever \\\\sein")\
            .scale(0.65)\
            .next_to(brain, RIGHT)

        self.play(Create(sur_rect), run_time = 2)
        self.wait()

        self.play(
            Create(brain),
            Write(brain_text, rate_func = squish_rate_func(smooth, 0.5, 1)),
            run_time = 2
        )
        self.wait(3)
        self.remove(sur_rect)
        self.add(prob[-1])
        self.wait(2)


        alpha_result = MathTex(str(get_binom_cdf_result(300, 0.97, 285)))
        alpha_result.next_to(prob, RIGHT)

        uline_group = [self.header[0], self.lefties[1][1:], self.cross, alpha_result]
        for mob, ucolor in zip(uline_group, [RED, RED, YELLOW_D, YELLOW_D]):
            if mob is alpha_result:
                self.play(FadeIn(alpha_result, shift = 2*LEFT))

            uline = Underline(mob, color = ucolor)
            self.play(Create(uline), run_time = 1.5)
            uline.reverse_direction()
            self.play(Uncreate(uline), run_time = 1.5)
            self.wait(0.5)

        self.wait(3)


class Thumbnail(HistoScene):
    def construct(self):
        chips = VGroup(*[get_chip().set_opacity(0.15) for x in range(28)])
        chips.arrange_in_grid(4,7)
        chips.set(height = config["frame_height"] - 0.5)


        title1 = Tex("Fehler 1. Art", color = YELLOW)\
            .scale(2.75)\
            .to_edge(UP)\
            .add_background_rectangle(buff = 0.15)

        title2 = Tex("$\\alpha$", "-", "Fehler")\
            .scale(1.5)\
            .next_to(title1, DOWN, buff = 0.1)\
            .add_background_rectangle(buff = 0.15)


        # Histo
        histo_kwargs = {
            "width": config["frame_width"] / 3, "height": config["frame_height"] / 2,
            "x_tick_freq": 20, "x_label_freq": 20, "y_max_value": 0.15, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False, "include_x_labels": True,
        }
        n, p = 300, 0.97
        histo = self.get_histogram(n,p, **histo_kwargs)
        histo.to_edge(DOWN, buff = 1)


        bars = histo.bars[275:]
        bars.stretch_to_fit_width(9).set_x(0)

        ticks = VGroup()
        for bar in bars:
            tick = Line(UP, DOWN, stroke_width = 2)
            tick.set_length(0.2)
            tick.move_to(bar.get_corner(DR))
            ticks.add(tick)

        new_x_axis = Line(histo.axes.c2p(0,0), ticks[-1].get_center(), stroke_width = 2)
        new_x_labels = VGroup()
        for x, bar in zip([275, 280, 285, 290, 295, 300], bars[::5]):
            label = MathTex(str(x)).scale(0.75)
            label.next_to(bar, DOWN)
            new_x_labels.add(label)

        bars[11:].set_fill(color = BLUE, opacity = 0.75)
        bars[:11].set_fill(color = YELLOW, opacity = 0.75)


        # Text on Screen
        cc = Tex("Computerchips")\
            .set(height = new_x_labels.height)\
            .next_to(new_x_labels, RIGHT)

        annahme = Tex("Annahme-\\\\bereich")\
            .set_color(BLUE)\
            .next_to(bars, RIGHT)\
            .shift(LEFT)\
            .add_background_rectangle(buff = 0.1)


        formula = MathTex("\\alpha", "=", "P", "\\big(", "X", "\\leq", "285", "\\big)")\
            .set_color_by_tex_to_color_map({"\\alpha": YELLOW, "\\leq": PINK})\
            .scale(1.5)\
            .move_to(3*LEFT)\
            .add_background_rectangle(buff = 0.15)

        brace = Brace(bars[:11], UP, color = YELLOW_B)

        path1 = VMobject()
        path1.set_points_smoothly([
            title1.get_right(),
            title1.get_right() + 1.5*RIGHT,
            title1.get_right() + RIGHT + DOWN,
            3*LEFT + 2*UP, 
            formula[1].get_center(),
            brace.get_top()
        ])
        path1.set_color([YELLOW, BLUE, BLUE, YELLOW])



        self.add(chips, path1, title1, title2)
        self.add(bars, ticks, new_x_axis, new_x_labels, cc, annahme)
        self.add(formula)
        self.add(brace)
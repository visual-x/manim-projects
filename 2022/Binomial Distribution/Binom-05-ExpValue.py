from manim import *
from BinomHelpers import *



class Shooting(Scene):
    def construct(self):
        couple = SVGMobject(SVG_DIR + "emoji_couple_holding_hands")\
            .set(height = 3)

        shooting_area = Tex("Schießstand", font_size = 72)\
            .to_edge(LEFT)\
            .shift(2*UP)\
            .set_color_by_gradient(MAROON, PURPLE, PINK, RED)\
            .set_fill(WHITE, opacity = 0.25)\
            .set_stroke(width = 2)

        rose = SVGMobject(SVG_DIR + "rose_illustration")\
            .set(height = 4)\
            .to_edge(UP)\
            .shift(0.073*LEFT)

        # couples move to shooting area to shoot roses
        self.play(DrawBorderThenFill(couple))
        self.wait()
        self.play(couple.animate(rate_func = linear).shift(4.5*LEFT), run_time = 4)
        self.play(
            couple.animate(rate_func = linear, run_time = 2).shift(2.25*LEFT), 
            FadeIn(shooting_area, shift = 3*LEFT, run_time = 1),
        )
        self.play(
            couple.animate(rate_func = linear, run_time = 2).shift(2.25*LEFT), 
            FadeOut(shooting_area, shift = 3*LEFT, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)), 
            Create(rose)
        )
        self.wait()

        # 10 out of 10???
        bools1 = 10 * [True]
        bools2 = 2 * [True] + [False] + 7 * [True]
        cac1 = get_checks_and_crosses(bools1, width = 10).shift(DOWN)
        cac2 = get_checks_and_crosses(bools2, width = 10).shift(DOWN)
        underlines = VGroup(*[Underline(sym).set_y(-1.6) for sym in cac1])
        self.play(
            AnimationGroup(
                ShowIncreasingSubsets(underlines), 
                FadeIn(cac1, shift = 0.5*DOWN, lag_ratio = 0.1),
                lag_ratio = 0.2
            ),
            run_time = 2.5
        )
        self.wait()
        self.play(Transform(cac1, cac2), run_time = 1.5)
        self.wait()

        # # probabaility stuff
        p_line =  NumberLine(x_range = [0, 1, 0.2], length = 8, include_numbers=True)
        p_line.shift(2.5*DOWN)

        p_title = Tex("Erfolgswahrscheinlichkeit ", "$p$").next_to(p_line, UP, buff = 0.1)
        p_title[0].set_color_by_gradient(GREEN, GREY_A, GREEN)
        p_title[-1].set_color(GREEN)

        p_val = ValueTracker(0.8)
        p_dot = Dot(point = p_line.n2p(p_val.get_value()), radius = 0.1, color = YELLOW)
        p_dot.set_sheen(-0.5, DR)

        self.play(
            ShrinkToCenter(underlines, lag_ratio = 0.1, run_time = 1), 
            ShrinkToCenter(cac1, lag_ratio = 0.1, run_time = 1), 
            Create(p_line, run_time = 3), 
            Write(p_title, rate_func = squish_rate_func(smooth, 0.6, 1), run_time = 3), 
            FadeIn(p_dot, shift = UP, rate_func = squish_rate_func(smooth, 0.6, 1), run_time = 3)
        )
        self.wait()

        # fadenkreuz
        r_val = ValueTracker(0.25)
        curve = always_redraw(lambda: ParametricFunction(
            lambda t: self.infinity_func(r_val.get_value(), t), t_range = [0, TAU], fill_opacity = 0, stroke_opacity = 0
        ))
        self.add(curve)


        fk_path = VMobject()
        fk_path.set_points_smoothly([
            5*RIGHT, 
            4*RIGHT + 3*UP, 
            2*RIGHT + DOWN, 
            curve.point_from_proportion(0)
        ])
        fk = self.get_fadenkreuz().scale(0.5)
        fk.move_to(fk_path.get_start())

        self.play(Create(fk))
        self.wait()
        self.play(MoveAlongPath(fk, fk_path), run_time = 3)


        # move fk along infinity curve as dt updater
        p_dot.add_updater(lambda dot: dot.move_to(p_line.n2p(p_val.get_value())))
        self.t_offset = 0
        def move_along_infinity(mob, dt):
            rate = dt * 0.3
            mob.move_to(curve.point_from_proportion((self.t_offset + rate) % 1))
            self.t_offset += rate
        fk.add_updater(move_along_infinity)
        self.wait(3)

        self.play(
            r_val.animate.set_value(1),
            p_val.animate.set_value(0.2),
            run_time = 6
        )
        self.wait(6)


    # functions
    def infinity_func(self, r, t):
        curve = np.array([ r * np.cos(t), r * np.sin(2* t) / 2, 0 ])
        return curve

    def get_fadenkreuz(self):
        circles = VGroup(*[
            Circle(radius = r, color = c, stroke_width = w) for r, c, w in zip(
                [0.75, 1.5, 1.7], [RED_A, GREY, WHITE], [3, 1, 3]
            )
        ])

        cross_lines = VGroup()
        for x in range(4):
            line = Line(0.5*RIGHT, 2*RIGHT, stroke_width = 1.5)
            line.rotate(45*DEGREES + x * 90*DEGREES, about_point = ORIGIN)
            cross_lines.add(line)

        dot = Dot(radius = 0.12, color = RED)

        fk = VGroup(circles, cross_lines, dot)
        return fk


class LookingForAverage(Scene):
    def construct(self):


        self.possible_vs_most_likely()
        self.simulate()

    def possible_vs_most_likely(self):
        possible = Tex("mögliche\\\\Ergebnisse")\
            .to_corner(UL)
        s_numbers = VGroup(*[MathTex(str(num)) for num in range(11)])
        s_numbers.arrange(RIGHT, buff = 0.75)
        s_numbers.next_to(possible, RIGHT, buff = 0.5)

        def get_pile_of_roses(num):
            roses = VGroup()
            for x in range(num):
                rose = SVGMobject(SVG_DIR + "rose_illustration")
                rose.set_stroke(width = 2)
                rose.set(height = 0.3)
                roses.add(rose)
            roses.arrange(DOWN)
            return roses

        piles_of_roses = VGroup(*[get_pile_of_roses(num) for num in range(11)])
        for s_number, pile in zip(s_numbers, piles_of_roses):
            pile.next_to(s_number, DOWN)

        self.add(possible)
        self.play(
            LaggedStartMap(FadeIn, s_numbers, shift = 0.5*DOWN, lag_ratio = 0.1), 
            AnimationGroup(
                *[GrowFromEdge(pile, UP) for pile in piles_of_roses], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait()

        column_rects = VGroup()
        for x in range(len(s_numbers)):
            column = VGroup(s_numbers[x], piles_of_roses[x])
            rect = SurroundingRectangle(column, color = BLUE, stroke_width = 2)
            column_rects.add(rect)

        self.play(
            LaggedStartMap(
                ShowCreationThenFadeOut, column_rects, run_time = 4, lag_ratio = 0.2
            ),
        )
        self.wait()

        self.play(
            AnimationGroup(
                *[GrowFromEdge(pile, UP, rate_func = lambda t: smooth(1-t)) for pile in piles_of_roses], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(LaggedStartMap(Indicate, s_numbers, color = YELLOW_D, lag_ratio = 0.1), run_time = 3)
        self.wait()


        self.top_group = VGroup(possible, s_numbers)

    def simulate(self):
        decimals = VGroup()
        for num in range(10):
            dec = DecimalNumber()
            decimals.add(dec)

        def randomize_decimals(decimals):
            for dec in decimals:
                value = random.random()
                dec.set_value(value)
                dec.value = value
                if value > 0.2:
                    dec.set_color(GREY_B)
                else:
                    dec.set_color(C_COLOR)
        randomize_decimals(decimals)

        decimals.set(height = 0.3)
        decimals.arrange(RIGHT, buff = 0.25)
        decimals[0].set_value(0.42)
        decimals[0].set_color(GREY_B)
        decimals[1].set_value(0.14)
        decimals[1].set_color(C_COLOR)

        label_rn = Tex("Zufallszahl\\\\ aus [0, 1]", font_size = 30)\
            .next_to(decimals[0], DOWN)\
            .set_color(GREY_B)

        gt = MathTex(">", "0.2")\
            .set(height = 0.3)\
            .set_color(X_COLOR)\
            .next_to(decimals[0], RIGHT)

        lt = MathTex("\\leq", "0.2")\
            .set(height = 0.3)\
            .set_color(C_COLOR)\
            .next_to(decimals[1], RIGHT)

        arrows = VGroup(*[Vector(0.4 * UP).next_to(dec, UP) for dec in decimals])

        def get_cx_marks(decimals, arrows):
            cx_marks = VGroup()
            for dec, arrow in zip(decimals, arrows):
                value = dec.get_value()
                if value < 0.2:
                    mark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
                else:
                    mark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
                mark.next_to(arrow, UP)
                mark.value = value
                cx_marks.add(mark)
            return cx_marks
        cx_marks = get_cx_marks(decimals, arrows)

        # show first pile of mark, number, label
        self.play(Write(label_rn))
        self.play(FadeIn(decimals[0], shift = UP), run_time = 1.5)
        self.wait(0.5)
        self.play(FadeIn(gt, shift = RIGHT))
        self.wait(0.5)
        self.play(
            GrowArrow(arrows[0]), 
            FadeIn(cx_marks[0], target_position=decimals[0]), 
            run_time = 2
        )
        self.wait()

        # show second pile 
        self.play(
            AnimationGroup(
                FadeTransform(gt, lt), 
                label_rn.animate.next_to(decimals[1], DOWN),
                lag_ratio = 0.2
            ),
            run_time = 2
        )
        self.play(FadeIn(decimals[1], shift = UP), run_time = 1.5)
        self.play(
            GrowArrow(arrows[1]), 
            FadeIn(cx_marks[1], target_position=decimals[1]), 
            run_time = 2
        )
        self.wait()

        # complete first row
        self.play(
            FadeOut(lt, shift = 2*DOWN), 
            FadeOut(label_rn, shift = 2*DOWN),
            LaggedStartMap(FadeIn, decimals[2:], shift = 2*UP, lag_ratio = 0.05), 
            run_time = 2
        )
        self.play(
            LaggedStartMap(GrowArrow, arrows[2:], lag_ratio = 0.05), 
            LaggedStartMap(FadeIn, cx_marks[2:], shift = UP),
        )
        self.wait()


        # generate next three rows
        rows = VGroup(cx_marks)
        for x in range(3):
            self.play(
                arrows.animate.shift(DOWN),
                decimals.animate.shift(DOWN),
                UpdateFromFunc(decimals, randomize_decimals)
            )
            new_cx_marks = get_cx_marks(decimals, arrows)
            self.play(FadeIn(new_cx_marks, lag_ratio = 0.1))
            self.wait(0.5)

            rows.add(new_cx_marks)


        # Create a stockpile of new rows
        added_rows = VGroup()
        decimals.clear_updaters()
        decimals.save_state()
        for x in range(80):
            randomize_decimals(decimals)
            added_rows.add(get_cx_marks(decimals, arrows))
        decimals.restore()


        # Compress rows
        rows.generate_target()
        for group in rows.target, added_rows:
            group.scale(0.3)
            for row in group:
                row.arrange(RIGHT, buff=SMALL_BUFF)
            group.arrange(DOWN, buff=0.2)
        rows.target.set_y( 3.0)
        rows.target.set_x(-4.5)


        self.play(
            MoveToTarget(rows),
            FadeOut(self.top_group, shift = 2*UP),
            FadeOut(decimals),
            FadeOut(arrows),
            run_time = 2
        )
        self.wait(0.5)


        nr = 20
        added_rows[:nr].move_to(rows.target, UP)
        added_rows[nr:2 * nr].move_to(rows.target, UP)
        added_rows[nr:2 * nr].shift(3 * RIGHT)
        added_rows[2 * nr:3 * nr].move_to(rows.target, UP)
        added_rows[2 * nr:3 * nr].shift(6 * RIGHT)
        added_rows[3 * nr:4 * nr].move_to(rows.target, UP)
        added_rows[3 * nr:4 * nr].shift(9 * RIGHT)
        added_rows = added_rows[4:4 * nr]

        self.play(ShowIncreasingSubsets(added_rows), run_time = 3)
        self.wait()

        # Scores
        all_rows = VGroup(*rows, *added_rows)
        scores = VGroup()
        twos = VGroup()
        twos_counter = 0
        for row in all_rows:
            score = Integer(sum([
                mark.value < 0.2
                for mark in row
            ]))
            score.match_height(row)
            score.next_to(row, RIGHT)

            if score.get_value() == 2:
                twos_counter += 1
                score.set_color(YELLOW)
                twos.add(SurroundingRectangle(score))
            scores.add(score)

        self.play(ShowIncreasingSubsets(scores), run_time = 4)
        self.play(LaggedStartMap(FadeIn, twos, lag_ratio = 0.1), run_time = 5)
        self.wait()

        twos_val = ValueTracker(0)
        num_of_twos = Integer(twos_val.get_value(), edge_to_fix = RIGHT)\
            .scale(1.5)\
            .add_updater(lambda dec: dec.set_value(twos_val.get_value()))
        out_of_80 = Tex("von $80$").scale(1.5).next_to(num_of_twos, RIGHT, aligned_edge=UP)
        proportion = VGroup(num_of_twos, out_of_80)\
            .to_edge(DOWN)\
            .shift(LEFT)

        print(proportion.get_right())

        self.play(FadeIn(num_of_twos, shift = UP))
        self.play(
            twos_val.animate(run_time = 2).set_value(twos_counter),
            Write(proportion[1])
        )
        self.play(LaggedStartMap(FadeOut, twos, lag_ratio = 0.1), run_time = 2)
        self.wait()


        self.play(
            LaggedStartMap(FadeOut, all_rows, shift = DOWN, lag_ratio=0.01),
            ShrinkToCenter(scores, rate_func = running_start),
            run_time = 2
        )
        self.wait()


class HistogramConnection(HistoScene):
    def construct(self):
        self.n = 10
        self.p = 0.2
        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 4,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.32, "y_tick_num": 4,
            "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }

        self.empirical_probability()
        self.binomial_probability()


    def empirical_probability(self):
        result = Tex("$28$", " von ", "$80$")\
            .scale(1.5)\
            .next_to(1.54253944*RIGHT + 3.2429639 * DOWN, LEFT, buff = 0)

        result.generate_target()
        result.target.to_edge(UP, buff = 0.5)

        roses = VGroup(*[SVGMobject(SVG_DIR + "rose_illustration").set(height = 1).set_stroke(width = 1) for x in range(2)])
        roses.arrange(RIGHT, buff = 0.1)
        roses.next_to(result.target, LEFT, buff = 1)

        histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(DOWN)

        possible = Tex("mögliche\\\\ Ergebnisse")\
            .next_to(histo.axes.x_labels, UP, buff = 1)

        self.add(result)
        self.play(
            MoveToTarget(result), 
            FadeIn(roses, shift = 2*RIGHT, lag_ratio = 0.1),
            FadeIn(histo.axes.x_labels, shift = UP, lag_ratio = 0.1, rate_func = squish_rate_func(smooth, 0.3, 1)),
            GrowFromCenter(possible, rate_func = squish_rate_func(smooth, 0.6, 1)),
            run_time = 2
        )
        self.wait()

        roses_copy = roses.copy()
        self.play(FadeOut(roses_copy, scale = 0.25, target_position = histo.axes.x_labels[2]), run_time = 2)
        self.wait()

        # relative
        rel = MathTex("{28", "\\over", "80}", "=", "35", "\\%")
        rel.scale(1.5)
        rel.next_to(result, DOWN)
        rel.shift(4.5*RIGHT)
        rel[-2].set_fill(opacity = 0).set_stroke(width = 0)

        rel_title = Tex("relative Häufigkeit")\
            .set_color(TEAL)\
            .match_width(rel)\
            .next_to(rel, UP)

        self.play(
            Write(rel_title, run_time = 1),
            AnimationGroup(
                FadeTransform(result[-1].copy(), rel[2]),
                Write(rel[1]),
                FadeTransform(result[0].copy(), rel[0]),
                lag_ratio = 0.2,
                run_time = 2
            )
        )
        self.play(Write(rel[3]))
        self.wait()

        rel_val = ValueTracker(0)
        rel_dec = DecimalNumber(rel_val.get_value(), num_decimal_places=0, edge_to_fix=RIGHT)
        rel_dec.scale(1.5)
        rel_dec.next_to(rel[-1], LEFT, buff = 0.1)
        rel_dec.add_updater(lambda dec: dec.set_value(rel_val.get_value()))


        ref_bar = histo.bars[2]
        rect = Rectangle()
        rect.match_style(ref_bar)
        rect.match_width(ref_bar)
        rect.stretch_to_fit_height(0.35*histo.axes.y_axis.unit_size)
        rect.next_to(ref_bar.get_bottom(), UP, buff = 0)

        rect0 = rect.copy()
        rect0.stretch_to_fit_height(0)
        rect0.next_to(ref_bar.get_bottom(), UP, buff = 0)

        self.add(rel_dec)
        self.play(
            rel_val.animate(run_time = 4).set_value(35),
            FadeOut(possible, run_time = 1),
            Create(rel[-1], rate_func = squish_rate_func(smooth, 0.65, 1), run_time = 2.5),
            Create(histo.axes.x_axis, run_time = 2.5), 
            Create(histo.axes.y_axis, run_time = 2.5),
            *[GrowFromCenter(hline, run_time = 2.5) for hline in histo.axes.h_lines],
            ReplacementTransform(rect0, rect, run_time = 4),
        )
        self.wait()


        self.rel_title = rel_title
        self.rel_group = VGroup(rel, rel_dec)
        self.histo, self.rect, self.result, self.roses = histo, rect, result, roses

    def binomial_probability(self):
        histo, rect, result, roses = self.histo, self.rect, self.result, self.roses

        formula = get_binom_formula(self.n, self.p, 2)\
            .next_to(self.result, DOWN)\
            .shift(2.5*LEFT)

        bin_title = Tex("Bernoulli$-$Formel")\
            .match_height(self.rel_title)\
            .match_color(self.rel_title)\
            .match_y(self.rel_title)\
            .match_x(formula, LEFT)

        bin_result = MathTex("\\approx", str(get_binom_result(self.n, self.p, 2)))\
            .next_to(formula, RIGHT, buff = 0.1)

        self.play(
            FadeOut(roses, shift = UP), 
            FadeOut(result, shift = UP),
            run_time = 2
        )
        self.play(
            Write(bin_title),
            self.rel_group.animate.scale(2/3).next_to(self.rel_title, DOWN, aligned_edge = RIGHT),
            run_time = 2
        )
        self.play(Write(formula[:6]))                               # P(X = 2)
        self.wait()
        self.play(FadeIn(formula[6], shift = 0.75*UP))              # =
        self.wait()
        self.play(Write(formula[7:11]))                             # n choose k
        self.wait()
        self.play(FadeIn(formula[11], shift = 0.75*UP))             # cdot
        self.play(Write(formula[12]))                               # p
        self.wait(0.5)
        self.play(FadeIn(formula[13], shift = 0.75*LEFT))           # ^k
        self.wait()
        self.play(FadeIn(formula[14]), shift = 0.75*UP)             # cdot
        self.play(Write(formula[15:]))                              # (1-p)^k
        self.wait()

        self.play(Flash(formula[20], color = RED, run_time = 2))
        self.wait()


        self.play(Circumscribe(formula, color = BLUE, fade_out = True, stroke_width = 2, run_time = 3))
        self.play(FadeIn(bin_result, shift = UP))
        self.play(ReplacementTransform(rect, histo.bars[2]), run_time = 4)
        self.wait()


        histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        histo_0.to_edge(DOWN)

        self.play(
            AnimationGroup(
                *[ReplacementTransform(bars1, bars2, rate_func = rush_into) for bars1, bars2 in zip(histo_0.bars, histo.bars)], 
                lag_ratio = 0.1
            ),
            run_time = 8
        )
        self.wait()


class ExpectedValueMeansHighestProb(HistoScene):
    def construct(self):
        self.n = 10
        self.p = 0.2
        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 4,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.32, "y_tick_num": 4,
            "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }

        self.setup_old_scene()

    def setup_old_scene(self):
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(DOWN)

        self.add(histo)
        self.wait()

        title = Tex("Erwartungswert", font_size = 72).to_edge(UP)
        uline = Underline(title, color = GREY)

        ex = MathTex("E[X]", "=", font_size = 72)
        ex_val = ValueTracker(self.n * self.p)
        ex_dec = Integer(ex_val.get_value())\
            .scale(1.5)\
            .next_to(ex, RIGHT)\
            .add_updater(lambda dec: dec.set_value(ex_val.get_value()))

        ex_group = VGroup(ex, ex_dec)
        ex_group.next_to(title, DOWN, buff = 0.5)


        n = MathTex("n", "=", "10")
        p = MathTex("p", "=", )
        np_group = VGroup(n, p)
        np_group.arrange(DOWN, buff = 0.5, aligned_edge = LEFT)
        np_group.to_corner(UL)

        p_dec = DecimalNumber(0.2).next_to(p, RIGHT).shift(0.05*UP)
        np_group.add(p_dec)



        self.play(
            AnimationGroup(
                Create(uline), 
                Write(title),
                FadeIn(np_group),
                lag_ratio = 0.25
            ),
            run_time = 2
        )
        self.play(FadeIn(ex_group))
        self.play(
            Circumscribe(ex_dec, color = PINK, time_width = 0.5, stroke_width = 3),
            Circumscribe(histo.axes.x_labels[2], color = PINK, time_width = 0.5, stroke_width = 4), 
        )
        self.wait()


        p_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        # Verschiedene Histogramme nacheinander zeigen
        # Bei jedem höchsten Wahrscheinlichkeit kennzeichnen --> highlight_single_bar
        for value, x in zip(p_values, range(3,9)):
            new_histo = self.get_histogram(self.n, value, **self.histo_kwargs).to_edge(DOWN)
            new_ex = self.n * value

            histo.become(new_histo)
            ex_val.set_value(new_ex)
            p_dec.set_value(value)
            self.wait(0.5)
            self.play(
                Circumscribe(ex_dec, color = PINK, time_width = 0.5, stroke_width = 3),
                Circumscribe(histo.axes.x_labels[x], color = PINK, time_width = 0.5, stroke_width = 4), 
            )
            self.wait()
        self.wait(3)


class DefineExpectedValue(Scene):
    def construct(self):

        self.explain_binomial_dist()
        self.definition_and_formula()


    def explain_binomial_dist(self):
        prob = Tex("Erfolgswahrscheinlichkeit ", "$p$")
        prob.move_to(3.67353169 * LEFT + 3.14520993*UP)
        prob[0].set_color_by_gradient(GREEN, GREY_A, GREEN)
        prob[-1].set_color(GREEN)

        exp = Tex("Bernoulli", "$-$", "Experiment", font_size = 72)
        exp.move_to(3*RIGHT + UP)

        trail = Tex("Bernoulli", "$-$", "Kette", font_size = 72)
        trail.move_to(exp, aligned_edge=UL)

        self.wait()
        self.play(Write(prob))
        self.wait()

        # bernoulli - exp
        roses = VGroup(*[SVGMobject(SVG_DIR + "rose_illustration").set_stroke(width = 1) for x in range(2)])
        roses.set(height = 1)
        roses.arrange(RIGHT, buff = 2)
        roses.next_to(exp, UP, buff = 0.5)

        check = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        cross = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
        for mark, rose in zip([check, cross], roses):
            mark.match_height(rose)
            mark.move_to(rose)

        for rose in roses:
            rose.save_state()
            rose.next_to(exp, UP, buff = 0.5)

        self.play(
            ShowIncreasingSubsets(VGroup(*exp)),
            FadeIn(roses),
            run_time = 2
        )
        self.play(
            *[Restore(rose) for rose in roses], 
            LaggedStartMap(FadeIn, VGroup(check, cross), shift = DOWN, lag_ratio = 0.2, rate_func = squish_rate_func(smooth, 0.3, 1)), 
            run_time = 3
        )
        self.wait()

        # bernoulli - trail
        bools = [False] + [True] + 3*[False] + [True] + 4*[False]
        cac = get_checks_and_crosses(bools, width = 7)
        cac.next_to(exp, DOWN, buff = 0.5, aligned_edge=LEFT)
        u_lines = VGroup(*[Underline(mark).set_y(-0.545946) for mark in cac])
        u_numbers = VGroup(*[
            Integer(num).set(height = 0.2).next_to(line, DOWN, buff = 0.1) for num, line in zip(range(1, 11), u_lines)
        ])

        check_copy = check.copy()
        cross_copy = cross.copy()
        self.play(
            AnimationGroup(
                check_copy.animate.become(cac[1]),
                cross_copy.animate.become(cac[0]),
                lag_ratio = 0.1
            ),
            LaggedStartMap(Create, u_lines, lag_ratio = 0.05),
            ReplacementTransform(exp, trail, rate_func = squish_rate_func(smooth, 0.66, 1)),
            run_time = 3
        )
        self.play(
            LaggedStartMap(FadeIn, cac[2:], shift = UP), 
            run_time = 1.5
        )
        self.play(
            LaggedStartMap(FadeIn, u_numbers, shift = 0.25*UP, lag_ratio = 0.05, rate_func = there_and_back), 
            run_time = 1.5
        )

        brace = Brace(u_lines, DOWN, color = GREY)
        brace_text = brace.get_text("$n$", " $=$ ", "10", " Wiederholungen")
        self.play(
            GrowFromEdge(brace, LEFT), 
            Write(brace_text)
        )
        self.wait()

        arrows = VGroup(*[
            CurvedArrow(cac[2].get_top() + 0.1*UP, cac[3].get_top() + 0.1*UP, angle = -90*DEGREES, color = YELLOW_D, tip_length = 0.2)
            for x in range(9)
        ])
        for arrow, mark in zip(arrows, cac):
            arrow.next_to(mark.get_top() + 0.1*UP, UP, buff = 0)
            arrow.shift(0.3*RIGHT)

        self.play(LaggedStartMap(FadeIn, arrows, rate_func = there_and_back_with_pause, lag_ratio = 0.1), run_time = 3)
        self.wait()


        self.exp, self.prob, self.brace_text = exp, prob, brace_text 

    def definition_and_formula(self):
        formula = MathTex("E", "[", "X", "]", "=", "n", "\\cdot", "p", font_size = 72)
        formula.to_edge(DOWN, buff = 0.75)
        formula.align_to(self.exp, LEFT)

        print(formula.get_center())

        name = Tex("Erwartungswert", font_size = 72)
        name.next_to(formula, LEFT, buff = 0.75)

        p = self.prob[-1].copy()
        n = self.brace_text[0].copy()

        product = MathTex("10", "\\cdot", "0{,}2")\
            .match_width(formula[-3:])\
            .next_to(formula[-3:], UP)\
            .set_color(YELLOW_D)

        self.play(
            AnimationGroup(
                Transform(p, formula[-1]), 
                Transform(n, formula[-3]), 
                FadeIn(formula[-2], shift = DOWN),
                lag_ratio = 0.1
            ),
            Write(product, rate_func = squish_rate_func(smooth, 0.66, 1)),
            run_time = 4
        )
        self.wait()

        self.play(Write(name), run_time = 1.5)
        self.play(
            FadeOut(product),
            FadeIn(formula[:-3], shift = 0.5*RIGHT), 
            run_time = 2
        )

        rect = SurroundingRectangle(formula, color = YELLOW_D)
        self.play(Create(rect), run_time = 3)
        self.play(FadeOut(rect, scale = 4))
        self.wait()

        self.play(FadeToColor(formula[5], BLUE), run_time = 1.5)
        self.play(FadeToColor(formula[7], YELLOW_D), run_time = 1.5)
        self.wait(3)


class DefineBGAnimation(Shooting):
    def construct(self):
        rose = SVGMobject(SVG_DIR + "rose_illustration")\
            .set(height = 4)\
            .to_edge(LEFT, buff = 2.25)

        p_line =  NumberLine(x_range = [0, 1, 0.2], length = 4.5, include_numbers=True)
        p_line.next_to(rose, UP)

        p_title = Tex("Erfolgswahrscheinlichkeit ", "$p$")
        p_title.next_to(p_line, UP, buff = 0.1, aligned_edge=LEFT)
        p_title[0].set_color_by_gradient(GREEN, GREY_A, GREEN)
        p_title[-1].set_color(GREEN)

        # print(p_title.get_center())

        p_val = ValueTracker(0.8)
        p_dot = Dot(point = p_line.n2p(p_val.get_value()), radius = 0.1, color = YELLOW)
        p_dot.set_sheen(-0.5, DR)



        r_val = ValueTracker(0.25)
        curve = always_redraw(lambda: ParametricFunction(
            lambda t: self.infinity_func(r_val.get_value(), t), t_range = [0, TAU], fill_opacity = 0, stroke_opacity = 0)\
                .move_to(rose.get_bottom())\
                .shift(UP)
        )
        fk = self.get_fadenkreuz()
        fk.scale(0.5)
        fk.move_to(curve.get_start())

        self.add(curve)
        self.play(
            Create(p_line), 
            FadeIn(p_dot, scale = 0.1),
            DrawBorderThenFill(rose),
            Create(fk), 
            run_time = 2
        )
        self.wait()

        p_dot.add_updater(lambda dot: dot.move_to(p_line.n2p(p_val.get_value())))
        self.t_offset = 0
        def move_along_infinity(mob, dt):
            rate = dt * 0.3
            mob.move_to(curve.point_from_proportion((self.t_offset + rate) % 1))
            self.t_offset += rate
        fk.add_updater(move_along_infinity)
        self.wait(3)

        self.play(
            r_val.animate.set_value(1),
            p_val.animate.set_value(0.2),
            run_time = 6
        )
        self.wait(30)


class ItCanBeADecimal(HistoScene):
    def construct(self):
        self.n = 10
        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 4,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.32, "y_tick_num": 4,
            "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }

        self.setup_old_scene()
        self.integer_values()


    def setup_old_scene(self):
        formula = MathTex("E", "[", "X", "]", "=", "n", "\\cdot", "p", font_size = 72)
        formula.move_to(1.35519266 * RIGHT + 2.876401 * DOWN)

        name = Tex("Erwartungswert", font_size = 72)
        name.next_to(formula, LEFT, buff = 0.75)

        self.add(formula, name)
        self.wait()

        name.generate_target()
        name.target.to_edge(UP)

        uline = Underline(name.target, color = GREY)

        formula.generate_target()
        formula.target.next_to(name.target, RIGHT, buff = 0.5)

        self.play(
            LaggedStartMap(MoveToTarget, VGroup(name, formula), lag_ratio = 0.2), 
            run_time = 3
        )
        self.play(Create(uline))
        self.wait()

        self.name, self.formula = name, formula

    def integer_values(self):
        histo = self.get_histogram(self.n, 0.2, **self.histo_kwargs)
        histo_0 = self.get_histogram(self.n, 0.2, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.to_edge(DOWN)

        self.play(
            FadeIn(histo.axes),
            ReplacementTransform(histo_0.bars, histo.bars),
            run_time = 4
        )
        self.wait()

        trail = MathTex("n", "=", "10", font_size = 72)\
            .next_to(self.name, DOWN, buff = 0.5)\
            .shift(RIGHT)
        prob = MathTex("p", "=", "10", font_size = 72)
        prob.next_to(trail, RIGHT, buff = 1.5, aligned_edge=UP)
        prob[-1].set_fill(opacity = 0)

        p_val = ValueTracker(0)
        p_dec = DecimalNumber(p_val.get_value())\
            .scale(1.5)\
            .next_to(prob[1], RIGHT)\
            .shift(0.05*UP)\
            .add_updater(lambda dec: dec.set_value(p_val.get_value()))

        arrow = Arrow(ORIGIN, RIGHT, buff = 0, color = PINK)
        arrow.next_to(self.formula, RIGHT)

        ex_dec = DecimalNumber(self.n * p_val.get_value())\
            .scale(1.5)\
            .next_to(arrow, RIGHT)\
            .add_updater(lambda dec: dec.set_value(self.n * p_val.get_value()))

        self.play(Write(trail))
        self.wait()
        self.add(p_dec)
        self.play(
            FadeIn(prob, shift = RIGHT),
            p_val.animate(run_time = 2).set_value(0.2)
        )
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(FadeIn(ex_dec, shift = LEFT), run_time = 2)
        self.play(Circumscribe(ex_dec, time_width = 0.75, color = YELLOW_D, stroke_width = 2, run_time = 2))
        self.wait()

        # Line for expected value
        ex_line = always_redraw(lambda: Line(
            histo.axes.c2p(self.n * p_val.get_value() + 0.5, 0), histo.axes.c2p(self.n * p_val.get_value() + 0.5, 0.32), 
            stroke_width = 8, color = PINK
        ))
        self.play(GrowFromEdge(ex_line, DOWN), run_time = 3)
        self.wait()

        p_values = [0.3, 0.5, 0.7, 0.8]
        for value, x in zip(p_values, range(3,9)):
            new_histo = self.get_histogram(self.n, value, **self.histo_kwargs).to_edge(DOWN)

            histo.become(new_histo)
            p_val.set_value(value)
            self.wait(1.5)

        self.play(Circumscribe(ex_dec, time_width = 0.75, color = YELLOW_D, stroke_width = 2, run_time = 2))
        self.wait()

        histo.p_val = p_val
        histo.n = self.n
        self.play(
            UpdateFromFunc(histo, self.update_histogram),
            p_val.animate.set_value(0.42),
            run_time = 8
        )
        self.wait()

        p_rect = SurroundingRectangle(VGroup(prob, p_dec), color = YELLOW_D, stroke_width = 3)
        ex_rect = SurroundingRectangle(ex_dec, color = YELLOW_D, stroke_width = 3)

        self.play(Create(p_rect), run_time = 2)
        self.wait(0.5)
        self.play(ReplacementTransform(p_rect, ex_rect), run_time = 2)
        self.wait()
        self.play(FadeOut(ex_rect, scale = 2))
        self.wait()

        add_anim = [ex_line.animate(rate_func = there_and_back).shift(0.2*histo.axes.x_axis.unit_size*LEFT)]
        self.highlight_single_bar(histo, 4, add_anim, run_time = 4)
        self.wait()

        p_values = [0.77, 0.31, 0.55, 0.87, 0.2]
        h_bar_nums = [8, 3, 6, 9, 2]
        for value, bar_num in zip(p_values, h_bar_nums):
            self.play(
                UpdateFromFunc(histo, self.update_histogram),
                p_val.animate.set_value(value),
                run_time = 4
            )
            self.highlight_single_bar(histo, bar_num, run_time = 1.5)
            self.wait()
        self.wait(3)


    # functions 
    def update_histogram(self, hist):
        new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
        new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)


class DecimalMeaning(Scene):
    def construct(self):

        self.roses()
        self.repeat_10_times()



    def roses(self):
        roses = VGroup(*[SVGMobject(SVG_DIR + "rose_illustration") for x in range(4)])
        roses.arrange(RIGHT, buff = 1)

        brace4 = Brace(roses, DOWN, color = GREY)
        text4 = brace4.get_text("$4$ ", "Rosen")
        text4.scale(1.25)
        text4[1].set_color(MAROON)


        self.play(
            LaggedStartMap(FadeIn, roses, lag_ratio = 0.1),
            Create(brace4),
            run_time = 1
        )
        self.play(Write(text4), run_time = 0.75)
        self.wait(0.5)


        self.play(
            ApplyMethod(roses.shift, 1.5*LEFT),
            MaintainPositionRelativeTo(brace4, roses), 
            MaintainPositionRelativeTo(text4, roses), 
            run_time = 1
        )
        self.wait(0.5)

        rose = SVGMobject(SVG_DIR + "rose_illustration")
        rose.next_to(roses, RIGHT, buff = 1)
        brace02 = Brace(rose, DOWN, color = GREY)
        text02 = brace02.get_text("wtf")
        text02.scale(1.25)
        self.play(
            Create(rose[2:5]), 
            GrowFromCenter(brace02)
        )
        self.play(Write(text02), run_time = 0.75)
        self.wait(2)

        self.mobs = self.mobjects

    def repeat_10_times(self):
        bools = 2*[False] + [True] + [False] + 2*[True] + 2*[False] + [True] + [False]

        example = get_checks_and_crosses(bools, width = 10)
        brace1 = Brace(example, UP, color = GREY)
        text1 = brace1.get_text("10 ", "$\\times$")
        text1[1].set_color(YELLOW_D)

        self.play(
            LaggedStartMap(FadeOut, self.mobs, lag_ratio = 0.1, run_time = 1), 
            FadeIn(example, lag_ratio = 0.1, shift = DOWN, run_time = 2)
        )
        self.play(
            Create(brace1), 
            Write(text1)
        )
        self.wait()


        cac_group = VGroup(*[
            get_random_checks_and_crosses(n = 10, s = 0.42, width = 4)
            for x in range(10)
        ])
        cac_group.arrange(DOWN, buff = 0.2)
        cac_group.shift(2*LEFT)


        first_row = example.copy()
        first_row.match_width(cac_group)
        first_row.move_to(cac_group[0])

        cac_group[0] = first_row


        top_brace = Brace(cac_group, UP, color = GREY)

        self.play(
            AnimationGroup(
                *[ShowIncreasingSubsets(row) for row in cac_group[1:]], 
                lag_ratio = 0.05
            ), 
            Transform(example, first_row),
            ReplacementTransform(brace1, top_brace),
            MaintainPositionRelativeTo(text1, brace1),
            run_time = 3
        )
        self.wait()

        # 4.2 out of 10 shots
        arrow = Arrow(LEFT, RIGHT, color = GREY, stroke_width = 3, tip_length = 0.2)
        arrow.next_to(cac_group[0], RIGHT, buff = 1)

        approx = MathTex("\\approx")
        approx.scale(1.5)
        approx.next_to(arrow, RIGHT, buff = 0.5)

        ex_val = ValueTracker(4.20)
        ex_dec = DecimalNumber(ex_val.get_value(), edge_to_fix=LEFT)
        ex_dec.scale(1.5)
        ex_dec.next_to(approx, RIGHT, buff = 0.5)
        ex_dec.add_updater(lambda dec: dec.set_value(ex_val.get_value()))

        self.play(
            GrowArrow(arrow), 
            Write(approx), 
            FadeIn(ex_dec, shift = LEFT)
        )

        # 42 out of 100 shots
        left_brace = Brace(cac_group, LEFT, color = GREY)
        text2 = left_brace.get_text("10 ", "$\\times$")
        text2[1].set_color(YELLOW_D)

        shift_diff = cac_group[0].get_right()[1] - cac_group[-1].get_right()[1]
        self.play(
            ex_val.animate.set_value(42),
            ex_dec.animate.shift(shift_diff * DOWN),
            MaintainPositionRelativeTo(VGroup(arrow, approx), ex_dec),
            Create(left_brace), 
            Write(text2), 
            run_time = 3
        )
        self.wait()

        # makes sense
        ms = Tex("Macht irgendwie\\\\", "mehr Sinn, oder?")
        ms.shift(3*RIGHT + UP)

        curve = CurvedArrow(ex_dec.get_top() + 0.2*UP, ms.get_bottom() + 0.5*RIGHT + 0.2*DOWN, angle = 45*DEGREES, color = YELLOW_D)

        self.play(Create(curve), run_time = 0.75)
        self.play(Write(ms), run_time = 0.5)
        self.wait(3)


class WhatIsItThen(Scene):
    def construct(self):

        answer = Tex("Eine reelle Zahl")
        answer.scale(1.5)
        self.add(answer)

        question = Tex("Was ist denn nun\\\\", "der ", "Erwartungswert", "?")
        question.scale(2)
        question.add_background_rectangle(opacity = 1, buff = 0.2, stroke_width=2, stroke_opacity=1, stroke_color = PINK)


        strings = [
            "Beschreibt eine Erfolgszahl\\\\ der Bernoulli$-$Kette",
            "Beschreibt die Erfolgszahl, \\\\die am wahrscheinlichsten ist"
        ]
        options = VGroup(*[Tex(string, color = GREY_B).scale(1.25) for string in strings])
        options.arrange(DOWN, buff = 4)


        self.add(question, options)
        self.wait(2)


        self.play(FadeOut(options[0], shift = 5*LEFT), run_time = 1.5)
        self.wait()

        self.play(FadeOut(options[1], shift = 5*RIGHT), run_time = 1.5)
        self.wait()


        self.play(
            ApplyMethod(question.shift, 2*DOWN), 
            ApplyMethod(answer.shift, 2.5*UP), 
        )
        sur_rects = VGroup(*[
            SurroundingRectangle(answer, buff = buff, stroke_width = 2).set_color([BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E])
            for buff in reversed(np.linspace(0.1, 0.55, 11))
        ])
        self.play(
            LaggedStartMap(FadeOut, sur_rects, scale = 4, lag_ratio = 0.1), 
            run_time = 2
        )

        ex = MathTex("E", "[", "X", "]", "=", "4.2", color = GREY_B)
        ex[0].set_color(YELLOW_D)
        ex[-1].set_color(PINK)
        ex.scale(1.5)
        ex.next_to(answer, DOWN, buff = 0.75)
        self.play(FadeIn(ex, shift = DOWN))
        self.play(FocusOn(ex[-1], run_time = 1.5))
        self.wait(3)


class Thumbnail(Shooting):
    def construct(self):
        ten = Tex("10 Schüsse")
        ten.set(width = 6)
        ten.to_corner(DL)

        question = Tex("Wie viele Rosen?")
        question.set(height = ten.height)
        question.to_corner(UL)

        self.add(ten, question)


        rose = SVGMobject(SVG_DIR + "rose_illustration")\
            .set(height = 5.5)\
            .to_edge(RIGHT, buff = 2.25)\
            .shift(DOWN)

        p_line =  NumberLine(x_range = [0, 1, 0.2], length = 4.5, include_numbers=False)
        p_line.to_edge(LEFT).shift(1.5*RIGHT)

        p_line_texs = VGroup(*[MathTex(tex, color = GREY) for tex in ["0", "0.2", "1"]])
        p_line_texs[1].set_color(WHITE)
        for tex, x in zip(p_line_texs, [0,0.2,1]):
            tex.next_to(p_line.n2p(x), DOWN)

        p_title = Tex("Erfolgswahrscheinlichkeit ", "$p$")
        p_title.set(width = p_line.width + 2.5)
        p_title.next_to(p_line, UP)
        p_title[0].set_color_by_gradient(GREEN, GREY_A, GREEN)
        p_title[-1].set_color(GREEN)

        p_val = ValueTracker(0.2)
        p_dot = Dot(point = p_line.n2p(p_val.get_value()), radius = 0.12, color = YELLOW)
        p_dot.set_sheen(-0.35, DR)

        fk = self.get_fadenkreuz()
        fk.scale(0.75)
        fk.move_to(2.75*RIGHT + 2*DOWN)



        cac = VGroup(*[
            get_random_checks_and_crosses(n = 10, s = 0.42, width = 2.5) 
            for x in range(250)
        ])
        cac.arrange_in_grid(rows = 25, columns = 10, buff = 0.5)
        cac.set(height = config["frame_height"] - 1)
        cac.set_fill(opacity = 0.5)

        self.bring_to_back(cac)




        self.add(rose, p_line, p_line_texs, p_title, p_dot, fk)






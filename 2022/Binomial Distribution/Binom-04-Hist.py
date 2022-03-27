from manim import *
from BinomHelpers import *
import random

import scipy.stats 


class Intro(HistoScene):
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
            mob.center().to_edge(DOWN)

        title = Tex("Histogramm")\
            .set_color_by_gradient(*histo_kwargs["bar_colors"])\
            .set_fill(color = WHITE, opacity = 0.3)\
            .set_stroke(width = 1.5)\
            .set(width = config["frame_width"] - 6)\
            .to_corner(UR)


        self.add(histo_0)
        self.play(
            DrawBorderThenFill(title, rate_func = squish_rate_func(smooth, 0.6, 1)), 
            ReplacementTransform(histo_0.bars, histo.bars, lag_ratio = 0.2),
            run_time = 5
        )
        self.wait()
        self.remove(histo_0)


        prop_val = ValueTracker(p)
        histo.p_val = prop_val
        histo.n = n
        def update_histogram(hist):
            new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
            new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])
            new_bars = hist.get_bars(new_data)
            new_bars.match_style(hist.bars)
            hist.bars.become(new_bars)

        for prop in [0.1, 0.5, p]:
            self.play(
                prop_val.animate.set_value(prop),
                UpdateFromFunc(histo, update_histogram, suspend_mobject_updating=False),
                run_time = 4.5
            )
            self.wait(0.5)
        self.wait(0.5)

        remember = Tex("Merke dir das...", font_size = 72).shift(2*LEFT + 0.4*DOWN)
        self.play(Write(remember))
        self.wait(3)


class WhatsTheModell(HistoScene):
    def construct(self):
        self.n = 10
        self.p = 0.7

        self.both_result()
        self.probability()
        self.trail_of_length_10()

    def both_result(self):
        coin_scale = 1.5
        results = VGroup(*[get_coin(symbol).scale(coin_scale) for symbol in ["Z", "K"]])
        results.arrange(RIGHT, buff = 2)
        for result in results:
            result.save_state()
            result.center()

        init_heads = get_coin("K").scale(1.5)

        def random_update_result(mob):
            p = random.uniform(0,1)
            if p > 0.5:
                choice = get_coin("K")
            else:
                choice = get_coin("Z")
            choice.scale(coin_scale)
            mob.become(choice)

        self.play(
            UpdateFromFunc(init_heads, random_update_result, run_time = 6)
        )
        self.add(results)
        self.remove(init_heads)
        self.play(*[Restore(result) for result in results], run_time = 2)


        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        sf_marks = VGroup(*[
            Tex(mark, color = tex_color, tex_template = myTemplate, font_size = 120) 
            for mark, tex_color in zip([CMARK_TEX, XMARK_TEX], [C_COLOR, X_COLOR])
        ])
        for mark, result in zip(sf_marks, results):
            mark.next_to(result, UP, buff = 1)

        self.play(DrawBorderThenFill(sf_marks, lag_ratio = 0.1), run_time = 1.5)
        self.play(Swap(*results), run_time = 1.5)
        self.wait()

        succ_group = VGroup(sf_marks[0], results[1])
        succ_group.generate_target()
        succ_group.target.arrange(RIGHT, buff = 0.5).to_edge(UP).shift(4*RIGHT)

        fail_group = VGroup(results[0], sf_marks[1])
        fail_group.generate_target()
        fail_group.target.arrange(RIGHT, buff = 0.5).to_edge(UP).shift(4*LEFT)

        self.play(
            *[MoveToTarget(group) for group in [succ_group, fail_group]], 
            run_time = 1.5
        )

        self.succ_group, self.fail_group = succ_group, fail_group

    def probability(self):
        prob = ValueTracker(0.5)
        succ = DecimalNumber(prob.get_value())\
            .scale(1.5)\
            .set_color(C_COLOR)\
            .next_to(self.succ_group, DOWN, buff = 0.5)\
            .add_updater(lambda dec: dec.set_value(prob.get_value()))
        fail = DecimalNumber(1 - prob.get_value())\
            .scale(1.5)\
            .set_color(X_COLOR)\
            .next_to(self.fail_group, DOWN, buff = 0.5)\
            .add_updater(lambda dec: dec.set_value(1 - prob.get_value()))

        self.play(*[FadeIn(sf, shift = DOWN) for sf in [succ, fail]])
        self.wait()
        self.play(prob.animate.set_value(self.p), run_time = 3)
        self.play(Circumscribe(succ, color = C_COLOR, stroke_width = 6, run_time = 2))
        self.wait()

        bools = 7 * [True] + 3 * [False]
        grid = get_coin_grid(bools, height=6)
        grid.arrange(RIGHT).set(height = 1).shift(DOWN)

        random.shuffle(bools)
        grid_shuffle = get_coin_grid(bools, height=6)
        grid_shuffle.arrange(RIGHT).set(height = 1).shift(DOWN)
        self.play(LaggedStartMap(FadeIn, grid_shuffle, shift = 0.5*UP, lag_ratio = 0.1), run_time = 1.5)
        self.wait()

        self.play(ReplacementTransform(grid_shuffle, grid))
        self.wait()


        bools = 70 * [True] + 30 * [False]
        new_grid = get_coin_grid(bools, height = 5)
        new_grid.to_edge(DOWN)

        random.shuffle(bools)
        new_grid_shuffle = get_coin_grid(bools, height = 5)
        new_grid_shuffle.to_edge(DOWN)

        self.play(ReplacementTransform(grid, new_grid_shuffle))
        self.wait()

        self.play(TransformMatchingShapes(new_grid_shuffle, new_grid))
        self.wait(2)

        self.play(
            AnimationGroup(
                FadeOut(new_grid[:70], shift = 5*UP),
                FadeOut(new_grid[70:], shift = 3*DOWN), 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()

        self.play(
            AnimationGroup(
                *[dec.animate.next_to(group, direction, buff = 0.35) for dec, group, direction 
                in zip([succ, fail],[self.succ_group, self.fail_group],[LEFT, RIGHT])], 
                lag_ratio = 0.1
            ),
            run_time = 2.5
        )
        self.wait()

    def trail_of_length_10(self):
        # Create 20 DecimalNumbers
        numbers = VGroup()
        for i in range(self.n):
            num = DecimalNumber()
            numbers.add(num)

        # set their value
        def randomize_numbers(numbers):
            for num in numbers:
                value = random.uniform(0,1)
                num.set_value(value)
                if value < 0.3:
                    num.set_color(RED)
                else:
                    num.set_color(GREEN)

        numbers.set(height = 0.2)
        numbers.arrange(RIGHT, buff = 0.35)
        numbers.to_edge(UP, buff = 2.75)

        # get results (K or Z) depending on that number
        def get_results(numbers):
            results = VGroup()
            for num in numbers:
                if num.get_value() < 0.3:
                    result = Tex("Z").set_color(RED)
                else:
                    result = Tex("K").set_color(BLUE)

                result.set(height = 0.4)
                result.next_to(num, UP)
                results.add(result)
            return results

        succ_nums = VGroup()
        grid = VGroup()
        for x in range(10):
            succ_var = 0
            self.play(
                numbers.animate.shift(0.5*DOWN), 
                UpdateFromFunc(numbers, randomize_numbers)
            )

            for num in numbers:
                if num.get_value() > 0.3:
                    succ_var += 1

            results = get_results(numbers)
            grid.add(*results)
            self.play(LaggedStartMap(FadeIn, results, shift = 0.2*DOWN))

            succ_num = Integer()\
                .set_value(succ_var)\
                .next_to(results, RIGHT, buff = 0.5)\
                .align_to(self.succ_group, RIGHT)\
                .shift(0.6*LEFT)\
                .set_color(YELLOW_E)
            succ_num.value = succ_var

            succ_nums.add(succ_num)

            self.play(Write(succ_num))

        self.wait(2)

        # FadeOut numbers, results & arrange succ_nums
        succ_nums.generate_target()
        succ_nums.target.scale(1.75).arrange(RIGHT, buff = 0.75).center()
        self.play(
            LaggedStartMap(ShrinkToCenter, grid, lag_ratio = 0.01, run_time = 2),
            LaggedStartMap(ShrinkToCenter, numbers, lag_ratio = 0.1, run_time = 2),
            MoveToTarget(succ_nums, lag_ratio = 0.05, rate_func = squish_rate_func(smooth, 0.3, 1), run_time = 3)
        )
        self.wait()

        # clarify meaning again
        def get_arrows_from_value(value):
            value_group = VGroup(*[number for number in succ_nums if number.value == value])
            arrows = VGroup()
            for mob in value_group:
                arrow = Arrow(ORIGIN, 1.5*UP)
                arrow.next_to(mob, DOWN)
                arrows.add(arrow)

            return arrows

        arrows_6 = get_arrows_from_value(6)
        arrows_7 = get_arrows_from_value(7)
        self.play(FadeIn(arrows_6, shift = UP, lag_ratio = 0.1))
        self.wait()
        self.play(
            FadeOut(arrows_6, shift = DOWN, lag_ratio = 0.1),
            FadeIn(arrows_7, shift = UP, lag_ratio = 0.1)
        )
        self.wait()
        self.play(FadeOut(arrows_7))
        self.wait()

        # prepare for histogram
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "include_h_lines": True, "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        histo.center().to_edge(DOWN)

        for num in succ_nums:
            value = num.value
            num.generate_target()
            target_mob = histo.axes.x_labels[value]
            num.target.match_height(target_mob).match_color(target_mob).move_to(target_mob)
        self.play(
            LaggedStartMap(MoveToTarget, succ_nums, lag_ratio = 0.1), run_time = 5
        )
        self.wait()
        self.play(
            Create(histo.axes.x_axis), 
            ShowIncreasingSubsets(histo.axes.x_labels), 
            run_time = 5
        )
        self.remove(succ_nums)
        self.wait(2)

        self.play(
            Create(histo.axes.y_axis),
            Create(histo.axes.h_lines),
            run_time = 3
        )
        self.wait(3)


# Brian Links: 
# https://github.com/brianamedee/3B1B-Animated-Tutorials/blob/main/3b1bProbability.py
# https://www.youtube.com/watch?v=t_wBGoO8TA8&t=467s

# 3Blue1Brown
# https://youtu.be/8idr1WZ1A7Q?t=366


class SimulateHistogram(HistoScene):
    def construct(self):
        self.n = 10
        self.p = 0.7
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "include_h_lines": True, "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        histo.center().to_edge(DOWN)


        def get_bars(histogram, data):
            portions = np.array(data).astype(float)
            total = portions.sum()
            if total == 0:
                portions[:] = 0
            else:
                portions /= total

            bars = VGroup()

            for x, prop in enumerate(portions):
                p1 = VectorizedPoint().move_to(histogram[0].c2p(x, 0))
                p2 = VectorizedPoint().move_to(histogram[0].c2p(x + 1, 0))
                p3 = VectorizedPoint().move_to(histogram[0].c2p(x + 1, prop))
                p4 = VectorizedPoint().move_to(histogram[0].c2p(x, prop))
                points = VGroup(p1, p2, p3, p4)
                bar = Rectangle().replace(points, stretch=True)
                bar.set_stroke(width = 1)
                bars.add(bar)
            # bars.set_style(fill_color = [*histo_kwargs["bar_colors"]], fill_opacity = 0.6, stroke_color = WHITE)
            return bars


        data = np.zeros(11)  # Possible outcomes as an array
        row = get_random_row(p = self.p, n = self.n).shift(0.25*DOWN)
        bars = get_bars(histogram=histo, data=data)

        text_counter = Tex("Anzahl: ", font_size = 60).shift(3.5*LEFT + UP)
        counter = always_redraw(
            lambda: Integer()\
                .scale(1.25)\
                .set_value(sum(data))\
                .next_to(text_counter, RIGHT, buff=0.3, aligned_edge = UP)
        )
        arrow = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(PINK)

        # Update function
        def update(dummy, n_added_data_points=0):
            new_row = get_random_row().shift(0.25*DOWN)
            row.become(new_row)

            count = sum([m.positive for m in new_row.nums])
            data[count] += 1
            if n_added_data_points:
                values = np.random.random((n_added_data_points, 10))
                counts = (values > 0.3).sum(1)                              # changed from < 0.2
                for i in range(len(data)):
                    data[i] += (counts == i).sum()

            bars.become(get_bars(histogram=histo, data=data))

            arrow.next_to(bars[count], UP, buff=0.1)

            # bars[2].set_style(
            #     fill_color = [*histo_kwargs["bar_colors"]],
            #     fill_opacity = 0.6,
            #     stroke_color = WHITE,
            # )

        self.add(histo.axes)
        self.wait()
        
        self.play(
            AnimationGroup(
                FadeIn(row, shift = DOWN, lag_ratio = 0.1),
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait()
        self.play(
            AnimationGroup(
                Write(text_counter),
                FadeIn(counter, shift = UP),
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait()
        self.play(Circumscribe(counter, color = YELLOW_D, time_width = 0.75, run_time = 3))
        self.wait()
        self.add(bars, arrow)


        group = VGroup(row, bars, arrow)
        self.play(UpdateFromFunc(group, update), run_time = 2)
        self.wait(2)


        self.play(
            LaggedStart(*[mark.animate(rate_func = there_and_back).shift(0.5*DOWN) for mark in row.syms], lag_ratio = 0.1),
            run_time = 3
        )
        self.play(Circumscribe(arrow, color = YELLOW_D, time_width = 0.75, run_time = 3))
        self.wait()


        self.play(UpdateFromFunc(group, lambda m: update(m, 10)), run_time = 2)
        self.wait(2)
        self.play(UpdateFromFunc(group, lambda m: update(m, 100)), run_time = 2)
        self.play(UpdateFromFunc(group, lambda m: update(m, 500)), run_time = 2)
        self.play(UpdateFromFunc(group, lambda m: update(m, 1000)), run_time = 2)
        self.play(UpdateFromFunc(group, lambda m: update(m, 1000)), run_time = 2)
        self.wait(3)


        histo_0 = self.get_histogram(self.n, self.p, zeros = True, **histo_kwargs)
        histo_0.center().to_edge(DOWN)

        counter.clear_updaters()
        self.play(
            FadeOut(VGroup(row, text_counter, counter, arrow)),
            ReplacementTransform(histo_0.bars, histo.bars, lag_ratio = 0.1),
            run_time = 5
        )
        self.remove(bars)
        self.wait(3)


class SimulationAfterEffects(HistoScene, MovingCameraScene):
    def construct(self):
        self.n = 10
        self.p = 0.7
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "include_h_lines": True, "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        histo.center().to_edge(DOWN)

        self.add(histo)
        self.wait(2)

        self.connect_to_formula()
        self.formula_to_bar()
        self.probs_sum_up_to_1()
        self.changing_parameters()


    def connect_to_formula(self):
        n, p, histo = self.n, self.p, self.histo

        k = self.k = 7
        binom_data = VGroup(*[MathTex(*tex) for tex in (["n", "=", str(n)], ["p", "=", str(p)])])\
            .arrange_submobjects(RIGHT, aligned_edge = UP)\
            .scale(0.6)\
            .to_corner(UL, buff = 0.1)\
            .save_state()\
            .scale(2.5)\
            .center()\
            .shift(LEFT + UP)

        formula = get_binom_formula(n, p, k)
        formula.scale(1.25)
        formula.to_edge(UP)
        formula.shift(1.1*LEFT)

        self.play(ShowIncreasingSubsets(binom_data), run_time = 2)
        self.wait()
        self.play(Restore(binom_data))
        self.wait(0.5)

        self.play(Write(formula[:7]), run_time = 1)
        self.wait()

        self.play(FocusOn(histo.axes.x_labels[k], run_time = 1))
        self.play(Circumscribe(histo.axes.x_labels[k], color = C_COLOR))
        self.wait()

        self.play(Write(formula[7:11]))
        self.wait()
        self.play(Write(formula[11:14]))
        self.wait()
        self.play(Write(formula[14:]))
        self.wait()

        self.play(Circumscribe(formula, color = BLUE, time_width = 0.75, stroke_width = 2, run_time = 3))
        self.wait()

        self.formula, self.binom_data = formula, binom_data

    def formula_to_bar(self):
        k, n, p, histo = self.k, self.n, self.p, self.histo
        formula = self.formula

        result = get_binom_result(n, p, k)
        result_tex = MathTex("\\approx", str(result)).scale(1.25).next_to(formula, RIGHT, buff = 0.1)

        line = DashedLine(dash_length = 0.01, stroke_width = 1, stroke_color = WHITE)
        line.match_width(histo.axes.x_axis)
        line.next_to(histo.axes.c2p(0, result), buff = 0)

        self.play(FadeIn(result_tex, shift = 2*LEFT), run_time = 2)
        self.play(Circumscribe(result_tex, color = histo.bars[k].get_color(), run_time = 2))
        self.wait() 

        dot = Dot(point = histo.axes.c2p(0,0), color = histo.bars[k].get_color())
        self.play(FocusOn(dot))
        self.play(dot.animate.move_to(histo.axes.c2p(0, result)), run_time = 2)
        self.play(
            Create(line),
            dot.animate.move_to(histo.axes.c2p(n + 1, result)),
            rate_func = smooth, run_time = 2
        )
        self.highlight_single_bar(histo, k, run_time = 2)
        self.play(ApplyWave(histo.bars[k], run_time = 2))
        self.play(ShrinkToCenter(dot))
        self.wait()


        for k in [10, 6, 3]:
            new_formula = get_binom_formula(n, p, k)\
                .scale(1.25)\
                .to_edge(UP)\
                .shift(1.1*LEFT)
            self.play(Transform(formula, new_formula))
            self.wait(0.5)

            new_result = round(scipy.stats.binom.pmf(k,n,p), 4)
            new_tex = MathTex("\\approx", str(new_result)).scale(1.25).next_to(formula, RIGHT, buff = 0.1)
            self.play(Transform(result_tex, new_tex))
            self.wait(0.5)

            new_line = DashedLine(dash_length = 0.01, stroke_width = 1, stroke_color = WHITE)
            new_line.match_width(histo.axes.x_axis)
            new_line.next_to(histo.axes.c2p(0, new_result), buff = 0)

            self.highlight_single_bar(histo, k, run_time = 1.5)
            self.play(Transform(line, new_line))
            self.wait()

        self.highlight_group_of_bars(histo, 0, 10, run_time = 3)
        self.play(
            FadeOut(line), 
            FadeOut(formula),
            FadeOut(result_tex),
            FadeOut(self.binom_data)
        )
        self.wait()


        formulas = VGroup(*[MathTex("P", "(", "X", "=", str(num), ")") for num in range(11)])
        formulas.rotate(90*DEGREES)

        for form, bar in zip(formulas, histo.bars):
            form[-2].set_color(C_COLOR)
            form.add_background_rectangle()
            form.next_to(bar.get_top(), UP, buff = 0.15)

        labels = histo.axes.x_labels.copy()
        for label, form in zip(labels, formulas):
            label.generate_target()
            label.target.rotate(90*DEGREES).match_height(form[-2]).move_to(form[-2]).set_color(C_COLOR)

        self.play(
            AnimationGroup(
                LaggedStartMap(MoveToTarget, labels, lag_ratio = 0.1),
                LaggedStartMap(FadeIn, formulas, lag_ratio = 0.1), 
                lag_ratio = 0.3
            ),
            run_time = 4
        )
        self.remove(*labels)
        self.wait()

        self.play(
            LaggedStart(*[Indicate(form[1:], color = RED) for form in formulas], lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()

        self.formulas = formulas

    def probs_sum_up_to_1(self):
        histo, formulas = self.histo, self.formulas

        group = VGroup()
        formulas.generate_target()
        formulas.target.rotate(-90*DEGREES).arrange_submobjects(DOWN, buff = 0.15, aligned_edge = RIGHT).to_edge(LEFT)

        equals = VGroup()
        for form in formulas.target: # added .target
            equal = MathTex("=")
            equal.next_to(form, RIGHT, buff = 0.5)
            equals.add(equal)

        datas = np.array([round(scipy.stats.binom.pmf(x, 10, 0.7), 4) for x in range(0, 10 + 1)])
        results = VGroup()
        for data, equal in zip(datas, equals):
            result = MathTex(str(data))
            result.next_to(equal, RIGHT, buff = 0.5)
            results.add(result)

        result0 = MathTex("0.0000").move_to(results[0], aligned_edge=LEFT)
        result3 = MathTex("0.0090").move_to(results[3], aligned_edge=LEFT)
        results[0] = result0
        results[3] = result3

        braces = VGroup()
        for result in results:
            brace = Brace(VGroup(results[0], result), RIGHT, buff = 0.5, color = GREY)
            braces.add(brace)

        cum_datas = np.array([round(scipy.stats.binom.cdf(x, 10, 0.7), 4) for x in range(0, 10 + 1)])
        cum_results = VGroup()
        for brace, data in zip(braces, cum_datas):
            cum = MathTex(str(data), font_size = 60, color = YELLOW)
            cum.next_to(brace, RIGHT, buff = 0.5)
            cum_results.add(cum)

        # Show binom probability results
        self.play(
            FadeOut(histo),
            MoveToTarget(formulas),
            AnimationGroup(
                LaggedStartMap(FadeIn, equals, shift = LEFT, lag_ratio = 0.1),
                LaggedStartMap(FadeIn, results, shift = LEFT, lag_ratio = 0.1),
                lag_ratio = 0.3
            ),
            run_time = 3
        )
        self.wait()

        cum_brace = braces[0]
        cum_result = cum_results[0]
        self.play(
            Create(cum_brace), 
            Write(cum_result)
        )
        self.wait()

        # Add prob up to 1
        for k in range(1, len(braces)):
            self.play(
                Transform(cum_brace, braces[k]), 
                Transform(cum_result, cum_results[k]), 
                run_time = 0.75
            )
            self.wait(0.25)

        # highlight 1
        self.play(Circumscribe(cum_result, color = YELLOW_D, run_time = 3))
        self.wait()


        # 
        group.add(formulas, equals, results, cum_brace, cum_result)

        self.play(
            group.animate.scale(0.75).shift(RIGHT + UP),
            FadeIn(self.histo)
        )

        histo_one_kwargs = {
            "width": config["frame_width"] - 2, "height": 10/3*(config["frame_height"] - 3.25),
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 1, "y_tick_num": 10,
            "include_h_lines": True, "bar_colors": [RED, GREEN, BLUE, YELLOW]
        }
        histo_one = self.get_histogram(10, 0.7, **histo_one_kwargs)
        histo_one.center().to_edge(DOWN)

        bars = self.histo.bars
        bars.save_state()
        bars.generate_target()
        bars.target.arrange_submobjects(DOWN, buff = 0).next_to(histo.axes.c2p(7.5,0), UP, buff = 0)

        self.play(
            MoveToTarget(bars, lag_ratio = 0.1), 
            run_time = 3
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.shift(10*UP),
            group.animate.shift(9*UP),
            FadeIn(histo_one.axes),
            run_time = 3
        )

        dot = Dot(point = histo_one.axes.c2p(0,1), color = YELLOW_D)
        trace = TracedPath(dot.get_center, dissipating_time=0.5, stroke_width = 4, stroke_color = YELLOW_D, stroke_opacity=[1,0])
        self.add(dot, trace)
        self.play(
            Circumscribe(histo_one.axes.y_labels[-1], color = YELLOW_D, run_time = 3),
            dot.animate(run_time = 3).move_to(histo_one.axes.c2p(11,1)), 
        )
        trace.clear_updaters()
        dot.clear_updaters()
        self.play(FadeOut(dot), FadeOut(trace))
        self.wait()


        self.play(
            Restore(self.camera.frame),
            Restore(bars),
            FadeOut(histo_one.axes),
            run_time = 4
        )
        self.remove(*group)
        self.wait()

    def changing_parameters(self):
        num_line = NumberLine(x_range = [0, 1, 0.25], length = 6, include_numbers=True, decimal_number_config={"num_decimal_places": 2})
        num_line.to_edge(UP, buff = 1)

        label = MathTex("p", "=").next_to(num_line, RIGHT, buff = 0.75)

        p_val = ValueTracker(0.7)
        p_dec = DecimalNumber(p_val.get_value())\
            .next_to(label, RIGHT, aligned_edge=UP)\
            .shift(0.1*UP)

        dot = Dot(point = num_line.n2p(p_val.get_value()), color = PINK, radius = 0.1)
        dot.set_sheen(-0.3, DR)

        self.play(
            Create(num_line, run_time = 2), 
            Write(label), 
            Write(p_dec), 
            FadeIn(dot, shift = DOWN, run_time = 2)
        )
        self.wait()

        p_dec.add_updater(lambda dec: dec.set_value(p_val.get_value()))
        dot.add_updater(lambda d: d.move_to(num_line.n2p(p_val.get_value())))

        histo = self.histo
        histo.p_val = p_val
        histo.n = self.n
        def update_histogram(hist):
            new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
            new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])
            new_bars = hist.get_bars(new_data)
            new_bars.match_style(hist.bars)
            hist.bars.become(new_bars)

        for prop in [0.5, 0.1, 0.4, 0.8]:
            self.play(
                p_val.animate.set_value(prop),
                UpdateFromFunc(histo, update_histogram, suspend_mobject_updating=False),
                run_time = 4.5
            )
            self.wait(0.5)
        self.wait(3)


class NoNeedFor320000Calc(Scene):
    def construct(self):
        panic = Tex("Keine Panik auf der Titanic")
        panic.scale(1.75)
        panic.to_corner(UL)

        rescue = Tex("Rettung naht...")
        rescue.scale(1.25)
        rescue.to_edge(DOWN, buff = 0.5)

        self.play(FadeIn(panic, shift = 5*RIGHT), run_time = 1.5)
        self.wait(0.5)

        self.play(FadeIn(rescue, shift = 5*LEFT), run_time = 1.5)
        self.wait()

        bernoulli = Tex("Bernoulli", "$-$", "Formel")
        bernoulli[0].set_color(BLUE)
        bernoulli[-1].set_color(YELLOW_D)
        def update(mob):
            x = random.uniform(-5,5)
            y = random.uniform(-2.5,2.5)

            bernoulli.move_to(x * RIGHT + y * UP)
            mob.become(bernoulli)

        self.add(bernoulli)
        self.play(
            UpdateFromFunc(bernoulli, update), 
            run_time = 2
        )
        bernoulli.scale(2)
        bernoulli.center()

        brain = SVGMobject(SVG_DIR + "BrainBulb")
        brain.next_to(bernoulli, RIGHT)
        self.play(Create(brain), run_time = 2)
        self.play(Indicate(brain), run_time = 1)
        self.wait(2)


class Thumbnail(HistoScene):
    def construct(self):
        total_calc = 319152
        n = 10
        p = 0.7
        histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] - 3.25,
            "x_tick_freq": 1, "x_label_freq": 1, "y_max_value": 0.3, "y_tick_num": 3,
            "bar_colors": [YELLOW, GREEN, BLUE]
        }
        histo = self.get_histogram(n, p, **histo_kwargs)
        histo.center().to_edge(DOWN)
        self.add(histo)


        calc1 = Tex("$319.152$ ")
        calc1.scale(2.5)
        calc1.move_to(histo.axes.c2p(2.5, 0.25))
        calc1.set_color(RED)

        calc2 = Tex("Wiederholungen?!")
        calc2.set(width = calc1.width + 1)
        calc2.next_to(calc1, DOWN)
        calc2.set_color_by_gradient(RED, WHITE)
        calc2.add_background_rectangle()
        self.add(calc1, calc2)


        arrow = ArcBetweenPoints(
            calc1.get_corner(UR) + 0.25*RIGHT, 
            histo.bars[6].get_top() + 0.2*UP, 
            angle = -90*DEGREES, 
            stroke_width = 6
        )
        arrow.set_color([histo.bars[6].get_color(), RED])
        arrow.add_tip(tip_length = 0.35)
        arrow[-1].set_color(histo.bars[6].get_color())
        self.add(arrow)


        title = Tex("Histogramme")
        title.scale(4)
        title.set_color_by_gradient(YELLOW_E, GREEN, BLUE)
        title.set_stroke(color = WHITE, width = 1)
        title.to_edge(UP, buff = 0.2)
        self.add(title)







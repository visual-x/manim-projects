from manim import *
from BinomHelpers import *
import math


class Compare5Histos(HistoScene):
    def construct(self):
        self.n = 20
        self.p_values = [0.15, 0.30, 0.50, 0.70, 0.85]
        self.p_val = ValueTracker(0.5)

        self.histo_kwargs = {
            "width": config["frame_width"] / 5 - 0.5, "height": config["frame_height"] / 4,
            "include_x_labels": False, "include_y_labels": False, "include_h_lines": False,
            "x_tick_freq": 5, "x_label_freq": 5, "y_max_value": 0.25, "y_tick_num": 5,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }
        self.base_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] * 1/2,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.25, "y_tick_num": 5,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }

        self.introduce_5_histos()
        self.map_prob_with_histos()
        self.symmetrie()
        self.shift_left()
        self.shift_right()


    def introduce_5_histos(self):
        base = self.base = self.get_histogram(self.n, self.p_val.get_value(), **self.base_kwargs)
        base.to_edge(DOWN)

        histo_group = self.histo_group = VGroup(*[self.get_histogram(self.n, p, **self.histo_kwargs) for p in self.p_values])
        histo_group.arrange_submobjects(RIGHT)
        histo_group.shift(UP)

        # all 5 bars
        bars_list = [histo.bars for histo in histo_group]
        self.play(AnimationGroup(*[FadeIn(bar) for bar in bars_list], lag_ratio = 0.1, run_time = 3))
        self.wait()


        n_constant = Tex("$n =$", " konstant", font_size = 72).shift(2.75*LEFT + 2.75*UP)
        p_variable = Tex("$p =$", " variabel", font_size = 72).shift(2.75*RIGHT + 2.68*UP)
        n_text = Tex("Länge der Bernoulli-Kette")
        p_text = Tex("Erfolgswahrscheinlichkeit")

        for text, state in zip([n_text, p_text], [n_constant, p_variable]):
            text.match_width(state)
            text.next_to(state, UP, buff = 0.1)
            text.set_color(GREY)

        self.play(
            AnimationGroup(
                FadeIn(n_constant, shift = 3*RIGHT), 
                FadeIn(n_text, shift = 3*LEFT), 
                lag_ratio = 0.25, run_time = 3
            )
        )
        self.wait()

        # show width (n) 
        h2c1 = self.get_histo_to_compare(1)
        h2c2 = self.get_histo_to_compare(2)
        h2c4 = self.get_histo_to_compare(4)

        com1_x = VGroup(h2c1.axes.x_axis.copy(), h2c1.axes.x_labels.copy())
        com2_x = VGroup(h2c2.axes.x_axis.copy(), h2c2.axes.x_labels.copy())
        com4_x = VGroup(h2c4.axes.x_axis.copy(), h2c4.axes.x_labels.copy())
        
        base_x = VGroup(base.axes.x_axis.copy(), base.axes.x_labels.copy())

        self.play(Create(base_x))
        self.wait()
        self.play(ReplacementTransform(base_x, com2_x), run_time = 2)
        self.wait()

        self.play(Transform(com2_x, com1_x))
        self.wait(0.5)
        self.play(Transform(com2_x, com4_x))
        self.wait(2)
        self.play(FadeOut(com2_x))

        # p is variable
        self.play(
            AnimationGroup(
                FadeIn(p_variable, shift = 3*RIGHT), 
                FadeIn(p_text, shift = 3*LEFT), 
                lag_ratio = 0.25, run_time = 3
            )
        )
        self.wait()


        # rotate_group
        colors = [YELLOW_A, YELLOW_B, YELLOW_C, YELLOW_D, YELLOW_E]
        rg = VGroup(*[MathTex(tex, font_size = 60, color = color) for tex, color in zip(["0.15", "0.30", "0.50", "0.70", "0.85"], colors)])
        rg.arrange_submobjects(RIGHT, buff = 0.75).shift(2*DOWN)
        rg.save_state()

        
        for x, tex in enumerate(rg):
            angle = TAU * x / len(self.p_values)

            tex.set_color(colors[x])
            tex.move_to(np.array([np.cos(angle), np.sin(angle), 0]))
            tex.rotate(angle)
            rg.add(tex)
        rg.shift(2*DOWN)
        rg_center = rg.get_center()


        big_rect = Rectangle(width = 4, height = 4).move_to(rg)
        small_sector = AnnularSector(inner_radius = 0.4, angle=72*DEGREES, start_angle=-36*DEGREES).next_to(rg_center, RIGHT, buff = 0)
        cut = Cutout(big_rect, small_sector)
        cut.set_fill(color = BLACK, opacity = 1)
        cut.set_stroke(width = 0)

        self.add(rg)
        self.add(cut)
        self.wait()

        def rotation_update(mob, dt):
            mob.rotate(angle = -0.75*dt, about_point = rg_center)
        for mob in rg:
            mob.add_updater(rotation_update)
        self.wait(20)


        for mob in rg:
            mob.clear_updaters()
        self.remove(cut)
        self.wait()


        self.n_desc = VGroup(n_constant, n_text)
        self.p_desc = VGroup(p_variable, p_text)
        self.p_texs = rg

    def map_prob_with_histos(self):
        histo_group, n_desc, p_desc, p_texs = self.histo_group, self.n_desc, self.p_desc, self.p_texs

        self.play(
            AnimationGroup(
                n_desc.animate.shift(5*UP),
                p_desc.animate.shift(5*UP),
                lag_ratio = 0.2, run_time = 3
            ),
            AnimationGroup(*[hist.bars.animate.shift(1.5*UP) for hist in histo_group], lag_ratio = 0.1, run_time = 4), 
            Restore(p_texs, lag_ratio = 0.1, run_time = 3)
        )
        for hist in histo_group:            # axes needs to be shifted also, otherwise axes stay at original positition
            hist.axes.shift(1.5*UP)         # while bars moving up --> important for later when circumscribing
        self.wait()


        # Target generation for alle probababilties
        for x, prob in enumerate(p_texs):
            prob.generate_target()
            prob.target.move_to(histo_group[x]).shift(1.05*UP)

        self.play(MoveToTarget(p_texs[2]), run_time = 3)
        self.play(Circumscribe(VGroup(histo_group[2], p_texs[2]), color = p_texs[2].get_color(), fade_out = True, run_time = 3))
        self.wait()

        self.play(
            LaggedStartMap(MoveToTarget, p_texs, lag_ratio = 0.1), 
            run_time = 3
        )
        self.play(
            AnimationGroup(*[
                Circumscribe(VGroup(histo_group[k], p_texs[k]), color = p_texs[k].get_color(), fade_out = True, run_time = 3)
                for k in [0,1,3,4]
            ], lag_ratio = 0.15)
        )
        self.wait()

    def symmetrie(self):
        histo_group, base, p_texs = self.histo_group, self.base, self.p_texs

        self.play(FadeIn(base.axes), run_time = 2)
        self.wait()

        # p_num_lines
        p_hori = NumberLine(x_range = [0,1,0.2], length = 6, include_numbers=True, numbers_to_exclude = [0]).shift(0.8*UP)
        p_vert = self.get_vert_p_line()

        self.play(Create(p_hori), run_time = 2)
        self.wait()

        self.play(ReplacementTransform(p_hori, p_vert), run_time = 4)
        self.wait()

        p_val = ValueTracker(0)
        p_dot = always_redraw(lambda: Dot(point = p_vert.n2p(p_val.get_value()), radius = 0.12, color = PINK).set_sheen(-0.6, UR))

        anims = [p_val.animate(run_time = 5).set_value(0.5)]

        self.add(p_dot)
        self.transform_zeros_into_histo(base, added_anims = anims, **self.base_kwargs)
        self.wait(0.5)
        self.play(Circumscribe(VGroup(histo_group[2], p_texs[2]), color = p_texs[2].get_color(), fade_out = True, run_time = 3))
        self.wait(2)

        # Highlight bars: 10 
        self.highlight_single_bar(base, 10, run_time = 3)

        bools = 10 * [True] + 10 * [False]
        random.shuffle(bools)

        cac = get_checks_and_crosses(bools, width = 10)
        cac.shift (0.6 * UP)
        self.play(LaggedStartMap(FadeIn, cac, shift = 0.5*DOWN, lag_ratio = 0.05), run_time = 2)
        self.wait()


        self.play(                                                          # fade_out those who are checks
            AnimationGroup(*[                                               # using positive attribute
                FadeOut(check.copy(), target_position = base.axes.x_labels[2], scale = 0.25) 
                for check in cac if check.positive
            ], lag_ratio = 0.1, run_time = 3)
        )
        self.wait()


        # Highlight bars: 9 2nd
        # turn a positive into negative
        positive = [check for check in cac if check.positive]
        negative = [cross for cross in cac if not cross.positive]


        sur_rect = SurroundingRectangle(positive[2], color = YELLOW)
        self.play(FadeIn(sur_rect, scale = 1.5))
        self.wait(0.5)

        neg_copy = negative[0].copy()
        neg_copy.next_to(sur_rect, DOWN)
        self.play(DrawBorderThenFill(neg_copy))
        self.highlight_single_bar(base, 9, run_time = 2)
        self.play(LaggedStartMap(FadeOut, VGroup(neg_copy, sur_rect), lag_ratio = 0.2))
        self.wait()

        # turn a negative into positive
        sur_rect = SurroundingRectangle(negative[3], color = YELLOW)
        self.play(FadeIn(sur_rect, scale = 1.5))
        self.wait(0.5)

        pos_copy = positive[0].copy()
        pos_copy.next_to(sur_rect, DOWN)
        self.play(DrawBorderThenFill(pos_copy))
        self.highlight_single_bar(base, 11, run_time = 2)
        self.play(LaggedStartMap(FadeOut, VGroup(pos_copy, sur_rect), lag_ratio = 0.2))
        self.wait()

        # highlight bars symmetric
        start, end = 9, 11
        for k in range(6):
            if k == 1:
                added_anim = [ShrinkToCenter(cac, lag_ratio = 0.05)]
            else:
                added_anim = []
            self.highlight_group_of_bars(base, start, end, added_anims=added_anim, run_time = 1.5)
            start -= 1
            end += 1

        self.highlight_group_of_bars(base, 0, 20, added_anims=added_anim, run_time = 1)
        self.wait(2)

        self.p_val, self.p_dot, self.p_vert = p_val, p_dot, p_vert

    def shift_left(self):
        histo_group, p_texs = self.histo_group, self.p_texs
        base, p_val, p_dot = self.base, self.p_val, self.p_dot


        # add base as a reference
        ref_mid = base.bars.copy()
        ref_mid.set_fill(opacity = 0)
        self.bring_to_back(ref_mid)

        self.ref_bars = VGroup()
        self.ref_bars.add(ref_mid)


        base.p_val = p_val
        base.n = self.n
        # def update_histogram(hist):
        #     new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
        #     new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])

        #     new_bars = hist.get_bars(new_data)
        #     new_bars.match_style(hist.bars)
        #     hist.bars.become(new_bars)

        self.play(Circumscribe(VGroup(histo_group[1], p_texs[1]), color = p_texs[1].get_color(), run_time = 1.5)) # fade_out = True,
        self.play(FocusOn(p_dot))

        self.play(
            p_val.animate.set_value(self.p_values[1]),
            UpdateFromFunc(base, self.update_histogram, suspend_mobject_updating=False),
            run_time = 6
        )
        self.wait()

        # checks and crosses
        bools1 = 10 * [True] + 10 * [False]
        bools2 =  6 * [True] + 14 * [False]
        cac1 = get_checks_and_crosses(bools1, width = 8).shift(0.6*UP + 1.5*RIGHT)
        cac2 = get_checks_and_crosses(bools2, width = 8).move_to(cac1)

        brace1 = Brace(cac1[10:], DOWN)
        text1 = MathTex("=", "10").next_to(brace1, DOWN, buff = 0.1)

        brace2 = Brace(cac2[6:], DOWN)
        text2 = MathTex("=", "14").next_to(brace2, DOWN, buff = 0.1)

        self.play(
            LaggedStartMap(FadeIn, cac1, shift = 0.5*DOWN, lag_ratio = 0.1),
            run_time = 1.5
        )
        self.play(
            Create(brace1), 
            FadeIn(text1, shift = LEFT),
            run_time = 1.5
        )
        self.wait()
        self.play(
            ReplacementTransform(cac1, cac2), 
            ReplacementTransform(brace1, brace2), 
            ReplacementTransform(text1, text2)
        )
        self.wait()


        self.play(                                                          # fade_out those who are checks
            AnimationGroup(*[                                               # using positive attribute
                FadeOut(check, target_position = base.axes.c2p(6, -0.025), scale = 0.25) 
                for check in cac2 if check.positive
            ], lag_ratio = 0.1, run_time = 3), 
            AnimationGroup(*[
                FadeOut(check, scale = 0.25) 
                for check in cac2 if not check.positive
            ], lag_ratio = 0.1, run_time = 3),
            FadeOut(text2, run_time = 2),
            FadeOut(brace2, run_time = 2),
        )
        self.wait()

        # Arrows indicating smaller p --> smaller E[X]
        arrow_down = Arrow(1.5*UP, 1.5*DOWN, color = YELLOW_B).next_to(self.p_vert, LEFT)
        arrow_left = Arrow(1.5*RIGHT, 1.5*LEFT, color = YELLOW_B).move_to(base.axes.c2p(8, 0.125))
        self.play(GrowArrow(arrow_down), run_time = 2)
        self.wait()
        self.play(ReplacementTransform(arrow_down, arrow_left))
        self.wait(2)
        self.play(FadeOut(arrow_left))
        self.wait()

        # setting p = 0.15
        self.play(
            p_val.animate.set_value(self.p_values[0]),
            UpdateFromFunc(base, self.update_histogram, suspend_mobject_updating=False),
            run_time = 6
        )
        self.play(Circumscribe(VGroup(histo_group[0], p_texs[0]), color = p_texs[0].get_color(), run_time = 1.5)) # fade_out = True,
        self.wait(3)

        # add to ref_group
        ref_left = base.bars.copy()
        ref_left.set_fill(opacity = 0)
        self.bring_to_back(ref_left)

        self.ref_bars.add(ref_left)

    def shift_right(self):
        histo_group, p_texs = self.histo_group, self.p_texs
        base, p_val, p_dot = self.base, self.p_val, self.p_dot


        self.play(
            Circumscribe(VGroup(histo_group[3], p_texs[3]), color = p_texs[3].get_color(), run_time = 1.5),
            Circumscribe(VGroup(histo_group[4], p_texs[4]), color = p_texs[4].get_color(), run_time = 1.5),
        )
        self.wait()

        self.play(
            p_val.animate.set_value(self.p_values[-1]), 
            UpdateFromFunc(base, self.update_histogram, suspend_mobject_updating=False), 
            run_time = 9
        )
        self.wait()

        self.highlight_group_of_bars(base, 15, 20, run_time = 3)
        self.wait()
        self.highlight_group_of_bars(base, 0, 14, run_time = 3)
        self.wait()
        self.highlight_group_of_bars(base, 0, 20, run_time = 3)
        self.wait()

        ref_right = base.bars.copy()
        ref_right.set_fill(opacity = 0)
        self.bring_to_back(ref_right)

        self.ref_bars.add(ref_right)

        self.play(
            p_val.animate.set_value(self.p_values[0]), 
            UpdateFromFunc(base, self.update_histogram, suspend_mobject_updating=False), 
            rate_func = there_and_back, run_time = 12
        )
        self.wait(3)


    # functions
    def get_histo_to_compare(self, number):
        histo_to_compare = self.get_histogram(
            self.n, 0.5, 
            width = self.histo_kwargs["width"], height = self.histo_kwargs["height"],
            x_tick_freq = self.base_kwargs["x_tick_freq"], x_label_freq = self.histo_kwargs["x_label_freq"], 
            y_max_value = self.histo_kwargs["y_max_value"], y_tick_num = self.histo_kwargs["y_tick_num"], 
            bar_colors = self.histo_kwargs["bar_colors"],
            include_x_labels = True, include_y_labels = True, include_h_lines = False,
        )
        histo_to_compare.move_to(self.histo_group[number])\
            .shift(0.37*LEFT)\
            .shift(0.135*DOWN)

        return histo_to_compare

    def get_vert_p_line(self):
        num_line = NumberLine(
            x_range = [0,1,0.2], length = self.base_kwargs["height"], include_numbers=True,
            tick_size = 0, numbers_to_exclude = [0],
            rotation = 90*DEGREES, label_direction = RIGHT
        )
        num_line.next_to(self.base.axes.c2p(self.n + 1, 0), UR, buff = 0)

        return num_line

    def update_histogram(self, hist):
        new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
        new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)


class CollectKeyPoints(HistoScene):
    def construct(self):
        histo_kwargs = {
            "width": config["frame_width"] / 4 - 0.5, "height": config["frame_height"] / 4,
            "include_x_labels": True, "include_y_labels": False, "include_h_lines": True,
            "x_tick_freq": 5, "x_label_freq": 5, "y_max_value": 0.24, "y_tick_num": 4,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }

        title = Title("Eigenschaften der Binomialverteilung")
        title.set_color(LIGHT_GREY)
        options = VGroup(*[
            MathTex(*tex, font_size = 60) for tex in 
            [["p", "<", "0.5"], ["p", "=", "0.5"], ["p", ">", "0.5"]]
        ])
        options.arrange(RIGHT, buff = 2.5)
        options.next_to(title, DOWN, buff = 0.5)
        for option in options:
            option[1].set_color(YELLOW_D)


        histos = VGroup(*[self.get_histogram(n = 20, p = p_val, **histo_kwargs) for p_val in [0.2, 0.5, 0.8]])
        for histo, option in zip(histos, options):
            histo.next_to(option, DOWN)
            histo.to_edge(DOWN)

        # key points
        kp0 = BulletedList("Verteilung rutscht \\\\nach links", "wahrscheinlicher:\\\\ weniger Erfolge")
        kp1 = BulletedList("Verteilung ist\\\\ symmetrisch", "wahrscheinlicher:\\\\ links $\\hat{=}$ rechts")
        kp2 = BulletedList("Verteilung rutscht \\\\nach rechts", "wahrscheinlicher:\\\\ mehr Erfolge")
        for kp, option in zip([kp0, kp1, kp2], options):
            kp.scale(0.75)
            kp.next_to(option, DOWN, buff = 0.5)



        # p = 0.5
        self.add(title, options[1])
        self.wait()

        self.play(FadeIn(histos[1]), run_time = 1.5)
        self.play(FadeIn(kp1, shift = 2*LEFT, lag_ratio = 0.1), run_time = 1.5)
        self.wait(2)


        # p < 0.5
        self.play(FocusOn(options[0], run_time = 1.5))
        self.play(Write(options[0]))
        self.wait(2)

        self.play(
            FadeIn(histos[0]), 
            FadeIn(kp0, shift = 2*RIGHT, lag_ratio = 0.1),
            run_time = 1.5
        )
        self.wait(2)


        # p > 0.5
        self.play(Write(options[2]))
        self.play(
            FadeIn(histos[2]), 
            FadeIn(kp2, shift = 2*RIGHT, lag_ratio = 0.1),
            run_time = 1.5
        )
        self.wait(3)


class WheelOfFortune(HistoScene):
    def construct(self):
        self.n, self.p = 10, 1/3

        self.histo_kwargs = {
            "width": config["frame_width"] / 3 - 1.5, "height": config["frame_height"] / 4,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.3, "y_tick_num": 3,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }

        histo_group = self.histo_group = VGroup(*[self.get_histogram(self.n, p, **self.histo_kwargs) for p in [0.2, 0.75, 1/3]])
        histo_group.arrange_submobjects(RIGHT)
        histo_group.shift(1.5*DOWN)

        wheel = self.get_wheel()
        wheel.to_edge(UP)

        title = self.get_title()
        title.to_corner(UL)

        n_group = self.get_n_text_group()
        n_group.to_corner(UR)


        c = Tex(CMARK_TEX, color = C_COLOR, font_size = 72, tex_template = myTemplate)
        x = Tex(XMARK_TEX, color = X_COLOR, font_size = 72, tex_template = myTemplate)
        cx = VGroup(c,x)\
            .arrange(RIGHT, buff = 2)\
            .next_to(title, DOWN, buff = 0.65, aligned_edge=LEFT)\
            .shift(0.5*RIGHT)

        self.play(
            Write(title), 
            FadeIn(wheel, shift = 2*UP), 
            run_time = 2
        )
        self.wait()

        self.play(
            Rotate(wheel.arrow, angle = (3*360 - 30)*DEGREES, about_point = wheel.get_center(), rate_func = slow_into, run_time = 3.5),
            DrawBorderThenFill(cx[0], rate_func = squish_rate_func(smooth, 0.6, 1), run_time = 3.5)
        )
        succ = wheel.copy()
        succ.generate_target()
        succ.target.scale(0.3).next_to(c, DOWN)
        self.play(MoveToTarget(succ), run_time = 3)
        self.wait()


        self.play(
            Rotate(wheel.arrow, angle = (3*360 + 126)*DEGREES, about_point = wheel.get_center(), rate_func = slow_into, run_time = 3.5), 
            DrawBorderThenFill(cx[1], rate_func = squish_rate_func(smooth, 0.6, 1), run_time = 3.5)
        )
        fail = wheel.copy()
        fail.generate_target()
        fail.target.scale(0.3).next_to(x, DOWN)
        self.play(MoveToTarget(fail), run_time = 3)
        self.wait()

        self.play(Write(n_group), run_time = 2)
        self.wait()


        zv = Tex("$X$", "$-$", "$\\#$", CMARK_TEX, font_size = 72, tex_template = myTemplate)
        zv[-2:].set_color(C_COLOR)
        zv.next_to(n_group, DOWN, buff = 1)
        self.play(Write(zv), run_time = 2)
        self.wait()


        histo_zero_group = VGroup(*[self.get_histogram(self.n, p, zeros = True, **self.histo_kwargs) for p in [0.2, 0.75, 1/3]])
        histo_zero_group.arrange_submobjects(RIGHT)
        histo_zero_group.shift(1.5*DOWN)

        self.play(
            AnimationGroup(
                *[Create(hist.axes) for hist in histo_group],
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.play(
            AnimationGroup(
                *[ReplacementTransform(hist.bars, zero.bars) for zero, hist in zip(histo_group, histo_zero_group)], 
                lag_ratio = 0.1
            ),
            run_time = 4
        )
        self.wait()

        choices = VGroup(*[
            MathTex(tex, color = YELLOW_D, font_size = 72).next_to(hist, DOWN) 
            for tex, hist in zip(["(1)", "(2)", "(3)"], histo_group)
        ])
        self.play(
            LaggedStartMap(FadeIn, choices, shift = DOWN, scale = 0.25, lag_ratio = 0.2), 
            run_time = 3
        )
        self.wait(5)

    # functions 
    def get_wheel(self):
        succ_sector = Sector(outer_radius = 1.5, angle = 120*DEGREES, start_angle = -30*DEGREES)\
            .set_fill(color = WHITE, opacity = 0.5)\
            .set_stroke(width = 1)
        fail_sector = Sector(outer_radius = 1.5, angle = 240*DEGREES, start_angle =  90*DEGREES)\
            .set_fill(opacity = 0)\
            .set_stroke(width = 1)
        dot = Dot()
        arrow = Arrow(DOWN, UP, stroke_width = 8, color = YELLOW_D).move_to(dot)

        wheel = VGroup(succ_sector, fail_sector, arrow, dot)
        wheel.arrow = arrow
        wheel.s_sector = succ_sector
        wheel.f_sector = fail_sector

        return wheel

    def get_title(self):
        title = Tex("Glücksrad")\
            .scale(1.5)
        uline = Underline(title, color = GREY)

        return VGroup(title, uline)

    def get_n_text_group(self):
        n_num = MathTex("n = 10", font_size = 96)
        n_tex = Tex("Länge der Bernoulli-Kette")\
            .set(width = 5)\
            .next_to(n_num, UP, buff = 0.15, aligned_edge=RIGHT)\
            .set_color(GREY)

        result = VGroup(n_num, n_tex)
        result.num = n_num

        return result


class Conclusion1(HistoScene):
    def construct(self):
        self.n = 50
        self.p = 0.5
        self.p_val = ValueTracker(self.p)
        self.n_val = ValueTracker(self.n)

        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] * 2/5,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.20, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(DOWN)

        n_tex = Tex("Länge der Bernoulli-Kette")\
            .set(width = 5)\
            .to_corner(UL)\
            .set_color(GREY)
        n_dec = DecimalNumber(self.n_val.get_value(), num_decimal_places=0, font_size = 72)\
            .next_to(n_tex, DOWN, aligned_edge=LEFT)\
            .add_updater(lambda dec: dec.set_value(self.n_val.get_value()))
        n_num = MathTex("= n", font_size = 72)\
            .next_to(n_dec, RIGHT)\
            .shift(0.08*DOWN)
        self.n_group = VGroup(n_tex, n_num, n_dec)

        p_tex = Tex("Erfolgswahrscheinlichkeit")\
            .match_height(n_tex)\
            .to_corner(UR)\
            .set_color(GREY)
        p_dec = DecimalNumber(self.p_val.get_value(), edge_to_fix=RIGHT, font_size = 72)\
            .next_to(p_tex, DOWN, aligned_edge=RIGHT)\
            .add_updater(lambda dec: dec.set_value(self.p_val.get_value()))
        p_num = MathTex("p = ", font_size = 72)\
            .next_to(p_dec, LEFT)\
            .shift(0.18*DOWN)
        self.p_group = VGroup(p_tex, p_num, p_dec)

        p_line = self.get_vert_p_line()
        p_dot = always_redraw(lambda: Dot(point = p_line.n2p(self.p_val.get_value()), radius = 0.12, color = PINK).set_sheen(-0.6, UR))

        self.add(histo.axes)
        self.add(n_tex, n_num, n_dec)
        self.add(p_tex, p_num, p_dec)
        self.add(p_line, p_dot)
        self.wait()


        self.symmetrie()
        self.shift_left()
        self.shift_right()


    def symmetrie(self):
        histo, p_group, n_group = self.histo, self.p_group, self.n_group

        # bring back bars
        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = rect_color) for mob, rect_color in 
            zip([p_group, n_group], [C_COLOR, BLUE])
        ])
        self.play(Create(sur_rects[0]), run_time = 1.5)
        self.wait()
        self.play(Transform(sur_rects[0], sur_rects[1]), run_time = 2)
        self.wait()
        self.play(FadeOut(sur_rects[0]))


        zeros = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        zeros.to_edge(DOWN)

        self.play(ReplacementTransform(zeros.bars, histo.bars), run_time = 3)
        self.wait()

        # Symmetrie
        con1 = self.con1 = Tex("Symmetrie", font_size = 72, color = YELLOW_D).move_to(1.5*UP)
        con1_rect = SurroundingRectangle(con1, color = BLUE)
        self.play(Write(con1))
        self.play(FadeIn(con1_rect, scale = 1.5))

        bar25_copy = histo.bars[25].copy()
        self.play(Transform(con1_rect, bar25_copy), run_time = 3)
        self.wait()

        calc = MathTex("50", "\cdot", "0.5", font_size = 60).next_to(con1, UP)
        self.play(
            AnimationGroup(
                FadeIn(calc[0], shift = 3*RIGHT, scale = 0.1), 
                FadeIn(calc[1], shift = 3*DOWN),
                FadeIn(calc[2], shift = 3*LEFT, scale = 0.1),
                lag_ratio = 0.1 
            ), 
            run_time = 2
        )
        self.wait()
        result = MathTex("25", font_size = 60).move_to(calc)
        self.play(FadeTransform(calc, result))
        self.wait()

        self.play(
            FadeOut(con1_rect), 
            FadeOut(result)
        )
        self.wait()

    def shift_left(self):
        histo, p_val = self.histo, self.p_val

        con2 = self.con2 = Tex("Verschiebung nach links", font_size = 72, color = YELLOW_D).move_to(1.5*UP)
        con2_rect = SurroundingRectangle(con2, color = histo.bars[5].get_color())

        histo.p_val = self.p_val
        histo.n = self.n
        self.play(
            p_val.animate.set_value(0.1), 
            UpdateFromFunc(histo, self.update_histogram, suspend_mobject_updating=False),
            ReplacementTransform(self.con1, con2, rate_func = squish_rate_func(smooth, 0.75, 1)),
            run_time = 6
        )
        self.wait()


        calc = MathTex("50", "\cdot", "0.1", font_size = 60).next_to(con2, UP)
        self.play(
            AnimationGroup(
                FadeIn(calc[0], shift = 3*RIGHT, scale = 0.1), 
                FadeIn(calc[1], shift = 3*DOWN),
                FadeIn(calc[2], shift = 3*LEFT, scale = 0.1),
                lag_ratio = 0.1 
            ), 
            run_time = 2
        )
        self.wait()
        result = MathTex("5", font_size = 60).move_to(calc)
        self.play(
            FadeTransform(calc, result), 
            FadeIn(con2_rect, run_time = 2)
        )
        self.wait()

        bar5_copy = histo.bars[5].copy()
        self.play(Transform(con2_rect, bar5_copy), run_time = 3)
        self.wait()

        self.play(
            FadeOut(con2_rect), 
            FadeOut(result)
        )
        self.wait()

    def shift_right(self):
        histo, p_val = self.histo, self.p_val

        con3 = self.con3 = Tex("Verschiebung nach rechts", font_size = 72, color = YELLOW_D).move_to(1.5*UP)
        self.play(
            p_val.animate.set_value(0.7), 
            UpdateFromFunc(histo, self.update_histogram, suspend_mobject_updating=False),
            ReplacementTransform(self.con2, con3, rate_func = squish_rate_func(smooth, 0.75, 1)),
            run_time = 6
        )
        self.wait()

        con3_rect = SurroundingRectangle(con3, color = histo.bars[35].get_color())
        calc = MathTex("50", "\cdot", "0.7", font_size = 60).next_to(con3, UP)
        self.play(
            AnimationGroup(
                FadeIn(calc[0], shift = 3*RIGHT, scale = 0.1), 
                FadeIn(calc[1], shift = 3*DOWN),
                FadeIn(calc[2], shift = 3*LEFT, scale = 0.1),
                lag_ratio = 0.1 
            ),
            run_time = 2
        )
        self.wait()
        result = MathTex("35", font_size = 60).move_to(calc)
        self.play(
            FadeTransform(calc, result), 
            FadeIn(con3_rect)
        )

        bar35_copy = histo.bars[35].copy()
        self.play(Transform(con3_rect, bar35_copy), run_time = 3)
        self.wait()

        self.play(
            FadeOut(con3_rect), 
            FadeOut(result)
        )
        self.wait(3)

        self.play(FadeOut(con3, shift = 2*DOWN, scale = 0.1))
        self.wait()


        histo.p = 0.7
        histo.n_val = self.n_val
        self.play(
            self.n_val.animate.set_value(10), 
            UpdateFromFunc(histo, self.update_histogram_n, suspend_mobject_updating=False),
            run_time = 6
        )
        self.wait()

    # functions
    def get_vert_p_line(self):
        num_line = NumberLine(
            x_range = [0,1,0.2], length = self.histo_kwargs["height"], include_numbers=True,
            tick_size = 0.1, numbers_to_exclude = [0],
            rotation = 90*DEGREES, label_direction = RIGHT
        )
        num_line.next_to(self.histo.axes.c2p(self.n + 1, 0), UR, buff = 0)
        num_line.shift(0.1*LEFT)
        return num_line

    def update_histogram(self, hist):
        new_dist = scipy.stats.binom(hist.n, hist.p_val.get_value())
        new_data = np.array([new_dist.pmf(x) for x in range(0, hist.n + 1)])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)

    def update_histogram_n(self, hist):     # this is wrong --> bars verschwinden irgendwann????
        new_data = np.array([
            scipy.stats.binom.pmf(x, int(hist.n_val.get_value()), hist.p) 
            for x in range(0, int(hist.n_val.get_value()) + 1)
        ])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)


class Thumbnail(HistoScene):
    def construct(self):
        self.n = 50
        self.p = 0.5

        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] * 2/5,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.20, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(DOWN)

        histos = VGroup(*[self.get_histogram(n = 50, p = p_val, **self.histo_kwargs) for p_val in [0.12, 0.5, 0.88]])
        histos.to_edge(DOWN)

        self.add(histo.axes, *[histos[x].bars for x in range(3)])


        # title = Tex("Histogramme", font_size = 72)
        # title.to_corner(UL)


        np1 = self.get_np_group(p = 0.5, color = YELLOW_A)
        np2 = self.get_np_group(p = 0.8, color = BLUE_A)
        np3 = self.get_np_group(p = 0.2, color = RED_A)

        nps = VGroup(np1, np2, np3)
        nps.arrange(RIGHT, buff = 3)
        nps.to_edge(UP)


        arrows = VGroup()
        points = [4*LEFT, 0.75*DOWN, 4*RIGHT]
        for group in nps:
            for point in points:
                arrow = Arrow(group.get_bottom() + 0.1*DOWN, point, buff = 0.1, stroke_width = 3, tip_length = 0.2)
                arrow.set_fill(opacity = 0.6)
                arrow.set_stroke(opacity = 0.6)
                arrows.add(arrow)

        arrows[0:3].set_color(YELLOW_A)
        arrows[3:6].set_color(BLUE_A)
        arrows[6:9].set_color(RED_A)



        title = Tex("Einfluss der Erfolgswahrscheinlichkeit $p$")
        title.set(width = config["frame_width"] - 1)
        title.move_to(arrows)
        title.shift(0.5*UP)
        title.add_background_rectangle(
            buff = 0.1, stroke_color = GREEN, stroke_width=4, stroke_opacity=1,
        )


        self.add(nps, arrows, title)

    def get_np_group(self, p, color, n = 50):

        n_tex = MathTex("n", "=", str(n), font_size = 60, color = GREY)
        p_tex = MathTex("p", "=", str(p), font_size = 60, color = color)

        result = VGroup(n_tex, p_tex)
        result.arrange(DOWN, aligned_edge = LEFT)

        return result




# ##############
# VIDEO 2 


# shit doesn't work

class UpdateHisto(HistoScene):
    def construct(self):
        self.n, self.p = 50, 0.5

        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] * 2/5,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.20, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED]
        }
        histo = self.histo = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        histo.to_edge(DOWN)


        dist = scipy.stats.binom(self.n, self.p)
        data = np.array([dist.pmf(x) for x in range(0, self.n + 1)])
        bars = histo.get_bars(data)

        n_val = ValueTracker(50)

        self.add(histo, bars)
        self.wait()

        histo.n_val = n_val
        histo.p = self.p

        self.play(
            UpdateFromFunc(histo, self.update_histogram_n), 
            n_val.animate.__iadd__(-10), 
            run_time = 2
        )
        self.wait()

    def update_histogram_n(self, hist):     # this is wrong --> bars verschwinden irgendwann????
        new_dist = scipy.stats.binom(hist.n_val.get_value(), hist.p)
        new_data = np.array([new_dist.pmf(x) for x in range(0, int(hist.n_val.get_value()) + 1)])

        new_bars = hist.get_bars(new_data)
        new_bars.match_style(hist.bars)
        hist.bars.become(new_bars)








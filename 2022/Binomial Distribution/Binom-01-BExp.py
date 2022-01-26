from manim import *
from BinomHelpers import *
import random




class ManDontGetAngry(Scene):
    def construct(self):
        self.color1, self.color2 = BLUE, YELLOW

        self.game_setup()
        self.initialize_game()
        self.restore_game()

    def game_setup(self):
        path = VMobject()
        path.set_points_as_corners([
            2*UP, 4*RIGHT + 2*UP, 4*RIGHT, ORIGIN, 4*DOWN, 4*DOWN + 2*LEFT, 2*LEFT, 6*LEFT, 6*LEFT + 2*UP, 2*LEFT + 2*UP
        ])
        path.center()
        path.to_edge(UP)

        circles = VGroup()
        for i in range(31):
            circ = Circle(radius = 0.3, stroke_color = GREY)
            circ.move_to(path.point_from_proportion(i/30))
            circles.add(circ)

        circles[6].set_fill(color = self.color1, opacity = 0.25).set_stroke(color = self.color1)
        circles[16].set_fill(color = self.color2, opacity = 0.25).set_stroke(color = self.color2)

        house1 = VGroup(*[Circle(radius = 0.3, stroke_color = self.color1) for _ in range(4)])
        for h, c in zip(house1, [*circles[0:4]]):
            h.next_to(c, DOWN)
            h.align_to(circles[5], DOWN)

        house2 = VGroup(*[Circle(radius = 0.3, stroke_color = self.color2) for _ in range(4)])
        for h, c in zip(house2, [*circles[10:14]]):
            h.next_to(c, LEFT)
            h.align_to(circles[15], LEFT)

        players1 = VGroup(*[Circle(radius = 0.3, fill_color = self.color1, fill_opacity = 1, stroke_color = self.color1) for _ in range(4)])
        players1.arrange_in_grid(2, 2, buff = 0.4)
        players1.next_to(circles.get_corner(DR), UL, buff = 0)

        players1_start = players1.copy()\
            .set_fill(opacity = 0.25)\
            .set_stroke(color = self.color1)

        players2 = VGroup(*[Circle(radius = 0.3, fill_color = self.color2, fill_opacity = 1, stroke_color = self.color2) for _ in range(4)])
        players2.arrange_in_grid(2, 2, buff = 0.4)
        players2.next_to(circles.get_corner(DL), UR, buff = 0)

        players2_start = players2.copy()\
            .set_fill(opacity = 0.25)\
            .set_stroke(color = self.color2)

        self.circles, self.house1, self.house2 = circles, house1, house2
        self.players1, self.players2 = players1, players2
        self.players1_start, self.players2_start = players1_start, players2_start

    def initialize_game(self):
        circles, house1, house2 = self.circles, self.house1, self.house2
        players1, players2 = self.players1, self.players2
        # self.add(circles, house1, house2, players1_start, players1, players2_start, players2)
        self.play(
            AnimationGroup(*[GrowFromCenter(circ) for circ in circles], lag_ratio = 0.1), 
            FadeIn(house1, shift = 8*RIGHT), 
            FadeIn(house2, shift = 8*DOWN), 
            DrawBorderThenFill(players1, lag_ratio = 0.2), 
            DrawBorderThenFill(players2, lag_ratio = 0.2), 
            run_time = 6
        )
        self.bring_to_back(self.players1_start, self.players2_start)
        self.wait()

        title = Tex("Mensch, ", "ärgere \\\\", "Dich nicht!")
        title.set(width = config["frame_width"] - 2)
        title.add_background_rectangle(buff = 0.3, opacity = 0.8)

        self.play(
            Create(title[0]), 
            Write(title[1:]), 
        )
        self.wait()
        self.play(FadeToColor(title[2], color = RED), run_time = 2)
        self.wait()
        self.play(ShrinkToCenter(title))
        self.wait()

        # yellow figures to places
        fig_tex = Tex("Spielfiguren")\
            .next_to(players2, DOWN, aligned_edge=LEFT)

        self.play(
            Write(fig_tex, run_time = 1),
            Circumscribe(players2, color = self.color2, fade_out=True, run_time = 2)
        )
        self.wait()

        for player, house in zip(players2, [*house2[:3], circles[14]]):
            player.save_state()
            player.generate_target()
            player.target.move_to(house)

        self.play(
            AnimationGroup(*[MoveToTarget(player) for player in players2[:3]], lag_ratio = 0.2),
            run_time = 3
        )
        self.play(MoveToTarget(players2[-1]), run_time = 2)
        self.wait()

        die_group = get_die_faces(dot_color = RED)
        die_group.scale(0.65).to_edge(RIGHT)
        self.play(FadeIn(die_group, lag_ratio = 0.1))

        arcs2 = VGroup(*[
            CurvedArrow(circles[start_index].get_center(), end.get_center(), angle = -TAU/4, color = RED) 
            for start_index, end in zip([14, 15], [circles[15], house2[-1]])
        ])
        self.play(
            Create(arcs2, lag_ratio = 0.5),
            die_group[1].animate(rate_func = there_and_back).shift(0.5*DOWN),
            run_time = 2
        )
        self.wait()
        self.play(FadeOut(arcs2, shift = 3*DOWN))
        self.wait()

        # blue figures to places
        self.play(
            fig_tex.animate.next_to(players1, DOWN, aligned_edge = RIGHT),
            Circumscribe(players1, color = self.color1, fade_out = True),
            run_time = 3
        )
        for player, house in zip(players1, [*house1[:3], circles[8]]):
            player.generate_target()
            player.target.move_to(house)

        self.play(
            AnimationGroup(*[MoveToTarget(player) for player in players1[:3]], lag_ratio = 0.2),
            run_time = 3
        )
        self.play(MoveToTarget(players1[-1]), run_time = 2)
        self.wait()

        # blue kills yellow
        player1 = players1[-1]
        steps = [2*LEFT, 4*DOWN]# [2*LEFT, 4*UP, 4*LEFT, 2*UP, 4*RIGHT, 4*UP]
        rts = [1, 2] #[1, 2, 2, 1, 2, 2]
        trace = TracedPath(player1.get_center, stroke_color = RED, stroke_width = 5, stroke_opacity = [0.2, 1, 0.2], dissipating_time = 0.75)
        self.add(trace)
        for step, rt in zip(steps, rts):
            self.play(player1.animate(rate_func = linear).shift(step), run_time = rt)

        self.play(
            die_group[-1].animate(rate_func = there_and_back).shift(0.5*DOWN),
            run_time = 2
        )
        self.play(Restore(players2[-1]), run_time = 2)
        self.wait()

        # blue runs the whole round
        steps = [2*LEFT, 4*UP, 4*LEFT, 2*UP, 4*RIGHT, 4*UP]
        rts = [1, 2, 2, 1, 2, 2]
        for step, rt in zip(steps, rts):
            self.play(player1.animate(rate_func = linear).shift(step), run_time = rt)
        self.wait(2)
        self.remove(fig_tex)

        self.die_group = die_group

    def restore_game(self):
        circles, die_group = self.circles, self.die_group
        players1, players2 = self.players1, self.players2


        player1, player2 = players1[-1], players2[-1]
        player1.move_to(circles[8]).save_state()
        player2.move_to(circles[14]).save_state()
        self.wait(3)

        rect = SurroundingRectangle(die_group[-1], buff = 0.05, color = C_COLOR)
        self.play(Create(rect), run_time = 2)
        self.wait()

        arrow = Arrow(ORIGIN, UP, color = WHITE)
        arrow.next_to(die_group[-1], DOWN)
        self.play(GrowArrow(arrow), run_time = 2)
        self.wait()

        result_list = [0]
        def animate_arrow(arrow):
            num_arrow = random.randint(1, 6)
            arrow.next_to(die_group[num_arrow - 1], DOWN)
            result_list[0] = num_arrow

        self.play(UpdateFromFunc(arrow, animate_arrow), run_time = 4)
        self.wait()

        result = result_list[0]

        if result == 2 or result == 1:
            self.play(player1.animate(rate_func=linear).shift(result * LEFT), run_time = result)

        elif result > 2:
            self.play(player1.animate(rate_func=linear).shift(2 * LEFT), run_time = 2)
            diff = result - 2
            self.play(player1.animate(rate_func=linear).shift(diff * DOWN), run_time = diff)
        self.wait()

        self.play(rect.animate.move_to(die_group[(6 - result) - 1]), run_time = 3)
        self.wait()

        self.play(UpdateFromFunc(arrow, animate_arrow), run_time = 4)
        self.wait()


class IntroduceTerms(MovingCameraScene):
    def construct(self):
        
        self.show_all_outcomes()
        self.propability()
        self.bernoulli()

    def show_all_outcomes(self):
        df_fail = VGroup(*[get_die_face(number) for number in range(1, 6)])\
            .arrange_submobjects(RIGHT)
        df_succ = get_die_face(6)\
            .next_to(df_fail, RIGHT, buff = 0.5)\
            .save_state()

        df = VGroup(df_fail, df_succ).center()
        df_succ.next_to(df_fail, RIGHT)

        outcome_text = Tex("Ergebnisse")\
            .next_to(df_fail, LEFT, buff = 0.5)

        # present alle possible outcomes and rearrange them
        self.play(
            FadeIn(outcome_text, shift = RIGHT),
            FadeIn(VGroup(*df_fail, df_succ), shift = 1.5*DOWN, lag_ratio = 0.1),
            run_time = 2
        )
        self.wait()

        self.play(Restore(df_succ), run_time = 3)
        self.wait()

        # introduce useful names
        braces = VGroup(*[Brace(die_faces, DOWN, color = GREY) for die_faces in df])
        braces_texts = VGroup(*[
            Tex(tex, color = tex_color).next_to(brace, DOWN) 
            for tex, tex_color, brace in zip(["Misserfolg", "Erfolg"], [X_COLOR, C_COLOR], braces)
        ])
        braces_texts_alternative = VGroup(*[
            Tex(tex).next_to(brace_text, DOWN) 
            for tex, brace_text in zip(["Niete", "Treffer"], braces_texts)
        ])

        self.play(Create(braces))
        self.play(Write(braces_texts[1]))
        self.wait()
        self.fadein_fadeout_anim(braces_texts_alternative[1])

        self.play(TransformFromCopy(braces_texts[1], braces_texts[0]), run_time = 1.5)
        self.wait()
        self.fadein_fadeout_anim(braces_texts_alternative[0])


        self.df_fail, self.df_succ, self.outcome_text = df_fail, df_succ, outcome_text

    def propability(self):
        df_fail, df_succ, outcome_text = self.df_fail, self.df_succ, self.outcome_text
        v_buff = 1.5

        prop_text = Tex("Wahrscheinlichkeit")\
            .next_to(outcome_text.get_center(), UP, buff = v_buff + 0.1)\
            .align_to(outcome_text, LEFT)

        self.play(FocusOn(prop_text, run_time = 1))
        self.play(Write(prop_text))
        self.wait()

        prop_nums = VGroup(*[
            MathTex(*tex).next_to(df.get_center(), UP, buff = v_buff) 
            for tex, df in zip([["5","/","6"], ["1","/","6"]], [df_fail, df_succ])
        ])

        # transforming die 6 into prop denominator
        self.play(ReplacementTransform(df_succ.copy(), prop_nums[1][0]), run_time = 2)
        self.play(Write(prop_nums[1][1:]), run_time = 1.5)
        self.play(Circumscribe(prop_nums[1], color = C_COLOR, run_time = 2))
        self.wait()


        # transforming die 1-5 into prop deniminator
        count_val = ValueTracker(0)
        count_num = Integer(0).move_to(prop_nums[0][0])
        count_num.add_updater(lambda dec: dec.set_value(count_val.get_value()))

        self.add(count_num)
        self.play(
            AnimationGroup(
                *[FadeOut(df.copy(), target_position = count_num.get_center(), scale = 0.1) for df in [*df_fail]], 
                lag_ratio = 0.1
            ),
            count_val.animate.set_value(5), 
            run_time = 4
        )
        self.play(Write(prop_nums[0][1:]), run_time = 1.5)
        self.play(Circumscribe(prop_nums[0], color = X_COLOR, run_time = 2))
        self.wait(2)

        # p and q
        arrow = CurvedArrow(
            prop_nums[1].get_top() + 0.2*UP, 
            prop_nums[0].get_top() + 0.2*UP, 
            angle = PI/2, color = YELLOW_D
        )

        prop_varp = MathTex("p", "=").next_to(prop_nums[1], LEFT)
        prop_varq = MathTex("q", "=").next_to(prop_nums[0], LEFT)
        pq = MathTex("q", "=", "1", "-", "p").move_to(arrow.get_top())
        for tex in prop_varp, prop_varq, pq:
            tex.set_color_by_tex_to_color_map({"p": C_COLOR, "q": X_COLOR})
            tex.shift(0.05*DOWN)
        pq.add_background_rectangle(buff = 0.1, opacity = 0.85)

        self.play(FadeIn(prop_varp, shift = 2*DOWN), run_time = 2)
        self.wait(0.5)
        self.play(FadeIn(prop_varq, shift = 2*DOWN), run_time = 2)
        self.wait()


        self.play(Create(arrow), run_time = 2)
        self.play(
            FadeIn(pq[0]), 
            Write(pq[1:]), 
            run_time = 1.5
        )
        self.wait()

        self.play(Circumscribe(pq[3:], color = YELLOW_E, fade_out = True, run_time = 4))
        self.wait(3)

    def bernoulli(self):
        bernoulli = Tex("Bernoulli", "-", "Experiment")\
            .set_color_by_gradient(RED, YELLOW, GREEN, BLUE)\
            .set(width = config["frame_width"] - 1)\
            .set_fill(GREY, 0.4)\
            .set_stroke(width = 1)\
            .to_edge(DOWN)

        self.play(DrawBorderThenFill(bernoulli), run_time = 2)
        self.wait()

        # camera shift parameter 
        x_shift = 14*RIGHT

        # prepare for camera shift --> add all mobjects
        image = ImageMobject(IMG_DIR + "Jakob_Bernoulli.jpg")\
            .set_width(4)\
            .to_corner(UR, buff = 0.5)\
            .shift(x_shift)
        self.add(image)


        text1 = Tex(
            "Ein Zufallsexperiment mit nur ", "zwei\\\\", "interessierenden Ergebnissen", " heißt\\\\", "Bernoulli-Experiment.\\\\", 
            color = GREY_A, tex_environment = "flushleft"
        )
        text2 = Tex(
            "Die Ergebnisse bezeichnet man als\\\\", "Erfolg", " bzw. ", "Misserfolg", ".",
            color = GREY_A, tex_environment = "flushleft"
        )
        text3 = Tex(
            "Die Wkt. für einen Erfolg bezeichnet\\\\", "man mit ", "$p$", ", die für einen Misserfolg \\\\ mit ", "$q$", ". ",
            "Es gilt ", "$q = 1 - p$", ".",
            color = GREY_A, tex_environment = "flushleft"
        )

        for text in text1, text2, text3:
            text.to_corner(UL, buff = 0.5)
            text.shift(x_shift)
        text2.shift(2.1*DOWN)
        text3.shift(3.6*DOWN)

        self.add(text1, text2, text3)

        # moving camera
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.shift(x_shift), 
            bernoulli.animate.shift(x_shift), 
            run_time = 3
        )
        self.wait()

        # indicating text
        self.play(FadeToColor(text1[1:3], BLUE_D), run_time = 1.5)
        self.wait(0.5)
        self.play(FadeToColor(text2[1], C_COLOR), run_time = 1)
        self.play(FadeToColor(text2[3], X_COLOR), run_time = 1)
        self.wait()

        self.play(FadeToColor(text3[2], C_COLOR), run_time = 1)
        self.play(FadeToColor(text3[4], X_COLOR), run_time = 1)
        self.wait()
        self.play(FadeToColor(text3[7], YELLOW_E), run_time = 1.5)
        self.wait(2)

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.shift(-x_shift), 
            bernoulli.animate.shift(-x_shift), 
            run_time = 3
        )
        self.wait(3)


    # function
    def fadein_fadeout_anim(self, mob):
        self.play(FadeIn(mob, shift = 2*LEFT))
        self.wait()
        self.play(FadeOut(mob, shift = 2*LEFT))
        self.wait()


class StandardExperiments(Scene):
    def construct(self):
        processes = VGroup(
            get_random_coin(shuffle_time = 1), 
            get_random_die(shuffle_time = 1.5), 
            get_random_card(shuffle_time = 2)
        )
        processes.scale(1.5)
        processes.arrange(RIGHT, buff = 2.5)
        processes.shift(UP)

        titles = VGroup(*[
            Tex(*tex, font_size = 60).next_to(process, UP, buff = 0.5)
            for tex, process in zip(
                [["Werfen einer\\\\", "Münze"], ["Werfen eines\\\\", "Würfels"], ["Ziehen einer\\\\", "Karte"]], 
                processes
            )
        ])
        for title in titles:
            title[0].set_color(GREY_A)
            title[-1].set_color(YELLOW_E)

        self.add(processes, titles)
        self.wait(6)


        self.processes = processes

        self.coin_flip()
        self.die_flip()
        self.card_flip()

    def coin_flip(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        success = Tex(CMARK_TEX, tex_template = myTemplate, font_size = 72, color = C_COLOR)\
            .to_edge(LEFT)\
            .shift(1.1 * DOWN)
        failure = Tex(XMARK_TEX, tex_template = myTemplate, font_size = 72, color = X_COLOR)\
            .to_edge(LEFT)\
            .shift(3*DOWN)

        succ_fail = VGroup(get_coin("K"), get_coin("Z"))\
            .arrange_submobjects(DOWN, buff = 0.75)\
            .next_to(self.processes[0], DOWN, buff = 0.75)

        for coin in succ_fail:
            coin.scale(0.8)

        self.play(
            AnimationGroup(
                FadeIn(succ_fail[0], shift = RIGHT), 
                DrawBorderThenFill(success), 
                lag_ratio = 0.25
            ),
            run_time = 1.5
        )
        self.play(
            AnimationGroup(
                TransformFromCopy(succ_fail[0], succ_fail[1]),
                DrawBorderThenFill(failure), 
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait(3)

    def die_flip(self):
        succ = VGroup(*[get_die_face(number) for number in [2,3,5]]).arrange_submobjects(RIGHT)
        fail = VGroup(*[get_die_face(number) for number in [1,4,6]]).arrange_submobjects(RIGHT)

        succ_fail = VGroup(succ, fail)\
            .arrange_submobjects(DOWN, buff = 0.75)\
            .next_to(self.processes[1], DOWN, buff = 0.75)

        for die in succ, fail:
            die.scale(0.8)

        self.play(ShowIncreasingSubsets(succ), run_time = 3)
        self.wait()

        self.play(TransformFromCopy(succ, fail), run_time = 2)
        self.wait(3)

    def card_flip(self):
        nums_and_faces = list(range(2, 11)) + ["B", "D", "K", "A"]

        card_height = 0.8
        diamonds = VGroup(*[PlayingCard(height = card_height, value = value, suit = "diamonds", key = None) for value in nums_and_faces])
        hearts = VGroup(*[PlayingCard(height = card_height, value = value, suit = "hearts", key = None) for value in nums_and_faces])

        spades = VGroup(*[PlayingCard(height = card_height, value = value, suit = "spades", key = None) for value in nums_and_faces])
        clubs = VGroup(*[PlayingCard(height = card_height, value = value, suit = "clubs", key = None) for value in nums_and_faces])

        for cards in diamonds, hearts, spades, clubs:
            cards.arrange(RIGHT, buff = -card_height/2, center = True)

        succ = VGroup(spades, clubs)\
            .arrange_submobjects(DOWN, buff = -0.2)

        fail = VGroup(diamonds, hearts)\
            .arrange_submobjects(DOWN, buff = -0.2)

        succ_fail = VGroup(succ, fail)\
            .arrange_submobjects(DOWN, buff = 0.25)\
            .next_to(self.processes[2], DOWN, buff = 0.75)

        self.play(
            AnimationGroup(
                ShowIncreasingSubsets(spades), 
                ShowIncreasingSubsets(clubs),
                lag_ratio = 0.3
            ),
            run_time = 3
        )
        self.wait()

        self.play(TransformFromCopy(succ, fail), run_time = 2)
        self.wait(5)


class RealityCheck(Scene):
    def construct(self):
        ellipses = VGroup(*[
            Ellipse(width = 6, height = 4.5, fill_opacity=0.5, color=ell_color, stroke_width=10) 
            for ell_color in [BLUE_B, YELLOW_D]
        ])
        ellipses.arrange(RIGHT, buff = -2)
        ellipses.rotate(-30*DEGREES)
        ellipses.shift(1*LEFT)
        ellipses.scale(0.8)

        circle = Circle(radius = 1.5, fill_opacity=0.5, color=GREEN_B, stroke_width=10)
        circle.to_corner(DL)

        real = Ellipse(width = 4, height = 2.5, fill_opacity=0.5, color=RED_B, stroke_width=10)
        real.to_corner(UR)

        ellipses.add(circle, real)

        strings = [
            "''Das musst du\\\\ noch lernen''", 
            "''Das weiß \\\\ich schon''", 
            "Kommt im \\\\Test dran", 
            "Braucht man im\\\\ wahren Leben"
        ]

        texts = VGroup(*[
            Tex(string, color = BLACK).move_to(ell) 
            for string, ell in zip(strings, ellipses)
        ])
        texts[0].shift(0.5*UP + 0.35*LEFT)
        texts[1].shift(0.5*DOWN + 0.45*RIGHT)

        teacher = Tex("Lehrer", font_size = 72).next_to(ellipses[0].get_corner(UL), LEFT)
        student = Tex("Du", font_size = 72).next_to(ellipses[1].get_corner(DR), RIGHT)

        self.add(ellipses[0], teacher)
        self.wait(0.5)
        self.play(Write(texts[0]), run_time = 0.75)
        self.wait(0.5)

        self.play(
            Create(ellipses[1]), 
            Write(texts[1]), 
            FadeIn(student, shift = LEFT), 
            run_time = 0.75
        )
        self.wait()

        self.play(
            GrowFromCenter(ellipses[2]), 
            Write(texts[2]), 
            run_time = 0.75
        )
        self.wait(1)

        self.play(
            FadeIn(ellipses[3], shift = 3*LEFT), 
            Write(texts[3]), 
            run_time = 0.75
        )
        self.wait(2)



        def func(t):
            return np.array((16 * np.sin(t)**3, 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t), 0))
        heart = ParametricFunction(func, t_range = np.array([0, TAU]))\
            .set_color(RED)\
            .scale(0.15)\
            .center()


        fade_out_list = [x for x in self.mobjects if x != ellipses[-1]]
        self.play(
            FadeOut(Group(*fade_out_list)),
            ReplacementTransform(ellipses[-1], heart), 
            run_time = 2
        )
        self.play(
            FadeOut(heart, scale = 3), 
            rate_func = rush_into, run_time = 2
        )


class GoOnADate(Scene):
    def construct(self):
        question = Tex("Willst du mit mir gehen?")\
            .scale(2)\
            .to_edge(UP)
        self.add(question)

        sf_texs = VGroup(*[Tex(tex, color = tex_color) for tex, tex_color in zip(["Erfolg:", "Misserfolg:"], [C_COLOR, X_COLOR])])
        sf_texs.arrange_submobjects(DOWN, buff = 2, aligned_edge = RIGHT)
        sf_texs.to_edge(LEFT)

        sf_numlines = VGroup(*[NumberLine(x_range = [0, 1, 0.25], length = config["frame_width"]/2) for _ in range(2)])
        for num_line, tex in zip(sf_numlines, sf_texs):
            num_line.next_to(tex, RIGHT, buff = 1)

        dlines = VGroup(*[DashedLine(2.5*UP, 2.5*DOWN, color = GREY, dash_length=0.13).set_stroke(width = 2) for _ in range(5)])\
            .arrange_submobjects(RIGHT, sf_numlines[0].unit_size/4)\
            .next_to(midpoint(sf_numlines[0].get_left(), sf_numlines[1].get_left()), RIGHT, buff = 0)

        numbers = VGroup(*[MathTex(tex, font_size = 36, color = GREY_A).next_to(line, DOWN) for tex, line in zip(
            ["0{,}00", "0{,}25", "0{,}50", "0{,}75", "1{,}00"], dlines)]
        )

        self.add(dlines, numbers, sf_texs)

        hearts = SVGMobject(SVG_DIR + "emoji_heart_eyes").scale(0.65)
        finger = SVGMobject(SVG_DIR + "emoji_middle_finger").scale(0.65)

        init_height = hearts.height

        val = ValueTracker(0.5)

        linep = always_redraw(lambda: Line(sf_numlines[0].n2p(0), sf_numlines[0].n2p(val.get_value()), color = GREY))
        lineq = always_redraw(lambda: Line(sf_numlines[1].n2p(0), sf_numlines[1].n2p(1 - val.get_value()), color = GREY))

        hearts.add_updater(lambda h: h.move_to(linep.get_end()).set(height = ( 0.9*val.get_value() + 0.1) * init_height))
        finger.add_updater(lambda h: h.move_to(lineq.get_end()).set(height = ((1 - 0.9*val.get_value())) * init_height))

        self.add(linep, hearts)
        self.wait()

        self.play(val.animate.set_value(1), run_time = 4)
        self.wait()

        self.add(lineq, finger)
        self.play(val.animate.set_value(0), run_time = 6)
        self.wait()
        self.play(val.animate.set_value(0.75), run_time = 4.5)
        self.wait()


class ItsRainingMan(Scene):
    def construct(self):

        couple = SVGMobject(SVG_DIR + "emoji_couple_holding_hands")
        couple.to_edge(LEFT)
        couple.shift(2*LEFT + 1.5*DOWN)

        speed = 1
        def update_rotate(mob, dt):
            width = mob.width
            x = mob.get_left()[0]
            if x > config["frame_x_radius"]:
                mob.move_to((config["frame_x_radius"] + width) * LEFT + 1.5*DOWN)
                mob.shift(speed*RIGHT * dt)

            mob.shift(speed*RIGHT * dt)

        couple.add_updater(update_rotate)
        self.add(couple)

        date_sign = self.get_date_sign().shift(2*UP).to_edge(RIGHT)
        date_night = Tex("DATE ", "$-$", " Night").move_to(date_sign)

        colors = [PINK, RED, BLUE, GREEN, PURPLE, GOLD, ORANGE, MAROON, TEAL]
        def change_color(mob, dt):
            color = random.choice(colors)
            mob.set_color(color)
        date_night[0].add_updater(change_color)

        self.wait(2)
        self.play(
            DrawBorderThenFill(date_sign, run_time = 2), 
            Write(date_night, rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 2)
        )
        self.wait(10)

        sf_texs = VGroup(*[Tex(tex, color = tex_color) for tex, tex_color in zip(["Erfolg:", "Misserfolg:"], [C_COLOR, X_COLOR])])
        sf_texs.arrange_submobjects(DOWN, buff = 1, aligned_edge = RIGHT)
        sf_texs.to_edge(LEFT).shift(1.5*UP)

        sf_desc = VGroup(*[Tex(tex) for tex in ["Es regnet.", "Es regnet nicht."]])
        for desc, texs in zip(sf_desc, sf_texs):
            desc.next_to(texs, RIGHT, buff = 1, aligned_edge=DOWN)

        self.play(FadeIn(sf_texs, shift = 3*RIGHT, lag_ratio = 0.25), run_time = 1)
        self.play(
            AnimationGroup(*[GrowFromEdge(desc, DL) for desc in sf_desc], lag_ratio = 0.25), run_time = 2
        )
        self.wait(3)

        val = ValueTracker(0)
        prop_succ = DecimalNumber(val.get_value())\
            .next_to(sf_desc[0], RIGHT, buff = 2, aligned_edge=UP)\
            .set_color(C_COLOR)
        prop_fail = DecimalNumber(1 - val.get_value())\
            .next_to(sf_desc[1], RIGHT, aligned_edge=UP)\
            .align_to(prop_succ, LEFT)\
            .set_color(X_COLOR)


        self.play(
            *[GrowFromCenter(prop) for prop in [prop_succ, prop_fail]]
        )
        self.wait()

        prop_succ.add_updater(lambda dec: dec.set_value(val.get_value()))
        prop_fail.add_updater(lambda dec: dec.set_value(1 - val.get_value()))

        self.play(val.animate.set_value(1), run_time = 3)
        self.wait()
        self.play(val.animate.set_value(0.3), run_time = 2.7)
        self.wait()

    # functions
    def get_date_sign(self):
        shape = VMobject()
        shape.set_points_as_corners([
            2.5*LEFT + 0.4*DOWN, 2.5*LEFT + 0.4*UP, 0.4*UP, 1*UP, 1.25*RIGHT, 1*DOWN, 0.4*DOWN, 2.5*LEFT + 0.4*DOWN
        ])

        shape2 = VMobject()
        shape2.set_points_as_corners([
            2.7*LEFT + 0.6*DOWN, 
            2.7*LEFT + 0.6*UP, 
            0.2*LEFT + 0.6*UP, 
            0.2*LEFT + 1.4*UP, 
            1.5*RIGHT, 
            0.2*LEFT + 1.4*DOWN, 
            0.2*LEFT + 0.6*DOWN, 
            2.7*LEFT + 0.6*DOWN
        ])

        date_sign = Cutout(shape2, shape, stroke_width = 0, fill_opacity = 0.5, fill_color = YELLOW)

        return date_sign


class ItsRainingManAnimation(Scene):
    def construct(self):
        rain_lines = VGroup(*[self.get_rain_line() for _ in range(15)])
        def animate_rain(mob):
            x = random.uniform(-config["frame_x_radius"], config["frame_x_radius"])
            y = random.uniform(-config["frame_y_radius"], config["frame_y_radius"])

            next_pos = np.array([x,y,0])

            mob.move_to(next_pos)

        self.play(
            *[UpdateFromFunc(line, animate_rain) for line in rain_lines], 
            run_time = 20
        )

    def get_rain_line(self):
        line = Line(UP, DOWN, color = GREY_D, stroke_width = 2)
        line.set_length(0.75)
        angle = random.uniform(25, 35)
        line.rotate(angle*DEGREES)

        return line


class NextSteps(Scene):
    def construct(self):
        strings = [
            ["Bernoulli", "$-$", "Experiment"], 
            ["Bernoulli", "$-$", "Kette"], 
            ["Bernoulli", "$-$", "Formel"]
        ]
        titles = VGroup(*[Tex(*string, font_size = 72) for string in strings])
        titles.arrange(DOWN, buff = 2.25)
        titles.to_edge(UP, buff = 0.25)
        for title, b_col, e_col in zip(titles, [YELLOW_A, YELLOW_B, YELLOW_C], [BLUE_A, BLUE_B, BLUE_C]):
            title[0].set_color(b_col)
            title[-1].set_color(e_col)

        arrows = VGroup(*[
            Arrow(0.8*UP, 0.8*DOWN, color = GREY_D, tip_length = 0.25).next_to(title, DOWN) 
            for title in titles
        ])

        # information left from arrows
        infos_str = [
            ["Erfolg"],
            ["3", "$\\times$", "wiederholen"], 
            ["Wkt. berechnen"]
        ]
        infos = VGroup(*[
            Tex(*string).next_to(arrow, LEFT, buff = 1) 
            for string, arrow in zip(infos_str, arrows)
        ])


        # mathematical symbols right from arrows
        symbols = VGroup()

        six = get_die_face(6, dot_color = PINK).set(height = 0.5)

        sixes = VGroup(*[get_die_face(6, dot_color = PINK).set(height = 0.5) for x in range(3)])
        sixes.arrange(RIGHT)

        prob = MathTex("P", "(", "KKaKK", ")")
        prob[2].set_color(BLACK).set_fill(BLACK, 0)
        prob_sixes = sixes.copy()
        prob_sixes.move_to(prob[2])
        prob.add(prob_sixes)

        symbols.add(six, sixes, prob)
        for symbol, arrow in zip(symbols, arrows):
            symbol.next_to(arrow, RIGHT, buff = 1)


        # Animations
        self.add(titles[0], arrows)
        self.wait(1)
        self.play(
            AnimationGroup(
                FadeIn(infos[0], shift = 3*RIGHT), 
                ShowIncreasingSubsets(symbols[0]), 
                lag_ratio = 0.25
            )
        )
        self.wait()

        self.play(Write(titles[1]), run_time = 0.75)
        self.play(
            AnimationGroup(
                FadeIn(infos[1], shift = 3*RIGHT), 
                ShowIncreasingSubsets(symbols[1]), 
                lag_ratio = 0.25
            )
        )
        self.wait()


        self.play(Write(titles[2]), run_time = 0.75)
        # self.play(
        #     AnimationGroup(
        #         FadeIn(infos[2], shift = 3*RIGHT), 
        #         ShowIncreasingSubsets(symbols[2]), 
        #         lag_ratio = 0.25
        #     )
        # )
        self.add(infos[2])
        self.add(symbols[2])
        self.wait()


        focus_group = VGroup(titles[1], infos[1], symbols[1], arrows[1])
        self.add(focus_group)

        sur_rects = VGroup(*[
            SurroundingRectangle(focus_group, buff = buff, stroke_width = 2)\
                .set_color([YELLOW_A, YELLOW_B, YELLOW_C, BLUE_C, BLUE_B, BLUE_A])
            for buff in reversed(np.linspace(0.1, 0.55, 11))
        ])


        fadeout_list = [x for x in self.mobjects if x != focus_group]
        self.play(
            FadeIn(sur_rects, scale = 2, lag_ratio = 0.05, rate_func = lambda t: smooth(1-t)),
            FadeOut(Group(*fadeout_list)),
            FadeOut(focus_group, scale = 2, rate_func = rush_into),
            run_time = 2
        )
        self.wait()


class Outro(Scene):
    def construct(self):
        bi_terms = ["Biathlon", "Bisexualität", "Binomische Formeln", "Binomialverteilung"]
        bi_group = VGroup(*[Tex(term, font_size = 72) for term in bi_terms])
        bi_group.arrange_submobjects(DOWN, buff = 1.25, aligned_edge = LEFT)
        bi_group.to_edge(RIGHT)
        for element in bi_group:
            element[0][:2].set_color(ORANGE)

        svg1 = SVGMobject(SVG_DIR + "biathlon-shoot").next_to(bi_group[0], LEFT, buff = 2)
        svg2 = SVGMobject(SVG_DIR + "biathlon-skiing").next_to(svg1, LEFT, buff = 1).shift(0.4*LEFT)
        svg3 = SVGMobject(SVG_DIR + "emoji_couple_holding_hands_ww").next_to(bi_group[1], LEFT, buff = 2)
        svg4 = SVGMobject(SVG_DIR + "emoji_couple_holding_hands").next_to(svg3, LEFT, buff = 1)

        eq = MathTex("(", "a", "\\pm", "b", ")^2", "=", "a^", "2", "\\pm", "2", "a", "b", "+", "b^", "2")
        eq.next_to(bi_group[2], LEFT, buff = 2)
        eq.shift(0.8*RIGHT)
        eq.set_color_by_tex_to_color_map({"a": BLUE, "b": YELLOW})


        cmark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate).next_to(bi_group[-1], LEFT, buff = 2).shift(0.4*LEFT)
        xmark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate).next_to(cmark, LEFT, buff = 2.8)

        for svg in svg1, svg2:
            svg.set_color(WHITE)
        for svg in svg1, svg2, svg3, svg4:
            svg.set(height = 1.25)
            svg.save_state()
            svg.set(height = 4)
            svg.center()

        svg1.shift(2*LEFT)
        svg2.shift(2*RIGHT)
        svg3.shift(2*LEFT + 1.5*DOWN)
        svg4.shift(2*RIGHT + 1.5*DOWN)

        for mark in cmark, xmark:
            mark.set(height = 1.25)

        self.play(ShowIncreasingSubsets(VGroup(svg1, svg2)))
        self.play(Write(bi_group[0]), run_time = 0.75)
        self.play(LaggedStartMap(Restore, VGroup(svg1, svg2), lag_ratio = 0.5), run_time = 1.5)

        self.play(ShowIncreasingSubsets(VGroup(svg3, svg4)))
        self.play(Write(bi_group[1]), run_time = 0.75)
        self.play(LaggedStartMap(Restore, VGroup(svg3, svg4), lag_ratio = 0.5), run_time = 1.5)

        self.play(Write(eq))
        self.play(FadeIn(bi_group[2], shift = 2*RIGHT), run_time = 0.75)

        self.play(
            AnimationGroup(
                DrawBorderThenFill(cmark), 
                DrawBorderThenFill(xmark),
                Write(bi_group[-1]),
                lag_ratio = 0.25
            ),
            run_time = 2
        )
        self.wait(0.5)

        self.play(Circumscribe(VGroup(cmark, xmark), color = YELLOW_D, stroke_width = 3, fade_out=True, run_time = 3))
        self.wait(3)

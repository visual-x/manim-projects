from manim import *
from BinomHelpers import *


class Intro(Scene):
    def construct(self):
        titles = self.titles = VGroup(*[
            Tex(tex, font_size = 72, color = t_color) 
            for tex, t_color in zip(["Erfolg", "Misserfolg"], [C_COLOR, X_COLOR])
        ])
        titles.arrange(RIGHT, buff = 3.5)
        titles.to_edge(UP)

        probs = self.probs = VGroup(*[
            MathTex(tex, font_size = 72)\
                .next_to(title, dir, buff = 1.5)\
                .match_color(title)
            for tex, title, dir in zip(["p", "q"], titles, [LEFT, RIGHT])
        ])


        self.add(titles)

        self.dice()
        self.cards()
        self.show_probs()


    def dice(self):
        dies = VGroup(*[get_die_face(number = num) for num in [1,2]])
        dief = VGroup(*[get_die_face(number = num) for num in [3,4,5,6]])
        for die, title in zip([dies, dief], self.titles):
            die.set(height = 0.8)
            die.arrange(RIGHT)
            die.next_to(title, DOWN, buff = 1)

        self.ereignis = Tex("Werfen einer Zahl kleiner als $3$", font_size = 72)
        self.play(Write(self.ereignis), run_time = 0.75)
        self.wait()


        self.play(FadeIn(dies, shift = UP, lag_ratio = 0.25), run_time = 1.5)
        self.wait()

        self.play(TransformFromCopy(dies, dief, lag_ratio = 0.05), run_time = 1.5)
        self.wait()

        self.dies, self.dief = dies, dief

    def cards(self):
        suits = ["diamonds", "hearts", "spades", "clubs"]

        card_ereignis = Tex("Ziehen einer Bildkarte", font_size = 72)
        self.play(Transform(self.ereignis, card_ereignis))
        self.wait()

        cardss = VGroup(*[
            VGroup(*[
                PlayingCard(height = 1.5, value = value, suit = suit, key = None)
                for value in ["B", "D", "K", "A"]
            ]).arrange(RIGHT, buff = -0.6)
            for suit in suits
        ]).arrange(DOWN, buff = -1)

        cardsf = VGroup(*[
            VGroup(*[
                PlayingCard(height = 1.5, value = value, suit = suit, key = None)
                for value in list(range(2, 11))
            ]).arrange(RIGHT, buff = -0.6)
            for suit in suits
        ]).arrange(DOWN, buff = -1)


        for cards, title in zip([cardss, cardsf], self.titles):
            cards.next_to(title, DOWN, buff = 3.5)

        self.play(FadeIn(cardss, lag_ratio = 0.05), run_time = 1.5)
        self.wait()
        self.play(FadeIn(cardsf, lag_ratio = 0.05), run_time = 1.5)
        self.wait()

    def show_probs(self):
        self.play(
            AnimationGroup(
                *[FadeIn(prob, shift = 2*direc, scale = 0.2) for prob, direc in zip(self.probs, [LEFT, RIGHT])], 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()


        die_probs = VGroup(*[
            MathTex(tex, font_size = 60)\
                .next_to(mobj, DOWN, buff = 1)
            for tex, mobj in zip(["\\frac{2}{6}", "\\frac{4}{6}"], self.probs)
        ])


        card_probs = VGroup(*[
            MathTex(tex, font_size = 60)\
                .next_to(mobj, DOWN, buff = 4)
            for tex, mobj in zip(["\\frac{16}{52}", "\\frac{36}{52}"], self.probs)
        ])

        self.play(
            FadeIn(die_probs[0], shift = RIGHT), 
            FadeIn(card_probs[0], shift = RIGHT), 
            run_time = 1.5
        )
        self.wait()

        self.play(
            FadeIn(die_probs[1], shift = LEFT), 
            FadeIn(card_probs[1], shift = LEFT), 
            run_time = 1.5
        )
        self.wait()


class FromExpToTrail(Scene):
    def construct(self):

        self.create_trail()
        self.prob_remains()

    def create_trail(self):
        path = VMobject()
        path.set_points_smoothly([
            6*LEFT + 1*UP,
            5*LEFT + 2*UP, 
            4*RIGHT + 3*UP,
            4*RIGHT + 2*UP,
            5*LEFT + 0.5*DOWN,
            4*LEFT + 3.0*DOWN, 
            5*RIGHT + 2.5*DOWN
        ])
        dpath = DashedVMobject(path, num_dashes = 50, color = GREY)

        dice_values = [1,5,4,1,3,6,6,4,1,2]
        dices = VGroup(*[get_die_face(number = num) for num in dice_values])
        for die, prop in zip(dices, [0, 0.1, 0.2, 0.3, 0.45, 0.55, 0.65, 0.82, 0.92, 1]): # np.linspace(0, 1, 10)
            die.set(height = 0.8)
            die.move_to(path.point_from_proportion(prop))


        choices = get_die_faces()
        choices.shift(2*RIGHT + 0.5*DOWN)
        def shuffle_die(mob):
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            mob.become(new_mob)

        first_die = get_die_face(1)

        counter = 0
        num = Integer(counter)\
            .scale(1.5)\
            .move_to(5.5*RIGHT + 1.5*UP)\
            .set_color(YELLOW_D)
        self.add(num)

        for k in range(len(dices)):
            self.play(UpdateFromFunc(first_die, shuffle_die), run_time = 1)
            first_die.become(choices[dice_values[k] - 1])
            self.play(TransformFromCopy(first_die, dices[k]))
            counter += 1
            num.set_value(counter).set_color(YELLOW_D)
        self.wait()


        trail = Tex("Bernoulli", "$-$", "Kette", font_size = 60, color = YELLOW_D)
        trail.move_to(choices)
        trail.shift(0.75*UP)

        self.play(
            Write(trail),
            FadeOut(first_die, run_time = 1),
        )
        self.bring_to_front(dices)
        self.wait()

        self.play(Create(dpath, run_time = 4))
        self.wait()


        dices.generate_target()
        dices.target.arrange(RIGHT, buff = 0.45).center()
        brace = Brace(dices.target, DOWN, color = GREY)
        dline = DashedLine(6.5*LEFT, 6.5*RIGHT, dash_length = 0.25)

        self.play(
            MoveToTarget(dices),
            ReplacementTransform(dpath, dline),
            Create(brace),
            trail.animate.center().to_edge(UP), 
            run_time = 2
        )
        self.bring_to_front(dices)
        self.wait()

        length = Tex("Länge ", "$n=$ ", "$10$", font_size = 60)
        length.next_to(brace, DOWN, buff = 0.35)
        length[-1].set_color(YELLOW_D)

        self.play(
            Write(length[:-1], run_time = 1), 
            ReplacementTransform(num, length[-1], rate_func = squish_rate_func(smooth, 0.3, 1), path_arc = -90*DEGREES, run_time = 3),
        )
        self.wait(2)


        self.dices, self.trail, self.length = dices, trail, length

    def prob_remains(self):
        shift_mobs = Group(*[x for x in self.mobjects if x != self.trail])

        define = Tex(
            "Wird ein Bernoulli$-$Versuch $n$-mal durchgeführt, \\\\", 
            "wobei sich die Erfolgswahrscheinlichkeit $p$ von \\\\ Stufe zu Stufe nicht ändert, ", 
            "so spricht man von einer \\\\", "Bernoulli-Kette der Länge $n$.", 
            tex_environment = "flushleft", color = DARKER_GREY
        )
        define.next_to(self.trail, DOWN)
        define[0].set_color(WHITE)

        self.play(shift_mobs.animate.shift(1.5*DOWN))
        self.play(
            FadeIn(define[0], shift = 3*RIGHT),
            FadeIn(define[1]),
            FadeIn(define[2], shift = 3*LEFT),
        )
        self.play(FadeToColor(define[2:], WHITE), run_time = 2)
        self.wait()

        arrows = VGroup(*[
            CurvedArrow(
                self.dices[x].get_top() + 0.1*(UP + RIGHT), self.dices[x + 1].get_top() + 0.1*(UP + LEFT), 
                angle = -60*DEGREES, tip_length = 0.25, color = GREEN_D
            )
            for x in range(9)
        ])
        self.play(LaggedStartMap(FadeIn, arrows, lag_ratio = 0.1, run_time = 3))
        self.wait()

        self.play(FadeToColor(define[1], GREEN_D), run_time = 2)
        self.wait(2)



        bools = [True] + 2*[False] + [True] + 4*[False] + [True] + [False]
        probs = VGroup()
        for entry, dice in zip(bools, self.dices):
            if entry is True:
                prob = MathTex("\\frac{1}{6}", font_size = 36, color = C_COLOR)
            else:
                prob = MathTex("\\frac{5}{6}", font_size = 36, color = X_COLOR)
            prob.next_to(dice, UP, buff = 0.5)
            probs.add(prob)

        copy = probs.copy()
        self.play(
            ShowSubmobjectsOneByOne(copy),
            run_time = 5
        )
        self.remove(copy)
        self.play(
            LaggedStartMap(FadeIn, probs, shift = 0.5*DOWN, lag_ratio = 0.1), 
            LaggedStartMap(FadeOut, arrows, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait(3)


class GummiBears(Scene):
    def construct(self):
        main_colors = [GREY_A, YELLOW_D, GREEN, ORANGE, RED, RED_E]
        light_colors = [LIGHT_GREY, YELLOW_B, GREEN_A, LIGHT_BROWN, RED_A, RED_D]

        gbs = VGroup(*[self.get_gummy_bear(main_color = col1, light_color = col2) for col1, col2 in zip(main_colors, light_colors)])
        gbs.arrange(RIGHT)
        gbs.to_edge(UP, buff = 0.1)
        podium = self.get_podium()

        self.play(
            LaggedStartMap(DrawBorderThenFill, gbs, lag_ratio = 0.1),
            FadeIn(podium, shift = 1.5*UP),
            run_time = 2
        )
        self.wait()

        self.play(
            AnimationGroup(
                gbs[1].animate.next_to(podium.boxes[2], UP),
                gbs[4].animate.next_to(podium.boxes[0], UP),
                gbs[2].animate.next_to(podium.boxes[1], UP),
                lag_ratio = 0.3
            ), 
            run_time = 3
        )
        self.wait()

    # function 
    def get_gummy_bear(self, main_color, light_color):
        gb = SVGMobject(SVG_DIR + "GummyBear")
        gb[0].set_color(main_color)
        gb[1:17].set_color(light_color)
        gb[17:].set_color(BLACK)
        
        return gb

    def get_podium(self):

        boxes = VGroup(*[Rectangle(width = 2, height = h, stroke_width = 0, fill_color = GREY, fill_opacity = 1) for h in [2,2.75,1.25]])
        boxes.arrange(RIGHT, aligned_edge = DOWN, buff = 0)

        places = VGroup(*[MathTex(str(num)).scale(1.5) for num in [2,1,3]])
        places.arrange(2*RIGHT)
        for place, box, color in zip(places, boxes, [LIGHT_GREY, GOLD, LIGHT_BROWN]):
            place.next_to(box.get_top(), DOWN)
            place.set_color(color)

        rings = VGroup(*[Circle(color = DARK_GREY).surround(place, buffer_factor=1.25) for place in places])

        result = VGroup(boxes, rings, places)
        result.to_edge(DOWN, buff = 0.1)

        result.boxes = boxes

        return result


class WheelOfFortune(Scene):
    def construct(self):
        self.show_bern_trail()
        self.prob_remains()


    def show_bern_trail(self):
        title = Tex("Glücksrad", font_size = 60)
        title.to_corner(UL)

        wheel = self.wheel = self.get_wheel()
        wheel.shift(3*LEFT + 1.25*DOWN)

        self.play(
            AnimationGroup(
                Write(title),
                DrawBorderThenFill(wheel), 
                lag_ratio = 0.4
            ),
            run_time = 3
        )
        self.wait()

        succ_mark = Tex(CMARK_TEX, color = C_COLOR, font_size = 48*2, tex_template = myTemplate)
        succ_arrow = Arrow(LEFT, RIGHT)
        succ_sector = wheel.succ[0].copy().scale(0.5).rotate(-90*DEGREES)
        succ_group = VGroup(succ_mark, succ_arrow, succ_sector)
        succ_group.arrange(RIGHT, buff = 1)
        succ_group.to_edge(UP)

        self.play(Create(succ_mark), run_time = 1.5)
        self.wait(0.5)
        self.play(
            GrowArrow(succ_arrow), 
            TransformFromCopy(wheel.succ[0], succ_sector), 
            run_time = 3
        )
        self.wait()


        # show outcome and possible spots for trail
        dline = DashedLine(5*LEFT, 5*RIGHT, dash_length = 0.4)
        dline.shift(1.5*UP)

        spots = self.spots = VGroup(*[Square(side_length=1, color = DARK_GREY, fill_color = DARK_GREY, fill_opacity = 0.75) for x in range(4)])
        spots.arrange(RIGHT, buff = 1.5)
        spots.move_to(dline)


        mark = self.big_succ_mark = Tex(XMARK_TEX, color = X_COLOR, font_size = 48*4, tex_template = myTemplate)
        mark.next_to(wheel, RIGHT, buff = 4)
        self.play(
            FadeIn(mark, shift = 4*LEFT, scale = 0.2),
            ShowIncreasingSubsets(dline), 
            LaggedStartMap(GrowFromCenter, spots, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()

        def update_mark(mob):
            angle = wheel.arrow.get_angle() % TAU
            if TAU/10 < angle < PI or 7*TAU/10 < angle < 9*TAU/10:
                new_mark = Tex(XMARK_TEX, color = X_COLOR, font_size = 48*4, tex_template = myTemplate)
            else:
                new_mark = Tex(CMARK_TEX, color = C_COLOR, font_size = 48*4, tex_template = myTemplate)
            new_mark.move_to(mark)
            mark.become(new_mark)


        # Loop  for  Rotation and results

        bools = [True] + 2*[False] + [True]
        trail_marks = VGroup()
        for x, positive in enumerate(bools):
            if positive:
                mob = Tex(CMARK_TEX, font_size = 80, color = C_COLOR, tex_template = myTemplate)
            else:
                mob = Tex(XMARK_TEX, font_size = 80, color = X_COLOR, tex_template = myTemplate)
            mob.move_to(spots[x])
            trail_marks.add(mob)

        anims = [UpdateFromFunc(mark, update_mark)]
        deg_angles = [-(4*360 - 110), -(4*360 + 105), -(4*360 + 270), -(4*360 + 180)]
        rts = [6, 4, 3, 2]

        for deg_angle, rt, trail_mark in zip(deg_angles, rts, trail_marks):
            self.rotate_arrow(deg_angle = deg_angle, added_anims = anims, run_time = rt)
            self.play(TransformFromCopy(mark, trail_mark), run_time = 1.5)
            self.wait()
        self.wait()

    def prob_remains(self):
        wheel, spots = self.wheel, self.spots

        # center wheel show probs
        arrows = VGroup(*[
            CurvedArrow(
                spots[x].get_bottom() + 0.1*(DOWN + RIGHT), spots[x + 1].get_bottom() + 0.1*(DOWN + LEFT), 
                angle = 60*DEGREES, tip_length = 0.25, color = GREEN_D
            )
            for x in range(3)
        ])

        wheel.generate_target()
        wheel.target.scale(0.75).shift(3*RIGHT + DOWN)
        self.play(MoveToTarget(wheel), run_time = 3)
        self.play(LaggedStartMap(FadeIn, arrows, lag_ratio = 0.1, rate_func = there_and_back), run_time = 3)
        self.wait()

        # transform wheel sectors into succ sectors
        succ_sectors = VGroup()
        for sector in wheel.succ:
            succ_sectors.add(sector.copy())

        # succ_sectors[0].rotate(-90*DEGREES)
        # succ_sectors[1].rotate(54*DEGREES)
        succ_sectors.scale(0.75).arrange(RIGHT, buff = 0.25)
        succ_sectors.next_to(self.big_succ_mark, DOWN, aligned_edge=LEFT)

        succ_prob = MathTex("p", "=", "{" + "2", "\\over", "5" + "}", font_size = 80)
        succ_prob.next_to(self.big_succ_mark, RIGHT, buff = 0.5)

        self.play(
            LaggedStart(
                *[TransformFromCopy(wheel, succ) for wheel, succ in zip(wheel.succ, succ_sectors)], 
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.play(FadeIn(succ_prob, shift = RIGHT), run_time = 2)
        self.wait()


        # transform wheel sectors into fail sectors
        big_fail_mark = Tex(XMARK_TEX, color = X_COLOR, font_size = 48*4, tex_template = myTemplate)
        big_fail_mark.move_to(np.array([-self.big_succ_mark.get_x(), self.big_succ_mark.get_y(), 0]))

        fail_sectors = VGroup()
        for sector in wheel.fail:
            fail_sectors.add(sector.copy())

        fail_sectors.scale(0.75).arrange(RIGHT, buff = 0.25)
        fail_sectors.next_to(big_fail_mark, DOWN, aligned_edge=RIGHT)

        fail_prob = MathTex("q", "=", "{" + "3", "\\over", "5" + "}", font_size = 80)
        fail_prob.next_to(big_fail_mark, LEFT, buff = 0.5)

        self.play(
            DrawBorderThenFill(big_fail_mark),
            LaggedStart(
                *[TransformFromCopy(wheel, fail) for wheel, fail in zip(wheel.fail, fail_sectors)], 
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.play(FadeIn(fail_prob, shift = LEFT), run_time = 2)
        self.wait()


        # final rotation animation
        deg_angles = [-(4*360 + 200), -(4*360 + 170), -(4*360 + 120)]
        for deg_angle in deg_angles:
            self.rotate_arrow(deg_angle = deg_angle, run_time = 3)
            self.wait()
        self.wait(3)


    # functions 
    def get_wheel(self):
        colors = [BLUE_B, YELLOW_E, ORANGE, BLUE_B, LIGHT_BROWN]
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
        wheel.succ = VGroup(sectors[0], sectors[3])
        wheel.fail = VGroup(sectors[1], sectors[2], sectors[4])

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


class AskAboutEveryExperiment(WheelOfFortune):
    def construct(self):
        die_faces = get_die_faces()
        die_faces.arrange_in_grid(2,3)
        wheel = self.get_wheel().match_height(die_faces)
        card = PlayingCard(value = 2, suit = "diamonds", key = "2D", height = die_faces.height)

        experiments = VGroup(die_faces, wheel, card)
        experiments.arrange(RIGHT, buff = 1)
        experiments.to_edge(UP)

        self.play(
            LaggedStartMap(FadeIn, experiments, lag_ratio = 0.2), 
            run_time = 4
        )
        self.wait()

        question = Tex("Wird jedes Bernoulli-", "Experiment\\\\", "zu einer Bernoulli-", "Kette", "???")
        question.set_color_by_tex_to_color_map({"Experiment": BLUE, "Kette": YELLOW_D})
        question.scale(1.75).shift(DOWN)

        self.play(Write(question))
        self.wait()


        card.generate_target()
        card.target.center().set(height = 3)

        self.play(
            MoveToTarget(card, path_arc = -90*DEGREES), 
            LaggedStartMap(FadeOut, VGroup(wheel, die_faces), lag_ratio = 0.3, shift = 2*UP, scale = 2), 
            FadeOut(question, shift = 2*DOWN, scale = 0.1), 
            run_time = 4
        )


class FlippingCards(Scene):
    def construct(self):
        self.show_all_cards()
        self.flip_cards()


    def show_all_cards(self):
        suits = ["diamonds", "hearts", "spades", "clubs"]
        suits_german = ["Karo", "Herz", "Pik", "Kreuz"]
        suits_color = ["#D02028", "#D02028", BLACK, BLACK]

        stack_pos = 5.5*RIGHT + 1.5*UP
        stack = DeckOfCards()
        for card in stack:
            card.height = 1.5
        stack.move_to(stack_pos)
        stack.save_state()
        stack.center()
        for card in stack:
            card.height = 3


        title = Tex("Kartensatz\\\\", "52", " Karten")
        title.scale(1.35)
        title.next_to(stack_pos, UP, buff = 0.85)
        title.shift(0.5*LEFT)
        title[-2].set_color(BLACK).set_stroke(width = 0)

        num_cards = Integer(52)\
            .scale(1.35)\
            .set_color(GOLD)\
            .move_to(title[-2])


        self.play(ShowIncreasingSubsets(stack), run_time = 2)
        self.wait()

        self.play(
            Write(title[0], run_time = 1),
            Write(title[-1], run_time = 1),
            FadeIn(num_cards, shift = RIGHT, run_time = 2),
            Restore(stack, path_arc = np.pi/2, lag_ratio = 0.05, run_time = 2), 
        )
        self.wait()


        cards = VGroup(*[
            VGroup(*[
                PlayingCard(height = 1.5, value = value, suit = suit, key = None)
                for value in list(range(2, 11)) + ["B", "D", "K", "A"]
            ]).arrange(RIGHT, buff = -0.6)
            for suit in suits
        ]).arrange(DOWN, buff = 0.5)
        cards.to_edge(LEFT)

        suit_names = VGroup(*[
            Tex(suit, font_size = 72, color = suit_color)\
                .set_stroke(color = GREY_A, width = 1)
                .next_to(cards[block_index][-1], RIGHT, buff = 1, aligned_edge=LEFT)
            for suit, suit_color, block_index in zip(suits_german, suits_color, range(4))
        ])

        # show all cards and suit_names
        self.play(
            AnimationGroup(*[FadeIn(card, shift = 0.5*RIGHT) for card in cards], lag_ratio = 0.05),
            LaggedStartMap(FadeIn, suit_names, shift = 3*RIGHT, lag_ratio = 0.05), 
            run_time = 1.5
        )
        self.wait()

        # Indicate all hearts cards
        self.play(
            AnimationGroup(*[ApplyMethod(card.shift, 0.35*UP, rate_func = there_and_back) for card in cards[1]], lag_ratio = 0.05),
            run_time = 2
        )
        self.wait(2)


        suit_symbols = VGroup(*[SuitSymbol(suit_name, height = 0.5) for suit_name in suits])\
            .arrange_submobjects(RIGHT, buff = 0.15)\
            .next_to(stack.get_bottom(), DOWN, buff = 1)\
            .align_to(num_cards, LEFT)

        mult_13 = MathTex("\\times", "13")\
            .next_to(suit_symbols, RIGHT)

        self.play(
            Transform(suit_names, suit_symbols),
            FadeIn(mult_13, shift = 2*LEFT)
        )
        self.wait()


        # Indicate number cards for all suits + shift face_cards
        tex_of_numbers = MathTex("2,3,\\ldots,10")
        tex_of_numbers.next_to(suit_symbols, DOWN, buff = 1, aligned_edge=LEFT)
        mult_9 = MathTex("\\times", "9")
        mult_9.next_to(tex_of_numbers, RIGHT)

        tex_of_faces = Tex("B, D, K, A")
        tex_of_faces.next_to(tex_of_numbers, DOWN, buff = 1, aligned_edge=LEFT)
        mult_4 = MathTex("\\times", "4", color = GREEN)
        mult_4.next_to(tex_of_faces, RIGHT)

        for mult in mult_9, mult_4:
            mult.align_to(mult_13, LEFT)


        self.play(
            AnimationGroup(*[ApplyMethod(card.shift, 0.35*UP, rate_func = there_and_back) for card in cards[0][0:9]], lag_ratio = 0.05),
            AnimationGroup(*[ApplyMethod(card.shift, 0.35*UP, rate_func = there_and_back) for card in cards[1][0:9]], lag_ratio = 0.05),
            AnimationGroup(*[ApplyMethod(card.shift, 0.35*UP, rate_func = there_and_back) for card in cards[2][0:9]], lag_ratio = 0.05),
            AnimationGroup(*[ApplyMethod(card.shift, 0.35*UP, rate_func = there_and_back) for card in cards[3][0:9]], lag_ratio = 0.05),
            *[cards[suit_index][9:].animate.shift(RIGHT) for suit_index in range(4)],
            run_time = 2
        )
        self.play(
            Write(tex_of_numbers), 
            FadeIn(mult_9, shift = 2*LEFT)
        )
        self.wait()

        # define success 
        sur_rect1 = SurroundingRectangle(
            VGroup(*[cards[suit_index][9:] for suit_index in range(4)]),
            color = GREEN, buff = 0.1
        )

        self.play(
            Write(tex_of_faces, run_time = 1),
            FadeIn(mult_4, shift = 2*LEFT, run_time = 2), 
        )
        self.play(Create(sur_rect1, run_time = 2))
        self.wait()

        self.play(
            AnimationGroup(
                FadeOut(cards[2][10], target_position = 10*UP),
                FadeOut(cards[0][12], target_position = 10*UP),
                FadeOut(cards[3][9], target_position = 10*UP),
                FadeOut(cards[1][10], target_position = 10*UP),
                FadeOut(cards[2][11], target_position = 10*UP),
                FadeOut(cards[0][9], target_position = 10*UP),
                lag_ratio = 0.25
            ),
            run_time = 6
        )
        self.wait()


        # define failure
        sur_rect2 = SurroundingRectangle(
            VGroup(*[cards[suit_index][:9] for suit_index in range(4)]),
            color = RED, buff = 0.1
        )

        self.play(Transform(sur_rect1, sur_rect2), run_time = 3)
        self.play(
            AnimationGroup(
                FadeOut(cards[1][2], target_position = 10*UP),
                FadeOut(cards[0][7], target_position = 10*UP),
                FadeOut(cards[2][4], target_position = 10*UP),
                FadeOut(cards[1][6], target_position = 10*UP),
                FadeOut(cards[3][8], target_position = 10*UP),
                FadeOut(cards[2][1], target_position = 10*UP),
                lag_ratio = 0.25
            ),
            run_time = 4
        )
        self.wait()

        group = VGroup(
            *[cards[suit_index][9:] for suit_index in range(4)], 
            *[cards[suit_index][0:] for suit_index in range(4)]
        )
        self.play(
            FadeOut(sur_rect1),
            FadeOut(group, lag_ratio = 0.05), 
            run_time = 1.5
        )
        self.wait()


        self.stack, self.num_cards = stack, num_cards
        self.tex_of_numbers, self.tex_of_faces = tex_of_numbers, tex_of_faces

    def flip_cards(self):
        stack = self.stack
        self.flip_pos = RIGHT

        self.deck_card = deck_card = self.get_deck_card()
        deck_card.move_to(stack)
        self.play(FadeIn(deck_card, shift = 1.5*RIGHT), run_time = 2)
        self.wait()

        card_draw_numbers = VGroup(*[Tex(str(k), ".", " Zug") for k in [1,2]])\
            .arrange_submobjects(DOWN, buff = 2)\
            .to_edge(LEFT)\
            .shift(0.5*UP)

        title_result = Tex("Ergebnis").move_to(4*LEFT + 3*UP)
        success = Tex("Erfolg", color = GREEN).move_to(1.5*LEFT + 3*UP)
        failure = Tex("Misserfolg", color = RED).move_to(1*RIGHT + 3*UP)
        prop = Tex("Wahrscheinlichkeit").next_to(VGroup(success, failure), UP)

        self.play(
            AnimationGroup(
                FadeIn(card_draw_numbers, shift = 2*RIGHT, lag_ratio = 0.25),
                ShowIncreasingSubsets(VGroup(title_result, success, failure)),
                FadeIn(prop, shift = 2*DOWN),
                lag_ratio = 0.1
            ),
            run_time = 1.5
        )
        self.wait()

        # flip cards from deck
        self.play(FocusOn(stack, run_time = 1.5))
        self.wait(0.5)

        result_cards = VGroup(*[
            PlayingCard(value = value, suit = suit, key = key, height = 1.5)
            for value, suit, key in zip(
                [7, "K"], ["diamonds", "clubs"], ["7D", "KC"]
            )
        ])
        result_positions = [4*LEFT + card_draw_numbers[0].get_y()*UP, 4*LEFT + card_draw_numbers[1].get_y()*UP]
        for card, pos in zip(result_cards, result_positions):
            self.animate_card_flip(card, pos)


        event_num_rects = VGroup(*[
            SurroundingRectangle(mob, color = BLUE) 
            for mob in card_draw_numbers
        ])

        self.play(Create(event_num_rects[0]), run_time = 2)
        self.wait()


        #                         0         1       2    3     4
        prop_result_s1 = MathTex("{16", "\\over", "52", "}").next_to(success, DOWN, buff = 0.5)
        prop_result_f1 = MathTex("{36", "\\over", "52", "}").next_to(failure, DOWN, buff = 0.5)

        prop_result_s2 = MathTex("{16", "\\over", "51", "}").next_to(prop_result_s1, DOWN, buff = 1.4)
        prop_result_f2 = MathTex("{35", "\\over", "51", "}").next_to(prop_result_f1, DOWN, buff = 1.4)

        tex_list = [prop_result_s1, prop_result_f1, prop_result_s2, prop_result_f2]
        for tex in tex_list:
            tex.set_color_by_tex_to_color_map({"51": GOLD, "52": GOLD})


        self.play(Circumscribe(self.num_cards, color = GOLD, run_time = 2))
        self.play(Write(prop_result_s1[2]))
        self.play(Write(prop_result_s1[1]))
        self.wait()

        self.play(Circumscribe(self.tex_of_faces, color = BLUE, run_time = 2))
        self.wait()

        self.play(Write(prop_result_s1[0]))
        self.add(prop_result_s1)
        self.wait()


        self.play(FadeIn(prop_result_f1, target_position=prop_result_s1.get_center(), path_arc = np.pi/4), run_time = 2)
        self.wait()

        # second card pick
        self.play(Transform(event_num_rects[0], event_num_rects[1]), run_time = 2)
        self.wait()

        self.play(Circumscribe(self.tex_of_faces, color = BLUE, run_time = 2))
        self.wait()

        self.play(
            LaggedStart(Write(prop_result_s2[0]), Write(prop_result_s2[1]), lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait()

        self.play(FocusOn(self.num_cards, run_time = 1.5))
        self.play(self.num_cards.animate.set_value(51))
        self.wait()

        self.play(ReplacementTransform(self.num_cards.copy(), prop_result_s2[2]), path_arc = -np.pi/6, run_time = 3)
        self.add(prop_result_s2)
        self.wait()

        self.play(FadeIn(prop_result_f2, target_position=prop_result_s2.get_center(), path_arc = np.pi/6), run_time = 2)
        self.wait(3)


        neq = MathTex("\\neq", color = RED)
        p1, p2 = prop_result_s1.copy(), prop_result_s2.copy()
        props = VGroup(p1, neq, p2)\
            .arrange_submobjects(RIGHT, buff = 0.5)\
            .move_to(1.5*LEFT + 2.5*DOWN)

        self.play(
            AnimationGroup(
                TransformFromCopy(prop_result_s1.copy(), props[0]), 
                TransformFromCopy(prop_result_s2.copy(), props[-1]),
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.play(FadeIn(props[1], shift = 0.5*DOWN))
        self.play(Circumscribe(props, color = BLUE, fade_out = True, run_time = 3))
        self.wait(3)


    # functions
    def get_deck_card(self):
        height = 1.5
        width = height / (3.5/2.5)
        deck = RoundedRectangle(
            corner_radius = height / 20, 
            height = height, 
            width = width,
            fill_opacity = 1,
            stroke_color = WHITE, 
            stroke_width = 5
        )
        deck.set_color_by_gradient([YELLOW, GREEN, BLUE, PINK, RED])

        main_title = Text("Visual X", font = "Bahnschrift")
        sub_title = Text("MagiX Cards", font = "Bahnschrift")

        title = VGroup(main_title, sub_title)
        title.arrange_submobjects(DOWN, buff = 1)
        title.width = width - 0.1

        deck.add(title)

        return deck

    def animate_card_flip(self, result, result_pos, total_time = 3):
        deck_copy = self.deck_card.copy()
        deck_copy.generate_target()
        deck_copy.target.move_to(self.flip_pos).rotate(angle = 90*DEGREES, axis = UP)

        result.move_to(self.flip_pos).rotate(angle = 90*DEGREES, axis = UP)
        result.generate_target()
        result.target.move_to(result_pos).rotate(angle = -90*DEGREES, axis = UP)

        self.play(
            MoveToTarget(deck_copy, path_arc = -np.pi/6, rate_func = rush_into), 
            run_time = total_time / 2
        )
        self.remove(deck_copy)
        self.add(result)
        self.play(
            MoveToTarget(result, path_arc = -np.pi/6, rate_func = rush_from), 
            run_time = total_time / 2
        )
        self.wait()


class PickingClassMates(Scene):
    def construct(self):

        self.introduce_students()
        self.check_for_bernoulli()

    def introduce_students(self):
        m, f = 11, 9

        genders = m*["male"] + f*["female"]
        random.shuffle(genders)

        students = VGroup(*[self.get_student(sex = gender) for gender in genders])
        students.arrange_in_grid(4,5)
        students.center().to_edge(LEFT)


        males = VGroup(*[self.get_student(sex = "male") for x in range(m)])\
            .arrange(RIGHT)\
            .shift(UP)
        females = VGroup(*[self.get_student(sex = "female") for x in range(f)])\
            .arrange(RIGHT)\
            .shift(DOWN)

        m_brace = Brace(males, UP)
        m_num = MathTex(str(m), font_size = 72).next_to(m_brace, UP)
        f_brace = Brace(females, DOWN)
        f_num = MathTex(str(f), font_size = 72).next_to(f_brace, DOWN)

        self.play(
            ShowIncreasingSubsets(males),
            GrowFromEdge(m_brace, LEFT, rate_func = linear),
            run_time = 2
        )
        self.play(Write(m_num))
        self.wait()


        self.play(
            ShowIncreasingSubsets(females), 
            GrowFromEdge(f_brace, LEFT, rate_func = linear)
        )
        self.play(Write(f_num))
        self.wait()


        # rearrange in grid
        males_grid = [student for student in students if student.sex is "male"]
        females_grid = [student for student in students if student.sex is "female"]
        for male_line, male_grid in zip(males, males_grid):
            male_line.generate_target()
            male_line.target.move_to(male_grid)

        for female_line, female_grid in zip(females, females_grid):
            female_line.generate_target()
            female_line.target.move_to(female_grid)

        self.play(
            LaggedStartMap(MoveToTarget, males, lag_ratio = 0.1, run_time = 4), 
            LaggedStartMap(MoveToTarget, females, lag_ratio = 0.1, run_time = 4),
            *[FadeOut(mob, run_time = 1) for mob in [m_brace, f_brace, m_num, f_num]],
        )
        self.remove(*males, *females)
        self.add(students)
        self.wait()


        self.students = students

    def check_for_bernoulli(self):
        students = self.students 


        cmark = Tex(CMARK_TEX, font_size = 96, color = C_COLOR, tex_template = myTemplate)
        cmark.to_edge(UP).shift(2*RIGHT)

        carrow = Arrow(ORIGIN, 1.5*RIGHT, tip_length = 0.2)
        carrow.next_to(cmark, RIGHT, buff = 0.5)

        cstud = self.get_student(sex = "female")
        cstud.next_to(carrow, RIGHT, buff = 0.5)
        cstud.match_height(cmark)

        self.play(
            LaggedStartMap(DrawBorderThenFill, VGroup(cmark, carrow, cstud), lag_ratio = 0.2), 
            run_time = 4
        )
        self.wait()

        # prop for success
        prob_tex = Tex("Erfolgswahrscheinlichkeit")
        prob_tex.next_to(carrow, DOWN, buff = 0.75)

        prob = MathTex("p", "=", "{" + "9", "\\over", "20" + "}", font_size = 60)\
            .next_to(prob_tex, DOWN)\
            .set_color_by_tex_to_color_map({"9": interpolate_color(RED, DARK_GREY, 0.5), "20": YELLOW_D})

        self.play(Write(prob_tex), run_time = 1)
        self.wait(0.5)
        self.play(Write(prob))
        self.play(Circumscribe(prob, color = C_COLOR, time_width = 0.75, run_time = 3))
        self.wait()

        # picking the first one
        num = random.choice(range(20))

        choosen_one = students[num]
        choosen_one.generate_target()
        choosen_one.target.move_to(cstud.get_left()[0]*RIGHT + DOWN, aligned_edge=LEFT)

        choosen_rect = SurroundingRectangle(choosen_one, color = YELLOW_D)

        if choosen_one.sex is "female":
            mark = Tex(CMARK_TEX, font_size = 96, color = C_COLOR, tex_template = myTemplate)
            new_prob = MathTex("p", "=", "{" + "8", "\\over", "19" + "}", font_size = 60)
        else:
            mark = Tex(XMARK_TEX, font_size = 96, color = X_COLOR, tex_template = myTemplate)
            new_prob = MathTex("p", "=", "{" + "9", "\\over", "19" + "}", font_size = 60)
        mark.move_to(cmark.get_center()[0]*RIGHT + DOWN)
        new_prob.next_to(VGroup(mark, choosen_one.target), DOWN, buff = 0.75)
        new_prob[2].set_color(interpolate_color(RED, DARK_GREY, 0.5))
        new_prob[-1].set_color(YELLOW_E)


        self.play(MoveToTarget(choosen_one, path_arc = -120*DEGREES), run_time = 4)
        self.play(DrawBorderThenFill(mark), run_time = 1.5)
        self.wait()


        self.play(
            LaggedStart(
                *[ApplyWave(student) for student in students if student.sex is "female" and student != choosen_one], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(Write(new_prob))
        self.wait()

        self.play(GrowFromCenter(choosen_rect), run_time = 3)
        self.wait(3)


    # functions
    def get_student(self, sex = None, color = GREEN_B):
        if sex is None:
            color = color
        elif sex is "male":
            color = interpolate_color(BLUE, DARK_GREY, 0.5)
        elif sex is "female":
            color = interpolate_color(RED, DARK_GREY, 0.5)

        body = VMobject()
        body.set_points_smoothly([LEFT, LEFT + 1.25*UP, UP, 1.25*UP + RIGHT, RIGHT, LEFT])
        body.set_fill(color = color, opacity = 1)
        body.set_stroke(width = 2)

        head = Circle()
        head.match_style(body)
        head.set(width = body.width / 2)
        head.next_to(body, UP)

        student = VGroup(head, body)
        student.set(width = 1)

        student.sex = sex
        return student


class NoPuttingBack(Scene):
    def construct(self):
        urn1 = self.get_urn(total_balls = 5, stroke_color = WHITE)
        urn1.shift(4*LEFT + 1.75*UP)

        urn2 = self.get_urn(total_balls = 5, stroke_color = WHITE)
        urn2.shift(4*LEFT + 1.75*DOWN)

        lines1 = VGroup(*[Line(color = GREY) for _ in range(5)])
        for line in lines1:
            line.set_length(0.75)
        lines2 = lines1.copy()
        for lines, urn in zip([lines1, lines2], [urn1, urn2]):
            lines.arrange(RIGHT, buff = 0.2)
            lines.next_to(urn, RIGHT, buff = 2)
            lines.shift(0.5*DOWN)

        bern_succ = MathTex("{2", "\\over", "5}")
        bern_succ.scale(2)
        bern_succ[0].set_color(YELLOW)
        bern_succ.next_to(lines2, RIGHT, buff = 1)
        bern_succ.shift(0.05*UP)


        denom = ValueTracker(5)
        numer = ValueTracker(2)
        numerator = Integer(numer.get_value(), color = YELLOW)
        numerator.add_updater(lambda n: n.set_value(numer.get_value()))
        denominator = Integer(denom.get_value())
        denominator.add_updater(lambda d: d.set_value(denom.get_value()))
        for mob in numerator, denominator:
            mob.scale(2)
        frac_line = bern_succ[1].copy()
        frac_line.next_to(lines1, RIGHT, buff = 1)
        numerator.next_to(frac_line, UP)
        denominator.next_to(frac_line, DOWN)

        prop_succ = Tex("Erfolgswahr-\\\\scheinlichkeit")
        prop_succ.next_to(numerator, UP, buff = 1)

        self.play(
            Create(urn1),
            Create(urn2),
            LaggedStartMap(FadeIn, lines1, shift = DOWN, lag_ratio = 0.2), 
            LaggedStartMap(FadeIn, lines2, shift = UP, lag_ratio = 0.2), 
            *[Write(mob) for mob in [bern_succ, frac_line, numerator, denominator, prop_succ]],
            run_time = 2
        )


        test_list = list(range(5))
        for k in range(5):
            k_rand = test_list.pop(random.randrange(len(test_list)))
            if k_rand == 1 or k_rand == 3:
                numer_anim = [numer.animate.increment_value(-1)]
            else:
                numer_anim = []

            fb1, fb2 = urn1.balls[k_rand], urn2.balls[k_rand]
            fb2.save_state()

            self.play(
                fb1.animate(path_arc = (-160 + 10*k)*DEGREES).next_to(lines1[k], UP),
                fb2.animate(path_arc = (-160 + 10*k)*DEGREES).next_to(lines2[k], UP),
                run_time = 2
            )

            fb2_copy = fb2.copy()
            self.add(fb2_copy)
            self.play(
                Restore(fb2, path_arc = -(-160 + 10*k)*DEGREES),
                denom.animate.increment_value(-1),
                *numer_anim,
                run_time = 2
            )
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
        # balls.move_to(urn).shift(0.25*DOWN)

        return balls


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


        focus_group = VGroup(titles[2], infos[2], symbols[2], arrows[2])
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


class WhereThisIsGoing(Scene):
    def construct(self):
        self.create_bernoulli_trail()
        self.translate_into_formula()
        self.translate_into_visuals()



    def create_bernoulli_trail(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        b_trail = Tex("10", "$\\times$", "Werfen eines Würfels ", "$\\rightarrow$ ", "Primzahl?").to_edge(UP)
        b_trail.set_color_by_tex_to_color_map({"Primzahl?": TEAL, "10": PINK, "$\\times$": PINK})
        succ = Tex("Erfolg:")\
            .next_to(b_trail, DOWN, buff = 0.5)\
            .align_to(b_trail[2:], LEFT)
        fail = Tex("Misserfolg:")\
            .next_to(succ, RIGHT, buff = 3)

        succ_die = VGroup(*[get_die_face(number, dot_color = GREEN).set(height = 0.4) for number in [2,3,5]])
        fail_die = VGroup(*[get_die_face(number, dot_color = RED).set(height = 0.4) for number in [1,4,6]])
        for die, pos_obj in zip([succ_die, fail_die], [succ, fail]):
            die.arrange_submobjects(RIGHT)
            die.next_to(pos_obj, RIGHT)

        succ_brace = Brace(succ_die, DOWN).set_color(GREY)
        fail_brace = Brace(fail_die, DOWN).set_color(GREY)

        succ_prop = MathTex("p", "=", "0.5").next_to(succ_brace, DOWN)
        fail_prop = MathTex("q", "=", "1", "-", "0.5").next_to(fail_brace, DOWN)
        for prop in succ_prop, fail_prop:
            prop.set_color_by_tex_to_color_map({"p": C_COLOR, "q": X_COLOR})

        process = get_random_die()
        process.to_edge(UL)

        self.add(b_trail, succ, fail, succ_die, fail_die, succ_brace, fail_brace, succ_prop, fail_prop, process)
        self.wait(2)

        start_point = config["frame_x_radius"] * LEFT + RIGHT
        step = 1.2*RIGHT
        die_group, cx_marks = VGroup(), VGroup()
        counter = 0

        for i in range(10):
            result = process.copy().clear_updaters()

            if result.submobjects[0].number == 2 or result.submobjects[0].number == 3 or result.submobjects[0].number == 5:
                mark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
                mark.outcome = 1
                counter += 1
            else:
                mark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
                mark.outcome = 0
            cx_marks.add(mark)

            result.generate_target()
            result.target.set(height = 0.8).move_to(start_point + i * step)
            die_group.add(result)

            self.play(MoveToTarget(result), run_time = 1)
            if i < 9:
                self.wait(2.05)

        process.clear_updaters()

        for die, mark in zip(die_group, cx_marks):
            mark.next_to(die, DOWN)

        self.play(
            AnimationGroup(
                *[FadeIn(mark, target_position = die, scale = 0.2) for mark, die in zip(cx_marks, die_group)], 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()


        fade_out_group = VGroup(b_trail, succ, fail, succ_die, fail_die, succ_brace, fail_brace, succ_prop, fail_prop, process)
        self.play(
            FadeOut(fade_out_group, shift = 5*UP), 
            *[group.animate.shift(3*UP) for group in [die_group, cx_marks]], 
            run_time = 2
        )


        self.counter, self.die_group, self.cx_marks = counter, die_group, cx_marks

    def translate_into_formula(self):
        counter, die_group, cx_marks = self.counter, self.die_group, self.cx_marks

        self.play(
            AnimationGroup(
                *[mark.animate(rate_func = there_and_back).shift(0.3*UP) for mark in cx_marks], 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()

        nums = Tex("Anzahlen").to_edge(LEFT).shift(UP)
        nums_uline = Underline(nums)

        texs = VGroup(*[Tex(tex) for tex in ["Wiederholungen", "Erfolge", "Misserfolge"]])
        texs.arrange_submobjects(DOWN, aligned_edge = RIGHT)
        texs.next_to(nums, DOWN, aligned_edge=LEFT)

        decs = VGroup(*[Integer(number) for number in [10, counter, 10 - counter]])
        for tex, dec, d_color in zip(texs, decs, [WHITE, C_COLOR, X_COLOR]):
            dec.next_to(tex, RIGHT, buff = 1, aligned_edge = UP)
            dec.set_color(d_color)

        all_outcomes = VGroup(*[mark.copy() for mark in cx_marks])\
            .arrange_submobjects(RIGHT)\
            .next_to(decs[0], RIGHT, buff = 1)\
            .shift(0.18*LEFT)

        positive_outcomes = VGroup(*[mark.copy() for mark in cx_marks if mark.outcome == 1])\
            .arrange_submobjects(RIGHT)\
            .next_to(decs[1], RIGHT, buff = 1)

        negative_outcomes = VGroup(*[mark.copy() for mark in cx_marks if mark.outcome != 1])\
            .arrange_submobjects(RIGHT)\
            .next_to(decs[2], RIGHT, buff = 1)


        #self.add(all_outcomes, positive_outcomes, negative_outcomes, nums, nums_uline, texs, decs)
        self.play(
            Write(nums, run_time = 1), 
            Create(nums_uline, run_time = 1.5),
            LaggedStartMap(FadeIn, texs, shift = 2*RIGHT, lag_ratio = 0.25, run_time = 2)
        )

        self.play(
            AnimationGroup(
                TransformFromCopy(VGroup(*[mark.copy() for mark in cx_marks if mark.outcome != 1]), negative_outcomes),
                TransformFromCopy(VGroup(*[mark.copy() for mark in cx_marks if mark.outcome == 1]), positive_outcomes),
                TransformFromCopy(VGroup(*[mark.copy() for mark in cx_marks]), all_outcomes),
                lag_ratio = 0.3
            ),
            run_time = 3
        )
        self.play(ShowIncreasingSubsets(decs), run_time = 2)
        self.wait()


        formula = get_binom_formula(10, 0.5, counter)
        formula.scale(1.5).to_edge(DOWN)

        # self.add(formula)
        self.play(Write(formula, lag_ratio = 0.1), run_time = 2)
        self.wait()


        fadeout_group = VGroup(die_group, cx_marks, all_outcomes, positive_outcomes, negative_outcomes, nums, nums_uline, texs, decs)
        self.play(
            FadeOut(fadeout_group, shift = 8*UP), 
            formula.animate.to_edge(UP), 
            run_time = 2
        )

    def translate_into_visuals(self):
        counter = self.counter

        tree = BinomTree(width = config["frame_width"], height = config["frame_height"] - 3, num_events=10)
        tree.to_edge(DOWN)
        self.play(Create(tree))
        self.wait(2)

        data_0 = np.zeros(11)
        histo_0 = Histogram(
            data = data_0, width = config["frame_width"] - 3, height = config["frame_height"] - 3.5,
            y_max_value = 0.27, y_tick_num = 3
        )
        histo_0.to_edge(DOWN)

        dist = scipy.stats.binom(10, 0.5)
        data = np.array([dist.pmf(x) for x in range(0, 11)])
        histo = Histogram(
            data = data, width = config["frame_width"] - 3, height = config["frame_height"] - 3.5,
            y_max_value = 0.27, y_tick_num = 3
        )
        histo.to_edge(DOWN)


        self.play(
            Create(histo_0, run_time = 3), 
            FadeOut(tree, shift = 5*RIGHT, run_time = 1)
        )
        self.play(
            ReplacementTransform(histo_0.bars[counter], histo.bars[counter]),
            run_time = 3
        )
        self.play(
            AnimationGroup(
                *[ReplacementTransform(histo_0.bars[index], histo.bars[index]) for index in range(10) if index != counter],
                lag_ratio = 0.1
            ), 
            run_time = 5
        )
        self.wait(3)


class Thumbnail(Scene):
    def construct(self):

        path = VMobject()
        path.set_points_smoothly([
            6*LEFT + 1*UP,
            5*LEFT + 2*UP, 
            4*RIGHT + 3*UP,
            4*RIGHT + 2*UP,
            5*LEFT + 0.5*DOWN,
            4*LEFT + 3.0*DOWN, 
            5*RIGHT + 2.5*DOWN
        ])
        dpath = DashedVMobject(path, num_dashes = 50)
        dpath.set_stroke(width = 8)
        dpath.set_color(YELLOW_D)

        dice_values = [1,5,4,1,3,6,6,4,1,2]
        dices = VGroup(*[get_die_face(number = num) for num in dice_values])
        for die, prop in zip(dices, [0, 0.1, 0.2, 0.3, 0.45, 0.55, 0.65, 0.82, 0.92, 1]): # np.linspace(0, 1, 10)
            die.set(height = 0.8)
            die.move_to(path.point_from_proportion(prop))

        nums = VGroup(*[MathTex(str(num)) for num in range(1, len(dices) + 1)])
        for num, die in zip(nums, dices):
            num.next_to(die.get_corner(UR), UR, buff = 0.1)
            num.set_color(RED) # "#00f700"


        choices = get_die_faces()
        choices.shift(2*RIGHT + 0.5*DOWN)
        def shuffle_die(mob):
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            mob.become(new_mob)

        first_die = get_die_face(1)

        counter = 0
        num = Integer(counter)\
            .scale(1.5)\
            .move_to(5.5*RIGHT + 1.5*UP)\
            .set_color(YELLOW_D)
        self.add(num)

        for k in range(len(dices)):
            self.play(UpdateFromFunc(first_die, shuffle_die), run_time = 1)
            first_die.become(choices[dice_values[k] - 1])
            self.play(TransformFromCopy(first_die, dices[k]))
            counter += 1
            num.set_value(counter).set_color(YELLOW_D)
        self.wait()


        self.bring_to_back(dpath)
        self.add(nums)
        self.remove(first_die, num)
        self.wait()


        suits = ["diamonds", "hearts", "spades", "clubs"]
        cards = VGroup(*[
            VGroup(*[
                PlayingCard(height = 1.25, value = value, suit = suit, key = None)
                for value in list(range(2, 11)) + ["B", "D", "K", "A"]
            ]).arrange(RIGHT, buff = 0.1)
            for suit in suits
        ]).arrange(DOWN, buff = 0.5)
        cards.center()
        cards.set_fill(opacity = 0.15)
        cards.set_stroke(opacity = 0.15)

        self.bring_to_back(cards)


        trail = Tex("Bernoulli", "$-$", "Kette")
        trail.scale(2.75)
        trail.next_to(cards[2].get_right(), LEFT, aligned_edge=RIGHT)
        trail[0].set_color_by_gradient(BLUE, BLUE_D, BLUE)
        trail[2].set_color_by_gradient(YELLOW_D, YELLOW_E, YELLOW_D)
        trail.set_stroke(BLACK, 1, 1)

        exp = Tex("Bernoulli", "$-$", "Experiment")
        exp.next_to(cards[1].get_right(), LEFT, aligned_edge=RIGHT)
        exp[0].set_color_by_gradient(BLUE, BLUE_D, BLUE)
        exp[2].set_color_by_gradient(YELLOW_D, YELLOW_E, YELLOW_D)

        self.add(trail, exp)







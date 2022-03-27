from ctypes import alignment
from manim import *
from BinomHelpers import *

a_color = YELLOW_D
b_color = GREEN
ab_color = LIGHT_GREY
zero_color = BLUE


def get_blood_type_ball(type = None, height = 2):
    ball = Circle(radius = 1, fill_color = RED, fill_opacity = 1)
    ball.set_stroke(width = 5, color = GREY)
    ball.set_sheen(-0.3, UR)

    symbol_a = Circle(color = a_color)
    symbol_b = Triangle(start_angle = -60*DEGREES, color = b_color)
    symbol_0 = Star(color = zero_color, start_angle = -36*DEGREES).set_stroke(width = 0, opacity = 0)

    if type == "a":
        symbol = symbol_a
    if type == "b":
        symbol = symbol_b
    if type == "0":
        symbol = symbol_0

    ball_center = ball.get_center()
    angles = np.linspace(0, TAU, 8, endpoint=False)
    for x, angle in enumerate(angles):
        tick = Line(color = GREY)
        tick.set_length(0.3)
        tick.next_to(ball.get_start(), RIGHT, buff = 0)

        if type is not "ab":
            symbol_copy = symbol.copy()

        if type is "ab":
            if x % 2 == 0:
                symbol_copy = symbol_a.copy()
            else:
                symbol_copy = symbol_b.copy()

        symbol_copy.set(height = 0.3)
        symbol_copy.next_to(tick, RIGHT, buff = 0)

        tick.set_color([symbol_copy.get_color(), GREY])
        tick.rotate(angle, about_point = ball_center)
        symbol_copy.rotate(angle, about_point = ball_center)

        ball.add(tick, symbol_copy)

    ball.set(height = height)
    ball.ball = ball

    return ball

def get_donator(typ):
    if typ == "a":
        color = a_color
    if typ is "b":
        color = b_color
    if typ is "ab":
        color = ab_color
    if typ is "0":
        color = zero_color

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
    student.typ = typ

    return student


class BloodDonation(Scene):
    def construct(self):


        self.blood_donation()
        self.donations_per_day()


    def blood_donation(self):

        donate = self.donate = self.get_blood_donation()
        self.play(
            DrawBorderThenFill(donate.arm_l), 
            FadeIn(donate.needle_l, shift = 2*UP), 
            run_time = 1.5
        )
        drop = Dot(point = donate.needle_l.get_bottom(), color = RED)
        self.play(
            MoveAlongPath(drop, donate.path_l), 
            FadeIn(donate.path_l),
            run_time = 3
        )
        self.play(
            Create(donate.blood_pack),
            DrawBorderThenFill(donate.blood_inside),
            ApplyMethod(drop.move_to, donate.path_r.get_start(), path_arc = -TAU/2),
        )
        self.play(
            DrawBorderThenFill(donate.arm_r), 
            FadeIn(donate.needle_r, shift = 2*DOWN),
            MoveAlongPath(drop, donate.path_r), 
            FadeIn(donate.path_r),
            run_time = 3
        )
        self.remove(drop)
        self.wait()

        # animation for end of scene
        self.fadeout_anims = [
            *[
                GrowFromPoint(mob, ORIGIN, rate_func = lambda t: smooth(1-t)) 
                for mob in [donate.needle_l, donate.path_l, donate.blood_pack, donate.blood_inside, donate.path_r, donate.needle_r]
            ], 
            FadeOut(donate.arm_l, shift = 3*UP), 
            FadeOut(donate.arm_r, shift = 3*DOWN), 
        ]

    def donations_per_day(self):
        donate = self.donate

        total_val = ValueTracker(0)
        total_dec = Integer(total_val.get_value(), edge_to_fix = RIGHT)
        total_dec.scale(3)
        total_dec.to_edge(DOWN)
        total_dec.add_updater(lambda dec: dec.set_value(total_val.get_value()))
        self.add(total_dec)
        self.play(total_val.animate.set_value(15000), run_time = 1)
        self.wait()

        per_day = Tex("pro\\\\", "Tag")
        per_day.match_height(total_dec[0])
        per_day.next_to(total_dec, LEFT, buff = 0.5)
        self.play(FadeIn(per_day, scale = 0.1))

        self.play(Circumscribe(VGroup(per_day, total_dec), color = BLUE, time_width = 0.75, run_time = 3))
        self.wait()

        # donations per 1000 
        year1 = Tex("2011")
        year2 = Tex("2019")
        for year, arm, direc in zip([year1, year2], [donate.arm_l, donate.arm_r], [LEFT, RIGHT]):
            year.scale(2)
            year.set_color(YELLOW_B)
            year.next_to(arm, direc, buff = 1)

        num_val = ValueTracker(0)
        num_dec = Integer(num_val.get_value())
        num_dec.scale(2)
        num_dec.next_to(year1, DOWN)
        num_dec.add_updater(lambda dec: dec.set_value(num_val.get_value()))

        self.play(
            LaggedStart(
                GrowFromPoint(year1, ORIGIN, path_arc =  120*DEGREES), 
                GrowFromPoint(year2, ORIGIN, path_arc = -120*DEGREES), 
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.add(num_dec)
        self.play(num_val.animate.set_value(95))
        self.wait()

        new_num = num_dec.copy()
        num_dec.clear_updaters()

        self.add(new_num)
        self.play(
            new_num.animate.next_to(year2, UP), 
            num_val.animate.set_value(79), 
            run_time = 3
        )
        self.wait()

        procent = MathTex("-", "17 \\%")
        procent.scale(1.5)
        procent.next_to(new_num, UP)
        procent.set_color(BLUE)

        self.play(GrowFromEdge(procent, DOWN))
        self.wait()
        self.play(GrowFromEdge(procent, UP, rate_func = lambda t: smooth(1-t)))
        self.wait()


        # fadeout 
        self.play(
            *self.fadeout_anims, 
            FadeOut(VGroup(per_day, total_dec), shift = 4*LEFT),
            FadeOut(VGroup(num_dec, year1), shift = 4*LEFT),
            FadeOut(VGroup(new_num, year2), shift = 4*RIGHT),
            run_time = 2
        )


    # functions
    def get_blood_donation(self):
        svg = SVGMobject(SVG_DIR + "Blood_Donation", height = 6)

        # colors 
        arm_l = "#F4C592"
        arm_r = "#FEE7AF"

        svg[0:9].set_stroke(width = 3, color = WHITE)
        svg[9].set_fill(arm_l, 0.4)

        svg[10:19].set_stroke(width = 3, color = WHITE)
        svg[19].set_fill(arm_r, 0.4)

        svg[20:22].set_fill(opacity = 0).set_stroke(width = 5, color = RED)             # blood path
        svg[22:24].set_fill("#9B9B9B", 1)       # needles

        svg[24].set_stroke(width = 3, color = WHITE)    # blood pack
        svg[25].set_fill(RED, 1)                        # blood insinde pack


        svg.arm_l = svg[0:10]
        svg.arm_r = svg[10:20]
        svg.path_l = svg[20]
        svg.path_r = svg[21].reverse_direction()
        svg.needle_r = svg[22]
        svg.needle_l = svg[23]
        svg.blood_pack = svg[24]
        svg.blood_inside = svg[25]

        return svg


class PeopleDonating(Scene):
    def construct(self):
        blood_station = self.get_blood_station()
        blood_station.to_corner(DL, buff = 1)

        entry = blood_station.get_corner(DR) + 3*LEFT + 0.1*UP
        n_donators = 40
        types = 43*["a"] + 11*["b"] + 5*["ab"] + 41*["0"]
        donators = VGroup()
        for x in range(n_donators):
            typ = random.choice(types)
            donator = self.get_donator(typ = typ)
            donators.add(donator)

        donators.next_to(entry, UP, buff = 0.1)
        start = donators.get_center()

        donators.to_edge(RIGHT).shift(1.5*RIGHT)
        self.add(donators)
        end = donators.get_center()

        # show blood_station
        self.play(DrawBorderThenFill(blood_station), run_time = 2)
        self.add(donators)


        # donators going to blood_station
        diff = end - start
        self.play(
            AnimationGroup(
                *[donator.animate(rate_func = linear).shift(-diff) for donator in donators], 
                lag_ratio = 0.2,
            ),
            run_time = n_donators
        )
        self.wait()



    def get_donator(self, typ):
        if typ == "a":
            color = a_color
        if typ is "b":
            color = b_color
        if typ is "ab":
            color = ab_color
        if typ is "0":
            color = zero_color

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

        return student

    def get_blood_station(self):
        blood_station = VMobject()
        blood_station.set_points_as_corners([
            [-3,0,0], 
            [1,0,0], 
            [1,1.25,0], 
            [2,1.25,0], 
            [2,0,0], 
            [3,0,0], 
            [3,2.5,0],
            [-3,2.5,0], 
            [-3,0,0]
        ])
        blood_station.set_fill(GREY, 1)
        blood_station.set_stroke(opacity = 0)

        name = Tex("Blutspende")
        name.set_color_by_gradient(RED_D, RED_B, RED_D)
        name.set_stroke(width = 0.5, color = DARK_GREY)
        name.next_to(blood_station.get_top(), DOWN, buff = 0.45)
        name.set(width = blood_station.width - 1)

        rect1 = Rectangle(width = 1, height = 3, stroke_width = 0, fill_color = RED, fill_opacity = 1)
        rect2 = rect1.copy().rotate(TAU/4)
        cross = VGroup(rect1, rect2)
        cross.set(height = blood_station.height * 1/3)
        cross.next_to(blood_station.get_left() + 0.5*RIGHT).shift(0.35*DOWN)

        blood_station.add(cross)
        blood_station.add(name)

        return blood_station


class TypesOfBlood(Scene):
    def construct(self):
        num_donators = Tex("100", " Spender")
        num_donators.set_color(RED)
        num_donators.next_to(1/9*LEFT + 0.5*DOWN, RIGHT, buff = 0.5, aligned_edge=UP)

        self.play(FadeIn(num_donators, shift = 3*LEFT))
        self.wait()

        types = VGroup(*[self.get_blood_type_ball(type = blood_type, height = 1.75) for blood_type in ["a", "b", "ab", "0"]])
        types.arrange(RIGHT, buff = 1)
        types.to_edge(UP)

        names = VGroup()
        percents = VGroup()
        for type, tex, percent, color in zip(types, ["A", "B", "AB", "0"], [43, 11, 5, 41], [a_color, b_color, ab_color, zero_color]):
            name = Tex(tex)
            name.scale(1.75)
            name.set_color(color)
            name.next_to(type, DOWN, buff = 0.5)
            names.add(name)

            percent = MathTex(str(percent), "\\%")
            percent.scale(1.2)
            percent.set_color(color)
            percent.next_to(name, DOWN)
            percents.add(percent)


        self.play(LaggedStartMap(DrawBorderThenFill, types, lag_ratio = 0.25), run_time = 3)
        self.wait(0.5)

        self.play(LaggedStartMap(FadeIn, names, shift = UP, lag_ratio = 0.25))
        self.wait()

        self.play(GrowFromCenter(percents[0]), run_time = 1.5)
        self.wait()

        self.play(GrowFromCenter(percents[2]), run_time = 1.5)
        self.wait()

        self.play(LaggedStartMap(GrowFromCenter, percents[1::2], lag_ratio = 0.25), run_time = 2)
        self.wait(2)

        # fadeout unnecessary infos
        self.play(
            LaggedStart(
                *[FadeOut(VGroup(name, percent), shift = 5*RIGHT, scale = 0.1) for name, percent in zip(names[1:], percents[1:])], 
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()

        text_start = VGroup(names[0], percents[0]).get_center()
        q1 = Tex("höchstens ", "45")
        q2 = Tex("mindestens ", "36")
        q3 = Tex("mehr als ", "40")
        q4 = Tex("mindestens ", "38", " und ", "höchstens ", "45")
        qs = VGroup(q1, q2, q3, q4)

        for q in qs:
            q.scale(1.25)
            q.next_to(text_start, RIGHT, buff = 1.5)
            q.set_color_by_tex_to_color_map({"mindestens": BLUE, "höchstens": PINK, "mehr als": BLUE_D})

        self.play(Write(q1), run_time = 0.75)
        self.wait()

        for k in range(1, len(qs)):
            self.play(Transform(q1, qs[k]))
            self.wait()
        self.wait(3)

    # functions
    def get_blood_type_ball(self, type = None, height = 2):
        ball = Circle(radius = 1, fill_color = RED, fill_opacity = 1)
        ball.set_stroke(width = 5, color = GREY)
        ball.set_sheen(-0.3, UR)

        symbol_a = Circle(color = a_color)
        symbol_b = Triangle(start_angle = -60*DEGREES, color = b_color)
        symbol_0 = Star(color = zero_color, start_angle = -36*DEGREES).set_stroke(width = 0, opacity = 0)

        if type == "a":
            symbol = symbol_a
        if type == "b":
            symbol = symbol_b
        if type == "0":
            symbol = symbol_0

        ball_center = ball.get_center()
        angles = np.linspace(0, TAU, 8, endpoint=False)
        for x, angle in enumerate(angles):
            tick = Line(color = GREY)
            tick.set_length(0.3)
            tick.next_to(ball.get_start(), RIGHT, buff = 0)

            if type is not "ab":
                symbol_copy = symbol.copy()

            if type is "ab":
                if x % 2 == 0:
                    symbol_copy = symbol_a.copy()
                else:
                    symbol_copy = symbol_b.copy()

            symbol_copy.set(height = 0.3)
            symbol_copy.next_to(tick, RIGHT, buff = 0)

            tick.set_color([symbol_copy.get_color(), GREY])
            tick.rotate(angle, about_point = ball_center)
            symbol_copy.rotate(angle, about_point = ball_center)

            ball.add(tick, symbol_copy)

        ball.set(height = height)

        return ball


class SimplerVersion(Scene):
    def construct(self):
        self.shrink_down_to_40()
        self.bernoulli_trail()


    def shrink_down_to_40(self):
        values = [0.43, 0.11, 0.05, 0.41]
        bar = self.bar = BarChart(
            values, bar_colors = [a_color, b_color, ab_color, zero_color], 
            bar_fill_opacity = 0.6, bar_stroke_width = 2, stroke_color = WHITE,
            n_ticks = 5, max_value = 0.5,
            bar_names = ["A", "B", "AB", "0"]
            # bar_names = ["\\text{Blutgruppe }A", "\\text{Blutgruppe }B", "\\text{Blutgruppe }AB", "\\text{Blutgruppe }0"]
        )
        for name, single_bar, color in zip(bar.bar_labels, bar.bars, [a_color, b_color, ab_color, zero_color]):
            # name.rotate(90*DEGREES)
            name.scale(1.5)
            name.next_to(single_bar, DOWN)
            name.set_color(color)


        value_trackers = [ValueTracker(val) for val in values]
        decimal_numbers = VGroup(*[DecimalNumber(val_track.get_value()) for val_track in value_trackers])
        for dec_num, single_bar in zip(decimal_numbers, bar.bars):
            dec_num.next_to(single_bar, UP)

        self.play(
            Create(bar.x_axis),
            Create(bar.y_axis),
            LaggedStartMap(FadeIn, bar.y_axis_labels, shift = RIGHT, lag_ratio = 0.1),
            LaggedStartMap(FadeIn, bar.bar_labels, shift = UP, lag_ratio = 0.1),
            *[GrowFromEdge(single_bar, DOWN) for single_bar in bar.bars], 
            run_time = 3
        )
        self.play(
            LaggedStartMap(FadeIn, decimal_numbers, shift = DOWN, lag_ratio = 0.1), 
            run_time = 2
        )


        new_values = [0.4, 0.12, 0.06, 0.42]
        decimal_numbers[0].add_updater(lambda dec: dec.set_value(value_trackers[0].get_value()))
        decimal_numbers[1].add_updater(lambda dec: dec.set_value(value_trackers[1].get_value()))
        decimal_numbers[2].add_updater(lambda dec: dec.set_value(value_trackers[2].get_value()))
        decimal_numbers[3].add_updater(lambda dec: dec.set_value(value_trackers[3].get_value()))

        self.play(
            LaggedStart(
                value_trackers[0].animate.set_value(new_values[0]),
                value_trackers[1].animate.set_value(new_values[1]),
                value_trackers[2].animate.set_value(new_values[2]),
                value_trackers[3].animate.set_value(new_values[3]),
                lag_ratio = 0.1
            ),
            LaggedStart(*[
                bar.bars[k].animate.stretch_to_fit_height((new_values[k] / values[k]) * bar.bars[k].height).next_to(bar.bars[k].get_bottom(), UP, buff = 0)
                for k in range(4)], lag_ratio = 0.1
            ),
            LaggedStart(
                *[MaintainPositionRelativeTo(dec_num, single_bar) for dec_num, single_bar in zip(decimal_numbers, bar.bars)],
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.play(Circumscribe(decimal_numbers[0], color = a_color, run_time = 2))
        self.wait()

    def bernoulli_trail(self):
        succ = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate).scale(3).to_edge(UP).shift(3.5*LEFT)
        fail = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate).scale(3).to_edge(UP).shift(3.5*RIGHT)

        fadeout_group = Group(*[x for x in self.mobjects])

        self.play(
            FadeOut(fadeout_group, shift = 4*DOWN, lag_ratio = 0.05), 
            FadeIn(succ, shift = 2*DOWN),
            FadeIn(fail, shift = 2*DOWN),
            run_time = 2
        )

        n_donators = 100
        types = 40*["a"] + 12*["b"] + 6*["ab"] + 42*["0"]
        donators = VGroup()
        for x in range(n_donators):
            typ = random.choice(types)
            donator = get_donator(typ = typ)
            donator.set_fill(opacity = 0.7)
            donator.set(width = 0.35 * 4)
            donators.add(donator)
        donators.center()
        self.add(donators)


        type_a = self.get_donator_type_group(donators, "a")
        type_b = self.get_donator_type_group(donators, "b")
        type_ab = self.get_donator_type_group(donators, "ab")
        type_0 = self.get_donator_type_group(donators, "0")

        for type_group in type_a, type_b, type_ab, type_0:
            type_group.generate_target()
            type_group.target.scale(0.25).arrange_in_grid(cols = 10, rows = 10, buff = 0.2)

        type_a.target.next_to(succ, DOWN)
        type_b.target.next_to(type_a.target, RIGHT, buff = 1.75, aligned_edge=UP)
        type_ab.target.next_to(type_b.target, DOWN, aligned_edge=LEFT)
        type_0.target.next_to(type_ab.target, DOWN, aligned_edge=LEFT)


        self.play(
            LaggedStart(
                *[MoveToTarget(type_group, lag_ratio = 0.05) for type_group in [type_0, type_ab, type_b, type_a]], 
                lag_ratio = 0.1
            ),
            run_time = 8
        )
        types = VGroup(*[Tex(typ, color = typ_color) for typ, typ_color in zip(["A", "B", "AB", "0"], [a_color, b_color, ab_color, zero_color])])
        types[0].next_to(type_a[9], RIGHT)
        types[1].next_to(type_b[0], LEFT)
        types[2].next_to(type_ab[0], LEFT)
        types[3].next_to(type_0[0], LEFT)

        self.play(FadeIn(types[0], shift = LEFT))
        self.play(LaggedStartMap(FadeIn, types[1:], shift = RIGHT, lag_ratio = 0.1), run_time = 1.5)
        self.wait(3)



    # functions 
    def get_donator_type_group(self, donators, typ):
        type_group = VGroup(*[donator for donator in donators if donator.typ is typ])

        return type_group


class AtMost45(HistoScene):
    def construct(self):
        self.n = 100
        self.p = 0.4
        self.k = 45

        self.histo_kwargs = {
            "width": config["frame_width"] * 1.45, "height": config["frame_height"] * 0.2,
            "x_tick_freq": 1, "x_label_freq": 10, "y_max_value": 0.08, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW],
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.to_corner(DL)

        par_values = self.par_values = VGroup(*[MathTex(*tex).scale(0.8) for tex in [["n", "=", str(self.n)], ["p", "=", str(self.p)]]])
        par_values.arrange(DOWN, aligned_edge = LEFT)
        par_values.add_background_rectangle(buff = 0.2, stroke_width = 1, stroke_opacity = 1, stroke_color = WHITE)
        par_values.next_to(histo.axes.c2p(62, 0.08), DL, buff = 0.15)


        self.explain_cumulative()
        self.cas_math()
        self.tables_math()


    def explain_cumulative(self):
        histo, histo_0, par_values = self.histo, self.histo_0, self.par_values

        eq1 = self.eq1 = get_binom_cdf_summands(self.k)
        eq1.to_edge(UP)

        head = eq1[:6].copy()
        head.scale(2)
        head.center()

        brace = Brace(head[2:5], UP, color = GREY)
        text = brace.get_text("höchstens \\\\", "45 ", "Erfolge")
        text.set_color_by_tex_to_color_map({"höchstens": PINK, "45": C_COLOR})

        # add P( ... ) + text
        self.play(
            FadeIn(head[:2]),
            FadeIn(head[-1]),
            FadeIn(brace), 
            Write(text),
        )
        self.wait()
        self.play(Circumscribe(text[0], color = YELLOW_D, time_width = 0.75, run_time = 2))


        self.play(
            AnimationGroup(
                ReplacementTransform(text[1].copy(), head[-2]),     # transform 45 into 45
                FadeIn(head[2], shift = UP),                        # add X
                lag_ratio = 0.5
            ), 
            run_time = 3
        )
        self.play(GrowFromCenter(head[3], run_time = 1.5))          # add =< symbol
        self.wait()


        # connect to histogram
        arrow_kwargs = {"angle": -TAU/4,"color": histo.bars[45].get_color()}
        arrow = CurvedArrow(head[-2].get_right() + 0.1*RIGHT, histo.bars[45].get_top() + 0.1*UP, **arrow_kwargs)


        self.play(
            Create(histo.axes), 
            ReplacementTransform(histo_0.bars, histo.bars),
            FadeIn(par_values[0]), 
            FadeIn(par_values[1], shift = 2*RIGHT), 
            FadeIn(par_values[2], shift = 2*LEFT), 
            run_time = 3
        )
        self.play(Create(arrow), run_time = 2)
        self.highlight_group_of_bars(histo, 0, 45, run_time = 3)
        self.wait()

        # move to edge, fadeout unnecessary things
        self.play(
            FadeOut(VGroup(brace, text), shift = 3*UP),
            FadeOut(arrow),
            head.animate.move_to(eq1[:6]).scale(0.5), 
            run_time = 2
        )
        self.remove(head)
        self.add(eq1[:6])
        self.play(Write(eq1[6:]))
        self.wait()

        # cumulative prob 
        brace = Brace(eq1[7:], DOWN, color = GREY)
        text = brace.get_text("kumulierte Wahrscheinlichkeit")
        self.play(
            FadeIn(brace), 
            Write(text)
        )
        self.wait()

        # Screenrectangle
        screen = ScreenRectangle(height = 2.5, stroke_width = 3, color = GREY)
        screen.next_to(text, DOWN)
        self.play(Create(screen), run_time = 3)
        self.wait(3)

        self.play(FadeOut(screen), run_time = 2)
        self.wait()

    def cas_math(self):
        eq1 = self.eq1

        mathcal = get_binom_cdf_mathcal(self.n, self.p, self.k)
        mathcal.next_to(eq1[6:], DOWN, buff = 1.5, aligned_edge=LEFT)

        short = Tex("Abkürzung für\\\\", "kumulierte Wkt.")
        short.scale(0.6)
        short.next_to(mathcal.get_left(), LEFT, buff = 0.5).shift(0.5*DOWN)
        short_arrow = CurvedArrow(short.get_top() + 0.1*UP, mathcal[1].get_corner(UL), angle = -TAU/3,color = DARK_BLUE)
        self.play(
            Create(short_arrow), 
            FadeIn(short, shift = UP)
        )
        self.wait(0.5)

        result = MathTex("\\approx", get_binom_cdf_result(self.n, self.p, self.k))
        result.next_to(mathcal, DOWN, buff = 0.75, aligned_edge=LEFT)

        cas_arrow = CurvedArrow(mathcal.get_left() + 0.1*LEFT, result.get_left() + 0.1*LEFT, color = GREY, angle = -TAU/4)
        cas_arrow.shift(4*RIGHT)
        cas_command = Tex("binomcdf", "(", str(self.n), ", ", str(self.p), ", ", "0", ", ", str(self.k), ")")
        cas_command.next_to(cas_arrow, RIGHT)
        cas_command[4].set_color(YELLOW_D)
        cas_command[-2].set_color(C_COLOR)

        self.play(Write(mathcal))
        self.wait()

        self.play(Create(cas_arrow), run_time = 1.5)
        self.play(GrowFromPoint(cas_command, cas_arrow.get_right()), run_time = 2)
        self.wait()

        uline = Underline(cas_command, stroke_width = 2, color = DARK_BLUE)
        self.play(Create(uline))
        uline.reverse_direction()
        self.play(Uncreate(uline))
        self.wait()


        self.play(FadeIn(result, shift = 3*LEFT), run_time = 1.5)
        self.wait(0.5)
        self.play(Circumscribe(result, time_width = 0.75, run_time = 3))
        self.wait(2)


        self.play(Unwrite(cas_command))

        self.cas_command, self.cas_arrow = cas_command, cas_arrow

    def tables_math(self):
        tables = Tex("Tabellen")
        tables.next_to(self.cas_arrow, RIGHT)

        self.play(Unwrite(self.cas_command))
        self.play(FadeIn(tables, shift = 3*LEFT), run_time = 2)
        self.wait()

        arrow = Arrow(UP, ORIGIN, tip_length = 0.2)\
            .next_to(tables, DOWN)\
            .set_color(GREY)
        tw = Tex("Tafelwerk")\
            .next_to(arrow, DOWN)\
            .set_color(TEAL)
        self.play(
            LaggedStart(
                GrowArrow(arrow), 
                Write(tw), 
                lag_ratio = 0.4
            ), 
            run_time = 2
        )
        self.wait()


class Tables(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height= 2,
            zoomed_display_width= 5,
            zoomed_display_corner=UP + RIGHT,
            image_frame_stroke_width=5,
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
        x_p_pos = 2.176*LEFT                     # x position p = 0.4
        x_n_pos = 5.77*LEFT                     # x position n = 100 left side
        x_k_pos = 5.58*LEFT

        self.nk_bound_pos = 5.675*LEFT + 3.5*DOWN      # position of bottom boundary line point between n & k

        self.pos_n1 = 4.02*LEFT + 3.44*UP
        self.pos_n2 = x_n_pos + 0.10*DOWN
        self.pos_p = x_p_pos + 3.18*UP
        self.pos_k45 = x_k_pos + 1.07*DOWN


        self.p_pos_45 = x_p_pos + 1.07*DOWN
        self.p_pos_35 = x_p_pos + 0.155*DOWN
        self.p_pos_40 = x_p_pos + 0.617*DOWN # 0.71
        self.p_pos_37 = x_p_pos + 0.34*DOWN

        self.k_pos_45 =  + self.p_pos_45[1]*UP

        self.positions = [self.p_pos_45, self.p_pos_35, self.p_pos_40, self.p_pos_37]

        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_100")
        table.set(height = config["frame_height"] - 0.5)
        table.to_edge(LEFT, buff = 1)


        self.general_settings()
        self.at_most_45()
        self.at_least_36()
        self.more_than_40()
        self.between_38_45()


    def general_settings(self):
        self.play(FadeIn(self.table, shift = LEFT), run_time = 2)

        #######################################################
        # ref_dots = VGroup()
        # for pos in [self.pos_k45]:# self.positions:
        #     dot = Dot(point = pos, color = RED)
        #     ref_dots.add(dot)
        # axes = NumberPlane()
        # # self.add(axes)
        # self.add(ref_dots)
        # self.wait()
        #######################################################


        self.zoomed_display.shift(0.5*DOWN)
        self.zoomed_camera.frame.move_to(self.pos_n1)
        self.activate_zooming(animate=True)
        self.wait()

        self.play(self.zoomed_camera.frame.animate.move_to(self.pos_n2), run_time = 2)
        self.wait(0.5)

        n_par, p_par = self.get_np_group()
        self.play(Write(n_par, shift = 2*LEFT))
        self.wait()

        self.play(FadeIn(p_par, shift = UP), run_time = 1.5)
        self.play(self.zoomed_camera.frame.animate.move_to(self.pos_p), run_time = 2)
        self.wait()


        rect1, rect2 = self.get_npk_block()
        self.play(
            LaggedStart(
                GrowFromEdge(rect1, UP), 
                GrowFromEdge(rect2, LEFT), 
                lag_ratio = 0.1
            ), 
            run_time = 3
        )
        self.wait()


        false_rect1 = rect1.copy().next_to(rect2, RIGHT, buff = 0, aligned_edge=UP).set_fill(ORANGE)
        false_rect2 = rect2.copy().next_to(rect1, RIGHT, buff = 0, aligned_edge=DOWN).set_fill(ORANGE)

        self.play(
            LaggedStart(
                TransformFromCopy(rect2, false_rect2),
                TransformFromCopy(rect1, false_rect1),
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()

        self.play(LaggedStartMap(FadeOut, VGroup(rect1, rect2, false_rect1, false_rect2), lag_ratio = 0.2))
        self.wait()

    def at_most_45(self):
        self.eq_45 = get_binom_cdf_summands(45)[:6]
        self.eq_45.scale(1.5)
        self.eq_45.next_to(self.zoomed_display, DOWN, buff = 0.5)

        self.text_45 = Tex("höchstens ", "45", " Erfolge")
        self.text_45.scale(1.25)
        self.text_45[0].set_color(PINK)
        self.text_45[1].set_color(C_COLOR)
        self.text_45.next_to(self.eq_45, DOWN, aligned_edge = RIGHT)

        self.play(FadeIn(self.text_45, shift = UP))
        self.wait(0.5)
        self.play(Write(self.eq_45))
        self.wait()

        block45 = self.block45 = self.highlight_blocks(self.positions[0])
        k_arrow = self.k_arrow = Arrow(ORIGIN, RIGHT, buff = 0, color = C_COLOR, tip_length = 0.2)
        k_arrow.set_length(0.75)
        k_arrow.next_to(block45, LEFT, buff = 0)
        k_arrow.set_y(self.p_pos_45[1])

        k_val = self.k_val = ValueTracker(0)
        k_tex = self.k_tex = Integer(k_val.get_value(), edge_to_fix = LEFT, color = C_COLOR)
        k_tex.next_to(self.k_arrow, UP, aligned_edge = LEFT)
        k_tex.add_updater(lambda dec: dec.set_value(self.k_val.get_value()).next_to(self.k_arrow, UP, aligned_edge = LEFT))
        self.add(k_tex)
        self.play(
            FadeIn(k_arrow, shift = 4*DOWN),
            k_val.animate.set_value(45),
            run_time = 3
        )
        self.wait()

        # LaggedStartMap(Create, block45, lag_ratio = 0.2), run_time = 3
        self.play(
            GrowFromEdge(block45[0], DR), 
            GrowFromEdge(block45[1], DL), 
            GrowFromEdge(block45[2], UR), 
            GrowFromEdge(block45[3], UL), 
            run_time = 3
        )
        self.play(self.zoomed_camera.frame.animate.move_to(self.p_pos_45), run_time = 3)
        self.wait(3)

    def at_least_36(self):
        self.eq_35 = get_binom_cdf_summands(35)[:6]
        self.eq_35.scale(1.5)
        self.eq_35.move_to(self.eq_45)

        self.text_35 = Tex("höchstens ", "35", " Erfolge")
        self.text_35.scale(1.25)
        self.text_35[0].set_color(PINK)
        self.text_35[1].set_color(C_COLOR)
        self.text_35.next_to(self.eq_45, DOWN, aligned_edge = RIGHT)

        self.play(ReplacementTransform(self.text_45, self.text_35))
        self.wait(0.5)
        self.play(ReplacementTransform(self.eq_45, self.eq_35))
        self.wait()

        block35 = self.block35 = self.highlight_blocks(self.positions[1])
        self.play(
            self.k_val.animate.set_value(35),
            self.k_arrow.animate.set_y(self.p_pos_35[1]),
            ReplacementTransform(self.block45, block35),
            self.zoomed_camera.frame.animate.move_to(self.p_pos_35),
            run_time = 3
        )
        self.wait(3)

    def more_than_40(self):
        self.eq_40 = get_binom_cdf_summands(40)[:6]
        self.eq_40.scale(1.5)
        self.eq_40.move_to(self.eq_45)

        self.text_40 = Tex("höchstens ", "40", " Erfolge")
        self.text_40.scale(1.25)
        self.text_40[0].set_color(PINK)
        self.text_40[1].set_color(C_COLOR)
        self.text_40.next_to(self.eq_45, DOWN, aligned_edge = RIGHT)

        self.play(
            ReplacementTransform(self.text_35, self.text_40),
            ReplacementTransform(self.eq_35, self.eq_40)
        )
        self.play(Flash(self.k_tex))
        self.wait()

        block40 = self.block40 = self.highlight_blocks(self.positions[2])
        self.play(
            self.k_val.animate.set_value(40),
            self.k_arrow.animate.set_y(self.p_pos_40[1]),
            ReplacementTransform(self.block35, block40),
            self.zoomed_camera.frame.animate.move_to(self.p_pos_40),
            run_time = 3
        )
        self.wait(3)

    def between_38_45(self):
        self.eq_37 = get_binom_cdf_summands(37)[:6]
        self.eq_37[3].set_color(BLUE)
        self.eq_37.scale(1.5)
        self.eq_37.move_to(self.eq_45)

        self.text_37 = Tex("höchstens ", "37", " Erfolge")
        self.text_37.scale(1.25)
        self.text_37[0].set_color(BLUE)
        self.text_37[1].set_color(C_COLOR)
        self.text_37.next_to(self.eq_45, DOWN, aligned_edge = RIGHT)

        self.play(
            ReplacementTransform(self.text_40, self.text_37),
            ReplacementTransform(self.eq_40, self.eq_37)
        )
        self.wait()

        block37 = self.block37 = self.highlight_blocks(self.positions[3])
        self.play(
            self.k_val.animate.set_value(37),
            self.k_arrow.animate.set_y(self.p_pos_37[1]),
            ReplacementTransform(self.block40, block37),
            self.zoomed_camera.frame.animate.move_to(self.p_pos_37),
            run_time = 3
        )
        self.wait(3)


    # functions 
    def get_np_group(self):
        n = MathTex("n", "=", "100")
        p = MathTex("p", "=", "0.4")

        group = VGroup(n, p)
        group.arrange(DOWN, aligned_edge = LEFT)
        group.next_to(self.zoomed_display, LEFT, buff = 0.5, aligned_edge = UP)

        return n, p

    def get_npk_block(self):
        rect_vert = Rectangle(width = 0.37, height = 6.79)
        rect_vert.next_to(self.nk_bound_pos, UP, buff = 0)

        rect_hori = Rectangle(width = 3.88, height = 0.21)
        rect_hori.next_to(rect_vert, RIGHT, buff = 0, aligned_edge=UP)

        for rect in rect_vert, rect_hori:
            rect.set_stroke(width = 0)
            rect.set_fill(BLUE, 0.5)

        return rect_vert, rect_hori

    def highlight_blocks(self, pos):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]
        left = self.table.get_left()[0]
        right = self.table.get_right()[0]

        width, height = 0.375, 0.09

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


class AtLeast36(HistoScene):
    def construct(self):
        self.n = 100
        self.p = 0.4
        self.k = 36

        self.histo_kwargs = {
            "width": config["frame_width"] * 1.45, "height": config["frame_height"] * 0.2,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.08, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW], "include_h_lines": False,
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.to_corner(DL)

        par_values = self.par_values = VGroup(*[MathTex(*tex).scale(0.8) for tex in [["n", "=", str(self.n)], ["p", "=", str(self.p)]]])
        par_values.arrange(DOWN, aligned_edge = LEFT)
        par_values.add_background_rectangle(buff = 0.15, stroke_width = 1, stroke_opacity = 1, stroke_color = WHITE)
        par_values.next_to(histo.axes.c2p(62, 0.08), DL, buff = 0.15)


        self.setup_old_scene()
        self.meaning_of_at_least()
        self.donator_animations()
        self.sum_of_successes_bigger_than()
        self.use_complementary_event()


    def setup_old_scene(self):
        self.histo.bars[46:].set_fill(opacity = 0.15),
        self.add(self.histo, self.par_values)
        self.wait(1)
        self.highlight_group_of_bars(self.histo, 0, self.n)
        self.wait()

    def meaning_of_at_least(self):

        eq_least = MathTex("P", "\\big(", "X", "\\geq", str(self.k), "\\big)")
        eq_least[3].set_color(BLUE)
        eq_least[4].set_color(C_COLOR)
        eq_least.scale(2)

        question_mark = Tex("?")
        question_mark.scale(2)
        question_mark.set_color(BLUE)
        question_mark.move_to(midpoint(eq_least[2].get_center(), eq_least[4].get_center()))

        brace = Brace(eq_least[2:5], UP, color = GREY)
        text = brace.get_text("mindestens \\\\", str(self.k), " Erfolge")
        text[0].set_color(BLUE)
        text[1].set_color(C_COLOR)


        # add P( ... ) + text
        self.play(
            FadeIn(eq_least[:2]),
            FadeIn(eq_least[-1]),
            FadeIn(brace), 
            Write(text),
        )
        self.wait()
        self.play(Circumscribe(text[0], color = YELLOW_D, time_width = 0.75, run_time = 2))


        self.play(
            AnimationGroup(
                ReplacementTransform(text[1].copy(), eq_least[-2]),     # transform 36 into 36
                FadeIn(eq_least[2], shift = UP),                        # add X
                GrowFromCenter(question_mark),                          # add ?
                lag_ratio = 0.5
            ), 
            run_time = 3
        )
        self.wait(2)

        self.question_mark, self.eq_least = question_mark, eq_least
        self.least_text, self.brace = text, brace

    def donator_animations(self):
        n_donators = 100
        types = 43*["a"] + 11*["b"] + 5*["ab"] + 41*["0"]
        donators = VGroup()
        for x in range(n_donators):
            typ = random.choice(types)
            donator = self.get_donator(typ = typ)
            donator.set(width = self.histo.bars[0].width)
            donators.add(donator)

        donators.arrange_in_grid(rows = 10, cols = 10, buff = 0.2)
        donators.to_edge(UL)

        self.play(LaggedStartMap(FadeIn, donators, lag_ratio = 0.05), run_time = 3)
        self.wait()

        # group donators due to their blood type
        type_a = self.type_a = self.get_donator_type_group(donators, "a")
        type_b = self.get_donator_type_group(donators, "b")
        type_ab = self.get_donator_type_group(donators, "ab")
        type_0 = self.get_donator_type_group(donators, "0")

        for type_group in type_a, type_b, type_ab, type_0:
            type_group.generate_target()
            type_group.target.arrange_in_grid(cols = 10, rows = 10, buff = 0.2)

        type_a.target.to_corner(UL)
        type_b.target.next_to(type_a.target, DOWN, buff = 1, aligned_edge=LEFT)
        type_0.target.to_corner(UR)
        type_ab.target.next_to(type_0.target, DOWN, buff = 1, aligned_edge=RIGHT)


        self.play(
            LaggedStart(
                *[MoveToTarget(type_group, lag_ratio = 0.05) for type_group in [type_0, type_ab, type_b, type_a]], 
                lag_ratio = 0.1
            ),
            run_time = 6
        )
        self.wait()


        # count number of blood type a and show P(X = ) in histo
        n_type_a = len(type_a)
        val_type_a = ValueTracker(0)
        dec_type_a = Integer(val_type_a.get_value(), edge_to_fix = RIGHT)\
            .scale(2)\
            .to_edge(UP).shift(0.65*RIGHT)\
            .add_updater(lambda dec: dec.set_value(val_type_a.get_value()))

        self.play(Circumscribe(type_a, color = a_color, time_width = 0.75, run_time = 2))
        self.add(dec_type_a)


        added_anims = [
            val_type_a.animate(run_time = 3).set_value(int(n_type_a)),
            *[FadeOut(donators, lag_ratio = 0.1, run_time = 1) for donators in [type_b, type_0, type_ab]],
        ]
        self.highlight_single_bar(self.histo, n_type_a, added_anims, run_time = 3)
        self.play(FocusOn(self.histo.bars[n_type_a]))
        self.play(ApplyWave(self.histo.bars[n_type_a]), run_time = 2)
        self.wait()


        # what if it were 3 more?
        typ = "a"
        extra_donators = VGroup()
        for x in range(3):
            donator = self.get_donator(typ = typ)
            donator.set(width = self.histo.bars[0].width)
            extra_donators.add(donator)

        extra_donators.arrange(RIGHT)
        extra_donators.next_to(type_a[-1], RIGHT)

        self.play(FocusOn(type_a), run_time = 1.5)
        self.play(FadeIn(extra_donators, shift = UP, lag_ratio = 0.2), run_time = 2)
        self.play(val_type_a.animate.set_value(n_type_a + 3), run_time = 2)
        self.wait(0.5)

        self.play(FocusOn(self.histo.bars[n_type_a + 3]), run_time = 1.5)
        self.highlight_single_bar(self.histo, n_type_a + 3, run_time = 2)
        self.wait()

        # shrink down to exactely 36
        diff = n_type_a - self.k

        exactely_36_anims = [
            FadeOut(extra_donators, shift = DOWN, lag_ratio = 0.2), 
            val_type_a.animate.set_value(n_type_a - diff), 
            FadeOut(type_a[n_type_a - diff:], lag_ratio = 0.1)
        ]
        # shrink down to exactely 36
        # exaclty_36_anims = [
        #     FadeOut(type_a[n_type_a - diff:], lag_ratio = 0.1),
        #     val_type_a.animate().set_value(n_type_a - diff)
        # ]
        self.highlight_single_bar(self.histo, n_type_a - diff, added_anims = exactely_36_anims, run_time = 2)
        self.wait()

        text_36andmore = self.text_36andmore = Tex("... ", "36", " und ", "mehr")
        text_36andmore[1].set_color(C_COLOR)
        text_36andmore[3].set_color(BLUE)
        text_36andmore.next_to(self.least_text, RIGHT, buff = 1)

        self.play(Write(text_36andmore))
        self.wait()


        self.fadeout_dec = [FadeOut(dec_type_a, shift = 3*UP)]

    def sum_of_successes_bigger_than(self):

        # show boundary
        lower_bound = Line(DOWN, UP, color = BLUE)\
            .set_length(1)\
            .next_to(self.type_a[self.k-1], LEFT, buff = 0.1, aligned_edge=UP)

        lower_bound_tex = Tex("untere Grenze")\
            .set_color_by_gradient(BLUE, WHITE)\
            .scale(0.8)\
            .next_to(lower_bound, RIGHT, aligned_edge=DOWN)

        bound_histo = self.bound_histo = self.get_boundary_line(self.k)
        self.play(
            GrowFromEdge(lower_bound, UP),
            GrowFromEdge(bound_histo, DOWN),
            FadeIn(lower_bound_tex, shift = 3*LEFT),
            run_time = 3
        )
        self.wait()

        # P ( X >= 36) 
        eq_least_old, least_text = self.eq_least, self.least_text
        self.play(ReplacementTransform(self.question_mark, eq_least_old[3], run_time = 1.5))          # add >= symbol
        self.wait()


        # all bars right next to lower bound
        text_histo_least = Tex("m", "i", "n", "d", "e", "s", "t", "e", "n", "s")\
            .scale(0.75)\
            .set_color(BLUE)
        for x, letter in enumerate(text_histo_least):
            letter.next_to(self.histo.bars[self.k + 2 + x], UP)

        histo_text = [FadeIn(text_histo_least, shift = 0.5*DOWN, lag_ratio = 0.1, rate_func = squish_rate_func(smooth, 0, 0.4))]
        self.highlight_group_of_bars(self.histo, self.k, 100, added_anims = histo_text, run_time = 4)
        self.bring_to_front(bound_histo)
        self.wait()


        # arrange scene
        self.play(
            FadeOut(self.brace),
            *self.fadeout_dec,
            self.least_text.animate.to_edge(UP),
            MaintainPositionRelativeTo(self.text_36andmore, least_text),
            eq_least_old.animate.scale(0.5).to_edge(LEFT).shift(0.25*UP),
            run_time = 3 
        )
        eq_least = self.eq_least = get_binom_cdf_least(self.n, self.k)\
            .next_to(eq_least_old.get_left(), RIGHT, buff = 0)


        # write P(X = 36) + P(X = 37) + .... + P(X = 100)
        self.play(Write(eq_least[6:]))
        self.remove(eq_least_old)
        self.add(eq_least)

        self.play(Circumscribe(eq_least[7:], time_width = 0.75, color = YELLOW_D, run_time = 3))
        self.wait()

    def use_complementary_event(self):
        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[self.k:70]], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[:self.k]], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.play(
            LaggedStart(
                *[bar.animate.set_fill(PINK, 0.6) for bar in self.histo.bars[0:self.k]], 
                lag_ratio = 0.1
            ),
            run_time = 2
        )


        most_text = Tex("höchstens\\\\", "35", " Erfolge")
        most_text[0].set_color(PINK)
        most_text[1].set_color(C_COLOR)
        most_text.next_to(self.least_text, DOWN)

        text_35andless = Tex("... ", "35", " oder ", "weniger")
        text_35andless[1].set_color(C_COLOR)
        text_35andless[3].set_color(PINK)
        text_35andless.next_to(most_text, RIGHT)
        text_35andless.align_to(self.text_36andmore, LEFT)


        self.play(FadeIn(text_35andless, shift = DOWN))
        self.wait() 


        self.play(GrowFromPoint(most_text, text_35andless.get_left()), run_time = 2)
        self.wait()



        text_histo_most = Tex("h", "ö", "c", "h", "s", "t", "e", "n", "s")\
            .scale(0.75)\
            .set_color(PINK)
        for x, letter in enumerate(text_histo_most):
            letter.next_to(self.histo.bars[self.k - 2 - 9 + x], UP)
        self.play(FadeIn(text_histo_most, shift = 0.5*DOWN, lag_ratio = 0.1), run_time = 2)
        self.wait()


        # highlight all --> sum up to 1
        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[:70]], 
                lag_ratio = 0.05
            ),
            run_time = 3
        )


        complement_event = MathTex("=", "1", "-", "P", "\\big(", "X", "\\leq", "35", "\\big)")
        complement_event.next_to(self.eq_least, DOWN)
        complement_event.align_to(self.eq_least[6:], LEFT)
        complement_event[6].set_color(PINK)
        complement_event[7].set_color(C_COLOR)

        self.play(Write(complement_event[:3]))
        self.wait()
        self.play(FadeIn(complement_event[3:], shift = 2*LEFT, scale = 0.1), run_time = 1.5)
        self.add(complement_event)
        self.wait()

        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = YELLOW_D) for mob in [complement_event[1:], complement_event[3:]]
        ])
        self.play(Create(sur_rects[0]), run_time = 3)
        self.wait()

        self.play(Transform(sur_rects[0], sur_rects[1]), run_time = 2)
        self.wait(3)


        result1 = MathTex("\\approx", "1", "-", str(get_binom_cdf_result(self.n, self.p, 35)))
        result1.next_to(complement_event, DOWN, aligned_edge=LEFT)
        self.add(result1[:3])
        self.remove(sur_rects[0])
        self.wait(2)


        self.play(Write(result1[3:]))
        self.wait()

        result2 = MathTex("\\approx", str(1 - get_binom_cdf_result(self.n, self.p, 35)))
        result2.next_to(result1, DOWN, buff = 0.35, aligned_edge=LEFT)

        self.play(
            LaggedStart(
                FadeIn(result2[0], shift = 2*RIGHT),
                FadeIn(result2[1], shift = 2*LEFT),
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.play(Circumscribe(result2, color = YELLOW_D, time_width = 0.75, run_time = 3))
        self.wait(3)


    # functions
    def get_donator(self, typ):
        if typ == "a":
            color = a_color
        if typ is "b":
            color = b_color
        if typ is "ab":
            color = ab_color
        if typ is "0":
            color = zero_color

        student = VMobject()
        student.set_points_smoothly([LEFT, LEFT + 1.25*UP, UP, 1.25*UP + RIGHT, RIGHT, LEFT])
        student.set_fill(color = color, opacity = 1)
        student.set_stroke(width = 1)

        head = Circle()
        head.match_style(student)
        head.set(width = student.width / 2)
        head.next_to(student, UP)

        student.add(head)
        student.set(width = 1)

        student.typ = typ
        return student

    def get_donator_type_group(self, donators, typ):
        type_group = VGroup(*[donator for donator in donators if donator.typ is typ])

        return type_group

    def get_boundary_line(self, k):
        start = self.histo.axes.c2p(k, 0) 
        end = self.histo.axes.c2p(k, 0.1)
        dline = Line(start, end, color = BLUE, stroke_width = 6)

        return dline


class MoreThan40(HistoScene):
    def construct(self):
        self.n = 100
        self.p = 0.4
        self.k = 40

        self.histo_kwargs = {
            "width": config["frame_width"] * 1.45, "height": config["frame_height"] * 0.2,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.08, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW], "include_h_lines": False,
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.to_corner(DL)

        par_values = self.par_values = VGroup(*[MathTex(*tex).scale(0.8) for tex in [["n", "=", str(self.n)], ["p", "=", str(self.p)]]])
        par_values.arrange(DOWN, aligned_edge = LEFT)
        par_values.add_background_rectangle(buff = 0.15, stroke_width = 1, stroke_opacity = 1, stroke_color = WHITE)
        par_values.next_to(histo.axes.c2p(62, 0.08), DL, buff = 0.15)


        self.meaning_of_more_than()
        self.transform_into_at_most()


    def meaning_of_more_than(self):
        self.histo.bars[:36].set_fill(opacity = 0.15),
        self.add(self.histo, self.par_values)
        self.wait(2)


        eq_more_than = MathTex("P", "\\big(", "X", ">", str(self.k), "\\big)")
        eq_more_than[3].set_color(LIGHT_BROWN)
        eq_more_than[4].set_color(C_COLOR)
        eq_more_than.scale(2)

        question_mark = Tex("?")
        question_mark.scale(2)
        question_mark.set_color(LIGHT_BROWN)
        question_mark.move_to(midpoint(eq_more_than[2].get_center(), eq_more_than[4].get_center()))

        greater_than = MathTex("\\geq")
        greater_than.scale(2)
        greater_than.set_color(BLUE)
        greater_than.move_to(midpoint(eq_more_than[2].get_center(), eq_more_than[4].get_center()))

        brace = Brace(eq_more_than[2:5], UP, color = GREY)
        text = brace.get_text("mehr als \\\\", str(self.k), " Erfolge")
        text[0].set_color(LIGHT_BROWN)
        text[1].set_color(C_COLOR)


        # add P( ... ) + text
        self.play(
            FadeIn(eq_more_than[:2]),
            FadeIn(eq_more_than[-1]),
            FadeIn(brace), 
            Write(text),
        )
        self.wait(0.5)
        self.play(Circumscribe(text[0], color = YELLOW_D, time_width = 0.75, run_time = 2))


        self.play(
            AnimationGroup(
                ReplacementTransform(text[1].copy(), eq_more_than[-2]),     # transform 36 into 36
                FadeIn(eq_more_than[2], shift = UP),                        # add X
                GrowFromCenter(question_mark),                          # add ?
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()

        at_least = Tex("mindestens")
        at_least.set_color(BLUE)
        at_least.next_to(eq_more_than, DOWN, buff = 1)
        at_least.shift(LEFT)

        at_least_arrow = CurvedArrow(at_least.get_top(), greater_than.get_bottom() + 0.1*DOWN, color = GREY, angle = TAU/10, tip_length = 0.2)
        self.play(
            Write(at_least), 
            Create(at_least_arrow)
        )
        self.play(ReplacementTransform(question_mark, greater_than))
        self.wait()

        at_least_mean = Tex("4","0","u","n","d","m","e","h","r", color = BLUE)
        for x, letter in enumerate(at_least_mean):
            letter.set(width = self.histo.bars[0].width)
            letter.next_to(self.histo.bars[40 + x], UP, buff = 0.1)

        fade_in_text = [LaggedStartMap(FadeIn, at_least_mean, shift = 0.5*DOWN, lag_ratio = 0.1), ]
        self.highlight_group_of_bars(self.histo, 40, 70, lag_ratio = 0.01, added_anims=fade_in_text, run_time = 3)
        self.wait()

        more_than = Tex("mehr als", color = LIGHT_BROWN)
        more_than.move_to(at_least)

        self.play(FadeTransform(at_least, more_than))
        self.wait()


        added_anims = [
            Transform(greater_than, eq_more_than[3], run_time = 1),
        ]
        self.highlight_group_of_bars(self.histo, 41, 70, added_anims=added_anims, run_time = 2)
        self.wait()

        at_least2_mean = Tex("4","1","u","n","d","m","e","h","r", color = BLUE_D)
        for x, letter in enumerate(at_least2_mean):
            letter.set(width = self.histo.bars[0].width)
            letter.next_to(self.histo.bars[41 + x], UP, buff = 0.1)


        self.play(
            Transform(at_least_mean, at_least2_mean)
        )
        self.wait()


        for mob in text, eq_more_than:
            mob.generate_target()

        eq_more_than.target.scale(0.5).to_corner(UL).shift(DOWN)
        text.target.next_to(eq_more_than.target, UP)

        self.play(
            AnimationGroup(
                FadeOut(greater_than),
                FadeOut(brace), 
                FadeOut(more_than),
                FadeOut(at_least_arrow), 
                MoveToTarget(text),
                MoveToTarget(eq_more_than),
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait()


        self.eq_more_than, self.text_more_than = eq_more_than, text

    def transform_into_at_most(self):
        eq_more_than, text_more_than = self.eq_more_than, self.text_more_than

        eq_at_least = MathTex("=", "P", "\\big(", "X", "\\geq", "41", "\\big)")
        eq_at_least[4].set_color(BLUE)
        eq_at_least[5].set_color(C_COLOR)
        eq_at_least.next_to(eq_more_than, RIGHT)

        text_at_least = Tex("mindestens\\\\", "41", " Erfolge")
        text_at_least[0].set_color(BLUE)
        text_at_least[1].set_color(C_COLOR)
        text_at_least.next_to(eq_at_least[1:], UP)

        self.play(
            FadeIn(text_at_least, shift = DOWN), 
            Write(eq_at_least)
        )
        self.wait()

        eq_compl_event = MathTex("=", "1", "-", "P", "\\big(", "X", "\\leq", "40", "\\big)")
        eq_compl_event[6].set_color(PINK)
        eq_compl_event[7].set_color(C_COLOR)
        eq_compl_event.next_to(eq_at_least, RIGHT)

        text_at_most = Tex("höchstens\\\\", "40", " Erfolge")
        text_at_most[0].set_color(PINK)
        text_at_most[1].set_color(C_COLOR)
        text_at_most.next_to(eq_compl_event[3:], UP)

        # highlight all --> sum up to 1
        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[:70]], 
                lag_ratio = 0.05
            ),
            run_time = 3
        )

        # write as complement event
        arrow_compl = CurvedArrow(
            eq_at_least[4].get_bottom() + 0.2*DOWN, eq_compl_event[6].get_bottom() + 0.2*DOWN, 
            angle = 75*DEGREES, tip_length = 0.2
        )
        arrow_compl.set_color([BLUE, PINK])
        arrow_compl.tip.set_color(PINK)

        text_compl = Tex("Gegenereignis", color = GREY_B)
        text_compl.next_to(arrow_compl, DOWN)

        self.play(
            FadeTransform(eq_at_least[4].copy(), eq_compl_event[6].copy(), path_arc = 75*DEGREES, run_time = 2),
            Create(arrow_compl, run_time = 2),
            FadeIn(text_compl, shift = 2*UP, run_time = 1.5),
            Write(eq_compl_event[:3], run_time = 1)
        )
        self.wait()


        histo_text_most = Tex("4","0","u","n","d","w","e","n","i","g","e","r", color = PINK)
        for x, letter in enumerate(histo_text_most):
            letter.set(width = self.histo.bars[0].width)
            letter.next_to(self.histo.bars[29 + x], UP, buff = 0.1)
        histo_text_most[-4].set(width = self.histo.bars[0].width - 0.1).next_to(self.histo.bars[37], UP, buff = 0.1)

        self.play(
            LaggedStart(*[self.histo.bars[x].animate.set_fill(PINK, 0.6) for x in range(15,41)], lag_ratio = 0.05),
            FadeIn(histo_text_most, shift = 0.5*DOWN, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()
        self.play(FadeIn(text_at_most))
        self.wait(0.5)
        self.play(Write(eq_compl_event[3:]))
        self.wait(2)

        self.play(
            Circumscribe(VGroup(text_at_most, eq_compl_event[3:]), color = LIGHT_BROWN, fade_out = True, run_time = 3)
        )
        self.wait()

        text_compl.scale(0.5).next_to(arrow_compl.get_bottom(), UP, buff = 0.15)

        # switch Scene to Tables and come back
        table_result = MathTex("\\approx", "1", "-", str(get_binom_cdf_result(self.n, self.p, 40)))
        table_result.next_to(arrow_compl, DOWN, buff = 0.5)
        table_result.align_to(eq_compl_event, LEFT)

        self.add(table_result[:3])
        self.wait()

        self.play(FadeIn(table_result[-1], shift = 2*LEFT))
        self.wait()

        sur_rects = VGroup(*[SurroundingRectangle(mob, color = YELLOW_D) for mob in [table_result[3], eq_compl_event[3:]]])
        self.play(LaggedStartMap(Create, sur_rects, lag_ratio = 0.2), run_time = 3)
        self.wait()
        self.play(LaggedStartMap(FadeOut, sur_rects, scale = 4, lag_ratio = 0.2), run_time = 1.5)
        self.wait(0.5)

        result = MathTex("=", "0.4567")
        result.next_to(table_result, DOWN, buff = 0.5, aligned_edge = LEFT)

        self.play(Write(result))
        self.play(Circumscribe(result[1], color = LIGHT_BROWN, run_time = 3))
        self.wait()


        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[41:]], 
                lag_ratio = 0.05
            ),
            run_time = 5
        )
        self.wait(3)


class Between(HistoScene):
    def construct(self):
        self.n = 100
        self.p = 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] * 1.45, "height": config["frame_height"] * 0.2,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.08, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW], "include_h_lines": False,
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        histo_down = self.histo_down = self.get_histogram(self.n, self.p, include_x_labels = True, include_y_labels = False, **self.histo_kwargs)
        histo_mid = self.histo_mid = self.get_histogram(self.n, self.p, include_x_labels = False, include_y_labels = False, **self.histo_kwargs)

        for hist in histo, histo_0, histo_mid, histo_down:
            hist.to_corner(UL)
        histo_mid.next_to(histo, DOWN, buff = 0.5).align_to(histo.axes.c2p(0,0), LEFT)
        histo_down.next_to(histo_mid, DOWN, buff = 0.5).align_to(histo.axes.c2p(0,0), LEFT)

        histo.save_state()
        histo.to_corner(DL)
        self.add(histo)
        self.wait(2)


        self.prob_notation()
        self.seperate_calculations()
        self.do_the_math()


    def prob_notation(self):
        histo = self.histo

        task = Tex("mindestens ", "38", " und ", "höchstens ", "45", " Erfolge")
        task.scale(1.5)
        task.to_edge(DOWN)
        task[0].set_color(BLUE)
        task[1].set_color(C_COLOR)
        task[3].set_color(PINK)
        task[4].set_color(C_COLOR)


        self.play(
            Restore(histo),
            Write(task, rate_func = squish_rate_func(smooth, 0.4, 0.8)), 
            run_time = 3
        )
        self.wait()


        donators = VGroup(*[get_donator("a").set(width = 0.35) for _ in range(38)])
        donators.arrange_in_grid(4, 10, buff = 0.5)
        donators.shift(2.25*DOWN)
        donators.align_to(task, LEFT)

        numbers = VGroup()
        for x, don in enumerate(donators):
            num = MathTex(str(x + 1))
            num.scale(0.4)
            num.next_to(don.get_corner(DR), DR, buff = 0.05)
            numbers.add(num)

        extra_donators = VGroup(*[get_donator("a").set(width = 0.35) for _ in range(8)])
        extra_donators.arrange_in_grid(1, 10, buff = 0.5)
        extra_donators.next_to(donators[-1], RIGHT, buff = 0.6)

        extra_numbers = VGroup()
        for x, don in enumerate(extra_donators):
            num = MathTex(str(38 + x + 1))
            num.scale(0.4)
            num.next_to(don.get_corner(DR), DR, buff = 0.05)
            extra_numbers.add(num)

        self.play(
            LaggedStartMap(FadeIn, donators, lag_ratio = 0.05), 
            LaggedStartMap(GrowFromCenter, numbers, lag_ratio = 0.05), 
            run_time = 3
        )
        self.play(
            LaggedStartMap(DrawBorderThenFill, extra_donators, lag_ratio = 0.05), 
            LaggedStartMap(GrowFromCenter, extra_numbers, lag_ratio = 0.05), 
            run_time = 3
        )
        self.wait()


        succ_group = VGroup(donators[-1], numbers[-1], *extra_donators[:-1], extra_numbers[:-1])
        succ_rect = SurroundingRectangle(succ_group)
        succ_rect.set_color([PINK, BLUE])
        succ_group.add(succ_rect)

        self.play(FadeIn(succ_rect, scale = 3), run_time = 2)
        self.wait()

        text_most = Tex("höchstens \\\\", "45", " Erfolge")
        text_most[0].set_color(PINK)
        text_most[1].set_color(C_COLOR)
        text_most.next_to(histo.bars[40], RIGHT, buff = 1.5, aligned_edge=UP)

        text_least = Tex("mindestens \\\\", "38", " Erfolge")
        text_least[0].set_color(BLUE)
        text_least[1].set_color(C_COLOR)
        text_least.next_to(histo.bars[40], LEFT, buff = 1.5, aligned_edge=UP)


        fadeout_anims = [
            LaggedStartMap(FadeOut, donators[:37], lag_ratio = 0.05),
            LaggedStartMap(FadeOut, numbers[:37], lag_ratio = 0.05),
            LaggedStartMap(FadeOut, extra_donators[-1], lag_ratio = 0.05),
            LaggedStartMap(FadeOut, extra_numbers[-1], lag_ratio = 0.05),
            GrowFromPoint(succ_group, histo.axes.c2p(41.5, 0.04), rate_func = lambda t: smooth(1-t)),
        ]
        self.highlight_group_of_bars(histo, 38, 45, added_anims = fadeout_anims, run_time = 4)
        self.wait()


        eq_least = MathTex("X", "\\geq", "38")
        eq_most = MathTex("X", "\\leq", "45")
        for equ in eq_least, eq_most:
            equ.scale(1.5)
            equ.set_color_by_tex_to_color_map({"\\geq": BLUE, "\\leq": PINK, "38": C_COLOR, "45": C_COLOR})
        eq_least.next_to(task[:2], UP, buff = 1.75)
        eq_most.next_to(task[3:5], UP, buff = 1.75)

        self.play(FadeIn(eq_least, shift = UP), run_time = 2)
        self.wait()
        self.play(FadeIn(eq_most, shift = UP), run_time = 2)
        self.wait()


        between = MathTex("38", "\\leq", "X", "\\leq", "45")
        between.scale(1.5)
        between[0].set_color(C_COLOR)
        between[1].set_color(BLUE)
        between[3].set_color(PINK)
        between[4].set_color(C_COLOR)
        between.next_to(eq_most.get_right(), LEFT, buff = 0)

        self.play(
            AnimationGroup(
                FadeTransform(eq_least[0], between[2], path_arc = -120*DEGREES),
                FadeTransform(eq_least[1], between[1], path_arc = -105*DEGREES),
                FadeTransform(eq_least[2], between[0], path_arc = -90*DEGREES),
                lag_ratio = 0.5
            ),
            run_time = 4
        )
        self.add(between)
        self.remove(eq_least, eq_most)
        self.wait()

        arrows_least = VGroup()
        arrow1 = CurvedArrow(between[2].get_top(), between[1].get_top(), color = YELLOW_D, tip_length = 0.15)
        arrow2 = CurvedArrow(between[1].get_top(), between[0].get_top(), color = YELLOW_D, tip_length = 0.15)
        arrows_least.add(arrow1, arrow2)
        arrows_least.shift(0.1*UP)

        arrows_most = VGroup()
        arrow3 = CurvedArrow(between[2].get_bottom(), between[3].get_bottom(), color = YELLOW_D, tip_length = 0.15)
        arrow4 = CurvedArrow(between[3].get_bottom(), between[4].get_bottom(), color = YELLOW_D, tip_length = 0.15)
        arrows_most.add(arrow3, arrow4)
        arrows_most.shift(0.1*DOWN)

        self.play(Succession(Create(arrows_least), lag_ratio = 0.5), run_time = 1.5)
        self.wait(0.5)
        self.play(Succession(Create(arrows_most), lag_ratio = 0.5), run_time = 1.5)
        self.wait()

        self.play(FadeOut(VGroup(*arrows_least, *arrows_most), lag_ratio = 0.15), run_time = 3)
        self.wait()


        eq = self.eq = MathTex("P", "\\big(", "38", "\\leq", "X", "\\leq", "45", "\\big)")
        eq.set_color_by_tex_to_color_map({"\\leq": PINK, "38": C_COLOR, "45": C_COLOR})
        eq[3].set_color(BLUE)
        eq.next_to(histo.axes.c2p(1, 0.05), RIGHT, aligned_edge=LEFT)

        between.generate_target()
        between.target.scale(2/3).move_to(eq[2:-1])

        self.play(
            AnimationGroup(
                FadeIn(eq[:2]),
                MoveToTarget(between),
                FadeIn(eq[-1]),
                ReplacementTransform(task[:2], text_least),
                ReplacementTransform(task[3:], text_most),
                FadeOut(task[2], shift = 3*DOWN),
                lag_ratio = 0.2
            ),
            run_time = 4
        )
        self.add(eq)
        self.remove(between)
        self.wait()

    def seperate_calculations(self):
        histo, histo_down, histo_mid = self.histo, self.histo_down, self.histo_mid

        # add middle histo
        self.play(FadeIn(histo_mid, shift = 3*DOWN), run_time = 2)

        k_val = self.k_val = ValueTracker(45)
        hbar = always_redraw(lambda: self.get_highlight_bar())
        self.play(Write(hbar), run_time = 1.5)
        self.wait(0.5)

        self.play(
            LaggedStart(*[histo_mid.bars[x].animate.set_fill(color = PINK, opacity = 0.6) for x in reversed(range(46))], lag_ratio = 0.05),
            LaggedStart(*[histo_mid.bars[x].animate.set_fill(opacity = 0.15) for x in range(46, 70)], lag_ratio = 0.05),
            k_val.animate.set_value(0),
            run_time = 4
        )

        eq1 = MathTex("P", "\\big(", "X", "\\leq", "45", "\\big)")
        eq1[3].set_color(PINK)
        eq1[4].set_color(C_COLOR)
        eq1.next_to(histo_mid.axes.c2p(1, 0.05), RIGHT, aligned_edge=LEFT)

        self.play(FadeIn(eq1, shift = 3*LEFT), run_time = 1.5)
        self.wait()

        # add bottom histo
        self.play(FadeIn(histo_down, shift = 2.5*DOWN), run_time = 2)

        self.play(
            LaggedStart(*[histo_down.bars[x].animate.set_fill(color = BLUE, opacity = 0.6) for x in range(38)], lag_ratio = 0.05),
            LaggedStart(*[histo_down.bars[x].animate.set_fill(opacity = 0.15) for x in range(38, 70)], lag_ratio = 0.05),
            k_val.animate.set_value(38),
            run_time = 4
        )
        self.wait()

        eq2 = MathTex("P", "\\big(", "X", "\\leq", "37", "\\big)")
        eq2[3].set_color(BLUE)
        eq2[4].set_color(C_COLOR)
        eq2.next_to(histo_down.axes.c2p(1, 0.05), RIGHT, aligned_edge=LEFT)

        self.play(FadeIn(eq2, shift = 3*LEFT), run_time = 1.5)
        self.wait(0.5)

        self.play(Circumscribe(eq2[4], color = YELLOW_D, fade_out = True, run_time = 3))

        left, right = self.get_highlight_lines()
        hbar.clear_updaters()
        self.play(
            FadeOut(hbar), 
            Create(left), 
            Create(right), 
            run_time = 3
        )


        self.play(Wiggle(histo.bars[38], scale_value = 1.2, run_time = 2))
        self.wait(0.5)
        self.play(Wiggle(histo_down.bars[38], scale_value = 1.2, run_time = 2))
        self.wait()


        self.eq1, self.eq2, self.left, self.right = eq1, eq2, left, right

    def do_the_math(self):
        equals, minus = MathTex("="), MathTex("-")

        eq_group = VGroup(self.eq, equals, self.eq1, minus, self.eq2)
        eq_group.generate_target()
        eq_group.target.arrange(RIGHT, buff = 0.5).center()

        self.play(
            AnimationGroup(
                FadeOut(self.histo_mid), 
                FadeOut(self.histo_down),
                GrowFromEdge(self.left, UP, rate_func = lambda t: smooth(1-t)),
                GrowFromEdge(self.right, UP, rate_func = lambda t: smooth(1-t)),
                MoveToTarget(eq_group, lag_ratio = 0.1),
                lag_ratio = 0.05
            ), 
            run_time = 4
        )
        self.wait()

        result45 = MathTex(str(get_binom_cdf_result(self.n, self.p, 45)))
        result37 = MathTex(str(get_binom_cdf_result(self.n, self.p, 37)))
        equals2, minus2 = MathTex("\\approx"), minus.copy()

        for mob, ref_mob in zip([equals2, result45, minus2, result37], eq_group[1:]):
            mob.move_to(ref_mob)
            mob.shift(DOWN)

        self.play(Write(equals2))
        self.wait(0.5)
        self.play(FadeIn(result45, shift = DOWN, scale = 0.1), run_time = 2)
        self.wait(0.5)

        self.play(Create(minus2))
        self.wait(2)

        self.play(FadeIn(result37, shift = 2*LEFT, scale = 0.1), run_time = 2)
        self.wait()

        result = MathTex("=", "0.5621")
        result.next_to(equals2, DOWN, buff = 1, aligned_edge=LEFT)
        self.play(Write(result[0]))
        self.wait(0.5)

        result[1].align_to(result45, LEFT)
        self.play(Write(result[1]))
        self.play(
            Circumscribe(result[1], color = YELLOW_D, run_time = 3), 
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.5*UP) for bar in self.histo.bars[38:46]], 
                lag_ratio = 0.05, run_time = 3
            )
        )
        self.wait(3)


    # functions 
    def get_highlight_bar(self):
        bar_width = self.histo.bars[0].width
        bar = Rectangle(width = bar_width, height = 7.5, stroke_width = 0, fill_color = PINK, fill_opacity = 0.35)
        bar.next_to(self.histo.axes.c2p(self.k_val.get_value() + 0.5, 0.1), DOWN, buff = 0)

        return bar

    def get_highlight_lines(self):
        right = DashedLine(
            start = self.histo.axes.c2p(46, 0.1), end = self.histo_down.axes.c2p(46, -0.03), 
            color = YELLOW_D
        )
        left = DashedLine(
            start = self.histo.axes.c2p(38, 0.1), end = self.histo_down.axes.c2p(38, -0.03), 
            color = YELLOW_D
        )

        return left, right 


class Summary(HistoScene):
    def construct(self):
        self.n = 20
        self.p = 0.25

        self.histo_kwargs = {
            "width": config["frame_width"] - 2, "height": config["frame_height"] * 0.2,
            "x_tick_freq": 1, "x_label_freq": 2, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW], "include_h_lines": False,
        }

        histo = self.histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo_0 = self.get_histogram(self.n, self.p, zeros = True, **self.histo_kwargs)
        for hist in histo, histo_0:
            hist.center().to_edge(DOWN)

        np_group = self.np_group = self.get_np_group()
        np_group.move_to(histo.axes.c2p(19, 0.1))

        self.play(
            Create(histo.axes, run_time = 2),
            ReplacementTransform(histo_0.bars, histo.bars, run_time = 4), 
            Write(np_group, rate_func = squish_rate_func(smooth, 0.66, 1), run_time = 4), 
        )
        for bar in histo.bars:
            bar.save_state()

        self.show_parameters()
        self.at_least()
        self.more_than()
        self.between()


    def show_parameters(self):
        arrows_np = VGroup(*[Arrow(ORIGIN, RIGHT, buff = 0, tip_length = 0.2, stroke_width = 3) for _ in range(2)])
        for arrow, parameter in zip(arrows_np, self.np_group):
            arrow.next_to(parameter, LEFT, buff = 0.5)

        text_n = Tex("Anzahl Wiederholungen")
        text_p = Tex("Erfolgswahrscheinlichkeit")

        for text, arrow in zip([text_n, text_p], arrows_np):
            text.scale(0.8)
            text.add_background_rectangle()
            text.next_to(arrow, LEFT)

        self.play(
            Create(arrows_np, lag_ratio = 0.1),
            AnimationGroup(FadeIn(text_n, shift = RIGHT), FadeIn(text_p, shift = RIGHT), lag_ratio = 0.2), 
            run_time = 1.5
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(text_n, text_p, *arrows_np), lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait()

    def at_least(self):
        title = self.title1 = self.get_title("Mindestens", BLUE)
        eq = get_binom_cdf_least(self.n, 6)
        eq.shift(1.5*UP)

        self.play(
            FadeIn(title, shift = 2*DOWN),
            Write(eq[:7])
        )
        self.play(LaggedStartMap(FadeIn, eq[7:], shift = UP, lag_ratio = 0.05), run_time = 2)
        self.highlight_group_of_bars(self.histo, 6, self.n, lag_ratio = 0.1, run_time = 3)
        self.wait()

        self.play(
            LaggedStart(
                *[bar.animate(rate_func = there_and_back).shift(0.35*UP) for bar in self.histo.bars], 
                lag_ratio = 0.05, run_time = 2
            )
        )
        self.wait(0.5)

        eq_kum = MathTex("=", "1", "-", "P", "\\big(", "X", "\\leq", "5", "\\big)")
        eq_kum[6].set_color(PINK)
        eq_kum[7].set_color(C_COLOR)
        eq_kum.next_to(eq, DOWN, buff = 0.5)
        eq_kum.align_to(eq[6:], LEFT)

        self.play(
            LaggedStart(*[bar.animate.set_fill(PINK, opacity = 0.6) for bar in self.histo.bars[:6]]), 
            run_time = 2
        )
        self.play(Write(eq_kum))
        self.wait()

        sur_rect = SurroundingRectangle(eq_kum[3:], color = YELLOW_D)
        self.play(Create(sur_rect), run_time = 2)
        self.wait()


        arrow = CurvedArrow(eq[4].get_bottom() + 0.1*DOWN, eq_kum[-2].get_bottom() + 0.1*DOWN, angle = 150*DEGREES, color = YELLOW_D, tip_length = 0.25)
        self.play(ReplacementTransform(sur_rect, arrow))
        self.wait()

        sub = MathTex("-", "1", color = YELLOW_D)
        sub.add_background_rectangle()
        sub.next_to(arrow.point_from_proportion(0.9), DOWN)
        self.play(FadeIn(sub, shift = UP))
        self.wait(3)

        self.fadeout_anim = [LaggedStartMap(FadeOut, VGroup(sub, arrow, eq_kum, eq), scale = 0.5, shift = UP, lag_ratio = 0.1, run_time = 2)]

    def more_than(self):
        title = self.title2 = self.get_title("mehr als", LIGHT_BROWN)

        eq = MathTex(
            "P", "\\big(", "X", ">", "4", "\\big)", "=", 
            "P", "\\big(", "X", "=", "5", "\\big)", "+",
            #                                     20
            "P", "\\big(", "X", "=", "6", "\\big)", "+",
            #          22
            "\\ldots", "+",
            #                          27
            "P", "\\big(", "X", "=", "20", "\\big)"
        )
        eq.set_color_by_tex_to_color_map({"+": LIGHT_BROWN})
        eq[3].set_color(LIGHT_BROWN)
        eq[4].set_color(C_COLOR)
        eq[11].set_color(C_COLOR)
        eq.shift(1.5*UP)

        self.play(
            ReplacementTransform(self.title1, title), 
            *self.fadeout_anim,
            Write(eq),
            LaggedStart(*[Restore(bar) for bar in self.histo.bars], lag_ratio = 0.1)
        )
        self.wait()

        arrow = CurvedArrow(eq[4].get_bottom() + 0.1*DOWN, eq[11].get_bottom() + 0.1*DOWN, color = YELLOW_D, tip_length = 0.25)
        self.play(Create(arrow), run_time = 1.5)
        self.play(
            LaggedStartMap(Indicate, VGroup(eq[11], self.histo.bars[5]), color = YELLOW_D, lag_ratio = 0.25), 
            run_time = 3
        )
        self.highlight_group_of_bars(self.histo, 5, 21, run_time = 2)
        self.wait()

        at_least5 = MathTex("=", "P", "\\big(", "X", "\\geq", "5", "\\big)")
        at_least5[4].set_color(BLUE)
        at_least5[5].set_color(C_COLOR)
        at_least5.next_to(eq, DOWN, buff = 0.5)
        at_least5.align_to(eq[6:], LEFT)
        sur_rect = SurroundingRectangle(at_least5[1:])
        
        self.play(
            ReplacementTransform(arrow, sur_rect), 
            Write(at_least5)
        )
        self.wait()


        at_most4 =  MathTex("=", "1", "-", "P", "\\big(", "X", "\\leq", "4", "\\big)")
        at_most4[6].set_color(PINK)
        at_most4[7].set_color(C_COLOR)
        at_most4.next_to(at_least5, DOWN, buff = 0.5, aligned_edge=LEFT)
        sur_rect2 = SurroundingRectangle(at_most4[3:])

        self.play(Write(at_most4[:3]))
        self.play(
            LaggedStart(*[self.histo.bars[:5].animate.set_fill(PINK, 0.6)], lag_ratio = 0.1), 
            run_time = 2
        )
        self.play(ReplacementTransform(sur_rect, sur_rect2))
        self.play(Write(at_most4[3:]))
        self.wait(3)

        self.fadeout_anim2 = [LaggedStartMap(FadeOut, VGroup(sur_rect2, at_most4, at_least5, eq), shift = 4*RIGHT, lag_ratio = 0.1)]

    def between(self):
        title = Tex("Mindestens", " ...", " und ", "... ", "höchstens")\
            .scale(1.5)\
            .to_edge(UP)
        title[0].set_color(BLUE)
        title[-1].set_color(PINK)

        brace = Brace(self.histo.bars[4:9], UP, color = GREY)
        brace_text = MathTex("4", "\\leq", "X", "\\leq", "8")
        brace_text.next_to(brace, UP)
        brace_text[0].set_color(C_COLOR)
        brace_text[1].set_color(BLUE)
        brace_text[3].set_color(PINK)
        brace_text[4].set_color(C_COLOR)

        self.play(
            ReplacementTransform(self.title2, title),
            LaggedStart(*[Restore(bar) for bar in self.histo.bars], lag_ratio = 0.1), 
            *self.fadeout_anim2, 
            Create(brace), 
            run_time = 2
        )

        self.play(
            AnimationGroup(
                LaggedStart(*[self.histo.bars[k].animate.set_fill(opacity = 0.15) for k in [0,1,2,3,9,10,11,12]], lag_ratio = 0.1),
                TransformFromCopy(self.histo.axes.x_labels[2], brace_text[0]),
                TransformFromCopy(self.histo.axes.x_labels[4], brace_text[4]),
                Write(brace_text[2]),
                FadeIn(brace_text[1], shift = DOWN),
                FadeIn(brace_text[3], shift = DOWN),
                lag_ratio = 0.1
            ),
            run_time = 4
        )
        self.wait()

        eq = MathTex("P", "\\big(", "4", "\\leq", "X", "\\leq", "8", "\\big)")
        eq[2].set_color(C_COLOR)
        eq[3].set_color(BLUE)
        eq[5].set_color(PINK)
        eq[6].set_color(C_COLOR)
        eq.shift(1.5*UP + 4*LEFT)

        self.play(
            Write(eq[:2]), 
            Write(eq[-1]), 
            brace_text.animate.move_to(eq[2:-1]),
            Uncreate(brace),
            run_time = 2
        )
        self.remove(brace_text)
        self.add(eq)
        self.wait()

        #                 0    1      2       3      4      5      6       7    8
        eq_add = MathTex("=", "P", "\\big(", "X", "\\leq", "8", "\\big)", "-", "P", "\\big(", "X", "\\leq", "3", "\\big)")
        eq_add.next_to(eq, RIGHT)
        eq_add[4].set_color(PINK)
        eq_add[5].set_color(C_COLOR)
        eq_add[11].set_color(BLUE)
        eq_add[12].set_color(C_COLOR)

        brace8 = Brace(self.histo.bars[:9], UP, color = GREY)
        brace8_tex = MathTex("P", "\\big(", "X", "\\leq", "8", "\\big)")
        brace8_tex.next_to(brace8, UP)
        brace8_tex[3].set_color(PINK)
        brace8_tex[4].set_color(C_COLOR)

        brace3 = Brace(self.histo.bars[:4], UP, color = GREY)
        brace3.set_y(brace8.get_y())
        brace3_tex = MathTex("P", "\\big(", "X", "\\leq", "3", "\\big)")
        brace3_tex.next_to(brace3, UP)
        brace3_tex[3].set_color(BLUE)
        brace3_tex[4].set_color(C_COLOR)

        self.play(
            Create(brace8), 
            FadeIn(brace8_tex, shift = DOWN), 
            LaggedStart(*[self.histo.bars[k].animate.set_fill(opacity = 0.6) for k in [0,1,2,3]], lag_ratio = 0.1),
            run_time = 1.5
        )

        first = brace8_tex.copy()
        self.play(
            Write(eq_add[0]),
            first.animate(run_time = 2.5).move_to(eq_add[1:7])
        )
        self.wait()


        self.play(
            AnimationGroup(
                ReplacementTransform(brace8, brace3), 
                ReplacementTransform(brace8_tex, brace3_tex), 
                LaggedStart(*[self.histo.bars[k].animate.set_fill(opacity = 0.15) for k in range(4, 20)], lag_ratio = 0.1),
                lag_ratio = 0.1
            ), 
            run_time = 3.5
        )
        self.wait(0.5)

        second = brace3_tex.copy()
        self.play(
            Write(eq_add[7]), 
            second.animate(run_time = 2.5).move_to(eq_add[8:]),
            FadeOut(brace3), 
            FadeOut(brace3_tex),
            LaggedStart(*[self.histo.bars[k].animate.set_fill(opacity = 0.15) for k in [0,1,2,3,9,10,11,12]], lag_ratio = 0.1),
            LaggedStart(*[self.histo.bars[k].animate.set_fill(opacity = 0.6) for k in range(4, 9)], lag_ratio = 0.1),
        )
        self.wait()

        sur_rects = VGroup(*[SurroundingRectangle(part, color = YELLOW_D) for part in [eq_add[1:7], eq_add[8:]]])
        self.play(LaggedStartMap(Create, sur_rects, lag_ratio = 0.25), run_time = 3)
        self.wait()
        self.play(LaggedStartMap(FadeOut, sur_rects, scale = 4, lag_ratio = 0.25), run_time = 2)

        arrow = CurvedArrow(eq[2].get_bottom() + 0.1*DOWN, eq_add[12].get_bottom() + 0.1*DOWN, angle = 60*DEGREES, color = YELLOW_D, tip_length = 0.25)
        sub = MathTex("-", "1", color = YELLOW_D)
        sub.add_background_rectangle()
        sub.next_to(arrow.point_from_proportion(0.9), DOWN)
        self.play(Create(arrow), run_time = 2)
        self.play(FadeIn(sub, shift = UP))
        self.wait(3)


    # functions 
    def get_np_group(self):
        n = MathTex("n", "=", str(self.n)).scale(0.8)
        p = MathTex("p", "=", str(self.p)).scale(0.8)

        group = VGroup(n,p)
        group.arrange(DOWN, aligned_edge = LEFT)
        sur_rect = SurroundingRectangle(group, color = WHITE, stroke_width = 2)
        group.add(sur_rect)

        return group

    def get_title(self, name, color):
        title = Tex(name)
        title.scale(1.5)
        title.set_color(color)
        title.to_edge(UP)

        return title


class Thumbnail(HistoScene, BloodDonation):
    def construct(self):
        self.n = 100
        self.p = 0.4

        self.histo_kwargs = {
            "width": config["frame_width"] * 1.45, "height": config["frame_height"] * 0.3,
            "x_tick_freq": 1, "x_label_freq": 5, "y_max_value": 0.08, "y_tick_num": 2,
            "bar_colors": [BLUE, GREEN, YELLOW], "include_h_lines": False,
        }

        histo = self.get_histogram(self.n, self.p, **self.histo_kwargs)
        histo.to_edge(DOWN, buff = 0.1).shift(1*LEFT)
        self.add(histo.bars[20:65], histo.axes.x_labels[5:12])


        # probabilities
        eq1 = get_binom_cdf_summands(35)[:6]
        eq1.scale(1.35)
        eq1.move_to(histo.axes.c2p(28,0.04)) #.to_corner(UL).shift(0.6*RIGHT)
        eq1.rotate(30*DEGREES)
        self.add(eq1)

        eq2 = MathTex("P", "\\big(", "39", "\\leq", "X", "\\leq", "43", "\\big)")
        eq2.scale(1.35)
        eq2.next_to(histo.bars[40], UP, buff = 0.1) # next_to(eq1, DOWN)
        eq2.shift(0.3*LEFT)
        eq2[2].set_color(C_COLOR)
        eq2[3].set_color(BLUE)
        eq2[5].set_color(PINK)
        eq2[6].set_color(C_COLOR)
        self.add(eq2)

        eq3 = get_binom_cdf_least(100, 46)[:6].scale(1.35).move_to(histo.axes.c2p(60, 0.02)) # next_to(eq2, DOWN)
        self.add(eq3)

        # bars manipulation
        histo.bars.set_fill(opacity = 0.15)
        histo.bars[:36].set_fill(color = PINK, opacity = 0.6)
        histo.bars[46:].set_fill(color = BLUE, opacity = 0.6)
        histo.bars[39:44].set_fill(color = YELLOW_D, opacity = 0.6)


        # texts
        at_least = Tex("Mindestens ...", color = BLUE)
        at_most = Tex("Höchstens ...", color = PINK)
        more_than = Tex("Mehr als ...", color = LIGHT_BROWN)

        texts = VGroup(at_least, at_most, more_than)
        for text in texts:
            text.scale(1.75)
        texts.arrange(DOWN)
        texts.to_corner(UL)

        self.add(texts)


        # blood
        blood_types = VGroup(*[get_blood_type_ball(type = typ, height = 1) for typ in ["a", "b", "ab", "0"]])
        blood_types.arrange(RIGHT)
        blood_types.to_corner(UR)
        self.add(blood_types)


        donation = self.get_blood_donation()
        donation.to_corner(UR)
        self.add(donation)









from unittest import skip
from manim import *
from BinomHelpers import *


class LastVideo(Scene):
    def construct(self):
        rect = ScreenRectangle(height = 6, stroke_width = 3, stroke_color = YELLOW_A)
        rect.to_edge(DOWN)

        title = Tex("Letztes ", "Video", color = YELLOW_A)
        title.scale(1.75)
        title.next_to(rect, UP)

        self.play(
            FadeIn(title, run_time = 3),
            Create(rect, run_time = 3)
        )
        self.wait(3)

        title2 = Tex("Video", " heute", color = BLUE_A)
        title2.scale(1.75)
        title2.next_to(rect, UP)

        self.play(
            Transform(title[0], title2[1], path_arc = -TAU/2),
            Transform(title[1], title2[0]),
            FadeToColor(rect, BLUE_A), 
            run_time = 2
        )
        self.wait(3)


class FirstExplanation(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height= 2,
            zoomed_display_width= 5,
            zoomed_display_corner = UP + RIGHT,
            image_frame_stroke_width = 5,
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
        x_p_pos = 0.872*LEFT                     # x position p = 0.4
        x_n_pos = 4.47*LEFT                     # x position n = 100 left side
        x_k_pos = 4.275*LEFT

        self.pos_p = x_p_pos + 3.15*UP
        self.pos_k = x_k_pos + 3.15*UP

        self.nk_bound_pos = 4.37*LEFT + 2.93*DOWN       # position of bottom boundary line point between n & k

        self.n25_top = 4.56*LEFT + 0.18*DOWN
        self.n25_bottom = 4.56*LEFT + 2.675*DOWN

        self.k10_top = 4.37*LEFT + 1.275*DOWN
        self.k10_bottom = 4.37*LEFT + 1.38*DOWN

        self.pos_k_0 = x_k_pos + 0.245*DOWN
        self.pos_k_10 = x_k_pos + 1.328*DOWN
        self.pos_k_22 = x_k_pos + 2.625*DOWN

        self.p_pos_10 = x_p_pos + 1.328*DOWN


        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_10_20_25")
        table.set(height = config["frame_height"] - 0.5)
        table.shift(2.25*LEFT)


        # TRY AND ERROR FOR POSITIONS ########################

        # self.add(table)

        # ref_dots = VGroup()
        # for pos in [self.k10_top, self.k10_bottom]:# self.positions:
        #     dot = Dot(point = pos, radius = 0.02, color = RED, fill_opacity = 0.4)
        #     ref_dots.add(dot)
        # axes = NumberPlane()
        # self.add(axes)
        # self.add(ref_dots)
        # self.wait()


        # self.zoomed_camera.frame.move_to(self.pos_k_10)
        # self.activate_zooming(animate=True)
        # self.wait()

        # #####################################################

        self.open_book()
        self.bernoulli_parameters()
        self.orientation_according_to_prob()
        self.find_block_and_row_according_to_n_k()
        self.highlight_blocks()


    def open_book(self):
        tw = ImageMobject(IMG_DIR + "open-tafelwerk-tables")
        tw.set(height = config["frame_height"] - 1)
        self.play(FadeIn(tw), run_time = 2)
        self.wait()

        header = Tex("Überschrift")\
            .scale(1.5)\
            .to_edge(UP)

        headlines = VGroup(*[Tex(tex) for tex in ["Summierte Binomialverteilung", "Kumulierte Binomialverteilung", "Kumulierte Wahrscheinlichkeitsverteilung"]])
        for headline in headlines:
            headline.scale(1.5)\
                .next_to(header, DOWN)\
                .set_color(RED)

        self.play(FadeIn(header, shift = DOWN))
        self.play(Write(headlines[0]), run_time = 0.8)
        self.wait()
        for k in range(2):
            self.play(Transform(headlines[0], headlines[k + 1]))
            self.wait()


        self.play(
            AnimationGroup(
                FadeOut(header), 
                FadeOut(headlines[0]),
                FadeOut(tw), 
                FadeIn(self.table, scale = 0.2, target_position=1*RIGHT + 0.25*DOWN), 
                lag_ratio = 0.15
            ), 
            run_time = 3
        )
        self.wait()

    def bernoulli_parameters(self):
        n, p, k = self.get_npk_group()
        for mob in n, p, k:
            mob.save_state()
            mob.scale(1.5)
            mob.next_to(self.zoomed_display, DOWN)

            if mob is k:
                at_most = Tex("höchstens\\\\", "10 ", "Erfolge")\
                    .set_color_by_tex_to_color_map({"höchstens": PINK, "10": C_COLOR})\
                    .move_to(mob, aligned_edge = UP)\
                    .shift(2*LEFT)

                self.play(Write(at_most))
                uline = Line(color = BLUE, stroke_width = 2)\
                    .set(width = at_most.width)\
                    .next_to(at_most, DOWN, buff = 0.1)
                self.play(Create(uline))
                uline.reverse_direction()
                self.play(Uncreate(uline))
                self.wait()

                prob = MathTex("P", "\\big(", "X", "\\leq", "10", "\\big)")\
                    .scale(1.5)\
                    .set_color_by_tex_to_color_map({"\\leq": PINK, "10": C_COLOR})\
                    .next_to(self.zoomed_display.get_bottom(), UP)
                self.play(Write(prob))


                mob.next_to(at_most, RIGHT, buff = 1)

            self.play(FadeIn(mob, shift = 2*LEFT))
            self.wait()

            self.play(Restore(mob), run_time = 2.5)
            self.wait()

        self.trail_num = n
        self.succ_prob = p
        self.succ_nums = k
        self.prob_tex = prob
        self.at_most_text = at_most

    def orientation_according_to_prob(self):
        vert, hori = self.get_npk_block()
        vert2, hori2 = self.get_opposite_npk_block()

        # p < 0.5
        self.play(
            AnimationGroup(
                GrowFromPoint(vert, vert.get_corner(UL)), 
                GrowFromPoint(hori, hori.get_corner(UL)), 
                lag_ratio = 0.15
            ), 
            run_time = 3
        )
        self.wait()


        l05 = VGroup(vert, hori)
        l05.generate_target()
        l05.target.scale_to_fit_height(1).move_to(2*RIGHT + 2.25*UP)

        l05_tex = MathTex("p", "<", "0.5", color = vert.get_color())
        l05_tex.next_to(l05.target, RIGHT).shift(0.5*LEFT)

        self.play(
            MoveToTarget(l05),
            Write(l05_tex, rate_func = squish_rate_func(smooth, 0.6, 1)),
            self.prob_tex.animate.shift(2.75*DOWN),
            self.at_most_text.animate.next_to(self.zoomed_display, DOWN),
            run_time = 3
        )
        self.wait()

        # p > 0.5
        g05_tex = MathTex("p", ">", "0.5", color = vert2.get_color())
        g05_tex.next_to(l05_tex, RIGHT, buff = 0.5)

        g05 = VGroup(vert2, hori2)
        g05.generate_target()
        g05.target.scale_to_fit_height(1).next_to(g05_tex, RIGHT).shift(0.5*LEFT)

        self.play(Write(g05_tex))
        self.wait(0.5)

        self.play(
            AnimationGroup(
                GrowFromPoint(vert2, vert2.get_corner(DR)), 
                GrowFromPoint(hori2, hori2.get_corner(DR)), 
                lag_ratio = 0.15
            ),
            run_time = 3
        )
        self.wait()
        self.play(MoveToTarget(g05), run_time = 3)
        self.wait()

    def find_block_and_row_according_to_n_k(self):
        # find block for n = 25
        brace = Brace(Line(self.n25_top, self.n25_bottom), LEFT, buff = 0.25, color = GREY)
        self.play(
            Circumscribe(self.trail_num, color = BLUE, run_time = 2),
            Create(brace, run_time = 2)
        )
        self.play(
            self.trail_num.animate.next_to(brace, LEFT), 
            run_time = 3
        )
        self.wait()


        rect_up, rect_down = self.get_n25_blocks()
        self.play(
            LaggedStart(
                GrowFromEdge(rect_up, DOWN), 
                GrowFromEdge(rect_down, UP), 
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.wait()

        # show different values for k 0...22...10
        self.zoomed_camera.frame.move_to(self.pos_k_0)
        self.activate_zooming(animate=True)
        self.wait()

        self.play(self.zoomed_camera.frame.animate.move_to(self.pos_k_22), run_time = 4)
        self.wait(2)
        self.play(self.zoomed_camera.frame.animate.move_to(self.pos_k_10), run_time = 4)
        self.wait(2)

        # find row for k = 10
        row_up, row_down = self.get_k10_row()

        self.play(
            Transform(rect_up, row_up),
            Transform(rect_down, row_down), 
            run_time = 2
        )
        self.wait()

        self.rect_up, self.rect_down = rect_up, rect_down

    def highlight_blocks(self):
        rect_ul, rect_ur, rect_dl, rect_dr = self.get_highlight_blocks(self.p_pos_10)

        self.play(Circumscribe(self.succ_prob, color = BLUE, run_time = 3))
        self.wait(0.5)

        self.play(
            LaggedStart(
                ReplacementTransform(self.rect_up, rect_ul), 
                ReplacementTransform(self.rect_down, rect_dl), 
                GrowFromEdge(rect_ur, DL), 
                GrowFromEdge(rect_dr, UL), 
                lag_ratio = 0.1
            ),
            self.zoomed_camera.frame.animate.move_to(self.pos_p),
            run_time = 3
        )
        self.wait()

        self.play(self.zoomed_camera.frame.animate.move_to(self.p_pos_10), run_time = 5)
        self.wait()

        result = MathTex("=", str(get_binom_cdf_result(25, 0.4, 10)))
        result.scale(1.4)
        result.next_to(self.prob_tex, DOWN, buff = 0.5)

        self.play(Write(result))
        self.play(Circumscribe(result, color = YELLOW_D, run_time = 3))
        self.wait(3)


    # functions 
    def get_npk_group(self):
        n = MathTex("n", "=", "25")
        p = MathTex("p", "=", "0.4")
        p[-1].set_color(YELLOW_D)
        k = MathTex("k", "=", "10")
        k[1].set_color(PINK)
        k[2].set_color(C_COLOR)

        group = VGroup(n, p, k)
        group.arrange(DOWN, aligned_edge = LEFT)
        group.next_to(self.table, LEFT, buff = 0.5, aligned_edge=UP)

        return n, p, k

    def get_npk_block(self):
        rect_vert = Rectangle(width = 0.37, height = 6.22)
        rect_vert.next_to(self.nk_bound_pos, UP, buff = 0)

        rect_hori = Rectangle(width = 3.88, height = 0.25)
        rect_hori.next_to(rect_vert, RIGHT, buff = 0, aligned_edge=UP)

        for rect in rect_vert, rect_hori:
            rect.set_stroke(width = 0)
            rect.set_fill(BLUE, 0.5)

        return rect_vert, rect_hori

    def get_opposite_npk_block(self):
        vert, hori = self.get_npk_block()

        vert2 = vert.copy()\
            .set_fill(color = ORANGE)\
            .next_to(hori, RIGHT, buff = 0, aligned_edge = UP)
        hori2 = hori.copy()\
            .set_fill(color = ORANGE)\
            .next_to(vert, RIGHT, buff = 0, aligned_edge = DOWN)

        return vert2, hori2

    def get_n25_blocks(self):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}
        rect_up = Rectangle(width = self.table.width, height = abs(top - self.n25_top[1]), **rect_kwargs)
        rect_up.next_to(self.table.get_top(), DOWN, buff = 0)

        rect_down = Rectangle(width = self.table.width, height = abs(bottom - self.n25_bottom[1]), **rect_kwargs)
        rect_down.next_to(self.table.get_bottom(), UP, buff = 0)

        return rect_up, rect_down

    def get_k10_row(self):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}
        rect_up = Rectangle(width = self.table.width, height = abs(top - self.k10_top[1]), **rect_kwargs)
        rect_up.next_to(self.table.get_top(), DOWN, buff = 0)

        rect_down = Rectangle(width = self.table.width, height = abs(bottom - self.k10_bottom[1]), **rect_kwargs)
        rect_down.next_to(self.table.get_bottom(), UP, buff = 0)

        return rect_up, rect_down

    def get_highlight_blocks(self, pos):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]
        left = self.table.get_left()[0]
        right = self.table.get_right()[0]

        width, height = 0.375, self.k10_top[1] - self.k10_bottom[1]

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}

        rect_ul = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ul.next_to(self.table.get_corner(UL), DR, buff = 0)

        rect_ur = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ur.next_to(self.table.get_corner(UR), DL, buff = 0)

        rect_dl = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dl.next_to(self.table.get_corner(DL), UR, buff = 0)

        rect_dr = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dr.next_to(self.table.get_corner(DR), UL, buff = 0)

        return rect_ul, rect_ur, rect_dl, rect_dr


class WheelOfFortune(HistoScene):
    def construct(self):
        self.n, self.p = 10, 1/3

        wheel = self.get_wheel()
        wheel.to_edge(UP)
        wheel.save_state()

        title = self.get_title()
        title.to_corner(UL)

        c = Tex(CMARK_TEX, color = C_COLOR, font_size = 72, tex_template = myTemplate)
        x = Tex(XMARK_TEX, color = X_COLOR, font_size = 72, tex_template = myTemplate)
        cx = VGroup(c,x)\
            .arrange(RIGHT, buff = 2)\
            .to_corner(UR)\
            .shift(0.5*LEFT)


        numbers = VGroup()
        lines = VGroup()
        for k in range(25):
            line = Line(color = GREY).set_length(0.75)

            num = MathTex(str(k + 1))
            num.scale(0.65)
            num.next_to(line, DOWN, buff = 0.1)
            numbers.add(num)

            line.num = num
            lines.add(line)

        lines.arrange_in_grid(rows = 3, cols = 10, buff = 0.5)
        lines[10:20].shift(DOWN)
        lines[20:].shift(2*DOWN)
        lines.to_edge(DOWN).shift(0.25*UP)

        for line, number in zip(lines, numbers):
            number.next_to(line, DOWN)


        # genearte succ and fail
        wheel.arrow.rotate(-36*DEGREES)
        succ = wheel.copy()
        succ.scale_to_fit_width(lines[0].width + 0.5).next_to(c, DOWN)

        wheel.arrow.rotate(-200*DEGREES)
        fail = wheel.copy()
        fail.scale_to_fit_width(lines[0].width + 0.5).next_to(x, DOWN)

        # counter
        count_tex = Tex("\\#", CMARK_TEX, ":", color = C_COLOR, tex_template = myTemplate)
        count_tex.scale(1.4)
        count_tex.next_to(title, DOWN, buff = 0.5)

        counter = 0
        count_dec = always_redraw(
            lambda: Integer()\
                .scale(1.4)\
                .set_value(counter)\
                .next_to(count_tex, RIGHT)
        )


        self.play(
            AnimationGroup(
                Write(title), 
                FadeIn(wheel, shift = 2*UP),
                DrawBorderThenFill(cx, lag_ratio = 0.3),
                FadeIn(succ),
                FadeIn(fail),
                FadeIn(count_tex),
                FadeIn(count_dec, shift = UP),
                Create(lines, lag_ratio = 0.2),
                FadeIn(numbers, lag_ratio = 0.2),
                lag_ratio = 0.1
            ),
            run_time = 3
        )


        marks = VGroup()
        for k in range(len(lines)):
            random_angle = random.uniform(720, 1080)

            self.play(Rotate(wheel.arrow, angle = random_angle*DEGREES, about_point = wheel.get_center(), rate_func = slow_into))
            if -54*DEGREES < wheel.arrow.get_angle() < TAU/4:
                mark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
                counter += 1
            else:
                mark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
            mark.move_to(lines[k].num)
            marks.add(mark)


            outcome = wheel.copy()
            outcome.generate_target()
            outcome.target.scale_to_fit_width(lines[k].width - 0.1).next_to(lines[k], UP, buff = 0.1)
            self.play(
                Transform(numbers[k], mark), 
                MoveToTarget(outcome)
            )

        self.wait(3)


    # functions 
    def get_wheel(self):
        succ_sector = Sector(outer_radius = 1.25, angle = 144*DEGREES, start_angle = -54*DEGREES)\
            .set_fill(color = WHITE, opacity = 0.5)\
            .set_stroke(width = 1)
        fail_sector = Sector(outer_radius = 1.25, angle = 216*DEGREES, start_angle =  90*DEGREES)\
            .set_fill(opacity = 0)\
            .set_stroke(width = 1)
        radial_lines = VGroup()
        for angle in np.linspace(0, 360, 6):
            line = Line(ORIGIN, 1.25*RIGHT, stroke_width = 1)
            line.rotate((angle + 18) * DEGREES, about_point = ORIGIN)
            radial_lines.add(line)

        dot = Dot()
        arrow = Arrow(DOWN, UP, stroke_width = 8, color = YELLOW_D).move_to(dot)

        wheel = VGroup(succ_sector, fail_sector, radial_lines, arrow, dot)
        wheel.arrow = arrow
        wheel.s_sector = succ_sector
        wheel.f_sector = fail_sector

        return wheel

    def get_title(self):
        title = Tex("Glücksrad")\
            .scale(1.5)
        uline = Underline(title, color = GREY)

        return VGroup(title, uline)


class RandomDie(Scene):
    def construct(self):
        process = get_random_die()
        process.center()
        process.to_edge(UP)
        self.add(process)
        self.wait(18)


class SecondExample(ZoomedScene, HistoScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height= 2,
            zoomed_display_width= 5,
            zoomed_display_corner = UP + RIGHT,
            image_frame_stroke_width = 5,
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

        self.k8_top = 4.37*LEFT + 2.09*UP
        self.k8_bottom = 4.37*LEFT + 1.97*UP

        self.final_pos = 2.75*LEFT + 2.03*UP

        n = MathTex("n", "=", "50")
        p = MathTex("p", "=", "\\frac{1}{6}")
        k = MathTex("k", "=", "8")

        npk_group = VGroup(n, p, k)
        npk_group.arrange(DOWN, buff = 0.5)
        npk_group.to_corner(UL)
        npk_group.save_state()

        for mob in npk_group:
            mob.scale(2)
        npk_group.center()
        npk_group.arrange(RIGHT, buff = 1.5)

        ntex = Tex("Anzahl\\\\", "Wiederholungen", color = BLUE_D).next_to(n, UP)
        ptex = Tex("Erfolgswahr-\\\\", "scheinlichkeit", color = YELLOW_D).next_to(p, DOWN)
        k1tex = Tex("höchstens", color = PINK).next_to(k, UP)
        k2tex = Tex("Erfolge").next_to(k, DOWN)


        self.play(FadeIn(VGroup(ntex, ptex, k1tex, k2tex), lag_ratio = 0.1), run_time = 2)
        self.play(Write(n))
        self.wait()
        self.play(GrowFromCenter(p))
        self.wait()
        self.play(FadeIn(k, shift = 3*LEFT))
        self.wait(3)


        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_50")
        table.set(height = config["frame_height"] - 0.5)
        table.shift(2.25*LEFT)

        prob = get_binom_cdf_summands(8)[:6]
        prob.scale(1.5)
        prob.next_to(self.zoomed_display, DOWN, buff = 1)

        self.play(
            AnimationGroup(
                FadeOut(VGroup(ntex, ptex, k1tex, k2tex), lag_ratio = 0.1),
                Restore(npk_group),
                FadeIn(table),
                Write(prob),
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait()

        rect_up, rect_down = self.get_k10_row()
        self.play(Circumscribe(k, color = PINK, run_time = 2))
        self.play(
            LaggedStart(
                GrowFromEdge(rect_up, DOWN), 
                GrowFromEdge(rect_down, UP), 
            ), 
            run_time = 2
        )
        self.wait()

        rect_ul, rect_ur, rect_dl, rect_dr = self.get_highlight_blocks(self.final_pos)
        self.play(Circumscribe(p, color = YELLOW_D, run_time = 2))
        self.play(
            LaggedStart(
                ReplacementTransform(rect_up, rect_ur), 
                ReplacementTransform(rect_down, rect_dr), 
                GrowFromEdge(rect_ul, DL), 
                GrowFromEdge(rect_dl, UL), 
                lag_ratio = 0.1
            ),
            run_time = 3
        )

        self.zoomed_camera.frame.move_to(self.final_pos)
        self.activate_zooming(animate=True)
        self.wait(3)


        histo_kwargs = {
            "width": 0.8*config["frame_width"], "height": 0.3*config["frame_height"],
            "x_tick_freq": 1, "x_label_freq": 4, "y_max_value": 0.2, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": True
        }
        histo = self.get_histogram(50, 1/6, **histo_kwargs)
        histo0 = self.get_histogram(50, 1/6, zeros = True, **histo_kwargs)

        for hist in histo, histo0:
            hist.next_to(self.table, RIGHT)
            hist.to_edge(DOWN)

        self.transform_zeros_into_histo(histo, run_time = 3, **histo_kwargs)
        self.play(
            histo.bars[:9].animate.set_fill(color = PINK),
            histo.bars[9:].animate.set_fill(opacity = 0.15), 
            run_time = 3
        )
        self.wait()

        self.play(
            LaggedStart(
                *[histo.bars[x].animate(rate_func = there_and_back).shift(0.5*UP) for x in range(9)]
            ), 
            run_time = 3
        )
        self.wait()



    def get_k10_row(self):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}
        rect_up = Rectangle(width = self.table.width, height = abs(top - self.k8_top[1]), **rect_kwargs)
        rect_up.next_to(self.table.get_top(), DOWN, buff = 0)

        rect_down = Rectangle(width = self.table.width, height = abs(bottom - self.k8_bottom[1]), **rect_kwargs)
        rect_down.next_to(self.table.get_bottom(), UP, buff = 0)

        return rect_up, rect_down

    def get_highlight_blocks(self, pos):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]
        left = self.table.get_left()[0]
        right = self.table.get_right()[0]

        width, height = 0.375, self.k8_top[1] - self.k8_bottom[1]

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}

        rect_ul = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ul.next_to(self.table.get_corner(UL), DR, buff = 0)

        rect_ur = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ur.next_to(self.table.get_corner(UR), DL, buff = 0)

        rect_dl = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dl.next_to(self.table.get_corner(DL), UR, buff = 0)

        rect_dr = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dr.next_to(self.table.get_corner(DR), UL, buff = 0)

        return rect_ul, rect_ur, rect_dl, rect_dr


class ProbabilityMoreThan05(ZoomedScene, HistoScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height= 2,
            zoomed_display_width= 5,
            zoomed_display_corner = UP + RIGHT,
            image_frame_stroke_width = 5,
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
        self.n, self.p = 100, 0.8

        self.nk_bound_pos = 4.37*LEFT + 3.5*DOWN       # position of bottom boundary line point between n & k
        self.final_pos = 2.377*LEFT + 0.935*UP

        self.something_is_wrong()
        self.histo_tells_you_whats_wrong()


    def something_is_wrong(self):
        histo_kwargs = {
            "width": 0.9*config["frame_width"], "height": 0.4*config["frame_height"],
            "x_tick_freq": 1, "x_label_freq": 10, "y_max_value": 0.1, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": True
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        histo0 = self.get_histogram(self.n, self.p, zeros = True, **histo_kwargs)

        for hist in histo, histo0:
            hist.center()
            hist.to_edge(DOWN)

        n = MathTex("n", "=", "100")
        p = self.p_text = MathTex("p", "=", "0.8")
        k = MathTex("k", "=", "76")

        npk_group = VGroup(n, p, k)
        npk_group.arrange(DOWN, buff = 0.5)
        npk_group.to_corner(UL)
        npk_group.save_state()

        for mob in npk_group:
            mob.scale(1.5)
        npk_group.center()
        npk_group.arrange(DOWN, buff = 0.5, aligned_edge = LEFT)
        npk_group.next_to(histo, UP, buff = 0.5).shift(4.75*RIGHT)

        ntex = Tex("Tabelle", color = BLUE_D).next_to(n[2].get_left(), LEFT, buff = 2)
        ptex = Tex("Spalte", color = YELLOW_D).next_to(p[2].get_left(), LEFT, buff = 2)
        ktex = Tex("Zeile", color = PINK).next_to(k[2].get_left(), LEFT, buff = 2)

        for tex, obj in zip([ntex, ktex, ptex], [n,k,p]):
            self.play(
                LaggedStart(
                    FadeIn(tex, shift = RIGHT),
                    FadeIn(obj, shift = 3*LEFT)
                ),
                run_time = 1.5
            )
            self.wait(0.25)
        self.wait()


        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_100")
        table.set(height = config["frame_height"] - 0.5)
        table.shift(2.25*LEFT)


        self.play(
            AnimationGroup(
                Create(histo.axes), 
                ReplacementTransform(histo0.bars, histo.bars), 
                FadeIn(table),
                lag_ratio = 0.12
            ),
            run_time = 3
        )
        self.bring_to_front(table)
        self.wait()


        rect_vert, rect_hori = self.get_npk_block()
        rect_vert2, rect_hori2 = self.get_opposite_npk_block()

        self.play(*[FadeIn(rect) for rect in [rect_vert, rect_hori]], run_time = 2)
        self.wait()

        self.play(
            Transform(rect_vert, rect_vert2), 
            Transform(rect_hori, rect_hori2), 
            run_time = 2
        )
        self.wait()


        rect_ul, rect_ur, rect_dl, rect_dr = self.get_highlight_blocks(self.final_pos)
        prob = self.prob = MathTex("P", "\\big(", "X", "\\leq", "76", "\\big)")
        prob.scale(1.5)
        prob[3].set_color(PINK)
        prob.next_to(self.zoomed_display, DOWN)


        self.play(
            *[
                GrowFromEdge(rect, edge = rect_edge) 
                for rect, rect_edge in zip([rect_ul, rect_ur, rect_dl, rect_dr], [DR, DL, UR, UL])
            ],
            LaggedStart(
                *[FadeOut(mob) for mob in [ntex, ptex, ktex, rect_vert, rect_hori]],
                lag_ratio = 0.1
            ),
            Restore(npk_group),
            Write(prob, rate_func = squish_rate_func(smooth, 0.6, 1)),
            run_time = 2
        )
        self.wait()

        self.zoomed_camera.frame.move_to(self.final_pos)
        self.activate_zooming(animate=True)
        self.wait(3)

    def histo_tells_you_whats_wrong(self):
        histo = self.histo

        arrow_left = CurvedArrow(3*RIGHT + 2.5*UP, 2*DOWN + 3*RIGHT, angle = 150*DEGREES, color = C_COLOR)
        arrow_right = CurvedArrow(5*RIGHT + 2.5*UP, 2*DOWN + 5*RIGHT, angle =-150*DEGREES, color = X_COLOR)

        # highlight bars[51:76]
        self.play(
            LaggedStart(*[bar.animate.set_fill(opacity = 0.15) for bar in histo.bars[77:]]),
            LaggedStart(*[bar.animate.set_fill(opacity = histo.bar_style.get("fill_opacity")) for bar in histo.bars[51:77]]),
            Create(arrow_left),
            run_time = 3
        )
        self.wait()

        self.play(
            ReplacementTransform(arrow_left, arrow_right),
            *[bar.animate.set_fill(color = X_COLOR, opacity = histo.bar_style.get("fill_opacity")) for bar in histo.bars[77:]],
            run_time = 2
        )
        self.wait()


        text = Tex(
            "Werden Werte über den nicht hinterlegten, \\\\",                   # 1
            "kursiv gedruckten Eingang der Tabelle \\\\ abgelesen, also ",      # 2
            "für ",                                                             # 3
            "$p \\geq 0.5$", ",",                                               # 4 5
            " muss die ", "Differenz \\\\",                                     # 6 7
            "$1$", "$-$", "(abgelesener Wert)",                                 # 8 - 10
            " ermittelt werden.",                                               # 11
            tex_environment = "flushleft"
        )
        text.add_background_rectangle(opacity = 0.85, buff = 0.2)
        text.to_edge(LEFT, buff = 0)
        text.shift(0.5*DOWN)
        text[1:].set_color(GREY_E)
        self.play(
            FadeIn(text, target_position = 2.377*LEFT + 3*DOWN, scale = 0.1), 
            run_time = 2
        )


        self.play(FadeToColor(text[1], WHITE, lag_ratio = 0.1), rate_func = linear)
        self.play(FadeToColor(text[2], WHITE, lag_ratio = 0.1), rate_func = linear)
        self.wait(0.5)

        self.play(FadeToColor(text[3:6], WHITE, lag_ratio = 0.1), rate_func = linear)
        self.wait(0.5)
        self.play(
            FadeToColor(text[4], YELLOW_D),
            FadeToColor(self.p_text, YELLOW_D),
            Circumscribe(self.p_text, color = YELLOW_D, run_time = 2)
        )
        self.wait()

        self.play(FadeToColor(text[6:], WHITE, lag_ratio = 0.1), rate_func = linear)
        self.play(FadeToColor(text[8:11], YELLOW_D))
        self.wait(3)


        self.prob.generate_target()
        self.prob.target.next_to(text[0].get_left(), RIGHT).shift(0.65*UP)

        equals = MathTex("=")
        result_1minus = MathTex("1", "-")
        result_table = MathTex("0.8109")
        result_real = MathTex("=", str(get_binom_cdf_result(self.n, self.p, 76)))

        for mob in [equals, result_1minus, result_table, result_real]:
            mob.scale(1.5)
        calc_group = VGroup(equals, result_1minus, result_table)
        calc_group.arrange(RIGHT)
        calc_group.next_to(self.prob.target, RIGHT)

        result_real.next_to(calc_group, DOWN, buff = 1, aligned_edge = LEFT)


        self.bring_to_front(self.prob)
        self.play(
            MoveToTarget(self.prob),
            FadeOut(text[1:8]),
            FadeOut(text[-1]),
            text[8:11].animate.next_to(calc_group[1:], DOWN),
            run_time = 3
        )
        result_table.save_state()
        result_table.next_to(equals, RIGHT)
        self.play(
            Write(equals),
            FadeIn(result_table, target_position=4*RIGHT + 3*UP, scale = 0.1, run_time = 2)
        )
        self.wait()

        self.play(
            FadeIn(result_1minus, rate_func = squish_rate_func(smooth, 0.5, 1)),
            Restore(result_table),
            run_time = 2
        )
        self.wait()

        self.play(Write(result_real[0]))
        self.play(Write(result_real[1]))
        self.play(Circumscribe(result_real[1], color = PINK, time_width = 0.75, run_time = 2.5))
        self.wait(0.25)

        arrow = CurvedArrow(result_real.get_right() + 0.2*RIGHT, histo.bars[73].get_corner(UL) + 0.2*UL, color = GREEN, angle = -TAU/6)
        self.play(Create(arrow), run_time = 1.5)
        self.wait(3)


    # functions
    def get_npk_block(self):
        rect_vert = Rectangle(width = 0.37, height = 6.78)
        rect_vert.next_to(self.nk_bound_pos, UP, buff = 0)

        rect_hori = Rectangle(width = 3.87, height = 0.2)
        rect_hori.next_to(rect_vert, RIGHT, buff = 0, aligned_edge=UP)

        for rect in rect_vert, rect_hori:
            rect.set_stroke(width = 0)
            rect.set_fill(BLUE, 0.5)

        return rect_vert, rect_hori

    def get_opposite_npk_block(self):
        vert, hori = self.get_npk_block()

        vert2 = vert.copy()\
            .set_fill(color = ORANGE)\
            .next_to(hori, RIGHT, buff = 0, aligned_edge = UP)
        hori2 = hori.copy()\
            .set_fill(color = ORANGE)\
            .next_to(vert, RIGHT, buff = 0, aligned_edge = DOWN)

        return vert2, hori2

    def get_highlight_blocks(self, pos):
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

        return rect_ul, rect_ur, rect_dl, rect_dr


class ExercisesParameter(Scene):
    def construct(self):
        n_tex = MathTex("n", "=")
        p_tex = self.p_text = MathTex("p", "=")
        k_tex = MathTex("k", "=")

        group_tex = self.group_tex = VGroup(n_tex, p_tex, k_tex)
        for tex in group_tex:
            tex.scale(1.5)
        group_tex.arrange(DOWN, buff = 0.75, aligned_edge = RIGHT)
        group_tex.move_to(3*RIGHT + 2.25*DOWN)
        k_tex.shift(0.25*UP)

        n_val, p_val, k_val = ValueTracker(50), ValueTracker(0.2), ValueTracker(8)
        self.n_val, self.p_val, self.k_val = n_val, p_val, k_val
        n_dec = always_redraw(lambda: Integer(n_val.get_value(), edge_to_fix = LEFT).scale(1.5).next_to(n_tex, RIGHT, aligned_edge=DOWN))
        p_dec = always_redraw(lambda: DecimalNumber(p_val.get_value(), edge_to_fix = LEFT).scale(1.5).next_to(p_tex, RIGHT, aligned_edge=DOWN).shift(0.08*UP))
        k_dec = always_redraw(lambda: Integer(k_val.get_value(), edge_to_fix = LEFT).scale(1.5).next_to(k_tex, RIGHT, aligned_edge=DOWN))

        group_dec = VGroup(n_dec, p_dec, k_dec)

        # Exercise 01 --> n = 50, p = 0.2, k = 8
        self.play(
            LaggedStartMap(FadeIn, group_tex, shift = RIGHT, lag_ratio = 0.25),
            LaggedStartMap(FadeIn, group_dec, shift = 2*LEFT, lag_ratio = 0.25),
            run_time = 2 
        )
        self.wait(2)

        prob1 = self.get_prob_label(k=8)
        self.play(FadeIn(prob1, lag_ratio = 0.1))
        self.wait()

        result1 = self.get_prob_result().next_to(prob1, RIGHT)
        self.play(Write(result1))
        self.wait()

        # Exercise 02 --> n = 10,  p = 0.2, k = 3
        # Exercise 03 --> n = 100, p = 0.6, k = 55
        # Exercise 04 --> n = 50,  p = 0.7, k = 30
        n_list = [10, 100, 50, 20]
        p_list = [0.2, 0.6, 0.7, 0.1]
        k_list = [3, 55, 33, 5]

        for n, p, k in zip(n_list, p_list, k_list):
            prob_new = self.get_prob_label(k)
            self.play(
                LaggedStart(
                    n_val.animate.set_value(n),
                    p_val.animate.set_value(p),
                    k_val.animate.set_value(k),
                    lag_ratio = 0.3
                ),
                Transform(prob1, prob_new, rate_func = squish_rate_func(smooth, 0.6, 1)),
                FadeOut(result1, shift = RIGHT, rate_func = squish_rate_func(smooth, 0, 0.65)),
                run_time = 3
            )
            self.wait()

            result_new = self.get_prob_result().next_to(prob_new, RIGHT)
            if p > 0.5:
                reminder = Tex("$1$", "$-$", "(abgelesener Wert)", color = YELLOW_D)
                reminder.scale(0.75)
                reminder.next_to(prob_new[-1], DOWN, buff = 0.5)

                self.play(Write(result_new))
                self.play(
                    Circumscribe(VGroup(p_tex, p_dec), color = YELLOW_D, run_time = 2), 
                    FadeIn(reminder, scale = 0.1, rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 2)
                )
                self.wait(2)

                self.play(FadeOut(reminder, scale = 0.1))

            else:
                self.play(Write(result_new))
                self.wait(2)


            result1 = result_new

        self.wait(2)


    # functions
    def get_prob_label(self, k):
        prob = MathTex("P", "\\big(", "X", "\\leq", str(k), "\\big)", "=")
        prob[3].set_color(PINK)
        prob.scale(1.5)
        prob.next_to(self.group_tex, UP, buff = 0.85)
        prob.shift(0.45*LEFT)

        return prob

    def get_prob_result(self):
        result = MathTex(str(get_binom_cdf_result(n=self.n_val.get_value(), p=self.p_val.get_value(), k=self.k_val.get_value())))
        result.scale(1.5)

        return result


class ExerciseN100P060K55(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.1,
            zoomed_display_height= 2,
            zoomed_display_width= 5,
            zoomed_display_corner = UP + RIGHT,
            image_frame_stroke_width = 5,
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
        self.table_name = "table_binom_cdf_100"
        self.p_width, self.p_height = 0.375, 0.09
        self.final_pos = 0.871*LEFT + 0.978*DOWN


        self.open_table()

    def open_table(self):

        table = self.table = ImageMobject(IMG_DIR + self.table_name)
        table.set(height = config["frame_height"] - 0.5)
        table.shift(2.25*LEFT)


        self.play(FadeIn(table))
        self.wait()

        rect_ul, rect_ur, rect_dl, rect_dr = self.get_highlight_blocks(self.final_pos)
        self.play(
            *[
                GrowFromEdge(rect, edge = rect_edge) 
                for rect, rect_edge in zip([rect_ul, rect_ur, rect_dl, rect_dr], [DR, DL, UR, UL])
            ],
            run_time = 2
        )
        self.wait()

        self.zoomed_camera.frame.move_to(self.final_pos)
        self.activate_zooming(animate=True)
        self.wait(3)

    # functions 
    def get_highlight_blocks(self, pos):
        top = self.table.get_top()[1]
        bottom = self.table.get_bottom()[1]
        left = self.table.get_left()[0]
        right = self.table.get_right()[0]

        width, height = self.p_width, self.p_height

        rect_kwargs = {"stroke_width": 0, "fill_color": DARK_GREY, "fill_opacity": 0.75}

        rect_ul = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ul.next_to(self.table.get_corner(UL), DR, buff = 0)

        rect_ur = Rectangle(height = abs(top - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_ur.next_to(self.table.get_corner(UR), DL, buff = 0)

        rect_dl = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(left - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dl.next_to(self.table.get_corner(DL), UR, buff = 0)

        rect_dr = Rectangle(height = abs(bottom - pos[1]) - 1/2*height, width = abs(right - pos[0]) - 1/2*width, **rect_kwargs)
        rect_dr.next_to(self.table.get_corner(DR), UL, buff = 0)

        return rect_ul, rect_ur, rect_dl, rect_dr


class Exercise01_N50P020K8(ExerciseN100P060K55):
    def construct(self):
        self.table_name = "table_binom_cdf_50"
        self.p_width, self.p_height = 0.375, 0.12
        self.final_pos = 2.374*LEFT + 2.028*UP

        self.open_table()


class Exercise02_N10P020K3(ExerciseN100P060K55):
    def construct(self):
        self.table_name = "table_binom_cdf_10_20_25"
        self.p_width, self.p_height = 0.375, 0.107
        self.final_pos = 2.374*LEFT + 2.655*UP

        self.open_table()


class Exercise04_N50P070K30(ExerciseN100P060K55):
    def construct(self):
        self.table_name = "table_binom_cdf_50"
        self.p_width, self.p_height = 0.375, 0.12
        self.final_pos = 1.624*LEFT + 1.082*UP

        self.open_table()


class Exercise05_N20P010K5(ExerciseN100P060K55):
    def construct(self):
        self.table_name = "table_binom_cdf_10_20_25"
        self.p_width, self.p_height = 0.375, 0.107
        self.final_pos = 3.124*LEFT + 1.318*UP

        self.open_table()


class Why1Minus(Scene):
    def construct(self):
        tex1 = Tex("Die Zufallsvariable ", "$X\\sim\\mathcal{B}(n,p)$", " beschreibt wie üblich die Anzahl der Erfolge.\\\\", tex_environment= "flushleft")
        tex1.scale(0.7)
        tex1.to_corner(UL)

        tex2 = Tex("Die Zufallsvariable ", "$Y = n - X$", " beschreibt dann die Anzahl der Misserfolge.", tex_environment="flushleft")
        tex2.scale(0.7).next_to(tex1, DOWN, buff = 0.1, aligned_edge=LEFT)

        tex3 = Tex("$\\text{Wegen } E(Y) = E(n-X) = n - E(X) = n - n\\cdot p = n\\cdot(1-p) \\text{ ist }Y\\sim\\mathcal{B}(n, 1-p)$.", tex_environment="flushleft")
        tex3.scale(0.7).next_to(tex2, DOWN, aligned_edge=LEFT)

        tex4 = Tex("Für die kumulierte Wahrscheinlichkeit gilt dann:", tex_environment="flushleft")
        tex4.scale(0.7).next_to(tex3, DOWN, buff = 0.5, aligned_edge=LEFT)

        math1 = MathTex("P(X\\leq k)", "=", "P(n-X\\geq n - k)", "=", "P(Y\\geq n-k)", "=", "1", "-", "P(Y\\leq n - k - 1)")
        math1.scale(0.7).next_to(tex4, DOWN, buff = 0.5, aligned_edge=LEFT).shift(0.5*RIGHT)
        math1[6:8].set_color(YELLOW_D)

        brace1 = Brace(math1[0], DOWN, color = GREY)
        brace1_tex = Tex("höchstens\\\\", "$k$", " Erfolge").scale(0.5).next_to(brace1, DOWN, buff = 0.1)

        brace2 = Brace(math1[4], DOWN, color = GREY)
        brace2_tex = Tex("mindestens\\\\", "$n-k$", " Misserfolge").scale(0.5).next_to(brace2, DOWN, buff = 0.1)

        brace3 = Brace(math1[6:], DOWN, color = GREY)
        brace3_tex = Tex("Gegenereignis zu mindestens\\\\", "$n-k$", " Misserfolgen").scale(0.5).next_to(brace3, DOWN, buff = 0.1)


        result1 = Tex(
            "Demnach kann für eine Erfolgswahrscheinlichkeit von $p\\geq 0.5$ die kumulierte Wahrscheinlichkeit auch in der Spalte mit Erfolgswahrscheinlichkeit $1-p$ abgelesen werden. Statt in der Zeile mit $k$ Erfolgen muss dann aber in der Zeile mit $n-k-1$ Erfolgen gesucht werden.\\\\", 
            "Beide stehen aber in derselben Zeile. ", "Durch die Formulierung mit dem Gegenereignis gilt Gleichheit nur bei ", "$1-$", "abgelesener Wert.",
            tex_environment="flushleft"
        )
        result1[3].set_color(YELLOW_D)
        result1.scale(0.7).to_edge(LEFT).shift(2.25*DOWN)

        self.add(tex1, tex2, tex3, tex4)
        self.add(math1, brace1, brace1_tex, brace2, brace2_tex, brace3, brace3_tex)
        self.add(result1)


        self.play(
            LaggedStartMap(FadeIn, Group(*self.mobjects), lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait(3)


        self.play(
            LaggedStartMap(FadeOut, Group(*self.mobjects), shift = 5*RIGHT, lag_ratio = 0.1), 
            run_time = 3
        )


class Thumbnail(ProbabilityMoreThan05):
    def construct(self):

        self.n, self.p = 100, 0.8

        self.nk_bound_pos = 0.5*RIGHT +  4.37*LEFT + 3.5*DOWN       # position of bottom boundary line point between n & k
        self.final_pos = 0.5*RIGHT + 2.377*LEFT + 0.935*UP


        histo_kwargs = {
            "width": 0.9*config["frame_width"], "height": 0.4*config["frame_height"],
            "x_tick_freq": 1, "x_label_freq": 10, "y_max_value": 0.1, "y_tick_num": 2,
            "bar_colors": [RED, GREEN, BLUE, GREEN, RED], 
            "include_h_lines": False
        }
        histo = self.histo = self.get_histogram(self.n, self.p, **histo_kwargs)
        histo.center().to_edge(DOWN)
        histo.bars[:77].set_fill(color = PINK, opacity = 0.6)
        histo.bars[77:].set_fill(color = YELLOW_D, opacity = 0.6)

        n = MathTex("n", "=", "100")
        p = self.p_text = MathTex("p", "=", "0.8")
        k = MathTex("k", "=", "76")

        npk_group = VGroup(n, p, k)
        npk_group.scale(1.25)
        npk_group.arrange(DOWN, buff = 0.5)
        npk_group.to_corner(UL)


        table = self.table = ImageMobject(IMG_DIR + "table_binom_cdf_100")
        table.set(height = config["frame_height"] - 0.5)
        table.shift(1.75*LEFT)


        rect_ul, rect_ur, rect_dl, rect_dr = self.get_highlight_blocks(self.final_pos)
        prob = self.prob = MathTex("P", "\\big(", "X", "\\leq", "76", "\\big)")
        prob.scale(2)
        prob[3].set_color(PINK)
        prob.next_to(self.zoomed_display, DOWN)



        self.add(histo, npk_group, table, rect_ul, rect_ur, rect_dl, rect_dr, prob)
        self.zoomed_camera.frame.move_to(self.final_pos)
        self.activate_zooming(animate=False)


        arrow_left = CurvedArrow(prob.get_corner(DL) + 0.2*LEFT, 2*DOWN + 3*RIGHT, angle = 90*DEGREES, color = PINK)
        arrow_right = CurvedArrow(5*RIGHT + 2.5*UP, 2*DOWN + 5*RIGHT, angle =-150*DEGREES, color = YELLOW_D)

        self.add(arrow_left, arrow_right)


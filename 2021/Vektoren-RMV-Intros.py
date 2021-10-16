from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE


# Video Icon
class Intro_Addition(Scene):
    def construct(self):

        self.video_nums = 5
        self.this_video_index = 0
        self.video_path_arc = -90*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)

        self.title_episode = Text("Addition von Vektoren")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .next_to(self.video_rect.get_top(), UP)

        self.setup_scene()
        self.pop_out_this_series()
        self.show_scenes_from_episode()


    def setup_scene(self):

        series = self.series = self.get_series_filmrolls()
        # calcs = self.calcs = self.get_calc_symbols()
        addition = self.get_add_pic()
        scalar = self.get_scalar_pic()
        lin_comp = self.get_lincomb_pic()
        dot_prod = self.get_dotprod_pic()
        cross_prod = self.get_crossprod_pic()

        self.calc_pics = VGroup(addition, scalar, lin_comp, dot_prod, cross_prod)


        self.play(
            AnimationGroup(
                *[DrawBorderThenFill(episode, run_time = 3) for episode in series], lag_ratio = 0.1, 
            ),
            AnimationGroup(
                *[Create(pic, run_time = 3) for pic in self.calc_pics], lag_ratio = 0.1
            ),
            # Create(calcs, lag_ratio = 0.1, run_time = 3),
            Write(self.title_series, run_time = 1.5)
        )
        self.wait()

    def pop_out_this_series(self):
        target_point = self.target_point

        icon_and_pic = VGroup(self.series[self.this_video_index], self.calc_pics[self.this_video_index])
        icon_and_pic.save_state()

        icon_and_pic.generate_target()
        icon_and_pic.target.move_to(target_point)

        self.this_video = self.series[self.this_video_index]

        self.play(
            MoveToTarget(icon_and_pic, path_arc = self.video_path_arc),
            FadeOut(self.title_series, shift = 4*RIGHT),
            run_time = 2
        )
        self.wait()

        self.icon_and_pic = icon_and_pic

    def show_scenes_from_episode(self):
        this_video = self.this_video

        rotation_point = this_video[0:5].get_left()

        self.play(
            Rotating(this_video[0:5], radians = 30*DEGREES, about_point = rotation_point, rate_func = smooth, run_time = 1.5), 
            Create(self.video_rect, run_time = 2),
            Write(self.title_episode, run_time = 2)
        )
        self.wait()

        self.play(Rotating(this_video[0:5], radians = -30*DEGREES, about_point = rotation_point, rate_func = smooth, run_time = 0.5))
        self.play(
            ShrinkToCenter(self.video_rect), 
            FadeOut(self.title_episode, target_position = self.video_rect.get_center())
        )
        self.wait()


        self.play(
            Restore(self.icon_and_pic, path_arc = -self.video_path_arc),
            run_time = 2
        )
        self.wait()


        self.play(
            LaggedStartMap(FadeOut, self.series, shift = 2*UP, lag_ratio = 0.15), 
            LaggedStartMap(FadeOut, self.calc_pics, shift = 2*UP, lag_ratio = 0.15), 
            run_time = 3
        )
        self.wait()

    # functions 

    def get_series_filmrolls(self):
        icon = SVGMobject(file_name = "video_icon")

        series = VGroup(*[icon.copy() for x in range(self.video_nums)])
        series.arrange_submobjects(RIGHT, buff = 0.75)
        series.set(width = config["frame_width"] - MED_LARGE_BUFF)
        series.set_color(GREY)#(LIGHTER_GREY, LIGHT_GREY, GREY, DARK_GREY, DARKER_GREY)#RED_A, RED_B, RED_C, RED_D, RED_E
        series.to_edge(UP)

        return series

    def get_calc_symbols(self):
        calcs = VGroup(*[
            MathTex(*tex)\
                .move_to(icon[-1])\
                .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "r": vec_c_color, "\\bullet": GREEN, "\\times": GREEN})
            for tex, icon in zip(
                [["\\vec{a}", "+", "\\vec{b}"], ["r", "\\cdot", "\\vec{a}"], ["r", "\\cdot", "\\vec{a}", "+", "s", "\\cdot", "\\vec{b}"], ["\\vec{a}", "\\bullet", "\\vec{b}"], ["\\vec{a}", "\\times", "\\vec{b}"]], 
                self.series
            )
        ])

    def get_add_pic(self):
        vec_a_num = [1.5, 0, 0]
        vec_b_num = [0.5, 1, 0]
        vec_c_num = [a+b for a,b in zip(vec_a_num, vec_b_num)]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        vec_a2 = vec_a.copy().shift(vec_b_num[0]*RIGHT + vec_b_num[1]*UP)
        vec_b2 = vec_b.copy().shift(vec_a_num[0]*RIGHT + vec_a_num[1]*UP)

        for vec in vec_a2, vec_b2:
            vec.set_stroke(opacity = 0.4)
            vec.set_fill(opacity = 0.4)

        pic = VGroup(vec_a, vec_b, vec_a2, vec_b2, vec_c)
        pic.move_to(self.series[0][-1])
        pic.set(height = self.series[0][-1].get_height() - 0.2)

        return pic

    def get_scalar_pic(self):
        vec_a_num = [0.7, 0.2, 0]
        vec_c_num = [3*x for x in vec_a_num]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_a2 = vec_a.copy().shift(vec_a_num[0]*RIGHT + vec_a_num[1]*UP)
        vec_a3 = vec_a2.copy().shift(vec_a_num[0]*RIGHT + vec_a_num[1]*UP)

        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        for vec in vec_a, vec_a2, vec_a3:
            vec.shift(0.5*UP)

        pic = VGroup(vec_a, vec_a2, vec_a3, vec_c)
        pic.move_to(self.series[1][-1])
        pic.set(height = self.series[1][-1].get_height() - 0.2)

        return pic

    def get_lincomb_pic(self):
        scalar_a = 0.5
        scalar_b = 2/3

        vec_a_num = [1.5, 0, 0]
        vec_b_num = [0.5, 1, 0]
        vec_c_num = [scalar_a * a + scalar_b * b for a,b in zip(vec_a_num, vec_b_num)]

        vec_a2_num = [scalar_a * x for x in vec_a_num]
        vec_b2_num = [scalar_b * x for x in vec_b_num]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        vec_a2 = Arrow(ORIGIN, vec_a2_num[0]*RIGHT + vec_a2_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b2 = Arrow(ORIGIN, vec_b2_num[0]*RIGHT + vec_b2_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)

        line_a = DashedLine(vec_a2.get_end(), vec_c.get_end(), color = GREY)
        line_b = DashedLine(vec_b2.get_end(), vec_c.get_end(), color = GREY)

        for vec in vec_a, vec_b:
            vec.set_stroke(opacity = 0.4)
            vec.set_fill(opacity = 0.4)

        pic = VGroup(line_a, line_b, vec_a, vec_b, vec_a2, vec_b2, vec_c)
        pic.move_to(self.series[2][-1])
        pic.set(height = self.series[2][-1].get_height() - 0.2)

        return pic

    def get_dotprod_pic(self):
        vec_a_num = [1.5, 0, 0]
        vec_b_num = [0.8, 1, 0]
        vec_c_num = [0.8, 0, 0]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        line = DashedLine(vec_b.get_end(), vec_c.get_end(), color = GREY)

        pic = VGroup(line, vec_a, vec_b, vec_c)
        pic.move_to(self.series[3][-1])
        pic.set(height = self.series[3][-1].get_height() - 0.2)

        return pic

    def get_crossprod_pic(self):
        vec_a_num = [1.25, 0.0, 0]
        vec_b_num = [0.75, 0.5, 0]
        vec_c_num = [0.00, 1, 0]

        vec_s_num = [a+b for a,b in zip(vec_a_num, vec_b_num)]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        vec_s = Arrow(ORIGIN, vec_s_num[0]*RIGHT + vec_s_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        rect = VMobject()
        rect.set_points_as_corners([
            vec_a.get_start(), 
            vec_a.get_end(),
            vec_s.get_end(), 
            vec_b.get_end(), 
            vec_b.get_start()
        ])
        rect.set_fill(color = vec_c_color, opacity = 0.3)
        rect.set_stroke(width = 0)


        pic = VGroup(rect, vec_a, vec_b, vec_c)
        pic.move_to(self.series[4][-1])
        pic.set(height = self.series[4][-1].get_height() - 0.2)

        return pic


class Intro_Scalar(Intro_Addition):
    def construct(self):

        self.video_nums = 5
        self.this_video_index = 1
        self.video_path_arc = -120*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)

        self.title_episode = Text("Skalare Multiplikation")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .next_to(self.video_rect.get_top(), UP)

        self.setup_scene()
        self.pop_out_this_series()
        self.show_scenes_from_episode()


class Intro_Linear_Combination(Intro_Addition):
    def construct(self):

        self.video_nums = 5
        self.this_video_index = 2
        self.video_path_arc = -90*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)

        self.title_episode = Text("Linearkombinationen")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .next_to(self.video_rect.get_top(), UP)

        self.setup_scene()
        self.pop_out_this_series()
        self.show_scenes_from_episode()


class Intro_DotProduct(Intro_Addition):
    def construct(self):

        self.video_nums = 5
        self.this_video_index = 3
        self.video_path_arc = -90*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)

        self.title_episode = Text("Skalarprodukt")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .next_to(self.video_rect.get_top(), UP)

        self.setup_scene()
        self.point_at_coming_episodes()
        self.new_pop_out_this_series()
        self.show_scenes_from_episode()



    def point_at_coming_episodes(self):
        self.play(
            AnimationGroup(
                VGroup(self.series[-2], self.calc_pics[-2]).animate(rate_func = there_and_back).shift(0.75*DOWN),
                VGroup(self.series[-1], self.calc_pics[-1]).animate(rate_func = there_and_back).shift(0.75*DOWN),
                FadeOut(self.title_series, shift = 14*LEFT),
                lag_ratio = 0.1
            ), 
            run_time = 4
        )
        self.wait()

    def new_pop_out_this_series(self):
        target_point = self.target_point

        icon_and_pic = VGroup(self.series[self.this_video_index], self.calc_pics[self.this_video_index])
        icon_and_pic.save_state()

        icon_and_pic.generate_target()
        icon_and_pic.target.move_to(target_point)

        self.this_video = self.series[self.this_video_index]

        self.play(
            MoveToTarget(icon_and_pic, path_arc = self.video_path_arc),
            run_time = 4
        )
        self.wait()

        self.icon_and_pic = icon_and_pic


class Intro_CrossProduct(Intro_Addition):
    def construct(self):

        self.video_nums = 5
        self.this_video_index = 4
        self.video_path_arc = -90*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)

        self.title_episode = Text("Kreuzprodukt")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .next_to(self.video_rect.get_top(), UP)

        self.setup_scene()
        self.pop_out_this_series()
        self.show_scenes_from_episode()





class Intro_Trailer(Intro_Addition):
    def construct(self):
        self.video_nums = 5
        self.this_video_index = 1
        self.video_path_arc = -120*DEGREES
        self.target_point = 4.5*LEFT + DOWN

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.title_series = Text("Rechnen mit \nVektoren", font = "Bahnschrift")\
            .scale(2)\
            .shift(RIGHT + DOWN)\
            .set_color(GREEN_E)

        self.video_rect = ScreenRectangle(height = 4)\
            .set_color(GREY)\
            .move_to(1.5*RIGHT + 1.5*DOWN)


        self.setup_scene()
        self.arrange_vertically()
        self.go_through_episodes()
        self.pop_out_window()


    def arrange_vertically(self):
        for mob in self.series, self.calc_pics:
            mob.save_state()

        self.calc_pics.generate_target()
        self.calc_pics.target.arrange_submobjects(DOWN).to_edge(LEFT).shift(2*RIGHT)

        self.play(
            AnimationGroup(
                ApplyMethod(self.series.shift, 3*UP, lag_ratio = 0.2),
                FadeOut(self.title_series), 
                MoveToTarget(self.calc_pics),
                lag_ratio = 0.2
            ),
            run_time = 4
        )
        self.wait()


        self.epi_numbers = VGroup(*[
            MathTex(tex).next_to(pic.get_center(), LEFT, buff = 1.5)
            for tex, pic in zip(
                ["01", "02", "03", "04", "05"], 
                self.calc_pics
            )
        ])

        self.epi_titles = VGroup(*[
            Tex(tex).next_to(pic.get_center(), RIGHT, buff = 1.5)
            for tex, pic in zip(
                ["Addition", "Skalare Multiplikation", "Linearkombinationen", "Skalarprodukt", "Kreuzprodukt"], 
                self.calc_pics
            )
        ])
        self.play(
            FadeIn(self.epi_numbers, shift = RIGHT, lag_ratio = 0.15), 
            FadeIn(self.epi_titles, shift = LEFT, lag_ratio = 0.15), 
            run_time = 2
        )
        self.wait()

    def go_through_episodes(self):
        self.play(
            *[mob[1:].animate.set_color(DARK_GREY) for mob in [self.epi_numbers, self.epi_titles]]
        )
        self.wait(1.75)

        for index in range(1, len(self.calc_pics)):
            self.play(
                *[mob[index - 1].animate.set_color(DARK_GREY) for mob in [self.epi_numbers, self.epi_titles]],
                *[mob[index].animate.set_color(WHITE) for mob in [self.epi_numbers, self.epi_titles]], 
            )
            self.wait(1.75)

        self.play(*[mob[:-1].animate.set_color(WHITE) for mob in [self.epi_numbers, self.epi_titles]])
        self.wait()


        self.play(
            Restore(self.calc_pics), 
            Restore(self.series), 
            FadeOut(self.epi_numbers, shift = RIGHT), 
            FadeOut(self.epi_titles, shift = LEFT), 
            run_time = 3
        )
        self.wait()

    def pop_out_window(self):
        rect = ScreenRectangle(height = 5, stroke_width = 3)
        rect.next_to(self.series, DOWN)

        self.play(Create(rect), run_time = 2)
        self.wait()



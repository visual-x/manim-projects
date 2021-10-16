from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE



class IsSubtraktionReallyHarder(Scene):
    def construct(self):
        sum = MathTex("51", "+", "17", "=")
        diff = MathTex("51", "-", "17", "=")

        sum_value = ValueTracker(51)
        diff_value = ValueTracker(51)

        sum_dec = DecimalNumber(sum_value.get_value(), num_decimal_places=0)
        diff_dec = DecimalNumber(sum_value.get_value(), num_decimal_places=0)

        sum_tex = Tex("Addition").set_color(GREY)
        diff_tex = Tex("Subtraktion").set_color(GREY)

        for mob in (sum, diff, sum_dec, diff_dec, sum_tex, diff_tex):
            mob.scale(1.5)

        for dec, eq, corner in zip([sum_dec, diff_dec], [sum, diff], [UL, UR]):
            dec.next_to(eq, RIGHT, buff = 0.25)
            eq[1].set_color(LIGHT_BROWN)

        sum_eq = VGroup(sum, sum_dec).to_corner(UL, buff = 1).shift(0.75*DOWN)
        diff_eq = VGroup(diff, diff_dec).to_corner(UR, buff = 1).shift(0.75*DOWN)

        sum_tex.next_to(sum_eq, UP, buff = 0.5)
        diff_tex.next_to(diff_eq, UP, buff = 0.5)

        self.play(*[Write(text) for text in [sum_tex, diff_tex]])
        self.play(
            FadeIn(VGroup(sum_eq, diff_eq), shift = UP, lag_ratio = 0.2, run_time = 2)
        )
        self.wait(2)

        self.play(FocusOn(sum_dec), run_time = 1.5)


        # Updater für Decimalzahlen
        sum_dec.add_updater(lambda s: s.set_value(sum_value.get_value()))
        diff_dec.add_updater(lambda d: d.set_value(diff_value.get_value()))

        # Addition ausrechnen
        self.play(sum_value.animate.set_value(68), rate_func = linear, run_time = 2)
        self.wait()

        # Subtraktion ausrechnen
        self.play(FocusOn(diff_dec), run_time = 1.5)
        self.play(diff_value.animate.set_value(43), rate_func = linear, run_time = 2)
        self.wait()
        self.play(diff_value.animate.set_value(45), rate_func = linear, run_time = 0.5)
        self.wait()
        self.play(diff_value.animate.set_value(44), rate_func = linear, run_time = 0.5)
        self.play(Circumscribe(diff_dec, color = LIGHT_BROWN, time_with = 0.75, run_time = 2))
        self.wait()


        rect = ScreenRectangle(height = 4, color = TEAL, stroke_width = 3).move_to(2*LEFT+ 1.5*DOWN)
        self.play(Create(rect), run_time = 2)
        self.wait(0.5)


        diff_vec = diff_tex.copy()
        self.play(diff_vec.animate.shift(3*DOWN), run_time = 3)
        text_vec = Tex("von Vektoren").set_color(TEAL).set(width = diff_vec.get_width() - 1).next_to(diff_vec, DOWN, buff = 0.25)
        self.play(DrawBorderThenFill(text_vec))
        self.wait(3)


        # Ausfaden in unterscheidliche Richtungen
        self.play(
            AnimationGroup(
                FadeOut(rect, shift = 3*LEFT + 3*DOWN), 
                FadeOut(VGroup(diff_vec, text_vec), shift = 3*RIGHT + 3*DOWN), 
                FadeOut(VGroup(diff_eq, diff_tex), shift = 3*RIGHT + 3*UP), 
                FadeOut(VGroup(sum_eq, sum_tex), shift = 3*LEFT + 3*UP),
                lag_ratio = 0.2
            ),
            run_time = 2
        )
        self.wait()


class Numberline(Scene):
    def construct(self):
        num_line_c = NumberLine(x_range = [-5.5, 6, 1], unit_size = 1, include_numbers = True, include_tip = True)
        num_line_a = num_line_c.copy()
        num_line_b = num_line_c.copy()

        num_lines = VGroup(num_line_a, num_line_b, num_line_c)\
            .arrange_submobjects(DOWN, buff = 1)

        colors = self.colors = [vec_a_color, vec_b_color, vec_c_color]

        labels = VGroup(*[
            MathTex(tex).set_color(color).next_to(num_line.tip, RIGHT, buff = 0.5)
            for tex, color, num_line in zip(
                ["a", "b", "c"], colors, [*num_lines],
            )
        ])


        a_val = self.a_val = ValueTracker(4)
        b_val = self.b_val = ValueTracker(1)
        c_val = self.c_val = ValueTracker(a_val.get_value() - b_val.get_value())

        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda a: a.set_value(a_val.get_value()))\
            .set_color(colors[0])

        minus = MathTex("-")

        b_dec = DecimalNumber(b_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda b: b.set_value(b_val.get_value()))\
            .set_color(colors[1])

        equal = MathTex("=")

        c_dec = DecimalNumber(c_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda c: c.set_value(a_val.get_value() - b_val.get_value()))\
            .set_color(colors[2])

        task = self.task = VGroup(a_dec, minus, b_dec, equal, c_dec)\
            .arrange_submobjects(RIGHT, buff = 0.75)\
            .to_edge(UP)\
            .scale(1.5)


        arrows = self.arrows = VGroup(*[
            Arrow(num_line.number_to_point(0), num_line.number_to_point(value.get_value()), color = color, buff = 0)
            for num_line, value, color in zip(
                [*num_lines], [a_val, b_val, c_val], colors
            )
        ])


        self.play(
            AnimationGroup(
                FadeIn(task[:-1], shift = DOWN, lag_ratio = 0.15),
                Create(num_lines, lag_ratio = 0.25),
                FadeIn(labels, shift = LEFT, lag_ratio = 0.25),
                FadeIn(task[-1], shift = LEFT), 
                lag_ratio = 0.15
            ),
            run_time = 4
        )
        self.wait()

        self.play(
            LaggedStart(
                TransformFromCopy(a_dec, num_line_a.get_number_mobject(a_val.get_value())), 
                TransformFromCopy(b_dec, num_line_b.get_number_mobject(b_val.get_value())),
                TransformFromCopy(c_dec, num_line_c.get_number_mobject(c_val.get_value())),
                lag_ratio = 0.3
            ),
            *[GrowArrow(arrow) for arrow in arrows], 
            run_time = 4
        )
        self.wait()



        ##############################
        self.turn_addition_into_subtraktion()
        ##############################



        arrows[0].add_updater(lambda h: h.become(
            Arrow(num_line_a.number_to_point(0), num_line_a.number_to_point(a_val.get_value()), color = colors[0], buff = 0)
        ))
        arrows[1].add_updater(lambda h: h.become(
            Arrow(num_line_b.number_to_point(0), num_line_b.number_to_point(b_val.get_value()), color = colors[1], buff = 0)
        ))
        arrows[2].add_updater(lambda h: h.become(
            Arrow(num_line_c.number_to_point(0), num_line_c.number_to_point(a_val.get_value() - b_val.get_value()), color = colors[2], buff = 0)
        ))


        a_values = [4, -5]
        b_values = [1, -2]
        brackets_top = self.brackets_bot.copy()
        brackets_top.move_to(b_dec).shift(0.25*RIGHT)

        for index in range(len(a_values)):
            if b_values[index] < 0:
                direction = RIGHT
                added_anims_1 = [FadeIn(brackets_top, shift = DOWN)]
                added_anims_2 = [FadeOut(brackets_top, shift = UP)]
            else:
                direction = LEFT
                added_anims_1 = [FadeIn(self.brackets_bot, shift = DOWN)]
                added_anims_2 = [FadeOut(self.brackets_bot, shift = UP)]

            self.play(
                a_val.animate.set_value(a_values[index]), 
                b_val.animate.set_value(b_values[index]),
                *added_anims_1,
                run_time = 3
            )
            self.wait(2)

            arrow_b_copy = arrows[1].copy().clear_updaters()
            arrow_b_copy.generate_target()
            arrow_b_copy.target.rotate(TAU/2).next_to(arrows[0].get_end(), direction = direction, buff = 0)
            
            self.play(
                MoveToTarget(arrow_b_copy),
                run_time = 3
            )
            self.remove(self.arrow_addition_example)
            self.wait()
            self.play(
                FadeOut(arrow_b_copy),
                *added_anims_2
            )
            self.wait()


    def turn_addition_into_subtraktion(self):
        a_val, b_val, c_val = self.a_val, self.b_val, self.c_val
        colors = self.colors


        arrow_addition_example = self.arrows[1].copy().clear_updaters()
        self.arrow_addition_example = arrow_addition_example

        a_dec2 = DecimalNumber(a_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda a: a.set_value(a_val.get_value()))\
            .set_color(colors[0])

        plus = MathTex("+")

        b_dec2 = DecimalNumber(-b_val.get_value(), num_decimal_places=0, include_sign=True)\
            .add_updater(lambda b: b.set_value(-b_val.get_value()))\
            .set_color(colors[1])

        equal2 = MathTex("=")

        c_dec2 = DecimalNumber(c_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda c: c.set_value(a_val.get_value() - b_val.get_value()))\
            .set_color(colors[2])

        task2 = VGroup(a_dec2, plus, b_dec2, equal2, c_dec2)\
            .arrange_submobjects(RIGHT, buff = 0.75)\
            .to_edge(DOWN)\
            .scale(1.5)


        self.play(arrow_addition_example.animate.next_to(self.arrows[0], RIGHT, buff = 0), run_time = 4)
        self.wait()

        self.play(
            FadeIn(task2[:2], shift = DOWN), 
            lag_ratio = 0.25, run_time = 3
        )


        self.play(Rotating(arrow_addition_example, radians = TAU/2, about_edge = LEFT, run_time = 4))
        self.wait()

        brackets_bot = self.brackets_bot = VGroup(*[
            MathTex(tex).scale(1.5) for tex in ["(", ")"]
        ])
        brackets_bot.arrange_submobjects(RIGHT, buff = 1)
        brackets_bot.move_to(b_dec2)

        self.play(
            *[FadeIn(mob, shift = DOWN) for mob in [task2[2], brackets_bot]], 
            run_time = 2
        )
        self.play(Write(task2[3:]), run_time = 2)
        self.wait()


class AdaptToVectors(Scene):
    def construct(self):

        self.text_scale_factor = 1.2

        sub_color = MAROON
        add_color = TEAL
        anti_color = LIGHT_BROWN

        subtract = VGroup(*[
            Tex(*tex).scale(self.text_scale_factor).set_color(LIGHT_GREY)
            for tex in [["Subtraktion\\\\", "reeller Zahlen"], ["Subtraktion\\\\", "von Vektoren"]]
        ])
        subtract.arrange_submobjects(DOWN, buff = 2.5)
        subtract.to_corner(UL)
        for tex in subtract:
            tex[1].set_color(sub_color)
            tex[1].scale(0.85)

        addition = VGroup(*[
            Tex(*tex)\
                .scale(self.text_scale_factor)\
                .next_to(sub_text[0], RIGHT, buff = 2)\
                .set_color_by_tex_to_color_map({"Addition": add_color, "Gegenzahl": anti_color, "Gegenvektors": anti_color})
            for tex, sub_text in zip([["Addition ", "der ", "Gegenzahl"], ["Addition ", "des ", "Gegenvektors"]], subtract)
        ])

        calcs = VGroup(*[
            MathTex(*tex)\
                .scale(self.text_scale_factor)\
                .next_to(text, DOWN, buff = 1.25, aligned_edge = LEFT)\
                .shift(1*RIGHT)\
                .set_color_by_tex_to_color_map({"+": add_color, "-17": anti_color, "-\\vec{b}": anti_color})
            for tex, text in zip(
                [
                    ["51", "-", "17", "=", "51", "+", "(", "-17", ")"], 
                    ["\\vec{a}", "-", "\\vec{b}", "=", "\\vec{a}", "+", "(", "-\\vec{b}", ")"]
                ], 
                addition
            )
        ])

        self.subtract, self.addition, self.calcs = subtract, addition, calcs



        self.setup_scene()
        self.geometric_vs_algebraisch()


    def setup_scene(self):
        subtract, addition, calcs = self.subtract, self.addition, self.calcs

        for index in range(len(subtract)):
            self.play(Write(subtract[index]))
            self.wait(0.5)

            self.play(FadeIn(addition[index][0:2], shift = DOWN))
            self.wait(0.25)
            self.play(FadeIn(addition[index][2], shift = DOWN))
            self.wait(0.5)
            self.play(Write(calcs[index][:4]))
            self.wait(0.5)

            self.play(
                AnimationGroup(
                    TransformFromCopy(calcs[index][0], calcs[index][4], path_arc = -2),
                    TransformFromCopy(calcs[index][1], calcs[index][5]),
                    TransformFromCopy(calcs[index][2], calcs[index][6:], path_arc = +2),
                    lag_ratio = 0.1
                ), 
                run_time = 3
            )
            self.wait()

    def geometric_vs_algebraisch(self):
        subtract, addition, calcs = self.subtract, self.addition, self.calcs

        sur_rects_geo = VGroup(*[
            SurroundingRectangle(mob, color = YELLOW)
            for mob in [self.calcs[0][4:], self.calcs[1][4:]] 
        ])

        sur_rects_alg = VGroup(*[
            SurroundingRectangle(mob, color = BLUE)
            for mob in [self.calcs[0][:3], self.calcs[1][:3]] 
        ])

        text_geo = Tex("geometrisch")\
            .scale(self.text_scale_factor)\
            .set_color(GREY)\
            .next_to(sur_rects_geo[1], UP, aligned_edge = LEFT)

        text_alg = Tex("algebraisch")\
            .scale(self.text_scale_factor)\
            .set_color(GREY)\
            .next_to(sur_rects_alg[1], UP, aligned_edge = RIGHT)


        self.play(Create(sur_rects_geo, lag_ratio = 0.25), run_time = 3)
        self.wait(0.5)
        self.play(Write(text_geo))
        self.wait()


        self.play(Create(sur_rects_alg, lag_ratio = 0.25), run_time = 3)
        self.wait(0.5)
        self.play(Write(text_alg))
        self.wait(3)


class Geometric2D(VectorScene):
    def construct(self):
        self.show_sum_again()
        self.how_to_subtrakt()

    def show_sum_again(self):
        plane = self.plane = NumberPlane(
            y_range = [-4.5, 3.5, 1],
            axis_config = {"stroke_color": GREY}, background_line_style={"stroke_opacity": 0.6}
        )
        plane.add_coordinates()

        # numerical vectors
        veca_num = self.veca_num = np.array([-1,2,0])
        vecb_num = self.vecb_num = np.array([4,1,0])
        vecc_num = self.vecc_num = [a - b for a,b in zip(veca_num, vecb_num)]

        # Vektorpfeile
        arrows = self.arrows = VGroup(*[
            self.get_vector(vec_num, color = color)
            for vec_num, color in zip(
                [veca_num, vecb_num, vecc_num], 
                [vec_a_color, vec_b_color, vec_c_color]
            )
        ])


        veca_mat = Matrix([[veca_num[0]],[veca_num[1]]], left_bracket="(", right_bracket=")")
        vecb_mat = self.vecb_mat = Matrix([[vecb_num[0]],[vecb_num[1]]], left_bracket="(", right_bracket=")")
        sub_sign = self.sub_sign = MathTex("-")
        equal_sign = self.equal_sign = MathTex("=")
        vecc_mat = self.vecc_mat = Matrix([[vecc_num[0]],[vecc_num[1]]], left_bracket="(", right_bracket=")")

        mat_equation = self.mat_equation = VGroup(veca_mat, sub_sign, vecb_mat, equal_sign, vecc_mat)\
            .arrange_submobjects(RIGHT)\
            .to_edge(DOWN, buff = 0.75)


        texs_abc = self.texs_abc = VGroup(*[
            MathTex(tex)\
                .set_color(color)\
                .next_to(ref_mat.get_center(), DOWN, buff = 1.15, aligned_edge = DOWN)\
            for color, tex, ref_mat in zip(
                [vec_a_color, WHITE, vec_b_color, WHITE, vec_c_color],
                ["\\vec{a}", "-", "\\vec{b}", "=", "\\vec{c}"], 
                [*mat_equation]
            )
        ])


        bgr = Rectangle(width = config["frame_width"], height = config["frame_height"]/2 - 0.5)\
            .to_edge(DOWN, buff = 0)\
            .set_stroke(opacity = 0)\
            .set_fill(color = BLACK, opacity = 0.8)



        # Ebene, Pfeile, Adddition als Rechenaufgabe
        self.play(Create(plane), run_time = 3)
        self.play(
            LaggedStartMap(Create, VGroup(arrows[0], arrows[1]), lag_ratio = 0.15), 
            Create(bgr), 
            run_time = 3
        )

        sub_sign_copy = sub_sign.copy().rotate(90*DEGREES)
        sub_sign_copy2 = sub_sign.copy().rotate(90*DEGREES).move_to(texs_abc[1])
        self.play(
            LaggedStartMap(Create, VGroup(*mat_equation[:4], sub_sign_copy), lag_ratio = 0.15),
            LaggedStartMap(Create, VGroup(*texs_abc, sub_sign_copy2), lag_ratio = 0.15),
            run_time = 2
        )
        self.wait()

        # Vektor b ans Ende von Vektor a verschieben
        text_add = Tex("Addition: ", "Vektor ", "$\\vec{b}$ ", "ans Ende von Vektor ", "$\\vec{a}$ ", "verschieben")\
            .next_to(bgr.get_top(), DOWN, buff = 0.25)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})

        self.play(Write(text_add), run_time = 2)
        self.play(arrows[1].animate.shift(veca_num), run_time = 3)


        # Summenvektor zeichnen
        vec_sum_num = self.vecc_num = [a + b for a,b in zip(veca_num, vecb_num)]
        arrow_sum = self.get_vector(vec_sum_num, color = vec_c_color)
        self.play(GrowArrow(arrow_sum), run_time = 3)
        self.wait()

        sum_mat = Matrix([[vec_sum_num[0]],[vec_sum_num[1]]], left_bracket="(", right_bracket=")")\
            .next_to(equal_sign, RIGHT)
        self.play(Write(sum_mat), run_time = 2)
        self.wait()


        # Addition weg, Vektoren zurück
        self.play(
            arrows[1].animate.shift(-veca_num), 
            FadeOut(arrow_sum),
            run_time = 3
        )


        self.sub_sign_copy, self.sub_sign_copy2 = sub_sign_copy, sub_sign_copy2
        self.text_add = text_add
        self.sum_mat = sum_mat

    def how_to_subtrakt(self):
        arrows = self.arrows

        text_sub = Tex("Subtraktion: ", "Vektor ", "$-\\vec{b}$ ", "ans Ende von Vektor ", "$\\vec{a}$ ", "verschieben")\
            .move_to(self.text_add)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})

        self.play(FocusOn(self.sub_sign_copy))
        self.play(
            ReplacementTransform(self.text_add[0], text_sub[0]),
            *[Rotating(sign, radians = 90*DEGREES) for sign in [self.sub_sign_copy, self.sub_sign_copy2]],
            FadeOut(self.sum_mat, shift = RIGHT),
            run_time = 1.5
        )
        self.remove(self.sub_sign_copy, self.sub_sign_copy2)
        self.wait()



        self.play(
            ReplacementTransform(self.text_add[1:], text_sub[1:]),
        )
        self.wait()


        arrow_b_ori = arrows[1].copy()
        arrow_b_ori.set_opacity(0.25)
        self.add(arrow_b_ori)

        self.play(arrows[1].animate.shift(self.veca_num), run_time = 3)
        self.wait()

        gegenvektor = arrows[1].copy().flip(axis = np.array([-1,4,0]), about_point = self.plane.c2p(-1,2))
        components = VGroup(*[
            self.get_xy_lines(arrow, stroke_width = 5) for arrow in [arrows[1], gegenvektor]
        ])
        labels = VGroup(*[
            self.get_xy_labels(xy_lines) for xy_lines in components
        ])

        self.play(
            Create(components[0]),
            FadeIn(labels[0]),
            lag_ratio = 0.15, 
            run_time = 3
        )
        self.wait()

        self.play(
            arrows[1].animate.flip(axis = np.array([-1,4,0]), about_point = self.plane.c2p(-1,2)),
            ReplacementTransform(components[0], components[1]), 
            ReplacementTransform(labels[0], labels[1]), 
            run_time = 3
        )
        self.wait()

        self.play(
            Uncreate(components[1]),
            FadeOut(labels[1]),
            lag_ratio = 0.15, 
            run_time = 3
        )


        final_component = self.get_xy_lines(arrows[-1], stroke_width = 5)
        self.play(GrowArrow(arrows[-1]), run_time = 3)
        self.play(Create(final_component), lag_ratio = 0.15, run_time = 2)
        self.wait()

        self.play(FadeIn(self.mat_equation[-1], shift = LEFT), run_time = 2)
        self.wait(2)


    # functions

    def get_xy_lines(self, arrow, **kwargs):
        x_line = Line(arrow.get_start(), arrow.get_start() + (arrow.get_end()[0] - arrow.get_start()[0]) * RIGHT, color = x_color, **kwargs)
        y_line = Line(arrow.get_start() + (arrow.get_end()[0] - arrow.get_start()[0]) * RIGHT, arrow.get_end(), color = y_color, **kwargs)

        result = VGroup(x_line, y_line)

        return result

    def get_xy_labels(self, xy_lines):
        x_line, y_line = xy_lines[0], xy_lines[1]

        x_step = int(round(x_line.get_end()[0] - x_line.get_start()[0], 0))
        y_step = int(round(y_line.get_end()[1] - y_line.get_start()[1], 0))

        if x_step > 0:
            direc_x = DOWN
            direc_y = RIGHT
        else:
            direc_x = UP
            direc_y = LEFT

        x_label = MathTex(str(x_step)).next_to(x_line, direction = direc_x)
        y_label = MathTex(str(y_step)).next_to(y_line, direction = direc_y)

        labels = VGroup(x_label, y_label)

        return labels


class Geometric3D(ThreeDScene): 
    def construct(self):

        axes = self.axes = ThreeDAxes()
        axes.add_coordinates()
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)
        self.origin = axes.c2p(0,0,0)

        self.veca_num = [3,-1,2]
        self.vecb_num = [1,2,-1]
        self.vecc_num = [a - b for a,b in zip(self.veca_num, self.vecb_num)]

        self.draw_axes()
        self.draw_vectors()
        self.shift_vector_b()


    def draw_axes(self):
        labels_axes = VGroup(*[
            MathTex(label).next_to(axis, direction = direction)
            for label, axis, direction in zip(
                ["x", "y", "z"], 
                [self.axes.x_axis, self.axes.y_axis, self.axes.z_axis], 
                [RIGHT, UP, OUT]
            )
        ])

        self.add_fixed_orientation_mobjects(*labels_axes)
        self.play(
            Create(self.axes),
            Create(labels_axes, lag_ratio = 0.1),
            run_time = 2
        )

    def draw_vectors(self):
        self.cone_height = 0.5
        self.cone_radius = 0.15
        self.cone_kwargs = {"cone_height": self.cone_height, "base_radius": self.cone_radius}

        arrow_a = Arrow3D(start = self.origin, end = self.axes.coords_to_point(*self.veca_num), **self.cone_kwargs, color = vec_a_color)
        arrow_b = Arrow3D(start = self.origin, end = self.axes.coords_to_point(*self.vecb_num), **self.cone_kwargs, color = vec_b_color)
        arrow_c = Arrow3D(start = self.origin, end = self.axes.coords_to_point(*self.vecc_num), **self.cone_kwargs, color = vec_c_color)

        components_a = self.get_component_lines(arrow_a, line_class = Line, color = RED_E)
        components_b = self.get_component_lines(arrow_b, line_class = Line, color = YELLOW_E)
        components_c = self.get_component_lines(arrow_c, line_class = Line, color = BLUE_E)

        self.play(
            LaggedStartMap(
                Create, 
                VGroup(components_a, arrow_a, components_b, arrow_b), 
                lag_ratio = 0.3
            ), 
            run_time = 3
        )
        self.wait(0.5)

        self.play(LaggedStartMap(FadeOut, VGroup(components_a, components_b), lag_ratio = 0.05))
        self.wait()


        self.arrow_a, self.arrow_b, self.arrow_c = arrow_a, arrow_b, arrow_c
        self.components_c = components_c

    def shift_vector_b(self):
        arrow_bshift = Arrow3D(
            start = self.axes.c2p(*self.veca_num),
            end = self.axes.c2p(*self.veca_num) + self.axes.c2p(*self.vecb_num), 
            **self.cone_kwargs, color = vec_b_color
        )

        self.play(Transform(self.arrow_b, arrow_bshift), run_time = 3)
        self.begin_ambient_camera_rotation(rate = -0.08)
        self.wait()

        arrow_bgegen = Arrow3D(
            start = self.axes.c2p(*self.veca_num), 
            end = self.axes.c2p(*self.veca_num) - self.axes.c2p(*self.vecb_num), 
            **self.cone_kwargs, color = vec_b_color
        )

        self.play(Transform(self.arrow_b, arrow_bgegen), run_time = 3)
        self.wait()

        self.play(
            LaggedStartMap(
                Create, VGroup(self.components_c, self.arrow_c), 
                lag_ratio = 0.5
            ),
            run_time = 3
        )
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(2)


    # functions

    def get_component_lines(self, arrow3d, line_class = DashedLine, color = BLUE, **kwargs):
        axes = self.axes
        x_end = arrow3d.get_end()[0] + self.cone_height * arrow3d.get_direction()[0]
        y_end = arrow3d.get_end()[1] + self.cone_height * arrow3d.get_direction()[1]
        z_end = arrow3d.get_end()[2] + self.cone_height * arrow3d.get_direction()[2]

        component_x = line_class(
            axes.c2p(*axes.p2c([x_end, y_end,0])), 
            axes.c2p(*axes.p2c([0,y_end,0])), 
            color = color, **kwargs
        )
        component_y = line_class(
            axes.c2p(*axes.p2c([x_end, y_end,0])), 
            axes.c2p(*axes.p2c([x_end,0,0])), 
            color = color, **kwargs
        )
        component_z = line_class(
            axes.c2p(*axes.p2c([x_end, y_end,0])), 
            axes.c2p(*axes.p2c([x_end, y_end, z_end])), 
            color = color, **kwargs
        )

        result = VGroup(component_x, component_y, component_z)

        return result


class Geometric3DCalc(Scene):
    def construct(self):
        self.veca_num = [3,-1,2]
        self.vecb_num = [1,2,-1]
        self.vecc_num = [a - b for a,b in zip(self.veca_num, self.vecb_num)]

        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6, "bracket_v_buff": 0.1}

        mats = VGroup(*[
            Matrix([[vec_num[0]], [vec_num[1]], [vec_num[2]]], **self.matrix_kwargs)
            for vec_num in [self.veca_num, self.vecb_num, self.vecc_num]
        ])

        minus = MathTex("-")
        equals = MathTex("=")

        vec_eq = VGroup(mats[0], minus, mats[1], equals, mats[2])\
            .arrange_submobjects(RIGHT)\
            .to_corner(UR, buff = 0.25)


        vecs = VGroup(*[
            MathTex(tex).set_color(color = color).next_to(mat, DOWN, buff = 0.1)
            for tex, color, mat in zip(
                ["\\vec{a}", "\\vec{b}", "\\vec{c}"], 
                [vec_a_color, vec_b_color, vec_c_color], 
                mats
            )
        ])

        self.play(
            LaggedStartMap(Create, VGroup(mats[0], mats[1]), lag_ratio = 0.3), 
            LaggedStartMap(Create, VGroup(vecs[0], vecs[1]), lag_ratio = 0.3), 
            run_time = 3
        )
        self.wait(0.5)

        self.play(Write(minus), Write(equals))
        self.wait() 

        self.play(Write(mats[2]), Write(vecs[2]))
        self.wait(3)


class Analytic(Scene):
    def construct(self):
        self.prepare_for_operation()
        self.compute_operation()



    def prepare_for_operation(self):
        vec_num_a = np.array([-1,2,0])
        vec_num_b = np.array([4,1,0])
        vec_num_c_add = [a + b for a,b in zip(vec_num_a, vec_num_b)]
        vec_num_c_sub = [a - b for a,b in zip(vec_num_a, vec_num_b)]


        titles = VGroup(*[
            Tex(tex)\
                .set_color_by_gradient(GREEN, GREEN_A, BLUE_A, BLUE)\
                .set_fill(color = BLACK, opacity = 0.5)\
                .set_stroke(width = 2)\
                .scale(2)\
                .to_edge(direction)
            for tex, direction in zip(
                ["Addition von Vektoren", "Subtraktion von Vektoren"], 
                [UP, DOWN]
            )
        ])

        vector_eqs = VGroup(*[
            self.get_vector_equation(vec_num_a, vec_num_b, vec_c, add = boolean, three_dim = False)\
                .next_to(title, direction, buff = 0.5)
            for boolean, vec_c, title, direction in zip(
                [True, False],
                [vec_num_c_add, vec_num_c_sub], 
                titles, 
                [DOWN, UP]
            )
        ])
        vector_eqs[1].align_to(vector_eqs[0], LEFT)

        self.play(*[Write(title) for title in titles], run_time = 2)
        self.play(
            *[FadeIn(vector_eq[:4], shift = 0.5*direction) for vector_eq, direction in zip(vector_eqs, [UP, DOWN])], 
            run_time = 1.5
        )
        self.play(
            *[Wiggle(vector_eq[1]) for vector_eq in vector_eqs], 
            run_time = 1.5
        )
        self.wait()

        shift_num = 1.6
        *[vector_eq[4].shift(shift_num*RIGHT) for vector_eq in [*vector_eqs]],
        self.play(
            *[vector_eq[0:3].animate.shift(shift_num*LEFT) for vector_eq in [*vector_eqs]],
            *[vector_eq[3].animate.shift(shift_num*RIGHT) for vector_eq in [*vector_eqs]],
            run_time = 2
        )


        inter_equals = VGroup(*[
            MathTex("=").next_to(vector_eq[0:3], RIGHT, buff = 0.25)
            for vector_eq in vector_eqs
        ])

        inter_mats = VGroup(*[
            MobjectMatrix([[x], [y]], element_alignment_corner = DOWN, left_bracket="(", right_bracket=")")\
                .next_to(inter_equal, RIGHT, buff = 0.25)
            for x, y, inter_equal in zip(
                [MathTex(str(vec_num_a[0]), "+", str(vec_num_b[0])), MathTex(str(vec_num_a[0]), "-", str(vec_num_b[0]))], 
                [MathTex(str(vec_num_a[1]), "+", str(vec_num_b[1])), MathTex(str(vec_num_a[1]), "-", str(vec_num_b[1]))], 
                inter_equals
            )
        ])


        self.play(
            Create(VGroup(*inter_equals, *inter_mats[0][-2:], *inter_mats[1][-2:]), lag_ratio = 0.15),
            run_time = 2
        )


        self.titles, self.vector_eqs, self.inter_mats = titles, vector_eqs, inter_mats

    def compute_operation(self):
        titles, vector_eqs, inter_mats = self.titles, self.vector_eqs, self.inter_mats

        rects_xcomp = VGroup(*[
            SurroundingRectangle(vector_eqs[eq][element][0][component]).set_color(color)
            for element, component, color in zip([0,2], [0, 0], [x_color, x_color])
            for eq in [0,1]
        ])
        rects_ycomp = VGroup(*[
            SurroundingRectangle(vector_eqs[eq][element][0][component]).set_color(color)
            for element, component, color in zip([0,2], [1, 1], [y_color, y_color])
            for eq in [0,1]
        ])


        self.play(
            Create(rects_xcomp, lag_ratio = 0.15), 
            run_time = 2
        )
        self.wait()

        inter_mats[0][0][0][1].set_stroke(width = 3).set_color(YELLOW)
        inter_mats[1][0][0][1].set_stroke(width = 3).set_color(YELLOW)

        self.play(
            TransformFromCopy(vector_eqs[0][0][0][0], inter_mats[0][0][0][0]),          # x Komponente Addition
            TransformFromCopy(vector_eqs[1][0][0][0], inter_mats[1][0][0][0]),          # x Komponente Subtraktion
            TransformFromCopy(vector_eqs[0][1], inter_mats[0][0][0][1]),                # Additionszeichen
            TransformFromCopy(vector_eqs[1][1], inter_mats[1][0][0][1]),                # Subtraktionszeichen
            TransformFromCopy(vector_eqs[0][2][0][0], inter_mats[0][0][0][2]),          # y Komponente Addition
            TransformFromCopy(vector_eqs[1][2][0][0], inter_mats[1][0][0][2]),          # y Komponente Subtraktion
            run_time = 2
        )
        self.wait()

        self.play(
            Create(vector_eqs[0][-1][0][0]),        # Ergebnis x Komponente
            Create(vector_eqs[0][-1][1:]),          # Ergebnis Vektorklammern
            Create(vector_eqs[1][-1][0][0]),        # Ergebnis x Komponente
            Create(vector_eqs[1][-1][1:]),          # Ergebnis Vektorklammern
            run_time = 1.5
        )
        self.wait()



        # y-Komponenten berechnen
        self.play(ReplacementTransform(rects_xcomp, rects_ycomp), run_time = 1)
        self.wait(0.5)


        inter_mats[0][0][1][1].set_stroke(width = 3).set_color(YELLOW)
        inter_mats[1][0][1][1].set_stroke(width = 3).set_color(YELLOW)
        self.play(
            TransformFromCopy(vector_eqs[0][0][0][1], inter_mats[0][0][1][0]),          # x Komponente Addition
            TransformFromCopy(vector_eqs[1][0][0][1], inter_mats[1][0][1][0]),          # x Komponente Subtraktion
            TransformFromCopy(vector_eqs[0][1], inter_mats[0][0][1][1]),                # Additionszeichen
            TransformFromCopy(vector_eqs[1][1], inter_mats[1][0][1][1]),                # Subtraktionszeichen
            TransformFromCopy(vector_eqs[0][2][0][1], inter_mats[0][0][1][2]),          # y Komponente Addition
            TransformFromCopy(vector_eqs[1][2][0][1], inter_mats[1][0][1][2]),          # y Komponente Subtraktion
            run_time = 2
        )
        self.wait()

        self.play(
            Create(vector_eqs[0][-1][0][1]),        # Ergebnis x Komponente
            Create(vector_eqs[1][-1][0][1]),        # Ergebnis x Komponente
            run_time = 1.5
        )
        self.wait()

        self.play(FadeOut(rects_ycomp))
        self.wait()

    # functions
    def get_vector_equation(self, vec_num_a, vec_num_b, vec_num_c, add = False, three_dim = False):
        if three_dim:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]], [vec_num_a[2]]], left_bracket="(", right_bracket=")")
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]], [vec_num_b[2]]], left_bracket="(", right_bracket=")")
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]], [vec_num_c[2]]], left_bracket="(", right_bracket=")")

        else:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]]], left_bracket="(", right_bracket=")")
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]]], left_bracket="(", right_bracket=")")
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]]], left_bracket="(", right_bracket=")")

        if add:
            calc_sign = MathTex("+")
        else:
            calc_sign = MathTex("-")
        calc_sign.set_stroke(width = 3).set_color(YELLOW)
        equal_sign = MathTex("=")

        vector_equation = VGroup(vector_a, calc_sign, vector_b, equal_sign, vector_c)\
            .arrange_submobjects(RIGHT)

        return vector_equation


class AdditionVsSubtraktion(Scene):
    def construct(self):
        self.vec_a_num = [4,0,0]
        self.vec_b_num = [1,2,0]

        self.vec_p_num = [a + b for a,b in zip(self.vec_a_num, self.vec_b_num)]
        self.vec_m_num = [a - b for a,b in zip(self.vec_a_num, self.vec_b_num)]


        self.arrow_kwargs = {"buff": 0, "stroke_width": 3}


        self.setup_scene()
        self.sum_and_diff()
        self.parallelogramm()


    def setup_scene(self):
        titles = self.titles = VGroup(*[
            Tex(tex).scale(1.5).set_color(LIGHT_GREY)
            for tex, colors in zip(
                ["Addition", "Subtraktion"], 
                [[vec_a_color, vec_b_color, vec_c_color], [vec_c_color, vec_b_color, vec_a_color]]
            )
        ])
        titles.arrange_submobjects(RIGHT, buff = 3)
        titles.to_edge(UP)


        eq_add = MathTex("\\vec{a}", "+", "\\vec{b}", "=", "\\vec{c}_1}")
        eq_sub = MathTex("\\vec{a}", "-", "\\vec{b}", "=", "\\vec{c}_2}")

        for eq, title in zip([eq_add, eq_sub], titles):
            eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\vec{c}": vec_c_color})
            eq.next_to(title, DOWN)
            eq.to_edge(DOWN)


        vecs_ab = VGroup(*[self.get_vecs_ab() for _ in range(len(titles))])
        for vec_ab, title in zip(vecs_ab, titles):
            vec_ab.next_to(title, DOWN, buff = 1)


        self.play(
            Write(titles, lag_ratio = 0.15), 
            Write(VGroup(eq_add, eq_sub), lag_ratio = 0.15), 
            run_time = 2
        )
        self.play(Create(vecs_ab, lag_ratio = 0.15), run_time = 2)
        self.wait()

        self.vecs_ab = vecs_ab
        self.eq_add, self.eq_sub = eq_add, eq_sub

    def sum_and_diff(self):
        self.vecs_a_copy = VGroup(self.vecs_ab[0][0].copy(), self.vecs_ab[1][0].copy())
        self.vecs_b_copy = VGroup(self.vecs_ab[0][1].copy(), self.vecs_ab[1][1].copy())

        self.play(
            *[vec_b.animate.shift(self.vec_a_num[0]*RIGHT) for vec_b in self.vecs_b_copy], 
            run_time = 4
        )
        self.wait()


        vec_b_gegen = Arrow(
            self.vecs_ab[1][0].get_end(), self.vecs_ab[1][0].get_end() + -self.vec_b_num[0]*RIGHT - self.vec_b_num[1]*UP, 
            color = vec_b_color, **self.arrow_kwargs
        )

        self.play(
            Transform(self.vecs_b_copy[1], vec_b_gegen), 
            run_time = 3
        )
        self.wait()


        # Summen- und Differenzvektor
        self.vec_p = Arrow(self.vecs_ab[0][0].get_start(), self.vecs_b_copy[0].get_end(), color = vec_c_color, **self.arrow_kwargs)
        self.vec_m = Arrow(self.vecs_ab[1][0].get_start(), self.vecs_b_copy[1].get_end(), color = vec_c_color, **self.arrow_kwargs)

        self.play(*[GrowArrow(vec, run_time = 3) for vec in [self.vec_p, self.vec_m]])
        self.wait()

    def parallelogramm(self):
        # Vektoren zum Parallelogramm verschieben ADDITION
        self.play(self.vecs_a_copy[0].animate(run_time = 5).shift(self.vec_b_num[0]*RIGHT + self.vec_b_num[1]*UP))
        self.bring_to_front(self.vec_p)
        self.wait()

        a1 = self.eq_add[0].copy()
        b1 = self.eq_add[2].copy()

        for tex, vec, pos in zip([a1, b1], [self.vecs_ab[0][0], self.vecs_b_copy[0]], [DOWN, RIGHT]):
            tex.generate_target()
            tex.target.next_to(vec, direction = pos, buff = 0.1)

        self.play(MoveToTarget(a1), run_time = 2)
        self.play(MoveToTarget(b1), run_time = 2)


        # Vektoren zum Parallelogramm verschieben SUBTRAKTION
        self.play(VGroup(self.vecs_a_copy[1], self.vec_m, self.vecs_b_copy[1]).animate(run_time = 5).shift(self.vec_b_num[0]*RIGHT + self.vec_b_num[1]*UP))
        self.wait()

        a2 = self.eq_sub[0].copy()
        b2 = self.eq_sub[2].copy()

        for tex, vec, pos in zip([a2, b2], [self.vecs_ab[1][0], self.vecs_ab[1][1]], [DOWN, LEFT]):
            tex.generate_target()
            tex.target.next_to(vec, direction = pos, buff = 0.1)

        self.play(MoveToTarget(b2), run_time = 2)
        self.play(MoveToTarget(a2), run_time = 2)


        text_para = Tex("Parallelogrammregel")\
            .set_fill(color = BLACK)\
            .set_stroke(width = 2, color = GREY)\
            .set(width = config["frame_width"] - 3)\
            .shift(1.5*DOWN)

        self.play(Write(text_para), run_time = 3)
        self.wait(3)


    # functions 

    def get_vecs_ab(self):
        vec_a = Arrow(ORIGIN, self.vec_a_num[0]*RIGHT + self.vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, self.vec_b_num[0]*RIGHT + self.vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)

        result = VGroup(vec_a, vec_b)
        return result





class Thumbnail(AdditionVsSubtraktion):
    def construct(self):

        self.vec_a_num = [4,0,0]
        self.vec_b_num = [1,2,0]

        self.vec_p_num = [a + b for a,b in zip(self.vec_a_num, self.vec_b_num)]
        self.vec_m_num = [a - b for a,b in zip(self.vec_a_num, self.vec_b_num)]


        self.arrow_kwargs = {"buff": 0, "stroke_width": 3}

        self.setup_scene()
        self.sum_and_diff()
        self.add_title()


        title = Tex("Vektorsubtraktion")\
            .set_color_by_gradient(vec_b_color, vec_c_color, vec_a_color)\
            .set_fill(color = BLACK, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 1)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1.5)

        self.add(title)

        self.eq_add.to_edge(UP).scale(1.5)
        self.eq_sub.to_edge(UP).scale(1.5)
        self.remove(self.titles)



    def add_title(self):
        # Vektoren zum Parallelogramm verschieben ADDITION
        self.play(self.vecs_a_copy[0].animate(run_time = 5).shift(self.vec_b_num[0]*RIGHT + self.vec_b_num[1]*UP))
        self.bring_to_front(self.vec_p)
        self.wait()

        a1 = self.eq_add[0].copy()
        b1 = self.eq_add[2].copy()

        for tex, vec, pos in zip([a1, b1], [self.vecs_ab[0][0], self.vecs_b_copy[0]], [DOWN, RIGHT]):
            tex.generate_target()
            tex.target.next_to(vec, direction = pos, buff = 0.1)

        self.play(MoveToTarget(a1), run_time = 2)
        self.play(MoveToTarget(b1), run_time = 2)


        # Vektoren zum Parallelogramm verschieben SUBTRAKTION
        self.play(VGroup(self.vecs_a_copy[1], self.vec_m, self.vecs_b_copy[1]).animate(run_time = 5).shift(self.vec_b_num[0]*RIGHT + self.vec_b_num[1]*UP))
        self.wait()

        a2 = self.eq_sub[0].copy()
        b2 = self.eq_sub[2].copy()

        for tex, vec, pos in zip([a2, b2], [self.vecs_ab[1][0], self.vecs_ab[1][1]], [DOWN, LEFT]):
            tex.generate_target()
            tex.target.next_to(vec, direction = pos, buff = 0.1)

        self.play(MoveToTarget(b2), run_time = 2)
        self.play(MoveToTarget(a2), run_time = 2)






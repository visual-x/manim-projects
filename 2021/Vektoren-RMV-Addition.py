from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE


class Numberline(Scene):
    def construct(self):

        num_line_c = NumberLine(x_range = [-5.5, 6, 1], unit_size = 1, include_numbers = True, include_tip = True)
        num_line_a = num_line_c.copy()
        num_line_b = num_line_c.copy()

        num_lines = VGroup(num_line_a, num_line_b, num_line_c)\
            .arrange_submobjects(DOWN, buff = 1)

        colors = [vec_a_color, vec_b_color, vec_c_color]

        labels = VGroup(*[
            MathTex(tex).set_color(color).next_to(num_line.tip, RIGHT, buff = 0.5)
            for tex, color, num_line in zip(
                ["a", "b", "c"], colors, [*num_lines],
            )
        ])


        a_val = ValueTracker(2)
        b_val = ValueTracker(3)
        c_val = ValueTracker(a_val.get_value() + b_val.get_value())

        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda a: a.set_value(a_val.get_value()))\
            .set_color(colors[0])

        plus = MathTex("+")

        b_dec = DecimalNumber(b_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda b: b.set_value(b_val.get_value()))\
            .set_color(colors[1])

        task = VGroup(a_dec, plus, b_dec)\
            .arrange_submobjects(RIGHT, buff = 0.5)\
            .to_edge(UP)\
            .scale(1.5)

        c_dec = DecimalNumber(c_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda c: c.set_value(a_val.get_value() + b_val.get_value()))\
            .set_color(colors[2])\
            .to_edge(DOWN)\
            .scale(1.5)


        arrows = VGroup(*[
            Arrow(num_line.number_to_point(0), num_line.number_to_point(value.get_value()), color = color, buff = 0)
            for num_line, value, color in zip(
                [*num_lines], [a_val, b_val, c_val], colors
            )
        ])


        self.play(FadeIn(task, shift = DOWN, lag_ratio = 0.15), run_time = 2)
        self.wait()

        self.play(FadeIn(c_dec, shift = UP), run_time = 2)
        self.wait()

        self.play(
            Create(num_lines, lag_ratio = 0.25),
            FadeIn(labels, shift = LEFT, lag_ratio = 0.25),
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


        arrows[0].add_updater(lambda h: h.become(
            Arrow(num_line_a.number_to_point(0), num_line_a.number_to_point(a_val.get_value()), color = colors[0], buff = 0)
        ))
        arrows[1].add_updater(lambda h: h.become(
            Arrow(num_line_b.number_to_point(0), num_line_b.number_to_point(b_val.get_value()), color = colors[1], buff = 0)
        ))
        arrows[2].add_updater(lambda h: h.become(
            Arrow(num_line_c.number_to_point(0), num_line_c.number_to_point(a_val.get_value() + b_val.get_value()), color = colors[2], buff = 0)
        ))



        a_values = [2, -5,  4, -3]
        b_values = [3,  2, -3,  1]
        c_values = [a + b for a,b in zip(a_values, b_values)]
        brackets = VGroup(*[
            MathTex(tex).scale(1.5) for tex in ["(", ")"]
        ])
        brackets.arrange_submobjects(RIGHT, buff = 1)
        brackets.move_to(b_dec).shift(0.25*RIGHT)

        for index in range(len(a_values)):
            if b_values[index] < 0:
                direction = LEFT
                added_anims_1 = [FadeIn(brackets, shift = DOWN)]
                added_anims_2 = [FadeOut(brackets, shift = UP)]
            else:
                direction = RIGHT
                added_anims_1 = []
                added_anims_2 = []

            self.play(
                a_val.animate.set_value(a_values[index]), 
                b_val.animate.set_value(b_values[index]),
                *added_anims_1,
                run_time = 3
            )
            self.wait(2)

            arrow_b_copy = arrows[1].copy()
            arrow_b_copy.clear_updaters()
            
            self.play(
                arrow_b_copy.animate.next_to(arrows[0].get_end(), direction, buff = 0),
                run_time = 3
            )
            self.play(
                Circumscribe(num_line_a.get_number_mobject(c_values[index]), color = BLUE, run_time = 2), 
                Circumscribe(num_line_c.get_number_mobject(c_values[index]), color = BLUE, run_time = 2), 
            )
            self.wait(0.5)
            self.play(
                FadeOut(arrow_b_copy),
                *added_anims_2
            )
            self.wait()


class UseGhostMovements(VectorScene):
    def construct(self):
        self.first_vector()
        self.second_vector()
        self.ghost_dots_addition()
        self.result()
        self.component_addition()

    def first_vector(self):
        plane = self.plane = NumberPlane(
            axis_config = {"stroke_color": GREY}, background_line_style={"stroke_opacity": 0.6}
        )
        plane.add_coordinates()
        self.dot_radius = 0.08

        self.play(Create(plane, lag_ratio=0.5), run_time = 3)

        # Pfeile
        veca_num = self.veca_num = np.array([4,3,0])
        vecb_num = self.vecb_num = np.array([1,-2,0])
        vecc_num = self.vecc_num = [a + b for a,b in zip(veca_num, vecb_num)]

        arrows = self.arrows = VGroup(*[
            self.get_vector(vec_num, color = color)
            for vec_num, color in zip(
                [veca_num, vecb_num, vecc_num], 
                [vec_a_color, vec_b_color, vec_c_color]
            )
        ])


        # Vektoren Schreibweise
        veca_mat = Matrix([[veca_num[0]],[veca_num[1]]], left_bracket="(", right_bracket=")")
        vecb_mat = self.vecb_mat = Matrix([[vecb_num[0]],[vecb_num[1]]], left_bracket="(", right_bracket=")")
        add_sign = self.add_sign = MathTex("+")
        equal_sign = self.equal_sign = MathTex("=")
        vecc_mat = self.vecc_mat = Matrix([[vecc_num[0]],[vecc_num[1]]], left_bracket="(", right_bracket=")")

        texs_vec = self.texs_vec = VGroup(veca_mat, add_sign, vecb_mat, equal_sign, vecc_mat)\
            .arrange_submobjects(RIGHT)\
            .to_corner(UL, buff = 0.5)\
            .add_background_rectangle(buff = 0.25)


        texs_abc = self.texs_abc = VGroup(*[
            MathTex(tex)\
                .set_color(color)\
                .next_to(ref_mat.get_center(), DOWN, buff = 1.5, aligned_edge = DOWN)\
            for color, tex, ref_mat in zip(
                [vec_a_color, WHITE, vec_b_color, WHITE, vec_c_color],
                ["\\vec{a}", "+", "\\vec{b}", "=", "\\vec{c}"], 
                [*texs_vec[1:]]
            ) 
        ])
        texs_abc.add_background_rectangle()


        self.play(Create(VGroup(*texs_vec[:2]), lag_ratio = 0.25))
        self.wait()

        init_dot = self.init_dot = Dot(radius = self.dot_radius, color = vec_a_color)
        self.play(FadeIn(init_dot))

        # Pfad des Vektors aufzeigen
        x_line = DashedLine(ORIGIN, veca_num[0] * RIGHT).set_color(x_color)
        y_line = DashedLine(x_line.get_end(), arrows[0].get_end()).set_color(y_color)

        xy_lines = VGroup(x_line, y_line)

        path = VMobject()
        path.set_points_as_corners([
            x_line.get_start(), 
            x_line.get_end(),
            y_line.get_end()
        ])

        self.play(
            Create(xy_lines, lag_ratio = 1),
            MoveAlongPath(init_dot, path),
            run_time = 4
        )

        # Vektor zeichnen
        self.play(GrowArrow(arrows[0]), run_time = 2)
        self.wait()

        self.play(
            LaggedStartMap(
                FocusOn, VGroup(Dot(), init_dot), 
                lag_ratio = 0.25
            ),
            run_time = 2
        )
        self.wait()

        # init_dot verschieben
        self.play(ApplyMethod(init_dot.shift, -1*veca_num + 5*LEFT + 2*DOWN), run_time = 3)
        self.play(*[
            ApplyMethod(mob.shift, 5*LEFT + 2*DOWN, run_time = 3) 
            for mob in [arrows[0], xy_lines]
        ])
        self.play(ApplyMethod(init_dot.shift, veca_num), run_time = 3)
        self.wait()

        # Vector zurück zum Anfang
        self.play(
            LaggedStart(
                *[ApplyMethod(mob.shift, 5*RIGHT + 2*UP) for mob in [arrows[0], xy_lines]],
                ApplyMethod(init_dot.shift, RIGHT + DOWN)
            ), 
            run_time = 3
        )

        # ghost dots
        dots_veca = self.my_ghost_dots(veca_num, color = vec_a_color)

        dots_veca_halfway = dots_veca.copy().shift(veca_num / 2).set_fill(vec_a_color, 1)
        dots_veca_end = dots_veca.copy().shift(veca_num)

        self.play(
            FadeIn(dots_veca, shift = IN, scale = 0.85),
            FadeOut(xy_lines),
            run_time = 3
        )
        self.remove(init_dot)
        self.wait()

        self.play(
            Transform(dots_veca, dots_veca_end), 
            GrowArrow(arrows[0]),
            run_time = 4
        )
        self.play(FadeOut(dots_veca, shift = OUT))
        self.wait()

    def second_vector(self):
        arrows = self.arrows

        dots_vecb = self.my_ghost_dots(self.vecb_num, color = vec_b_color).set_fill(BLACK, 0)
        dots_vecb_halfway = dots_vecb.copy().shift(self.vecb_num / 2).set_fill(vec_b_color, 1)
        dots_vecb_end = dots_vecb.copy().shift(self.vecb_num)

        # Vektor b zeichnen, Vektorschreibweise notieren, Ghost Dot Movemont
        self.play(GrowArrow(arrows[1]))
        self.play(Create(self.texs_vec[3]), run_time = 2)
        self.wait()

        self.play(Transform(dots_vecb, dots_vecb_halfway, rate_func=rush_into, run_time = 2))
        self.play(Transform(dots_vecb, dots_vecb_end, rate_func=rush_from, run_time = 2))

    def ghost_dots_addition(self):
        # + und = schreiben
        self.play(FocusOn(self.texs_vec[2]))
        self.play(Create(VGroup(self.texs_vec[2], self.texs_vec[4]), lag_ratio = 0.25), run_time = 2)
        self.wait()

        # background dots
        dots_veca = self.my_ghost_dots(self.veca_num, color = vec_a_color)
        dots_vecb = self.my_ghost_dots(self.vecb_num, color = vec_b_color)

        for dots in dots_veca, dots_vecb:
            dots.set_fill(BLACK, 0)

        dots_veca_halfway = dots_veca.copy().shift(self.veca_num / 2).set_fill(vec_a_color, 0.5)
        dots_veca_end = dots_veca.copy().shift(self.veca_num)

        dots_vecb_halfway = dots_vecb.copy().shift(self.vecb_num / 2).set_fill(vec_b_color, 0.5)
        dots_vecb_end = dots_vecb.copy().shift(self.vecb_num)

        # Show Dot entlang vector a
        show_dot = Dot().set_color(vec_a_color)
        self.play(
            show_dot.animate.shift(self.veca_num/2),
            Transform(dots_veca, dots_veca_halfway),
            Create(self.texs_abc[0]),
            rate_func=rush_into, run_time = 2
        )
        self.play(
            show_dot.animate.shift(self.veca_num/2),
            Transform(dots_veca, dots_veca_end), 
            rate_func=rush_from, run_time = 2
        )
        self.play(Create(self.texs_abc[1]))

        # Show Dot entlang vector b
        show_dot2 = Dot()\
            .set_color(vec_b_color)\
            .move_to(self.veca_num + self.vecb_num/2)

        self.play(
            ReplacementTransform(show_dot, show_dot2),
            Transform(dots_vecb, dots_vecb_halfway),
            Create(self.texs_abc[2]),
            rate_func=rush_into, run_time = 2
        )
        self.play(
            show_dot2.animate.shift(self.vecb_num/2),
            Transform(dots_vecb, dots_vecb_end), 
            rate_func=rush_from, run_time = 2
        )
        self.play(Create(self.texs_abc[3:5]))
        self.wait()

    def result(self):
        arrows = self.arrows
        # resultierender Vektor 
        self.play(FocusOn(ORIGIN))
        self.play(GrowArrow(arrows[-1]), run_time = 4)
        self.play(Create(self.texs_abc[-1]))
        self.wait()

        # Vektor Komponenten
        xline = Line(ORIGIN, arrows[-1].get_end()[0] * RIGHT, color = x_color)
        yline = Line(arrows[-1].get_end()[0]*RIGHT, arrows[-1].get_end()[0]*RIGHT + arrows[-1].get_end()[1] * UP, color = y_color)

        self.play(
            AnimationGroup(
                ShowPassingFlash(xline, time_width = 0.25), 
                ShowPassingFlash(yline, time_width = 0.75),
                lag_ratio = 0.5
            ), 
            run_time = 4
        )


        self.play(Create(self.texs_vec[-1]), run_time = 2)
        self.wait()


        dots_vecb = self.my_ghost_dots(self.vecb_num, color = vec_b_color).set_fill(BLACK, 0)
        dots_vecb_halfway = dots_vecb.copy().shift(self.vecb_num / 2).set_fill(vec_b_color, 0.5)
        dots_vecb_end = dots_vecb.copy().shift(self.vecb_num)
        self.play(
            Transform(dots_vecb, dots_vecb_halfway),
            rate_func=rush_into, run_time = 2
        )
        self.play(
            Transform(dots_vecb, dots_vecb_end), 
            rate_func=rush_from, run_time = 2
        )

        # Vector b verschieben
        self.play(arrows[1].animate.shift(self.veca_num), run_time = 4)
        self.wait(2)

    def component_addition(self):

        rects_lhs = VGroup(*[
            SurroundingRectangle(entry).set_color(color)
            for entry, color in zip(
                [self.texs_vec[1][0][0], self.texs_vec[3][0][0], self.texs_vec[1][0][1], self.texs_vec[3][0][1]], 
                [x_color, x_color, y_color, y_color]
            ) 
        ])

        rects_rhs = VGroup(*[
            SurroundingRectangle(entry).set_color(color)
            for entry, color in zip(
                [self.texs_vec[5][0][0], self.texs_vec[5][0][1], ], 
                [x_color, y_color]
            ) 
        ])

        x_lines = VGroup(*[
            Line(self.arrows[index].get_start(), self.arrows[index].get_start() + vec_num[0] * RIGHT)\
                .set_color(x_color)\
                .set_stroke(width = 6)
            for index, vec_num in zip(
                [0,1,2], 
                [self.veca_num, self.vecb_num, self.vecc_num]
            )
        ])

        y_lines = VGroup(*[
            Line(x_line.get_end(), x_line.get_end() + vec_num[1]*UP)\
                .set_color(y_color)\
                .set_stroke(width = 6)
            for x_line, vec_num in zip(
                [*x_lines], 
                [self.veca_num, self.vecb_num, self.vecc_num]
            )
        ])

        self.play(
            LaggedStartMap(
                Create, 
                VGroup(*rects_lhs[:2], *x_lines[:2]), 
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.play(*[ApplyWave(x_line, amplitude = 0.1, run_time = 2) for x_line in [*x_lines[:2]]])
        self.wait()

        self.play(x_lines[1].animate.shift(3*DOWN), run_time = 3)
        self.remove(*x_lines[:2])
        self.add(x_lines[2])

        self.play(
            Create(rects_rhs[0]), 
            FadeOut(rects_lhs[:2]),
            run_time = 2
        )
        self.wait()


        self.play(
            LaggedStartMap(
                Create, 
                VGroup(*rects_lhs[2:], *y_lines[:2]), 
                lag_ratio = 0.25
            ),
            run_time = 3
        )

        self.play(
            Transform(y_lines[0], y_lines[2].copy()),
            Transform(y_lines[1], y_lines[2].copy()),
            FadeOut(rects_lhs[2:]), 
            Create(rects_rhs[1]),
            run_time = 3
        )
        self.wait()


    # functions

    def my_ghost_dots(self, vector, color):
        if isinstance(vector, Arrow):
            vector = vector.get_end() - vector.get_start()
        elif len(vector) == 2:
            vector = np.append(np.array(vector), 0.0)
        x_max = int(config["frame_x_radius"] + abs(vector[0]))
        y_max = int(config["frame_y_radius"] + abs(vector[1]))
        dots = VGroup(
            *[
                Dot(x * RIGHT + y * UP, radius = self.dot_radius)
                for x in range(-x_max, x_max)
                for y in range(-y_max, y_max)
            ]
        )
        dots.set_fill(color, opacity=1)

        return dots


class Geometric2D(VectorScene):
    def construct(self):
        # numerical vectors
        veca_num = self.veca_num = np.array([4,1,0])
        vecb_num = self.vecb_num = np.array([-1,2,0])
        vecc_num = self.vecc_num = [a + b for a,b in zip(veca_num, vecb_num)]

        self.example()

    def example(self):
        veca_num = self.veca_num
        vecb_num = self.vecb_num
        vecc_num = self.vecc_num


        plane = self.plane = NumberPlane(
            axis_config = {"stroke_color": GREY}, background_line_style={"stroke_opacity": 0.6}
        )
        plane.add_coordinates()
        self.add(plane)

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
        add_sign = self.add_sign = MathTex("+")
        equal_sign = self.equal_sign = MathTex("=")
        vecc_mat = self.vecc_mat = Matrix([[vecc_num[0]],[vecc_num[1]]], left_bracket="(", right_bracket=")")

        mat_equation = self.mat_equation = VGroup(veca_mat, add_sign, vecb_mat, equal_sign, vecc_mat)\
            .arrange_submobjects(RIGHT)\
            .to_corner(DR, buff = 0.5)\
            .add_background_rectangle(buff = 0.25)

        abc_equation = VGroup(*[
            MathTex(tex)\
                .set_color(color)\
                .next_to(ref_mat.get_center(), UP, buff = 1.5, aligned_edge = UP)\
            for color, tex, ref_mat in zip(
                [vec_a_color, WHITE, vec_b_color, WHITE, vec_c_color],
                ["\\vec{a}", "+", "\\vec{b}", "=", "\\vec{c}"], 
                [*mat_equation[1:]]
            ) 
        ])
        abc_equation.add_background_rectangle()

        # vec a + vec b = vec c und BGR hinzufügen
        self.add(abc_equation, mat_equation[0])
        self.wait()

        # Vektor a und Vektor b nacheinander schreiben und Pfeil zeichne
        self.play(
            AnimationGroup(
                Write(mat_equation[1]), 
                GrowArrow(arrows[0]),
                lag_ratio = 0.5
            ), run_time = 3
        )
        self.play(TransformFromCopy(abc_equation[2], mat_equation[2]))
        self.play(
            AnimationGroup(
                Write(mat_equation[3]), 
                GrowArrow(arrows[1]),
                lag_ratio = 0.5
            ), run_time = 3
        )
        self.wait(2)

        # Verschiebung vec b
        vecb_copy = self.vecb_copy = arrows[1].copy().set_opacity(0.25)
        veca_copy = self.veca_copy = arrows[0].copy().set_opacity(0.25)
        self.add(veca_copy, vecb_copy)
        self.play(arrows[1].animate.shift(veca_num), run_time = 4)
        self.wait()

        # Resultierenden Vektor
        self.play(GrowArrow(arrows[-1]), run_time = 3)

        xline = Line(arrows[-1].get_start(), arrows[-1].get_end()[0] * RIGHT, color = x_color, stroke_width = 6)
        yline = Line(arrows[-1].get_end()[0]*RIGHT, arrows[-1].get_end()[0]*RIGHT + arrows[-1].get_end()[1] * UP, color = y_color, stroke_width = 6)

        self.play(
            AnimationGroup(
                ShowPassingFlash(xline, time_width = 0.25), 
                ShowPassingFlash(yline, time_width = 0.75),
                lag_ratio = 0.5
            ), 
            run_time = 3
        )
        self.play(
            AnimationGroup(
                Write(mat_equation[4]),
                Write(mat_equation[-1]), 
                lag_ratio = 0.3
            ), run_time = 3
        )
        self.wait(2)


class AskHowToCompute(Scene):
    def construct(self):
        text = Tex("Wie berechnet man")\
            .shift(UP)\
            .scale(2)
        eq = MathTex("\\vec{a}", "+", "\\vec{b}")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .scale(2)\
            .next_to(text, DOWN)

        self.play(Write(text))
        self.wait(0.5)
        self.play(Write(eq))
        self.wait(3)


class Analytic(VectorScene):
    def construct(self):
        self.all_three_examples()

    def all_three_examples(self):

        vec_num_a1 = np.array([4,3,0])
        vec_num_b1 = np.array([1,-2,0])
        vec_num_c1 = [a + b for a,b in zip(vec_num_a1, vec_num_b1)]

        vec_num_a2 = np.array([-2,3,0])
        vec_num_b2 = np.array([-4,-2,0])
        vec_num_c2 = [a + b for a,b in zip(vec_num_a2, vec_num_b2)]

        vec_num_a3 = np.array([3,-2,2])
        vec_num_b3 = np.array([1,3,-1])
        vec_num_c3 = [a + b for a,b in zip(vec_num_a3, vec_num_b3)]


        vector_eq_sub_1 = self.get_vector_equation(vec_num_a1, vec_num_b1, vec_num_c1)
        vector_eq_sub_2 = self.get_vector_equation(vec_num_a2, vec_num_b2, vec_num_c2)
        vector_eq_sub_3 = self.get_vector_equation(vec_num_a3, vec_num_b3, vec_num_c3, three_dim = True)

        eqs = VGroup(*vector_eq_sub_1, *vector_eq_sub_2, *vector_eq_sub_3)\
            .arrange_in_grid(rows = 3, cols = 5, buff = 0.5)

        self.play(
            LaggedStart(
                FadeIn(vector_eq_sub_1, shift = 4*LEFT),
                FadeIn(vector_eq_sub_2, shift = 4*RIGHT),
                FadeIn(vector_eq_sub_3, shift = 2*UP),
                lag_ratio = 0.25
            ), run_time = 3
        )
        self.wait()

        rects_x_a = VGroup(*[SurroundingRectangle(vector_eq_sub_1[index][0][0], color = YELLOW) for index in [0,2,4]])
        rects_x_b = VGroup(*[SurroundingRectangle(vector_eq_sub_2[index][0][0], color = YELLOW) for index in [0,2,4]])
        rects_x_c = VGroup(*[SurroundingRectangle(vector_eq_sub_3[index][0][0], color = YELLOW) for index in [0,2,4]])

        rects_x = VGroup(*[
            VGroup(*[
                SurroundingRectangle(vector_eq_sub[index][0][0], color = YELLOW) for vector_eq_sub in [vector_eq_sub_1, vector_eq_sub_2, vector_eq_sub_3]
            ]) for index in [0,2,4]
        ])

        rects_y = VGroup(*[
            VGroup(*[
                SurroundingRectangle(vector_eq_sub[index][0][1], color = BLUE) for vector_eq_sub in [vector_eq_sub_1, vector_eq_sub_2, vector_eq_sub_3]
            ]) for index in [0,2,4]
        ])

        rects_z = VGroup(*[
            SurroundingRectangle(vector_eq_sub_3[index][0][2], color = RED) for index in [0,2,4]
        ])

        # Rechtecke x-Komponenten erste Gleichung, letzten beiden Gleichungen abdunkeln
        self.play(
            LaggedStartMap(Create, VGroup(*[rects_x[cols][0] for cols in [0,1,2]]), lag_ratio = 0.25),
            *[eq.animate.set_opacity(0.25) for eq in [vector_eq_sub_2, vector_eq_sub_3]],
            run_time = 3
        )
        self.wait()



        # Teile der Gleichungen + Rechtecke x_Komponente nach links und rechts verschieben
        shift_num = 2.1
        self.play(
            *[eq[0:3].animate.shift(shift_num*LEFT) for eq in [vector_eq_sub_1, vector_eq_sub_2, vector_eq_sub_3]],
            *[eq[3:].animate.shift(shift_num*RIGHT) for eq in [vector_eq_sub_1, vector_eq_sub_2, vector_eq_sub_3]],
            VGroup(*[rects_x[cols][0] for cols in [0,1]]).animate.shift(shift_num * LEFT),
            rects_x[2][0].animate.shift(shift_num*RIGHT),
            run_time = 3
        )


        # = und Matrix Klammer schreiben
        a1 = MathTex("4", "+", "1")
        b1 = MathTex("3", "+", "(", "-", "2", ")")
        inter_equal_1 = MathTex("=")\
            .next_to(vector_eq_sub_1[0:3], RIGHT, buff = 0.5)
        inter_mat_1 = MobjectMatrix([[a1], [b1]], element_alignment_corner = DOWN, left_bracket="(", right_bracket=")")\
            .next_to(inter_equal_1, RIGHT, buff = 0.5)


        self.play(
            Write(inter_mat_1.get_brackets()),
            Write(inter_equal_1),
        )
        self.play(
            ReplacementTransform(vector_eq_sub_1[0][0][0].copy(), inter_mat_1[0][0][0]),         # 4
            ReplacementTransform(vector_eq_sub_1[1].copy(), inter_mat_1[0][0][1]),         # +
            ReplacementTransform(vector_eq_sub_1[2][0][0].copy(), inter_mat_1[0][0][2]),         # 1
            run_time = 4
        )
        self.wait()

        for rect in rects_y[0][0], rects_y[1][0], rects_z[0][0], rects_z[1][0]:
            rect.shift(shift_num * LEFT)
        for rect in rects_y[2][0], rects_z[2][0]:
            rect.shift(shift_num * RIGHT)

        # Rechtecke x_Komponente in Rechtecke y_Komponente transformieren
        self.play(
            ReplacementTransform(
                VGroup(*[rects_x[cols][0] for cols in [0,1,2]]), 
                VGroup(*[rects_y[cols][0] for cols in [0,1,2]]),
                run_time = 2
            )
        )

        self.play(
            ReplacementTransform(vector_eq_sub_1[0][0][1].copy(), inter_mat_1[0][1][0]),         # 3
            ReplacementTransform(vector_eq_sub_1[1].copy(), inter_mat_1[0][1][1]),         # +
            ReplacementTransform(vector_eq_sub_1[2][0][1].copy(), inter_mat_1[0][1][2:]),         # -2
            run_time = 4
        )
        self.wait()





        # Rechtecke y_Komponente ausfaden, Gleichung 1 abdunkeln, Gleichungen 2 & 3 aufhellen,
        self.play(
            FadeOut(VGroup(*[rects_y[cols][0] for cols in [0,1,2]]), lag_ratio = 0.25),
            *[eq.animate.set_opacity(0.25) for eq in [vector_eq_sub_1, inter_equal_1, inter_mat_1]],
            *[eq.animate.set_opacity(1) for eq in [vector_eq_sub_2, vector_eq_sub_3]],
            run_time = 2
        )
        self.wait()


        a2 = MathTex("-2", "+", "(", "-", "4", ")")
        b2 = MathTex("3", "+", "(", "-", "2", ")")
        inter_equal_2 = MathTex("=")\
            .next_to(vector_eq_sub_2[0:3], RIGHT, buff = 0.5)
        inter_mat_2 = MobjectMatrix([[a2], [b2]], element_alignment_corner = DOWN, left_bracket="(", right_bracket=")")\
            .next_to(inter_equal_2, RIGHT, buff = 0.5)


        a3 = MathTex("3", "+", "1")
        b3 = MathTex("-2", "+", "3")
        c3 = MathTex("2", "+", "(", "-", "1", ")")
        inter_equal_3 = MathTex("=")\
            .next_to(vector_eq_sub_3[0:3], RIGHT, buff = 0.5)
        inter_mat_3 = MobjectMatrix([[a3], [b3], [c3]], element_alignment_corner = DOWN, left_bracket="(", right_bracket=")")\
            .next_to(inter_equal_3, RIGHT, buff = 0.5)


        self.play(
            LaggedStartMap(
                FadeIn, 
                VGroup(inter_equal_2, inter_mat_2.get_brackets(), inter_equal_3, inter_mat_3.get_brackets()), 
                lag_ratio = 0.25
            ),
            run_time = 2
        )


        #         rects_x[a][b]    a --> Spalte       b --> Nummer Vectorgleichung
        for rect in rects_x[0][1], rects_x[0][2], rects_x[1][1], rects_x[1][2], rects_y[0][1], rects_y[0][2], rects_y[1][1], rects_y[1][2]:
            rect.shift(shift_num*LEFT)

        for rect in rects_x[2][1], rects_x[2][2], rects_y[2][1], rects_y[2][2]:
            rect.shift(shift_num*RIGHT)


        self.play(
            Create(VGroup(*[rects_x[cols][1] for cols in [0,1,2]])), 
            Create(VGroup(*[rects_x[cols][2] for cols in [0,1,2]])),
        )
        self.wait()

        # x-Komponenten von Gleichung 2 und 3 addieren
        self.play(
            ReplacementTransform(vector_eq_sub_2[0][0][0].copy(), inter_mat_2[0][0][0]),         # -2       zweite Zeile
            ReplacementTransform(vector_eq_sub_2[1].copy(), inter_mat_2[0][0][1]),               # +
            ReplacementTransform(vector_eq_sub_2[2][0][0].copy(), inter_mat_2[0][0][2:]),        # -4
            ReplacementTransform(vector_eq_sub_3[0][0][0].copy(), inter_mat_3[0][0][0]),         # 3       dritte Zeile
            ReplacementTransform(vector_eq_sub_3[1].copy(), inter_mat_3[0][0][1]),               # +
            ReplacementTransform(vector_eq_sub_3[2][0][0].copy(), inter_mat_3[0][0][2]),         # 1
            run_time = 4
        )
        self.wait()


        # Rechtecke x_Komponente in Rechtecke y_Komponente transformieren
        self.play(
            ReplacementTransform(
                VGroup(*[rects_x[cols][1] for cols in [0,1,2]]), 
                VGroup(*[rects_y[cols][1] for cols in [0,1,2]]),
            ),
            ReplacementTransform(
                VGroup(*[rects_x[cols][2] for cols in [0,1,2]]), 
                VGroup(*[rects_y[cols][2] for cols in [0,1,2]]),
            ), 
            run_time = 2
        )
        self.wait()

        # y-Komponenten von Gleichung 2 und 3 addieren
        self.play(
            ReplacementTransform(vector_eq_sub_2[0][0][1].copy(), inter_mat_2[0][1][0]),         # 3
            ReplacementTransform(vector_eq_sub_2[1].copy(), inter_mat_2[0][1][1]),               # +
            ReplacementTransform(vector_eq_sub_2[2][0][1].copy(), inter_mat_2[0][1][2:]),        # -2
            ReplacementTransform(vector_eq_sub_3[0][0][1].copy(), inter_mat_3[0][1][0]),         # -2
            ReplacementTransform(vector_eq_sub_3[1].copy(), inter_mat_3[0][1][1]),               # +
            ReplacementTransform(vector_eq_sub_3[2][0][1].copy(), inter_mat_3[0][1][2:]),        # -3
            run_time = 4
        )
        self.wait()



        # Rechtecke y_Komponenten 2te Gleichung ausfaden, Rechtecke y_Komponente 3te Gleichung --> Rechtecke z_Komponente
        self.play(
            FadeOut(VGroup(*[rects_y[cols][1] for cols in [0,1,2]]), shift = 0.5*DOWN), 
            ReplacementTransform(
                VGroup(*[rects_y[cols][2] for cols in [0,1,2]]),
                VGroup(*[rects_z[cols] for cols in [0,1,2]]),
            ),
            run_time = 2
        )
        self.wait(2)


        self.play(
            ReplacementTransform(vector_eq_sub_3[0][0][2].copy(), inter_mat_3[0][2][0]),         # 2
            ReplacementTransform(vector_eq_sub_3[1].copy(), inter_mat_3[0][2][1]),               # +
            ReplacementTransform(vector_eq_sub_3[2][0][2].copy(), inter_mat_3[0][2][2:]),        # -1
            run_time = 4
        )
        self.wait(2)


    # functions
    def get_vector_equation(self, vec_num_a, vec_num_b, vec_num_c, three_dim = False):
        if three_dim:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]], [vec_num_a[2]]], left_bracket="(", right_bracket=")")
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]], [vec_num_b[2]]], left_bracket="(", right_bracket=")")
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]], [vec_num_c[2]]], left_bracket="(", right_bracket=")")

        else:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]]], left_bracket="(", right_bracket=")")
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]]], left_bracket="(", right_bracket=")")
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]]], left_bracket="(", right_bracket=")")

        add_sign = MathTex("+")
        equal_sign = MathTex("=")

        vector_eq_subuation = VGroup(vector_a, add_sign, vector_b, equal_sign, vector_c)\
            .arrange_submobjects(RIGHT)

        return vector_eq_subuation


class Commutativ(Geometric2D):
    def construct(self):

        # numerical vectors
        veca_num = self.veca_num = np.array([-2,3,0])
        vecb_num = self.vecb_num = np.array([-4,-2,0])
        vecc_num = self.vecc_num = [a + b for a,b in zip(veca_num, vecb_num)]

        self.example()
        self.commutativ()
        self.parallelogramm()


    def commutativ(self):
        arrows = self.arrows

        self.play(arrows[1].animate.shift(-self.veca_num), run_time = 4, rate_func = there_and_back)
        self.wait()

        self.play(arrows[0].animate.shift(self.vecb_num), run_time = 4)
        self.wait()

        # Gleichung a + b = b + a
        #                    1         2       3        4       5        6        7
        comu_eq = MathTex("\\vec{a}", "+", "\\vec{b}", "=", "\\vec{b}", "+", "\\vec{a}")\
            .move_to(3.5*RIGHT + 2 * UP)\
            .scale(1.35)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .add_background_rectangle()

        comu_text = Text("Kommutativ-Gesetz")\
            .next_to(comu_eq, UP)\
            .add_background_rectangle()

        ab = comu_eq[1:4].copy().save_state().move_to(2*LEFT + 3.5*UP)
        ba = comu_eq[5:].copy().save_state().move_to(4*LEFT + 2.5*DOWN)

        # a + b, oberer Weg
        self.play(
            FadeIn(ab, shift = DOWN), 
            self.veca_copy.animate.set_opacity(1),
            arrows[0].animate.set_opacity(0.25),
            run_time = 2 
        )
        self.play(
            LaggedStartMap(ApplyWave, VGroup(self.veca_copy, arrows[1]), amplitude = 0.15, lag_ratio = 0.5), 
            run_time = 2
        )
        self.wait()

        # b + a, unterer Weg
        self.play(
            FadeIn(ba, shift = UP), 
            self.veca_copy.animate.set_opacity(0.25),
            arrows[1].animate.set_opacity(0.25),
            self.vecb_copy.animate.set_opacity(1),
            arrows[0].animate.set_opacity(1),
            run_time = 2 
        )
        self.play(
            LaggedStartMap(ApplyWave, VGroup(self.vecb_copy, arrows[0]), amplitude = 0.15, lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait()

        # a + b = b + a erzeugen
        self.play(
            Create(comu_eq[4]),
            *[Restore(rlhs) for rlhs in [ab, ba]], 
            run_time = 3
        )
        self.play(Circumscribe(comu_eq, color=vec_c_color, time_width = 0.5, run_time = 2))
        self.wait(0.5)

        # text kommutativ-gesetz
        self.play(
            FadeIn(comu_text[0]),
            AddTextLetterByLetter(comu_text[1:]), 
        )
        self.wait(2)

        # kommutativ weg alle Vektoren aufhellen
        self.play(
            FadeOut(VGroup(comu_text, ab, comu_eq[4], ba), shift = UP, lag_ratio = 0.2), 
            self.veca_copy.animate.set_opacity(1),
            arrows[1].animate.set_opacity(1),
            run_time = 3
        )
        self.wait()

    def parallelogramm(self):

        # Parallelogramm
        plane = self.plane
        para = VMobject()
        para.set_points_as_corners([
            plane.c2p(0,0), plane.c2p(-2,3), plane.c2p(-6,1), plane.c2p(-4,-2), plane.c2p(0,0)
        ])
        para.set_fill(color = PURPLE, opacity = 0.4)
        para.set_stroke(width = 0)

        self.play(Create(para), run_time = 3)
        self.bring_to_back(para)
        self.bring_to_front(self.arrows[2])
        self.wait()


        text_para = Tex("Parallelogramm", "regel")\
            .move_to(3.5*RIGHT + 2 * UP)\
            .set_color_by_tex_to_color_map({"Parallelogramm": PURPLE})\
            .add_background_rectangle()

        self.play(
            FadeIn(text_para[0]), Write(text_para[1:]), run_time = 2
        )
        self.wait(3)


class Geometric3D(ThreeDScene):
    def construct(self):
        axes = self.axes = ThreeDAxes()
        axes.add_coordinates()
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)
        origin = axes.coords_to_point(0,0,0)

        veca_num = [3,-2,2]
        vecb_num = [1,3,-1]
        vecc_num = [a + b for a,b in zip(veca_num, vecb_num)]

        self.cone_height = 0.5
        self.cone_radius = 0.15
        cone_kwargs = {"cone_height": self.cone_height, "base_radius": self.cone_radius}
        
        arrow_a = Arrow3D(start = origin, end = axes.coords_to_point(*veca_num), **cone_kwargs, color = vec_a_color)
        arrow_b = Arrow3D(start = origin, end = axes.coords_to_point(*vecb_num), **cone_kwargs, color = vec_b_color)
        arrow_c = Arrow3D(start = origin, end = axes.coords_to_point(*vecc_num), **cone_kwargs, color = vec_c_color)


        components_a = self.get_component_lines(arrow_a, line_class = Line, color = RED_E)
        components_b = self.get_component_lines(arrow_b, line_class = Line, color = YELLOW_E)
        components_c = self.get_component_lines(arrow_c, line_class = Line, color = BLUE_E)



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
            Create(axes),
            Create(labels_axes),
            run_time = 2
        )
        self.play(
            LaggedStartMap(
                Create, VGroup(components_a, arrow_a, components_b, arrow_b), lag_ratio = 0.3
            ), 
            run_time = 3
        )
        self.wait()
        self.begin_ambient_camera_rotation(rate = 0.15)

        self.play(LaggedStartMap(FadeOut, VGroup(components_a, components_b), lag_ratio = 0.05))
        self.wait()

        arrow_bmove = Arrow3D(
            start = arrow_a.get_end() + self.cone_height * arrow_a.get_direction(), 
            end = arrow_a.get_end() + self.cone_height * arrow_a.get_direction() + axes.coords_to_point(*vecb_num), 
            **cone_kwargs,
            color = vec_b_color
        )

        self.play(Transform(arrow_b, arrow_bmove), run_time = 4)
        self.stop_ambient_camera_rotation()
        self.begin_ambient_camera_rotation(rate = -0.15)
        self.wait()

        self.play(
            LaggedStartMap(
                Create, VGroup(arrow_c, components_c), 
                lag_ratio = 0.5
            ),
            run_time = 3
        )
        self.wait(10)


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


class Geometric3D_Calc(Scene):
    def construct(self):
        vec_num_a = np.array([3,-2,2])
        vec_num_b = np.array([1,3,-1])
        vec_num_c = [a + b for a,b in zip(vec_num_a, vec_num_b)]

        vector_eq = self.get_vector_equation(vec_num_a, vec_num_b, vec_num_c, three_dim = True,  v_buff = 0.6, bracket_v_buff = 0.1, bracket_h_buff = 0.1)\
            .to_corner(UR, buff = 0.75)

        abc_eq = VGroup(*[
            MathTex(tex)\
                .set_color(color)\
            for tex, color in zip(
                ["\\vec{a}", "\\vec{b}", "\\vec{c}"], 
                [vec_a_color, vec_b_color, vec_c_color]
            )
        ])
        
        abc_eq[0].next_to(vector_eq[0], UP)
        abc_eq[1].next_to(vector_eq[2], UP)
        abc_eq[2].next_to(vector_eq[4], UP)

        self.play(
            FadeIn(abc_eq[:2], shift = DOWN, lag_ratio = 0.25), 
            Write(vector_eq[:4]), 
            run_time = 3
        )
        self.wait()


        self.play(FadeIn(abc_eq[2], shift = DOWN), run_time = 2)
        self.wait(0.5)
        self.play(Write(vector_eq[4]), run_time = 3)
        self.wait(2)

    # functions
    def get_vector_equation(self, vec_num_a, vec_num_b, vec_num_c, three_dim = False, **kwargs):
        if three_dim:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]], [vec_num_a[2]]], left_bracket="(", right_bracket=")", **kwargs)
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]], [vec_num_b[2]]], left_bracket="(", right_bracket=")", **kwargs)
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]], [vec_num_c[2]]], left_bracket="(", right_bracket=")", **kwargs)

        else:
            vector_a = Matrix([[vec_num_a[0]],[vec_num_a[1]]], left_bracket="(", right_bracket=")", **kwargs)
            vector_b = Matrix([[vec_num_b[0]],[vec_num_b[1]]], left_bracket="(", right_bracket=")", **kwargs)
            vector_c = Matrix([[vec_num_c[0]],[vec_num_c[1]]], left_bracket="(", right_bracket=")", **kwargs)

        add_sign = MathTex("+")
        equal_sign = MathTex("=")

        vector_eq_subuation = VGroup(vector_a, add_sign, vector_b, equal_sign, vector_c)\
            .arrange_submobjects(RIGHT)

        return vector_eq_subuation


class GeoVSAnal(Scene):
    def construct(self):

        frames = VGroup(*[
            ScreenRectangle(height = 3.5).set(stroke_width = 2) 
            for _ in range(2)
        ])
        frames[0].to_corner(UR, buff = 0.75)
        frames[1].to_corner(DL, buff = 0.75)

        titles = VGroup(*[
            Text(text)\
                .next_to(frame.get_corner(corner), direction, aligned_edge = edge, buff = 0.75)\
                .set_color_by_gradient(*colors)\
                .set_fill(color = GREY, opacity = 0.5)\
                .set_stroke(width = 1)
            for text, frame, corner, direction, edge, colors in zip(
                ["geometrisch", "algebraisch"], 
                frames, 
                [UL, DR],
                [LEFT, RIGHT],
                [UP, DOWN],
                [[vec_a_color, vec_b_color], [vec_b_color, BLUE]]
            )
        ])

        text_geo = Tex("Vektor des ", "zweiten Summanden\\\\", "parallel ans Ende des\\\\", "ersten Vektors ", "verschieben")
        text_geo.set_color_by_tex_to_color_map({"zweiten Summanden": vec_b_color, "ersten Vektors": vec_a_color})
        text_geo.scale(0.8)

        text_anal = Tex("Komponentenweise\\\\", "Addition")
        text_anal.scale(0.8)

        text_geo.next_to(frames[0], LEFT, buff = 1)
        text_anal.next_to(frames[1], RIGHT, buff = 1)

        self.play(
            AnimationGroup(
                FadeIn(frames[0], shift = 2*LEFT),
                FadeIn(titles[0], shift = 2*RIGHT),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()
        self.play(Write(text_geo), run_time = 2)
        self.wait()

        self.play(
            AnimationGroup(
                FadeIn(frames[1], shift = 2*RIGHT), 
                FadeIn(titles[1], shift = 2*LEFT),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()
        self.play(Write(text_anal), run_time = 2)
        self.wait(3)





class Thumbnail(UseGhostMovements):
    def construct(self):

        self.first_vector()
        self.second_vector()
        self.ghost_dots_addition()
        self.result()
        self.component_addition()

        title = Tex("Vektoraddition")\
            .set_color_by_gradient(vec_a_color, vec_c_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 1)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1.5)

        epi = Tex("Episode 01")\
            .next_to(title, DOWN, aligned_edge = RIGHT)\
            .add_background_rectangle()

        self.add(title, epi)
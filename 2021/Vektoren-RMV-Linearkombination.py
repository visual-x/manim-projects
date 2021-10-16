from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE


class StandardBasis(VectorScene):
    def construct(self):
        self.vec_num = [3,2,0]
        self.write_coords()
        self.turn_coords_into_vector_matrix()
        self.basis_vector()
        self.scaled_basis_vectors()
        self.write_as_linear_combination()
        self.def_linear_combination()


    def write_coords(self):
        self.plane = NumberPlane(background_line_style={"stroke_opacity": 0.6})
        self.add(self.plane)
        self.wait()

        self.vector = self.get_vector(self.vec_num, color = vec_c_color)
        self.play(GrowArrow(self.vector), run_time = 2)
        self.wait()

        self.xy_lines = self.get_xy_lines(self.vec_num)
        self.play(Create(self.xy_lines))
        self.wait()

        self.xy_coordinates = self.get_xy_lines_coordinates(self.vec_num, self.xy_lines)
        self.play(Create(self.xy_coordinates))
        self.wait()

    def turn_coords_into_vector_matrix(self):
        matrix = [[self.vec_num[0]], [self.vec_num[1]]]

        if self.vec_num[0] > 0:
            direc = RIGHT + np.sign(self.vec_num[1]) * UP
        else:
            direc = LEFT + np.sign(self.vec_num[1]) * UP

        vector_matrix = self.vector_matrix = Matrix(matrix, left_bracket="(", right_bracket=")", bracket_v_buff = 0.1)\
            .next_to(self.vector.get_end(), direc)

        rect_top = Rectangle(width = config["frame_width"], height = 2)\
            .set_fill(color = BLACK, opacity = 0.7)\
            .set_stroke(width = 0)\
            .to_edge(UP, buff = 0)\
            .shift(0.1*UP)


        x_coord = self.xy_coordinates[0].copy()
        y_coord = self.xy_coordinates[1].copy()
        self.play(
            AnimationGroup(
                Create(rect_top),
                Transform(x_coord, vector_matrix[0][0]), 
                Transform(y_coord, vector_matrix[0][1]), 
                Write(vector_matrix[1:]),
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait()


        self.play(LaggedStartMap(FadeOut, VGroup(*self.xy_lines, *self.xy_coordinates), lag_ratio = 0.15))
        self.wait()

        self.vector_matrix = vector_matrix

    def basis_vector(self):

        basis_vectors = self.get_basis_vectors(i_hat_color = x_color, j_hat_color = y_color)
        basis_vector_labels = VGroup(*[
            MathTex(label).next_to(vect, direc).set_color(color)
            for vect, label, color, direc in [
                (basis_vectors[0], "\\vec{e}_x", x_color, DOWN),
                (basis_vectors[1], "\\vec{e}_y", y_color, LEFT),
            ]
        ])

        basis_vector_mat_labels = VGroup(*[
            MathTex("\\vec{e}_", str(coord), "=")\
            for coord in ["x", "y"]
        ])
        basis_vector_mat_labels.arrange_submobjects(RIGHT, buff = 3)\
            .next_to(self.vector_matrix, LEFT, buff = 3.5)
        basis_vector_mat_labels[0][:2].set_color(x_color)
        basis_vector_mat_labels[1][:2].set_color(y_color)

        basis_vector_matrices = VGroup(*[
            Matrix(matrix, left_bracket="(", right_bracket=")", bracket_v_buff = 0.1)\
                .next_to(label, RIGHT)
            for matrix, label in zip(
                [[[1], [0]], [[0], [1]]], 
                basis_vector_mat_labels
            )
        ])
        basis_vector_matrices[0][0][0].set_color(x_color)
        basis_vector_matrices[1][0][1].set_color(y_color)

        for index in range(len(basis_vectors)):
            self.play(Create(basis_vectors[index]), run_time = 1.5)
            self.play(Write(basis_vector_labels[index]), run_time = 1.5)
            self.wait()

            self.play(
                AnimationGroup(
                    TransformFromCopy(basis_vector_labels[index], basis_vector_mat_labels[index][:2]),
                    Create(basis_vector_mat_labels[index][2]),
                    Create(basis_vector_matrices[index]),
                    lag_ratio = 0.2
                ), 
                run_time = 3
            )
            self.wait()

        self.basis_vectors = basis_vectors
        self.basis_vector_matrices = basis_vector_matrices
        self.basis_vector_labels = basis_vector_labels

    def scaled_basis_vectors(self):
        unit_vectors_scaled = VGroup(*[
            Vector(self.vec_num[index] * self.basis_vectors[index].get_end(), color = color)
            for index, color in zip([0,1], [x_color, y_color])
        ])

        new_labels = VGroup(*[
            MathTex(str(self.vec_num[index]), "\\cdot", "\\vec{e}_", str(coord))\
                .set_color(color)\
                .next_to(unit_vector, direction)
            for index, coord, color, unit_vector, direction in zip(
                [0, 1], ["x", "y"], [x_color, y_color], unit_vectors_scaled, [DOWN, LEFT]
            )
        ])

        for index in range(len(unit_vectors_scaled)):
            self.play(ReplacementTransform(self.basis_vectors[index].copy(), unit_vectors_scaled[index]), run_time = 2)
            self.play(ReplacementTransform(self.basis_vector_labels[index], new_labels[index]))
            self.wait()


        self.play(
            new_labels[1].animate.shift((self.vec_num[0] + 1.75) * RIGHT),
            unit_vectors_scaled[1].animate.shift(self.vec_num[0] * RIGHT),
            run_time = 3
        )
        self.wait()

        colors = [x_color, y_color]
        sur_rects_scalars = VGroup(*[
            SurroundingRectangle(number, color = color)
            for number, color in zip(
                [new_labels[0][0], new_labels[1][0]], 
                colors
            ) 
        ])

        sur_rects_coords = VGroup(*[
            SurroundingRectangle(coord, color = color)
            for coord, color in zip(
                [self.vector_matrix[0][0], self.vector_matrix[0][1]], 
                colors
            )
        ])

        for index in range(len(sur_rects_scalars)):
            self.play(
                AnimationGroup(
                    Create(sur_rects_scalars[index]),
                    Create(sur_rects_coords[index]),
                    lag_ratio = 0.5
                )
            )
        self.wait()
        self.play(FadeOut(VGroup(sur_rects_scalars, sur_rects_coords)))


        self.new_labels = new_labels

    def write_as_linear_combination(self):
        rect_bot = Rectangle(width = config["frame_width"], height = 2)\
            .set_fill(color = BLACK, opacity = 0.7)\
            .set_stroke(width = 0)\
            .to_edge(DOWN, buff = 0)\
            .shift(0.1*DOWN)

        vec_mat = self.vector_matrix.copy()
        vec_mat.generate_target()
        vec_mat.target.next_to(rect_bot.get_left(), buff = 1).set_color(vec_c_color)

        self.play(
            Create(rect_bot, run_time = 1), 
            MoveToTarget(vec_mat, path_arc = -60*DEGREES, run_time = 2), 
        )

        eq_buff = 0.42
        equal1 = MathTex("=").next_to(vec_mat, RIGHT, buff = eq_buff)
        scalar1 = MathTex(str(self.vec_num[0])).next_to(equal1, RIGHT, buff = eq_buff).set_color(x_color)
        cdot1 = MathTex("\\cdot").next_to(scalar1, RIGHT, buff = eq_buff)


        ex_vec = self.basis_vectors[0].copy()
        ex_vec.generate_target()
        ex_vec.target.next_to(cdot1, RIGHT, buff = eq_buff)

        # 3 * unit_x
        self.play(
            AnimationGroup(
                Write(equal1),
                TransformFromCopy(self.new_labels[0][0], scalar1),
                Write(cdot1),
                MoveToTarget(ex_vec),
                lag_ratio = 0.2
            ),
            run_time = 3
        )

        # + 2 * unit_y
        plus = MathTex("+").next_to(ex_vec, RIGHT, buff = eq_buff)
        scalar2 = MathTex(str(self.vec_num[1])).next_to(plus, RIGHT, buff = eq_buff).set_color(y_color)
        cdot2 = MathTex("\\cdot").next_to(scalar2, RIGHT, buff = eq_buff)

        ey_vec = self.basis_vectors[1].copy()
        ey_vec.generate_target()
        ey_vec.target.next_to(cdot2, RIGHT, buff = eq_buff)

        self.play(
            AnimationGroup(
                Write(plus),
                TransformFromCopy(self.new_labels[1][0], scalar2),
                Write(cdot2),
                MoveToTarget(ey_vec),
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()


        ex_mat = self.basis_vector_matrices[0].copy()
        ex_mat.move_to(ex_vec)


        self.vec_mat = vec_mat

    def def_linear_combination(self):
        title = Text("Linearkombination")\
            .set_color_by_gradient(vec_c_color, x_color, y_color)\
            .set_fill(color = BLACK, opacity = 0)\
            .set_stroke(width = 2)\
            .scale(1.25)\
            .next_to(self.vec_mat, 1.5*UP, aligned_edge = LEFT)

        self.play(AddTextLetterByLetter(title), run_time = 1.5)
        self.wait()

        print(title.get_center())



    # functions

    def get_xy_lines(self, vec_num):
        x_line = Line(ORIGIN, vec_num[0] * RIGHT, color = x_color)
        y_line = Line(x_line.get_end(), x_line.get_end() + vec_num[1] * UP, color = y_color)

        result = VGroup(x_line, y_line)
        return result

    def get_xy_lines_coordinates(self, vec_num, xy_lines):
        x_step = MathTex(str(vec_num[0]))
        y_step = MathTex(str(vec_num[1]))

        if vec_num[0] > 0 and vec_num[1] > 0:
            direc_x, direc_y = DOWN, RIGHT
        elif vec_num[0] < 0 and vec_num[1] > 0:
            direc_x, direc_y = DOWN, LEFT
        elif vec_num[0] < 0 and vec_num[1] < 0:
            direc_x, direc_y = UP, LEFT
        elif vec_num[0] > 0 and vec_num[1] < 0:
            direc_x, direc_y = UP, RIGHT

        for coord, line, direction in zip([x_step, y_step], xy_lines, [direc_x, direc_y]):
            coord.next_to(line, direction)
            coord.set_color(line.get_color())

        result = VGroup(x_step, y_step)
        return result


class SecondExample(StandardBasis):
    def construct(self):
        self.vec_num = [-4,-1,0]

        self.write_coords()
        self.turn_coords_into_vector_matrix()


class DefineLinearCombination(Scene):
    def construct(self):
        self.vec_num = [3,2,0]
        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "bracket_v_buff": 0.1}

        self.get_mobjects_from_old_scene()
        self.scalars_and_vectors()
        self.write_with_three_vectors()
        self.show_three_vectors()


    def get_mobjects_from_old_scene(self):
        self.title = Text("Linearkombination")\
            .set_color_by_gradient(vec_c_color, x_color, y_color)\
            .set_fill(color = BLACK, opacity = 0)\
            .set_stroke(width = 2)\
            .scale(1.25)\
            .move_to(-2.58230252*RIGHT + 1.72795901 * DOWN)

        matrix = [[self.vec_num[0]], [self.vec_num[1]]]
        vec_mat = self.vec_mat = Matrix(matrix, **self.matrix_kwargs)\
            .move_to(5.52661541 * LEFT + 3.1 * DOWN)

        eq_buff = 0.42
        equal1 = MathTex("=").next_to(vec_mat, RIGHT, buff = eq_buff)
        scalar1 = MathTex(str(self.vec_num[0])).next_to(equal1, RIGHT, buff = eq_buff).set_color(x_color)
        cdot1 = MathTex("\\cdot").next_to(scalar1, RIGHT, buff = eq_buff)

        ex_vec = Arrow(ORIGIN, RIGHT, color = x_color, buff = 0)
        ex_vec.next_to(cdot1, RIGHT, buff = eq_buff)

        plus = MathTex("+").next_to(ex_vec, RIGHT, buff = eq_buff)
        scalar2 = MathTex(str(self.vec_num[1])).next_to(plus, RIGHT, buff = eq_buff).set_color(y_color)
        cdot2 = MathTex("\\cdot").next_to(scalar2, RIGHT, buff = eq_buff)

        ey_vec = Arrow(ORIGIN, UP, color = y_color, buff = 0)
        ey_vec.next_to(cdot2, RIGHT, buff = eq_buff)


        self.vec_eq = VGroup(vec_mat, equal1, scalar1, cdot1, ex_vec, plus, scalar2, cdot2, ey_vec)
        self.add(self.title, self.vec_eq)
        self.wait()


        self.plus = plus

    def scalars_and_vectors(self):
        self.title.generate_target()
        self.title.target.to_edge(UP)

        self.vec_eq.generate_target()
        self.vec_eq.target.center().shift(LEFT)

        self.play(
            AnimationGroup(
                MoveToTarget(self.title), 
                MoveToTarget(self.vec_eq), 
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()


        # Skalare nach unten, Vektoren nach oben
        shift_vec = [self.vec_eq[4], self.vec_eq[8]]
        shift_sca = [self.vec_eq[2], self.vec_eq[6]]

        self.play(
            AnimationGroup(
                VGroup(*shift_vec).animate.shift(1*UP),
                VGroup(*shift_sca).animate.shift(1*DOWN),
                lag_ratio = 0.15
            ),
            run_time = 2
        )

        # Pfeile durch Vektoren ersetzen
        mat_a = Matrix([[1], [0]], **self.matrix_kwargs).move_to(self.vec_eq[4])
        mat_b = Matrix([[0], [1]], **self.matrix_kwargs).move_to(self.vec_eq[8], aligned_edge=LEFT)
        self.play(
            Transform(self.vec_eq[4], mat_a), 
            Transform(self.vec_eq[8], mat_b),
        )
        self.wait(0.5)

        # Vektoren zurück schieben
        self.play(VGroup(*shift_vec).animate.shift(1*DOWN))
        self.wait()

        # Skalare zurück schieben
        self.play(VGroup(*shift_sca).animate.shift(1*UP), run_time = 1.5)
        self.wait()

        # Pluszeichen highlighten --> Gesetze der Addition --> aneinanderhängen
        self.play(Circumscribe(self.vec_eq[5], color = YELLOW, shape = Circle, time_width = 0.5, run_time = 2))
        self.wait()


        self.play(self.vec_eq.animate.shift(1.5*LEFT), run_time = 3)

    def write_with_three_vectors(self):
        eq_buff = 0.42

        scalar_1 = MathTex("2").set_color(x_color).move_to(self.vec_eq[2])
        mat_a = Matrix([[2], [1]], **self.matrix_kwargs).move_to(self.vec_eq[4])
        scalar_2 = MathTex("1").set_color(y_color).move_to(self.vec_eq[6])
        mat_b = Matrix([[-1], [1]], **self.matrix_kwargs).move_to(self.vec_eq[8])


        plus = MathTex("+").next_to(self.vec_eq[-1], RIGHT, buff = eq_buff)
        scalar_3 = MathTex("(-1)").set_color(MAROON).next_to(plus, RIGHT, buff = eq_buff)
        cdot3 = MathTex("\\cdot").next_to(scalar_3, RIGHT, buff = eq_buff)
        mat_c = Matrix([[0], [1]], **self.matrix_kwargs).next_to(cdot3, RIGHT, buff = eq_buff)


        self.play(
            AnimationGroup(
                Transform(self.vec_eq[2], scalar_1),
                Transform(self.vec_eq[4], mat_a),
                Transform(self.vec_eq[6], scalar_2),
                Transform(self.vec_eq[8], mat_b),
                Write(plus), 
                Write(scalar_3), 
                Write(cdot3),
                Write(mat_c),
                lag_ratio = 0.15
            ), 
            run_time = 4
        )
        self.wait(3)

        self.play(
            FadeOut(self.title, shift = 2*UP), 
            VGroup(*self.vec_eq, plus, scalar_3, cdot3, mat_c).animate.to_edge(UP), 
            run_time = 2
        )

        self.plus2, self.scalar_1, self.scalar_2, self.scalar_3 = plus, self.vec_eq[2], self.vec_eq[6], scalar_3

    def show_three_vectors(self):
        rect = ScreenRectangle(height = 5.5)
        rect.to_edge(DOWN)
        rect.set_stroke(width = 3, color = GREY)

        self.play(Create(rect), run_time = 2)
        self.wait(3)

        # Indicating all three scalars
        self.play(Circumscribe(self.scalar_1, color = BLUE, shape = Rectangle, time_width = 0.5, run_time = 2))
        self.wait()

        self.play(Circumscribe(self.scalar_2, color = BLUE, shape = Rectangle, time_width = 0.5, run_time = 2))
        self.wait()

        self.play(Circumscribe(self.scalar_3, color = BLUE, shape = Rectangle, time_width = 0.5, run_time = 2))
        self.wait()

        # Indicating taking the sum --> adding vectors

        self.play(Circumscribe(self.plus, color = YELLOW, shape = Circle, time_width = 0.5, run_time = 2))
        self.wait()

        self.play(Circumscribe(self.plus2, color = YELLOW, shape = Circle, time_width = 0.5, run_time = 2))
        self.wait()


class ShowThreeVectors(MovingCameraScene, VectorScene):
    def construct(self):
        self.camera.frame.set(width = config.frame_width * 0.7)
        self.camera.frame.shift(1.5*RIGHT + 1*UP)

        self.vec_a_num = [2,1,0]
        self.vec_b_num = [-1,1,0]
        self.vec_c_num = [0,1,0]

        plane = self.plane = NumberPlane(
            axis_config = {"stroke_color": GREY},
            background_line_style={"stroke_opacity": 0.6}
        )
        plane.add_coordinates(x_values=[3], y_values=[2])

        arrow_kwargs = {"max_tip_length_to_length_ratio": 0.5}
        vecs = VGroup(*[
            self.get_vector(vec_num, color = color, **arrow_kwargs)
            for vec_num, color in zip(
                [self.vec_a_num, self.vec_b_num, self.vec_c_num], 
                [x_color, y_color, MAROON]
            )
        ])

        vecs_scaled = VGroup(*[
            self.get_vector([scalar * x for x in vec_num], color = color, **arrow_kwargs)
            for scalar, vec_num, color in zip(
                [2,1,-1],
                [self.vec_a_num, self.vec_b_num, self.vec_c_num], 
                [x_color, y_color, MAROON]
            )
        ])

        self.play(Create(plane, lag_ratio = 0.15), run_time = 2)
        self.play(LaggedStartMap(GrowArrow, vecs, lag_ratio = 0.25), run_time = 2)
        self.wait()


        self.play(
            AnimationGroup(
                *[Transform(vec, vec_scaled) for vec, vec_scaled in zip(vecs, vecs_scaled)], lag_ratio = 0.75
            ), 
            run_time = 6
        )
        self.wait()


        self.play(vecs[1].animate.shift([2*x for x in self.vec_a_num]), run_time = 4)
        self.wait(0.5)

        self.play(vecs[2].animate.shift([2*x + y for x,y in zip(self.vec_a_num, self.vec_b_num)]),run_time = 4)
        self.wait()


        final_vec = self.get_vector([3,2,0], color = BLUE, **arrow_kwargs)
        self.play(
            GrowArrow(final_vec),
            *[vec.animate.set_stroke(opacity = 0.5).set_fill(opacity = 0.5) for vec in vecs],
            run_time = 2
        )
        xy_lines = self.get_xy_lines(final_vec).set_color(WHITE)
        self.play(ShowPassingFlash(xy_lines, time_width = 1, lag_ratio = 0.15), run_time = 3)
        self.wait(3)


    # functions 
    def get_xy_lines(self, arrow):
        x_line = Line(arrow.get_end(), arrow.get_end()[1]*UP, color = x_color)
        y_line = Line(arrow.get_end(), arrow.get_end()[0]*RIGHT, color = y_color)

        result = VGroup(x_line, y_line)

        return result


class ShowLinearCombinations(StandardBasis):
    def construct(self):

        sca_val_a = self.sca_val_a = ValueTracker(1)
        sca_val_b = self.sca_val_b = ValueTracker(1)

        self.sca_val_a_starting = 1.5
        self.sca_val_b_starting = 0.5

        self.vec_a_num = [1,2,0]
        self.vec_b_num = [3,-1,0]
        self.vec_l_num = [self.sca_val_a_starting * a + self.sca_val_b_starting * b for a,b in zip(self.vec_a_num, self.vec_b_num)]

        self.vector_kwargs = {"stroke_width": 3, "max_tip_length_to_length_ratio": 0.5}

        self.a_values = [-0.5, -1.20,  0.7, 1.50]
        self.b_values = [1.33, -1.75, -1.4, 0.50]

        self.setup_plane_vectors()
        self.add_updaters_to_vectors()
        self.show_first_sum()
        self.varying_values()
        self.show_lines_effect()
        self.calc_linear_combination()
        self.final_scalars_animation()


    def setup_plane_vectors(self):
        plane = self.plane = NumberPlane(
            axis_config = {"stroke_color": GREY},
            background_line_style={"stroke_opacity": 0.4}
        )

        vector_a = self.get_vector(self.vec_a_num, color = vec_a_color, **self.vector_kwargs)
        vector_b = self.get_vector(self.vec_b_num, color = vec_b_color, **self.vector_kwargs)
        vector_l = self.get_vector(self.vec_l_num, color = vec_c_color, **self.vector_kwargs)

        self.add(plane, vector_a, vector_b)
        self.wait()

        self.vector_a, self.vector_b, self.vector_l = vector_a, vector_b, vector_l

    def add_updaters_to_vectors(self):
        sca_val_a, sca_val_b = self.sca_val_a, self.sca_val_b

        self.vector_a.add_updater(lambda v: v.become(
            self.get_vector(
                [sca_val_a.get_value() * self.vec_a_num[0], sca_val_a.get_value() * self.vec_a_num[1], sca_val_a.get_value() * self.vec_a_num[2]], 
                color = vec_a_color, **self.vector_kwargs)
        ))

        self.vector_b.add_updater(lambda v: v.become(
            self.get_vector(
                [
                    sca_val_b.get_value() * self.vec_b_num[0], 
                    sca_val_b.get_value() * self.vec_b_num[1], 
                    sca_val_b.get_value() * self.vec_b_num[2]
                ],
                color = vec_b_color, **self.vector_kwargs
            )
        ))

        self.vector_l.add_updater(lambda v: v.become(
            Arrow(ORIGIN, self.vector_b.get_end(), color = vec_c_color, buff = 0, **self.vector_kwargs)
        ))

    def show_first_sum(self):
        vector_a, vector_b, vector_l = self.vector_a, self.vector_b, self.vector_l
        sca_val_a, sca_val_b = self.sca_val_a, self.sca_val_b

        ori_vectors = self.ori_vectors = VGroup(*[
            vector.copy().clear_updaters().set_fill(opacity = 0.3).set_stroke(opacity = 0.3)
            for vector in [vector_a, vector_b]
        ])
        self.add(ori_vectors)


        dec_a = DecimalNumber(sca_val_a.get_value(), unit = "\\ \\vec{a}")
        dec_b = DecimalNumber(sca_val_b.get_value(), unit = "\\ \\vec{b}")
        for dec, color in zip([dec_a, dec_b], [vec_a_color, vec_b_color]):
            dec[4:].set_color(color)

        dec_a.add_updater(lambda a: a.set_value(sca_val_a.get_value()))
        dec_a.add_updater(lambda a: a.next_to(midpoint(vector_a.get_end(), vector_a.get_start()), LEFT))

        dec_b.add_updater(lambda b: b.set_value(sca_val_b.get_value()))
        dec_b.add_updater(lambda b: b.next_to(midpoint(vector_b.get_end(), vector_b.get_start()), UP))


        self.play(Create(dec_a), Create(dec_b))
        self.wait()

        self.play(
            sca_val_a.animate(rate_func = squish_rate_func(smooth, 0, 0.8)).set_value(self.sca_val_a_starting),
            sca_val_b.animate(rate_func = squish_rate_func(smooth, 0.2, 1)).set_value(self.sca_val_b_starting),
            run_time = 3
        )
        self.wait()

        vector_b.clear_updaters()
        self.play(
            vector_b.animate.shift(
                sca_val_a.get_value() * self.vec_a_num[0] * RIGHT + 
                sca_val_a.get_value() * self.vec_a_num[1] * UP
            ),
            run_time = 3
        )

        self.vector_b.add_updater(lambda v: v.become(
            self.get_vector(
                [
                    self.sca_val_b.get_value() * self.vec_b_num[0], 
                    self.sca_val_b.get_value() * self.vec_b_num[1], 
                    self.sca_val_b.get_value() * self.vec_b_num[2]
                ],
                color = vec_b_color, **self.vector_kwargs
            ).shift(self.sca_val_a.get_value() * self.vec_a_num[0]*RIGHT + self.sca_val_a.get_value() * self.vec_a_num[1] * UP)
        ))

        vector_l.suspend_updating()
        self.play(GrowArrow(vector_l), run_time = 2)
        vector_l.resume_updating()
        self.wait()

    def varying_values(self):
        sca_val_a, sca_val_b = self.sca_val_a, self.sca_val_b

        for a_val, b_val in zip(self.a_values, self.b_values):
            self.play(
                sca_val_a.animate(rate_func = squish_rate_func(smooth, 0, 0.8)).set_value(a_val),
                sca_val_b.animate(rate_func = squish_rate_func(smooth, 0.2, 1)).set_value(b_val),
                run_time = 3
            )
            self.wait(1)
        self.wait(2)

    def show_lines_effect(self):
        self.play(self.sca_val_a.animate.set_value(-2), run_time = 1.5)

        trace_a_changing = TracedPath(self.vector_l.get_end, stroke_width = 4)
        self.add(trace_a_changing)
        self.play(self.sca_val_a.animate.set_value(1.5), run_time = 6)

        line_a = Line(start = self.plane.c2p(3, 2.5), end = self.plane.c2p(-1,-5.5), stroke_width = 4, color = WHITE)
        self.add(line_a)
        self.wait()

        trace_b_changing = TracedPath(self.vector_l.get_end, stroke_width = 4)
        self.add(trace_b_changing)
        self.play(self.sca_val_b.animate.set_value(2), run_time = 1.5)
        self.play(self.sca_val_b.animate.set_value(-2), run_time = 6)

        line_b = Line(start = self.plane.c2p(9, 0.5), end = self.plane.c2p(-3,4.5), stroke_width = 4, color = WHITE)
        self.add(line_b)
        self.wait()


        hoch = Tex("Hoch").rotate(self.vector_a.get_angle()).move_to(self.plane.c2p(2,1))
        runter = Tex("Runter").rotate(self.vector_a.get_angle() + TAU/2).move_to(self.plane.c2p(1,-2))
        links = Tex("Links").rotate(self.vector_b.get_angle() + TAU/2).move_to(self.plane.c2p(1.5, 3.5))
        rechts = Tex("Rechts").rotate(self.vector_b.get_angle() + TAU/2).move_to(self.plane.c2p(4.5, 2.5))

        self.play(
            AnimationGroup(
                FadeIn(hoch, shift = self.vector_a.get_unit_vector()), 
                FadeIn(runter, shift = -1*self.vector_a.get_unit_vector()),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()
        self.play(
            AnimationGroup(
                FadeIn(links, shift = self.vector_b.get_unit_vector()), 
                FadeIn(rechts, shift = -1*self.vector_b.get_unit_vector()),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()


        trace_a_changing.clear_updaters()
        trace_b_changing.clear_updaters()

        self.play(
            *[FadeOut(mob) for mob in [trace_a_changing, trace_b_changing, line_a, line_b, hoch, runter, links, rechts]],
            self.sca_val_a.animate.set_value(self.a_values[-1]),
            self.sca_val_b.animate.set_value(self.b_values[-1]),
            run_time = 2
        )
        self.wait()


    def calc_linear_combination(self):
        sca_val_a, sca_val_b = self.sca_val_a, self.sca_val_b

        rect_bot = Rectangle(width = config["frame_width"], height = 2)\
            .set_fill(color = BLACK, opacity = 0.7)\
            .set_stroke(width = 0)\
            .to_edge(DOWN, buff = 0)\
            .shift(0.1*DOWN)

        lc_vec = [
            sca_val_a.get_value() * self.vec_a_num[0] + sca_val_b.get_value() * self.vec_b_num[0], 
            sca_val_a.get_value() * self.vec_a_num[1] + sca_val_b.get_value() * self.vec_b_num[1],
            sca_val_a.get_value() * self.vec_a_num[2] + sca_val_b.get_value() * self.vec_b_num[2],
        ]

        x_comp = DecimalNumber(sca_val_a.get_value() * self.vec_a_num[0] + sca_val_b.get_value() * self.vec_b_num[0])
        y_comp = DecimalNumber(sca_val_a.get_value() * self.vec_a_num[1] + sca_val_b.get_value() * self.vec_b_num[1])
        # mat_c = Matrix([[lc_vec[0]], [lc_vec[1]]], left_bracket="(", right_bracket=")", bracket_v_buff = 0.1).set_color(vec_c_color)
        mat_c = MobjectMatrix([[x_comp], [y_comp]], left_bracket="(", right_bracket=")", bracket_h_buff = 0.4, bracket_v_buff = 0.1).set_color(vec_c_color)
        equals = MathTex("=")
        scalar_a = DecimalNumber(sca_val_a.get_value(), num_decimal_places = 2)
        cdota = MathTex("\\cdot")
        mat_a = Matrix([[self.vec_a_num[0]],[self.vec_a_num[1]]], left_bracket="(", right_bracket=")", bracket_v_buff = 0.1).set_color(vec_a_color)
        plus = MathTex("+")
        scalar_b = DecimalNumber(sca_val_b.get_value(), num_decimal_places = 2)
        cdotb = MathTex("\\cdot")
        mat_b = Matrix([[self.vec_b_num[0]],[self.vec_b_num[1]]], left_bracket="(", right_bracket=")", bracket_v_buff = 0.1).set_color(vec_b_color)

        eq_buff = 0.5
        final_eq = VGroup(mat_c, equals, scalar_a, cdota, mat_a, plus, scalar_b, cdotb, mat_b)\
            .arrange_submobjects(RIGHT, buff = eq_buff)\
            .move_to(rect_bot)



        vec_a = self.ori_vectors[0].copy()
        vec_a.generate_target()
        vec_a.target.set_stroke(opacity = 1).set_fill(opacity = 1).match_height(mat_a).move_to(mat_a)

        vec_b = self.ori_vectors[1].copy()
        vec_b.generate_target()
        vec_b.target.set_stroke(opacity = 1).set_fill(opacity = 1).match_width(mat_b).move_to(mat_b)


        self.play(
            Create(rect_bot, run_time = 1),
            AnimationGroup(*[MoveToTarget(target) for target in [vec_a, vec_b]], lag_ratio = 0.1, run_time = 3), 
        )
        self.play(
            AnimationGroup(
                Write(final_eq[1:4]), 
                Write(final_eq[5:8]),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.play(
            Write(final_eq[0][1:]), run_time = 2
        )
        self.wait()

        # Pfeile in LC durch Vektoren ersetzen
        self.play(
            AnimationGroup(
                *[FadeOut(vec, shift = UP) for vec in [vec_a, vec_b]],
                *[FadeIn(mat, shift = UP) for mat in [mat_a, mat_b]],
                lag_ratio = 0.1
            ),
            run_time = 2
        )
        self.wait()

        # Koordinateneinträge berechnen
        self.play(
            *[mat[0][1].animate.set_fill(opacity = 0.3) for mat in [mat_a, mat_b]], 
            run_time = 3
        )
        self.wait()

        braces = VGroup(*[
            BraceBetweenPoints(final_eq[start:end].get_corner(UL), final_eq[start:end].get_corner(UR), UP)
            for start, end in zip([2, 6], [5, 9])
        ])

        braces_tex1 = VGroup(*[
            brace.get_tex(tex) for brace, tex in zip(
                braces, ["1.5", "1.5"]
            )
        ])

        for brace, brace_tex, index in zip(braces, braces_tex1, range(len(braces))):
            self.play(Create(brace))
            self.play(Write(brace_tex))
            self.wait()

        self.play(Write(mat_c[0][0]))

        self.play(
            *[mat[0][0].animate.set_fill(opacity = 0.3) for mat in [mat_a, mat_b]], 
            *[mat[0][1].animate.set_fill(opacity = 1.0) for mat in [mat_a, mat_b]], 
            run_time = 3
        )

        braces_tex2 = VGroup(*[
            brace.get_tex(tex) for brace, tex in zip(
                braces, ["3", "-0.5"]
            )
        ])

        for index in range(len(braces_tex1)):
            self.play(Transform(braces_tex1[index], braces_tex2[index]))
            self.wait(0.5)

        self.play(Write(mat_c[0][1]))


        xy_lines = self.get_xy_lines(lc_vec)
        xy_coords = self.get_xy_lines_coordinates(lc_vec, xy_lines)
        self.play(
            Create(xy_lines, run_time = 3), 
            Create(xy_coords, run_time = 2, rate_func = squish_rate_func(smooth, 0.4, 1)),
        )
        self.wait(3)


        self.play(
            FadeOut(VGroup(*braces, *braces_tex1, *xy_lines, *xy_coords), lag_ratio = 0.1),
            *[mat[0][0].animate.set_fill(opacity = 1) for mat in [mat_a, mat_b]],  
            run_time = 2
        )
        self.wait()

        self.scalar_a, self.scalar_b = scalar_a, scalar_b
        self.x_comp, self.y_comp = x_comp, y_comp

    def final_scalars_animation(self):
        scalar_a, scalar_b = self.scalar_a, self.scalar_b
        sca_val_a, sca_val_b = self.sca_val_a, self.sca_val_b
        x_comp, y_comp = self.x_comp, self.y_comp

        scalar_a.add_updater(lambda a: a.set_value(sca_val_a.get_value()))
        scalar_b.add_updater(lambda b: b.set_value(sca_val_b.get_value()))

        x_comp.add_updater(lambda x: x.set_value(sca_val_a.get_value() * self.vec_a_num[0] + sca_val_b.get_value() * self.vec_b_num[0]))
        y_comp.add_updater(lambda x: x.set_value(sca_val_a.get_value() * self.vec_a_num[1] + sca_val_b.get_value() * self.vec_b_num[1]))

        a_values = [ 0.5, -0.25, 1.2]
        b_values = [-1.4,  1.25, 1.6]

        for a_val, b_val in zip(a_values, b_values):
            self.play(
                sca_val_a.animate(rate_func = squish_rate_func(smooth, 0, 0.8)).set_value(a_val),
                sca_val_b.animate(rate_func = squish_rate_func(smooth, 0.2, 1)).set_value(b_val),
                run_time = 2.5
            )
            self.wait(2)
        self.wait(2)


class VaryingLC(ShowLinearCombinations):
    def construct(self):
        sca_val_a = self.sca_val_a = ValueTracker(1)
        sca_val_b = self.sca_val_b = ValueTracker(1)

        self.sca_val_a_starting = 0.75
        self.sca_val_b_starting = -2

        self.vec_a_num = [4,-1,0]
        self.vec_b_num = [-1,-2,0]
        self.vec_l_num = [self.sca_val_a_starting * a + self.sca_val_b_starting * b for a,b in zip(self.vec_a_num, self.vec_b_num)]

        self.vector_kwargs = {"stroke_width": 3, "max_tip_length_to_length_ratio": 0.5}


        self.a_values = [-0.5, -0.80, 1.5,  1.10]
        self.b_values = [1.33, -1.25, 1.0, -1.60]

        self.setup_plane_vectors()
        self.add_updaters_to_vectors()
        self.show_first_sum()
        self.varying_values()


class Thumbnail1(ShowLinearCombinations):
    def construct(self):

        sca_val_a = self.sca_val_a = ValueTracker(1)
        sca_val_b = self.sca_val_b = ValueTracker(1)

        self.sca_val_a_starting = 1.5
        self.sca_val_b_starting = 0.5

        self.vec_a_num = [1,2,0]
        self.vec_b_num = [3,-1,0]
        self.vec_l_num = [self.sca_val_a_starting * a + self.sca_val_b_starting * b for a,b in zip(self.vec_a_num, self.vec_b_num)]

        self.vector_kwargs = {"stroke_width": 3, "max_tip_length_to_length_ratio": 0.5}

        self.a_values = [-0.5, -1.20,  0.7, 1.50]
        self.b_values = [1.33, -1.75, -1.4, 0.50]

        self.setup_plane_vectors()
        self.add_updaters_to_vectors()
        self.show_first_sum()
        self.varying_values()
        self.show_lines_effect()



        dots = VGroup()
        for r in np.linspace(-3,3,7):
            for s in np.linspace(-3,3,7):
                dot = Dot(
                    point = self.plane.c2p(*[r*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                    radius = 0.06, 
                    color = GREY
                )
                dots.add(dot)


        lines_kwags = {"stroke_width": 2, "stroke_opacity": 0.4}
        lines_a = VGroup(*[
            Line(
                start = self.plane.c2p(*[-3*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.plane.c2p(*[+3*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags, color = vec_a_color
            )
            for s in np.linspace(-3,3,7)
        ])


        lines_b = VGroup(*[
            Line(
                start = self.plane.c2p(*[r*comp_a - 3*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.plane.c2p(*[r*comp_a + 3*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags, color = vec_b_color
            )
            for r in np.linspace(-3,3,7)
        ])



        title = Tex("Linearkombinationen")\
            .set_color_by_gradient(vec_a_color, vec_c_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 1)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1.5)

        epi = Tex("Episode 03")\
            .next_to(title, UP, aligned_edge = RIGHT)\
            .add_background_rectangle()



        self.add(dots, lines_a, lines_b, title, epi)








class StudentsJob(Scene):
    def construct(self):
        self.vec_a_num = [2,1,1]
        self.vec_b_num = [1,1,2]
        self.vec_l_num = [2*a - b for a,b in zip(self.vec_a_num, self.vec_b_num)]

        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6 , "bracket_v_buff": 0.1}
        self.arrow_kwargs = {"stroke_width": 4, "max_tip_length_to_length_ratio": 0.25}

        self.what_students_are_asked_to_do()
        self.prepare_for_next_scene()



    def what_students_are_asked_to_do(self):
        vec_eq = self.get_vector_equation()
        vec_eq.shift(UP)

        title = Text("Linearkombination")\
            .set_color_by_gradient(vec_c_color, x_color, y_color)\
            .set_fill(color = BLACK, opacity = 0)\
            .set_stroke(width = 1.25)\
            .set(width = vec_eq.get_width())\
            .next_to(vec_eq, UP)

        self.play(
            Create(vec_eq, lag_ratio = 0.2), 
            AddTextLetterByLetter(title), 
            run_time = 2
        )
        self.wait()

        self.play(
            AnimationGroup(
                Indicate(vec_eq[0], color = vec_c_color),
                Indicate(vec_eq[4], color = vec_a_color),
                Indicate(vec_eq[8], color = vec_b_color),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()


        arrow_a = Arrow(vec_eq[2].get_bottom(), 2.1*DOWN + 1.5*LEFT,  color = x_color, **self.arrow_kwargs)
        arrow_b = Arrow(vec_eq[6].get_bottom(), 2.1*DOWN + 3.0*RIGHT, color = y_color, **self.arrow_kwargs)

        self.play(LaggedStartMap(GrowArrow, VGroup(arrow_a, arrow_b), lag_ratio = 0.25), run_time = 3)
        self.wait(3)


        self.vec_eq, self.title = vec_eq, title
        self.arrow_a, self.arrow_b = arrow_a, arrow_b

    def prepare_for_next_scene(self):
        self.play(
            AnimationGroup(
                FadeOut(self.title, shift = 3*UP),
                self.vec_eq.animate.to_edge(UP),
                *[FadeOut(arrow, shift = direction) for arrow, direction in zip([self.arrow_a, self.arrow_b], [3*LEFT, 3*RIGHT])], 
                lag_ratio = 0.1
            ),
            run_time = 3
        )
        self.wait()

    # functions

    def get_vector_equation(self, scalar_1_name = "r", scalar_2_name = "s"):
        mat_a = Matrix([[self.vec_a_num[0]], [self.vec_a_num[1]], [self.vec_a_num[2]]], **self.matrix_kwargs)
        mat_b = Matrix([[self.vec_b_num[0]], [self.vec_b_num[1]], [self.vec_b_num[2]]], **self.matrix_kwargs)
        mat_c = Matrix([[self.vec_l_num[0]], [self.vec_l_num[1]], [self.vec_l_num[2]]], **self.matrix_kwargs)

        equals = MathTex("=")
        scalar_a = MathTex(scalar_1_name)
        cdot1 = MathTex("\\cdot")
        plus = MathTex("+")
        scalar_b = MathTex(scalar_2_name)
        cdot2 = MathTex("\\cdot")

        eqs = VGroup(mat_c, equals, scalar_a, cdot1, mat_a, plus, scalar_b, cdot2, mat_b)\
            .arrange_submobjects(RIGHT)

        return eqs


class StudentsJobLinCombAnimation(Scene):
    def construct(self):
        vec_a_num = [2,1,1]
        vec_b_num = [1,1,2]
        vec_l_num = [2*a - b for a,b in zip(vec_a_num, vec_b_num)]

        sca_val_a = ValueTracker(3)
        sca_val_b = ValueTracker(1)

        matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6 , "bracket_v_buff": 0.1}
        mat_a = Matrix([[vec_a_num[0]], [vec_a_num[1]], [vec_a_num[2]]], **matrix_kwargs)
        mat_b = Matrix([[vec_b_num[0]], [vec_b_num[1]], [vec_b_num[2]]], **matrix_kwargs)

        x_comp = DecimalNumber(sca_val_a.get_value() * vec_a_num[0] + sca_val_b.get_value() * vec_b_num[0], edge_to_fix = RIGHT)
        y_comp = DecimalNumber(sca_val_a.get_value() * vec_a_num[1] + sca_val_b.get_value() * vec_b_num[1], edge_to_fix = RIGHT)
        z_comp = DecimalNumber(sca_val_a.get_value() * vec_a_num[2] + sca_val_b.get_value() * vec_b_num[2], edge_to_fix = RIGHT)
        mat_c = MobjectMatrix([[x_comp], [y_comp], [z_comp]], **matrix_kwargs, bracket_h_buff = 0.5)


        equals = MathTex("=")
        scalar_a = DecimalNumber(sca_val_a.get_value(), edge_to_fix = RIGHT)
        cdot1 = MathTex("\\cdot")
        plus = MathTex("+")
        scalar_b = DecimalNumber(sca_val_b.get_value(), edge_to_fix = RIGHT)
        cdot2 = MathTex("\\cdot")

        lincomb = VGroup(mat_c, equals, scalar_a, cdot1, mat_a, plus, scalar_b, cdot2, mat_b)\
            .arrange_submobjects(RIGHT, buff = 0.5)\
            .to_edge(DOWN, buff = 0.75)


        self.play(FadeIn(lincomb, shift = 0.35*DOWN, lag_ratio = 0.1), run_time = 3)
        self.wait(2)


        x_comp.add_updater(lambda x: x.set_value(sca_val_a.get_value() * vec_a_num[0] + sca_val_b.get_value() * vec_b_num[0]))
        y_comp.add_updater(lambda x: x.set_value(sca_val_a.get_value() * vec_a_num[1] + sca_val_b.get_value() * vec_b_num[1]))
        z_comp.add_updater(lambda x: x.set_value(sca_val_a.get_value() * vec_a_num[2] + sca_val_b.get_value() * vec_b_num[2]))

        scalar_a.add_updater(lambda a: a.set_value(sca_val_a.get_value()))
        scalar_b.add_updater(lambda b: b.set_value(sca_val_b.get_value()))


        a_values = [0.5, -1,  2, -1, 0.2,  2]
        b_values = [2.0,  4, -3, -3, 0.8, -1]

        for a_val, b_val in zip(a_values, b_values):
            self.play(
                sca_val_a.animate(rate_func = squish_rate_func(smooth, 0, 0.8)).set_value(a_val),
                sca_val_b.animate(rate_func = squish_rate_func(smooth, 0.2, 1)).set_value(b_val),
                run_time = 2.5
            )
            self.wait(2)

        sur_rects = VGroup(*[
            SurroundingRectangle(scalar, color = color)
            for scalar, color in zip(
                [scalar_a, scalar_b], [y_color, x_color]
            )
        ])
        self.play(Create(sur_rects, lag_ratio = 0.15), run_time = 3)
        self.wait(2)


class StudentsJobCalculation(Scene):
    def construct(self):
        vec_a_num = self.vec_a_num = [2,1,1]
        vec_b_num = self.vec_b_num = [1,1,2]
        vec_l_num = self.vec_l_num = [2*a - b for a,b in zip(vec_a_num, vec_b_num)]

        self.eq_buff = 0.5
        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6 , "bracket_v_buff": 0.1}

        self.vector_equation()
        self.turn_vec_eq_into_lgs()
        self.what_kind_of_lgs()
        self.solve_lgs()
        self.sample()


    def vector_equation(self):
        vec_eq = self.vec_eq = self.get_vector_equation()
        vec_eq.to_edge(UP)

        self.add(vec_eq)
        self.wait()

    def turn_vec_eq_into_lgs(self):
        # Linien für das Gleichungssystem
        line_buff = 0.75
        lines = VGroup(*[
            Line(
                self.vec_eq.get_left() + line_buff * LEFT, self.vec_eq.get_right() + line_buff * RIGHT, 
                color = LIGHT_BROWN, stroke_width = 3
            )
            for x in range(2)
        ])
        lines.arrange_submobjects(DOWN, buff = self.matrix_kwargs.get("v_buff"))
        lines.move_to(self.vec_eq)

        self.play(Create(lines, lag_ratio = 0.25), run_time = 2)

        # Gleichungen aus der Vector_eq finden
        vec_eq = self.vec_eq
        x_comps = VGroup(vec_eq[0][0][0], vec_eq[4][0][0], vec_eq[8][0][0])
        y_comps = VGroup(vec_eq[0][0][1], vec_eq[4][0][1], vec_eq[8][0][1])
        z_comps = VGroup(vec_eq[0][0][2], vec_eq[4][0][2], vec_eq[8][0][2])

        eqs = self.get_three_equations()

        # Gleichung 1 schreiben
        self.play(
            VGroup(*y_comps, *z_comps, vec_eq[0][1:], vec_eq[4][1:], vec_eq[8][1:]).animate.set_color(DARK_GREY), lag_ratio = 0.1, 
            run_time = 4
        )
        self.wait()
        self.play(Write(eqs[0]), run_time = 2)
        self.wait()

        # Gleichung 2 schreiben
        self.play(
            VGroup(*y_comps).animate.set_color(WHITE),
            VGroup(*x_comps).animate.set_color(DARK_GREY), lag_ratio = 0.1, 
            run_time = 4
        )
        self.wait()
        self.play(Write(eqs[1]), run_time = 2)
        self.wait()

        # Gleichung 2 schreiben
        self.play(
            VGroup(*z_comps).animate.set_color(WHITE),
            VGroup(*y_comps).animate.set_color(DARK_GREY), lag_ratio = 0.1, 
            run_time = 4
        )
        self.wait()
        self.play(Write(eqs[2]), run_time = 2)
        self.wait()


        # alles ausfaden
        self.play(
            vec_eq.animate(lag_ratio = 0.1).set_color(DARK_GREY),
            Uncreate(lines, lag_ratio = 0.2), 
            run_time = 2
        )

        self.eqs = eqs

    def what_kind_of_lgs(self):
        eqs = self.eqs 

        brace = BraceBetweenPoints(eqs.get_corner(UR), eqs.get_corner(DR), direction = RIGHT, color = GREY)
        brace_text = brace.get_text("3 ", "Gleichungen\\\\", "2 ", "Unbekannte")
        brace_text.set_color_by_tex_to_color_map({"3": BLUE, "2": YELLOW})

        # 3 Gleichungen
        self.play(Create(brace), run_time = 1.5)
        self.play(Write(brace_text[:2]))
        self.play(LaggedStartMap(Indicate, VGroup(eqs[0][0], eqs[1][0], eqs[2][0]), color = BLUE, lag_ratio = 0.1), run_time = 2)

        # 2 Unbekannte
        rs_list = [eqs[number][index] for number in range(3) for index in [4,7]]
        self.play(Write(brace_text[2:]))
        self.play(
            LaggedStartMap(
                Indicate, 
                VGroup(*rs_list), color = YELLOW, lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait()


        self.play(
            eqs.animate.shift(3*LEFT), 
            *[FadeOut(mob, shift = 3*RIGHT) for mob in [brace, brace_text]], 
            run_time = 2
        )
        self.wait(2)

    def solve_lgs(self):
        eqs = self.eqs

        self.play(Circumscribe(eqs[2][1], color = YELLOW, run_time = 2))

        arrow_kwargs = self.arrow_kwargs = {"color": TEAL, "buff": 0, "rectangular_stem_width": 0.04, "tip_width_to_length_ratio": 0.6}
        eq_arrow = self.eq_arrow = Arrow(ORIGIN, 0.75*RIGHT, **arrow_kwargs)\
            .next_to(eqs[2], RIGHT)

        # 3te Gleichung nach r umstellen
        self.play(GrowArrow(eq_arrow), run_time = 2)
        self.wait()

        eq_rs = MathTex("-2s", "=", "r").next_to(eq_arrow, RIGHT)
        sur_rect = SurroundingRectangle(eq_rs)
        self.play(Write(eq_rs))
        self.wait(0.5)
        self.play(Create(sur_rect), run_time = 2)
        self.wait()

        sur_rect2 = SurroundingRectangle(eqs[1][4])
        self.play(ReplacementTransform(sur_rect.copy(), sur_rect2), run_time = 3)
        self.wait()


        # s aus 2ter Gleichung berechnen
        eq_arrow2 = eq_arrow.copy().next_to(eqs[1], RIGHT)
        self.play(GrowArrow(eq_arrow2), run_time = 2)
        self.wait()

        eq_s1 = MathTex("1", "=", "-2", "s", "+", "s").next_to(eq_arrow2, RIGHT)
        eq_s2 = MathTex("1", "=", "-", "s").move_to(eq_s1, aligned_edge=LEFT)
        eq_s3 = MathTex("-", "1", "=", "s").move_to(eq_s2, aligned_edge=RIGHT)

        self.play(Write(eq_s1), run_time = 1.5)
        self.play(FadeOut(VGroup(sur_rect, sur_rect2), lag_ratio = 0.25), run_time = 2)
        self.wait()

        self.play(Transform(eq_s1, eq_s2))
        self.wait()
        self.play(Transform(eq_s1, eq_s3))
        final_rect_s = SurroundingRectangle(eq_s1, color = x_color)
        self.play(Create(final_rect_s))
        self.wait(2)


        # r aus rs Gleichung bestimmen
        eq_r1 = MathTex("-2", "\\cdot", "(", "-", "1", ")", "=", "r").next_to(eq_rs, RIGHT, buff = 1.5)
        eq_r2 = MathTex("2", "=", "r").move_to(eq_r1)

        arc1 = ArcBetweenPoints(final_rect_s.get_right() + 0.2*RIGHT, eq_r1.get_top() + 0.2*UP, angle = -TAU/6)
        arc2 = ArcBetweenPoints(eq_rs.get_right() + 0.2*RIGHT, eq_r1.get_top() + 0.2*UP, angle = -TAU/6)

        self.play(
            LaggedStartMap(Create, VGroup(arc1, arc2), lag_ratio = 0.1), run_time = 2
        )
        self.wait(0.5)
        self.play(Write(eq_r1))
        self.wait()

        self.play(Transform(eq_r1, eq_r2))
        final_rect_r = SurroundingRectangle(eq_r1, color = y_color)
        self.play(Create(final_rect_r))
        self.wait(3)

    def sample(self):
        eqs = self.eqs

        rect_23 = SurroundingRectangle(eqs[1:], color = BLUE)
        rect_1 = SurroundingRectangle(eqs[0], color = BLUE)

        self.play(Create(rect_23), run_time = 2)
        self.wait()

        self.play(ReplacementTransform(rect_23, rect_1), run_time = 1.5)
        self.wait()

        eq_arrow = Arrow(ORIGIN, 0.75*RIGHT, **self.arrow_kwargs)\
            .next_to(eqs[0], RIGHT)

        self.play(
            FadeOut(rect_1),
            GrowArrow(eq_arrow),
            run_time = 1.5
        )
        self.wait()


        eq1 = MathTex("3", "=", "2", "\\cdot", "2", "+", "(", "-", "1", ")")\
            .next_to(eq_arrow, RIGHT)

        self.play(ShowIncreasingSubsets(eq1), rate_func = linear, run_time = 3)
        self.wait(3)



    # functions
    def get_three_equations(self):
        #                    0         1                       2             3              4    5             6              7
        eq1 = MathTex("\\text{I:}",   str(self.vec_l_num[0]), "=", str(self.vec_a_num[0]), "r", "+", str(self.vec_b_num[0]), "s")
        eq2 = MathTex("\\text{II:}",  str(self.vec_l_num[1]), "=", str(self.vec_a_num[1]), "r", "+", str(self.vec_b_num[1]), "s")
        eq3 = MathTex("\\text{III:}", str(self.vec_l_num[2]), "=", str(self.vec_a_num[2]), "r", "+", str(self.vec_b_num[2]), "s")

        # Gleichungen untereinander
        eqs = VGroup(eq1, eq2, eq3)\
            .arrange_submobjects(DOWN, buff = self.eq_buff)

        # Abstand zwischen I und Gleichung bei eq1 festlegen
        eq1[1:].next_to(eq1[0], RIGHT, buff = 0.75)

        # andere Gleichungen an Gleichung 1 ausrichten
        for index in range(len(eq1)):
            for eq in (eq2, eq3):
                eq[index].align_to(eq1[index], RIGHT)

        # 1 auf rhs der Gleichungen schwarz färben und durchsichtig
        for eq_part in (eq1[6], eq2[3], eq2[6], eq3[3]):
            eq_part.set_color(BLACK).set_fill(opacity = 0)

        return eqs

    def get_vector_equation(self, scalar_1_name = "r", scalar_2_name = "s"):
        mat_a = Matrix([[self.vec_a_num[0]], [self.vec_a_num[1]], [self.vec_a_num[2]]], **self.matrix_kwargs)
        mat_b = Matrix([[self.vec_b_num[0]], [self.vec_b_num[1]], [self.vec_b_num[2]]], **self.matrix_kwargs)
        mat_c = Matrix([[self.vec_l_num[0]], [self.vec_l_num[1]], [self.vec_l_num[2]]], **self.matrix_kwargs)

        equals = MathTex("=")
        scalar_a = MathTex(scalar_1_name)
        cdot1 = MathTex("\\cdot")
        plus = MathTex("+")
        scalar_b = MathTex(scalar_2_name)
        cdot2 = MathTex("\\cdot")

        eqs = VGroup(mat_c, equals, scalar_a, cdot1, mat_a, plus, scalar_b, cdot2, mat_b)\
            .arrange_submobjects(RIGHT)

        return eqs


class ShowLinearCombinationIn3D(ThreeDScene):
    def construct(self):
        vec_a_num = self.vec_a_num = [2,1,1]
        vec_b_num = self.vec_b_num = [1,1,2]
        vec_l_num = self.vec_l_num = [2*a - b for a,b in zip(vec_a_num, vec_b_num)]

        axes = self.axes = ThreeDAxes()
        axes.add_coordinates()
        self.origin = axes.coords_to_point(0,0,0)

        self.cone_height, self.cone_radius = 0.5, 0.15
        self.cone_kwargs = {"cone_height": self.cone_height, "base_radius": self.cone_radius}

        self.draw_axes()
        self.draw_vecs()
        self.combine_scaled_vectors()
        self.draw_linear_combination()
        self.draw_parameter_plane()
        self.varying_parameters_rs()
        # self.draw_plane()
        # self.draw_plane_rect()
        self.no_complanar_vector()


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
        self.add(self.axes, labels_axes)
        self.wait()

        self.move_camera(phi = 70*DEGREES, theta = -30*DEGREES, run_time = 3)
        self.wait()

    def draw_vecs(self):
        axes, cone_kwargs = self.axes, self.cone_kwargs

        vec_a = Arrow3D(start = self.origin, end = axes.coords_to_point(*self.vec_a_num), **cone_kwargs, color = vec_a_color)
        vec_b = Arrow3D(start = self.origin, end = axes.coords_to_point(*self.vec_b_num), **cone_kwargs, color = vec_b_color)

        comp_a = self.get_component_lines(self.vec_a_num, line_class = DashedLine, color = RED_E)
        comp_b = self.get_component_lines(self.vec_b_num, line_class = DashedLine, color = YELLOW_E)

        for comp, vec in zip([comp_a, comp_b], [vec_a, vec_b]):
            self.play(Create(comp), lag_ratio = 0.15, run_time = 2)
            self.play(
                Create(vec),
                FadeOut(comp, rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 2.5
            )
            self.wait(0.5)

        for vec in vec_a, vec_b:
            vec.save_state()
        self.wait()

        self.vec_a, self.vec_b = vec_a, vec_b

    def combine_scaled_vectors(self):
        axes, cone_kwargs = self.axes, self.cone_kwargs

        vec_a2 = Arrow3D(start = self.origin, end = axes.c2p(4,2,2), **cone_kwargs, color = vec_a_color)
        vec_b2 = Arrow3D(start = axes.c2p(4,2,2), end = axes.c2p(5,3,4), **cone_kwargs, color = vec_b_color)
        vec_b3 = Arrow3D(start = axes.c2p(4,2,2), end = axes.c2p(3,1,0), **cone_kwargs, color = vec_b_color)

        rt = 2.5
        self.play(Transform(self.vec_a, vec_a2), run_time = rt)
        self.wait()

        self.play(Transform(self.vec_b, vec_b2), run_time = rt)
        self.wait()

        self.play(Transform(self.vec_b, vec_b3), run_time = rt)
        self.wait()

    def draw_linear_combination(self):
        vec_l = self.vec_l = Arrow3D(start = self.origin, end = self.axes.coords_to_point(*self.vec_l_num), **self.cone_kwargs, color = vec_c_color)
        comp_l = self.get_component_lines(self.vec_l_num, line_class = DashedLine, color = BLUE_E)

        self.play(Create(comp_l), lag_ratio = 0.15, run_time = 2)
        self.play(
            Create(vec_l), 
            FadeOut(comp_l, rate_func = squish_rate_func(smooth, 0.5, 1)),
            run_time = 2.5
        )
        self.wait()




    def draw_parameter_plane(self):
        dots = VGroup()
        for r in np.linspace(-3,3,7):
            for s in np.linspace(-3,3,7):
                dot = Dot3D(
                    point = self.axes.c2p(*[r*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                    radius = 0.04, 
                    color = GREY
                )
                dots.add(dot)

        lines_kwags = {"stroke_width": 2, "color": GREY, "stroke_opacity": 0.2}
        lines_a = VGroup(*[
            Line(
                start = self.axes.c2p(*[-3*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[+3*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for s in np.linspace(-3,3,7)
        ])


        lines_b = VGroup(*[
            Line(
                start = self.axes.c2p(*[r*comp_a - 3*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[r*comp_a + 3*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for r in np.linspace(-3,3,7)
        ])


        self.play(
            FadeIn(dots),
            LaggedStartMap(Create, VGroup(lines_a, lines_b), lag_ratio = 0.15), 
            run_time = 3
        )

        # self.add(lines_a, lines_b, dots)
        # self.add(self.vec_a, self.vec_b)

        big_rect = ThreeDVMobject()
        big_rect.set_points_as_corners([
            lines_a[0].get_start(),
            lines_b[0].get_end(), 
            lines_a[-1].get_end(),
            lines_b[-1].get_start(),
            lines_a[0].get_start()
        ])
        big_rect.set_fill(color = BLUE_E, opacity = 0.3)
        big_rect.set_stroke(width = 0.5, color = GREY)
        self.play(DrawBorderThenFill(big_rect), run_time = 2)
        self.wait()


        self.move_camera(phi = 70*DEGREES, theta = 30*DEGREES, rate_func = there_and_back_with_pause, run_time = 7) # there_and_back_with_pause
        self.wait(2)

    def varying_parameters_rs(self):
        sca_val_a = ValueTracker(2)
        sca_val_b = ValueTracker(-1)

        sca_vec_a, sca_vec_b, sca_vec_l = self.vec_a, self.vec_b, self.vec_l
        vec_a_num, vec_b_num, vec_l_num = self.vec_a_num, self.vec_b_num, self.vec_l_num

        sca_vec_a.add_updater(lambda vec: vec.become(
            Arrow3D(
                start = self.origin, 
                end = self.axes.c2p(*[
                    sca_val_a.get_value() * vec_a_num[0], 
                    sca_val_a.get_value() * vec_a_num[1], 
                    sca_val_a.get_value() * vec_a_num[2]
                ]),
                **self.cone_kwargs, color = vec_a_color
            )
        ))

        sca_vec_b.add_updater(lambda vec: vec.become(
            Arrow3D(
                start = self.axes.c2p(*[
                    sca_val_a.get_value() * vec_a_num[0], 
                    sca_val_a.get_value() * vec_a_num[1], 
                    sca_val_a.get_value() * vec_a_num[2]
                ]),
                end = self.axes.c2p(*[
                    sca_val_a.get_value() * vec_a_num[0] + sca_val_b.get_value() * vec_b_num[0], 
                    sca_val_a.get_value() * vec_a_num[1] + sca_val_b.get_value() * vec_b_num[1], 
                    sca_val_a.get_value() * vec_a_num[2] + sca_val_b.get_value() * vec_b_num[2]
                ]),
                **self.cone_kwargs, color = vec_b_color
            )
        ))

        sca_vec_l.add_updater(lambda vec: vec.become(
            Arrow3D(
                start = self.origin,
                end = self.axes.c2p(*[
                    sca_val_a.get_value() * vec_a_num[0] + sca_val_b.get_value() * vec_b_num[0], 
                    sca_val_a.get_value() * vec_a_num[1] + sca_val_b.get_value() * vec_b_num[1], 
                    sca_val_a.get_value() * vec_a_num[2] + sca_val_b.get_value() * vec_b_num[2]
                ]), 
                **self.cone_kwargs, color = vec_c_color
            )
        ))


        self.begin_ambient_camera_rotation(rate = 0.02)
        self.wait()

        self.a_values = [ 2, -1, -2, -1,  2]
        self.b_values = [-3, -2,  1,  2, -1]

        for a_val, b_val in zip(self.a_values, self.b_values):
            self.play(
                sca_val_a.animate(rate_func = squish_rate_func(smooth, 0, 0.8)).set_value(a_val),
                sca_val_b.animate(rate_func = squish_rate_func(smooth, 0.2, 1)).set_value(b_val),
                run_time = 4
            )
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
        self.wait()

        self.move_camera(phi = 70*DEGREES, theta = 18*DEGREES, rate_func = smooth, run_time = 4)
        self.wait(2)




    def draw_plane(self):

        ebene = ParametricSurface(
            u_min=-1.25, u_max=1.5, v_min=-1.25, v_max=1.5, func = self.plane_func, 
            resolution=16, fill_opacity=0.25, checkerboard_colors=[BLUE_D, BLUE_D], stroke_width = 0.1
        )
        self.add(ebene)
        self.wait(2)

        self.move_camera(phi = 70*DEGREES, theta = 25*DEGREES, run_time = 4) # rate_func = there_and_back_with_pause, 
        self.wait(3)

    def draw_plane_rect(self):
        rect = Rectangle(color = BLUE, height = 7, width = 12)
        rect.set_fill(opacity = 0.25)
        rect.set_stroke(width = 1, opacity = 0.5)
        rect.rotate(angle = 72.4584*DEGREES, axis = RIGHT)
        rect.rotate(angle = 17.55*DEGREES, axis = OUT)

        self.play(DrawBorderThenFill(rect), run_time = 3)
        self.wait()

        dot_end_red = Dot3D(point = self.axes.c2p(4,2,2), color = RED)
        dot_end_yel = Dot3D(point = self.axes.c2p(3,1,0), color = YELLOW)

        self.add(dot_end_red, dot_end_yel)

        dot_inplane = Dot3D(point = self.axes.c2p(2,1.5,2.5), color = RED)
        self.add(dot_inplane)

        self.move_camera(phi = 70*DEGREES, theta = 25*DEGREES, rate_func = smooth, run_time = 5) # there_and_back_with_pause
        self.wait()

    def no_complanar_vector(self):
        axes = self.axes
        self.vec_l.clear_updaters()

        vec_l2 = Arrow3D(start = self.origin, end = axes.coords_to_point(2,-1,2), **self.cone_kwargs, color = BLUE_E)
        comp_l = self.get_component_lines([2,-1,2], line_class = DashedLine, color = BLUE_E)

        self.play(
            Create(vec_l2, run_time = 3),
            Create(comp_l, run_time = 2),
        )
        self.wait(3)


    # functions
    def get_component_lines(self, vec_num, line_class = DashedLine, color = BLUE, **kwargs):
        axes = self.axes

        x_component = line_class(
            axes.c2p(vec_num[0], vec_num[1], 0), 
            axes.c2p(0, vec_num[1], 0), 
            color = color, **kwargs
        )
        y_component = line_class(
            axes.c2p(vec_num[0], vec_num[1], 0), 
            axes.c2p(vec_num[0], 0, 0), 
            color = color, **kwargs
        )
        z_component = line_class(
            axes.c2p(vec_num[0], vec_num[1], 0), 
            axes.c2p(vec_num[0], vec_num[1], vec_num[2]), 
            color = color, **kwargs
        )

        result = VGroup(x_component, y_component, z_component)

        return result

    def plane_func(self, u, v):
        # return np.array([2*u + v, u + v, u + 2*v])
        return np.array([3*u, u + v, 3*v])


class ComplanarityExample(StudentsJob):
    def construct(self):

        self.vec_a_num = [2,1,1]
        self.vec_b_num = [1,1,2]
        self.vec_l_num = [2*a - b for a,b in zip(self.vec_a_num, self.vec_b_num)]

        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6 , "bracket_v_buff": 0.1}
        self.arrow_kwargs = {"stroke_width": 4, "max_tip_length_to_length_ratio": 0.25}


        self.what_students_are_asked_to_do()
        self.remove(self.arrow_a, self.arrow_b)
        self.wait()


        self.vec_l_num = [2,-1,2]
        vec_eq2 = self.get_vector_equation()
        vec_eq2.move_to(self.vec_eq, aligned_edge=RIGHT)

        self.play(FocusOn(self.vec_eq[0], run_time = 1.5))
        self.play(Transform(self.vec_eq, vec_eq2))
        self.wait(3)

        self.play(*[
            Circumscribe(scalar, color = color, run_time = 1.5) 
            for scalar, color in zip([self.vec_eq[2], self.vec_eq[6]], [x_color, y_color])
        ])
        self.play(
            *[GrowArrow(arrow) for arrow in [self.arrow_a, self.arrow_b]], 
            run_time = 3
        )
        self.wait(3)


class NoSolutionForParameters(StudentsJobCalculation):
    def construct(self):
        vec_a_num = self.vec_a_num = [2,  1, 1]
        vec_b_num = self.vec_b_num = [1,  1, 2]
        vec_l_num = self.vec_l_num = [2, -1, 2]

        self.eq_buff = 0.5
        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "v_buff": 0.6 , "bracket_v_buff": 0.1}

        self.vector_equation()
        self.turn_vec_eq_into_lgs()
        self.try_solving_lgs()
        self.try_sample()

    def try_solving_lgs(self):
        eqs = self.eqs

        self.play(eqs.animate.shift(3*LEFT), run_time = 2)
        self.wait()

        arrow_kwargs = self.arrow_kwargs = {"color": TEAL, "buff": 0, "rectangular_stem_width": 0.04, "tip_width_to_length_ratio": 0.6}
        arrow1 = self.arrow1 = Arrow(ORIGIN, 0.75*RIGHT, **arrow_kwargs)\
            .next_to(eqs[0], RIGHT)

        sub_eq_text = MathTex("\\text{I}", "-", "\\text{II}", ":").next_to(arrow1, RIGHT)

        self.play(GrowArrow(arrow1), run_time = 1.5)
        self.wait(0.5)
        self.play(Write(sub_eq_text))
        self.wait()

        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = BLUE)
            for mob in [
                VGroup(eqs[0][1], eqs[1][1]), 
                VGroup(eqs[0][3:5], eqs[1][3:5]),
                VGroup(eqs[0][7:], eqs[1][7:])
            ]
        ])

        eq_r2 = MathTex("3", "=", "r").next_to(sub_eq_text, RIGHT)

        self.play(Create(sur_rects[2]), run_time = 2)
        self.wait(2)

        self.play(Transform(sur_rects[2], sur_rects[0]), run_time = 2)
        self.wait()
        self.play(Write(eq_r2[0]))
        self.wait()
        self.play(
            Write(eq_r2[1], run_time = 1), 
            Transform(sur_rects[2], sur_rects[1], run_time = 2)
        )
        self.wait()


        sur_rect_r = SurroundingRectangle(eq_r2, color = x_color)
        self.play(
            Write(eq_r2[2]), 
            FadeOut(sur_rects[2])
        )
        self.play(Create(sur_rect_r), run_time = 2)
        self.wait(2)


        # Wert für s herausfinden
        arrow2 = arrow1.copy().next_to(eqs[1], RIGHT)

        self.play(Circumscribe(eqs[1][4], time_width = 0.75, color = x_color, run_time = 2))
        self.play(GrowArrow(arrow2), run_time = 2)
        self.wait()

        eq_s1 = MathTex("-1", "=", "3", "+", "s").next_to(arrow2, RIGHT)
        eq_s2 = MathTex("-4", "=", "s").move_to(eq_s1, aligned_edge=LEFT)
        sur_rect_s = SurroundingRectangle(eq_s2, color = y_color)

        self.play(Write(eq_s1), run_time = 2)
        self.wait()

        self.play(Transform(eq_s1, eq_s2))
        self.wait(0.5)
        self.play(Create(sur_rect_s), run_time = 2)
        self.wait(2)

    def try_sample(self):
        eqs = self.eqs

        rect_01 = SurroundingRectangle(eqs[:2], color = BLUE)
        rect_2 = SurroundingRectangle(eqs[2], color = BLUE)

        self.play(Create(rect_01), run_time = 3)
        self.wait() 

        self.play(Transform(rect_01, rect_2), run_time = 2)
        self.wait()


        arrow3 = self.arrow1.copy().next_to(eqs[2], RIGHT)
        sample1 = MathTex("2", "=", "3", "+", "2", "\\cdot", "(", "-4", ")")\
            .next_to(arrow3, RIGHT)\
            .set_color_by_tex_to_color_map({"3": x_color, "-4": y_color})

        sample2 = MathTex("2", "=", "3", "-", "8")\
            .move_to(sample1, aligned_edge=LEFT)

        sample3 = MathTex("2", "=", "-5")\
            .move_to(sample1, aligned_edge=LEFT)

        self.play(GrowArrow(arrow3), run_time = 2)
        self.wait()

        self.play(ShowIncreasingSubsets(sample1, rate_func = linear), run_time = 3)
        self.wait()

        self.play(Transform(sample1, sample2))
        self.wait()

        self.play(Transform(sample1, sample3))
        self.wait()

        cross = Cross(sample1, stroke_width = 3, color = RED)
        self.play(Create(cross), lag_ratio = 0.25, run_time = 2)
        self.wait()


        # Vector equation hervorheben
        self.play(self.vec_eq.animate(lag_ratio = 0.25).set_color(WHITE), run_time = 3)
        self.wait()

        not_equal = MathTex("\\neq")\
            .set_color(RED)\
            .move_to(self.vec_eq[1])

        self.play(Transform(self.vec_eq[1], not_equal))
        self.wait(3)





class Thumbnail2(Scene):
    def construct(self):
        title = Tex("Linearkombinationen")\
            .set_color_by_gradient(vec_a_color, vec_c_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 1)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1.5)

        self.add(title)


        math = MathTex("\\vec{c}", "=", "r", "\\cdot", "\\vec{a}", "+", "s", "\\cdot", "\\vec{b}")\
            .scale(1.5)\
            .set_color_by_tex_to_color_map({"\\vec{c}": vec_c_color, "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})

        ask = Tex("?")\
            .scale(2.5)\
            .set_color(GREEN)\
            .set_fill(opacity = 0.25)\
            .set_stroke(width = 2)\
            .next_to(math, RIGHT, buff = 0.5)


        self.add(math, ask)






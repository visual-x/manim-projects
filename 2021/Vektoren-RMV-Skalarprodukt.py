from manim import *


vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE


class ProjectionVectorScene(VectorScene):
    def construct(self):
        pass

    def get_plane(self, **kwargs):
        plane = NumberPlane(**kwargs)
        origin = plane.coords_to_point(0,0)

        self.plane, self.origin = plane, origin

        return plane

    def get_vectors_ab(self):
        xval = ValueTracker(self.x_value)
        yval = ValueTracker(self.y_value)
        zval = ValueTracker(self.z_value)

        veca = self.get_vector(self.vector_stat, color = vec_a_color)
        vecb = self.get_vector([xval.get_value(), yval.get_value(), zval.get_value()], color = vec_b_color)

        self.veca, self.vecb = veca, vecb
        self.xval, self.yval, self.zval = xval, yval, zval

        return veca, vecb


    # functions
    def get_pro_vector(self, v1, **kwargs):
        vec1 = v1.get_vector()

        return Arrow(
            np.array([0,0,0]),
            np.dot(np.array([self.xval.get_value(), self.yval.get_value(), self.zval.get_value()]), vec1)/np.linalg.norm(vec1)**2 * vec1, 
            buff = 0, 
            **kwargs
        )

    def get_pro_line(self, v1, **kwargs):
        vec1 = v1.get_vector()
        start = np.array([self.xval.get_value(), self.yval.get_value(), self.zval.get_value()])
        end = np.dot(np.array([self.xval.get_value(), self.yval.get_value(), self.zval.get_value()]), vec1)/np.linalg.norm(vec1)**2 * vec1

        return DashedLine(start, end, **kwargs)

    def get_pro_vector_rotate(self, v1, **kwargs):
        vec1 = np.array([self.xval.get_value(), self.yval.get_value(), 0])
        vec2 = v1.get_vector()

        if angle_between_vectors(vec1, vec2) < PI/2:
            normal_vec = np.array([vec2[1], -vec2[0], 0])
        else:
            normal_vec = np.array([-vec2[1], vec2[0], 0])

        start = self.origin
        end = np.dot(vec1, vec2)/np.linalg.norm(vec2)**2 * normal_vec

        return Arrow(start, end, buff = 0, **kwargs)

    def get_dot_prod_rectangle(self, v1, **kwargs):

        vec1 = v1.get_vector()
        normal_vec = np.array([vec1[1], -vec1[0], 0])

        rect = Rectangle(
            width = np.linalg.norm(vec1), 
            height = np.linalg.norm(np.dot(np.array([self.xval.get_value(), self.yval.get_value(), 0]), vec1)/np.linalg.norm(vec1)**2 * normal_vec), 
            stroke_width = 1
        )
        rect.set_fill(**kwargs)
        rect.next_to(self.origin, RIGHT, buff = 0, aligned_edge = UL)
        rect.rotate(v1.get_angle(), about_point = self.origin)

        return rect


class Calculations(Scene):

    def construct(self):
        pass


    def group_vecs_with_symbol(self, mat_a, mat_b, type = "dot"):
        if type is "dot":
            mult = MathTex("\\cdot").set_color(self.dot_color)
        elif type is "bullet":
            mult = MathTex("\\bullet").set_color(self.dot_color)
        elif type is "cdot":
            mult = MathTex("\\cdot").set_color(self.dot_color)
        else:
            mult = MathTex("\\times").set_color(self.cross_color)

        group = VGroup(mat_a, mult, mat_b)
        group.arrange_submobjects(RIGHT)

        return group

    def get_dotproduct_path(self, vec_group, dimension = 3, color = ORANGE, stroke_width = 5):
        path = VMobject()
        if dimension == 3:
            path.set_points_smoothly([
                vec_group[0][0][0].get_center(),     # x Kompenente vec1 und vec2
                vec_group[2][0][0].get_center(),
                vec_group[0][0][1].get_center(),     # y Kompenente vec1 und vec2
                vec_group[2][0][1].get_center(),
                vec_group[0][0][2].get_center(),     # z Kompenente vec1 und vec2
                vec_group[2][0][2].get_center(),
            ])
        elif dimension == 2:
            path.set_points_smoothly([
                vec_group[0][0][0].get_center(),     # x Kompenente vec1 und vec2
                vec_group[2][0][0].get_center(),
                vec_group[0][0][1].get_center(),     # y Kompenente vec1 und vec2
                vec_group[2][0][1].get_center(),
            ])

        path.set_color(color = color)
        path.set_stroke(width = stroke_width)

        return path

    def get_dotproduct_surrects(self, vec_group, color = ORANGE):
        rects = VGroup(*[
            SurroundingRectangle(matrix_element).set_color(color = color)
            for matrix_element in [
                vec_group[0][0][0],     # x Kompenente vec1 und vec2
                vec_group[2][0][0],
                vec_group[0][0][1],     # y Kompenente vec1 und vec2
                vec_group[2][0][1],
                vec_group[0][0][2],     # z Kompenente vec1 und vec2
                vec_group[2][0][2],
            ]
        ])
        return rects

    def get_crossproduct_path_xyz(self, vec_group, color = ORANGE, stroke_width = 5):
        path_x, path_y, path_z = VMobject(), VMobject(), VMobject()

        # vec_group[0] --> erster Vektor, maths[1][1] Mal zeichen, maths[1][2] zweiter Vektor
        # vec_group[i][0] --> Vektoreinträge
        # vec_group[i][0][j] --> x,y,z Komponente

        path_x.set_points_smoothly([
            vec_group[0][0][1].get_center(),     # y Komponente vec1
            vec_group[2][0][2].get_center(),     # z Komponente vec2
            vec_group[0][0][2].get_center(),     # y Komponente vec1
            vec_group[2][0][1].get_center(),     # z Komponente vec2
        ])

        path_y.set_points_smoothly([
            vec_group[0][0][2].get_center(),     # z Komponente vec1
            vec_group[2][0][0].get_center(),     # x Komponente vec2
            vec_group[0][0][0].get_center(),     # x Komponente vec1
            vec_group[2][0][2].get_center(),     # z Komponente vec2
        ])

        path_z.set_points_smoothly([
            vec_group[0][0][0].get_center(),     # x Komponente vec1
            vec_group[2][0][1].get_center(),     # y Komponente vec2
            vec_group[0][0][1].get_center(),     # y Komponente vec1
            vec_group[2][0][0].get_center(),     # x Komponente vec2
        ])

        for path in path_x, path_y, path_z:
            path.set_color(ORANGE).set_stroke(width = 7)

        return path_x, path_y, path_z

    # ToDo: elemente im Skalarprodukt anordnen & Klammern für negative Zahlen
    def get_dotproduct(self, vec_group):
        # vec_group_elements = VGroup(*[
        #     TexMobject(element.get_tex_string())
        #     for element in [
        #         vec_group[0][0][0],     # x Kompenente vec1 und vec2
        #         vec_group[2][0][0],
        #         vec_group[0][0][1],     # y Kompenente vec1 und vec2
        #         vec_group[2][0][1],
        #         vec_group[0][0][2],     # z Kompenente vec1 und vec2
        #         vec_group[2][0][2],
        #     ]
        # ])
        dot_product = MathTex(
            vec_group[0][0][0].get_tex_string(),     # x Kompenente vec1 und vec2
            "\\cdot",
            vec_group[2][0][0].get_tex_string(),
            "+",
            vec_group[0][0][1].get_tex_string(),     # y Kompenente vec1 und vec2
            "\\cdot",
            vec_group[2][0][1].get_tex_string(),
            "+",
            vec_group[0][0][2].get_tex_string(),     # z Kompenente vec1 und vec2
            "\\cdot",
            vec_group[2][0][2].get_tex_string()
        )
        return dot_product


# Scenes Einfürhung Skalarprodukt DONE
class KnownVectorOperations(Scene):
    def construct(self):
        self.dot_color = GREEN
        self.cross_color = BLUE
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
        }


        self.new_intro()
        self.scalar_multiplication()
        self.vector_addition()
        self.what_its_not()


    def new_intro(self):
        plane = NumberPlane(
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 2, "stroke_opacity": 0.6}, 
        )
        plane.add_coordinates()
        self.origin = plane.c2p(0,0)

        vec_a_num = self.vec_a_num = [1,2]
        vec_b_num = self.vec_b_num = [-3,1]
        vec_sum_num = self.vec_sum_num = [a + b for a,b in zip(vec_a_num, vec_b_num)]

        vec_a = plane.get_vector(vec_a_num, buff = 0, color = vec_a_color)
        vec_b = plane.get_vector(vec_b_num, buff = 0, color = vec_b_color)

        for vec in vec_a, vec_b:
            vec.save_state()

        mats = VGroup(*[
            Matrix(matrix, **self.mat_kwargs, include_background_rectangle = True).next_to(vec.get_end(), direction = direc)
            for matrix, vec, direc in zip(
                [[[str(vec_a_num[0])], [str(vec_a_num[1])]], [[str(vec_b_num[0])], [str(vec_b_num[1])]]], 
                [vec_a, vec_b], 
                [RIGHT, LEFT]
            )
        ])

        # NumberPlane, Vektoren und Matrizen
        self.play(Create(plane), lag_ratio = 0.1, run_time = 2)
        self.play(
            LaggedStart(*[GrowArrow(vec) for vec in [vec_a, vec_b]]),
            *[FadeIn(mat[0]) for mat in [mats[0], mats[1]]],            # bg rect der Matrizen
            *[FadeIn(mat[2:]) for mat in [mats[0], mats[1]]],           # Klammern der Matrizen
            run_time = 2
        )

        xy_lines = VGroup(*[
            self.get_xy_lines(vec_num) for vec_num in [vec_a_num, vec_b_num]
        ])

        self.play(
            AnimationGroup(
                *[ShowPassingFlash(comp, time_width = 0.75, lag_ratio = 0.2) for comp in xy_lines[0]],
                *[Create(mats[0][1][comp]) for comp in [0, 1]],
                lag_ratio = 0.5
            ), 
            run_time = 1.5
        )
        self.play(
            AnimationGroup(
                *[ShowPassingFlash(comp, time_width = 0.75, lag_ratio = 0.2) for comp in xy_lines[1]],
                *[Create(mats[1][1][comp]) for comp in [0, 1]], 
                lag_ratio = 0.5
            ),
            run_time = 1.5
        )


        # Vektoren zurück zum Urpsrung
        big_rect = Rectangle(width = config["frame_width"], height = config["frame_height"]/2 - 1.5)
        big_rect.set_stroke(width = 0, color = BLACK)
        big_rect.set_fill(color = BLACK, opacity = 0.85)
        big_rect.to_edge(DOWN, buff = 0)

        self.play(
            DrawBorderThenFill(big_rect, run_time = 2),
            ApplyMethod(mats[0].move_to, 2.5*RIGHT + 2.5*DOWN, run_time = 3),
            ApplyMethod(mats[1].move_to, 4.5*LEFT + 2.5*DOWN, run_time = 3),
        )
        self.wait()


        self.plane, self.mats = plane, mats
        self.vec_a, self.vec_b = vec_a, vec_b

    def scalar_multiplication(self):
        plane, mats = self.plane, self.mats
        vec_a, vec_b = self.vec_a, self.vec_b

        scalars = VGroup(*[
            MathTex(*tex).set_color(scalar_color).next_to(mat, LEFT)
            for tex, scalar_color, mat in zip(
                [["-", "\\frac{1}{2}\\", "\\cdot"], ["2\\", "\\cdot"]], 
                [vec_a_color, vec_b_color], 
                [mats[0], mats[1]]
            )
        ])

        vec_scalars = VGroup(*[
            plane.get_vector(coords = xycoords, buff = 0, color = scalar_color)
            for xycoords, scalar_color in zip(
                [[-0.5,-1], [-6,2]], [vec_a_color, vec_b_color]
            )
        ])

        equals = VGroup(*[
            MathTex("=").next_to(mat, RIGHT)
            for mat in [mats[0], mats[1]]
        ])

        results = VGroup(*[
            Matrix(mat_new, element_alignment_corner = direc,**self.mat_kwargs).next_to(equal, RIGHT)
            for mat_new, equal, direc in zip(
                [[["-0.5"], ["-1"]], [["-6"], ["2"]]], [equals[0], equals[1]], [DL, DR]
            )
        ])

        components = VGroup(*[
            self.get_xy_lines(vec)
            for vec in [self.vec_a_num, self.vec_b_num]
        ])

        results_scalar = VGroup(*[
            Matrix(mat_new, element_alignment_corner = direc, **self.mat_kwargs).next_to(equal, RIGHT)
            for mat_new, equal,direc in zip(
                [[["-0.5\\cdot 1"], ["-0.5\\cdot 2"]], [["2\\cdot (-3)"], ["2\\cdot 1"]]], 
                [equals[0], equals[1]], 
                [DL, DL]
            )
        ])

        results_scalar[0][0][0][0][:5].set_color(vec_a_color)
        results_scalar[0][0][1][0][:5].set_color(vec_a_color)

        results_scalar[1][0][0][0][:2].set_color(vec_b_color)
        results_scalar[1][0][1][0][:2].set_color(vec_b_color)


        # Ohne Schleife
        self.play(*[Write(scalar) for scalar in scalars])
        self.wait()

        vecs_original = [vec_a, vec_b]
        self.play(
            AnimationGroup(
                Transform(vecs_original[0], vec_scalars[0]),
                Transform(vecs_original[1], vec_scalars[1]),
                lag_ratio = 0.5
            ), 
            run_time = 3
        )

        self.play(Write(equals))
        self.play(Create(results), run_time = 2)
        self.wait()

        self.play(
            AnimationGroup(
                Transform(results[0], results_scalar[0]),
                Transform(results[1], results_scalar[1]),
                lag_ratio = 0.5
            ), 
            run_time = 1.5
        )
        self.wait()

        # Vektoren restoren, alles andere ausfaden
        self.play(
            *[Restore(vec) for vec in [vec_a, vec_b]],
            LaggedStart(*[FadeOut(mob, shift = DOWN) for mob in [*scalars, *equals, *results]]),
            run_time = 3
        )
        self.wait()

    def vector_addition(self):
        plane, mats = self.plane, self.mats
        vec_a, vec_b = self.vec_a, self.vec_b

        # Addition der Vektoren schreiben
        plus = MathTex("+")\
            .move_to(2.5*DOWN)\
            .set_color(vec_c_color)

        for mat, direc in zip(mats, [RIGHT, LEFT]):
            mat.generate_target()
            mat.target.next_to(plus, direction = direc)

        self.play(
            FadeIn(plus, shift = UP), 
            *[MoveToTarget(mat) for mat in mats], 
            run_time = 2
        )
        self.wait()

        # graphische Lösung
        vec_res = plane.get_vector(self.vec_sum_num, buff = 0, color = vec_c_color)
        component = self.get_xy_lines(self.vec_sum_num)
        self.play(
            ApplyMethod(vec_a.shift, 3*LEFT + 1*UP), 
            run_time = 3
        )
        self.play(GrowArrow(vec_res), run_time = 2)
        self.wait()

        # rechnerische Lösungen

        equals = MathTex("=").next_to(mats[0], RIGHT)
        mat_res = Matrix([["-2"], ["3"]], **self.mat_kwargs).next_to(equals, RIGHT)

        mat_add = Matrix([["-3 + 1"], ["1 + 2"]], element_alignment_corner = RIGHT, **self.mat_kwargs).next_to(equals, RIGHT)
        mat_add[0][0][0][2].set_color(vec_c_color)
        mat_add[0][1][0][1].set_color(vec_c_color)


        self.play(Write(equals))
        self.play(Write(mat_res), run_time = 1.5)
        self.play(LaggedStart(*[ShowPassingFlash(comp, time_width = 0.75) for comp in [*component]]), run_time = 3)
        self.wait()

        self.play(Transform(mat_res, mat_add))
        self.wait()

        # restoren und alles wegnnehmen 
        self.play(
            *[Restore(vec) for vec in [vec_a, vec_b]],
            LaggedStart(*[FadeOut(mob, shift = UP) for mob in [vec_res, equals, mat_res]]),
            run_time = 3
        )
        self.wait()

        # Vektormultiplikation
        text = Text("Vektormultiplikation")\
            .set_color_by_gradient(GREEN, GREEN_A, BLUE_A, BLUE)\
            .set_fill(color = BLACK, opacity = 0.5)\
            .set_stroke(width = 2)\
            .set(width = config["frame_width"] - 1)\
            .to_edge(UP, buff = 0.25)

        mult = MathTex("\\bullet")\
            .move_to(plus)\
            .set_color(plus.get_color())

        self.play(ShowIncreasingSubsets(VGroup(*text)), run_time = 3)
        self.play(FocusOn(plus), run_time = 1.5)
        self.play(ReplacementTransform(plus, mult))
        self.wait()

        self.text = text

    def what_its_not(self):
        plane, mats = self.plane, self.mats

        equals = MathTex("=").next_to(mats[0], RIGHT)
        mat_mult = Matrix([["-3 \\bullet 1"], ["1 \\bullet 2"]], **self.mat_kwargs)\
            .next_to(equals, RIGHT)
        mat_mult[0][0][0][2].set_color(vec_c_color)
        mat_mult[0][1][0][1].set_color(vec_c_color)

        self.play(Write(equals))
        self.wait()

        self.play(Write(mat_mult), run_time = 1.5)
        self.wait()

        self.play(Circumscribe(
            VGroup(mat_mult[0][0][0][2], mat_mult[0][1][0][1]), 
            color = YELLOW, 
            run_time = 4
        ))

        cross = Cross(mat_mult)
        self.play(Create(cross))
        self.wait(3)


        # prepare VisualX Intro
        rect = RoundedRectangle(width = 9, height = 3.5, stroke_width = 1)
        rect.set_fill(color = BLACK, opacity = 0.85)
        rect.move_to(0.5*UP)

        self.play(
            DrawBorderThenFill(rect, run_time = 3), 
            FadeOut(VGroup(equals, mat_mult, cross), shift = DOWN, run_time = 1)
        )
        self.wait(3)


        # alles ausfaden
        mobs = Group(*self.mobjects[:-8], *self.mobjects[-7:])
        self.play(ShrinkToCenter(mobs), run_time = 1.5)
        self.wait()

    # functions
    def get_xy_lines(self, vec_num):
        x_line = Line(self.origin, vec_num[0] * RIGHT, color = x_color)
        y_line = Line(x_line.get_end(), x_line.get_end() + vec_num[1] * UP, color = y_color)

        result = VGroup(x_line, y_line)
        return result


class ScalarVsCross(Calculations):
    def construct(self):
        self.dot_color = GREEN
        self.cross_color = BLUE
        self.vec_a_color = YELLOW
        self.vec_b_color = RED
        self.mat_kwargs = {"v_buff": 0.6, "bracket_v_buff": 0.1, "left_bracket": "(", "right_bracket": ")"}

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}

        self.multiply_2_vectors()
        self.clac_animation_and_results()

    def multiply_2_vectors(self):
        title = Text("Vektormultiplikation")\
            .set_color_by_gradient(GREEN, GREEN_A, BLUE_A, BLUE)\
            .set_fill(color = BLACK, opacity = 0.5)\
            .set_stroke(width = 2)\
            .set(width = config["frame_width"] - 1)\
            .to_edge(UP, buff = 0.25)
        self.add(title)


        mat_a = Matrix([["1"], ["2"], ["-1"]], **self.mat_kwargs)
        mat_b = Matrix([["3"], ["0"], ["2"]], **self.mat_kwargs)
        mat_a2 = mat_a.copy()
        mat_b2 = mat_b.copy()
        mat_a3 = mat_a.copy()
        mat_b3 = mat_b.copy()

        # Skalarprodukt, Kreuzprodukt
        maths = VGroup(*[
            self.group_vecs_with_symbol(mat1, mat2, doc)
            for mat1, mat2, doc in zip([mat_a, mat_a2], [mat_b, mat_b2], ["dot", "cross"])
        ])
        maths.arrange_submobjects(RIGHT, buff = 3)

        # Vektorenprodukt mit bullet anzeigen
        math_bullet1 = self.group_vecs_with_symbol(mat_a3, mat_b3, "bullet")
        math_bullet2 = math_bullet1.copy()
        self.play(
            ShowIncreasingSubsets(VGroup(
                *math_bullet1[0], *math_bullet1[1], *math_bullet1[2]
            )), 
            run_time = 3
        )
        self.add(math_bullet2)
        self.wait()

        self.play(
            ApplyMethod(math_bullet1.move_to, maths[0], path_arc = PI),
            ApplyMethod(math_bullet2.move_to, maths[1], path_arc = PI),
            run_time = 3
        )
        self.wait()


        # Ergebnisse --> Zahl oder Vektor
        results_text = VGroup(*[
            Tex(text).next_to(product, DOWN, buff = 1.5).set_color(text_color)
            for text, product, text_color in zip(["reelle Zahl", "Vektor"], [maths[0], maths[1]], [self.dot_color, self.cross_color])
        ])

        self.play(Write(results_text[0]))
        self.wait()
        self.play(Write(results_text[1]))
        self.wait()


        # Namen
        names = VGroup(*[
            Tex(name).next_to(product, UP, buff = 0.5)
            for name, product in zip(["Skalarprodukt", "Kreuzprodukt"], [maths[0], maths[1]])
        ])
        names[0][0][:6].set_color(self.dot_color)
        names[1][0][:5].set_color(self.cross_color)

        # Namen beider Operationen
        self.play(ShowIncreasingSubsets(VGroup(*names[0][0])), run_time = 2)
        self.wait()

        self.play(ShowIncreasingSubsets(VGroup(*names[1][0])), run_time = 2)
        self.wait()


        # Rechnensymbole transformieren
        self.play(FocusOn(math_bullet1), run_time = 1)
        self.play(ReplacementTransform(math_bullet1, maths[0]))
        self.wait()
        self.play(FocusOn(math_bullet2), run_time = 1)
        self.play(ReplacementTransform(math_bullet2, maths[1]))
        self.wait()

        self.names, self.results_text, self.maths, self.title = names, results_text, maths, title

    def clac_animation_and_results(self):
        results_text = self.results_text
        maths, names = self.maths, self.names

        result_prod = MathTex("1").move_to(results_text[0])
        result_cross = Matrix([["4"], ["-5"], ["-6"]], **self.mat_kwargs).move_to(results_text[1])
        results_math = VGroup(result_prod, result_cross)


        path_dot = VMobject()
        path_dot.set_points_smoothly([
            maths[0][0][0][0].get_center(),     # x Kompenente vec1 und vec2
            maths[0][2][0][0].get_center(),
            maths[0][0][0][1].get_center(),     # y Kompenente vec1 und vec2
            maths[0][2][0][1].get_center(),
            maths[0][0][0][2].get_center(),     # z Kompenente vec1 und vec2
            maths[0][2][0][2].get_center(),
        ])
        path_dot.set_color(ORANGE).set_stroke(width = 5)

        self.play(ShowPassingFlash(path_dot), rate_func = linear, run_time = 6)
        self.play(results_text[0].animate.next_to(results_math[0], LEFT, buff = 0.5))
        self.play(FadeIn(results_math[0], shift = 0.5*UP))
        self.wait(0.5)


        # Text Vektor verschieben und Klammern vom Vektor schreiben
        self.play(results_text[1].animate.next_to(results_math[1], buff =0.5))
        self.play(
            Write(results_math[1][1]),
            Write(results_math[1][2]),
        )
        self.wait()

        # Kreuzprodukt animation
        path_cross1, path_cross2, path_cross3 = self.get_crossproduct_path_xyz(maths[1])

        self.play(ShowPassingFlash(path_cross1), rate_func = linear, run_time = 1)
        self.play(
            Write(results_math[1][0][0], run_time = 0.75)
        )

        self.play(ShowPassingFlash(path_cross2), rate_func = linear, run_time = 1)
        self.play(Write(results_math[1][0][1]), run_time = 0.75)


        self.play(ShowPassingFlash(path_cross3), rate_func = linear, run_time = 1)
        self.play(Write(results_math[1][0][2]), run_time = 0.75)
        self.wait()

        dot_pic = self.get_dotprod_pic().next_to(result_prod, RIGHT)
        cross_pic = self.get_crossprod_pic().next_to(result_cross, LEFT)

        pics = VGroup(dot_pic, cross_pic)

        self.play(
            LaggedStartMap(
                Create, VGroup(*pics), lag_ratio = 0.15
            ), 
            run_time = 3
        )
        self.wait()


        # Alles ausfaden
        # self.play(
        #     FadeOut(self.title, shift = 5*LEFT),
        #     FadeOut(VGroup(maths[1], names[1]), shift = 4*RIGHT),
        #     FadeOut(VGroup(results_math[1], results_text[1]), shift = 4*DOWN),
        #     FadeOut(VGroup(results_math[0], results_text[0]), shift = 5*LEFT),
        #     FadeOut(pics, shift = 3*DOWN),
        #     run_time = 3
        # )
        # self.wait()

    # functions 

    def get_dotprod_pic(self):
        vec_a_num = [1.5, 0, 0]
        vec_b_num = [0.8, 1, 0]
        vec_c_num = [0.8, 0, 0]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = GREEN, **self.arrow_kwargs)

        line = DashedLine(vec_b.get_end(), vec_c.get_end(), color = GREY)

        pic = VGroup(line, vec_a, vec_b, vec_c)

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
        return pic


class Definition(Calculations):
    def construct(self):
        self.dot_color = GREEN
        self.cross_color = BLUE 
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.vec_a_num = [1,2,-1]
        self.vec_b_num = [3,0, 2]

        #                     0        1        2        3        4
        self.result = MathTex("1\\cdot 3", "+", "2\\cdot 0", "+", "(-1)\\cdot 2")


        self.setup_old_scene()
        self.component_combination()
        self.result_component_mult()
        self.calculation1()
        self.calculation2()

    def setup_old_scene(self):
        name = Tex("Skalarprodukt")
        name.move_to(np.array([-3.2726103, 1.62026773, 0]))
        name[0][:6].set_color(GREEN)

        mat_a = Matrix([[str(self.vec_a_num[0])], [str(self.vec_a_num[1])], [str(self.vec_a_num[2])]], element_alignment_corner = DOWN, **self.mat_kwargs)
        mat_b = Matrix([[str(self.vec_b_num[0])], [str(self.vec_b_num[1])], [str(self.vec_b_num[2])]], element_alignment_corner = DOWN, **self.mat_kwargs)

        # Skalarprodukt
        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, "dot")
        vec_group.move_to(np.array([-3.2726103, 0, 0]))

        self.add(name, vec_group)
        self.wait()


        self.vec_group = vec_group

    def component_combination(self, show_mat_brackets = True):
        vec_group = self.vec_group

        # Sklarprodukt Flash Animation
        self.path_flash = self.get_dotproduct_path(vec_group, dimension = 3)
        self.play(ShowPassingFlash(self.path_flash), rate_func = smooth, run_time = 2)
        self.wait()

        # equals
        equals = self.equals = MathTex("=").next_to(vec_group, RIGHT)
        self.play(Write(equals), run_time = 1.5)


        x_comp = MathTex(str(self.vec_a_num[0]), "\\cdot", str(self.vec_b_num[0]))
        y_comp = MathTex(str(self.vec_a_num[1]), "\\cdot", str(self.vec_b_num[1]))
        z_comp = MathTex(str(self.vec_a_num[2]), "\\cdot", str(self.vec_b_num[2]))

        mat = self.mat = MobjectMatrix([[x_comp], [y_comp], [z_comp]], element_alignment_corner = DR, **self.mat_kwargs)
        mat.next_to(equals, RIGHT)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformFromCopy(vec_group[0][0][0], mat[0][0][0]),
                    TransformFromCopy(vec_group[1], mat[0][0][1]),
                    TransformFromCopy(vec_group[2][0][0], mat[0][0][2]),
                    lag_ratio = 0
                ),

                AnimationGroup(
                    TransformFromCopy(vec_group[0][0][1], mat[0][1][0]),
                    TransformFromCopy(vec_group[1], mat[0][1][1]),
                    TransformFromCopy(vec_group[2][0][1], mat[0][1][2]),
                    lag_ratio = 0
                ),

                AnimationGroup(
                    TransformFromCopy(vec_group[0][0][2], mat[0][2][0]),
                    TransformFromCopy(vec_group[1], mat[0][2][1]),
                    TransformFromCopy(vec_group[2][0][2], mat[0][2][2]),
                    lag_ratio = 0
                ),

                lag_ratio = 0.8
            ), 
            run_time = 6
        )
        self.wait()

        if show_mat_brackets:
            self.play(Write(mat[1:]))
            self.wait()

            self.play(FadeOut(mat[1:], shift = 3*UP))
            self.wait()

    def result_component_mult(self, fade_out_result = True):
        result = self.result
        result.next_to(self.equals, RIGHT)
        result.set_color_by_tex_to_color_map({"+": LIGHT_BROWN})

        self.play(
            ReplacementTransform(self.mat[0][0], result[0]), 
            ReplacementTransform(self.mat[0][1], result[2]), 
            ReplacementTransform(self.mat[0][2], result[4]), 
            run_time = 1
        )
        self.play(LaggedStartMap(FadeIn, VGroup(result[1], result[3]), shift = UP, lag_ratio = 0.2))
        self.wait()

        if fade_out_result:
            self.play(FadeOut(self.mat[0][0], self.mat[0][1], self.mat[0][2], result))
            self.wait(0.5)

    def calculation1(self):
        vec_group = self.vec_group

        # Berechnung Skalarprodukt
        rects = self.get_dotproduct_surrects(vec_group, color = RED_A)

        #                         0      1       2    3    4      5       6    7    8    9   10   11      12     13
        dot_product = MathTex("1", "\\cdot", "3", "+", "2", "\\cdot", "0", "+", "(", "-", "1", ")", "\\cdot", "2")
        dot_product.set_color_by_tex_to_color_map({"\\cdot": self.dot_color, "+": RED_A})
        dot_product.next_to(self.equals, RIGHT)


        self.play(
            LaggedStartMap(Create, VGroup(rects[0], rects[1]), lag_ratio = 0.75), 
            run_time = 3
        )

        self.play(ShowIncreasingSubsets(VGroup(*dot_product[0:3])), run_time = 1.5)
        self.wait()
        self.play(FadeIn(dot_product[3], shift = DOWN))
        self.wait()

        self.play(
            Transform(rects[0], rects[2]),
            Transform(rects[1], rects[3]), 
            run_time = 2
        )
        self.wait()
        self.play(ShowIncreasingSubsets(VGroup(*dot_product[4:7])), run_time = 1.5)
        self.wait()
        self.play(FadeIn(dot_product[7], shift = UP))
        self.wait()

        self.play(
            Transform(rects[0], rects[4]),
            Transform(rects[1], rects[5]), 
            run_time = 2
        )
        self.play(ShowIncreasingSubsets(VGroup(*dot_product[8:])), run_time = 1.5)
        self.play(*[FadeOut(rect) for rect in [rects[0], rects[1]]])
        self.wait()


        # Klammern
        braces = VGroup(*[
            Brace(part, DOWN, buff = 0.35)
            for part in [
                dot_product[0:3], dot_product[4:7], dot_product[8:]
            ]
        ])
        braces[2].shift(0.1*UP)

        braces_texs = VGroup(*[
            brace.get_tex(str(number))
            for brace, number in zip(braces, [3, 0, -2])
        ])

        self.play(LaggedStartMap(FadeIn, braces, shift = 0.5*DOWN, lag_ratio = 0.25), run_time = 1.5)
        self.play(LaggedStartMap(FadeIn, braces_texs, shift = 0.5*DOWN, lag_ratio = 0.75), run_time = 3)
        self.wait()


        # Ergebnis
        result = MathTex("=", "1")
        result.next_to(dot_product, RIGHT)
        result.shift(0.05*UP)

        self.play(Write(result))
        self.wait()


        # Text zusammenfassung
        und = MathTex("\\&", color = RED_A, height = 1.35, fill_color = RED_A, fill_opacity = 0.1, stroke_width = 2)\
            .to_edge(UP)

        text1 = Text("komponentenweise\nmultiplizieren", size = 0.75, line_spacing = 1, color = GREY)\
            .next_to(und, LEFT, buff = 1)
        text2 = Text("alle Produkte\nzusammenaddieren", size = 0.75, line_spacing = 1, color = GREY)\
            .next_to(und, RIGHT, buff = 1)

        self.play(AddTextLetterByLetter(text1), run_time = 2)
        self.wait(0.75)
        self.play(Create(und), run_time = 0.5)
        self.play(AddTextLetterByLetter(text2), run_time = 2)
        self.wait()

        self.play(ShowPassingFlash(self.path_flash), rate_func = linear, run_time = 2)
        self.wait(3)

        # Ausfaden
        self.play(
            LaggedStart(*[FadeOut(mob, shift = DOWN) for mob in [*braces_texs, *braces, result, dot_product, self.equals]], lag_ratio = 0.05), 
            run_time = 3
        )
        self.wait()

    def calculation2(self):
        mat_a = Matrix([["4"], ["-3"], ["1"]], **self.mat_kwargs)
        mat_b = Matrix([["-2"], ["-1"], ["2"]], **self.mat_kwargs)

        # Skalarprodukt
        vec_group_new = self.group_vecs_with_symbol(mat_a, mat_b, "dot")
        vec_group_new.move_to(self.vec_group)

        self.play(ReplacementTransform(self.vec_group, vec_group_new))
        self.wait()

        path_flash = self.get_dotproduct_path(vec_group_new, dimension = 3)
        self.play(ShowPassingFlash(path_flash), rate_func = smooth, run_time = 3)
        self.wait()

        # equals
        equals = MathTex("=").next_to(vec_group_new, RIGHT)
        self.play(Write(equals), run_time = 1.5)

        # Berechnung Skalarprodukt
        rects = self.get_dotproduct_surrects(vec_group_new, color = RED_A)

        #                      0      1       2    3    4    5    6    7    8    9   10      11     12   13   14   15   16   17      18     19
        dot_product = MathTex("4", "\\cdot", "(", "-", "2", ")", "+", "(", "-", "3", ")", "\\cdot", "(", "-", "1", ")", "+", "1", "\\cdot", "2")
        dot_product.set_color_by_tex_to_color_map({"\\cdot": self.dot_color, "+": RED_A})
        dot_product.next_to(equals, RIGHT)

        part1 = dot_product[0:6]
        plus1 = dot_product[6]
        part2 = dot_product[7:16]
        plus2 = dot_product[16]
        part3 = dot_product[17:]


        self.play(
            LaggedStartMap(Create, VGroup(rects[0], rects[1]), lag_ratio = 0.75), 
            run_time = 1.5
        )

        self.play(ShowIncreasingSubsets(VGroup(*part1)), run_time = 1.5)
        self.wait(0.5)
        self.play(FadeIn(plus1 , shift = 0.5*DOWN), run_time = 0.5)

        self.play(
            Transform(rects[0], rects[2]),
            Transform(rects[1], rects[3]), 
            run_time = 1
        )
        self.play(ShowIncreasingSubsets(VGroup(*part2)), run_time = 1)
        self.wait(0.25)
        self.play(FadeIn(plus2 , shift = 0.5*UP))

        self.play(
            Transform(rects[0], rects[4]),
            Transform(rects[1], rects[5]), 
            run_time = 1
        )
        self.play(ShowIncreasingSubsets(VGroup(*part3)), run_time = 1)
        self.play(*[FadeOut(rect) for rect in [rects[0], rects[1]]])
        self.wait()


        # Klammern
        braces = VGroup(*[
            Brace(part, DOWN, buff = 0.35)
            for part in [
                part1, part2, part3
            ]
        ])
        braces[2].shift(0.1*DOWN)

        braces_texs = VGroup(*[
            brace.get_tex(str(number))
            for brace, number in zip(braces, [-8, 3, 2])
        ])

        self.play(LaggedStartMap(FadeIn, braces, shift = 0.5*DOWN, lag_ratio = 0.25), run_time = 1.5)
        self.play(LaggedStartMap(FadeIn, braces_texs, shift = 0.5*DOWN, lag_ratio = 0.75), run_time = 3)
        self.wait()


        # Ergebnis
        result = MathTex("=", "-", "3")
        result.next_to(dot_product, RIGHT)
        result.shift(0.05*UP)

        self.play(Write(result))
        self.wait()

        self.play(ShowPassingFlash(self.path_flash), rate_func = smooth, run_time = 2)
        self.wait(3)


class KindOfNumbers(Scene):
    def construct(self):

        dot_prod_tex = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=")\
            .scale(1.5)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\cdot": GREEN})

        dot_prod_val = ValueTracker(4)
        dot_prod_dec = DecimalNumber(dot_prod_val.get_value(), num_decimal_places=1, include_sign=True)\
            .scale(1.5)\

        dot_prod_eq = VGroup(dot_prod_tex, dot_prod_dec)\
            .arrange_submobjects(RIGHT, aligned_edge = DOWN)\
            .to_edge(UP)

        numline = NumberLine(x_range=[-6.9,7,1], length = config["frame_width"] - 2, include_numbers = True, include_tip = True)
        numline.shift(UP)

        arrow = Arrow(dot_prod_dec.get_bottom() + 0.2*DOWN, numline.number_to_point(dot_prod_val.get_value()), color = GREEN, buff = 0)

        self.play(
            AnimationGroup(
                FadeIn(dot_prod_eq, shift = DOWN), 
                Create(numline, lag_ratio = 0.25),
                GrowArrow(arrow), 
                lag_ratio = 0.25
            ), 
            run_time = 4
        )
        self.wait()


        dot_prod_dec.add_updater(lambda dec: dec.set_value(dot_prod_val.get_value()))
        arrow.add_updater(lambda ar: ar.become(
            Arrow(dot_prod_dec.get_bottom() + 0.2*DOWN, numline.number_to_point(dot_prod_val.get_value()), color = GREEN, buff = 0)
        ))

        values = [1, -6, -3, 0]
        for x in values:
            self.play(dot_prod_val.animate.set_value(x), run_time = 3)
            self.wait()

        frames = VGroup(*[
            ScreenRectangle(height = 2.4, color = GREY, stroke_width = 2) for _ in range(3)
        ])
        frames.arrange_submobjects(RIGHT)
        frames.to_edge(DOWN)

        lines = VGroup(*[
            Line(start = numline.n2p(start_x), end = numline.n2p(end_x), color = GREY, stroke_width = 2)
            for start_x, end_x in zip(
                [-6.9, -0.1, 0.1], 
                [-0.1, +0.1, 6.6]
            )
        ])

        self.play(
            AnimationGroup(
                *[Transform(line, frame) for line, frame in zip(lines, frames)], 
                lag_ratio = 0.15
            ), 
            run_time = 4
        )
        self.wait()


        values = [5, -2, 3, -5, 0, 4, -4, 1]
        for x in values:
            self.play(dot_prod_val.animate.set_value(x), run_time = 3)
            self.wait()
        self.wait(3)


class VectorSquared(Definition):
    def construct(self):
        self.dot_color = GREEN
        self.cross_color = BLUE 
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.vec_a_num = [4,1,3]
        self.vec_b_num = [4,1,3]

        self.result = MathTex("4\\cdot 4", "+", "1\\cdot 1", "+", "3\\cdot 3")


        self.setup_old_scene()
        self.component_combination(show_mat_brackets=False)
        self.result_component_mult(fade_out_result=False)
        self.turn_result_into_squares()
        self.connect_with_length()


    def turn_result_into_squares(self):
        new_result = MathTex("4^2", "+", "1^2", "+", "3^2", "=", "26")\
            .move_to(self.result, aligned_edge=DL)\
            .set_color_by_tex_to_color_map({"+": LIGHT_BROWN})

        self.play(ReplacementTransform(self.result, new_result[:-2]))
        self.wait(1)

        self.play(Write(new_result[-2:]))
        self.wait()

        self.play(Circumscribe(new_result[:-2], color = BLUE, fade_out = True, time_width = 0.75, run_time = 3))
        self.wait()


        self.new_result = new_result

    def connect_with_length(self):
        self.starting_mobs = Group(*self.mobjects)

        vec_a = self.vec_group[0].copy()
        vec_a.generate_target()
        vec_a.target.move_to(3*LEFT + DOWN)

        lvert = MathTex("\\lvert")\
            .next_to(vec_a.target, LEFT)\
            .set(height = vec_a.get_height())
            
        rvert = MathTex("\\rvert")\
            .next_to(vec_a.target, RIGHT)\
            .set(height = vec_a.get_height())

        self.play(
            self.starting_mobs.animate.to_edge(UP),
            MoveToTarget(vec_a), 
            FadeIn(lvert, shift = RIGHT), 
            FadeIn(rvert, shift = LEFT), 
            run_time = 3
        )
        self.wait()


        # Koordinaten in die Wurzel transformieren
        #                 0       1       2     3    4    5     6    7    8     9  10   11      12      13    14
        length = MathTex("=", "\\sqrt{", "4^", "2", "+", "1^", "2", "+", "3^", "2" "}", "=", "\\sqrt{", "26", "}")\
            .next_to(rvert, RIGHT)\
            .set_color_by_tex_to_color_map({"+": LIGHT_BROWN})

        x = vec_a[0][0].copy()
        y = vec_a[0][1].copy()
        z = vec_a[0][2].copy()

        self.play(
            AnimationGroup(
                x.animate.move_to(length[2]),
                y.animate.move_to(length[5]),
                z.animate.move_to(length[8]),
                lag_ratio = 0.25
            ),
            LaggedStartMap(
                FadeIn, VGroup(length[3], length[6], length[9]), lag_ratio = 0.25, rate_func = squish_rate_func(smooth, 0.4, 0.8)
            ),
            LaggedStartMap(
                FadeIn, VGroup(length[4], length[7]), shift = DOWN, lag_ratio = 0.25, rate_func = squish_rate_func(smooth, 0.6,1)
            ),
            Write(length[0]),
            run_time = 4
        )
        self.remove(x,y,z)
        self.add(length[2], length[5], length[8])
        self.wait()

        self.play(Create(length[1]))
        self.play(Write(length[10:]))
        self.wait()


        # Länge eines Vektors nach unten verschieben
        self.play(
            VGroup(lvert, vec_a, rvert, length).animate.to_edge(DOWN), 
            run_time = 3
        )
        self.wait()


        # Zusammenhang Skalarprodukt und Länge eines Vektors
        #                0           1          2       3       4          5            6       7
        eq = MathTex("\\vec{a}", "\\cdot", "\\vec{a}", "=", "\\lvert", "\\vec{a}", "\\rvert^", "2")\
            .set_color_by_tex_to_color_map({"\\vec{a}": ORANGE, "\\cdot": self.dot_color})\
            .scale(2)\
            .shift(0.5*DOWN)

        self.play(
            AnimationGroup(    
                TransformFromCopy(self.vec_group[:3], eq[:3]),
                Write(eq[3]), 
                TransformFromCopy(VGroup(lvert, vec_a, rvert), eq[4:7]),
                FadeIn(eq[-1], shift = LEFT),
                lag_ratio = 0.3
            ),
            run_time = 3
        )
        self.play(Circumscribe(eq, color = BLUE, time_width = 0.75, run_time = 2))
        self.wait(3)


class Thumbnail_Calc(Calculations):
    def construct(self):
        self.dot_color = BLUE
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
        }

        title = Tex("Skalar", "produkt")\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 4)\
            .add_background_rectangle()\
            .to_edge(UP, buff = 1)
        title[1].set_color(vec_c_color)
        title[2].set_color_by_gradient(vec_c_color, vec_b_color, vec_a_color)

        epi = Tex("Episode 04")\
            .next_to(title, UP, aligned_edge = RIGHT)\
            .add_background_rectangle()


        vec_a_num = [ 1, 2, -1]
        vec_b_num = [-3, 1,  4]

        bullet = MathTex("\\bullet")\
            .set_color(vec_c_color)\
            .shift(3*LEFT + DOWN)

        mats = VGroup(*[
            Matrix(matrix, **self.mat_kwargs).set_color(GREY).next_to(bullet, direction = direc)
            for matrix, direc in zip(
                [
                    [[str(vec_a_num[0])], [str(vec_a_num[1])], [str(vec_a_num[2])]], 
                    [[str(vec_b_num[0])], [str(vec_b_num[1])], [str(vec_b_num[2])]]
                ],
                [RIGHT, LEFT]
            )
        ])

        mats[0][0].set_color(vec_a_color)
        mats[1][0].set_color(vec_b_color)

        arrow = Arrow(UP, DOWN, color = LIGHT_BROWN, max_tip_length_to_length_ratio=0.1)\
            .set_stroke(width = 3)\
            .next_to(bullet, UP, buff = 0.75)


        equals1 = MathTex("=").next_to(mats, RIGHT, buff = 0.75)

        mats_copy = self.group_vecs_with_symbol(mats[0].copy(), mats[1].copy(), type = "bullet")
        mats_copy.next_to(mats, RIGHT, buff = 1)
        path = self.get_dotproduct_path(mats_copy)



        equals2 = MathTex("=").next_to(path, RIGHT, buff = 0.75)
        result = MathTex("-5").set_color(vec_c_color).scale(2).next_to(equals2, RIGHT, buff = 0.75)



        self.add(path, equals1, equals2, result)
        self.add(mats, bullet, arrow)
        self.add(title, epi)


# Scenes Geometrische Bedeutung Skalarprodukt
class Intro_OpeningBook(MovingCameraScene, Calculations):
    def construct(self):

        book = SVGMobject(file_name = "Opening-Book")
        book.scale(3)
        self.play(Write(book[:-13]), run_time = 4)
        self.wait()

        self.play(Write(book[-13:]))
        self.wait()

        black_rect = book[-26]
        self.play(
            self.camera.frame.animate.set(width = black_rect.get_width() - 1).move_to(black_rect), 
            run_time = 2
        )
        self.wait()


class Intro_GeoInter(Calculations):
    def construct(self):
        self.tsf = 1.5
        self.dot_color = vec_c_color
        self.vec_a_num = [ 4, 3, 0]
        self.vec_b_num = [ 1, 2, 0]

        self.mat_kwargs = {
            "v_buff": 0.6,
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1,
            "bracket_h_buff": 0.1
        }

        self.dot_product()


    def dot_product(self):

        mat_a = Matrix([[str(self.vec_a_num[0])], [str(self.vec_a_num[1])]], element_alignment_corner = DOWN, **self.mat_kwargs)
        mat_b = Matrix([[str(self.vec_b_num[0])], [str(self.vec_b_num[1])]], element_alignment_corner = DOWN, **self.mat_kwargs)

        cdot = MathTex("\\cdot").set_color(self.dot_color)
        equals = MathTex("=")
        result = MathTex("10").set_color(self.dot_color)

        calc_group = VGroup(mat_a, cdot, mat_b, equals, result)\
            .arrange_submobjects(RIGHT, buff = 0.25)\
            .scale(self.tsf)

        for index in range(3):
            calc_group[index].save_state()

        text = Tex("Skalar","produkt").scale(self.tsf).next_to(calc_group, UP, aligned_edge=LEFT)
        text[0].set_color(self.dot_color)
        text[1].set_color(GREY)


        calc_group[:3].center()
        self.play(
            GrowFromCenter(calc_group[:3]),
            GrowFromEdge(text, RIGHT),
            run_time = 2
        )

        path = self.get_dotproduct_path(calc_group[:3], dimension=2, stroke_width = 8)
        self.play(ShowPassingFlash(path), run_time = 2)
        self.wait(0.5)

        self.play(
            *[Restore(calc_group[index]) for index in range(3)],
            Write(calc_group[3], rate_func = squish_rate_func(smooth, 0.4, 1)),
        )
        self.wait()

        # Koordinaten in "falschen Vektor" transformieren
        x = MathTex("4", "\\cdot", "1")
        y = MathTex("3", "\\cdot", "2")
        vec_result = MobjectMatrix([[x], [y]], element_alignment_corner = DOWN, **self.mat_kwargs)\
            .scale(self.tsf)\
            .next_to(equals, RIGHT, buff = 0.5)

        self.play(
            TransformFromCopy(mat_a[0][0], vec_result[0][0][0]),
            TransformFromCopy(cdot, vec_result[0][0][1]),
            TransformFromCopy(mat_b[0][0], vec_result[0][0][2]),

            TransformFromCopy(mat_a[0][1], vec_result[0][1][0]),
            TransformFromCopy(cdot, vec_result[0][1][1]),
            TransformFromCopy(mat_b[0][1], vec_result[0][1][2]),

            run_time = 2
        )

        # Koordinaten des falschen Vektors in Summe transformieren
        result_1 = MathTex("4", "\\cdot", "1", "+", "3", "\\cdot", "2").scale(self.tsf).next_to(equals, RIGHT)
        result_1[3].set_color(LIGHT_BROWN)

        self.play(
            ReplacementTransform(vec_result[0][0], result_1[:3]), 
            ReplacementTransform(vec_result[0][1], result_1[4:]), 
            FadeIn(result_1[3], shift = UP, rate_func = squish_rate_func(smooth, 0.4,1)), 
            run_time = 2
        )
        self.wait()

        self.play(ReplacementTransform(result_1, result))
        self.play(Create(SurroundingRectangle(result, color = LIGHT_BROWN)), rate_func = there_and_back_with_pause, run_time = 5)
        self.wait()


class BouncingBall(MovingCameraScene):
    def construct(self):
        self.setup_scene()
        self.show_ball_movements()
        self.center_balls_hits_surface()
        self.outer_ball_hits_surface()
        self.louder_and_quieter()
        self.show_velocity_vectors()
        self.projection()


    def setup_scene(self):
        surface = Line(4*LEFT, 4*RIGHT)\
            .set_color(GREY)
        surface_center = surface.get_center()

        self.ball_kwargs = {"radius": 0.3, "fill_color": BLUE_E, "fill_opacity": 0.5, "sheen_factor": 0.5}
        balls = VGroup(*[self.get_ball(**self.ball_kwargs) for x in range(7)]).move_to(surface)
        balls_num = len(balls) + 1
        ball_target = surface_center + self.ball_kwargs["radius"]*UP
        dlines = VGroup()
        for num, ball in enumerate(balls, start = 1):
            ball.move_to(np.array([3*np.cos(num * 180*DEGREES/balls_num), 3*np.sin(num * 180*DEGREES/balls_num), 0]))

            dline = DashedLine(ball.get_center(), ball_target, color = GREY, dash_length=0.1)
            dline.set_stroke(opacity = 0.5)
            dlines.add(dline)


        balls.save_state()


        self.play(
            Create(surface), 
            LaggedStartMap(DrawBorderThenFill, balls, lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()


        self.surface, self.surface_center = surface, surface_center
        self.balls, self.ball_target, self.balls_num, self.dlines = balls, ball_target, balls_num, dlines

    def show_ball_movements(self):
        self.play(
            AnimationGroup(
                *[self.balls[num].animate(rate_func = linear).move_to(self.ball_target) for num in range(len(self.balls))],
                lag_ratio = 0.2
            ),
            AnimationGroup(
                *[Create(dline) for dline in self.dlines], 
                lag_ratio = 0.2
            ),
            run_time = 5
        )
        self.bring_to_back(self.dlines)
        self.wait()


        text_wand = Tex("Wand")\
            .set_color(vec_a_color)\
            .next_to(self.surface_center, DOWN, buff = 0.5, aligned_edge=LEFT)

        self.play(Write(text_wand))
        self.wait()
        self.play(FadeOut(text_wand, shift = 2 * RIGHT))
        self.wait()


        self.play(Restore(self.balls, lag_ratio = 0.2), run_time = 3)
        self.wait()

    def center_balls_hits_surface(self):
        center_ball = self.balls[3]
        self.play(center_ball.animate(rate_func = linear).move_to(self.ball_target), run_time = 3)
        self.wait()
        self.play(Restore(self.balls), run_time = 2)
        self.wait()

        self.play(center_ball.animate(rate_func = linear).move_to(self.ball_target), run_time = 3)
        self.wait()

    def outer_ball_hits_surface(self):
        outer_ball = self.balls[-1]
        self.play(outer_ball.animate(rate_func = linear).move_to(self.ball_target), run_time = 3)
        self.wait()

        self.play(Restore(self.balls), run_time = 2)
        self.wait()

    def louder_and_quieter(self):
        self.camera.frame.save_state()

        curved_arrow = CurvedDoubleArrow(
            start_point = 3.5*(np.cos(170*DEGREES)*LEFT + np.sin(170*DEGREES)*UP), 
            end_point = 3.5*(np.cos(10*DEGREES)*LEFT + np.sin(10*DEGREES)*UP), 
            angle = -160*DEGREES, radius = 3.5, color = GREY
        )
        louder = Tex("lauter")\
            .add_background_rectangle()\
            .move_to(curved_arrow.get_top())

        quieter1 = Tex("leiser")\
            .add_background_rectangle()\
            .scale(0.6)\
            .move_to(curved_arrow.point_from_proportion(0.1))

        quieter2 = quieter1.copy()\
            .move_to(curved_arrow.point_from_proportion(0.9))

        self.play(
            Create(curved_arrow),
            run_time = 2
        )
        self.play(
            *[Create(tex) for tex in [louder, quieter1, quieter2]], 
            run_time = 1
        )
        self.wait()

    def show_velocity_vectors(self):

        self.pause_button = self.get_pause_button()
        self.pause_button.to_corner(UL)
        self.play_button = self.get_play_button()
        self.play_button.to_corner(UL)

        self.play(DrawBorderThenFill(self.pause_button), run_time = 3)
        self.wait()

        velo_vectors = VGroup()
        for num, ball in enumerate(self.balls, start = 1):
            line_unit = Line(ball.get_center(), self.ball_target)\
                .get_unit_vector()
            velo_vector = Arrow(start = ball.get_center(), end = ball.get_center() + line_unit, buff = 0, color = vec_b_color)
            velo_vectors.add(velo_vector)

        for velo_vector in velo_vectors:
            velo_vector.save_state()

        # Dont know why, but i had to replace direction for center ball with DOWN = np.array([0,-1,0]) in order to work like intended
        directions = [vector.get_end() - vector.get_start() for vector in velo_vectors]
        directions[3] = DOWN 

        self.play(
            AnimationGroup(
                FadeOut(self.pause_button, shift = 2*RIGHT), 
                FadeIn(self.play_button, shift = 2*RIGHT),
                lag_ratio = 0.25
            )
        )
        self.wait()

        self.play(LaggedStartMap(GrowArrow, velo_vectors, lag_ratio = 0.2), run_time = 2)
        self.wait()

        normal_vec = self.normal_vec = Vector(DOWN, buff = 0, color = vec_a_color)
        normal_vec.next_to(self.surface_center, DOWN, buff = 0)
        self.play(GrowArrow(normal_vec), run_time = 2)
        self.wait()

        self.play(
            AnimationGroup(
                FadeIn(self.pause_button, shift = 2*RIGHT), 
                FadeOut(self.play_button, shift = 2*RIGHT),
                lag_ratio = 0.25
            )
        )
        self.wait()

        self.play(
            AnimationGroup(
                FadeOut(self.pause_button, shift = 2*RIGHT), 
                FadeIn(self.play_button, shift = 2*RIGHT),
                lag_ratio = 0.25
            )
        )
        self.wait()

        # Center vector to surface_center
        self.play(
            velo_vectors[3].animate(rate_func = linear).next_to(self.surface_center, direction = directions[3], buff = 0),
            run_time = 4
        )
        self.wait()

        self.rot_vector = velo_vectors[-1].copy()
        self.play(
            Restore(velo_vectors[3]),
            self.rot_vector.animate(rate_func = linear).next_to(self.surface_center, direction = directions[-1], buff = 0),
            self.camera.frame.animate.set(height = 2).move_to(self.normal_vec),
            run_time = 6
        )
        self.remove(self.play_button)
        self.wait(2)

        self.velo_vectors = velo_vectors
        self.directions = directions

    def projection(self):
        vec_num_velo = self.rot_vector.get_end() - self.rot_vector.get_start()
        vec_num_norm = self.normal_vec.get_end() - self.normal_vec.get_start()

        pro_vec = self.get_projection_vec(vec_num_norm, vec_num_velo, color = vec_c_color)
        pro_line = self.get_pro_line(self.rot_vector, pro_vec, color = GREY)
        self.play(Create(pro_line), run_time = 3)
        self.wait(0.5)
        self.play(
            TransformFromCopy(self.rot_vector, pro_vec),
            self.normal_vec.animate.set_fill(opacity = 0.3).set_stroke(opacity = 0.3),
            run_time = 4
        )
        self.wait()

        # Klammer für die Länge des blauen Vektors
        brace = Brace(pro_vec, LEFT, buff = 0)
        brace_tex = brace.get_text("Länge", buff = -0.2).scale(0.5)

        self.play(Create(brace), Write(brace_tex), run_time = 1.5)
        self.wait(0.5)

        # Gleichung mit Skalarprodukt
        lhs = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=").scale(0.5).set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})
        dec = DecimalNumber(
            np.dot(self.rot_vector.get_end(), self.normal_vec.get_end()) / np.linalg.norm(self.rot_vector.get_end())**2, 
            num_decimal_places = 2
        )
        dec.scale(0.5)
        dec.set_color(vec_c_color)

        eq = VGroup(lhs, dec).arrange_submobjects(RIGHT, buff = 0.1, aligned_edge = DOWN).next_to(self.normal_vec, DOWN, buff = 0.1)

        # Gleichung schreiben, Ball fällt von links auf target
        self.play(Write(eq))
        self.wait()

        self.play(self.balls[-1].animate(rate_func = linear).move_to(self.ball_target), run_time = 2)
        self.wait()

        self.play(FadeOut(VGroup(brace, brace_tex), shift = 0.5*LEFT))
        self.wait()

        dec.add_updater(lambda d: d.set_value(np.dot(self.rot_vector.get_end(), self.normal_vec.get_end()) / np.linalg.norm(self.rot_vector.get_end())**2))

        # Updater für Vektoren
        pro_vec.add_updater(lambda v: v.become(
            self.get_projection_vec(
                self.normal_vec.get_end() - self.normal_vec.get_start(), 
                self.rot_vector.get_end() - self.rot_vector.get_start(), 
                color = vec_c_color)
        ))
        pro_line.add_updater(lambda l: l.become(
            self.get_pro_line(self.rot_vector, pro_vec, color = GREY, stroke_opacity = 0.5)
        ))


        self.play(Rotating(self.rot_vector, radians = -72.987*DEGREES, about_point=self.surface_center, run_time = 5))
        self.play(self.balls[3].animate(rate_func = linear).move_to(self.ball_target), run_time = 2)
        self.wait()

        self.play(Rotating(self.rot_vector, radians = -72.987*DEGREES, about_point=self.surface_center, run_time = 5))
        self.play(self.balls[0].animate(rate_func = linear).move_to(self.ball_target), run_time = 2)
        self.wait()


    # functions 
    def get_ball(self, radius, fill_color, fill_opacity, sheen_factor):
        ball = Circle(radius = radius)\
            .set_fill(color = fill_color, opacity = fill_opacity)\
            .set_stroke(width = 0)\
            .set_sheen(factor = sheen_factor, direction = DR)

        return ball

    def get_pause_button(self):
        pause = VGroup(*[
            Rectangle(height = 1, width = 0.25)\
                .set_fill(color = MAROON_E, opacity = 0.75)\
                .set_stroke(width = 2, color = MAROON_E)
            for _ in range(2)
        ])
        pause.arrange_submobjects(RIGHT)

        return pause

    def get_play_button(self):
        play = RegularPolygon(n = 3)\
            .set_fill(color = GREEN_E, opacity = 0.75)\
            .set_stroke(color = GREEN_E, width = 2)\
            .rotate(-TAU/4)\
            .set(height = self.pause_button.get_height())

        return play

    def get_projection_vec(self, num_vec_a, num_vec_b, **kwargs):
        dot_prod_value = np.dot(num_vec_a, num_vec_b)
        dot_prod_norm = dot_prod_value / np.linalg.norm(num_vec_a)**2

        start = self.surface_center
        end = np.array([dot_prod_norm * x for x in num_vec_a])

        projection_vec = Arrow(start, end, buff = 0, **kwargs)

        return projection_vec

    def get_pro_line(self, vec, pro_vec, **kwargs):
        dline = DashedLine(start = vec.get_end(), end = pro_vec.get_end(), **kwargs)
        return dline 


class VideoParts(Scene):
    def construct(self):
        self.num_examples = 2

        self.plane_kwargs = {
            "x_length": config["frame_height"]/2.5 * 16/9, "y_length": config["frame_height"]/2.5,
            "axis_config": {"stroke_color": WHITE}, "background_line_style": {"stroke_opacity": 0.4, "stroke_color": BLUE_D}
        }

        # Vectors
        vec_a_nums = self.vec_a_nums = [[np.cos(30*DEGREES),  np.sin(30*DEGREES),  0], [ 4, 3, 0]]
        vec_b_nums = self.vec_b_nums = [[np.cos(150*DEGREES), np.sin(150*DEGREES), 0], [ 1, 2, 0]]

        # Numberplanes and Surrounding Rectangles
        planes = self.planes = VGroup(*[
            NumberPlane(
                x_range = [y_min*16/9, y_max*16/9], y_range = [y_min, y_max], 
                **self.plane_kwargs
            ) for _, y_min, y_max in zip(range(self.num_examples), [-1.15, -3.25], [1.15, 3.25])
        ])
        planes.arrange_submobjects(DOWN, buff = 0.5)
        planes.to_edge(RIGHT, buff = 1)

        planes[0].add_coordinates()

        a_vectors = VGroup(*[self.get_vector(plane, vec_a_num, color = vec_a_color) for plane, vec_a_num in zip(planes, vec_a_nums)])
        b_vectors = VGroup(*[self.get_vector(plane, vec_b_num, color = vec_b_color) for plane, vec_b_num in zip(planes, vec_b_nums)])


        texts = VGroup(*[
            Tex(tex) 
            for tex in ["1. Einheitsvektoren", "2. beliebige Vektoren"]
        ])
        texts.arrange_submobjects(DOWN, buff = 4, aligned_edge = RIGHT)
        texts.next_to(planes, LEFT, buff = 1)

        dot_prod_val = ValueTracker(1)
        dot_prod_dec = DecimalNumber(dot_prod_val.get_value(), include_sign = True, edge_to_fix = LEFT).scale(1.5).set_color(vec_c_color)
        dot_prod_tex = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=")\
            .scale(1.5)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})

        dot_prod = VGroup(dot_prod_tex, dot_prod_dec)\
            .arrange_submobjects(RIGHT, aligned_edge = DOWN)\
            .shift(2*LEFT)\
            .align_to(texts, RIGHT)


        # ANIMATIONS UNIT_VECTORS
        self.play(FadeIn(dot_prod, shift = LEFT))
        self.play(
            AnimationGroup(
                Create(planes[0]), 
                GrowArrow(a_vectors[0]), 
                GrowArrow(b_vectors[0]), 
                lag_ratio = 0.5
            ),
            run_time = 2
        )
        self.wait(0.5)

        pro_vec_1 = self.get_projection_vec(planes[0], vec_a_nums[0], vec_b_nums[0], color = BLUE)
        self.play(TransformFromCopy(b_vectors[0], pro_vec_1), run_time = 2)
        self.wait()

        circle = Circle(arc_center = planes[0].c2p(0,0), radius = planes[0].get_x_unit_size(), color = WHITE)
        self.play(
            Create(circle), 
            Write(texts[0]), 
        )
        self.wait()


        arrow = Arrow(texts[0].get_bottom(), dot_prod_dec[0].get_top(), color = GREEN)
        self.play(GrowArrow(arrow))
        self.wait(0.5)

        dot_prod_dec.add_updater(lambda dec: dec.set_value(dot_prod_val.get_value()))
        values = (-1, 0.59, -0.87, 0.31)
        for value in values:
            self.play(dot_prod_val.animate.set_value(value), run_time = 1.5)
            self.wait(0.5)

        arrow2 = Arrow(texts[1].get_top(), dot_prod_dec[3].get_bottom(), color = GREEN)
        self.play(
            GrowArrow(arrow2), 
            Write(texts[1])
        )
        self.wait(0.5)

        self.play(
            AnimationGroup(
                Create(planes[1]), 
                GrowArrow(a_vectors[1]), 
                GrowArrow(b_vectors[1]), 
                lag_ratio = 0.5
            ),
            run_time = 2
        )
        self.wait()


        pro_vec_2 = self.get_projection_vec(planes[1], vec_a_nums[1], vec_b_nums[1], color = BLUE)
        self.play(TransformFromCopy(b_vectors[1], pro_vec_2), run_time = 2)
        self.wait()


        values = (5, -3.87, 0, 10)
        for value in values:
            self.play(dot_prod_val.animate.set_value(value), run_time = 1.5)
            dot_prod_dec.set_color(vec_c_color)
            self.wait(0.5)
        self.wait(2)


    # functions
    def get_vector(self, plane, vec_num, **kwargs):
        return Arrow(
            plane.coords_to_point(0, 0),
            plane.coords_to_point(*vec_num),
            buff=0,
            **kwargs,
        )

    def get_projection_vec(self, plane, num_vec_a, num_vec_b, **kwargs):
        dot_prod_value = np.dot(num_vec_a, num_vec_b)
        dot_prod_norm = dot_prod_value / np.linalg.norm(num_vec_a)**2

        start = plane.c2p(0,0)
        end = plane.c2p(*[dot_prod_norm * x for x in num_vec_a])

        return Arrow(start, end, buff = 0, **kwargs)


class UnitVectors(MovingCameraScene, VectorScene):
    def construct(self):
        self.plane_kwargs = {
            "x_range": [-2 * 16/9, 2*16/9], "y_range": [-2.75,1.25], 
            "x_length": config["frame_width"], "y_length": config["frame_height"],
            "axis_config": {"stroke_color": GREY}, "background_line_style": {"stroke_opacity": 0.6, "stroke_color": GREY}
        }

        self.plane = self.get_plane(**self.plane_kwargs) 
        self.circle = self.get_circle(color = GREY)

        self.vec_a_num = [np.cos(30*DEGREES), np.sin(30*DEGREES), 0]
        self.vec_b_num = [np.cos(150*DEGREES), np.sin(150*DEGREES), 0]

        self.vec_a = self.get_vector(self.vec_a_num, color = vec_a_color)
        self.vec_b = self.get_vector(self.vec_b_num, color = vec_b_color)


        self.play(Create(self.plane, lag_ratio = 0.1), run_time = 2)
        self.wait()

        self.make_vectors_unit_vectors()
        self.zoom_camera_in()
        self.project_on_vec_a()
        self.zoom_camera_out()
        self.numberline_rotation()


    def make_vectors_unit_vectors(self):

        vec_a_init = self.get_vector([1,2,0], color = vec_a_color).move_to(self.plane.c2p(1,-0.5))
        vec_b_init = self.get_vector([-2.5,0.75,0], color = vec_b_color).move_to(self.plane.c2p(-1.65,-0.65))


        self.play(
            LaggedStartMap(GrowArrow, VGroup(vec_a_init, vec_b_init), lag_ratio = 0.2), 
            run_time = 3
        )
        self.wait()


        vector = Tex("Vektor")
        properties = VGroup(*[
            Tex(text) for text in ["Betrag/Länge", "Richtung"]
        ])
        properties.arrange_submobjects(DOWN, buff = 0.75, aligned_edge = LEFT)
        properties.next_to(vector, RIGHT, buff = 2)

        text_group = VGroup(vector, properties)\
            .center()\
            .shift(2.8*DOWN)\
            .add_background_rectangle(buff = 0.15)


        arrow_kwargs = {"color": GREY, "buff": 0.1, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}
        arrows = VGroup(*[
            Arrow(start = vector.get_right() + vbuff*UP, end = prop.get_left() + hbuff*LEFT, **arrow_kwargs)
            for vbuff, prop, hbuff in zip(
                [0.15, -0.15], [properties[0], properties[1]], [0.2, 0.2]
            )
        ])

        self.play(
            FadeIn(text_group[0]), 
            Write(text_group[1]),
            LaggedStartMap(Create, arrows, lag_ratio = 0.25, run_time = 2)
        )
        self.wait()

        self.play(Write(properties[0]))
        self.play(vec_b_init.animate(rate_func = there_and_back, run_time = 1.5).scale(0.25, about_point = vec_b_init.get_start()))

        self.play(Write(properties[1]))
        self.play(Rotating(vec_a_init, radians = TAU, about_point = vec_a_init.get_start(), rate_func = smooth, run_time = 1.5))
        self.wait()




        # Vektoren in Einheitsvektoren transformieren
        self.play(
            ReplacementTransform(vec_a_init, self.vec_a), 
            ReplacementTransform(vec_b_init, self.vec_b), 
            Create(self.circle),
            FadeToColor(properties[0], DARK_GREY),
            FadeToColor(arrows[0], DARK_GREY),
            run_time = 4
        )
        self.play(Circumscribe(properties[1], color = BLUE, run_time = 2))
        self.wait()

        self.play(
            LaggedStartMap(FadeOut, VGroup(
                text_group[0], properties[1], arrows[1], properties[0], arrows[0], vector
            ), lag_ratio = 0.1), 
            run_time = 3
        )
        self.wait()

        # Einheitsvektoren auf Achsen drehen, um Länge zu verdeutlichen
        text = Tex("Einheitsvektoren")\
            .to_edge(UL, buff = 0.5)\
            .add_background_rectangle()


        self.play(
            Rotate(self.vec_a, angle = -30*DEGREES, about_point = self.origin, rate_func = there_and_back_with_pause, run_time = 4),
            Rotate(self.vec_b, angle = -60*DEGREES, about_point = self.origin, rate_func = there_and_back_with_pause, run_time = 4),
            FadeIn(text, shift = RIGHT, rate_func = squish_rate_func(smooth, 0.2, 0.5), run_time = 4)
        )
        self.play(FadeOut(text, shift = UP))
        self.wait()

    def zoom_camera_in(self):
        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.set(height = self.plane.y_axis.get_unit_size() * 2.5).move_to(self.origin),
            run_time = 2
        )
        self.wait()

    def project_on_vec_a(self):

        pro_vec = self.get_projection_vec(self.vec_a_num, self.vec_b_num, color = vec_c_color)
        pro_vec.add_updater(lambda v: v.become(
            self.get_projection_vec(self.plane.p2c(self.vec_a.get_end()), self.plane.p2c(self.vec_b.get_end()), color = vec_c_color)
        ))
        pro_line = self.get_pro_line(self.vec_b, pro_vec, color = WHITE)
        pro_line.add_updater(lambda l: l.become(
            self.get_pro_line(self.vec_b, pro_vec)
        ))



        circle_ticks = self.get_circle_ticks(pro_on_vec = self.vec_a, color = vec_c_color)
        circle_ticks_nums = self.get_tick_labels(circle_ticks)

        self.play(Rotating(self.vec_b, radians = -60*DEGREES, about_point=self.origin, run_time = 2))
        self.wait()

        self.play(
            TransformFromCopy(self.vec_b, pro_vec),
            Create(pro_line), 
            run_time = 3
        )
        self.wait()

        self.play(Create(circle_ticks[1]), Write(circle_ticks_nums[1]))
        self.wait()

        angles = [30*DEGREES, 30*DEGREES, 60*DEGREES, 60*DEGREES, 30*DEGREES, 30*DEGREES, 60*DEGREES]
        tick_index = [2,3,4,5,6,7,0]

        for angle, index in zip(angles, tick_index):
            self.play(Rotating(self.vec_b, radians = angle, about_point=self.origin, run_time = 5))
            self.wait()

            self.play(Create(circle_ticks[index]), Write(circle_ticks_nums[index]))
            self.wait()
        self.wait()


        sector_pos = self.get_circle_sector(pos_or_neg = "pos")
        sector_neg = self.get_circle_sector(pos_or_neg = "neg")

        self.play(Rotating(self.vec_b, radians = 90*DEGREES, about_point=self.origin, run_time = 2))
        self.play(
            FadeIn(sector_pos, run_time = 2),
            Rotating(self.vec_b, radians = -180*DEGREES, about_point=self.origin, run_time = 5)
        )
        self.bring_to_back(sector_pos)
        self.play(
            FadeIn(sector_neg, run_time = 2),
            Rotating(self.vec_b, radians = -180*DEGREES, about_point=self.origin, run_time = 5)
        )
        self.bring_to_back(sector_neg)
        self.wait()

    def zoom_camera_out(self):
        self.play(Restore(self.camera.frame), run_time = 2)
        self.wait()

    def numberline_rotation(self):

        num_line = NumberLine(
            x_range = [-1.25, 1.25, 0.5], length = 2.5*self.plane.x_axis.get_unit_size(), 
            include_numbers = True, numbers_to_exclude=[0.5, -0.5],
            stroke_width = 5,
        )
        num_line.to_edge(DOWN)


        arrow = Arrow(ORIGIN, 0.5*DOWN, buff = 0, color = TEAL)
        arrow.add_updater(lambda a: a.next_to(num_line.number_to_point(self.get_dot_prod_from_vecs(self.vec_a, self.vec_b)), UP))


        dot_tex = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=").set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})
        dot_dec = DecimalNumber(self.get_dot_prod_from_vecs(self.vec_a, self.vec_b), include_sign = True, edge_to_fix = RIGHT, color = vec_c_color)
        dot_dec.add_updater(lambda dec: dec.set_value(self.get_dot_prod_from_vecs(self.vec_a, self.vec_b)))

        calc = VGroup(dot_tex, dot_dec).arrange_submobjects(RIGHT, aligned_edge = DOWN)
        calc.add_updater(lambda c: c.next_to(arrow, UP))

        big_rect = Rectangle(width = config["frame_width"], height = 1.5 * self.plane.y_axis.get_unit_size())\
            .set_stroke(width = 0)\
            .set_fill(color = BLACK, opacity = 0.8)\
            .to_edge(DOWN, buff = 0)


        self.play(
            AnimationGroup(
                Create(big_rect), 
                Create(num_line), 
                GrowArrow(arrow), 
                Write(calc),
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.play(
            Rotating(self.vec_b, radians = 2*TAU, about_point=self.origin, run_time = 20)
        )
        self.wait()

    # functions 
    def get_plane(self, **kwargs):
        plane = NumberPlane(**kwargs)
        plane.add_coordinates()
        self.origin = plane.c2p(0,0)

        return plane

    def get_circle(self, **kwargs):
        circle = Circle(radius = self.plane.get_x_unit_size(), **kwargs)
        circle.move_to(self.origin)

        return circle

    def get_circle_ticks(self, pro_on_vec, tick_length = 0.2, **line_kwargs):
        circle = self.circle

        num_ticks = 8

        angle_values = [0, 60, 90, 120, 180, 240, 270, 300, 360]

        ticks = VGroup()
        for num in range(num_ticks):
            tick = Line(LEFT, RIGHT, **line_kwargs)\
                .set_length(tick_length)\
                .move_to(circle.get_start())\
                .rotate(angle = angle_values[num] * DEGREES, about_point=circle.get_center())
            ticks.add(tick)

        ticks.rotate(angle = pro_on_vec.get_angle())

        return ticks

    def get_tick_labels(self, ticks, num_scale_value = 0.75):
        num_ticks = len(ticks)

        values = [1, 0.5, 0, -0.5, -1, -0.5, 0, 0.5]
        numbers = VGroup()

        for num in range(num_ticks):
            direc = ticks[num].get_center() - self.origin
            number = MathTex(str(values[num]))\
                .scale(num_scale_value)\
                .next_to(ticks[num], direction = direc, buff = 0.05)\
                .set_color(ticks[num].get_color())
            numbers.add(number)

        return numbers

    def get_circle_sector(self, pos_or_neg = "pos"):

        if pos_or_neg is "pos":
            color = vec_a_color
            angle = TAU/2
        else:
            color = vec_b_color
            angle = -TAU/2

        sector = Sector(
            outer_radius = self.plane.x_axis.get_unit_size(), 
            start_angle = self.vec_a.get_angle() - TAU/4, angle = angle, 
            arc_center = self.origin, 
            color = color, fill_opacity = 0.2
        )
        
        return sector

    def get_dot_prod_from_vecs(self, vec_a, vec_b):
        coords_a = self.plane.p2c(vec_a.get_end())
        coords_b = self.plane.p2c(vec_b.get_end())

        return np.dot(coords_a, coords_b)

    def get_projection_vec(self, num_vec_a, num_vec_b, **kwargs):
        dot_prod_value = np.dot(num_vec_a, num_vec_b)
        dot_prod_norm = dot_prod_value / np.linalg.norm(num_vec_a)**2

        start = self.origin
        end = self.plane.c2p(*[dot_prod_norm * x for x in num_vec_a])

        projection_vec = Arrow(start, end, buff = 0, **kwargs)

        return projection_vec

    def get_pro_line(self, vec, pro_vec, **kwargs):
        dline = DashedLine(start = vec.get_end(), end = pro_vec.get_end(), **kwargs)
        return dline 


class CosineValues(UnitVectors):
    def construct(self):
        self.plane_kwargs = {
            "x_range": [-1.25, 1.25], "y_range": [-1.25, 1.25], 
            "x_length": 4, "y_length": 4,
            "axis_config": {"stroke_color": GREY}, "background_line_style": {"stroke_opacity": 0.6, "stroke_color": GREY}
        }
        self.plane = self.get_plane(**self.plane_kwargs) 
        self.plane.shift(4*RIGHT)
        self.origin = self.plane.c2p(0,0)

        self.vec_a_num = [np.cos(30*DEGREES), np.sin(30*DEGREES), 0]
        self.vec_b_num = [np.cos(150*DEGREES), np.sin(150*DEGREES), 0]

        self.vec_a = self.get_vector(self.vec_a_num, color = vec_a_color)
        self.vec_b = self.get_vector(self.vec_b_num, color = vec_b_color)

        self.num_sampled_graph_points_per_tick = 20
        self.axes = Axes(
            x_range = [0, 2*PI + 0.5, PI/2], y_range = [-1.5, 1.5],
            x_length = 7, y_length = 4, 
            y_axis_config = {"include_numbers": True}, 
        )
        self.axes.shift(3*LEFT)


        self.axes_rad_labels = VGroup(*[
            MathTex(tex).scale(0.75).next_to(self.axes.c2p(x_coord, 0), DOWN)
            for tex, x_coord in zip(
                ["180^\\circ", "360^\\circ"], 
                [PI, 2*PI]
            )
        ])


        self.circle = self.get_circle(arc_center = self.origin, color = GREY)
        self.circle_ticks = self.get_circle_ticks(self.vec_a, color = vec_c_color)
        self.circle_ticks_nums = self.get_tick_labels(self.circle_ticks)

        self.setup_scene()
        self.projection_to_graph()
        self.cos_equation()



    def setup_scene(self):
        self.axes.x_label = MathTex("\\varphi")\
            .set_color(GREEN)\
            .next_to(self.axes.x_axis, RIGHT)
        self.axes.y_label = MathTex("\\vec{a}", "\\cdot", "\\vec{b}")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .next_to(self.axes.y_axis, UP)\
            .shift(0.2*RIGHT)

        self.play(
            AnimationGroup(
                Create(self.plane, lag_ratio = 0.1),
                Create(self.axes, lag_ratio = 0.1),
                Create(self.circle), 
                ShowIncreasingSubsets(self.circle_ticks),
                ShowIncreasingSubsets(self.circle_ticks_nums),
                Create(VGroup(self.axes.x_label, self.axes.y_label), lag_ratio = 0.25),
                Create(self.axes_rad_labels, lag_ratio = 0.25),
                LaggedStartMap(GrowArrow, VGroup(self.vec_a, self.vec_b), lag_ratio = 0.25),
                lag_ratio = 0.15
            ),
            run_time = 6
        )
        self.wait()

    def projection_to_graph(self):
        pro_vec = self.get_projection_vec(self.vec_a_num, self.vec_b_num, color = vec_c_color)
        pro_line = self.get_pro_line(self.vec_b, pro_vec, color = WHITE, stroke_opacity = 0.5)

        self.play(
            Create(pro_line), 
            TransformFromCopy(self.vec_b, pro_vec), 
            run_time = 4
        )
        self.wait()

        arc_kwargs = {"radius": 0.6, "arc_center": self.origin, "color": GREEN}
        arc = Arc(start_angle = self.vec_a.get_angle(), angle = self.vec_b.get_angle() - self.vec_a.get_angle(), **arc_kwargs)
        arc.add_updater(lambda arc: arc.become(
            Arc(
                start_angle = self.vec_a.get_angle(), 
                angle = self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b), 
                **arc_kwargs
            )
        ))


        self.play(
            AnimationGroup(
                Create(arc), 
                Circumscribe(self.axes.x_label, color = GREEN, time_width = 0.75, run_time = 2), 
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()

        # UPDATERS
        pro_vec.add_updater(lambda v: v.become(
            self.get_projection_vec(self.plane.p2c(self.vec_a.get_end()), self.plane.p2c(self.vec_b.get_end()), color = vec_c_color)
        ))
        pro_line.add_updater(lambda l: l.become(
            self.get_pro_line(self.vec_b, pro_vec, color = WHITE, stroke_opacity = 0.5)
        ))

        self.play(Rotating(self.vec_b, radians = -120*DEGREES, about_point = self.origin, run_time = 5.5))
        self.wait()


        graph_vec = Arrow(
            self.axes.c2p(0,0), self.axes.c2p(0, self.get_dot_prod_from_vecs(self.vec_a, self.vec_b)), 
            buff = 0, color = vec_c_color
        )
        self.play(ReplacementTransform(pro_vec.copy(), graph_vec), run_time = 7)
        self.wait()


        graph_vec.add_updater(lambda gv: gv.become(
            Arrow(
                self.axes.c2p(self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b), 0), 
                self.axes.c2p(
                    self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b), 
                    self.get_dot_prod_from_vecs(self.vec_a, self.vec_b)
                ),
                buff = 0, color = vec_c_color
            )
        ))


        graph_cos = self.axes.get_graph(lambda x: np.cos(x), x_range = [0, 2*PI], color = graph_vec.get_color())
        graph_cos2 = graph_cos.copy()
        graph_cos.add_updater(lambda g: g.become(
            self.axes.get_graph(
                lambda x: np.cos(x), x_range = [0, self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b)], 
                color = graph_vec.get_color()
            )
        ))
        self.add(graph_cos)


        # ROTATE VECTOR TAU
        self.play(Rotating(self.vec_b, radians = 359.99999*DEGREES, about_point = self.origin, run_time = 12))
        graph_cos.clear_updaters()


        tex_cos = Tex("Kosinusfunktion").next_to(self.axes, DOWN)

        self.add(graph_cos2)
        self.play(
            Rotating(self.vec_b, radians = TAU, about_point = self.origin, rate_func = linear, run_time = 12),
            Create(tex_cos, run_time = 3, rate_func = squish_rate_func(smooth)),
        )
        self.wait()

    def cos_equation(self):
        #                 0          1          2       3      4      5       6        7
        eq1 = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=", "\\cos", "(", "\\varphi", ")")

        #                 0          1          2       3         4         5           6          7         8          9           10         11       12     13       14     15        
        eq2 = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\cos", "(", "\\varphi", ")")

        for eq in eq1, eq2:
            eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\varphi": GREEN})
            eq.scale(1.4)

        eq1.to_edge(UP, buff = 0.35).shift(1.5*LEFT)
        eq2.move_to(eq1, aligned_edge=LEFT)

        self.play(Write(eq1))
        self.play(Circumscribe(eq1[4:], color = vec_c_color, time_width = 0.75, run_time = 3))
        self.wait()

        self.play(
            ReplacementTransform(eq1[:4], eq2[:4]), 
            ReplacementTransform(eq1[4:], eq2[12:]), 
        )

        self.play(
            LaggedStartMap(
                FadeIn, VGroup(eq2[4:7], eq2[7], eq2[8:11], eq2[11]), shift = 0.5*UP, lag_ratio = 0.15
            )
        )
        self.play(Circumscribe(eq2, time_width = 0.75, color = vec_c_color, run_time = 2))
        self.play(
            Rotating(self.vec_b, radians = PI/3, about_point = self.origin),
            rate_func = smooth, run_time = 3
        )
        self.wait()


        brace_a = Brace(eq2[4:7], DOWN)
        a_tex = brace_a.get_tex("1")

        brace_b = Brace(eq2[8:11], DOWN)
        b_tex = brace_b.get_tex("1")

        self.play(
            LaggedStartMap(Create, VGroup(brace_a, brace_b), lag_ratio = 0.25), 
            Write(VGroup(a_tex, b_tex), lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait()

        self.play(FadeOut(VGroup(a_tex, b_tex, brace_a, brace_b), shift = 0.5*DOWN, lag_ratio = 0.1), run_time = 1.5)
        self.wait()

        self.play(
            Rotating(self.vec_b, radians = TAU, about_point = self.origin, rate_func = linear, run_time = 12),
        )
        self.wait()

    # functions 
    def angle_between_vectors_bigger_than_pi(self, arrow_a, arrow_b):
        angle = arrow_b.get_angle() - arrow_a.get_angle()

        if angle < 0:
            new_angle = angle + TAU
            return new_angle
        else:
            return angle


class AskAboutNonUnitVectors(Scene):
    def construct(self):
        sort_of_vectors = VGroup(*[
            Tex(tex) for tex in [
                "Einheitsvektoren", "beliebige Vektoren"
            ]
        ])
        sort_of_vectors.arrange_submobjects(RIGHT, buff = 3, aligned_edge = UP).to_edge(UP, buff = 1)

        self.play(FadeIn(sort_of_vectors, shift = 0.5*DOWN, lag_ratio = 0.2), run_time = 2)
        self.wait()


        vec_a_num = [1,0,0]
        vec_b_num = [np.cos(50*DEGREES), np.sin(50*DEGREES), 0]
        start_unit = 4*LEFT
        vec_a = Arrow(start = start_unit, end = start_unit + vec_a_num, color = vec_a_color, buff = 0)
        vec_b = Arrow(start = start_unit, end = start_unit + vec_b_num, color = vec_b_color, buff = 0)

        pro_vec_unit = self.get_projection_vec(vec_a_num, vec_b_num, start = start_unit, color = vec_c_color)
        pro_line_unit = self.get_pro_line(vec_b, pro_vec_unit, color = GREY)

        self.play(
            LaggedStartMap(GrowArrow, VGroup(vec_a, vec_b), lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait(0.5)
        self.play(
            Create(pro_line_unit), 
            TransformFromCopy(vec_b, pro_vec_unit), 
            run_time = 3
        )
        self.wait()


        vec_c_num = [2.5,0,0]
        vec_d_num = [3*np.cos(50*DEGREES), 3*np.sin(50*DEGREES), 0]
        start_non_unit = 1.75*RIGHT
        vec_c = Arrow(start = start_non_unit, end = start_non_unit + vec_c_num, color = vec_a_color, buff = 0)
        vec_d = Arrow(start = start_non_unit, end = start_non_unit + vec_d_num, color = vec_b_color, buff = 0)

        pro_vec_non_unit = self.get_projection_vec(vec_c_num, vec_d_num, start = start_non_unit, color = vec_c_color)
        pro_line_non_unit = self.get_pro_line(vec_d, pro_vec_non_unit, color = GREY)


        self.play(
            AnimationGroup(
                *[TransformFromCopy(vec1, vec2) for vec1, vec2 in zip([vec_a, vec_b], [vec_c, vec_d])], 
                lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.wait(0.5)
        self.play(
            Create(pro_line_non_unit), 
            TransformFromCopy(vec_d, pro_vec_non_unit), 
            run_time = 3
        )
        self.wait()


        #                0          1          2       3         4         5           6          7         8          9           10         11       12     13       14     15        
        eq = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\cos", "(", "\\varphi", ")")
        eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\varphi": GREEN})
        eq.scale(1.4)
        eq.to_edge(DOWN, buff = 1)

        self.play(ShowIncreasingSubsets(eq), run_time = 5)
        self.wait(3)




    def get_projection_vec(self, num_vec_a, num_vec_b, start, **kwargs):
        dot_prod_value = np.dot(num_vec_a, num_vec_b)
        dot_prod_norm = dot_prod_value / np.linalg.norm(num_vec_a)**2

        end = start + np.array([dot_prod_norm * x for x in num_vec_a])

        projection_vec = Arrow(start, end, buff = 0, **kwargs)

        return projection_vec

    def get_pro_line(self, vec, pro_vec, **kwargs):
        dline = DashedLine(start = vec.get_end(), end = pro_vec.get_end(), **kwargs)
        return dline 


class DotProdRectangle(MovingCameraScene, ProjectionVectorScene):
    def construct(self):

        self.plane_config = {
            "axis_config": {"stroke_color": GREY}, "background_line_style": {"stroke_opacity": 0.6, "stroke_color": GREY}
        }
        self.pro_color = GREEN
        self.rect_color = BLUE_E
        self.x_value = 1
        self.y_value = 2
        self.z_value = 0
        self.vector_stat = [4,3,0]
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1,
        }

        self.setup_scene()
        self.calc_dot_product()
        self.zoom_camera()
        self.second_formula()
        self.projection_vectors()
        self.length_of_projection_vector()
        self.projection_rectangle()
        # self.varying_rectangles()
        # self.varying_vectors()


    def setup_scene(self):
        plane = self.get_plane(**self.plane_config)
        plane.add_coordinates()

        self.camera.frame.save_state()
        self.camera.frame.set(width = config["frame_width"] * 0.33),
        start_vec_a = plane.get_vector([np.cos(30*DEGREES), np.sin(30*DEGREES), 0], color = vec_a_color)
        start_vec_b = plane.get_vector([np.cos(90*DEGREES), np.sin(90*DEGREES), 0], color = vec_b_color)
        circle = Circle(arc_center = self.origin, radius = plane.get_x_unit_size(), color = GREY)

        self.add(plane)
        self.wait(2)

        self.play(
            LaggedStartMap(GrowArrow, VGroup(start_vec_a, start_vec_b)), 
            Create(circle), 
            run_time = 1.5
        )
        self.wait()


        veca, vecb = self.get_vectors_ab()

        a_matrix = Matrix([[str(self.vector_stat[0])], [str(self.vector_stat[1])]], **self.mat_kwargs)
        b_matrix = Matrix([["1"], ["2"]], **self.mat_kwargs)
        a_matrix_label = MathTex("\\vec{a}", "=").set_color(veca.get_color())
        b_matrix_label = MathTex("\\vec{b}", "=").set_color(vecb.get_color())
        
        for label, matrix in zip([a_matrix_label, b_matrix_label], [a_matrix, b_matrix]):
            label.next_to(matrix, LEFT)

        a_texs = VGroup(a_matrix_label, a_matrix).to_corner(UL)
        b_texs = VGroup(b_matrix_label, b_matrix).next_to(a_texs, RIGHT, buff = 0.5)

        self.matrix_group = VGroup(a_texs, b_texs)


        bg_rect1 = Rectangle(
            width = self.matrix_group.width + 0.1,
            height = self.matrix_group.height + 0.1,
            stroke_width = 0,
        )
        bg_rect1.set_fill(color = BLACK, opacity=0.7)
        bg_rect1.move_to(self.matrix_group)
        self.play(
            AnimationGroup(
                FadeIn(bg_rect1), 
                Write(a_texs),
                Uncreate(circle),
                Restore(self.camera.frame),
                ReplacementTransform(start_vec_a, veca),
                Write(b_texs),
                ReplacementTransform(start_vec_b, vecb),
                lag_ratio = 0.05
            ), 
            run_time = 3
        )
        self.wait()


        self.a_matrix, self.b_matrix = a_matrix, b_matrix
        self.a_matrix_label, self.b_matrix_label = a_matrix_label, b_matrix_label

    def calc_dot_product(self):
        a_matrix, b_matrix = self.a_matrix, self.b_matrix
        a_matrix_label, b_matrix_label = self.a_matrix_label, self.b_matrix_label


        dot_prod1 = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=", "4", "\\cdot", "1", "+", "3", "\\cdot", "2")\
            .next_to(self.matrix_group, DOWN, buff = 0.5)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .add_background_rectangle()
        dot_prod2 = MathTex("\\vec{a}", "\\cdot", "\\vec{b}", "=", "10")\
            .move_to(dot_prod1, aligned_edge = LEFT)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .add_background_rectangle()

        a_copy = a_matrix_label[0].copy()
        b_copy = b_matrix_label[0].copy()
        for copy in a_copy, b_copy:
            copy.generate_target()
        a_copy.target.move_to(dot_prod1[1])
        b_copy.target.move_to(dot_prod1[3])

        # bg, a * b = schreiben
        self.play(
            FadeIn(dot_prod1[0]),
            Write(dot_prod1[2]),
            *[MoveToTarget(vec) for vec in [a_copy, b_copy]],
            Write(dot_prod1[4]),
            run_time = 2
        )
        self.remove(a_copy, b_copy)
        self.add(dot_prod1[1], dot_prod1[3])

        # Path für Skalarprodukt
        path = VMobject()
        path.set_points_smoothly([
            a_matrix[0][0].get_center(), b_matrix[0][0].get_center(), a_matrix[0][1].get_center(), b_matrix[0][1].get_center()
        ])
        path.set_color(vec_c_color)
        path.set_stroke(width = 5)

        self.play(
            ShowPassingFlash(path, rate_func = smooth),
            ShowIncreasingSubsets(dot_prod1[5:], rate_func = linear), 
            run_time = 2
        )
        self.wait(0.5)

        # Transforming into result
        self.play(
            Transform(dot_prod1[0], dot_prod2[0]),
            Transform(dot_prod1[5:], dot_prod2[5]),
        )
        self.wait(2)

    def zoom_camera(self):
        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.set(width = config.frame_width * 0.77).move_to(1.7*RIGHT + 0.95*UP),
            run_time = 2
        )
        self.wait()

    def second_formula(self):

        angle = Arc(
            angle = angle_between_vectors(self.veca.get_vector(), self.vecb.get_vector()), start_angle = self.veca.get_angle(), 
            radius = 1, color = self.pro_color
        )

        tex_phi = MathTex("\\varphi")\
            .move_to(1*RIGHT + 1.25*UP)\
            .set_color(angle.get_color())\
            .add_background_rectangle()

        new_formula = MathTex(
            "\\vec{a}", "\\cdot", "\\vec{b}", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", 
            "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", 
            "\\cos", "(", "\\varphi", ")"
        )\
            .next_to(self.veca.get_end(), UP)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\varphi": self.pro_color})\
            .add_background_rectangle()


        self.play(
            LaggedStartMap(Create, VGroup(angle, tex_phi), lag_ratio = 0.25), 
            FadeIn(new_formula[0]),
            ShowIncreasingSubsets(VGroup(*new_formula[1:])), 
            run_time = 2
        )
        self.wait()

        self.play(Uncreate(angle), FadeOut(tex_phi))
        self.wait()

        self.new_formula = new_formula

    def projection_vectors(self):
        veca, vecb = self.veca, self.vecb

        pro_vec = self.pro_vec = self.get_pro_vector(veca, color = vec_c_color)
        pro_line = self.pro_line = self.get_pro_line(veca, color = WHITE)

        self.play(
            Create(pro_line),
            ReplacementTransform(vecb.copy(), pro_vec), 
            run_time = 2
        )
        self.wait()

        brace = Brace(Line(ORIGIN, 2*RIGHT), DOWN, buff = 0.6, color = GREY)
        brace.next_to(self.origin, RIGHT, buff = 0, aligned_edge = UL)
        brace.rotate(veca.get_angle(), about_point = self.origin)

        self.play(Create(brace))

        ba = brace.get_tex("\\vec{b}_", "{\\vec{a}}", buff = 0.1)\
            .set_color(vec_c_color)\
            .add_background_rectangle()

        ba_text = Tex("senkrechte Projektion \\\\ von ", "$\\vec{b}$", " auf ", "$\\vec{a}$")\
            .next_to(ba, RIGHT)\
            .shift(0.75*DOWN)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .add_background_rectangle()

        self.play(Create(ba))
        self.play(
            FadeIn(ba_text[0], run_time = 1), 
            Write(ba_text[1:], run_time = 2), 
        )
        self.wait()

        # Ausfaden von Projektionsgedöns
        self.play(
            LaggedStartMap(FadeOut, VGroup(ba_text[0], ba_text[1:], ba[0], ba[1:], brace), shift = DOWN, lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait()

    def length_of_projection_vector(self):
        angle = Arc(angle = angle_between_vectors(self.veca.get_vector(), self.vecb.get_vector()), start_angle = self.veca.get_angle(), radius = 1)
        angle.set_color(GREEN)
        self.play(Create(angle))
        self.wait(0.5)

        for vec in self.pro_vec, self.vecb:
            self.play(ApplyWave(vec), run_time = 1.5)
            self.wait(0.5)

        #                     0     1       2        3    4    5       6          7         8        9      10      11         12         13           14        15     16
        length1 = MathTex("\\cos", "(", "\\varphi", ")", "=", "{", "\\lvert", "\\vec{b}_", "{", "\\vec{a}", "}", "\\rvert", "\\over", "\\lvert", "\\vec{b}", "\\rvert", "}")\
            .move_to(4*RIGHT + UP)
        length1[2].set_color(self.pro_color)
        length1[7:10].set_color(vec_c_color)
        length1[14].set_color(vec_b_color)

        self.play(FadeIn(length1[:4]), run_time = 1)
        self.play(LaggedStartMap(FadeIn, VGroup(length1[4], length1[5:12], length1[12], length1[13:]), lag_ratio = 0.4), run_time = 3)
        self.wait()


        #                     0                1                2       3       4           5          6         7         8      9       10      11
        length2 = MathTex("\\lvert", "\\vec{b}_{\\vec{a}}", "\\rvert", "=", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\cos", "(", "\\varphi", ")")\
            .move_to(4*RIGHT + DOWN)
        length2[1].set_color(vec_c_color)
        length2[5].set_color(vec_b_color)
        length2[10].set_color(self.pro_color)


        phi_copy, b_copy, ba_copy = length1[:4].copy(), length1[13:16].copy(), length1[6:12].copy()
        targets = [length2[8:], length2[4:7], length2[:3]]
        for element, target in zip([phi_copy, b_copy, ba_copy], targets):
            element.generate_target()
            element.target.move_to(target)

        self.play(
            LaggedStartMap(MoveToTarget, VGroup(phi_copy, b_copy, ba_copy), lag_ratio = 0.5, run_time = 5),
            LaggedStartMap(Create, VGroup(length2[3], length2[7]), lag_ratio = 0.75, run_time = 3),
        )
        self.wait()


        sur_rects = VGroup(*[
            SurroundingRectangle(mob).set_color(vec_c_color)
            for mob in [self.new_formula[9:], length2[4:]]
        ])

        self.play(Create(sur_rects), lag_ratio = 0.15, run_time = 2)
        self.wait()

        vector_texs = VGroup(*[
            Tex(tex)\
                .scale(0.5)\
                .rotate(self.veca.get_angle())\
                .set_color(color = color)\
                .next_to(vec.get_end(), direction = DL)\
                .shift(0.25*DOWN)
            for tex, color, vec in zip(
                ["Vektor $\\vec{a}$", "Projektionsvektor $\\vec{b}_{\\vec{a}}$"], 
                [vec_a_color, vec_c_color], 
                [self.veca, self.pro_vec]
            )
        ])

        self.bring_to_front(
            self.veca, self.vecb, self.pro_vec, self.pro_line,
            self.new_formula, sur_rects
        )

        self.curr_mobs = Group(*self.mobjects[:-11])
        self.play(
            FadeOut(self.curr_mobs, run_time = 4), 
            *[Write(text, rate_func = squish_rate_func(smooth, 0.5, 0.8)) for text in vector_texs]
        )
        self.wait()


        self.play(FadeOut(vector_texs[0], target_position = self.new_formula[5]), run_time = 1.5)
        self.play(FadeOut(vector_texs[1], target_position = self.new_formula[7:]), run_time = 2)
        self.wait()

        self.remove(length2[0])
        self.play(
            FadeIn(self.plane), 
            FadeOut(sur_rects, length2[3], length2[7], length2[11], phi_copy, b_copy, ba_copy),
            run_time = 2
        )

        self.bring_to_back(self.plane)
        self.wait()

    def projection_rectangle(self):
        # rotate pro_vec 90 Degrees + Rectangle
        pro_vec_rot = self.pro_vec_rot = self.get_pro_vector_rotate(self.veca, color = self.pro_vec.get_color())

        self.play(ReplacementTransform(self.pro_vec.copy(), pro_vec_rot, path_arc = -PI/2), run_time = 5)
        self.wait()

        square = Square(stroke_color = BLACK, stroke_width = 1, fill_color = self.rect_color, fill_opacity = 0.4)
        square.replace(
            VGroup(*[
                VectorizedPoint(self.plane.coords_to_point(i, i))
                for i in (0, 1)
            ]),
            stretch = True
        )

        unit_areas = VGroup(*[
            square.copy().move_to(
                self.plane.coords_to_point(x, y),
                DOWN+LEFT
            )
            for x in range(int(np.linalg.norm(self.veca.get_vector())))
            for y in range(int(np.linalg.norm(self.pro_vec.get_vector())))
        ])\
            .set_color(self.rect_color)\
            .set_stroke(opacity = 0.75)\
            .next_to(self.origin, RIGHT, buff = 0, aligned_edge = UL)\
            .rotate(angle = self.veca.get_angle(), about_point = self.origin)

        self.play(LaggedStartMap(DrawBorderThenFill, unit_areas, lag_ratio = 0.05), run_time = 3)
        self.bring_to_front(self.veca, self.pro_line, self.pro_vec, pro_vec_rot)
        self.wait()


        # Rotate pro_vec und veca --> show their length
        for vec in self.pro_line, self.pro_vec:
            vec.suspend_updating()

        # rate_func = there_and_back_with_pause doesn't work
        for angle in [-36.87*DEGREES, 36.87*DEGREES]:
            self.play(*[
                Rotating(vec, radians = angle, about_point = self.origin, rate_func = there_and_back_with_pause, run_time = 1.75)
                for vec in [self.pro_vec, self.veca]
            ])
            self.wait()


        for vec in self.pro_line, self.pro_vec:
            vec.resume_updating()


        pro_rect = self.pro_rect = self.get_dot_prod_rectangle(self.veca, color = BLUE_E, opacity = 0.4)
        self.play(
            LaggedStartMap(FadeOut, unit_areas), 
            FadeIn(pro_rect),
            run_time = 3
        )
        self.bring_to_front(self.veca, self.pro_line, self.pro_vec, pro_vec_rot)
        self.wait()


        # updaters
        pro_vec, pro_line = self.pro_vec, self.pro_line
        veca, vecb = self.veca, self.vecb
        xval, yval = self.xval, self.yval

        vecb.add_updater(lambda v: v.become(
            self.get_vector([xval.get_value(),yval.get_value(),0], color = vec_b_color)
        ))
        pro_vec.add_updater(lambda v: v.become(
            self.get_pro_vector(veca, color = vec_c_color)
        ))
        pro_line.add_updater(lambda v: v.become(
            self.get_pro_line(veca, color = WHITE)
        ))

        pro_vec_rot.add_updater(lambda r: r.become(
            self.get_pro_vector_rotate(self.veca, color = self.pro_vec.get_color())
        ))
        pro_rect.add_updater(lambda r: r.become(
            self.get_dot_prod_rectangle(self.veca, color = BLUE_E, opacity = 0.4)
        ))

        # self.bring_to_front(self.vecb)

    def varying_rectangles(self):

        bg_rect = Rectangle(width = 5, height = 1.75, color=BLACK, stroke_width=0, stroke_opacity=0, fill_opacity=0.75)
        bg_rect.move_to(self.a_matrix, aligned_edge=LEFT)
        self.a_matrix[0].set_color(vec_a_color)

        self.play(
            Restore(self.camera.frame), 
            self.xval.animate.set_value(-2), 
            self.yval.animate.set_value(1),
            Create(bg_rect, rate_func = squish_rate_func(smooth, 0, 0.3)), 
            Write(self.a_matrix, rate_func = squish_rate_func(smooth, 0, 0.3)),
            run_time = 4
        )
        self.wait()


        x_values = [-2, -5, 1.5,  3, 4]
        y_values = [ 1,  0,  -2, -1, 3]

        cdot = MathTex("\\cdot").set_color(self.pro_color).next_to(self.a_matrix, RIGHT)
        b_matrizes = VGroup(*[
            Matrix([[str(x_value)], [str(y_value)]], **self.mat_kwargs).next_to(cdot, RIGHT)
            for x_value, y_value in zip(x_values, y_values)
        ])
        for matrix in b_matrizes:
            matrix[0].set_color(vec_b_color)
        equals = MathTex("=").next_to(b_matrizes, RIGHT)


        self.play(
            FadeIn(cdot, shift = UP), 
            TransformFromCopy(self.vecb, b_matrizes[0]),
            run_time = 2
        )
        self.wait()
        self.play(Write(equals))
        self.wait()


        results_list = [round(4*x_value + 3*y_value, 0) for x_value, y_value in zip(x_values, y_values)]
        results = VGroup(*[
            MathTex(str(result)).next_to(equals, RIGHT).set_color(vec_c_color)
            for result in results_list
        ])
        self.play(Write(results[0]))
        self.wait()


        # for obj in self.pro_line, self.pro_vec, self.pro_vec_rot, self.pro_rect:
        #     obj.suspend_updating()

        self.pro_rect.clear_updaters()

        self.play(Rotating(self.pro_rect, radians = -1 * self.veca.get_angle(), about_point = self.origin, rate_func = smooth, run_time = 3))
        self.wait()
        self.play(Rotating(self.pro_rect, radians = self.veca.get_angle(), about_point = self.origin, rate_func = smooth, run_time = 3))
        self.wait()

        self.pro_rect.add_updater(lambda r: r.become(
            self.get_dot_prod_rectangle(self.veca, color = BLUE_E, opacity = 0.4)
        ))

        # for obj in self.pro_line, self.pro_vec, self.pro_vec_rot, self.pro_rect:
        #     obj.resume_updating()

        for x, y, index in zip(x_values[1:], y_values[1:], range(len(b_matrizes))):
            self.play(
                self.xval.animate.set_value(x),
                self.yval.animate.set_value(y),
                Transform(b_matrizes[0], b_matrizes[index + 1], rate_func = squish_rate_func(smooth, 0.5, 1)),
                run_time = 4
            )
            self.wait()
            self.play(Transform(results[0], results[index + 1]))
            self.wait()
        self.wait(3)

    def varying_vectors(self):
        xval, yval = self.xval, self.yval

        # verschiedene Projektionen zeigen
        xval_list = [0.5, 4, 4, 1.5, -1,-3, 1]
        yval_list = [3.5, 3, 1,  -2, -2, 1, 2]
        runtime_list = [3,4,3,5,3,3,3]
        for xvalue, yvalue, runtime in zip(xval_list, yval_list, runtime_list):
            self.play(
                xval.animate.set_value(xvalue), 
                yval.animate.set_value(yvalue), 
                run_time = runtime
            )
            self.wait()


class ProjectionIn3d(ThreeDScene):
    def construct(self):
        axes = self.axes = ThreeDAxes()
        origin = axes.c2p(0,0,0)

        x_tex = MathTex("x").next_to(axes.x_axis, RIGHT)
        y_tex = MathTex("y").next_to(axes.y_axis, UP)
        z_tex = MathTex("z")\
            .rotate(angle = 90*DEGREES, axis = RIGHT)\
            .next_to(axes.c2p(0,0,4), UP)

        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)

        self.cone_height = 0.25
        self.vec_3d_kwargs = {
            "start": origin,
            "base_radius": 0.125, 
            "height": self.cone_height
        }
        self.mat_kwargs = {
            "v_buff": 0.6,
            "bracket_v_buff": 0.1,
            "left_bracket": "(",
            "right_bracket": ")",
        }

        line_through_OA = Line3D(start = axes.c2p(6,-4,4), end = axes.c2p(-9,6,-6), thickness = 0.01, color = GREY)

        arrow_a = Arrow3D(end = axes.c2p(3,-2,2), color = vec_a_color, **self.vec_3d_kwargs)
        arrow_b = Arrow3D(end = axes.c2p(-3,4,1), color = vec_b_color, **self.vec_3d_kwargs)
        arrow_pro = self.get_pro_vector(arrow_a, arrow_b, color = vec_c_color)

        arrow_a_comp = self.get_component_lines(arrow_a)
        arrow_b_comp = self.get_component_lines(arrow_b)
        line_pro = self.get_pro_line(arrow_a, arrow_b)

        mat_a = Matrix([[3], [-2], [2]], **self.mat_kwargs)\
            .move_to(4*LEFT + 2.75*UP)
        mat_b = Matrix([[-3], [4], [1]], **self.mat_kwargs)\
            .move_to(5*RIGHT + 2.75*UP)

        dot_a = Dot3D(point = axes.c2p(3,-2,2))
        dot_b = Dot3D(point = axes.c2p(-3,4,1))


        # Matrizen, Achse, Komponente und Vektoren hinzufügen
        self.add_fixed_in_frame_mobjects(mat_a, mat_b)
        self.wait()
        self.play(
            LaggedStartMap(Create, VGroup(*axes, x_tex, y_tex, z_tex), lag_ratio = 0.25),
            run_time = 3
        )
        self.play(
            LaggedStartMap(Create, VGroup(*arrow_a_comp, *arrow_b_comp, dot_a, dot_b), lag_ratio = 0.05),
            run_time = 3
        )
        self.play(*[Create(arrow) for arrow in [arrow_a, arrow_b]], run_time = 3)
        self.wait()

        # Projektion von Vector b auf Vector a
        self.play(
            FadeIn(line_through_OA),
            Create(line_pro), 
            run_time = 4
        )
        self.play(ReplacementTransform(arrow_b.copy(), arrow_pro), run_time = 5)
        self.play(FadeOut(line_through_OA))
        self.wait(2)


        # Vector b in neuen Vektor transformieren
        mat_b_new = Matrix([[1], [-1], [4]], **self.mat_kwargs)\
            .move_to(5*RIGHT + 2.75*UP)
        arrow_b_new = Arrow3D(end = axes.c2p(1,-1,4), color = vec_b_color, **self.vec_3d_kwargs)
        arrow_b_comp_new = self.get_component_lines(arrow_b_new)
        arrow_pro_new = self.get_pro_vector(arrow_a, arrow_b_new, color = vec_c_color)
        line_pro_new = self.get_pro_line(arrow_a, arrow_b_new)
        dot_b_new = Dot3D(point = axes.c2p(1,-1,4))
        self.play(
            FadeOut(mat_b, shift = RIGHT),
            Transform(arrow_b, arrow_b_new),
            Transform(arrow_b_comp, arrow_b_comp_new),
            Transform(arrow_pro, arrow_pro_new), 
            Transform(line_pro, line_pro_new),
            Transform(dot_b, dot_b_new),
            run_time = 6
        )
        self.wait()
        self.add_fixed_in_frame_mobjects(mat_b_new)
        self.wait(3)

        # Projektions-Vektor um 90 Grad drehen --> Drehachse = Normalenvektor(vec_a, vec_b_new)
        # Rotatio not working, dont know why

        # dot_proj_vector = Dot3D(point = axes.c2p(2.2941, -1.5294, 1.5294))
        # dot_rota_vector = Dot3D(point = axes.c2p(1.4373, -0.5880, -2.7440))

        arrow_pro_rotate = Arrow3D(end = axes.c2p(1.4373, -0.5880, -2.7440), color = vec_c_color, **self.vec_3d_kwargs)

        arrow_pro_copy = arrow_pro.copy().clear_updaters()
        rot_kwargs = {"radians": 90*DEGREES, "axis": axes.c2p(*axes.p2c(6*RIGHT + 10*UP + 1*OUT)), "about_point": origin, "rate_func": smooth, "run_time": 5}
        self.play(
            *[FadeOut(comp, run_time = 1.5) for comp in [arrow_a_comp, arrow_b_comp]],
            # Rotating(arrow_pro_copy, **rot_kwargs),
            Transform(
                arrow_pro_copy, arrow_pro_rotate, 
                # path_arc = PI, # path_arc_axis = axes.c2p(*axes.p2c(6*RIGHT + 10*UP + 1*OUT)),
                rate_func = smooth, run_time = 5
            ),
        )
        self.wait(3)


        arrow_a_end = arrow_a.get_end() + self.cone_height * arrow_a.get_direction()
        arrow_pro_rotate_end = arrow_pro_rotate.get_end() + self.cone_height * arrow_pro_rotate.get_direction()


        points_rect = [[
            axes.c2p(*axes.p2c([0,0,0])),
            axes.c2p(*axes.p2c(arrow_a_end)),
            axes.c2p(*axes.p2c(arrow_a_end + arrow_pro_rotate_end)),
            axes.c2p(*axes.p2c(arrow_pro_rotate_end))
        ]]
        rect = VGroup()
        for v in points_rect:
            face = ThreeDVMobject()
            face.set_points_as_corners([v[0], v[1], v[2], v[3], v[0]])
            rect.add(face)
        rect.set_stroke(width = 1)
        rect.set_fill(color = BLUE_E, opacity = 0.5)
        self.add(rect)
        self.play(DrawBorderThenFill(rect), run_time = 4)
        self.wait()


        # Rotating
        self.play(*[
            Rotating(
                mob, radians = TAU, axis = arrow_a.get_end() - arrow_a.get_start(), about_point = origin, 
                rate_func = linear, run_time = 10
            ) 
            for mob in [rect, arrow_pro_rotate]
        ])
        self.wait(3)




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

    def get_pro_vector(self, arrow3d_1, arrow3d_2, **kwargs):
        vec1 = arrow3d_1.get_end() + self.cone_height * arrow3d_1.get_direction() - arrow3d_1.get_start()
        vec2 = arrow3d_2.get_end() + self.cone_height * arrow3d_2.get_direction() - arrow3d_2.get_start()

        axes = self.axes
        return Arrow3D(
            end = np.dot(axes.p2c(vec1), axes.p2c(vec2))/np.linalg.norm(axes.p2c(vec1))**2 * axes.c2p(*axes.p2c(vec1)), 
            **self.vec_3d_kwargs, 
            **kwargs
        )

    def get_pro_line(self, arrow3d_1, arrow3d_2, **kwargs):
        vec1 = arrow3d_1.get_end() + self.cone_height * arrow3d_1.get_direction() - arrow3d_1.get_start()
        vec2 = arrow3d_2.get_end() + self.cone_height * arrow3d_2.get_direction() - arrow3d_2.get_start()

        axes = self.axes
        start = vec2
        end = np.dot(axes.p2c(vec1), axes.p2c(vec2))/np.linalg.norm(axes.p2c(vec1))**2 * axes.c2p(*axes.p2c(vec1))

        return Line3D(start, end, **kwargs)


class TwoEquations(Calculations):
    def construct(self):
        self.dot_color = vec_c_color
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1,
        }

        self.setup_scene()
        self.multiply_components()
        self.multiply_lengths_cos()
        self.why_are_they_equal()



    def setup_scene(self):
        equa_sp = MathTex("\\vec{a}", "\\cdot", "\\vec{b}")
        equa_sp.scale(1.5)
        equa_sp.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\cdot": vec_c_color})

        text_sp = Tex("Skalar","produkt")
        text_sp.scale(1.5)
        text_sp.next_to(equa_sp, RIGHT, buff = 0.5)
        text_sp.shift(0.15*DOWN)
        text_sp[0].set_color(vec_c_color)

        self.play(
            AnimationGroup(
                Write(equa_sp),
                Write(text_sp),
                lag_ratio = 0.25
            ), 
            run_time = 2
        )
        self.wait()

        self.eq_sp, self.text_sp = equa_sp, text_sp

    def multiply_components(self):
        matrix_a = Matrix([["a_x"], ["a_y"], ["a_z"]], **self.mat_kwargs)
        matrix_b = Matrix([["b_x"], ["b_y"], ["b_z"]], **self.mat_kwargs)
        matrix_group = self.group_vecs_with_symbol(matrix_a, matrix_b, type = "dot")
        matrix_group.to_corner(UL, buff = 1)

        x = MathTex("a_x", "\\cdot", "b_x")
        y = MathTex("a_y", "\\cdot", "b_y")
        z = MathTex("a_z", "\\cdot", "b_z")
        matrix_result = MobjectMatrix([[x], [y], [z]], **self.mat_kwargs)
        matrix_result.next_to(matrix_group, RIGHT, buff = 1)

        result = MathTex("=", "a_x", "\\cdot", "b_x", "+", "a_y", "\\cdot", "b_y", "+", "a_z", "\\cdot", "b_z")\
            .next_to(matrix_group, RIGHT)

        # Coloring
        for matrix, color in zip([matrix_a, matrix_b], [vec_a_color, vec_b_color]):
            matrix[0].set_color(color)

        for comp in x,y,z:
            comp[0].set_color(vec_a_color)
            comp[2].set_color(vec_b_color)

        result.set_color_by_tex_to_color_map({
                    "a_x": vec_a_color, "a_y": vec_a_color, "a_z": vec_a_color,
                    "b_x": vec_b_color, "b_y": vec_b_color, "b_z": vec_b_color,
                })

        self.play(
            AnimationGroup(
                *[TransformFromCopy(self.eq_sp[index], matrix_group[index], path_arc = -PI/2) for index in range(3)],
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformFromCopy(matrix_group[0][0][0], matrix_result[0][0][0]),
                    TransformFromCopy(matrix_group[1], matrix_result[0][0][1]),
                    TransformFromCopy(matrix_group[2][0][0], matrix_result[0][0][2]),
                    lag_ratio = 0
                ),

                AnimationGroup(
                    TransformFromCopy(matrix_group[0][0][1], matrix_result[0][1][0]),
                    TransformFromCopy(matrix_group[1], matrix_result[0][1][1]),
                    TransformFromCopy(matrix_group[2][0][1], matrix_result[0][1][2]),
                    lag_ratio = 0
                ),

                AnimationGroup(
                    TransformFromCopy(matrix_group[0][0][2], matrix_result[0][2][0]),
                    TransformFromCopy(matrix_group[1], matrix_result[0][2][1]),
                    TransformFromCopy(matrix_group[2][0][2], matrix_result[0][2][2]),
                    lag_ratio = 0
                ),
                lag_ratio = 0.4
            ),
            run_time = 3
        )
        self.wait()


        self.play(
            ReplacementTransform(matrix_result[0][0], result[1:4]), 
            ReplacementTransform(matrix_result[0][1], result[5:8]), 
            ReplacementTransform(matrix_result[0][2], result[9:]), 
            run_time = 1
        )
        self.play(LaggedStartMap(FadeIn, VGroup(result[0], result[4], result[8]), shift = UP, lag_ratio = 0.2))
        self.wait()


        self.matrix_group, self.result = matrix_group, result

    def multiply_lengths_cos(self):

        matrix_group2 = self.matrix_group.copy()
        matrix_group2.to_corner(DL, buff = 1)

        #                   0       1          2            3         4         5           6         7           8        9     10       11      12
        cos_term = MathTex("=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\cos", "(", "\\varphi", ")")
        cos_term.set_color_by_tex_to_color_map({
                    "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\varphi": GREEN
                })
        cos_term.next_to(matrix_group2, RIGHT)

        self.play(
            AnimationGroup(
                *[TransformFromCopy(self.eq_sp[index], matrix_group2[index], path_arc = PI/2) for index in range(3)],
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()


        self.play(
            AnimationGroup(
                TransformFromCopy(matrix_group2[0], cos_term[1:4]),
                TransformFromCopy(matrix_group2[2], cos_term[5:8]),
                FadeIn(cos_term[9:], shift = LEFT),
                lag_ratio = 0.2
            ), 
            run_time = 2
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, VGroup(cos_term[0], cos_term[4], cos_term[8]), shift = UP, lag_ratio = 0.2))
        self.wait(2)


        self.cos_term = cos_term

    def why_are_they_equal(self):

        sur_rects = VGroup(*[
            SurroundingRectangle(eq, color = vec_c_color)
            for eq in [self.result[1:], self.cos_term[1:]]
        ])

        self.play(
            TransformFromCopy(self.text_sp[0], sur_rects[0]), 
            run_time = 2
        )
        self.wait(0.5)


        self.play(
            TransformFromCopy(self.text_sp[0], sur_rects[1]), 
            run_time = 2
        )
        self.wait(3)


class Thumbnail_Geo(DotProdRectangle):
    def construct(self):

        self.plane_config = {
            "axis_config": {"stroke_color": GREY}, "background_line_style": {"stroke_opacity": 0.6, "stroke_color": GREY}
        }
        self.pro_color = GREEN
        self.rect_color = BLUE_E
        self.x_value = 1
        self.y_value = 2
        self.z_value = 0
        self.vector_stat = [4,3,0]
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1,
        }

        self.setup_scene()
        self.calc_dot_product()
        self.zoom_camera()
        self.second_formula()
        self.projection_vectors()
        self.length_of_projection_vector()
        self.projection_rectangle()


        square = Square(stroke_color = BLACK, stroke_width = 1, fill_color = self.rect_color, fill_opacity = 0.4)
        square.replace(
            VGroup(*[
                VectorizedPoint(self.plane.coords_to_point(i, i))
                for i in (0, 1)
            ]),
            stretch = True
        )

        unit_areas = VGroup(*[
            square.copy().move_to(
                self.plane.coords_to_point(x, y),
                DOWN+LEFT
            )
            for x in range(int(np.linalg.norm(self.veca.get_vector())))
            for y in range(int(np.linalg.norm(self.pro_vec.get_vector())))
        ])\
            .set_color(self.rect_color)\
            .set_stroke(opacity = 0.75)\
            .next_to(self.origin, RIGHT, buff = 0, aligned_edge = UL)\
            .rotate(angle = self.veca.get_angle(), about_point = self.origin)

        self.play(LaggedStartMap(DrawBorderThenFill, unit_areas, lag_ratio = 0.05), run_time = 3)


        title2 = Tex("Skalarprodukt")\
            .set_color_by_gradient(vec_a_color, ORANGE, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 3)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1)\
            .shift(0.5*LEFT)

        title1 = Tex("Interpretation")\
            .set_color(vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 2)\
            .set(width = 5.25)\
            .add_background_rectangle()\
            .next_to(title2, UP, aligned_edge=LEFT)

        title0 = Tex("geometrische")\
            .set_color(vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 2)\
            .set(width = 4.75)\
            .add_background_rectangle()\
            .next_to(title1, UP, aligned_edge=LEFT)

        self.new_formula.scale(1.5).next_to(title1, UP, buff = 3, aligned_edge=LEFT)

        self.remove(self.a_matrix, self.pro_rect)
        self.add(title0, title1, title2) # bg_rect, self.a_matrix, cdot, b_matrix, equals, result


        self.bring_to_front(unit_areas, self.veca, self.pro_line, self.pro_vec, self.pro_vec_rot)

        self.play(Restore(self.camera.frame))
        self.wait()







# Orthogonale Vektoren
class ProvingOrthogonalVectors(Scene):
    def construct(self):
        pass 


class RightTriangle(Scene):
    def construct(self):
        pass


class RightTriangle3D(ThreeDScene):
    def construct(self):

        self.coords_a, self.coords_b, self.coords_c = [2,2,0], [1,4,2], [-1,4,0.5]
        self.dot_kwargs = {"radius": 0.07, "color": WHITE}

        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)


        point_a, point_b, point_c = axes.c2p(*self.coords_a), axes.c2p(*self.coords_b), axes.c2p(*self.coords_c)
        dots = VGroup(*[Dot3D(point, **self.dot_kwargs) for point in [point_a, point_b, point_c]])
        triangle = ThreeDVMobject()\
            .set_points_as_corners([point_a, point_b, point_c, point_a])\
            .set_fill(color = BLUE_E, opacity = 0.25)\
            .set_stroke(color = BLUE_E)


        self.add(axes, dots, triangle)


class SquarePyramidScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        vertex_coords = [
            axes.c2p(*[1, 1, -2]),
            axes.c2p(*[1, -1, -2]),
            axes.c2p(*[-1, -1, -2]),
            axes.c2p(*[-1, 1, -2]),
            axes.c2p(*[0, 0, 2])
        ]
        faces_list = [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 1, 2, 3]
        ]
        pyramid = Polyhedron(vertex_coords, faces_list)
        self.add(pyramid)





























class Numline(Scene):
    def construct(self):
        title1 = Tex("Zahlenstrahl")
        title2 = Tex("Zahlengerade")

        for title in title1, title2:
            title.scale(1.75)
            title.to_edge(UP)
            title.set_color_by_gradient(BLUE, YELLOW, RED)
            title.set_fill(color = GREY, opacity = 0.4)
            title.set_stroke(width = 1)


        line_pure = NumberLine(x_range = [0,5.9,1], include_numbers = False, include_tip = False)
        line_num_tip = NumberLine(x_range = [0,5.9,1], include_numbers = False, include_tip = True)

        for line in line_pure, line_num_tip:
            line.next_to(np.array([0,0,0]), RIGHT, buff = 0)

        labels_pos = VGroup(*[
            MathTex(number).scale(0.75).next_to(line_pure.n2p(number), DOWN)
            for number in range(6)
        ])

        self.play(
            AnimationGroup(
                Write(title1),
                Create(line_num_tip),
                FadeIn(labels_pos, shift = UP, lag_ratio = 0.1), 
                lag_ratio = 0.3
            ), 
            run_time = 4
        )
        self.add(line_pure)
        self.wait()


        # Rotation
        self.play(
            Rotating(line_pure.copy(), radians = TAU/2, about_point = line_pure.n2p(0), run_time = 5, rate_func = smooth), 
            rate_func = smooth
        )
        self.wait()
        self.play(Transform(title1, title2))
        self.play(Circumscribe(title1, color = BLUE, time_width = 0.75, run_time = 3))
        self.wait()


        labels_neg = VGroup(*[
            MathTex(number).scale(0.75).next_to(line_pure.n2p(number), DOWN)
            for number in [0,-1,-2,-3,-4,-5]
        ])

        for x in range(len(labels_pos)):
            self.play(
                TransformFromCopy(labels_pos[x], labels_neg[x], path_arc = 60*DEGREES), 
                run_time = 2
            )
            self.wait()
        self.wait()


        val = ValueTracker(2)
        arrow = Arrow(line_pure.n2p(val.get_value()) + UP, line_pure.n2p(val.get_value()), buff = 0, color = TEAL)
        dec = DecimalNumber(val.get_value(), num_decimal_places=1).next_to(arrow, UP)


        self.play(
            GrowArrow(arrow), 
            Write(dec), 
            run_time = 2
        )
        self.wait()

        arrow.add_updater(lambda h: h.become(
            Arrow(line_pure.n2p(val.get_value()) + UP, line_pure.n2p(val.get_value()), buff = 0, color = TEAL)
        ))
        dec.add_updater(lambda dec: dec.set_value(val.get_value()).next_to(arrow, UP))


        values = [-3, -1.5, 4.3, -4.8, 0.4, -2.6]
        for value in values:
            self.play(
                val.animate.set_value(value), 
                run_time = 3
            )
            self.wait()

        self.wait()





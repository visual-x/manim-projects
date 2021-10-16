from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE


class Calculations(Scene):
    def construct(self):
        pass
        # self.mat_kwargs = {
        #     "v_buff": 0.6, 
        #     "left_bracket": "(", 
        #     "right_bracket": ")",
        #     "bracket_v_buff": 0.1
        # }

    def get_vector_matrix_from_num_vec(self, num_vec, dimension = 3, **mat_kwargs):
        if dimension == 3:
            mat = Matrix([[num_vec[0]], [num_vec[1]], [num_vec[2]]], **mat_kwargs)
        elif dimension == 2:
            mat = Matrix([[num_vec[0]], [num_vec[1]]], **mat_kwargs)

        return mat

    def group_vecs_with_symbol(self, mat_a, mat_b, type = "dot", color = WHITE):
        if type is "dot":
            mult = MathTex("\\cdot").set_color(color)
        elif type is "bullet":
            mult = MathTex("\\bullet").set_color(color)
        elif type is "cdot":
            mult = MathTex("\\cdot").set_color(color)
        else:
            mult = MathTex("\\times").set_color(color)

        group = VGroup(mat_a, mult, mat_b)
        group.arrange_submobjects(RIGHT)

        return group

    def get_dotproduct_path(self, vec_group, dimension = 3, color = LIGHT_BROWN, stroke_width = 5):
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
            path.set_color(color).set_stroke(width = stroke_width)

        return path_x, path_y, path_z

    def get_crossproduct_cut_lines(self, vec_group, color, line_buff = 0.1):
        line_buff = 0.1
        if color is None:
            color = LIGHT_BROWN

        lines = VGroup(*[
            Line(
                vec_group.get_left() + line_buff * LEFT, vec_group.get_right() + line_buff * RIGHT, 
                color = color, stroke_width = 5
            )
            for x in range(3)
        ])
        lines.arrange_submobjects(DOWN, buff = self.mat_kwargs.get("v_buff"))
        lines.move_to(vec_group)

        return lines

    def get_lines_for_comp_calc(self, vec_group, comp1, comp2, **kwargs):
        line1 = Line(
            start = vec_group[0][0][comp1].get_right(), 
            end = vec_group[2][0][comp2].get_left(),
            **kwargs
        )
        line2 = Line(
            start = vec_group[0][0][comp2].get_right(),
            end = vec_group[2][0][comp1].get_left(),
            **kwargs
        )

        lines = VGroup(line1, line2)

        return lines


class ProjectionScene(VectorScene):
    def constuct(self):
        pass

    def get_plane(self, **kwargs):
        self.plane = NumberPlane(**kwargs)
        self.plane.add_coordinates()
        self.origin = self.plane.c2p(0,0)

        return self.plane

    def get_vecs_from_nums(self, vec_a_num, vec_b_num):
        return VGroup(*[
            self.get_vector(vec_num, color = color)
            for vec_num, color in zip([vec_a_num, vec_b_num], [vec_a_color, vec_b_color])
        ])

    def get_parallelogramm_from_vecs(self, vec_a, vec_b, fill_opacity = 0.25):
        parallelo = VMobject()\
            .set_points_as_corners([
                vec_a.get_start(), vec_a.get_end(), vec_a.get_end() + vec_b.get_end(), vec_b.get_end(), vec_b.get_start()
            ])\
            .set_fill(color = vec_c_color, opacity = fill_opacity)\
            .set_stroke(color = BLUE, width = 2)

        return parallelo

    def get_projection_vec(self, num_vec_a, num_vec_b, **kwargs):
        cross_prod_value = np.dot(num_vec_a, num_vec_b)
        cross_prod_norm = cross_prod_value / np.linalg.norm(num_vec_a)**2

        start = self.origin
        end = self.plane.c2p(*[cross_prod_norm * x for x in num_vec_a])

        projection_vec = Arrow(start, end, buff = 0, **kwargs)

        return projection_vec

    def get_projection_line(self, num_vec_a, num_vec_b, **kwargs):
        pro_vec = self.get_projection_vec(num_vec_a, num_vec_b)

        line = Line(
            start = self.plane.c2p(*num_vec_b),
            end = pro_vec.get_end(),
            **kwargs
        )

        return line


# SCENES CALCULATION

class Definition(Calculations):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6,
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.cut_color = MAROON
        self.com_color = ORANGE
        self.path_color = LIGHT_BROWN

        self.vec_a_num = [1, 2, -1]
        self.vec_b_num = [3, 0,  2]


        self.setup_scene()
        self.crosspath_animation()
        self.cross_vector_calculations()
        self.cut_lines_for_calculations()
        self.prepare_for_next_scene()


    def setup_scene(self):
        vec_a_num, vec_b_num = self.vec_a_num, self.vec_b_num
        mat_a = Matrix([[vec_a_num[0]], [vec_a_num[1]], [vec_a_num[2]]], **self.mat_kwargs)
        mat_b = Matrix([[vec_b_num[0]], [vec_b_num[1]], [vec_b_num[2]]], **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type = "times", color = vec_c_color)
        vec_group.move_to(np.array([3.12092922, 0, 0]))

        name = Tex("Kreuz","produkt")
        name[0].set_color(vec_c_color)
        name.move_to(np.array([3.12092922, 1.592528, 0]))

        self.add(vec_group, name)
        self.wait(2)

        self.play(
            AnimationGroup(
                vec_group.animate.move_to(np.array([-3.5, 0, 0])), 
                name.animate.move_to(np.array([-3.5, 1.592528, 0])), 
                lag_ratio = 0.15
            ),
            run_time = 3
        )
        self.wait()

        self.vec_group, self.name = vec_group, name

    def crosspath_animation(self):
        equals1 = MathTex("=").next_to(self.vec_group, RIGHT)

        path_cross1, path_cross2, path_cross3 = self.get_crossproduct_path_xyz(self.vec_group, color = self.path_color, stroke_width = 7)
        cross_res = np.cross(self.vec_a_num, self.vec_b_num)
        cross_vec = Matrix([[cross_res[0]], [cross_res[1]], [cross_res[2]]], **self.mat_kwargs)\
            .next_to(equals1, RIGHT)


        self.play(
            Write(equals1), 
            FadeIn(cross_vec[1:], lag_ratio = 0.1, shift = 0.5*UP),
        )
        self.wait() 

        self.play(ShowPassingFlash(path_cross1, time_width = 0.5), rate_func = linear, run_time = 2)
        self.play(
            Write(cross_vec[0][0], run_time = 0.75)
        )

        self.play(ShowPassingFlash(path_cross2, time_width = 0.5), rate_func = linear, run_time = 2)
        self.play(Write(cross_vec[0][1]), run_time = 0.75)


        self.play(ShowPassingFlash(path_cross3, time_width = 0.5), rate_func = linear, run_time = 2)
        self.play(Write(cross_vec[0][2]), run_time = 0.75)
        self.wait()

        self.equals1, self.cross_vec = equals1, cross_vec

    def cross_vector_calculations(self):
        x1, xm, x2 = MathTex("(", "2", "\\cdot", "2"),  MathTex("(", "-", ")"), MathTex("(", "-1", ")", "\\cdot", "0")
        y1, ym, y2 = MathTex("-1", "\\cdot", "3"), MathTex("1", "-", "1"), MathTex("1", "\\cdot", "2")
        z1, zm, z2 = MathTex("1", "\\cdot", "0"),  MathTex("1", "-", "1"), MathTex("2", "\\cdot", "3")

        x1[0].set_color(BLACK)
        for minus in xm, ym, zm:
            minus[0::2].set_color(BLACK)

        cross_calc = MobjectMatrix([[x1, xm, x2], [y1, ym, y2], [z1, zm, z2]], **self.mat_kwargs, element_alignment_corner=DOWN)
        cross_calc.next_to(self.equals1, RIGHT)
        cross_calc[1:].set_color(DARK_GREY)

        equals2 = self.equals1.copy()\
            .next_to(cross_calc, RIGHT)

        self.equals2, self.cross_calc = equals2, cross_calc

    def cut_lines_for_calculations(self):
        path_cross1, path_cross2, path_cross3 = self.get_crossproduct_path_xyz(self.vec_group, color = self.path_color, stroke_width = 7)

        # Name & Klammern dunkel machen, Lösungsvektor verschieben
        self.play(
            LaggedStartMap(
                FadeToColor, VGroup(self.name[1], self.vec_group[0][1:], self.vec_group[2][1:]), color = DARK_GREY,
                lag_ratio = 0.15
            ), 
            self.cross_vec.animate.next_to(self.equals2, RIGHT).set_color(DARK_GREY),
            run_time = 2
        )
        self.wait()

        # Linien für das Gleichungssystem & SurRects für CrossVector
        cross_vec_rects = VGroup(*[
            SurroundingRectangle(self.cross_vec[0][index], color = self.com_color) for index in range(len(self.cross_vec)) 
        ])

        lines = self.get_crossproduct_cut_lines(self.vec_group, color = self.cut_color)
        text_comp = VGroup(*[
            Tex(tex, "-", "Komponente").next_to(2*RIGHT + 3*UP, LEFT, aligned_edge=UR) 
            for tex in ["$x$", "$y$", "$z$"]
        ])

        text_cut = VGroup(*[
            Tex("Streiche ", tex, " Zeile") 
            for tex in ["$1.$", "$2.$", "$3.$"]
        ])
        text_cut.move_to(3*LEFT + 2*DOWN)

        text_mult = Tex("Multipliziere über ", "Kreuz")
        text_mult.next_to(text_cut, RIGHT, buff = 1, aligned_edge=UP)
        text_mult[1].set_color(vec_c_color)

        for index in range(len(text_cut)):
            text_cut[index][1:].set_color(self.cut_color)
        for index in range(len(text_comp)):
            text_comp[index][0].set_color(self.com_color)

        cross_line1 = Line(UP + LEFT, DOWN + RIGHT, stroke_width = 2, color = vec_c_color)
        cross_line2 = Line(DOWN + LEFT, UP + RIGHT, stroke_width = 2, color = vec_c_color)
        cross_sign = VGroup(cross_line1, cross_line2)\
            .match_height(self.vec_group[1])\
            .move_to(self.vec_group[1])

        lines_kwargs = {"stroke_width": 3, "buff": 0.1, "color": vec_c_color}
        cross_lines_x = self.get_lines_for_comp_calc(self.vec_group, 1,2, **lines_kwargs)
        cross_lines_y = self.get_lines_for_comp_calc(self.vec_group, 0,2, **lines_kwargs)
        cross_lines_z = self.get_lines_for_comp_calc(self.vec_group, 0,1, **lines_kwargs)


        self.play(
            AnimationGroup(
                Write(text_comp[0]),
                Write(self.equals2), 
                FadeIn(self.cross_calc[1:], shift=0.5*UP, lag_ratio = 0.15),
                Create(cross_vec_rects[0]), 
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()


        # 1. Zeile streichen & Multipliziere über Kreuz
        self.play(Write(text_cut[0]))
        self.wait()

        self.play(
            LaggedStartMap(FadeToColor, VGroup(self.vec_group[0][0][0], self.vec_group[2][0][0]), color = DARK_GREY, lag_ratio = 0.1),
            Create(lines[0]),
            run_time = 2
        )
        self.wait()

        self.play(Write(text_mult))
        self.wait()


        self.play(ReplacementTransform(cross_sign.copy(), cross_lines_x))
        self.wait()

        self.play(                                          # index  0 1 2 3  
            AnimationGroup(                                 # !!!    ( 2 * 2 
                TransformFromCopy(self.vec_group[0][0][1], self.cross_calc[0][0][1]),
                TransformFromCopy(self.vec_group[2][0][2], self.cross_calc[0][0][3]),
                FadeIn(self.cross_calc[0][0][2]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()
        self.play(Write(self.cross_calc[0][1]))
        self.play(                                          # index  0  1 2 3 4  
            AnimationGroup(                                 # !!!    ( -1 ) * 0 
                TransformFromCopy(self.vec_group[0][0][2], self.cross_calc[0][2][1]),
                TransformFromCopy(self.vec_group[2][0][1], self.cross_calc[0][2][4]),
                FadeIn(self.cross_calc[0][2][3]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.play(LaggedStartMap(FadeIn, VGroup(self.cross_calc[0][2][0], self.cross_calc[0][2][2]), shift = 0.5*DOWN, lag_ratio = 0.1))
        self.wait()

        self.play(ShowPassingFlash(path_cross1, time_width = 0.5), rate_func = linear, run_time = 2)
        self.wait()

        self.play(FocusOn(self.cross_vec[0][0]), run_time = 1)
        self.play(FadeToColor(self.cross_vec[0][0], WHITE))
        self.wait()

        # FadeOut cross_lines, Streichlinie
        self.play(
            AnimationGroup(
                Uncreate(lines[0]),
                GrowFromPoint(cross_lines_x, point = self.vec_group[1].get_center(), rate_func = lambda t: smooth(1-t)),
                FadeToColor(VGroup(self.vec_group[0][0][0], self.vec_group[2][0][0]), WHITE, lag_ratio = 0.15),
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()

        # y-Komponente, 2 Zeile Streichen
        self.play(
            AnimationGroup(
                ReplacementTransform(text_comp[0], text_comp[1]), 
                ReplacementTransform(cross_vec_rects[0], cross_vec_rects[1]), 
                lag_ratio = 0.4
            ), 
            run_time = 2
        )
        self.wait()

        self.play(Transform(text_cut[0], text_cut[1]))
        self.wait()

        # 2. Zeile Streichen 
        self.play(
            LaggedStartMap(FadeToColor, VGroup(self.vec_group[0][0][1], self.vec_group[2][0][1]), color = DARK_GREY, lag_ratio = 0.1),
            Create(lines[1]),
            run_time = 2
        )
        self.wait()

        self.play(ReplacementTransform(cross_sign.copy(), cross_lines_y))
        self.wait()

        self.play(                                          # index   0 1 2 
            AnimationGroup(                                 # !!!    -1 * 3 
                TransformFromCopy(self.vec_group[0][0][2], self.cross_calc[0][3][0]),
                TransformFromCopy(self.vec_group[2][0][0], self.cross_calc[0][3][2]),
                FadeIn(self.cross_calc[0][3][1]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()
        self.play(Write(self.cross_calc[0][4]))
        self.play(                                                  # index  0 1 2 
            AnimationGroup(                                         # !!!    1 * 2 
                TransformFromCopy(self.vec_group[0][0][0], self.cross_calc[0][5][0]),
                TransformFromCopy(self.vec_group[2][0][2], self.cross_calc[0][5][2]),
                FadeIn(self.cross_calc[0][5][1]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()

        self.play(ShowPassingFlash(path_cross2, time_width = 0.5), rate_func = linear, run_time = 2)
        self.wait()

        self.play(FocusOn(self.cross_vec[0][1]), run_time = 1)
        self.play(FadeToColor(self.cross_vec[0][1], WHITE))
        self.wait()


        # FadeOut cross_lines, Streichlinie
        self.play(
            AnimationGroup(
                Uncreate(lines[1]),
                GrowFromPoint(cross_lines_y, point = self.vec_group[1].get_center(), rate_func = lambda t: smooth(1-t)),
                FadeToColor(VGroup(self.vec_group[0][0][1], self.vec_group[2][0][1]), WHITE, lag_ratio = 0.15),
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()


        # z-Komponente, 3 Zeile Streichen
        self.play(
            AnimationGroup(
                ReplacementTransform(text_comp[1], text_comp[2]), 
                ReplacementTransform(cross_vec_rects[1], cross_vec_rects[2]), 
                lag_ratio = 0.4
            ), 
            run_time = 2
        )
        self.wait()

        self.play(ReplacementTransform(text_cut[0], text_cut[2]))
        self.wait()

        # 3. Zeile Streichen 
        self.play(
            LaggedStartMap(FadeToColor, VGroup(self.vec_group[0][0][2], self.vec_group[2][0][2]), color = DARK_GREY, lag_ratio = 0.1),
            Create(lines[2]),
            run_time = 2
        )
        self.wait()

        self.play(ReplacementTransform(cross_sign.copy(), cross_lines_z))
        self.wait()

        self.play(                                          # index   0 1 2 
            AnimationGroup(                                 # !!!     1 * 0 
                TransformFromCopy(self.vec_group[0][0][0], self.cross_calc[0][6][0]),
                TransformFromCopy(self.vec_group[2][0][1], self.cross_calc[0][6][2]),
                FadeIn(self.cross_calc[0][6][1]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()
        self.play(Write(self.cross_calc[0][7]))
        self.play(                                                  # index  0 1 2 
            AnimationGroup(                                         # !!!    2 * 3 
                TransformFromCopy(self.vec_group[0][0][1], self.cross_calc[0][8][0]),
                TransformFromCopy(self.vec_group[2][0][0], self.cross_calc[0][8][2]),
                FadeIn(self.cross_calc[0][8][1]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()

        self.play(ShowPassingFlash(path_cross3, time_width = 0.5), rate_func = linear, run_time = 2)
        self.wait()

        self.play(FocusOn(self.cross_vec[0][2]), run_time = 1)
        self.play(FadeToColor(self.cross_vec[0][2], WHITE))
        self.wait()

        # FadeOut cross_lines, Streichlinie
        self.play(
            AnimationGroup(
                Uncreate(cross_vec_rects[2]),
                Uncreate(lines[2]),
                GrowFromPoint(cross_lines_z, point = self.vec_group[1].get_center(), rate_func = lambda t: smooth(1-t)),
                FadeToColor(VGroup(self.vec_group[0][0][2], self.vec_group[2][0][2]), WHITE, lag_ratio = 0.15),
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait(3)


        self.text_mult, self.text_cut, self.text_comp = text_mult, text_cut, text_comp

    def prepare_for_next_scene(self):
        fadeout_group = VGroup(
            self.text_comp[2], self.text_cut[2], self.text_mult,
            self.equals1, self.cross_calc, self.equals2
        )

        self.play(
            LaggedStartMap(
                FadeOut, 
                fadeout_group, 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.wait(2)


class OrthogonalProperty(Calculations):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }
        self.dot_color = LIGHT_BROWN

        self.vec_a_num = [1, 2, -1]
        self.vec_b_num = [3, 0,  2]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        self.mat_a = self.get_vector_matrix_from_num_vec(self.vec_a_num, **self.mat_kwargs)
        self.mat_b = self.get_vector_matrix_from_num_vec(self.vec_b_num, **self.mat_kwargs)
        self.mat_n = self.get_vector_matrix_from_num_vec(self.vec_n_num, **self.mat_kwargs)

        self.setup_from_old_scene()
        self.dot_product_with_a()
        self.dot_product_with_b()
        self.text_for_ortho()


    def setup_from_old_scene(self):
        self.mat_n.move_to(np.array([5.5806598, 0, 0]))

        cross_group = self.group_vecs_with_symbol(self.mat_a, self.mat_b, type = "\\times", color = vec_c_color)\
            .move_to(np.array([-3.5, 0, 0]))
        for element in cross_group[0], cross_group[2], self.mat_n:
            element[1:].set_color(DARK_GREY)

        cross_name = Tex("Kreuz", "produkt")\
            .move_to(np.array([-3.5, 1.592528, 0]))
        cross_name[0].set_color(vec_c_color)
        cross_name[1].set_color(DARK_GREY)


        self.add(cross_group, cross_name, self.mat_n)
        self.wait()

        cross_name.generate_target()
        cross_name.target.move_to(4.5*LEFT + 2.5*UP)

        cross_group.generate_target()
        cross_group.target.next_to(cross_name.target, RIGHT, buff = 0.5)

        cross_equals = MathTex("=")\
            .set_color(DARK_GREY)\
            .next_to(cross_group.target, RIGHT)

        self.mat_n.generate_target()
        self.mat_n.target.next_to(cross_equals, RIGHT)

        self.play(
            LaggedStartMap(MoveToTarget, VGroup(cross_name, cross_group, self.mat_n), path_arc = 1, lag_ratio = 0.15),
            Write(cross_equals, rate_func = squish_rate_func(smooth, 0.66, 1)),
            run_time = 3
        )
        self.wait()


        self.cross_name, self.cross_group = cross_name, cross_group

    def dot_product_with_a(self):
        dot_name = Tex("Skalar", "produkt")\
            .next_to(self.cross_name, DOWN, buff = 2, aligned_edge=RIGHT)
        dot_name[0].set_color(self.dot_color)
        dot_name[1].set_color(DARK_GREY)

        self.play(Write(dot_name))
        self.wait()

        vec_a = self.mat_a.copy()
        vec_n1 = self.mat_n.copy()

        dot_group_a = self.dot_group_a = self.group_vecs_with_symbol(vec_a, vec_n1, type = "dot", color = self.dot_color)
        dot_group_a.next_to(dot_name, RIGHT, buff = 0.5)

        self.play(
            Transform(self.mat_a.copy(), vec_a), 
            Transform(self.mat_n.copy(), vec_n1, path_arc = -1), 
            FadeIn(dot_group_a[1], shift = DOWN), 
            run_time = 3
        )
        self.wait()

        dot_equals1 = MathTex("=").set_color(DARK_GREY).next_to(dot_group_a, RIGHT)
        self.play(Write(dot_equals1))
        self.wait()

        dot_path = self.get_dotproduct_path(dot_group_a)
        self.play(ShowPassingFlash(dot_path, time_width = 0.25), rate_func = linear, run_time = 2)
        self.wait()

        # Aus beiden Vektoren --> Vektor fürs Skalarprodukt

        x = MathTex("1", "\\cdot", "4")
        y = MathTex("2", "\\cdot", "(", "-5", ")")
        z = MathTex("-1", "\\cdot", "(", "-6", ")")
        dot_vec = MobjectMatrix([[x], [y], [z]], **self.mat_kwargs, element_alignment_corner = DOWN)
        dot_vec.next_to(dot_equals1, RIGHT)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    TransformFromCopy(dot_group_a[2][0][0], dot_vec[0][0][2]),
                    FadeIn(dot_vec[0][0][1], shift = UP),
                    TransformFromCopy(dot_group_a[0][0][0], dot_vec[0][0][0]),
                    lag_ratio = 0.05
                ),
                AnimationGroup(
                    TransformFromCopy(dot_group_a[2][0][1], dot_vec[0][1][3]),
                    FadeIn(dot_vec[0][1][1], shift = UP),
                    TransformFromCopy(dot_group_a[0][0][1], dot_vec[0][1][0]),
                    FadeIn(dot_vec[0][1][2], shift = UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
                    FadeIn(dot_vec[0][1][4], shift = UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
                    lag_ratio = 0.05
                ),
                AnimationGroup(
                    TransformFromCopy(dot_group_a[2][0][2], dot_vec[0][2][3]),
                    FadeIn(dot_vec[0][2][1], shift = UP),
                    TransformFromCopy(dot_group_a[0][0][2], dot_vec[0][2][0]),
                    FadeIn(dot_vec[0][2][2], shift = UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
                    FadeIn(dot_vec[0][2][4], shift = UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
                    lag_ratio = 0.05
                ), 
                lag_ratio = 0.3
            ), 
            run_time = 3
        )
        self.wait()

        # Vektor fürs Kreuzprodukt --> einzelne Komponenten 
        dot_vec_num = [a*b for a,b in zip(self.vec_a_num, self.vec_n_num)]
        dot_vec2 = self.get_vector_matrix_from_num_vec(dot_vec_num, **self.mat_kwargs, element_alignment_corner = DOWN)
        dot_vec2.next_to(dot_equals1, RIGHT)
        self.play(
            AnimationGroup(
                *[
                    ReplacementTransform(dot_vec[0][index], dot_vec2[0][index])
                    for index in range(3)
                ], lag_ratio = 0.15
            ),
            run_time = 1
        )
        self.wait()

        # Ergebnis als Summe
        #                      0    1    2     3     4    5    6
        dot_result1 = MathTex("4", "+", "(", "-10", ")", "+", "6")\
            .next_to(dot_equals1, RIGHT)

        self.play(
            ReplacementTransform(dot_vec2[0][0], dot_result1[0]),
            ReplacementTransform(dot_vec2[0][1], dot_result1[3]),
            ReplacementTransform(dot_vec2[0][2], dot_result1[6]),
            AnimationGroup(*[FadeIn(dot_result1[index], shift = 0.5*UP) for index in [1,2,4,5]], lag_ratio = 0.1), 
            run_time = 1.5
        )
        self.wait()

        self.dot_result = MathTex("0")\
            .next_to(dot_equals1, RIGHT)
        self.play(Transform(dot_result1, self.dot_result))
        self.wait()

    def dot_product_with_b(self):
        vec_b = self.mat_b.copy()
        vec_n2 = self.mat_n.copy()


        dot_group_b = self.group_vecs_with_symbol(vec_b, vec_n2, type = "dot", color = self.dot_color)
        dot_group_b.next_to(self.dot_group_a, DOWN, buff = 0.5, aligned_edge=RIGHT)

        self.play(
            Transform(self.mat_b.copy(), vec_b), 
            Transform(self.mat_n.copy(), vec_n2, path_arc = -1), 
            FadeIn(dot_group_b[1], shift = DOWN), 
            run_time = 3
        )
        self.wait()

        dot_equals2 = MathTex("=").set_color(DARK_GREY).next_to(dot_group_b, RIGHT)
        self.play(Write(dot_equals2))
        self.wait()

        dot_path = self.get_dotproduct_path(dot_group_b)
        self.play(ShowPassingFlash(dot_path, time_width = 0.25), rate_func = linear, run_time = 2)
        self.wait()

        self.dot_result2 = MathTex("0").next_to(dot_equals2, RIGHT)
        self.play(Write(self.dot_result2))
        self.wait(2)

    def text_for_ortho(self):
        texs = VGroup(*[
            MathTex(tex).set_color(color).next_to(mob, UP, buff = 0)
            for tex, color, mob in zip(
                ["\\vec{a}", "\\vec{b}", "\\vec{n}"], 
                [vec_a_color, vec_b_color, vec_c_color],
                [self.cross_group[0], self.cross_group[2], self.mat_n]
            )
        ])

        # ortho_a = MathTex("\\vec{a}", "\\cdot", "\\vec{n}", "=", "0").next_to(self.dot_result, RIGHT, buff = 1)
        # ortho_b = MathTex("\\vec{b}", "\\cdot", "\\vec{n}", "=", "0").next_to(self.dot_result2, RIGHT, buff = 1)

        # for eq in ortho_a, ortho_b:
        #     eq.set_color_by_tex_to_color_map({
        #         "\\vec{a}": vec_a_color, "\\cdot": self.dot_color, "\\vec{b}": vec_b_color, "\\vec{n}": vec_c_color
        #     })

        # self.add(texs, ortho_a, ortho_b)

        brace = Brace(Line(self.dot_result.get_corner(UR), self.dot_result2.get_corner(DR)), RIGHT, color = DARK_GREY)
        brace_text = Tex(
            "Vektor ", "$\\vec{n}$", " steht \\\\", "senkrecht zum \\\\", 
            "Vektor ", "$\\vec{a}$", " und \\\\", "zum Vektor ", "$\\vec{b}$"
        )
        brace_text.next_to(brace, RIGHT)
        brace_text.set_color_by_tex_to_color_map({
                "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\vec{n}": vec_c_color,
            })

        self.play(LaggedStartMap(FadeIn, texs, lag_ratio = 0.1))
        self.play(Create(brace))
        self.play(Write(brace_text))
        self.wait()

        arrow = Arrow(brace_text[1].get_top() + 0.75*UP, brace_text[1].get_top(), buff = 0.1, color = PINK)

        text_nvec = Tex("Normalen", "vektor")
        text_nvec[0].set_color(vec_c_color)
        text_nvec[1].set_color(LIGHT_GREY)
        text_nvec.next_to(arrow, UP)

        self.play(Write(text_nvec))
        self.play(GrowArrow(arrow), run_time = 1.5)
        self.wait()

        self.play(
            Circumscribe(brace_text[6], color = PINK, fade_out = True, time_width = 0.5, run_time = 2),
            FadeToColor(brace_text[6], PINK, run_time = 2),
        )
        self.wait()

        text_perp = Tex("senkrecht")\
            .set_color(vec_c_color)\
            .next_to(text_nvec, UP, buff = 1)\
            .shift(0.5*RIGHT)
        arrow2 = Arrow(text_nvec[0].get_top(), text_perp[0].get_bottom(), buff = 0.1, color = PINK)
        self.play(GrowArrow(arrow2))
        self.play(Write(text_perp))
        self.wait(3)


class OrthogonalProperty3D(ThreeDScene):
    def construct(self):
        self.vec_a_num = [1, 2, -1]
        self.vec_b_num = [3, 0,  2]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axes = self.axes = ThreeDAxes()
        axes.set_color(DARK_GREY)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)
        self.origin = axes.coords_to_point(0,0,0)

        self.cone_height, self.cone_radius = 0.5, 0.15
        self.cone_kwargs = {"height": self.cone_height, "base_radius": self.cone_radius}

        self.draw_axes()
        self.draw_vecs()


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
        self.add(self.axes)
        self.wait(2)

    def draw_vecs(self):
        axes = self.axes
        cone_kwargs = self.cone_kwargs

        # vec_a = Arrow(start = self.origin, end = axes.coords_to_point(*self.vec_a_num), buff = 0, color = vec_a_color)
        # vec_b = Arrow(start = self.origin, end = axes.coords_to_point(*self.vec_b_num), buff = 0, color = vec_b_color)
        # vec_n = Arrow(start = self.origin, end = axes.coords_to_point(*self.vec_n_num), buff = 0, color = vec_c_color)

        vec_a = Arrow3D(start = self.origin, end = axes.coords_to_point(*self.vec_a_num), **cone_kwargs, color = vec_a_color)
        vec_b = Arrow3D(start = self.origin, end = axes.coords_to_point(*self.vec_b_num), **cone_kwargs, color = vec_b_color)
        vec_n = Arrow3D(start = self.origin, end = axes.coords_to_point(*self.vec_n_num), **cone_kwargs, color = vec_c_color)

        comp_a = self.get_component_lines(self.vec_a_num, line_class = Line, color = RED_E)
        comp_b = self.get_component_lines(self.vec_b_num, line_class = Line, color = YELLOW_E)
        comp_n = self.get_component_lines(self.vec_n_num, line_class = Line, color = BLUE_E)

        # for comp, vec in zip([comp_a, comp_b, comp_n], [vec_a, vec_b, vec_n]):
        #     self.play(Create(comp), lag_ratio = 0.15, run_time = 2)
        #     self.play(Create(vec), run_time = 2)
        #     self.wait(0.5)

        self.play(
            LaggedStartMap(Create, VGroup(comp_a, comp_b, comp_n), lag_ratio = 0.25), run_time = 2
        )
        self.play(
            LaggedStartMap(Create, VGroup(vec_a, vec_b, vec_n), lag_ratio = 0.25), run_time = 2
        )
        self.wait()

        self.move_camera(zoom = 0.75, run_time = 3)
        self.wait()
        self.play(
            ApplyMethod(self.renderer.camera.zoom_tracker.set_value, 1, run_time = 3),
            *[Uncreate(comp, lag_ratio = 0.1, run_time = 3) for comp in [comp_a, comp_b, comp_n]],
        )
        self.wait()

        # Move Camera --> Orthogonalität zwischen Vektor b und n
        self.move_camera(phi = 65.90516*DEGREES, theta = -116.56505*DEGREES, run_time = 3)
        self.wait(2)

        # Move Camera --> Orthogonalität zwischen Vektor a und n
        self.move_camera(phi = 56.30993*DEGREES, theta = 0*DEGREES, run_time = 3)
        self.wait(3)


        self.move_camera(phi = 70*DEGREES, theta = 30*DEGREES, run_time = 3)
        self.wait(3)




    # functions
    def get_component_lines(self, vec_num, line_class = DashedLine, color = BLUE, **kwargs):
        axes = self.axes
        x, y, z = vec_num[0], vec_num[1], vec_num[2]

        x_component = line_class(axes.c2p(x, y, 0), axes.c2p(0, y, 0), color = color, **kwargs)
        y_component = line_class(axes.c2p(x, y, 0), axes.c2p(x, 0, 0), color = color, **kwargs)
        z_component = line_class(axes.c2p(x, y, 0), axes.c2p(x, y, z), color = color, **kwargs)

        result = VGroup(x_component, y_component, z_component)

        return result


class OriginOfNormalVector(Calculations, MovingCameraScene):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.word_property()
        self.eq_property()
        self.solution_vector()
        self.proof_for_vector_a()
        self.proof_for_vector_b()


    def word_property(self):

        eq1 = MathTex("\\vec{a}", "\\cdot", "\\vec{n}", "=", "0").to_corner(UL)
        eq2 = MathTex("\\vec{b}", "\\cdot", "\\vec{n}", "=", "0").next_to(eq1, DOWN, aligned_edge = RIGHT)

        for eq in eq1, eq2:
            eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": GREEN , "\\vec{n}": vec_c_color})

        eqs = VGroup(eq1, eq2)
        eqs.save_state()

        text = Tex("Der ", "Normalenvektor", " ist sowohl zu Vektor ", "$\\vec{a}$\\\\", " als auch zu Vektor ", "$\\vec{b}$", " senkrecht orientiert.")
        text.set_color(LIGHT_GREY)
        text.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "Normalenvektor": vec_c_color})
        text.next_to(eqs, RIGHT, buff = 1)

        # Gleichungen centern
        eqs.center().scale(2)

        self.play(AnimationGroup(*[
            FadeIn(eq, shift = direction) for eq, direction in zip([eq1, eq2], [LEFT, RIGHT])
        ], lag_ratio = 0.1))
        self.wait()

        self.play(
            Restore(eqs, path_arc = -2, run_time = 3), 
            Write(text, run_time = 1.5)
        )
        self.wait()


        self.eqs = eqs
        self.text = text

    def eq_property(self):

        ax, ay, az = MathTex("a_1"), MathTex("a_2"), MathTex("a_3")
        bx, by, bz = MathTex("b_1"), MathTex("b_2"), MathTex("b_3")
        nx, ny, nz = MathTex("n_1"), MathTex("n_2"), MathTex("n_3")
        for element in ax, ay, az, bx, by, bz, nx, ny, nz:
            element.set_color_by_tex_to_color_map({"a": vec_a_color, "b": vec_b_color, "n": vec_c_color})

        mat_a = MobjectMatrix([[ax], [ay], [az]], **self.mat_kwargs)
        mat_b = MobjectMatrix([[bx], [by], [bz]], **self.mat_kwargs)
        mat_n = MobjectMatrix([[nx], [ny], [nz]], **self.mat_kwargs)
        mat_n2 = mat_n.copy()

        for mat in mat_a, mat_b, mat_n, mat_n2:
            mat[1:].set_color(DARK_GREY)

        eq1_mat = self.group_vecs_with_symbol(mat_a, mat_n, type="cdot")
        eq2_mat = self.group_vecs_with_symbol(mat_b, mat_n2, type="cdot").next_to(eq1_mat, DOWN, aligned_edge=RIGHT)

        equals_zero_a = MathTex("=", "0")
        equals_zero_a[0].set_color(DARK_GREY)
        equals_zero_a.next_to(eq1_mat, RIGHT)
        equals_zero_b = equals_zero_a.copy().next_to(eq2_mat, RIGHT)

        self.play(
            LaggedStartMap(Create, VGroup(eq1_mat, eq2_mat, equals_zero_a, equals_zero_b), lag_ratio = 0.1), 
            run_time = 2
        )
        self.wait()

        # Skalarprodukte nach links, 
        for eq in eq1_mat, eq2_mat:
            eq.generate_target()
            eq.target.to_edge(LEFT)

        #               0     1        2       3     4     5        6       7     8     9       10       11
        dot1 = MathTex("=", "a_1", "\\cdot", "n_1", "+", "a_2", "\\cdot", "n_2", "+", "a_3", "\\cdot", "n_3")
        dot2 = MathTex("=", "b_1", "\\cdot", "n_1", "+", "b_2", "\\cdot", "n_2", "+", "b_3", "\\cdot", "n_3")

        for dot, eq_mat in zip([dot1, dot2], [eq1_mat, eq2_mat]):
            dot[0].set_color(DARK_GREY)
            dot.next_to(eq_mat.target, RIGHT)
            dot.set_color_by_tex_to_color_map({"a": vec_a_color, "b": vec_b_color, "n": vec_c_color})

        self.play(
            MoveToTarget(eq1_mat), 
            MoveToTarget(eq2_mat),
            equals_zero_a.animate.next_to(dot1, RIGHT),
            equals_zero_b.animate.next_to(dot2, RIGHT),
            run_time = 2
        )
        self.wait()

        self.play(
            ShowIncreasingSubsets(dot1), ShowIncreasingSubsets(dot2), 
            run_time = 2
        )
        self.wait()


        # Surrounding Rectangles
        sur_rects1 = VGroup(*[SurroundingRectangle(dot1[index], color = LIGHT_BROWN) for index in [3,7,11]])
        sur_rects2 = VGroup(*[SurroundingRectangle(dot2[index], color = LIGHT_BROWN) for index in [3,7,11]])

        self.play(Create(sur_rects1, lag_ratio = 0.15), run_time = 2)
        self.wait()

        self.play(
            Uncreate(sur_rects1, lag_ratio = 0.15), 
            Create(sur_rects2, lag_ratio = 0.15), 
            run_time = 2
        )
        self.wait()
        self.play(FadeOut(sur_rects2))
        self.wait()


        # Ausfaden und verschieben --> in der Mitt Platz machen
        self.play(
            VGroup(eq1_mat, dot1, equals_zero_a).animate.to_edge(UP), 
            VGroup(eq2_mat, dot2, equals_zero_b).animate.to_edge(DOWN), 
            FadeOut(VGroup(*self.eqs, self.text), shift = 2*UP),
            run_time = 2
        )
        self.wait()

        self.mat_a, self.mat_b = mat_a, mat_b
        self.equals_zero_a, self.equals_zero_b = equals_zero_a, equals_zero_b
        self.eq1_mat, self.eq2_mat = eq1_mat, eq2_mat
        self.dot1, self.dot2 = dot1, dot2

    def solution_vector(self):
        mat_a, mat_b = self.mat_a.copy(), self.mat_b.copy()
        cross = self.group_vecs_with_symbol(mat_a, mat_b, type = "times", color = vec_c_color)\
            .shift(3*LEFT)
        equals = MathTex("=").next_to(cross, RIGHT)

        nx_comp = MathTex("a_2", "\\cdot", "b_3", "-", "a_3", "\\cdot", "b_2")
        ny_comp = MathTex("a_3", "\\cdot", "b_1", "-", "a_1", "\\cdot", "b_3")
        nz_comp = MathTex("a_1", "\\cdot", "b_2", "-", "a_2", "\\cdot", "b_1")

        for coord in nx_comp, ny_comp, nz_comp:
            coord.set_color_by_tex_to_color_map({"a": vec_a_color, "b": vec_b_color})

        mat_cross_calc = MobjectMatrix([[nx_comp], [ny_comp], [nz_comp]], **self.mat_kwargs)
        mat_cross_calc[1:].set_color(DARK_GREY)
        mat_cross_calc.next_to(equals, RIGHT)


        self.play(
            AnimationGroup(
                TransformFromCopy(self.mat_a, mat_a), 
                Write(cross[1]),
                TransformFromCopy(self.mat_b, mat_b),
                Write(equals),
                lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()


        path_x, path_y, path_z = self.get_crossproduct_path_xyz(cross, color = vec_c_color, stroke_width = 7)
        paths = VGroup(path_x, path_y, path_z)
        cut_lines = self.get_crossproduct_cut_lines(cross, color = WHITE, line_buff = 0.1)

        for number in range(len(cut_lines)):
            self.play(
                AnimationGroup(
                    Create(cut_lines[number]), 
                    ShowPassingFlash(paths[number]),
                    Write(mat_cross_calc[0][number]), 
                    lag_ratio = 0.25
                ), 
                run_time = 2.5
            )
            self.play(Uncreate(cut_lines[number]))
            self.wait()
        self.play(Write(mat_cross_calc[1:]))
        self.wait()


        self.mat_cross_calc = mat_cross_calc

    def proof_for_vector_a(self):
        part1 = self.dot1[:4]
        part1.generate_target()
        part1.target.shift(2.4*UP)

        part2 = self.dot1[4:8]
        part2.generate_target()
        part2.target.next_to(part1.target, DOWN, buff = 0.8, aligned_edge=LEFT)

        part3 = self.dot1[8:]
        part3.generate_target()
        part3.target.next_to(part2.target, DOWN, buff = 0.8, aligned_edge=LEFT)

        # 
        self.play(
            self.camera.frame.animate.shift(2.4*UP), 
            VGroup(self.eq1_mat).animate.shift(2.4*UP),
            MoveToTarget(part1),
            MoveToTarget(part2, path_arc = -1), 
            MoveToTarget(part3, path_arc = -2), 
            FadeOut(self.equals_zero_a),
            run_time = 2
        )
        self.wait()


        # transform components from cross vector into dot product
        insert1 = MathTex("(", "a_2", "\\cdot", "b_3", "-", "a_3", "\\cdot", "b_2", ")")
        insert2 = MathTex("(", "a_3", "\\cdot", "b_1", "-", "a_1", "\\cdot", "b_3", ")")
        insert3 = MathTex("(", "a_1", "\\cdot", "b_2", "-", "a_2", "\\cdot", "b_1", ")")

        for eq, target in zip([insert1, insert2, insert3], [part1[2], part2[2], part3[2]]):
            eq.set_color_by_tex_to_color_map({"a": vec_a_color, "b": vec_b_color})
            eq.next_to(target, RIGHT)

        self.play(
            AnimationGroup(
                *[FadeOut(part[-1], shift = 0.5*UP) for part in [part1, part2, part3]],
                *[FadeIn(VGroup(eq[0], eq[-1]), shift = 0.5*UP) for eq in [insert1, insert2, insert3]], 
                lag_ratio = 0.1
            ), 
            run_time = 1.5
        )
        self.play(
            AnimationGroup(
                TransformFromCopy(self.mat_cross_calc[0][0], insert1[1:-1]),
                TransformFromCopy(self.mat_cross_calc[0][1], insert2[1:-1]),
                TransformFromCopy(self.mat_cross_calc[0][2], insert3[1:-1]),
                lag_ratio = 0.25
            ),
            run_time = 3
        )
        self.wait()

        # Terms cancel each other out
        front_rects = VGroup(*[SurroundingRectangle(self.dot1[index], color = vec_c_color) for index in [1, 5, 9]])
        front_rects1 = front_rects[1].copy()

        inner_rects = VGroup()
        for part in insert1, insert2, insert3:
            sur_rect_front = SurroundingRectangle(part[1:4], color = vec_c_color)
            sur_rect_back = SurroundingRectangle(part[5:8], color = vec_c_color) 
            inner_rects.add(sur_rect_front, sur_rect_back)

        # a1 * a2 * b3
        self.play(*[Create(rect, run_time = 2) for rect in [front_rects[0], inner_rects[0]]])
        self.wait()
        self.play(*[Create(rect, run_time = 2) for rect in [front_rects[1], inner_rects[3]]])
        self.wait()

        self.play(
            ReplacementTransform(inner_rects[0], inner_rects[1]),
            insert1[1:4].animate.fade(darkness = 0.75),
            insert2[5:8].animate.fade(darkness = 0.75),
            Uncreate(front_rects[1]),
            Uncreate(inner_rects[3]),
            run_time = 3
        )
        self.wait()

        # a1 * a3 * b2
        self.play(*[Create(rect, run_time = 2) for rect in [front_rects[2], inner_rects[4]]])
        self.wait()

        self.play(
            ReplacementTransform(inner_rects[4], inner_rects[5]),
            *[Uncreate(rect) for rect in [front_rects[0], inner_rects[1]]],
            insert3[1:4].animate.fade(darkness = 0.75),
            insert1[5:8].animate.fade(darkness = 0.75),
            run_time = 3
        )
        self.wait()

        # a2 * a3 * b1
        self.play(*[Create(rect, run_time = 2) for rect in [front_rects1, inner_rects[2]]])
        self.wait()


        self.play(
            *[Uncreate(rect) for rect in [front_rects1, front_rects[2], inner_rects[2], inner_rects[5]]],
            insert2[1:4].animate.fade(darkness = 0.75),
            insert3[5:8].animate.fade(darkness = 0.75),
            run_time = 3
        )
        self.wait()

        self.equals_zero_a.next_to(insert3, RIGHT)
        self.play(FadeIn(self.equals_zero_a))
        self.wait()

    def proof_for_vector_b(self):
        self.play(
            self.camera.frame.animate.shift(5*DOWN), 
            run_time = 5
        )
        self.wait(3)


class TwoOrthogonalVectors(ThreeDScene):
    def construct(self):
        self.vec_a_num = [2/3, -1/3, 2/3]
        self.vec_b_num = [2/3,  2/3, -1/3]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length, 
            axis_config = {"color": DARK_GREY},
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)

        self.acr_rate = 0.1

        self.setup_scene()
        self.draw_plane()
        self.show_second_vector()



    def setup_scene(self):
        axes, origin = self.axes, self.origin

        self.vec_a = Arrow3D(origin, axes.c2p(*self.vec_a_num), color = vec_a_color)
        self.vec_b = Arrow3D(origin, axes.c2p(*self.vec_b_num), color = vec_b_color)
        self.vec_n = Arrow3D(origin, axes.c2p(*self.vec_n_num), color = vec_c_color)

        self.play(Create(self.axes), run_time = 2)
        self.begin_ambient_camera_rotation(rate = self.acr_rate)
        self.wait()

        self.play(*[Create(mob, run_time = 2) for mob in [self.vec_a, self.vec_b]])
        self.wait(3)

    def draw_plane(self):
        lines_kwags = {"stroke_width": 2, "color": GREY, "stroke_opacity": 0.2}
        lines_a = VGroup(*[
            Line(
                start = self.axes.c2p(*[-1.5*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[+1.5*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for s in np.linspace(-1.5,1.5,7)
        ])

        lines_b = VGroup(*[
            Line(
                start = self.axes.c2p(*[r*comp_a - 1.5*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[r*comp_a + 1.5*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for r in np.linspace(-1.5,1.5,7)
        ])

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


        self.play(Create(big_rect), Create(lines_a), Create(lines_b), run_time = 3)
        self.wait()

        self.play(Create(self.vec_n), run_time = 2)
        self.wait(3)

    def show_second_vector(self):
        self.stop_ambient_camera_rotation()
        self.move_camera(phi = 70*DEGREES, theta = 20*DEGREES, run_time = 3)
        self.wait()

        self.move_camera(phi = 70*DEGREES, theta = -15*DEGREES, run_time = 3)
        self.wait()

        vec_n2_num = np.cross(self.vec_b_num, self.vec_a_num)
        self.vec_n2 = Arrow3D(self.origin, self.axes.c2p(*vec_n2_num), color = vec_c_color)

        self.play(Create(self.vec_n2), run_time = 2)
        self.wait(3)


        self.begin_ambient_camera_rotation(rate = 0.1)
        self.wait(25)


class OverlayTwoOrthoVectors(Scene):
    def construct(self):
        self.correct_cross_vector()
        self.opposite_cross_vector()
        self.right_hand_rule()


    def correct_cross_vector(self):
        plane = Tex("Ebene, die von ", "$\\vec{a}$", "\\\\und ", "$\\vec{b}$", " aufgespannt\\\\", "wird")\
            .next_to(2.5*RIGHT + 1.5*DOWN, RIGHT)

        arc = CurvedArrow(start_point = plane[0].get_left() + 0.2*LEFT, end_point = 1.5*RIGHT + 2*DOWN, color = DARK_BLUE)
        
        eq = MathTex("\\vec{n}", "=", "\\vec{a}", "\\times", "\\vec{b}")\
            .next_to(2*RIGHT + 2*UP, RIGHT)

        norm_vec = Tex("Normalenvektor")\
            .set_color(vec_c_color)\
            .next_to(eq, UP, aligned_edge = LEFT)

        for mob in plane, eq:
            mob.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\vec{n}": vec_c_color})


        self.play(Write(eq), run_time = 1.5)
        self.wait()

        self.play(FadeIn(norm_vec, shift = 3*LEFT), run_time = 2)
        self.wait()

        self.play(Write(plane), run_time = 1.5)
        self.play(Create(arc))
        self.wait()


        self.play(
            FadeOut(arc, rate_func = squish_rate_func(smooth, 0, 0.5)),
            VGroup(eq, norm_vec).animate.shift(0.5*LEFT + 0.5*UP),
            plane.animate(rate_func = squish_rate_func(smooth, 0, 0.6)).scale_about_point(0.75, plane.get_corner(UR)),
            run_time = 3
        )
        self.wait()

        self.plane, self.eq, self.norm_vec = plane, eq, norm_vec

    def opposite_cross_vector(self):
        wrong_cross = MathTex("\\vec{a}", "\\times", "\\vec{b}")
        right_cross = MathTex("\\vec{b}", "\\times", "\\vec{a}")
        anti_commut = MathTex("\\vec{a}", "\\times", "\\vec{b}", "=", "-", "\\vec{b}", "\\times", "\\vec{a}")\

        for cross in wrong_cross, right_cross, anti_commut:
            cross.next_to(1.5*LEFT + 2*DOWN, LEFT)
            cross.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "-": vec_c_color})

        self.play(Write(wrong_cross), run_time = 1.5)
        self.wait()

        question_mark = Tex("?")
        exclamation_mark = Tex("!")
        for mark in question_mark, exclamation_mark:
            mark.scale(2)
            mark.set_color(GREEN)
            mark.set_fill(color = GREY, opacity = 0.25)
            mark.set_stroke(width = 1.5)
            mark.next_to(wrong_cross, LEFT, buff = 0.75)

        self.play(DrawBorderThenFill(question_mark))
        self.wait()

        self.play(
            ReplacementTransform(question_mark, exclamation_mark, rate_func = squish_rate_func(smooth, 0.4, 1)),
            ClockwiseTransform(wrong_cross[0], right_cross[2]),
            ClockwiseTransform(wrong_cross[2], right_cross[0]),
            run_time = 2
        )
        self.wait()


        anti_commut.to_edge(LEFT).shift(4.25*UP)
        arrow = Arrow(ORIGIN, UP, buff = 0, color = vec_c_color).next_to(anti_commut[4], DOWN)
        text_anti = Tex("Anti", "-", "Kommutativ").next_to(arrow, DOWN)
        text_anti[0].set_color(vec_c_color)

        self.play(
            ShrinkToCenter(exclamation_mark),
            Write(anti_commut),
            run_time = 1.5
        )
        self.wait()

        self.play(GrowArrow(arrow))
        self.play(Write(text_anti))
        self.wait(3)


        fadeout_group = VGroup(wrong_cross, text_anti, arrow, anti_commut, self.plane, self.eq, self.norm_vec)
        self.play(
            AnimationGroup(
                *[
                    FadeOut(mob, shift = 3*direction) for mob, direction in zip(
                        fadeout_group, [LEFT, LEFT, LEFT, LEFT, RIGHT, RIGHT, RIGHT]
                    )
                ], lag_ratio = 0.1
            ), 
            run_time = 3
        )
        self.wait()

    def right_hand_rule(self):
        svg = SVGMobject("Right_Hand_Rule_Winding")\
            .scale(1.5)\
            .shift(5*RIGHT)

        for part in svg[0], svg[12:14]:
            part.set_fill(color = "#E5C489", opacity = 1)
            part.set_stroke(color=DARK_GREY, width = 2)

        for part in svg[1:12], svg[14:]:
            part.set_fill(opacity = 0)
            part.set_stroke(color = DARK_GREY, width = 2)

        svg.rotate(angle = -25*DEGREES, axis = OUT)

        self.play(DrawBorderThenFill(svg))
        self.wait()

        text = Tex("Rechte","-","Hand","-","Regel")
        text.next_to(svg, UP, buff = 1, aligned_edge=RIGHT)
        self.play(Write(text))
        self.wait()

        arrowa = Arrow(ORIGIN, 2*LEFT + 1.6*UP, buff = 0, color = vec_a_color)
        arrowb = Arrow(ORIGIN, 2*LEFT + 0.1*UP, buff = 0, color = vec_b_color)
        arrowc = Arrow(ORIGIN, 2*UP + RIGHT, buff = 0, color = vec_c_color)


        arcs_hand = Arc(
            radius = 1.5, start_angle = arrowa.get_angle(), angle = angle_between_vectors([2,1.6,0], [2, 0.1, 0]), color = GREEN,

        ).add_tip()

        for arrow in arrowa, arrowb:
            arrow.shift(5*RIGHT)
            self.play(GrowArrow(arrow), run_time = 2)
            self.wait()

        for mob in arcs_hand, arrowc:
            mob.shift(5*RIGHT)

        self.play(Create(arcs_hand), run_time = 3)
        self.wait()

        self.play(GrowArrow(arrowc), run_time = 3)
        self.wait()

        self.play(
            AnimationGroup(
                *[GrowFromPoint(mob, point = arrowa.get_start(), rate_func = lambda t: smooth(1-t)) for mob in [svg, arrowc, arrowb, arrowa, arcs_hand, text]], 
                lag_ratio = 0.1
            ),
            run_time = 1.5
        )
        self.wait()


class DifferentCalculation(Calculations):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6,
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.vec_a_num = [1, 2, -1]
        self.vec_b_num = [3, 0,  2]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        self.vec_a_num5 = [1, 2, -1, 1, 2]
        self.vec_b_num5 = [3, 0,  2, 3, 0]


        self.make_them_5_dimensional()
        self.cross_calculation()

    def make_them_5_dimensional(self):
        vec_a_num, vec_b_num, vec_n_num = self.vec_a_num,  self.vec_b_num, self.vec_n_num

        cross_name = Tex("Kreuz", "produkt")\
            .move_to(np.array([-3.5, 1.592528, 0]))
        cross_name[0].set_color(vec_c_color)
        cross_name[1].set_color(DARK_GREY)

        self.vec_a = self.get_vector_matrix_from_num_vec(vec_a_num, **self.mat_kwargs)
        self.vec_b = self.get_vector_matrix_from_num_vec(vec_b_num, **self.mat_kwargs)
        self.vec_n = self.get_vector_matrix_from_num_vec(vec_n_num, **self.mat_kwargs)\
            .move_to(np.array([5.5806598, 0, 0]))

        self.vec_a_5 = Matrix([[vec_a_num[0]], [vec_a_num[1]], [vec_a_num[2]], [vec_a_num[0]], [vec_a_num[1]]], **self.mat_kwargs)
        self.vec_b_5 = Matrix([[vec_b_num[0]], [vec_b_num[1]], [vec_b_num[2]], [vec_b_num[0]], [vec_b_num[1]]], **self.mat_kwargs)

        for vec in self.vec_a, self.vec_b, self.vec_a_5, self.vec_b_5, self.vec_n:
            vec[1:].set_color(DARK_GREY)

        vec_group = self.group_vecs_with_symbol(self.vec_a, self.vec_b, type = "times", color = vec_c_color)\
            .move_to(np.array([-3.5, 0, 0]))

        self.equals1 = MathTex("=").next_to(vec_group, RIGHT)


        self.add( cross_name, vec_group, self.equals1, self.vec_n)
        self.wait()

        vec_group_5 = self.group_vecs_with_symbol(self.vec_a_5, self.vec_b_5, type = "times", color = vec_c_color)
        self.vec_a_5.move_to(self.vec_a, aligned_edge=UP)
        self.vec_b_5.move_to(self.vec_b, aligned_edge=UP)


        sur_rect1 = SurroundingRectangle(VGroup(vec_group_5[0][0][:2], vec_group_5[2][0][:2], ), color = MAROON)
        sur_rect2 = SurroundingRectangle(VGroup(vec_group_5[0][0][3:], vec_group_5[2][0][3:], ), color = MAROON)
        self.play(Create(sur_rect1))
        self.wait()

        self.play(ReplacementTransform(sur_rect1.copy(), sur_rect2), run_time = 1.5)
        self.wait()

        self.play(
            AnimationGroup(
                TransformFromCopy(self.vec_a[0][1], self.vec_a_5[0][4], path_arc = -PI),
                TransformFromCopy(self.vec_a[0][0], self.vec_a_5[0][3], path_arc = -PI),
                TransformFromCopy(self.vec_b[0][1], self.vec_b_5[0][4], path_arc =  PI),
                TransformFromCopy(self.vec_b[0][0], self.vec_b_5[0][3], path_arc =  PI),
                lag_ratio = 0.2,
            ),
            run_time = 3
        )

        self.play(LaggedStartMap(FadeOut, VGroup(sur_rect1, sur_rect2), lag_ratio = 0.15))
        self.wait()





        self.vec_group, self.vec_group_5 = vec_group, vec_group_5

    def cross_calculation(self):

        lines_kwargs = {"stroke_width": 3, "buff": 0.1, "color": LIGHT_BROWN}
        lines_x = self.get_lines_for_comp_calc(self.vec_group_5, 1, 2, **lines_kwargs)
        lines_y = self.get_lines_for_comp_calc(self.vec_group_5, 2, 3, **lines_kwargs)
        lines_z = self.get_lines_for_comp_calc(self.vec_group_5, 3, 4, **lines_kwargs)

        cross_lines = VGroup(lines_x, lines_y, lines_z)

        x1, xm, x2 = MathTex("(", "2", "\\cdot", "2"),  MathTex("(", "-", ")"), MathTex("(", "-1", ")", "\\cdot", "0")
        y1, ym, y2 = MathTex("-1", "\\cdot", "3"), MathTex("1", "-", "1"), MathTex("1", "\\cdot", "2")
        z1, zm, z2 = MathTex("1", "\\cdot", "0"),  MathTex("1", "-", "1"), MathTex("2", "\\cdot", "3")

        x1[0].set_color(BLACK)
        for minus in xm, ym, zm:
            minus[0::2].set_color(BLACK)

        cross_calc = MobjectMatrix([[x1, xm, x2], [y1, ym, y2], [z1, zm, z2]], **self.mat_kwargs, element_alignment_corner=DOWN)
        cross_calc.next_to(self.equals1, RIGHT)
        cross_calc[1:].set_color(DARK_GREY)

        self.equals2 = MathTex("=")\
            .next_to(cross_calc, RIGHT)

        self.play(
            Write(self.equals2), 
            Write(cross_calc[1:]), 
        )
        self.wait()

        cut_lines = self.get_crossproduct_cut_lines(self.vec_group, MAROON)
        path_x, path_y, path_z = self.get_crossproduct_path_xyz(self.vec_group_5[:3], stroke_width = 7)
        added_anims = [ShowPassingFlash(path_y, run_time = 3)]
        for index in range(len(cross_lines)):
            self.play(Create(cut_lines[index]), run_time = 2)
            self.wait()
            self.play(ShowPassingFlash(path_x), run_time = 3)
            self.wait()
            self.play(Write(cross_calc[0][3*index:3*(index + 1)]), run_time = 1.5)
            self.wait()
            if index == 1:
                self.play(*added_anims)
                self.wait()

            path_x.shift(self.mat_kwargs.get("v_buff") * DOWN)
        self.wait(3)

        self.cross_calc = cross_calc


class NextVideo(Scene):
    def construct(self):
        title = Tex("Nächstes Video")\
            .scale(1.5)\
            .to_edge(UP)\
            .set_color_by_gradient(vec_a_color, vec_c_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.25)\
            .set_stroke(width = 2)

        rect = ScreenRectangle(height = 6)\
            .set_color([vec_a_color, vec_c_color, vec_b_color])\
            .fade(darkness=0.5)\
            .next_to(title, DOWN)

        self.wait()
        self.play(
            Write(title, run_time = 1.5), 
            Create(rect, run_time = 3)
        )
        self.wait(5)

        group = Group(*self.mobjects)
        self.play(ShrinkToCenter(group), rate_func = running_start, run_time = 1)
        self.wait()


class Thumbnail1(Scene):
    def construct(self):

        plane = Tex("Ebene, die von ", "$\\vec{a}$", "\\\\und ", "$\\vec{b}$", " aufgespannt\\\\", "wird")\
            .scale(0.75)\
            .next_to(7*LEFT + 2.5*UP, RIGHT)

        arc = CurvedArrow(
            start_point = plane.get_corner(DR) + 0.2*RIGHT, 
            end_point = 2*LEFT + 2*UP, 
            color = DARK_BLUE
        )
        
        eq = MathTex("\\vec{n}", "=", "\\vec{a}", "\\times", "\\vec{b}")\
            .next_to(2*RIGHT + 2*UP, RIGHT)

        norm_vec = Tex("Normalenvektor")\
            .set_color(vec_c_color)\
            .next_to(eq, UP, aligned_edge = LEFT)

        for mob in plane, eq:
            mob.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\vec{n}": vec_c_color})


        self.add(plane, arc, eq, norm_vec)

        title = Tex("Kreuzprodukt")\
            .set_color_by_gradient(vec_a_color, vec_c_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 5)\
            .add_background_rectangle()\
            .to_edge(LEFT, buff = 1)\
            .shift(2.5*DOWN)

        epi = Tex("Episode 05")\
            .next_to(title, UP, aligned_edge = LEFT)\
            .add_background_rectangle()


        self.add(title, epi)


class Thumbnail2(TwoOrthogonalVectors):
    def construct(self):
        self.vec_a_num = [2/3, -1/3, 2/3]
        self.vec_b_num = [2/3,  2/3, -1/3]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length, 
            axis_config = {"color": DARK_GREY},
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)

        self.setup_scene()
        self.draw_plane()

        self.stop_ambient_camera_rotation()
        self.move_camera(phi = 70*DEGREES, theta = 20*DEGREES, run_time = 3)
        self.wait()




# QUICK RELEASE: DIRECTION NORMALVEKTOR

class NormalVektorFromRotation(ThreeDScene, MovingCameraScene):
    def construct(self):
        self.rot_time = 8
        self.start_angle = PI/6
        self.angle = ValueTracker(self.start_angle)

        self.vec_a_num = [1,0,0]
        self.vec_b_num = [np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)


        self.setup_scene(animate = True)
        self.add_updaters()
        self.rotate_vec_b_first()
        self.right_hand_rule_up()
        self.right_hand_rule_down()
        self.right_hand_rule_winding()
        #self.rotate_vec_b_for_sin_term()


    def setup_scene(self, animate = True):
        axes, origin = self.axes, self.origin

        self.vec_a = Arrow(origin, axes.c2p(*self.vec_a_num), color = vec_a_color, buff = 0)
        self.vec_b = Arrow(origin, axes.c2p(*self.vec_b_num), color = vec_b_color, buff = 0)
        self.vec_n = Arrow(origin, axes.c2p(*self.vec_n_num), color = vec_c_color, buff = 0)

        circle = Circle(arc_center = self.origin, radius = self.axis_length/(self.axis_max - self.axis_min), color = GREY)
        circle_ticks = self.get_circle_ticks(circle, PINK)
        circle_ticks_labels = self.get_circle_ticks_labels(circle_ticks, color = GREY)

        tex = MathTex("\\vec{n}", "=", "\\vec{a}", "\\times", "\\vec{b}")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\vec{n}": vec_c_color})\
            .to_edge(UP)

        if animate:
            self.play(
                LaggedStartMap(
                    Create, 
                    VGroup(self.vec_a, self.vec_b, circle, circle_ticks, circle_ticks_labels), 
                    lag_ratio = 0.2
                ),
                run_time = 3
            )
            self.wait()

            self.add_fixed_in_frame_mobjects(tex)
            self.play(
                Write(tex),
                Create(self.vec_n), 
                run_time = 2
            )
            self.wait()
        else:
            self.add(circle, circle_ticks, circle_ticks_labels)
            self.add(self.vec_a, self.vec_b, self.vec_n)

        self.cross_tex = tex

    def add_updaters(self):
        vec_b, vec_n = self.vec_b, self.vec_n
        axes, origin, angle = self.axes, self.origin, self.angle

        vec_b.add_updater(lambda b: b.become(
            Arrow(origin, axes.c2p(*[np.cos(angle.get_value()), np.sin(angle.get_value()), 0]), color = vec_b_color, buff = 0)
        ))

        vec_n.add_updater(lambda n: n.become(
            Arrow(
                origin, 
                axes.c2p(*np.cross(self.vec_a_num, [np.cos(angle.get_value()), np.sin(angle.get_value()), 0])),
                color = vec_c_color, buff = 0
            )
        ))

    def rotate_vec_b_first(self):
        for x in range(1):
            self.play(self.angle.animate(rate_func = linear).set_value(2*PI + self.start_angle), run_time = self.rot_time)
            self.angle.set_value(self.start_angle)
        self.wait()

    def right_hand_rule_up(self):
        svg_up = SVGMobject("Right_Hand_Rule_Up")\
            .scale(1.5)\
            .shift(5*RIGHT)

        for part in svg_up[0], svg_up[12:14]:
            part.set_stroke(color=DARK_GREY, width = 2)

        for part in svg_up[1:12], svg_up[14:]:
            part.set_fill(opacity = 0)
            part.set_stroke(color = DARK_GREY, width = 2)

        self.add_fixed_in_frame_mobjects(svg_up)
        self.play(DrawBorderThenFill(svg_up))
        self.wait()

        self.play(
            ApplyMethod(self.renderer.camera.theta_tracker.set_value, 135*DEGREES, rate_func = smooth, run_time = 3),
            ApplyMethod(self.renderer.camera.phi_tracker.set_value, -60*DEGREES, rate_func = smooth, run_time = 3),
            ApplyMethod(self.renderer.camera.gamma_tracker.set_value, -55*DEGREES, rate_func = smooth, run_time = 3),
            self.angle.animate(rate_func = linear).set_value(90*DEGREES),
            run_time = 3
        )
        self.wait()


        start_a = self.axes.c2p(1.1, -2.45, 0)
        hand_a = Arrow(start_a, self.axes.c2p(2.1, -2.3, 0), buff = 0, color = vec_a_color)

        start_b = self.axes.c2p(1.1, -2.2, 0)
        hand_b = Arrow(start_b, self.axes.c2p(1, -1.2, 0), buff = 0, color = vec_b_color)

        start_c = self.axes.c2p(1.1, -2.33, 0)
        hand_c = Arrow(start_c, self.axes.c2p(1.1, -2.1, 0.8), buff = 0, color = vec_c_color)

        vec_copys = [vec.copy() for vec in [self.vec_a, self.vec_b, self.vec_n]]
        hands = [hand_a, hand_b, hand_c]

        for index in range(len(vec_copys)):
            self.play(
                TransformFromCopy(vec_copys[index], hands[index]), 
                run_time = 3
            )
            self.wait()
        self.wait(2)

        # self.play(
        #     *[GrowArrow(arrow, rate_func = lambda t: smooth(1-t), run_time = 2) for arrow in [hand_a, hand_b, hand_c]]
        # )
        # self.wait()
        self.svg_up = svg_up

    def right_hand_rule_down(self):
        svg_down = SVGMobject("Right_Hand_Rule_Down")\
            .scale(1.5)\
            .shift(5*RIGHT)\
            .set_stroke(width = 3)\
            .set_stroke(color=DARK_GREY, width = 2)

        self.play(
            Transform(self.svg_up, svg_down, run_time = 1), 
            ApplyMethod(self.renderer.camera.theta_tracker.set_value, -15*DEGREES, rate_func = smooth, run_time = 3),
            ApplyMethod(self.renderer.camera.phi_tracker.set_value, 70*DEGREES, rate_func = smooth, run_time = 3),
            ApplyMethod(self.renderer.camera.gamma_tracker.set_value, 0*DEGREES, rate_func = smooth, run_time = 3),
            self.angle.animate(rate_func = linear, run_time = 3).set_value(-90*DEGREES),
        )
        self.wait()


        start_a = self.axes.c2p(0.3, 2.5, 0)
        hand_a = Arrow(start_a, self.axes.c2p(1.3, 2.32, 0), buff = 0, color = vec_a_color)

        start_b = self.axes.c2p(0, 2.2, 0.05)
        hand_b = Arrow(start_b, self.axes.c2p(0, 1.2, 0.05), buff = 0, color = vec_b_color)

        start_c = self.axes.c2p(0.3, 2.0, 0)
        hand_c = Arrow(start_c, self.axes.c2p(0.3, 2.0, -1), buff = 0, color = vec_c_color)

        vec_copys = [vec.copy() for vec in [self.vec_a, self.vec_b, self.vec_n]]
        hands = [hand_a, hand_b, hand_c]

        for index in range(len(vec_copys)):
            self.play(
                TransformFromCopy(vec_copys[index], hands[index]), 
                run_time = 3
            )
            self.wait()

        # self.play(
        #     AnimationGroup(
        #         *[TransformFromCopy(vec.copy(), hand) for vec, hand in zip([self.vec_a, self.vec_b, self.vec_n], [hand_a, hand_b, hand_c])], 
        #         lag_ratio = 0.2
        #     ), 
        #     run_time = 5
        # )
        self.wait(2)

        self.play(
            *[GrowArrow(arrow, rate_func = lambda t: smooth(1-t), run_time = 2) for arrow in [hand_a, hand_b, hand_c]]
        )
        self.wait()

        self.svg_down = svg_down

    def right_hand_rule_winding(self):
        svg2_winding = SVGMobject("Right_Hand_Rule_Winding")\
            .scale(1.5)\
            .shift(5*RIGHT)\
            .set_stroke(width = 3)\
            .set_stroke(color=DARK_GREY, width = 2)
        svg2_winding[-1].set_stroke(width = 1)

        self.play(
            Transform(self.svg_up, svg2_winding, run_time = 1), 
            ApplyMethod(self.renderer.camera.theta_tracker.set_value, 120*DEGREES, rate_func = smooth, run_time = 3),
            ApplyMethod(self.renderer.camera.phi_tracker.set_value, 70*DEGREES, rate_func = smooth, run_time = 3),
            self.angle.animate(rate_func = linear).set_value(90*DEGREES),
        )
        self.wait()

        arc_vecs = Arc(
            radius = 3.5, start_angle = 0, angle = 90*DEGREES, 
            arc_center = self.origin, color = GREEN
        ).add_tip()

        arcs_hand = VGroup(*[
            Arc(
                radius = 1.5, start_angle = -20*DEGREES, angle = 90*DEGREES, color = GREEN,
                arc_center = self.axes.c2p(-2,-0.3, z)
            ).add_tip()
            for z in [0,0.2,0.4,0.6]
        ])

        a_copy = self.vec_a.copy().clear_updaters().save_state()
        b_copy = self.vec_b.copy().clear_updaters().save_state()
        self.play(
            Transform(a_copy, b_copy, path_arc = PI/2),
            Create(arc_vecs),
            run_time = 5
        )
        self.remove(a_copy)
        self.wait()


        start_c = self.axes.c2p(-2, 0, 0.2)
        hand_c = Arrow(start_c, self.axes.c2p(-1.95, 0, 1.2), buff = 0, color = vec_c_color)

        added_anims = [TransformFromCopy(self.vec_n.copy(), hand_c)]
        for x in range(5):
            if x == 2:
                self.play(*[Create(arc) for arc in arcs_hand], *added_anims, run_time = 4)
                self.wait(0.5)
            else:
                self.play(*[Create(arc) for arc in arcs_hand], run_time = 2)
                self.wait(0.5)
        self.wait(3)

        fadeout_group = VGroup(arc_vecs, *arcs_hand, hand_c, self.svg_up, self.cross_tex)
        self.play(
            ApplyMethod(self.renderer.camera.theta_tracker.set_value, 45*DEGREES, rate_func = smooth),
            FadeOut(fadeout_group, lag_ratio = 0.1),
            run_time = 3
        )
        self.wait()

    def rotate_vec_b_for_sin_term(self):

        arc_kwargs = {"radius": 1, "arc_center": self.origin, "color": GREEN}
        arc = Arc(start_angle = self.vec_a.get_angle(), angle = self.vec_b.get_angle() - self.vec_a.get_angle(), **arc_kwargs)

        self.play(Create(arc), run_time = 2)
        self.wait()

        arc.add_updater(lambda arc: arc.become(
            Arc(
                start_angle = self.vec_a.get_angle(), 
                angle = self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b), 
                **arc_kwargs
            )
        ))

        for x in range(3):
            self.play(self.angle.animate(rate_func = linear).set_value(2*PI + self.start_angle), run_time = self.rot_time)
            self.angle.set_value(self.start_angle)
        self.wait(3)


    # functions
    def get_circle_ticks(self, circle, color):
        ticks_num = 12

        ticks = VGroup()
        for num in range(ticks_num):
            tick = Line(LEFT, RIGHT)\
                .set_length(0.2)\
                .set_color(color)\
                .rotate(num * 360/ticks_num * DEGREES)\
                .move_to(circle.point_from_proportion(num/ticks_num))

            vect = tick.get_center() - self.origin
            vect_norm = [-vect[1], vect[0], 0]
            tick.rotate_in_place(90*DEGREES, axis = vect_norm)
            
            ticks.add(tick)

        return ticks

    def get_circle_ticks_labels(self, circle_ticks, color):
        num_ticks = len(circle_ticks)

        texs = VGroup(*[
            MathTex(tex)\
                .set_color(color)\
            for tex in ["0^\\circ", "90^\\circ", "180^\\circ", "270^\\circ"]
        ])
        texs[0].next_to(circle_ticks[0], RIGHT)
        texs[1].next_to(circle_ticks[3], UP)
        texs[2].next_to(circle_ticks[6], LEFT)
        texs[3].next_to(circle_ticks[9], DOWN)

        return texs

    def angle_between_vectors_bigger_than_pi(self, arrow_a, arrow_b):
        angle = arrow_b.get_angle() - arrow_a.get_angle()

        if angle < 0:
            new_angle = angle + TAU
            return new_angle
        else:
            return angle


class NormaleVektorForAnitKommutativ(ThreeDScene):
    def construct(self):
        self.vec_a_num = [2/3, -1/3, 2/3]
        self.vec_b_num = [2/3,  2/3, -1/3]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length, 
            axis_config = {"color": DARK_GREY},
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)

        self.setup_scene()
        self.a_cross_b()
        self.b_cross_a()

    def setup_scene(self):
        axes, origin = self.axes, self.origin

        self.vec_a = Arrow3D(origin, axes.c2p(*self.vec_a_num), color = vec_a_color)
        self.vec_b = Arrow3D(origin, axes.c2p(*self.vec_b_num), color = vec_b_color)
        self.vec_n = Arrow3D(origin, axes.c2p(*self.vec_n_num), color = vec_c_color)


        lines_kwags = {"stroke_width": 2, "color": GREY, "stroke_opacity": 0.2}
        lines_a = VGroup(*[
            Line(
                start = self.axes.c2p(*[-1.5*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[+1.5*comp_a + s*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for s in np.linspace(-1.5,1.5,7)
        ])

        lines_b = VGroup(*[
            Line(
                start = self.axes.c2p(*[r*comp_a - 1.5*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                end  =  self.axes.c2p(*[r*comp_a + 1.5*comp_b for comp_a, comp_b in zip(self.vec_a_num, self.vec_b_num)]), 
                **lines_kwags
            )
            for r in np.linspace(-1.5,1.5,7)
        ])

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


        self.play(
            LaggedStartMap(
                Create, VGroup(self.axes, big_rect, lines_a, lines_b, self.vec_a, self.vec_b), lag_ratio = 0.25
            ), 
            run_time = 3
        )
        self.wait(2)

    def a_cross_b(self):
        self.move_camera(phi = 70*DEGREES, theta = 100*DEGREES, run_time = 8)
        self.play(Create(self.vec_n), run_time = 3)
        self.wait()

    def b_cross_a(self):
        self.move_camera(phi = 70*DEGREES, theta = -10*DEGREES, run_time = 8)
        self.wait()

        vec_n2_num = np.cross(self.vec_b_num, self.vec_a_num)
        self.vec_n2 = Arrow3D(self.origin, self.axes.c2p(*vec_n2_num), color = vec_c_color)

        self.play(Create(self.vec_n2), run_time = 3)
        self.wait(3)


class AntiKommutativ(Scene):
    def construct(self):
        # svg_up = SVGMobject("Right_Hand_Rule_UP")\
        #     .scale(1.5)\
        #     .to_corner(UR)\
        #     .rotate(angle = 45*DEGREES)

        # for part in svg_up[0], svg_up[12:14]:
        #     part.set_stroke(color = DARK_GREY, width = 2)

        # for part in svg_up[1:12], svg_up[14:]:
        #     part.set_fill(opacity = 0)
        #     part.set_stroke(color = DARK_GREY, width = 2)

        a_cross_b = MathTex("\\vec{a}", "\\times", "\\vec{b}")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .next_to(1.4*RIGHT + 1.75*UP, RIGHT)

        self.play(Write(a_cross_b))
        self.wait()

        svg_down = SVGMobject("Right_Hand_Rule_Down")\
            .scale(1.25)\
            .to_edge(LEFT)\
            .set_stroke(width = 3)\
            .set_stroke(color = DARK_GREY, width = 2)\
            .rotate(angle = -30*DEGREES)\
            .rotate(angle = 10*DEGREES, axis = RIGHT)

        b_cross_a = MathTex("\\vec{b}", "\\times", "\\vec{a}")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .next_to(1.4*LEFT + 1.75*DOWN, DOWN)

        self.play(Write(b_cross_a))
        self.wait()

        self.play(Create(svg_down), run_time = 3)
        self.wait()


        equals = MathTex("=", "-")\
            .next_to(a_cross_b, RIGHT)\
            .shift(0.1*DOWN)
        equals[1].set_color(vec_c_color)

        ba = b_cross_a.copy()
        self.play(
            Write(equals, run_time = 1),
            ba.animate(run_time = 4).next_to(equals, RIGHT).shift(0.1*UP)
        )
        self.wait(3)

        anti = Tex("Anti", "$-$", "Kommutativ")\
            .scale(1.15)\
            .next_to(equals, UP, buff = 0.5)
        anti[:2].set_color(vec_c_color)

        self.play(Write(anti))
        self.wait(3)


class CGPhysicsImage(Scene):
    def construct(self):
        frame = ScreenRectangle(height = 5, color = GREY, stroke_width = 3)
        frame.to_corner(DR)

        # image = ImageMobject("cg-physics-image")
        # image.set(height = frame.height)
        # image.move_to(frame)

        self.frame = frame

        self.add(frame)
        self.wait()

        self.old_lorentz()
        self.current_direction()
        self.magnetic_direction()
        self.new_lorentz()
        # self.all_directions()

    def old_lorentz(self):
        #             0     1    2    3       4      5       6      7
        eq = MathTex("F_", "L", "=", "q", "\\cdot", "v", "\\cdot", "B")\
            .scale(1.25)\
            .to_edge(UP).shift(3*RIGHT)\
            .set_color_by_tex_to_color_map({"F": GREEN, "L": GREEN, "v": YELLOW, "B": BLUE})

        name = Tex("Lorentzkraft")\
            .scale(1.25)\
            .set_color(GREEN)\
            .next_to(eq, LEFT, buff = 0.5)


        self.play(
            FadeIn(name, shift = 3*RIGHT),
            Write(eq)
        )
        self.wait()

        texts = VGroup(*[
            Tex(tex).next_to(eq, DOWN, buff = 0.9) for tex in [
                "Elementarladung e", 
                "Geschwindigkeit der Elektronen", 
                "Flussdichte des Magnetfeldes"
            ]
        ])

        parts = [eq[3], eq[5], eq[7]]

        for index in range(len(texts)):
            self.play(parts[index].animate.shift(0.5*DOWN))
            self.play(FadeIn(texts[index], shift = 3*RIGHT))
            self.wait()
            self.play(
                parts[index].animate.shift(0.5*UP),
                FadeOut(texts[index], shift = 3*RIGHT),
            )
            self.wait(0.5)
        self.play(FadeOut(name, shift = 3 * LEFT))
        self.old_eq = eq

    def current_direction(self):
        minus = self.get_pols(BLUE_E, "$-$")\
            .move_to(4.15*RIGHT + 0.65*DOWN)
        plus = self.get_pols(RED_E, "$+$")\
            .move_to(1.75*RIGHT + 0.65*DOWN)

        for sign in minus, plus:
            sign.save_state()

        self.play(*[FocusOn(sign, run_time = 1) for sign in [minus, plus]])
        self.play(
            GrowFromEdge(plus, RIGHT), 
            GrowFromEdge(minus, LEFT), 
        )
        self.wait()

        signs = VGroup(plus, minus)
        signs.generate_target()
        signs.target.arrange_submobjects(RIGHT, buff = 4).to_corner(UL)

        self.play(
            MoveToTarget(signs),
            run_time = 2.5
        )

        dots = VGroup(*[Dot() for dot in range(50)])\
            .arrange_submobjects(RIGHT, buff = 0.25)\
            .next_to(minus.get_center(), RIGHT, buff = 0)\
            .set_fill(opacity = 0)

        self.add(dots)
        self.wait()
        def particle_updater(d, dt):
            d.shift(0.02*LEFT)

            if d.get_center()[0] < minus.get_left()[0]:
                d.set_fill(opacity = 1)

            if d.get_center()[0] < plus.get_right()[0]:
                d.fade(darkness = 1)
    
        for dot in dots:
            dot.add_updater(particle_updater)
        self.wait(5)

        arrow = Arrow(minus.get_bottom(), plus.get_bottom(), color = YELLOW, stroke_width = 3)
        arrow.shift(0.25*DOWN)
        dir_phy = Tex("physikalische ", "Stromrichtung")
        dir_tec = Tex("technische ", "Stromrichtung")

        for tex in dir_phy, dir_tec:
            tex.next_to(arrow, DOWN)
            tex.set(width = arrow.width)
            tex.set_color(YELLOW)

        dir_tec.set(height = dir_phy.height)
        dir_tec.move_to(dir_phy, aligned_edge=RIGHT)
        

        self.play(GrowArrow(arrow), run_time = 2)
        self.wait()

        self.play(Write(dir_phy))
        self.wait(2)

        arrow2 = arrow.copy().rotate(TAU/2)
        self.play(
            AnimationGroup(
                Transform(arrow, arrow2),
                ReplacementTransform(dir_phy, dir_tec),
                lag_ratio = 0.75
            ), 
            run_time = 2
        )
        self.wait(7)

        for dot in dots:
            dot.clear_updaters()
            self.remove(dot)

    def magnetic_direction(self):
        north = self.get_pols(RED, "N")\
            .move_to(2.95*RIGHT + 2*DOWN)
        south = self.get_pols(GREEN, "S")\
            .move_to(2.95*RIGHT + 0.75*UP)

        self.play(*[FocusOn(sign, run_time = 1) for sign in [north, south]])
        self.play(
            GrowFromEdge(north, UP), 
            GrowFromEdge(south, DOWN), 
            run_time = 2
        )
        self.wait()

        self.play(VGroup(north, south).animate.to_edge(LEFT, buff = 1.5), run_time = 2)

        field_line = Arrow(north.get_top(), south.get_bottom(), color = BLUE)
        self.play(GrowArrow(field_line), run_time = 2)
        self.wait()

    def new_lorentz(self):
        #                0         1    2    3       4         5           6           7
        eq = MathTex("\\vec{F}_", "L", "=", "q", "\\cdot", "\\vec{v}", "\\times", "\\vec{B}")\
            .scale(1.25)\
            .next_to(self.old_eq, DOWN, aligned_edge=LEFT)\
            .set_color_by_tex_to_color_map({"\\vec{F}": GREEN, "L": GREEN, "\\vec{v}": YELLOW, "\\vec{B}": BLUE})


        self.play(Write(eq[0:3], run_time = 1.5))
        self.wait()

        for i in [5,7,6]:
            self.play(TransformFromCopy(self.old_eq[i], eq[i]), run_time = 1.5)
            self.wait()
        self.play(Write(eq[3:5]))
        self.wait()


        sur_rects = VGroup(*[
            SurroundingRectangle(mob, color = RED)
            for mob in [eq, eq[6]]
        ])
        self.play(Create(sur_rects[0]), run_time = 3)
        self.wait()

        self.play(Transform(sur_rects[0], sur_rects[1]), run_time = 2)
        self.wait(3)


    # def all_directions(self):
    #     image2 = ImageMobject("cg-physics-image2")
    #     image2.set(height = self.frame.height)
    #     image2.move_to(self.frame)

    #     self.add(image2)

    #     start = 2.5*RIGHT + 0.5*DOWN
    #     cur = Arrow(start, start + 1.25*RIGHT + 0.2*UP, color = YELLOW, buff = 0)
    #     mag = Arrow(start, start + UP, color = BLUE, buff = 0)
    #     lor = Arrow(start, start + RIGHT, color = GREEN, buff = 0)

    #     self.add(cur, mag, lor)


    # functions
    def get_pols(self, fill_color, sign):
        circle = Circle(radius = 0.25, stroke_width = 1, color = WHITE)
        circle.set_fill(color = fill_color, opacity = 0.5)

        sign = Tex(sign)
        sign.move_to(circle)

        pol = VGroup(circle, sign)
        pol.sign = sign

        return pol


class CGPhysicsThankYou(Scene):
    def construct(self):
        frame = ScreenRectangle(height = 5, color = GREY, stroke_width = 3)
        frame.to_corner(DR)
        self.add(frame)
        self.wait()

        thanks = Tex("Thank ", "You", ",")\
            .scale(1.25)\
            .to_corner(UL)
        self.play(FadeIn(thanks, shift = 3*DOWN), run_time = 2)
        self.wait()

        def func(t):
            return np.array((16 * np.sin(t)**3, 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t), 0))

        heart = ParametricFunction(func, t_range = np.array([0, TAU]))\
            .set_color(RED)\
            .scale(0.1)\
            .next_to(thanks, DOWN)

        self.play(Create(heart), run_time = 3)

        cg = Tex("cg-physics")\
            .scale(1.5)\
            .move_to(heart)\
            .set_color_by_gradient(RED, BLUE, GREEN, YELLOW)

        self.play(Transform(heart, cg))
        self.wait(3)


class Right_Vs_Left(Scene):
    def construct(self):
        halt_stop = Tex("Halt Stop!")\
            .scale(3)

        self.add(halt_stop)
        self.wait()
        self.play(ScaleInPlace(halt_stop, scale_factor = 100))
        self.remove(halt_stop)

        left = Tex("Linke", "-", "Hand", "-", "Regel")
        right = Tex("Rechte", "-", "Hand", "-", "Regel")

        for mob, color in zip([left, right], [RED, BLUE]):
            mob[:3].set_color_by_gradient(color, WHITE)

        lr_tex = VGroup(left, right)\
            .arrange_submobjects(RIGHT, buff = 4)\
            .to_edge(UP, buff = 1.5)

        lr_svg = VGroup(*[SVGMobject(name).shift(0.5*DOWN).scale(1.75) for name in ["Left_Hand_Rule_Up", "Right_Hand_Rule_Up"]])\
            .arrange_submobjects(RIGHT, buff = 3)

        for part in lr_svg[0][0], lr_svg[0][12:14], lr_svg[1][0], lr_svg[1][12:14]:
            part.set_stroke(color = LIGHT_GREY, width = 2)
            part.set_fill(color = BLACK, opacity = 1)

        for part in lr_svg[0][1:12], lr_svg[0][14:], lr_svg[1][1:12], lr_svg[1][14:]:
            part.set_fill(opacity = 0)
            part.set_stroke(color = LIGHT_GREY, width = 2)

        self.play(Write(lr_tex[1]), run_time = 0.75)
        self.play(Write(lr_svg[1]), run_time = 1.5)
        self.wait()

        self.play(
            Rotating(lr_svg[1].copy(), radians = TAU/2, axis = UP, about_point = ORIGIN, rate_func = smooth, run_time = 2),
            TransformFromCopy(lr_tex[1], lr_tex[0], run_time = 1.5),
        )
        self.wait(0.5)
        self.play(Indicate(lr_tex[0]))
        self.play(Circumscribe(lr_tex[0], time_width = 0.6, run_time = 2))
        self.wait(3)


class ThumbnailDirection(NormalVektorFromRotation):
    def construct(self):
        self.rot_time = 8
        self.start_angle = PI/6
        self.angle = ValueTracker(self.start_angle)

        self.vec_a_num = [1,0,0]
        self.vec_b_num = [np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)
        
        self.setup_scene(animate = False)
        self.add_updaters()
        self.rotate_vec_b_first()
        self.right_hand_rule_up()



        for part in self.svg_up[0], self.svg_up[12:14]:
            part.set_stroke(color = LIGHT_GREY, width = 2)
            part.set_fill(color = BLACK, opacity = 1)

        for part in self.svg_up[1:12], self.svg_up[14:]:
            part.set_fill(opacity = 0)
            part.set_stroke(color = LIGHT_GREY, width = 2)



        acb = MathTex("\\vec{n}", "=", "\\vec{a}", "\\cross", "\\vec{b}")\
            .scale(1.5)\
            .set_color_by_tex_to_color_map({"\\vec{n}": vec_c_color, "\\vec{b}": vec_b_color, "\\vec{a}": vec_a_color})

        self.add_fixed_in_frame_mobjects(acb)
        acb.move_to(3*RIGHT + 2.5*UP)


class ThumbnailDirection2(Scene):
    def construct(self):
        dir = Tex("Richtung")\
            .scale(2.5).to_edge(UP).set_color_by_gradient(vec_a_color, vec_b_color)\
            .set_fill(color = GREY, opacity = 0.5).set_stroke(width = 3)

        des = Tex("des")
        nv = Tex("Normalenvektors")\
            .scale(2.5).to_edge(DOWN).shift(UP).set_color(vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5).set_stroke(width = 2)

        self.add(dir, des, nv)



# SCENE GEOMETRIC INTERPRETATION

class IntroGeo(Calculations):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6,
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.path_color = LIGHT_BROWN

        self.vec_a_num = [ 2,-1, 1]
        self.vec_b_num = [-1, 2, 1]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        self.setup_scene()
        self.cross_path_animation()
        self.more_than_a_vector()
        self.calc_area()
        self.vectors_into_para()

    def setup_scene(self):
        vec_a_num, vec_b_num, vec_n_num = self.vec_a_num, self.vec_b_num, self.vec_n_num

        mat_a = self.get_vector_matrix_from_num_vec(vec_a_num, **self.mat_kwargs)
        mat_b = self.get_vector_matrix_from_num_vec(vec_b_num, **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type = "times", color = vec_c_color)
        vec_group.move_to(np.array([-3.5, 0, 0]))

        name = Tex("Kreuz","produkt")
        name[0].set_color(vec_c_color)
        name[1].set_color(DARK_GREY)
        name.move_to(np.array([-4.5, 1.592528, 0]))

        equals = MathTex("=").next_to(vec_group, RIGHT)
        mat_n = self.get_vector_matrix_from_num_vec(vec_n_num, **self.mat_kwargs).next_to(equals, RIGHT)

        for mat in mat_a, mat_b, mat_n:
            mat[1:].set_color(DARK_GREY)

        self.play(
            AnimationGroup(
                Write(name),
                Create(vec_group),
                Write(equals),
                Create(mat_n[1:]),
                lag_ratio = 0.2
            ),
            run_time = 2
        )

        self.vec_group, self.equals, self.mat_n, self.name = vec_group, equals, mat_n, name

    def cross_path_animation(self):
        path_x, path_y, path_z = self.get_crossproduct_path_xyz(self.vec_group, stroke_width = 7)
        paths = VGroup(path_x, path_y, path_z)

        cut_lines = self.get_crossproduct_cut_lines(self.vec_group, MAROON)

        # elements for added_anims
        vec_name = Tex("Normalen", "vektor")
        vec_name.next_to(self.mat_n, DOWN, buff = 1, aligned_edge=RIGHT)
        vec_name[0].set_color(vec_c_color)
        vec_name[1].set_color(DARK_GREY)

        vec_labels = VGroup(*[
            MathTex(tex).set_color(color).next_to(mat, DOWN, aligned_edge = DOWN)
            for tex, color, mat in zip(
                ["\\vec{a}", "\\vec{b}", "\\vec{n}"], 
                [vec_a_color, vec_b_color, vec_c_color], 
                [self.vec_group[0], self.vec_group[2], self.mat_n]
            )
        ])

        #                         0        1       2           3          4
        cross_label = MathTex("\\vec{n}", "=", "\\vec{a}", "\\times", "\\vec{b}")\
            .set_color_by_tex_to_color_map({"\\vec{n}": vec_c_color, "\\times": vec_c_color, "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color})\
            .next_to(vec_name, DOWN, aligned_edge=LEFT)
        self.vec_name, self.vec_labels, self.cross_label = vec_name, vec_labels, cross_label


        # Schleife mit cut_lines, paht_i, Einträge hinschreiben
        added_anims = [
            Write(vec_name), 
            FadeIn(vec_labels, shift = 0.5*RIGHT, lag_ratio = 0.2), 
            AnimationGroup(
                TransformFromCopy(vec_labels[2], cross_label[0]), 
                Write(cross_label[1]), 
                TransformFromCopy(vec_labels[1], cross_label[2]),
                Write(cross_label[3]),
                TransformFromCopy(vec_labels[0], cross_label[4]), 
                lag_ratio = 0.3
            )
        ]
        for index in range(len(paths)):
            self.play(
                Create(cut_lines[index], rate_func = there_and_back_with_pause),
                FadeToColor(self.vec_group[0][0][index], DARK_GREY, rate_func = there_and_back_with_pause),
                FadeToColor(self.vec_group[2][0][index], DARK_GREY, rate_func = there_and_back_with_pause),
                ShowPassingFlash(paths[index]), 
                run_time = 2.75
            )
            self.play(
                added_anims[index],
                Write(self.mat_n[0][index]), 
                run_time = 1.5
            )
            self.wait(0.5)
        self.wait(3)

    def more_than_a_vector(self):
        text = Tex("Mehr als nur\\\\", "ein Vektor!")\
            .to_corner(DL, buff = 1)\
            .scale(0.8)


        para = VMobject()
        para.set_points_as_corners([
            np.array([0,0,0]), 
            np.array([3,0,0]),
            np.array([3.5,1.5,0]),
            np.array([0.5,1.5,0]),
            np.array([0,0,0]),
        ])
        para.set_fill(color = vec_c_color, opacity = 0.1)
        para.set_stroke(color = vec_c_color, width = 3)
        para.move_to(text)

        n = 100
        dots = VGroup()
        paths = VGroup()
        for num in range(n):
            dot = Dot(radius = 0.03).set_color(vec_c_color)
            dot.move_to(para.point_from_proportion(num / n))
            dot.save_state()
            dots.add(dot)
            dots.set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)
        for dot in dots:
            dot.move_to(self.cross_label.get_left())
            path = TracedPath(dot.get_center, dissipating_time=0.2, stroke_opacity=[0, 0.5])
            paths.add(path)

        self.add(text)
        self.add(paths)
        self.play(
            AnimationGroup(
                *[Restore(dot) for dot in dots], lag_ratio = 0.05
            ),
            run_time = 2
        )
        self.play(
            FadeOut(dots),
            Create(para),
        )
        self.wait(3)
        self.para, self.text = para, text

    def calc_area(self):
        self.play(
            AnimationGroup(
                FadeOut(VGroup(self.vec_name, self.vec_labels)),
                VGroup(self.name, self.vec_group, self.equals, self.mat_n).animate.to_corner(UL), 
                lag_ratio = 0.4
            ), run_time = 3
        )
        self.wait()

        mat_n_copy = self.mat_n.copy()
        mat_n_copy.generate_target()
        mat_n_copy.target.center().shift(4*LEFT + 0.5*DOWN)

        lvert = MathTex("\\lvert")\
            .next_to(mat_n_copy.target, LEFT)\
            .set(height = mat_n_copy.height)\
            .set_color(DARK_GREY)
            
        rvert = MathTex("\\rvert")\
            .next_to(mat_n_copy.target, RIGHT)\
            .set(height = mat_n_copy.height)\
            .set_color(DARK_GREY)

        self.play(
            MoveToTarget(mat_n_copy, path_arc = -3), 
            Create(VGroup(lvert, rvert), rate_func = squish_rate_func(smooth, 0.4, 1)), 
            run_time = 4
        )
        self.wait()

        #                 0       1       2     3     4    5    6    7     8     9    9   10   11    12   13
        result = MathTex("=", "\\sqrt{", "(", "-3^", "2", ")", "+", "(", "-3^", "2", ")", "+", "3^", "2", "}")
        result.next_to(rvert, RIGHT)

        result2 = MathTex("=", "\\sqrt{27}", "\\approx", "5{,}20")
        result2.next_to(rvert, RIGHT)

        self.play(Write(result))
        self.wait(2)
        self.play(
            FadeOut(result, shift = 0.5*DOWN), 
            FadeIn(result2, shift = 0.5*DOWN), 
            run_time = 1.5
        )
        self.wait(2)

    def vectors_into_para(self):
        vec_a = Arrow(self.para.get_corner(DL), self.para.get_points_defining_boundary()[2], color = vec_a_color, buff = 0)
        vec_b = Arrow(self.para.get_corner(DL), self.para.get_points_defining_boundary()[5], color = vec_b_color, buff = 0)

        self.play(
            AnimationGroup(
                TransformFromCopy(self.cross_label[2], vec_a), 
                TransformFromCopy(self.cross_label[4], vec_b),
                lag_ratio = 0.5
            ),
            run_time = 3
        )
        self.wait()

        text2 = MathTex("5{,}20\\text{ FE}").move_to(self.text)
        self.play(Transform(self.text, text2))
        self.wait(3)


class IntroGeo3D(TwoOrthogonalVectors):
    def construct(self):
        self.vec_a_num = [ 2,-1, 1]
        self.vec_b_num = [-1, 2, 1]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        print(self.vec_n_num)

        axis_length = self.axis_length = 6
        axis_min = self.axis_min = -3
        axis_max = self.axis_max = 3
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length, 
            axis_config = {"color": DARK_GREY},
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)
        self.acr_rate = -0.08
        self.cone_height = 0.25

        self.setup_scene()
        self.draw_plane()
        self.draw_parallelogramm()

    def draw_parallelogramm(self):
        self.wait(5)

        para = self.get_parallelogramm_from_vec_nums(self.vec_a_num, self.vec_b_num)
        self.play(DrawBorderThenFill(para), run_time = 1.5)
        self.bring_to_front(self.vec_a, self.vec_b, self.vec_n)
        self.wait(30)


    # functions
    def get_parallelogramm_from_vec_nums(self, vec_a_num, vec_b_num, fill_opacity = 0.25):
        parallelo = VMobject()\
            .set_points_as_corners([
                self.origin,
                self.axes.c2p(*vec_a_num), 
                self.axes.c2p(*[a + b for a,b in zip(vec_a_num, vec_b_num)]), 
                self.axes.c2p(*vec_b_num), 
                self.origin
            ])\
            .set_fill(color = vec_c_color, opacity = fill_opacity)\
            .set_stroke(color = BLUE, width = 2)

        return parallelo


class AngleDependency(NormalVektorFromRotation):
    def construct(self):
        self.rot_time = 8
        self.start_angle = PI/6
        self.angle = ValueTracker(self.start_angle)

        self.vec_a_num = [1,0,0]
        self.vec_b_num = [np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.5
        axis_max = self.axis_max = 1.5
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)


        self.setup_scene(animate = True)
        self.add_updaters()
        self.rotate_vec_b_first()
        self.rotate_vec_b_for_sin_term()


class CompareDotVsCross(Scene):
    def construct(self):
        frames = VGroup(*[
            ScreenRectangle(height = 3.25, color = GREY, stroke_width = 3)
            for x in range(2)
        ])
        frames.arrange_submobjects(DOWN, buff = 0.5)
        frames.to_edge(LEFT)

        titles = VGroup(*[
            MathTex(*tex)\
                .next_to(screen_frame.get_corner(UR), RIGHT, buff = 1, aligned_edge=UP)\
                .set_color_by_tex_to_color_map({
                    "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "produkt": GREY, "\\times": vec_c_color, "\\cdot": vec_c_color
                })
            for tex, screen_frame in zip(
                [["\\text{Skalar}", "\\text{produkt}\\ ", "\\vec{a}", "\\cdot", "\\vec{b}"], ["\\text{Kreuz}", "\\text{produkt} \\", "\\vec{a}", "\\times", "\\vec{b}"]], 
                frames
            )
        ])


        maths = VGroup(*[
            MathTex(*tex)\
                .next_to(title, DOWN, buff = 1)\
                .shift(RIGHT)\
                .set_color_by_tex_to_color_map({
                    "\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\varphi": GREEN, "\\times": vec_c_color
                })
            for tex, title in zip(
                [
                    ["\\vec{a}", "\\cdot",  "\\vec{b}", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\cos", "(", "\\varphi", ")"], 
                    ["\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")"]
                ],
                titles
            )
        ])
        maths[0][1].set_color(vec_c_color)



        self.add(frames, titles)
        self.wait(2)


        self.play(TransformFromCopy(titles[0][2:], maths[0][:3]), run_time = 2)
        self.play(Write(maths[0][3:]))
        self.wait()

        self.play(
            AnimationGroup(
                TransformFromCopy(titles[1][2:], maths[1][1:4]),
                FadeIn(VGroup(maths[1][0], maths[1][4]), shift = 0.75*UP), 
                lag_ratio = 0.5
            ), 
            run_time = 2
        )
        self.wait()
        self.play(Write(maths[1][5:14]))
        self.wait(0.5)


        ldots = MathTex(".", ".", ".", ".", ".", ".", ".").next_to(maths[1][:14], RIGHT, buff = 0.25, aligned_edge=DOWN)
        self.play(ShowIncreasingSubsets(ldots), run_time = 2)
        self.wait(3)

        self.remove(ldots)
        self.wait()

        self.play(Write(maths[1][14:]))
        self.wait(0.5)

        sur_rects_big = VGroup(*[
            SurroundingRectangle(eq, color = vec_c_color) for eq in maths
        ])
        sur_rects_trig = VGroup(*[
            SurroundingRectangle(eq[-4:], color = vec_c_color) for eq in maths
        ])

        self.play(Create(sur_rects_big[1]))
        self.wait(0.5)
        self.play(Create(sur_rects_big[0]))
        self.wait()

        self.play(
            ReplacementTransform(sur_rects_big[0], sur_rects_trig[0]),
            ReplacementTransform(sur_rects_big[1], sur_rects_trig[1]),
            run_time = 1.5
        )
        self.wait(3)

        self.play(FadeOut(sur_rects_trig, lag_ratio = 0.25), run_time = 2)
        self.wait()


class SinGraphFromRotation(Scene):
    def construct(self):
        self.rot_time = 8
        self.start_angle = PI/6
        self.angle = ValueTracker(self.start_angle)


        self.setup_scene()
        self.vector_to_graph()
        self.sin_equation()
        self.difference_unit_and_non_unit()

    def setup_scene(self):
        self.axes = Axes(
            x_range = [0, 2*PI + 0.5, PI/6], y_range = [-1.25, 1.5], x_length = 7, y_length = 4, 
            y_axis_config = {"include_numbers": True}, 
        )
        self.axes.to_corner(DL)

        self.axes_rad_labels = VGroup(*[
            MathTex(tex).scale(0.75).next_to(self.axes.c2p(x_coord, 0), DOWN)
            for tex, x_coord in zip(["180^\\circ", "360^\\circ"], [PI, 2*PI])
        ])

        self.axes_cross_label = MathTex("\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert")\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\times": vec_c_color, "\\vec{b}": vec_b_color})\
            .next_to(self.axes.y_axis.get_tip(), UP)

        self.axes_x_label = MathTex("\\varphi")\
            .set_color(GREEN)\
            .next_to(self.axes.x_axis.get_tip(), RIGHT)

        self.play(
            LaggedStartMap(
                Create,
                VGroup(self.axes, self.axes_rad_labels, self.axes_cross_label[1:-1], self.axes_x_label), 
                lag_ratio = 0.15
            ), 
            run_time = 3
        )
        self.wait()

    def vector_to_graph(self):
        sin_vec = self.get_sin_vector()
        sin_graph = self.get_sin_graph()

        self.play(
            Create(sin_graph), 
            FadeIn(sin_vec, shift = DOWN + 2*LEFT), 
            run_time = 2
        )
        self.wait()

        sin_vec.add_updater(lambda vec: vec.become(self.get_sin_vector()))
        sin_graph.add_updater(self.update_sin_graph())

        self.play(
            self.angle.animate.set_value(2*PI), 
            rate_func = linear, run_time = 11/12 * self.rot_time
        )
        sin_graph.clear_updaters()
        self.angle.set_value(0)

        for x in range(1):
            self.play(
                self.angle.animate.set_value(2*PI), 
                rate_func = linear, run_time = self.rot_time
            )
            self.angle.set_value(0)


        self.play(
            self.angle.animate.set_value(self.start_angle), 
            rate_func = linear, run_time = 1/12 * self.rot_time
        )
        self.wait()

    def sin_equation(self):
        #                 0           1          2        3      4      5       6        7
        eq1 = MathTex("\\vec{a}", "\\times", "\\vec{b}", "=", "\\sin", "(", "\\varphi", ")")

        #                 0            1          2       3         4         5           6          7         8          9           10         11       12     13       14     15        
        eq2 = MathTex("\\vec{a}", "\\times", "\\vec{b}", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")")

        #                 0          1           2          3          4        5       6          7            8        9          10         11         12         13       14     15      16       17
        eq3 = MathTex("\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")")
        self.eq3 = eq3

        for eq in eq1, eq2, eq3:
            eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color, "\\varphi": GREEN})
            eq.scale(1.4)

        eq1.to_corner(UL, buff = 0.35)
        eq2.move_to(eq1, aligned_edge=LEFT)
        eq3.move_to(eq1, aligned_edge=LEFT)

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
        self.wait()


        brace_left = Brace(eq2[0:3], DOWN, color = DARK_GREY)
        brace_left2 = Brace(eq3[0:5], DOWN, color = DARK_GREY)
        brace_right = Brace(eq2[4:], DOWN, color = DARK_GREY)
        brace_right2 = Brace(eq3[6:], DOWN, color = DARK_GREY)

        brace_left_tex = brace_left.get_text("Vektor")
        brace_left_tex2 = brace_left2.get_text("Zahl")
        brace_right_tex = brace_right.get_text("Zahl")
        brace_right_tex2 = brace_right2.get_text("Zahl")

        self.play(
            LaggedStartMap(
                FadeIn, VGroup(brace_left, brace_right), lag_ratio = 0.1
            ), 
            run_time = 1.5
        )
        self.wait()

        self.play(Write(brace_left_tex))
        self.wait()
        self.play(Write(brace_right_tex))
        self.wait()


        self.play(
            ReplacementTransform(eq2[:3], eq3[1:4]),
            FadeIn(VGroup(eq3[0], eq3[4]), shift = DOWN, lag_ratio = 0.2),
            ReplacementTransform(eq2[3], eq3[5]),
            ReplacementTransform(eq2[4:], eq3[6:]),
            FadeIn(VGroup(self.axes_cross_label[0], self.axes_cross_label[-1]), shift = DOWN, lag_ratio = 0.2),
            run_time = 2
        )
        self.play(
            ReplacementTransform(brace_left, brace_left2),
            ReplacementTransform(brace_left_tex, brace_left_tex2),
            ReplacementTransform(brace_right, brace_right2),
            ReplacementTransform(brace_right_tex, brace_right_tex2)
        )
        self.wait(3)

        self.play(
            LaggedStartMap(FadeOut, VGroup(brace_left_tex2, brace_left2, brace_right_tex2, brace_right2), shift = 0.5*DOWN, lag_ratio = 0.1),
            run_time = 2
        )
        self.wait()

    def difference_unit_and_non_unit(self):
        dline = always_redraw(
            lambda: DashedLine(
                start = self.axes.c2p(0, np.sin(self.angle.get_value())),
                end = self.axes.c2p(self.angle.get_value(), np.sin(self.angle.get_value())),
                buff = 0, color = GREY
            )
        )

        arrow1 = Arrow(UP, 0.25*LEFT, stroke_width = 3, color = MAROON).next_to(self.eq3[6:9], DOWN)
        tex1 = MathTex("=", "1").next_to(arrow1, DOWN)

        arrow2 = Arrow(UP, 0.25*RIGHT, stroke_width = 3, color = LIGHT_BROWN).next_to(self.eq3[10:13], DOWN)
        tex2 = tex1.copy().next_to(arrow2, DOWN)

        tex3 = MathTex("\\neq", "1").move_to(tex1)
        tex4 = tex3.copy().move_to(tex2)

        self.play(
            *[GrowArrow(arrow) for arrow in [arrow1, arrow2]], 
            *[FadeIn(tex, shift = direction, rate_func = squish_rate_func(smooth, 0.4,1)) for tex, direction in zip([tex1, tex2], [RIGHT, LEFT])], 
            Create(dline),
            run_time = 2
        )
        self.wait(0.5)

        self.play(
            self.angle.animate.set_value(2*PI), 
            rate_func = linear, run_time = 11/12 * self.rot_time
        )
        self.angle.set_value(0)
        self.play(
            self.angle.animate.set_value(self.start_angle), 
            rate_func = linear, run_time = 1/12 * self.rot_time
        )
        self.wait()

        # non_unit_vectors
        self.play(Transform(tex1, tex3), Transform(tex2, tex4))
        self.wait(3)


    # functions
    def get_sin_vector(self):
        return Arrow(
            start = self.axes.c2p(self.angle.get_value(), 0),
            end = self.axes.c2p(self.angle.get_value(), np.sin(self.angle.get_value())), 
            buff = 0, color = vec_c_color,
        )

    def get_sin_graph(self):
        graph = self.axes.get_graph(
            lambda x: np.sin(x), 
            x_range = [0, self.angle.get_value()], 
            color = vec_c_color
        )
        return graph

    def update_sin_graph(self):
        def updater(mob):
            graph = self.get_sin_graph()
            mob.become(graph)
        return updater


class SinusGraph(Scene):
    def construct(self):
        self.axes_config = {"color": GREY, "stroke_width": 4}
        self.graph_line_config = {"color": vec_c_color, "stroke_width": 4}
        self.unit_c_line_config = {"color": WHITE, "stroke_width": 4}
        self.vec_kwargs = {"buff": 0, "rectangular_stem_width": 0.02, "tip_width_to_length_ratio": 0.6}


        self.show_axis()
        self.show_circle_and_axis_func()
        self.move_dot_and_draw_curve()

    def show_axis(self):
        x_start = np.array([-6.25,0,0])
        x_end = np.array([-3.75,0,0])

        y_start = np.array([-5,-1.25,0])
        y_end = np.array([-5,1.25,0])

        x_axis = Line(x_start, x_end, **self.axes_config)
        y_axis = Line(y_start, y_end, **self.axes_config)

        self.add(x_axis, y_axis)

        self.orgin_point = np.array([-5,0,0])
        self.curve_start = np.array([-3,0,0])

    def show_circle_and_axis_func(self):
        circle = Circle(radius = 1, color = GREY, stroke_width = 4)\
            .move_to(self.orgin_point)

        self.circle = circle

        axes = self.axes = Axes(
            x_range = [0, 9.5, 1], y_range = [-1.25, 1.25, 1], y_length = 2.5, x_length = 9.5,
            axis_config = {
                "color": GREY, 
                "font_size": 36, 
                "include_numbers": False, 
                "stroke_width": 2, 
                "tick_size": 0.0,
                "include_tip": False, 
            },
            y_axis_config = {
                "unit_size": 1, "tick_size": 0.1, 
                "decimal_number_config": {"num_decimal_places": 0, "color": GREY}
            }, 
            x_axis_config = {
                "unit_size": 1, "tick_size": 0.05,
                "longer_tick_multiple": 2, "numbers_with_elongated_ticks": [1,2,3,4,5,6,7,8]
            },
        )


        axes.shift(1.75*RIGHT)
        self.origin_axes = axes.coords_to_point(0,0)

        axes.y_axis.add_numbers(x_values = [-1,1])


        ticks_x_axis_tex = [
            MathTex("\\frac{\\pi}{2}"), MathTex("\\pi"), MathTex("\\frac{3\\pi}{2}"), MathTex("2\\pi"), 
            MathTex("\\frac{5\\pi}{2}"), MathTex("3\\pi"), MathTex("\\frac{7\\pi}{2}"), MathTex("4\\pi"), 
            MathTex("\\frac{9\\pi}{2}")
        ]
        ticks_x_axis_labels = VGroup()
        for x, tex in enumerate(ticks_x_axis_tex):
            tex.set_color(GREY)
            tex.scale(0.5)
            tex.next_to(axes.x_axis.number_to_point((x+1)), DOWN, buff = 0.25)
            ticks_x_axis_labels.add(tex)
        axes.add(ticks_x_axis_labels)


        self.play(
            LaggedStartMap(Create, VGroup(circle, axes), lag_ratio = 0.75), run_time = 3
        )

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        orgin_point = self.orgin_point

        dot = self.dot = Dot(radius=0.06, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 1/8 #0.25


        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_y_axis():
            return Line(orgin_point, np.array([-5, dot.get_center()[1],0]), color=vec_c_color, stroke_width = 4)

        def get_line_to_circle():
            return Line(orgin_point, dot.get_center(), **self.unit_c_line_config)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return DashedLine(dot.get_center(), np.array([x,y,0]), color=GREY, stroke_width=4, dash_length = 0.05)


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start, **self.graph_line_config))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), **self.graph_line_config)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)


        origin_to_circle_line = always_redraw(get_line_to_circle)
        origin_to_y_axis_line = always_redraw(get_line_to_y_axis)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.dot_to_curve_line = dot_to_curve_line

        self.add(orbit, origin_to_y_axis_line, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.add(dot)
        self.wait(20)


class SinusTriangle(Scene):
    def construct(self):
        self.x_max = 3
        self.circle_radius = 3

        self.setup_scene()
        self.create_triangle()
        self.label_triangle()

    def setup_scene(self):
        #                                  0          1           2          3          4        5       6          7            8        9          10         11         12         13       14     15      16       17
        sin_eq = self.sin_eq = MathTex("\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")")
        sin_eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color, "\\varphi": GREEN})
        sin_eq.scale(1.4)
        sin_eq.move_to(np.array([-3.26364788, 3.22184406, 0]))

        self.add(sin_eq)
        self.wait()

    def create_triangle(self):
        thales = Circle(radius = self.circle_radius).shift(2*LEFT)
        proportions = [0.5, 0, 0.35]
        dots_triangle = VGroup(*[
            Dot().set_color(GREY).move_to(thales.point_from_proportion(prop))
            for prop in proportions
        ])

        triangle = VMobject()
        triangle.set_points_as_corners([
            *[dot.get_center() for dot in dots_triangle], 
            dots_triangle[0].get_center()
        ])
        triangle.set_color(GREY)

        n = 100
        dots = VGroup()
        paths = VGroup()
        for num in range(n):
            dot = Dot(radius = 0.03)
            dot.move_to(triangle.point_from_proportion(num / n))
            dot.save_state()
            dots.add(dot)
            dots.set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)
        for dot in dots:
            dot.move_to(triangle.get_center_of_mass())
            path = TracedPath(dot.get_center, dissipating_time=0.3, stroke_opacity=[0, 1])
            paths.add(path)

        self.add(paths)
        self.play(
            AnimationGroup(
                *[Restore(dot) for dot in dots], lag_ratio = 0.05
            ),
            run_time = 2
        )
        self.play(
            FadeOut(dots),
            Create(triangle), 
            *[GrowFromCenter(dot) for dot in dots_triangle]
        )

        self.triangle, self.dots_triangle = triangle, dots_triangle

    def label_triangle(self):

        dots_labels = VGroup(*[
            MathTex(tex).set_color(GREY).next_to(dot.get_center(), direction)
            for tex, dot, direction in zip(["A", "B", "C"], self.dots_triangle, [DL, DR, LEFT])
        ])

        side_labels = VGroup(*[
            Tex(tex) for tex in ["GK", "AK", "HY"]
        ])
        side_labels[0].next_to(midpoint(self.dots_triangle[1].get_center(), self.dots_triangle[2].get_center()), UR).set_color(vec_c_color)
        side_labels[1].next_to(midpoint(self.dots_triangle[2].get_center(), self.dots_triangle[0].get_center()), UL).set_color(GREY)
        side_labels[2].next_to(midpoint(self.dots_triangle[0].get_center(), self.dots_triangle[1].get_center()), DOWN).set_color(vec_b_color)

        arc_a = Arc(
            radius = 1, arc_center = self.dots_triangle[0].get_center(), color = GREEN,
            start_angle = 0, angle = Line(self.dots_triangle[0].get_center(), self.dots_triangle[-1].get_center()).get_angle()
        )
        tex_a = MathTex("\\alpha")\
            .next_to(self.dots_triangle[0], UR)\
            .shift(0.1*DOWN)\
            .set_color(GREEN)

        for mob in [*dots_labels, *side_labels, arc_a, tex_a]:
            mob.save_state()
            mob.set_color(BLACK)
            mob.move_to(self.triangle.get_center_of_mass())

        self.play(
            AnimationGroup(
                *[Restore(mob) for mob in [*dots_labels, *side_labels, tex_a, arc_a]], 
                lag_ratio = 0.1
            ), 
            run_time = 1.5
        )
        self.wait()

        eq = MathTex("\\sin", "(", "\\alpha", ")", "=", "{", "\\text{GK}", "\\over", "\\text{HY}", "}")\
            .scale(1.4)\
            .next_to(self.triangle, RIGHT, buff = 1)\
            .set_color_by_tex_to_color_map({"\\alpha": GREEN, "GK": vec_c_color, "\\text{HY}": vec_b_color})

        self.play(ShowIncreasingSubsets(eq), run_time = 1.5)
        self.wait(3)


        arc_b = Arc(
            radius = 1, arc_center = self.dots_triangle[1].get_center(), color = GREEN,
            start_angle = Line(self.dots_triangle[1].get_center(), self.dots_triangle[-1].get_center()).get_angle(), 
            angle = 90*DEGREES - Line(self.dots_triangle[0].get_center(), self.dots_triangle[-1].get_center()).get_angle()
        )
        tex_b = MathTex("\\beta")\
            .next_to(self.dots_triangle[1], np.array([-4,1,0]))\
            .shift(0.3*DOWN)\
            .set_color(GREEN)

        tex_sin_b = tex_b.copy().scale(1.4).move_to(eq[2])

        side_labels[0].generate_target()
        side_labels[0].target.move_to(side_labels[1])
        side_labels[1].generate_target()
        side_labels[1].target.move_to(side_labels[0])


        self.play(
            AnimationGroup(
                Transform(arc_a, arc_b),
                Transform(tex_a, tex_b),
                FadeOut(eq[2], shift = 0.5*UP),
                FadeIn(tex_sin_b, shift = 0.5*UP),
                CyclicReplace(side_labels[0], side_labels[1]),
                lag_ratio = 0.3
            ),
            run_time = 2
        )
        self.wait(3)


class Parallelogramm(MovingCameraScene, ProjectionScene): 
    def construct(self):
        self.plane_kwargs = {
            "axis_config": {"stroke_color": GREY}, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2, "stroke_opacity": 0.4}
        }
        self.plane = self.get_plane(**self.plane_kwargs)

        self.start_a_num = [3, 2, 0]
        self.start_b_num = [2,-1, 0]

        self.start_vecs = self.get_vecs_from_nums(self.start_a_num, self.start_b_num)
        self.start_para = self.get_parallelogramm_from_vecs(*self.start_vecs)

        self.setup_scene()
        self.geometric_sin_term()
        self.from_rect_to_parallelo()
        self.create_parallelo_from_vecs_copy()
        self.vary_vectors()


    def setup_scene(self):
        #                                  0          1           2          3          4        5       6          7            8        9          10         11         12         13       14     15      16       17
        sin_eq = self.sin_eq = MathTex("\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert", "=", "\\lvert", "\\vec{a}", "\\rvert", "\\cdot", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")")
        sin_eq.set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color, "\\varphi": GREEN})
        sin_eq.scale(1.4)
        sin_eq.move_to(np.array([-3.26364788, 3.22184406, 0]))

        bg_rect = BackgroundRectangle(sin_eq, buff = 0.1)
        self.add(bg_rect, sin_eq)
        self.wait(2)

        self.play(
            AnimationGroup(
                Create(self.plane, lag_ratio = 0.05),
                *[GrowArrow(vec) for vec in self.start_vecs],
                lag_ratio = 0.15
            ),
            run_time = 3
        )
        self.bring_to_front(bg_rect, sin_eq)
        self.wait()

    def geometric_sin_term(self):
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(height = config["frame_height"] * 0.6).move_to(2.7*RIGHT + 0.2*UP),
            run_time = 4
        )
        self.wait()

        pro_line = self.get_projection_line(self.start_a_num, self.start_b_num, color = vec_c_color)
        self.play(Create(pro_line), run_time = 2)
        self.wait(2)


        arc = self.arc = Arc(
            radius = 0.5, color = GREEN,
            start_angle = self.start_vecs[0].get_angle(), 
            angle = -angle_between_vectors(self.start_a_num, self.start_b_num)
        )
        tex_b = MathTex("\\vec{b}").set_color(vec_b_color).move_to(self.plane.c2p(0.5, -0.75))
        tex_gk = Tex("GK").set_color(pro_line.get_color()).move_to(self.plane.c2p(1.75, 0.2))

        #                      0      1        2       3    4    5        6            7        8           9          10      11
        sin_term1 = MathTex("\\sin", "(", "\\varphi", ")", "=", "{", "\\text{GK}", "\\over", "\\lvert", "\\vec{b}", "\\rvert", "}")\
            .move_to(self.plane.c2p(3,0.75), aligned_edge=LEFT)

        #                        0         1       2          3           4         5         6      7       8        9
        sin_term2 = MathTex("\\text{GK}", "=", "\\lvert", "\\vec{b}", "\\rvert", "\\cdot", "\\sin", "(", "\\varphi", ")")\
            .next_to(sin_term1, DOWN, buff = 0.5, aligned_edge=LEFT)

        for term in sin_term1, sin_term2:
            term.set_color_by_tex_to_color_map({"\\vec{b}": vec_b_color, "GK": vec_c_color, "\\varphi": GREEN})

        bg_rect = BackgroundRectangle(VGroup(sin_term1, sin_term2), buff = 0.1)

        self.play(
            Create(arc), 
            Write(tex_gk),
            Write(tex_b)
        )
        self.wait()

        self.play(Create(bg_rect))
        self.play(ShowIncreasingSubsets(sin_term1[:5]))
        self.wait()
        self.play(
            AnimationGroup(
                ApplyWave(pro_line,),
                ShowIncreasingSubsets(sin_term1[5:8]), 
                lag_ratio = 0.5
            ), 
            run_time = 2
        )
        self.wait()
        self.play(
            AnimationGroup(
                ApplyWave(self.start_vecs[1]),
                ShowIncreasingSubsets(sin_term1[8:]),
                lag_ratio = 0.5
            ), 
            run_time = 2
        )
        self.wait()

        self.play(TransformMatchingTex(sin_term1.copy(), sin_term2, lag_ratio = 0.33), run_time = 4)
        self.wait(3)


        sur_rect0 = self.sur_rect0 = SurroundingRectangle(self.sin_eq[10:], color = vec_c_color)
        sur_rect1 = SurroundingRectangle(sin_term2[2:], color = vec_c_color)

        self.add(sur_rect0)
        self.play(
            Restore(self.camera.frame, run_time = 4),
            Create(sur_rect1, run_time = 2)
        )
        self.wait()



        # FadeOut
        fadeout_group = VGroup(bg_rect, *sin_term1, *sin_term2, sur_rect1, tex_gk, tex_b)
        self.play(FadeOut(fadeout_group, lag_ratio = 0.1), run_time = 3)
        self.wait()


        self.pro_line = pro_line

    def from_rect_to_parallelo(self):
        pro_line = self.pro_line

        # Indicating factors in multiplication
        self.play(AnimationGroup(Wiggle(self.sin_eq[6:9]), ApplyWave(self.start_vecs[0]), lag_ratio = 0.3), run_time = 2)
        self.wait(0.5)
        self.play(AnimationGroup(Wiggle(self.sin_eq[10:]), ApplyWave(pro_line), lag_ratio = 0.3), run_time = 2)
        self.wait()

        # move pro_line to form rectangle
        dot_prod_value = np.dot(self.start_a_num, self.start_b_num)
        dot_prod_norm = dot_prod_value / np.linalg.norm(self.start_a_num)**2

        vect = pro_line.get_end() - self.origin
        self.play(pro_line.animate.shift(-vect), run_time = 2)
        self.wait()

        pro_line.rotate(180*DEGREES)
        rect = self.get_parallelogramm_from_vecs(self.start_vecs[0], pro_line)
        self.play(Create(rect), run_time = 3)
        self.bring_to_front(self.arc, self.start_vecs)

        # Text: Flächeninhalt des Rechtecks
        area_text1 = Tex("Flächeninhalt des \\\\", "Rechtecks")\
            .scale(1.35)\
            .add_background_rectangle(buff = 0.1)\
            .to_edge(LEFT, buff = 0.5)
        area_text1[-1].set_color(vec_c_color)

        para_text = Tex("Parallelogramms")\
            .scale(1.35)\
            .set_color(vec_c_color)\
            .move_to(area_text1[-1], aligned_edge=UP)

        sur_rect = SurroundingRectangle(para_text, color = area_text1[-1].get_color())

        arrow = DoubleArrow(
            start = self.sin_eq[1:4].get_bottom(), 
            end = area_text1.get_top(), 
            color = GREY, buff = 0.2
        )
        self.play(
            AnimationGroup(
                GrowArrow(arrow, run_time = 2),
                FadeIn(area_text1[0]),
                Write(area_text1[1:], run_time = 1.5),
                lag_ratio = 0.25
            ),
        )
        self.wait()

        # Triangle shift
        triangle = VMobject()
        triangle.set_points_as_corners([self.origin, pro_line.get_end(), self.start_vecs[1].get_end(), self.origin])
        triangle.set_fill(color = PINK, opacity = 0.25)
        triangle.set_stroke(color = PINK, width = 2)

        self.play(Create(triangle), run_time = 3)
        self.wait()

        self.play(triangle.animate.shift(self.start_a_num), run_time = 4)
        self.wait()
        self.play(
            ReplacementTransform(rect, self.start_para, run_time = 3),
            Transform(area_text1[-1], para_text, run_time = 1),
            FadeOut(triangle, run_time = 3)
        )
        self.bring_to_front(self.start_vecs)

        # Text Parallelogramm
        self.play(ReplacementTransform(self.start_para.copy(), sur_rect), run_time = 1)
        self.bring_to_front(self.start_vecs)
        self.play(
            Uncreate(sur_rect),
            FadeOut(VGroup(self.sur_rect0, pro_line, self.arc), lag_ratio = 0.25),
            run_time = 2
        )
        self.wait(3)

    def create_parallelo_from_vecs_copy(self):
        a_copy, b_copy = self.start_vecs[0].copy(), self.start_vecs[1].copy()
        self.play(a_copy.animate.shift(self.start_b_num), run_time = 2)
        self.play(b_copy.animate.shift(self.start_a_num), run_time = 2)
        self.wait()

        self.bring_to_front(self.start_vecs, a_copy, b_copy)
        self.play(*[FadeOut(vec) for vec in [a_copy, b_copy]])
        self.wait()

    def vary_vectors(self):
        vec_a_nums = [[2, 3,0], [-4, 1,0], [5,-3,0], self.start_a_num]
        vec_b_nums = [[1,-2,0], [-3,-3,0], [1, 2,0], self.start_b_num]

        for a_num, b_num in zip(vec_a_nums, vec_b_nums):
            vecs = self.get_vecs_from_nums(a_num, b_num)
            para = self.get_parallelogramm_from_vecs(*vecs)
            self.play(
                Transform(self.start_vecs, vecs), 
                Transform(self.start_para, para), 
                run_time = 3
            )
            self.wait()
        self.wait(3)


class NormalVektorWithParallelo(NormalVektorFromRotation):
    def construct(self):
        self.rot_time = 8
        self.start_angle = PI/6
        self.angle = ValueTracker(self.start_angle)

        self.vec_a_num = [1,0,0]
        self.vec_b_num = [np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -1.25
        axis_max = self.axis_max = 1.25
        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)

        self.setup_scene(animate = True)
        self.add_updaters()
        self.draw_parallelo()
        self.rotate_step_by_step()
        self.rotate_vec_b()


    def draw_parallelo(self):
        para = self.get_parallelogramm_from_vecs(self.vec_a, self.vec_b)
        self.play(Create(para), run_time = 4)
        self.bring_to_front(self.vec_a, self.vec_b, self.vec_n)
        self.wait()

        para.add_updater(lambda p: p.become(
            self.get_parallelogramm_from_vecs(self.vec_a, self.vec_b)
        ))




        n = lambda angle: np.linalg.norm(np.cross([1,0,0], [np.cos(angle.get_value()), np.sin(angle.get_value()), 0]))
        cross_val = ValueTracker(n(self.angle))
        cross_dec = DecimalNumber(cross_val.get_value(), include_sign = True, edge_to_fix=LEFT)\
            .scale(1.5)\
            .set_color(vec_c_color)\
            .to_edge(UP)\
            .shift(5*RIGHT + 1.5*DOWN)

        self.add_fixed_in_frame_mobjects(cross_dec)

        text = Tex("Länge des \\\\", "Normalenvektors")
        area = Tex("Flächeninhalt \\\\", "Parallelogramm")
        for mob, direc, buff in zip([text, area], [UP, DOWN], [1, 0.75]):
            mob[0].set_color(LIGHT_GREY)
            mob[1].set_color(BLUE_B)
            self.add_fixed_in_frame_mobjects(mob)
            mob.next_to(cross_dec, direc, buff = buff, aligned_edge = UP)

        self.play(
            AnimationGroup(
                Write(text), Write(cross_dec), Write(area), lag_ratio = 1
            ), 
            run_time = 3
        )
        self.wait()
        self.wait()


        cross_dec.add_updater(lambda dec: self.add_fixed_in_frame_mobjects(dec.set_value(n(self.angle))))
        self.cross_dec = cross_dec

    def rotate_step_by_step(self):
        arc_kwargs = {"radius": 1, "arc_center": self.origin, "color": GREEN}
        arc = Arc(start_angle = self.vec_a.get_angle(), angle = self.vec_b.get_angle() - self.vec_a.get_angle(), **arc_kwargs)

        self.play(Create(arc), run_time = 2)

        arc.add_updater(lambda arc: arc.become(
            Arc(
                start_angle = self.vec_a.get_angle(), 
                angle = self.angle_between_vectors_bigger_than_pi(self.vec_a, self.vec_b), 
                **arc_kwargs
            )
        ))

        angle_increments = [60, 90, 90, 90, 30]
        run_times = [increment/360 * 40 for increment in angle_increments]
        print(run_times)
        for increment, run_time in zip(angle_increments, run_times):
            self.play(
                self.angle.animate(rate_func = smooth).increment_value(increment*DEGREES), run_time = run_time
            )
            self.wait()
        self.wait()

    def rotate_vec_b(self):
        for x in range(3):
            self.play(self.angle.animate(rate_func = linear).set_value(2*PI + self.start_angle), run_time = self.rot_time)
            self.angle.set_value(self.start_angle)
        self.wait(3)


    # functions
    def get_parallelogramm_from_vecs(self, vec_a, vec_b, fill_opacity = 0.25):
        parallelo = VMobject()\
            .set_points_as_corners([
                vec_a.get_start(), 
                vec_a.get_end(), 
                vec_a.get_end() + self.axes.c2p(np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0), # vec_b.get_end() 
                self.axes.c2p(np.cos(self.angle.get_value()), np.sin(self.angle.get_value()), 0), 
                vec_b.get_start()
            ])\
            .set_fill(color = vec_c_color, opacity = fill_opacity)\
            .set_stroke(color = BLUE, width = 2)

        return parallelo


class CharacteristicPropoerties(ProjectionScene):
    def construct(self):
        self.plane_kwargs = {
            "axis_config": {"stroke_color": GREY}, 
            "background_line_style": {"stroke_color": BLUE_E, "stroke_width": 2, "stroke_opacity": 0.4}
        }
        self.plane = self.get_plane(**self.plane_kwargs)

        self.start_a_num = [1, 1, 0]
        self.start_b_num = [2,-1, 0]

        self.start_vecs = self.get_vecs_from_nums(self.start_a_num, self.start_b_num)
        self.start_para = self.get_parallelogramm_from_vecs(*self.start_vecs)

        self.setup_scene()
        self.multiples_of_b()
        self.multiples_of_a()


    def setup_scene(self):
        self.vec_a, self.vec_b = self.start_vecs[0], self.start_vecs[1]

        brace_a = BraceBetweenPoints(self.vec_a.get_end(), self.vec_a.get_start(), color = GREY)
        brace_b = BraceBetweenPoints(self.vec_b.get_start(), self.vec_b.get_end(), color = GREY)

        brace_a_tex = brace_a.get_tex("\\vec{a}").set_color(vec_a_color).add_background_rectangle()
        brace_b_tex = brace_b.get_tex("\\vec{b}").set_color(vec_b_color).add_background_rectangle()

        for element in brace_a, brace_b, brace_a_tex, brace_b_tex:
            element.save_state()

        self.play(
            AnimationGroup(
                Create(self.plane),
                *[GrowArrow(arrow) for arrow in self.start_vecs],
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.play(
            AnimationGroup(
                *[Create(brace) for brace in [brace_a, brace_b]],
                *[FadeIn(tex) for tex in [brace_a_tex, brace_b_tex]],
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()

        cross_value = np.abs(np.cross(self.start_a_num, self.start_b_num)[-1])
        #                         0          1           2           3          4       5         6
        self.cross1 = MathTex("\\lvert", "\\vec{a}", "\\times", "\\vec{b}", "\\rvert", "=", str(cross_value))\
            .scale(1.4)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color})\
            .next_to(5.25*LEFT + 3*UP, RIGHT, buff = 0)
        self.cross1[-1].set_color(vec_c_color)

        bg_rect = BackgroundRectangle(self.cross1, buff = 0.2)

        self.play(FadeIn(bg_rect), Write(self.cross1[:-1]))
        self.wait()

        self.play(Create(self.start_para), run_time = 3)
        self.bring_to_front(*self.start_vecs)
        self.wait()
        self.play(TransformFromCopy(self.start_para, self.cross1[-1].copy()), run_time = 2)
        self.add(self.cross1[-1])
        #self.play(Write(self.cross1[-1]))
        self.wait(3)

        self.brace_b, self.brace_b_tex = brace_b, brace_b_tex
        self.brace_a, self.brace_a_tex = brace_a, brace_a_tex

    def multiples_of_b(self):
        vec_b1 = self.start_vecs[1].copy()
        vec_b1.put_start_and_end_on(start = self.start_vecs[1].get_end(), end = self.start_vecs[1].get_end() + self.start_b_num)

        vec_b2 = self.start_vecs[1].copy()
        vec_b2.put_start_and_end_on(start = vec_b1.get_end(), end = vec_b1.get_end() + self.start_b_num)

        self.vec_b1, self.vec_b2 = vec_b1, vec_b2

        self.play(
            AnimationGroup(
                TransformFromCopy(self.start_vecs[1], vec_b1, path_arc = -45*DEGREES),
                TransformFromCopy(self.start_vecs[1], vec_b2, path_arc = -90*DEGREES),
                lag_ratio = 0.7
            ), 
            run_time = 5
        )
        self.wait()


        brace_b3 = BraceBetweenPoints(self.vec_b.get_start(), vec_b2.get_end(), color = GREY)
        brace_b3_tex = brace_b3.get_tex("3", "\\cdot", "\\vec{b}").add_background_rectangle()
        brace_b3_tex[3].set_color(vec_b_color)

        self.play(
            Transform(self.brace_b, brace_b3), 
            Transform(self.brace_b_tex, brace_b3_tex), 
        )
        self.wait(2)

        # neues Kreuzprodukt mit 3*b notieren
        #                         0          1           2       3    4       5         6       7        8       9    10
        self.cross2 = MathTex("\\lvert", "\\vec{a}", "\\times", "(", "3", "\\cdot", "\\vec{b}", ")", "\\rvert", "=", "3", "\\cdot", "3")\
            .scale(1.4)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color})\
            .next_to(6.5*LEFT + 1.5*UP, RIGHT, buff = 0)
        self.cross2[-1].set_color(vec_c_color)

        bg_rect = BackgroundRectangle(self.cross2, buff = 0.2)


        self.play(FadeIn(bg_rect), Write(self.cross2[:-3]))
        self.wait()


        # Parallelogramme verschieben
        para1, para2 = self.start_para.copy(), self.start_para.copy()
        for para in para1, para2:
            para.save_state()

        para1.shift(self.start_b_num)
        para2.shift([2*comp for comp in self.start_b_num])

        self.play(
            AnimationGroup(
                TransformFromCopy(self.start_para, para1),
                TransformFromCopy(self.start_para, para2),
                lag_ratio = 0.7
            ), 
            run_time = 5
        )
        self.wait()

        # Ergebnis schreiben
        self.play(
            TransformFromCopy(self.cross2[4], self.cross2[-3], path_arc = -PI/3),
            Write(self.cross2[-2]),
            TransformFromCopy(self.cross1[-1], self.cross2[-1]),
            run_time = 3
        )
        self.wait()

        self.para1, self.para2 = para1, para2

    def multiples_of_a(self):
        self.play(
            *[GrowFromPoint(vec, self.origin, rate_func = lambda t: smooth(1-t)) for vec in [self.vec_b1, self.vec_b2]],
            *[Restore(mob) for mob in [self.brace_b, self.brace_b_tex]], 
            *[Restore(para) for para in [self.para1, self.para2]],
            run_time = 2
        )

        vec_a1, vec_a2 = self.start_vecs[0].copy(), self.start_vecs[0].copy()
        brace_a3 = BraceBetweenPoints([3*x for x in self.start_a_num], vec_a2.get_start(), color = GREY)
        brace_a3_tex = brace_a3.get_tex("3", "\\cdot", "\\vec{a}").add_background_rectangle()
        brace_a3_tex[3].set_color(vec_a_color)

        self.play(
            self.para1.animate.shift(self.start_a_num),
            self.para2.animate.shift([2*x for x in self.start_a_num]),
            vec_a1.animate.put_start_and_end_on(start = self.start_vecs[0].get_end(), end = self.start_vecs[0].get_end() + self.start_a_num),
            vec_a2.animate.put_start_and_end_on(start = self.start_vecs[0].get_end(), end = vec_a1.get_end() + [2*x for x in self.start_a_num]),
            Transform(self.brace_a, brace_a3),
            Transform(self.brace_a_tex, brace_a3_tex),
            run_time = 2
        )
        self.wait(2)


        # neues Kreuzprodukt mit 3*a notieren
        #                         0       1    2       3         4        5        6         7            8      9    10
        self.cross3 = MathTex("\\lvert", "(", "3", "\\cdot", "\\vec{a}", ")", "\\times", "\\vec{b}", "\\rvert", "=", "3", "\\cdot", "3")\
            .scale(1.4)\
            .set_color_by_tex_to_color_map({"\\vec{a}": vec_a_color, "\\vec{b}": vec_b_color, "\\times": vec_c_color})\
            .next_to(6.5*LEFT + 1.5*UP, RIGHT, buff = 0)
        self.cross3[-1].set_color(vec_c_color)


        self.play(
            Transform(self.cross2[:8], self.cross3[:10]), 
            run_time = 1
        )
        self.wait(3)


        self.play(
            *[GrowFromPoint(vec, self.origin, rate_func = lambda t: smooth(1-t)) for vec in [vec_a1, vec_a2]],
            *[Restore(mob) for mob in [self.brace_a, self.brace_a_tex]], 
            *[FadeOut(para, target_position = self.start_para.get_center()) for para in [self.para1, self.para2]],
            run_time = 2
        )
        self.wait(3)


class ThumbnailGeo(Scene):
    def construct(self):
        title2 = Tex("Kreuzprodukt")\
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

        self.add(title1, title2, title0)


# QUICK RELEASE: Vektorprodukt in 2 Dimensionen

class DefIn3Dimensions1(Calculations):
    def construct(self):

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        title = Tex("Kreuzprodukt")\
            .scale(3)\
            .shift(2*UP)\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.25)\
            .set_stroke(width = 3)

        # eq = MathTex("\\text{Vektor}_1 ", "\\times", "\\text{ Vektor}_2", "=", "\\text{Vektor}_3")\
        #     .scale(1.5)\
        #     .next_to(title, DOWN, buff = 1)
        # for part, color in zip([eq[0], eq[2], eq[-1]], [RED_A, YELLOW_A, BLUE_A]):
        #     part.set_color(color)

        ax, bx, nx = MathTex("a_1"), MathTex("b_1"), MathTex("n_1")
        ay, by, ny = MathTex("a_2"), MathTex("b_2"), MathTex("n_2")
        az, bz, nz = MathTex("a_3"), MathTex("b_3"), MathTex("n_3")

        mat_a = MobjectMatrix([[ax], [ay], [az]], **self.mat_kwargs)
        mat_b = MobjectMatrix([[bx], [by], [bz]], **self.mat_kwargs)
        mat_n = MobjectMatrix([[nx], [ny], [nz]], **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type = "times", color = WHITE)
        vec_group[0][0].set_color(vec_a_color)
        vec_group[2][0].set_color(vec_b_color)
        equals = MathTex("=").next_to(vec_group, RIGHT)
        mat_n.next_to(equals, RIGHT)
        mat_n[0].set_color(vec_c_color)

        equation = VGroup(vec_group, equals, mat_n)\
            .scale(1.5)\
            .next_to(title, DOWN, buff = 1)

        self.play(Write(title))
        self.wait()

        self.play(FadeIn(*equation, lag_ratio = 0.25), run_time = 3)
        self.wait(3)

        mobs = Group(*self.mobjects)
        self.play(
            GrowFromPoint(mobs, point = 7*RIGHT + 4*DOWN, rate_func = lambda t: smooth(1-t), run_time = 1)
        )


class DefIn3Dimensions2(Scene):
    def construct(self):
        rect = RoundedRectangle(corner_radius = 0.25, height = 1, width = config["frame_width"] - 2)\
            .set_color(RED_E)\
            .to_edge(UP)

        link = Tex("https://de.","wikipedia",".org/wiki/","Kreuzprodukt")\
            .set(width = rect.width - 1)\
            .move_to(rect)

        link[1].set_color(vec_b_color)
        link[-1].set_color(vec_c_color)


        wiki_text = Text(
            "Das Kreuzprodukt, auch Vektorprodukt, \nist eine Verknüpfung im dreidimensionalen \neuklidischen Vektorraum, die zwei Vektoren \nwieder einen Vektor zuordnet.", 
            line_spacing = 2
        )
        wiki_text.next_to(rect, DOWN, buff = 1)

        self.play(Create(rect), run_time = 2)
        self.play(Write(link), run_time = 2)
        self.wait()

        self.play(
            AddTextLetterByLetter(wiki_text), run_time = 3
        )
        self.wait()

        sur_rect = SurroundingRectangle(wiki_text[54:71], color = YELLOW)
        self.play(Create(sur_rect))
        self.wait(3)

        mobs = Group(*self.mobjects)
        self.play(
            GrowFromPoint(mobs, point = 7*LEFT + 4*DOWN, rate_func = lambda t: smooth(1-t), run_time = 1)
        )


class DefIn3Dimensions3(Definition):
    def construct(self):
        self.mat_kwargs = {
            "v_buff": 0.6,
            "left_bracket": "(",
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.cut_color = MAROON
        self.com_color = ORANGE
        self.path_color = LIGHT_BROWN

        self.vec_a_num = [1, 2, -1]
        self.vec_b_num = [3, 0,  2]


        self.setup_scene()
        self.crosspath_animation()
        self.cross_vector_calculations()
        self.cut_lines_for_calculations()
        # self.prepare_for_next_scene()


        mobs = Group(*self.mobjects)
        self.play(
            GrowFromPoint(mobs, point = 7*RIGHT + 4*UP, rate_func = lambda t: smooth(1-t), run_time = 1)
        )


class DefIn3Dimensions4(Scene):
    def construct(self):
        pass


class AskFor2DEquivalent(Calculations):
    def construct(self):
        dim = Tex("2","D").scale(3)
        dim[0].set_color(RED)
        dim[1].set_color(BLUE)

        vec_a_num = [2,-1,0]
        vec_b_num = [0, 2,0]

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }


        mat_a = self.get_vector_matrix_from_num_vec(vec_a_num, dimension = 2, **self.mat_kwargs)
        mat_b = self.get_vector_matrix_from_num_vec(vec_b_num, dimension = 2, **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type="times", color = vec_c_color)
        equals = MathTex("=")
        qmark = Tex("?").scale(1.5).set_color(RED)

        eq = VGroup(vec_group, equals, qmark)\
            .scale(1.5)\
            .arrange_submobjects(RIGHT)\
            .to_edge(UP)

        self.play(GrowFromCenter(dim))
        self.play(Circumscribe(dim, color = YELLOW, time_width = 0.75, run_time = 1))
        self.wait(0.5)

        self.play(
            dim.animate(run_time = 1).shift(3*DOWN), 
            FadeIn(eq, lag_ratio = 0.25, run_time = 2)
        )
        self.wait(3)

        vec_group.generate_target()
        vec_group.target.scale(2/3).move_to(4*LEFT + 2*UP)

        shrink_group = VGroup(equals, qmark, dim)
        self.play(
            MoveToTarget(vec_group, run_time = 2),
            GrowFromPoint(shrink_group, point = ORIGIN, rate_func = lambda t: smooth(1-t))
        )
        self.wait()


class CalcIn2D(Calculations):
    def construct(self):
        self.vec_a_num = [2,-1,0]
        self.vec_b_num = [0, 2,0]
        self.result_num = int(np.linalg.norm(np.cross(self.vec_a_num, self.vec_b_num)))

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        self.setup_from_old_scene()
        self.path_animation()
        self.transform_calc_to_3d()


    def setup_from_old_scene(self):
        mat_a = self.get_vector_matrix_from_num_vec(self.vec_a_num, dimension = 2, **self.mat_kwargs)
        mat_b = self.get_vector_matrix_from_num_vec(self.vec_b_num, dimension = 2, **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type="times", color = vec_c_color)
        vec_group.move_to(4*LEFT + 2*UP)

        label_a = MathTex("\\vec{a}", color = vec_a_color)
        label_b = MathTex("\\vec{b}", color = vec_b_color)

        for label, mat in zip([label_a, label_b], [mat_a, mat_b]):
            label.next_to(mat, UP)

        self.add(vec_group)
        self.wait()
        self.play(
            FadeIn(label_a, shift = 3*RIGHT), 
            FadeIn(label_b, shift = 3*LEFT)
        )

        self.vec_group = vec_group

    def path_animation(self):
        vec_group = self.vec_group

        equals = MathTex("=").next_to(self.vec_group, RIGHT)
        final_result = MathTex(str(self.result_num)).next_to(equals, RIGHT)

        self.play(Write(equals))

        rect = ScreenRectangle(height = 4.75, color = GREY, stroke_width = 3).to_corner(DR)
        self.play(Create(rect), run_time = 3)
        self.wait(3)

        self.play(ShrinkToCenter(rect), rate_func = running_start)
        self.wait(0.5)


        path = VMobject()
        path.set_points_smoothly([
            vec_group[0][0][0].get_center(),     # x Komponente vec1
            vec_group[2][0][1].get_center(),     # y Komponente vec2
            vec_group[0][0][1].get_center(),     # y Komponente vec1
            vec_group[2][0][0].get_center(),     # x Komponente vec2
        ])
        path.set_color(ORANGE).set_stroke(width = 7)

        result1 = MathTex(
            str(self.vec_a_num[0]), "\\cdot", str(self.vec_b_num[1]), "-",
            "(", str(self.vec_a_num[1]), ")", "\\cdot", str(self.vec_b_num[0])
        )
        result2 = MathTex("4", "-", "0")
        for result in result1, result2:
            result.next_to(equals, RIGHT)

        self.play(ShowPassingFlash(path), run_time = 4)

        self.play(Write(result1[:3]))
        self.wait(0.5)
        self.play(Write(result1[3]))
        self.wait(0.5)
        self.play(Write(result1[4:]))
        self.wait()

        self.play(Transform(result1, result2))
        self.wait()

        self.play(Transform(result1, final_result))
        self.wait()


        vector = Tex("Vektor").next_to(final_result, RIGHT, buff = 2)
        scalar = Tex("Zahl").move_to(vector)
        for mob in vector, scalar:
            mob.scale(1.5)
            mob.set_color(TEAL)

        cross = Cross(vector)
        self.play(Write(vector))
        self.play(Create(cross))
        self.wait()

        self.play(
            ReplacementTransform(vector, scalar), 
            ShrinkToCenter(cross)
        )
        self.wait(3)


        self.remove(scalar)
        self.wait()

        self.final_result, self.path = final_result, path


        # Das Ergebnis ist 4. Beim Kreuzprodukt im zweidimensionalen kommt also eine Zahl und kein Vektor heraus. 

    def transform_calc_to_3d(self):
        mat_a2 = self.get_vector_matrix_from_num_vec(self.vec_a_num, dimension = 3, **self.mat_kwargs)
        mat_b2 = self.get_vector_matrix_from_num_vec(self.vec_b_num, dimension = 3, **self.mat_kwargs)

        vec_group2 = self.group_vecs_with_symbol(mat_a2, mat_b2, type="times", color = vec_c_color)
        vec_group2.move_to(4*LEFT + 2*DOWN)

        self.play(
            AnimationGroup(
                ReplacementTransform(self.vec_group[0][0][1].copy(), vec_group2[0][0][1]),
                ReplacementTransform(self.vec_group[0][0][0].copy(), vec_group2[0][0][0]),
                ReplacementTransform(self.vec_group[1].copy(), vec_group2[1]),
                ReplacementTransform(self.vec_group[2][0][1].copy(), vec_group2[2][0][1]),
                ReplacementTransform(self.vec_group[2][0][0].copy(), vec_group2[2][0][0]),
                lag_ratio = 0.3
            ),
            run_time = 3
        )
        self.wait()

        self.play(
            FadeIn(VGroup(vec_group2[0][0][2], vec_group2[2][0][2]), shift = UP, lag_ratio = 0.25), 
            FadeIn(VGroup(*vec_group2[0][1:], vec_group2[2][1:]), lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait()

        equals = MathTex("=").next_to(vec_group2, RIGHT)
        mat_n = self.get_vector_matrix_from_num_vec(np.cross(self.vec_a_num, self.vec_b_num), **self.mat_kwargs)
        mat_n.next_to(equals, RIGHT)
        self.play(
            Write(equals), 
            Create(VGroup(*mat_n[1:]), lag_ratio = 0.25)
        )
        self.wait(0.5)


        path_x, path_y, path_z = self.get_crossproduct_path_xyz(vec_group2, stroke_width=7)
        paths = VGroup(path_x, path_y, path_z)
        cut_lines = self.get_crossproduct_cut_lines(vec_group2, color = MAROON)


        for index in range(len(paths) - 1):
            self.play(
                Create(cut_lines[index]), 
                FadeToColor(vec_group2[0][0][index], color = DARK_GREY),
                FadeToColor(vec_group2[2][0][index], color = DARK_GREY),
                run_time = 1.5
            )
            self.play(ShowPassingFlash(paths[index]), run_time = 2.5)
            self.play(Write(mat_n[0][index]))
            self.wait(0.5)
            self.play(
                Uncreate(cut_lines[index]),
                FadeToColor(vec_group2[0][0][index], color = WHITE),
                FadeToColor(vec_group2[2][0][index], color = WHITE),
            )
            self.wait(0.5)
        self.wait()

        self.play(
            Create(cut_lines[-1]), 
            FadeToColor(vec_group2[0][0][2], color = DARK_GREY),
            FadeToColor(vec_group2[2][0][2], color = DARK_GREY),
            run_time = 2
        )
        self.play(
            ShowPassingFlash(self.path),
            ShowPassingFlash(path_z), run_time = 6
        )
        self.wait()

        self.play(
            TransformFromCopy(self.final_result.copy(), mat_n[0][2], path_arc = PI),
            run_time = 5
        )
        self.wait(3)


class From2DTo3D(ThreeDScene, Calculations, ProjectionScene):
    def construct(self):

        self.unit_a = [1,0,0]
        self.unit_b = [0,1,0]

        self.vec_a_num = [2,-1,0]
        self.vec_b_num = [0, 2,0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)
        self.result_num = int(np.linalg.norm(np.cross(self.vec_a_num, self.vec_b_num)))

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -4
        axis_max = self.axis_max = 4

        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 0*DEGREES, theta = -90*DEGREES)
        # self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)

        self.xlabel = MathTex("x").next_to(self.axes.x_axis, RIGHT)
        self.ylabel = MathTex("y").next_to(self.axes.y_axis.get_top(), RIGHT)


        self.setup_scene()
        self.area_of_parallelogramm()
        self.move_camera_to_see_3d()
        self.camera_rotation()

    def setup_scene(self):
        axes, origin = self.axes, self.origin

        lines_kwags = {"stroke_width": 2, "color": GREY, "stroke_opacity": 0.25}
        lines_a = VGroup(*[
            Line(
                start = self.axes.c2p(*[-10*comp_a + s*comp_b for comp_a, comp_b in zip(self.unit_a, self.unit_b)]), 
                end  =  self.axes.c2p(*[+10*comp_a + s*comp_b for comp_a, comp_b in zip(self.unit_a, self.unit_b)]), 
                **lines_kwags
            )
            for s in np.linspace(-10,10,21)
        ])

        lines_b = VGroup(*[
            Line(
                start = self.axes.c2p(*[r*comp_a - 10*comp_b for comp_a, comp_b in zip(self.unit_a, self.unit_b)]), 
                end  =  self.axes.c2p(*[r*comp_a + 10*comp_b for comp_a, comp_b in zip(self.unit_a, self.unit_b)]), 
                **lines_kwags
            )
            for r in np.linspace(-10,10,21)
        ])

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


        vec_a = Arrow(origin, axes.c2p(*self.vec_a_num), color = vec_a_color, buff = 0)
        vec_b = Arrow(origin, axes.c2p(*self.vec_b_num), color = vec_b_color, buff = 0)
        vec_n = Arrow(origin, axes.c2p(*self.vec_n_num), color = vec_c_color, buff = 0)

        mat_a = self.get_vector_matrix_from_num_vec(self.vec_a_num, dimension = 2, **self.mat_kwargs)
        mat_b = self.get_vector_matrix_from_num_vec(self.vec_b_num, dimension = 2, **self.mat_kwargs)
        mat_n = self.get_vector_matrix_from_num_vec(self.vec_n_num, dimension = 2, **self.mat_kwargs)

        vec_group = self.group_vecs_with_symbol(mat_a, mat_b, type="times", color = vec_c_color)
        vec_group.move_to(4*LEFT + 2*UP)

        label_a = MathTex("\\vec{a}", color = vec_a_color)
        label_b = MathTex("\\vec{b}", color = vec_b_color)
        label_n = MathTex("\\vec{n}", color = vec_c_color)

        for label, mat in zip([label_a, label_b, label_n], [mat_a, mat_b, mat_n]):
            label.next_to(mat, UP)

        equals = MathTex("=").next_to(vec_group, RIGHT)
        final_result = MathTex(str(self.result_num)).next_to(equals, RIGHT)

        self.add(label_a, label_b, vec_group, equals, final_result)
        self.wait()

        self.play(
            Create(VGroup(lines_a, lines_b, big_rect, self.axes.x_axis, self.axes.y_axis, self.xlabel, self.ylabel), lag_ratio = 0.25),
            LaggedStartMap(GrowArrow, VGroup(vec_a, vec_b), lag_ratio = 0.25),
            run_time = 3
        )
        self.bring_to_front(label_a, label_b, vec_group, equals, final_result)
        self.wait()


        self.vec_a, self.vec_b, self.vec_n = vec_a, vec_b, vec_n
        self.vec_group = vec_group
        self.equals, self.final_result = equals, final_result
        self.label_a, self.label_b, self.label_n = label_a, label_b, label_n

    def area_of_parallelogramm(self):
        para = self.get_parallelogramm_from_vecs(self.vec_a, self.vec_b)

        self.play(DrawBorderThenFill(para), run_time = 3)
        self.bring_to_front(self.vec_a, self.vec_b)
        self.wait()


        vec_a2 = Arrow(self.origin, self.axes.c2p(*[2,0,0]), color = vec_a_color, buff = 0)
        square = self.get_parallelogramm_from_vecs(vec_a2, self.vec_b)

        self.play(Transform(para, square), rate_func = there_and_back_with_pause, run_time = 7)
        self.wait(3)

        self.para = para

    def move_camera_to_see_3d(self):
        plane_tex = Tex("$xy-$", "Ebene")\
            .shift(10*LEFT)\
            .rotate_in_place(angle = 90*DEGREES, axis = OUT)\
            .rotate_in_place(angle = -90*DEGREES, axis = DOWN)
        self.add(plane_tex)

        self.move_camera(phi = 70*DEGREES, theta = 45*DEGREES, run_time = 7)
        self.wait()

        self.play(GrowArrow(self.vec_n), run_time = 3)
        self.wait()

    def camera_rotation(self):
        self.begin_ambient_camera_rotation(rate = -0.08)
        self.wait(20)


class From2DTo3DNegative(From2DTo3D):
    def construct(self):

        self.unit_a = [1,0,0]
        self.unit_b = [0,1,0]

        self.vec_a_num = [2,-1,0]
        self.vec_b_num = [0, 2,0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)
        self.result_num = int(np.linalg.norm(np.cross(self.vec_a_num, self.vec_b_num)))

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -4
        axis_max = self.axis_max = 4

        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 0*DEGREES, theta = -90*DEGREES)
        # self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)

        self.xlabel = MathTex("x").next_to(self.axes.x_axis, RIGHT)
        self.ylabel = MathTex("y").next_to(self.axes.y_axis.get_top(), RIGHT)


        self.setup_scene()
        self.area_of_parallelogramm()
        self.new_vectors_new_parallelogram()
        self.move_camera_once_again()

    def new_vectors_new_parallelogram(self):

        new_vec_b = Arrow(self.origin, self.axes.c2p(*[0,-2,0]), color = vec_b_color, buff = 0)
        new_mat_b = self.get_vector_matrix_from_num_vec([0,-2,0], dimension = 2, **self.mat_kwargs)\
            .move_to(self.vec_group[2], aligned_edge = LEFT)

        new_para = self.get_parallelogramm_from_vecs(self.vec_a, new_vec_b)

        self.play(
            VGroup(self.equals, self.final_result).animate.next_to(new_mat_b, RIGHT),
            Transform(self.vec_group[2], new_mat_b), 
            Transform(self.vec_b, new_vec_b), 
            Transform(self.para, new_para), 
            run_time = 5
        )
        self.bring_to_front(self.vec_a, new_vec_b)
        self.wait()


        path_z = VMobject()
        path_z.set_points_smoothly([
            self.vec_group[0][0][0].get_center(),     # x Komponente vec1
            self.vec_group[2][0][1].get_center(),     # y Komponente vec2
            self.vec_group[0][0][1].get_center(),     # y Komponente vec1
            self.vec_group[2][0][0].get_center(),     # x Komponente vec2
        ])
        path_z.set_color(ORANGE).set_stroke(width = 7)
        new_final_result = MathTex("-4").move_to(self.final_result, aligned_edge=LEFT)


        self.play(ShowPassingFlash(path_z), run_time = 7)
        self.wait(0.5)
        self.play(Transform(self.final_result, new_final_result))
        self.wait()

    def move_camera_once_again(self):
        plane_tex = Tex("$xy-$", "Ebene")\
            .shift(10*LEFT)\
            .rotate_in_place(angle = 90*DEGREES, axis = OUT)\
            .rotate_in_place(angle = -90*DEGREES, axis = DOWN)
        self.add(plane_tex)

        self.move_camera(phi = 87*DEGREES, theta = 45*DEGREES, run_time = 7)


        new_vec_n = Arrow(self.origin, self.axes.c2p(*[0,0,-4]), color = vec_c_color, buff = 0)
        self.play(GrowArrow(new_vec_n), run_time = 3)
        self.wait()

        self.move_camera(phi = 70*DEGREES, theta = 45*DEGREES, run_time = 3)
        self.wait()


class ThumbnailTwoDimensions(From2DTo3D):
    def construct(self):

        self.unit_a = [1,0,0]
        self.unit_b = [0,1,0]

        self.vec_a_num = [2,-1,0]
        self.vec_b_num = [0, 2,0]
        self.vec_n_num = np.cross(self.vec_a_num, self.vec_b_num)
        self.result_num = int(np.linalg.norm(np.cross(self.vec_a_num, self.vec_b_num)))

        self.mat_kwargs = {
            "v_buff": 0.6, 
            "left_bracket": "(", 
            "right_bracket": ")",
            "bracket_v_buff": 0.1
        }

        axis_length = self.axis_length = 7.5
        axis_min = self.axis_min = -4
        axis_max = self.axis_max = 4

        axes = self.axes = ThreeDAxes(
            x_range = [axis_min, axis_max, 1], y_range = [axis_min, axis_max, 1], z_range = [axis_min, axis_max, 1], 
            x_length = axis_length, y_length = axis_length, z_length = axis_length
        )
        self.origin = axes.c2p(0,0,0)
        self.set_camera_orientation(phi = 0*DEGREES, theta = -90*DEGREES)
        # self.set_camera_orientation(phi = 70*DEGREES, theta = 45*DEGREES)

        self.xlabel = MathTex("x").next_to(self.axes.x_axis, RIGHT)
        self.ylabel = MathTex("y").next_to(self.axes.y_axis.get_top(), RIGHT)


        self.setup_scene()
        self.area_of_parallelogramm()
        self.move_camera_to_see_3d()


        tex_group = VGroup(self.vec_group, self.equals, self.final_result, self.label_a, self.label_b)
        # tex_group.add_background_rectangle(opacity = 0.4)
        self.add_fixed_in_frame_mobjects(tex_group)
        tex_group.to_edge(RIGHT).shift(2*DOWN + 10*RIGHT)

        fs = 90
        t4 = Tex("2", font_size = fs + 70).move_to(axes.c2p(4,4))
        t5 = Tex("D", "imensionen", font_size = fs + 40).next_to(t4, UP, aligned_edge=RIGHT)
        t2 = Tex("Kreuzprodukt", font_size = fs).move_to(axes.c2p(5,2.5))
        t3 = Tex("in", font_size = fs).next_to(t4, RIGHT, buff = 0.75, aligned_edge=UP)

        for mob in t2, t3, t4, t5:
            mob.rotate(angle = TAU/2)
            mob.set_color(LIGHT_GREY)

        t2.set_color_by_gradient(vec_a_color, vec_b_color)

        for mob in t4, t5[0]:
            mob.set_color(vec_c_color)
            #mob.set_stroke(color = YELLOW, width = 2)

        self.add(t2, t3, t4, t5)



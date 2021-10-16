from manim import *

vec_a_color = RED
vec_b_color = YELLOW
vec_c_color = BLUE

x_color = PINK
y_color = ORANGE




class Intro(VectorScene):
    def construct(self):
        plane = self.plane = NumberPlane(
            x_range = [-16, 16], y_range = [-10, 10],
            x_length = config["frame_width"], y_length = config["frame_height"],
            background_line_style={"stroke_color": GREY, "stroke_width": 2, "stroke_opacity": 0.4}
        )
        #self.play(Create(plane, lag_ratio = 0.05), run_time = 3)
        #self.wait()

        # numerical vector and scalare
        # scalars = [0.5, 1.5, 2, 0.75, 1/3]
        k_val = ValueTracker(0)
        num_vecs_input = [np.array(arr) for arr in 
            [[-2,4,0], [3,2,0], [3,-1.5,0], [-1,-4,0], [-6,-2,0]]
        ]
        num_vecs_output = [k_val.get_value() * num_vec for num_vec in num_vecs_input]

        colors_input = [YELLOW_A, YELLOW_B, YELLOW_C, YELLOW_D, YELLOW_E]
        colors_output = [BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E]

        arrows_input = VGroup(*[self.get_vector(num_vec).set_color(color).set_opacity(0.6) for num_vec, color in zip(num_vecs_input, colors_input)])
        arrows_output = VGroup(*[self.get_vector(num_vec).set_color(color).set_opacity(0.6) for num_vec, color in zip(num_vecs_output, colors_output)])


        ring_input = self.get_ring(arrows_input, color = YELLOW)
        ring_output = self.get_ring(arrows_output, color = BLUE)


        self.play(
            LaggedStartMap(GrowArrow, arrows_input, lag_ratio = 0.05),
            Create(ring_input),
            run_time = 4
        )
        self.wait()


        arrows_output[0].add_updater(lambda a: a.become(
            self.get_vector(k_val.get_value() * num_vecs_input[0]).set_color(colors_output[0]).set_opacity(0.6)
        ))
        arrows_output[1].add_updater(lambda a: a.become(
            self.get_vector(k_val.get_value() * num_vecs_input[1]).set_color(colors_output[1]).set_opacity(0.6)
        ))
        arrows_output[2].add_updater(lambda a: a.become(
            self.get_vector(k_val.get_value() * num_vecs_input[2]).set_color(colors_output[2]).set_opacity(0.6)
        ))
        arrows_output[3].add_updater(lambda a: a.become(
            self.get_vector(k_val.get_value() * num_vecs_input[3]).set_color(colors_output[3]).set_opacity(0.6)
        ))
        arrows_output[4].add_updater(lambda a: a.become(
            self.get_vector(k_val.get_value() * num_vecs_input[4]).set_color(colors_output[4]).set_opacity(0.6)
        ))


        self.add(*arrows_output)

        ring_output.add_updater(lambda r: r.become(
            self.get_ring(arrows_output, color = BLUE)
        ))
        self.add(ring_output)
        self.bring_to_front(*arrows_input, ring_input)

        static_scalars = [0.5, 1.0, 1.5, 2, 2.5, 3]
        static_arrows = VGroup(*[
            VGroup(*[self.get_vector(scalar * num_vec) for num_vec in num_vecs_input])
            for scalar in static_scalars
        ])
        static_rings = VGroup(*[self.get_ring(arrows, color = BLUE) for arrows in static_arrows])
        for ring in static_rings:
            ring.set_fill(color = BLACK, opacity = 0)

        # self.add(*static_rings)
        # self.wait()


        self.play(
            k_val.animate.set_value(3),
            run_time = 8
        )
        self.wait()
        self.play(k_val.animate.set_value(0.5), run_time = 2)
        self.play(k_val.animate.set_value(-2), run_time = 6)
        self.wait(2)




        # k_dec = DecimalNumber(k_val.get_value(), num_decimal_places = 1, include_sign = True).set_color(colors[0])
        # k_dec.add_updater(lambda k: k.set_value(k_val.get_value()))

        # mult = MathTex("\\cdot")

    # functions
    def get_ring(self, arrows, color):
        ring = VMobject()
        ring.set_points_as_corners([
            *[arrow.get_end() for arrow in arrows], 
            arrows[0].get_end()
        ])
        ring.set_stroke(color = color, width = 2)

        return ring


class WhatsAScalar(Scene):
    def construct(self):

        self.arrow_kwargs = {"buff": 0, "stroke_width": 3, "max_tip_length_to_length_ratio": 0.2}
        self.matrix_kwargs = {"left_bracket": "(", "right_bracket": ")", "element_alignment_corner": UP}

        self.title_of_this_episode()
        self.title_into_vec_eq()
        self.result_of_multiplication()


    def title_of_this_episode(self):
        title_episode = self.title_episode = Tex("Skalare ", "Multiplikation")\
            .set_color_by_gradient(vec_a_color, vec_b_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 1.5)\
            .scale(2)\
            .to_corner(UL)

        title_vec = self.title_vec = Tex("mit einem ", "Vektor")\
            .next_to(title_episode, DOWN, aligned_edge = RIGHT)\
            .shift(0.1*UP)

        for title in title_episode, title_vec:
            title.save_state()
            title.center()

        self.title_vec.next_to(title_episode, DOWN, aligned_edge = RIGHT).shift(0.1*UP)


        self.play(DrawBorderThenFill(title_episode), run_time = 3)
        self.wait()
        self.play(Write(title_vec))
        self.wait(2)

        title_rects = VGroup(*[
            SurroundingRectangle(part, color = color)
            for part, color in zip(
                [title_episode[1], title_episode[0]], 
                [vec_c_color, vec_a_color]
            )
        ])

        self.play(Create(title_rects[0]), run_time =2)
        self.wait(0.5)
        self.play(Transform(title_rects[0], title_rects[1]))
        self.wait(2)

        self.play(FadeOut(title_rects[0]))
        self.wait()

        self.play(
            LaggedStartMap(
                Restore, VGroup(title_episode, title_vec), lag_ratio = 0.15
            ), 
            run_time = 2
        )
        self.wait()

    def title_into_vec_eq(self):
        vec_gen = Matrix([["x"], ["y"], ["z"]], **self.matrix_kwargs)

        cdot = MathTex("\\cdot")
        sca_gen = MathTex("k").set_color(vec_a_color)

        vec_eq = VGroup(sca_gen, cdot, vec_gen)\
            .arrange_submobjects(RIGHT, buff = 0.5)

        self.play(TransformFromCopy(self.title_vec[1], vec_eq[-1]))
        self.play(TransformFromCopy(self.title_episode[1], vec_eq[1]))
        self.wait()

        vec_gen_sca = Matrix([["a"], ["b"], ["c"]], **self.matrix_kwargs).next_to(cdot, LEFT, buff = 0.5)

        self.play(Create(vec_gen_sca))
        self.wait()

        self.filmroll_pics()

        self.play(ReplacementTransform(vec_gen_sca, sca_gen))
        self.wait()


        brace_vec = Brace(vec_gen, DOWN)
        brace_vec_tex = brace_vec.get_text("Vektor").set_color(TEAL)

        arrow_sca = Arrow(ORIGIN, 1.5*RIGHT, color = GREY, **self.arrow_kwargs)\
            .next_to(sca_gen, LEFT, buff = 0.75)
        arrow_sca_tex = Tex("Skalar")\
            .set_color(vec_a_color)\
            .next_to(arrow_sca, LEFT, buff = 0.75)

        self.play(Create(brace_vec), Write(brace_vec_tex))
        self.wait()

        self.play(GrowArrow(arrow_sca), Write(arrow_sca_tex))
        self.wait()


        self.vec_gen = vec_gen
        self.sca_gen = sca_gen
        self.cdot = cdot
        self.scalar_text = arrow_sca_tex

    def result_of_multiplication(self):
        equals = MathTex("=").next_to(self.vec_gen, RIGHT, buff = 0.5)

        vec_out1 = Matrix([["r"], ["s"], ["t"]], **self.matrix_kwargs).next_to(equals, RIGHT, buff = 0.5)

        x_comp = MathTex("k", "\\cdot", "x")
        y_comp = MathTex("k", "\\cdot", "y")
        z_comp = MathTex("k", "\\cdot", "z")
        for comp in x_comp, y_comp, z_comp:
            comp.set_color_by_tex_to_color_map({"k": vec_a_color})

        vec_out2 = MobjectMatrix([[x_comp], [y_comp], [z_comp]], **self.matrix_kwargs)\
            .move_to(vec_out1, aligned_edge = LEFT)

        brace1 = Brace(vec_out1, DOWN)
        brace1_text = brace1.get_text("Vektor").set_color(TEAL)

        brace2 = Brace(vec_out2, DOWN)
        brace2_text = brace2.get_text("skalares\\\\", "Vielfaches\\\\", "des ", "Vektors")
        brace2_text[0].set_color(vec_a_color)
        brace2_text[3].set_color(TEAL)

        self.play(
            Write(equals), 
            Create(vec_out1),
        )
        self.play(Create(brace1), Write(brace1_text))
        self.wait()

        # aus einem Skalar --> je eins für die Komponenten machen
        vec_k = Matrix([["k"], ["k"], ["k"]], **self.matrix_kwargs).move_to(self.sca_gen)
        vec_k[0].set_color(vec_a_color)

        self.play(
            ReplacementTransform(self.sca_gen.copy(), vec_k[0][0]),
            ReplacementTransform(self.sca_gen.copy(), vec_k[0][1]),
            ReplacementTransform(self.sca_gen.copy(), vec_k[0][2]),
            run_time = 2
        )
        self.wait(0.5)

        # Skalara und Komponenten in den Ergebnisvektor kopieren
        self.play(
            AnimationGroup(
                Transform(vec_out1[1:], vec_out2[1:], run_time = 1),
                FadeOut(vec_out1[0], run_time = 1), 
                Transform(brace1, brace2, run_time = 1), 
                lag_ratio = 0.25
            ),
            Transform(vec_k[0][0], vec_out2[0][0][0]),
            Transform(vec_k[0][1], vec_out2[0][1][0]),
            Transform(vec_k[0][2], vec_out2[0][2][0]),
            TransformFromCopy(self.cdot, vec_out2[0][0][1]),
            TransformFromCopy(self.cdot, vec_out2[0][1][1]),
            TransformFromCopy(self.cdot, vec_out2[0][2][1]),
            TransformFromCopy(self.vec_gen[0][0], vec_out2[0][0][2]),
            TransformFromCopy(self.vec_gen[0][1], vec_out2[0][1][2]),
            TransformFromCopy(self.vec_gen[0][2], vec_out2[0][2][2]),
            run_time = 3.5
        )
        self.play(Transform(brace1_text, brace2_text))
        self.wait()


        self.play(
            *[ScaleInPlace(mob, scale_factor = 3, rate_func = there_and_back) for mob in [self.sca_gen, self.scalar_text]], 
            run_time = 2
        )
        self.play(
            *[ScaleInPlace(mob, scale_factor =-3, rate_func = there_and_back) for mob in [self.sca_gen, self.scalar_text]], 
            run_time = 2
        )
        self.wait(3)




    def filmroll_pics(self):
        self.video_nums = 2
        self.series = self.get_series_filmrolls()
        self.series.to_edge(DOWN)
        
        pic_dot = self.get_dotprod_pic()
        pic_cross = self.get_crossprod_pic()

        texts = VGroup(*[
            Tex(*tex).set_color(LIGHT_GREY).next_to(episode, direc)
            for tex, episode, direc in zip(
                [["Episode 04"], ["Episode 05"]], 
                self.series,
                [LEFT, RIGHT]
            )
        ])

        self.play(Create(self.series, lag_ratio = 0.15), run_time = 2)
        self.play(
            AnimationGroup(
                Create(VGroup(pic_dot, pic_cross)),
                Create(texts), 
                lag_ratio = 0.15
            ),
            run_time = 2
        )
        self.wait()

        self.play(ShrinkToCenter(VGroup(self.series, pic_dot, pic_cross, texts)))
        self.wait()

    # functions 

    def get_series_filmrolls(self):
        icon = SVGMobject(file_name = "video_icon")

        series = VGroup(*[icon.copy() for x in range(self.video_nums)])
        series.arrange_submobjects(RIGHT, buff = 0.75)
        series.set(width = 5)
        series.set_color(GREY)
        series.to_edge(UP)

        return series

    def get_dotprod_pic(self):
        vec_a_num = [1.5, 0, 0]
        vec_b_num = [0.8, 1, 0]
        vec_c_num = [0.8, 0, 0]

        vec_a = Arrow(ORIGIN, vec_a_num[0]*RIGHT + vec_a_num[1]*UP, color = vec_a_color, **self.arrow_kwargs)
        vec_b = Arrow(ORIGIN, vec_b_num[0]*RIGHT + vec_b_num[1]*UP, color = vec_b_color, **self.arrow_kwargs)
        vec_c = Arrow(ORIGIN, vec_c_num[0]*RIGHT + vec_c_num[1]*UP, color = vec_c_color, **self.arrow_kwargs)

        line = DashedLine(vec_b.get_end(), vec_c.get_end(), color = GREY)

        pic = VGroup(line, vec_a, vec_b, vec_c)
        pic.move_to(self.series[0][-1])
        pic.set(height = self.series[0][-1].get_height() - 0.2)

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
        pic.move_to(self.series[1][-1])
        pic.set(height = self.series[1][-1].get_height() - 0.2)

        return pic


class Numberline(Scene):
    def construct(self):

        num_line_c = NumberLine(
            x_range = [-8, 13, 1], length = 13, unit_size = 1, 
            include_numbers = True, include_tip = True, 
            numbers_to_exclude = range(-7,12,2)
        )
        num_line_a = num_line_c.copy()
        num_line_k = NumberLine(x_range = [-4, 5, 1], length = 6.5, unit_size = 2, include_numbers = True, include_tip = True)

        num_lines = VGroup(num_line_k, num_line_a, num_line_c)\
            .arrange_submobjects(DOWN, buff = 1)

        colors = [vec_a_color, vec_b_color, vec_c_color]

        labels = VGroup(*[
            MathTex(tex).set_color(color).next_to(num_line.tip, RIGHT, buff = 0.5)
            for tex, color, num_line in zip(
                ["k", "a", "c"], colors, [*num_lines],
            )
        ])


        k_val = ValueTracker(4)
        a_val = ValueTracker(2)
        c_val = ValueTracker(k_val.get_value() * a_val.get_value())

        k_dec = DecimalNumber(k_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda a: a.set_value(k_val.get_value()))\
            .set_color(colors[0])

        plus = MathTex("\\cdot")

        a_dec = DecimalNumber(a_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda a: a.set_value(a_val.get_value()))\
            .set_color(colors[1])

        task = VGroup(k_dec, plus, a_dec)\
            .arrange_submobjects(RIGHT, buff = 0.5)\
            .to_edge(UP)\
            .scale(1.5)

        c_dec = DecimalNumber(c_val.get_value(), num_decimal_places=0)\
            .add_updater(lambda c: c.set_value(k_val.get_value() * a_val.get_value()))\
            .set_color(colors[2])\
            .to_edge(DOWN)\
            .scale(1.5)


        arrows = VGroup(
            Arrow(k_dec.get_bottom() + 0.15*DOWN, num_line_k.number_to_point(k_val.get_value()), stroke_width = 3, color = colors[0], buff = 0),
            *[
                Arrow(num_line.number_to_point(0), num_line.number_to_point(value.get_value()), color = color, buff = 0)
                for num_line, value, color in zip(
                    [*num_lines[1:]], [a_val, c_val], [*colors[1:]]
                )
            ]
        )


        self.play(FadeIn(VGroup(*task, c_dec), shift = DOWN, lag_ratio = 0.15), run_time = 2)
        self.wait()

        self.play(
            Create(num_lines, lag_ratio = 0.25),
            FadeIn(labels, shift = LEFT, lag_ratio = 0.25),
            run_time = 4
        )
        self.wait()

        self.play(
            LaggedStart(
                TransformFromCopy(k_dec, num_line_k.get_number_mobject(k_val.get_value())), 
                TransformFromCopy(a_dec, num_line_a.get_number_mobject(a_val.get_value())),
                TransformFromCopy(c_dec, num_line_c.get_number_mobject(c_val.get_value())),
                lag_ratio = 0.3
            ),
            *[GrowArrow(arrow) for arrow in arrows], 
            run_time = 4
        )
        self.wait()


        arrows[0].add_updater(lambda h: h.become(
            Arrow(k_dec.get_bottom() + 0.15*DOWN, num_line_k.number_to_point(k_val.get_value()), stroke_width = 3, color = colors[0], buff = 0)
        ))
        arrows[1].add_updater(lambda h: h.become(
            Arrow(num_line_a.number_to_point(0), num_line_a.number_to_point(a_val.get_value()), color = colors[1], buff = 0)
        ))
        arrows[2].add_updater(lambda h: h.become(
            Arrow(num_line_c.number_to_point(0), num_line_c.number_to_point(k_val.get_value() * a_val.get_value()), color = colors[2], buff = 0)
        ))


        k_values = [4, -3, -3]
        a_values = [2,  2, -4]
        brackets = VGroup(*[
            MathTex(tex).scale(1.5) for tex in ["(", ")"]
        ])
        brackets.arrange_submobjects(RIGHT, buff = 1)
        brackets.move_to(a_dec).shift(0.25*RIGHT)

        for index in range(len(k_values)):
            if a_values[index] < 0:
                direc_a_value = -1
                fade_in_anims = [FadeIn(brackets, shift = DOWN)]
                fade_out_anims = [FadeOut(brackets, shift = UP)]
            else:
                direc_a_value = 1
                fade_in_anims = []
                fade_out_anims = []


            self.play(
                k_val.animate.set_value(k_values[index]),
                a_val.animate.set_value(a_values[index]),
                *fade_in_anims,
                run_time = 3
            )
            self.wait()


            if k_values[index] < 0:
                direc_k_value = LEFT
                arrow_number_correction = 0
            else:
                direc_k_value = RIGHT
                arrow_number_correction = 1

            arrow_copys = VGroup(*[
                arrows[1].copy().clear_updaters() 
                for _ in range(int(abs(k_val.get_value())) - arrow_number_correction)
            ])
            arrow_copys.arrange_submobjects(direc_k_value * direc_a_value, buff=0)

            if k_values[index] < 0:
                arrow_copys.rotate(180*DEGREES)
            arrow_copys.next_to(arrows[1], direc_k_value * direc_a_value, buff = 0)

            self.play(
                *[FadeIn(arrow, target_position = arrows[1].get_center()) for arrow in arrow_copys],
                run_time = 3
            )
            self.play(
                Circumscribe(num_line_a.get_number_mobject(k_values[index] * a_values[index]), color = colors[1]), 
                Circumscribe(num_line_c.get_number_mobject(k_values[index] * a_values[index]), color = colors[2]), 
                run_time = 2
            )
            self.wait(0.5)

            self.play(
                *[FadeOut(arrow, target_position = arrows[1].get_center()) for arrow in arrow_copys],
                run_time = 3
            )
            self.wait()


class Geometric2D(VectorScene):
    def construct(self):
        self.different_scalars()
        self.walk_along_line()

    def different_scalars(self):
        plane = self.plane = NumberPlane(
            x_range = [-16, 16], y_range = [-10, 10],
            x_length = config["frame_width"], y_length = config["frame_height"],
            background_line_style={"stroke_color": GREY, "stroke_width": 2, "stroke_opacity": 0.4}
        )
        plane.add_coordinates(x_values = range(-16,16,2), y_values = range(-12,12,2))
        self.play(Create(plane, lag_ratio = 0.05), run_time = 3)


        sca_val = ValueTracker(2)
        veca_num = np.array([4,3,0])

        # Vektoren
        arrow_ori = self.get_vector(veca_num, color = vec_b_color)
        arrow_sca = self.get_vector(sca_val.get_value() * veca_num, color = BLUE)


        # alle Elemente für die Rechnung
        sca_dec = DecimalNumber(sca_val.get_value(), num_decimal_places = 1, include_sign=True).set_color(vec_a_color)
        times = MathTex("\\cdot")
        veca_mat = Matrix([[veca_num[0]],[veca_num[1]]], left_bracket="(", right_bracket=")")
        equals = MathTex("=")

        mat_x = DecimalNumber(sca_val.get_value() * veca_num[0], num_decimal_places=1, include_sign=True)
        mat_y = DecimalNumber(sca_val.get_value() * veca_num[1], num_decimal_places=1, include_sign=True)
        vecc_mat = MobjectMatrix([[mat_x],[mat_y]], left_bracket="(", right_bracket=")", element_alignment_corner = RIGHT)

        sca_dec.add_updater(lambda d: d.set_value(sca_val.get_value()))
        mat_x.add_updater(lambda x: x.set_value(sca_val.get_value() * veca_num[0]))
        mat_y.add_updater(lambda y: y.set_value(sca_val.get_value() * veca_num[1]))

        equation = VGroup(sca_dec, times, veca_mat, equals, vecc_mat)\
            .arrange_submobjects(RIGHT)\
            .to_corner(UL, buff = 0.25)\
            .add_background_rectangle()


        # Vektor vorstellen
        self.play(
            Create(equation[0]), 
            GrowArrow(arrow_ori), 
            run_time = 2
        )
        self.play(FadeIn(equation[3], shift = 0.5*UP), run_time = 2)

        xy_lines = self.get_xy_lines(arrow_ori)
        self.play(ShowPassingFlash(xy_lines, time_width = 1, lag_ratio = 0.15), run_time = 3)
        self.wait()

        # Scalar vorstellen, Vektor verlängern
        self.play(
            FadeIn(VGroup(equation[1], equation[2]), shift = 0.5*UP, lag_ratio = 0.25), 
            run_time = 2
        )
        self.wait()

        arrow_ori_copy = arrow_ori.copy()
        self.play(arrow_ori_copy.animate.put_start_and_end_on(start = arrow_ori.get_end(), end = plane.coords_to_point(8,6)), run_time = 3.5)
        self.wait()

        self.play(
            FadeOut(arrow_ori_copy), 
            GrowArrow(arrow_sca), 
            run_time = 3.5
        )
        self.bring_to_front(arrow_ori)
        self.wait()

        # Ergebnis Vektor
        xy_lines = self.get_xy_lines(arrow_sca)
        self.play(ShowPassingFlash(xy_lines, time_width = 1, lag_ratio = 0.15), run_time = 3)
        self.play(FadeIn(VGroup(equation[4], equation[5]), shift = 0.5*UP, lag_ratio = 0.15), run_time = 2)
        self.wait()

        arrow_sca.add_updater(lambda a: a.become(self.get_vector(sca_val.get_value() * veca_num, color = BLUE)))


        # Schleife ValueTracker Animation
        scale_values = [3, 0.5, -1, -2, -4]

        for scale_value in scale_values:
            self.play(
                sca_val.animate.set_value(scale_value), 
                run_time = 3
            )
            self.play(Circumscribe(sca_dec, color = vec_a_color))
            xy_lines = self.get_xy_lines(arrow_sca)
            self.play(ShowPassingFlash(xy_lines, time_width = 1, lag_ratio = 0.15), run_time = 2)
            self.wait()


        self.sca_val = sca_val
        self.arrow_ori, self.arrow_sca = arrow_ori, arrow_sca

    def walk_along_line(self):

        line = Line(self.plane.c2p(-16, -12), self.plane.c2p(16, 12))
        line_ticks = self.get_vector_line_ticks(self.arrow_ori, line, divide_num = 9)

        labels = VGroup(*[
            MathTex(*tex).set_color(vec_a_color).scale(0.75)
            for tex in ["-4", "-3", "-2", "-1", "0", "1", "2", "3", "4"]
        ])
        for label, tick in zip(labels, line_ticks):
            label.next_to(tick, DR, buff = 0.1)


        self.play(
            Create(line),
            self.sca_val.animate.set_value(4),
            ShowIncreasingSubsets(line_ticks),
            ShowIncreasingSubsets(labels),
            run_time = 10
        )
        self.bring_to_front(self.arrow_sca, self.arrow_ori)
        self.play(self.sca_val.animate.set_value(1))
        self.wait()

        for scale_value in [3, -2]:
            self.play(self.sca_val.animate.set_value(scale_value), run_time = 6)
            self.wait()
        self.wait(3)

    # functions

    def get_xy_lines(self, arrow):
        x_line = Line(arrow.get_end(), arrow.get_end()[1]*UP, color = x_color)
        y_line = Line(arrow.get_end(), arrow.get_end()[0]*RIGHT, color = y_color)

        result = VGroup(x_line, y_line)

        return result

    def get_vector_line_ticks(self, vector, line, divide_num):
        angle = line.get_angle()

        ticks = VGroup()
        tick_length = 0.2

        ticks = VGroup()
        for x in np.linspace(0,1,divide_num):
            tick = Line(UP, DOWN)
            tick.set_length(tick_length)
            tick.move_to(line.point_from_proportion(x))
            tick.rotate(angle)
            ticks.add(tick)

        return ticks


class Geometric3D(ThreeDScene):
    def construct(self):

        axes = self.axes = ThreeDAxes(x_range = [-12, 14], y_range = [-10, 10], z_range = [-6,6])
        axes.add_coordinates(x_values = range(-10,13,2), y_values = range(-10,9,2))
        self.set_camera_orientation(phi = 70*DEGREES, theta = 30*DEGREES)
        origin = axes.coords_to_point(0,0,0)

        sca_val = ValueTracker(1)
        veca_num = np.array([4,-2,2])
        vecc_num = sca_val.get_value() * veca_num


        self.cone_height, self.cone_radius = 0.5, 0.15
        cone_kwargs = {"cone_height": self.cone_height, "base_radius": self.cone_radius}
        arrow_a = Arrow3D(start = origin, end = axes.coords_to_point(*veca_num), **cone_kwargs, color = vec_b_color)
        arrow_c = Arrow3D(start = origin, end = axes.coords_to_point(*vecc_num), **cone_kwargs, color = BLUE)

        components_a = self.get_component_lines(veca_num, line_class = Line, color = YELLOW_E)
        components_c = self.get_component_lines(veca_num, line_class = Line, color = BLUE_E)

        labels_axes = VGroup(*[
            MathTex(label).next_to(axis, direction = direction)
            for label, axis, direction in zip(
                ["x", "y", "z"], 
                [self.axes.x_axis, self.axes.y_axis, self.axes.z_axis], 
                [RIGHT, UP, OUT]
            )
        ])

        self.add_fixed_orientation_mobjects(*labels_axes)

        max_dist = 6
        line = Line3D(
            start = axes.c2p(-1*max_dist * veca_num[0], -1*max_dist * veca_num[1], -1*max_dist * veca_num[2]),
            end = axes.c2p(max_dist * veca_num[0], max_dist * veca_num[1], max_dist * veca_num[2]),
            color = GREY, thickness = 0.01
        )
        line.set_opacity(0.25)


        # Elemente Hinzufügen
        dot = Dot3D(point = origin, radius = 0.1)
        self.play(
            Create(axes), 
            Create(labels_axes),
            FadeIn(dot, shift = 3*OUT),
            run_time = 3
        )
        self.wait()

        directions = [4*RIGHT, 4*RIGHT+2*DOWN, 4*RIGHT+2*DOWN+2*OUT]
        for direc in directions:
            self.play(dot.animate.move_to(axes.c2p(*direc)), run_time = 1)
            self.wait(0.25)


        self.play(
            Create(line),
            LaggedStartMap(
                Create, VGroup(*components_a, arrow_a), lag_ratio = 0.15
            ),
            FadeOut(dot),
            run_time = 2
        )
        self.wait()

        #self.begin_ambient_camera_rotation(rate = 0.07)
        self.wait()


        # Updaters
        arrow_c.add_updater(lambda ac: ac.become(
            Arrow3D(
                start = origin, 
                end = axes.coords_to_point(sca_val.get_value() * veca_num[0], sca_val.get_value() * veca_num[1], sca_val.get_value() * veca_num[2]), 
                **cone_kwargs, color = BLUE
            )
        ))
        components_c.add_updater(self.get_component_lines_updater(tracker = sca_val, vec_num = veca_num, line_class = Line, color = BLUE_E))

        self.add(arrow_c, components_c)
        self.play(sca_val.animate.set_value(3), run_time = 2.5)
        self.play(sca_val.animate(rate_func = linear).set_value(1), run_time = 5)

            # if scale_value == 1:
            #     self.stop_ambient_camera_rotation()
            #     self.begin_ambient_camera_rotation(rate = -0.15)

        arrow_c.suspend_updating()
        components_c.suspend_updating()
        new_arrow_c = Arrow3D(start = origin, end = axes.coords_to_point(*[-1 * x for x in vecc_num]), **cone_kwargs, color = BLUE)
        new_components_c = self.get_component_lines([-1*x for x in veca_num], line_class = Line, color = BLUE_E)

        self.play(
            Transform(arrow_c, new_arrow_c), 
            Transform(components_c, new_components_c), 
            sca_val.animate.set_value(-1),
            rate_func = linear, run_time = 2.5
        )
        arrow_c.resume_updating()
        components_c.resume_updating()

        self.play(sca_val.animate(rate_func = linear).set_value(-3), run_time = 5)
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

    def get_component_lines_updater(self, tracker, vec_num, line_class = DashedLine, color = BLUE, **kwargs):
        def updater(mob):
            axes = self.axes

            x_component = line_class(
                axes.c2p(tracker.get_value() * vec_num[0], 0, 0),
                axes.c2p(tracker.get_value() * vec_num[0], tracker.get_value() * vec_num[1], 0),
                color = color, **kwargs
            )
            y_component = line_class(
                axes.c2p(0, tracker.get_value() * vec_num[1], 0),
                axes.c2p(tracker.get_value() * vec_num[0], tracker.get_value() * vec_num[1], 0),
                color = color, **kwargs
            )
            z_component = line_class(
                axes.c2p(tracker.get_value() * vec_num[0], tracker.get_value() * vec_num[1], 0),
                axes.c2p(tracker.get_value() * vec_num[0], tracker.get_value() * vec_num[1], tracker.get_value() * vec_num[2]),
                color = color, **kwargs
            )

            components = VGroup(x_component, y_component, z_component)


            mob.become(components)
        return updater


class Geometric3D_Calc(Scene):
    def construct(self):
        sca_val = ValueTracker(1)
        veca_num = np.array([4,-2,2])

        sca_dec = DecimalNumber(sca_val.get_value(), num_decimal_places=1, include_sign = True)\
            .set_color(vec_a_color)
        times = MathTex("\\cdot")
        veca_mat = Matrix([[veca_num[0]], [veca_num[1]], [veca_num[2]]], left_bracket="(", right_bracket=")", v_buff = 0.6, bracket_v_buff = 0.1)

        eq = VGroup(sca_dec, times, veca_mat)\
            .arrange_submobjects(RIGHT)\
            .add_background_rectangle()\
            .to_corner(UR)

        self.wait(2)
        self.play(Write(eq[3][1:]), run_time = 2)

        for index in range(3):
            self.play(Write(eq[3][0][index]), run_time = 1)
            self.wait(0.25)

        self.play(
            FadeIn(eq[1:3], shift = 0.5*RIGHT), 
            run_time = 2
        )
        self.wait(2)


        sca_dec.add_updater(lambda dec: dec.set_value(sca_val.get_value()))

        self.play(sca_val.animate.set_value(3), run_time = 2.5)
        self.play(sca_val.animate(rate_func = linear).set_value(1), run_time = 5)

        self.play(sca_val.animate.set_value(-1), rate_func = linear, run_time = 2.5)
        self.play(sca_val.animate(rate_func = linear).set_value(-3), run_time = 5)
        self.wait(3)


class Analytic(Scene):
    def construct(self):

        sca_val = ValueTracker(-2)
        veca_num = np.array([4,3,0])


        # alle Elemente für die Rechnung
        sca_dec = DecimalNumber(sca_val.get_value(), num_decimal_places = 1, include_sign=True).set_color(vec_a_color)
        times = MathTex("\\cdot")
        veca_mat = Matrix([[veca_num[0]],[veca_num[1]]], left_bracket="(", right_bracket=")")
        equals = MathTex("=")

        mat_x = DecimalNumber(sca_val.get_value() * veca_num[0], num_decimal_places=1, include_sign=True)
        mat_y = DecimalNumber(sca_val.get_value() * veca_num[1], num_decimal_places=1, include_sign=True)
        vecc_mat = MobjectMatrix([[mat_x],[mat_y]], left_bracket="(", right_bracket=")", element_alignment_corner = RIGHT)

        sca_dec.add_updater(lambda d: d.set_value(sca_val.get_value()))
        mat_x.add_updater(lambda x: x.set_value(sca_val.get_value() * veca_num[0]))
        mat_y.add_updater(lambda y: y.set_value(sca_val.get_value() * veca_num[1]))

        equation = VGroup(sca_dec, times, veca_mat, equals, vecc_mat)\
            .arrange_submobjects(RIGHT)\
            .to_corner(UL, buff = 0.25)\
            .add_background_rectangle()

        self.add(equation)
        self.wait()


        text_top = Text("Skalare Multiplikation")\
            .set_color_by_gradient(vec_a_color, vec_b_color, BLUE)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 2)\
            .set(width = config["frame_width"] - 2)\
            .move_to(2*UP)

        text_bottom = Tex("Multiplikation des ", "Skalars\\\\", "in jeder Komponente").move_to(2.5*DOWN)
        text_bottom[1].set_color(vec_a_color)

        # equaiton auseinanderziehen
        self.play(equation.animate.center(), run_time = 3)
        self.play(
            Write(text_top),
            equation[1:4].animate.shift(1.8*LEFT), 
            equation[4:].animate.shift(1.8*RIGHT),
            run_time = 2
        )


        inter_equal = MathTex("=").next_to(equation[3], RIGHT, buff = 0.25)

        x_dec = DecimalNumber(sca_val.get_value(), num_decimal_places = 1, include_sign=True).set_color(vec_a_color)
        y_dec = DecimalNumber(sca_val.get_value(), num_decimal_places = 1, include_sign=True).set_color(vec_a_color)

        x_coord = [x_dec, MathTex("\\cdot \\ \\", str(veca_num[0]))]
        y_coord = [y_dec, MathTex("\\cdot \\ \\", str(veca_num[1]))]

        inter_mat = MobjectMatrix(
            [[*x_coord], [*y_coord]], 
            element_alignment_corner = DOWN, 
            left_bracket="(", right_bracket=")", 
            h_buff = 1
        )
        inter_mat.next_to(inter_equal, RIGHT, buff = 0.25)


        self.play(
            FadeIn(inter_equal, shift = 0.5*UP), 
            FadeIn(inter_mat[-2:], shift = 0.5*DOWN), 
            run_time = 1.5
        )
        self.wait()

        x_dec.add_updater(lambda d: d.set_value(sca_val.get_value()))
        y_dec.add_updater(lambda d: d.set_value(sca_val.get_value()))


        # Scalar in die Komponenten kopieren
        self.play(
            AnimationGroup(
                ApplyMethod(sca_dec.copy().move_to, inter_mat[0][0][0].get_right(), path_arc = -2),
                ApplyMethod(sca_dec.copy().move_to, inter_mat[0][2][0].get_right(), path_arc = +2),
                lag_ratio = 0.2
            ),
            run_time = 4
        )
        self.wait()

        # originale Komponenten kopieren
        self.play(
            AnimationGroup(
                ApplyMethod(equation[3][0][0].copy().move_to, inter_mat[0][1][1], path_arc = -1),
                ApplyMethod(equation[3][0][1].copy().move_to, inter_mat[0][3][1], path_arc = +1),
                ApplyMethod(equation[2].copy().move_to, inter_mat[0][1][0], path_arc = -1),
                ApplyMethod(equation[2].copy().move_to, inter_mat[0][3][0], path_arc = +1),
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.play(
            Write(text_bottom), run_time = 2
        )
        self.wait()


        sur_rects = VGroup(*[
            SurroundingRectangle(mat_entry, buff = 0.3)
            for mat_entry in [inter_mat[0][0:2], inter_mat[0][2:]]
        ])

        self.play(Create(sur_rects[0]), run_time = 2)
        self.wait()
        self.play(Transform(sur_rects[0], sur_rects[1]), run_time = 1.5)
        self.wait()
        self.play(FadeOut(sur_rects[0]))
        self.wait()


        for scale_value in [3, -2, 0.5, -1]:
            self.play(sca_val.animate.set_value(scale_value), run_time = 5)
            self.wait()
        self.wait()




class Thumbnail(Geometric2D):
    def construct(self):

        self.different_scalars()
        self.walk_along_line()


        self.play(self.sca_val.animate.set_value(3), run_time = 6)
        self.wait()


        title1 = Tex("Multiplikation")\
            .set_color_by_gradient(vec_b_color, vec_c_color, vec_c_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = config["frame_width"] - 2)\
            .add_background_rectangle()\
            .to_edge(DOWN, buff = 1.5)

        title0 = Tex("Skalare")\
            .set_color(vec_a_color)\
            .set_fill(color = GREY, opacity = 0.5)\
            .set_stroke(width = 3)\
            .set(width = 5)\
            .add_background_rectangle()\
            .next_to(title1, UP, aligned_edge=LEFT)

        epi = Tex("Episode 02")\
            .next_to(title1, DOWN, aligned_edge = RIGHT)\
            .add_background_rectangle()

        self.add(title0, title1, epi)




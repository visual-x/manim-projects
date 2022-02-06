from manim import *
from BinomHelpers import *
import random

import scipy.stats 
import itertools as it


def get_row_of_boxes(height = 0.5, n = 4, **kwargs):
    boxes = VGroup()
    for _ in range(n):
        box = Square(color = LIGHT_GREY, stroke_width = 2, **kwargs)
        box.set(height = height)
        boxes.add(box)
    boxes.arrange(RIGHT, buff = 0.25)
    return boxes

def get_general_bin_formula():
        formula = MathTex(
            "P", "(", "X", "=", "k", ")", "=",
            "\\left(", "{" + "n", "\\over", "k" + "}", "\\right)", "\\cdot", 
            "p^", "k", "\\cdot", 
            "(", "1", "-", "p", ")^", "{" + "n-k" + "}"
        )
        formula.remove(formula.get_part_by_tex("\\over"))
        formula.set_color_by_tex_to_color_map({"p": YELLOW_D, "k": C_COLOR, "n-k": X_COLOR})

        return formula


class MultipleChoice(Scene):
    def construct(self):


        self.medicine_question()
        self.pass_this_test()


    def medicine_question(self):
        task1 = Tex("Frage 1:", font_size = 60)\
            .to_corner(UL)\
            .set_color_by_gradient(TEAL, TEAL_A, TEAL)\
            .save_state()
        uline = Underline(task1, color = DARK_GREY)

        task1.scale(1.6).center()

        body = SVGMobject(SVG_DIR + "human_body_back")
        body.set(height = 6)
        body.to_edge(RIGHT)
        gluteus = body[-4:-2]
        for muscle in body:
            muscle.save_state()
        body.center()

        colors = [BLUE, YELLOW, PINK, TEAL]
        self.play(DrawBorderThenFill(body, rate_func = rush_into), run_time = 5)
        self.play(
            AnimationGroup(
                *[FadeToColor(body[index], color = random.choice(colors), rate_func = there_and_back) for index in range(1, len(body))], 
                lag_ratio = 0.02
            ), run_time = 4
        )


        # body to side, show number of questions
        questions = VGroup(*[Tex("Frage ", str(x), ":", ) for x in range(1, 11)])
        questions.arrange(DOWN, aligned_edge = LEFT)
        questions.to_corner(UL)

        self.play(
            AnimationGroup(
                *[Restore(muscle, path_arc = np.pi/3) for muscle in body], lag_ratio = 0.05
            ),
            LaggedStartMap(FadeIn, questions, shift = 0.25*RIGHT, lag_ratio = 0.05, rate_func = there_and_back), 
            run_time = 4
        )


        # show question number 1
        question = Tex("Welche Antwort ist falsch?\\\\ Der ", "Musculus gluteus maximus", "...", tex_environment="flushleft")
        question.to_corner(UL).shift(2.5*RIGHT)

        self.play(
            AnimationGroup(Restore(task1, path_arc = -np.pi/3), Create(uline), lag_ratio = 0.2),
            Write(question),
            run_time = 2
        )
        self.wait(0.5)
        self.play(
            AnimationGroup(*[FadeToColor(mob, PINK) for mob in [question[1], gluteus]], lag_ratio = 0.25),
            run_time = 2.5
        )
        self.wait(0.5)


        answers_list = [
            "wird vom Nervus gluteus inferior aus \\\\dem Plexus sacralis innerviert", 
            "hat seinen Ursprung u.a. an der Spina \\\\iliaca posterior superior", 
            "fällt bei Schädigungen durch das \\\\Trendelenburg-Zeichen auf", 
            "ist ein wichtiger Extensor im Hüftgelenk \\\\und ermöglicht das Treppensteigen"
        ]
        answers = VGroup(*[Tex(answer, tex_environment="flushleft") for answer in answers_list])
        answers.arrange(DOWN, buff = 0.45, aligned_edge = LEFT)
        answers.to_edge(LEFT, buff = 1.5)
        answers.shift(0.75*DOWN)

        boxes = VGroup(*[Square() for x in range(4)])
        for box, answer in zip(boxes, answers):
            box.set(height = 0.5)
            box.set_color(TEAL_A)
            box.next_to(answer, LEFT, buff = 0.75, aligned_edge=UL)

        self.play(FadeIn(boxes, shift = RIGHT, lag_ratio = 0.1), run_time = 2)
        self.play(LaggedStartMap(FadeIn, answers, lag_ratio = 0.1), run_time = 2)
        self.wait()

        # randomize answer & highlight options
        cross = Cross(boxes[0], stroke_color = YELLOW_D, stroke_width = 3)
        def randomize_cross(mob):
            choices = range(4)
            num = random.choice(choices)
            mob.move_to(boxes[num])

        for x in range(len(answers)):
            highlight = answers[x]
            make_dark = [answers[i] for i in range(4) if i != x]
            self.play(
                FadeToColor(highlight, WHITE),
                *[FadeToColor(mob, DARK_GREY) for mob in make_dark], 
                UpdateFromFunc(cross, randomize_cross),
                run_time = 3
            )
            self.wait()
        self.play(FadeToColor(answers, WHITE))
        self.wait(3)


        self.fade_out_group = VGroup(task1, uline, question, answers, cross)
        self.first_boxes = boxes
        self.body = body

    def pass_this_test(self):
        boxes = VGroup(*[self.get_row() for x in range(10)])
        boxes.arrange(DOWN, buff = 0.25)
        boxes.set_color(TEAL_A)

        for box, index in zip(self.first_boxes, range(4)):
            box.generate_target()
            box.target.become(boxes[0][index])

        numbers = VGroup(*[Tex(str(num)) for num in range(1, 11)])
        for num, row in zip(numbers, boxes):
            num.set(height = row.height - 0.25)
            num.next_to(row, LEFT, buff = 0.5)

        crosses = VGroup()
        for row in boxes:
            cross = Cross(boxes[0][0], stroke_color = YELLOW_D, stroke_width = 3)
            choices = range(4)
            value = random.choice(choices)

            cross.move_to(row[value])
            crosses.add(cross)

        bools = 3*[False] + 2*[True] + 3*[False] + [True] + [False]
        cac = get_checks_and_crosses(bools)
        for row, mark in zip(boxes, cac):
            mark.match_height(row)
            mark.next_to(row, RIGHT, buff = 0.5)


        self.play(
            FadeOut(self.fade_out_group, rate_func = squish_rate_func(smooth, 0, 0.4)),
            AnimationGroup(*[MoveToTarget(box) for box in self.first_boxes], lag_ratio = 0.05),
            LaggedStartMap(FadeIn, boxes[1:], lag_ratio = 0.1),
            run_time = 3
        )
        self.wait(0.5)

        self.play(
            LaggedStartMap(GrowFromCenter, crosses, lag_ratio = 0.1),
            FadeIn(numbers, shift = 0.5*RIGHT, lag_ratio = 0.1),
            run_time = 2
        )

        self.play(FadeIn(cac, shift = 0.5*LEFT, lag_ratio = 0.1), run_time = 1.5)
        self.wait()


        prop = ValueTracker(0)
        prop_dec = Integer(edge_to_fix = RIGHT, unit = "\\%")
        prop_dec.set_color(RED)
        prop_dec.set(height = 1)
        prop_dec.move_to(4*LEFT + 2.5*UP)
        prop_dec.add_updater(lambda dec: dec.set_value(prop.get_value()))
        prop_dec.add_updater(lambda dec: dec.set_color(self.parameter_to_color(prop.get_value(), 0, 80, [RED, GREEN])))

        mt = Tex("mehr als")
        mt.set(width = prop_dec.width)
        mt.next_to(prop_dec, UP, buff = 0.1)

        self.add(prop_dec)
        self.play(
            prop.animate.set_value(80),
            Write(mt, rate_func = squish_rate_func(smooth, 0.75, 1)),
            run_time = 4
        )
        self.wait(0.5)


        certi = self.get_certificate()
        certi.next_to(prop_dec, DOWN, buff = 2.5)

        arrow = Arrow(prop_dec.get_bottom(), certi.get_top(), color = YELLOW_D)
        self.play(GrowArrow(arrow))


        self.play(LaggedStartMap(Create, certi, lag_ratio = 0.1), run_time = 2)
        self.play(DrawBorderThenFill(self.body.copy(), rate_func = rush_into), run_time = 5)
        self.wait(3)

    # functions 
    def get_row(self, height = 0.5, n = 4):
        boxes = VGroup()
        for _ in range(n):
            box = Square(color = GREY_B, stroke_width = 2)
            box.set(height = height)
            boxes.add(box)
        boxes.arrange(RIGHT, buff = 0.25)
        
        return boxes

    def get_certificate(self):
        rect = Rectangle(width = 2, height = 2*1.414, stroke_width = 1.5)
        text = Tex("Zertifikat")
        text.set(width = rect.width - 0.2)
        text.next_to(rect.get_top(), DOWN, buff = 0.2)

        lines = VGroup(*[Line() for x in range(10)])
        for line in lines:
            line.set(width = rect.width - 0.3)
            line.set_stroke(width = 1)
        lines.arrange(DOWN, buff = 0.1)

        passed = Tex("Bestanden")
        passed.set_color(C_COLOR)
        passed.set(width = rect.width - 0.5)
        passed.next_to(rect.get_corner(DR), UL, aligned_edge=RIGHT)

        result = VGroup(rect, text, lines, passed)
        return result

    def parameter_to_color(self, value, min, max, colors):
        alpha = inverse_interpolate(min, max, value)
        index, sub_alpha = integer_interpolate(0, len(colors) - 1, alpha)

        return interpolate_color(colors[index], colors[index + 1], sub_alpha)


class IntroduceFormula(Scene):
    def construct(self):


        self.get_to_three_questions()
        self.explain_xek()
        self.bernoulli_trail()


    def get_to_three_questions(self):
        formula = MathTex(
            "P", "(", "X", "=", "k", ")", "=",
            "\\left(", "{" + "n", "\\over", "k" + "}", "\\right)", "\\cdot", 
            "p^", "k", "\\cdot", 
            "(", "1", "-", "p", ")^", "{" + "n-k" + "}"
        )
        formula.scale(1.5)
        formula.move_to(0.75*UP)
        formula.remove(formula.get_part_by_tex("\\over"))
        formula.set_color_by_tex_to_color_map({"p": YELLOW_D, "k": C_COLOR, "n-k": X_COLOR})

        name = Tex("Bernoulli", "$-$", "Formel")\
            .set_color_by_gradient(GREEN, YELLOW_D, RED)\
            .set_fill(GREY, 0.3)\
            .set_stroke(width = 1.5)\
            .set(width = formula.width)\
            .to_edge(DOWN)

        self.play(Write(formula), run_time = 1.5)
        self.wait()
        sur_rects = VGroup(*[
            SurroundingRectangle(formula, buff = buff, stroke_width = 2).set_color([GREEN, YELLOW_D, RED])
            for buff in reversed(np.linspace(0.1, 0.55, 11))
        ])
        self.play(FadeIn(sur_rects, scale = 2, lag_ratio = 0.05), rate_func = lambda t: smooth(1-t), run_time = 2)
        self.play(DrawBorderThenFill(name, rate_func = rush_into), run_time = 2)
        self.wait()


        meaning_list = [
            "Anzahl der\\\\ Erfolge", 
            "Anzahl, die zu\\\\ $k$ Erfolgen führen", 
            "Wkt. für \\\\ Erfolge", 
            "Wkt. für \\\\ Misserfolge"
        ]
        targets = [formula[2:5], formula[7:11], formula[12:14], formula[15:]]
        meanings = VGroup(*[Tex(mean) for mean in meaning_list])
        for tex, target, dir in zip(meanings, targets, [UP, DOWN, UP, DOWN]):
            tex.next_to(target, dir, buff = 0.75)

        target_rects = VGroup(*[
            DashedVMobject(SurroundingRectangle(obj, color = BLUE_E), num_dashes=50)
            for obj in targets
        ])

        self.play(
            LaggedStartMap(FadeIn, meanings, lag_ratio = 0.25, rate_func = there_and_back_with_pause),
            LaggedStartMap(Create, target_rects, lag_ratio = 0.25),
            run_time = 6
        )
        self.wait()


        www = VGroup(*[Tex(word, font_size = 72) for word in ["Wann?", "Wie?", "Warum?"]])
        www.arrange(RIGHT, buff = 1)
        www.to_edge(UP, buff = 0.75)
        self.play(
            AnimationGroup(
                *[ReplacementTransform(rect, word) for rect, word in zip(target_rects[1:], www)], 
                lag_ratio = 0.2
            ),
            run_time = 4
        )
        self.wait()


        www.generate_target()
        www.target.arrange(RIGHT, buff = 2).scale(0.6).to_edge(UP, buff = 0.25)
    
        formula.save_state()
        formula.generate_target()
        formula.target.scale(0.5).to_edge(DOWN, buff = 0.25)
    
        xek = formula[2:5].copy()
        self.add(xek)
        self.play(
            MoveToTarget(www),
            MoveToTarget(formula), 
            FadeOut(name, shift = 3*DOWN), 
            run_time = 2
        )

        self.formula, self.xek, self.dash_rect = formula, xek, target_rects[0]

    def explain_xek(self):
        xeks = VGroup(*[MathTex("X", "=", str(k)) for k in [0,1,2,3,4,5]])
        for tex in xeks:
            tex.scale(1.5)
            tex[-1].set_color(GREEN_A)
        xeks.arrange(DOWN)
        xeks[:2].next_to(self.xek, UP, buff = 0.35, aligned_edge=LEFT)
        xeks[2:].next_to(self.xek, DOWN, buff = 0.35, aligned_edge=LEFT)

        boxes = VGroup(*[get_row_of_boxes(height = 0.3, n = 4) for x in range(10)])
        boxes.arrange(DOWN)
        boxes.shift(3.5*RIGHT)

        correct =      [1, 2, 2, 0, 3, 3, 1, 2, 0, 0]
        cross_places = [0, 2, 3, 1, 2, 3, 1, 0, 2, 3]
        bools = [False] + [True] + 3*[False] + 2*[True] + 3*[False]

        cross = Cross(boxes[0][0], stroke_color = YELLOW_D, stroke_width = 3)
        crosses = VGroup(*[cross.copy() for x in range(10)])
        cac = get_checks_and_crosses(bools)

        for mark, row in zip(cac, boxes):
            mark.match_height(row)
            mark.next_to(row, RIGHT, buff = 0.35)

        for row, i_correct, cross, i_place in zip(boxes, correct, crosses, cross_places):
            row[i_correct].generate_target()
            row[i_correct].target.set_fill(C_COLOR, 0.4)
            cross.move_to(row[i_place])

        self.play(LaggedStartMap(FadeIn, xeks, shift = RIGHT, lag_ratio = 0.1), run_time = 2.5)
        self.wait()
        self.play(FadeIn(boxes, lag_ratio = 0.1), run_time = 2)
        self.play(FadeIn(crosses, lag_ratio = 0.1), run_time = 2)
        self.play(
            AnimationGroup(
                *[MoveToTarget(row[i_correct]) for row, i_correct in zip(boxes, correct)], 
                lag_ratio = 0.1
            ), 
            run_time = 2
        )
        self.bring_to_front(crosses)
        self.wait()

        self.play(FadeIn(cac, shift = LEFT, lag_ratio = 0.1), run_time = 3)
        self.wait()

        num_of_succ = Tex("\\#", CMARK_TEX, " = ", "3", tex_template = myTemplate)
        num_of_succ.scale(1.5)
        num_of_succ.next_to(xeks[3], RIGHT, buff = 1)
        num_of_succ[:2].set_color(C_COLOR)
        self.play(self.dash_rect.animate.move_to(xeks[3]), run_time = 2)
        self.play(Write(num_of_succ))
        self.wait(2)


        self.boxes, self.crosses = boxes, crosses
        self.test_group = VGroup(boxes, crosses, cac)

        self.play(
            FadeOut(self.dash_rect), 
            FadeOut(num_of_succ),
            FadeOut(xeks),
            FadeOut(self.xek), 
            run_time = 3
        )

    def bernoulli_trail(self):
        first_row = get_row_of_boxes(height = 0.75)
        first_row[1].set_fill(C_COLOR, 0.4)
        first_row.move_to(2.25*LEFT + UP)
        cross = Cross(first_row[1], stroke_color = YELLOW_D, stroke_width = 3)

        bern_trail = Tex("Bernoulli", "$-$", "Kette", "?", font_size = 60)
        bern_trail.next_to(first_row, UP)

        self.play(Write(bern_trail))
        self.wait()


        self.play(FadeIn(first_row, shift = 0.25 * RIGHT, lag_ratio = 0.1), run_time = 1.5)
        self.play(GrowFromCenter(cross), run_time = 1.5)
        self.wait()

        self.play(cross.animate.move_to(first_row[0]), run_time = 1.5)
        cmark = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        xmark = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
        for mark, box in zip([xmark, cmark], first_row[:2]):
            mark.match_width(first_row[0])
            mark.next_to(box, DOWN)

        self.play(FadeIn(VGroup(cmark, xmark), shift = 0.5*UP, lag_ratio = 0.2), run_time = 2)
        self.wait(2)


        self.play(
            AnimationGroup(
                TransformFromCopy(first_row, self.boxes[0]), 
                TransformFromCopy(cross, self.crosses[0]),
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait()


        arrow_kwargs = {"color": PINK, "stroke_width": 2.5, "tip_length": 0.2}
        arrows = VGroup(*[CurvedArrow(self.boxes[k].get_left(), self.boxes[k+1].get_left(), **arrow_kwargs) for k in range(9)])
        arrows.shift(0.15*LEFT)

        braces = VGroup(*[Brace(self.boxes[:k], LEFT, buff = 0.75) for k in range(10)])
        braces_nums = VGroup(*[MathTex(str(k)).next_to(brace, LEFT) for k, brace in zip(range(10), braces)])

        for k in range(len(self.boxes) - 1):
            if k < 9:
                added_anims = [Create(arrows[k])]
            else:
                added_anims = []
            self.play(
                *added_anims,
                GrowFromCenter(self.crosses[k]), 
                ReplacementTransform(braces[k], braces[k + 1]),
                ReplacementTransform(braces_nums[k], braces_nums[k + 1]),
                run_time = 0.5
            )
            self.wait(0.1)
        final_brace = Brace(self.boxes, LEFT, buff = 0.75)
        final_number = MathTex("10").next_to(final_brace, LEFT)
        self.play(
            ReplacementTransform(braces[-1], final_brace), 
            ReplacementTransform(braces_nums[-1], final_number), 
            run_time = 0.5
        )
        self.wait(2)


        length = MathTex("n", "=", "10")
        prob = MathTex("p", "=", "0{,}25")
        prob[0].set_color(YELLOW_D)

        for mob in length, prob:
            mob.next_to(cmark, DOWN, buff = 0.75)
            mob.align_to(bern_trail, LEFT)
        prob.shift(0.75*DOWN)

        self.play(FadeIn(length, shift = LEFT), run_time = 3)
        self.wait()
        self.play(FadeIn(prob, shift = LEFT), run_time = 3)
        self.wait()

        sur_rects = VGroup(*[SurroundingRectangle(mob, color = BLUE_E) for mob in [VGroup(bern_trail, prob), self.formula]])
        self.play(Create(sur_rects[0]), run_time = 5)
        self.wait(0.5)
        self.play(ReplacementTransform(sur_rects[0], sur_rects[1]), run_time = 3)
        self.wait(3)


class ConnectToBinomTree(MovingCameraScene):
    def construct(self):

        self.setup_old_scene()
        self.binom_tree()
        self.pfad_probability(pfad_nums = [1, 4, 11, 24])
        self.calc_probability1()
        self.pfad_probability(pfad_nums = [0, 3, 8, 18])
        self.calc_probability2()
        self.bring_back_formula()

    def setup_old_scene(self):
        formula = get_general_bin_formula()
        formula.scale(0.75)
        formula.to_corner(DL)
        formula.save_state()
        formula.center().to_edge(DOWN, buff = 0.25)
        rect = SurroundingRectangle(formula, color = BLUE_E)

        www = VGroup(*[Tex(word, font_size = 72) for word in ["Wann?", "Wie?", "Warum?"]])
        www.arrange(RIGHT, buff = 2)
        www.scale(0.6).to_edge(UP, buff = 0.25)


        self.add(formula, rect, www)
        self.wait(2)


        formula.generate_target()
        formula.target.scale(4/3 * 1.5).center()
        rect.generate_target()
        rect.target.set(width = formula.target.width + 3).set(height = formula.target.height + 0.2).center()

        self.play(
            MoveToTarget(formula),
            MoveToTarget(rect, rate_func = rush_into),
            run_time = 3
        )
        self.play(
            FadeOut(rect, scale = 4, run_time = 1), 
            FadeOut(www[0], shift = UP, run_time = 1.5),
        )
        self.wait(0.5)

        self.play(formula[12:].animate.shift(UP), run_time = 1.5)
        self.play(FadeOut(www[1], shift = UP))
        self.wait()

        self.play(
            formula[7:11].animate(rate_func = there_and_back_with_pause).shift(DOWN),
            FadeOut(www[2], shift = UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
            formula[12:].animate(rate_func = squish_rate_func(smooth, 0.5, 1)).shift(DOWN),
            run_time = 4
        )
        self.wait()
        self.play(Restore(formula), run_time = 1.5)

        self.formula = formula

    def binom_tree(self):
        boxes = VGroup(*[get_row_of_boxes(height = 0.5, n = 4) for x in range(10)])
        boxes.arrange(DOWN)
        boxes.to_corner(UR)
        boxes.shift(0.75*LEFT)

        correct =      [1, 2, 2, 0, 3, 3, 1, 2, 0, 0]
        cross_places = [0, 2, 3, 1, 2, 3, 1, 0, 2, 3]

        cross = Cross(boxes[0][0], stroke_color = YELLOW_D, stroke_width = 3)
        crosses = VGroup(*[cross.copy() for x in range(10)])

        bools = [False] + [True] + 3*[False] + 2*[True] + 3*[False]
        cac = get_checks_and_crosses(bools)
        for mark, row in zip(cac, boxes):
            mark.match_height(row)
            mark.next_to(row, RIGHT, buff = 0.35)

        for row, true_place, cross, cross_place in zip(boxes, correct, crosses, cross_places):
            row[true_place].generate_target()
            row[true_place].target.set_fill(C_COLOR, 0.4)
            cross.move_to(row[cross_place])

        self.play(LaggedStartMap(FadeIn, boxes, lag_ratio = 0.1), run_time = 3)
        self.wait()
        self.play(LaggedStartMap(GrowFromCenter, crosses, lag_ratio = 0.05), run_time = 3)
        self.wait()


        # build the tree
        tree_config = {"width": 6, "height": 6, "num_events": 4}
        tree = BinomTree(**tree_config)
        tree.shift(2*LEFT + 0.5*UP)

        #tree_nums = tree.get_pfad_nums()
        #self.add(tree_nums)

        path_indis = [0, 3, 8, 18]
        added_anims = [FocusOn(tree.lines[0], rate_func = squish_rate_func(smooth, 0.5, 1), run_time = 3)]
        for k in range(4):

            self.play(
                MoveToTarget(boxes[k][correct[k]]), 
                *added_anims
            )
            self.wait()

            added_anims = []                                # make sure not to Focus On line every time

            path_indi = path_indis[k]
            line = tree.lines[path_indi]
            self.play(Create(line), run_time = 1.5)

            cx_mark = tree.cx_marks[path_indi]
            self.play(GrowFromCenter(cx_mark), run_time = 1.5)
            self.wait()
        self.wait(2)


        # swap decisions
        new_cross_places = [1, 0, 2, 3, 1, 0, 2, 1, 3, 1]
        for cross, row, c_place in zip(crosses, boxes, new_cross_places):
            cross.generate_target()
            cross.target.move_to(row[c_place])

        self.play(LaggedStartMap(MoveToTarget, crosses, path_arc = np.pi/3, lag_ratio = 0.1), run_time = 5)
        self.wait()

        path_indis = [1,4,11,24]
        for k in range(4):
            self.play(Circumscribe(boxes[k][correct[k]], time_width = 0.75, fade_out = True, color = PINK))

            path_indi = path_indis[k]
            line = tree.lines[path_indi]
            self.play(Create(line), run_time = 1.5)

            cx_mark = tree.cx_marks[path_indi]
            self.play(GrowFromCenter(cx_mark), run_time = 1.5)
            self.wait()
        self.wait(2)

        tree_copy = tree.copy()
        self.play(FadeIn(tree_copy, lag_ratio = 0.1), run_time = 3)
        self.add(tree)
        self.remove(tree_copy)
        self.wait(3)

        # show big tree just to remove it afterwards
        big_tree = BinomTree(width = tree.width * 2.57, height = tree.height * 1.02, num_events = 10)
        big_tree.next_to(tree.get_left(), RIGHT, buff = 0)

        frame = self.camera.frame
        frame.save_state()

        self.play(
            FadeIn(big_tree.lines[30:], lag_ratio = 0.01), 
            frame.animate.set(width = big_tree.width + 2).move_to(big_tree.get_center()),
            run_time = 4
        )
        self.wait()

        self.play(
            Restore(frame), 
            FadeOut(big_tree.lines[30:], lag_ratio = 0.01), 
            run_time = 4
        )
        self.wait()


        # get rid of boxes[4:]
        top_boxes = VGroup(boxes[:4], crosses[:4]).copy()
        top_boxes.generate_target()
        top_boxes.target.scale(0.6).to_corner(UL, buff = 0.2)
        self.remove(*boxes[:4], *crosses[:4])
        self.add(top_boxes)
        self.play(
            LaggedStartMap(FadeOut, boxes[4:], shift = 3*RIGHT, lag_ratio = 0.1),
            LaggedStartMap(FadeOut, crosses[4:], shift = 3*RIGHT, lag_ratio = 0.1),
            MoveToTarget(top_boxes, path_arc = np.pi),
            run_time = 3
        )
        self.wait()


        self.boxes, self.tree = top_boxes, tree

    def pfad_probability(self, pfad_nums):
        tree, boxes = self.tree, self.boxes

        # pfad_nums = [1,4,11,24]
        moving_dot = Dot(point = tree.lines[0].get_start()).set_fill(opacity = 0)
        pfad = tree.get_pfad(pfad_nums)
        trace = TracedPath(moving_dot.get_center, dissipating_time=0.75, stroke_opacity=[0, 1, 0], stroke_color = YELLOW_D, stroke_width = 8)


        self.add(trace)
        self.play(MoveAlongPath(moving_dot, pfad, run_time = 3))
        self.remove(trace)
        self.wait()

        tree_probs = tree.get_pfad_prob(texp = "0.25", texq = "0.75", use_prob_values=True)
        pfad_probs = [tree_probs[k] for k in pfad_nums]

        for k, num in enumerate(pfad_nums):
            self.play(
                FadeToColor(tree.lines[num], color = YELLOW_D),
                FadeIn(pfad_probs[k], scale = 0.5),
            )
            self.wait(0.5)
        self.wait()

    def calc_probability1(self):
        tree = self.tree

        calc = MathTex("0{,}25", "\\cdot", "0{,}75", "\\cdot", "0{,}25", "\\cdot", "0{,}75")\
            .next_to(tree.lines[24], RIGHT, buff = 0.75)

        self.play(ShowIncreasingSubsets(calc), run_time = 3)
        self.wait()

        calc2 = MathTex("0{,}25^", "2", "\\cdot", "0{,}75^", "2")\
            .move_to(calc, aligned_edge=DOWN)

        self.play(TransformMatchingTex(calc, calc2))
        self.wait(0.5)
        self.play(Circumscribe(calc2, color = YELLOW_D, time_width = 0.75, fade_out = True, run_time = 3))
        self.wait()

        self.result1 = calc2

    def calc_probability2(self):
        tree = self.tree
        calc = MathTex("0{,}75", "\\cdot", "0{,}25", "\\cdot", "0{,}75", "\\cdot", "0{,}75")\
            .next_to(tree.lines[18], RIGHT, buff = 0.75)

        self.play(ShowIncreasingSubsets(calc), run_time = 3)
        self.wait()

        calc2 = MathTex("0{,}25^", "1", "\\cdot", "0{,}75^", "3")\
            .move_to(calc, aligned_edge=DOWN)

        self.play(TransformMatchingTex(calc, calc2))
        self.wait(0.5)
        self.play(Circumscribe(calc2, color = YELLOW_D, time_width = 0.75, fade_out = True, run_time = 3))
        self.wait(2)

        self.result2 = calc2

    def bring_back_formula(self):
        formula, result1, result2 = self.formula, self.result1, self.result2

        formula.add_background_rectangle(buff = 0.25, opacity = 0.85)
        self.bring_to_front(formula)

        dest = result2.get_part_by_tex("\\cdot").get_center() + 2*DOWN
        self.play(
            formula.animate.scale(4/3 * 1.25, about_point = formula[15].get_center()).shift(dest - formula[15].get_center()), 
            run_time = 3
        )
        self.wait()


        cac1 = get_checks_and_crosses([True, False, True, False], width = result1.width)
        cac1.next_to(result1, UP)

        cac2 = get_checks_and_crosses([False, True, False, False], width = result2.width)
        cac2.next_to(result2, UP)




        # transform c_marks, x_marks into exponents first example
        self.play(FadeIn(cac1, shift = DOWN, lag_ratio = 0.1), run_time = 3)
        self.wait()

        self.play(
            FadeToColor(result1[0], YELLOW_D),
            FadeToColor(result1[1], C_COLOR), 
            AnimationGroup(
                *[FadeOut(check, target_position = result1[1], path_arc = np.pi/3) for check in cac1 if check.positive],
                lag_ratio = 0.2
            ), 
            run_time = 3
        )
        self.wait(0.5)


        self.play(
            FadeToColor(result1[4], X_COLOR), 
            AnimationGroup(
                *[FadeOut(check, target_position = result1[4], path_arc = -np.pi/3) for check in cac1 if not check.positive],
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()


        # transform c_marks, x_marks into exponents first example
        self.play(FadeIn(cac2, shift = DOWN, lag_ratio = 0.1), run_time = 3)
        self.wait()


        self.play(
            FadeToColor(result2[0], YELLOW_D),
            FadeToColor(result2[1], C_COLOR), 
            AnimationGroup(
                *[FadeOut(check, target_position = result2[1], path_arc = np.pi/3) for check in cac2 if check.positive],
                lag_ratio = 0.2
            ), 
            run_time = 1.5
        )
        self.wait(0.5)

        self.play(
            FadeToColor(result2[4], X_COLOR), 
            AnimationGroup(
                *[FadeOut(check, target_position = result2[4], path_arc = -np.pi/3) for check in cac2 if not check.positive],
                lag_ratio = 0.2
            ),
            run_time = 3
        )
        self.wait()



        # # highlight Exponent for success and failure
        self.play(Circumscribe(formula[14], color = PINK, shape = Circle, time_width = 0.75, run_time = 3))
        self.wait()

        self.play(
            *[
                Circumscribe(expo, color = PINK, shape = Circle, fade_in = True ,time_width = 0.75, run_time = 3) 
                for expo in [result1[1], result2[1]]
            ],
        )
        self.wait()


        self.play(Circumscribe(formula[-1], color = PINK, shape = Circle, time_width = 0.75, fade_out = True, run_time = 3))
        self.wait()
        self.play(
            *[
                Circumscribe(expo, color = PINK, shape = Circle, time_width = 0.75, run_time = 3) 
                for expo in [result1[4], result2[4], formula[-1]]
            ],
        )
        self.wait()


        # Fadeout result2 + this is not P(X=2)
        self.play(FadeOut(result2, shift = 2*RIGHT), run_time = 2)
        self.wait()

        not_equal = MathTex("\\neq", color = RED)\
            .scale(1.25)\
            .next_to(result1, DOWN)

        text = MathTex("P", "(", "X", "=", "2", ")")\
            .scale(1.25)\
            .next_to(not_equal, DOWN)

        self.play(Write(not_equal))
        self.play(Write(text))
        self.wait(2)


        self.play(Circumscribe(formula[8:12], color = PINK, fade_out = True, run_time = 3))
        self.wait(3)


class NChooseK(MovingCameraScene):
    def construct(self):
        tree_config = {"width": 6, "height": 6, "num_events": 4}
        tree = self.tree = BinomTree(**tree_config)
        tree.shift(2*LEFT + 0.5*UP)


        self.choose_2_out_of_4()
        self.choose_1_out_of_4()
        self.how_many_are_there()


    def choose_2_out_of_4(self):
        tree = self.tree

        pfad_lists = [[1, 5, 12, 26], [1, 4, 11, 24], [1, 4, 10, 23], [0, 3, 9, 20], [0, 3, 8, 19], [0, 2, 7, 17]]
        two_pfads = VGroup(*[tree.get_pfad(numbers) for numbers in pfad_lists])
        self.add(two_pfads)
        self.add(tree.circles, tree.cx_marks)

        cx_remove = self.get_remove_pfad_nums_list(pfad_lists)
        self.remove(*[tree.cx_marks[k] for k in cx_remove])
        self.wait(2)


        # Moving Camera to tree 
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(height = tree.height).move_to(tree).shift(1.75*RIGHT), 
            run_time = 2
        )
        self.wait()


        # Add checks and crosses according to tree
        bool_lists = self.get_bool_lists(4, 2)
        cac_group = self.get_orientated_cac_group(bool_lists, two_pfads)

        add_anim = [ShowIncreasingSubsets(cac_group[0], run_time = 3)]
        self.animate_trace_along_path(pfad_lists[0], add_anim)
        self.wait()

        add_anim = [ShowIncreasingSubsets(cac_group[1], run_time = 3)]
        self.animate_trace_along_path(pfad_lists[1], add_anim)
        self.wait()


        for cac in cac_group[2:]:
            self.play(ShowIncreasingSubsets(cac))
        self.wait()

        c_list1 = [0,0,0,1,1,2]             # this is super hacky
        c_list2 = [1,2,3,2,3,3]             # ....
        self.play(
            AnimationGroup(
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, c_list1)], 
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, c_list2)],
                lag_ratio = 0.05
            ),
            run_time = 2
        )
        self.wait()


        brace = Brace(cac_group, RIGHT, color = GREY)
        brace_tex = brace.get_tex(str(choose(4,2)))

        self.play(Create(brace))
        self.play(Write(brace_tex))
        self.wait(2)

        self.clear()

    def choose_1_out_of_4(self):
        tree = self.tree

        pfad_lists = [[1, 4, 10, 22], [0, 3, 8, 18], [0, 2, 7, 16], [0, 2, 6, 15]]
        one_pfads = VGroup(*[tree.get_pfad(numbers) for numbers in pfad_lists])

        self.add(one_pfads)
        self.add(tree.circles, tree.cx_marks)

        cx_remove = self.get_remove_pfad_nums_list(pfad_lists)
        self.remove(*[tree.cx_marks[k] for k in cx_remove])
        self.wait(2)

        # Add checks and crosses according to tree
        bool_lists = self.get_bool_lists(4, 1)
        cac_group = self.get_orientated_cac_group(bool_lists, one_pfads)

        add_anim = [ShowIncreasingSubsets(cac_group[0], run_time = 3)]
        self.animate_trace_along_path(pfad_lists[0], add_anim)
        self.wait()

        add_anim = [ShowIncreasingSubsets(cac_group[1], run_time = 3)]
        self.animate_trace_along_path(pfad_lists[1], add_anim)
        self.wait()

        for cac in cac_group[2:]:
            self.play(ShowIncreasingSubsets(cac))
        self.wait()

        brace = Brace(cac_group, RIGHT, color = GREY)
        brace_tex = brace.get_tex(str(choose(4,1)))

        self.play(Create(brace))
        self.play(Write(brace_tex))
        self.wait(2)


        self.num_of_combs = brace_tex

    def how_many_are_there(self):

        hm = Tex("Wie viele Möglichkeiten?")\
            .align_to(self.num_of_combs, RIGHT)\
            .shift(2.5*UP)

        hm2 = Tex("1 Erfolg auf 4 mögliche Plätze zu verteilen")\
            .set(width = hm.width - 0.75)\
            .next_to(hm, DOWN, buff = 0.1)\
            .set_color(GREY_B)

        arrow = CurvedArrow(self.num_of_combs.get_corner(UR), hm.get_corner(DR), color = YELLOW_D, stroke_width = 3, tip_length = 0.25)
        self.play(Create(arrow), run_time = 1.5)
        self.play(Write(hm))
        self.play(FadeIn(hm2))
        self.wait(3)


    # functions

    def get_remove_pfad_nums_list(self, pfad_lists):
        # Create one list containing all number --> this include duplicates
        combine_pfad_lists = [x for lists in pfad_lists for x in lists]

        # Create target list --> add only those, you are not already in that list
        remove_duplicates = []
        [remove_duplicates.append(x) for x in combine_pfad_lists if x not in remove_duplicates]
        remove_duplicates.sort()

        final_numbers = []
        [final_numbers.append(x) for x in list(range(30)) if x not in remove_duplicates]

        return final_numbers

    def get_bool_lists(self, n, k):
        combs = list(it.combinations(range(n), k))
        bool_lists = [
            [i in comb for i in range(n)]
            for comb in combs
        ]
        return bool_lists

    def get_orientated_cac_group(self, bool_lists, pfads):
        cac_group = VGroup(*[
            get_checks_and_crosses(bool_list, width = 1.5) 
            for bool_list in bool_lists
        ])

        for cac, pfad in zip(cac_group, pfads):
            cac.set(height = self.tree.cx_marks[0].height)          # compare height with first cx_mark
            cac.next_to(pfad.get_end(), RIGHT, buff = 1)            # place cac next to end of pfad line

        return cac_group

    def animate_trace_along_path(self, pfad_list, added_anims = None):
        moving_dot = Dot(point = self.tree.lines[0].get_start()).set_fill(opacity = 0)
        pfad = self.tree.get_pfad(pfad_list)
        trace = TracedPath(moving_dot.get_center, dissipating_time=0.75, stroke_opacity=[0, 1, 0], stroke_color = YELLOW_D, stroke_width = 8)

        if added_anims is None:
            added_anims = []

        self.add(trace)
        self.play(
            MoveAlongPath(moving_dot, pfad, run_time = 3), 
            *added_anims
        )
        self.remove(trace)


class BinomialCoefficient(Scene):
    def construct(self):

        slots = VGroup(*[Line() for x in range(4)])
        for slot in slots:
            slot.set(width = 1)
            slot.set_stroke(width = 3)
            slot.set_color(GREY_B)
        slots.arrange(RIGHT, buff = 1)
        slots.shift(0.5*UP)


        bool_lists = self.get_bool_lists(4, 2)
        cac_group = self.get_orientated_cac_group(bool_lists)

        for cac in cac_group:
            for cx, slot in zip(cac, slots):
                cx.match_width(slot)
                cx.next_to(slot, UP)

        first_row = cac_group[0]

        comb_counter = 1
        comb_dec = Integer(comb_counter)\
            .scale(2.5)\
            .next_to(slots, DOWN, buff = 1.5)\
            .add_updater(lambda dec: dec.set_value(comb_counter))

        self.play(
            Create(slots, lag_ratio = 0.2, run_time = 2), 
            LaggedStartMap(DrawBorderThenFill, first_row, lag_ratio = 0.2, run_time = 3), 
            Write(comb_dec, run_time = 1)
        )
        self.wait()

        for k in range(1, len(cac_group)):
            comb_counter +=1

            new_cac = cac_group[k]
            first_row.become(new_cac)
            self.wait(0.75)
        self.wait()

        equals = MathTex("=", font_size = 96)
        equals.next_to(comb_dec, RIGHT)

        bin_coeff = MathTex("\\left(", "4", "\\over", "2", "\\right)", font_size = 96)
        bin_coeff.remove(bin_coeff.get_part_by_tex("\\over"))
        bin_coeff.next_to(equals, RIGHT)

        bin_tex = Tex("Bi", "nomialkoeffizient", font_size = 72)
        bin_tex[0].set_color(YELLOW_D)
        bin_tex[1].set_color(BLUE_B)
        bin_tex.next_to(bin_coeff, DOWN)

        self.play(FadeIn(equals, shift=LEFT))
        self.play(
            Write(bin_coeff), 
            Write(bin_tex)
        )
        self.wait()

        bin_speech = Tex("Vier\\\\", "über\\\\", "Zwei", font_size = 96)
        bin_speech[1].scale(0.5)
        bin_speech.match_height(bin_coeff)
        bin_speech.next_to(bin_coeff, RIGHT)

        self.play(LaggedStartMap(FadeIn, bin_speech, rate_func = there_and_back_with_pause), run_time = 3)
        self.wait()

        self.play(
            *[mob.animate.shift(5*LEFT) for mob in [comb_dec, equals, bin_coeff]], 
            run_time = 1.5
        )
        self.wait()

        bin_def = MathTex("{" + "n", "!", "\\over", "k", "!", "\\cdot", "(", "n", "-", "k", ")", "!" + "}", font_size = 96)
        bin_def.next_to(bin_coeff, RIGHT, buff = 1)
        bin_def.align_to(bin_tex, ORIGIN)

        bin_def2 = MathTex("{" + "4", "!", "\\over", "2", "!", "\\cdot", "(", "4", "-", "2", ")", "!" + "}", font_size = 96)
        bin_def2.next_to(bin_coeff, RIGHT, buff = 1)
        bin_def2.align_to(bin_tex, ORIGIN)

        self.play(Write(bin_def), run_time = 2)
        self.wait()

        self.play(Transform(bin_def, bin_def2, lag_ratio = 0.2), run_time = 2)
        self.wait(2)

        rect = SurroundingRectangle(comb_dec).set_color([YELLOW_D, BLUE])
        self.play(Create(rect), run_time = 3)
        self.wait(0.5)
        self.play(FadeOut(rect, scale = 4))
        self.wait(3)



    # functions 
    def get_bool_lists(self, n, k):
        combs = list(it.combinations(range(n), k))
        bool_lists = [
            [i in comb for i in range(n)]
            for comb in combs
        ]
        return bool_lists

    def get_orientated_cac_group(self, bool_lists):
        cac_group = VGroup(*[
            get_checks_and_crosses(bool_list, width = 1.5) 
            for bool_list in bool_lists
        ])
        return cac_group


class ShowAllBinCoeffInBinomTree(NChooseK):
    def construct(self):

        self.show_coeffs()
        self.bring_back_2()
        self.add_them_all_up()


    def show_coeffs(self):
        tree_config = {"width": 6, "height": 6, "num_events": 4}
        tree = self.tree = BinomTree(**tree_config)
        tree.shift(2*LEFT + 0.5*UP)

        # tree_nums = tree.get_pfad_nums()
        # self.add(tree, tree_nums)


        self.pfad_lists_0 = [[0, 2, 6, 14]]
        self.pfad_lists_1 = [[1, 4, 10, 22], [0, 3, 8, 18], [0, 2, 7, 16], [0, 2, 6, 15]]
        self.pfad_lists_2 = [[1, 5, 12, 26], [1, 4, 11, 24], [1, 4, 10, 23], [0, 3, 9, 20], [0, 3, 8, 19], [0, 2, 7, 17]]
        self.pfad_lists_3 = [[0, 3, 9, 21], [1, 4, 11, 25], [1, 5, 12, 27], [1, 5, 13, 28]]
        self.pfad_lists_4 = [[1, 5, 13, 29]]

        all_pfad_lists = [lists for lists in [self.pfad_lists_0, self.pfad_lists_1, self.pfad_lists_2, self.pfad_lists_3, self.pfad_lists_4]]

        for x, pfad_lists in enumerate(all_pfad_lists):
            pfade = VGroup(*[tree.get_pfad(numbers) for numbers in pfad_lists])
            cx_remove = self.get_remove_pfad_nums_list(pfad_lists)


            bool_lists = self.get_bool_lists(4, x)
            cac_group = self.get_orientated_cac_group(bool_lists, pfade)
            if x == 4:
                cac_group.scale_to_fit_width(width = 1, about_point = cac_group.get_left())


            brace = Brace(cac_group, RIGHT, color = GREY)
            num_of_pfads = brace.get_tex(str(choose(4, x)))

            equals = MathTex("=").next_to(num_of_pfads, RIGHT)

            bin_coeff = MathTex("\\left(", "4", "\\over", str(x), "\\right)")
            bin_coeff.remove(bin_coeff.get_part_by_tex("\\over"))
            bin_coeff.next_to(equals, RIGHT)

            if x == 0:
                self.play(Create(pfade), run_time = 1.5)
                self.add(tree.circles, tree.cx_marks)
                self.remove(*[tree.cx_marks[k] for k in cx_remove])
                self.play(
                    AnimationGroup(
                        *[ShowIncreasingSubsets(cac) for cac in cac_group], 
                        lag_ratio = 0.2
                    ), 
                    run_time = 2
                )
                self.remove(*[cac for cac in cac_group])
                self.add(cac_group)
                self.play(
                    Create(brace), 
                    Write(num_of_pfads), 
                    FadeIn(equals, shift = UP),
                    FadeIn(bin_coeff, shift = LEFT), 
                    run_time = 2
                )
            else:
                self.add(pfade, tree.circles, tree.cx_marks)
                self.remove(*[tree.cx_marks[k] for k in cx_remove])
                self.add(cac_group, brace, num_of_pfads, equals, bin_coeff)
            self.wait(2)


            self.remove(pfade, tree.circles, tree.cx_marks, cac_group, brace, num_of_pfads, equals, bin_coeff)
        self.clear()



        # # Moving Camera to tree 
        # self.camera.frame.save_state()
        # self.play(
        #     self.camera.frame.animate.set(height = tree.height).move_to(tree).shift(1.75*RIGHT), 
        #     run_time = 2
        # )
        # self.wait()


        # # Add checks and crosses according to tree
        # 

    def bring_back_2(self):
        tree = self.tree

        pfade = VGroup(*[tree.get_pfad(numbers) for numbers in self.pfad_lists_2])
        cx_remove = self.get_remove_pfad_nums_list(self.pfad_lists_2)

        bool_lists = self.get_bool_lists(4, 2)
        cac_group = self.get_orientated_cac_group(bool_lists, pfade)

        brace = Brace(cac_group, RIGHT, color = GREY)
        num_of_pfads = brace.get_tex(str(choose(4, 2)))

        equals = MathTex("=").next_to(num_of_pfads, RIGHT)

        bin_coeff = MathTex("\\left(", "4", "\\over", "2", "\\right)")
        bin_coeff.remove(bin_coeff.get_part_by_tex("\\over"))
        bin_coeff.next_to(equals, RIGHT)


        self.add(pfade, tree.circles, tree.cx_marks)
        self.remove(*[tree.cx_marks[k] for k in cx_remove])
        self.add(cac_group, brace, num_of_pfads, equals, bin_coeff)

        bin_tex1 = Tex("Binomialkoeffizient")\
            .set(width = bin_coeff.width * 3.5)\
            .next_to(bin_coeff, UP, buff = 0.5)\
            .set_color(BLUE_D)
        bin_tex2 = Tex("Anzahl der Pfade, die\\\\", "zu $k$ Erfolgen führen")\
            .set(width = bin_tex1.width)\
            .next_to(bin_tex1, UP)\
            .set_color(GREY)

        self.add(bin_tex1, bin_tex2)

        self.wait(2)



        moving_dots = VGroup(*[Dot(point = self.tree.lines[0].get_start()).set_fill(opacity = 0) for x in range(choose(4, 2))])
        traces = VGroup(*[
            TracedPath(dot.get_center, dissipating_time=0.75, stroke_opacity=[0, 1, 0], stroke_color = YELLOW_D, stroke_width = 8)
            for dot in moving_dots
        ])

        self.add(traces)
        self.play(
            AnimationGroup(
                *[MoveAlongPath(dot, pfad, run_time = 5) for dot, pfad in zip(moving_dots, pfade)], 
                lag_ratio = 0.1
            ), 
            run_time = 5
        )
        self.remove(traces)
        self.wait(2)


        self.cac_group, self.coeff = cac_group, num_of_pfads

    def add_them_all_up(self):
        bg = Rectangle(width = self.tree.width + 0.5, height = self.tree.height + 0.5)
        bg.set_stroke(width = 0)
        bg.set_fill(BLACK, 0.8)
        bg.move_to(self.tree)

        cac_group = self.cac_group.copy()
        cac_group.generate_target()
        cac_group.target.scale(1.5).arrange(DOWN, buff = 0.5).move_to(bg.get_center())

        prob = MathTex("P", "(", "X", "=", "2", ")")
        prob.set_color_by_tex_to_color_map({"2": C_COLOR})
        prob.next_to(cac_group.target, LEFT, buff = 1.5, aligned_edge = UP)
        prob.shift(0.05*UP)

        self.play(
            FadeIn(bg),
            Create(prob, rate_func = squish_rate_func(smooth, 0.5, 1)),
        )
        self.wait(0.25)

        self.play(MoveToTarget(cac_group, lag_ratio = 0.2), run_time = 3)


        ps = VGroup()
        left_braces = VGroup()
        right_braces = VGroup()
        pluses = VGroup()

        for cac in cac_group:
            left_brace = MathTex("(")\
                .set(height = cac.height + 0.1)\
                .next_to(cac, LEFT, buff = 0.1)
            right_brace = MathTex(")")\
                .set(height = cac.height + 0.1)\
                .next_to(cac, RIGHT, buff = 0.1)
            p = MathTex("P")\
                .match_height(cac)\
                .next_to(left_brace, LEFT, buff = 0.1)
            plus = MathTex("+")\
                .next_to(p, LEFT)\
                .set_color(BLUE_D)

            ps.add(p)
            left_braces.add(left_brace)
            right_braces.add(right_brace)
            pluses.add(plus)


        self.play(
            LaggedStartMap(FadeIn, right_braces, shift = LEFT, lag_ratio = 0.1),
            LaggedStartMap(FadeIn, left_braces, shift = RIGHT, lag_ratio = 0.1),
            LaggedStartMap(FadeIn, ps, shift = RIGHT, lag_ratio = 0.1),
            run_time = 1.5
        )

        equals = MathTex("=").move_to(pluses[0])
        pluses[0] = equals

        self.play(
            LaggedStartMap(FadeIn, pluses, scale = 0.2, lag_ratio = 0.1),
            run_time = 1.5
        )
        self.wait(2)


        line = Line(stroke_width = 3, color = GREY)
        line.set(width = VGroup(pluses, right_braces).height + 0.5)
        line.next_to(VGroup(pluses, right_braces), DOWN, buff = 0.2)
        self.play(Create(line))


        coeff = self.coeff.copy()
        coeff.generate_target()
        coeff.target.scale(1.25).next_to(pluses, DOWN, buff = 0.7).set_color(BLUE_D)


        rest = MathTex("\\cdot \\", "0.25^", "2", "\\cdot", "0.75^", "2")
        rest.scale(1.25)
        rest[-1].set_color(X_COLOR)
        rest[2].set_color(C_COLOR)
        rest[1].set_color(YELLOW_D)
        rest.next_to(coeff.target, RIGHT, aligned_edge = DOWN)

        self.play(Write(rest[:3]))
        c_list1 = [0,0,0,1,1,2]             # this is super hacky
        c_list2 = [1,2,3,2,3,3]             # ....
        self.play(
            AnimationGroup(
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, c_list1)], 
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, c_list2)],
                lag_ratio = 0.05
            ),
            run_time = 2
        )
        self.wait()

        self.play(Write(rest[3:]))
        x_list1 = [2,1,1,0,0,0]
        x_list2 = [3,3,2,3,2,1]
        self.play(
            AnimationGroup(
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, x_list1)],
                *[row[k].animate(rate_func = there_and_back).shift(0.2*UP) for row, k in zip(cac_group, x_list2)],
                lag_ratio = 0.05
            ),
            run_time = 2
        )
        self.wait(2)


        self.play(MoveToTarget(coeff, path_arc = -np.pi/4), run_time = 3)
        rect = SurroundingRectangle(VGroup(coeff, rest)).set_color([BLUE_D, RED, GREEN, YELLOW_D])
        self.play(Create(rect), run_time = 3)
        self.wait(0.25)
        self.play(FadeOut(rect, scale = 4))
        self.wait(3)


class CalculateProbability(Scene):
    def construct(self):

        self.setup_scene()
        self.prob_2_out_of_4()
        self.prob_1_out_of_4()
        self.prob_8_out_of_10()


    def setup_scene(self):
        # title = Tex("Wahrscheinlichkeit für ", "2", " Erfolge bei 4 Wiederholungen")
        # title.set(width = config["frame_width"] - 3)
        # title.set_color_by_gradient(YELLOW_D, BLUE_B, LIGHT_GREY, BLUE_B, YELLOW_D)
        # title.to_edge(UP)

        # uline = Line(color = DARK_GREY, stroke_width = 2)
        # uline.set_length(config["frame_width"])
        # uline.next_to(title, DOWN, buff = 0.1)

        # self.add(title, uline)

        formula_gen = MathTex(
            "P", "(", "X", "=", "k", ")", "=",
            "\\left(", "{" + "n", "\\over", "k" + "}", "\\right)", "\\cdot", 
            "p^", "k", "\\cdot", 
            "(", "1", "-", "p", ")^", "{" + "n-k" + "}"
        )
        formula_gen.scale(1.5)
        formula_gen.move_to(1.25*UP + 0.5*LEFT)
        formula_gen.remove(formula_gen.get_part_by_tex("\\over"))
        formula_gen.set_color_by_tex_to_color_map({"p": YELLOW_D, "k": C_COLOR, "n-k": X_COLOR})


        meaning_list = [
            "Anzahl der\\\\ Erfolge", 
            "Anzahl der Pfade, die\\\\ zu $k$ Erfolgen führen", 
            "Wkt. für \\\\ Erfolge", 
            "Wkt. für \\\\ Misserfolge"
        ]
        targets = [formula_gen[2:5], formula_gen[7:11], formula_gen[12:14], formula_gen[15:]]
        meanings = VGroup(*[Tex(mean) for mean in meaning_list])
        for tex, target, dir in zip(meanings, targets, [UP, DOWN, UP, DOWN]):
            tex.next_to(target, dir, buff = 0.75)

        target_rects = VGroup(*[
            DashedVMobject(SurroundingRectangle(obj, color = BLUE_E), num_dashes=50)
            for obj in targets
        ])

        self.play(
            LaggedStartMap(FadeIn, meanings, lag_ratio = 0.25),
            LaggedStartMap(Create, target_rects, lag_ratio = 0.25),
            run_time = 4
        )
        self.wait()
        self.play(
            FadeIn(formula_gen, lag_ratio = 0.1), run_time = 3 
        )
        self.wait()

        target_positions = [
            formula_gen[2:5].get_center() + 1.5*UP, 
            formula_gen[7:11].get_center() + 1.5*UP + 0.5*LEFT, 
            formula_gen[12:14].get_center() + 1.5*UP + 0.25*DOWN, 
            formula_gen[15:].get_center() + 1.5*UP + 0.25*DOWN
        ]

        for meaning, pos in zip(meanings, target_positions):
            meaning.generate_target()
            meaning.target.scale(0.5).move_to(pos)
        
        self.play(LaggedStartMap(MoveToTarget, meanings, lag_ratio = 0.2), run_time = 1.5)
        self.wait()


        self.formula_gen = formula_gen

    def prob_2_out_of_4(self):
        formula_gen = self.formula_gen

        n, p, k = 4, 0.25, 2

        formula = get_binom_formula(n, p, k)
        formula.scale(1.5)
        formula.next_to(formula_gen, DOWN, buff = 1)

        formula[:6].align_to(formula_gen[:6], RIGHT)
        formula[6:].align_to(formula_gen[6:], LEFT)

        self.play(Write(formula[:6]))
        self.wait(0.5)
        self.play(FadeIn(formula[6:11]))
        self.wait()

        self.play(Write(formula[11:14]))
        self.wait()
        self.play(Write(formula[14:]))
        self.wait(2)

        approx = MathTex("\\approx")\
            .scale(1.5)\
            .to_edge(DOWN, buff = 1)\
            .shift(1.5*RIGHT)

        result_num = get_binom_result(n, p, k)
        result = MathTex(str(result_num)).scale(1.5).next_to(approx, RIGHT)

        self.play(FadeIn(approx, shift = LEFT))
        self.play(Write(result))
        rect = SurroundingRectangle(VGroup(approx, result)).set_color([YELLOW_D, GREEN, RED])
        self.play(Create(rect), run_time = 3)
        self.play(FadeOut(rect, scale = 4))
        self.wait(3)


        self.formula, self.result = formula, result

    def prob_1_out_of_4(self):
        formula_gen = self.formula_gen

        n, p, k = 4, 0.25, 1

        formula = get_binom_formula(n, p, k)
        formula.scale(1.5)
        formula.next_to(formula_gen, DOWN, buff = 1)

        formula[:6].align_to(formula_gen[:6], RIGHT)
        formula[6:].align_to(formula_gen[6:], LEFT)

        self.play(FadeTransform(self.formula, formula, lag_ratio = 0.2), run_time = 2)
        self.wait()

        self.play(Flash(self.formula[-2], color = RED, flash_radius = 0.2))
        self.wait()

        approx = MathTex("\\approx")\
            .scale(1.5)\
            .to_edge(DOWN, buff = 1)\
            .shift(1.5*RIGHT)

        result_num = get_binom_result(n, p, k)
        result = MathTex(str(result_num)).scale(1.5).next_to(approx, RIGHT)

        self.play(Transform(self.result, result, lag_ratio = 0.1))
        rect = SurroundingRectangle(VGroup(approx, result)).set_color([YELLOW_D, GREEN, RED])
        self.play(Create(rect), run_time = 3)
        self.play(FadeOut(rect, scale = 4))
        self.wait(3)


        self.old_formula = formula

    def prob_8_out_of_10(self):
        formula_gen = self.formula_gen

        n, p, k = 10, 0.25, 8

        formula = get_binom_formula(n, p, k)
        formula.scale(1.5)
        formula.next_to(formula_gen, DOWN, buff = 1)

        formula[:6].align_to(formula_gen[:6], RIGHT)
        formula[6:].align_to(formula_gen[6:], LEFT)

        self.remove(self.old_formula)
        self.wait()


        self.play(Write(formula[:6]))
        self.wait(0.5)
        self.play(FadeIn(formula[6:11]))
        self.wait()

        self.play(Write(formula[11:14]))
        self.wait()
        self.play(Write(formula[14:]))
        self.wait(2)

        self.play(Flash(formula[-1], color = RED, flash_radius = 0.2))
        self.wait()

        approx = MathTex("\\approx")\
            .scale(1.5)\
            .to_edge(DOWN, buff = 1)\
            .shift(1.5*RIGHT)

        result_num = get_binom_result(n, p, k)
        result = MathTex(str(result_num)).scale(1.5).next_to(approx, RIGHT)

        self.play(Transform(self.result, result))
        rect = SurroundingRectangle(VGroup(approx, result)).set_color([YELLOW_D, GREEN, RED])
        self.play(Create(rect), run_time = 3)
        self.play(FadeOut(rect, scale = 4))
        self.wait(3)


class DealingWithMoreThen8(Scene):
    def construct(self):
        title1 = Tex("Einzelwahrscheinlichkeit", font_size = 72, color = GREY_B)
        title1.move_to(2*LEFT + 3*UP)

        eq1 = MathTex("P", "(", "X", "=", "8", ")", "=", "\\ldots", font_size = 72)
        eq1.next_to(title1, DOWN, buff = 0.5, aligned_edge=LEFT)
        eq1.shift(0.5*RIGHT)

        title2 = Tex("??? Wahrscheinlichkeit", font_size = 72, color = GREY_B)
        title2.move_to(2*LEFT + 0.5*DOWN)
        title2.align_to(title1, LEFT)

        eq2 = MathTex("P", "(", "X", ">", "8", ")", "=", "\\ldots", font_size = 72)
        eq2.next_to(title2, DOWN, buff = 0.5, aligned_edge=LEFT)
        eq2.shift(0.5*RIGHT)

        exp1 = Tex("genau ", "8", font_size = 60)\
            .next_to(eq1, DOWN, buff = 0.5, aligned_edge=LEFT)\
            .shift(3*RIGHT)

        exp2 = Tex("mehr als ", "8", font_size = 60)\
            .next_to(eq2, DOWN, buff = 0.5, aligned_edge=LEFT)\
            .shift(3*RIGHT)

        for eq in eq1, eq2:
            eq[3].set_color(MAROON)
            eq[4].set_color(C_COLOR)

        for exp in exp1, exp2:
            exp[0].set_color(MAROON)
            exp[1].set_color(C_COLOR)

        arrow1 = CurvedArrow(exp1.get_left() + 0.15*LEFT, eq1[3].get_bottom() + 0.15*DOWN, angle=-TAU / 4, tip_length = 0.25)
        arrow2 = CurvedArrow(exp2.get_left() + 0.15*LEFT, eq2[3].get_bottom() + 0.15*DOWN, angle=-TAU / 4, tip_length = 0.25)


        self.add(title1, eq1, eq2)
        self.wait()

        self.play(Create(arrow1))
        self.play(Write(exp1))
        self.wait()


        self.play(Create(arrow2))
        self.play(Write(exp2))
        self.wait()

        # self.play(Write(title2))
        # self.wait()

        tbc = Tex("...to be continued...", color = GREY)\
            .next_to(VGroup(eq2, exp2), RIGHT, buff = 1)
        for x in range(3):
            new_tbc = tbc.copy()
            self.play(FadeIn(new_tbc, rate_func = there_and_back), run_time = 2)
        self.wait(3)


class NextVideo(Scene):
    def construct(self):
        fsr = ScreenRectangle(height = 5, stroke_width = 3, stroke_color = DARK_GREY)
        fsr.to_edge(DOWN, buff = 1)

        title = Tex("Nächstes Video", font_size = 72, color = GREY_A)
        title.to_edge(UP)

        uline = Line(color = GREY, stroke_width = 3)
        uline.set(width = config["frame_width"] - 5)
        uline.next_to(title, DOWN, buff = 0.1)

        self.play(
            Create(uline, run_time = 3),
            Write(title, run_time = 1),
            Create(fsr, run_time = 3),
        )
        self.wait(5)


class Thumbnail(Scene):
    def construct(self):
        formula = get_general_bin_formula()
        formula.set(width = config["frame_width"] - 1)
        formula.add_background_rectangle(buff = 0.2, opacity = 0.85, stroke_opacity = 1, stroke_width = 4, stroke_color = PINK)
        formula.shift(1.5*DOWN)

        body = SVGMobject(SVG_DIR + "human_body_back")
        body.set(height = 7)
        body.to_corner(UL)

        colors = [BLUE, YELLOW, PINK, TEAL]
        for n in range(1, len(body)):
            color = random.choice(colors)
            body[n].set_fill(color, 0.3)
        body[0].set_fill(opacity = 0).set_stroke(width = 1)
        body[-4:-2].set_fill(PINK, 0.75)


        tree = BinomTree(width = 0.4*config["frame_width"], height = body.height / 2.25, num_events=3)
        tree.next_to(formula, UP)

        boxes = VGroup(*[get_row_of_boxes() for x in range(10)])
        boxes.arrange(DOWN)
        boxes.set(height = body.height)
        boxes.to_corner(UR)

        correct = [1, 2, 2, 0, 3, 1, 1, 2, 0, 2]
        for row, index in zip(boxes, correct):
            row[:].set_fill(X_COLOR, 0.15)
            row[index].set_fill(C_COLOR, 0.3)

        title = Tex("Die Bernoulli", "$-$","Formel")
        title.to_edge(UP)
        title.scale(1.5)
        title.set_fill(WHITE, opacity = 0.2)
        title.set_stroke(width = 1.5)


        self.add(body, tree, boxes, title, formula)











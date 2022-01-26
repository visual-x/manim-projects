from manim import *
import random
import scipy.stats

C_COLOR = GREEN
X_COLOR = RED

CMARK_TEX = "\\ding{51}"
XMARK_TEX = "\\ding{55}"

COIN_COLOR_MAP = {
    "K": BLUE_E,
    "Z": RED_E,
}

IMG_DIR = "C:/Programme/Manim/manim_ce/media/img_dir/"
SVG_DIR = "C:/Programme/Manim/manim_ce/media/svg_dir/"

myTemplate = TexTemplate()
myTemplate.add_to_preamble(r"\usepackage{pifont}")


class Histogram(VGroup):
    def __init__(
            self,
            data,
            width, 
            height,
            x_tick_freq = 1,
            x_label_freq = 1,
            y_max_value = 0.4,
            y_tick_num = 4,
            y_axis_label_height = 0.25,
            include_x_labels = True,
            include_y_labels = True,
            include_h_lines = True,
            h_line_style = {
                "stroke_width": 1,
                "stroke_color": GREY_B,
            },
            bar_colors = [BLUE, GREEN],
            bar_style = {
                "stroke_width": 1,
                "stroke_color": WHITE,
                "fill_opacity": 0.6,
            },
            **kwargs
        ):
        super().__init__(**kwargs)
        self.data = data

        self.width = width
        self.height = height
        # axes...
        self.x_tick_freq = x_tick_freq
        self.x_label_freq = x_label_freq
        self.y_max_value = y_max_value
        self.y_tick_num = y_tick_num
        self.y_axis_label_height = y_axis_label_height
        # include axis labels
        self.include_x_labels = include_x_labels
        self.include_y_labels = include_y_labels
        # hlines
        self.include_h_lines = include_h_lines
        self.h_line_style = h_line_style
        # bars
        self.bar_colors = bar_colors
        self.bar_style = bar_style


        self.add_axes(width, height)

        if self.include_h_lines:
            self.add_h_lines()

        self.add_bars(data)

        if self.include_x_labels:
            self.add_x_axis_labels()

        if self.include_y_labels:
            self.add_y_axis_labels()

    def add_axes(self, width, height):
        n_bars = len(self.data)
        axes_configs = {
            "x_range": [0, n_bars, self.x_tick_freq],
            "y_range": [0, self.y_max_value, self.y_tick_num], 
            "x_length": width,
            "y_length": height,
            "x_axis_config": {
                #"unit_size": self.width / n_bars,
                "include_tip": False,
            },
            "y_axis_config": {
                "include_tip": False
            },
        }
        axes = Axes(**axes_configs)
        # axes.center()
        self.axes = axes
        self.add(axes)

    def add_h_lines(self):
        axes = self.axes
        axes.h_lines = VGroup()

        y_values = np.linspace(0, self.y_max_value, self.y_tick_num + 1)
        for y_value in y_values:
            line = DashedLine(dash_length = 0.01, **self.h_line_style)
            line.match_width(axes.x_axis)
            line.next_to(axes.c2p(0, y_value), buff = 0)
            axes.h_lines.add(line)
        axes.add(axes.h_lines)

    def add_bars(self, data):
        self.bars = self.get_bars(data)
        self.add(self.bars)

    def add_x_axis_labels(self):
        axes = self.axes
        axes.x_labels = VGroup()
        for x, bar in list(enumerate(self.bars))[::self.x_label_freq]:
            label = Integer(x)
            label.set(height = 0.25)
            label.next_to(bar, DOWN)
            axes.x_labels.add(label)
        axes.add(axes.x_labels)

    def add_y_axis_labels(self):
        axes = self.axes
        labels = VGroup()
        # for value in self.y_axis_numbers_to_show:
        y_values = np.linspace(0, self.y_max_value, self.y_tick_num + 1)
        for value in y_values:
            label = DecimalNumber(value)
            label.set(height = self.y_axis_label_height)
            label.next_to(axes.y_axis.n2p(value), LEFT)
            labels.add(label)
        axes.y_labels = labels
        axes.y_axis.add(labels)

    def get_axes(self):
        return self.axes

    def get_bars(self, data):
        portions = np.array(data).astype(float)
        total = portions.sum()
        if total == 0:
            portions[:] = 0
        # else:
        #     portions /= total
        bars = VGroup()
        for x, prop in enumerate(portions):
            x_unit = np.linalg.norm(self.axes.c2p(1, 0) - self.axes.c2p(0, 0))
            y_unit = np.linalg.norm(self.axes.c2p(0, 1) - self.axes.c2p(0, 0))

            bar = Rectangle(width = x_unit, height = y_unit * prop)
            bar.move_to(self.axes.c2p(x, 0), DL)
            bars.add(bar)

        bars.set_submobject_colors_by_gradient(*self.bar_colors)
        bars.set_style(**self.bar_style)
        return bars

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_bernoulli_trail_length(self):
        return len(self.data)


class HistoScene(Scene):
    def construct(self):
        pass


    def get_histogram(self, n, p, width, height, zeros = False, **kwargs):
        if zeros is True:
            data = np.zeros(n + 1)
        else:
            dist = scipy.stats.binom(n, p)
            data = np.array([dist.pmf(x) for x in range(0, n + 1)])

        histogram = Histogram(data, width, height, **kwargs)
        return histogram

    def get_histogram_cdf(self, n, p, width, height, zeros = False, **kwargs):
        if zeros is True:
            data = np.zeros(n + 1)
        else:
            data = np.array([scipy.stats.binom.cdf(x, n, p) for x in range(0, n + 1)])

        histogram = Histogram(data, width, height, **kwargs)
        return histogram

    def get_highlight_bars(self, histogram, start, end):
        bars = histogram.bars

        highlight_bars = bars[start:end + 1]
        other_bars = bars[:start] + bars[end + 1:]

        return highlight_bars, other_bars

    def highlight_group_of_bars(self, histogram, start, end, added_anims = None, **kwargs):
        highlight_bars, other_bars = self.get_highlight_bars(histogram, start, end)

        if added_anims is None:
            added_anims = []

        self.play(
            other_bars.animate.set_fill(opacity = 0.15),
            highlight_bars.animate.set_fill(opacity = histogram.bar_style.get("fill_opacity")),
            *added_anims,
            **kwargs
        )

    def highlight_single_bar(self, histogram, bar_num, added_anims = None, **kwargs):
        highlight_bars, other_bars = self.get_highlight_bars(histogram, bar_num, bar_num)

        if added_anims is None:
            added_anims = []

        self.play(
            highlight_bars.animate.set_fill(opacity = histogram.bar_style.get("fill_opacity")),
            other_bars.animate.set_fill(opacity = 0.15),
            *added_anims,
            **kwargs
        )

    def transform_zeros_into_histo(self, histogram, width, height, run_time = 5, added_anims = None, **histo_kwargs):
        n = histogram.get_bernoulli_trail_length()
        data_0 = np.zeros(n)
        histo_0 = Histogram(data_0, width, height, **histo_kwargs)
        histo_0.move_to(histogram)

        if added_anims is None:
            added_anims = []
        
        self.play(
            ReplacementTransform(histo_0, histogram, run_time = run_time), 
            *added_anims
        )


class BinomTree(VGroup):
    def __init__(
            self, 
            width, 
            height, 
            num_events = 4,
            level_buff = 0.5,
            line_config = {
                "color": BLUE_E, 
                "stroke_width": 3
            },
            circle_config = { 
                "color": BLACK, 
                "stroke_width": 0, 
                "stroke_color": WHITE, 
                "fill_opacity": 0.6
            },
            dot_radius_buff = 0.02,
            prob_font_size = 24,
            cx_font_size = 24,
            **kwargs
        ):
        super().__init__(**kwargs)

        self.width = width
        self.height = height

        self.num_events = num_events
        self.level_buff = level_buff
        self.level_width = width / self.num_events - self.level_buff

        self.dot_radius_max = height / 2**(num_events + 1.5)
        self.dot_radius_buff = dot_radius_buff
        self.dot_radius = self.dot_radius_max - self.dot_radius_buff
        self.circle_config = circle_config

        self.line_config = line_config
        self.prob_font_size = prob_font_size
        self.cx_font_size = cx_font_size

        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{pifont}")

        self.add_lines(height)
        self.add_circles()
        self.add_cx_marks()
        self.center()

    def get_cx_line(self, event_num, height):

        line_height = (1/2)**event_num * 1/2 * height
        line_up = Line(LEFT, RIGHT + line_height * UP, buff = 0, **self.line_config)
        line_do = Line(LEFT, RIGHT - line_height * UP, buff = 0, **self.line_config)

        for line in line_up, line_do:
            line.stretch_to_fit_width(self.level_width)
        cx_lines = VGroup(line_do, line_up)

        return cx_lines

    def add_lines(self, height):
        lines = VGroup()
        event_lines = VGroup()

        for i in range(1, self.num_events + 1):
            level_lines = VGroup()
            for k in range(1, 2**(i-1) + 1):
                cx_line = self.get_cx_line(i, height)
                cx_line.shift((i - 1) * self.level_width * RIGHT)
                cx_line.shift((1/2)**(i-1) * k * height * UP)

                level_lines.add(*cx_line)
            event_lines.add(level_lines)
            level_lines.next_to(lines, RIGHT, buff = self.level_buff)
            lines.add(*level_lines)

        self.level_lines = event_lines
        self.lines = lines
        self.add(lines)

    def get_pfad_nums(self):
        lines = self.lines
        num_texs = VGroup()
        for r in range(len(lines)):
            tex = MathTex(str(r), font_size = 12)
            tex.move_to(lines[r])
            tex.add_background_rectangle()
            num_texs.add(tex)

        return num_texs

    def get_pfad_prob(self, texp = None, texq = None, use_prob_values = False, include_colors = False):
        lines = self.lines

        if use_prob_values:
            p = MathTex(texp, font_size = self.prob_font_size).add_background_rectangle()
            q = MathTex(texq, font_size = self.prob_font_size).add_background_rectangle()
        else:
            p = MathTex("p", font_size = self.prob_font_size).add_background_rectangle()
            q = MathTex("q", font_size = self.prob_font_size).add_background_rectangle()

        if include_colors:
            p.set_color(C_COLOR)
            q.set_color(X_COLOR)

        prob_texs = VGroup()
        for r in range(len(lines)):
            if r % 2 == 0:
                direc = DOWN
                obj = q.copy()
            else:
                direc = UP
                obj = p.copy()

            obj.next_to(lines[r].get_center(), direc, buff = 0.05)
            prob_texs.add(obj)

        self.prob_texs = prob_texs
        return prob_texs

    def get_pfad(self, pfad_nums):
        lines = self.lines

        init_start = lines[pfad_nums[0]].get_start()
        init_end = lines[pfad_nums[0]].get_end()

        pfad = Line(init_start, init_end, **self.line_config)

        for num in pfad_nums:
            pfad.add_line_to(lines[num].get_end())
            pfad.add_line_to(lines[num].get_end() + self.level_buff * RIGHT)

        return pfad

    def add_circles(self):
        circles = VGroup()
        for line in [*self.lines]:
            circle = Circle(radius = self.dot_radius, **self.circle_config) 
            circle.move_to(line.get_end() + 1/2*self.level_buff * RIGHT)
            circles.add(circle)

        self.circles = circles
        self.add(circles)

    def add_cx_marks(self):
        c_mark = Tex(CMARK_TEX, tex_template = self.myTemplate, color=C_COLOR, font_size = self.cx_font_size)
        x_mark = Tex(XMARK_TEX, tex_template = self.myTemplate, color=X_COLOR, font_size = self.cx_font_size)

        c_marks, x_marks = VGroup(), VGroup()
        all_marks = VGroup()

        for x, circle in enumerate(self.circles):
            if x % 2:
                mark = c_mark.copy()
                c_marks.add(mark)
            else:
                mark = x_mark.copy()
                x_marks.add(mark)
            mark.match_height(circle)
            mark.move_to(circle)
            all_marks.add(mark)


        # for circle in self.circles[::2]:
        #     x_copy = x_mark.copy()
        #     x_copy.match_height(circle)
        #     x_copy.move_to(circle.get_center())
        #     x_marks.add(x_copy)

        # for circle in self.circles[1::2]:
        #     c_copy = c_mark.copy()
        #     c_copy.match_height(circle)
        #     c_copy.move_to(circle.get_center())
        #     c_marks.add(c_copy)


        self.cx_marks = all_marks

        self.add(c_marks, x_marks)

    def get_c_numbers_next_to_tree(self):
        list_num_events = list(range(self.num_events + 1))
        y_positions = list(np.linspace(0, 1, self.num_events + 1))

        for x in list_num_events, y_positions:
            x.reverse()

        numbers = VGroup()
        for num, y in zip(list_num_events, y_positions):
            tex = MathTex(num)
            tex.shift((y - 0.5) * self.height * UP)
            numbers.add(tex)
        numbers.next_to(self, RIGHT, buff = 1)

        # numbers = VGroup(*[Tex(num).scale(1.1) for num in list_num_events])
        # numbers.arrange_submobjects(DOWN, buff = self.height / (self.num_events + 1))
        # numbers.next_to(self, RIGHT, buff = 1)

        return numbers


class SuitSymbol(SVGMobject):
    def __init__(
            self,
            suit_name,
            height,
            fill_opacity = 1, 
            stroke_width = 1,
            red = "#D02028",
            black = BLACK,
            **kwargs
        ):
        super().__init__(file_name = SVG_DIR + suit_name, **kwargs)

        self.suit_name = suit_name
        self.height = height
        self.fill_opacity = fill_opacity
        self.stroke_width = stroke_width
        self.red = red
        self.black = black

        suits_to_colors = {
            "hearts": self.red,
            "diamonds": self.red,
            "spades": self.black,
            "clubs": self.black,
        }

        color = suits_to_colors[suit_name]
        self.set_stroke(width=self.stroke_width, color = GREY)
        self.set_fill(color, 1)
        self.height = self.height


class PlayingCard(VGroup):
    def __init__(
            self,
            value,
            suit,
            key,
            height,
            color = GREY_A,
            height_to_width = 3.5 / 2.5,
            card_height_to_symbol_height = 5,
            card_width_to_corner_num_width = 10,
            card_height_to_corner_num_height = 10,
            possible_suits = ["diamonds", "hearts", "spades", "clubs"], 
            possible_values = list(map(str, list(range(2, 11)))) + ["B", "D", "K", "A"],
            **kwargs
        ):
        super().__init__(**kwargs)

        self.value = value
        self.suit = suit
        self.key = key
        self.height = height
        self.color = color
        self.height_to_width = height_to_width

        self.card_height_to_symbol_height = card_height_to_symbol_height
        self.card_width_to_corner_num_width = card_width_to_corner_num_width
        self.card_height_to_corner_num_height = card_height_to_corner_num_height

        self.possible_suits = possible_suits
        self.possible_values = possible_values


        self.add_blank_card(height)
        symbol = self.get_symbol()
        number = self.get_corner_elements(value, symbol)

        self.add(symbol, number)


    def add_blank_card(self, height):
        card = RoundedRectangle(
            corner_radius = height / 20, 
            height = height, 
            width = height / self.height_to_width, 
            fill_color = self.color,
            fill_opacity = 1,
            stroke_color = WHITE, 
            stroke_width = 2
        )

        vx = Text("Visual X", font = "Bahnschrift")
        vx.height = height / 15
        vx.set_color(LIGHT_GREY)
        vx.next_to(card.get_corner(UR), DOWN + LEFT, buff = 0.1)

        vx2 = vx.copy().rotate(PI).next_to(card.get_corner(DL), UP + RIGHT, buff = 0.1)

        card.add(vx, vx2)
        self.card = card
        self.add(card)

    def get_value(self):
        value = self.value
        if value is None:
            if self.key is not None:
                value = self.key[:-1]
            else:
                value = random.choice(self.possible_values)
        value = str(value).upper()
        if value == "1":
            value = "A"
        if value not in self.possible_values:
            raise Exception("Invalid card value")

        face_card_to_value = {
            "B": 11,
            "D": 12,
            "K": 13,
            "A": 14,
        }
        try:
            self.numerical_value = int(value)
        except Exception:
            self.numerical_value = face_card_to_value[value]
        return value

    def get_symbol(self):
        suit = self.suit
        if suit is None:
            if self.key is not None:
                suit = dict([
                    (s[0].upper(), s)
                    for s in self.possible_suits
                ])[self.key[-1].upper()]
            else:
                suit = random.choice(self.possible_suits)
        if suit not in self.possible_suits:
            raise Exception("Invalud suit value")
        self.suit = suit
        symbol_height = float(self.height) / self.card_height_to_symbol_height
        symbol = SuitSymbol(suit, height=symbol_height)
        return symbol

    def get_corner_elements(self, value, symbol):
        value_mob = Tex(value)
        width = self.width / self.card_width_to_corner_num_width
        height = self.height / self.card_height_to_corner_num_height
        value_mob.width = width
        value_mob.stretch_to_fit_height(height)
        value_mob.next_to(
            self.get_corner(UP + LEFT), DOWN + RIGHT,
            buff=MED_LARGE_BUFF * width
        )
        value_mob.set_color(symbol.get_color())
        corner_symbol = symbol.copy()
        corner_symbol.set_width(width)
        corner_symbol.next_to(
            value_mob, DOWN,
            buff=MED_SMALL_BUFF * width
        )
        corner_group = VGroup(value_mob, corner_symbol)
        opposite_corner_group = corner_group.copy()
        opposite_corner_group.rotate(
            np.pi, about_point=self.get_center()
        )

        return VGroup(corner_group, opposite_corner_group)


class DeckOfCards(VGroup):
    def __init__(self, **kwargs):
        possible_values = list(map(str, list(range(2, 11)))) + ["B", "D", "K", "A"]
        possible_suits = ["diamonds", "hearts", "spades", "clubs"]
        VGroup.__init__(self, *[
            PlayingCard(value=value, suit=suit, key = None, height = 2, **kwargs)
            for suit in possible_suits
            for value in possible_values
        ])


# ####################################
# DIE FACES, COINS, CHECK_MARKS

def get_die_face(number, dot_color = None):
    if dot_color is None:
        dot_color = "#50CBFF"

    dot = Dot(fill_color = dot_color)
    dot.width = 0.15

    square = Square(fill_color = GREY_E, fill_opacity = 1)\
        .round_corners(0.25)\
        .set_stroke(WHITE, 2)\
        .set(width = 0.6)

    edge_groups = [
        (ORIGIN,),
        (UL, DR),
        (UL, ORIGIN, DR),
        (UL, UR, DL, DR),
        (UL, UR, ORIGIN, DL, DR),
        (UL, UR, LEFT, RIGHT, DL, DR),
    ]

    arrangement = VGroup(*[
        dot.copy().move_to(square.get_critical_point(ec))
        for ec in edge_groups[number - 1]
    ])
    square.set(width = 1)
    result = VGroup(square, arrangement)
    result.number = number
    return result

def get_die_faces(dot_color = None):
    if dot_color is None:
        dot_color = "#50CBFF"
    dot = Dot(fill_color = dot_color)
    dot.width = 0.15

    square = Square(fill_color = GREY_E, fill_opacity = 1)\
        .round_corners(0.25)\
        .set_stroke(WHITE, 2)\
        .set(width = 0.6)

    edge_groups = [
        (ORIGIN,),
        (UL, DR),
        (UL, ORIGIN, DR),
        (UL, UR, DL, DR),
        (UL, UR, ORIGIN, DL, DR),
        (UL, UR, LEFT, RIGHT, DL, DR),
    ]

    arrangements = VGroup(*[
        VGroup(*[
            dot.copy().move_to(square.get_critical_point(ec))
            for ec in edge_group
        ])
        for edge_group in edge_groups
    ])
    square.set(width = 1)

    faces = VGroup(*[
        VGroup(square.copy(), arrangement)
        for arrangement in arrangements
    ])
    faces[0].number = 1
    faces[1].number = 2
    faces[2].number = 3
    faces[3].number = 4
    faces[4].number = 5
    faces[5].number = 6

    faces.arrange(RIGHT)

    return faces

def get_coin(symbol, color=None):
    if color is None:
        color = COIN_COLOR_MAP.get(symbol, GREY_E)
    coin = VGroup()

    circ = Circle(fill_color = color, fill_opacity = 1, stroke_color = WHITE, stroke_width = 1)
    circ.height = 1

    label = Tex(symbol)
    label.height = 0.5 * circ.height
    label.move_to(circ)

    coin.add(circ, label)
    coin.symbol = symbol
    return coin

def get_coin_grid(bools, height=6):
    coins = VGroup(*[
        get_coin("K" if heads else "Z")
        for heads in bools
    ])
    coins.arrange_in_grid()
    coins.height = height
    return coins



def get_random_process(choices, shuffle_time=2, total_time=3, change_rate=0.05, h_buff=0.1, v_buff=0.1):
                            # choices --> heads or tail, die 1,2,3,4,5,6, full deck of cards
    content = choices[0]    # choices[0] --> heads, 1, 2 of diamonds

    container = Square()
    container.set_opacity(0)
    container.width = content.get_width() + 2 * h_buff          # hori buff for animation
    container.height = content.get_height() + 2 * v_buff        # vert buff for animation
    container.move_to(content)
    container.add(content)
    container.time = 0
    container.last_change_time = 0

    def update(container, dt):
        container.time += dt

        t = container.time
        change = all([
            (t % total_time) < shuffle_time,
            container.time - container.last_change_time > change_rate
        ])
        if change:
            mob = container.submobjects[0]
            new_mob = random.choice(choices)
            new_mob.match_height(mob)
            new_mob.move_to(container, DL)
            new_mob.shift(2 * np.random.random() * h_buff * RIGHT)
            new_mob.shift(2 * np.random.random() * v_buff * UP)
            container.set_submobjects([new_mob])
            container.last_change_time = container.time

    container.add_updater(update)
    return container

def get_random_coin(**kwargs):
    return get_random_process([get_coin("K"), get_coin("Z")], **kwargs)

def get_random_die(**kwargs):
    return get_random_process(get_die_faces(), **kwargs)

def get_random_card(height = 1, **kwargs):
    cards = DeckOfCards()
    cards.set_height(height)
    return get_random_process(cards, **kwargs)



def get_checks_and_crosses(bools, width=12):

    result = VGroup()
    for positive in bools:
        if positive:
            mob = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        else:
            mob = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
        mob.positive = positive
        mob.set(width = 0.5)
        result.add(mob)
    result.arrange(RIGHT, buff=MED_SMALL_BUFF)
    result.set(width = width)
    return result

def get_random_checks_and_crosses(n=10, s=0.95, width=12):
    return get_checks_and_crosses(
        bools=(np.random.random(n) < s),
        width=width
    )


# ######################################
# 

def get_random_row(p = 0.7, n=10):  # p is the probability of success
    values = np.random.random(n)
    nums = VGroup()
    syms = VGroup()
    for x, value in enumerate(values):
        num = DecimalNumber(value)
        num.set(height=0.25)
        num.move_to(x * RIGHT)
        num.positive = num.get_value() > 1 - p
        if num.positive:
            num.set_color(C_COLOR)
            sym = Tex(CMARK_TEX, color = C_COLOR, tex_template = myTemplate)
        else:
            num.set_color(X_COLOR)
            sym = Tex(XMARK_TEX, color = X_COLOR, tex_template = myTemplate)
        # sym.match_color(num)
        sym.match_height(num)
        sym.positive = num.positive
        sym.next_to(num, DOWN, buff=0.25)

        nums.add(num)
        syms.add(sym)

    row = VGroup(nums, syms)
    row.nums = nums
    row.syms = syms
    row.n_positive = sum([m.positive for m in nums])

    row.center().to_edge(UP, buff=0)
    return row



########################################
# Bernoulli formula - PMF
def get_binom_formula_with_nmk(n, p, k):
    n_num = Integer(n, color = WHITE)
    k_num = Integer(k, color = C_COLOR)
    nmk_num = Integer(n - k, color = X_COLOR)
    p_num = DecimalNumber(p)

    # create space within formular to place DecimalNumbers
    n_str = "N" * len(n_num)
    k_str = "K" * len(k_num)
    nmk_str = "M" * len(nmk_num)
    p_str = "P" * len(nmk_num)


    formula = MathTex(
        "P",                                        #
        "\\big(",                                   # 1
        "X",                                        # 2
        "=",                                        # 3
        str(k_num.get_value()),                     # 4
        "\\big)",                                   # 5
        "=",                                        # 6
        "\\left(",                                  # 7
        "{" + str(n_num.get_value()),               # 8
        "\\over",                                   # 9
        str(k_num.get_value()) + "}",               # 9
        "\\right)", 
        "\\cdot", 
        str(p_num.get_value()), 
        "^{", 
        str(k_num.get_value()),                     # 14
        "}" 
        "\\cdot", 
        "\\big(", 
        "1", 
        "-", 
        str(p_num.get_value()), 
        "\\big)^{", 
        str(n_num.get_value()),                     # 21
        "-", 
        str(k_num.get_value()),                     # 23
        "}",
        "."
    )
    formula[-1].set_opacity(0)

    formula.remove(formula.get_part_by_tex("\\over"))
    formula[4].match_color(k_num)
    # formula[8].match_color(nmk_num)
    formula[9].match_color(k_num)
    formula[14].match_color(k_num)
    # formula[21].match_color(nmk_num)
    formula[23].match_color(k_num)


    return formula

def get_binom_formula(n, p, k, color_p = True):
    n_num = Integer(n, color = WHITE)
    k_num = Integer(k, color = C_COLOR)
    nmk_num = Integer(n - k, color = X_COLOR)
    p_num = DecimalNumber(p)

    if color_p is True:
        p_num.set_color(YELLOW_D)

    # create space within formular to place DecimalNumbers
    n_str = "N" * len(n_num)
    k_str = "K" * len(k_num)
    nmk_str = "M" * len(nmk_num)
    p_str = "P" * len(nmk_num)


    formula = MathTex(
        "P",                                        #           P(X = k)
        "\\big(",                                   # 1
        "X",                                        # 2
        "=",                                        # 3
        str(k_num.get_value()),                     # 4
        "\\big)",                                   # 5

        "=",                                        # 6            =

        "\\left(",                                  # 7         (  n  )
        "{" + str(n_num.get_value()),               # 8         ( --- )
        "\\over",                                   #           (  k  )
        str(k_num.get_value()) + "}",               # 9
        "\\right)",                                 # 10

        "\\cdot",                                   # 11
        str(p_num.get_value()),                     # 12
        "^{" + str(k_num.get_value()) + "}",        # 13

        "\\cdot",                                   # 14
        "\\big(",                                   # 15
        "1",                                        # 16
        "-",                                        # 17
        str(p_num.get_value()),                     # 18
        "\\big)^{",                                 # 19
        str(nmk_num.get_value()),                   # 20
        "}",
    )

    formula.remove(formula.get_part_by_tex("\\over"))
    formula[4].match_color(k_num)
    formula[9].match_color(k_num)
    formula[12].match_color(p_num)
    formula[13].match_color(k_num)
    formula[18].match_color(p_num)
    formula[20].match_color(nmk_num)

    formula.p = VGroup(formula[12], formula[18])
    formula.n = formula[8]
    formula.k = VGroup(formula[4], formula[9], formula[13])
    formula.nmk = formula[20]

    return formula

def get_binom_result(n, p, k, num_decimal_places = None):
    if num_decimal_places is None:
        result = round(scipy.stats.binom.pmf(k, n, p), 4)
    else:
        result = round(scipy.stats.binom.pmf(k, n, p), num_decimal_places)

    return result


# Bernoulli Formula - CDF
def get_binom_cdf_summands(k):
    eq = MathTex(
        "P", "\\big(", "X", "\\leq", str(k), "\\big)", "=",
        # 7                      11           13
        "P", "\\big(", "X", "=", 0, "\\big)", "+",
        #                                     20
        "P", "\\big(", "X", "=", 1, "\\big)", "+",
        #          22
        "\\ldots", "+",
        #                          27
        "P", "\\big(", "X", "=", str(k), "\\big)",
    )
    eq.set_color_by_tex_to_color_map({"+": PINK})
    eq[3].set_color(PINK)
    eq[4].set_color(C_COLOR)
    eq[-2].set_color(C_COLOR)

    return eq

def get_binom_cdf_sum_notation(n, p, k):
    eq = MathTex(
        "=", 
        "\\sum", 
        "\\left(", 
        "{" + n, 
        "\\over", 
        "i" + "}", 
        "\\right)", 
        "\\cdot", 
        p +"^{", 
        "i}", 
        "\\cdot", 
        "\\left(", 
        "1", 
        "-", 
        p, 
        "\\right)^", 
        "{" + n, 
        "- i}"
    )
    eq.remove(eq.get_part_by_tex("\\over"))
    eq.set_color_by_tex_to_color_map({"p": YELLOW_D, "i": C_COLOR, "\\right": WHITE})
    eq[1].set_color(PINK)
    eq[7].set_color(YELLOW_D)
    eq[13].set_color(YELLOW_D)
    eq[-2:].set_color(X_COLOR)

    lower = MathTex("i", "=", "0")
    lower.scale(0.6)
    lower.next_to(eq[1], DOWN, buff = 0.1)
    lower[0].set_color(C_COLOR)

    upper = MathTex(k)
    upper.scale(0.7)
    upper.set_color(C_COLOR).next_to(eq[1], UP, buff = 0.1)

    eq.add(lower, upper)

    return eq

def get_binom_cdf_mathcal(n, p, k):
    eq = MathTex("=", "\\mathcal{F}", "\\big(", n, ",", p, ",", k, "\\big)")
    eq[5].set_color(YELLOW_D)
    eq[7].set_color(C_COLOR)

    return eq

def get_binom_cdf_result(n, p, k, num_decimal_places = None):
    if num_decimal_places is None:
        result = round(scipy.stats.binom.cdf(k, n, p), 4)
    else:
        result = round(scipy.stats.binom.cdf(k, n, p), num_decimal_places)

    return result










import manim.utils.rate_functions
from manim import *
import math

from manim.utils.rate_functions import ease_in_sine, ease_out_sine
from numpy.ma.core import less_equal


def Text2(text, kwargs={}):  # Text util
    return Text(text, font="JetBrains Mono", **kwargs)

def Arrow2(start, end, **kwargs):
    return Arrow(start=start, end=end, max_stroke_width_to_length_ratio=100, **kwargs)

N = 3

def increment(counters, index):
    old = counters[index]
    num = (int(old.text) + 1) % N
    new = Text2(str(num), {'font_size': old.font_size}).move_to(old.get_center())
    counters[index] = new
    return AnimationGroup(FadeOut(old, shift=DOWN), FadeIn(new, shift=DOWN), run_time=0.75)

class Intro(Scene):
    def construct(self):
        brackets = VGroup(*[Text2('[', {'font_size':100, 'color':GRAY}).rotate(PI / 2)
                          .shift(DOWN + RIGHT * 2 * (i - 0.5)).stretch(1.3, 0) for i in range(2)])
        counters = VGroup(*[Text2('0', {'font_size':120}).shift(RIGHT * 2 * (i - 0.5)) for i in range(2)])
        ntext = Text2('n = ' + str(N), {'font_size':120}).shift(UP * 2.5)
        self.wait()
        self.play(FadeIn(counters), FadeIn(brackets), Write(ntext))

        self.wait()
        self.play(increment(counters, 0))
        self.play(increment(counters, 0))
        self.play(increment(counters, 1))
        self.play(increment(counters, 0))
        self.play(increment(counters, 1))
        self.play(increment(counters, 1))
        self.wait()

        state = VGroup(brackets, counters)
        self.play(state.animate.shift(LEFT * 5 + UP).scale(0.5))
        states = VGroup(state)

        states.add(states[-1].copy().shift(RIGHT * 2.5))
        arrow = Arrow2(start=states[0], end=states[1], buff=0, color=BLUE).shift(UP * 0.6)
        self.play(GrowArrow(arrow), ReplacementTransform(states[0].copy(), states[1]))
        arrows = VGroup(arrow)
        self.play(increment(states[1][1], 1))

        states.add(states[-1].copy().shift(RIGHT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 1))

        states.add(states[-1].copy().shift(RIGHT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 0))

        states.add(states[-1].copy().shift(RIGHT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 1))

        states.add(states[-1].copy().shift(DOWN * 2 + LEFT * 1.25))
        arrow = Arrow2(start=states[-2].get_edge_center(DOWN), end=states[-1].get_edge_center(UP), buff=MED_SMALL_BUFF, color=BLUE)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 1))

        states.add(states[-1].copy().shift(LEFT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 0))

        states.add(states[-1].copy().shift(LEFT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 1))

        states.add(states[-1].copy().shift(LEFT * 2.5))
        arrow = Arrow2(start=states[-2], end=states[-1], buff=0, color=BLUE).shift(UP * 0.6)
        arrows.add(arrow)
        self.play(GrowArrow(arrows[-1]), ReplacementTransform(states[-2].copy(), states[-1]))
        self.play(increment(states[-1][1], 1))
        self.wait()

        self.play(Transform(ntext, Text2('n=3', {'font_size':60}).to_corner(UL)))
        statesgrid = VGroup(states[0].copy().move_to(UP * 2.5 + LEFT * 3),
                            states[1].copy().move_to(UP * 2.5),
                            states[2].copy().move_to(UP * 2.5 + RIGHT * 3),
                            states[3].copy().move_to(RIGHT * 3),
                            states[4].copy().move_to(LEFT * 3),
                            states[5].copy().move_to(ORIGIN),
                            states[6].copy().move_to(DOWN * 2.5),
                            states[7].copy().move_to(DOWN * 2.5 + RIGHT * 3),
                            states[8].copy().move_to(DOWN * 2.5 + LEFT * 3))
        arrowsgrid = VGroup(Arrow(start=statesgrid[0].get_edge_center(RIGHT), end=statesgrid[1].get_edge_center(LEFT), color=BLUE, buff=0),
                            Arrow(start=statesgrid[1].get_edge_center(RIGHT), end=statesgrid[2].get_edge_center(LEFT), color=BLUE, buff=0),
                            Arrow(start=statesgrid[2].get_edge_center(DOWN), end=statesgrid[3].get_edge_center(UP), color=BLUE),
                            VGroup(Arrow(start=statesgrid[3].get_edge_center(RIGHT), end=statesgrid[3].get_edge_center(RIGHT) + RIGHT, color=BLUE, buff=0),
                                   Arrow(start=statesgrid[4].get_edge_center(LEFT) + LEFT, end=statesgrid[4].get_edge_center(LEFT), color=BLUE, buff=0)),
                            Arrow(start=statesgrid[4].get_edge_center(RIGHT), end=statesgrid[5].get_edge_center(LEFT), color=BLUE, buff=0),
                            Arrow(start=statesgrid[5].get_edge_center(DOWN), end=statesgrid[6].get_edge_center(UP), color=BLUE),
                            Arrow(start=statesgrid[6].get_edge_center(RIGHT), end=statesgrid[7].get_edge_center(LEFT), color=BLUE, buff=0),
                            VGroup(Arrow(start=statesgrid[7].get_edge_center(RIGHT), end=statesgrid[7].get_edge_center(RIGHT) + RIGHT, color=BLUE, buff=0),
                                   Arrow(start=statesgrid[8].get_edge_center(LEFT) + LEFT, end=statesgrid[8].get_edge_center(LEFT), color=BLUE, buff=0)))

        self.play(Transform(states, statesgrid), Transform(arrows, arrowsgrid), run_time=2)
        self.wait()
        self.play(Indicate(states[2]), Indicate(states[5]), Indicate(states[8]))
        self.wait()

class Analysis(Scene):
    def construct(self):
        ntext = Text2('n=7', {'font_size':60}).to_corner(UL)
        self.wait(0.5)
        self.play(Write(ntext))

        vertices = VGroup()
        for i in range(7):
            for j in range(7):
                if i == 0 and j == 0:
                    vertices.add(Dot(color=YELLOW).move_to(RIGHT * (j - 2.5) + DOWN * (i - 2.5)))
                else:
                    vertices.add(Dot(color=GRAY).move_to(RIGHT * (j - 2.5) + DOWN * (i - 2.5)))
        vertices.set_z_index(10)

        coords = VGroup(VGroup([Text2(str(i), {'font_size':40}).move_to(RIGHT * (i - 2.5) + UP * 3.5) for i in range(7)]),
                        VGroup([Text2(str(i), {'font_size':40}).move_to(DOWN * (i - 2.5) + LEFT * 3.5) for i in range(7)]))
        coords.set_z_index(100)

        self.play(AnimationGroup(*[Create(vertex) for vertex in vertices], lag_ratio=0.025),
                  AnimationGroup(*[Write(xcoord) for xcoord in coords[0]], lag_ratio=0.15),
                  AnimationGroup(*[Write(ycoord) for ycoord in coords[1]], lag_ratio=0.15))
        self.wait(0.5)

        v_d_label = MathTex('v_d').next_to(vertices[24], UP + RIGHT, buff=SMALL_BUFF)
        self.play(vertices[24].animate.set_color(YELLOW), Write(v_d_label))
        self.wait()

        TINY_BUFF = 0.05
        # consider this vertex
        highlight = Circle(color=RED, radius=0.2, stroke_width=6).move_to(vertices[24])
        self.play(FadeIn(highlight))
        arrow = Arrow2(start=vertices[24], end=vertices[31], buff=0, color=BLUE)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(Transform(arrow, Arrow2(start=vertices[30], end=vertices[31], buff=0, color=BLUE)), FadeOut(highlight))
        self.wait()

        diagonalarrows = VGroup(arrow)
        for i in range(2):
            diagonalarrows.add(Arrow2(start=vertices[36 + 6 * i], end=vertices[37 + 6 * i], color=BLUE, buff=0))
        self.play(AnimationGroup(*[FadeIn(diagonalarrows[i]) for i in range(1, 3)], lag_ratio=0.2))

        for i in range(3):
            diagonalarrows.add(Arrow2(start=vertices[18 - 6 * i], end=vertices[25 - 6 * i], color=GREEN, buff=0))
        self.play(AnimationGroup(*[FadeIn(diagonalarrows[i]) for i in range(3, 6)], lag_ratio=0.2))
        self.wait()

        indices = [7 * i - 1 - (i + 1) % 7 for i in range(7)]
        self.play(AnimationGroup(*[Indicate(vertices[index], color=RED) for index in indices]))
        self.wait(0.5)

        arrows1 = VGroup(Arrow2(start=vertices[10], end=vertices[17], color=GREEN, buff=0))
        self.play(GrowArrow(arrows1[0]))
        self.wait(0.5)
        highlight = Circle(color=RED, radius=0.2, stroke_width=6).move_to(vertices[11])
        self.play(FadeIn(highlight))
        arrows1.add(Arrow2(start=vertices[4], end=vertices[11], color=GREEN, buff=0))
        self.play(FadeIn(arrows1[-1]))
        self.play(FadeOut(highlight))

        arrows1.add(VGroup(Arrow2(start=vertices[5].get_center() + UP, end=vertices[5], buff=0),
                           Line(start=vertices[47], end=vertices[47].get_center() + DOWN * 0.5,
                                color=[BLACK, GREEN], stroke_width=6)))
        arrows1[-1][0].set_color([BLACK, GREEN]).set_sheen_direction([0, -1, 0])
        arrows1[-1][0].get_tip().set_color(GREEN)

        for i in range(4):
            start = 7 * (5 - i) + (i + 6) % 7
            arrows1.add(Arrow2(start=vertices[start], end=vertices[start + 7], color=GREEN, buff=0))
        self.play(AnimationGroup(*[FadeIn(arrows1[i]) for i in range(2, 7)], lag_ratio=0.5))

        arrows2 = VGroup(Arrow2(start=vertices[9], end=vertices[10], color=BLUE, buff=0))
        self.play(FadeIn(arrows2[-1]))
        self.wait(0.5)

        for i in range(2):
            arrows2.add(Arrow2(start=vertices[15 + 6 * i], end=vertices[16 + 6 * i], color=BLUE, buff=0))

        arrows2.add(VGroup(Arrow2(start=vertices[28].get_center() + LEFT, end=vertices[28], buff=0),
                           Line(start=vertices[34], end=vertices[34].get_center() + RIGHT * 0.5,
                                color=[BLACK, BLUE], stroke_width=5)))
        arrows2[-1][0].set_color([BLACK, BLUE]).set_sheen_direction([1, 0, 0])
        arrows2[-1][0].get_tip().set_color(BLUE)

        for i in range(3):
            start = 7 * ((5 + i) % 7) + 5 - i
            arrows2.add(Arrow2(start=vertices[start], end=vertices[start + 1], color=BLUE, buff=0))

        self.play(AnimationGroup(*[FadeIn(arrows2[i]) for i in range(1, 7)], lag_ratio=0.4))

        allarrows = VGroup(VGroup([arrows2[i] for i in range(2, -1, -1)] + [arrows2[i] for i in range(6, 2, -1)]),
                     VGroup([arrows1[i] for i in range(1, -1, -1)] + [arrows1[i] for i in range(6, 1, -1)]),
                     VGroup([diagonalarrows[i] for i in range(5, 2, -1)] + [diagonalarrows[i] for i in range(3)]))
        self.remove(diagonalarrows, arrows1, arrows2)
        self.add(allarrows[0], allarrows[1], allarrows[2])
        self.wait()

        allarrows.add(allarrows[0].copy().shift(UP * 3))
        allarrows[-1][1:4].shift(DOWN * 7)
        self.play(AnimationGroup([GrowArrow(allarrows[-1][i]) for i in range(6)] +
                                 [FadeIn(allarrows[-1][-1][1]), GrowArrow(allarrows[-1][-1][0])], lag_ratio=0.2))

        allarrows.add(allarrows[1].copy().shift(LEFT * 3))
        allarrows[-1][2:5].shift(RIGHT * 7)
        self.play(AnimationGroup([GrowArrow(allarrows[-1][i]) for i in range(6)] +
                                 [FadeIn(allarrows[-1][-1][1]), GrowArrow(allarrows[-1][-1][0])], lag_ratio=0.2))

        allarrows.add(allarrows[0].copy().shift(UP))
        allarrows[-1][3].shift(DOWN * 7)
        self.play(AnimationGroup([GrowArrow(allarrows[-1][i]) for i in range(6)] +
                                 [FadeIn(allarrows[-1][-1][1]), GrowArrow(allarrows[-1][-1][0])], lag_ratio=0.2))

        allarrows.add(allarrows[0].copy().shift(DOWN * 2))
        allarrows[-1][4:6].shift(UP * 7)
        self.play(AnimationGroup([GrowArrow(allarrows[-1][i]) for i in range(6)] +
                                 [FadeIn(allarrows[-1][-1][1]), GrowArrow(allarrows[-1][-1][0])], lag_ratio=0.2))
        self.wait()

        pos = [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1]

        indices = [0]
        for d in pos:
            last = indices[-1]
            x = last % 7
            y = last // 7
            if d == 1:
                x = (x + 1) % 7
            else:
                y = (y + 1) % 7
            indices.append(y * 7 + x)

        self.play(AnimationGroup(*[Indicate(vertices[index], color=PURE_RED) for index in indices], lag_ratio=0.1, run_time=6))
        self.wait()

        self.play(allarrows[0][:3].animate.shift(UP), allarrows[0][4:].animate.shift(UP),
                  allarrows[0][3].animate.shift(DOWN * 6), allarrows[5][:2].animate.shift(UP),
                  allarrows[5][3:].animate.shift(UP), allarrows[5][2].animate.shift(DOWN * 6),
                  allarrows[6][:4].animate.shift(UP * 2), allarrows[6][4:6].animate.shift(DOWN * 5),
                  allarrows[6][6:].animate.shift(UP * 2), allarrows[4][:2].animate.shift(RIGHT * 4),
                  allarrows[4][2:-1].animate.shift(LEFT * 3), allarrows[4][-1].animate.shift(RIGHT * 4),
                  run_time=1.5)
        self.wait()

        brace = BraceBetweenPoints(vertices[0].get_edge_center(UP), vertices[4].get_edge_center(UP))
        x_text = brace.get_tex('X=4').shift(UP * 0.2)
        self.play(Write(brace), Write(x_text))
        self.wait()

        grid = VGroup(allarrows, vertices, coords, v_d_label, brace, x_text)
        self.play(grid.animate.shift(LEFT * 3), Unwrite(ntext))
        self.play(AnimationGroup(*[vertices[7 * i + 6 - i].animate.set_color(YELLOW) for i in range(7)]))
        self.wait()

        highlight = Circle(color=RED, radius=0.2, stroke_width=6).move_to(vertices[0])
        x_1 = MathTex('x_1 = X').shift(RIGHT * 4 + UP * 3)
        self.play(Write(highlight), run_time=0.5)
        self.play(highlight.animate.shift(RIGHT * 4), run_time=0.75)
        self.play(highlight.animate.shift(DOWN * 2), Write(x_1), run_time=0.75)
        self.wait()

        condition1 = VGroup(Tex('If $x_{i - 1} > d$:'),
                            Tex('$x_i \equiv x_{i - 1} + X \pmod{n}$')).arrange(DOWN).scale(0.9).shift(RIGHT * 3.5 + UP * 1.5)
        condition2 = VGroup(Tex('If $x_{i - 1} < d$:'),
                            Tex('$x_i \equiv x_{i - 1} + 1 + X \pmod{n}$')).arrange(DOWN).scale(0.9).shift(RIGHT * 3.5 + DOWN * 0.5)
        condition1[0].align_to(condition1[1], LEFT)
        condition2[0].align_to(condition2[1], LEFT)
        condition2.align_to(condition1, LEFT)

        self.play(Write(condition1[0]), highlight.animate.shift(DOWN))
        highlight2 = highlight.copy().shift(LEFT * 3)
        self.play(FadeOut(highlight, shift=RIGHT * 3), FadeIn(highlight2, shift=RIGHT * 2), run_time=0.75)
        self.play(highlight2.animate.shift(DOWN * 2), run_time=0.75)
        self.wait(0.5)
        self.play(Write(condition1[1]))
        self.wait()

        self.play(Write(condition2[0]))
        self.play(highlight2.animate.shift(RIGHT), run_time=0.75)
        self.play(highlight2.animate.shift(RIGHT * 4), run_time=0.75)
        highlight3 = highlight2.copy().shift(UP * 5)
        self.play(FadeOut(highlight2, shift=DOWN * 2), FadeIn(highlight3, shift=DOWN), run_time=0.75)
        self.wait(0.5)
        self.play(Write(condition2[1]))

        ending = Tex('If $x_i = d$, stop').scale(0.9).shift(DOWN * 2).align_to(condition2, LEFT)
        self.play(Write(ending))
        self.wait()

        grid.add(highlight3)
        divider = Line(start=UP * 10, end=DOWN * 10)
        self.play(Unwrite(x_1), Unwrite(condition1), Unwrite(condition2), Unwrite(ending),
                  grid.animate.scale(0.8).to_edge(LEFT), Write(divider))

        self.wait()

class Cycle(Scene):
    def construct(self):
        counter = Tex('Flips: ', '0').shift(DOWN * 2 + LEFT * 5).scale(1.5)
        parity = Tex('Parity: ', 'even').shift(DOWN * 2).scale(1.5)
        sign = Tex('Sign: ', '$+1$').shift(DOWN * 2 + RIGHT * 5).scale(1.5)

        self.wait(0.5)
        self.play(Write(counter), Write(parity), Write(sign))
        permutation = Matrix([[0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]], left_bracket="(", right_bracket=")",
                             h_buff=0.75, bracket_h_buff=0.2).shift(UP).scale(2)
        self.play(Write(permutation))
        self.wait()

        elements = permutation.get_rows()[1]

        self.play(elements[0].animate.shift(RIGHT * 1.5), elements[1].animate.shift(LEFT * 1.5))
        self.play(AnimationGroup(*[Transform(counter[1], Tex('1').scale(1.5).move_to(counter[1])),
                                 Transform(parity[1], Tex('odd').scale(1.5).move_to(parity[1])),
                                 Transform(sign[1], Tex('$-1$').scale(1.5).move_to(sign[1]))]))
        self.wait(0.5)
        self.play(AnimationGroup(
            AnimationGroup(elements[0].animate.shift(RIGHT * 1.5), elements[2].animate.shift(LEFT * 1.5)),
            AnimationGroup([Transform(counter[1], Tex('2').scale(1.5).move_to(counter[1])),
                            Transform(parity[1], Tex('even').scale(1.5).move_to(parity[1])),
                            Transform(sign[1], Tex('$+1$').scale(1.5).move_to(sign[1]))]),
            lag_ratio=0.3
        ))

        self.play(AnimationGroup(
            AnimationGroup(elements[0].animate.shift(RIGHT * 1.5), elements[3].animate.shift(LEFT * 1.5)),
            AnimationGroup([Transform(counter[1], Tex('3').scale(1.5).move_to(counter[1])),
                            Transform(parity[1], Tex('odd').scale(1.5).move_to(parity[1])),
                            Transform(sign[1], Tex('$-1$').scale(1.5).move_to(sign[1]))]),
            lag_ratio=0.3
        ))

        self.play(AnimationGroup(
            AnimationGroup([elements[0].animate.shift(RIGHT * 1.5), elements[4].animate.shift(LEFT * 1.5)]),
            AnimationGroup([Transform(counter[1], Tex('4').scale(1.5).move_to(counter[1])),
                            Transform(parity[1], Tex('even').scale(1.5).move_to(parity[1])),
                            Transform(sign[1], Tex('$+1$').scale(1.5).move_to(sign[1]))]),
            lag_ratio=0.3
        ))

        self.play(AnimationGroup(
            AnimationGroup([elements[0].animate.shift(RIGHT * 1.5), elements[5].animate.shift(LEFT * 1.5)]),
            AnimationGroup([Transform(counter[1], Tex('5').scale(1.5).move_to(counter[1])),
                            Transform(parity[1], Tex('odd').scale(1.5).move_to(parity[1])),
                            Transform(sign[1], Tex('$-1$').scale(1.5).move_to(sign[1]))]),
            lag_ratio=0.3
        ))

        self.play(AnimationGroup(
            AnimationGroup([elements[0].animate.shift(RIGHT * 1.5), elements[6].animate.shift(LEFT * 1.5)]),
            AnimationGroup([Transform(counter[1], Tex('6').scale(1.5).move_to(counter[1])),
                            Transform(parity[1], Tex('even').scale(1.5).move_to(parity[1])),
                            Transform(sign[1], Tex('$+1$').scale(1.5).move_to(sign[1]))]),
            lag_ratio=0.3
        ))

        # self.play(elements[2].animate.shift(RIGHT * 4.5), elements[5].animate.shift(LEFT * 4.5))
        # self.play(AnimationGroup(*[Transform(counter[1], Tex('1').scale(1.5).move_to(counter[1])),
        #                          Transform(parity[1], Tex('odd').scale(1.5).move_to(parity[1])),
        #                          Transform(sign[1], Tex('$-1$').scale(1.5).move_to(sign[1]))],
        #                          lag_ratio=0.3))
        # self.wait(0.5)
        #
        # self.play(elements[3].animate.shift(LEFT * 1.5), elements[5].animate.shift(RIGHT * 1.5))
        # self.play(AnimationGroup(*[Transform(counter[1], Tex('2').scale(1.5).move_to(counter[1])),
        #                            Transform(parity[1], Tex('even').scale(1.5).move_to(parity[1])),
        #                            Transform(sign[1], Tex('$+1$').scale(1.5).move_to(sign[1]))],
        #                          lag_ratio=0.3))
        # self.wait(0.5)
        #
        # self.play(elements[0].animate.shift(RIGHT * 6), elements[4].animate.shift(LEFT * 6))
        # self.play(AnimationGroup(*[Transform(counter[1], Tex('3').scale(1.5).move_to(counter[1])),
        #                            Transform(parity[1], Tex('odd').scale(1.5).move_to(parity[1])),
        #                            Transform(sign[1], Tex('$-1$').scale(1.5).move_to(sign[1]))],
        #                          lag_ratio=0.3))
        # self.wait(0.5)
        #
        # self.play(elements[2].animate.shift(RIGHT * 1.5), elements[6].animate.shift(LEFT * 1.5))
        # self.play(AnimationGroup(*[Transform(counter[1], Tex('4').scale(1.5).move_to(counter[1])),
        #                            Transform(parity[1], Tex('even').scale(1.5).move_to(parity[1])),
        #                            Transform(sign[1], Tex('$+1$').scale(1.5).move_to(sign[1]))],
        #                          lag_ratio=0.3))
        # self.wait(0.5)

        self.wait()

class Calculation(Scene):
    def construct(self):
        vertices = VGroup()
        for i in range(7):
            for j in range(7):
                if i == 0 and j == 0:
                    vertices.add(Dot(color=YELLOW).move_to(RIGHT * (j - 2.5) + DOWN * (i - 2.5)))
                else:
                    vertices.add(Dot(color=GRAY).move_to(RIGHT * (j - 2.5) + DOWN * (i - 2.5)))
        vertices.set_z_index(10)

        coords = VGroup(VGroup([Text2(str(i), {'font_size':40}).move_to(RIGHT * (i - 2.5) + UP * 3.5) for i in range(7)]),
                        VGroup([Text2(str(i), {'font_size':40}).move_to(DOWN * (i - 2.5) + LEFT * 3.5) for i in range(7)]))
        coords.set_z_index(100)


        v_d_label = MathTex('v_d').next_to(vertices[24], UP + RIGHT, buff=SMALL_BUFF)
        vertices[24].set_color(YELLOW)

        TINY_BUFF = 0.05
        # consider this vertex
        arrow = Arrow2(start=vertices[30], end=vertices[31], buff=0, color=BLUE)

        diagonalarrows = VGroup(arrow)
        for i in range(2):
            diagonalarrows.add(Arrow2(start=vertices[36 + 6 * i], end=vertices[37 + 6 * i], color=BLUE, buff=0))

        for i in range(3):
            diagonalarrows.add(Arrow2(start=vertices[18 - 6 * i], end=vertices[25 - 6 * i], color=GREEN, buff=0))

        indices = [7 * i - 1 - (i + 1) % 7 for i in range(7)]

        arrows1 = VGroup(Arrow2(start=vertices[10], end=vertices[17], color=GREEN, buff=0))
        arrows1.add(Arrow2(start=vertices[4], end=vertices[11], color=GREEN, buff=0))

        arrows1.add(VGroup(Arrow2(start=vertices[5].get_center() + UP, end=vertices[5], buff=0),
                           Line(start=vertices[47], end=vertices[47].get_center() + DOWN * 0.5,
                                color=[BLACK, GREEN], stroke_width=6)))
        arrows1[-1][0].set_color([BLACK, GREEN]).set_sheen_direction([0, -1, 0])
        arrows1[-1][0].get_tip().set_color(GREEN)

        for i in range(4):
            start = 7 * (5 - i) + (i + 6) % 7
            arrows1.add(Arrow2(start=vertices[start], end=vertices[start + 7], color=GREEN, buff=0))

        arrows2 = VGroup(Arrow2(start=vertices[9], end=vertices[10], color=BLUE, buff=0))

        for i in range(2):
            arrows2.add(Arrow2(start=vertices[15 + 6 * i], end=vertices[16 + 6 * i], color=BLUE, buff=0))

        arrows2.add(VGroup(Arrow2(start=vertices[28].get_center() + LEFT, end=vertices[28], buff=0),
                           Line(start=vertices[34], end=vertices[34].get_center() + RIGHT * 0.5,
                                color=[BLACK, BLUE], stroke_width=5)))
        arrows2[-1][0].set_color([BLACK, BLUE]).set_sheen_direction([1, 0, 0])
        arrows2[-1][0].get_tip().set_color(BLUE)

        for i in range(3):
            start = 7 * ((5 + i) % 7) + 5 - i
            arrows2.add(Arrow2(start=vertices[start], end=vertices[start + 1], color=BLUE, buff=0))


        allarrows = VGroup(VGroup([arrows2[i] for i in range(2, -1, -1)] + [arrows2[i] for i in range(6, 2, -1)]),
                     VGroup([arrows1[i] for i in range(1, -1, -1)] + [arrows1[i] for i in range(6, 1, -1)]),
                     VGroup([diagonalarrows[i] for i in range(5, 2, -1)] + [diagonalarrows[i] for i in range(3)]))

        allarrows.add(allarrows[0].copy().shift(UP * 3))
        allarrows[-1][1:4].shift(DOWN * 7)

        allarrows.add(allarrows[1].copy().shift(LEFT * 3))
        allarrows[-1][2:5].shift(RIGHT * 7)

        allarrows.add(allarrows[0].copy().shift(UP))
        allarrows[-1][3].shift(DOWN * 7)

        allarrows.add(allarrows[0].copy().shift(DOWN * 2))
        allarrows[-1][4:6].shift(UP * 7)

        pos = [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1]

        indices = [0]
        for d in pos:
            last = indices[-1]
            x = last % 7
            y = last // 7
            if d == 1:
                x = (x + 1) % 7
            else:
                y = (y + 1) % 7
            indices.append(y * 7 + x)

        allarrows[0][:3].shift(UP)
        allarrows[0][4:].shift(UP),
        allarrows[0][3].shift(DOWN * 6), allarrows[5][:2].shift(UP),
        allarrows[5][3:].shift(UP), allarrows[5][2].shift(DOWN * 6),
        allarrows[6][:4].shift(UP * 2), allarrows[6][4:6].shift(DOWN * 5),
        allarrows[6][6:].shift(UP * 2), allarrows[4][:2].shift(RIGHT * 4),
        allarrows[4][2:-1].shift(LEFT * 3), allarrows[4][-1].shift(RIGHT * 4),

        brace = BraceBetweenPoints(vertices[0].get_edge_center(UP), vertices[4].get_edge_center(UP))
        x_text = brace.get_tex('X=4').shift(UP * 0.2)

        grid = VGroup(allarrows, vertices, coords, v_d_label, brace, x_text)
        grid.shift(LEFT * 3)
        for i in range(7):
            vertices[7 * i + 6 - i].set_color(YELLOW)

        divider = Line(start=UP * 10, end=DOWN * 10)
        grid.scale(0.8).to_edge(LEFT)
        self.add(grid, divider)

        ordermatrix = Matrix([['x_1', 'x_2', 'x_3', '\cdots', 'x_{n - 1}', 'x_n'], ['x_2', 'x_3', 'x_4', '\cdots', 'x_n', 'x_1']],
                             left_bracket="(", right_bracket=")")
        e1 = ordermatrix.get_entries()
        e1.arrange_in_grid(rows=2, cols=6, buff=(0.4, 0.4)).shift(RIGHT * 32/9 + UP * 2)
        b1 = ordermatrix.get_brackets()
        b1[0].next_to(e1, LEFT, buff=0.2)
        b1[1].next_to(e1, RIGHT, buff=0.2)

        equal = MathTex('=').next_to(ordermatrix, DOWN)
        self.play(AnimationGroup(*[Write(ordermatrix), Write(equal)], lag_ratio=0.7))
        self.wait()

        dmatrix = Matrix([['0', '1', '\cdots', 'd', 'd + 1', '\cdots', 'n - 1'],
                            ['1', '2', '\cdots', '0', 'd + 1', '\cdots', 'n - 1']],
                             left_bracket="(", right_bracket=")").scale(0.7)
        e2 = dmatrix.get_entries()
        e2.arrange_in_grid(rows=2, cols=7, buff=(0.3, 0.4)).align_to(e1, LEFT)
        b2 = dmatrix.get_brackets()
        b2[0].next_to(e2, LEFT, buff=0.2)
        b2[1].next_to(e2, RIGHT, buff=0.2)
        comp = MathTex('\circ').next_to(dmatrix, RIGHT)

        self.play(AnimationGroup(*[Write(dmatrix), Write(comp)], lag_ratio=0.7))
        self.wait()

        incmatrix = Matrix([['0', '1', '2', '\cdots', 'n - 1'],
                            ['X', 'X + 1', 'X + 2', '\cdots', 'X + n - 1']],
                           left_bracket="(", right_bracket=")").scale(0.7)
        e3 = incmatrix.get_entries()
        e3.arrange_in_grid(rows=2, cols=5, buff=(0.3, 0.4)).shift(RIGHT * 32 / 9 + DOWN * 1.5)
        b3 = incmatrix.get_brackets()
        b3[0].next_to(e3, LEFT, buff=0.2)
        b3[1].next_to(e3, RIGHT, buff=0.2)
        self.play(Write(incmatrix))
        self.wait()

        self.play(Unwrite(grid), Unwrite(divider))
        order2 = ordermatrix.copy().move_to(UP * 2.5)
        d2 = dmatrix.copy().move_to(UP * 0.5 + LEFT * 3.6).scale(0.8/0.7)
        inc2 = incmatrix.copy().scale(0.8/0.7).next_to(d2, RIGHT).shift(RIGHT * 0.4)

        self.play(Transform(ordermatrix, order2), Transform(dmatrix, d2), Transform(incmatrix, inc2),
                  equal.animate.next_to(order2, RIGHT), comp.animate.next_to(d2, RIGHT))
        self.wait()

        signtex = MathTex('(-1)^{n - 1} =', '(-1)^{d}', r'\left((-1)^{\frac{n}{\gcd(n, d)} - 1}\right)^{\gcd(n, d)}')
        signtex.shift(DOWN)
        self.play(Write(signtex[0]))
        self.wait(0.5)
        self.play(Write(signtex[1]))
        self.wait()
        self.play(Write(signtex[2][1:-9]))
        self.wait(0.5)
        self.play(Write(signtex[2][0]), Write(signtex[2][-9:]))
        self.wait()
        new = MathTex('(-1)^{n - \gcd(n, d)}').align_to(signtex[2][1], DL)
        exponent = signtex[2][-8:]
        exponent1 = exponent.copy()
        exponent2 = exponent.copy()
        self.play(Unwrite(exponent), Unwrite(signtex[2][0]), Unwrite(signtex[2][-9]),
                  ReplacementTransform(VGroup(signtex[2][5:15], exponent1), new[0][4]),
                  ReplacementTransform(signtex[2][15], new[0][5]),
                  ReplacementTransform(VGroup(signtex[2][16], exponent2), new[0][6:]))
        self.remove(signtex[2])
        self.add(new)
        self.wait()

        merge = MathTex('(-1)^{n - 1} = ', '(-1)^{d + n - \gcd(n, d)}').shift(DOWN)
        self.play(ReplacementTransform(signtex[0], merge[0]),
                  ReplacementTransform(VGroup(signtex[1:], new), merge[1]))
        self.wait()

        result = MathTex('d - \gcd(n, d) \equiv 1 \pmod{2}').shift(DOWN * 2)
        self.play(Write(result))

        self.wait()



from manim import *
import math

class Chessboard(Scene):
    def construct(self):
        invariant = Tex("Invariant").scale(3)
        self.wait()
        self.play(Write(invariant))
        self.wait()

        ivory = ManimColor([255, 234, 176])
        grid = VGroup()
        xgrid = RIGHT * 7 / 8
        ygrid = DOWN * 7 / 8
        for i in range(8):
            for j in range(8):
                grid.add(Rectangle(width=7/8, height=7/8).shift((i - 3.5) * xgrid + (j - 3.5) * ygrid))
        self.wait()
        self.play(Unwrite(invariant), AnimationGroup(*[Create(grid[i]) for i in range(64)], lag_ratio=0.05, run_time=2))
        self.play(FadeOut(grid[0]), FadeOut(grid[-1]))
        self.wait(0.5)
        # 67 domino of doom
        domino = VGroup(
            RoundedRectangle(width=13/8, height=3/4, corner_radius=0.15, color=ivory, fill_opacity=1),
            Line(color=BLACK, start=UP * 5/16, end = DOWN * 5/16, stroke_width=6))
        for i in range(6):
            domino.add(Dot(color=BLACK).shift(LEFT * (1/4 if i < 3 else 5/8) + UP * 1/4  * (i % 3 - 1)))
        for i in range(6):
            domino.add(Dot(color=BLACK).shift([7/16 + 1/4 * math.cos(i * PI / 3 + PI / 6), 1/4 * math.sin(i * PI / 3 + PI / 6), 0]))
        domino.add(Dot(color=BLACK).shift(RIGHT * 7/16))
        hor = domino.copy().shift(UP * 7/16 - 3 * ygrid - 3 * xgrid).set_z_index(10)
        ver = domino.copy().rotate(-PI / 2).shift(-3 * ygrid + LEFT * 7/16 - 3 * xgrid).set_z_index(10)

        dominoes = VGroup()

        dominoes.add(hor.copy().shift(xgrid * 3), ver.copy().shift(xgrid * 5), ver.copy().shift(xgrid * 7 + ygrid),
                     hor.copy().shift(xgrid * 5 + ygrid * 2), hor.copy().shift(xgrid * 3 + ygrid * 2),
                     hor.copy().shift(ygrid), hor.copy().shift(xgrid * 2 + ygrid), ver.copy().shift(ygrid * 2),
                     ver.copy().shift(ygrid * 5), hor.copy().shift(ygrid * 7), hor.copy().shift(ygrid * 5 + xgrid * 2),
                     hor.copy().shift(ygrid * 4 + xgrid), hor.copy().shift(ygrid * 3 + xgrid),
                     ver.copy().shift(xgrid * 4 + ygrid * 4), hor.copy().shift(ygrid * 4 + xgrid * 5),
                     ver.copy().shift(xgrid * 7 + ygrid * 3), ver.copy().shift(xgrid * 6 + ygrid * 5),
                     hor.copy().shift(xgrid * 5 + ygrid * 7), ver.copy().shift(ygrid * 6 + xgrid * 4),
                     hor.copy().shift(xgrid * 2 + ygrid * 7), hor.copy().shift(xgrid + ygrid * 6),
                     hor.copy().shift(xgrid * 3 + ygrid * 3), hor.copy().shift(xgrid + ygrid * 2),
                     hor.copy().shift(xgrid), hor.copy().shift(xgrid * 6), hor.copy().shift(xgrid * 5 + ygrid * 3),
                     ver.copy().shift(xgrid * 5 + ygrid * 5), ver.copy().shift(ygrid * 5 + xgrid * 7))
        self.play(AnimationGroup(*[FadeIn(dominoes[i]) for i in range(len(dominoes))], lag_ratio=0.1))
        self.wait()
        colored = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    colored.append(i * 8 + j)
        self.play(FadeOut(dominoes))
        self.play(AnimationGroup(*[grid[i].animate.set_fill(color=WHITE, opacity=1) for i in colored], lag_ratio=0.05))
        self.wait()
        dominoes.set_opacity(0.2)
        self.play(FadeIn(dominoes))
        self.wait()

class Ants(Scene):
    def construct(self):
        grid = NumberPlane(
            x_range=[0, 5.2, 1],
            y_range=[0, 5.2, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
            }
        )

        speed = 0.5
        def updater1(mob, dt):
            mob.shift(RIGHT * speed * dt if mob.get_left()[0] <= 2.8 else LEFT * 0.4)
        def updater2(mob, dt):
            mob.shift(UP * speed * dt if mob.get_bottom()[1] <= 2.8 else DOWN * 0.4)
        def updater3(mob, dt):
            mob.shift(RIGHT * speed * dt if mob.get_left()[0] <= -0.2 else LEFT * 0.4)

        def hline(col, width, offset):
            line = DashedLine(ORIGIN, RIGHT, dash_length=0.2, stroke_color=col, stroke_width=width)
            line.add_updater(updater1).shift(RIGHT * offset)
            return line

        def vline(col, width, offset):
            line = DashedLine(ORIGIN, UP, dash_length=0.2, stroke_color=col, stroke_width=width)
            line.add_updater(updater2).shift(UP * offset)
            return line

        horizontal = VGroup([hline(TEAL, 4, i * 0.06 - 0.1).shift(UP * (2.4 - i) + RIGHT * 2.4) for i in range(5)] +
                           [hline(WHITE, 3, 0.2).shift(DOWN * 2.6 + RIGHT * 2.4)])
        vertical = VGroup([vline(TEAL, 4, i * 0.06 - 0.1).shift(RIGHT * (2.4 - i) + UP * 2.4) for i in range(5)] +
                            [vline(WHITE, 3, 0.2).shift(LEFT * 2.6 + UP * 2.4)])
        lines = VGroup(horizontal, vertical)

        mask = VGroup()
        rect = Rectangle(width=3, height=10, color=BLACK, fill_opacity=1).shift(RIGHT * 4.6)
        mask.add(rect)
        rect = Rectangle(width=10, height=3, color=BLACK, fill_opacity=1).shift(UP * 4.6)
        mask.add(rect).set_z_index(10)
        self.add(mask)

        ant = ImageMobject("ant.png").rotate(-PI / 4).scale(0.16).shift(LEFT * 2.1 + DOWN * 2.1)
        stuff = VGroup(grid, lines, mask)
        self.add(stuff)
        # self.add(mask)
        self.wait(0.5)
        # self.play(Create(grid))
        self.play(FadeIn(ant))
        # self.wait(4)
        # self.play(FadeIn(lines))
        self.wait(10)
        weight = MathTex("1", font_size=60).move_to(ant.get_center())
        self.play(FadeOut(ant), FadeIn(weight))
        self.wait(2)

        # ants = Group()
        # ants.add(ant)
        # ants.add(ants[0].copy())
        # self.play(ants[0].animate.shift(UP), ants[1].animate.shift(RIGHT))
        # self.wait()
        # ants.add(ants[1].copy())
        # self.play(ants[1].animate.shift(UP), ants[2].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[2].copy())
        # self.play(ants[2].animate.shift(UP), ants[3].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[2].copy())
        # self.play(ants[2].animate.shift(UP), ants[4].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[2].copy())
        # self.play(ants[2].animate.shift(UP), ants[5].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[1].copy())
        # self.play(ants[1].animate.shift(UP), ants[6].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[5].copy())
        # self.play(ants[5].animate.shift(UP), ants[7].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[1].copy())
        # self.play(ants[1].animate.shift(UP), ants[8].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[5].copy())
        # self.play(ants[5].animate.shift(UP), ants[9].animate.shift(RIGHT), run_time=0.8)
        # ants.add(ants[2].copy())
        # self.play(ants[2].animate.shift(UP), ants[10].animate.shift(RIGHT), run_time=0.8)
        # self.wait()
        #
        # yhor = Rectangle(color=YELLOW, fill_opacity=1, width=1, height=2).shift(DOWN * 1.6 + LEFT * 0.1)
        # yver = Rectangle(color=YELLOW, fill_opacity=1, width=2, height=1).shift(DOWN * 0.1 + LEFT * 1.6)
        # ysquare = Rectangle(color=YELLOW, fill_opacity=1, width=2, height=2).shift(LEFT * 1.6 + DOWN * 1.6)
        # target = VGroup(yhor, yver, ysquare).set_opacity(0.5).set_z_index(-2)
        # self.play(FadeIn(target))
        # self.wait(10)

        weights = VGroup()
        weights.add(weight)
        weights.add(weight.copy())
        self.play(Transform(weights[0], MathTex(r"\frac{1}{2}", font_size=32).shift(LEFT * 2.1 + DOWN * 1.1)),
                  Transform(weights[1], MathTex(r"\frac{1}{2}", font_size=32).shift(LEFT * 1.1 + DOWN * 2.1)))
        weights.add(weights[1].copy())
        self.play(Transform(weights[1], MathTex(r"\frac{1}{4}", font_size=32).shift(LEFT * 1.1 + DOWN * 1.1)),
                  Transform(weights[2], MathTex(r"\frac{1}{4}", font_size=32).shift(LEFT * 0.1 + DOWN * 2.1)))
        weights.add(weights[2].copy())
        self.play(Transform(weights[2], MathTex(r"\frac{1}{8}", font_size=32).shift(LEFT * 0.1 + DOWN * 1.1)),
                  Transform(weights[3], MathTex(r"\frac{1}{8}", font_size=32).shift(RIGHT * 0.9 + DOWN * 2.1)))
        weights.add(weights[2].copy())
        self.play(Transform(weights[2], MathTex(r"\frac{1}{16}", font_size=32).shift(LEFT * 0.1 + DOWN * 0.1)),
                  Transform(weights[4], MathTex(r"\frac{1}{16}", font_size=32).shift(RIGHT * 0.9 + DOWN * 1.1)))
        self.wait()
        xcoords = VGroup([Text(str(i), font_size=32, font='JetBrains Mono').shift(DOWN * 3.1 + RIGHT * (i - 2.1)) for i in range(5)])
        ycoords = VGroup([Text(str(i), font_size=32, font='JetBrains Mono').shift(LEFT * 3.1 + UP * (i - 2.1)) for i in range(5)])
        self.play(Write(xcoords), Write(ycoords))

        fullweights = VGroup()
        for i in range(5):
            for j in range(5):
                tex = r"\frac{1}{2^" + str(i + j) + "}"
                fullweights.add(MathTex(tex, font_size=36).shift(RIGHT * (i - 2.1) + UP * (j - 2.1)))
        self.play(FadeOut(weights))
        self.play(AnimationGroup(*[Write(fullweights[i]) for i in range(25)], lag_ratio=0.1))
        self.wait(2)
        self.play(stuff.animate.shift(LEFT * 3), xcoords.animate.shift(LEFT * 3), ycoords.animate.shift(LEFT * 3),
                  fullweights.animate.shift(LEFT * 3))
        for i in range(6):
            lines[0][i].remove_updater(updater1)
            lines[0][i].add_updater(updater3)
        self.wait()
        working = VGroup(MathTex(r"S =", r"\sum_{x\geq 0} \sum_{y\geq 0} \frac{1}{2^{x + y}"),
                         MathTex("=", r"\left(\sum_{x\geq 0}\frac{1}{2^x} \right)", r"\left(\sum_{y\geq 0}\frac{1}{2^y} \right)"),
                         MathTex("=", "2", "\cdot", "2")).arrange(DOWN).shift(RIGHT * 3 + UP * 1).set_z_index(100)
        self.play(Write(working[0]))
        working[1][0].align_to(working[0][0], RIGHT)
        working[1][1:].align_to(working[0][1], LEFT)
        self.play(AnimationGroup(Write(working[1][0]), Transform(working[0][1].copy(), working[1][1]),
                                 Transform(working[0][1].copy(), working[1][2]), lag_ratio=0.2))
        working[2][0].align_to(working[1][0], RIGHT)
        working[2][1:].align_to(working[1][1], LEFT)
        self.play(AnimationGroup(Write(working[2][0]), ReplacementTransform(working[1][1].copy(), working[2][1]),
                                 Write(working[2][2]), ReplacementTransform(working[1][2].copy(), working[2][3]), lag_ratio=0.2))
        ans = MathTex("4").move_to(working[2][1]).set_z_index(100)
        self.play(Transform(working[2][1:], ans))
        self.wait(2)
        yhor = Rectangle(color=YELLOW, fill_opacity=1, width=1, height=2).shift(DOWN * 1.6 + LEFT * 3.1)
        yver = Rectangle(color=YELLOW, fill_opacity=1, width=2, height=1).shift(DOWN * 0.1 + LEFT * 4.6)
        ysquare = Rectangle(color=YELLOW, fill_opacity=1, width=2, height=2).shift(LEFT * 4.6 + DOWN * 1.6)
        target = VGroup(yhor, yver, ysquare).set_opacity(0.5).set_z_index(-2)
        self.play(FadeIn(target))
        self.wait()
        yellowsum = MathTex(r"\frac{1}{1} + \frac{2}{2} + \frac{3}{4} + \frac{2}{8} = 3").shift(DOWN * 2)
        yellowsum.set_color(YELLOW).set_z_index(10).align_to(working, LEFT)
        self.play(Write(yellowsum))
        self.wait(10)


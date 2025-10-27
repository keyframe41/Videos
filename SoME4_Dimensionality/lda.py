from manim import *
import math
import numpy as np
import matplotlib.pyplot as plt

class Introduce(Scene):
    def FetchData(self):
        class1 = []
        class2 = []
        with open("ldaDataset.txt", "r") as file:
            lineIndex = 1
            for line in file:
                if lineIndex <= 50:
                    class1.append(list(map(float, line.split())))
                else:
                    class2.append(list(map(float, line.split())))
                lineIndex += 1

        return np.array(class1), np.array(class2)

    def construct(self):
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=7,
            y_length=7,
            axis_config={
                "stroke_width" : 2,
                "tip_width" : 0.25,
            }
        )

        self.play(Create(axes))

        c1, c2 = self.FetchData()
        dotsAll = VGroup(*[Dot(point=axes.c2p(c1[i][0], c1[i][1]), color=YELLOW) for i in range(len(c1))],
                         *[Dot(point=axes.c2p(c2[i][0], c2[i][1]), color=BLUE) for i in range(len(c2))])
        dotsAll.set_z_index(10)
        self.play(AnimationGroup(*[FadeIn(dotsAll[i]) for i in range(80)], lag_ratio=0.01))
        self.wait(0.5)

        projAngle = ValueTracker(0)
        def getLine():
            line = axes.plot(lambda x : x * math.tan(projAngle.get_value()), stroke_width=4, x_range=[-4, 4])
            line.set_z_index(1).set_color(GREEN)
            return line
        def getProjectedDots(dots):
            projDots = VGroup().set_z_index(10)
            wx, wy = math.cos(projAngle.get_value()), math.sin(projAngle.get_value())
            for dot in dots:
                x, y = axes.p2c(dot.get_center())
                mag = x * wx + y * wy
                projDots.add(*Dot(point=axes.c2p(wx * mag, wy * mag), color=dot.color, fill_opacity=0.3))
            return projDots


        line = always_redraw(lambda: getLine())
        projDots = always_redraw(lambda: getProjectedDots(dotsAll))
        projDots.set_z_index(100)
        self.play(Create(line))
        self.wait(0.5)
        self.play(FadeTransform(dotsAll.copy(), projDots))
        self.wait()
        self.play(projAngle.animate.set_value(PI / 3 - 0.2))
        self.wait(0.5)
        self.play(projAngle.animate.set_value(PI / 6))
        self.wait(0.5)
        self.play(projAngle.animate.set_value(-PI / 8))
        self.wait(0.5)

        loc = np.array([np.mean(c1, axis=0), np.mean(c2, axis=0), np.mean(c1, axis=0) * 0.625 + np.mean(c2, axis=0) * 0.375])
        centroids = VGroup()
        self.wait(0.5)
        colors = [YELLOW, BLUE, GREEN]
        for i in range(3):
            centroids.add(Circle(color=colors[i], stroke_width=5, fill_color=BLACK, fill_opacity=1).scale(0.1).move_to(axes.c2p(loc[i][0], loc[i][1])))
        centroids.set_z_index(100)
        self.play(FadeIn(centroids))

        def getProjectedCentroids():
            wx, wy = math.cos(projAngle.get_value()), math.sin(projAngle.get_value())
            projCentroids = VGroup()
            for i in range(3):
                mag = loc[i][0] * wx + loc[i][1] * wy
                projCentroids.add(Circle(color=colors[i], stroke_width=5, fill_color=BLACK, fill_opacity=1).scale(0.1).move_to(axes.c2p(wx * mag, wy * mag)))
            return projCentroids.set_z_index(100)
        projCentroids = always_redraw(lambda: getProjectedCentroids())
        self.play(ReplacementTransform(centroids.copy(), projCentroids), FadeOut(projDots), dotsAll.animate.set_opacity(0.3))
        self.wait()
        self.play(axes.animate.shift(LEFT * 32/9), dotsAll.animate.shift(LEFT * 32/9), centroids.animate.shift(LEFT * 32/9))
        self.wait(0.5)

        globalLabels = VGroup(Tex("$m_1$").next_to(centroids[0], DOWN),
                              Tex("$m_2$").next_to(centroids[1], UP),
                              Tex("$m$").next_to(centroids[2], DOWN))
        globalLabels.set_color(BLUE)
        self.play(Write(globalLabels))
        projLabels = VGroup(Tex("$\mu_1$").next_to(projCentroids[0], UP),
                              Tex("$\mu_2$").next_to(projCentroids[1], DOWN),
                              Tex("$\mu$").next_to(projCentroids[2], UP + RIGHT * 0.2))
        projLabels.set_color(TEAL)
        self.play(Write(projLabels))
        variableText = VGroup(Tex("Number of classes = $c$"),
                              Tex("Number of data points = $n$"),
                              Tex("Projection vector = $w$ (again)")).scale(0.6)
        variableText.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 32/9 + UP * 3)
        variableText[2][0][-8].set_color(YELLOW)
        self.play(Write(variableText))
        self.wait(0.5)
        hLine = Line(start=ORIGIN, end=ORIGIN + RIGHT * 6).next_to(variableText, DOWN)
        self.play(Write(hLine))
        title = Text("Variance of Projected Means", font_size=40).next_to(hLine, DOWN)
        self.play(Write(title))
        self.wait(0.5)

        magTex = VGroup(MathTex("\sum_{i = 1}^c", "n_i", "\|", "\mu_i", "-", "\mu", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "n_i", "\|", "w^T", "m_i", "-", "w^T", "m", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "n_i", "\|", "w^T(m_i - m)", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "n_i", "(", "w^T(m_i - m)", ")^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "n_i", "(w^T(m_i - m))", "(w^T(m_i - m))^T", font_size=36),
                        MathTex("\sum_{i = 1}^c", "n_i", "w^T", "(m_i - m)", "(m_i - m)^T", "w", font_size=36),
                        MathTex("w^T", "S_b", "w", font_size=36))

        magTex.arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN)
        # skull emoji
        magTex[2:].align_to(magTex[1], UP)
        magTex[4].align_to(magTex[3], UP)
        magTex[5:].align_to(magTex[3], UP)

        magTex[0][3].set_color(TEAL)
        magTex[0][5].set_color(TEAL)
        for i in [3, 6]:
            magTex[1][i].set_color(YELLOW)
            magTex[1][i + 1].set_color(BLUE)

        magTex[2][3][0:2].set_color(YELLOW)
        magTex[2][3][3:5].set_color(BLUE)
        magTex[2][3][6].set_color(BLUE)

        magTex[3][3][0:2].set_color(YELLOW)
        magTex[3][3][3:5].set_color(BLUE)
        magTex[3][3][6].set_color(BLUE)
        for i in [2, 3]:
            magTex[4][i][1:3].set_color(YELLOW)
            magTex[4][i][4:6].set_color(BLUE)
            magTex[4][i][7].set_color(BLUE)

        magTex[5][2].set_color(YELLOW)
        for i in [3, 4]:
            magTex[5][i][1:3].set_color(BLUE)
            magTex[5][i][4].set_color(BLUE)
        magTex[5][5].set_color(YELLOW)
        magTex[6][0].set_color(YELLOW)
        magTex[6][1].set_color(BLUE)
        magTex[6][2].set_color(YELLOW)
        self.play(Write(magTex[0]))
        self.wait(0.5)
        self.play(FadeIn(magTex[1][:2], shift=DOWN), ReplacementTransform(magTex[0][2:].copy(), magTex[1][2:]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[1][:3], magTex[2][:3]), ReplacementTransform(magTex[1][3], magTex[2][3][:2]),
                  ReplacementTransform(VGroup(magTex[1][4:6], magTex[1][7]), magTex[2][3][2:]), ReplacementTransform(magTex[1][-1], magTex[2][-1]),
                  FadeOut(magTex[1][6], shift=LEFT))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[2].copy(), magTex[3]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[3][:2], magTex[4][:2]),
                  FadeTransform(magTex[3][2:], magTex[4][2]),
                  FadeTransform(magTex[3][2:].copy(), magTex[4][3]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[4][:2], magTex[5][:2]),
                  ReplacementTransform(magTex[4][2][1:3], magTex[5][2]), ReplacementTransform(magTex[4][2][3:-1], magTex[5][3]),
                  ReplacementTransform(magTex[4][3][1:3], magTex[5][5]), FadeTransform(magTex[4][3][3:-2], magTex[5][4]), ReplacementTransform(magTex[4][3][-1], magTex[5][4][-1]),
                  FadeOut(magTex[4][2][0], magTex[4][2][-1], magTex[4][3][0], magTex[4][3][-2]))
        self.wait(0.5)

        temp1 = magTex[5][0].copy()
        temp2 = magTex[5][2].copy()
        self.play(magTex[5][0:2].animate.align_to(temp2, RIGHT), magTex[5][2].animate.align_to(temp1, LEFT))
        self.wait(0.5)
        self.play(Write(magTex[6]))
        self.wait()

        self.play(FadeOut(variableText, title, hLine, magTex[0], magTex[2], magTex[5:], shift=RIGHT),
                  axes.animate.center(), dotsAll.animate.shift(RIGHT * 32 / 9), centroids.animate.shift(RIGHT * 32 / 9),
                  projLabels.animate.shift(RIGHT * 32 / 9), globalLabels.animate.shift(RIGHT * 32 / 9))
        self.wait()
        newDots = VGroup(*[Dot(point=axes.c2p(c1[i][0] + c1[i][1], c1[i][1]), color=YELLOW) for i in range(len(c1))],
                         *[Dot(point=axes.c2p(c2[i][0] + c2[i][1], c2[i][1]), color=BLUE) for i in range(len(c2))]).set_opacity(0.5)
        dotsAll2 = dotsAll.copy()
        self.add(dotsAll2)
        self.remove(dotsAll)
        self.play(ReplacementTransform(dotsAll2, newDots))
        self.wait(0.5)
        projDots = getProjectedDots(newDots)
        self.play(ReplacementTransform(newDots.copy(), projDots))
        self.wait()
        self.play(FadeOut(projDots))
        self.play(ReplacementTransform(newDots, dotsAll))
        self.wait(0.5)
        self.play(axes.animate.shift(LEFT * 32 / 9), dotsAll.animate.shift(LEFT * 32 / 9), centroids.animate.shift(LEFT * 32 / 9),
                  projLabels.animate.shift(LEFT * 32 / 9), globalLabels.animate.shift(LEFT * 32 / 9),
                  FadeIn(variableText, title, hLine, magTex[0], magTex[2], magTex[5:], shift=LEFT))
        self.wait()

        self.play(Transform(title, Text("Variance of Projected Classes", font_size=40).next_to(hLine, DOWN)))
        self.wait(0.5)
        self.play(FadeOut(magTex[0], shift=UP), FadeOut(magTex[2], shift=UP), FadeOut(magTex[5:], shift=UP))
        magTex = VGroup(MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "\|", "w^Tx_j", "-", "\mu_i", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "\|", "w^T", "x_j", "-", "w^T", "m_i", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "\|", "w^T(x_j - m_i)", "\|^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "(", "w^T(x_j - m_i)", ")^2", font_size=36),
                        MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "(w^T(x_j - m_i))", "(w^T(x_j - m_i))^T", font_size=36),
                        MathTex("\sum_{i = 1}^c", "\sum_{x_j\in c_i}", "w^T", "(x_j - m_i)", "(x_j - m_i)^T", "w", font_size=36),
                        MathTex("w^T", "S_w", "w", font_size=36))

        magTex.arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN)
        # skull emoji 2
        magTex[2:].align_to(magTex[1], UP)
        magTex[4].align_to(magTex[3], UP)
        magTex[5:].align_to(magTex[3], UP)
        for i in range(6):
            magTex[i][1][1:3].set_color(BLUE)
        magTex[0][3][:2].set_color(YELLOW)
        magTex[0][3][2:].set_color(BLUE)
        for i in [3, 6]:
            magTex[1][i].set_color(YELLOW)
            magTex[1][i + 1].set_color(BLUE)
        magTex[0][5].set_color(TEAL)

        magTex[2][3][0:2].set_color(YELLOW)
        magTex[2][3][3:5].set_color(BLUE)
        magTex[2][3][6:8].set_color(BLUE)

        magTex[3][3][0:2].set_color(YELLOW)
        magTex[3][3][3:5].set_color(BLUE)
        magTex[3][3][6:8].set_color(BLUE)

        for i in [2, 3]:
            magTex[4][i][1:3].set_color(YELLOW)
            magTex[4][i][4:6].set_color(BLUE)
            magTex[4][i][7:9].set_color(BLUE)

        magTex[5][2].set_color(YELLOW)
        for i in [3, 4]:
            magTex[5][i][1:3].set_color(BLUE)
            magTex[5][i][4:6].set_color(BLUE)
        magTex[5][5].set_color(YELLOW)
        magTex[6][0].set_color(YELLOW)
        magTex[6][1].set_color(BLUE)
        magTex[6][2].set_color(YELLOW)
        self.play(Write(magTex[0]))
        self.wait(0.5)
        self.play(FadeIn(magTex[1][:5], shift=DOWN), ReplacementTransform(magTex[0][5:].copy(), magTex[1][5:]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[1][:3], magTex[2][:3]),
                  ReplacementTransform(magTex[1][3], magTex[2][3][:2]),
                  ReplacementTransform(VGroup(magTex[1][4:6], magTex[1][7]), magTex[2][3][2:]),
                  ReplacementTransform(magTex[1][-1], magTex[2][-1]),
                  FadeOut(magTex[1][6], shift=LEFT))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[2].copy(), magTex[3]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[3][:2], magTex[4][:2]),
                  FadeTransform(magTex[3][2:], magTex[4][2]),
                  FadeTransform(magTex[3][2:].copy(), magTex[4][3]))
        self.wait(0.5)
        self.play(ReplacementTransform(magTex[4][:2], magTex[5][:2]),
                  ReplacementTransform(magTex[4][2][1:3], magTex[5][2]),
                  ReplacementTransform(magTex[4][2][3:-1], magTex[5][3]),
                  ReplacementTransform(magTex[4][3][1:3], magTex[5][5]),
                  FadeTransform(magTex[4][3][3:-2], magTex[5][4]),
                  ReplacementTransform(magTex[4][3][-1], magTex[5][4][-1]),
                  FadeOut(magTex[4][2][0], magTex[4][2][-1], magTex[4][3][0], magTex[4][3][-2]))
        self.wait(0.5)
        temp1 = magTex[5][0].copy()
        temp2 = magTex[5][2].copy()
        self.play(magTex[5][0:2].animate.align_to(temp2, RIGHT), magTex[5][2].animate.align_to(temp1, LEFT))
        self.wait(0.5)
        self.play(Write(magTex[6]))
        self.wait()


class Maximize(Scene):
    def construct(self):
        centroidVarText = Tex("Maximize: variance of projected centroids $=$ ", "$w^TS_bw$").to_edge(UP)
        classVarText = Tex("Minimize: total variance of projected classes $=$ ", "$w^TS_ww$").next_to(centroidVarText, DOWN)
        centroidVarText[1][0:2].set_color(YELLOW)
        centroidVarText[1][2:4].set_color(BLUE)
        centroidVarText[1][4].set_color(YELLOW)
        classVarText[1][0:2].set_color(YELLOW)
        classVarText[1][2:4].set_color(BLUE)
        classVarText[1][4].set_color(YELLOW)
        self.play(AnimationGroup(Write(centroidVarText), Write(classVarText), lag_ratio=0.2))

        function = MathTex("F(w) = ", r"\frac{w^TS_bw}{w^TS_ww}").shift(UP * 1.25)
        function[1][0:2].set_color(YELLOW)
        function[1][2:4].set_color(BLUE)
        function[1][4].set_color(YELLOW)
        function[1][6:8].set_color(YELLOW)
        function[1][8:10].set_color(BLUE)
        function[1][10].set_color(YELLOW)
        self.wait()
        self.play(ReplacementTransform(centroidVarText[1].copy(), function[1][:5]),
                  ReplacementTransform(classVarText[1].copy(), function[1][6:]),
                  Write(function[1][5]), Write(function[0]))
        self.wait()

        derivative = MathTex(r"\frac{dF}{dw} = ", r"\frac{(w^TS_ww)(2S_bw) - (w^TS_bw)(2S_ww)}{(w^TS_ww)^2}", "= 0").shift(DOWN * 0.5)
        derivative[0][4].set_color(YELLOW)
        derivative[1][1:3].set_color(YELLOW)
        derivative[1][3:5].set_color(BLUE)
        derivative[1][5].set_color(YELLOW)
        derivative[1][9:11].set_color(BLUE)
        derivative[1][11].set_color(YELLOW)
        derivative[1][15:17].set_color(YELLOW)
        derivative[1][17:19].set_color(BLUE)
        derivative[1][19].set_color(YELLOW)
        derivative[1][23:25].set_color(BLUE)
        derivative[1][25].set_color(YELLOW)
        derivative[1][29:31].set_color(YELLOW)
        derivative[1][31:33].set_color(BLUE)
        derivative[1][33].set_color(YELLOW)
        self.play(Write(derivative[:2]))
        self.play(Write(derivative[2]))
        self.wait()

        simplify = MathTex("(w^TS_ww)", "(2S_bw)", "-", "(w^TS_bw)", "(2S_ww)", "= 0").shift(DOWN * 2)
        for i in [0, 3]:
            simplify[i][1:3].set_color(YELLOW)
            simplify[i][3:5].set_color(BLUE)
            simplify[i][5].set_color(YELLOW)
            simplify[i + 1][2:4].set_color(BLUE)
            simplify[i + 1][4].set_color(YELLOW)
        self.play(ReplacementTransform(derivative[1][0:7].copy(), simplify[0]),
                  ReplacementTransform(derivative[1][7:13].copy(), simplify[1]),
                  ReplacementTransform(derivative[1][13].copy(), simplify[2]),
                  ReplacementTransform(derivative[1][14:21].copy(), simplify[3]),
                  ReplacementTransform(derivative[1][21:27].copy(), simplify[4]),
                  ReplacementTransform(derivative[2].copy(), simplify[5]))
        self.wait()
        self.play(simplify[5][0].animate.move_to(simplify[2]), FadeOut(simplify[2], simplify[5][1]))
        self.wait()
        frac = function[1].copy().move_to(simplify[3])
        func = function[0][:4].copy().move_to(simplify[3])
        self.play(FadeOut(simplify[0][0], simplify[0][-1], simplify[3][0], simplify[3][-1]),
                  ReplacementTransform(simplify[3][1:-1], frac[:5]),
                  ReplacementTransform(simplify[0][1:-1], frac[6:11]),
                  Write(frac[5]))
        self.wait(0.5)
        self.play(ReplacementTransform(frac, func))
        self.wait(0.5)
        self.play(FadeOut(simplify[1][:2], simplify[1][-1], simplify[4][:2], simplify[4][-1]))
        self.wait(0.5)
        inv = MathTex("S_w^{-1}").next_to(simplify[1][2], LEFT, buff=SMALL_BUFF).set_color(BLUE)
        self.play(ReplacementTransform(simplify[4][2:4], inv))
        self.wait()

        simplified = MathTex("S_w^{-1}S_bw", "=", "F(w)", "w").shift(DOWN * 2)
        simplified[0][:6].set_color(BLUE)
        simplified[0][6].set_color(YELLOW)
        simplified[3].set_color(YELLOW)
        self.play(FadeTransform(inv, simplified[0][:4]),
                  ReplacementTransform(simplify[1][2:5], simplified[0][4:]),
                  ReplacementTransform(simplify[5][0], simplified[1]),
                  ReplacementTransform(func, simplified[2]),
                  ReplacementTransform(simplify[4][4], simplified[3]))
        self.wait()

class Dependent(Scene):
    def construct(self):
        definition = MathTex("S_b = ", "\sum_j n_j(m_j - m)(m_j - m)^T").shift(UP * 2.5)
        definition[0][0:2].set_color(BLUE)
        definition[1][5:7].set_color(BLUE)
        definition[1][8].set_color(BLUE)
        definition[1][11:13].set_color(BLUE)
        definition[1][14].set_color(BLUE)
        mats = VGroup(Matrix([["\sqrt{n_j}(m_j - m)", "\cdots"]], h_buff=1), Matrix([["\sqrt{n_j}(m_j - m)^T"], [r"\vdots"]]))
        mats.arrange(RIGHT)
        temp = mats[0].get_entries()
        temp[0][0][5:7].set_color(BLUE)
        temp[0][0][8].set_color(BLUE)
        temp[1].next_to(temp[0], RIGHT).shift(RIGHT * 0.2)
        temp = mats[1].get_entries()
        temp[0][0][5:7].set_color(BLUE)
        temp[0][0][8].set_color(BLUE)
        temp[1].next_to(temp[0], DOWN).shift(DOWN * 0.2)
        mats.shift(UP * 0.4)
        self.play(Write(definition))
        self.play(Write(mats))
        self.wait(0.5)
        text = Text("This has linearly dependent columns").shift(UP * 1.5)
        self.play(FadeOut(mats[1]), mats[0].animate.set_x(0), FadeIn(text))
        self.wait()
        math = MathTex("\sum_j \sqrt{n_j}(\sqrt{n_j}(m_j - m))", "= \sum_j n_j(m_j - m)").shift(DOWN)
        math[0][12:14].set_color(BLUE)
        math[0][15].set_color(BLUE)
        math[1][6:8].set_color(BLUE)
        math[1][9].set_color(BLUE)
        math2 = MathTex("=\sum_j n_jm_j - m\sum_j n_j", "= mn - mn = 0").shift(DOWN * 2.5)
        math2[0][5:7].set_color(BLUE)
        math2[0][8].set_color(BLUE)
        math2[1][1].set_color(BLUE)
        math2[1][4].set_color(BLUE)
        self.play(Write(math))
        self.play(Write(math2))

class LDAres(Scene):
    def construct(self):
        points = [VGroup() for i in range(10)]
        with open("ldaResult.txt", "r") as file:
            lines = file.readlines()
        cmap = plt.get_cmap('hsv')
        for i in range(2000):
            data = lines[i].split()
            points[int(data[2])].add(Dot(point=(float(data[0]) / 1.5, float(data[1]) / 1.5, 0), color=ManimColor(cmap(int(data[2]) / 10)),
                           radius=0.05, fill_opacity=0.8))
        key = VGroup()
        for i in range(10):
            key.add(Rectangle(width=0.2, height=0.2, fill_color=ManimColor(cmap(i / 10)), fill_opacity=1))
            key.add(MathTex(str(i)))
        key.arrange(RIGHT).to_edge(DOWN, buff=MED_SMALL_BUFF)
        self.add(key)
        self.wait()
        for i in range(10):
            # self.add(points[i])
            self.play(FadeIn(points[i]))
        self.wait()
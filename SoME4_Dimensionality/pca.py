from manim import *
import math
import numpy as np
import matplotlib.pyplot as plt

class ProjectLines(Scene):
    def FetchData(self):
        class1 = []
        class2 = []
        class3 = []
        with open("pcaDataset.txt", "r") as file:
            lineIndex = 1
            for line in file:
                if lineIndex <= 25:
                    class1.append(list(map(float, line.split())))
                elif lineIndex <= 75:
                    class2.append(list(map(float, line.split())))
                else:
                    class3.append(list(map(float, line.split())))
                lineIndex += 1

        return class1, class2, class3

    def construct(self):
        axes = Axes(
            x_range=[0, 6.5],
            y_range=[0, 5],
            x_length=6.5 * 1.3,
            y_length=5 * 1.3,

            axis_config={
                "stroke_width" : 4,
                # "include_ticks" : False,
                "tip_width" : 0.25,
            }
        )
        centeredAxes = Axes(
            x_range=[-2.5, 2.5],
            y_range=[-2.5, 2.5],
            x_length=7,
            y_length=7,
            axis_config={
                "stroke_width" : 4,
                # "include_ticks" : False,
                "tip_width": 0.25,
                "fill_opacity" : 0.75
            }
        )
        centeredAxes.set_z_index(-2)
        self.play(Create(axes))

        c1, c2, c3 = self.FetchData()
        dots1 = VGroup(*[Dot(point=axes.c2p(c1[i][0], c1[i][1]), color=GREEN_D) for i in range(len(c1))])
        dots2 = VGroup(*[Dot(point=axes.c2p(c2[i][0], c2[i][1]), color=RED_E) for i in range(len(c2))])
        dots3 = VGroup(*[Dot(point=axes.c2p(c3[i][0], c3[i][1]), color=BLUE_D) for i in range(len(c3))])
        dotsAll = VGroup()
        for i in dots1:
            dotsAll.add(i)
        for i in dots2:
            dotsAll.add(i)
        for i in dots3:
            dotsAll.add(i)
        self.play(LaggedStart(FadeIn(dots1), FadeIn(dots2), FadeIn(dots3), lag_ratio=0.5))
        self.add(dotsAll)
        self.remove(dots1, dots2, dots3)

        linearProjText = Text("Linear Projection")
        linearProjText.to_edge(UP)
        linearProjTextBg = BackgroundRectangle(linearProjText, color=BLACK)
        self.add(linearProjTextBg)
        self.play(Write(linearProjText), run_time=1.5)

        # projAngle = ValueTracker(PI / 4)
        projAngle = ValueTracker(-PI / 6)
        projCenter = [3.25, 2.5]
        def getLine(ax, center):
            cx, cy = center[0], center[1]
            line = ax.plot(lambda x : (x - cx) * math.tan(projAngle.get_value()) + cy, stroke_width=4, x_range=[-5, 10])
            line.set_z_index(-1)
            return line
        def getProjectedDots(ax, center, dots):
            projDots = VGroup()
            wx, wy = math.cos(projAngle.get_value()), math.sin(projAngle.get_value())
            cx, cy = center[0], center[1]
            for dot in dots:
                x, y = ax.p2c(dot.get_center())
                x -= cx
                y -= cy
                mag = x * wx + y * wy
                projDots.add(*Dot(point=ax.c2p(wx * mag + cx, wy * mag + cy), color=dot.color, fill_opacity=0.5))
            return projDots

        line = always_redraw(lambda: getLine(axes, projCenter))
        projDots = always_redraw(lambda: getProjectedDots(axes, projCenter, dotsAll))
        projDots.set_z_index(100)
        self.play(Write(line))
        self.wait(0.5)
        self.play(ReplacementTransform(dotsAll.copy(), projDots))
        self.wait()
        self.play(FadeOut(line, projDots))
        projAngle.set_value(PI / 6)
        self.wait(0.5)

        dotsMean = np.array([3.52869604, 2.7803617])
        dotsStdev = np.array([1.31264739, 1.035075])
        def switchAxes(x):
            dot = dotsAll[x]
            pos = (axes.p2c(dot.get_center()) - dotsMean) / dotsStdev
            return centeredAxes.c2p(pos[0], pos[1])
        self.play(FadeTransform(axes, centeredAxes),
                  AnimationGroup(dotsAll[i].animate.move_to(switchAxes(i)) for i in range(len(dotsAll))),
                  linearProjText.animate.to_corner(DL),
                  linearProjTextBg.animate.to_corner(DL))

        projCenter = [0, 0]
        line = always_redraw(lambda: getLine(centeredAxes, projCenter))
        projDots = always_redraw(lambda: getProjectedDots(centeredAxes, projCenter, dotsAll))
        projDots.set_z_index(100)
        self.play(FadeIn(line), FadeIn(projDots))
        self.wait()
        components = [[0.70710678, -0.70710678], [0.70710678, 0.70710678]]
        variance = [0.745986, 0.254014]
        for i in range(2):
            for j in range(2):
                components[i][j] *= variance[i] * 3
        pca = VGroup(Arrow(start=ORIGIN, end=centeredAxes.c2p(components[0][0], components[0][1]), color=YELLOW, buff=0, fill_opacity=0.5),
                     Arrow(start=ORIGIN, end=centeredAxes.c2p(components[1][0], components[1][1]), color=YELLOW, buff=0))
        self.play(Create(pca))
        self.wait()
        self.play(FadeOut(pca))

        singleDot = dotsAll[0].copy()
        singleProjDot = always_redraw(lambda: getProjectedDots(centeredAxes, projCenter, singleDot))
        self.add(singleDot, singleProjDot)
        self.play(FadeOut(dotsAll), FadeOut(projDots))
        dotLabel = Tex("$x_i$").next_to(singleDot, UP)
        projVector = Arrow(start=centeredAxes.c2p(0, 0), end=centeredAxes.c2p(math.cos(projAngle.get_value()), math.sin(projAngle.get_value())), color=YELLOW)
        projVectorLabel = Tex("$w$").next_to(projVector.get_end(), UP)
        self.play(FadeIn(dotLabel), FadeIn(projVector), FadeIn(projVectorLabel))
        self.wait()

class AnalyzePoint(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2.5, 2.5],
            y_range=[-2.5, 2.5],
            x_length=7,
            y_length=7,
            axis_config={
                "stroke_width": 4,
                # "include_ticks" : False,
                "tip_width": 0.25,
                "fill_opacity": 0.75
            }
        )
        axes.set_z_index(-2)
        self.add(axes)

        linearProjText = Text("Linear Projection")
        linearProjTextBg = BackgroundRectangle(linearProjText, color=BLACK)
        linearProjText.to_corner(DL),
        linearProjTextBg.to_corner(DL)
        self.add(linearProjTextBg, linearProjText)

        # projAngle = ValueTracker(PI / 4)
        projAngle = ValueTracker(PI / 6)
        projCenter = [3.25, 2.5]

        def getLine(ax, center):
            cx, cy = center[0], center[1]
            line = ax.plot(lambda x: (x - cx) * math.tan(projAngle.get_value()) + cy, stroke_width=4, x_range=[-2.5, 2.5])
            line.set_z_index(-1)
            return line

        def getProjectedDots(ax, center, dots):
            projDots = VGroup()
            wx, wy = math.cos(projAngle.get_value()), math.sin(projAngle.get_value())
            cx, cy = center[0], center[1]
            for dot in dots:
                x, y = ax.p2c(dot.get_center())
                x -= cx
                y -= cy
                mag = x * wx + y * wy
                projDots.add(*Dot(point=ax.c2p(wx * mag + cx, wy * mag + cy), color=dot.color, fill_opacity=0.75))
            return projDots

        projCenter = [0, 0]
        dotsMean = np.array([3.52869604, 2.7803617])
        dotsStdev = np.array([1.31264739, 1.035075])
        pos = np.array([1.3921584028938874, 4.17299717866506])
        stdPos = (pos - dotsMean) / dotsStdev
        dir = np.array([math.cos(projAngle.get_value()), math.sin(projAngle.get_value())])
        w = lambda mag: axes.c2p(mag * math.cos(projAngle.get_value()), mag * math.sin(projAngle.get_value()))
        # Initial vectors
        line = always_redraw(lambda: getLine(axes, projCenter))
        self.add(line)
        singleDot = always_redraw(lambda: Dot(point=axes.c2p(stdPos[0], stdPos[1]), color=BLUE))
        singleProjDot = always_redraw(lambda: getProjectedDots(axes, projCenter, singleDot))
        self.add(singleDot, singleProjDot)
        dotLabel = always_redraw(lambda: Tex("$x_i$", color=BLUE).next_to(singleDot, UP))
        dotVector = always_redraw(lambda: Arrow(start=axes.get_origin(), end=singleDot.get_center(), color=BLUE, buff=0, max_tip_length_to_length_ratio=0.15))
        dirVector =  always_redraw(lambda: Arrow(start=axes.get_origin(), end=w(1), color=YELLOW, buff=0, fill_opacity=0.75))
        dirVectorLabel = always_redraw(lambda: Tex("$w$", color=YELLOW).next_to(dirVector.get_end(), UP))
        self.wait(0.5)
        self.play(FadeIn(dotVector), FadeIn(dotLabel))
        self.wait(0.5)
        self.play(FadeIn(dirVector), FadeIn(dirVectorLabel))
        self.play(AnimationGroup(axes.animate.scale(0.8).to_edge(LEFT)))
        # Projected vector
        magnitude = np.dot(stdPos, dir)
        projVector = always_redraw(lambda: Arrow(start=axes.get_origin(), end=w(magnitude), color=YELLOW, buff=0))
        projMagnitudeText = always_redraw(lambda: Tex("$(w\cdot x_i) w$", font_size=28).next_to(projVector.get_end(), DOWN * 1.5))
        dummyGroup = VGroup(dotLabel.copy(), dirVectorLabel.copy())
        dotVectorCopy = dotVector.copy()
        self.add(dotVectorCopy)
        self.wait(0.5)

        vertLine = Line(start=DOWN * 4, end=UP * 4, stroke_width=2)
        self.play(ReplacementTransform(dotVectorCopy, projVector),
                  ReplacementTransform(dummyGroup, projMagnitudeText),
                  Create(vertLine))
        self.wait(0.5)

        minimizeText = Text("Maximize Variance", font_size=40)
        minimizeText.shift(RIGHT * 32 / 9).to_edge(UP, buff=MED_SMALL_BUFF)
        self.play(Write(minimizeText))

        varianceTex = VGroup()
        texStr = [r"\text{max}\left\{ \frac{1}{n} \sum_i (",
                  r"w", r"x_i",
                  r"\cdot", r")^2\right\}"]
        # First math stuff
        dummyTex = MathTex(texStr[0], texStr[1], "\cdot", texStr[2], r"- mean(", texStr[1], "\cdot", texStr[2], r")", texStr[4], font_size=28)
        dummyTex[1].set_fill(YELLOW)
        dummyTex[5].set_fill(YELLOW)
        dummyTex[3].set_fill(BLUE)
        dummyTex[7].set_fill(BLUE)
        varianceTex.add(dummyTex)

        dummyTex = MathTex(texStr[0], texStr[1], "\cdot", texStr[2], texStr[4], font_size=28)
        dummyTex[1].set_fill(YELLOW)
        dummyTex[3].set_fill(BLUE)
        varianceTex.add(dummyTex)

        varianceTex.arrange(DOWN).shift(RIGHT * 32 / 9 + UP * 3)
        varianceTex[0].move_to(varianceTex[1].get_center())
        self.play(Write(varianceTex[0]))
        self.play(Transform(varianceTex[0][4:9], MathTex(r"- 0)", font_size=28).move_to(varianceTex[0][6].get_center())))
        self.play(ReplacementTransform(varianceTex[0], varianceTex[1]))
        # Side note on error
        errorVector = always_redraw(lambda: Arrow(start=w(magnitude), end=singleDot.get_center(), color=GREEN, buff=0, max_tip_length_to_length_ratio=0.15))
        errorVectorLabel = always_redraw(lambda: Tex("$x_i - (w\cdot x_i)w$", font_size=28).next_to(errorVector.get_center(), LEFT * 0.7 + DOWN * 0.5))
        self.play(FadeIn(errorVector), FadeIn(errorVectorLabel))

        errorLabelCopy = errorVectorLabel.copy()
        self.add(errorLabelCopy)
        errorTex = VGroup()
        dummyTex = MathTex("\sum_i ||", texStr[2], "- (", texStr[1], "\cdot", texStr[2], ")", texStr[1], "||^2", font_size=28)
        dummyTex[1].set_fill(BLUE), dummyTex[5].set_fill(BLUE)
        dummyTex[3].set_fill(YELLOW), dummyTex[7].set_fill(YELLOW)
        dummyTex.next_to(vertLine.get_center(), RIGHT, buff=LARGE_BUFF)
        errorTex.add(dummyTex)


        dummyTex = MathTex("\sum_i (", texStr[2], "- (", texStr[1], "\cdot", texStr[2], ")", texStr[1], ")\cdot (",
                            texStr[2], "- (", texStr[1], "\cdot", texStr[2], ")", texStr[1], ")", font_size=28)
        dummyTex[1].set_fill(BLUE), dummyTex[5].set_fill(BLUE), dummyTex[9].set_fill(BLUE), dummyTex[13].set_fill(BLUE)
        dummyTex[3].set_fill(YELLOW), dummyTex[7].set_fill(YELLOW), dummyTex[11].set_fill(YELLOW), dummyTex[15].set_fill(YELLOW)
        dummyTex.next_to(errorTex[0], DOWN)
        dummyTex.align_to(errorTex[0], LEFT)
        errorTex.add(dummyTex)
        self.play(ReplacementTransform(errorLabelCopy, errorTex[0]))
        dummyTex = errorTex[0][1:8].copy()
        dummyTex2 = dummyTex.copy()
        self.add(dummyTex, dummyTex2)
        self.play(dummyTex.animate.align_to(errorTex[1][1], LEFT + DOWN * 1.4),
                  dummyTex2.animate.align_to(errorTex[1][9], LEFT + DOWN * 1.4))
        self.play(FadeIn(errorTex[1]), FadeOut(dummyTex), FadeOut(dummyTex2))

        dummyTex = MathTex("\sum_i ||", texStr[2], "||^2", "- \sum_i (", texStr[1], "\cdot", texStr[2], ")^2", font_size=28)
        dummyTex[1].set_fill(BLUE), dummyTex[6].set_fill(BLUE)
        dummyTex[4].set_fill(YELLOW)
        dummyTex.next_to(errorTex[1], direction=DOWN).align_to(errorTex[1], LEFT)
        errorTex.add(dummyTex)
        self.play(FadeIn(errorTex[2], shift=DOWN))
        dummyTex = MathTex(r"\text{constant}", font_size=28)
        dummyTex.move_to(errorTex[2][5].get_center()).align_to(errorTex[2], LEFT)
        self.play(ReplacementTransform(errorTex[2][0:3], dummyTex))
        self.wait(0.5)
        self.play(FadeOut(errorTex), FadeOut(dummyTex))
        # Into matrix form
        strings = [["x_{11}w_1 + x_{12}w_2 + \cdots + x_{1d}w_d"],
                   ["+", "x_{21}w_1 + x_{22}w_2 + \cdots + x_{2d}w_d"],
                   ["+", "x_{31}w_1 + x_{32}w_2 + \cdots + x_{3d}w_d"],
                   ["+", r"\vdots"],
                   ["+", "x_{n1}w_1 + x_{n2}w_2 + \cdots + x_{nd}w_d"]]

        lines = VGroup()
        for i in range(len(strings)):
            if i == 0:
                lines.add(MathTex(r"1 / n(" + strings[0][0] + ")^2", font_size=28))
            elif i == len(strings) - 2:
                lines.add(MathTex(strings[i][0], strings[i][1], font_size=28))
            else:
                lines.add(MathTex(strings[i][0], r"1 / n(" + strings[i][1] + ")^2", font_size=28))
        lines.arrange(DOWN, buff=SMALL_BUFF)
        lines.next_to(varianceTex[1], DOWN).shift(RIGHT * 0.3)
        for i in range(1, len(lines)):
            lines[i][1].align_to(lines[i - 1][-1], LEFT)
            lines[i][0].next_to(lines[i][-1], LEFT)
        lines[3][1].move_to(lines[2][-1].get_center())
        lines[3][1].align_to(lines[3][0], UP)
        self.play(Write(lines))
        self.wait()

        temp = r"=\frac{1}{n}\begin{Vmatrix}"
        for line in strings:
            temp += line[-1] + r"\\ "
        temp += r" \end{Vmatrix}^2"

        m = MathTex(temp, font_size=28).move_to(lines)
        self.play(FadeTransform(lines, m))
        self.wait()

        prodMatrix = MathTex(r"=\frac{1}{n} \begin{vmatrix} \\ \\ \\ \\ \\ \end{vmatrix} ",
                             r"""\begin{bmatrix}
                                 x_{11} & x_{12} & \cdots & x_{1d} \\
                                 x_{21} & x_{22} & \cdots & x_{2d} \\
                                 x_{31} & x_{32} & \cdots & x_{3d} \\
                                 & & \vdots & \\
                                 x_{n1} & x_{n2} & \cdots & x_{nd} \\
                                 \end{bmatrix}""",
                             r"""\begin{bmatrix}
                                 w_1 \\ w_2 \\ w_3 \\ \vdots \\ w_d \\
                                 \end{bmatrix}""",
                             r"\begin{vmatrix} \\ \\ \\ \\ \\ \end{vmatrix}^2", font_size=28).move_to(lines)
        prodMatrix[1].set_fill(BLUE)
        prodMatrix[2].set_fill(YELLOW)
        m2 = m[0][4:].copy()
        m3 = m[0][4:].copy()
        mX = prodMatrix[1]
        mW = prodMatrix[2]
        mLines = VGroup(prodMatrix[0], prodMatrix[3])
        self.play(FadeTransform(m2, mX), FadeTransform(m3, mW), FadeTransform(m, mLines))
        self.wait()

        simpleMatrix = MathTex(r"=\frac{1}{n}||", "X", "w", "||^2", font_size=28)
        simpleMatrix.next_to(lines, DOWN)
        simpleMatrix[1].set_fill(BLUE)
        simpleMatrix[2].set_fill(YELLOW)
        simpleLines = VGroup(simpleMatrix[0], simpleMatrix[3])
        mX_ = mX.copy()
        mW_ = mW.copy()
        mLines_ = mLines.copy()
        self.play(Transform(mX_, simpleMatrix[1]), Transform(mW_, simpleMatrix[2]), Transform(mLines_, simpleLines))
        simplification = VGroup(MathTex(r"=\frac{1}{n}(Xw)^TXw", font_size=28),
                                MathTex(r"=\frac{1}{n}w^TX^TXw", font_size=28),
                                MathTex(r"=w^TSw", font_size=28))
        simplification.arrange(DOWN).next_to(simpleMatrix, DOWN)
        for i in simplification:
            i.align_to(simpleMatrix, LEFT)
        simplification[0][0][5].set_fill(BLUE)
        simplification[0][0][6].set_fill(YELLOW)
        simplification[0][0][9].set_fill(BLUE)
        simplification[0][0][10].set_fill(YELLOW)
        simplification[1][0][4:6].set_fill(YELLOW)
        simplification[1][0][6:9].set_fill(BLUE)
        simplification[1][0][9].set_fill(YELLOW)
        simplification[2][0][1:3].set_fill(YELLOW)
        simplification[2][0][3].set_fill(BLUE)
        simplification[2][0][4].set_fill(YELLOW)
        self.play(Write(simplification[0]))
        self.play(Write(simplification[1]))
        self.wait()
        self.play(Write(simplification[2]))

class Transpose(Scene):
    def construct(self):
        title = Text("Matrix Transpose", font_size=60)
        title.to_edge(UP)
        line = Line(start=LEFT * 6, end=RIGHT * 6)
        line.align_to(title, DOWN).shift(DOWN * 0.3)
        self.play(AnimationGroup(Write(title), Write(line), lag_ratio=0.5))

        data = [np.array([[1, 3], [-1, 2]]),
                np.array([[7, 1, -2], [0, 4, -2], [1, -1, 3]]),
                np.array([[1, 2, 3, 4], [5, 6, 7, 8]])]
        mats = VGroup()
        matsT = VGroup()
        for i in range(len(data)):
            mats.add(Matrix(data[i], h_buff=1))
        mats[0].shift(LEFT * 4.5)
        mats[2].shift(RIGHT * 4.5)

        labels = VGroup(MathTex("A"), MathTex("B"), MathTex("C"))
        labelsT = VGroup(MathTex("A^T"), MathTex("B^T"), MathTex("C^T"))
        for i in range(len(data)):
            labels[i].move_to(mats[i]).shift(DOWN * 2)
            labelsT[i].move_to(mats[i]).shift(DOWN * 2)

        self.play(AnimationGroup(*[[FadeIn(mats[i], scale=0.6), FadeIn(labels[i])] for i in range(len(mats))], lag_ratio=0.25))
        self.wait(0.5)

        def showTranspose(data, mat, index):
            dataT = np.transpose(data)
            matT = Matrix(dataT).move_to(mat)
            row, col = len(mat.get_rows()), len(mat.get_columns())
            elements = mat.get_entries()
            elementsT = matT.get_entries()
            brackets = mat.get_brackets()
            bracketsT = matT.get_brackets()
            label = labels[index]
            labelT = labelsT[index]
            newPos = []
            for i in range(row):
                for j in range(col):
                    newPos.append(elementsT[j * row + i].get_center())
            self.play(AnimationGroup(*[ApplyMethod(elements[i].move_to, newPos[i], rate_func=rate_functions.ease_in_out_cubic) for i in range(len(elements))]),
                      FadeTransform(brackets, bracketsT),
                      ReplacementTransform(label, labelT))
            self.add(matT)
            matsT.add(matT)
            self.play(FadeOut(elements), run_time=0.1)

        for i in range(len(mats)):
            showTranspose(data[i], mats[i], i)

        self.play(FadeOut(matsT), FadeOut(labelsT))

        self.wait()
        m = Matrix([["a_1"], ["a_2"], ["a_3"], [r"\vdots"], ["a_d"]], left_bracket=r"\lVert", right_bracket=r"\rVert^2")
        me = m.get_entries()
        me[3].move_to(me[2]).shift(DOWN * 0.8)
        self.play(Write(m), run_time=1.5)
        self.wait(0.5)
        sumTex = MathTex("=", "a_1^2", "+", "a_2^2", "+", "a_3^2", "+", "\cdots", "+", "a_d^2")
        sumTex.to_edge(DOWN, buff=LARGE_BUFF)

        self.play(AnimationGroup(*[FadeIn(sumTex[2 * i]) for i in range(5)]))
        me = me.copy()
        self.play(AnimationGroup(*[ReplacementTransform(me[i], sumTex[2 * i + 1]) for i in range(len(me))], lag_ratio=0.25))
        self.wait()

        mT = Matrix([["a_1", "a_2", "a_3", r"\cdots", "a_d"]], h_buff=1)
        mTe = mT.get_entries()
        mTe[3].move_to(mTe[2]).shift(RIGHT)
        m2 = Matrix([["a_1"], ["a_2"], ["a_3"], [r"\vdots"], ["a_d"]])
        m2e = m2.get_entries()
        m2e[3].move_to(m2e[2]).shift(DOWN * 0.8)
        prod = VGroup(mT, m2, MathTex("="), m.copy())
        prod.arrange(RIGHT, buff=SMALL_BUFF)
        self.play(Transform(m, prod[3]))
        self.play(FadeIn(prod))
        self.wait()
        mTe = mTe.copy()
        m2e = m2e.copy()
        self.play(AnimationGroup(*[(ReplacementTransform(mTe[i], sumTex[2 * i + 1]),
                                    ReplacementTransform(m2e[i], sumTex[2 * i + 1]))
                                   for i in range(len(me))], lag_ratio=0.25))
        self.wait(0.5)
        result = MathTex("=", "a_1^2 + a_2^2 + a_3^2 + \cdots + a_d^2", "=", "A^T A")
        result.arrange(RIGHT).to_edge(DOWN, buff=LARGE_BUFF)
        result[0].shift(DOWN * 0.05)
        result[2].shift(DOWN * 0.05)
        self.play(FadeTransform(sumTex[0], result[0]), FadeTransform(sumTex[1:], result[1]), FadeIn(result[2:]))
        self.wait()
        self.play(FadeOut(result), FadeOut(prod), FadeOut(m))

        proof = VGroup(MathTex("(AB)", "^T_{ij}", "= (AB)_{ji}", "= (B^TA^T)_{ij}"),
                       MathTex("= \sum_{k = 1}^n", "A_{jk}", "B_{ki}"),
                       MathTex("= \sum_{k = 1}^n", "A^T_{kj}", "B^T_{ik}"),
                       MathTex("= \sum_{k = 1}^n", "B^T_{ik}", "A^T_{kj}", "= (B^TA^T)_{ij}"))
        proof.arrange(DOWN)
        for i in range(1, len(proof)):
            proof[i].align_to(proof[0][1], LEFT)
        proof.center().shift(DOWN * 0.7)
        self.play(Write(proof[0][:-1]))
        dimArrow = Arrow(end=proof[0][0].get_bottom(), start=proof[0][0].get_bottom() + DOWN * 1.5 + LEFT)
        dimTex = VGroup(MathTex(r"A \in \mathbb{R}^{a \times n}", font_size=40), MathTex(r"B \in \mathbb{R}^{n \times b}", font_size=40))
        dimTex.arrange(DOWN).move_to(dimArrow.get_bottom()).shift(DOWN + LEFT)
        self.play(AnimationGroup(FadeIn(dimArrow, shift=DOWN), FadeIn(dimTex, shift=DOWN), lag_ratio=0.25))
        self.play(FadeIn(proof[1], shift=DOWN))
        self.play(FadeIn(proof[2][0], shift=DOWN),
                  Transform(proof[1][1].copy(), proof[2][1]),
                  Transform(proof[1][2].copy(), proof[2][2]))
        self.play(FadeIn(proof[3][0], shift=DOWN),
                  Transform(proof[2][1].copy(), proof[3][2]),
                  Transform(proof[2][2].copy(), proof[3][1]))
        self.play(Write(proof[3][3]))
        proof[0][-1].align_to(proof[3][3], LEFT)
        self.play(Transform(proof[3][3].copy(), proof[0][-1]))
        self.wait()

class Covariance(Scene):
    def fetchData(self):
        with open("covarianceDataset.txt", "r") as file:
            lines = file.readlines()
        c1, c2, c3 = np.zeros((50, 2)), np.zeros((50, 2)), np.zeros((50, 2))
        for i in range(50):
            c1[i] = list(map(float, lines[i].split()))
            c2[i] = list(map(float, lines[i + 50].split()))
            c3[i] = list(map(float, lines[i + 100].split()))
        m1 = np.mean(c1, axis=0)
        m2 = np.mean(c2, axis=0)
        m3 = np.mean(c3, axis=0)
        c = np.array([c1, c2, c3])
        c[0] -= m1
        c[1] -= m2
        c[2] -= m3
        return c


    def construct(self):
        title = Text("Covariance", font_size=60).to_edge(UP)
        line = Line(start=LEFT * 6, end=RIGHT * 6).align_to(title, DOWN).shift(DOWN * 0.3)
        self.play(AnimationGroup(Write(title), Write(line), lag_ratio=0.5))
        C = self.fetchData()
        definition = MathTex(r"\text{cov}(X, Y) = E[(X - E[X])", "(Y - E[Y])]", "= E[XY]", "- E[X]E[Y]", font_size=40)
        definition.align_to(line, UP).shift(DOWN * 0.3)
        self.play(Write(definition[0]))
        self.wait()
        self.play(Write(definition[1]))
        self.wait()
        self.play(Write(definition[2]))
        self.wait(0.5)
        self.play(Write(definition[3]))
        self.wait()

        axes = Axes(x_range=[-5, 5, 5], y_range=[-5, 5, 5], x_length=3.8, y_length=3.8, tips=False)
        plots = VGroup(axes, axes.copy(), axes.copy()).shift(DOWN)
        amt = (plots[1].get_right()[0] + config.frame_x_radius) / 2
        plots[0].shift(LEFT * amt)
        plots[2].shift(RIGHT * amt)
        labels = VGroup(plot.get_x_axis_label("X", edge=RIGHT, direction=RIGHT) for plot in plots)
        labels.add(plot.get_y_axis_label("Y", direction=UP) for plot in plots)
        self.play(Write(plots), Write(labels))
        self.wait()

        dots = VGroup(VGroup(), VGroup(), VGroup())
        colors = [BLUE, YELLOW, GREEN]
        for i in range(3):
            for j in range(50):
                dots[i].add(Dot(point=plots[i].c2p(C[i][j][0], C[i][j][1]), color=colors[i], radius=0.06))
            self.play(AnimationGroup(*[FadeIn(dots[i][j]) for j in range(50)], lag_ratio=0.05), run_time=1.5)
        self.wait()

        def getFocus(index):
            fPlot = Axes(x_range=[-5, 5, 5], y_range=[-5, 5, 5], x_length=5.5, y_length=5.5, tips=False).shift(DOWN)
            fLabels = VGroup(fPlot.get_x_axis_label("X", edge=RIGHT, direction=RIGHT), fPlot.get_y_axis_label("Y", direction=UP))
            fDots = VGroup(*[Dot(point=fPlot.c2p(C[index][j][0], C[index][j][1]), color=colors[index], radius=0.06) for j in range(50)])
            return fPlot, fLabels, fDots

        def getDummy(index):
            return plots[index].copy(), VGroup(labels[index].copy(), labels[index + 3].copy()), dots[index].copy()

        focusPlot, focusLabels, focusDots = getFocus(0)
        dummyPlot, dummyLabels, dummyDots = getDummy(0)
        self.play(FadeOut(plots), FadeOut(labels), FadeOut(dots), FadeOut(definition[:2]),
                  ReplacementTransform(dummyPlot.copy(), focusPlot),
                  ReplacementTransform(dummyLabels.copy(), focusLabels),
                  ReplacementTransform(dummyDots.copy(), focusDots))
        self.wait()

        quadrants = VGroup(Polygon(*[focusPlot.c2p(0, 0), focusPlot.c2p(5, 0), focusPlot.c2p(5, 5), focusPlot.c2p(0, 5)], fill_color=RED, fill_opacity=0.3, stroke_width=0),
                           Polygon(*[focusPlot.c2p(0, 0), focusPlot.c2p(-5, 0), focusPlot.c2p(-5, 5), focusPlot.c2p(0, 5)], fill_color=RED, fill_opacity=0.3, stroke_width=0),
                           Polygon(*[focusPlot.c2p(0, 0), focusPlot.c2p(-5, 0), focusPlot.c2p(-5, -5), focusPlot.c2p(0, -5)], fill_color=RED, fill_opacity=0.3, stroke_width=0),
                           Polygon(*[focusPlot.c2p(0, 0), focusPlot.c2p(5, 0), focusPlot.c2p(5, -5), focusPlot.c2p(0, -5)], fill_color=RED, fill_opacity=0.3, stroke_width=0))
        self.play(FadeIn(quadrants[0]), FadeIn(quadrants[2]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(quadrants[0]), FadeOut(quadrants[2]), run_time=0.5)
        self.wait()
        self.play(FadeIn(plots), FadeIn(labels), FadeIn(dots), FadeIn(definition[:2]),
                  ReplacementTransform(focusPlot, dummyPlot),
                  ReplacementTransform(focusLabels, dummyLabels),
                  ReplacementTransform(focusDots, dummyDots))
        self.remove(dummyPlot, dummyLabels, dummyDots)
        self.wait()

        focusPlot, focusLabels, focusDots = getFocus(1)
        dummyPlot, dummyLabels, dummyDots = getDummy(1)
        self.play(FadeOut(plots), FadeOut(labels), FadeOut(dots), FadeOut(definition[:2]),
                  ReplacementTransform(dummyPlot.copy(), focusPlot),
                  ReplacementTransform(dummyLabels.copy(), focusLabels),
                  ReplacementTransform(dummyDots.copy(), focusDots))
        self.wait()
        self.play(FadeIn(quadrants[1]), FadeIn(quadrants[3]), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(quadrants[1]), FadeOut(quadrants[3]), run_time=0.5)
        self.wait()
        self.play(FadeIn(plots), FadeIn(labels), FadeIn(dots), FadeIn(definition[:2]),
                  ReplacementTransform(focusPlot, dummyPlot),
                  ReplacementTransform(focusLabels, dummyLabels),
                  ReplacementTransform(focusDots, dummyDots))
        self.remove(dummyPlot, dummyLabels, dummyDots, focusPlot, focusLabels, focusDots)
        self.wait()

        focusPlot, focusLabels, focusDots = getFocus(2)
        dummyPlot, dummyLabels, dummyDots = getDummy(2)
        self.play(FadeOut(plots), FadeOut(labels), FadeOut(dots), FadeOut(definition[:2]),
                  ReplacementTransform(dummyPlot.copy(), focusPlot),
                  ReplacementTransform(dummyLabels.copy(), focusLabels),
                  ReplacementTransform(dummyDots.copy(), focusDots))
        self.wait()
        self.play(FadeIn(quadrants), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(quadrants), run_time=0.5)
        self.wait()
        self.play(FadeIn(plots), FadeIn(labels), FadeIn(dots), FadeIn(definition[:2]),
                  ReplacementTransform(focusPlot, dummyPlot),
                  ReplacementTransform(focusLabels, dummyLabels),
                  ReplacementTransform(focusDots, dummyDots))
        self.remove(dummyPlot, dummyLabels, dummyDots, focusPlot, focusLabels, focusDots)
        self.wait()
        self.play(FadeOut(plots), FadeOut(labels), FadeOut(dots))
        covmatrix = MathTex("\mathbf{S} = [", r"\text{cov}(X_i, X_j)", "]", "_{1\leq i, j\leq n}")
        covmatrix[0][0].set_color(BLUE)
        covmatrix[1][4:9].set_color(BLUE)
        self.wait(0.5)
        self.play(Write(covmatrix[0]), Write(covmatrix[2]))
        self.play(Write(covmatrix[1]), Write(covmatrix[3]))

class LagrangeMultiplier(ThreeDScene):
    def construct(self):
        def f(x, y):
            return 2 * np.exp(-(x ** 2 / 3 + y ** 2 / 2)) + np.sin(x + y) / 4 + np.exp(-((x - 2) ** 2 / 2 + (y - 1) ** 2 / 3)) - (x ** 2 + y ** 2) / 50
        def dfdx(x, y):
            return -4 * x / 3 * np.exp(-(x ** 2 / 3 + y ** 2 / 2)) + np.cos(x + y) / 4 - (x - 2) * np.exp(-((x - 2) ** 2 / 2 + (y - 1) ** 2 / 3)) - x / 25
        def dfdy(x, y):
            return -2 * y * np.exp(-(x ** 2 / 3 + y ** 2 / 2)) + np.cos(x + y) / 4 - 2 * (y - 1) / 3 *  np.exp(-((x - 2) ** 2 / 2 + (y - 1) ** 2 / 3)) - y / 25
        def g(x, y):
            return (y ** 2 - (x - 1) ** 3 - (x - 1)) / 5
        def gConstr(x, y, c):
            return (y ** 2 - (x - 1) ** 3 - (x - 1)) / 5 - c

        axes = ThreeDAxes(z_range=[-1, 4], x_range=[-5, 5], y_range=[-5, 5], z_length=4)
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES, frame_center=[0, 0, 1], zoom=1.4)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.add(axes)

        text3d = Text("Lagrange Multipliers")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        self.play(Write(text3d))
        self.wait()

        graph = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=100,
            fill_color=TEAL,
            fill_opacity=0.4,
            stroke_opacity=0.0,
            stroke_width=0,
            stroke_color=TEAL,
            surface_piece_config={
                "gloss" : 0.5,
                "shade_in_3d" : True
            },
            checkerboard_colors=False,
        )
        graph.set_fill_by_value(axes=axes, colorscale=[BLUE_D, TEAL_A], axis=2)
        fTex = MathTex("f(x, y)")
        gTex = MathTex("g(x, y)", "= c")
        self.add_fixed_in_frame_mobjects(fTex)
        fTex.to_edge(LEFT).shift(UP * 2.5).set_fill(TEAL)
        gTex.to_edge(LEFT).shift(UP * 1.8)
        gTex[0].set_fill(YELLOW)
        self.play(Create(graph), Write(fTex), run_time=2.5, rate_func=rate_functions.ease_in_out_cubic)
        self.wait(2)

        constraintLine = axes.plot_implicit_curve(lambda x, y: gConstr(x, y, 1), color=YELLOW)
        self.play(Create(constraintLine), run_time=2)
        self.add_fixed_in_frame_mobjects(gTex)
        self.play(Write(gTex))
        for i in range(30):
            self.begin_ambient_camera_rotation(rate=-0.005)
            self.wait(0.05)
        self.wait()
        pos = ValueTracker(np.sqrt(5))
        def getx(y):
            term = np.cbrt(9 * y ** 2 + 1.7321 * np.sqrt(27 * y ** 4 - 270 * y ** 2 + 679) - 45)
            return 0.38157 * term - 0.87358 / term + 1
        dot = always_redraw(lambda: Dot(axes.c2p(getx(pos.get_value()), pos.get_value(), 0), color=RED))
        def getGradientArrow():
            y = pos.get_value()
            x = getx(y)
            return Arrow(start=axes.c2p(x, y, 0), end=axes.c2p(x + dfdx(x, y), y + dfdy(x, y), 0), buff=0, color=RED)
        gradient = always_redraw(lambda: getGradientArrow())
        self.play(FadeIn(dot), Flash(dot, color=RED))
        self.wait()
        self.play(FadeIn(gradient))
        self.wait()
        maximum = Dot3D(point=axes.c2p(0.45, 0.18, 2.22), color=GREEN, resolution=8)
        maximum2D = Dot(point=axes.c2p(0.45, 0.18), color=GREEN)
        dropDown = DashedLine(start=maximum.get_center(), end=maximum2D.get_center(), color=GREEN)
        self.play(Create(maximum))
        self.play(Transform(maximum.copy(), maximum2D), Create(dropDown))
        self.wait()
        self.play(pos.animate.set_value(0.15), run_time=5)
        self.wait()
        self.move_camera(phi=0, theta=180 * DEGREES, zoom=1, run_time=1.5)
        self.wait()
        self.play(pos.animate.set_value(-1))
        self.play(pos.animate.set_value(0.15))
        self.wait()
        self.move_camera(phi=75 * DEGREES, theta = 135 * DEGREES, zoom=1.4, run_time=1.5)

        constraintMaximum = Dot3D(point=axes.c2p(getx(pos.get_value()), pos.get_value(), f(getx(pos.get_value()), pos.get_value())), color=RED)
        constraintDropDown = DashedLine(start=dot.get_center(), end=constraintMaximum.get_center(), color=RED)
        self.play(Transform(dot.copy(), constraintMaximum), Create(constraintDropDown))
        for i in range(30):
            self.begin_ambient_camera_rotation(rate=0.005)
            self.wait(0.05)
        self.wait(2)
        equation = MathTex(r"\nabla f", r"= \lambda", r"\nabla g")
        self.add_fixed_in_frame_mobjects(equation)
        equation.to_corner(UR)
        equation[0].set_fill(TEAL)
        equation[2].set_fill(YELLOW)
        self.play(Write(equation))
        self.wait(5)
        # RENDERED IN 42 MINUTES LMAO SKULLEMOJI

class FinalCalculation(Scene):
    def construct(self):
        function = MathTex(r"\mathcal{L}(w, \lambda) = ", r"w^TSw", "-", "\lambda", "(", "w^Tw", "- 1", ")")
        function[0][0].set_color(RED)
        function[0][2].set_color(YELLOW)
        function[0][4].set_color(GREEN)
        function[1][0:2].set_color(YELLOW)
        function[1][3].set_color(YELLOW)
        function[1][2].set_color(BLUE)
        function[3].set_color(GREEN)
        function[5].set_color(YELLOW)
        derivative = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = ", # 0
                             r"\frac{\partial}{\partial w}", "w^TSw", "-", # 3
                             r"\frac{\partial}{\partial w}", "\lambda", # 5
                             "(", "w^Tw", "- 1", ")") # 9
        derivative[0][1].set_color(RED)
        derivative[0][4].set_color(YELLOW)
        derivative[1][3].set_color(YELLOW)
        derivative[2][0:2].set_color(YELLOW)
        derivative[2][3].set_color(YELLOW)
        derivative[2][2].set_color(BLUE)
        derivative[4][3].set_color(YELLOW)
        derivative[5].set_color(GREEN)
        derivative[7].set_color(YELLOW)

        self.play(Write(function))
        self.play(function.animate.shift(UP))
        self.wait(0.5)
        self.play(Write(derivative[0]))
        self.wait(0.5)
        self.play(ReplacementTransform(derivative[0].copy(), derivative[1]),
                  ReplacementTransform(derivative[0].copy(), derivative[4]),
                  Write(derivative[3]))
        self.play(ReplacementTransform(function[1].copy(), derivative[2]),
                  ReplacementTransform(function[3:].copy(), derivative[5:]))
        self.wait(0.5)
        self.play(FadeOut(derivative[8]), derivative[9].animate.shift(LEFT * 0.85))
        self.wait(0.5)
        self.play(derivative[4].animate.shift(RIGHT * 0.3), derivative[5].animate.shift(LEFT * 0.8))
        self.play(FadeOut(derivative[6], derivative[9]))
        self.wait(0.5)
        self.play(FadeOut(derivative[:6]), derivative[7].animate.center(), function.animate.to_edge(UP))
        self.wait(0.5)

        # First derivative
        w = Matrix([["w_1"], ["w_2"], ["w_3"], [r"\vdots"], ["w_d"]], v_buff=0.8)
        wT = Matrix([["w_1", "w_2", "w_3", "\cdots", "w_d"]], h_buff=1)
        wTw = MathTex("w_1^2", "+", "w_2^2", "+", "w_3^2", "+", "\cdots", "+", "w_d^2")
        we, wTe = w.get_entries(), wT.get_entries()
        wb, wTb = w.get_brackets(), wT.get_brackets()
        for i in [0, 1, 2, 4]:
            we[i].set_color(YELLOW)
            wTe[i].set_color(YELLOW)
        we[3].move_to(we[2]).shift(DOWN * 0.8)
        wTe[3].move_to(wTe[2]).shift(RIGHT)
        for i in [0, 2, 4, 8]:
            wTw[i].set_color(YELLOW)
        expr = VGroup(wT, w).arrange(RIGHT)
        self.remove(derivative[7])
        self.play(ReplacementTransform(derivative[7].copy(), expr))
        self.wait(0.5)

        self.play(FadeOut(wb, wTb),
                  AnimationGroup(*[ReplacementTransform(we[i], wTw[2 * i]) for i in range(5)], lag_ratio=0.2),
                  AnimationGroup(*[ReplacementTransform(wTe[i], wTw[2 * i]) for i in range(5)], lag_ratio=0.2),
                  AnimationGroup(*[FadeIn(wTw[2 * i + 1]) for i in range(4)], lag_ratio=0.25))
        self.wait(0.5)

        dwTw = MathTex(r"\frac{\partial}{\partial w_i}", "(w_1^2 + w_2^2 + w_3^2 + \cdots + w_d^2)", "=", "2w_i").shift(DOWN * 0.5)
        dwTw[0][3:].set_color(YELLOW)
        for i in [1, 5, 9, 17]:
            dwTw[1][i:i + 3].set_color(YELLOW)
        dwTw[3][-2:].set_color(YELLOW)

        dwTw[1].move_to(wTw).shift(DOWN * 0.5)
        dwTw[0].next_to(dwTw[1], LEFT, buff=SMALL_BUFF / 2)
        dwTw[2:].next_to(dwTw[1], RIGHT, buff=SMALL_BUFF)
        self.play(wTw.animate.shift(UP * 0.7), FadeIn(dwTw[:2], shift=DOWN * 0.3))
        self.play(FadeIn(dwTw[2:], shift=RIGHT))
        self.wait(0.5)

        dw = VGroup(MathTex(r"\frac{\partial}{\partial w}", "="),
                    Matrix([[r"\frac{\partial}{\partial w_1}"], [r"\frac{\partial}{\partial w_2}"],
                            [r"\frac{\partial}{\partial w_3}"], [r"\vdots"], [r"\frac{\partial}{\partial w_d}"]],
                           v_buff=0.9, element_to_mobject_config={"font_size" : 32}))
        dw[0][0][3].set_color(YELLOW)
        dw.arrange(RIGHT)
        dwe = dw[1].get_entries()
        for i in [0, 1, 2, 4]:
            dwe[i][0][3:].set_color(YELLOW)
        dwe[3].move_to(dwe[2]).shift(DOWN * 0.9)
        self.play(dwTw.animate.to_edge(DOWN),
                  FadeOut(wTw))
        self.wait(0.5)
        self.play(Write(dw))
        self.wait(0.5)
        temp = dw.copy()
        self.add(temp)
        self.remove(dw)
        dw.add(MathTex("="))
        dw.add(Matrix([["2w_1"], ["2w_2"], ["2w_3"], [r"\vdots"], ["2w_d"]], v_buff=1))
        dwe = dw[3].get_entries()
        for i in [0, 1, 2, 4]:
            dwe[i][0][1:].set_color(YELLOW)
        dwe[3].move_to(dwe[2]).shift(DOWN * 0.9)
        dw.arrange(RIGHT)
        self.play(FadeTransform(temp, dw[:2]), Write(dw[2]), Write(dw[3].get_brackets()),
                  AnimationGroup(*[ReplacementTransform(dwTw[3].copy(), dwe[i]) for i in range(5)], lag_ratio=0.2))
        self.wait(0.5)
        dw.add(MathTex("= 2w").next_to(dw[3], RIGHT))
        dw[-1][0][2].set_color(YELLOW)
        self.play(Write(dw[-1]))
        self.wait(0.5)

        derivativeOld = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = ", r"\frac{\partial}{\partial w}", "w^T", "Sw",
                                "-", r"\lambda \frac{\partial}{\partial w} w^Tw").next_to(function, DOWN)
        derivativeOld[0][1].set_color(RED)
        derivativeOld[0][4].set_color(YELLOW)
        derivativeOld[1][3].set_color(YELLOW)
        derivativeOld[2].set_color(YELLOW)
        derivativeOld[3][0].set_color(BLUE)
        derivativeOld[3][1].set_color(YELLOW)
        derivativeOld[5][0].set_color(GREEN)
        derivativeOld[5][4:].set_color(YELLOW)
        derivative = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = ", r"\frac{\partial}{\partial w}", "w^T", "Sw",
                             "-", r"2\lambda w").next_to(function, DOWN)
        derivative[0][1].set_color(RED)
        derivative[0][4].set_color(YELLOW)
        derivative[1][3].set_color(YELLOW)
        derivative[2].set_color(YELLOW)
        derivative[3][0].set_color(BLUE)
        derivative[3][1].set_color(YELLOW)
        derivative[5][1].set_color(GREEN)
        derivative[5][2].set_color(YELLOW)
        self.play(FadeOut(dw[:-1]), Write(derivativeOld))
        self.play(ReplacementTransform(derivativeOld, derivative))
        self.play(FadeOut(dw[-1]), FadeOut(dwTw), FadeOut(derivative[:2]), FadeOut(derivative[4:]), derivative[2:4].animate.center())
        self.wait(0.5)
        swTex = MathTex("S", "w").move_to(derivative[3])
        swTex[0].set_color(BLUE)
        swTex[1].set_color(YELLOW)
        self.add(swTex)
        self.play(FadeOut(derivative[2:4]))
        self.wait(0.5)

        swmatrix = VGroup(Matrix([["s_{11}", "s_{12}", "\cdots", "s_{1d}"], ["s_{21}", "s_{22}", "\cdots", "s_{2d}"],
                                  ["s_{31}", "s_{32}", "\cdots", "s_{3d}"], [r"\vdots", r"\vdots", "\ddots", r"\vdots"],
                                  ["s_{d1}", "s_{d2}", "\cdots", "s_{dd}"]], v_buff=1, h_buff=1, bracket_h_buff=0.06),
                          Matrix([["w_1"], ["w_2"], ["w_3"], [r"\vdots"], ["w_d"]], v_buff=1, bracket_h_buff=0.06))
        swmatrix.arrange(RIGHT)
        se = swmatrix[0].get_entries()
        for i in [0, 1, 2, 4]:
            for j in [0, 1, 3]:
                se[i * 4 + j].set_color(BLUE)
        for i in range(4):
            se[12 + i].move_to(se[8 + i]).shift(DOWN)
        for i in range(5):
            se[i * 4 + 2].move_to(se[i * 4 + 3]).shift(LEFT)
        we = swmatrix[1].get_entries()
        for i in [0, 1, 2, 4]:
            we[i].set_color(YELLOW)
        we[3].move_to(we[2]).shift(DOWN)
        self.play(ReplacementTransform(swTex, swmatrix))
        self.wait(0.5)
        temp = swmatrix.copy()
        self.add(temp)
        self.remove(swmatrix)

        swmatrix.add(MathTex("="))
        sw = Matrix([["s_{11}w_1", "+", "s_{12}w_2", "+", "\cdots", "+", "s_{1d}w_d"],
                     ["s_{21}w_1", "+", "s_{22}w_2", "+", "\cdots", "+", "s_{2d}w_d"],
                     ["s_{31}w_1", "+", "s_{32}w_2", "+", "\cdots", "+", "s_{3d}w_d"],
                     [r"\vdots",   "",  r"\vdots",   "", "\ddots",  "",  r"\vdots"],
                     ["s_{d1}w_1", "+", "s_{d2}w_2", "+", "\cdots", "+", "s_{dd}w_d"]], v_buff=1, bracket_h_buff=0.1)
        swmatrix.add(sw)
        swe = sw.get_entries()
        for i in [0, 1, 2, 4]:
            for j in [0, 2, 6]:
                swe[i * 7 + j][0][0:3].set_color(BLUE)
                swe[i * 7 + j][0][3:].set_color(YELLOW)
        for i in range(1, 4):
            for j in range(5):
                swe[j * 7 + 2 * i - 1].shift(LEFT * 0.8 * i)
                swe[j * 7 + 2 * i].shift(LEFT * 0.8 * i)
        for i in range(4, 7):
            for j in range(5):
                swe[j * 7 + i].shift(LEFT * 0.6)
        for i in range(7):
            swe[21 + i].move_to(swe[14 + i]).shift(DOWN)
        for i in range(5):
            swe[i * 7 + 4].move_to(swe[i * 7 + 6]).shift(LEFT * 1.45)
        sw.get_brackets()[1].shift(LEFT * 3)
        swmatrix.arrange(RIGHT)
        self.play(ReplacementTransform(temp, swmatrix[:2]))
        self.wait(0.5)
        self.play(AnimationGroup(*[ReplacementTransform(se[i].copy(), swe[int(i / 4) * 7 + 2 * (i % 4)]) for i in range(20)], lag_ratio=0.2),
                  AnimationGroup(*[ReplacementTransform(we[i % 5].copy(), swe[int(i / 4) * 7 + 2 * (i % 4)]) for i in range(20)], lag_ratio=0.2),
                  AnimationGroup(*[Write(swe[int(i / 3) * 7 + 2 * (i % 3) + 1]) for i in range(15)], lag_ratio=0.2),
                  Write(sw.get_brackets()),
                  Write(swmatrix[-2]), run_time=5)
        self.wait(0.5)

        wT = Matrix([["w_1", "w_2", "w_3", "\cdots", "w_d"]], h_buff=1)
        wTe = wT.get_entries()
        for i in [0, 1, 2, 4]:
            wTe[i].set_color(YELLOW)
        wTe[3].move_to(wTe[2]).shift(RIGHT)
        wtswTex = VGroup(wT, sw.copy()).arrange(RIGHT)
        self.play(FadeOut(swmatrix[:-1]), sw.animate.move_to(wtswTex[1]))
        derivative[2].next_to(sw, LEFT)
        self.play(Write(derivative[2]))
        self.wait(0.5)
        self.play(ReplacementTransform(derivative[2], wT))
        self.wait(0.5)
        wtsw = VGroup(MathTex("s_{11}w_1w_1", "+", "s_{12}w_1w_2", "+", "s_{13}w_1w_3", "+\cdots +", "s_{1d}w_1w_d"),
                      MathTex("s_{21}w_1w_2", "+", "s_{22}w_2w_2", "+", "s_{23}w_2w_3", "+\cdots +", "s_{2d}w_2w_d"),
                      MathTex("s_{31}w_1w_3", "+", "s_{32}w_2w_3", "+", "s_{33}w_3w_3", "+\cdots +", "s_{3d}w_1w_d"),
                      MathTex(r"\vdots", "\ ", r"\vdots", "\ ", r"\vdots", "\ \ddots\ ", r"\vdots"),
                      MathTex("s_{d1}w_1w_d", "+", "s_{d2}w_2w_d", "+", "s_{d3}w_3w_d", "+\cdots +", "s_{dd}w_dw_d"))
        wtsw.arrange(DOWN)
        for i in [0, 1, 2, 4]:
            for j in [0, 2, 4, 6]:
                wtsw[i][j][0:3].set_color(BLUE)
                wtsw[i][j][3:].set_color(YELLOW)
        for i in [0, 1, 4]:
            for j in range(7):
                wtsw[i][j].move_to(wtsw[2][j]).shift(DOWN * (i - 2) * 0.8)
        for i in range(7):
            wtsw[3][i].move_to(wtsw[2][i]).shift(DOWN * 0.8)
        plus = MathTex("+", "+", "+", "+")
        for i in range(4):
            plus[i].next_to(wtsw[1], LEFT).shift(DOWN * i * 0.8)
        wte = wT.get_entries()
        wte_to_wtsw = [0, 2, 4, 5, 6]
        self.play(FadeOut(wT.get_brackets()), FadeOut(sw.get_brackets()),
                  AnimationGroup(*[ReplacementTransform(wte[i % 5].copy(), wtsw[i % 5][wte_to_wtsw[int(i / 5)]]) for i in range(25)], lag_ratio=0.1),
                  AnimationGroup(*[ReplacementTransform(swe[i], wtsw[int(i / 7)][i % 7]) for i in range(35)], lag_ratio=0.1),
                  Write(plus), FadeOut(wte))
        self.wait(0.5)
        dwtsw = MathTex(r"\frac{\partial}{\partial w_i} w^TSw",
                        r"=\frac{\partial}{\partial w_i}(s_{ii}w_i^2 + ", r"\sum_{j \neq i}s_{ij}w_iw_j", "+", r"\sum_{j \neq i}", "s_{ji}", r"w_iw_j)")
        dwtsw[0][3:5].set_color(YELLOW)
        dwtsw[0][5:7].set_color(YELLOW)
        dwtsw[0][7].set_color(BLUE)
        dwtsw[0][8].set_color(YELLOW)
        dwtsw[1][4:6].set_color(YELLOW)
        dwtsw[1][7:10].set_color(BLUE)
        dwtsw[1][10:13].set_color(YELLOW)
        dwtsw[2][5:8].set_color(BLUE)
        dwtsw[2][8:].set_color(YELLOW)
        dwtsw[5].set_color(BLUE)
        dwtsw[6][:-1].set_color(YELLOW)
        symmetric = MathTex(r"S\text{ is symmetric} \implies s_{ij} = s_{ji}!").scale(1.5).next_to(wtsw, UP)
        symmetric[0][0].set_color(BLUE)
        symmetric[0][-4:-1].set_color(BLUE)
        symmetric[0][-8:-5].set_color(BLUE)
        dwtsw.next_to(wtsw, DOWN)
        self.play(Write(dwtsw[0]))
        self.wait(0.5)
        self.play(Write(dwtsw[1:]))
        self.wait(0.5)
        self.play(FadeIn(symmetric))
        self.wait(0.5)
        self.play(FadeOut(wtsw), FadeOut(plus), symmetric.animate.shift(DOWN * 0.5), dwtsw.animate.center())
        self.wait(0.5)
        self.play(Transform(dwtsw[5], MathTex("s_{ij}").move_to(dwtsw[5]).set_color(BLUE) ))
        two = MathTex("2").next_to(dwtsw[1], RIGHT, buff=SMALL_BUFF)
        self.play(dwtsw[2].animate.shift(RIGHT * 0.3), dwtsw[4:].animate.align_to(dwtsw[2].copy().shift(RIGHT * 0.3), LEFT), FadeIn(two), FadeOut(dwtsw[3]))
        dwtsw2 = MathTex(r"= 2s_{ii}w_i + 2\sum_{j\neq i}s_{ij}w_j", "= 2\sum s_{ij}w_j").next_to(dwtsw, DOWN).align_to(dwtsw[1], LEFT)
        dwtsw2[0][2:5].set_color(BLUE)
        dwtsw2[0][5:7].set_color(YELLOW)
        dwtsw2[0][14:17].set_color(BLUE)
        dwtsw2[0][17:19].set_color(YELLOW)
        dwtsw2[1][3:6].set_color(BLUE)
        dwtsw2[1][6:].set_color(YELLOW)
        self.wait(0.5)
        self.play(Write(dwtsw2[0]))
        self.play(Write(dwtsw2[1]))
        self.wait(0.5)
        self.play(dwtsw2[1].animate.to_edge(DOWN), FadeOut(dwtsw2[0]), FadeOut(dwtsw[:3]), FadeOut(dwtsw[4:]), FadeOut(two), FadeOut(symmetric))
        self.wait(0.5)

        dw = VGroup(MathTex(r"\frac{\partial}{\partial w}", "="),
                    Matrix([[r"\frac{\partial}{\partial w_1}"], [r"\frac{\partial}{\partial w_2}"],
                            [r"\frac{\partial}{\partial w_3}"], [r"\vdots"], [r"\frac{\partial}{\partial w_d}"]],
                           v_buff=0.9, element_to_mobject_config={"font_size": 32}))
        dw.arrange(RIGHT)
        dw[0][0][3].set_color(YELLOW)
        dwe = dw[1].get_entries()
        for i in [0, 1, 2, 4]:
            dwe[i][0][3:].set_color(YELLOW)
        dwe[3].move_to(dwe[2]).shift(DOWN * 0.9)
        self.play(Write(dw))
        self.wait(0.5)
        temp = dw.copy()
        self.add(temp)
        self.remove(dw)
        dw.add(MathTex("=2"))
        dw.add(Matrix([["s_{11}w_1 + s_{12}w_2 + \cdots + s_{1d}w_d"],
                       ["s_{21}w_1 + s_{22}w_2 + \cdots + s_{2d}w_d"],
                       ["s_{31}w_1 + s_{32}w_2 + \cdots + s_{3d}w_d"],
                       [r"\vdots"],
                       ["s_{d1}w_1 + s_{d2}w_2 + \cdots + s_{dd}w_d"]], v_buff=1))
        dwe = dw[3].get_entries()
        for i in [0, 1, 2, 4]:
            for j in [0, 6, 16]:
                dwe[i][0][j:j + 3].set_color(BLUE)
                dwe[i][0][j + 3:j + 5].set_color(YELLOW)
        dwe[3].move_to(dwe[2]).shift(DOWN)
        dw.arrange(RIGHT).shift(LEFT)
        self.play(FadeTransform(temp, dw[:2]), Write(dw[2]), Write(dw[3].get_brackets()),
                  AnimationGroup(*[ReplacementTransform(dwtsw2[1].copy(), dwe[i]) for i in range(5)], lag_ratio=0.2))
        self.wait(0.5)
        sw = MathTex("= 2Sw").next_to(dw[3], RIGHT)
        sw[0][2].set_color(BLUE)
        sw[0][3].set_color(YELLOW)
        dw.add(sw)
        self.play(Write(dw[-1]))
        self.wait(0.5)
        derivativeOld = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = ", r"\frac{\partial}{\partial w}w^TSw",
                                "- 2\lambda w").next_to(function, DOWN)
        derivativeOld[0][1].set_color(RED)
        derivativeOld[0][4].set_color(YELLOW)
        derivativeOld[1][3].set_color(YELLOW)
        derivativeOld[1][4:6].set_color(YELLOW)
        derivativeOld[1][6].set_color(BLUE)
        derivativeOld[1][7].set_color(YELLOW)
        derivativeOld[2][2].set_color(GREEN)
        derivativeOld[2][3].set_color(YELLOW)
        derivative = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = ", r"2Sw",
                             "- 2\lambda w", "=0").next_to(function, DOWN)
        derivative[0][1].set_color(RED)
        derivative[0][4].set_color(YELLOW)
        derivative[1][1].set_color(BLUE)
        derivative[1][2].set_color(YELLOW)
        derivative[2][2].set_color(GREEN)
        derivative[2][3].set_color(YELLOW)
        self.play(FadeOut(dw[:-1]), FadeOut(dwtsw2[1]), Write(derivativeOld))
        self.play(ReplacementTransform(derivativeOld, derivative[:-1]), Transform(dw[-1], derivative[1]))
        self.remove(dw[-1])
        self.wait(0.5)
        self.play(Write(derivative[-1]))
        equation = MathTex("Sw = \lambda w").scale(5)
        equation[0][0].set_color(BLUE)
        equation[0][1].set_color(YELLOW)
        equation[0][3].set_color(GREEN)
        equation[0][4].set_color(YELLOW)
        self.play(Write(equation), run_time=2)

class Orthogonal(Scene):
    def construct(self):
        assumption = Tex("Let ", "$x, y$", " be eigenvectors of ", "$A$",  " with distinct eigenvalues ", "$u, v$").shift(UP * 2.5)
        assumption[1][0].set_color(BLUE)
        assumption[1][2].set_color(TEAL)
        assumption[3].set_color(YELLOW)
        assumption[5][0].set_color(BLUE)
        assumption[5][2].set_color(TEAL)
        self.play(Write(assumption))
        self.wait(0.5)
        working = VGroup(MathTex("Ax\cdot y",  "= ux\cdot y", "= u(x\cdot y)"),
                         MathTex("= x\cdot A^Ty", "=x\cdot Ay", "=x\cdot vy", "=v(x\cdot y)"),
                         MathTex(r"u(x\cdot y) = v(x\cdot y),\ u\neq v", "\implies x\cdot y = 0"),
                         Tex("So, distinct eigenvalues will have orthogonal eigenvectors."),
                         Tex("For same eigenvalues, you can choose an orthonormal basis."))
        working.arrange(DOWN)
        working[0:2].shift(LEFT * 3)
        working[1].align_to(working[0][1], LEFT)
        working[0][1:].align_to(working[1][2], LEFT)
        working[0][0].align_to(working[1][0][1], LEFT)
        working[3:].shift(DOWN * 0.5)
        working[0][0][0].set_color(YELLOW)
        working[0][0][1].set_color(BLUE)
        working[0][0][3].set_color(TEAL)
        working[0][1][1:3].set_color(BLUE)
        working[0][1][4].set_color(TEAL)
        working[0][2][1].set_color(BLUE)
        working[0][2][3].set_color(BLUE)
        working[0][2][5].set_color(TEAL)
        working[1][0][1].set_color(BLUE)
        working[1][0][3:5].set_color(YELLOW)
        working[1][0][5].set_color(TEAL)
        working[1][1][1].set_color(BLUE)
        working[1][1][3].set_color(YELLOW)
        working[1][1][4].set_color(TEAL)
        working[1][2][1].set_color(BLUE)
        working[1][2][3:5].set_color(TEAL)
        working[1][3][1].set_color(TEAL)
        working[1][3][3].set_color(BLUE)
        working[1][3][5].set_color(TEAL)
        working[2][0][0].set_color(BLUE)
        working[2][0][2].set_color(BLUE)
        working[2][0][4].set_color(TEAL)
        working[2][0][7].set_color(TEAL)
        working[2][0][9].set_color(BLUE)
        working[2][0][11].set_color(TEAL)
        working[2][0][14].set_color(BLUE)
        working[2][0][17].set_color(TEAL)
        working[2][1][2].set_color(BLUE)
        working[2][1][4].set_color(TEAL)
        self.play(Write(working[:3]))
        self.wait(0.5)
        self.play(Write(working[3:]))

class PCAres(Scene):
    def construct(self):
        points = [VGroup() for i in range(10)]
        with open("pcaResult.txt", "r") as file:
            lines = file.readlines()
        cmap = plt.get_cmap('hsv')
        for i in range(2000):
            data = lines[i].split()
            points[int(data[2])].add(Dot(point=(1.8 * float(data[0]) / 6 - 2, float(data[1]) / 6, 0), color=ManimColor(cmap(int(data[2]) / 10)),
                           radius=0.05))
        key = VGroup()
        for i in range(10):
            key.add(Rectangle(width=0.2, height=0.2, fill_color=ManimColor(cmap(i / 10)), fill_opacity=1))
            key.add(MathTex(str(i)))
        key.arrange(RIGHT).to_edge(DOWN, buff=MED_SMALL_BUFF)
        self.add(key)
        self.wait()
        for i in range(10):
            self.play(FadeIn(points[i]))
        self.wait()
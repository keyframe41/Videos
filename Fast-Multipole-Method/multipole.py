from manim import *
import matplotlib.pyplot as plt
from scipy.ndimage import value_indices


class Multipole(Scene):
    def construct(self):
        self.wait(0.5)
        working = VGroup(MathTex(r"m_i", r"\log(z - z_i)"),
                         MathTex(r"m_i", r"\log\left(z\left(1 - \frac{z_i}{z}\right)\right)"),
                         MathTex(r"m_i \log{z} +", r"m_i\log \left(1 - \frac{z_i}{z}\right)"),
                         MathTex(r"m_i \log{z} +", r"m_i \sum_{k = 1}^\infty -\frac{1}{k}",
                                 r"\left(\frac{z_i}{z}\right)^k"))
        working[0:2].shift(UP * 1.2)
        working[-1].shift(DOWN * 1.2)
        self.play(Write(working[0]))
        temp = working[0][1][4].copy()
        self.play(ReplacementTransform(working[0][0], working[1][0]),
                  ReplacementTransform(working[0][1][:3], working[1][1][:3]),
                  FadeTransform(working[0][1][3], working[1][1][3]),
                  FadeTransform(working[0][1][-1], working[1][1][-1]),
                  ReplacementTransform(temp, working[1][1][4]),
                  ReplacementTransform(working[0][1][4:-1], working[1][1][5:-1]))
        self.wait()
        g1 = VGroup(working[1][0], working[1][1][:5].copy())
        g2 = VGroup(working[1][0].copy(), working[1][1])
        self.play(FadeTransform(g1.copy(), working[2][0]), FadeTransform(g2.copy(), working[2][1]))
        self.wait(0.5)
        self.play(ReplacementTransform(working[2][0].copy(), working[3][0]),
                  ReplacementTransform(working[2][1][:2].copy(), working[3][1][:2]),
                  ReplacementTransform(working[2][1][2:5].copy(), working[3][1][2:]),
                  ReplacementTransform(working[2][1][5].copy(), working[3][2][0]),
                  ReplacementTransform(working[2][1][-1].copy(), working[3][2][-2:]),
                  ReplacementTransform(working[2][1][8:-1].copy(), working[3][2][1:-2]),
                  )
        self.wait()

def getGrid():
    layers = VGroup()
    yorange = (YELLOW + ORANGE) / 2

    layers.add(Rectangle(height=6, width=6, color=yorange, stroke_width=3.5))

    def subdivide(rect):
        d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
        len = rect.width
        center = rect.get_center()
        return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3.5).move_to(
            center + len * (d[i][0] * RIGHT + d[i][1] * UP)) for i in range(4)).set_color(yorange)
        # return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3.5).move_to(
        #     center + d[i][0] * (len) * RIGHT + d[i][1] * (len) * UP) for i in range(4))

    layers.add(subdivide(layers[0]))
    layers.add(subdivide(layers[1][0]))
    layers[2].add(*subdivide(layers[1][1]))
    layers[2].add(*subdivide(layers[1][2]))
    next = [3, 4, 5, 7, 8]
    layers.add(subdivide(layers[2][2]))
    for i in next:
        layers[-1].add(*subdivide(layers[2][i]))
    layers.add(subdivide(layers[3][2]))
    next = [16, 17, 19, 20]
    for i in next:
        layers[-1].add(*subdivide(layers[3][i]))
    layers.add(subdivide(layers[4][6]))
    layers[-1].add(*subdivide(layers[4][13]))

    return layers


class Introduce(Scene):
    def construct(self):
        line = Line(UP * 4, DOWN * 4)

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 1000
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.5},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        coords = [[ValueTracker(0.5 * np.cos(i * np.pi / 5)), ValueTracker(0.5 * np.sin(i * np.pi / 5))] for i in
                  range(10)]

        # points = [0.5 * np.cos(i * np.pi / 5) + 0.5j * np.sin(i * np.pi / 5) for i in range(10)]

        def f(z):
            ans = np.zeros_like(z)
            for i in range(len(coords)):
                ans += np.real(np.log(z - (coords[i][0].get_value() + 1j * coords[i][1].get_value())))
            return np.real(ans)

        def get_heatmap(func):
            raw_values = func(Z)
            raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

            val_min, val_max = raw_values.min(), raw_values.max()
            # print(val_min, val_max)
            cmap = plt.get_cmap("plasma")
            rgba_image = cmap((raw_values + 5) / 25)
            rgba_image[:, :, 3] = 0.75
            rgb_uint8 = (rgba_image * 255).astype(np.uint8)

            res = ImageMobject(rgb_uint8)
            res.width = plane.x_length
            res.height = plane.y_length
            return res.shift(LEFT * 32 / 9)

        self.wait(0.5)
        fakeplane = plane.copy().shift(RIGHT * 64 / 9)
        fakeborder = border.copy().shift(RIGHT * 64 / 9)

        self.play(Write(line), Create(border), Write(plane), run_time=2)
        self.wait(0.5)
        dot_opacity = ValueTracker(1.0)
        dots = always_redraw(lambda: VGroup([Dot(color=GREEN, radius=DEFAULT_DOT_RADIUS * 0.6).move_to(
            plane.c2p(coords[i][0].get_value(), coords[i][1].get_value())).set_opacity(1 if i == 0 else dot_opacity.get_value())
                                             for i in range(len(coords))])).set_z_index(5)
        heatmap = always_redraw(lambda: get_heatmap(f))

        def bf_pot(z):
            return 10 * np.real(np.log(z))

        fakeheatmap = get_heatmap(bf_pot).shift(RIGHT * 64 / 9)
        fakedot = Dot(radius=DEFAULT_DOT_RADIUS * 3, color=GREEN_D).shift(RIGHT * 32 / 9).set_z_index(5)
        self.play(Write(dots))
        self.play(FadeIn(heatmap))
        self.wait()
        self.play(Create(fakeborder), Write(fakeplane), FadeIn(fakeheatmap), Write(fakedot))
        self.wait()
        self.play(AnimationGroup(*[coords[i][0].animate.increment_value(0.5) for i in range(-2, 3)]),
                  AnimationGroup(*[coords[i][0].animate.increment_value(-0.5) for i in range(3, 8)]))
        self.wait(0.5)
        self.play(AnimationGroup(*[coords[i][0].animate.increment_value(-0.5) for i in [-2, 2]]),
                  AnimationGroup(*[coords[i][0].animate.increment_value(0.5) for i in [-3, 3]]),
                  AnimationGroup(*[coords[i][1].animate.increment_value(0.3) for i in [2, 3]]),
                  AnimationGroup(*[coords[i][1].animate.increment_value(-0.3) for i in [-3, -2]]), run_time=0.75)
        self.wait(0.5)
        self.play(AnimationGroup(*[coords[i][1].animate.increment_value(-0.4) for i in [2, 3]]),
                  AnimationGroup(*[coords[i][1].animate.increment_value(0.4) for i in [-3, -2]]),
                  AnimationGroup(*[coords[i][0].animate.increment_value(0.3) for i in [-1, 1]]),
                  AnimationGroup(*[coords[i][0].animate.increment_value(-0.3) for i in [4, 6]]),
                  coords[0][0].animate.increment_value(0.5),
                  coords[5][0].animate.increment_value(-0.5), run_time=0.75)
        self.wait(0.5)
        final_coords = [[1, 0], [0.6, 0.4], [0.5, 0.9], [-0.4, 0.8], [-0.8, 0.3], [-0.9, 0.6],
                        [-1.1, -0.2], [-0.6, -0.5], [-0.3, -1], [0.2, -0.7], [0.7, -0.8]]
        self.play(AnimationGroup(*[coords[i][0].animate.set_value(final_coords[i][0]) for i in range(10)]),
                  AnimationGroup(*[coords[i][1].animate.set_value(final_coords[i][1]) for i in range(10)]),
                  run_time=0.75)
        self.wait()
        approximation = Text("Multipole Expansion").to_edge(UP).shift(RIGHT * 32 / 9)
        heatmap.clear_updaters()
        self.play(Unwrite(fakedot), Unwrite(fakeplane), FadeOut(fakeheatmap), Unwrite(fakeborder), Write(approximation))
        eval_dot = Dot(color=BLUE).move_to(plane.c2p(3, -3))
        eval_label = MathTex("z").scale(0.6).next_to(eval_dot, DOWN)
        source_label = MathTex("z_i").scale(0.6).next_to(dots[0], UP + RIGHT)
        self.play(heatmap.animate.set_opacity(0.4), plane.animate.set_opacity(0.2),
                  dot_opacity.animate.set_value(0.25),
                  Write(eval_dot), Write(eval_label), Write(source_label))

        self.wait()

        bh_approx = Tex("B-H: ", r"$P(z) = \sum m_i\log(z)$").shift(RIGHT * 32 / 9)
        bh_approx[1][2].set_color(BLUE)
        bh_approx[1][6:8].set_color(YELLOW)
        bh_approx[1][-2].set_color(BLUE)

        self.play(Write(bh_approx))
        self.wait(0.5)

        working = VGroup(MathTex(r"m_i", r"\log(z - z_i)"),
                         MathTex("=", r"m_i", r"\log\left(z\left(1 - \frac{z_i}{z}\right)\right)"),
                         MathTex("=", r"m_i \log{z} +", r"m_i\log \left(1 - \frac{z_i}{z}\right)"),
                         MathTex("=", r"m_i \log{z} +", r"m_i \sum_{k = 1}^\infty -\frac{1}{k}",
                                 r"\left(\frac{z_i}{z}\right)^k")).scale(0.8).arrange(DOWN).shift(
            RIGHT * 32 / 9 + UP * 0.5)
        working[0][0].set_color(YELLOW)
        working[0][1][4].set_color(BLUE)
        working[0][1][6:8].set_color(GREEN)

        working[1][1].set_color(YELLOW)
        working[1][2][4].set_color(BLUE)
        working[1][2][8:10].set_color(GREEN)
        working[1][2][11].set_color(BLUE)

        working[2][1][:2].set_color(YELLOW)
        working[2][1][-2].set_color(BLUE)
        working[2][2][:2].set_color(YELLOW)
        working[2][2][8:10].set_color(GREEN)
        working[2][2][11].set_color(BLUE)

        working[3][1][:2].set_color(YELLOW)
        working[3][1][-2].set_color(BLUE)
        working[3][2][:2].set_color(YELLOW)
        working[3][3][1:3].set_color(GREEN)
        working[3][3][4].set_color(BLUE)

        working[3].align_to(working[1], UP)
        working[2].shift(UP * (working[3][0][0].get_y() - working[2][0][0].get_y()))
        working[1].move_to(working[0])

        self.play(Write(working[0]), bh_approx.animate.shift(UP * 2).set_opacity(0))
        temp = working[0][1][4].copy()
        self.wait()
        self.play(Write(working[1][0]),
                  ReplacementTransform(working[0][0], working[1][1]),
                  ReplacementTransform(working[0][1][:3], working[1][2][:3]),
                  FadeTransform(working[0][1][3], working[1][2][3]),
                  FadeTransform(working[0][1][-1], working[1][2][-1]),
                  ReplacementTransform(temp, working[1][2][4]),
                  ReplacementTransform(working[0][1][4:-1], working[1][2][5:-1]))
        self.wait()
        g1 = VGroup(working[1][1], working[1][2][:5].copy())
        g2 = VGroup(working[1][1].copy(), working[1][2])
        self.play(ReplacementTransform(working[1][0], working[2][0]),
                  FadeTransform(g1.copy(), working[2][1]), FadeTransform(g2.copy(), working[2][2]))
        self.remove()
        self.wait(0.5)
        self.play(ReplacementTransform(working[2][0], working[3][0]),
                  ReplacementTransform(working[2][1], working[3][1]),
                  ReplacementTransform(working[2][2][:2], working[3][2][:2]),
                  ReplacementTransform(working[2][2][2:5], working[3][2][2:]),
                  ReplacementTransform(working[2][2][5], working[3][3][0]),
                  ReplacementTransform(working[2][2][-1], working[3][3][-2:]),
                  ReplacementTransform(working[2][2][8:-1], working[3][3][1:-2]),
                  Unwrite(working[2][2][6:8]))
        self.wait()
        plane_unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]
        conv = VGroup(
            Circle(radius=plane_unit, stroke_opacity=0, fill_opacity=0.3, fill_color=BLACK).move_to(plane.c2p(0, 0)),
            DashedVMobject(Circle(radius=plane_unit, color=WHITE).move_to(plane.c2p(0, 0)), dashed_ratio=0.5), )
        self.wait()
        conv_text = Tex("Converges when ", r"$|z_i| < |z|$").scale(0.75).shift(RIGHT * 32 / 9)
        conv_text[1][1:3].set_color(GREEN)
        conv_text[1][6].set_color(BLUE)
        self.play(Write(conv_text))
        self.play(FadeIn(conv), run_time=1)
        self.wait()

        working2 = VGroup(MathTex(
            r"P(z) = \sum_{i = 1}^n \left(m_i\log z + m_i \sum_{k = 1}^\infty -\frac{1}{k} \left(\frac{z_i}{z}\right)^k\right)"),
                          MathTex("P(z) = \sum_{i = 1}^n m_i\log z + ",
                                  r"\sum_{i = 1}^n m_i \sum_{k = 1}^\infty -\frac{1}{k}",
                                  r"\left(\frac{z_i}{z}\right)^k"),
                          MathTex("P(z) = \sum_{i = 1}^n m_i\log z + ",
                                  r"\sum_{k = 1}^\infty", r"\left(-\sum_{i = 1}^n\frac{m_i z_i^k}{k}\right)",
                                  r"\frac{1}{z^k}"),
                          MathTex("P(z) = a_0\log z +", "\sum_{k = 1}^\infty a_k z^{-k}"))
        working2.shift(RIGHT * 32 / 9 + DOWN).scale(0.7)
        y = working2[0][0][0].get_center()[1]
        for w in working2:
            w.shift(UP * (y - w[0][0].get_center()[1]))
        working2[0][0][2].set_color(BLUE)
        working2[0][0][11:13].set_color(YELLOW)
        working2[0][0][16].set_color(BLUE)
        working2[0][0][18:20].set_color(YELLOW)
        working2[0][0][30:32].set_color(GREEN)
        working2[0][0][33].set_color(BLUE)

        working2[1][0][2].set_color(BLUE)
        working2[1][0][10:12].set_color(YELLOW)
        working2[1][0][15].set_color(BLUE)
        working2[1][1][5:7].set_color(YELLOW)
        working2[1][2][1:3].set_color(GREEN)
        working2[1][2][4].set_color(BLUE)

        working2[2][0][2].set_color(BLUE)
        working2[2][0][10:12].set_color(YELLOW)
        working2[2][0][15].set_color(BLUE)
        working2[2][2][7:9].set_color(YELLOW)
        working2[2][2][9].set_color(GREEN)
        working2[2][2][11].set_color(GREEN)
        working2[2][3][2].set_color(BLUE)

        working2[3][0][2].set_color(BLUE)
        working2[3][0][5:7].set_color(YELLOW)
        working2[3][0][10].set_color(BLUE)
        working2[3][1][5:7].set_color(YELLOW)
        working2[3][1][7].set_color(BLUE)

        self.play(Write(working2[0]))
        self.wait()
        self.play(Unwrite(working2[0][0][10]), Unwrite(working2[0][0][-1]),
                  ReplacementTransform(working2[0][0][:10], working2[1][0][:10]),
                  ReplacementTransform(working2[0][0][11:18], working2[1][0][10:]),
                  ReplacementTransform(working2[0][0][5:10].copy(), working2[1][1][:5]),
                  ReplacementTransform(working2[0][0][18:29], working2[1][1][5:]),
                  ReplacementTransform(working2[0][0][29:-1], working2[1][2]), )
        self.wait()
        self.play(AnimationGroup([AnimationGroup([ReplacementTransform(working2[1][0], working2[2][0]),
                                                  Unwrite(working2[1][2][0]), Unwrite(working2[1][2][-2]),
                                                  Unwrite(working2[1][1][-3]),
                                                  Write(working2[2][3][0]),
                                                  ReplacementTransform(working2[1][1][:5], working2[2][2][2:7]),
                                                  ReplacementTransform(working2[1][1][5:7], working2[2][2][7:9]),
                                                  ReplacementTransform(working2[1][1][7:12], working2[2][1]),
                                                  ReplacementTransform(working2[1][1][12], working2[2][2][1]),
                                                  ReplacementTransform(working2[1][1][14:], working2[2][2][12:14]),
                                                  ReplacementTransform(working2[1][2][1], working2[2][2][9]),
                                                  ReplacementTransform(working2[1][2][2], working2[2][2][11]),
                                                  ReplacementTransform(working2[1][2][3], working2[2][3][1]),
                                                  ReplacementTransform(working2[1][2][4], working2[2][3][2]),
                                                  ReplacementTransform(working2[1][2][-1], working2[2][2][-5]),
                                                  ReplacementTransform(working2[1][2][-1].copy(), working2[2][3][-1])]),
                                  AnimationGroup([Write(working2[2][2][0]), Write(working2[2][2][-1])])],
                                 lag_ratio=0.5), run_time=2)
        self.wait()
        braces = VGroup(Brace(working2[2][2]), Brace(working2[2][0][5:12]))
        self.play(Write(braces))
        self.wait(0.5)

        coefficients = MathTex("a_0 = \sum_{i = 1}^n m_i", r"a_k = -\sum_{i = 1}^n\frac{m_i z_i^k}{k}")
        coefficients.scale(0.7).shift(RIGHT * 32 / 9 + DOWN * 2.2)
        coefficients[1].shift(RIGHT * 0.6)
        coefficients[0].shift(LEFT * 0.3)
        coefficients[0][:2].set_color(YELLOW)
        coefficients[0][-2:].set_color(YELLOW)
        coefficients[1][:2].set_color(YELLOW)
        coefficients[1][9:11].set_color(YELLOW)
        coefficients[1][11].set_color(GREEN)
        coefficients[1][13].set_color(GREEN)
        self.play(ReplacementTransform(working2[2][0][:5], working2[3][0][:5]),
                  ReplacementTransform(working2[2][0][5:12], working2[3][0][5:7]),
                  ReplacementTransform(working2[2][0][12:], working2[3][0][7:]),
                  ReplacementTransform(working2[2][1], working2[3][1][:5]),
                  ReplacementTransform(working2[2][2], working2[3][1][5:7]),
                  ReplacementTransform(working2[2][3], working2[3][1][7:]),
                  FadeOut(braces),
                  FadeIn(coefficients, shift=DOWN), )
        self.wait()

        temp = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                            x_length=plane_size, y_length=plane_size,
                            axis_config={"color": WHITE, "stroke_width": 2.5},
                            background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.5},
                            faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                            faded_line_ratio=5).shift(LEFT * 32 / 9).set_z_index(-5)
        self.play(AnimationGroup([
            AnimationGroup([FadeOut(working[1]), FadeOut(working[3]), FadeOut(conv_text), working2[-1].animate.shift(UP * 3.2),
                            Unwrite(coefficients), Transform(plane, temp), Unwrite(eval_dot), Unwrite(source_label),
                            FadeOut(eval_dot), Unwrite(eval_label)]),
            AnimationGroup([FadeOut(conv), heatmap.animate.set_opacity(0.75), dot_opacity.animate.set_value(1)])
        ], lag_ratio=0.5))
        self.wait()

        def interpolate(f1, f2, t):
            return f1(Z) * (1 - t.get_value()) + f2(Z) * t.get_value()

        def get_truncated(p, center):
            a_coeff = [10]
            for k in range(1, 16):
                res = 0
                for xt, yt in coords:
                    x = xt.get_value()
                    y = yt.get_value()
                    z_i = x + 1j * y
                    res += (z_i - center) ** k
                a_coeff.append(-1 / k * res)
            def evaluate(z):
                res = a_coeff[0] * np.log(z - center)
                for k in range(1, p + 1):
                    res += a_coeff[k] * (z - center) ** -k
                return np.real(res)

            return evaluate

        truncated = MathTex("P_0(z) = a_0\log z").shift(RIGHT * 32 / 9 + UP * 0.5)
        truncated[0][3].set_color(BLUE)
        truncated[0][6:8].set_color(YELLOW)
        truncated[0][-1].set_color(BLUE)

        def get_truncated_exp(p):
            str1 = "P_{" + str(p) + "}(z) = a_0\log z"
            str2 = "+ \sum_{k = 1}^{" + str(p) + "} a_k z^{-k}"
            temp = MathTex(str1, str2).shift(RIGHT * 32 / 9 + UP * 0.5)
            temp[0][-9].set_color(BLUE)
            temp[0][-6:-4].set_color(YELLOW)
            temp[0][-1].set_color(BLUE)
            temp[1][-5:-3].set_color(YELLOW)
            temp[1][-3].set_color(BLUE)
            return temp

        heatmap.clear_updaters()
        interp = ValueTracker(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(lambda z: interpolate(f, get_truncated(0, 0), interp))
        ))
        self.play(interp.animate.set_value(1), Write(truncated[0]))
        self.wait()
        heatmap.clear_updaters()
        interp.set_value(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(lambda z: interpolate(get_truncated(0, 0), get_truncated(1, 0), interp))
        ))
        next = get_truncated_exp(1)
        self.play(interp.animate.set_value(1), FadeTransform(truncated, next[0]),
                  Write(next[1]))
        truncated = next
        self.wait()
        for i in range(1, 10):
            heatmap.clear_updaters()
            interp.set_value(0)
            heatmap.add_updater(lambda m: m.become(
                get_heatmap(lambda z: interpolate(get_truncated(i, 0), get_truncated(i + 1, 0), interp))
            ))
            if i < 9:
                next = get_truncated_exp(i + 1)
                self.play(interp.animate.set_value(1),
                          ReplacementTransform(truncated[0][0], next[0][0]),
                          ReplacementTransform(truncated[0][-10:], next[0][-10:]),
                          ReplacementTransform(truncated[0][1:-10], next[0][1:-10]),
                          ReplacementTransform(truncated[1][0], next[1][0]),
                          ReplacementTransform(truncated[1][-9:], next[1][-9:]),
                          ReplacementTransform(truncated[1][1:-9], next[1][1:-9])
                          , run_time=0.75)
            else:
                next = get_truncated_exp("p").shift(UP * 1.5)
                self.play(interp.animate.set_value(1),
                          ReplacementTransform(truncated[0][0], next[0][0]),
                          ReplacementTransform(truncated[0][-10:], next[0][-10:]),
                          ReplacementTransform(truncated[0][1:-10], next[0][1:-10]),
                          ReplacementTransform(truncated[1][0], next[1][0]),
                          ReplacementTransform(truncated[1][-9:], next[1][-9:]),
                          ReplacementTransform(truncated[1][1:-9], next[1][1:-9]),
                          FadeOut(working2[-1]))
            truncated = next
        heatmap.clear_updaters()
        self.wait()

        conv_text = MathTex(r"\text{Converges when }", r"\max_{1\leq i \leq n}|z_i| < |z|").scale(0.75).shift(
            RIGHT * 32 / 9 + UP * 0.7)
        conv_text[1][-7:-5].set_color(GREEN)
        conv_text[1][-2].set_color(BLUE)
        self.play(Write(conv_text))

        m_radius = max(
            [np.sqrt(coords[i][0].get_value() ** 2 + coords[i][1].get_value() ** 2) for i in range(10)]) * plane_unit
        conv_circle = VGroup(
            Circle(radius=m_radius, stroke_opacity=0, fill_opacity=0.3, fill_color=BLACK).move_to(plane.c2p(0, 0)),
            DashedVMobject(Circle(radius=m_radius, color=WHITE).move_to(plane.c2p(0, 0)), dashed_ratio=0.5))
        self.play(FadeIn(conv_circle))
        self.wait()

        grid = getGrid().shift(LEFT * 32 / 9).set_color(BLUE)
        self.play(FadeIn(grid), FadeOut(conv_circle))
        self.wait()

        new_coords = [[-0.1, -0.4], [-0.2, -0.8], [-0.3, -0.2], [-0.4, -0.6], [-0.5, -0.9],
                  [-0.6, -0.5], [-0.7, -0.7], [-0.8, -0.3], [-0.9, -0.6], [-3.7, -3.8]]
        avg = np.mean(new_coords, axis=0)
        com = avg[0] + 1j * avg[1]

        com_circle = Circle(radius = DEFAULT_DOT_RADIUS * 1.5, color=RED, stroke_width=4).move_to(plane.c2p(avg[0], avg[1]))

        heatmap.add_updater(lambda m: m.become(get_heatmap(get_truncated(10, com * interp.get_value())) ) )
        interp.set_value(0)
        self.play(AnimationGroup(*[coords[i][0].animate.set_value(new_coords[i][0]) for i in range(10)]),
                  AnimationGroup(*[coords[i][1].animate.set_value(new_coords[i][1]) for i in range(10)]),
                  interp.animate.set_value(1), Write(com_circle),
                  run_time=1)
        self.wait()
        m_radius = max(
            [np.sqrt((coords[i][0].get_value() - avg[0]) ** 2 + (coords[i][1].get_value() - avg[1]) ** 2) for i in range(10)]) * plane_unit
        conv_circle = VGroup(
            Circle(radius=m_radius, stroke_opacity=0, fill_opacity=0.3, fill_color=BLACK).move_to(plane.c2p(avg[0], avg[1])),
            DashedVMobject(Circle(radius=m_radius, color=WHITE).move_to(plane.c2p(avg[0], avg[1])), dashed_ratio=0.5, num_dashes=50))
        self.play(FadeIn(conv_circle))
        self.wait()

        heatmap.clear_updaters()
        interp.set_value(0)
        heatmap.add_updater(lambda m: m.become(get_heatmap(get_truncated(10, com * (1 - interp.get_value())
                                                                         + (-2 - 2j)  * interp.get_value() ) )))
        m_radius = max(
            [np.sqrt((coords[i][0].get_value() + 2) ** 2 + (coords[i][1].get_value() + 2) ** 2) for i in
             range(10)]) * plane_unit
        conv_circle_2 = VGroup(
            Circle(radius=m_radius, stroke_opacity=0, fill_opacity=0.3, fill_color=BLACK).move_to(plane.c2p(-2, -2)),
            DashedVMobject(Circle(radius=m_radius, color=WHITE).move_to(plane.c2p(-2, -2)), dashed_ratio=0.5, num_dashes=50))
        self.play(Transform(conv_circle, conv_circle_2), interp.animate.set_value(1), com_circle.animate.move_to(plane.c2p(-2, -2)))
        # self.play(Transform(conv_circle, conv_circle_2), com_circle.animate.move_to(plane.c2p(-2, -2)),
        #           Transform(heatmap, get_heatmap(get_truncated(10, -2-2j))) )
        self.wait()

        error = VGroup(MathTex(r"\text{Error}=", r"\left|\sum_{k = p + 1}^\infty a_k z^{-k}\right|"),
                       MathTex(r"= \left|\sum_{k = p + 1}^\infty \left(-\sum_{i = 1}^n \frac{m_i}{k}\right) \frac{z_i^k}{z^k}\right|"),
                       MathTex(r"\leq \sum_{k = p + 1}^\infty \sum_{i = 1}^n", r"\frac{m_i}{p + 1}\left|\frac{r^k}{z^k}\right|"),
                       MathTex(r"\leq \frac{a_0}{p + 1}", r"\sum_{k = p + 1}^\infty", r"\left|\frac{r}{z}\right|^k"),
                       MathTex(r"\leq \frac{a_0}{p + 1}", r"\frac{\left|\frac{r}{z}\right|^{p + 1}}{1 - \left|\frac{r}{z}\right|}"),
                       MathTex(r"\leq \frac{a_0}{p + 1}", r"\frac{\left|\frac{r}{z}\right|^p}{\left|\frac{z}{r}\right| - 1}"),
                       MathTex(r"\leq \frac{a_0}{(p + 1)(\left|\frac{z}{r}\right| - 1)}", r"\left|\frac{r}{z}\right|^p"),
                       # MathTex(r"\leq \frac{a_0}{(p + 1)(c - 1)} \left(\frac{1}{c}\right)^p")
                       )
        error.shift(RIGHT * 3 + DOWN * 0.5).scale(0.75)
        error[0][1][13:15].set_color(YELLOW)
        error[0][1][15].set_color(BLUE)

        error[1][0][21:23].set_color(YELLOW)
        error[1][0][26].set_color(GREEN)
        error[1][0][28].set_color(GREEN)
        error[1][0][30].set_color(BLUE)

        error[2][1][:2].set_color(YELLOW)
        error[2][1][10].set_color(GREEN)
        error[2][1][13].set_color(BLUE)

        error[3][0][1:3].set_color(YELLOW)
        error[3][2][3].set_color(GREEN)
        error[3][2][5].set_color(BLUE)

        error[4][0][1:3].set_color(YELLOW)
        error[4][1][2].set_color(GREEN)
        error[4][1][4].set_color(BLUE)
        error[4][1][15].set_color(GREEN)
        error[4][1][17].set_color(BLUE)

        error[5][0][1:3].set_color(YELLOW)
        error[5][1][2].set_color(GREEN)
        error[5][1][4].set_color(BLUE)
        error[5][1][11].set_color(BLUE)
        error[5][1][13].set_color(GREEN)

        error[6][0][1:3].set_color(YELLOW)
        error[6][0][12].set_color(BLUE)
        error[6][0][14].set_color(GREEN)
        error[6][1][3].set_color(GREEN)
        error[6][1][5].set_color(BLUE)

        # error[7][0][1:3].set_color(YELLOW)
        # error[7][0][10].set_color(BLUE)
        # error[7][0][17].set_color(BLUE)

        self.play(Write(error[0]))
        self.wait()
        error[1].next_to(error[0], DOWN)
        error[1].shift(RIGHT * (error[0][0][5].get_x() - error[1][0][0].get_x()))
        self.play(ReplacementTransform(error[0][0][5].copy(), error[1][0][0]),
                  ReplacementTransform(error[0][1][:13].copy(), error[1][0][1:14]),
                  ReplacementTransform(error[0][1][13:15].copy(), error[1][0][14:26]),
                  ReplacementTransform(error[0][1][13:15].copy(), error[1][0][26:30]),
                  ReplacementTransform(error[0][1][15].copy(), error[1][0][30]),
                  ReplacementTransform(error[0][1][17].copy(), error[1][0][31]),
                  ReplacementTransform(error[0][1][18:].copy(), error[1][0][32:]),
                  )
        self.wait()
        radius_arrow = Arrow(plane.c2p(-2, -2), plane.c2p(-2 + m_radius / plane_unit, -2), color=GREEN, buff=0)
        radius_label = MathTex("r").scale(0.75).next_to(radius_arrow, DOWN).shift(UP * 0.1)
        self.play(GrowArrow(radius_arrow), Write(radius_label),)
        error[2].shift(error[1][0][0].get_center() - error[2][0][0].get_center())
        self.play(ReplacementTransform(error[1][0][0], error[2][0][0]),
                  ReplacementTransform(error[1][0][1:7], error[2][1][6:10]),
                  ReplacementTransform(error[1][0][7:14], error[2][0][1:8]),
                  ReplacementTransform(error[1][0][16:21], error[2][0][8:13]),
                  ReplacementTransform(error[1][0][21:23], error[2][1][:2]),
                  ReplacementTransform(error[1][0][23], error[2][1][2]),
                  ReplacementTransform(error[1][0][24], error[2][1][3:6]),
                  Unwrite(error[1][0][14:16]), Unwrite(error[1][0][25]),
                  ReplacementTransform(error[1][0][29], error[2][1][12]),
                  ReplacementTransform(VGroup(error[1][0][26], error[1][0][28]), error[2][1][10]),
                  ReplacementTransform(error[1][0][27], error[2][1][11]),
                  ReplacementTransform(error[1][0][30:32], error[2][1][13:15]),
                  ReplacementTransform(error[1][0][32:], error[2][1][15:]),
                  )
        self.wait()
        error[3].shift(error[1][0][0].get_center() - error[3][0][0].get_center())
        self.play(ReplacementTransform(error[2][0][0], error[3][0][0]),
                  ReplacementTransform(VGroup(error[2][0][8:], error[2][1][:2]), error[3][0][1:3]),
                  ReplacementTransform(error[2][0][1:8], error[3][1][:7]),
                  ReplacementTransform(error[2][1][2:6], error[3][0][3:7]),
                  ReplacementTransform(error[2][1][6:10], error[3][2][:3]),
                  ReplacementTransform(error[2][1][10], error[3][2][3]),
                  ReplacementTransform(error[2][1][11], error[3][2][9]),
                  ReplacementTransform(error[2][1][12], error[3][2][4]),
                  ReplacementTransform(error[2][1][13], error[3][2][5]),
                  ReplacementTransform(error[2][1][15:], error[3][2][6:9]),
                  FadeOut(error[2][1][14], shift=(error[3][2][9].get_center() - error[2][1][14].get_center()) ),
                  )
        self.wait()
        error[4].shift(error[1][0][0].get_center() - error[4][0][0].get_center())
        self.play(ReplacementTransform(error[3][0], error[4][0]),
                  Unwrite(error[3][1][:4]),
                  ReplacementTransform(error[3][1][4:7], error[4][1][7:10]),
                  ReplacementTransform(error[3][2][0:3], error[4][1][0:2]),
                  ReplacementTransform(error[3][2][3:6], error[4][1][2:5]),
                  ReplacementTransform(error[3][2][6:9], error[4][1][5:7]),
                  Write(error[4][1][10:13]),
                  ReplacementTransform(error[3][2][0:3].copy(), error[4][1][13:15]),
                  ReplacementTransform(error[3][2][3:6].copy(), error[4][1][15:18]),
                  ReplacementTransform(error[3][2][6:9].copy(), error[4][1][18:20]),
                  Unwrite(error[3][2][9]),
                  )
        self.wait()
        error[5].shift(error[1][0][0].get_center() - error[5][0][0].get_center())
        self.play(ReplacementTransform(error[4][0], error[5][0]),
                  ReplacementTransform(error[4][1][:7], error[5][1][:7]),
                  ReplacementTransform(error[4][1][7:10], error[5][1][7]),
                  ReplacementTransform(error[4][1][10], error[5][1][8]),
                  ReplacementTransform(error[4][1][11], error[5][1][9:16]),
                  ReplacementTransform(error[4][1][12], error[5][1][16]),
                  ReplacementTransform(error[4][1][13:], error[5][1][17]),
                  )
        self.wait()
        error[6].shift(error[1][0][0].get_center() - error[6][0][0].get_center())
        self.play(ReplacementTransform(error[5][0][:3], error[6][0][:3]),
                  ReplacementTransform(VGroup(error[5][0][3], error[5][1][8]), error[6][0][3]),
                  Write(VGroup(error[6][0][4], error[6][0][8:10], error[6][0][19])),
                  ReplacementTransform(error[5][0][4:7], error[6][0][5:8]),
                  ReplacementTransform(error[5][1][9:], error[6][0][10:19]),
                  ReplacementTransform(error[5][1][:2], error[6][1][:3]),
                  ReplacementTransform(error[5][1][2], error[6][1][3]),
                  ReplacementTransform(error[5][1][3], error[6][1][4]),
                  ReplacementTransform(error[5][1][4], error[6][1][5]),
                  ReplacementTransform(error[5][1][5:7], error[6][1][6:9]),
                  ReplacementTransform(error[5][1][7], error[6][1][9]),
                  )
        self.wait()
        # error[7].shift(error[1][0][0].get_center() - error[7][0][0].get_center())
        # self.play(ReplacementTransform(error[6][0][:10], error[7][0][:10]),
        #           ReplacementTransform(error[6][0][10:17], error[7][0][10]),
        #           ReplacementTransform(error[6][0][17:], error[7][0][11:14]),
        #           ReplacementTransform(error[6][1][0:3], error[7][0][14]),
        #           ReplacementTransform(error[6][1][3:6], error[7][0][15:18]),
        #           ReplacementTransform(error[6][1][6:9], error[7][0][18]),
        #           ReplacementTransform(error[6][1][9], error[7][0][19]),
        #           )
        # self.wait()
        conv_circle.set_z_index(20)
        radius_arrow.set_z_index(20)
        radius_label.set_z_index(20)
        self.play(FadeOut(grid), FadeOut(radius_arrow), FadeOut(radius_label), FadeOut(com_circle))
        self.wait(0.5)
        heatmap.clear_updaters()
        self.play(Transform(heatmap, get_heatmap(f).set_opacity(0.75)))
        self.wait()
        self.play(Transform(heatmap, get_heatmap(get_truncated(10, -2 - 2j)).set_opacity(0.75) ))
        self.wait()


class Poles(Scene):
    def construct(self):
        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 1000
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.5},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).shift(LEFT * 2.5 + DOWN * 0.5)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        self.add(plane, border)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        def get_heatmap(func):
            raw_values = func(Z)
            raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

            val_min, val_max = raw_values.min(), raw_values.max()
            cmap = plt.get_cmap("plasma")
            rgba_image = cmap((raw_values + 5) / 25)
            rgba_image[:, :, 3] = 0.75
            rgb_uint8 = (rgba_image * 255).astype(np.uint8)

            res = ImageMobject(rgb_uint8)
            res.width = plane.x_length
            res.height = plane.y_length
            return res.shift(LEFT * 2.5 + DOWN * 0.5)

        def interpolate(f1, f2, t):
            return f1(Z) * (1 - t.get_value()) + f2(Z) * t.get_value()

        def get_pole(p):
            def evaluate(z):
                if p == 0:
                    return np.real(np.log(z))
                return 10 * np.real(z ** -p)

            return evaluate

        heatmap = get_heatmap(get_pole(1))
        self.add(heatmap)

        self.wait()
        title = Text("Multipoles").to_edge(UP)

        def get_exp(p):
            s = r"\operatorname{Re}\left(\frac{1}{z^{" + str(p) + r"}}\right)"
            temp = MathTex(s)
            temp[0][-3].set_color(BLUE)
            return temp.shift(RIGHT * 2.5 + DOWN * 0.5)

        expression = get_exp(1)

        self.play(AnimationGroup(*[Write(title), Write(expression)], lag_ratio=0.5))
        self.wait()
        for i in range(1, 9):
            tracker = ValueTracker(0)
            heatmap.clear_updaters()
            heatmap.add_updater(lambda m: m.become(
                get_heatmap(lambda z: interpolate(get_pole(i), get_pole(i + 1), tracker))
            ))
            next = get_exp(i + 1)
            # new = get_heatmap(get_truncated(i + 1))
            self.play(tracker.animate.set_value(1), Transform(expression, next), run_time=0.75)




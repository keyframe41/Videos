from manim import *
import matplotlib.pyplot as plt


def subdivide(rect):
    yorange = (YELLOW + ORANGE) / 2
    d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
    len = rect.width
    center = rect.get_center()
    return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3).move_to(
        center + len * (d[i][0] * RIGHT + d[i][1] * UP)) for i in range(4)).set_color(yorange)

def getGrid(instance):
    layers = VGroup()
    yorange = (YELLOW + ORANGE) / 2

    layers.add(Rectangle(height=6, width=6, color=yorange, stroke_width=3))

    if instance == 1:
        for layer in range(1, 4):
            layers.add(subdivide(layers[layer - 1][0]))
            for i in range(1, len(layers[layer - 1])):
                layers[layer].add(*subdivide(layers[layer - 1][i]))
    else:
        layers.add(subdivide(layers[0][0]))
        layers.add(subdivide(layers[1][1]))
        layers[-1].add(*subdivide(layers[1][2]))
        layers.add(subdivide(layers[2][2]))
        for i in range(3, 6):
            layers[-1].add(*subdivide(layers[2][i]))

    return layers


class Shift(Scene):
    def construct(self):
        cmap = plt.get_cmap("plasma")

        line = Line(UP * 4, DOWN * 4).set_z_index(10)

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 3000
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.2},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        title = Text("Multipole Shift").to_edge(UP).shift(RIGHT * 32 / 9)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        def f(z):
            ans = np.zeros_like(z)
            for i in range(len(source_coords)):
                ans += np.real(np.log(z - (source_coords[i][0] + 1j * source_coords[i][1])))
            return np.real(ans)

        def get_multipole(p, center):
            a_coeff = [len(source_coords)]
            for k in range(1, 16):
                res = 0
                for x, y in source_coords:
                    z_i = x + 1j * y
                    res += (z_i - center) ** k
                a_coeff.append(-1 / k * res)

            def evaluate(z):
                res = a_coeff[0] * np.log(z - center)
                for k in range(1, p + 1):
                    res += a_coeff[k] * (z - center) ** -k
                return np.real(res)

            return evaluate

        def get_local(p, center):
            a_coeff = []
            sum = 0
            for x, y in source_coords:
                z_i = x + 1j * y
                sum += np.log(-(z_i - center))
            a_coeff.append(sum)
            for k in range(1, 16):
                res = 0
                for x, y in source_coords:
                    z_i = x + 1j * y
                    res += (z_i - center) ** -k
                a_coeff.append(-1 / k * res)

            def evaluate(z):
                res = np.full_like(z, fill_value=a_coeff[0])
                for k in range(1, p + 1):
                    res += a_coeff[k] * (z - center) ** k
                return np.real(res)

            return evaluate

        def get_heatmap(func):
            raw_values = func(Z)
            raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

            val_min, val_max = raw_values.min(), raw_values.max()
            rgba_image = cmap((raw_values + 5) / 25)
            rgba_image[:, :, 3] = 0.75
            rgb_uint8 = (rgba_image * 255).astype(np.uint8)

            res = ImageMobject(rgb_uint8)
            res.width = plane.x_length
            res.height = plane.y_length
            return res.shift(LEFT * 32 / 9)

        self.add(line, plane, border, title)
        self.wait(0.5)

        def interpolate(f1, f2, t):
            return f1(Z) * (1 - t.get_value()) + f2(Z) * t.get_value()

        quadtree = getGrid(1).set_color(BLUE).shift(LEFT * 32/9).set_z_index(5)
        self.play(FadeIn(quadtree))
        self.wait()

        source_coords = [[0.2, 0.4], [0.4, 0.2], [0.5, 0.8], [0.8, 0.6], [0.9, 0.3]]
        sources = VGroup([Dot(plane.c2p(source_coords[i][0], source_coords[i][1]), color=BLUE) for i in range(5)])
        quadtree[3][31].set_z_index(6)
        self.play(FadeIn(sources), quadtree[3][31].animate.set_color(ORANGE))
        self.wait()

        bad = [9, 10, 28, 29, 30, 32, 33, 53]
        for b in bad:
            quadtree[3][b].set_z_index(4)
        good = []
        MEs = VGroup()
        for i in range(64):
            if i not in bad and i != 31:
                good.append(i)
            MEs.add(Text("ME").scale(0.4).move_to(quadtree[3][i]))

        self.play(AnimationGroup(*[quadtree[3][i].animate.set_color(YELLOW) for i in good], lag_ratio=0.01),
                  AnimationGroup(*[FadeIn(MEs[i]) for i in good], lag_ratio=0.01),)
        self.wait()

        LE = Text("LE").scale(0.5).move_to(quadtree[3][31])
        self.play(AnimationGroup(*[ReplacementTransform(MEs[i].copy(), LE) for i in good], lag_ratio=0.01),)
        self.wait()

        plane_unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]
        new_sources = sources.copy().shift(RIGHT * plane_unit)

        old = [24, 27, 36]
        new = [9, 10, 53]
        for i in new:
            good.append(i)
        for i in old:
            good.remove(i)
        new_quadtree = getGrid(1).set_color(BLUE).shift(LEFT * 32/9).set_z_index(5)
        for i in range(64):
            if i in good:
                new_quadtree[3][i].set_color(YELLOW).set_z_index(6)
            elif i == 30:
                new_quadtree[3][i].set_color(ORANGE).set_z_index(6)
            else:
                new_quadtree[3][i].set_z_index(4)
        for i in range(64):
            quadtree[3][i].set_z_index(5)
            if i in good or i == 30:
                quadtree[3][i].set_z_index(10)

        self.play(Transform(quadtree, new_quadtree), FadeOut(LE), FadeOut(sources), FadeIn(new_sources),
                  AnimationGroup(*[FadeOut(MEs[i]) for i in old]), AnimationGroup(*[FadeIn(MEs[i]) for i in new]),
                  )

        self.wait()

        LE = Text("LE").scale(0.5).move_to(quadtree[3][30])
        self.play(AnimationGroup(*[ReplacementTransform(MEs[i].copy(), LE) for i in good], lag_ratio=0.01), )
        self.wait()

        sources = sources.shift(RIGHT * plane_unit * 2)
        old = [25, 26, 37]
        new = [28, 31, 32]
        for i in new:
            good.append(i)
        for i in old:
            good.remove(i)

        n_quadtree = getGrid(1).set_color(BLUE).shift(LEFT * 32 / 9).set_z_index(5)
        for i in range(64):
            if i in good:
                n_quadtree[3][i].set_color(YELLOW).set_z_index(6)
            elif i == 27:
                n_quadtree[3][i].set_color(ORANGE).set_z_index(6)
            else:
                n_quadtree[3][i].set_z_index(4)
        for i in range(64):
            quadtree[3][i].set_z_index(5)
            if i in good or i == 27:
                quadtree[3][i].set_z_index(10)

        self.play(Transform(quadtree, n_quadtree), FadeOut(LE), FadeOut(new_sources), FadeIn(sources),
                  AnimationGroup(*[FadeOut(MEs[i]) for i in old]), AnimationGroup(*[FadeIn(MEs[i]) for i in new]),
                  )
        self.wait()

        LE = Text("LE").scale(0.5).move_to(quadtree[3][27])
        self.play(AnimationGroup(*[ReplacementTransform(MEs[i].copy(), LE) for i in good], lag_ratio=0.01), )
        self.wait()

        new_quadtree = getGrid(2).shift(LEFT * 32/9).set_z_index(5).set_color(BLUE)
        new_quadtree[3][3].set_color(ORANGE).set_z_index(10)
        self.play(AnimationGroup(*[FadeOut(MEs[i]) for i in good]), FadeOut(LE), FadeTransform(quadtree, new_quadtree))
        self.wait()

        universe = VGroup(plane, border, new_quadtree, sources)
        self.play(universe.animate.scale(3).shift(6.75 * LEFT + 6.75 * UP))
        self.wait()

        lower_level = subdivide(new_quadtree[2][6]).set_z_index(2)
        lower_rad = plane.c2p(np.sqrt(2) / 2, 0)[0] - plane.c2p(0, 0)[0]
        circles = VGroup([DashedVMobject(Circle(radius=lower_rad, color=WHITE), num_dashes=25).move_to(lower_level[i]) for i in range(4)])
        self.play(FadeIn(lower_level), FadeIn(circles))
        self.wait()
        higher_circle = DashedVMobject(Circle(radius=lower_rad * 2, color=WHITE), num_dashes=25).move_to(lower_level).set_z_index(8)
        self.play(AnimationGroup(*[ReplacementTransform(circles[i], higher_circle) for i in range(4)]))
        self.wait()

        for i in range(5):
            source_coords[i][0] += 2
            source_coords[i][1] -= 3
        source_coords.append([2.6, -2.5])
        source_coords.append([2.3, -2.1])
        source_coords.append([2.7, -2.9])

        sources = VGroup([Dot(plane.c2p(source_coords[i][0], source_coords[i][1]), color=BLUE) for i in range(8)]).set_z_index(6)
        heatmap = get_heatmap(get_multipole(10, 2.5 - 2.5j)).scale(3).shift(6.75 * LEFT + 6.75 * UP)

        conv_circle = VGroup(
            Circle(radius=lower_rad, stroke_opacity=0, fill_opacity=0.3, fill_color=BLACK).move_to(lower_level[0]),
            DashedVMobject(Circle(radius=lower_rad, color=WHITE).move_to(lower_level[0]), num_dashes=25)).set_z_index(8)

        z_0_circle = Circle(color=GREEN, radius=DEFAULT_DOT_RADIUS * 2,
                            fill_color=GREEN, fill_opacity=0.5).move_to(lower_level[0]).set_z_index(10)
        z_0_label = MathTex("z_0").scale(0.6).move_to(z_0_circle).set_z_index(12)

        self.play(Write(sources), FadeIn(heatmap), FadeIn(conv_circle), Write(z_0_label), FadeIn(z_0_circle),)
        self.wait()

        working = VGroup(MathTex("P_{z_0}(z) = a_0\log(z - z_0) + ", "\sum_{k = 1}^\infty a_k (z - z_0)^{-k}"),
                         MathTex(r"P_{z_0}(z) = a_0\log\left(z\left(1 - \frac{z_0}{z}\right)\right) + ",
                                 r"\sum_{k = 1}^\infty a_k z^{-k}\left(1 - \frac{z_0}{z}\right)^{-k}"),
                         MathTex(r"=a_0\log(z) +", r"a_0\log\left(1 - \frac{z_0}{z}\right) ", r"+\sum_{k = 1}^\infty a_k z^{-k}",
                                 r"\sum_{l = 0}^\infty \binom{k + l - 1}{l} \left(\frac{z_0}{z}\right)^l"),
                         MathTex(r"=a_0\log(z) +", r"\sum_{k = 1}^\infty -\frac{a_0}{k} \left(\frac{z_0}{z}\right)^k",
                                 r"+ \sum_{k = 1}^\infty a_k z^{-k}", r"\sum_{l = 0}^\infty \binom{k + l - 1}{l} \left(\frac{z_0}{z}\right)^l"),
                         MathTex(r"=a_0\log(z) +", r"\sum_{k = 1}^\infty -\frac{a_0}{k} z_0^k z^{-k}",
                                 r"+ \sum_{k = 1}^\infty a_k z^{-k}", r"\sum_{l = 0}^\infty \binom{k + l - 1}{l}  z_0^l z^{-l}"),
                         MathTex(r"=a_0\log(z) +", r"\sum_{k = 1}^\infty -\frac{a_0}{k} z_0^k z^{-k}",
                                 r"+ \sum_{k = 1}^\infty \sum_{l = 0}^\infty", r"a_k \binom{k + l - 1}{l}  z_0^l z^{-(k + l)}"),
                         MathTex(r"=a_0\log(z) +", r"\sum_{k = 1}^\infty -\frac{a_0}{k} z_0^k z^{-k}",
                                 r"+ \sum_{k = 1}^\infty \sum_{r = k}^\infty", r"a_k \binom{r - 1}{r - k}  z_0^{r - k} z^{-r}"),
                         MathTex(r"=a_0\log(z) +", r"\sum_{r = 1}^\infty -\frac{a_0}{r} z_0^r z^{-r}",
                                 r"+ \sum_{r = 1}^\infty \sum_{k = 1}^r", r"a_k \binom{r - 1}{k - 1} z_0^{r - k} z^{-r}"),
                         MathTex(r"=a_0\log(z) +",
                                 r"\sum_{r = 1}^\infty \left(\sum_{k = 1}^r a_k \binom{r - 1}{k - 1} z_0^{r - k} -\frac{a_0}{r} z_0^r\right)z^{-r}"),
                         MathTex(r"P(z) = a_0\log(z) +","\sum_{r = 1}^\infty a'_r z^{-r}")
                         ).scale(0.55).shift(RIGHT * 32/9 + UP * 2)

        for i in range(2):
            working[i][0][1:3].set_color(GREEN)
            working[i][0][4].set_color(BLUE)
        working[0][0][7:9].set_color(YELLOW)
        working[0][0][13].set_color(BLUE)
        working[0][0][15:17].set_color(GREEN)
        working[0][1][5:7].set_color(YELLOW)
        working[0][1][8].set_color(BLUE)
        working[0][1][10:12].set_color(GREEN)

        self.play(Write(working[0]))
        self.wait()

        z_0_arrow = Arrow(plane.c2p(3, -3), plane.c2p(2.5, -2.5), buff=0,
                          stroke_width=4, max_tip_length_to_length_ratio=0.1).set_z_index(3)
        z_arrow = Arrow(plane.c2p(3, -3), plane.c2p(3.6, -1.6), buff=0,
                        stroke_width=4, max_tip_length_to_length_ratio=0.1).set_z_index(3)
        z_label = MathTex("z").scale(0.75).move_to(plane.c2p(3.62, -1.5))

        self.play(GrowArrow(z_0_arrow), GrowArrow(z_arrow), Write(z_label))
        self.wait()

        working[1][0][7:9].set_color(YELLOW)
        working[1][0][13].set_color(BLUE)
        working[1][0][17:19].set_color(GREEN)
        working[1][0][20].set_color(BLUE)
        working[1][1][5:7].set_color(YELLOW)
        working[1][1][13:15].set_color(GREEN)
        working[1][1][16].set_color(BLUE)

        self.play(ReplacementTransform(working[0][0][:13], working[1][0][:13]), FadeIn(working[1][0][14]),
                  ReplacementTransform(working[0][0][13].copy(), working[1][0][13]),
                  ReplacementTransform(working[0][0][13:15], working[1][0][15:17]),
                  ReplacementTransform(working[0][0][15:17], working[1][0][17:21]), FadeIn(working[1][0][21]),
                  ReplacementTransform(working[0][0][17:], working[1][0][22:]),
                  ReplacementTransform(working[0][1][:7], working[1][1][:7]),
                  ReplacementTransform(working[0][1][8].copy(), working[1][1][7]),
                  ReplacementTransform(working[0][1][13:], working[1][1][8:10]),
                  ReplacementTransform(working[0][1][7], working[1][1][10]),
                  ReplacementTransform(working[0][1][8:10], working[1][1][11:13]),
                  ReplacementTransform(working[0][1][10:12], working[1][1][13:17]),
                  ReplacementTransform(working[0][1][12], working[1][1][17]),
                  ReplacementTransform(working[0][1][13:].copy(), working[1][1][18:]),
                  )
        self.wait()

        for i in range(2, 9):
            working[i][0][1:3].set_color(YELLOW)
            working[i][0][7].set_color(BLUE)
        working[2][1][:2].set_color(YELLOW)
        working[2][1][8:10].set_color(GREEN)
        working[2][1][11].set_color(BLUE)
        for i in range(2, 5):
            working[i][2][6:8].set_color(YELLOW)
            working[i][2][8].set_color(BLUE)
        for i in range(2, 4):
            working[i][3][14:16].set_color(GREEN)
            working[i][3][17].set_color(BLUE)

        working[2][:2].next_to(working[1], DOWN).align_to(working[1][0][6], LEFT)
        working[2][2:].next_to(working[2][0], DOWN).align_to(working[1], RIGHT).shift(DOWN * 0.2)
        self.play(Write(working[2][0][0]),
                  ReplacementTransform(working[1][0][7:14].copy(), working[2][0][1:8]),
                  ReplacementTransform(working[1][0][-2].copy(), working[2][0][8]), Write(working[2][0][9]),
                  ReplacementTransform(working[1][0][7:12].copy(), working[2][1][:5]),
                  ReplacementTransform(working[1][0][14:-2].copy(), working[2][1][5:]),
                  ReplacementTransform(working[1][0][-1].copy(), working[2][2][0]),
                  ReplacementTransform(working[1][1][:10].copy(), working[2][2][1:]),
                  Write(working[2][3][:13]),
                  ReplacementTransform(working[1][1][10].copy(), working[2][3][13]),
                  ReplacementTransform(working[1][1][13:18].copy(), working[2][3][14:19]), Write(working[2][3][19])
                  )
        self.wait()

        working[3][1][6:8].set_color(YELLOW)
        working[3][1][11:13].set_color(GREEN)
        working[3][1][14].set_color(BLUE)

        working[3][:2].set_y(working[2][:2].get_y()).align_to(working[2][0], LEFT)
        working[3][2:].set_y(working[2][2:].get_y()).align_to(working[2][3], RIGHT)
        self.play(ReplacementTransform(working[2][0], working[3][0]),
                  ReplacementTransform(working[2][1][2:5], working[3][1][:5]),
                  FadeIn(working[3][1][5]), FadeIn(working[3][1][8:10]), FadeOut(working[2][1][6:8]),
                  ReplacementTransform(working[2][1][:2], working[3][1][6:8]),
                  ReplacementTransform(working[2][1][5], working[3][1][10]),
                  ReplacementTransform(working[2][1][8:13], working[3][1][11:16]), FadeIn(working[3][1][16]),
                  ReplacementTransform(working[2][2:], working[3][2:]),
                  )
        self.wait()

        for i in range(4, 8):
            working[i][1][6:8].set_color(YELLOW)
            working[i][1][10].set_color(GREEN)
            working[i][1][12].set_color(GREEN)
            working[i][1][13].set_color(BLUE)
        working[4][2][6:8].set_color(YELLOW)
        working[4][2][8].set_color(BLUE)
        working[4][3][13].set_color(GREEN)
        working[4][3][15].set_color(GREEN)
        working[4][3][16].set_color(BLUE)

        working[4][:2].set_y(working[3][:2].get_y()).align_to(working[3][0], LEFT)
        working[4][2:].set_y(working[3][2:].get_y()).align_to(working[3][3], RIGHT)

        self.play(ReplacementTransform(working[3][0], working[4][0]),
                  ReplacementTransform(working[3][1][:10], working[4][1][:10]),
                  FadeOut(working[3][1][10]), FadeOut(working[3][1][15]),
                  ReplacementTransform(working[3][1][11], working[4][1][10]),
                  ReplacementTransform(working[3][1][12], working[4][1][12]), FadeOut(working[3][1][13]),
                  ReplacementTransform(working[3][1][14], working[4][1][13]),
                  ReplacementTransform(working[3][1][16], working[4][1][11]),
                  ReplacementTransform(working[3][1][16].copy(), working[4][1][15]), FadeIn(working[4][1][14]),
                  ReplacementTransform(working[3][2], working[4][2]),
                  ReplacementTransform(working[3][3][:13], working[4][3][:13]),
                  FadeOut(working[3][3][13]), FadeOut(working[3][3][16]), FadeOut(working[3][3][18]),
                  ReplacementTransform(working[3][3][14], working[4][3][13]),
                  ReplacementTransform(working[3][3][15], working[4][3][15]),
                  ReplacementTransform(working[3][3][17], working[4][3][16]),
                  ReplacementTransform(working[3][3][19], working[4][3][14]),
                  ReplacementTransform(working[3][3][19].copy(), working[4][3][18]), FadeIn(working[4][3][17]),
                  )
        self.wait()

        working[5][3][:2].set_color(YELLOW)
        working[5][3][10].set_color(GREEN)
        working[5][3][12].set_color(GREEN)
        working[5][3][13].set_color(BLUE)

        working[5][:2].set_y(working[4][:2].get_y()).align_to(working[4][0], LEFT)
        working[5][2:].set_y(working[4][2:].get_y()).align_to(working[4][3], RIGHT)
        self.play(ReplacementTransform(working[4][:2], working[5][:2]),
                  ReplacementTransform(working[4][2][:6], working[5][2][:6]),
                  ReplacementTransform(working[4][3][:5], working[5][2][6:]),
                  ReplacementTransform(working[4][2][6:8], working[5][3][:2]),
                  ReplacementTransform(working[4][3][5:-3], working[5][3][2 :-7]),
                  FadeIn(working[5][3][-5]), FadeIn(working[5][3][-1]), FadeIn(working[5][3][-3]),
                  ReplacementTransform(working[4][2][-3:-1], working[5][3][-7:-5]),
                  ReplacementTransform(working[4][3][-3:-1], working[5][3][-7:-5]),
                  ReplacementTransform(working[4][2][-1], working[5][3][-4]),
                  ReplacementTransform(working[4][3][-1], working[5][3][-2]),
                  )
        self.wait()

        r_text = MathTex(r"\text{Let } r = k + l").scale(0.6).shift(RIGHT * 32/9 + DOWN * 3)
        self.play(Write(r_text))
        self.wait()

        for i in range (6, 8):
            working[i][3][:2].set_color(YELLOW)
            working[i][3][10].set_color(GREEN)
            working[i][3][14].set_color(GREEN)
            working[i][3][15].set_color(BLUE)

        working[6][:2].set_y(working[5][:2].get_y()).align_to(working[5][0], LEFT)
        working[6][2:].set_y(working[5][2:].get_y()).align_to(working[5][2], LEFT)
        self.play(ReplacementTransform(working[5][:2], working[6][:2]),
                  ReplacementTransform(working[5][2][:5], working[6][2][:5]),
                  ReplacementTransform(working[5][2][5:], working[6][2][5:]),
                  ReplacementTransform(working[5][3][:2], working[6][3][:2]),
                  ReplacementTransform(working[5][3][2], working[6][3][2]),
                  ReplacementTransform(working[5][3][3:6], working[6][3][3]),
                  ReplacementTransform(working[5][3][6:8], working[6][3][4:6]),
                  ReplacementTransform(working[5][3][8], working[6][3][6:9]),
                  ReplacementTransform(working[5][3][9], working[6][3][9]),
                  ReplacementTransform(working[5][3][10], working[6][3][10]),
                  ReplacementTransform(working[5][3][11], working[6][3][11:14]),
                  ReplacementTransform(working[5][3][12], working[6][3][14]),
                  ReplacementTransform(working[5][3][13:15], working[6][3][15:17]),
                  ReplacementTransform(working[5][3][15:], working[6][3][17]),
                  )
        self.wait()

        working[7][1][6:8].set_color(YELLOW)
        working[7][1][10].set_color(GREEN)
        working[7][1][12].set_color(GREEN)
        working[7][1][13].set_color(BLUE)

        working[7][:2].next_to(working[6][2:], DOWN).align_to(working[6][0], LEFT)
        working[7][2:].next_to(working[7][:2], DOWN).align_to(working[6][3], RIGHT)
        self.play(ReplacementTransform(working[6][:2].copy(), working[7][:2]),
                  ReplacementTransform(working[6][2][0].copy(), working[7][2][0]),
                  ReplacementTransform(working[6][2][1:6].copy(), working[7][2][6:11]),
                  ReplacementTransform(working[6][2][6:11].copy(), working[7][2][1:6]),
                  ReplacementTransform(working[6][3].copy(), working[7][3]),
                  )
        self.wait()

        working[8][1][11:13].set_color(YELLOW)
        working[8][1][21].set_color(GREEN)
        working[8][1][25].set_color(GREEN)
        working[8][1][27:29].set_color(YELLOW)
        working[8][1][31].set_color(GREEN)
        working[8][1][33].set_color(GREEN)
        working[8][1][35].set_color(BLUE)

        working[8][0].set_y(working[7][:2].get_y()).align_to(working[7][0], LEFT)
        working[8][1].set_y(working[7][2:].get_y()).align_to(working[7][3], RIGHT).shift(UP * 0.2)
        self.play(ReplacementTransform(working[7][0], working[8][0]),
                  ReplacementTransform(working[7][2][1:6], working[8][1][:5]), FadeIn(working[8][1][5]),
                  ReplacementTransform(working[7][2][6:11], working[8][1][6:11]),
                  ReplacementTransform(working[7][3][:-3], working[8][1][11:26]),
                  ReplacementTransform(working[7][1][:5], working[8][1][:5]),
                  ReplacementTransform(working[7][1][5:13], working[8][1][26:34]), FadeIn(working[8][1][34]),
                  ReplacementTransform(working[7][1][-3:], working[8][1][-3:]),
                  ReplacementTransform(working[7][3][-3:], working[8][1][-3:]),
                  FadeOut(working[7][2][0]),
                  )
        self.wait()

        # MathTex(r"P(z) = a_0\log(z) +","\sum_{r = 1}^\infty a'_r z^{-r}")
        working[9][0][2].set_color(BLUE)
        working[9][0][5:7].set_color(YELLOW)
        working[9][0][11].set_color(BLUE)
        working[9][1][5:8].set_color(YELLOW)
        working[9][1][8].set_color(BLUE)
        working[9].set_y(working[2][:2].get_y()).set_x(32/9)

        coefficients = MathTex(r"a'_r = \sum_{k = 1}^r a_k \binom{r - 1}{k - 1} z_0^{r - k} -\frac{a_0}{r} z_0^r")
        coefficients.scale(0.55).shift(RIGHT * 32/9 + DOWN * 0.3)

        coefficients[0][9:11].set_color(YELLOW)
        coefficients[0][19].set_color(GREEN)
        coefficients[0][23].set_color(GREEN)
        coefficients[0][25:27].set_color(YELLOW)
        coefficients[0][29].set_color(GREEN)
        coefficients[0][31].set_color(GREEN)

        original = MathTex("P_{z_0}(z) = a_0\log(z - z_0) + ", "\sum_{k = 1}^\infty a_k (z - z_0)^{-k}").scale(0.55).move_to(working[0])
        original[0][1:3].set_color(GREEN)
        original[0][4].set_color(BLUE)
        original[0][7:9].set_color(YELLOW)
        original[0][13].set_color(BLUE)
        original[0][15:17].set_color(GREEN)
        original[1][5:7].set_color(YELLOW)
        original[1][8].set_color(BLUE)
        original[1][10:12].set_color(GREEN)

        self.play(FadeOut(VGroup(working[1], working[6])), FadeIn(original, shift=DOWN),
                  ReplacementTransform(working[8][0], working[9][0][4:]), Write(working[9][0][:4]),
                  ReplacementTransform(working[8][1][:5], working[9][1][:5]),
                  ReplacementTransform(working[8][1][5:-3], working[9][1][5:-3]),
                  ReplacementTransform(working[8][1][-3:], working[9][1][-3:]),
                  ReplacementTransform(working[8][1][5:-4].copy(), coefficients[0][4:]), Write(coefficients[0][:4]),
                  )
        self.wait()

        brace = Brace(coefficients[0][4:12]).shift(UP * 0.1)
        self.play(Write(brace))
        self.wait()

        tracker = ValueTracker(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(get_multipole(10, 2.5 + 0.5 * tracker.get_value() - 2.5j - 0.5j * tracker.get_value())
                        ).scale(3).shift(6.75 * LEFT + 6.75 * UP)
        ))
        original_conv = conv_circle[1].copy()
        self.add(original_conv)
        self.play(tracker.animate.set_value(1), lower_level.animate.set_opacity(0),
                  conv_circle.animate.scale(2).move_to(plane.c2p(3, -3)))
        self.remove(lower_level)
        self.remove(higher_circle)
        self.wait()

        universe = VGroup(plane, border, new_quadtree, sources, conv_circle,
                          original_conv, z_arrow, z_label, z_0_arrow, z_0_circle, z_0_label)
        heatmap.clear_updaters()
        temp = universe.copy().scale(1/3)
        temp[5:].set_opacity(0)
        temp.shift(LEFT * 32/9 - temp[0].get_center())
        self.play(Transform(universe, temp), heatmap.animate.move_to(LEFT * 32/9).scale(1/3))
        self.wait()

        plate = Rectangle(width=plane_size, height=plane_size, fill_opacity=1).move_to(LEFT * 32/9)
        local_conv = VGroup(
            Difference(plate, Circle(radius=lower_rad * 2 / 3).move_to(plane.c2p(3, 1)),
                       fill_color=BLACK, fill_opacity=0.3, stroke_width=0).set_z_index(3),
            DashedVMobject(Circle(radius=lower_rad * 2 / 3, color=WHITE).move_to(plane.c2p(3, 1)),
                           dashed_ratio=0.5, num_dashes=25).set_z_index(15))
        flip_text = Text("FLIP").move_to(plane.c2p(3, -1.5)).scale(0.75).set_z_index(20)
        self.play(Transform(heatmap, get_heatmap(get_local(10, 3 + 1j))),
                  ReplacementTransform(conv_circle, local_conv),
                  FadeIn(flip_text, shift=UP),
                  FadeOut(working[9]), FadeOut(original), FadeOut(coefficients), FadeOut(r_text), FadeOut(brace)
                  )
        self.wait()

        lower_conv = DashedVMobject(Circle(radius=lower_rad / 3, color=WHITE).move_to(plane.c2p(2.5, 0.5)),
                           dashed_ratio=0.5, num_dashes=25)
        self.play(ReplacementTransform(local_conv[1].copy(), lower_conv), FadeOut(flip_text))
        self.wait()

        universe = VGroup(plane, border, new_quadtree, sources, local_conv, lower_conv)
        temp = universe.copy().scale(3)
        temp.shift(LEFT * 32/9 - temp[0].c2p(3, 1))
        new_title = Text("Local Shift").to_edge(UP).shift(RIGHT * 32 / 9)
        self.play(Transform(universe, temp),
                  heatmap.animate.scale(3).shift(DOWN * 2.25 + LEFT * 6.75), Transform(title, new_title))
        self.wait()

        z_0_label = MathTex("z_0").scale(0.6).move_to(plane.c2p(3.1, 1.1)).set_z_index(12).set_color(GREEN)
        z_0_arrow = Arrow(plane.c2p(2.5, 0.5), plane.c2p(3, 1), buff=0, max_tip_length_to_length_ratio=0.1)
        z_label = MathTex("z").scale(0.6).move_to(plane.c2p(2.15, 0.85)).set_z_index(12).set_color(BLUE)
        z_arrow = Arrow(plane.c2p(2.5, 0.5), plane.c2p(2.2, 0.8), buff=0)
        self.play(GrowArrow(z_arrow), GrowArrow(z_0_arrow), FadeIn(z_0_label), FadeIn(z_label))
        self.wait()

        working = VGroup(MathTex("P_{z_0}(z) = \sum_{k = 0}^\infty b_k(z - z_0)^k"),
                         MathTex("= \sum_{k = 0}^\infty b_k", r"\sum_{l = 0}^k \binom{k}{l} z^l (-z_0)^{k - l}"),
                         MathTex("P(z) = \sum_{l = 0}^\infty", r"\left(\sum_{k = l}^\infty b_k \binom{k}{l} (-z_0)^{k - l}\right) z^l"),
                         ).arrange(DOWN).scale(0.65).shift(RIGHT * 32/9 + UP)
        working[0][0][1:3].set_color(GREEN)
        working[0][0][4].set_color(BLUE)
        working[0][0][12:14].set_color(YELLOW)
        working[0][0][15].set_color(BLUE)
        working[0][0][17:19].set_color(GREEN)
        working[1][0][6:8].set_color(YELLOW)
        working[1][1][9].set_color(BLUE)
        working[1][1][13:15].set_color(GREEN)
        working[2][0][2].set_color(BLUE)
        working[2][1][6:8].set_color(YELLOW)
        working[2][1][14:16].set_color(GREEN)
        working[2][1][21].set_color(BLUE)

        self.play(Write(working[0]))
        self.wait()
        self.play(ReplacementTransform(working[0][0][6:14].copy(), working[1][0]), Write(working[1][1][:9]),
                  ReplacementTransform(working[0][0][15].copy(), working[1][1][9]), Write(working[1][1][10]),
                  ReplacementTransform(working[0][0][14].copy(), working[1][1][11]),
                  ReplacementTransform(working[0][0][16:20].copy(), working[1][1][12:16]),
                  ReplacementTransform(working[0][0][20].copy(), working[1][1][16]), Write(working[1][1][17:])
                  )
        self.wait()
        self.play(Write(working[2][0][:5]), ReplacementTransform(working[1][1][:5].copy(), working[2][0][5:10]),
                  FadeIn(working[2][1][0]), ReplacementTransform(working[1][0][1:8].copy(), working[2][1][1:8]),
                  ReplacementTransform(working[1][1][5:9].copy(), working[2][1][8:12]),
                  ReplacementTransform(working[1][1][9:11].copy(), working[2][1][-2:]),
                  ReplacementTransform(working[1][1][11:19].copy(), working[2][1][12:20]), FadeIn(working[2][1][20])
                  )
        self.wait()

        tracker.set_value(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(get_local(10, 3 - 0.5 * tracker.get_value() + 1j - 0.5j * tracker.get_value())
                        ).scale(3).shift(6.75 * LEFT + 2.25 * DOWN)
        ))
        plate = Rectangle(width=plane_size * 3, height=plane_size * 3, fill_opacity=1).move_to(plane.c2p(0, 0))
        new_conv = Difference(plate, Circle(radius=lower_rad).move_to(plane.c2p(2.5, 0.5)),
                       fill_color=BLACK, fill_opacity=0.3, stroke_width=0)
        self.play(FadeTransform(local_conv[0], new_conv), tracker.animate.set_value(1),
                  ReplacementTransform(local_conv[1], lower_conv)
                  )
        self.wait()
        heatmap.clear_updaters()
        self.play(Unwrite(title), Unwrite(working), Unwrite(VGroup(plane, border, new_quadtree, sources, lower_conv)),
                  Unwrite(line), FadeOut(heatmap), FadeOut(new_conv),
                  Unwrite(VGroup(z_arrow, z_0_arrow, z_0_label, z_label)))
        self.wait()



class Efficiency(Scene):
    def construct(self):
        cmap = plt.get_cmap("plasma")

        line = Line(UP * 4, DOWN * 4).set_z_index(10)

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 3000
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.2},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        title = Text("Multipole Shift").to_edge(UP).shift(RIGHT * 32 / 9)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        def f(z):
            ans = np.zeros_like(z)
            for i in range(len(source_coords)):
                ans += np.real(np.log(z - (source_coords[i][0] + 1j * source_coords[i][1])))
            return np.real(ans)

        def get_multipole(p, center):
            a_coeff = [len(source_coords)]
            for k in range(1, 16):
                res = 0
                for x, y in source_coords:
                    z_i = x + 1j * y
                    res += (z_i - center) ** k
                a_coeff.append(-1 / k * res)

            def evaluate(z):
                res = a_coeff[0] * np.log(z - center)
                for k in range(1, p + 1):
                    res += a_coeff[k] * (z - center) ** -k
                return np.real(res)

            return evaluate

        def get_local(p, center):
            a_coeff = []
            sum = 0
            for x, y in source_coords:
                z_i = x + 1j * y
                sum += np.log(-(z_i - center))
            a_coeff.append(sum)
            for k in range(1, 16):
                res = 0
                for x, y in source_coords:
                    z_i = x + 1j * y
                    res += (z_i - center) ** -k
                a_coeff.append(-1 / k * res)

            def evaluate(z):
                res = np.full_like(z, fill_value=a_coeff[0])
                for k in range(1, p + 1):
                    res += a_coeff[k] * (z - center) ** k
                return np.real(res)

            return evaluate

        def get_heatmap(func):
            raw_values = func(Z)
            raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

            val_min, val_max = raw_values.min(), raw_values.max()
            rgba_image = cmap((raw_values + 5) / 25)
            rgba_image[:, :, 3] = 0.75
            rgb_uint8 = (rgba_image * 255).astype(np.uint8)

            res = ImageMobject(rgb_uint8)
            res.width = plane.x_length
            res.height = plane.y_length
            return res.shift(LEFT * 32 / 9)

        self.add(line, plane, border, title)

        new_quadtree = getGrid(2).shift(LEFT * 32/9).set_z_index(5).set_color(BLUE)
        new_quadtree[3][3].set_color(ORANGE).set_z_index(10)
        self.add(new_quadtree)
        self.wait(0.5)



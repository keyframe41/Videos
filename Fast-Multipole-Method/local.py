from manim import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

    layers.add(Rectangle(height=6, width=6, color=yorange, stroke_width=3))

    def subdivide(rect):
        d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
        len = rect.width
        center = rect.get_center()
        return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3).move_to(
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
        yorange = (YELLOW + ORANGE) / 2
        cmap = plt.get_cmap("plasma")

        line = Line(UP * 4, DOWN * 4).set_z_index(10)

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 200
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        target_coords = [[1, -1.2], [1.1, -1], [1.3, -0.8], [1.4, -1.3], [1.5, -1.6], [1.7, -1.4]]
        source_coords = [[-2.5, 1.3], [-2.7, 0.8], [-2.9, 1.4], [-3, 1.1], [-3.1, 1.5], [-3.2, 0.9], [-3.3, 1.2],
                         [-3.5, 1]]

        def f(z):
            ans = np.zeros_like(z)
            for i in range(len(source_coords)):
                ans += np.real(np.log(z - (source_coords[i][0] + 1j * source_coords[i][1])))
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

        self.add(line, plane, border)
        self.wait(0.5)

        def interpolate(f1, f2, t):
            return f1(Z) * (1 - t.get_value()) + f2(Z) * t.get_value()

        def get_truncated(p, center):
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


        quadtree = getGrid().shift(LEFT * 32/9).set_color(BLUE)
        sourcebox_ids = [0, 1, 3, 4, 5]

        for i in sourcebox_ids:
            quadtree[2][i].set_z_index(6)
        quadtree[2][8].set_z_index(6)
        title = Text("Local Expansion").to_edge(UP).shift(RIGHT * 32 / 9)
        self.play(Create(quadtree), run_time=1.5)
        self.play(quadtree[2][8].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(AnimationGroup(*[quadtree[2][i].animate.set_color(ORANGE) for i in sourcebox_ids], lag_ratio=0.1))
        self.wait()

        def get_wave(rad):
            r = rad.get_value()
            circ_rad = 0.03
            res = VGroup()
            for i in range(25):
                if r - 0.03 * i > 0:
                    res.add(Circle(radius=r - circ_rad * i, color=ManimColor(cmap(1 - i / 24)), stroke_width=8).set_stroke(
                        opacity = 0.4 if r - circ_rad * i < 3 else 0.4 - (r - circ_rad * i - 3) * 0.4
                    ))
            return res
        radii = [ValueTracker(0) for i in range(5)]
        ripples = always_redraw(lambda: VGroup([get_wave(radii[i]).move_to(quadtree[2][sourcebox_ids[i]]) for i in range(5)]))
        self.add(ripples)
        hex_colors = [mcolors.to_hex(cmap(val)) for val in np.linspace(0, 1, 20)]
        quadtree[2][8].set_sheen_direction(UL)
        for j in range(2):
            self.play(AnimationGroup(*[radii[i].animate.set_value(4.6) for i in range(5)], lag_ratio=0.05), run_time=4)
            for i in range(5):
                radii[i].set_value(0)
        self.play(AnimationGroup(*[radii[i].animate.set_value(4.6) for i in range(5)] +
                                  [quadtree[2][8].animate.set_fill(hex_colors, opacity=1)], lag_ratio=0.05), run_time=5)
        self.wait()

        boxes = VGroup(quadtree[2][3].copy(), quadtree[2][8].copy())
        self.add(boxes)

        temp = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        self.play(FadeOut(quadtree), Write(title), boxes[1].animate.set_fill(opacity=0), Transform(plane, temp))

        target_dots = VGroup([Dot(plane.c2p(target_coords[i][0], target_coords[i][1]), color=BLUE) for i in range(6)]).set_z_index(8)
        source_dots = VGroup([Dot(plane.c2p(source_coords[i][0], source_coords[i][1]), color=GREEN) for i in range(8)]).set_z_index(8)
        self.play(AnimationGroup(*[Write(target_dots[i]) for i in range(6)], lag_ratio=0.05),
                  AnimationGroup(*[Write(source_dots[i]) for i in range(8)], lag_ratio=0.05),)

        self.wait()
        target_label = MathTex("z").scale(0.6).next_to(target_dots[0], DOWN).shift(UP * 0.1).set_z_index(10)
        source_label = MathTex("z_i").scale(0.6).next_to(source_dots[0], UP).shift(DOWN * 0.1).set_z_index(10)
        self.play(Write(target_label), Write(source_label),
                  AnimationGroup(*[target_dots[i].animate.set_opacity(0.25) for i in range(1, 6)]),
                  AnimationGroup(*[source_dots[i].animate.set_opacity(0.25) for i in range(1, 8)]),)
        self.wait()

        heatmap = get_heatmap(f)
        self.play(FadeIn(heatmap))

        working = VGroup(MathTex("\sum_{i = 1}^n", "m_i \log(z - z_i)"),
                         MathTex("\sum_{i = 1}^n", r"m_i\log\left(-z_i\left(1 - \frac{z}{z_i}\right)\right)"),
                         MathTex("=\sum_{i = 1}^n m_i\log(-z_i)",
                                 "+\sum_{i = 1}^n", r"m_i\log\left(1 - \frac{z}{z_i}\right)"),
                         MathTex("=\sum_{i = 1}^n m_i\log(-z_i)",
                                 "+\sum_{i = 1}^n", r"m_i\sum_{k = 1}^\infty -\frac{1}{k}", r"\left(\frac{z}{z_i}\right)^k"),
                         MathTex("=\sum_{i = 1}^n m_i\log(-z_i)",
                                 r"+\sum_{k = 1}^\infty", r"\left(-\sum_{i = 1}^n \frac{m_i}{kz_i^k}\right)z^k"),
                         MathTex("P_p(z) = b_0 + \sum_{k = 1}^p b_k z^k")
                         ).scale(0.7).shift(RIGHT * 32 / 9).next_to(title, DOWN)
        working[0][1][:2].set_color(YELLOW)
        working[0][1][6].set_color(BLUE)
        working[0][1][8:10].set_color(GREEN)

        working[1][1][:2].set_color(YELLOW)
        working[1][1][7:9].set_color(GREEN)
        working[1][1][12].set_color(BLUE)
        working[1][1][14:16].set_color(GREEN)

        for i in [2, 3, 4]:
            working[i][0][6:8].set_color(YELLOW)
            working[i][0][13:15].set_color(GREEN)
        working[2][2][:2].set_color(YELLOW)
        working[2][2][8].set_color(BLUE)
        working[2][2][10:12].set_color(GREEN)

        working[3][2][:2].set_color(YELLOW)
        working[3][3][1].set_color(BLUE)
        working[3][3][3:5].set_color(GREEN)

        working[4][2][7:9].set_color(YELLOW)
        working[4][2][11].set_color(GREEN)
        working[4][2][13].set_color(GREEN)
        working[4][2][15].set_color(BLUE)

        working[5][0][3].set_color(BLUE)
        working[5][0][6:8].set_color(YELLOW)
        working[5][0][14:16].set_color(YELLOW)
        working[5][0][16].set_color(BLUE)

        self.play(Write(working[0]))
        self.wait()
        plane_unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]

        plate = Rectangle(width=plane_size, height=plane_size, fill_opacity=1).move_to(plane.c2p(0, 0))
        conv_circle = VGroup(
            Difference(plate, Circle(radius=np.sqrt(2) * plane_unit).move_to(plane.c2p(1, -1)),
                       fill_color=BLACK, fill_opacity=0.3, stroke_width=0),
            DashedVMobject(Circle(radius=np.sqrt(2) * plane_unit, color=WHITE).move_to(plane.c2p(1, -1)), dashed_ratio=0.5,
                           num_dashes=40))
        z_i_mag = Arrow(plane.c2p(1, -1), source_dots[0], buff=0)
        self.play(FadeIn(conv_circle), GrowArrow(z_i_mag))
        self.wait()

        self.play(ReplacementTransform(working[0][0], working[1][0]),
                  ReplacementTransform(working[0][1][:5], working[1][1][:5]),
                  ReplacementTransform(working[0][1][5], working[1][1][5]),
                  ReplacementTransform(working[0][1][7:10], working[1][1][6:9]),
                  ReplacementTransform(working[0][1][5].copy(), working[1][1][9]),
                  ReplacementTransform(working[0][1][8:10].copy(), working[1][1][10]),
                  ReplacementTransform(working[0][1][7].copy(), working[1][1][11]),
                  ReplacementTransform(working[0][1][6], working[1][1][12]),
                  Write(working[1][1][13]),
                  ReplacementTransform(working[0][1][8:10].copy(), working[1][1][14:16]),
                  ReplacementTransform(working[0][1][-1], working[1][1][16]),
                  ReplacementTransform(working[0][1][-1].copy(), working[1][1][17]),
                  )
        self.wait()
        working[2].next_to(working[1], DOWN)
        self.play(Write(working[2][0][0]), ReplacementTransform(working[1][0].copy(), working[2][0][1:6]),
                  ReplacementTransform(working[1][1][:9].copy(), working[2][0][6:15]),
                  ReplacementTransform(working[1][1][-1].copy(), working[2][0][15]),
                  Write(working[2][1][0]), ReplacementTransform(working[1][0].copy(), working[2][1][1:]),
                  ReplacementTransform(working[1][1][:5].copy(), working[2][2][:5]),
                  ReplacementTransform(working[1][1][9:-1].copy(), working[2][2][5:]))
        self.wait()
        working[3].shift(UP * (working[2][0][0].get_y() - working[3][0][0].get_y()))
        self.play(ReplacementTransform(working[2][0], working[3][0]),
                  ReplacementTransform(working[2][1], working[3][1]),
                  ReplacementTransform(working[2][2][:2], working[3][2][:2]),
                  ReplacementTransform(working[2][2][2:5], working[3][2][2:]), Unwrite(working[2][2][6:8]),
                  ReplacementTransform(working[2][2][5], working[3][3][0]),
                  ReplacementTransform(working[2][2][8:], working[3][3][1:6]), Write(working[3][3][6])
                  )
        self.wait()

        working[4].shift(UP * (working[2][0][0].get_y() - working[4][0][0].get_y()))

        conv_text = MathTex(r"\text{Converges when }", "|z| < \min_{1\leq i \leq n}|z_i|").shift(RIGHT * 32 / 9 + DOWN * 0.2).scale(0.75)
        conv_text[1][1].set_color(BLUE)
        conv_text[1][-3:-1].set_color(GREEN)
        self.play(Write(conv_text))
        self.wait()

        plate = Rectangle(width=plane_size, height=plane_size, fill_opacity=1).move_to(plane.c2p(0, 0))
        conv_radius = min([np.sqrt((1 - source_coords[i][0]) ** 2 + (-1 - source_coords[i][1]) ** 2) for i in
                           range(len(source_coords))])
        rad = ValueTracker(np.sqrt(2))
        conv_circle.add_updater(lambda m: m.become(
            VGroup(Difference(plate, Circle(radius=rad.get_value() * plane_unit).move_to(plane.c2p(1, -1)),
                              fill_color=BLACK, fill_opacity=0.3, stroke_width=0),
                   DashedVMobject(Circle(radius=rad.get_value() * plane_unit, color=WHITE).move_to(plane.c2p(1, -1)),
                                  dashed_ratio=0.5, num_dashes=40))
        ))
        self.play(rad.animate.set_value(conv_radius))
        conv_circle.clear_updaters()
        self.wait()

        self.play(ReplacementTransform(working[3][0], working[4][0]),
                  ReplacementTransform(working[3][1][0], working[4][1][0]),
                  ReplacementTransform(working[3][1][1:], working[4][2][2:7]),
                  ReplacementTransform(working[3][2][:2], working[4][2][7:9]),
                  ReplacementTransform(working[3][2][2:7], working[4][1][1:]),
                  ReplacementTransform(working[3][2][7], working[4][2][1]), Unwrite(working[3][2][8]),
                  ReplacementTransform(VGroup(working[3][2][9], working[3][3][2]), working[4][2][9]),
                  ReplacementTransform(working[3][2][10], working[4][2][10]),
                  ReplacementTransform(working[3][3][0], working[4][2][0]),
                  ReplacementTransform(working[3][3][1], working[4][2][-2]),
                  ReplacementTransform(working[3][3][3], working[4][2][11]),
                  ReplacementTransform(working[3][3][4], working[4][2][13]),
                  ReplacementTransform(working[3][3][5], working[4][2][-3]),
                  ReplacementTransform(working[3][3][6], working[4][2][12]),
                  ReplacementTransform(working[3][3][6].copy(), working[4][2][-1]),
                  )
        self.wait()

        coefficients = MathTex("b_0 = \sum_{i = 1}^n m_i\log(-z_i)", r"b_k = -\sum_{i = 1}^n \frac{m_i}{kz_i^k}")
        coefficients[0][:2].set_color(YELLOW)
        coefficients[0][8:10].set_color(YELLOW)
        coefficients[0][15:17].set_color(GREEN)
        coefficients[1][:2].set_color(YELLOW)
        coefficients[1][9:11].set_color(YELLOW)
        coefficients[1][13].set_color(GREEN)
        coefficients[1][15].set_color(GREEN)

        working[5].next_to(conv_text, DOWN)
        coefficients.scale(0.7).shift(RIGHT * 32/9).next_to(working[5], DOWN)
        coefficients[0].shift(LEFT * 0.3)
        coefficients[1].shift(RIGHT * 0.3)
        self.play(AnimationGroup([Write(working[5]), FadeIn(coefficients, shift=DOWN)], lag_ratio=0.5))

        self.play(FadeOut(z_i_mag), source_dots.animate.set_opacity(1),
                  target_dots.animate.set_opacity(0.5), Unwrite(source_label), Unwrite(target_label))
        self.wait()
        interp = ValueTracker(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(lambda z: interpolate(f, get_truncated(10, 1 - 1j), interp))
        ))
        self.play(interp.animate.set_value(1))
        self.wait()
        self.play(FadeOut(working[1]), FadeOut(working[4]), working[5].animate.next_to(title, DOWN), Unwrite(coefficients),
                  conv_text.animate.shift(UP * 1.2), run_time=1.5)
        self.wait()

        error = VGroup(MathTex(r"\text{Error}=", r"\left|\sum_{k = p + 1}^\infty b_k z^k \right|"),
                       MathTex(r"=\left| \sum_{k = p + 1}^\infty \left(-\sum_{i = 1}^n \frac{m_i}{kz_i^k} \right)z^k\right|"),
                       MathTex(r"\leq \frac{1}{p + 1} \sum_{i = 1}^n m_i", r"\sum_{k = p + 1}^\infty \left|\frac{z^k}{r^k}\right|"),
                       MathTex(r"\leq \frac{1}{p + 1} \sum_{i = 1}^n m_i", r"\sum_{k = p + 1}^\infty \left|\frac{z}{r}\right|^k"),
                       MathTex(r"\leq \frac{a_0}{p + 1}", r"\frac{\left|\frac{z}{r}\right|^p}{\left|\frac{r}{z}\right| - 1}"),
                       MathTex(r"\leq \frac{a_0}{(p + 1)(\left|\frac{r}{z}\right| - 1)}", r"\left|\frac{z}{r}\right|^p"),
                       ).scale(0.75)
        error[0][1][-10:-8].set_color(YELLOW)
        error[0][1][-8].set_color(BLUE)
        error[1][0][-16:-14].set_color(YELLOW)
        error[1][0][-12].set_color(GREEN)
        error[1][0][-10].set_color(GREEN)
        error[1][0][-8].set_color(BLUE)

        error[2][0][-2:].set_color(YELLOW)
        error[2][1][-9].set_color(BLUE)
        error[2][1][-6].set_color(GREEN)

        error[3][0][-2:].set_color(YELLOW)
        error[3][1][-7].set_color(BLUE)
        error[3][1][-5].set_color(GREEN)

        error[4][0][1:3].set_color(YELLOW)
        error[4][1][2].set_color(BLUE)
        error[4][1][4].set_color(GREEN)
        error[4][1][11].set_color(GREEN)
        error[4][1][13].set_color(BLUE)

        error[5][0][1:3].set_color(YELLOW)
        error[5][0][12].set_color(GREEN)
        error[5][0][14].set_color(BLUE)
        error[5][1][3].set_color(BLUE)
        error[5][1][5].set_color(BLUE)

        error[0].next_to(conv_text, DOWN).shift(LEFT)
        self.play(Write(error[0]))
        self.wait()
        error[1].next_to(error[0], DOWN)
        error[1].shift(RIGHT * (error[0][0][-1].get_x() - error[1][0][0].get_x()))
        self.play(ReplacementTransform(error[0][0][-1].copy(), error[1][0][0]),
                  ReplacementTransform(error[0][1][:13].copy(), error[1][0][1:14]),
                  ReplacementTransform(error[0][1][13:15].copy(), error[1][0][14:-8]),
                  ReplacementTransform(error[0][1][15:].copy(), error[1][0][-8:]),
                  )
        self.wait()
        radius_arrow = Arrow(plane.c2p(1, -1), plane.c2p(1 - rad.get_value(), -1), color=GREEN, buff=0)
        radius_label = MathTex("r").scale(0.75).next_to(radius_arrow, DOWN).shift(UP * 0.1)
        self.play(GrowArrow(radius_arrow), Write(radius_label), )

        error[2].shift(error[1][0][0].get_center() - error[2][0][0].get_center())
        self.play(ReplacementTransform(error[1][0][0], error[2][0][0]),
                  Write(error[2][0][1]), ReplacementTransform(error[1][0][23], error[2][0][2]),
                  Unwrite(error[1][0][14]), Unwrite(error[1][0][28]), Unwrite(error[1][0][15]),
                  ReplacementTransform(error[1][0][24], error[2][0][3:6]),
                  ReplacementTransform(error[1][0][16:21], error[2][0][6:-2]),
                  ReplacementTransform(error[1][0][21:23], error[2][0][-2:]),
                  ReplacementTransform(error[1][0][7:14], error[2][1][:7]),
                  ReplacementTransform(error[1][0][1:7], error[2][1][7:11]),
                  ReplacementTransform(error[1][0][-8:-6], error[2][1][11:13]),
                  ReplacementTransform(error[1][0][23].copy(), error[2][1][13]),
                  ReplacementTransform(VGroup(error[1][0][25], error[1][0][27]), error[2][1][14]),
                  ReplacementTransform(error[1][0][26], error[2][1][15]),
                  ReplacementTransform(error[1][0][-6:], error[2][1][-4:]),
                  )
        self.wait()
        error[3].shift(error[1][0][0].get_center() - error[3][0][0].get_center())
        self.play(ReplacementTransform(error[2][0], error[3][0]),
                  ReplacementTransform(error[2][1][:7], error[3][1][:7]),
                  ReplacementTransform(error[2][1][7:11], error[3][1][7:10]),
                  ReplacementTransform(error[2][1][11], error[3][1][10]),
                  ReplacementTransform(VGroup(error[2][1][12], error[2][1][15]), error[3][1][-1]),
                  ReplacementTransform(error[2][1][13], error[3][1][11]),
                  ReplacementTransform(error[2][1][14], error[3][1][12]),
                  ReplacementTransform(error[2][1][16:], error[3][1][-4:-1]),
                  )
        self.wait()
        error[4].shift(error[1][0][0].get_center() - error[4][0][0].get_center())
        self.play(ReplacementTransform(error[3][0][0], error[4][0][0]),
                  ReplacementTransform(error[3][0][2:6], error[4][0][3:7]), Unwrite(error[3][0][1]),
                  ReplacementTransform(error[3][0][6:], error[4][0][1:3]), Unwrite(error[3][1][:4]),
                  ReplacementTransform(error[3][1][7:10], error[4][1][:2]),
                  ReplacementTransform(error[3][1][10:13], error[4][1][2:5]),
                  ReplacementTransform(error[3][1][13:16], error[4][1][5:7]),
                  ReplacementTransform(VGroup(error[3][1][4:7], error[3][1][-1]), error[4][1][7]), Write(error[4][1][8]),
                  ReplacementTransform(error[3][1][7:10].copy(), error[4][1][9:11]),
                  ReplacementTransform(error[3][1][10].copy(), error[4][1][13]),
                  ReplacementTransform(error[3][1][11].copy(), error[4][1][12]),
                  ReplacementTransform(error[3][1][12].copy(), error[4][1][11]),
                  ReplacementTransform(error[3][1][13:16].copy(), error[4][1][14:16]),
                  Write(error[4][1][16:])
                  )
        self.wait()
        error[5].shift(error[1][0][0].get_center() - error[5][0][0].get_center())
        self.play(ReplacementTransform(error[4][0][0], error[5][0][0]),
                  ReplacementTransform(error[4][0][1:3], error[5][0][1:3]),
                  ReplacementTransform(VGroup(error[4][0][3], error[4][1][8]), error[5][0][3]),
                  Write(error[5][0][4]), Write(error[5][0][8]),
                  ReplacementTransform(error[4][0][4:7], error[5][0][5:8]),
                  Write(error[5][0][9]), Write(error[5][0][-1]),
                  ReplacementTransform(error[4][1][9:], error[5][0][10:-1]),
                  ReplacementTransform(error[4][1][:2], error[5][1][:3]),
                  ReplacementTransform(error[4][1][2:5], error[5][1][3:6]),
                  ReplacementTransform(error[4][1][5:7], error[5][1][6:9]),
                  ReplacementTransform(error[4][1][7], error[5][1][9]),
                  )
        self.wait()
        heatmap.clear_updaters()
        self.play(Transform(heatmap, get_heatmap(f).set_opacity(0.75)))
        self.wait()
        # self.play(Transform(heatmap, get_heatmap(get_truncated(10, 1 - 1j)).set_opacity(0.75)))
        # self.wait()
        self.play(FadeOut(radius_arrow), FadeOut(radius_label))
        # todo: add radius arrow

class Flip(Scene):
    def construct(self):
        cmap = plt.get_cmap("plasma")

        line = Line(UP * 4, DOWN * 4).set_z_index(10)

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        resolution = 1000
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).shift(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        target_coords = [[1, -1.2], [1.1, -1], [1.3, -0.8], [1.4, -1.3], [1.5, -1.6], [1.7, -1.4]]
        source_coords = [[-2.5, 1.3], [-2.7, 0.8], [-2.9, 1.4], [-3, 1.1], [-3.1, 1.5], [-3.2, 0.9], [-3.3, 1.2],
                         [-3.5, 1]]

        def f(z):
            ans = np.zeros_like(z)
            for i in range(len(source_coords)):
                ans += np.real(np.log(z - (source_coords[i][0] + 1j * source_coords[i][1])))
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

        self.add(line, plane, border)

        def interpolate(f1, f2, t):
            return f1(Z) * (1 - t.get_value()) + f2(Z) * t.get_value()

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

        quadtree = getGrid().shift(LEFT * 32 / 9).set_color(BLUE)
        title = Text("Local Expansion").to_edge(UP).shift(RIGHT * 32 / 9)
        quadtree[2][8].set_color(YELLOW).set_z_index(6)
        quadtree[2][3].set_color(ORANGE).set_z_index(6)

        boxes = VGroup(quadtree[2][3].copy(), quadtree[2][8].copy())

        target_dots = VGroup([Dot(plane.c2p(target_coords[i][0], target_coords[i][1]), color=BLUE) for i in range(6)]).set_z_index(8)
        target_dots.set_opacity(0.25)
        source_dots = VGroup(
            [Dot(plane.c2p(source_coords[i][0], source_coords[i][1]), color=GREEN) for i in range(8)]).set_z_index(8)
        self.add(boxes, title, target_dots, source_dots)

        heatmap = get_heatmap(f)
        self.add(heatmap)
        self.wait()
        newtitle = Text("Flip (M2L)").to_edge(UP).shift(RIGHT * 32 / 9)
        self.play(FadeTransform(title, newtitle))
        self.wait()

        z_0_circle = Circle(color=GREEN, radius=DEFAULT_DOT_RADIUS * 2,
                            fill_color=GREEN, fill_opacity=0.5).move_to(plane.c2p(-3, 1)).set_z_index(10)
        z_0_label = MathTex("z_0").scale(0.6).move_to(z_0_circle).set_z_index(12)
        self.play(source_dots.animate.set_opacity(0.25), Write(z_0_label), FadeIn(z_0_circle),
                  Transform(heatmap, get_heatmap(get_multipole(10, -3 + 1j)).set_opacity(0.75)))
        self.wait()

        plane_unit = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]
        multipole_conv_circle = VGroup(Circle(radius=np.sqrt(2) * plane_unit, fill_color=BLACK, fill_opacity=0.3, stroke_width=0
                                    ).move_to(plane.c2p(-3, 1)),
                             DashedVMobject(Circle(radius=np.sqrt(2) * plane_unit, color=WHITE).move_to(plane.c2p(-3, 1)),
                                           dashed_ratio=0.5, num_dashes=25))

        plate = Rectangle(width=plane_size, height=plane_size, fill_opacity=1).move_to(plane.c2p(0, 0))
        local_conv_circle = VGroup(
            Difference(plate, Circle(radius=np.sqrt(2) * plane_unit).move_to(plane.c2p(1, -1)),
                       fill_color=BLACK, fill_opacity=0.3, stroke_width=0),
            DashedVMobject(Circle(radius=np.sqrt(2) * plane_unit, color=WHITE).move_to(plane.c2p(1, -1)),
                           dashed_ratio=0.5, num_dashes=25))
        self.play(FadeIn(multipole_conv_circle))

        z_1_circle = Circle(color=BLUE, radius=DEFAULT_DOT_RADIUS * 2,
                            fill_color=BLUE, fill_opacity=0.5).move_to(plane.c2p(1, -1)).set_z_index(10)
        z_1_label = MathTex("z_1").scale(0.6).move_to(z_1_circle).set_z_index(12)
        interp = ValueTracker(0)
        heatmap.add_updater(lambda m: m.become(
            get_heatmap(lambda z: interpolate(get_multipole(10, -3 + 1j), get_local(10, 1 - 1j), interp))
        ))
        self.play(FadeOut(multipole_conv_circle), FadeIn(local_conv_circle), interp.animate.set_value(1),
                  Write(z_1_label), FadeIn(z_1_circle))
        self.wait()

        assumption = MathTex(r"\text{Assume } z_1 \text{ to be the origin}").scale(0.75).shift(RIGHT * 32/9 + UP * 2.5)
        assumption[0][6:8].set_color(BLUE)
        self.play(Write(assumption))
        self.wait()

        working = VGroup(MathTex("P_{ME}(z) = a_0\log(z - z_0) +", r"\sum_{k = 1}^\infty a_k (z - z_0)^{-k}"),
                         MathTex(r"P_{ME}(z) = a_0\log\left(-z_0\left(1 - \frac{z}{z_0}\right)\right)",
                                 r"+\sum_{k = 1}^\infty a_k (-z_0)^{-k}\left(1 - \frac{z}{z_0}\right)^{-k}"),
                         MathTex(r"= a_0\log(-z_0) +", r"a_0\log\left(1 - \frac{z}{z_0}\right)",
                                 r"+\sum_{k = 1}^\infty a_k (-z_0)^{-k}\left(1 - \frac{z}{z_0}\right)^{-k}"),
                         MathTex(r"= a_0\log(-z_0) +", r"\sum_{l = 1}^\infty -\frac{a_0}{l} \left(\frac{z}{z_0}\right)^l",
                                 r"+\sum_{k = 1}^\infty a_k (-z_0)^{-k}\left(1 - \frac{z}{z_0}\right)^{-k}"),
                         MathTex(r"= a_0\log(-z_0) +", r"\sum_{l = 1}^\infty -\frac{a_0}{l} \left(\frac{z}{z_0}\right)^l",
                                 r"+\sum_{k = 1}^\infty a_k (-z_0)^{-k}", r"\sum_{l = 0}^\infty \binom{k + l - 1}{l} \left(\frac{z}{z_0}\right)^l"),
                         MathTex(r"= \left(a_0\log(-z_0) + \sum_{k = 1}^\infty a_k (-z_0)^{-k}\right)",
                                 r"+ \sum_{l = 1}^\infty -\frac{a_0}{l} \left(\frac{z}{z_0}\right)^l",
                                 r"+ \sum_{l = 1}^\infty \sum_{k = 1}^\infty a_k (-z_0)^{-k} \binom{k + l - 1}{l} \left(\frac{z}{z_0}\right)^l",),
                         MathTex(r"= \left(a_0\log(-z_0) + \sum_{k = 1}^\infty a_k (-z_0)^{-k}\right)",
                                 r"+ \sum_{l = 1}^\infty z_0^{-l}\left(\sum_{k = 1}^\infty \left(a_k (-z_0)^{-k} \binom{k + l - 1}{l}\right)-\frac{a_0}{l}  \right)z^l", ),
                         MathTex(r"P_{LE}(z) = b_0 + \sum_{l = 1}^\infty b_k z^l")
                         ).scale(0.55).shift(RIGHT * 32/9 + UP * 1.5)
        working[0][0][4].set_color(BLUE)
        working[0][0][7:9].set_color(YELLOW)
        working[0][0][13].set_color(BLUE)
        working[0][0][15:17].set_color(GREEN)
        working[0][1][5:7].set_color(YELLOW)
        working[0][1][8].set_color(BLUE)
        working[0][1][10:12].set_color(GREEN)
        self.play(Write(working[0]))
        self.wait()

        z_1_arrow = Arrow(plane.c2p(1, -1), plane.c2p(-3, 1))
        rad_arrow = Arrow(plane.c2p(1.1, -0.9), plane.c2p(2, 0), buff=0.1)
        self.play(GrowArrow(z_1_arrow), GrowArrow(rad_arrow))

        self.wait()

        working[1][0].set_x(32/9).shift(UP * (working[0][0][0].get_y() - working[1][0][0].get_y()))
        working[1][1].next_to(working[1][0], DOWN).shift(RIGHT * (working[1][0][7].get_left()[0] - working[1][1][0].get_left()[0]))
        working[1][0][4].set_color(BLUE)
        working[1][0][7:9].set_color(YELLOW)
        working[1][0][14:16].set_color(GREEN)
        working[1][0][19].set_color(BLUE)
        working[1][0][21:23].set_color(GREEN)
        for i in [1, 2, 3]:
            working[i][-1][6:8].set_color(YELLOW)
            working[i][-1][10:12].set_color(GREEN)
            working[i][-1][18].set_color(BLUE)
            working[i][-1][20:22].set_color(GREEN)

        self.play(ReplacementTransform(working[0][0][:12], working[1][0][:12]), Write(working[1][0][12]),
                  ReplacementTransform(working[0][0][12], working[1][0][16]),
                  ReplacementTransform(working[0][0][14:17], working[1][0][13:16]),
                  ReplacementTransform(working[0][0][15:17].copy(), working[1][0][17]),
                  ReplacementTransform(working[0][0][14].copy(), working[1][0][18]),
                  ReplacementTransform(working[0][0][13], working[1][0][18:23]),
                  ReplacementTransform(working[0][0][17], working[1][0][23]), Write(working[1][0][24]),
                  ReplacementTransform(working[0][0][-1], working[1][1][0]),
                  ReplacementTransform(working[0][1][:7], working[1][1][1:8]), Write(working[1][1][8]), Write(working[1][1][12]),
                  ReplacementTransform(working[0][1][9:12], working[1][1][9:12]),
                  ReplacementTransform(working[0][1][-2:], working[1][1][13:15]),
                  ReplacementTransform(working[0][1][7], working[1][1][15]),
                  ReplacementTransform(working[0][1][10:12].copy(), working[1][1][16]),
                  ReplacementTransform(working[0][1][9].copy(), working[1][1][17]),
                  ReplacementTransform(working[0][1][8], working[1][1][18:22]),
                  ReplacementTransform(working[0][1][12], working[1][1][22]),
                  ReplacementTransform(working[0][1][-2:].copy(), working[1][1][23:]),
                  )
        self.wait()

        working[2][:2].next_to(working[1], DOWN).shift(RIGHT * (working[1][0][0].get_x() - working[2][0][0].get_x()))
        working[2][2].next_to(working[2][:2], DOWN).set_x(4.5)
        # working[2][2].align_to(working[2][0][1], LEFT)
        for i in [2, 3, 4]:
            working[i][0][1:3].set_color(YELLOW)
            working[i][0][8:10].set_color(GREEN)
        working[2][1][:2].set_color(YELLOW)
        working[2][1][8].set_color(BLUE)
        working[2][1][10:12].set_color(GREEN)

        self.play(Write(working[2]))
        self.wait()

        working[3][:2].align_to(working[2][0], LEFT).shift(UP * (working[2][0][0].get_y() - working[3][0][0].get_y()))
        # working[3][2].set_x(4.5).shift(UP * (working[2][2][0].get_y() - working[3][2][0].get_y()))
        working[3][2].align_to(working[2][2], LEFT).shift(UP * (working[2][2][0].get_y() - working[3][2][0].get_y()))
        working[3][1][6:8].set_color(YELLOW)
        working[3][1][11].set_color(BLUE)
        working[3][1][13:15].set_color(GREEN)

        self.play(ReplacementTransform(working[2][0], working[3][0]),
                  ReplacementTransform(working[2][1][:2], working[3][1][6:8]),
                  ReplacementTransform(working[2][1][2:5], working[3][1][:5]),
                  ReplacementTransform(working[2][1][7], working[3][1][5]), Write(working[3][1][8:10]),
                  ReplacementTransform(working[2][1][5], working[3][1][10]), Unwrite(working[2][1][6]),
                  ReplacementTransform(working[2][1][8:12], working[3][1][11:15]),
                  ReplacementTransform(working[2][1][12], working[3][1][15]), Write(working[3][1][16]),
                  ReplacementTransform(working[2][2], working[3][2]),
                  )
        self.wait()

        working[4][:2].align_to(working[3][0], LEFT).shift(UP * (working[3][0][0].get_y() - working[4][0][0].get_y()))
        working[4][2:].set_x(4).shift(UP * (working[3][2][0].get_y() - working[4][2][0].get_y()))
        working[4][1][6:8].set_color(YELLOW)
        working[4][1][11].set_color(BLUE)
        working[4][1][13:15].set_color(GREEN)
        working[4][2][6:8].set_color(YELLOW)
        working[4][2][10:12].set_color(GREEN)
        working[4][3][14].set_color(BLUE)
        working[4][3][16:18].set_color(GREEN)

        self.play(ReplacementTransform(working[3][:2], working[4][:2]),
                  ReplacementTransform(working[3][2][:15], working[4][2]), Write(working[4][3][:5]),
                  ReplacementTransform(working[3][2][15], working[4][3][13]), Unwrite(working[3][2][16:18]),
                  ReplacementTransform(working[3][2][18:23], working[4][3][14:19]), Unwrite(working[3][2][23]),
                  ReplacementTransform(working[3][2][24], working[4][3][6]), Write(VGroup(working[4][3][5], working[4][3][7:13])),
                  Write(working[4][3][-1])
                  )
        self.wait()

        working[5][0].align_to(working[4][0], LEFT).shift(UP * (working[4][0][0].get_y() - working[5][0][0].get_y()))
        working[5][1:].set_x(32/9).shift(UP * (working[4][2][0].get_y() - working[5][2][0].get_y()))
        for i in [5, 6]:
            working[i][0][2:4].set_color(YELLOW)
            working[i][0][9:11].set_color(GREEN)
            working[i][0][18:20].set_color(YELLOW)
            working[i][0][22:24].set_color(GREEN)
        working[5][1][7:9].set_color(YELLOW)
        working[5][1][12].set_color(BLUE)
        working[5][1][14:16].set_color(GREEN)
        working[5][2][11:13].set_color(YELLOW)
        working[5][2][15:17].set_color(GREEN)
        working[5][2][29].set_color(BLUE)
        working[5][2][31:33].set_color(GREEN)

        self.play(ReplacementTransform(working[4][0][0], working[5][0][0]), Write(working[5][0][1]),
                  ReplacementTransform(working[4][0][1:], working[5][0][2:13]),
                  ReplacementTransform(working[4][2][1:].copy(), working[5][0][13:-1]), Write(working[5][0][-1]),
                  ReplacementTransform(working[4][1], working[5][1][1:]), Write(working[5][1][0]),
                  ReplacementTransform(working[4][2][0], working[5][2][0]),
                  ReplacementTransform(working[4][3][:5], working[5][2][1:6]),
                  ReplacementTransform(working[4][2][1:], working[5][2][6:20]),
                  ReplacementTransform(working[4][3][5:], working[5][2][20:]),
                  )
        self.wait()

        working[6][0].align_to(working[5][0], LEFT).shift(UP * (working[5][0][0].get_y() - working[6][0][0].get_y()))
        working[6][1:].set_x(32/9).shift(UP * (working[5][1][0].get_y() - working[6][1][0].get_y()))
        working[6][1][6].set_color(GREEN)
        working[6][1][9].set_color(GREEN)
        working[6][1][17:19].set_color(YELLOW)
        working[6][1][21:23].set_color(GREEN)
        working[6][1][36:38].set_color(YELLOW)
        working[6][1][41].set_color(BLUE)

        self.play(ReplacementTransform(working[5][0], working[6][0]), ReplacementTransform(working[5][1][0], working[6][1][0]),
                  ReplacementTransform(working[5][1][1:6], working[6][1][1:6]), working[5][2][1:6].animate.move_to(working[6][1][1:6]),
                  ReplacementTransform(working[5][1][14:16], VGroup(working[6][1][6], working[6][1][9])),
                  working[5][2][-4].animate.move_to(working[6][1][6]), working[5][2][-3].animate.move_to(working[6][1][9]),
                  ReplacementTransform(working[5][1][17], working[6][1][7:9]), working[5][2][-1].animate.move_to(working[6][1][8]),
                  Write(working[6][1][10]),
                  ReplacementTransform(working[5][2][6:11], working[6][1][11:16]), Write(working[6][1][16]),
                  ReplacementTransform(working[5][2][11:28], working[6][1][17:34]), Write(working[6][1][34]),
                  FadeOut(working[5][2][28]), FadeOut(working[5][2][30]), FadeOut(working[5][2][33]),
                  ReplacementTransform(working[5][1][6:11], working[6][1][35:40]), Write(working[6][1][40]),
                  ReplacementTransform(working[5][1][12], working[6][1][-2]), working[5][2][29].animate.move_to(working[6][1][-2]),
                  ReplacementTransform(working[5][1][17].copy(), working[6][1][-1]),
                  ReplacementTransform(working[5][2][-1], working[6][1][-1]),
                  FadeOut(working[5][1][11]), FadeOut(working[5][1][16]), FadeOut(working[5][2][0]),
                  FadeOut(working[5][1][13]), FadeOut(working[5][2][30]),
                  )
        working[5].set_opacity(0)
        self.wait()

        working[7][0][4].set_color(BLUE)
        working[7][0][7:9].set_color(YELLOW)
        working[7][0][15:17].set_color(YELLOW)
        working[7][0][17].set_color(BLUE)

        coefficients = VGroup(MathTex("b_0 = a_0\log(-z_0) + \sum_{k = 1}^\infty a_k (-z_0)^{-k}"),
                              MathTex(r"b_l = z_0^{-l}\left(\sum_{k = 1}^\infty \left(a_k (-z_0)^{-k} \binom{k + l - 1}{l}\right)-\frac{a_0}{l}  \right)"))
        coefficients.scale(0.55).arrange(DOWN).shift(RIGHT * 32/9)
        coefficients[0][0][:2].set_color(YELLOW)
        coefficients[0][0][3:5].set_color(YELLOW)
        coefficients[0][0][10:12].set_color(GREEN)
        coefficients[0][0][19:21].set_color(YELLOW)
        coefficients[0][0][23:25].set_color(GREEN)
        coefficients[1][0][:2].set_color(YELLOW)
        coefficients[1][0][3].set_color(GREEN)
        coefficients[1][0][6].set_color(GREEN)
        coefficients[1][0][14:16].set_color(YELLOW)
        coefficients[1][0][18:20].set_color(GREEN)
        coefficients[1][0][33:35].set_color(YELLOW)

        working[7].set_x(32/9).shift(UP * (working[7][0][0].get_y() - working[1][0][0].get_y()))
        self.play(ReplacementTransform(working[1][0][:6], working[7][0][:6]), FadeOut(working[1][0][6:]), FadeOut(working[1][1:]),
                  ReplacementTransform(working[6][0][0], working[7][0][6]),
                  ReplacementTransform(working[6][0][1:], working[7][0][7:9]),
                  ReplacementTransform(working[6][1][:6], working[7][0][9:15]),
                  ReplacementTransform(working[6][1][6:-2], working[7][0][15:17]),
                  ReplacementTransform(working[6][1][-2:], working[7][0][17:]),
                  ReplacementTransform(working[6][0][2:-1].copy(), coefficients[0][0][3:]), Write(coefficients[0][0][:3]),
                  ReplacementTransform(working[6][1][6:-2].copy(), coefficients[1][0][3:]), Write(coefficients[1][0][:3]),
                  )
        self.wait()

        # MathTex(r"P_{z_0}(z) = b_0 + \sum_{l = 1}^\infty b_k z^l")
        # MathTex(r"= \left(a_0\log(-z_0) + \sum_{k = 1}^\infty a_k (-z_0)^{-k}\right)",
        #       r"+ \sum_{l = 1}^\infty z_0^{-l}\left(\sum_{k = 1}^\infty \left(a_k (-z_0)^{-k} \binom{k + l - 1}{l}\right)-\frac{a_0}{l}  \right)z^l", ),



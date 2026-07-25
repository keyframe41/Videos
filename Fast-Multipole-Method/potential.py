from manim import *
import numpy as np
import matplotlib.pyplot as plt

def make_manim_color(rgb_array):
    return ManimColor(rgb_array)

class Force2D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(frame_center=[0, 0, 2])
        self.wait()
        p1 = Dot([-3, 1.5, 0])
        p2 = Dot([3, 1.5, 0])
        self.play(AnimationGroup([FadeIn(p1, scale=0.5), FadeIn(p2, scale=0.5)], lag_ratio=0.5))
        self.wait(0.5)
        pos1 = MathTex("x_i").next_to(p1, DOWN)
        pos1.add_updater(lambda m: m.next_to(p1, DOWN))
        pos2 = MathTex("x_j").next_to(p2, DOWN)
        self.add_fixed_orientation_mobjects(pos1, pos2)
        self.play(AnimationGroup([Write(pos1), p1.animate.scale(1.5).set_color(BLUE)]))
        self.play(AnimationGroup([Write(pos2), p2.animate.scale(2).set_color(TEAL)]))
        self.wait()

        arrow = always_redraw(lambda: Arrow(p1, p2, buff=0, stroke_width=4.5, color=YELLOW))
        force = MathTex(r"\vec{F}_{ij} = G\frac{m_im_j}{\|x_j - x_i\|}", r"\cdot\frac{x_j - x_i}{\|x_j - x_i\|}").shift(DOWN * 2)
        temp = MathTex(r"F = G\frac{m_im_j}{\|x_j - x_i\|}")
        temp.move_to(DOWN * 2)
        temp[0][3:5].set_color(BLUE)
        temp[0][5:7].set_color(TEAL)
        temp[0][9:-1].set_color(YELLOW)
        self.play(Create(arrow))
        self.play(Write(temp))
        self.wait(0.5)
        force[1][1:6].set_color(YELLOW)
        force[1][7:].set_color(YELLOW)
        force[0][6:8].set_color(BLUE)
        force[0][8:10].set_color(TEAL)
        force[0][11:].set_color(YELLOW)
        self.play(ReplacementTransform(temp[0][0], force[0][1]), ReplacementTransform(temp[0][1:], force[0][4:]), Write(force[1]))
        self.play(Write(force[0][0]), Write(force[0][2:4]))

        self.remove(temp)
        self.wait()

        # potential heatmap
        resolution = 800
        x = np.linspace(-10, 4, resolution)
        y = np.linspace(-3, 3, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        Z[np.abs(Z) < 0.15] = np.nan

        t_track = ValueTracker(2)

        def f(Z, t):
            return np.real(t * np.log(Z))

        raw_values = f(Z, t_track.get_value())
        raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

        val_min, val_max = raw_values.min(), raw_values.max()
        norm_values = (raw_values - val_min) / (val_max - val_min)

        cmap = plt.get_cmap("plasma")
        rgba_image = cmap(norm_values)

        rgba_image[:, :, 3] = 0.75
        rgb_uint8 = (rgba_image * 255).astype(np.uint8)

        heatmap = ImageMobject(rgb_uint8)
        heatmap.stretch_to_fit_width(14).stretch_to_fit_height(6).move_to([0, 1.5, 0])
        heatmap.set_z_index(-10)

        self.play(FadeIn(heatmap), force.animate.shift(DOWN * 1.5).set_opacity(0.5))
        potential = MathTex(r"\Phi_{ij} = ", r"Gm_j\log(\|x_i - x_j\|)").shift(DOWN * 2).set_z_index(11)
        potential[1][1:3].set_color(TEAL)
        potential[1][7:-1].set_color(YELLOW)
        bg_rect = SurroundingRectangle(potential, fill_color=BLACK, fill_opacity=0.25).set_z_index(10)
        potential_g = VGroup(potential, bg_rect)
        self.add_fixed_in_frame_mobjects(potential_g)
        self.play(Write(potential), Create(bg_rect))
        self.wait()

        # centered heatmap
        x = np.linspace(-8, 8, resolution)
        y = np.linspace(-8, 8, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        Z[np.abs(Z) < 0.15] = np.nan

        raw_values = f(Z, t_track.get_value())
        raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

        val_min, val_max = raw_values.min(), raw_values.max()
        norm_values = (raw_values - val_min) / (val_max - val_min)

        cmap = plt.get_cmap("plasma")
        rgba_image = cmap(norm_values)

        rgba_image[:, :, 3] = 0.75
        rgb_uint8 = (rgba_image * 255).astype(np.uint8)

        heatmap2 = ImageMobject(rgb_uint8).stretch_to_fit_width(16).stretch_to_fit_height(16)
        heatmap2.set_z_index(-10)
        stuff = VGroup(p1, p2, pos1, pos2, arrow)

        self.play(stuff.animate.shift(-p2.get_center()),
                  heatmap.animate.shift(-p2.get_center()).set_opacity(0), FadeIn(heatmap2),
                  # FadeTransform(heatmap, heatmap2),
                  potential_g.animate.to_corner(UR),
                  Unwrite(force))
        self.wait()

        # shift to 3d
        axes = ThreeDAxes(
            x_range=[-8, 8, 2], y_range=[-8, 8, 2], z_range=[-6, 4, 2],
            x_length=16, y_length=16, z_length=10
        )

        cmap_3d = plt.get_cmap("plasma")
        num_stops = 8
        ratios = np.linspace(0, 1, num_stops)
        pivots = np.linspace(-6, 4, num_stops)
        colorscale = [(make_manim_color(cmap_3d(r)[:3]), p) for r, p in zip(ratios, pivots)]

        def param_surface(u, v):
            z_complex = u + 1j * v
            if np.abs(z_complex) < 0.1:
                z_complex = 0.1
            z_height = f(z_complex, t_track.get_value())
            return axes.c2p(u, v, z_height)

        surface = Surface(
            param_surface,
            u_range=[-8, 8], v_range=[-8, 8], resolution=(100, 100), fill_opacity=0.5,
            checkerboard_colors=False, stroke_width=0.2, stroke_opacity=0
        )
        surface.set_fill_by_value(axes=axes, colorscale=colorscale, axis=2)

        self.play(Create(axes), Create(surface), FadeOut(heatmap2), run_time=2)
        self.wait()


        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=3, rate_func=smooth)
        self.wait()

        p3 = always_redraw(lambda: Dot3D(param_surface(axes.p2c(p1.get_center())[0], axes.p2c(p1.get_center())[1]),
                                         color=BLUE, radius=0.1, resolution=(12, 12)))
        pos3 = MathTex("U_{ij}")
        pos3.add_updater(lambda m: m.move_to(p3.get_center() + UP * 0.4))
        self.add_fixed_orientation_mobjects(pos3, center_func=p3.get_center)
        line3d = always_redraw(lambda: DashedLine(p1.get_center(), p3))

        def get_derivative_arrow():
            coords = axes.p2c(p3.get_center())
            x, y, z = coords[0], coords[1], coords[2]
            t = t_track.get_value()
            z_complex = x + 1j * y

            dw_dz = t / z_complex
            gradient = np.conj(dw_dz)
            dx, dy = np.real(gradient) * -3, np.imag(gradient) * -3
            z_target = np.real(t * np.log((x + dx) + 1j * (y + dy)))
            start_point = p3.get_center()
            end_point = axes.c2p(x + dx, y + dy, z_target)

            return Arrow(start_point, end_point, buff=0, color=YELLOW)

        derivative = always_redraw(get_derivative_arrow)


        rot_tracker = ValueTracker(0.0)
        self.camera.theta_tracker.add_updater(lambda m, dt: m.increment_value(rot_tracker.get_value() * dt))
        self.play(rot_tracker.animate.set_value(0.1),
                  ReplacementTransform(p1.copy(), p3), Create(line3d), Write(pos3))
        self.play(GrowArrow(derivative))
        self.wait()
        self.play(p1.animate.move_to(axes.c2p(-3, 0, 0)))
        self.wait(0.5)
        self.play(p1.animate.move_to(axes.c2p(-2, -2, 0)))
        self.wait(0.5)
        self.play(p1.animate.move_to(axes.c2p(-3, 3, 0)))
        self.wait(0.5)
        self.play(p1.animate.move_to(axes.c2p(-5, 1.5, 0)))
        self.wait(25)


class ComplexLog(ThreeDScene):
    def construct(self):
        line = Line(4 * UP, 4 * DOWN, stroke_width=6)

        def f(z):
            return np.real(2 * np.real(np.log(z)))

        x_min, x_max = -2, 2
        y_min, y_max = -2, 2
        resolution = 800
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE,  "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.5},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).move_to(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        labels = VGroup()
        shift_vector = LEFT * 0.25 + DOWN * 0.25
        for x_val in [-1, 1, 2]:
            label = MathTex(str(x_val), color=WHITE, font_size=24)
            label.move_to(plane.n2p(x_val) + shift_vector)
            labels.add(label)

        y_vals = [(-1j, "-i"), (1j, "i"), (2j, "i")]
        for y_val, label_text in y_vals:
            label = MathTex(label_text, color=WHITE, font_size=24)
            label.move_to(plane.n2p(y_val) + shift_vector)
            labels.add(label)
        labels.set_z_index(5)

        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_max, y_min, resolution)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        raw_values = f(Z)
        raw_values = np.nan_to_num(raw_values, nan=0.0, posinf=0.0, neginf=0.0)

        val_min, val_max = raw_values.min(), raw_values.max()
        cmap = plt.get_cmap("plasma")
        rgba_image = cmap((raw_values - val_min) / (val_max - val_min))
        rgba_image[:, :, 3] = 0.6
        rgb_uint8 = (rgba_image * 255).astype(np.uint8)

        heatmap = ImageMobject(rgb_uint8)
        heatmap.width = plane.x_length
        heatmap.height = plane.y_length
        heatmap.move_to(LEFT * 32 / 9).set_z_index(2)

        self.play(Create(border), Write(plane), Create(line), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(heatmap))
        self.wait()

        heading = Text("Force Evaluation").shift(RIGHT * 32/9).to_edge(UP)
        self.play(Write(labels), Write(heading))
        eval_point = Dot(plane.c2p(1.2, 0.8), color=BLUE).set_z_index(10)
        label = MathTex("z").next_to(eval_point, RIGHT).set_z_index(10)
        arrow = Arrow(plane.c2p(0, 0), eval_point, buff=0, color=YELLOW).set_z_index(10)
        potential = MathTex(r"\Phi(z) = \log\|z\|").next_to(heading, direction=DOWN, buff=MED_LARGE_BUFF)
        potential[0][2].set_color(BLUE)
        potential[0][-3:].set_color(YELLOW)
        self.play(AnimationGroup(AnimationGroup(GrowArrow(arrow), Create(eval_point), Write(label)),
                                 Write(potential), lag_ratio = 0.5))
        self.wait()
        log = VGroup(MathTex("\log(z)"),
                     MathTex("=", r"\log(\|z\|e^{i\theta})"),
                     MathTex("=\log{\|z\|} +", r"\log(e^{i\theta})"),
                     MathTex("=\log{\|z\|} +", r"i\theta")).arrange(DOWN).shift(RIGHT * 3 + DOWN)
        log[0].align_to(log[1][1], LEFT)
        log[2].align_to(log[1], LEFT)
        log[3].align_to(log[1], LEFT).align_to(log[2], DOWN)
        log[0][0][-2].set_color(BLUE)
        log[1][1][4:7].set_color(YELLOW)
        log[1][1][-2].set_color(YELLOW)
        log[2][0][-4:-1].set_color(YELLOW)
        log[2][1][-2].set_color(YELLOW)
        log[3][0][-4:-1].set_color(YELLOW)
        log[3][1][-1].set_color(YELLOW)

        angle = Angle(plane.get_axes()[0], arrow)
        theta = MathTex(r"\theta").set_color(YELLOW).scale(0.5).next_to(angle, RIGHT, buff=SMALL_BUFF).shift(UP * 0.05)
        theta.set_z_index(10)
        self.play(Create(angle), Write(theta))
        self.wait()

        self.play(Write(log[0]))
        self.wait(0.5)
        self.play(Write(log[1][0]), ReplacementTransform(log[0][0][:4].copy(), log[1][1][:4]),
                  ReplacementTransform(log[0][0][:4].copy(), log[1][1][:4]),
                  ReplacementTransform(log[0][0][-1].copy(), log[1][1][-1]),
                  ReplacementTransform(log[0][0][4].copy(), log[1][1][4:-1]))
        self.wait(0.5)
        self.play(Write(log[2][0][0]), Write(log[2][0][-1]),
                  ReplacementTransform(log[1][1][:3].copy(), log[2][0][1:4]),
                  ReplacementTransform(log[1][1][4:7].copy(), log[2][0][-4:-1]),

                  ReplacementTransform(log[1][1][:4].copy(), log[2][1][:4]),
                  ReplacementTransform(log[1][1][-4:].copy(), log[2][1][-4:]),)
        self.wait(0.5)
        self.play(ReplacementTransform(log[2][1][5:7], log[3][1]), Unwrite(log[2][1][:5]), Unwrite(log[2][1][-1]))
        self.wait()
        ans = MathTex(r"= \operatorname{Re}(\log{z})").next_to(potential, DOWN).align_to(potential[0][4], LEFT)
        ans[0][-2].set_color(BLUE)
        self.play(Write(ans))
        self.wait()
        self.play(FadeOut(log))
        self.wait()
        note = Tex(r"Let $\Phi(z) = \operatorname{Re}(P(z))$, so $P$ is our "
                   r"complex-valued function").shift(UP + RIGHT * 32/9).scale(0.5)
        note[0][5].set_color(BLUE)
        note[0][13].set_color(BLUE)
        self.play(Write(note))
        force = VGroup(MathTex(r"F = -\nabla \Phi(z)", r"=-\nabla\operatorname{Re}(P(z))"),
                        MathTex(r"= -\frac{\partial u}{\partial x} - i\frac{\partial u}{\partial y}")).arrange(DOWN)
        force.scale(0.8).shift(RIGHT * 32/9 + DOWN * 0.4)
        force[1][0].align_to(force[0][0][1], LEFT)
        force[0][0][-2].set_color(BLUE)
        force[0][1][-3].set_color(BLUE)
        force[1][0][2:4].set_color(GREEN)
        force[1][0][5:7].set_color(YELLOW)
        force[1][0][9:11].set_color(GREEN)
        force[1][0][12:].set_color(YELLOW)
        self.play(Write(force))
        self.wait(0.5)
        derivative_x = MathTex(r"P'(z) =", r"\frac{\partial u}{\partial x} +", r"i\frac{\partial v}{\partial x},",
                               r"\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y}")
        derivative_x.scale(0.8).shift(DOWN * 1.8 + RIGHT * 32/9)
        derivative_x[0][3].set_color(BLUE)
        derivative_x[1][:2].set_color(GREEN)
        derivative_x[1][3:5].set_color(YELLOW)
        derivative_x[2][1:3].set_color(RED)
        derivative_x[2][4:6].set_color(YELLOW)
        derivative_x[3][:2].set_color(RED)
        derivative_x[3][3:5].set_color(YELLOW)
        derivative_x[3][7:9].set_color(GREEN)
        derivative_x[3][10:12].set_color(YELLOW)
        self.play(Write(derivative_x))
        self.wait()
        temp = MathTex(r"P'(z) =", r"\frac{\partial u}{\partial x}", r"-i\frac{\partial u}{\partial y}")
        temp.scale(0.8).shift(DOWN * 1.8 + RIGHT * 32/9)
        temp[2][2:4].set_color(GREEN)
        temp[2][5:7].set_color(YELLOW)
        self.play(Unwrite(derivative_x[2][1:]), Unwrite(derivative_x[3][:6]), Unwrite(derivative_x[1][-1]),
                  derivative_x[0].animate.move_to(temp[0]), derivative_x[1][:-1].animate.move_to(temp[1]),
                  Transform(derivative_x[2][0], temp[2][1]),
                  Transform(derivative_x[3][6], temp[2][0]), Transform(derivative_x[3][7:], temp[2][2:]))
        self.wait()
        final = MathTex(r"\vec{F} = \langle-\operatorname{Re}(P'(z)), \operatorname{Im}(P'(z))\rangle").shift(RIGHT * 32/9 + DOWN * 3)
        final[0][11].set_color(BLUE)
        final[0][21].set_color(BLUE)
        self.play(Write(final))

class CauchyRiemann(Scene):
    def construct(self):
        derivative = MathTex(r"\lim_{\Delta z\to0} \frac{f(z + \Delta z) - f(z)}{\Delta z}")
        line = Line(4 * UP, 4 * DOWN, stroke_width=6)

        x_min, x_max = -2, 2
        y_min, y_max = -2, 2
        plane_size = 6.0

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": WHITE, "stroke_width": 2.5},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.5},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.15},
                             faded_line_ratio=5).move_to(LEFT * 32 / 9)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)

        self.add(plane, border, line)
        self.wait()

        heading = Text("Cauchy-Riemann Equations").scale(0.8).shift(RIGHT * 32 / 9).to_edge(UP)
        self.play(Write(heading))
        self.wait()

        rect = Rectangle(height=8, width=32 / 9, color=BLACK, fill_opacity=1).shift(LEFT * 32 / 9).set_z_index(-20)
        self.add(rect)
        axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=6, y_length=4,
                    tips=False).shift(RIGHT * 32 / 9).set_z_index(-25)
        f = lambda x: np.cos(np.pi / 2 * x)
        graph = axes.plot(f, x_range=[-3, 3], color=BLUE)
        self.play(Create(axes), Create(graph))
        self.wait()

        target_x = 0.2
        left = ValueTracker(-1)

        def get_line(track):
            slope = (f(track.get_value()) - f(target_x)) / (track.get_value() - target_x)
            l = slope * (-3 - target_x) + f(target_x)
            r = slope * (3 - target_x) + f(target_x)
            return Line(start=axes.c2p(-3, l), end=axes.c2p(3, r), stroke_width=3).set_z_index(-5)

        def get_circle(track):
            return Circle(stroke_width=4, radius=0.1).move_to(axes.c2p(track.get_value(), f(track.get_value())))

        target = Circle(stroke_width=4, radius=0.1, color=BLUE).move_to(axes.c2p(target_x, f(target_x))).set_z_index(5)
        coords = MathTex("(a, f(a))").scale(0.6).next_to(target, RIGHT).shift(UP * 0.1)
        self.play(Create(target), Write(coords))

        left_tangent = always_redraw(lambda: get_line(left).set_color(GREEN))
        left_target = always_redraw(lambda: get_circle(left).set_color(GREEN))
        self.play(Create(left_tangent), Create(left_target))
        self.play(left.animate.set_value(target_x - 0.001))

        right = ValueTracker(2)
        right_tangent = always_redraw(lambda: get_line(right).set_color(YELLOW))
        right_target = always_redraw(lambda: get_circle(right).set_color(YELLOW))
        self.play(Create(right_tangent), Create(right_target))
        self.play(right.animate.set_value(target_x + 0.001))
        eq = MathTex(r"\lim_{x\to a^-} \frac{f(x) - f(a)}{x - a} =", r"\lim_{x\to a^+} \frac{f(x) - f(a)}{x - a}")
        eq.shift(RIGHT * 32 / 9 + DOWN * 2.5).scale(0.75)
        eq[0][5:7].set_color(BLUE)
        eq[0][12:16].set_color(BLUE)
        eq[0][19].set_color(BLUE)
        eq[1][5:7].set_color(BLUE)
        eq[1][12:16].set_color(BLUE)
        eq[1][19].set_color(BLUE)
        self.play(Write(eq))
        self.wait()
        self.play(Unwrite(axes), Unwrite(graph), Unwrite(target), Unwrite(coords), Unwrite(eq),
                  Unwrite(right_tangent), Unwrite(right_target), Unwrite(left_tangent), Unwrite(left_target))
        self.wait()

        z = Dot(plane.c2p(0.6, 0.4), color=WHITE)
        label = MathTex("z", color=BLUE).next_to(z, DR, buff=SMALL_BUFF)
        self.play(Write(z), Write(label))
        self.wait()

        arrow1 = Arrow(start=z.get_center() + UP, end=z, buff=0, color=YELLOW)
        arrow2 = CurvedArrow(start_point=z.get_center() + RIGHT * 1.5, end_point=z.get_center() + RIGHT * 0.05,
                             color=YELLOW, tip_length=0.25)
        arrow3 = VGroup(CubicBezier([-5.5, -1, 0], [-4.5, 1.5, 0], [-4, -2, 0], [-2.7, 0.5, 0]),
                        Triangle(fill_opacity=1).scale(0.1).rotate(90 * DEGREES).move_to([-2.75, 0.45, 0])).set_color(
            YELLOW)
        self.play(AnimationGroup([Create(arrow1), Create(arrow2), Create(arrow3)], lag_ratio=0.3))
        self.wait()
        derivative = MathTex(r"f'(z) =", r"\lim_{\Delta z\to 0}",
                             r"\frac{f(z + \Delta z) - f(z)}{\Delta z}").shift(RIGHT * 32 / 9 + UP * 2.2).scale(0.8)
        derivative[0][3].set_color(BLUE)
        derivative[1][-4:-2].set_color(YELLOW)
        derivative[2][2].set_color(BLUE)
        derivative[2][4:6].set_color(YELLOW)
        derivative[2][10].set_color(BLUE)
        derivative[2][-2:].set_color(YELLOW)
        self.play(Write(derivative))
        self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3))
        self.wait()
        splitfunction = MathTex("f(z) = u(z) + iv(z)").scale(0.6).next_to(z, UP).shift(RIGHT * 0.7)
        splitfunction[0][2].set_color(BLUE)
        splitfunction[0][5].set_color(GREEN)
        splitfunction[0][11].set_color(RED)
        splitfunction[0][7].set_color(BLUE)
        splitfunction[0][-2].set_color(BLUE)

        partialderivative = MathTex(r"f'(z) =", r"\frac{\partial u}{\partial z} + ", r"i\frac{\partial v}{\partial z}")
        partialderivative.scale(0.8).shift(RIGHT * 32 / 9 + UP)
        partialderivative[0][3].set_color(BLUE)
        partialderivative[1][:2].set_color(GREEN)
        partialderivative[1][3:5].set_color(BLUE)
        partialderivative[2][1:3].set_color(RED)
        partialderivative[2][4:6].set_color(BLUE)
        self.play(AnimationGroup([Write(splitfunction), Write(partialderivative)], lag_ratio=0.5, run_time=1.5))
        self.wait()

        # x direction
        x_arrow = Arrow(plane.c2p(-0.6, 0.4), z, color=YELLOW, tip_length=0.2, buff=0)
        delta_x_label = MathTex(r"\Delta x").set_color(YELLOW).scale(0.6).next_to(x_arrow, LEFT, buff=SMALL_BUFF)
        delta_x_lim = MathTex("f'(z) = ", r"\lim_{\Delta x\to 0}",
                              r"\frac{(u(z + \Delta x) + iv(z + \Delta x)) - (u(z) + iv(z))}{\Delta x}")
        delta_x_lim.scale(0.5).shift(RIGHT * 32 / 9)
        delta_x_lim[0][3].set_color(BLUE)
        delta_x_lim[1][-4:-2].set_color(YELLOW)
        delta_x_lim[2][1].set_color(GREEN)
        delta_x_lim[2][3].set_color(BLUE)
        delta_x_lim[2][5:7].set_color(YELLOW)
        delta_x_lim[2][10].set_color(RED)
        delta_x_lim[2][12].set_color(BLUE)
        delta_x_lim[2][14:16].set_color(YELLOW)
        delta_x_lim[2][20].set_color(GREEN)
        delta_x_lim[2][22].set_color(BLUE)
        delta_x_lim[2][26].set_color(RED)
        delta_x_lim[2][28].set_color(BLUE)
        delta_x_lim[2][-2:].set_color(YELLOW)
        self.play(GrowArrow(x_arrow), Write(delta_x_label)),
        self.play(Write(delta_x_lim))

        temp = MathTex(r"\lim_{\Delta x\to 0}", r"\frac{u(z + \Delta x) - u(z)}{\Delta x} + ", r"\lim_{\Delta x\to 0}",
                       r"\frac{iv(z + \Delta x) - iv(z)}{\Delta x}").scale(0.5).align_to(delta_x_lim[1], LEFT)
        temp[0][3:5].set_color(YELLOW)
        temp[1][0].set_color(GREEN)
        temp[1][2].set_color(BLUE)
        temp[1][4:6].set_color(YELLOW)
        temp[1][8].set_color(GREEN)
        temp[1][10].set_color(BLUE)
        temp[1][-3:-1].set_color(YELLOW)
        temp[2][3:5].set_color(YELLOW)
        temp[3][1].set_color(RED)
        temp[3][3].set_color(BLUE)
        temp[3][5:7].set_color(YELLOW)
        temp[3][10].set_color(RED)
        temp[3][12].set_color(BLUE)
        temp[3][-2:].set_color(YELLOW)
        self.wait()
        self.play(ReplacementTransform(delta_x_lim[1], temp[0]), ReplacementTransform(delta_x_lim[1].copy(), temp[2]),
                  ReplacementTransform(delta_x_lim[2][-2:], temp[1][-3:-1]),
                  ReplacementTransform(delta_x_lim[2][-2:].copy(), temp[3][-2:]),
                  FadeOut(delta_x_lim[2][-3]), FadeIn(temp[1][-4]), FadeIn(temp[3][-3]),
                  Unwrite(delta_x_lim[2][0]), Unwrite(delta_x_lim[2][17]),
                  Unwrite(delta_x_lim[2][19]), Unwrite(delta_x_lim[2][-4]),
                  ReplacementTransform(delta_x_lim[2][1:8], temp[1][:7]),
                  ReplacementTransform(delta_x_lim[2][8], temp[1][-1]),
                  ReplacementTransform(delta_x_lim[2][9:17], temp[3][:8]),
                  ReplacementTransform(delta_x_lim[2][18], temp[1][7]),
                  ReplacementTransform(delta_x_lim[2][20:24], temp[1][8:12]),
                  ReplacementTransform(delta_x_lim[2][24], temp[3][8]),
                  ReplacementTransform(delta_x_lim[2][25:30], temp[3][9:14]))
        self.wait()
        derivative_x = MathTex(r"f'(z) =", r"\frac{\partial u}{\partial x} +", r"i\frac{\partial v}{\partial x}")
        derivative_x.scale(0.8).shift(RIGHT * 32 / 9)
        derivative_x[0][3].set_color(BLUE)
        derivative_x[1][:2].set_color(GREEN)
        derivative_x[1][3:5].set_color(YELLOW)
        derivative_x[2][1:3].set_color(RED)
        derivative_x[2][4:6].set_color(YELLOW)
        self.play(ReplacementTransform(delta_x_lim[0], derivative_x[0]),
                  ReplacementTransform(VGroup(temp[0], temp[1][:-1]), derivative_x[1][:-1]),
                  ReplacementTransform(temp[1][-1], derivative_x[1][-1]),
                  ReplacementTransform(temp[2:], derivative_x[2]))
        self.wait()

        # y direction
        y_arrow = Arrow(plane.c2p(0.6, -0.8), z, color=YELLOW, tip_length=0.2, buff=0)
        delta_y_label = MathTex(r"\Delta y").set_color(YELLOW).scale(0.6).next_to(y_arrow, DOWN, buff=SMALL_BUFF)
        delta_y_lim = MathTex("f'(z) = ", r"\lim_{\Delta y\to 0}",
                              r"\frac{(u(z + \Delta y) + iv(z + \Delta y)) - (u(z) + iv(z))}{i\Delta y}")
        delta_y_lim.scale(0.5).shift(RIGHT * 32 / 9 + DOWN)
        delta_y_lim[0][3].set_color(BLUE)
        delta_y_lim[1][-4:-2].set_color(YELLOW)
        delta_y_lim[2][1].set_color(GREEN)
        delta_y_lim[2][3].set_color(BLUE)
        delta_y_lim[2][5:7].set_color(YELLOW)
        delta_y_lim[2][10].set_color(RED)
        delta_y_lim[2][12].set_color(BLUE)
        delta_y_lim[2][14:16].set_color(YELLOW)
        delta_y_lim[2][20].set_color(GREEN)
        delta_y_lim[2][22].set_color(BLUE)
        delta_y_lim[2][26].set_color(RED)
        delta_y_lim[2][28].set_color(BLUE)
        delta_y_lim[2][-2:].set_color(YELLOW)
        self.play(GrowArrow(y_arrow), Write(delta_y_label)),
        self.play(Write(delta_y_lim))

        temp = MathTex(r"\lim_{\Delta y\to 0}", r"\frac{u(z + \Delta y) - u(z)}{i\Delta y} + ", r"\lim_{\Delta y\to 0}",
                       r"\frac{iv(z + \Delta y) - iv(z)}{i\Delta y}").scale(0.5).align_to(delta_y_lim[1], LEFT).shift(
            DOWN)
        temp[0][3:5].set_color(YELLOW)
        temp[1][0].set_color(GREEN)
        temp[1][2].set_color(BLUE)
        temp[1][4:6].set_color(YELLOW)
        temp[1][8].set_color(GREEN)
        temp[1][10].set_color(BLUE)
        temp[1][-3:-1].set_color(YELLOW)
        temp[2][3:5].set_color(YELLOW)
        temp[3][1].set_color(RED)
        temp[3][3].set_color(BLUE)
        temp[3][5:7].set_color(YELLOW)
        temp[3][10].set_color(RED)
        temp[3][12].set_color(BLUE)
        temp[3][-2:].set_color(YELLOW)
        self.wait()
        self.play(ReplacementTransform(delta_y_lim[1], temp[0]), ReplacementTransform(delta_y_lim[1].copy(), temp[2]),
                  ReplacementTransform(delta_y_lim[2][-3:], temp[1][-4:-1]),
                  ReplacementTransform(delta_y_lim[2][-3:].copy(), temp[3][-3:]),
                  FadeOut(delta_y_lim[2][-4]), FadeIn(temp[1][-5]), FadeIn(temp[3][-4]),
                  Unwrite(delta_y_lim[2][0]), Unwrite(delta_y_lim[2][17]),
                  Unwrite(delta_y_lim[2][19]), Unwrite(delta_y_lim[2][-5]),
                  ReplacementTransform(delta_y_lim[2][1:8], temp[1][:7]),
                  ReplacementTransform(delta_y_lim[2][8], temp[1][-1]),
                  ReplacementTransform(delta_y_lim[2][9:17], temp[3][:8]),
                  ReplacementTransform(delta_y_lim[2][18], temp[1][7]),
                  ReplacementTransform(delta_y_lim[2][20:24], temp[1][8:12]),
                  ReplacementTransform(delta_y_lim[2][24], temp[3][8]),
                  ReplacementTransform(delta_y_lim[2][25:30], temp[3][9:14]))
        self.wait()
        derivative_y = MathTex(r"f'(z) =", r"-i\frac{\partial u}{\partial y} +", r"\frac{\partial v}{\partial y}")
        derivative_y.scale(0.8).shift(DOWN).align_to(derivative_x, LEFT)
        derivative_y[0][3].set_color(BLUE)
        derivative_y[1][2:4].set_color(GREEN)
        derivative_y[1][5:7].set_color(YELLOW)
        derivative_y[2][:2].set_color(RED)
        derivative_y[2][3:5].set_color(YELLOW)
        self.play(ReplacementTransform(delta_y_lim[0], derivative_y[0]),
                  ReplacementTransform(VGroup(temp[0], temp[1][:-1]), derivative_y[1][:-1]),
                  ReplacementTransform(temp[1][-1], derivative_y[1][-1]),
                  ReplacementTransform(temp[2:], derivative_y[2]))
        self.wait()

        cr_equation = MathTex(r"\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y},",
                              r"\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y}")
        cr_equation.scale(0.8).shift(RIGHT * 32 / 9 + DOWN * 2)
        cr_equation[0][:2].set_color(GREEN)
        cr_equation[0][3:5].set_color(YELLOW)
        cr_equation[0][6:8].set_color(RED)
        cr_equation[0][9:11].set_color(YELLOW)
        cr_equation[1][:2].set_color(RED)
        cr_equation[1][3:5].set_color(YELLOW)
        cr_equation[1][7:9].set_color(GREEN)
        cr_equation[1][10:12].set_color(YELLOW)

        self.play(Write(cr_equation[0][5]), Write(cr_equation[1][5]),
                  Write(cr_equation[0][-1]),
                  ReplacementTransform(derivative_x[1][:-1].copy(), cr_equation[0][:5]),
                  ReplacementTransform(derivative_x[2][1:].copy(), cr_equation[1][:5]),
                  ReplacementTransform(derivative_y[1][0], cr_equation[1][-6]),
                  ReplacementTransform(derivative_y[1][2:-1].copy(), cr_equation[1][-5:]),
                  ReplacementTransform(derivative_y[2].copy(), cr_equation[0][-6:-1]))
        self.wait()



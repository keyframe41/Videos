from manim import *
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
import copy

np.set_printoptions(linewidth=2000)

class Low(Scene):
    def construct(self):
        title = Text("Low Dimensions").shift(UP * 6.5).scale(2)
        self.play(Write(title))

        pos = [[[1,	1], [-3, 2], [-4, -3], [6, -1], [1.5, -1.5], [-1.5, -0.5], [-4.5, 0.5], [3.5, 3.5]],
               [[1.4, 2.1], [-1.51, 1.71], [-2.98, -2.325], [4.57, -0.99], [2.67, -1.975], [-0.49, -0.84], [-3.56, 1.17], [4.41, 2.84]],
               [[2.32, 2.03], [-0.68, 1.79], [-2.62, -1.8], [3.98, -0.61], [3.06, -2.54], [-0.25, -1.35], [-2.96, 0.92], [4.27, 2.224]],
               [[2.58, 1.74], [-0.3, 1.58], [-2.89, -1.54], [3.75, -0.36], [3.48, -2.75], [0.01, -1.69], [-2.83, 0.58], [4.58, 2.02]],
               [[2.79, 1.64], [-0.18, 1.43], [-2.89, -1.4], [3.55, -0.26], [3.69, -2.78], [0.18, -1.8], [-2.79, 0.45], [4.58, 1.845]]]

        for i in range(5):
            for j in range(8):
                pos[i][j][1] = pos[i][j][1] * 1.5 - 2.3
        points = VGroup()
        lines = VGroup()
        colors = [RED_D, BLUE, GREEN, ORANGE]
        for i in range(5):
            dots = VGroup()
            arrows = VGroup()
            for j in range(8):
                dots.add(Dot(point=pos[i][j] + [0], color=colors[j % 4], radius=0.15))
                if i > 0:
                    arrows.add(Arrow(start=pos[i - 1][j] + [0], end=pos[i][j] + [0], color=colors[j % 4], buff=0).set_opacity(0.3))
            if i == 0:
                self.play(FadeIn(dots, arrows))
            else:
                self.play(FadeIn(arrows), ReplacementTransform(points[-1].copy(), dots), points[-1].animate.set_opacity(0.3))
            points.add(dots)
            lines.add(arrows)
            self.wait(0.5)

        self.wait(0.5)
        self.play(points[0].animate.set_opacity(1), ReplacementTransform(points[-1].copy(), points[0]), FadeOut(points[1:], lines))
        self.wait()

        arrow = Arrow(start=points[0][6], end=points[0][0], buff=0)
        arrowLabel = Tex("$q_{i|j}$").next_to(arrow.get_center(), UP).scale(1.5).set_color(TEAL)
        iLabel = Tex("$i$").next_to(points[0][0], DOWN).scale(1.5)
        jLabel = Tex("$j$").next_to(points[0][6], DOWN).scale(1.5)
        labels = VGroup(arrowLabel, iLabel, jLabel)
        self.play(Write(arrow), Write(labels))
        self.wait()

        colors = mpl.colormaps['viridis'](np.linspace(0, 1, 60))
        def create_glow(obj, rad):
            glow_group = VGroup()
            for i in range(60):
                new_circle = Circle(radius=rad * (1 - i / 60), stroke_opacity=0, fill_color=colors[i], fill_opacity=0.03).move_to(obj)
                glow_group.add(new_circle)
            return glow_group.set_z_index(-1)

        glow = create_glow(points[0][0], 5)
        self.play(FadeIn(glow), run_time=2.5)
        self.wait()

        equations = MathTex(r"q(i, j) = e^{\textstyle -\lVert y_i - y_j\rVert^2}",
                            r"q_{j|i} = \dfrac{q(i, j)}{\sum_{k \neq i} q(i, k)}").shift(UP * 4.5).scale(1.2)
        equations[0][0:6].set_color(TEAL)
        equations[0][10:15].set_color(TEAL)
        equations[1][0:4].set_color(TEAL)
        equations[1][5:11].set_color(TEAL)
        equations[1][17:23].set_color(TEAL)
        equations[0].shift(LEFT * 0.5)
        equations[1].shift(RIGHT * 0.5)
        self.play(Write(equations[0]))
        self.wait()
        self.play(Write(equations[1]))
        box = SurroundingRectangle(equations, color=YELLOW, buff=MED_SMALL_BUFF)
        self.play(Create(box))
        self.wait()
        symmetric = MathTex(r"q_{ij} = \dfrac{q(i, j)}{\sum_{j \neq l} q(k, l)}").shift(UP * 2.5 + LEFT * 3).scale(1.2)
        symmetric[0][0:3].set_color(TEAL)
        symmetric[0][4:10].set_color(TEAL)
        symmetric[0][16:22].set_color(TEAL)
        self.play(Write(symmetric))
        self.wait()

class High(ThreeDScene):
    def construct(self):
        title = Text("High Dimensions")
        self.add_fixed_in_frame_mobjects(title)
        title.shift(UP * 6.5).scale(2)
        axes = ThreeDAxes(x_range=[0, 5], y_range=[0, 5], z_range=[0, 5], x_length=5, y_length=5, z_length=5,
                          x_axis_config={"stroke_width" : 3}, y_axis_config={"stroke_width" : 3}, z_axis_config={"stroke_width" : 3}).shift(IN * 4)
        self.set_camera_orientation(phi=80 * DEGREES, theta=30 * DEGREES, zoom=1.8)
        self.begin_3dillusion_camera_rotation(rate=0.2)
        self.add(axes)
        self.play(Write(title))
        pos = [[1, 3, 3], [4, 2, 1], [1, 1, 1.5], [3, 4, 4], [2, 0.5, 3.5], [4, 4.5, 0.5], [1, 4, 1], [4, 2, 2]]
        colors = [RED_D, BLUE, GREEN, ORANGE]
        dots = VGroup(*[Dot3D(point=axes.c2p(pos[i][0], pos[i][1], pos[i][2]), color=colors[i % 4]) for i in range(8)])
        self.play(AnimationGroup(*[Create(dots[i]) for i in range(8)], lag_ratio=0.2))
        self.wait(15)

        arrow = Arrow(start=dots[6], end=dots[0], buff=0)
        arrowLabel = Tex("$p_{i|j}$").next_to(arrow.get_center(), UP).scale(1.5).set_color(BLUE)
        iLabel = Tex("$i$").next_to(dots[0], DOWN).scale(1.5)
        jLabel = Tex("$j$").next_to(dots[6], DOWN).scale(1.5)
        self.add_fixed_orientation_mobjects(arrowLabel, iLabel, jLabel)
        labels = VGroup(arrowLabel, iLabel, jLabel)
        self.play(Write(arrow), Write(labels))
        self.wait(5)

        colors = mpl.colormaps['viridis'](np.linspace(0, 1, 60))
        def create_glow(obj, rad):
            glow_group = VGroup()
            for i in range(60):
                new_circle = Circle(radius=rad * (1 - i / 60), stroke_opacity=0, fill_color=colors[i], fill_opacity=0.03).move_to(obj)
                glow_group.add(new_circle)
            self.add_fixed_orientation_mobjects(glow_group)
            return glow_group.set_z_index(-10)

        glow = create_glow(dots[0], 4)
        self.play(AnimationGroup(*[FadeIn(glow[i]) for i in range(59, -1, -1)], lag_ratio=0.025))
        self.wait(3)

        equations = MathTex(r"p(i, j) = e^{-\dfrac{\lVert x_i - x_j\rVert^2}{2\sigma_i^2}}",
                           r"p_{j|i} = \dfrac{p(i, j)}{\sum_{k \neq i} p(i, k)}").shift(UP * 4.2).scale(1.2)
        equations[0][0:6].set_color(BLUE)
        equations[0][10:15].set_color(BLUE)
        equations[1][0:4].set_color(BLUE)
        equations[1][5:11].set_color(BLUE)
        equations[1][17:23].set_color(BLUE)
        equations[0].shift(LEFT * 0.5)
        equations[1].shift(RIGHT * 0.5)
        self.add_fixed_in_frame_mobjects(equations[0])
        equations[0].shift(LEFT * 0.5)
        equations[1].shift(RIGHT * 0.5)
        self.play(Write(equations[0]))
        self.wait()
        self.add_fixed_in_frame_mobjects(equations[1])
        self.play(Write(equations[1]))
        box = SurroundingRectangle(equations, color=YELLOW, buff=MED_SMALL_BUFF)
        self.add_fixed_in_frame_mobjects(box)
        self.play(Create(box))
        self.wait(32)
        symmetric = MathTex(r"p_{ij} = \frac{p_{i|j} + p_{j|i}}{2n}").shift(UP * 2 + LEFT * 4).scale(1.2)
        symmetric[0][0:3].set_color(BLUE)
        symmetric[0][4:13].set_color(BLUE)
        self.add_fixed_in_frame_mobjects(symmetric)
        self.play(Write(symmetric))
        self.wait(12)

class Cost(Scene):
    def construct(self):
        kl_divergence = Text("Kullback-Liebler Divergence").shift(UP * 3)
        self.play(Write(kl_divergence))
        self.wait(0.5)
        loss = MathTex("C = ", r"\sum_i KL(P_i || Q_i)", "=", r"\sum_i \sum_j p_{j|i}\log \frac{p_{j|i}}{q_{j|i}}").shift(UP * 1.5)
        loss[1][5:7].set_color(BLUE)
        loss[1][9:11].set_color(TEAL)
        loss[3][4:8].set_color(BLUE)
        loss[3][11:15].set_color(BLUE)
        loss[3][16:20].set_color(TEAL)
        self.play(Write(loss))
        self.wait()
        loss_derivative = MathTex(r"\frac{\delta C}{\delta y_i}", "=", "2\sum_j (p_{j|i} - q_{j|i} + p_{i|j} - q_{i|j})(y_i - y_j)")
        loss_derivative[2][4:8].set_color(BLUE)
        loss_derivative[2][9:13].set_color(TEAL)
        loss_derivative[2][14:18].set_color(BLUE)
        loss_derivative[2][19:23].set_color(TEAL)
        self.play(Write(loss_derivative))
        self.wait()
        dots = VGroup(Dot(point=[-4.5, -2, 0], color=BLUE), Dot(point=[4.5, -2, 0], color=BLUE))
        self.play(FadeIn(dots))
        self.wait()
        n_coils = 5
        dir = dots[1].get_center() - dots[0].get_center()
        mag = np.linalg.norm(dir)
        dir /= mag
        perp = np.array([-dir[1], dir[0], 0])
        pos = dots[0].get_center()
        lines = VGroup()
        lines.add(Line(start=pos, end=pos + dir * 0.5, color=GREEN))
        pos += dir * 0.5
        npos = pos.copy()
        step = (mag - 1) / (2 * n_coils)
        for i in range(n_coils):
            print(pos, npos)
            npos += dir * step / 2 + perp * step
            lines.add(Line(start=pos, end=npos, color=GREEN))
            print(pos, npos)
            pos += dir * step / 2 + perp * step
            npos += dir * step - 2 * perp * step
            lines.add(Line(start=pos, end=npos, color=GREEN))
            pos += dir * step - 2 * perp * step
            npos += dir * step / 2 + perp * step
            lines.add(Line(start=pos, end=npos, color=GREEN))
            pos += dir * step / 2 + perp * step
        lines.add(Line(start=npos, end=npos + dir * 0.5, color=GREEN))
        self.play(Create(lines))
# entropy = 0
class Perplexity(Scene):
    def construct(self):
        pos = np.array([[1, 1], [-3, 2], [-4, -3], [6, -1], [1.5, -1.5], [-1.5, -0.5], [-4.5, 0.5], [3.5, 3.5]])
        points = VGroup(*[Dot(point=pos[i].tolist() + [0], color=BLUE) for i in range(8)])
        points[0].set_color(WHITE)
        self.add(points)

        sigma = ValueTracker(0.5)
        def get_sigma_tex():
            res = VGroup()
            tex = MathTex("\sigma =", str('{:.2f}'.format(sigma.get_value())))
            tex[0].to_corner(UL).shift(RIGHT * 1.7)
            rect = Rectangle(width=sigma.get_value() * 0.75, height=0.25, fill_color=[RED, ORANGE], fill_opacity=1, stroke_width=3).next_to(tex[0], RIGHT)
            tex[1].next_to(rect, RIGHT)
            res.add(tex, rect)
            return res
        sigma_tex = always_redraw(lambda: get_sigma_tex())
        self.add(sigma_tex)

        def get_labels():
            global entropy
            labels = VGroup()
            val = np.zeros(7)
            tot = 0
            var = sigma.get_value() ** 2
            for i in range(1, 8):
                val[i - 1] = np.exp(-(np.linalg.norm(pos[0] - pos[i]) ** 2) / (2 * var))
                tot += val[i - 1]
            entropy = tot
            val /= entropy
            for i in range(1, 8):
                labels.add(MathTex(str(round(val[i - 1], 2))).next_to(points[i], DOWN))
            return labels
        labels_tex = always_redraw(lambda: get_labels())
        self.add(labels_tex)

        def create_glow(obj, rad):
            num_rings = int(rad * 12)
            colors = mpl.colormaps['viridis'](np.linspace(0, 1, num_rings))
            glow_group = VGroup()
            for i in range(num_rings):
                new_circle = Circle(radius=rad * (1 - i / num_rings), stroke_opacity=0, fill_color=colors[i],
                                    fill_opacity=i / (num_rings ** 2 * 0.6) + 0.01).move_to(obj)
                glow_group.add(new_circle)
            return glow_group.set_z_index(-1)
        distr = always_redraw(lambda: create_glow(points[0], 2 * sigma.get_value()))
        self.add(distr)
        def get_perplexity_tex():
            global entropy
            res = VGroup()
            tex = MathTex(r"\text{Perplexity} =", str('{:.2f}'.format(entropy)))
            tex[0].next_to(sigma_tex, DOWN).align_to(sigma_tex[0][0], RIGHT)
            rect = Rectangle(width=entropy * 0.75, height=0.25, fill_color=[YELLOW, GOLD], fill_opacity=1, stroke_width=3).next_to(tex[0], RIGHT)
            tex[1].next_to(rect, RIGHT)
            res.add(tex, rect)
            return res
        perplexity_tex = always_redraw(lambda: get_perplexity_tex())
        self.add(perplexity_tex)

        self.wait(0.5)
        self.play(sigma.animate.set_value(8), run_time=12)
        self.wait()

class SNE(Scene):
    def construct(self):
        n_points = 100
        pos = np.random.uniform(low=-0.75, high=0.75, size=(n_points, 2))
        # pos = np.zeros((n_points, 2))
        # for i in range(n_points):
        #     pos[i, 0] = 5 * i / n_points - 2.5
        #     pos[i, 1] = 2 * (i % 2) - 1
        target_pos = np.zeros_like(pos)
        for i in range(n_points):
            target_pos[i] = np.array([np.cos(i * np.pi / 50), np.sin(i * np.pi / 50)]) * 3

        perplexity = 20

        probs_p = np.zeros((n_points, n_points))
        sigma = np.zeros(n_points)
        # Find sigmas suitable for given perplexity using binary search
        for i in range(n_points):
            min_sigma, max_sigma = 0.01, 1000
            while max_sigma - min_sigma > 1e-6:
                mid = (min_sigma + max_sigma) / 2
                # Calculate probs
                tot = 0
                for j in range(n_points):
                    if i == j:
                        probs_p[i, j] = 0
                    else:
                        probs_p[i, j] = np.exp(-(np.linalg.norm(target_pos[i] - target_pos[j]) ** 2) / (2 * mid ** 2))
                        tot += probs_p[i, j]
                probs_p[i, :] /= tot
                entropy = 0
                for j in range(n_points):
                    if i == j:
                        continue
                    entropy += -probs_p[i, j] * np.log2(probs_p[i, j])
                if 2 ** entropy > perplexity:
                    max_sigma = mid
                else:
                    min_sigma = mid
            sigma[i] = min_sigma
        # Add dots to scene
        cmap = plt.get_cmap('hsv')
        dots = VGroup(*[Dot(point=pos[i].tolist() + [0], color=ManimColor(cmap(i / n_points))) for i in range(n_points)])
        self.add(dots)
        probs_p = (probs_p + probs_p.T) / (2 * n_points)

        # Perform gradient descent
        max_iterations = 2500
        learning_rate = 5
        def get_momentum(t):
            if t < 250:
                return 0.5
            else:
                return 0.8

        iteration = 0
        iteration_text = MathTex(r"\text{Iterat ions: }", str(iteration)).to_corner(UL)
        self.add(iteration_text)
        cost = -1
        cost_text = MathTex(r"\text{Cost: }", str(round(cost, 2))).to_edge(UP).shift(RIGHT * 5.5)
        momentum = np.zeros_like(pos)

        while iteration <= max_iterations:
            self.remove(iteration_text, cost_text, dots)
            iteration_text = MathTex(r"\text{Iterations: }", str(iteration)).to_corner(UL)
            # cost_text = MathTex(r"\text{Cost: }", str(round(cost, 2))).to_edge(UP).shift(RIGHT * 5.5)
            dots = VGroup(*[Dot(point=pos[i].tolist() + [0], color=ManimColor(cmap(i / n_points))) for i in range(n_points)])
            self.add(iteration_text, dots)

            if iteration < 250:
                iteration += 1
                updates = 1
            elif iteration < 1000:
                iteration += 5
                updates = 5
            else:
                iteration += 10
                updates = 10
            for update in range(updates):
                # Calculate low-dimensional probabilities
                probs_q = np.zeros((n_points, n_points))
                tot = 0
                for i in range(n_points):
                    for j in range(n_points):
                        if i == j:
                            probs_q[i, j] = 0
                        else:
                            probs_q[i, j] = np.exp(-np.linalg.norm(pos[i] - pos[j]) ** 2)
                            tot += probs_q[i, j]
                probs_q /= tot
                for i in range(n_points):
                    for j in range(n_points):
                        if i == j:
                            continue
                        cost += probs_p[i, j] * np.log2(probs_p[i, j] / probs_q[i, j])
                gradient = np.zeros_like(pos)
                for i in range(n_points):
                    for j in range(n_points):
                        if i == j:
                            continue
                        gradient[i] += 2 * (probs_p[i, j] - probs_q[i, j] + probs_p[j, i] - probs_q[j, i]) * (pos[i] - pos[j])
                # print(probs_q)
                # print(gradient)
                next_pos = pos - learning_rate * gradient + get_momentum(iteration) * momentum
                momentum = next_pos - pos
                pos = next_pos


            self.wait(1 / config.frame_rate)
# sne all LR = 0.1
# sne 1-2 perp 10, 3-4 perp 15, 5-6 perp 20, 7-8 perp 25, 9-10 perp 5 scaled 1/4

class tSNE(Scene):
    def construct(self):
        screen_scaling = 10
        n_points = 1000
        n_dim = 50
        pos = np.random.uniform(low=-3, high=3, size=(n_points, 2))
        learning_rate = np.full(shape=(n_points, 2), fill_value=100)
        with open("tsneResult.txt", "r") as file:
            data = file.read().splitlines()
        for i in range(n_points):
            data[i] = data[i].split()
            for j in range(2):
                pos[i, j] = float(data[i][2 * j])
                learning_rate[i, j] = float(data[i][2 * j + 1])
        target_pos = np.zeros((n_points, n_dim))
        colors = np.zeros(n_points)
        with open("tsneDataset.txt", "r") as file:
            data = file.read().splitlines()
        for i in range(n_points):
            data[i] = data[i].split()
            for j in range(n_dim):
                target_pos[i, j] = float(data[i][j])
            colors[i] = float(data[i][-1]) / 10


        perplexity = 50

        probs_p = np.zeros((n_points, n_points))
        sigma = np.zeros(n_points)
        # Find sigmas suitable for given perplexity using binary search
        for i in range(n_points):
            min_sigma, max_sigma = 0.01, 1000
            while max_sigma - min_sigma > 1e-6:
                mid = (min_sigma + max_sigma) / 2
                # Calculate high-dimensional probabilities
                tot = 0
                for j in range(n_points):
                    if i == j:
                        probs_p[i, j] = 0
                    else:
                        probs_p[i, j] = np.exp(-(np.linalg.norm(target_pos[i] - target_pos[j]) ** 2) / (2 * mid ** 2))
                        tot += probs_p[i, j]
                probs_p[i, :] /= tot
                entropy = 0
                for j in range(n_points):
                    if i == j:
                        continue
                    entropy += -probs_p[i, j] * np.log2(probs_p[i, j])
                if 2 ** entropy > perplexity:
                    max_sigma = mid
                else:
                    min_sigma = mid
            sigma[i] = min_sigma
        # Process high-dimensional probabilities to be symmetric
        probs_p = (probs_p + probs_p.T) / (2 * n_points)

        # probs_p *= 4 # Early exaggeration

        # Add dots to scene
        cmap = plt.get_cmap('hsv')
        dots = VGroup(*[Dot(point=(pos[i] / screen_scaling).tolist() + [0], color=ManimColor(cmap(colors[i])), radius=0.04) for i in range(n_points)])
        self.add(dots)

        # Perform gradient descent

        def get_momentum(t):
            if t < 250:
                return 0.5
            else:
                return 0.8

        max_iterations = 5000
        iteration = 1000
        iteration_text = MathTex(r"\text{Iterations: }", str(iteration)).to_corner(UL)
        self.add(iteration_text)

        momentum = np.zeros_like(pos)
        delta = np.zeros((2, n_points, 2))
        delta_bar = np.zeros_like(delta)
        kappa = 2
        phi = 0.2

        while iteration <= max_iterations:
            self.remove(iteration_text, dots)
            iteration_text = MathTex(r"\text{Iterations: }", str(iteration)).to_corner(UL)
            dots = VGroup(*[Dot(point=(pos[i] / screen_scaling).tolist() + [0], color=ManimColor(cmap(colors[i])), radius=0.04) for i in range(n_points)])
            self.add(iteration_text, dots)

            # if iteration < 250:
            #     iteration += 1
            #     updates = 1
            # elif iteration < 1000:
            #     iteration += 5
            #     updates = 5
            # else:
            #     iteration += 10
            #     updates = 10 # Stepping speedups
            iteration += 5
            updates = 5

            if iteration == 50: # Early exaggeration
                probs_p /= 4

            print(iteration)
            for update in range(updates):
                # Calculate low-dimensional probabilities
                probs_q = np.zeros((n_points, n_points))
                tot = 0
                for i in range(n_points):
                    for j in range(n_points):
                        if i == j:
                            probs_q[i, j] = 0
                        else:
                            probs_q[i, j] = 1 / (1 + np.linalg.norm(pos[i] - pos[j]) ** 2)
                            tot += probs_q[i, j]
                probs_q /= tot
                # Calculate learning rate and update learning rates according to the delta-bar-delta rule
                gradient = np.zeros_like(pos)
                for i in range(n_points):
                    for j in range(n_points):
                        if i == j:
                            continue
                        gradient[i] += 4 * (probs_p[i, j] - probs_q[i, j]) * (pos[i] - pos[j]) / (1 + np.linalg.norm(pos[i] - pos[j]) ** 2)

                delta[1] = gradient
                delta_bar[1] = (1 - get_momentum(iteration)) * delta[1] + get_momentum(iteration) * delta_bar[0]
                delta_prod = delta[1] * delta_bar[0]
                for i in range(n_points):
                    for j in range(2):
                        if delta_prod[i, j] > 0:
                            learning_rate[i, j] += kappa
                        elif delta_prod[i][j] < 0:
                            learning_rate[i, j] *= (1 - phi)

                delta[0] = copy.deepcopy(delta[1])
                delta_bar[0] = copy.deepcopy(delta_bar[1])

                next_pos = pos - learning_rate * gradient + get_momentum(iteration) * momentum
                momentum = next_pos - pos
                pos = next_pos
            self.wait(1 / config.frame_rate)
        self.wait()
        with open("tsneResult.txt", "w") as file:
            for i in range(n_points):
                for j in range(2):
                    file.write(str(pos[i, j]) + " " + str(learning_rate[i, j]) + " ")
                file.write("\n")
# 0 LR 7.5, 1 LR 5, 2-3 LR 10, rest LR 5
# 0-3 perplexity 20, 4-5 perplexity 10, 6-7 perplexity 15, 8 perplexity 25
# letters adaptive learning rate perplexity 25, a-c k=1 phi=0.2, 0.4, 0.6, d-f k=2, g-i k=3

class Distribution(Scene):
    def construct(self):
        axes = Axes(x_range=[-6, 6, 2], y_range=[0, 0.4, 0.2],
                    x_length=7 * 16 / 9, y_length=5,
                    tips=False, axis_config={"stroke_width" : 4}).shift(DOWN)
        self.play(Create(axes))
        self.wait()
        dim_text = VGroup(Text("High Dimensions"), Text("Low Dimensions")).shift(UP * 3)
        dim_text[0].shift(LEFT * 3.5)
        dim_text[1].shift(RIGHT * 3.5)

        normal = axes.plot(lambda x: np.exp(-x**2 / 2) / np.sqrt(2 * np.pi), color=BLUE)
        normal_eq = MathTex(r"y = \frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}", color=BLUE).shift(LEFT * 3.5 + UP * 0.8)
        normal_text = Text("Normal").shift(LEFT * 3.5 + UP * 2)
        self.play(Create(normal))
        self.play(AnimationGroup(Write(normal_eq), Write(normal_text), FadeIn(dim_text[0]), lag_ratio=0.5), run_time=2)
        self.wait()
        cauchy = axes.plot(lambda x: 1 / (np.pi * (1 + x**2)), color=TEAL)
        cauchy_eq = MathTex(r"y = \frac{1}{\pi(1 + x^2)}", color=TEAL).shift(RIGHT * 3.5 + UP * 0.8)
        cauchy_text = Text("Cauchy").shift(RIGHT * 3.5 + UP * 2)
        self.play(Create(cauchy))
        self.play(AnimationGroup(Write(cauchy_eq), Write(cauchy_text), FadeIn(dim_text[1]), lag_ratio=0.5), run_time=2)
        self.wait()
        tails = VGroup(axes.get_area(cauchy, [1.851, 6], color=TEAL, opacity=0.5), axes.get_area(cauchy, [-6, -1.851], color=TEAL, opacity=0.5))
        self.play(FadeIn(tails))
        self.wait(0.5)
        self.play(FadeOut(tails))
        self.wait()

class Nonlinear(Scene):
    def construct(self):
        orange = VGroup()
        blue = VGroup()
        for i in range(100):
            t = 4 * (1 - (i / 100)**2)
            x, y = np.cos(t * np.pi) * t, np.sin(t * np.pi) * t
            x, y = 2.5 * np.cos(i / 50 * np.pi), 2.5 * np.sin(i / 50 * np.pi)
            rx = np.random.normal() / 30
            ry = np.random.normal() / 30
            orange.add(Dot(point=(x + rx, y + ry, 0), color=ORANGE))
            rx = np.random.normal() / 30
            ry = np.random.normal() / 30
            x, y = 3.5 * np.cos(i / 50 * np.pi), 3.5 * np.sin(i / 50 * np.pi)
            blue.add(Dot(point=(-x + rx, -y + ry, 0), color=BLUE))
        self.play(AnimationGroup([FadeIn(orange[i], blue[i]) for i in range(100)], lag_ratio=0.01))

class Crowding(ThreeDScene):
    def construct(self):
        # phi = (1 + np.sqrt(5))
        # self.set_camera_orientation(phi=80 * DEGREES, theta=30 * DEGREES)
        # points = [[phi, 2, 0],
        #           [0, phi, 2],
        #           [2, 0, phi],
        #           [-phi, 2, 0],
        #           [0, -phi, 2],
        #           [2, 0, -phi],
        #           [phi, -2, 0],
        #           [0, phi, -2],
        #           [-2, 0, phi],
        #           [-phi, -2, 0],
        #           [0, -phi, -2],
        #           [-2, 0, -phi]]
        # for i in range(12):
        #     dot = Dot(point=points[i], color=BLUE)
        #     line = Line(start=[0, 0, 0], end=points[i])
        #     self.add_fixed_orientation_mobjects(dot)
        #     self.add(line)
        #     self.add(dot)
        # dot = Dot(point=[0, 0, 0], color=GREEN)
        # self.add_fixed_orientation_mobjects(dot)
        # self.add(dot)
        # self.begin_ambient_camera_rotation(rate=0.15)
        # self.wait(10)
        dots = VGroup()
        for i in range(12):
            dots.add(Dot(point=[2.5 * np.cos(i * np.pi / 6), 2.5 * np.sin(i * np.pi / 6), 0], color=BLUE))
            self.add(dots)
        dots.add(Dot(point=[0, 0, 0], color=GREEN))
        self.wait()
        self.play(AnimationGroup(dots[i].animate.move_to([(3 - i % 2 * 0.7) * np.cos(i * np.pi / 6), (3 - i % 2 * 0.7) * np.sin(i * np.pi / 6), 0]) for i in range(12)))
        self.wait()

class PerplexityDef(Scene):
    def construct(self):
        title = Text("Perplexity").shift(UP * 3)
        line = Line(start=LEFT * 3, end=RIGHT * 3).next_to(title, DOWN)
        eq1 = MathTex(r"\text{Perp}_i", "= 2^{H(i)}").shift(UP * 1.5)
        eq1[1][2:].set_color(YELLOW)
        eq2 = MathTex("H(i) = ", "-\sum_j p_{j|i}\log_2 p_{j|i}")
        eq2[0][:4].set_color(YELLOW)
        eq2[1][3:7].set_color(BLUE)
        eq2[1][11:].set_color(BLUE)
        self.play(Write(title), Create(line))
        self.wait()
        self.play(Write(eq1))
        self.wait()
        self.play(Write(eq2))
        self.wait()

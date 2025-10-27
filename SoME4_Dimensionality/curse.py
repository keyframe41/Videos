from manim import *
import math

from manim import config as global_config
config = global_config.copy()

class GrowDimensions(ThreeDScene):
    def construct(self):
        line = NumberLine(
            x_range=[0, 5, 1],
            length=8,
            include_numbers=True,
        )

        axes = ThreeDAxes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            z_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={
                "numbers_to_include": np.arange(0, 5 + 1, 1),
            },
            tips=False,
        )

        self.play(Write(line))
        self.wait()

        colors = [RED, YELLOW, GREEN, BLUE]
        points = []
        with open("randomPoints.txt", "r") as file:
            for fileLine in file:
                points.append(list(map(float, fileLine.split())))
        path = []
        with open("pathPoints.txt", "r") as file:
            for fileLine in file:
                path.append(list(map(float, fileLine.split())))
        for i in range(100):
            points[i][-1] = int(points[i][-1])

        dots = VGroup(
            *[Dot(point=line.n2p(points[i][0]), color=colors[points[i][-1]]) for i in range(100)]
        )
        dots_3d = VGroup(
            *[Dot3D(point=points[i][:3], color=colors[points[i][-1]]) for i in range(100)]
        )
        dots_3d_path = VGroup(
            *[Dot3D(point=path[i], color=colors[points[i][-1]]) for i in range(100)]
        )
        self.play(LaggedStartMap(FadeIn, dots), run_time=2)
        self.wait()
        self.play(FadeOut(line, run_time=0.5, shift=DOWN * 2),
                  Write(axes.get_axis(0)),
                  Write(axes.get_axis(1)),
                  LaggedStart(
                      (dots[i].animate.move_to(axes.c2p(points[i][0], points[i][1])) for i in range(100)),
                      lag_ratio=0
                  ),
                  run_time=2)
        self.wait()
        dots_3d.move_to(ORIGIN)
        dots_3d_path.move_to(ORIGIN)
        self.play(FadeIn(axes.get_axis(2)),
                  axes.animate.move_to(ORIGIN),
                  ReplacementTransform(dots, dots_3d))
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(8)
        self.play(Transform(dots_3d, dots_3d_path))
        self.wait(8)

class SparseInterpolation(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            tips=False,
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        functions = [
            lambda x : 0.00000331685 * x**9 - 0.00000485103 * x**8 - 0.000311925 * x ** 7 + 0.000408727 * x**6 +
                       0.0116148 * x**5 - 0.0121818 * x**4 - 0.195799 * x**3 + 0.0461754 * x**2 + 1.02387 * x + 2.08092,
            lambda x: -0.0000128493 * x**8 - 0.0000879058 * x**7 + 0.000892066 * x**6 + 0.00684957 * x**5 -
                      0.0205053 * x**4 - 0.164316 * x**3 + 0.07811 * x**2 + 1.01056 * x + 2.07261,
            lambda x: -0.0000706917 * x**7 + 0.00000577984 * x**6 + 0.00592697 * x**5 - 0.00105641 * x**4 -
                      0.152914 * x**3 - 0.0560726 * x**2 + 1.03065* x + 2.10264,
            lambda x: -0.00020655 * x**6 + 0.00197318 * x**5 + 0.0110403 * x**4 - 0.0984541 * x**3 - 0.229883 * x**2 +
                      1.04735 * x + 2.14068,
            lambda x: 0.000281521 * x**5 + 0.0082618 * x**4 - 0.0486985 * x**3 - 0.328817 * x**2 + 1.05262 * x + 2.1621,
            lambda x: 0.00974139 * x**4 - 0.0405697 * x**3 - 0.372779 * x**2 + 1.05846 * x + 2.17205,
            lambda x: 0.0145471 * x**3 - 0.113675 * x**2 - 0.566995 * x + 3.02807
        ]
        points = [
            [2.64508, 2.26308],
            [-1.07205, 1.24617],
            [-4.34282, 1.66068],
            [-5.18847, 0.82088],
            [2.95116, 1.8384],
            [-0.40223, 1.68886],
            [5.53566, -1.12635],
            [4.96902, -0.81139],
            [0.58807, 2.65855],
            [-5.43332, 0.41941]
        ]
        dots = VGroup(
            *[Dot(point=axes.c2p(points[i][0], points[i][1]), radius=0.05, color=RED, stroke_width=5, fill_opacity=0) for i in range(len(points))]
        )
        dots.set_z_index(1)

        title = Text("Underfitting")
        title.to_corner(UP + LEFT, buff=0.5)
        self.play(Write(title), Write(axes), Write(labels))

        reference = axes.plot(lambda x : abs(x) / 4 - x * x / 8 + math.sin(x) + 2, color=YELLOW)
        self.play(Create(reference))

        pointCount = 10
        pointCountText = Tex(f"{pointCount}")
        sampleText = Tex(r"Sample points: ")
        bottomGroup = VGroup(pointCountText, sampleText)
        pointCountText.next_to(sampleText, RIGHT)
        bottomGroup.to_edge(DOWN)

        approximation = axes.plot(functions[0], color=BLUE)
        self.play(FadeIn(dots), FadeIn(bottomGroup), Create(approximation))
        for i in range(1, len(functions)):
            if i < 3:
                self.wait()
            nextApprox = axes.plot(functions[i], color=BLUE)
            pointCount -= 1;
            newPointCount = Tex(f"{pointCount}")
            newPointCount.move_to(pointCountText.get_center())

            self.play(Flash(dots[i - 1], color=WHITE), run_time=0.5)
            self.play(AnimationGroup(FadeOut(dots[i - 1]), Transform(pointCountText, newPointCount), Transform(approximation, nextApprox)), run_time=1, lag_ratio=0.5)
            # self.play(, run_time=(1 if i < 3 else 0.5))

import matplotlib.colors
from fontTools.misc.psCharStrings import read_smallInt2
from manim import *
import matplotlib.pyplot as plt
import random

def get_coords():
    return [[2.830119790593244, -2.8249802318970647, 0], [-1.9921069939800902, -0.30219879802767213, 0], [1.9471370162238593, 1.0539175454444436, 0], [2.881081438471215, -2.2841035407590073, 0], [-0.6859616385584415, 2.9908916065997824, 0], [2.2261415724913167, -2.7372317158298403, 0], [-0.9753220362852772, -1.6303341296923066, 0], [-2.0748088324109752, -2.4361345925696356, 0], [2.327954707224471, 0.30085991991862127, 0], [2.8893907236297167, 0.9741232343472555, 0], [-1.028610922273788, -1.081570406417696, 0], [2.861096245714304, 2.175757583365872, 0], [0.28036494127873235, 0.5892929049896223, 0], [0.5806198289101232, 0.9217422753126439, 0], [1.9375836348610065, -0.49871106381095753, 0], [-0.5889037390534257, -2.668768203372313, 0], [-0.760843397786477, 0.6709920391584427, 0], [-2.391886449772789, -1.707118476366849, 0], [1.700885105777056, 1.705351638929236, 0], [1.248022344099569, 2.647336061769532, 0], [1.92087775702886, -1.0247506349389595, 0], [-2.3136343713058465, -1.0527049796472365, 0], [2.6424673394862843, -1.462678351632588, 0], [-1.651254882899178, 2.519861023322167, 0], [1.2842843396688632, 0.5305678884056944, 0], [-0.4958940766725015, -2.3731828027636537, 0], [-2.7669141929915217, -1.11017193043086, 0], [-2.3164912427346023, -0.5982975623390216, 0], [-2.0554933185143693, -1.2507158292465137, 0], [2.23768879382966, -0.5077250469013013, 0]]

def get_color(x):
    # return BLUE
    cmap = plt.get_cmap('Wistia')
    return matplotlib.colors.to_hex(cmap(x)[:3])


def check_aabb_circle_intersection(rect, circle):
    cx, cy, _ = circle.get_center()
    r = circle.radius

    rx, ry, _ = rect.get_center()
    w = rect.width
    h = rect.height

    # Calculate the rectangle's flat boundaries
    xmin = rx - w / 2
    xmax = rx + w / 2
    ymin = ry - h / 2
    ymax = ry + h / 2

    # Clamp the circle center to the closest point inside/on the rectangle
    closest_x = np.clip(cx, xmin, xmax)
    closest_y = np.clip(cy, ymin, ymax)

    # Calculate squared distance from closest point to the circle center
    dist_x = cx - closest_x
    dist_y = cy - closest_y
    distance_sq = dist_x ** 2 + dist_y ** 2

    return distance_sq <= r ** 2


class Hierarchical(ThreeDScene):
    def construct(self):
        self.camera.focal_distance = 100
        hierarchal = Tex("Hierarchal Methods").to_edge(UP, buff=MED_LARGE_BUFF)
        self.wait()
        self.play(Write(hierarchal), run_time=1.5)

        coords = get_coords()
        points = VGroup([Dot(c, color=BLUE) for c in coords]).shift(DOWN * 0.5).set_z_index(1000)
        # self.wait()
        self.play(AnimationGroup(*[Create(points[i]) for i in range(30)], lag_ratio=0.02))
        self.wait()

        layers = VGroup()
        ppu = config.frame_height / self.camera.pixel_height * 6

        layers.add(Rectangle(height=6 + 9 * ppu, width=6 + 9 * ppu,
                             color=get_color(0.99), stroke_width=3.5).shift(DOWN * 0.5))
        self.play(Create(layers[0]))

        # self.wait(0.5)

        def subdivide(rect):
            d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
            len = rect.width - 1 * ppu
            center = rect.get_center()
            # return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3.5).move_to(
            #     center + d[i][0] * (len) * RIGHT + d[i][1] * (len) * UP) for i in range(4))
            return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3.5).move_to(
                center + d[i][0] * (len) * RIGHT + d[i][1] * (len) * UP) for i in range(4))

        layers.add(subdivide(layers[0]).set_color(get_color(0.8)))
        self.play(AnimationGroup(*[FadeIn(layers[1][i]) for i in range(4)], lag_ratio=0.1), run_time=1)
        # self.wait(0.5)
        layers.add(subdivide(layers[1][0]).set_color(get_color(0.6)))
        layers[2].add(*subdivide(layers[1][1]).set_color(get_color(0.6)))
        layers[2].add(*subdivide(layers[1][2]).set_color(get_color(0.6)))
        layers[2].add(*subdivide(layers[1][3]).set_color(get_color(0.6)))
        self.play(AnimationGroup(*[FadeIn(layers[2][i]) for i in range(len(layers[2]))], lag_ratio=0.05), run_time=1)
        # self.wait(0.5)
        layers.add(subdivide(layers[2][5]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][6]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][7]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][9]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][10]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][12]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][14]).set_color(get_color(0.4)))
        layers[3].add(*subdivide(layers[2][15]).set_color(get_color(0.4)))
        self.play(AnimationGroup(*[FadeIn(layers[3][i]) for i in range(len(layers[3]))], lag_ratio=0.05), run_time=1)
        # self.wait(0.5)
        layers.add(subdivide(layers[3][12]).set_color(get_color(0.2)))
        layers[4].add(*subdivide(layers[3][21]).set_color(get_color(0.2)))
        layers[4].add(*subdivide(layers[3][22]).set_color(get_color(0.2)))
        layers[4].add(*subdivide(layers[3][26]).set_color(get_color(0.2)))
        self.play(AnimationGroup(*[FadeIn(layers[4][i]) for i in range(len(layers[4]))], lag_ratio=0.05), run_time=1)
        # self.wait(0.5)
        layers.add(subdivide(layers[4][12]).set_color(get_color(0)))
        self.play(AnimationGroup(*[FadeIn(layers[5][i]) for i in range(len(layers[5]))], lag_ratio=0.05), run_time=1)
        self.wait()

        uniform_layers = VGroup(Rectangle(height=6 + 9 * ppu, width=6 + 9 * ppu,
                                          color=get_color(0.99), stroke_width=3.5))

        def subdivide2(rect):
            d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
            len = rect.width
            center = rect.get_center()
            return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3.5).move_to(
                center + d[i][0] * len * RIGHT + d[i][1] * len * UP) for i in range(4))

        uniform_layers.add(subdivide2(uniform_layers[0]).set_color(get_color(0.8)))
        uniform_layers.add(subdivide2(uniform_layers[1][0]).set_color(get_color(0.6)))
        uniform_layers[2].add(*subdivide2(uniform_layers[1][1]).set_color(get_color(0.6)))
        uniform_layers[2].add(*subdivide2(uniform_layers[1][2]).set_color(get_color(0.6)))
        uniform_layers[2].add(*subdivide2(uniform_layers[1][3]).set_color(get_color(0.6)))
        uniform_layers.add(subdivide2(uniform_layers[2][5]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][6]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][7]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][9]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][10]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][12]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][14]).set_color(get_color(0.4)))
        uniform_layers[3].add(*subdivide2(uniform_layers[2][15]).set_color(get_color(0.4)))
        uniform_layers.add(subdivide2(uniform_layers[3][12]).set_color(get_color(0.2)))
        uniform_layers[4].add(*subdivide2(uniform_layers[3][21]).set_color(get_color(0.2)))
        uniform_layers[4].add(*subdivide2(uniform_layers[3][22]).set_color(get_color(0.2)))
        uniform_layers[4].add(*subdivide2(uniform_layers[3][26]).set_color(get_color(0.2)))
        uniform_layers.add(subdivide2(uniform_layers[4][12]).set_color(get_color(0)))

        depths = [3, 4, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 4, 5, 2, 3, 3, 2, 3, 4, 3, 2, 3, 5, 3, 4, 4, 4]
        self.begin_ambient_camera_rotation(rate=0.15)
        self.move_camera(phi=80 * DEGREES, zoom=1, run_time=2, added_anims=[
            Unwrite(hierarchal),
            AnimationGroup(*[layers[i].animate.set_z(3.2 - 1.2 * i).shift(UP * 0.5) for i in range(6)]),
            AnimationGroup(
                *[points[i].animate.set_z(3.2 - 1.2 * depths[i]).shift(UP * 0.5) for i in range(len(points))]),
        ])

        quadtree = Text("Quadtree")
        self.add_fixed_in_frame_mobjects(quadtree)
        quadtree.move_to(RIGHT * 4.5 + DOWN * 3).scale(1.5)
        self.play(Write(quadtree))
        self.wait(7)

        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, run_time=1.5, added_anims=[
            Unwrite(quadtree),
            AnimationGroup(*[Transform(layers[i], uniform_layers[i]) for i in range(6)]),
            AnimationGroup(*[points[i].animate.set_z(0) for i in range(len(points))])
        ])
        self.wait()
        rad1 = ValueTracker(0.2)
        center = layers[2][13].get_center()
        circ1 = always_redraw(lambda: Circle(color=BLUE_D, stroke_width=8, radius=rad1.get_value()).move_to(center))

        leaves = VGroup(VGroup(*layers[2][:5], layers[2][8], layers[2][11], layers[2][13]).set_z_index(13),
                        VGroup(*layers[3][:12], *layers[3][13:21], *layers[3][23:26], *layers[3][27:]).set_z_index(12),
                        VGroup(*layers[4][:12], *layers[4][-3:]).set_z_index(11),
                        VGroup(*layers[5]).set_z_index(10))

        def get_colored_boxes(track1, track2, cir, color1, color2):
            res = VGroup()
            r1 = track1.get_value()
            r2 = track2.get_value()
            cx, cy, _ = cir.get_center()

            for layer in leaves:
                res.add(VGroup())
                for box in layer:
                    res[-1].add(box.copy())
                    bx, by, _ = box.get_center()
                    w = box.width

                    xmin = bx - w / 2
                    xmax = bx + w / 2
                    ymin = by - w / 2
                    ymax = by + w / 2

                    closest_x = np.clip(cx, xmin, xmax)
                    closest_y = np.clip(cy, ymin, ymax)

                    dist_x = cx - closest_x
                    dist_y = cy - closest_y
                    distance_sq = dist_x ** 2 + dist_y ** 2

                    if distance_sq <= r1 ** 2:
                        res[-1][-1].set_color(color1).set_z_index(100)
                    elif distance_sq <= r2 ** 2:
                        res[-1][-1].set_color(color2)
            return res

        rad2 = ValueTracker(1)
        colored = always_redraw(lambda: get_colored_boxes(rad1, rad2, circ1, BLUE_D, YELLOW))

        self.play(Create(circ1), FadeIn(colored))
        self.wait()
        self.play(rad1.animate.set_value(1))
        near_label = Text("Near field").rotate(90 * DEGREES).scale(0.45).next_to(circ1, RIGHT)
        self.play(Write(near_label))
        self.wait(0.5)
        circ2 = always_redraw(lambda: Circle(color=ORANGE, stroke_width=8, radius=rad2.get_value()).move_to(center))
        self.play(Create(circ2))
        self.play(rad2.animate.set_value(5))
        far_label = Text("Far field").rotate(90 * DEGREES).next_to(circ2, UP)
        self.play(Write(far_label))
        self.wait()
        colored.clear_updaters()
        self.play(FadeOut(leaves[1][:8]), FadeOut(leaves[1][12:20]), FadeOut(leaves[2][:4]),
                  FadeOut(colored[1][:8]), FadeOut(colored[1][12:20]), FadeOut(colored[2][:4]), FadeOut(layers[3][12]))
        # labels = VGroup([Text(str(i)).scale(0.5).next_to(points[i]) for i in range(len(points))]).set_z_index(10)
        # self.add(labels)
        self.wait()
        groups = [[11, 18], [2, 8, 9], [14, 20, 22, 29], [0, 3, 5]]
        new_centers = [np.sum([points[i].get_center() for i in c], axis=0) / len(c) for c in groups]
        old = VGroup([VGroup(points[i] for i in c) for c in groups])
        com = VGroup([Dot(radius = DEFAULT_DOT_RADIUS * np.sqrt(len(groups[i])), color=BLUE_D).move_to(new_centers[i]) for i in range(4)])
        self.play(AnimationGroup(*[Transform(old[i], com[i]) for i in range(len(old))], lag_ratio=0.2))
        self.wait()
        distance = DoubleArrow(points[10], com[1], buff=0, max_tip_length_to_length_ratio=0.08)
        label_d = MathTex("d").scale(0.9).rotate(90 * DEGREES)
        label_d.next_to(distance, DOWN).shift(RIGHT * 0.5 + UP)
        self.play(GrowArrow(distance), Write(label_d))
        self.wait()
        width = DoubleArrow(layers[2][6].get_edge_center(DOWN), layers[2][6].get_edge_center(UP),
                            buff=0, max_tip_length_to_length_ratio=0.15).shift(RIGHT * 0.3)
        label_s = MathTex("s").scale(0.75).rotate(90 * DEGREES)
        label_s.next_to(width, RIGHT, buff=0.08)
        self.play(GrowArrow(width), Write(label_s))
        self.wait()

        eq = MathTex(r"\frac{s}{d} < \theta").rotate(90 * DEGREES).shift(UP * 5 + RIGHT * 2.5).scale(1.2)
        self.play(Write(eq))

def get_cluster():
    target = [[-0.57545809, -1.36312876,  0.], [-0.45443963, -1.67815458,  0.], [-0.50360931, -1.20775367,  0.], [-0.42446368, -2.52859344,  0.], [ 0.05283695, -1.51515078,  0.], [-0.23091564, -1.10431368,  0.], [ 0.35642743, -2.69963242,  0.], [ 0.45329731, -1.24978515,  0.], [ 0.6181645 , -2.79008803,  0.], [ 0.38134903, -1.89641619,  0.]]
    source = [[[-3.88491506,  2.29041917,  0.], [-4.37772212,  2.34131503,  0.], [-3.61647615,  1.79300171,  0.], [-3.6203192 ,  2.44589871,  0.], [-5.17575448,  1.96072821,  0.], [-4.52635335,  0.94520347,  0.], [-4.91998953,  1.42217343,  0.], [-4.1890457 ,  1.62628632,  0.], [-4.33948592,  2.61054823,  0.], [-3.80621747,  1.80370402,  0.]], [[-0.87011389,  2.55756561,  0.], [-1.34182749,  0.92909255,  0.], [-2.35168208,  2.60344811,  0.], [-2.32129456,  2.34134039,  0.], [-1.84059379,  2.56624222,  0.], [-2.37457029,  1.84566119,  0.], [-1.5435179 ,  1.39033954,  0.], [-2.22505363,  1.99045897,  0.], [-0.62301999,  2.24026105,  0.], [-1.37974609,  2.55770981,  0.]], [[1.74138792, 1.31516505, 0.], [2.23682811, 0.93033792, 0.], [0.69702639, 1.66263801, 0.], [2.08153272, 1.76997398, 0.], [0.83608037, 1.39954494, 0.], [2.10067965, 1.95058721, 0.], [1.84472191, 1.99559254, 0.], [0.75545346, 2.41199086, 0.], [1.51065278, 1.66722835, 0.], [0.8347844 , 2.59506053, 0.]], [[5.28174798, 2.54429541, 0.], [4.53356159, 2.64421726, 0.], [5.3610989 , 1.28738537, 0.], [4.47734115, 1.23456026, 0.], [4.3562247, 1.1928222, 0.       ], [4.63406672, 1.73533376, 0.], [4.51314473, 2.13984424, 0.], [5.2168972 , 2.35814806, 0.], [4.23318547, 2.10890466, 0.], [3.88024762, 1.61609962, 0.]]]
    return target, source

class Cluster2Cluster(Scene):
    def construct(self):
        target_box = Rectangle(width=2, height=2, color=BLUE_D, stroke_width=6).shift(DOWN * 2)
        source_boxes = VGroup([Rectangle(width=2, height=2, color=(YELLOW + ORANGE) / 2, stroke_width=4
                                         ).shift(UP * 1.75 - (4.5 - 3 * i) * RIGHT) for i in range(4)])
        fields = VGroup(Text("Near field").scale(0.75).next_to(target_box, DOWN),
                        Text("Far field").scale(1).next_to(source_boxes, UP))

        target_pos, source_pos = get_cluster()
        targets = VGroup([Dot(color=BLUE).move_to(target_pos[i]) for i in range(10)])
        sources = VGroup([Dot(color=GREEN).move_to(source_pos[i][j]) for j in range(10) for i in range(4)])

        self.wait(0.5)
        self.play(Write(fields), Create(target_box), Create(source_boxes))
        stats = VGroup(Text("4 source boxes"), Text("10 particles/box")).arrange(DOWN).scale(0.75).shift(RIGHT * 4 + DOWN * 2)
        self.play(AnimationGroup(*[Write(targets[i]) for i in range(len(targets))], lag_ratio=0.1),
                  AnimationGroup(*[Write(sources[i]) for i in range(len(sources))], lag_ratio = 0.03),
                  Write(stats))
        self.wait()
        track = ValueTracker(0)
        line = always_redraw(lambda: DoubleArrow(targets[int(track.get_value() / 40)], sources[int(track.get_value() % 40)],
                                          buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.08))
        operations1 = always_redraw(lambda: Text("Naive operations: " + str(int(track.get_value() * 400/399))).scale(0.75).to_corner(DL))
        self.play(Write(operations1), Write(line), run_time=1)
        self.wait(0.5)
        self.play(track.animate.set_value(399), run_time=4)
        operations1.clear_updaters()
        self.wait()
        self.play(operations1.animate.shift(UP * 0.7), Unwrite(line))
        self.wait()
        track.set_value(0)
        operations2 = always_redraw(lambda: Text("Barnes-Hut operations: " + str(int(track.get_value() * 80/79))).scale(0.75).to_corner(DL))
        self.play(Write(operations2))
        self.wait()
        self.play(track.animate.set_value(40), AnimationGroup(*[Indicate(sources[i]) for i in range(40)], lag_ratio=0.05), run_time=2.5)
        line = always_redraw(lambda: DoubleArrow(targets[int(track.get_value() / 4 - 10)],
                                                 source_boxes[int(track.get_value()) % 4].get_edge_center(DOWN),
                                                 buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.08))
        self.play(Write(line))
        self.play(track.animate.set_value(79), run_time=2.5)
        operations2.clear_updaters()
        self.wait()
        self.play(operations2.animate.shift(UP * 0.7), operations1.animate.shift(UP * 0.7), Unwrite(line))
        self.wait()
        counter = ValueTracker(0)
        operations3 = always_redraw(lambda: Text("Ideal operations: " + str(int(counter.get_value()))).scale(0.75).to_corner(DL))
        self.play(Write(operations3))
        self.play(counter.animate.set_value(40), AnimationGroup(*[Indicate(sources[i]) for i in range(40)], lag_ratio=0.05), run_time=2.5)
        line = DoubleArrow(target_box.get_edge_center(UP), source_boxes[0].get_edge_center(DOWN),
                                                 buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.1)
        self.play(Write(line))
        self.wait()
        self.play(Transform(source_boxes[0].copy(), target_box.copy()), run_time=0.75)
        counter.increment_value(1)
        for i in range(3):
            self.play(AnimationGroup([
                Transform(line, DoubleArrow(target_box.get_edge_center(UP), source_boxes[i + 1].get_edge_center(DOWN),
                                            buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.1)),
                Transform(source_boxes[i + 1].copy(), target_box.copy())], lag_ratio=0.5), run_time=1)
            counter.increment_value(1)
        # line2 = always_redraw(lambda: DoubleArrow(DOWN * 4, targets[int((counter.get_value() - 4) * 9/10)],
        #                                           buff=0, color=YELLOW))
        self.play(Unwrite(line),  run_time=1)
        self.play(counter.animate.set_value(54), AnimationGroup(*[Indicate(targets[i]) for i in range(10)], lag_ratio=0.06),
                  rate_func=linear, run_time=1.5)
        # self.play(Unwrite(line2))
        self.wait()



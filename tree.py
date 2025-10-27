from fontTools.varLib.instancer import setMacOverlapFlags
from manim import *
import numpy as np

def Text2(text, kwargs={}):  # Text util
    return Text(text, font="JetBrains Mono", **kwargs)

def pos2d(pos):  # Position conversion util (2 to 3 elements for manim)
    return [pos[0], pos[1], 0]

def offset():
    temp = np.random.rand(2) / 100
    if temp[1] > 0:
        temp[1] *= -1
    return temp

class Tree(MovingCameraScene):

    def construct(self):
        # bg_color = ManimColor((43, 44, 48))
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        def wait(time):
            self.play(Write(Text2("hello").shift(UP * 100)), run_time=time)

        pos_arr = []
        pos_prev_arr = []
        edges = []
        depths = []

        repulsion_const = 50
        attr_const = 80
        spring_const = 30
        spring_length = 1

        node_radius = 0.5

        make_layers = False
        make_directed = False

        def update_positions():
            n_nodes = len(pos_arr)
            forces = np.zeros((n_nodes, 2))
            for i in range(n_nodes): # Repulsion force
                for j in range(n_nodes):
                    if i == j:
                        continue
                    displacement = pos_arr[i] - pos_arr[j]
                    dist = np.linalg.norm(displacement)
                    displacement /= dist
                    forces[i] += (displacement * repulsion_const) / (dist ** 2)
            for edge in edges: # Edge spring force
                displacement = pos_arr[edge[1]] - pos_arr[edge[0]]
                dist = np.linalg.norm(displacement)
                displacement /= dist
                extension = dist - spring_length
                forces[edge[0]] += spring_const * displacement * extension
                forces[edge[1]] -= spring_const * displacement * extension
            if make_layers:
                for i in range(n_nodes): # y correction force
                    displacement = pos_arr[i][1] + 2 * depths[i]
                    dist = np.abs(displacement)
                    displacement = np.sign(displacement)
                    forces[i] += np.array([0, -attr_const]) * displacement * dist ** 2
            for i in range(n_nodes):
                displacement = pos_arr[i] - pos_prev_arr[i]
                if np.linalg.norm(forces[i]) > 100:
                    forces[i] *= 100 / np.linalg.norm(forces[i])
                pos_next = pos_arr[i] + displacement * 0.8 + forces[i] * (1 / config.frame_rate) ** 2
                pos_prev_arr[i] = pos_arr[i]
                pos_arr[i] = pos_next

        def add_node(pos, edge):
            index = len(pos_arr)
            pos_arr.append(pos)
            pos_prev_arr.append(pos)
            circle = Circle(radius=node_radius, stroke_width=8, color=BLUE, fill_color=bg_color, fill_opacity=1)
            num = Text2(str(index)).set_z_index(1).scale(0.8)
            node = VGroup(circle, num).move_to(pos2d(pos))
            for e in edge:
                edges.append([e, index])
            self.play(FadeIn(node), run_time=1 / config.frame_rate)
            self.remove(node)

        def draw_edges():
            lines = VGroup()
            for edge in edges:
                dir = pos_arr[edge[1]] - pos_arr[edge[0]]
                dir /= np.linalg.norm(dir)
                dir *= node_radius
                if make_directed:
                    tip_ratio = 100
                else:
                    tip_ratio = 0
                lines.add(Arrow(start = pos2d(pos_arr[edge[0]] + dir), end = pos2d(pos_arr[edge[1]] - dir),
                                color=LIGHT_GRAY, stroke_width=8, max_stroke_width_to_length_ratio=100,
                                max_tip_length_to_length_ratio=tip_ratio, buff=0).set_z_index(-1))
            return lines

        edge_lines = always_redraw(draw_edges)
        self.add(edge_lines)

        def draw_nodes():
            nodes_ = VGroup()
            for i in range(len(pos_arr)):
                pos = pos_arr[i]
                circle = Circle(radius=0.5, stroke_width=8, color=BLUE, fill_color=bg_color, fill_opacity=1)
                num = Text2(str(i)).set_z_index(1).scale(0.8)
                node = VGroup(circle, num).move_to(pos2d(pos))
                nodes_.add(node)
            update_positions()
            if len(pos_arr) > 0:
                self.camera.auto_zoom(nodes_, margin=2, animate=False)
            return nodes_
        nodes = always_redraw(draw_nodes)
        self.add(nodes)

        add_node(np.array([0, 0]), [])
        depths.append(0)
        temp = [0, 0, 1, 2, 1, 1, 4, 2]
        for i in range(8):
            # x = np.random.randint(i + 1)
            x = temp[i]
            wait(0.2)
            add_node(pos_arr[x] + offset(), [x])
            depths.append(depths[x] + 1)
        print(depths)
        wait(5)
        make_layers = True
        make_directed = True
        wait(15)

class BST(MovingCameraScene):
    def construct(self):
        # bg_color = ManimColor((43, 44, 48))
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        def wait(time):
            self.play(Write(Text2("hello").shift(UP * 100)), run_time=time)

        pos_arr = []
        pos_prev_arr = []
        children = []
        root = []
        depths = []
        labels = []
        colors = []

        repulsion_const = 20
        attr_const = 50
        spring_const = 5
        spring_length = 1.25
        binary_force_const = 100

        node_radius = 0.5

        make_layers = True
        make_directed = True
        make_binary = True
        slowmo = False

        def update_positions():
            n_nodes = len(pos_arr)
            forces = np.zeros((n_nodes, 2))
            for i in range(n_nodes): # Repulsion force
                for j in range(n_nodes):
                    if i == j:
                        continue
                    displacement = pos_arr[i] - pos_arr[j]
                    dist = np.linalg.norm(displacement)
                    displacement /= dist
                    forces[i] += (displacement * repulsion_const) / (dist ** 2)
                for child in children[i]: # Edge spring force
                    if child == -1:
                        continue
                    displacement = pos_arr[child] - pos_arr[i]
                    dist = np.linalg.norm(displacement)
                    displacement /= dist
                    extension = dist - spring_length
                    forces[i] += spring_const * displacement * extension
                    forces[child] -= spring_const * displacement * extension
            if make_layers:
                for i in range(n_nodes): # y correction force
                    displacement = pos_arr[i][1] + 2 * depths[i] - 2
                    dist = np.abs(displacement)
                    displacement = np.sign(displacement)
                    forces[i] += np.array([0, -attr_const]) * displacement * dist ** 2
            if make_binary:
                for i in range(n_nodes): # Spring direction force
                    for j in range(2):
                        child = children[i][j]
                        if child == -1:
                            continue
                        displacement = pos_arr[child] - pos_arr[i]
                        dist = np.linalg.norm(displacement)
                        displacement /= dist
                        if j == 0:
                            dist = -0.5 - displacement[0]
                            forces[child] += np.array([np.sign(dist) * dist ** 2, 0]) * binary_force_const
                        else:
                            dist = 0.5 - displacement[0]
                            forces[child] += np.array([np.sign(dist) * dist ** 2, 0]) * binary_force_const

            delta_time = 1 / config.frame_rate
            if slowmo:
                delta_time /= 3
            for i in range(n_nodes):
                displacement = pos_arr[i] - pos_prev_arr[i]
                if np.linalg.norm(forces[i]) > 500:
                    forces[i] *= 500 / np.linalg.norm(forces[i])
                pos_next = pos_arr[i] + displacement * 0.8 + forces[i] * delta_time ** 2
                pos_prev_arr[i] = pos_arr[i]
                pos_arr[i] = pos_next
            if n_nodes:
                pos_arr[0] = np.array([0, 2])

        def draw_edges():
            lines = VGroup()
            for i in range(len(pos_arr)):
                for child in children[i]:
                    if child == -1:
                        continue
                    dir = pos_arr[child] - pos_arr[i]
                    dir /= np.linalg.norm(dir)
                    dir *= node_radius
                    if make_directed:
                        tip_ratio = 100
                    else:
                        tip_ratio = 0
                    lines.add(Arrow(start = pos2d(pos_arr[i] + dir), end = pos2d(pos_arr[child] - dir),
                                    color=LIGHT_GRAY, stroke_width=8, max_stroke_width_to_length_ratio=100,
                                    max_tip_length_to_length_ratio=tip_ratio, buff=0).set_z_index(-1))
            return lines

        edge_lines = always_redraw(draw_edges)
        self.add(edge_lines)

        def draw_nodes():
            nodes_ = VGroup()
            for i in range(len(pos_arr)):
                pos = pos_arr[i]
                circle = Circle(radius=0.5, stroke_width=8, color=colors[i], fill_color=bg_color, fill_opacity=1)
                num = Text2(str(labels[i])).set_z_index(1).scale(0.8)
                node = VGroup(circle, num).move_to(pos2d(pos))
                nodes_.add(node)
            update_positions()
            if len(pos_arr):
                self.camera.auto_zoom([order, nodes_], margin=2, animate=False)
            return nodes_
        nodes = always_redraw(draw_nodes)
        self.add(nodes)

        def add_node(pos, label, col, parent, dir):
            index = len(pos_arr)
            pos_arr.append(pos)
            pos_prev_arr.append(pos)
            colors.append(col)
            labels.append(label)
            circle = Circle(radius=node_radius, stroke_width=8, color=col, fill_color=bg_color, fill_opacity=1)
            num = Text2(str(label)).set_z_index(1).scale(0.8)
            node = VGroup(circle, num).move_to(pos2d(pos))

            if parent >= 0:
                children[parent][dir] = index
            root.append(parent)

            children.append([-1, -1])
            self.play(FadeIn(node), run_time=1 / config.frame_rate)
            self.remove(node)

        def update_depths(): # Basic BFS
            nonlocal depths
            depths = [0] * len(pos_arr)
            temp = [0]
            while len(temp):
                cur = temp[0]
                temp.pop(0)
                if children[cur][0] != -1:
                    temp.append(children[cur][0])
                    depths[children[cur][0]] = depths[cur] + 1
                if children[cur][1] != -1:
                    temp.append(children[cur][1])
                    depths[children[cur][1]] = depths[cur] + 1

        def left_rotation(node_id):
            parent = root[node_id]
            grandparent = root[parent]
            lc = children[node_id][0]

            children[node_id][0] = parent
            root[parent] = node_id

            children[parent][1] = lc
            if lc != -1:
                root[lc] = parent

            dir = 1 if children[grandparent][1] == parent else 0
            children[grandparent][dir] = node_id
            root[node_id] = grandparent
            update_depths()

        def right_rotation(node_id):
            parent = root[node_id]
            grandparent = root[parent]
            rc = children[node_id][1]

            children[node_id][1] = parent
            root[parent] = node_id

            children[parent][0] = rc
            if rc != -1:
                root[rc] = parent

            dir = 1 if children[grandparent][1] == parent else 0
            children[grandparent][dir] = node_id
            root[node_id] = grandparent
            update_depths()

        # depths.append(0)
        # add_node(np.array([0, 0]), 0, BLUE, -1, 0)
        # wait(1)
        # temp = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 6]
        # temp1 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        # for i in range(11):
        #     # x = np.random.randint(i + 1)
        #     x = temp[i]
        #     wait(0.05)
        #     depths.append(depths[x] + 1)
        #     add_node(pos_arr[x] + offset(), i, BLUE, x, temp1[i])
        # wait(10)
        # make_layers = False
        # make_binary = False
        # for i in range(len(pos_arr)):
        #     children[i] = [-1, -1]
        # for i in range(35):
        #     pos_prev_arr[7] = [pos_arr[7][0] - 0.006 * i, pos_arr[7][1] - 0.006 * i]
        #     pos_prev_arr[5] = [pos_arr[5][0] + 0.006 * i, pos_arr[5][1] + 0.003 * i]
        #     wait(1 / config.frame_rate)
        # wait(0.5)
        # make_binary = True
        # children[7] = [3, 9]
        # children[3] = [1, 5]
        # children[1] = [0, 2]
        # children[5] = [4, 6]
        # children[9] = [8, 10]
        # children[10] = [-1, 11]
        # depths = [3, 2, 3, 1, 3, 2, 3, 0, 2, 1, 2, 3]
        # wait(1)
        # make_layers = True
        # wait(10)


        # self.wait()

        def get_highlight(node_id):
            return Circle(radius=node_radius, stroke_width=9, color=YELLOW).move_to(pos2d(pos_arr[node_id]))

        balance_factors = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        def draw_bfs():
            bf_text = VGroup()
            for i in range(len(pos_arr)):
                bf_text.add(Text2(str(balance_factors[i])).scale(0.6).next_to(nodes[i], LEFT))
            return bf_text
        balance = always_redraw(draw_bfs)
        self.add(balance)

        order = VGroup()
        # nums_order = [5, 3, 1, 8, 10, 0, 9, 11, 2, 7, 6, 4]
        nums_order = [4, 2, 6, 3, 5, 1, 7, 8, 9]
        # for i in range(8):
        #     order.add(Text2(str(nums_order[i])))
        # order.arrange(RIGHT, buff=MED_LARGE_BUFF).shift(UP * 3.5)
        # self.add(order)
        # underline = Rectangle(color=YELLOW, height = 0.1, width = 0.8, fill_color=YELLOW, fill_opacity=1).next_to(order[0], DOWN)
        # self.add(underline)

        depths.append(0)
        add_node(np.array([0, 2]), nums_order[0], RED, -1, 0)
        wait(1)

        for i in range(1, 9):
            # self.play(underline.animate.next_to(order[i], DOWN), run_time=0.5)
            cur = 0
            dir = 0
            # ring = always_redraw(lambda: get_highlight(cur))
            # self.add(ring)
            # self.play(FadeIn(ring), run_time=0.5)
            # wait(0.5)

            while True:
                if nums_order[i] < labels[cur]:
                    if children[cur][0] != -1:
                        cur = children[cur][0]
                    else:
                        dir = 0
                        break
                else:
                    if children[cur][1] != -1:
                        cur = children[cur][1]
                    else:
                        dir = 1
                        break
                # nxt = always_redraw(lambda: get_highlight(cur))
                # self.add(nxt)
                # self.remove(ring)
                # wait(0.5)

                # self.play(FadeIn(nxt), FadeOut(ring), run_time=0.5)
                # ring = nxt

            if i < 7:
                wait(1)
            else:
                wait(5)
            depths.append(depths[cur] + 1)
            if i > 1:
                colors[i - 1] = BLUE
            add_node(pos_arr[cur] + offset(), nums_order[i], GREEN, cur, dir)
            if i == 1:
                balance_factors[0] = -1
            if i == 2:
                balance_factors[0] = 0
            if i == 3:
                balance_factors[0] = -1
                balance_factors[1] = 1
            if i == 4:
                balance_factors[0] = 0
                balance_factors[2] = -1
            if i == 5:
                balance_factors[1] = 0
            if i == 6:
                balance_factors[2] = 0
            if i == 7:
                balance_factors[0] = 1
                balance_factors[2] = 1
                balance_factors[6] = 1
            if i == 8:
                balance_factors[0] = 2
                balance_factors[2] = 2
                balance_factors[6] = 2
                balance_factors[7] = 1
            # wait(0.5)
            # self.play(FadeOut(ring), run_time=0.5)
        wait(5)
        left_rotation(7)
        balance_factors[0] = 1
        balance_factors[2] = 1
        balance_factors[6] = 0
        balance_factors[7] = 0
        wait(15)

        # children[1] = [3, -1]
        # children[2] = [5, -1]
        # children[7] = [-1, 10]
        # wait(1)
        # children[1] = [3, 7]
        # children[2] = [5, 8]
        # children[7] = [2, 10]
        # update_depths()
        # slowmo = True
        # wait(6)
        # slowmo = False
        # wait(8)
        # children[1] = [3, -1]
        # children[2] = [5, -1]
        # children[7] = [-1, 10]
        # wait(1)
        # children[1] = [3, 2]
        # children[2] = [5, 7]
        # children[7] = [8, 10]
        # update_depths()
        # slowmo = True
        # wait(6)
        # slowmo = False
        # wait(8)

# .0 with highlight
# .1 no highlight
# .2 relaxed spring 5

class Rotation(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        tree_t1 = Polygon([-4.1, -2, 0], [-2.8, 1, 0], [-1.5, -2, 0], stroke_width=10, stroke_color=GOLD_B, fill_color=GRAY, fill_opacity=1)
        node_t1 = Circle(radius=0.4, stroke_width=8, color=GOLD_B, fill_color=bg_color, fill_opacity=1).move_to([-2.8, 1, 0])
        text_t1 = Text2("1").move_to(node_t1).scale(0.8)
        t1 = VGroup(tree_t1, node_t1, text_t1)
        self.add(t1)
        tree_t2 = Polygon([-0.5, -3.5, 0], [0.4, -0.3, 0], [1.3, -3.5, 0], stroke_width=10, stroke_color=GREEN_B, fill_color=GRAY, fill_opacity=1)
        node_t2 = Circle(radius=0.4, stroke_width=8, color=GREEN_B, fill_color=bg_color, fill_opacity=1).move_to([0.4, -0.3, 0])
        text_t2 = Text2("2").move_to(node_t2).scale(0.8)
        t2 = VGroup(tree_t2, node_t2, text_t2)
        self.add(t2)
        tree_t3 = Polygon([1.9, -3.5, 0], [2.8, -0.3, 0], [3.7, -3.5, 0], stroke_width=10, stroke_color=RED_B, fill_color=GRAY, fill_opacity=1)
        node_t3 = Circle(radius=0.4, stroke_width=8, color=RED_B, fill_color=bg_color, fill_opacity=1).move_to([2.8, -0.3, 0])
        text_t3 = Text2("3").move_to(node_t3).scale(0.8)
        t3 = VGroup(tree_t3, node_t3, text_t3)
        self.add(t3)

        circle = Circle(radius=0.4, stroke_width=8, color=BLUE_B, fill_color=bg_color, fill_opacity=1)
        num = Text2("Y").set_z_index(1).scale(0.8)
        node_y = VGroup(circle, num).move_to([1.6, 1, 0])
        self.add(node_y)
        edge_yl = Line(start=node_y.get_center(), end=node_t2.get_center(), stroke_width=8, color=GRAY_B).set_z_index(-1)
        edge_yr = Line(start=node_y.get_center(), end=node_t3.get_center(), stroke_width=8, color=GRAY_B).set_z_index(-1)
        self.add(edge_yl, edge_yr)

        circle = Circle(radius=0.4, stroke_width=8, color=BLUE_B, fill_color=bg_color, fill_opacity=1)
        num = Text2("X").set_z_index(1).scale(0.8)
        node_x = VGroup(circle, num).move_to([-0.6, 2.5, 0])
        self.add(node_x)
        edge_xl = Line(start=node_x.get_center(), end=node_t1.get_center(), stroke_width=8, color=GRAY_B).set_z_index(-1)
        edge_xr = Line(start=node_x.get_center(), end=node_y.get_center(), stroke_width=8, color=GRAY_B).set_z_index(-1)
        self.add(edge_xl, edge_xr)
        self.wait()

        nxt_yl = Line(start=[1.6, 2.5, 0], end=[-0.6, 1, 0], stroke_width=8, color=GRAY_B).set_z_index(-1)
        nxt_xr = Line(start=[-0.6, 1, 0], end=node_t2.get_center(), stroke_width=8, color=GRAY_B).set_z_index(-1)
        self.play(node_y.animate.shift(UP * 1.5), t3.animate.shift(UP * 1.5), edge_yr.animate.shift(UP * 1.5),
                  node_x.animate.shift(DOWN * 1.5), t1.animate.shift(DOWN * 1.5), edge_xl.animate.shift(DOWN * 1.5),
                  Transform(edge_yl, nxt_yl), Transform(edge_xr, nxt_xr))
        self.wait()

class Rebalance(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        node_kwargs = {'radius' : 0.5, 'stroke_width' : 8, 'fill_color' : bg_color, 'fill_opacity' : 1}
        tree_kwargs = {'stroke_width' : 10, 'fill_color' : GRAY, 'fill_opacity' : 1}
        edge_kwargs = {'stroke_width' : 8, 'color' : GRAY_B}

        def general_idea():
            tree_t1 = Polygon([-3, -1.5, 0], [-2, 1, 0], [1, 3, 0], [4, 1, 0], [5, -1.5, 0], stroke_width=10, stroke_color=BLUE_B,
                              fill_color=GRAY, fill_opacity=1)
            node_t1 = Circle(radius=0.4, stroke_width=8, color=BLUE_B, fill_color=bg_color, fill_opacity=1).move_to(
                [1, 3, 0])
            num = Text2("X").set_z_index(1).scale(0.8).move_to(node_t1)
            t1 = VGroup(tree_t1, node_t1, num).set_z_index(2)
            self.add(t1)
            t2 = Polygon([1.5, -3.5, 0], [2.25, 0, 0], [3, -3.5, 0], stroke_width=10, stroke_color=GREEN_B,
                              fill_color=GRAY, fill_opacity=1).set_z_index(1)
            self.add(t2)
            self.wait()

            line = DashedLine(LEFT * 5, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(DOWN * 1.5)
            dashed = VGroup(line, line.copy().shift(DOWN), line.copy().shift(DOWN * 2))
            heights = VGroup(Text2("h"), Text2("h+1"), Text2("h+2"))
            for i in range(3):
                heights[i].scale(0.75).next_to(dashed[i], LEFT)
            self.play(AnimationGroup(*[Write(dashed[i]) for i in range(3)], lag_ratio=0.25),
                      AnimationGroup(*[Write(heights[i]) for i in range(3)], lag_ratio=0.25))
            self.wait()

            t3 = t2.copy().shift(UP * 2 + LEFT * 2)
            self.play(t2.animate.shift(UP), t3.animate.shift(DOWN))
            self.wait()

        def show_cases():
            xnode = Circle(color=BLUE_B, **node_kwargs).move_to([-1, 3, 0])
            xnum = Text2("X").move_to(xnode)
            node_x = VGroup(xnode, xnum).set_z_index(3)

            ynode = Circle(color=BLUE_B, **node_kwargs).move_to([2.5, 2, 0])
            ynum = Text2("Y").move_to(ynode)
            node_y = VGroup(ynode, ynum).set_z_index(3)

            tree_t1 = Polygon([-4, -1.5, 0], [-3, 2, 0], [-2, -1.5, 0], stroke_color=GREEN_B, **tree_kwargs)
            node_1 = Circle(color=GREEN_B, **node_kwargs).move_to([-3, 2, 0])
            num = Text2("1").move_to(node_1)
            t1 = VGroup(tree_t1, node_1, num).set_z_index(2)

            tree_t2 = Polygram([[-0.5, -2.5, 0], [0.5, 1, 0], [1.5, -2.5, 0]], stroke_color=RED_B, **tree_kwargs)
            node_2 = Circle(color=RED_B, **node_kwargs).move_to([0.5, 1, 0])
            num = Text2("2").move_to(node_2)
            t2 = VGroup(tree_t2, node_2, num).set_z_index(2)

            tree_t2 = Polygram([[-0.5, -3.5, 0], [0.5, 1, 0], [1.5, -3.5, 0]], stroke_color=RED_B, **tree_kwargs)
            t2_tall = VGroup(tree_t2, node_2.copy(), num.copy()).set_z_index(2)

            tree_t3 = Polygon([3.5, -3.5, 0], [4.5, 1, 0], [5.5, -3.5, 0], stroke_color=GOLD_B, **tree_kwargs)
            node_3 = Circle(color=GOLD_B, **node_kwargs).move_to([4.5, 1, 0])
            num = Text2("3").move_to(node_3)
            t3 = VGroup(tree_t3, node_3, num).set_z_index(2)

            tree_t3_tall = Polygon([3.5, -2.5, 0], [4.5, 1, 0], [5.5, -2.5, 0], stroke_color=GOLD_B, **tree_kwargs)
            t3_tall = VGroup(tree_t3_tall, node_3.copy(), num.copy()).set_z_index(2)

            tree_t4 = Polygon([3.5, -2.5, 0], [4.5, 1, 0], [5.5, -2.5, 0], stroke_color=GOLD_B, **tree_kwargs)
            num = Text2("4").move_to(node_3)
            t4 = VGroup(tree_t4, node_3.copy(), num.copy()).set_z_index(2)

            edge_x1 = Line(start=node_x.get_center(), end=node_1.get_center(),  **edge_kwargs)
            edge_x2 = Line(start=node_x.get_center(), end=node_y.get_center(),  **edge_kwargs)
            edge_x22 = edge_x2.copy()
            edge_y1 = Line(start=node_y.get_center(), end=node_2.get_center(),  **edge_kwargs)
            edge_y11 = edge_y1.copy()
            edge_y2 = Line(start=node_y.get_center(), end=node_3.get_center(),  **edge_kwargs)

            line = DashedLine(LEFT * 5, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(DOWN * 1.5)
            dashed = VGroup(line, line.copy().shift(DOWN), line.copy().shift(DOWN * 2))
            heights = VGroup(Text2("h"), Text2("h+1"), Text2("h+2"))
            for i in range(3):
                heights[i].scale(0.75).next_to(dashed[i], LEFT)

            bf = VGroup()
            bf.add(Text2("2").scale(0.6).next_to(node_x, LEFT))
            bff = bf.copy()
            bf.add(Text2("1").scale(0.6).next_to(node_y, RIGHT))
            bff.add(Text2("-1").scale(0.6).next_to(node_y, RIGHT))

            bf2 = VGroup()
            bf2.add(Text2("0").scale(0.6).next_to(node_x, LEFT))
            bf2.add(Text2("0").scale(0.6).next_to(node_y, RIGHT))
            bf2[0].shift(DOWN)
            bf2[1].shift(UP)

            self.play(AnimationGroup(
                AnimationGroup(Create(xnode), Create(ynode), Write(xnum), Write(ynum), run_time=1),
                FadeIn(t1, t2, t3, shift=DOWN),
                AnimationGroup(*[Write(dashed[i]) for i in range(3)], lag_ratio=0.25, run_time=1),
                AnimationGroup(*[Write(heights[i]) for i in range(3)], lag_ratio=0.25, run_time=1),
                AnimationGroup(Create(edge_x1), Create(edge_x22), Create(edge_y11), Create(edge_y2), Write(bf)), lag_ratio=0.25, run_time=2.5),)
            self.wait()

            edge_x2_nxt = Line(start=[-1, 2, 0], end=node_2.get_center(),  **edge_kwargs)
            edge_y1_nxt = Line(start=[2.5, 3, 0], end=[-1, 2, 0],  **edge_kwargs)
            self.play(node_x.animate.shift(DOWN), t1.animate.shift(DOWN), edge_x1.animate.shift(DOWN),
                      node_y.animate.shift(UP), t3.animate.shift(UP), edge_y2.animate.shift(UP),
                      ReplacementTransform(edge_x22, edge_x2_nxt), ReplacementTransform(edge_y11, edge_y1_nxt),
                      ReplacementTransform(bf, bf2))
            self.wait()
            self.play(ReplacementTransform(bf2, bff),
                      node_x.animate.shift(UP), t1.animate.shift(UP), edge_x1.animate.shift(UP),
                      node_y.animate.shift(DOWN), edge_y2.animate.shift(DOWN),
                      ReplacementTransform(t2, t2_tall), ReplacementTransform(t3, t3_tall),
                      ReplacementTransform(edge_x2_nxt, edge_x2), ReplacementTransform(edge_y1_nxt, edge_y1))
            self.wait()

            tree_t2 = Polygon([-1.5, -3.5, 0], [-0.5, 0, 0], [0.5, -3.5, 0], stroke_color=RED_B, **tree_kwargs)
            node_2 = Circle(color=RED_B, **node_kwargs).move_to([-0.5, 0, 0])
            num = Text2("2").move_to(node_2)
            t2 = VGroup(tree_t2, node_2, num).set_z_index(3)

            tree_t3 = Polygon([1, -3.5, 0], [2, 0, 0], [3, -3.5, 0], stroke_color=RED_B, **tree_kwargs)
            node_3 = Circle(color=RED_B, **node_kwargs).move_to([2, 0, 0])
            num = Text2("3").move_to(node_3)
            t3 = VGroup(tree_t3, node_3, num).set_z_index(3)

            znode = Circle(color=BLUE_B, **node_kwargs).move_to([0.75, 1, 0])
            znum = Text2("Z").move_to(znode)
            node_z = VGroup(znode, znum).set_z_index(3)

            edge_z1 = Line(start=node_z.get_center(), end=node_2.get_center(),  **edge_kwargs)
            edge_z2 = Line(start=node_z.get_center(), end=node_3.get_center(),  **edge_kwargs)

            t2_tall_2 = t2_tall.copy()
            self.play(ReplacementTransform(t2_tall, t2), ReplacementTransform(t2_tall_2, t3), FadeIn(node_z),
                      Create(edge_z1), Create(edge_z2), ReplacementTransform(t3_tall, t4), FadeOut(bff),
                      node_x.animate.set_x(-1.75), node_y.animate.set_x(3.25),
                      Transform(edge_x1, Line(start=[-1.75, 3, 0], end=[-3, 2, 0], **edge_kwargs)),
                      Transform(edge_x2, Line(start=[-1.75, 3, 0], end=[3.25, 2, 0], **edge_kwargs)),
                      Transform(edge_y1, Line(start=[3.25, 2, 0], end=node_z.get_center(), **edge_kwargs)),
                      Transform(edge_y2, Line(start=[3.25, 2, 0], end=t4[1].get_center(), **edge_kwargs)),)
            self.wait()

            self.play(node_z.animate.shift(UP), edge_z1.animate.shift(UP), t2.animate.shift(UP),
                      node_y.animate.shift(DOWN), edge_y2.animate.shift(DOWN), t4.animate.shift(DOWN),
                      Transform(edge_x2, Line(start=node_x.get_center(), end=[0.75, 2, 0], **edge_kwargs)),
                      Transform(edge_y1, Line(start=[3.25, 1, 0], end=node_3.get_center(), **edge_kwargs)),
                      Transform(edge_z2, Line(start=[0.75, 2, 0], end=[3.25, 1, 0], **edge_kwargs)),)
            self.wait()

            self.play(node_z.animate.shift(UP), node_y.animate.shift(UP), t3.animate.shift(UP), t4.animate.shift(UP),
                      edge_z2.animate.shift(UP), edge_y1.animate.shift(UP), edge_y2.animate.shift(UP),
                      node_x.animate.shift(DOWN), t1.animate.shift(DOWN), edge_x1.animate.shift(DOWN),
                      Transform(edge_x2, Line(start=[-1.75, 2, 0], end=node_2.get_center(), **edge_kwargs)),
                      Transform(edge_z1, Line(start=[0.75, 3, 0], end=[-1.75, 2, 0], **edge_kwargs)))
            self.wait()

        show_cases()

square_kwargs = {'side_length' : 1, 'stroke_width' : 8}
edge_kwargs = {'stroke_width' : 8, 'buff' : 0, 'color' : GRAY_B,
               'max_tip_length_to_length_ratio' : 100, 'max_stroke_width_to_length_ratio' : 100}
node_edge_kwargs = {'stroke_width': 8, 'buff': 0.5, 'color': GRAY_A,
               'max_tip_length_to_length_ratio': 100, 'max_stroke_width_to_length_ratio': 100}
circle_kwargs = {'stroke_width' : 8, 'fill_opacity' : 1, 'radius' : 0.5}
node_kwargs = {'stroke_width' : 8, 'color' : BLUE, 'radius' : 0.5}
root_kwargs = {'stroke_width' : 8, 'color' : GREEN, 'radius' : 0.5}

def midpoint(sq, edge):
    verts = sq.get_vertices()
    return (verts[edge] + verts[(edge + 1) % 4]) / 2 # anticlockwise from top

def corner(sq, vert):
    return sq.get_vertices()[vert] # Anticlockwise from top-right

def node_edge(n1, n2):
    return Arrow(start=n1[0].get_center(), end=n2[0].get_center(), **node_edge_kwargs)

def null(node, dir):
    if dir == 0:
        return Circle(radius=0.2, color=BLACK, stroke_color=GRAY, fill_opacity=1, stroke_width=4).move_to(node).shift((LEFT + DOWN * np.sqrt(3)) / 3.5)
    else:
        return Circle(radius=0.2, color=BLACK, stroke_color=GRAY, fill_opacity=1, stroke_width=4).move_to(node).shift((RIGHT + DOWN * np.sqrt(3)) / 3.5)

class AVL(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color
        self.wait()

        nodes = VGroup()
        bfs = []
        def get_balance(target):
            nums = VGroup()
            for i in range(len(target)):
                nums.add(Text2(str(bfs[i])).scale(0.5).next_to(target[i], LEFT))
            return nums

        node = Circle(**node_kwargs).shift(UP * 3)
        text = Text2("8").move_to(node)
        node_8 = VGroup(node, text).set_z_index(2)
        bfs.append(0)
        nodes.add(node_8)
        factors = get_balance(nodes)
        self.play(Write(node_8), Write(factors))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(UP + LEFT * 1.5)
        text = Text2("4").move_to(node)
        node_4 = VGroup(node, text).set_z_index(2)
        bfs.append(0)
        bfs[0] = -1
        edge_1 = node_edge(node_8, node_4)
        nodes.add(node_4)
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_4), Write(edge_1), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN)
        text = Text2("7").move_to(node)
        node_7 = VGroup(node, text).set_z_index(2)
        edge_2 = node_edge(node_4, node_7)
        nodes.add(node_7)
        bfs.append(0)
        bfs[0] = -2
        bfs[1] = 1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_7), Write(edge_2), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        nxt = nodes.copy()
        nxt[1] = node_4.copy().shift(LEFT * 1.5 + DOWN * 2)
        nxt[2] = node_7.copy().shift(LEFT * 1.5 + UP * 2)
        edge_2_nxt = node_edge(nxt[2], nxt[1])
        bfs[2] = -1
        bfs[1] = 0
        factors_nxt = get_balance(nxt)
        self.play(Transform(node_4, nxt[1]), Transform(node_7, nxt[2]), Transform(edge_2, edge_2_nxt), Transform(factors, factors_nxt))
        self.wait(0.5)
        nxt = nodes.copy()
        nxt[1] = node_4.copy().shift(RIGHT * 1.5 + UP * 2)
        nxt[2] = node_7.copy().shift(RIGHT * 1.5 + UP * 2)
        nxt[0] = node_8.copy().shift(RIGHT * 1.5 + DOWN * 2)
        edge_1_nxt = node_edge(nxt[2], nxt[0])
        edge_2_nxt = node_edge(nxt[2], nxt[1])
        bfs[0] = 0
        bfs[1] = 0
        bfs[2] = 0
        factors_nxt = get_balance(nxt)
        self.play(Transform(node_4, nxt[1]), Transform(node_7, nxt[2]), Transform(node_8, nxt[0]),
                  Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(factors, factors_nxt))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN + LEFT * 3)
        text = Text2("2").move_to(node)
        node_2 = VGroup(node, text).set_z_index(2)
        edge_3 = node_edge(node_4, node_2)
        nodes.add(node_2)
        bfs.append(0)
        bfs[2] = -1
        bfs[1] = -1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_2), Write(edge_3), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN)
        text = Text2("5").move_to(node)
        node_5 = VGroup(node, text).set_z_index(2)
        edge_4 = node_edge(node_4, node_5)
        nodes.add(node_5)
        bfs.append(0)
        bfs[1] = 0
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_5), Write(edge_4), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN + RIGHT * 3)
        text = Text2("10").move_to(node)
        node_10 = VGroup(node, text).set_z_index(2)
        edge_5 = node_edge(node_8, node_10)
        nodes.add(node_10)
        bfs.append(0)
        bfs[2] = 0
        bfs[0] = 1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_10), Write(edge_5), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 4.5)
        text = Text2("1").move_to(node)
        node_1 = VGroup(node, text).set_z_index(2)
        edge_6 = node_edge(node_2, node_1)
        nodes.add(node_1)
        bfs.append(0)
        bfs[2] = -1
        bfs[1] = -1
        bfs[3] = -1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_1), Write(edge_6), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 1.5)
        text = Text2("3").move_to(node)
        node_3 = VGroup(node, text).set_z_index(2)
        edge_7 = node_edge(node_2, node_3)
        nodes.add(node_3)
        bfs.append(0)
        bfs[3] = 0
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_3), Write(edge_7), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN * 3 + RIGHT * 4.5)
        text = Text2("14").move_to(node)
        node_14 = VGroup(node, text).set_z_index(2)
        edge_8 = node_edge(node_10, node_14)
        nodes.add(node_14)
        bfs.append(0)
        bfs[2] = 0
        bfs[0] = 2
        bfs[5] = 1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_14), Write(edge_8), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait(0.5)
        nxt = nodes.copy()
        nxt[1] = node_4.copy().shift(LEFT)
        nxt[3] = node_2.copy().shift(LEFT)
        nxt[4] = node_5.copy().shift(LEFT)
        nxt[6] = node_1.copy().shift(LEFT * 0.5)
        nxt[7] = node_3.copy().shift(LEFT * 1.5)
        nxt[0] = node_8.copy().shift(DOWN * 2 + LEFT * 0.5)
        nxt[5] = node_10.copy().shift(LEFT * 0.5 + UP * 2)
        nxt[8] = node_14.copy().shift(LEFT * 0.5 + UP * 2)
        edge_1_nxt = node_edge(node_7, nxt[5])
        edge_2_nxt = node_edge(node_7, nxt[1])
        edge_3_nxt = node_edge(nxt[1], nxt[3])
        edge_4_nxt = node_edge(nxt[1], nxt[4])
        edge_5_nxt = node_edge(nxt[5], nxt[0])
        edge_6_nxt = node_edge(nxt[3], nxt[6])
        edge_7_nxt = node_edge(nxt[3], nxt[7])
        edge_8_nxt = node_edge(nxt[5], nxt[8])
        bfs[2] = -1
        bfs[5] = 0
        bfs[0] = 0
        factors_nxt = get_balance(nxt)
        self.play(Transform(node_4, nxt[1]), Transform(node_5, nxt[4]), Transform(node_2, nxt[3]), Transform(node_3, nxt[7]),
                  Transform(node_8, nxt[0]), Transform(node_10, nxt[5]), Transform(node_14, nxt[8]), Transform(node_1, nxt[6]),
                  Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_4, edge_4_nxt),
                  Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt), Transform(edge_8, edge_8_nxt),
                  Transform(factors, factors_nxt))
        self.wait(0.5)

        node = Circle(**node_kwargs).shift(DOWN * 3)
        text = Text2("6").move_to(node)
        node_6 = VGroup(node, text).set_z_index(2)
        edge_9 = node_edge(node_5, node_6)
        nodes.add(node_6)
        bfs.append(0)
        bfs[1] = 0
        bfs[4] = 1
        factors_nxt = get_balance(nodes)
        factors.add(factors_nxt[-1])
        self.play(Write(node_6), Write(edge_9), Transform(factors[:-1], factors_nxt[:-1]), Write(factors[-1]))
        self.wait()
        bfs.pop(0)
        nodes.remove(node_8)
        self.play(node_7[1].animate.move_to(node_8), node_8[1].animate.move_to(node_7))
        num7 = node_7[1]
        node_7.remove(num7)
        self.add(num7)
        self.wait(0.5)
        bfs[5] = 1
        self.play(Unwrite(node_8[0]), Unwrite(num7), Unwrite(edge_5),
                  Transform(factors[5], Text2('1').scale(0.5).next_to(node_10, LEFT)), Unwrite(factors[0]))
        self.wait()

class BTree(MovingCameraScene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        def show_nodes():
            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)
            self.add(node_a)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN + LEFT * 2)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN + RIGHT * 2)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text)

            edge_p = Arrow(start=midpoint(node_a[0], 2), end=midpoint(node_p[0], 0), **edge_kwargs)
            edge_q = Arrow(start=midpoint(node_a[0], 2), end=midpoint(node_q[0], 0), **edge_kwargs)

            ineq1 = Text2("p < a < q").shift(DOWN * 3)

            self.wait()
            self.play(AnimationGroup(AnimationGroup(Write(edge_p), Write(node_p)),
                                     AnimationGroup(Write(edge_q), Write(node_q)), Write(ineq1), lag_ratio=0.25))
            self.wait()

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + RIGHT * 0.5)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN + RIGHT * 3.5)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text)

            edge_r = Arrow(start=corner(node_b[0], 3), end=midpoint(node_r[0], 0), **edge_kwargs)

            ineq2 = Text2("p < a < q < b < r").shift(DOWN * 3)

            self.play(AnimationGroup(
                AnimationGroup(node_q.animate.shift(LEFT * 2), Transform(edge_q, Arrow(start=[0, 1.5, 0], end=[0, -0.5, 0], **edge_kwargs)),
                               FadeIn(node_r, shift=LEFT * 2)),
                AnimationGroup(node_a.animate.shift(LEFT * 0.5), FadeIn(node_b, shift=RIGHT * 0.5),
                               node_p.animate.shift(LEFT * 1.5), Transform(edge_p, Arrow(start=[-1, 1.5, 0], end=[-3.5, -0.5, 0], **edge_kwargs))),
                Write(edge_r),
                AnimationGroup(ReplacementTransform(ineq1[:5], ineq2[:5]), Write(ineq2[5:])), lag_ratio=0.25))
            self.wait()

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + RIGHT)
            text = Text2("c").move_to(node)
            node_c = VGroup(node, text).set_z_index(2)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN + RIGHT * 4.5)
            text = Text2("s").move_to(node)
            node_s = VGroup(node, text)

            edge_s = Arrow(start=[1.5, 1.5, 0], end=[4, -0.5, 0], **edge_kwargs)

            ineq3 = Text2("p < a < q < b < r < c < s").shift(DOWN * 3)

            self.play(AnimationGroup(
                AnimationGroup(node_r.animate.shift(LEFT * 2), Transform(edge_r, Arrow(start=[0.5, 1.5, 0], end=[1.5, -0.5, 0], **edge_kwargs)),
                               FadeIn(node_s, shift=LEFT * 2)),
                AnimationGroup(node_a.animate.shift(LEFT * 0.5), node_b.animate.shift(LEFT * 0.5), FadeIn(node_c, shift=RIGHT * 0.5),
                               node_q.animate.shift(LEFT * 1.5), Transform(edge_q, Arrow(start=[-0.5, 1.5, 0], end=[-1.5, -0.5, 0], **edge_kwargs))),
                AnimationGroup(node_p.animate.shift(LEFT), Transform(edge_p, Arrow(start=[-1.5, 1.5, 0], end=[-4, -0.5, 0], **edge_kwargs)),
                               Write(edge_s)),
                AnimationGroup(ReplacementTransform(ineq2[:9], ineq3[:9]), Write(ineq3[9:])), lag_ratio=0.25))
            self.wait()

        def tree3():
            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("8").move_to(node)
            node_8 = VGroup(node, text).set_z_index(2)

            order = VGroup()
            nums = [8, 4, 7, 2, 5, 10, 1, 3, 14, 6]
            for i in range(len(nums)):
                order.add(Text2(str(nums[i])).scale(1.25))
            order.arrange(RIGHT, buff=MED_LARGE_BUFF).shift(UP * 3.5)
            underline = Rectangle(color=YELLOW, height=0.1, width=0.8, fill_color=YELLOW, fill_opacity=1).next_to(order[0], DOWN)

            self.wait(0.5)
            self.play(FadeIn(order, underline))
            self.wait(0.5)
            self.play(Write(node_8))
            self.wait(0.5)

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + LEFT * 0.5)
            text = Text2("4").move_to(node)
            node_4 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_4), node_8.animate.shift(RIGHT * 0.5), underline.animate.next_to(order[1], DOWN))
            self.wait(0.5)

            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("7").move_to(node)
            node_7 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_7), node_8.animate.shift(RIGHT * 0.5), node_4.animate.shift(LEFT * 0.5), underline.animate.next_to(order[2], DOWN))

            edge_1 = Arrow(start=corner(node_7[0], 2), end=[-2, 0, 0], **edge_kwargs)
            edge_2 = Arrow(start=corner(node_7[0], 3), end=[2, 0, 0], **edge_kwargs)
            self.play(AnimationGroup(AnimationGroup(node_4[1].animate.shift(DOWN * 2.5 + LEFT), node_4[0].animate.shift(DOWN * 2.5 + LEFT).set_color(BLUE),
                      node_8[1].animate.shift(DOWN * 2.5 + RIGHT), node_8[0].animate.shift(DOWN * 2.5 + RIGHT).set_color(BLUE)),
                      AnimationGroup(Write(edge_1), Write(edge_2)), lag_ratio=0.5))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 0.5 + LEFT * 2.5)
            text = Text2("2").move_to(node)
            node_2 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_2), node_4.animate.shift(RIGHT * 0.5), underline.animate.next_to(order[3], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 0.5 + LEFT)
            text = Text2("5").move_to(node)
            node_5 = VGroup(node, text).set_z_index(2)
            edge_3 = Arrow(start=midpoint(node_7[0], 2), end=ORIGIN, **edge_kwargs)

            self.play(Write(node_5), node_2.animate.shift(LEFT * 0.5), node_4.animate.shift(LEFT * 0.5), underline.animate.next_to(order[4], DOWN))
            self.play(node_5.animate.shift(RIGHT), node_7.animate.shift(RIGHT * 0.5), node_8.animate.shift(RIGHT),
                      node_4[1].animate.shift(UP * 2.5 + RIGHT * 1.5), node_4[0].animate.shift(UP * 2.5 + RIGHT * 1.5).set_color(RED),
                      Transform(edge_1, Arrow(start=[-1, 1.5, 0], end=[-3, 0, 0], **edge_kwargs)),
                      Transform(edge_2, Arrow(start=[1, 1.5, 0], end=[3, 0, 0], **edge_kwargs)), Write(edge_3))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).move_to(node_8).shift(RIGHT * 0.5)
            text = Text2("10").move_to(node)
            node_10 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_10), node_8.animate.shift(LEFT * 0.5), underline.animate.next_to(order[5], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).move_to(node_2).shift(LEFT * 0.5)
            text = Text2("1").move_to(node)
            node_1 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_1), node_2.animate.shift(RIGHT * 0.5), underline.animate.next_to(order[6], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).move_to(node_2).shift(RIGHT * 0.5)
            text = Text2("3").move_to(node)
            node_3 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_3), node_1.animate.shift(LEFT * 0.5), node_2.animate.shift(LEFT * 0.5), underline.animate.next_to(order[7], DOWN))
            self.play(node_1.animate.shift(RIGHT * 0.5), node_3.animate.shift(LEFT * 0.5), node_4.animate.shift(RIGHT * 0.5), node_7.animate.shift(RIGHT * 0.5),
                      node_2[1].animate.shift(RIGHT * 2 + UP * 2.5), node_2[0].animate.shift(RIGHT * 2 + UP * 2.5).set_color(RED))

            edge_4 = Arrow(start=corner(node_4[0], 2), end=[-3, 0, 0], **edge_kwargs)
            edge_5 = Arrow(start=corner(node_4[0], 3), end=[3, 0, 0], **edge_kwargs)
            self.play(AnimationGroup(
                AnimationGroup(node_2[1].animate.shift(LEFT * 2 + DOWN * 2.5), node_2[0].animate.shift(LEFT * 2 + DOWN * 2.5).set_color(BLUE),
                      node_3[1].animate.shift(RIGHT + DOWN * 2.5), node_3[0].animate.shift(RIGHT + DOWN * 2.5).set_color(GREEN),
                      node_1[1].animate.shift(LEFT + DOWN * 2.5), node_1[0].animate.shift(LEFT + DOWN * 2.5).set_color(GREEN),
                      Transform(edge_1, Arrow(start=[-2.5, -1, 0], end=[-1.5, -2.5, 0], **edge_kwargs)),
                      Transform(edge_1.copy(), Arrow(start=[-3.5, -1, 0], end=[-4.5, -2.5, 0], **edge_kwargs)),
                      node_7[1].animate.shift(RIGHT * 2 + DOWN * 2.5), node_7[0].animate.shift(RIGHT * 2 + DOWN * 2.5).set_color(BLUE),
                      node_8[1].animate.shift(RIGHT * 1.5 + DOWN * 2.5), node_8[0].animate.shift(RIGHT * 1.5 + DOWN * 2.5).set_color(GREEN),
                      node_10[1].animate.shift(RIGHT * 1.5 + DOWN * 2.5), node_10[0].animate.shift(RIGHT * 1.5 + DOWN * 2.5).set_color(GREEN),
                      node_5[1].animate.shift(RIGHT * 1.5 + DOWN * 2.5), node_5[0].animate.shift(RIGHT * 1.5 + DOWN * 2.5).set_color(GREEN),
                      Transform(edge_3, Arrow(start=[2.5, -1, 0], end=[1.5, -2.5, 0], **edge_kwargs)),
                      Transform(edge_2, Arrow(start=[3.5, -1, 0], end=[4.5, -2.5, 0], **edge_kwargs))),
                AnimationGroup(Write(edge_4), Write(edge_5)), lag_ratio=0.5))
            self.wait(0.5)

            node = Square(color=GREEN, **square_kwargs).move_to(node_10).shift(RIGHT * 0.5)
            text = Text2("14").move_to(node)
            node_14 = VGroup(node, text).set_z_index(2)
            edge_6 = Arrow(start=midpoint(node_7[0], 2), end=[3, -2.5, 0], **edge_kwargs)

            self.play(Write(node_14), node_8.animate.shift(LEFT * 0.5), node_10.animate.shift(LEFT * 0.5), underline.animate.next_to(order[8], DOWN))
            self.play(node_7.animate.shift(LEFT * 0.5), node_5.animate.shift(LEFT), node_8.animate.shift(LEFT * 0.5),
                      node_10[1].animate.shift(LEFT + UP * 2.5), node_10[0].animate.shift(LEFT + UP * 2.5).set_color(BLUE),
                      ReplacementTransform(edge_2, Arrow(start=[4, -1, 0], end=[5.5, -2.5, 0], **edge_kwargs)),
                      ReplacementTransform(edge_3, Arrow(start=[2, -1, 0], end=[0.5, -2.5, 0], **edge_kwargs)),
                      ReplacementTransform(edge_2.copy(), edge_6))
            self.wait(0.5)

            node = Square(color=GREEN, **square_kwargs).move_to(node_5).shift(RIGHT * 0.5)
            text = Text2("6").move_to(node)
            node_6 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_6), node_5.animate.shift(LEFT * 0.5), underline.animate.next_to(order[9], DOWN))
            self.wait()

        def tree4():
            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("8").move_to(node)
            node_8 = VGroup(node, text).set_z_index(2)

            order = VGroup()
            nums = [8, 4, 7, 2, 5, 10, 1, 3, 14, 6]
            for i in range(len(nums)):
                order.add(Text2(str(nums[i])).scale(1.25))
            order.arrange(RIGHT, buff=MED_LARGE_BUFF).shift(UP * 3.5)
            underline = Rectangle(color=YELLOW, height=0.1, width=0.8, fill_color=YELLOW, fill_opacity=1).next_to(
                order[0], DOWN)

            self.wait(0.5)
            self.play(FadeIn(order, underline))
            self.wait(0.5)
            self.play(Write(node_8))
            self.wait(0.5)

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + LEFT * 0.5)
            text = Text2("4").move_to(node)
            node_4 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_4), node_8.animate.shift(RIGHT * 0.5), underline.animate.next_to(order[1], DOWN))
            self.wait(0.5)

            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("7").move_to(node)
            node_7 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_7), node_8.animate.shift(RIGHT * 0.5), node_4.animate.shift(LEFT * 0.5), underline.animate.next_to(order[2], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + LEFT * 3.5)
            text = Text2("2").move_to(node)
            node_2 = VGroup(node, text).set_z_index(2)
            edge_1 = Arrow(start=corner(node_7[0], 2), end=[-3, -1, 0], **edge_kwargs)
            edge_2 = Arrow(start=corner(node_7[0], 3), end=[3, -1, 0], **edge_kwargs)
            self.play(AnimationGroup(
                AnimationGroup(node_4[1].animate.shift(DOWN * 3.5 + LEFT * 2), node_4[0].animate.shift(DOWN * 3.5 + LEFT * 2).set_color(BLUE),
                               node_8[1].animate.shift(DOWN * 3.5 + RIGHT * 2), node_8[0].animate.shift(DOWN * 3.5 + RIGHT * 2).set_color(BLUE),
                               underline.animate.next_to(order[3], DOWN)),
                AnimationGroup(Write(edge_1), Write(edge_2)), lag_ratio=0.5))
            self.play(Write(node_2), node_4.animate.shift(RIGHT * 0.5))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + LEFT * 2)
            text = Text2("5").move_to(node)
            node_5 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_5), node_2.animate.shift(LEFT * 0.5), node_4.animate.shift(LEFT * 0.5), underline.animate.next_to(order[4], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + RIGHT * 3.5)
            text = Text2("10").move_to(node)
            node_10 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_10), node_8.animate.shift(LEFT * 0.5), underline.animate.next_to(order[5], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + LEFT * 3.5)
            text = Text2("1").move_to(node)
            node_1 = VGroup(node, text).set_z_index(2)
            edge_3 = Arrow(start=midpoint(node_7[0], 2), end=[0, -1, 0], **edge_kwargs)
            self.play(node_7.animate.shift(RIGHT * 0.5), node_5.animate.shift(RIGHT * 2), underline.animate.next_to(order[6], DOWN),
                      node_2.animate.shift(RIGHT), Write(edge_3),
                      node_4[0].animate.shift(UP * 3.5 + RIGHT * 2.5).set_color(RED), node_4[1].animate.shift(UP * 3.5 + RIGHT * 2.5),
                      Transform(edge_1, Arrow(start=[-1, 1.5, 0], end=[-3, -1, 0], **edge_kwargs)),
                      Transform(edge_2, Arrow(start=[1, 1.5, 0], end=[3, -1, 0], **edge_kwargs)))
            self.play(Write(node_1), node_2.animate.shift(RIGHT * 0.5))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + LEFT * 2)
            text = Text2("3").move_to(node)
            node_3 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_3), node_2.animate.shift(LEFT * 0.5), node_1.animate.shift(LEFT * 0.5), underline.animate.next_to(order[7], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + RIGHT * 4)
            text = Text2("14").move_to(node)
            node_14 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_14), node_10.animate.shift(LEFT * 0.5), node_8.animate.shift(LEFT * 0.5), underline.animate.next_to(order[8], DOWN))
            self.wait(0.5)

            node = Square(color=BLUE, **square_kwargs).shift(DOWN * 1.5 + RIGHT * 0.5)
            text = Text2("6").move_to(node)
            node_6 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_6), node_5.animate.shift(LEFT * 0.5), underline.animate.next_to(order[9], DOWN))
            self.wait()

        def make_color2():
            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)
            self.add(node_a)

            node = Square(color=BLUE, **square_kwargs).shift(LEFT * 1.5)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(RIGHT * 1.5)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text)

            edge_p = Arrow(start=midpoint(node_a[0], 2), end=midpoint(node_p[0], 0), **edge_kwargs)
            edge_q = Arrow(start=midpoint(node_a[0], 2), end=midpoint(node_q[0], 0), **edge_kwargs)

            self.add(node_a, node_p, node_q, edge_p, edge_q)
            self.wait()

            node1 = Circle(color=RED, fill_color=BLACK, **circle_kwargs).shift(UP * 2).set_z_index(2)
            node2 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(LEFT * 1.5).set_z_index(2)
            node3 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(RIGHT * 1.5).set_z_index(2)

            self.play(Transform(node_a[0], node1), Transform(node_p[0], node2), Transform(node_q[0], node3),
                      Transform(edge_p, node_edge(node1, node2)), Transform(edge_q, node_edge(node1, node3)))
            self.wait()

        def make_color3():
            node = Square(color=RED, **square_kwargs).shift(UP * 2 + LEFT * 0.5)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + RIGHT * 0.5)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Square(color=BLUE, **square_kwargs).shift(LEFT * 3)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(RIGHT * 3)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text)

            edge_p = Arrow(start=corner(node_a[0], 2), end=corner(node_p[0], 0), **edge_kwargs)
            edge_q = Arrow(start=corner(node_b[0], 2), end=midpoint(node_q[0], 0), **edge_kwargs)
            edge_r = Arrow(start=corner(node_b[0], 3), end=corner(node_r[0], 1), **edge_kwargs)

            self.add(node_a, node_b, node_p, node_q, node_r, edge_p, edge_q, edge_r)
            self.wait()

            node1 = Circle(color=RED, fill_color=BLACK, **circle_kwargs).shift(UP * 2).set_z_index(2)
            node2 = Circle(color=RED, fill_color=PURE_RED, **circle_kwargs).shift(LEFT * 2).set_z_index(2)
            node3 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(RIGHT * 2).set_z_index(2)
            node4 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2 + LEFT * 4).set_z_index(2)
            node5 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2).set_z_index(2)


            self.play(Transform(node_a[0], node2), node_a[1].animate.move_to(node2), Transform(node_b[0], node1), node_b[1].animate.move_to(node1),
                      Transform(node_p[0], node4), node_p[1].animate.move_to(node4), Transform(node_q[0], node5), node_q[1].animate.move_to(node5),
                      Transform(node_r[0], node3), node_r[1].animate.move_to(node3),
                      Transform(edge_p, node_edge(node2, node4)), Transform(edge_q, node_edge(node2, node5)),
                      Transform(edge_r, node_edge(node1, node3)), Write(node_edge(node1, node2)))
            self.wait()

        def make_color4():
            node = Square(color=RED, **square_kwargs).shift(UP * 2 + LEFT)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Square(color=RED, **square_kwargs).shift(UP * 2)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Square(color=RED, **square_kwargs).shift(UP * 2 + RIGHT)
            text = Text2("c").move_to(node)
            node_c = VGroup(node, text).set_z_index(2)

            node = Square(color=BLUE, **square_kwargs).shift(LEFT * 3 + DOWN)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(LEFT + DOWN)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(RIGHT + DOWN)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text)

            node = Square(color=BLUE, **square_kwargs).shift(RIGHT * 3 + DOWN)
            text = Text2("s").move_to(node)
            node_s = VGroup(node, text)

            edge_p = Arrow(start=corner(node_a[0], 2), end=corner(node_p[0], 0), **edge_kwargs)
            edge_q = Arrow(start=corner(node_b[0], 2), end=midpoint(node_q[0], 0), **edge_kwargs)
            edge_r = Arrow(start=corner(node_b[0], 3), end=midpoint(node_r[0], 0), **edge_kwargs)
            edge_s = Arrow(start=corner(node_c[0], 3), end=corner(node_s[0], 1), **edge_kwargs)

            self.add(node_a, node_b, node_c, node_p, node_q, node_r, node_s, edge_p, edge_q, edge_r, edge_s)
            self.wait()

            node1 = Circle(color=RED, fill_color=BLACK, **circle_kwargs).shift(UP * 2).set_z_index(2)
            node2 = Circle(color=RED, fill_color=PURE_RED, **circle_kwargs).shift(LEFT * 2).set_z_index(2)
            node3 = Circle(color=RED, fill_color=PURE_RED, **circle_kwargs).shift(RIGHT * 2).set_z_index(2)
            node4 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2 + LEFT * 3).set_z_index(2)
            node5 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2 + LEFT).set_z_index(2)
            node6 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2 + RIGHT).set_z_index(2)
            node7 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(DOWN * 2 + RIGHT * 3).set_z_index(2)


            self.play(Transform(node_a[0], node2), node_a[1].animate.move_to(node2), Transform(node_b[0], node1), node_b[1].animate.move_to(node1),
                      Transform(node_c[0], node3), node_c[1].animate.move_to(node3),
                      Transform(node_p[0], node4), node_p[1].animate.move_to(node4), Transform(node_q[0], node5), node_q[1].animate.move_to(node5),
                      Transform(node_r[0], node6), node_r[1].animate.move_to(node6), Transform(node_s[0], node7), node_s[1].animate.move_to(node7),
                      Transform(edge_p, node_edge(node2, node4)), Transform(edge_q, node_edge(node2, node5)),
                      Transform(edge_r, node_edge(node3, node6)), Transform(edge_s, node_edge(node3, node7)),
                      Write(node_edge(node1, node2)), Write(node_edge(node1, node3)))
            self.wait()

        def redblack():
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 3)
            text = Text2("8").move_to(node)
            node_8 = VGroup(node, text).set_z_index(2)

            nulls = VGroup()
            nulls.add(null(node_8, 0), null(node_8, 1))

            self.wait(0.5)
            self.play(AnimationGroup(Write(node_8), AnimationGroup(FadeIn(nulls[0]), FadeIn(nulls[1])), lag_ratio=0.3))
            self.play(Transform(node_8[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3)), run_time=0.75)
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP + LEFT * 1.5)
            text = Text2("4").move_to(node)
            node_4 = VGroup(node, text).set_z_index(2)
            edge_1 = node_edge(node_8, node_4).set_z_index(1)

            nulls.add(null(node_4, 0), null(node_4, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_4), ReplacementTransform(nulls[0], edge_1)),
                                     AnimationGroup(FadeIn(nulls[2]), FadeIn(nulls[3])), lag_ratio=0.3))
            nulls.remove(nulls[0])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN)
            text = Text2("7").move_to(node)
            node_7 = VGroup(node, text).set_z_index(2)
            edge_2 = node_edge(node_4, node_7).set_z_index(1)
            nulls.add(null(node_7, 0), null(node_7, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_7), ReplacementTransform(nulls[2], edge_2)),
                      AnimationGroup(FadeIn(nulls[3]), FadeIn(nulls[4])), lag_ratio=0.3))
            nulls.remove(nulls[2])
            self.wait(0.5)
            node_4_nxt = node_4.copy().shift(DOWN * 2 + LEFT * 1.5)
            node_7_nxt = node_7.copy().shift(UP * 2 + LEFT * 1.5)
            nulls.add(null(node_4_nxt, 1))
            edge_3 = node_edge(node_7_nxt, node_4_nxt).set_z_index(1)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt),
                      Transform(nulls[1], null(node_4_nxt, 0)), Transform(nulls[3], null(node_7_nxt, 1)),
                      ReplacementTransform(nulls[2], edge_3), ReplacementTransform(edge_2, nulls[4]))
            nulls.remove(nulls[2])

            node_8_nxt = node_8.copy().shift(DOWN * 2 + RIGHT * 1.5)
            node_8_nxt[0] = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP + RIGHT * 1.5)

            node_7_nxt = node_7.copy().shift(UP * 2 + RIGHT * 1.5)
            node_7_nxt[0] = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3)

            edge_2 = node_edge(node_8, node_8_nxt).set_z_index(1)

            nulls.add(null(node_8_nxt, 0))
            self.play(Transform(node_8, node_8_nxt), Transform(node_7, node_7_nxt), ReplacementTransform(nulls[2], edge_2),
                      node_4.animate.shift(RIGHT * 1.5 + UP * 2), nulls[1].animate.shift(RIGHT * 1.5 + UP * 2), nulls[3].animate.shift(RIGHT * 1.5 + UP * 2),
                      edge_3.animate.shift(RIGHT * 1.5 + UP * 2), nulls[0].animate.shift(RIGHT * 1.5 + DOWN * 2), ReplacementTransform(edge_1, nulls[4]))
            nulls.remove(nulls[2])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN + LEFT * 3)
            text = Text2("2").move_to(node)
            node_2 = VGroup(node, text).set_z_index(2)
            edge_1 = node_edge(node_4, node_2).set_z_index(1)
            nulls.add(null(node_2, 0), null(node_2, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_2), ReplacementTransform(nulls[1], edge_1)),
                                     AnimationGroup(FadeIn(nulls[4]), FadeIn(nulls[5])), lag_ratio=0.3))
            nulls.remove(nulls[1])
            self.play(Transform(node_4[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP + LEFT * 1.5)),
                      Transform(node_8[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP + RIGHT * 1.5)),
                      Transform(node_7[0], Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 3)), run_time=0.75)
            self.play(Transform(node_7[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3)), run_time=0.75)
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN)
            text = Text2("5").move_to(node)
            node_5 = VGroup(node, text).set_z_index(2)
            edge_4 = node_edge(node_4, node_5).set_z_index(1)
            nulls.add(null(node_5, 0), null(node_5, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_5), ReplacementTransform(nulls[1], edge_4)),
                                     AnimationGroup(FadeIn(nulls[5]), FadeIn(nulls[6])), lag_ratio=0.3))
            nulls.remove(nulls[1])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN + RIGHT * 3)
            text = Text2("10").move_to(node)
            node_10 = VGroup(node, text).set_z_index(2)
            edge_5 = node_edge(node_8, node_10).set_z_index(1)
            nulls.add(null(node_10, 0), null(node_10, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_10), ReplacementTransform(nulls[0], edge_5)),
                                     AnimationGroup(FadeIn(nulls[6]), FadeIn(nulls[7])), lag_ratio=0.3))
            nulls.remove(nulls[0])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN * 3 + LEFT * 4.5)
            text = Text2("1").move_to(node)
            node_1 = VGroup(node, text).set_z_index(2)
            edge_6 = node_edge(node_2, node_1).set_z_index(1)
            nulls.add(null(node_1, 0), null(node_1, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_1), ReplacementTransform(nulls[1], edge_6)),
                                     AnimationGroup(FadeIn(nulls[7]), FadeIn(nulls[8])), lag_ratio=0.3))
            nulls.remove(nulls[1])
            self.play(Transform(node_2[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(node_2)),
                      Transform(node_5[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(node_5)),
                      Transform(node_4[0], Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(node_4)), run_time=0.75)
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN * 3 + LEFT * 1.5)
            text = Text2("3").move_to(node)
            node_3 = VGroup(node, text).set_z_index(2)
            edge_7 = node_edge(node_2, node_3).set_z_index(1)
            nulls.add(null(node_3, 0), null(node_3, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_3), ReplacementTransform(nulls[1], edge_7)),
                                     AnimationGroup(FadeIn(nulls[8]), FadeIn(nulls[9])), lag_ratio=0.3))
            nulls.remove(nulls[1])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN * 3 + RIGHT * 4.5)
            text = Text2("14").move_to(node)
            node_14 = VGroup(node, text).set_z_index(2)
            edge_8 = node_edge(node_10, node_14).set_z_index(1)
            nulls.add(null(node_14, 0), null(node_14, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_14), ReplacementTransform(nulls[4], edge_8)),
                                     AnimationGroup(FadeIn(nulls[9]), FadeIn(nulls[10])), lag_ratio=0.3))
            nulls.remove(nulls[4])
            node_4_nxt = node_4.copy().shift(LEFT * 0.6)
            node_5_nxt = node_5.copy().shift(LEFT * 0.9)
            node_2_nxt = node_2.copy().shift(LEFT * 0.3)
            node_3_nxt = node_3.copy().shift(LEFT * 0.6)
            edge_3_nxt = node_edge(node_7, node_4_nxt).set_z_index(1)
            edge_1_nxt = node_edge(node_4_nxt, node_2_nxt).set_z_index(1)
            edge_4_nxt = node_edge(node_4_nxt, node_5_nxt).set_z_index(1)
            edge_6_nxt = node_edge(node_2_nxt, node_1).set_z_index(1)
            edge_7_nxt = node_edge(node_2_nxt, node_3_nxt).set_z_index(1)

            node_10_nxt = node_10.copy().move_to(node_8).shift(RIGHT * 0.6)
            node_10_nxt[0] = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(node_10_nxt)
            node_8_nxt = node_8.copy().shift(DOWN * 2 + LEFT * 0.6)
            node_8_nxt[0] = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(node_8_nxt)
            node_14_nxt = node_14.copy().shift(UP * 2 + LEFT * 1.2)
            node_14_nxt[0] = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(node_14_nxt)
            edge_2_nxt = node_edge(node_7, node_10_nxt).set_z_index(1)
            edge_5_nxt = node_edge(node_10_nxt, node_8_nxt).set_z_index(1)
            edge_8_nxt = node_edge(node_10_nxt, node_14_nxt).set_z_index(1)
            nulls.add(null(node_8_nxt, 1))

            self.play(Transform(node_4, node_4_nxt), Transform(node_5, node_5_nxt), Transform(node_2, node_2_nxt),
                      Transform(node_3, node_3_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_1, edge_1_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt),
                      nulls[1:3].animate.shift(LEFT * 0.9), nulls[6:8].animate.shift(LEFT * 0.6),
                      Transform(node_10, node_10_nxt), Transform(node_8, node_8_nxt), Transform(node_14, node_14_nxt),
                      Transform(edge_2, edge_2_nxt), ReplacementTransform(nulls[3], edge_5_nxt), Transform(edge_8, edge_8_nxt),
                      ReplacementTransform(edge_5, nulls[10]), nulls[8:10].animate.shift(UP * 2 + LEFT * 1.2),
                      nulls[0].animate.shift(DOWN * 2 + LEFT * 0.6))
            nulls.remove(nulls[3])
            self.wait()

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(DOWN * 3 + RIGHT * 0.3)
            text = Text2("6").move_to(node)
            node_6 = VGroup(node, text).set_z_index(2)
            edge_9 = node_edge(node_5, node_6)
            nulls.add(null(node_6, 0), null(node_6, 1))
            self.play(AnimationGroup(AnimationGroup(Write(node_6), ReplacementTransform(nulls[2], edge_9)),
                                     AnimationGroup(FadeIn(nulls[10]), FadeIn(nulls[11])), lag_ratio=0.3))
            self.wait()
            nodes = VGroup(node_1[0], node_2[0], node_3[0], node_4[0], node_5[0], node_6[0], node_7[0], node_8[0], node_10[0], node_14[0])
            nums = VGroup(node_1[1], node_2[1], node_3[1], node_4[1], node_5[1], node_6[1], node_7[1], node_8[1], node_10[1], node_14[1])
            edges = VGroup(edge_1, edge_2, edge_3, edge_4, edge_5_nxt, edge_6, edge_7, edge_8, edge_9)
            self.play(Unwrite(nodes), Unwrite(edges), Unwrite(nulls), Unwrite(nums))
            self.wait(0.5)

        redblack()

class RBTree(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        def case1(): # root
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 2)
            text = Text2("X").move_to(node)
            node_x = VGroup(node, text).set_z_index(2)
            self.wait(0.5)
            self.play(Write(node_x))
            self.wait(0.5)
            self.play(Transform(node_x[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 2)))
            self.wait()

        def case2(): # Black parent
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(LEFT + DOWN * 2)
            text = Text2("X").move_to(node)
            node_x = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 0.5 + RIGHT)
            text = Text2("Y").move_to(node)
            node_y = VGroup(node, text).set_z_index(2)

            edge = node_edge(node_y, node_x)
            n3 = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 4 + RIGHT)
            edge2 = node_edge(n3, node_y)
            self.wait(0.5)
            self.play(Write(node_y), Write(edge2))
            self.wait(0.5)
            self.play(Write(node_x), Write(edge)) # Black parent
            self.wait()

        def case3(): # Red uncle
            n = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 6)
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(LEFT * 4 + DOWN * 2)
            text = Text2("X").move_to(node)
            node_x = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 0.5 + LEFT * 2)
            text = Text2("Y").move_to(node)
            node_y = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3)
            text = Text2("Z").move_to(node)
            node_z = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 0.5 + RIGHT * 2)
            text = Text2("W").move_to(node)
            node_w = VGroup(node, text).set_z_index(2)

            edge1 = node_edge(node_z, node_y)
            edge2 = node_edge(node_z, node_w)
            edge3 = node_edge(node_y, node_x)
            top = node_edge(n, node_z)
            self.wait()
            self.play(AnimationGroup(Write(top), Write(node_z), Create(edge1), Write(node_y), Create(edge2), Write(node_w), lag_ratio=0.15))
            self.wait(0.5)
            self.play(Create(edge3), Write(node_x))
            self.wait()
            self.play(Transform(node_y[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(node_y)),
                      Transform(node_z[0], Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(node_z)),
                      Transform(node_w[0], Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(node_w)))
            self.wait()
            nodes = VGroup(node_x, node_y, node_z, node_w)
            edges = VGroup(edge1, edge2, edge3, top)
            self.play(nodes.animate.shift(DOWN * 3), edges.animate.shift(DOWN * 3))
            self.wait()

        def case4(): # Black uncle out
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(LEFT * 2 + DOWN * 2)
            text = Text2("X").move_to(node)
            node_x = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 0.5)
            text = Text2("Y").move_to(node)
            node_y = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3 + RIGHT * 2)
            text = Text2("Z").move_to(node)
            node_z = VGroup(node, text).set_z_index(2)
            n = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 6 + RIGHT * 2)
            edge1 = node_edge(node_z, node_y)
            edge2 = node_edge(node_y, node_x)
            top = node_edge(n, node_z)
            self.wait()
            self.play(AnimationGroup(Write(top), Write(node_z), Create(edge1), Write(node_y), Create(edge2), Write(node_x), lag_ratio=0.15))
            self.wait(0.5)
            nodes = VGroup(node_x, node_y, node_z)
            nxt = nodes.copy()
            nxt[2].shift(DOWN * 4)
            nxt[1].shift(UP)
            nxt[0].shift(UP)
            nxt[1][0] = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(nxt[1][0])
            nxt[2][0] = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(nxt[2][0])
            self.play(Transform(nodes, nxt), Transform(edge1, node_edge(nxt[1], nxt[2])),
                      Transform(edge2, node_edge(nxt[1], nxt[0])), top.animate.shift(LEFT * 2 + DOWN * 1.5))
            self.wait()

        def case5(): # Black uncle out
            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(RIGHT + DOWN * 2)
            text = Text2("X").move_to(node)
            node_x = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 0.5 + LEFT)
            text = Text2("Y").move_to(node)
            node_y = VGroup(node, text).set_z_index(2)

            node = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).shift(UP * 3 + RIGHT)
            text = Text2("Z").move_to(node)
            node_z = VGroup(node, text).set_z_index(2)
            n = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).shift(UP * 6 + RIGHT)
            edge1 = node_edge(node_z, node_y)
            edge2 = node_edge(node_y, node_x)
            top = node_edge(n, node_z)
            self.wait()
            self.play(AnimationGroup(Write(top), Write(node_z), Create(edge1), Write(node_y), Create(edge2), Write(node_x), lag_ratio=0.15))
            self.wait(0.5)
            nodes = VGroup(node_x, node_y, node_z)
            nxt = nodes.copy()
            nxt[1].shift(LEFT * 2 + DOWN * 2.5)
            nxt[0].shift(LEFT * 2 + UP * 2.5)
            self.play(Transform(nodes, nxt), Transform(edge2, node_edge(nxt[0], nxt[1])))
            self.wait(0.5)
            nxt = nodes.copy().shift(RIGHT)
            nxt[0].shift(UP)
            nxt[1].shift(UP)
            nxt[2].shift(DOWN * 4)
            nxt[0][0] = Circle(color=BLUE, fill_color=BLACK, **circle_kwargs).move_to(nxt[0][0])
            nxt[2][0] = Circle(color=BLUE, fill_color=PURE_RED, **circle_kwargs).move_to(nxt[2][0])
            self.play(Transform(nodes, nxt), Transform(edge1, node_edge(nxt[0], nxt[2])),
                      Transform(edge2, node_edge(nxt[0], nxt[1])), top.animate.shift(LEFT + DOWN * 1.5))
            self.wait()

        case5()

class AATree(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color

        def show_levels():
            node = Circle(fill_color=BLACK, fill_opacity=1, **node_kwargs).shift(UP * 2.5 + LEFT)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Circle(fill_color=PURE_RED, fill_opacity=1, **node_kwargs).shift(RIGHT)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Circle(fill_color=BLACK, fill_opacity=1, **node_kwargs).shift(LEFT * 3)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text).set_z_index(2)

            node = Circle(fill_color=BLACK, fill_opacity=1, **node_kwargs).shift(DOWN * 2.5 + LEFT)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text).set_z_index(2)

            node = Circle(fill_color=BLACK, fill_opacity=1, **node_kwargs).shift(DOWN * 2.5 + RIGHT * 3)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text).set_z_index(2)

            edge1 = node_edge(node_a, node_b)
            edge2 = node_edge(node_a, node_p)
            edge3 = node_edge(node_b, node_q)
            edge4 = node_edge(node_b, node_r)
            self.play(AnimationGroup(Write(node_a), Write(edge1), Write(node_b), Write(edge2), Write(node_p),
                                     Write(edge3), Write(node_q), Write(edge4), Write(node_r), lag_ratio=0.15))
            self.wait()

            line = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(UP * 3.75)
            lines = VGroup(line, line.copy().shift(DOWN * 2.5), line.copy().shift(DOWN * 5), line.copy().shift(DOWN * 7.5))
            levels = VGroup()
            for i in range(3):
                levels.add(Text2(str(i + 1)).shift(LEFT * 6.5 + UP * 2.5 * (i - 1)))

            node_a_nxt = node_a.copy().shift(DOWN * 2.25 + LEFT * 0.5)
            node_a_nxt[0] = Circle(**node_kwargs).move_to(node_a_nxt)
            node_b_nxt = node_b.copy().shift(DOWN * 0.25 + RIGHT * 0.5)
            node_b_nxt[0] = Circle(**node_kwargs).move_to(node_b_nxt)
            node_p_nxt = node_p.copy().shift(DOWN * 2.5 + LEFT * 0.25)
            node_p_nxt[0] = Circle(**node_kwargs).move_to(node_p_nxt)
            node_q_nxt = node_q.copy().shift(RIGHT)
            node_q_nxt[0] = Circle(**node_kwargs).move_to(node_q_nxt)
            node_r_nxt = node_r.copy()
            node_r_nxt[0] = Circle(**node_kwargs).move_to(node_r_nxt)
            self.play(AnimationGroup(
                *[Write(lines[i], run_time=0.75) for i in range(4)] +
                 [AnimationGroup(Transform(node_a, node_a_nxt), Transform(node_b, node_b_nxt),
                                 Transform(node_p, node_p_nxt), Transform(node_q, node_q_nxt), Transform(node_r, node_r_nxt),
                                 Transform(edge1, node_edge(node_a_nxt, node_b_nxt)), Transform(edge2, node_edge(node_a_nxt, node_p_nxt)),
                                 Transform(edge3, node_edge(node_b_nxt, node_q_nxt)), Transform(edge4, node_edge(node_b_nxt, node_r_nxt)))], lag_ratio=0.15),
                AnimationGroup(*[Write(levels[i], run_time=0.75) for i in range(3)], lag_ratio=0.25))
            self.wait()
            self.play(Unwrite(node_a), Unwrite(node_b), Unwrite(node_p), Unwrite(node_q), Unwrite(node_r),
                      Unwrite(edge1), Unwrite(edge2), Unwrite(edge3), Unwrite(edge4))
            self.wait()

        def skew():
            line = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(UP * 3.75)
            lines = VGroup(line, line.copy().shift(DOWN * 2.5), line.copy().shift(DOWN * 5),
                           line.copy().shift(DOWN * 7.5))
            self.add(lines)
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(LEFT * 1.5 + DOWN * 0.25)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 1.5 + UP * 0.25)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(DOWN * 2.5 + LEFT * 3.25)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(DOWN * 2.5)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 3 + DOWN * 2.5)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text).set_z_index(2)

            edge1 = node_edge(node_b, node_a)
            edge2 = node_edge(node_a, node_p)
            edge3 = node_edge(node_a, node_q)
            edge4 = node_edge(node_b, node_r)

            self.play(AnimationGroup(Write(node_a), Write(edge1), Write(node_b), Write(edge2), Write(node_p),
                                Write(edge3), Write(node_q), Write(edge4), Write(node_r), lag_ratio=0.15))
            self.wait()

            node_a_nxt = node_a.copy().shift(UP * 0.5)
            node_b_nxt = node_b.copy().shift(DOWN * 0.5)
            node_p_nxt = node_p.copy().shift(RIGHT * 0.25)
            node_r_nxt = node_r.copy().shift(RIGHT * 0.25)
            self.play(Transform(node_a, node_a_nxt), Transform(node_b, node_b_nxt),
                      Transform(node_p, node_p_nxt), Transform(node_r, node_r_nxt),
                      Transform(edge1, node_edge(node_a_nxt, node_b_nxt)), Transform(edge2, node_edge(node_a_nxt, node_p_nxt)),
                      Transform(edge3, node_edge(node_b_nxt, node_q)), Transform(edge4, node_edge(node_b_nxt, node_r_nxt)))
            self.wait()

        def split():
            line = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(UP * 3.75)
            lines = VGroup(line, line.copy().shift(DOWN * 2.5), line.copy().shift(DOWN * 5),
                           line.copy().shift(DOWN * 7.5))
            self.add(lines)
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(LEFT * 3 + UP * 0.25)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(LEFT * 4.5 + DOWN * 2.5)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(LEFT * 1.5 + DOWN * 2.5)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 3 + DOWN * 0.25)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text).set_z_index(2)

            edge1 = node_edge(node_a, node_b)
            edge2 = node_edge(node_b, node_r)
            edge3 = node_edge(node_a, node_p)
            edge4 = node_edge(node_b, node_q)

            self.play(AnimationGroup(Write(node_a), Write(edge1), Write(node_b), Write(edge2), Write(node_p),
                                     Write(edge3), Write(node_q), Write(edge4), Write(node_r), lag_ratio=0.15))
            self.wait()

            node_a_nxt = node_a.copy().shift(DOWN * 0.25 + RIGHT * 1.5)
            node_b_nxt = node_b.copy().shift(UP * 2.5)
            node_p_nxt = node_p.copy().shift(RIGHT * 1.5)
            node_q_nxt = node_q.copy().shift(RIGHT * 1.5)
            node_r_nxt = node_r.copy().shift(LEFT * 1.5 + UP * 0.25)

            self.play(Transform(node_a, node_a_nxt), Transform(node_b, node_b_nxt),
                      Transform(node_p, node_p_nxt), Transform(node_q, node_q_nxt), Transform(node_r, node_r_nxt),
                      Transform(edge1, node_edge(node_b_nxt, node_a_nxt)),
                      Transform(edge2, node_edge(node_b_nxt, node_r_nxt)),
                      Transform(edge3, node_edge(node_a_nxt, node_p_nxt)),
                      Transform(edge4, node_edge(node_a_nxt, node_q_nxt)))
            self.wait()

        def insert():
            line = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(UP * 3.75)
            lines = VGroup(line, line.copy().shift(DOWN * 2.5), line.copy().shift(DOWN * 5),
                           line.copy().shift(DOWN * 7.5))
            levels = VGroup()
            for i in range(3):
                levels.add(Text2(str(i + 1)).shift(LEFT * 6.5 + UP * 2.5 * (i - 1)))
            self.add(lines, levels)
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(DOWN * 2.5)
            text = Text2("8").move_to(node)
            node_8 = VGroup(node, text).set_z_index(2)
            self.play(Write(node_8))
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(DOWN * 2.75 + LEFT * 1.5)
            text = Text2("4").move_to(node)
            node_4 = VGroup(node, text).set_z_index(2)
            node_8_nxt = node_8.copy().shift(RIGHT * 1.5 + UP * 0.25)

            edge_1 = node_edge(node_8_nxt, node_4)
            self.play(AnimationGroup(Transform(node_8, node_8_nxt), Write(node_4), Write(edge_1), lag_ratio=0.25))

            node_4_nxt = node_4.copy().shift(UP * 0.5)
            node_8_nxt = node_8.copy().shift(DOWN * 0.5)
            edge_1_nxt = node_edge(node_4_nxt, node_8_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Transform(edge_1, edge_1_nxt))
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(DOWN * 3.1 + LEFT * 1.5)
            text = Text2("7").move_to(node)
            node_7 = VGroup(node, text).set_z_index(2)
            node_4_nxt = node_4.copy().shift(UP * 0.35)
            node_8_nxt = node_8.copy().shift(UP * 0.25)
            edge_1_nxt = node_edge(node_4_nxt, node_8_nxt)
            edge_2 = node_edge(node_8_nxt, node_7)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Write(node_7),
                      Transform(edge_1, edge_1_nxt), Write(edge_2))

            node_4_nxt = node_4.copy().shift(LEFT * 1.5)
            node_8_nxt = node_8.copy().shift(RIGHT * 1.5 + DOWN * 0.6)
            node_7_nxt = node_7.copy().shift(RIGHT * 1.5 + UP * 0.6)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Transform(node_7, node_7_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt))

            node_4_nxt = node_4.copy().shift(RIGHT * 1.5 + DOWN * 0.6)
            node_8_nxt = node_8.copy().shift(LEFT * 1.5 + UP * 0.6)
            node_7_nxt = node_7.copy().shift(UP * 2.5)
            edge_1_nxt = node_edge(node_7_nxt, node_4_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Transform(node_7, node_7_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt))
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(DOWN * 2.75 + LEFT * 3.5)
            text = Text2("2").move_to(node)
            node_2 = VGroup(node, text).set_z_index(2)
            node_4_nxt = node_4.copy().shift(RIGHT + UP * 0.25)
            node_7_nxt = node_7.copy().shift(RIGHT * 1.5)
            node_8_nxt = node_8.copy().shift(RIGHT * 2)
            edge_1_nxt = node_edge(node_7_nxt, node_4_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_3 = node_edge(node_4_nxt, node_2)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Transform(node_7, node_7_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Write(node_2), Write(edge_3))

            node_4_nxt = node_4.copy().shift(DOWN * 0.5)
            node_2_nxt = node_2.copy().shift(UP * 0.5)
            node_7_nxt = node_7.copy().shift(LEFT * 1.5)
            edge_1_nxt = node_edge(node_7_nxt, node_2_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8)
            edge_3_nxt = node_edge(node_2_nxt, node_4_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_8, node_8_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt))
            self.wait(0.5)

            node = Circle(**node_kwargs).shift(DOWN * 3.1 + RIGHT * 1.5)
            text = Text2("5").move_to(node)
            node_5 = VGroup(node, text).set_z_index(2)
            node_4_nxt = node_4.copy().shift(LEFT * 0.5 + UP * 0.25)
            node_2_nxt = node_2.copy().shift(UP * 0.35)
            edge_1_nxt = node_edge(node_7, node_2_nxt)
            edge_3_nxt = node_edge(node_2_nxt, node_4_nxt)
            edge_4 = node_edge(node_4_nxt, node_5)
            self.play(Transform(node_4, node_4_nxt), Transform(node_2, node_2_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_3, edge_3_nxt), Write(edge_4), Write(node_5))

            node_4_nxt = node_4.copy().shift(LEFT + UP * 2.25)
            node_2_nxt = node_2.copy().shift(DOWN * 0.6)
            node_7_nxt = node_7.copy().shift(RIGHT * 1.5 + UP * 0.25)
            node_5_nxt = node_5.copy().shift(LEFT * 2 + UP * 0.6)
            edge_1_nxt = node_edge(node_7_nxt, node_4_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_2_nxt)
            edge_4_nxt = node_edge(node_4_nxt, node_5_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt), Transform(node_5, node_5_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_4, edge_4_nxt))

            node_4_nxt = node_4.copy().shift(RIGHT * 0.5 + UP * 0.5)
            node_7_nxt = node_7.copy().shift(RIGHT * 0.5 + DOWN * 0.5)
            node_5_nxt = node_5.copy().shift(RIGHT)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_2_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_5, node_5_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_4, edge_4_nxt))
            self.wait(0.5)

            node_4_nxt = node_4.copy().shift(LEFT * 0.5)
            node_2_nxt = node_2.copy().shift(LEFT * 0.5)
            node_7_nxt = node_7.copy().shift(LEFT)
            node_5_nxt = node_5.copy().shift(LEFT)
            node_8_nxt = node_8.copy().shift(LEFT + UP * 0.25)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_2_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            node = Circle(**node_kwargs).shift(DOWN * 2.75 + RIGHT * 5)
            text = Text2("10").move_to(node)
            node_10 = VGroup(node, text).set_z_index(2)
            edge_5 = node_edge(node_8_nxt, node_10)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt),
                      Transform(node_5, node_5_nxt), Transform(node_8, node_8_nxt), Write(node_10),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Write(edge_5))
            self.wait(0.5)

            node_4_nxt = node_4.copy().shift(RIGHT * 0.5)
            node_2_nxt = node_2.copy().shift(RIGHT + UP * 0.25)
            node_7_nxt = node_7.copy().shift(RIGHT * 0.5)
            node_5_nxt = node_5.copy().shift(RIGHT * 0.5)
            node_8_nxt = node_8.copy().shift(RIGHT * 0.5)
            node_10_nxt = node_10.copy().shift(RIGHT * 0.5)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_2_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_5_nxt = node_edge(node_8_nxt, node_10_nxt)
            node = Circle(**node_kwargs).shift(DOWN * 2.75 + LEFT * 5.5)
            text = Text2("1").move_to(node)
            node_1 = VGroup(node, text).set_z_index(2)
            edge_6 = node_edge(node_2_nxt, node_1)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt),
                      Transform(node_5, node_5_nxt), Transform(node_8, node_8_nxt), Transform(node_10, node_10_nxt), Write(node_1),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Write(edge_6))

            node_4_nxt = node_4.copy().shift(LEFT)
            node_2_nxt = node_2.copy().shift(RIGHT * 0.5 + DOWN * 0.5)
            node_1_nxt = node_1.copy().shift(RIGHT * 0.5 + UP * 0.5)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_1_nxt)
            edge_6_nxt = node_edge(node_1_nxt, node_2_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_1, node_1_nxt), Transform(node_2, node_2_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_6, edge_6_nxt))
            self.wait(0.5)

            node_4_nxt = node_4.copy().shift(RIGHT)
            node_2_nxt = node_2.copy().shift(LEFT * 0.5 + UP * 0.25)
            node_1_nxt = node_1.copy().shift(UP * 0.35)
            node_7_nxt = node_7.copy().shift(RIGHT * 0.75)
            node_5_nxt = node_5.copy().shift(RIGHT)
            node_8_nxt = node_8.copy().shift(RIGHT * 0.5)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_5_nxt = node_edge(node_8_nxt, node_10_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_1_nxt)
            edge_6_nxt = node_edge(node_1_nxt, node_2_nxt)
            node = Circle(**node_kwargs).shift(DOWN * 3.1 + LEFT)
            text = Text2("3").move_to(node)
            node_3 = VGroup(node, text).set_z_index(2)
            edge_7 = node_edge(node_2_nxt, node_3)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt),
                      Transform(node_5, node_5_nxt), Transform(node_1, node_1_nxt), Transform(node_8, node_8_nxt), Write(node_3),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt), Write(edge_7))

            node_2_nxt = node_2.copy().shift(UP * 2.25 + LEFT)
            node_1_nxt = node_1.copy().shift(DOWN * 0.6 + LEFT * 0.5)
            node_3_nxt = node_3.copy().shift(UP * 0.6 + LEFT * 1.5)
            node_7_nxt = node_7.copy().shift(LEFT * 1.25)
            node_5_nxt = node_5.copy().shift(LEFT * 1.5)
            node_8_nxt = node_8.copy().shift(LEFT)
            node_10_nxt = node_10.copy().shift(LEFT * 0.5)
            edge_1_nxt = node_edge(node_4, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_5_nxt = node_edge(node_8_nxt, node_10_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_3_nxt = node_edge(node_4, node_2_nxt)
            edge_6_nxt = node_edge(node_2_nxt, node_1_nxt)
            edge_7_nxt = node_edge(node_2_nxt, node_3_nxt)
            self.play(Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt), Transform(node_5, node_5_nxt),
                      Transform(node_1, node_1_nxt), Transform(node_8, node_8_nxt), Transform(node_3, node_3_nxt), Transform(node_10, node_10_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt))

            node_4_nxt = node_4.copy().shift(DOWN * 0.25)
            node_2_nxt = node_2.copy().shift(UP * 0.85)
            node_3_nxt = node_3.copy().shift(LEFT * 0.5)
            node_7_nxt = node_7.copy().shift(DOWN * 0.35)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8)
            edge_4_nxt = node_edge(node_7_nxt, node_5)
            edge_6_nxt = node_edge(node_2_nxt, node_1)
            edge_3_nxt = node_edge(node_2_nxt, node_4_nxt)
            edge_7_nxt = node_edge(node_4_nxt, node_3_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt), Transform(node_3, node_3_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt))

            node_4_nxt = node_4.copy().shift(UP * 2.5 + LEFT * 0.25)
            node_2_nxt = node_2.copy().shift(DOWN * 0.6)
            node_7_nxt = node_7.copy().shift(UP * 0.6 + LEFT * 0.5)
            node_3_nxt = node_3.copy().shift(RIGHT * 0.5)
            node_5_nxt = node_5.copy().shift(LEFT * 0.5)
            node_8_nxt = node_8.copy().shift(LEFT * 0.5)
            node_10_nxt = node_10.copy().shift(LEFT * 0.5)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_8_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_6_nxt = node_edge(node_2_nxt, node_1)
            edge_3_nxt = node_edge(node_4_nxt, node_2_nxt)
            edge_7_nxt = node_edge(node_2_nxt, node_3_nxt)
            edge_5_nxt = node_edge(node_8_nxt, node_10_nxt)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt),
                      Transform(node_3, node_3_nxt), Transform(node_5, node_5_nxt), Transform(node_8, node_8_nxt), Transform(node_10, node_10_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt), Transform(edge_5, edge_5_nxt))
            self.wait(0.5)

            node_8_nxt = node_8.copy().shift(LEFT * 0.5 + UP * 0.35)
            node_10_nxt = node_10.copy().shift(LEFT + UP * 0.25)
            edge_2_nxt = node_edge(node_7, node_8_nxt)
            edge_5_nxt = node_edge(node_8_nxt, node_10_nxt)
            node = Circle(**node_kwargs).shift(DOWN * 3.1 + RIGHT * 5.5)
            text = Text2("14").move_to(node)
            node_14 = VGroup(node, text).set_z_index(2)
            edge_8 = node_edge(node_10_nxt, node_14)
            self.play(Transform(node_8, node_8_nxt), Transform(node_10, node_10_nxt), Write(node_14),
                      Transform(edge_2, edge_2_nxt), Transform(edge_5, edge_5_nxt), Write(edge_8))

            node_8_nxt = node_8.copy().shift(RIGHT + DOWN * 0.6)
            node_10_nxt = node_10.copy().shift(RIGHT * 0.5 + UP * 2.25)
            node_7_nxt = node_7.copy().shift(UP * 0.25)
            node_14_nxt = node_14.copy().shift(UP * 0.6)
            edge_1_nxt = node_edge(node_4, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_10_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_5_nxt = node_edge(node_10_nxt, node_8_nxt)
            edge_8_nxt = node_edge(node_10_nxt, node_14_nxt)
            self.play(Transform(node_8, node_8_nxt), Transform(node_10, node_10_nxt),  Transform(node_14, node_14_nxt),  Transform(node_7, node_7_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_4, edge_4_nxt),
                      Transform(edge_5, edge_5_nxt), Transform(edge_8, edge_8_nxt))
            self.wait(0.5)

            node_8_nxt = node_8.copy().shift(RIGHT * 0.5)
            node_10_nxt = node_10.copy().shift(RIGHT * 0.25)
            node_3_nxt = node_3.copy().shift(LEFT * 0.5)
            node_2_nxt = node_2.copy().shift(LEFT * 0.25)
            node_7_nxt = node_7.copy().shift(LEFT * 0.25)
            node_5_nxt = node_5.copy().shift(LEFT * 0.25 + UP * 0.25)
            edge_1_nxt = node_edge(node_4, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_10_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_3_nxt = node_edge(node_4, node_2_nxt)
            edge_6_nxt = node_edge(node_2_nxt, node_1)
            edge_7_nxt = node_edge(node_2_nxt, node_3_nxt)
            edge_5_nxt = node_edge(node_10_nxt, node_8_nxt)
            edge_8_nxt = node_edge(node_10_nxt, node_14)
            node = Circle(**node_kwargs).shift(DOWN * 2.75 + RIGHT * 1.25)
            text = Text2("6").move_to(node)
            node_6 = VGroup(node, text).set_z_index(2)
            edge_9 = node_edge(node_5_nxt, node_6)
            self.play(Transform(node_7, node_7_nxt), Transform(node_2, node_2_nxt), Transform(node_3, node_3_nxt),
                      Transform(node_5, node_5_nxt), Transform(node_8, node_8_nxt), Transform(node_10, node_10_nxt), Write(node_6),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_6, edge_6_nxt), Transform(edge_7, edge_7_nxt),
                      Transform(edge_5, edge_5_nxt), Transform(edge_8, edge_8_nxt), Write(edge_9))
            self.wait()

            self.play(node_3[1].animate.move_to(node_2), node_2[1].animate.move_to(node_3))
            num2 = node_2[1]
            node_2.remove(num2)
            num3 = node_3[1]
            node_3.remove(num3)
            node_2.add(num3)
            self.add(num2)
            self.wait(0.5)
            self.play(Unwrite(num2), Unwrite(node_3), Unwrite(edge_7))
            node_3 = node_2.copy()
            self.add(node_3)
            self.remove(node_2)
            self.wait(0.5)

            edge_7 = Arrow(start=node_2.get_center(), end=node_2.get_center() + RIGHT * 1.5 + DOWN * 4.5, **node_edge_kwargs)
            self.play(FadeIn(edge_7))
            self.wait(0.5)
            self.play(FadeOut(edge_7))
            self.wait(0.5)

            node_1_nxt = node_1.copy().shift(DOWN * 0.25)
            node_3_nxt = node_3.copy().shift(DOWN * 2.25 + RIGHT * 1.5)
            edge_6_nxt = node_edge(node_3_nxt, node_1_nxt)
            edge_3_nxt = node_edge(node_4, node_3_nxt)
            self.play(Transform(node_1, node_1_nxt), Transform(node_3, node_3_nxt),
                      Transform(edge_6, edge_6_nxt), Transform(edge_3, edge_3_nxt))
            self.wait(0.5)
            node_1_nxt = node_1.copy().shift(UP * 0.5)
            node_3_nxt = node_3.copy().shift(DOWN * 0.5)
            edge_6_nxt = node_edge(node_1_nxt, node_3_nxt)
            edge_3_nxt = node_edge(node_4, node_1_nxt)
            self.play(Transform(node_1, node_1_nxt), Transform(node_3, node_3_nxt),
                      Transform(edge_6, edge_6_nxt), Transform(edge_3, edge_3_nxt))
            self.wait(0.5)

            node_4_nxt = node_4.copy().move_to(LEFT * 3.75 + UP * 0.6)
            node_7_nxt = node_7.copy().shift(DOWN * 0.25)
            node_10_nxt = node_10.copy().shift(DOWN * 0.35)
            edge_1_nxt = node_edge(node_4_nxt, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_10_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_1)
            edge_4_nxt = node_edge(node_7_nxt, node_5)
            edge_5_nxt = node_edge(node_10_nxt, node_8)
            edge_8_nxt = node_edge(node_10_nxt, node_14)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_10, node_10_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_8, edge_8_nxt))
            self.wait(0.5)

            node_4_nxt = node_4.copy().shift(RIGHT * 0.5 + DOWN * 0.6)
            node_7_nxt = node_7.copy().shift(UP * 2.5 + RIGHT * 0.25)
            node_10_nxt = node_10.copy().shift(UP * 0.6)
            edge_1_nxt = node_edge(node_7_nxt, node_4_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_10_nxt)
            edge_3_nxt = node_edge(node_4_nxt, node_1)
            edge_4_nxt = node_edge(node_4_nxt, node_5)
            edge_5_nxt = node_edge(node_10_nxt, node_8)
            edge_8_nxt = node_edge(node_10_nxt, node_14)
            self.play(Transform(node_4, node_4_nxt), Transform(node_7, node_7_nxt), Transform(node_10, node_10_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_8, edge_8_nxt))
            self.wait(0.5)

            '''
            edge_1_nxt = node_edge(node_4, node_7_nxt)
            edge_2_nxt = node_edge(node_7_nxt, node_10_nxt)
            edge_4_nxt = node_edge(node_7_nxt, node_5_nxt)
            edge_3_nxt = node_edge(node_4, node_2_nxt)
            edge_6_nxt = node_edge(node_2_nxt, node_1)
            edge_7_nxt = node_edge(node_2_nxt, node_3_nxt)
            edge_5_nxt = node_edge(node_10_nxt, node_8_nxt)
            edge_8_nxt = node_edge(node_10_nxt, node_14)
            '''
            print(node_1.get_center(), node_3.get_center(), node_4.get_center(), node_5.get_center())
            print(node_6.get_center(), node_7.get_center(), node_8.get_center(), node_10.get_center(), node_14.get_center())
            self.wait()

        def delete():
            line = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.2, stroke_width=5).shift(UP * 3.75)
            lines = VGroup(line, line.copy().shift(DOWN * 2.5), line.copy().shift(DOWN * 5),
                           line.copy().shift(DOWN * 7.5))
            levels = VGroup()
            for i in range(3):
                levels.add(Text2(str(i + 1)).shift(LEFT * 6.5 + UP * 2.5 * (i - 1)))
            self.add(lines, levels)
            self.wait(0.5)

            node = Circle(**root_kwargs).shift(LEFT * 3.5 + UP * 2.75)
            text = Text2("a").move_to(node)
            node_a = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 2 + UP * 2.25)
            text = Text2("b").move_to(node)
            node_b = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(LEFT * 5 + DOWN * 2.5)
            text = Text2("c").move_to(node)
            node_c = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(LEFT * 1.5 + UP * 0.25)
            text = Text2("p").move_to(node)
            node_p = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT + DOWN * 0.25)
            text = Text2("q").move_to(node)
            node_q = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 3 + UP * 0.25)
            text = Text2("r").move_to(node)
            node_r = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs).shift(RIGHT * 5.5 + DOWN * 0.25)
            text = Text2("s").move_to(node)
            node_s = VGroup(node, text).set_z_index(2)

            edge_1 = node_edge(node_a, node_b)
            edge_2 = node_edge(node_a, node_c)
            edge_3 = node_edge(node_b, node_p)
            edge_4 = node_edge(node_b, node_r)
            edge_5 = node_edge(node_p, node_q)
            edge_6 = node_edge(node_r, node_s)

            self.play(AnimationGroup(Write(node_a), Write(edge_1), Write(node_b), Write(edge_2), Write(node_c),
                                     Write(edge_3), Write(node_p), Write(edge_4), Write(node_r),
                                     Write(edge_5), Write(node_q), Write(edge_6), Write(node_s), lag_ratio=0.1))
            self.wait(0.5)

            node_a_nxt = node_a.copy().shift(DOWN * 1.75)
            node_b_nxt = node_b.copy().shift(DOWN * 1.5 + LEFT * 0.5)
            node_p_nxt = node_p.copy().shift(DOWN * 0.5)
            node_q_nxt = node_q.copy().shift(DOWN * 0.75)
            node_r_nxt = node_r.copy().shift(DOWN * 0.5)
            node_s_nxt = node_s.copy().shift(DOWN * 0.75)
            edge_1_nxt = node_edge(node_a_nxt, node_b_nxt)
            edge_2_nxt = node_edge(node_a_nxt, node_c)
            edge_3_nxt = node_edge(node_b_nxt, node_p_nxt)
            edge_4_nxt = node_edge(node_b_nxt, node_r_nxt)
            edge_5_nxt = node_edge(node_p_nxt, node_q_nxt)
            edge_6_nxt = node_edge(node_r_nxt, node_s_nxt)
            self.play(Transform(node_a, node_a_nxt), Transform(node_b, node_b_nxt), Transform(node_p, node_p_nxt),
                      Transform(node_q, node_q_nxt), Transform(node_r, node_r_nxt), Transform(node_s, node_s_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt),
                      lines[1].animate.shift(UP * 0.5), lines[2].animate.shift(DOWN * 0.5))
            self.wait(0.5)

            node_b_nxt = node_b.copy().shift(DOWN * 0.25 + LEFT)
            node_p_nxt = node_p.copy().shift(UP)
            node_q_nxt = node_q.copy().shift(LEFT * 1.5)
            edge_1_nxt = node_edge(node_a, node_p_nxt)
            edge_3_nxt = node_edge(node_p_nxt, node_b_nxt)
            edge_4_nxt = node_edge(node_b_nxt, node_r)
            edge_5_nxt = node_edge(node_b_nxt, node_q_nxt)
            self.play(Transform(node_b, node_b_nxt), Transform(node_p, node_p_nxt), Transform(node_q, node_q_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt))
            self.wait(0.5)

            node_a_nxt = node_a.copy().shift(LEFT)
            node_b_nxt = node_b.copy().shift(RIGHT + DOWN * 0.7)
            node_p_nxt = node_p.copy().shift(LEFT + DOWN * 0.15)
            node_q_nxt = node_q.copy().shift(UP * 1.2)
            node_r_nxt = node_r.copy().shift(RIGHT * 0.5 + DOWN * 0.35)
            edge_1_nxt = node_edge(node_a_nxt, node_p_nxt)
            edge_2_nxt = node_edge(node_a_nxt, node_c)
            edge_3_nxt = node_edge(node_p_nxt, node_q_nxt)
            edge_4_nxt = node_edge(node_b_nxt, node_r_nxt)
            edge_5_nxt = node_edge(node_q_nxt, node_b_nxt)
            edge_6_nxt = node_edge(node_r_nxt, node_s)
            self.play(Transform(node_a, node_a_nxt), Transform(node_b, node_b_nxt), Transform(node_p, node_p_nxt),
                      Transform(node_q, node_q_nxt), Transform(node_r, node_r_nxt), Transform(node_s, node_s_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt))
            self.wait(0.5)

            node_a_nxt = node_a.copy().shift(DOWN * 0.75)
            node_a_nxt[0] = Circle(**node_kwargs).move_to(node_a_nxt)
            node_p_nxt = node_p.copy().shift(UP * 2.15)
            node_p_nxt[0] = Circle(**root_kwargs).move_to(node_p_nxt)
            node_q_nxt = node_q.copy().shift(UP * 0.05)
            edge_1_nxt = node_edge(node_p_nxt, node_a_nxt)
            edge_2_nxt = node_edge(node_a_nxt, node_c)
            edge_3_nxt = node_edge(node_p_nxt, node_q_nxt)
            edge_5_nxt = node_edge(node_q_nxt, node_b)
            self.play(Transform(node_a, node_a_nxt), Transform(node_p, node_p_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt), Transform(edge_5, edge_5_nxt))
            self.wait(0.5)

            node_b_nxt = node_b.copy().shift(UP * 2.45)
            node_r_nxt = node_r.copy().shift(UP * 0.85)
            node_s_nxt = node_s.copy().shift(UP * 0.75)
            edge_3_nxt = node_edge(node_p, node_b_nxt)
            edge_4_nxt = node_edge(node_b_nxt, node_r_nxt)
            edge_5_nxt = node_edge(node_b_nxt, node_q)
            edge_6_nxt = node_edge(node_r_nxt, node_s_nxt)
            self.play(Transform(node_b, node_b_nxt), Transform(node_r, node_r_nxt), Transform(node_s, node_s_nxt),
                      Transform(edge_3, edge_3_nxt), Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt),
                      lines[1].animate.shift(DOWN * 0.5), lines[2].animate.shift(UP * 0.5))
            node_a_nxt = node_a.copy().shift(RIGHT + DOWN * 0.25)
            node_p_nxt = node_p.copy().shift(RIGHT * 0.5)
            node_q_nxt = node_q.copy().shift(RIGHT * 0.5)
            node_r_nxt = node_r.copy().shift(LEFT * 0.5)
            node_s_nxt = node_s.copy().shift(LEFT * 0.5)
            edge_1_nxt = node_edge(node_p_nxt, node_a_nxt)
            edge_2_nxt = node_edge(node_a_nxt, node_c)
            edge_3_nxt = node_edge(node_p_nxt, node_b)
            edge_4_nxt = node_edge(node_b, node_r_nxt)
            edge_5_nxt = node_edge(node_b_nxt, node_q_nxt)
            edge_6_nxt = node_edge(node_r_nxt, node_s_nxt)
            self.play(Transform(node_a, node_a_nxt), Transform(node_p, node_p_nxt),
                      Transform(node_q, node_q_nxt), Transform(node_r, node_r_nxt), Transform(node_s, node_s_nxt),
                      Transform(edge_1, edge_1_nxt), Transform(edge_2, edge_2_nxt), Transform(edge_3, edge_3_nxt),
                      Transform(edge_4, edge_4_nxt), Transform(edge_5, edge_5_nxt), Transform(edge_6, edge_6_nxt))
            self.wait(0.5)

            print(node_a.get_center(), node_b.get_center(), node_c.get_center(), node_p.get_center(), node_q.get_center(), node_r.get_center(), node_s.get_center())
            self.wait()

        delete()

class FHQTreap(Scene):
    def construct(self):
        bg_color = DARKER_GRAY
        self.camera.background_color = bg_color
        self.wait()

        def get_priority(pri, target):
            nums = VGroup()
            for i in range(len(target)):
                nums.add(Text2(str(pri[i]), {'color': BLUE_B}).scale(0.4).next_to(target[i], LEFT, buff=SMALL_BUFF))
            return nums

        def splitmerge():
            node = Circle(**node_kwargs).shift(UP * 3)
            text = Text2("8").move_to(node)
            node8 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(UP + LEFT * 3)
            text = Text2("4").move_to(node)
            node4 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + LEFT * 4.5)
            text = Text2("2").move_to(node)
            node2 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + LEFT * 1.5)
            text = Text2("6").move_to(node)
            node6 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 3.75)
            text = Text2("3").move_to(node)
            node3 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 2.25)
            text = Text2("5").move_to(node)
            node5 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 0.75)
            text = Text2("7").move_to(node)
            node7 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(UP + RIGHT * 3)
            text = Text2("12").move_to(node)
            node12 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + RIGHT * 1.5)
            text = Text2("10").move_to(node)
            node10 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + RIGHT * 4.5)
            text = Text2("14").move_to(node)
            node14 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + RIGHT * 3.75)
            text = Text2("13").move_to(node)
            node13 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + RIGHT * 5.25)
            text = Text2("15").move_to(node)
            node15 = VGroup(node, text).set_z_index(3)

            nodes = VGroup(node2, node3, node4, node5, node6, node7, node8, node10, node12, node13, node14, node15)

            edges = VGroup(node_edge(node8, node4), node_edge(node4, node2), node_edge(node2, node3), node_edge(node4, node6),
                           node_edge(node6, node5), node_edge(node6, node7), node_edge(node8, node12), node_edge(node12, node10),
                           node_edge(node12, node14), node_edge(node14, node13), node_edge(node14, node15))
            self.play(AnimationGroup(*[Write(nodes[i]) for i in range(12)], lag_ratio=0.1),
                      AnimationGroup(*[Write(edges[i]) for i in range(11)], lag_ratio=0.1))
            self.wait()


            # pri = [75, 34, 292, 13, 240, 7, 411, 88, 156, 12, 94, 61]
            # priority = get_priority(pri, nodes)
            # self.play(AnimationGroup(*[Write(priority[i]) for i in range(12)], lag_ratio=0.1))
            # self.wait(0.5)
            # self.play(AnimationGroup(*[Unwrite(priority[i]) for i in range(12)], lag_ratio=0.1))
            # self.wait()
            # edges[0].set_z_index(2)
            # subtree = Polygon([-3, 2.25, 0], [-0.5, -1, 0], [0.5, -3.75, 0], [-6.5, -3.75, 0], [-5.5, -1, 0],
            #                   color=GREEN, fill_opacity=1, fill_color=GRAY_D, stroke_width=8).round_corners()
            # self.play(FadeIn(subtree))
            # self.play(Transform(edges[0], node_edge(node8, node5).set_z_index(2)), run_time=0.5)
            # self.play(Transform(edges[0], node_edge(node8, node2).set_z_index(2)), run_time=0.5)
            # self.play(Transform(edges[0], node_edge(node8, node4).set_z_index(2)), run_time=0.5)
            # self.wait(0.5)
            # self.play(FadeOut(subtree))
            # self.wait()
            # node10_nxt = node10.copy().shift(UP * 2 + LEFT * 0.75)
            # self.play(FadeOut(edges[7]), Transform(edges[6], node_edge(node8, node10_nxt)), Transform(node10, node10_nxt))
            # self.wait(0.5)
            # node = Circle(**node_kwargs).shift(DOWN + RIGHT * 1.5)
            # text = Text2("11").move_to(node)
            # node11 = VGroup(node, text).set_z_index(3)
            # edges.add(node_edge(node10, node11))
            # self.play(Write(edges[-1]), Write(node11))
            # self.wait(0.5)
            # node10_nxt = node10.copy().shift(DOWN * 2 + RIGHT * 0.75)
            # node11_nxt = node11.copy().shift(DOWN * 2 + RIGHT * 0.75)
            # self.play(Transform(edges[6], node_edge(node8, node12)), Write(edges[7]),
            #           Transform(edges[-1], node_edge(node10_nxt, node11_nxt)), Transform(node10, node10_nxt), Transform(node11, node11_nxt))
            # self.wait(0.5)
            # node10_nxt = node10.copy().shift(UP * 2 + LEFT * 0.75)
            # node11_nxt = node11.copy().shift(UP * 2 + LEFT * 0.75)
            # self.play(Transform(edges[6], node_edge(node8, node10_nxt)), FadeOut(edges[7]),
            #           Transform(edges[-1], node_edge(node12, node11_nxt)), Transform(node10, node10_nxt), Transform(node11, node11_nxt))
            # self.wait(0.5)
            # self.play(FadeOut(edges[-1]))
            # self.wait(0.5)
            # node10_nxt = node10.copy().shift(DOWN * 2 + RIGHT * 0.75)
            # edges[7] = node_edge(node12, node10_nxt)
            # self.play(FadeOut(node11, shift=DOWN), Transform(node10, node10_nxt), Transform(edges[6], node_edge(node8, node12)), Write(edges[7]))
            # self.wait(0.5)
            # self.play(AnimationGroup(*[Unwrite(nodes[i]) for i in range(12)], lag_ratio=0.1),
            #           AnimationGroup(*[Unwrite(edges[i]) for i in range(11)], lag_ratio=0.1))
            # 2-8 - 2, 10-15 - 3
            # '''
            self.wait()

        def o_of_n():
            node = Circle(**node_kwargs)
            text = Text2("8").move_to(node)
            node8 = VGroup(node, text).set_z_index(2).shift(UP * 3 + LEFT * 3)

            node = Circle(**node_kwargs)
            text = Text2("4").move_to(node)
            node4 = VGroup(node, text).set_z_index(2).shift(UP * 1.5 + LEFT * 1.5)

            node = Circle(**node_kwargs)
            text = Text2("2").move_to(node)
            node2 = VGroup(node, text).set_z_index(2)

            node = Circle(**node_kwargs)
            text = Text2("6").move_to(node)
            node6 = VGroup(node, text).set_z_index(2).shift(DOWN * 1.5 + RIGHT * 1.5)

            node = Circle(**node_kwargs)
            text = Text2("3").move_to(node)
            node3 = VGroup(node, text).set_z_index(2).shift(DOWN * 3 + RIGHT * 3)

            edge1 = node_edge(node8, node4)
            edge2 = node_edge(node4, node2)
            edge3 = node_edge(node2, node6)
            edge4 = node_edge(node6, node3)
            nodes = VGroup(node8, node4, node2, node6, node3)
            edges = VGroup(edge1, edge2, edge3, edge4)

            self.wait()
            self.play(AnimationGroup(Write(node8), Write(edge1), Write(node4), Write(edge2), Write(node2),
                      Write(edge3), Write(node6), Write(edge4), Write(node3), lag_ratio=0.1))
            self.wait()

            pri = [292, 240, 71, 25, 8]
            priority = get_priority(pri, nodes)
            self.play(AnimationGroup(*[Write(priority[i]) for i in range(5)], lag_ratio=0.15))
            self.wait()

            self.play(AnimationGroup(*[Unwrite(nodes[i]) for i in range(5)], lag_ratio=0.15),
                      AnimationGroup(*[Unwrite(edges[i]) for i in range(4)], lag_ratio=0.15),
                      AnimationGroup(*[Unwrite(priority[i]) for i in range(5)], lag_ratio=0.15))
            self.wait()

        def position():
            node = Circle(**node_kwargs).shift(UP * 3)
            text = Text2("8").move_to(node)
            node8 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(UP + LEFT * 3)
            text = Text2("4").move_to(node)
            node4 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + LEFT * 4.5)
            text = Text2("2").move_to(node)
            node2 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + LEFT * 3.75)
            text = Text2("3").move_to(node)
            node3 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(UP + RIGHT * 3)
            text = Text2("12").move_to(node)
            node12 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + RIGHT * 1.5)
            text = Text2("10").move_to(node)
            node10 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN + RIGHT * 4.5)
            text = Text2("14").move_to(node)
            node14 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + RIGHT * 3.75)
            text = Text2("13").move_to(node)
            node13 = VGroup(node, text).set_z_index(3)

            node = Circle(**node_kwargs).shift(DOWN * 3 + RIGHT * 5.25)
            text = Text2("15").move_to(node)
            node15 = VGroup(node, text).set_z_index(3)

            nodes = VGroup(node2, node3, node4, node8, node10, node12, node13, node14, node15)

            edges = VGroup(node_edge(node8, node4), node_edge(node4, node2), node_edge(node2, node3), node_edge(node8, node12),
                           node_edge(node12, node10), node_edge(node12, node14), node_edge(node14, node13), node_edge(node14, node15))
            self.play(AnimationGroup(*[Write(nodes[i]) for i in range(9)], lag_ratio=0.1),
                      AnimationGroup(*[Write(edges[i]) for i in range(8)], lag_ratio=0.1))
            self.wait()
            indices = VGroup()
            nxtnums = VGroup()
            for i in range(9):
                indices.add(Text2(str(i + 1)).move_to(nodes[i]))

                nxtnums.add(nodes[i][1].copy().scale(0.5).shift(LEFT * 0.8).set_color(BLUE))
            nxtnums[-1].shift(RIGHT * 1.6)
            self.play(AnimationGroup(*[Write(indices[i]) for i in range(9)]),
                      AnimationGroup(*[Transform(nodes[i][1], nxtnums[i]) for i in range(9)]))
            self.wait()
            for i in range(9):
                nodes[i].add(indices[i])
            nxt = VGroup(nodes[4].copy().shift(LEFT * 3 + UP), nodes[5].copy().shift(LEFT * 3 + UP), nodes[6].copy().shift(LEFT * 3.75 + UP),
                         nodes[7].copy().shift(LEFT * 3 + UP), nodes[8].copy().shift(LEFT * 2.25 + UP))
            edgenxt = VGroup(node_edge(nxt[1], nxt[0]), node_edge(nxt[1], nxt[3]), node_edge(nxt[3], nxt[2]), node_edge(nxt[3], nxt[4]))
            self.play(AnimationGroup(*[FadeOut(nodes[i]) for i in range(4)]), AnimationGroup(*[FadeOut(edges[i]) for i in range(4)]),
                      AnimationGroup(*[Transform(nodes[i], nxt[i - 4]) for i in range(4, 9)]),
                      AnimationGroup(*[Transform(edges[i], edgenxt[i - 4]) for i in range(4, 8)]))
            self.wait()
            self.play(AnimationGroup(*[Transform(nodes[i][2], Text2(str(i - 3)).move_to(nodes[i][0])) for i in range(4, 9)]))
            self.wait()
            self.play(AnimationGroup(*[Unwrite(nodes[i]) for i in range(4, 9)], lag_ratio=0.1),
                      AnimationGroup(*[Unwrite(edges[i]) for i in range(4, 8)], lag_ratio=0.1))
            self.wait()

        position()

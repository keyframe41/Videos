from manim import *
import math
import numpy as np
from manim.utils.rate_functions import ease_out_cubic
import copy


def Text2(text, kwargs={}):  # Text util
    return Text(text, font="JetBrains Mono", **kwargs)

class Coin:
    def __init__(self, pos, symbol, sf):
        self.symbol = symbol
        self.scale = sf
        self.disc = Circle(color=DARK_GRAY, fill_color=ManimColor([26, 57, 79]), fill_opacity=1, stroke_width=8, radius=0.75)
        self.text = Text2(symbol, {'font_size':60}).set_z_index(1)
        self.body = VGroup(self.disc, self.text).move_to(pos).scale(sf)

    def flip(self):
        if self.symbol == 'H':
            newsymbol = 'T'
        elif self.symbol == 'T':
            newsymbol = 'H'
        elif self.symbol == '0':
            newsymbol = '1'
        else:
            newsymbol = '0'
        newtext = Text2(newsymbol, {'font_size':60}).move_to(self.text).flip(UP)
        newtext.scale(self.scale).set_opacity(0)
        anim = AnimationGroup(
            self.disc.animate.flip(UP),
            self.text.animate.flip(UP).set_opacity(0),
            newtext.animate.flip(UP).set_opacity(1)
        )

        self.symbol = newsymbol
        self.text = newtext
        self.body = VGroup(self.disc, self.text)

        return anim

    def orbit(self, angle, sf, rad_sf, origin):
        pos = self.body.get_center() - origin
        rad = np.linalg.norm(pos)
        start_angle = math.atan2(pos[1], pos[0])

        self.scale *= sf

        original_body = self.body.copy()
        def update_fn(mobject, alpha):
            curr_angle = start_angle + (alpha * angle)
            x = rad * (1 + alpha * (rad_sf - 1)) * math.cos(curr_angle) + origin[0]
            y = rad * (1 + alpha * (rad_sf - 1)) * math.sin(curr_angle) + origin[1]
            curr_scale = 1.0 + (sf - 1.0) * alpha

            mobject.become(original_body).scale(curr_scale).move_to([x, y, 0])

        return UpdateFromAlphaFunc(self.body, update_fn)


def getfeel(coins, ids, rt=1):
    return AnimationGroup(*[Indicate(coins[id].body) for id in ids], run_time=rt, lag_ratio=0.075)

def getflash(bodies, ids, rad, rt=1):
    return AnimationGroup(*[Flash(bodies[id], flash_radius=rad) for id in ids], run_time=rt)

def getflips(coins, ids, rt=1):
    return AnimationGroup(*[coins[id].flip() for id in ids], lag_ratio=0.15, run_time=rt)

def getorbits(coins, angle, rt=1, sf=1, rad_sf=1, origin=ORIGIN):
    return AnimationGroup(*[coins[c].orbit(angle, sf, rad_sf, origin) for c in range(len(coins))], run_time=rt)

class Introduce(Scene):
    def part_a(self):
        bg_color = DARKER_GRAY
        light_room = Rectangle(width=20, height=10, fill_color=bg_color, fill_opacity=1).set_z_index(-10)
        self.add(light_room)

        coins = [Coin([2 * math.cos(PI * i / 2), 2 * math.sin(PI * i / 2), 0], 'H', 1) for i in range(4)]
        bodies = VGroup(*[coins[i].body for i in range(4)])

        self.play(FadeIn(bodies))
        self.wait(0.5)
        self.play(FadeOut(light_room), AnimationGroup(*[FadeOut(bodies[i][1]) for i in range(4)]))
        self.wait()
        self.play(getfeel(bodies, [0, 1], 1), FadeIn(coins[0].text), FadeIn(coins[1].text))
        self.wait(0.5)
        self.play(getflips(coins, [0, 1], 1))
        self.wait()
        self.play(getfeel(bodies, [2, 3], 1), FadeIn(coins[2].text), FadeIn(coins[3].text))
        self.wait(0.5)
        self.play(getflips(coins, [2, 3], 1))
        self.wait()
        self.play(getflips(coins, [3], 1))
        self.play(getorbits(coins, 13 * PI / 2, 4))
        self.wait()
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getorbits(coins, 4 * PI / 2, 1))
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getorbits(coins, 2 * PI / 2, 1))
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getorbits(coins, 6 * PI / 2, 1.5))
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getorbits(coins, 2 * PI / 2, 1))
        self.play(getfeel(bodies, [0, 2], 1))
        self.wait(2)
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getorbits(coins, 3 * PI / 2, 1))
        self.play(getfeel(bodies, [1, 2], 1))
        self.play(getorbits(coins, 7 * PI / 2, 2))
        self.wait(0.5)
        self.play(getfeel(bodies, [1, 3], 1))
        self.play(getflips(coins, [3], 1))
        self.wait()
        self.play(getflips(coins, [3], 1))
        self.play(getfeel(bodies, [0, 2], 1))
        self.play(getflips(coins, [0], 1))
        self.wait(0.5)
        self.play(getorbits(coins, 5 * PI / 2, 1.5))
        self.play(getfeel(bodies, [1, 2], 1))
        self.play(getflips(coins, [1, 2], 1))
        self.wait(0.5)
        self.play(getflips(coins, [1, 2], 1))
        self.play(getfeel(bodies, [2, 3], 1))
        self.play(getflips(coins, [2, 3], 1))
        self.wait(0.5)
        self.play(getorbits(coins, 5 * PI / 2, 1.5))
        self.play(getfeel(bodies, [1, 3], 1))
        self.play(getflips(coins, [1, 3], 1))
        self.wait()

    def morecoins(self):
        coins1 = [Coin([2 * math.cos(PI * i / 2), 2 * math.sin(PI * i / 2), 0], 'H', 1) for i in range(4)]
        bodies1 = VGroup(*[coins1[i].body for i in range(4)])
        self.add(bodies1)

        coins2 = [Coin([2 * math.cos(PI * i / 2), 2 * math.sin(PI * i / 2), 0], 'H', 1) for i in range(4)]
        bodies2 = VGroup(*[coins2[i].body for i in range(4)])

        self.wait(0.5)
        self.play(getorbits(coins1, PI / 8, 1.5, sf=0.9, rad_sf=1.5), getorbits(coins2, -PI / 8, 1, sf=0.9, rad_sf=1.5))

        coins = []
        for i in range(4):
            coins.append(coins2[i])
            coins.append(coins1[i])
        bodies = VGroup(*[coins[i].body for i in range(8)])
        self.add(bodies)
        self.remove(bodies1, bodies2)
        self.play(getflips(coins, [1, 3, 5, 7], 1))
        self.wait()
        self.play(getfeel(coins, [i for i in range(8)], 1))
        self.play(getflips(coins, [0, 1, 2, 4, 5, 6, 7], 1))
        self.wait(0.5)
        self.play(getorbits(coins, 5 * PI / 4, 1))
        # for i in range(8):
        #     bodies[i][0] = coins[i].disc
        #     bodies[i][1] = coins[i].text
        self.play(getfeel(coins, [1, 2, 3, 4], 1))

        self.play(getflips(coins, [2, 3, 4], 1))
        self.play(getorbits(coins, 9 * PI / 4, 1))
        self.play(getfeel(coins, [6, 7, 0, 1], 1))
        self.play(getflips(coins, [6, 0], 1))
        self.wait()
        self.play(getflips(coins, [0, 2, 3, 6], 1))
        self.wait(0.5)
        self.play(getorbits(coins, 7 * PI / 4, 1))
        self.play(getfeel(coins, [1, 2, 3, 4], 1))
        self.play(getflips(coins, [2, 3], 1))
        self.play(getorbits(coins, 1 * PI / 4, 1))
        self.play(getfeel(coins, [1, 2, 5, 6], 1))
        self.play(getflips(coins, [6], 1))
        self.play(getorbits(coins, 3 * PI / 4, 1))
        self.play(getfeel(coins, [1, 3, 5, 7], 1))
        self.wait()

        # symmetry
        self.play(AnimationGroup(*[coins[i].body.animate.shift(LEFT) for i in range(2, 6)]),
                  AnimationGroup(*[coins[i].body.animate.shift(RIGHT) for i in [0, 1, 6, 7]]))
        lines = VGroup()
        for i in range(4):
            lines.add(DoubleArrow(start=coins[i].body.get_center(), end=coins[i + 4].body.get_center(),
                                  buff=1.2, color=GREEN, stroke_width=8))
        self.play(AnimationGroup(FadeIn(lines), getflips(coins, [4], 1), lag_ratio=0.25))
        self.wait()

    def symmetry(self):
        symbols = ['T', 'T', 'H', 'T', 'T', 'T', 'H', 'H']
        coins = [Coin([3 * math.cos(-PI * i / 4 + PI * 3 / 8), 3 * math.sin(-PI * i / 4 + PI * 3 / 8), 0], symbols[i], 0.9) for i in range(8)]
        bodies = VGroup(*[coins[i].body for i in range(8)])
        self.add(bodies)
        self.wait(0.5)

        values = ['1' if symbols[i] == 'H' else '0' for i in range(8)]
        coins = [Coin([3 * math.cos(-PI * i / 4 + PI * 3 / 8), 3 * math.sin(-PI * i / 4 + PI * 3 / 8), 0], values[i], 0.9) for i in range(8)]
        temp = VGroup(*[coins[i].body for i in range(8)])
        self.play(Transform(bodies, temp))

        self.wait()
        divider = Line(start=[0, 4, 0], end=[0, -4, 0], stroke_width=6)
        self.play(Create(divider), bodies.animate.shift(LEFT * config.frame_width / 4).scale(0.8))
        for i in range(8):
            coins[i].scale *= 0.8

        new_pos = [UP * 2.5 + RIGHT * (i + 1) * 1.5 for i in range(4)] + [UP * 0.5 + RIGHT * (i + 1) * 1.5 for i in range(4)]
        sliced = VGroup(*[bodies[i].copy() for i in range(8)])
        self.play(AnimationGroup(*[sliced[i].animate.move_to(new_pos[i]) for i in range(8)], lag_ratio=0.1))
        self.wait()
        # show asymmetry generation
        opposite_arrow = DoubleArrow(start=bodies[0].get_center(), end=bodies[4].get_center(),
                                     buff=0.8, stroke_color=GREEN, stroke_width=8)
        vert_arrow = DoubleArrow(start=sliced[0].get_center(), end=sliced[4].get_center(),
                                 buff=0.6, stroke_color=YELLOW, stroke_width=8, tip_length=0.2,
                                 max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=5)
        asymmetry = VGroup(*[Text2('0' if symbols[i] == symbols[i + 4] else '1', {'font_size':60})
                           .shift(DOWN + RIGHT * (i + 1) * 1.5) for i in range(4)])

        self.play(AnimationGroup(Create(opposite_arrow), Create(vert_arrow), lag_ratio=0.25))
        self.play(ReplacementTransform(vert_arrow.copy(), asymmetry[0]))
        self.wait(0.5)

        for i in range(1, 4):
            self.play(AnimationGroup(
                Transform(opposite_arrow, DoubleArrow(start=bodies[i].get_center(), end=bodies[i + 4].get_center(),
                                                      buff=0.8, stroke_color=GREEN, stroke_width=8)),
                vert_arrow.animate.shift(RIGHT * 1.5),
                lag_ratio=0.25), run_time=0.75)
            self.play(ReplacementTransform(vert_arrow.copy(), asymmetry[i]), run_time=0.75)
        self.wait()

        sliced_coins = copy.deepcopy(coins)
        def reset():
            for i in range(8):
                sliced_coins[i].body = sliced[i]
                sliced_coins[i].disc = sliced[i][0]
                sliced_coins[i].text = sliced[i][1]
                sliced_coins[i].scale = coins[0].scale

                coins[i].body = bodies[i]
                coins[i].disc = bodies[i][0]
                coins[i].text = bodies[i][1]

        reset()

        for i in range(3):
            self.play(getorbits(coins, PI / 4, origin=bodies.get_center()), Rotate(opposite_arrow, PI / 4))
            self.play(AnimationGroup(*[sliced[j].animate.shift(LEFT * 1.5 if j % 4 != i else RIGHT * 4.5) for j in range(8)]),
                      AnimationGroup(*[asymmetry[j].animate.shift(LEFT * 1.5 if j != i else RIGHT * 4.5) for j in range(4)]),
                      vert_arrow.animate.shift(LEFT * 1.5), run_time=0.8)
            self.wait(0.5)
        self.play(FadeOut(opposite_arrow), FadeOut(vert_arrow))
        self.wait()

        self.play(AnimationGroup(getflash(bodies, [0, 4, 3, 7], 0.7), getflash(sliced, [0, 4, 3, 7], 0.7)))
        self.wait(0.5)

        self.play(AnimationGroup(getflips(coins, [3]), getflips(sliced_coins, [3]),
                                 Transform(asymmetry[3], Text2('0', {'font_size': 60}).shift(DOWN + RIGHT * 1.5)),
                                 lag_ratio=0.25))
        bodies[3] = coins[3].body
        sliced[3] = sliced_coins[3].body
        self.wait(0.5)
        reset()

        # solve for 4 coins
        instructions = VGroup()
        instruction = Text2('Make an opposite pair 1', {'font_size':30}).shift(RIGHT * 32 / 9 + DOWN * 2.5)
        instructions.add(instruction)
        self.play(Write(instruction))
        self.play(AnimationGroup(getflash(bodies, [0, 2, 4, 6], 0.7), getflash(sliced, [0, 2, 4, 6], 0.7)))
        self.play(AnimationGroup(getflips(coins, [0, 4]), getflips(sliced_coins, [0, 4]), lag_ratio=0.25))

        instruction = Text2('Make an adjacent pair 1', {'font_size': 30}).shift(RIGHT * 32 / 9 + DOWN * 2.5)
        instructions.add(instruction)
        self.play(Write(instructions[1]), instructions[0].animate.shift(DOWN * 0.6).set_opacity(0.4))
        self.play(AnimationGroup(getflash(bodies, [0, 1, 4, 5], 0.7), getflash(sliced, [0, 1, 4, 5], 0.7)))
        self.play(AnimationGroup(getflips(coins, [1, 5]), getflips(sliced_coins, [1, 5]), lag_ratio=0.25))



        self.wait()


    def construct(self):
        self.symmetry()

class Solution(Scene):
    def construct(self):
        self.wait(0.5)
        title = Tex("$2^n$ Coin Strategy ($n > 2$)").scale(1.5).to_edge(UP)
        line = Line(LEFT * 3, RIGHT * 3).next_to(title, DOWN)
        self.play(Write(title), Create(line))
        self.wait(0.5)

        algorithm = VGroup(Tex(r"- Assume symmetric, and try solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft"),
                           Tex(r"- If failed, the state is asymmetric. Flip one coin from each\\ opposite pair.", tex_environment="flushleft"),
                           Tex(r"- Once again, try solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft"),
                           Tex(r"- If failed, the asymmetry is neither $0\dots00$ or all $1\dots11$. Solve the\\ asymmetry.", tex_environment="flushleft"),
                           Tex(r"- Now, try solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft"),
                           Tex(r"- If failed, the asymmetry is all 1. Flip one coin from each\\ opposite pair.", tex_environment="flushleft"),
                           Tex(r"- Now we must be symmetric. Solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft")
                           ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).next_to(line, DOWN)

        algorithm2 = VGroup(Tex(r"- Assume symmetric, and try solve both halves of $2^{n - 1}$ coins. If\\ you find asymmetry, skip to next step.", tex_environment="flushleft"),
                           Tex(r"- If you did not find a symmetric pair, to eliminate possibility of\\"
                               r" asymmetry $1\dots11$, flip one coin from each opposite pair.", tex_environment="flushleft"),
                           Tex(r"- Once again, try solve both halves of $2^{n - 1}$ coins. If you find\\"
                               r" asymmetry, skip to next step.", tex_environment="flushleft"),
                           Tex(r"- Due to previous steps, the asymmetry is not $1\dots11$. Solve the\\ asymmetry.", tex_environment="flushleft"),
                           Tex(r"- Now we must be symmetric. Solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft"),
                            ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).next_to(line, DOWN)
        self.play(Write(algorithm))
        self.wait()

        self.play(Unwrite(algorithm[1:6]))
        self.play(FadeTransform(algorithm[0], algorithm2[0][0][:50]), Write(algorithm2[0][0][50:]),
                  Write(algorithm2[1:4]), ReplacementTransform(algorithm[6], algorithm2[4]))
        self.remove(algorithm[0])
        self.add(algorithm2[0])
        self.wait()

        algorithm3 = VGroup(Tex(r"- Take 2 opposite pairs and make one asymmetric and one symmetric.", tex_environment="flushleft"),
                            Tex(r"- The asymmetry is neither $0\dots00$ or $1\dots11$. Solve the asymmetry.", tex_environment="flushleft"),
                            Tex(r"- Try solve both halves. If you find the asymmetry is $1\dots11$, skip to\\ next step.", tex_environment="flushleft"),
                            Tex(r"- The asymmetry must be $1\dots11$. Flip one coin from each opposite\\ pair to make it $0\dots00$.", tex_environment="flushleft"),
                            Tex(r"- Now we must be symmetric. Solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft")
                            ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).next_to(line, DOWN)
        self.play(Unwrite(algorithm2[:-1]), ReplacementTransform(algorithm2[-1], algorithm3[-1]))
        self.play(Write(algorithm3[:-1]))
        self.wait()

        algorithm4 = VGroup(Tex(r"- Solve asymmetry. If we started out symmetric, nothing  is affected.", tex_environment="flushleft"),
                            Tex(r"- Try solve both halves of $2^{n - 1}$ coins. If we detect asymmetry\\"
                                r"after the first move, it must be $1\dots11$. Stop.", tex_environment="flushleft"),
                            Tex(r"- Flip one coin from each opposite pair to make symmetry.", tex_environment="flushleft"),
                            Tex(r"- Now we must be symmetric. Solve both halves of $2^{n - 1}$ coins.", tex_environment="flushleft")
                            ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).next_to(line, DOWN)
        self.play(Unwrite(algorithm3[:-1]), ReplacementTransform(algorithm3[-1], algorithm4[-1]))
        self.play(Write(algorithm4[:-1]))
        self.wait()

class Four(Scene):
    def construct(self):
        self.wait(0.5)
        title = Tex("4 Coin Strategy").scale(2).to_edge(UP)
        line = Line(LEFT * 2.5, RIGHT * 2.5).next_to(title, DOWN)
        self.play(Write(title), Create(line))
        self.wait(0.5)

        algorithm = VGroup(Tex(r"- Make an opposite pair heads.", tex_environment="flushleft"),
                           Tex(r"- Make an adjacent pair heads.", tex_environment="flushleft"),
                           Tex(r"If we are not done, there is exactly one tail. Feel an opposite pair.", tex_environment="flushleft"),
                           Tex(r"- If you find the tail, flip it, otherwise flip exactly one head.", tex_environment="flushleft"),
                           Tex(r"- If we are not done, we are in a rotation of HHTT.\\ Flip a pair of adjacent coins.", tex_environment="flushleft"),
                           Tex(r"- If we are not done, we must be in a rotation of HTHT.\\ Flip a pair of opposite coins.", tex_environment="flushleft")
                           ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).shift(DOWN * 0.5)
        self.play(Write(algorithm))
        self.wait()

        annotated = VGroup(Tex(r"- Make an opposite pair heads.", tex_environment="flushleft"),
                           Tex(r"- Make an adjacent pair heads.", tex_environment="flushleft"),
                           Tex(r"If we are not done, there is exactly one tail. Feel an opposite pair."),
                           Tex(r"(asymmetry = $01$)", tex_environment="flushleft", color=BLUE),
                           Tex(r"- If you find the tail, flip it, otherwise flip exactly one head.", tex_environment="flushleft"),
                           Tex(r"- If we are not done, we are in a rotation of HHTT.\\ Flip a pair of adjacent coins.", tex_environment="flushleft"),
                           Tex(r"- If we are not done, we must be in a rotation of HTHT.\\ Flip a pair of opposite coins.", tex_environment="flushleft")
                           ).arrange(DOWN, aligned_edge=LEFT).scale(0.9).shift(DOWN * 0.5)
        self.play(Transform(algorithm[:3], annotated[:3]), Transform(algorithm[3:], annotated[4:]), Write(annotated[3]))
        self.wait()

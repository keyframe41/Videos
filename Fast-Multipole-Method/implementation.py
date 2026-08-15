from manim import *
import matplotlib.pyplot as plt
import numpy as np
import math

class Horner(Scene):
    def construct(self):
        example = Tex("Example when ", "$p = 5$")
        working = VGroup(MathTex("P_{ME}(z) =", "a_0\log(z) +", "\sum_{k = 1}^5 a_k z^{-k}"),
                         MathTex("= a_0\log(z) +", "a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3} + a_4 z^{-4} + a_5 z^{-5}"),
                         MathTex("= a_0\log(z) +", "a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3} + z^{-4}(a_4 + a_5 z^{-1})"),
                         MathTex("= a_0\log(z) +", "a_1 z^{-1} + a_2 z^{-2} + z^{-3}(a_3  + z^{-1}(a_4 + a_5 z^{-1}))"),
                         MathTex("= a_0\log(z) +", "a_1 z^{-1} + z^{-2}(a_2 + z^{-1}(a_3  + z^{-1}(a_4 + a_5 z^{-1})))"),
                         MathTex("= a_0\log(z) +", "z^{-1}(a_1 + z^{-1}(a_2 + z^{-1}(a_3  + z^{-1}(a_4 + a_5 z^{-1}))))"),
                         )
        working[0][0][4].set_color(BLUE)
        working[0][1][:2].set_color(YELLOW)
        working[0][1][6].set_color(BLUE)
        for i in range(1, 6):
            working[i][0][1:3].set_color(YELLOW)
            working[i][0][7].set_color(BLUE)
        working[0][2][5:7].set_color(YELLOW)
        working[0][2][7].set_color(BLUE)
        for j in range(4):
            for i in range(4 - j):
                working[j + 1][1][6 * i:6 * i + 2].set_color(YELLOW)
                working[j + 1][1][6 * i + 2].set_color(BLUE)
        for j in range(5):
            working[j + 1][1][-3 - j].set_color(BLUE)
            working[j + 1][1][-5 - j:-3 - j].set_color(YELLOW)
            for i in range(j):
                working[j + 1][1][-j - 7 * i - 8 : -j - 7 * i - 6].set_color(YELLOW)
                working[j + 1][1][-j - 7 * i - 12].set_color(BLUE)

        working[1:].next_to(working[0], DOWN)
        working.center()

        self.wait(0.5)
        self.play(Write(working[0]))
        self.wait()
        self.play(ReplacementTransform(working[0][0][-1].copy(), working[1][0][0]),
                  ReplacementTransform(working[0][1].copy(), working[1][0][1:]),
                  Write(working[1][1]), run_time=1.5)
        self.wait()
        self.play(ReplacementTransform(working[1][0], working[2][0]),
                  ReplacementTransform(working[1][1][:18], working[2][1][:18]),
                  ReplacementTransform(working[1][1][20:23], working[2][1][18:21]),
                  ReplacementTransform(working[1][1][26:29].copy(), working[2][1][18:21]),
                  FadeIn(working[2][1][21]), FadeIn(working[2][1][-1]),
                  ReplacementTransform(working[1][1][18:20], working[2][1][22:24]),
                  ReplacementTransform(working[1][1][23:26], working[2][1][24:27]),
                  ReplacementTransform(working[1][1][26:29], working[2][1][27:30]), run_time=0.75)
        self.wait(0.5)

        self.play(ReplacementTransform(working[2][0], working[3][0]),
                  ReplacementTransform(working[2][1][:12], working[3][1][:12]),
                  ReplacementTransform(working[2][1][14:17], working[3][1][12:15]),
                  FadeIn(working[3][1][15]), FadeIn(working[3][1][-1]),
                  ReplacementTransform(working[2][1][12:14], working[3][1][16:18]),
                  ReplacementTransform(working[2][1][17:21], working[3][1][18:22]),
                  ReplacementTransform(working[2][1][18:21].copy(), working[3][1][12:15]),
                  ReplacementTransform(working[2][1][21:], working[3][1][22:-1]), run_time=0.75
                  )
        self.play(ReplacementTransform(working[3][0], working[4][0]),
                  ReplacementTransform(working[3][1][:6], working[4][1][:6]),
                  ReplacementTransform(working[3][1][8:11], working[4][1][6:9]),
                  FadeIn(working[4][1][9]), FadeIn(working[4][1][-1]),
                  ReplacementTransform(working[3][1][6:8], working[4][1][10:12]),
                  ReplacementTransform(working[3][1][11:15], working[4][1][12:16]),
                  ReplacementTransform(working[3][1][12:15].copy(), working[4][1][6:9]),
                  ReplacementTransform(working[3][1][15:], working[4][1][16:-1]), run_time=0.75
                  )
        self.play(ReplacementTransform(working[4][0], working[5][0]),
                  ReplacementTransform(working[4][1][2:5], working[5][1][:3]),
                  FadeIn(working[5][1][3]), FadeIn(working[5][1][-1]),
                  ReplacementTransform(working[4][1][:2], working[5][1][4:6]),
                  ReplacementTransform(working[4][1][5:9], working[5][1][6:10]),
                  ReplacementTransform(working[4][1][6:9].copy(), working[5][1][:3]),
                  ReplacementTransform(working[4][1][9:], working[5][1][10:-1]), run_time=0.75
                  )
        self.wait()

def subdivide(rect):
    yorange = (YELLOW + ORANGE) / 2
    d = [[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]
    len = rect.width
    center = rect.get_center()
    return VGroup(Rectangle(width=len / 2, height=len / 2, stroke_width=3).move_to(
        center + len * (d[i][0] * RIGHT + d[i][1] * UP)) for i in range(4)).set_color(yorange)

def get_nonuniform_grid():
    yorange = (YELLOW + ORANGE) / 2
    layers = VGroup(Rectangle(height=6, width=6, stroke_width=3.5))
    layers.add(subdivide(layers[0]))
    layers.add(subdivide(layers[1][0]))
    layers[2].add(*subdivide(layers[1][1]))
    layers[2].add(*subdivide(layers[1][2]))
    next = [3, 4, 5, 7, 8]
    layers.add(subdivide(layers[2][2]))
    for i in next:
        layers[-1].add(*subdivide(layers[2][i]))
    layers.add(subdivide(layers[3][2]))
    next = [16, 17, 19, 20, 23]
    for i in next:
        layers[-1].add(*subdivide(layers[3][i]))
    layers.add(subdivide(layers[4][6]))
    layers[-1].add(*subdivide(layers[4][13]))

    return layers

def get_nonuniform_coords():
    return [[-0.22, -0.61], [-2.190882637017235, -2.3307649007897226], [-1.8259480403643802, -2.099312602990542], [-3.7114040015885825, -0.4288963490779629], [-3.925321344625077, 3.3376003696368426], [-2.360596779079171, 3.652358968328466], [-1.2397476745664155, 3.997044358216298], [-1.0880914153576249, 3.4951364903137927], [2.2781798282490766, 0.3321463224106742], [2.312649556537804, 1.7802413526177914], [3.7173784557988787, 1.6330261909375159], [3.134138874097439, -0.3541280729776095], [2.9034626181813383, -0.12723524923982454], [2.4153717722216537, -1.610268207096759], [2.0599071868968206, -2.0071708625045295], [3.2822719001397713, -2.420176112905659], [3.254279269840854, -2.968948446009802], [2.4843739176506707, -3.4270411297251364], [0.07625895634735325, -3.912220947487892], [0.17183269846636695, -2.824154960380942], [1.9283984761288646, -3.8478984060249957], [1.714987990722574, -2.1300451198456107], [-1.573367817677806, 1.2904424130977197], [-0.5585728965960837, 1.5343075500950933], [-0.43354283921971115, 1.0813562623181872], [-0.9674492870304318, 1.626239647274892], [-0.1409415478249767, 1.5163960805818748], [-0.6053221377797711, 1.1130976004185467], [-1.3673058276155483, 0.01814121286473236], [-1.3273355710292225, 0.9051219050548516], [-1.727740232633351, 0.8386751688723261], [-3.022292398250717, 1.6013507347178977], [-3.1004376770526667, 1.246539015747547], [-2.475451602611189, 1.4218254272477786], [-2.2039944091157597, 0.5492150410512011], [-2.5133754943573843, 0.7902446732114669], [-3.5702144312293376, 0.4659979686293564], [-3.2002731024773254, 0.517073814535369], [-3.5844873361795226, 0.6626351859125472], [0.02292749316779985, 3.790627843122812], [1.0500866863120715, 3.2120917578129884], [1.0305770573399666, 2.460707873084135], [1.6576211260676665, 2.561930420899161], [1.392382540307276, 2.880235335226101], [1.5684577751666215, 2.1493332696782597], [0.0943855339502746, 2.420867951382236], [0.49584518847417625, 2.3319686134812896], [0.6650145050896604, 2.162971173464142], [0.1909520843875836, 2.44045954098873], [0.060335896379740905, 2.863219124801654], [2.3252886002400213, 3.5121707378081632], [2.93708902961809, 3.6471169115296203], [3.6952561325698303, 3.147058760519564], [3.8567132879871022, 3.59316281180975], [3.31892447772852, 2.1013158232021585], [3.883599307330112, 2.7320622171366193], [3.3522908754944036, 2.288498610257695], [3.656417385093811, 2.527851275906435], [3.571855242582719, 2.194984672313272], [2.896785251035194, 2.887874470948282], [2.3266112795324547, 2.5149257400229326], [2.7266266806711874, 2.3631575286597934], [1.0101301793591104, 0.9805404988390501], [1.0881817879126197, 0.49206405449097734], [1.131844426473592, -0.9850458116315164], [1.709601769943782, -0.7546947662653449], [1.6025525105865488, -0.9860983732542568], [1.641848361200134, -0.03584770344958521], [1.5967477775360444, -0.36070381083346714], [1.091249157014503, -1.8502874673998344], [1.5543436549279268, -1.762421238263454], [0.8644470264429095, -1.2194525920605206], [-0.6623646406459831, 0.9981433142279863], [-0.09167483894276268, 0.5106297786083109], [-0.12881071018324547, 0.8316741621160423], [-0.2853827992990969, 0.13879293738247184], [-0.25032997500630916, 0.29832009371687357], [-0.09900461101567098, 0.2924076109357151], [-0.7533047073232612, 0.23908783808625744], [-0.999265629600324, 0.07937357947237567], [0.11957006685807087, 1.744520906831808], [0.23793555245997589, 1.6549602468033386], [0.11913722791584003, 1.6841026195444935], [0.025228768789886835, 1.8706286673247536], [0.8823035323573987, 1.9769165013597867], [0.7231621903387777, 1.9590481682386578], [0.904677370521316, 1.6698579732266334], [0.9518066642219243, 1.983374877643855], [0.41453464345584784, 1.3421914769299965], [0.439085091912776, 1.1548266750094627], [1.252586833149532, 1.704428868637381], [1.370098575374388, 1.5735707921760609], [1.2063875373284807, 1.7837787035124997], [1.662330753182145, 1.6219924821099636], [1.511311063977415, 1.7292850589291637], [1.6308594474042881, 1.6000089090041754], [1.8043645683056186, 1.7914380215341779], [1.672656264408714, 1.1595954750913378], [1.8110774566264192, 1.1372655700603402], [1.7573931884225313, 1.0686636238486822], [1.0696224668049021, 1.274446698454598], [1.4088315076785074, 1.004900475767847], [1.1322098319999983, 1.016057093359164], [0.43175637163355807, 0.5355274069512485], [0.035199137790023205, 0.9215597063074488], [0.7800133884772023, 0.41789694023303464], [0.8758166337383367, 0.18477788010951107], [0.16728480935102746, 0.005352589191141399], [0.2994015032812539, 0.23252946414538544], [0.041014041144600666, 0.18137466587692086], [0.07708108695501048, 0.4147354053469216], [0.4335321563058419, -0.058283912648240566], [0.34943831955849014, -0.4787916902907501], [0.24864222668441582, -0.401336241875471], [0.9322552319632191, -0.2992066861886782], [0.8878295750093428, -0.3717174480823124], [0.9617315639664269, -0.8563710537963548], [0.21761750622560427, -0.9225422258188778], [0.4338466079503298, -0.5269627408682397], [0.3295511830600923, -0.9995000654046029], [0.34, -1.36], [0.67, -1.21], [0.71, -1.83], [0.91, -1.54], [0.55, -1.68], [0.5528457160852255, 1.3330458101325748], [0.7594202428901234, 1.3098797816116923], [0.8505258785210006, 1.1656430190811906], [0.8349137066555095, 1.1046689549792204], [0.8819026595324607, 1.17126484763934], [0.7084315884259876, 1.0001833089144916], [0.6893176697122638, 1.1167234968610285], [0.5905638395959827, 0.8379383135467161], [0.7171695910800893, 0.9738949090192672], [0.7315865819944674, 0.9095733585548811], [0.8837967758904027, 0.807696735999147], [0.7876668680042425, 0.9767760340098222], [0.7945129382405061, 0.8656736241388365], [0.8901733933477969, 0.6993036549465275], [0.5876487878811257, 0.5502441075657741], [0.6264094371778175, 0.5827857456971952], [0.6544408651994186, 0.5047244868240588]]

class Partitioning(Scene):
    def construct(self):
        yorange = (YELLOW + ORANGE) / 2
        quadtree = get_nonuniform_grid().set_color(BLUE).to_edge(DOWN)
        nu_coords = get_nonuniform_coords()
        n = len(nu_coords)
        coords = []

        def filter1(center, radius):
            ids = []
            for i in range(n):
                if abs(center[0] - nu_coords[i][0]) < radius and abs(center[1] - nu_coords[i][1]) < radius:
                    ids.append(i)
            return ids

        leaves = [[-3, 3, 1], [-1, 3, 1], [-1.5, 1.5, 0.5], [-0.5, 1.5, 0.5], [-0.75, 0.75, 0.25], [-0.25, 0.75, 0.25], [-0.25, 0.25, 0.25], [-0.75, 0.25, 0.25], [-1.5, 0.5, 0.5], [-3.5, 1.5, 0.5], [-2.5, 1.5, 0.5], [-2.5, 0.5, 0.5], [-3.5, 0.5, 0.5],
                  [0.5, 3.5, 0.5], [1.5, 3.5, 0.5], [1.5, 2.5, 0.5], [0.5, 2.5, 0.5], [2.5, 3.5, 0.5], [3.5, 3.5, 0.5], [3.5, 2.5, 0.5], [2.5, 2.5, 0.5], [3, 1, 1], [0.25, 1.75, 0.25], [0.75, 1.75, 0.25], [0.625, 1.375, 0.125], [0.875, 1.375, 0.125], [0.875, 1.125, 0.125], [0.625, 1.125, 0.125], [0.25, 1.25, 0.25],
                  [1.25, 1.75, 0.25], [1.75, 1.75, 0.25], [1.75, 1.25, 0.25], [1.25, 1.25, 0.25], [1.5, 0.5, 0.5], [0.25, 0.75, 0.25], [0.675, 0.875, 0.125], [0.875, 0.875, 0.125], [0.875, 0.625, 0.125], [0.625, 0.625, 0.125], [0.75, 0.25, 0.25], [0.25, 0.25, 0.25],
                  [0.25, -0.25, 0.25], [0.75, -0.25, 0.25], [0.75, -0.75, 0.25], [0.25, -0.75, 0.25], [1.5, -0.5, 0.5], [1.5, -1.5, 0.5], [0.25, -1.25, 0.25], [0.75, -1.25, 0.25], [0.75, -1.75, 0.25], [0.25, -1.75, 0.25], [3, -1, 1], [3, -3, 1], [1, -3, 1], [-2, -2, 2]]
        for leaf in leaves:
            ids = filter1([leaf[0], leaf[1]], leaf[2])
            coords += [nu_coords[i] for i in ids]

        x_min, x_max = -4, 4
        y_min, y_max = -4, 4
        plane_size = 6

        cmap = plt.get_cmap("gist_rainbow")

        plane = ComplexPlane(x_range=[x_min, x_max, 1], y_range=[y_min, y_max, 1],
                             x_length=plane_size, y_length=plane_size,
                             axis_config={"color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             background_line_style={"stroke_color": BLUE, "stroke_width": 2.5, "stroke_opacity": 0.35},
                             faded_line_style={"stroke_color": BLUE, "stroke_width": 1.0, "stroke_opacity": 0.2},
                             faded_line_ratio=5).to_edge(DOWN)
        border = SurroundingRectangle(plane, color=BLUE, buff=0, stroke_width=3).set_z_index(5)
        self.wait(0.5)
        self.play(FadeIn(plane), Write(border))
        self.wait()

        sources = VGroup([Dot(radius=DEFAULT_SMALL_DOT_RADIUS, color=ManimColor(cmap(i / n)))
        .move_to(plane.c2p(coords[i][0], coords[i][1])) for i in range(n)]).set_z_index(10)

        self.play(FadeIn(sources), FadeIn(quadtree))
        self.wait()


        rand = [27, 128, 47, 94, 1, 97, 129, 126, 5, 91, 134, 21, 74, 77, 15, 29, 71, 55, 22, 35, 34, 72, 133, 63, 54, 104, 95, 0, 89, 73, 46, 120, 40, 2, 85, 101, 8, 127, 121, 50, 20, 83, 37, 18, 125, 49, 82, 16, 13, 99, 52, 93, 114, 67, 42, 12, 131, 140, 81, 75, 33, 24, 70, 3, 60, 112, 14, 103, 23, 84, 66, 111, 68, 78, 118, 141, 43, 38, 69, 30, 57, 44, 7, 137, 123, 19, 61, 4, 107, 108, 124, 32, 53, 10, 96, 79, 51, 106, 105, 31, 86, 48, 9, 136, 36, 115, 90, 100, 116, 45, 135, 25, 58, 17, 113, 119, 39, 138, 117, 56, 11, 80, 62, 64, 98, 102, 65, 6, 132, 41, 122, 139, 88, 76, 87, 26, 92, 28, 109, 110, 59, 130]
        ideal_dots = VGroup([Dot(radius=DEFAULT_SMALL_DOT_RADIUS, color=ManimColor(cmap(i / n)))
                             .move_to(UP * 3 + 14 * RIGHT * (i - n / 2 + 0.5) / n) for i in range(n)])
        dots = VGroup([Dot(radius=DEFAULT_SMALL_DOT_RADIUS, color=ManimColor(cmap(i / n)))
                             .move_to(UP * 3 + 14 * RIGHT * (rand[i] - n / 2 + 0.5) / n) for i in range(n)])
        self.play(AnimationGroup(*[ReplacementTransform(sources[i].copy(), dots[i]) for i in range(n)], lag_ratio=0.01))
        self.wait()
        self.play(Transform(dots, ideal_dots), run_time=2)
        self.wait()

        def filter2(center, radius):
            min_id = 1000
            max_id = 0
            for i in range(n):
                if abs(center[0] - coords[i][0]) < radius and abs(center[1] - coords[i][1]) < radius:
                    min_id = min(min_id, i)
                    max_id = max(max_id, i)
            return min_id, max_id

        a, b = filter2([-3, 1], 1)
        targets = VGroup()
        temp = Rectangle(width=14 * (b - a + 2) / n, height=0.3, color=yorange).move_to(UP * 3 + 14 * RIGHT * ((a + b - n + 1) / (2 * n)))
        targets.add(temp)
        temp = quadtree[2][3].copy().set_z_index(6)
        self.play(temp.animate.set_color(yorange), run_time=0.5)
        self.play(ReplacementTransform(temp, targets[0]))

        a, b = filter2([3.5, 2.5], 0.5)
        temp = Rectangle(width=14 * (b - a + 2) / n, height=0.3, color=yorange).move_to(UP * 3 + 14 * RIGHT * ((a + b - n + 1) / (2 * n)))
        targets.add(temp)
        temp = quadtree[3][14].copy().set_z_index(6)
        self.play(temp.animate.set_color(yorange), run_time=0.5)
        self.play(ReplacementTransform(temp, targets[1]))

        a, b = filter2([2, -2], 2)
        temp = Rectangle(width=14 * (b - a + 2) / n, height=0.3, color=yorange).move_to(UP * 3 + 14 * RIGHT * ((a + b - n + 1) / (2 * n)))
        targets.add(temp)
        temp = quadtree[1][2].copy().set_z_index(6)
        self.play(temp.animate.set_color(yorange), run_time=0.5)
        self.play(ReplacementTransform(temp, targets[2]))

        a, b = filter2([0.75, 0.75], 0.25)
        temp = Rectangle(width=14 * (b - a + 2) / n, height=0.3, color=yorange).move_to(UP * 3 + 14 * RIGHT * ((a + b - n + 1) / (2 * n)))
        targets.add(temp)
        temp = quadtree[4][13].copy().set_z_index(6)
        self.play(temp.animate.set_color(yorange), run_time=0.5)
        self.play(ReplacementTransform(temp, targets[3]))
        self.wait()

class ParamS(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 150, 10], y_range=[0, 25, 5], axis_config={"include_numbers": True}, tips=False)
        self.add(ax)

        labels = ax.get_axis_labels("s", r"\text{Mean time per frame (ms)}").set_z_index(10)
        self.wait(0.5)
        self.play(Write(labels))
        self.wait()
        files = [open("TimeData/s_parameter/" + str(10 * i) + ".txt", "r") for i in range(3, 13)]
        raw = [files[i].readlines() for i in range(10)]
        data = [raw[i][1:] for i in range(10)]
        means = list(map(float, [raw[i][0].split(' ')[1] for i in range(10)]))
        for i in range(1800):
            for j in range(10):
                data[j][i] = float(data[j][i][:-1])
        for i in range(1800):
            for j in range(10):
                if data[j][i] > means[j] + 4:
                    data[j][i] = means[j]
        tracker = ValueTracker(0)
        frame = always_redraw(lambda: Text("Frame " + str(round(1800/1799 * tracker.get_value()))).set_color(BLUE).shift(DOWN * 2.2))
        dots = always_redraw(lambda: VGroup([
            Dot(color=BLUE).move_to(ax.c2p(30 + 10 * i, data[i][round(tracker.get_value())])) for i in range(10)
        ]).set_z_index(10))

        ub = always_redraw(lambda: VGroup([
            Line(LEFT * 0.05, RIGHT * 0.05, color=YELLOW).move_to(ax.c2p(30 + 10 * i, np.max(data[i][:round(tracker.get_value() + 1)])))
            for i in range(10)
        ]))
        lb = always_redraw(lambda: VGroup([
            Line(LEFT * 0.05, RIGHT * 0.05, color=YELLOW).move_to(ax.c2p(30 + 10 * i, np.min(data[i][:round(tracker.get_value() + 1)])))
            for i in range(10)
        ]))
        vert = always_redraw(lambda: VGroup([
            Line(ax.c2p(30 + 10 * i, np.min(data[i][:round(tracker.get_value() + 1)])),
                 ax.c2p(30 + 10 * i, np.max(data[i][:round(tracker.get_value() + 1)])), color=YELLOW) for i in range(10)
        ]))

        self.play(Write(dots), FadeIn(ub), FadeIn(lb), FadeIn(vert), Write(frame))
        self.play(tracker.animate.set_value(1799), rate_func=linear, run_time=5)
        dots.clear_updaters()
        ub.clear_updaters()
        lb.clear_updaters()
        vert.clear_updaters()
        frame.clear_updaters()
        ranges = VGroup(ub, lb, vert)

        mean_dots = VGroup([Dot(color=BLUE).move_to(ax.c2p(30 + 10 * i, means[i])) for i in range(10)]).set_z_index(10)
        self.wait()
        self.play(Transform(dots, mean_dots), ranges.animate.set_opacity(0.3), FadeOut(frame))
        self.wait()
        eq = VGroup(MathTex(r"T = N\left(\frac{92.5ap^3}{s} + 64bp^2 + 22cps + 3dp + e\right)"),
                    MathTex(r"T= \frac{A}{s} + Bs + C"))
        eq[0][0][0].set_color(GREEN)
        eq[1][0][0].set_color(GREEN)
        eq[0][0][12].set_color(BLUE)
        eq[0][0][24].set_color(BLUE)
        eq[1][0][4].set_color(BLUE)
        eq[1][0][7].set_color(BLUE)
        eq.shift(DOWN * 2.2)
        self.play(Write(eq[0]))
        self.wait(0.5)
        self.play(ReplacementTransform(eq[0][0][:2], eq[1][0][:2]), FadeOut(eq[0][0][3]), FadeOut(eq[0][0][-1]),
                  ReplacementTransform(eq[0][0][2], eq[1][0][2]), ReplacementTransform(eq[0][0][2].copy(), eq[1][0][6]),
                  ReplacementTransform(eq[0][0][2].copy(), eq[1][0][9]), ReplacementTransform(eq[0][0][4:11], eq[1][0][2]),
                  ReplacementTransform(eq[0][0][11:13], eq[1][0][3:5]),
                  ReplacementTransform(eq[0][0][14:19], eq[1][0][9]), ReplacementTransform(eq[0][0][13], eq[1][0][8]),
                  ReplacementTransform(eq[0][0][19], eq[1][0][5]), ReplacementTransform(eq[0][0][20:24], eq[1][0][6]),
                  ReplacementTransform(eq[0][0][24], eq[1][0][7]),
                  ReplacementTransform(eq[0][0][25], eq[1][0][8]), ReplacementTransform(eq[0][0][26:29], eq[1][0][9]),
                  ReplacementTransform(eq[0][0][29], eq[1][0][8]), ReplacementTransform(eq[0][0][30], eq[1][0][9]),
                  )
        self.wait()

        graph = ax.plot(lambda x: 0.0849672 * x + 300.86565 / x + 4.19209, x_range=[1, 150, 1]).set_color(GREEN)
        self.play(Create(graph))
        self.wait()

        tangent = ax.plot(lambda x: 14.3, x_range=[0, 150]).set_color(YELLOW)
        vert = Line(ax.c2p(60, 14.3), ax.c2p(60, 0)).set_color(YELLOW)
        self.play(AnimationGroup([Create(tangent), Write(vert)], lag_ratio=0.5), eq[1].animate.shift(RIGHT * 3))
        self.wait()

        files = [open("TimeData/s_parameter/" + str(10 * i) + "'.txt", "r") for i in range(3, 13)]
        other_means = list(map(float, [files[i].readlines()[0].split(' ')[1] for i in range(10)]))
        other_mean_dots = VGroup([Dot(color=BLUE_B).move_to(ax.c2p(30 + 10 * i, other_means[i])) for i in range(10)]).set_z_index(10)
        self.play(FadeOut(tangent), dots.animate.set_opacity(0.5), graph.animate.set(stroke_opacity=0.5))

        self.play(Write(other_mean_dots))
        self.wait()

        other_graph = ax.plot(lambda x: 0.109959 * x + 366.25945 / x + 0.7051, x_range=[1, 150, 1]).set_color(GREEN_D)
        self.play(Create(other_graph))
        self.wait()

        ax2 = Axes(x_range=[0, 22, 2], y_range=[0, 30, 5], axis_config={"include_numbers": True}, tips=False)
        labels2 = ax2.get_axis_labels("p", r"\text{Mean time per frame (ms)}").set_z_index(10)
        self.play(FadeOut(graph), FadeOut(other_graph), FadeOut(dots), FadeOut(other_mean_dots), FadeOut(vert),
                  FadeOut(eq[1]), FadeOut(ranges),
                  Transform(ax, ax2), Transform(labels, labels2))
        self.wait()

        files = [open("TimeData/p/" + str(2 + 2 * i) + ".txt", "r") for i in range(10)]
        means = list(map(float, [files[i].readlines()[0].split(' ')[0] for i in range(10)]))
        mean_dots = VGroup([Dot(color=BLUE).move_to(ax2.c2p(2 + 2 * i, means[i])) for i in range(10)]).set_z_index(10)
        eq = MathTex(r"T_{min} = N(\alpha p^2 + \beta p + \gamma)").shift(DOWN * 2.2)
        eq[0][:4].set_color(GREEN)
        eq[0][8].set_color(BLUE)
        eq[0][12].set_color(BLUE)
        self.play(Write(mean_dots), Write(eq))
        self.wait()
        graph = ax2.plot(lambda x: 0.026444 * x ** 2 + 0.204031 * x + 9.69934)
        self.play(Create(graph))
        self.wait()

        ax3 = Axes(x_range=[0, 130, 10], x_length=10, y_range=[10, 16, 1], axis_config={"include_numbers": True}, tips=False)
        labels3 = ax3.get_axis_labels(r"\text{Number of normally distributed particles (thousands)", r"\text{Mean time per frame (ms)}").set_z_index(10)
        self.play(FadeOut(graph), FadeOut(mean_dots), FadeOut(eq), Transform(ax, ax3), Transform(labels, labels3))
        self.wait()

        files = [open("TimeData/Concentration/" + str(10 * i) + "+" + str(120 - 10 * i) + ".txt", "r") for i in range(13)]
        means = list(map(float, [files[i].readlines()[0].split(' ')[1] for i in range(13)]))
        mean_dots = VGroup([Dot(color=BLUE).move_to(ax3.c2p(10 * i, means[i])) for i in range(13)]).set_z_index(10)
        self.play(Write(mean_dots))
        self.wait()
        lines = VGroup(
            Line(ax3.c2p(0, 13.4), ax3.c2p(35, 13.4), color=YELLOW),
            Line(ax3.c2p(55, 14.2), ax3.c2p(95, 14.2), color=YELLOW),
            Line(ax3.c2p(105, 14.4), ax3.c2p(120, 14.4), color=YELLOW),
        )
        self.play(Write(lines))
        self.wait()

class NumberComparison(Scene):
    def construct(self):
        naive_n = [0, 0.1, 0.2, 0.5, 1, 2, 4, 6, 8, 10, 12, 14]
        naive = [0.333482, 0.483535, 0.510472, 0.674992, 1.21809, 3.01386, 4.47177, 6.13229, 9.01276, 13.2702, 18.8985, 25.7307]

        fmm_n = [0, 1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
        bh_n = [0, 1, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

        files = [open("TimeData/Number/FMM/" + str(fmm_n[i]) + ".txt", "r") for i in range(len(fmm_n))]
        fmm = list(map(float, [files[i].readlines()[0].split(' ')[1] for i in range(len(fmm_n))]))

        files = [open("TimeData/Number/BH/bh" + str(bh_n[i]) + ".txt", "r") for i in range(len(bh_n))]
        bh = list(map(float, [files[i].readlines()[0].split(' ')[1] for i in range(len(bh_n))]))

        ax = Axes(x_range=[0, 220, 20], y_range=[0, 30, 5], axis_config={"include_numbers": True}, tips=False)
        labels = ax.get_axis_labels(r"\text{Number of particles (thousands)", r"\text{Mean time per frame (ms)}").set_z_index(10)
        
        key = VGroup(Text("Naive").set_color(YELLOW), Text("Barnes-Hut").set_color(GREEN), Text("FMM").set_color(BLUE))
        key.arrange(DOWN)
        key[1].align_to(key[0], RIGHT)
        key[2].align_to(key[0], RIGHT)
        key.to_corner(UR)
        self.wait(0.5)
        self.play(FadeIn(ax), Write(labels), Write(key))
        self.wait()

        naive_line = ax.plot_line_graph(x_values=naive_n, y_values=naive, line_color=YELLOW_E,
                                        vertex_dot_style=dict(color=YELLOW), stroke_width=4,)
        self.play(Write(naive_line))
        self.wait()
        bh_line = ax.plot_line_graph(x_values=bh_n, y_values=bh, line_color=GREEN_E,
                                        vertex_dot_style=dict(color=GREEN), stroke_width=4,)
        self.play(Write(bh_line))
        self.wait()
        fmm_line = ax.plot_line_graph(x_values=fmm_n, y_values=fmm, line_color=BLUE_E,
                                     vertex_dot_style=dict(color=BLUE), stroke_width=4, )
        self.play(Write(fmm_line))
        self.wait()

        line = ax.plot(lambda x: 0.112 * x + 0.87, x_range=[0, 200], color=BLUE_B)
        self.play(Create(line))
        self.wait()
        line2 = ax.plot(lambda x: 0.0805 * x + 3.32, x_range=[10, 125], color=BLUE_B)
        self.play(Create(line2))
        self.wait()


class AccuracyComparison(Scene):
    def construct(self):
        dot = Dot(color=BLUE).move_to(LEFT * 1.5).set_z_index(5)
        exact_dot = Dot(color=BLUE_D).move_to(RIGHT + UP * 2.7)
        approx_dot = Dot(color=BLUE_D).move_to(RIGHT * 0.9 + UP * 2.9)
        exact = Arrow(dot, exact_dot, buff=0).set_color(GREEN)
        approx = Arrow(dot, approx_dot, buff=0).set_color(YELLOW)

        exact_label = MathTex(r"\vec{F_i}").set_color(GREEN).next_to(exact_dot, RIGHT)
        approx_label = MathTex(r"\vec{F_i}'").set_color(YELLOW).next_to(approx_dot, UP * 0.5 + RIGHT)
        self.wait()
        self.play(Write(dot))
        self.play(FadeIn(exact_dot), FadeIn(approx_dot), GrowArrow(exact), GrowArrow(approx), Write(exact_label), Write(approx_label))
        self.wait()
        abs_error = MathTex(r"E_{abs, i} = ", r"\|\vec{F_i}' - \vec{F_i}\|").shift(DOWN * 1.5)
        abs_error[1][1:5].set_color(YELLOW)
        abs_error[1][6:9].set_color(GREEN)
        self.play(Write(abs_error))
        l2_error = MathTex(r"E = \sqrt{\frac{\sum E_{abs, i}^2}{\sum \|\vec{F_i}\|^2}}").shift(DOWN * 1.5 + LEFT * 2.5)
        l2_error[0][15:18].set_color(GREEN)
        self.play(Write(l2_error), abs_error.animate.shift(RIGHT * 2.5))
        self.wait()


        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 30, 5], axis_config={"include_numbers": True}, tips=False)
        labels = ax.get_axis_labels(r"\theta", r"\text{Error}").set_z_index(10)
        self.play(Unwrite(abs_error), Unwrite(l2_error),
                  Unwrite(exact_dot), Unwrite(approx_dot), Unwrite(exact_label), Unwrite(approx_label),
                  Unwrite(exact), Unwrite(approx), Unwrite(dot), Write(ax), Write(labels))
        self.wait()

        bh_theta = [0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5]
        files = [open("TimeData/Error/BH/" + str(bh_theta[i]) + ".txt", "r") for i in range(len(bh_theta))]
        raw = [files[i].readlines()[-2:] for i in range(len(bh_theta))]
        for i in range(len(bh_theta)):
            raw[i][0] = raw[i][0].split(' ')
            raw[i][0][0] = raw[i][0][0][:-1]
            raw[i][0] = list(map(float, raw[i][0]))
            raw[i][1] = [float(raw[i][1])]
        bh_data = np.array([raw[i][0] + raw[i][1] for i in range(len(bh_theta))]).T

        key = VGroup(Tex("Mean ms/frame").set_color(GOLD),
                     Tex("$L^2$ error (\%)").set_color(BLUE),
                     Tex("Mean absolute error").set_color(GREEN),
                     Tex("Max absolute error").set_color(YELLOW),
                     )
        key.arrange(DOWN).scale(0.9)
        key[1].align_to(key[0], RIGHT)
        key[2].align_to(key[0], RIGHT)
        key[3].align_to(key[0], RIGHT)
        key.to_corner(UR)

        time_graph = ax.plot_line_graph(x_values=bh_theta, y_values=bh_data[3, :], line_color=GOLD_E,
                           vertex_dot_style=dict(color=GOLD), stroke_width=4, )
        l2_graph = ax.plot_line_graph(x_values=bh_theta, y_values=bh_data[0, :], line_color=BLUE_E,
                                        vertex_dot_style=dict(color=BLUE), stroke_width=4, )
        signs = [-1, 1, -1, 1, -1, 1, -1, -1, -1, -1]

        def round_sig(x):
            if abs(x) < 1e3:
                return round(x, 3 - math.floor(math.log10(abs(x))))
            return round(x)

        abs_errors = VGroup([Tex(str(round_sig(bh_data[1, i]))).move_to(ax.c2p(bh_theta[i], bh_data[0, i] + 1.3 * signs[i]))
                            .set_color(GREEN).scale(0.5) for i in range(len(bh_theta))])
        max_errors = VGroup([Tex(str(round_sig(bh_data[2, i]))).move_to(ax.c2p(bh_theta[i], bh_data[0, i] + 2.6 * signs[i]))
                            .set_color(YELLOW).scale(0.5) for i in range(len(bh_theta))])
        self.play(Write(key),
                  AnimationGroup([Write(time_graph), Write(l2_graph), Write(abs_errors), Write(max_errors)], lag_ratio=0.25))
        self.wait()

        ax2 = Axes(x_range=[0, 22, 2], y_range=[-9, 3, 1], tips=False, axis_config={"include_numbers": True},
            y_axis_config={"scaling": LogBase(custom_labels=True)},)
        labels2 = ax2.get_axis_labels(r"p", r"\text{Error}")
        self.play(FadeOut(time_graph), FadeOut(l2_graph), FadeOut(abs_errors), FadeOut(max_errors),
                  ReplacementTransform(ax, ax2), ReplacementTransform(labels, labels2))
        self.wait()

        fmm_p = [2 * i for i in range(1, 11)]
        files = [open("TimeData/Error/FMM/" + str(fmm_p[i]) + ".txt", "r") for i in range(len(fmm_p))]
        raw = [files[i].readlines()[-1] for i in range(len(fmm_p))]
        for i in range(len(fmm_p)):
            raw[i] = raw[i].split(' ')
            raw[i][0] = raw[i][0][:-1]
        fmm_data = np.array([list(map(float, raw[i])) for i in range(len(fmm_p))]).T
        l2_graph = ax2.plot_line_graph(x_values=fmm_p, y_values=fmm_data[0, :], line_color=BLUE_E,
                                      vertex_dot_style=dict(color=BLUE), stroke_width=4, )
        abs_graph = ax2.plot_line_graph(x_values=fmm_p, y_values=fmm_data[1, :], line_color=GREEN_E,
                                      vertex_dot_style=dict(color=GREEN), stroke_width=4, )
        max_graph = ax2.plot_line_graph(x_values=fmm_p, y_values=fmm_data[2, :], line_color=YELLOW_E,
                                      vertex_dot_style=dict(color=YELLOW), stroke_width=4, )
        self.play(AnimationGroup([Write(l2_graph), Write(abs_graph), Write(max_graph)], lag_ratio=0.25))
        self.wait()
        line = Line(ax2.c2p(0, fmm_data[0, 9]), ax2.c2p(20, fmm_data[0, 9]), color=BLUE_B)
        self.play(Write(line))
        self.wait()


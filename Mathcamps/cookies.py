from manim import *
import math

class Cookie(Scene):
    def construct(self):
        self.wait()
        oreo = ImageMobject("oreos.png").scale(0.05).shift(LEFT * 2.5)
        choco = ImageMobject("Choco_chip_cookie.png").scale(0.3).shift(RIGHT * 2.5)

        mentors = VGroup([Circle(radius=0.4, stroke_color=GRAY, stroke_width=8, fill_color=ORANGE, fill_opacity=1)
                         .shift(RIGHT * (i - 7) * 0.75 + DOWN * 5) for i in range(15)])
        self.add(mentors)
        self.play(AnimationGroup(*[mentors[i].animate.shift(UP * 2) for i in range(15)], lag_ratio=0.05))
        self.wait()

        boxes = VGroup().set_z_index(100)
        for i in range(5):
            for j in range(3):
                boxes.add(Rectangle(width=2, height=2, stroke_width=6).move_to(RIGHT * (i - 2) * 2.5 + DOWN * (j - 1) * 2.5))

        anims = []
        for i in range(15):
            anims.append([mentors[i].animate.move_to(boxes[i].get_center() + UP * 0.5), Write(boxes[i])])
        self.play(AnimationGroup(*anims, lag_ratio=0.05))
        self.wait()

        assignment = [1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1]
        cookies = Group()
        for i in range(15):
            if assignment[i] == 1:
                cookies.add(oreo.copy().move_to(mentors[i]).shift(DOWN))
            else:
                cookies.add(choco.copy().move_to(mentors[i]).shift(DOWN))
        self.play(FadeIn(cookies))
        self.wait()
        mentors2 = mentors.copy()
        for i in range(15):
            if assignment[i] == 1:
                mentors2[i].set_fill_color(BLUE)
        self.play(FadeOut(cookies), Transform(mentors, mentors2))
        self.wait()

        mentors2 = mentors.copy()
        for i in range(15):
            mentors2[i].move_to([3 * math.cos(i / 15 * TAU), 3 * math.sin(i / 15 * TAU), 0])
        self.play(AnimationGroup(*[mentors[i].animate.move_to([3 * math.cos(i / 15 * TAU), 3 * math.sin(i / 15 * TAU), 0])
                                   for i in range(15)], lag_ratio=0.05),
                  Unwrite(boxes))
        self.wait()

        guesses = [5, 9, 10, 9, 14, 1, 12, 10, 6, 3, 4, 2, 6, 8, 7]
        arrows = VGroup([Arrow(start=mentors[i].get_center(), end=mentors[guesses[i]].get_center(), buff=0.4,
                               max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=3) for i in range(15)])
        self.play(AnimationGroup(*[GrowArrow(arrows[i]) for i in range(15)]))
        self.wait()

        success = []
        for i in range(15):
            if assignment[i] == assignment[guesses[i]]:
                success.append(i)
        arrows2 = arrows.copy()
        for s in success:
            arrows2[s].set_color(GREEN)
        self.play(Transform(arrows, arrows2))

        self.wait()


class Graph(Scene):
    def construct(self):
        mentors = VGroup([Circle(radius=0.4, stroke_color=GRAY, stroke_width=8, fill_opacity=1,
                                 fill_color=WHITE) for i in range(15)])

        mentors[0].move_to([-4.5, 3, 0])
        mentors[1].move_to([-5, 1, 0])
        mentors[2].move_to([-4, -3, 0])
        mentors[3].move_to([-1, 1, 0])
        mentors[4].move_to([-3, -1, 0])
        mentors[5].move_to([0, -2.5, 0])

        mentors[6].move_to([-1.5, 3, 0])
        mentors[7].move_to([3, 3, 0])
        mentors[8].move_to([1.5, 1, 0])
        mentors[9].move_to([0.5, 2, 0])
        mentors[10].move_to([3, -0.5, 0])
        mentors[11].move_to([5, 1, 0])

        mentors[12].move_to([2.5, -3, 0])
        mentors[13].move_to([4.5, -3, 0])
        mentors[14].move_to([3.5, -1.5, 0])

        self.add(mentors)
        guesses = [1, 3, 1, 5, 3, 2, 7, 8, 10, 8, 11, 8, 13, 14, 12]
        self.wait()
        arrows = VGroup([Arrow(start=mentors[i].get_center(), end=mentors[guesses[i]].get_center(), buff=0.45,
                               max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=3) for i in
                         range(15)])
        self.play(AnimationGroup(*[GrowArrow(arrows[i]) for i in range(15)]))
        self.wait()

        assignments = [1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2]
        self.play(AnimationGroup(*[mentors[i].animate.set_fill_color(ORANGE if assignments[i] == 1 else BLUE) for i in range(15)]))
        self.play(arrows[11].animate.set_color(GREEN), arrows[13].animate.set_color(GREEN))
        self.wait()

        guesses2 = [2, 6, 3, 1, 6, 3, 7, 4, 12, 14, 3, 13, 0, 5, 9]
        arrows2 = VGroup([Arrow(start=mentors[i].get_center(), end=mentors[guesses2[i]].get_center(), buff=0.45, color=BLUE,
                               max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=3) for i in range(15)])
        self.play(AnimationGroup(*[GrowArrow(arrows2[i]) for i in range(15)]))
        self.wait()

'''
#include <bits/stdc++.h>
#define int long long
using namespace std;
bool vis[20][20];
int n, tx, ty, cnt;
char path[500];
int dx[] = {1, 0}, dy[] = {0, 1};
void dfs (int d, int x, int y) {
    if (d == n * n) {
        cout << x << ' ' << y << ": ";
        int xsum = 0;
        for (int i = 1; i < n * n; i++) {
            if (i % n == 0) cout << ' ';
            if (path[i] == 'R') xsum = (xsum + 1) % n;
            cout << path[i];
            if (i % n == 0) cout << xsum << ' ';
        }
        cout << endl;
        return;
    }
    for (int i = 0; i < 2; i++) {
        int nx = (x + dx[i]) % n, ny = (y + dy[i]) % n;
        if (vis[nx][ny]) continue;
        vis[nx][ny] = true;
        if (i == 0) path[d] = 'R';
        else path[d] = 'D';
        dfs(d + 1, nx, ny);
        vis[nx][ny] = false;
    }
}
signed main() {
    n = 6;
    tx = 3, ty = n - tx - 1;
    vis[0][0] = true;
    dfs(1, 0, 0);
    return 0;
}
/*
x = n - 1
d = n - 1, n - 3, ..., 1
invert: d = 0, 2, ..., n - 2
7 0: RRRRRRD R7 RRRRRRD R6 RRRRRRD R5 RRRRRRD R4 RRRRRRD R3 RRRRRRD R2 RRRRRRD R1 RRRRRRD
5 2: RRRRRRD D6 RRRRRRD R5 RRRRRRD R4 RRRRRRD R3 RRRRRRD R2 RRRRRRD R1 RRRRRRD D7 RRRRRRD
3 4: RRRRRRD D6 RRRRRRD D4 RRRRRRD R3 RRRRRRD R2 RRRRRRD R1 RRRRRRD D7 RRRRRRD D5 RRRRRRD
1 6: RRRRRRD D6 RRRRRRD D4 RRRRRRD D2 RRRRRRD R1 RRRRRRD D7 RRRRRRD D5 RRRRRRD D3 RRRRRRD

6 0: RRRRRD R6 RRRRRD R5 RRRRRD R4 RRRRRD R3 RRRRRD R2 RRRRRD R1 RRRRRD
4 2: RRRRRD D5 RRRRRD R4 RRRRRD R3 RRRRRD R2 RRRRRD R1 RRRRRD D6 RRRRRD
2 4: RRRRRD D5 RRRRRD D3 RRRRRD R2 RRRRRD R1 RRRRRD D6 RRRRRD D4 RRRRRD
0 6: RRRRRD D5 RRRRRD D3 RRRRRD D1 RRRRRD D6 RRRRRD D4 RRRRRD D2 RRRRRD
*/
'''
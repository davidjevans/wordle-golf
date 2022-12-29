import pandas as pd
import numpy as np
import manim
from manim import *
from manim.utils.color import Colors
from collections import namedtuple
from scipy.ndimage import uniform_filter1d


PlayerScores = namedtuple("PlayerScores", "name x y")

wordle_to_golf_score = {
        '1': -10,
        '2': -3,
        '3': -1,
        '4': 0,
        '5': 1,
        '6': 2,
        'X': 4,
        }

PlayerToColor = {
        'madre': Colors.orange,
        'doug': Colors.blue_c,
        'daniel': Colors.yellow_c,
        'david': Colors.green_c,
        'jamie': Colors.purple_c,
        'lisa': Colors.red_c,
        }

day_order = ["Su", "M", "T", "W", "Th", "F", "Sa", ""]

def load_wordle_scores(path):
    scores_df = pd.read_csv(path)

    # Let's do a bit of preprocessing
    # Sort the puzzle numbers in chronological order
    scores_df = scores_df.sort_values("puzzle_number")
    # Map the puzzle number to the corresponding week. We started on puzzle number 302.
    scores_df['week'] = (scores_df.puzzle_number-302) // 7

    # Map the wordle score to the corresponding golf score
    scores_df['golf_score'] = scores_df['score'].map(wordle_to_golf_score)

    # Textra wrote out my scores as "me", let's get them back to "david"
    scores_df.name = scores_df.name.replace(['me'],'david')

    return scores_df

def create_legend(name_list):
    v_group = []
    for name in name_list:
        v_group.append(Dot(color=PlayerToColor[name].value))
        v_group.append(Text(name).scale(0.4))


    dots = VGroup(*v_group)
    dots.arrange_in_grid(
            buff=(0.25,0.1),
            cols=2,
            rows=len(name_list),
            flow_order="rd")
    return dots

class CumulativeGraph(Scene):
    def construct(self):
        scores_df = load_wordle_scores("wordle_scores.csv")

        scores_dict = {}
        for name, score_df in scores_df.groupby("name"):
            scores_dict[name] = PlayerScores(name, score_df.puzzle_number.tolist(), score_df.golf_score.cumsum().tolist())

        x_min = scores_df.puzzle_number.min()
        x_max = scores_df.puzzle_number.max()
        x_step = 7

        # y_min = scores_df.golf_score_sum.min()
        # y_max = scores_df.golf_score_sum.max()
        y_min = -30
        y_max = 11
        y_step = 5

        axes = Axes(
            x_range=[x_min, x_max, x_step],
            y_range=[y_min, y_max, y_step],
            x_length = 11)
        axes.align_on_border(LEFT, buff=0.75)

        lines = []
        for scores in scores_dict.values():
            line = axes.plot_line_graph(scores.x, scores.y, add_vertex_dots=False, line_color=PlayerToColor[scores.name].value)
            lines.append(line)

        x_label = axes.get_x_axis_label("\\text{ week }")
        y_label = axes.get_y_axis_label("\\text{ total score }")
        x_label.next_to(axes, DOWN)

        legend = create_legend(scores_df.name.unique().tolist())
        legend.next_to(axes, RIGHT, buff=0.5, aligned_edge=UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.add(legend)
        self.wait()
        line_creations = [Create(line) for line in lines]
        self.play(*line_creations, run_time=10)
        self.wait()

        # Add Jamie's -1
        jamies_scores = scores_dict['jamie']
        puzzle_of_interest = 395
        emphasis_line = axes.plot_line_graph(jamies_scores.x, jamies_scores.y, add_vertex_dots=False, line_color=PlayerToColor[jamies_scores.name].value, stroke_width=10)

        p1 = axes.coords_to_point(puzzle_of_interest, y_min)
        p2 = axes.coords_to_point(puzzle_of_interest, y_max)
        v1 = axes.get_vertical_line(p1, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        v2 = axes.get_vertical_line(p2, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        self.add(emphasis_line, v1, v2)
        self.wait()
        self.remove(emphasis_line, v1, v2)

        # Daniel gives up has firefighting season
        daniels_scores = scores_dict['daniel']
        puzzle_of_interest = 360
        emphasis_line = axes.plot_line_graph(daniels_scores.x, daniels_scores.y, add_vertex_dots=False, line_color=PlayerToColor[daniels_scores.name].value, stroke_width=10)

        p1 = axes.coords_to_point(puzzle_of_interest, y_min)
        p2 = axes.coords_to_point(puzzle_of_interest, y_max)
        v1 = axes.get_vertical_line(p1, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        v2 = axes.get_vertical_line(p2, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        self.add(emphasis_line, v1, v2)
        self.wait()
        self.remove(emphasis_line, v1, v2)

        # Everyone doesn't get word "Parer" (except mom)
        puzzle_of_interest = 454

        p1 = axes.coords_to_point(puzzle_of_interest, y_min)
        p2 = axes.coords_to_point(puzzle_of_interest, y_max)
        v1 = axes.get_vertical_line(p1, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        v2 = axes.get_vertical_line(p2, line_config={"dashed_ratio": .5, "dash_length": 0.15}, stroke_width=4)
        self.add(v1, v2)
        self.wait()
        self.remove(v1, v2)


class OneWeek(Scene):
    def construct(self):
        scores_df = load_wordle_scores("wordle_scores.csv")
        selected_week = 1
        week1_scores_df = scores_df[scores_df.week == selected_week]

        x_min = week1_scores_df.puzzle_number.min() - 1
        x_max = week1_scores_df.puzzle_number.max()
        x_step = 1

        y_min = -6
        y_max = 5
        y_step = 1

        axes = Axes(
            x_range=[x_min, x_max, x_step],
            y_range=[y_min, y_max, y_step],
            x_length = 11,
            y_axis_config={"include_numbers": True},
            )
        axes.align_on_border(LEFT, buff=0.75)

        week_text = Text(f"Week: {selected_week}" ).scale(0.7)
        week_text.next_to(axes, UP)

        scores_list = []
        for name, score_df in week1_scores_df.groupby("name"):
            scores_list.append(
                    PlayerScores(name,
                                 [x_min, *score_df.puzzle_number.tolist()],
                                 [0, *score_df.golf_score.cumsum().tolist()]))


        weeks_lines = []
        for today, _ in enumerate(scores_list[0].x):
            todays_lines = []
            for scores in scores_list:
                line = axes.plot_line_graph(scores.x[today:today+2], scores.y[today:today+2], add_vertex_dots=False, line_color=PlayerToColor[scores.name].value)
                todays_lines.append(Create(line))
            weeks_lines.append(todays_lines)

        x_label = axes.get_x_axis_label("\\text{ day }")
        y_label = axes.get_y_axis_label("\\text{ score }")
        x_label.next_to(axes, DOWN)

        legend = create_legend(scores_df.name.unique().tolist())
        legend.next_to(axes, RIGHT, buff=0.5, aligned_edge=UP)

        self.play(Create(axes), Write(x_label), Write(y_label), Create(week_text))
        self.add(legend)
        self.wait()

        for i, day_lines in enumerate(weeks_lines):
            day_text = Text(f"{day_order[i]}" ).scale(0.7)
            day_text.next_to(week_text, RIGHT)
            self.add(day_text)

            self.play(*day_lines)
            self.wait()
            self.remove(day_text)

        winning_player = week1_scores_df.groupby("name").sum().golf_score.idxmin()
        winning_player_text = Text(winning_player, color=PlayerToColor[winning_player].value)
        winner_text = Text(f"Winner: ")

        winning_player_text.next_to(axes, UP, buff=-0.5)
        winner_text.next_to(axes, UP, buff=-0.5)
        winning_player_text.next_to(winner_text, RIGHT)

        self.play(Create(winner_text), Create(winning_player_text))
        self.wait()

class ManyWeeks(Scene):
    def construct(self):
        scores_df = load_wordle_scores("wordle_scores.csv")

        for week_idx, week_scores_df in scores_df.groupby("week"):
            # We're skipping the first two weeks.
            # The first week was ugly (incomplete scores)
            # The second week was visualized in the OneWeek scene
            if week_idx < 2:
                continue


            scores_list = []
            min_total_score = None
            max_total_score = None
            for name, score_df in week_scores_df.groupby("name"):
                min_puzzle_num = score_df.puzzle_number.min()
                puzzle_nums = score_df.puzzle_number.tolist()
                puzzle_nums = puzzle_nums - min_puzzle_num + 1

                min_player_score = score_df.golf_score.cumsum().min()
                if not min_total_score:
                    min_total_score = min_player_score
                if min_player_score < min_total_score:
                    min_total_score = min_player_score

                max_player_score = score_df.golf_score.cumsum().max()
                if not max_total_score:
                    max_total_score = max_player_score
                if max_player_score > max_total_score:
                    max_total_score = max_player_score

                scores_list.append(
                        PlayerScores(name,
                                     [0, *puzzle_nums],
                                     [0, *score_df.golf_score.cumsum().tolist()]))

            x_min = 0
            x_max = 7
            x_step = 1

            y_min = min_total_score
            y_max = max_total_score
            y_step = 1

            axes = Axes(
                x_range=[x_min, x_max, x_step],
                y_range=[y_min, y_max, y_step],
                x_length = 11,
                y_axis_config={"include_numbers": True},
                )
            axes.align_on_border(LEFT, buff=0.75)
            x_label = axes.get_x_axis_label("\\text{ day }")
            y_label = axes.get_y_axis_label("\\text{ score }")
            x_label.next_to(axes, DOWN)

            legend = create_legend(scores_df.name.unique().tolist())
            legend.next_to(axes, RIGHT, buff=0.5, aligned_edge=UP)
            self.add(legend)

            week_text = Text(f"Week:" ).scale(0.7)
            week_text.next_to(axes, UP)


            week_idx_text = Text(str(week_idx)).scale(0.7)
            week_idx_text.next_to(week_text, RIGHT)

            self.add(axes, x_label, y_label, week_text, week_idx_text)

            lines = []
            for scores in scores_list:
                line = axes.plot_line_graph(scores.x, scores.y, add_vertex_dots=False, line_color=PlayerToColor[scores.name].value)
                lines.append(Create(line))
            self.play(*lines)

            winner_text = Text(f"Winner: ")
            winner_text.next_to(axes, UP, buff=-0.5)
            self.add(winner_text)

            summed_scores_df = week_scores_df.groupby("name").sum()
            winning_players = summed_scores_df[summed_scores_df.golf_score == summed_scores_df.golf_score.min()].index.tolist()

            prev_winning_player_text = None
            for winner_idx, winner_name in enumerate(winning_players):
                winning_player_text = Text(winner_name, color=PlayerToColor[winner_name].value)
                # For the first winner, place the text next to the winner text
                # Otherwise, place the text below the previous winner
                if winner_idx == 0:
                    winning_player_text.next_to(winner_text, RIGHT)
                else:
                    winning_player_text.next_to(prev_winning_player_text, DOWN)
                prev_winning_player_text = winning_player_text
                self.add(winning_player_text)

            self.wait()

            # Cleanup!!
            self.clear()

class WinnersBarChart(Scene):
    def construct(self):
        # We're going to count the number of wins for each person, the create a bar chart.
        scores_df = load_wordle_scores("wordle_scores.csv")
        scores_df = scores_df[scores_df.week < 23]

        # Create a variable to keep track of each person's number of wins. And initialize it for each person to zero.
        win_count = {}
        for name in scores_df.name.unique():
            win_count[name] = 0

        # Determine the winner's for each week. We're okay with friendly ties.
        for week_idx, week_scores_df in scores_df.groupby("week"):
            summed_scores_df = week_scores_df.groupby("name").sum()
            winning_players = summed_scores_df[summed_scores_df.golf_score == summed_scores_df.golf_score.min()].index.tolist()

            for name in winning_players:
                win_count[name] = win_count[name] + 1

        sorted_win_count = dict(sorted(win_count.items(), key=lambda item: item[1], reverse=True))
        max_num_wins = max(list(win_count.values()))
        bar_colors = [PlayerToColor[player].value for player in sorted_win_count.keys()]

        chart = BarChart(
            values=list(sorted_win_count.values()),
            bar_names=list(sorted_win_count.keys()),
            bar_colors=bar_colors,
            y_range=[0, max_num_wins, 1],
            y_length=5,
            x_length=10,
            x_axis_config={"font_size": 36},
        )

        c_bar_lbls = chart.get_bar_labels(font_size=48)

        title_text = Text("wins by player").next_to(chart, UP).scale(0.7)
        self.add(title_text)

        self.play(Write(chart), Write(c_bar_lbls), run_time=5)
        self.wait()

class ScoreChart(Scene):
    def construct(self):
        wordle_score_title_text = Text("wordle score")
        wordle_score_title_ul = Underline(wordle_score_title_text)
        wordle_score_title_text_group = Group(wordle_score_title_text, wordle_score_title_ul)

        wordle_golf_score_title_text = Text("golf score")
        wordle_golf_score_title_ul = Underline(wordle_golf_score_title_text)
        wordle_golf_score_title_text_group = Group(wordle_golf_score_title_text, wordle_golf_score_title_ul)

        title_group = Group(wordle_score_title_text_group, wordle_golf_score_title_text_group).arrange(RIGHT, buff=0.8).align_on_border(UP)
        self.add(title_group)

        golf_buff = 0.27
        _1_score_text = Text("1/6").next_to(wordle_score_title_text, DOWN)
        _1_golf_score_text = Text("-10").next_to(wordle_golf_score_title_text, DOWN, buff=golf_buff)

        _2_score_text = Text("2/6").next_to(_1_score_text, DOWN)
        _2_golf_score_text = Text("-3").next_to(_1_golf_score_text, DOWN, buff=golf_buff)

        _3_score_text = Text("3/6").next_to(_2_score_text, DOWN)
        _3_golf_score_text = Text("-1").next_to(_2_golf_score_text, DOWN, buff=golf_buff)

        _4_score_text = Text("4/6").next_to(_3_score_text, DOWN)
        _4_golf_score_text = Text("+0").next_to(_3_golf_score_text, DOWN, buff=golf_buff)

        _5_score_text = Text("5/6").next_to(_4_score_text, DOWN)
        _5_golf_score_text = Text("+1").next_to(_4_golf_score_text, DOWN, buff=golf_buff)

        _6_score_text = Text("6/6").next_to(_5_score_text, DOWN)
        _6_golf_score_text = Text("+2").next_to(_5_golf_score_text, DOWN, buff=golf_buff)

        _x_score_text = Text("X/6").next_to(_6_score_text, DOWN)
        _x_golf_score_text = Text("+4").next_to(_6_golf_score_text, DOWN, buff=golf_buff)

        self.play(Write(_4_score_text), Write(_4_golf_score_text))
        self.wait()

        self.play(Write(_3_score_text), Write(_3_golf_score_text))
        self.wait()

        self.play(Write(_2_score_text), Write(_2_golf_score_text))
        self.wait()

        self.play(Write(_1_score_text), Write(_1_golf_score_text))
        self.wait()

        self.play(Write(_5_score_text), Write(_5_golf_score_text))
        self.wait()

        self.play(Write(_6_score_text), Write(_6_golf_score_text))
        self.wait()

        self.play(Write(_x_score_text), Write(_x_golf_score_text))
        self.wait()

import os
import subprocess
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


OUTPUT = "assets/activity-graph.gif"

WIDTH = 13
HEIGHT = 4

FPS = 12
FRAMES = 90


def get_contributions():
    username = os.environ.get("GITHUB_REPOSITORY_OWNER")

    if not username:
        username = "aviral-dot"

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    import json
    import urllib.request

    token = os.environ.get("GITHUB_TOKEN")

    payload = json.dumps(
        {
            "query": query,
            "variables": {"login": username},
        }
    ).encode()

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        data = json.load(response)

    weeks = (
        data["data"]["user"]
        ["contributionsCollection"]
        ["contributionCalendar"]
        ["weeks"]
    )

    values = []

    for week in weeks:
        for day in week["contributionDays"]:
            values.append(
                (
                    day["date"],
                    day["contributionCount"],
                )
            )

    return values


def contribution_level(value):
    if value == 0:
        return 0

    if value <= 2:
        return 1

    if value <= 5:
        return 2

    if value <= 10:
        return 3

    return 4


def main():

    os.makedirs("assets", exist_ok=True)

    data = get_contributions()

    data = data[-365:]

    dates = [item[0] for item in data]
    counts = [item[1] for item in data]

    levels = [
        contribution_level(value)
        for value in counts
    ]

    fig, ax = plt.subplots(
        figsize=(WIDTH, HEIGHT)
    )

    def draw_frame(frame):

        ax.clear()

        ax.set_facecolor("white")

        progress = min(
            len(data),
            int((frame / FRAMES) * len(data))
        )

        visible_dates = dates[:progress]
        visible_levels = levels[:progress]

        x_positions = range(progress)

        for x, level in zip(
            x_positions,
            visible_levels,
        ):

            size = 0.8

            ax.add_patch(
                plt.Rectangle(
                    (
                        x,
                        level,
                    ),
                    size,
                    size,
                    linewidth=0.5,
                )
            )

        ax.set_xlim(
            0,
            max(len(data), 1),
        )

        ax.set_ylim(
            -0.5,
            5,
        )

        ax.set_yticks([])

        ax.set_xticks([])

        ax.set_title(
            "GitHub Activity",
            fontsize=18,
            fontweight="bold",
            pad=15,
        )

        ax.text(
            0,
            -0.35,
            "Contribution activity building over time",
            fontsize=9,
        )

        ax.axis("off")

    animation = FuncAnimation(
        fig,
        draw_frame,
        frames=FRAMES,
        interval=1000 / FPS,
        repeat=True,
    )

    animation.save(
        OUTPUT,
        writer=PillowWriter(fps=FPS),
    )

    plt.close(fig)

    print(
        f"Generated {OUTPUT}"
    )


if __name__ == "__main__":
    main()

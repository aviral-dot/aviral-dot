import math
import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


SKILLS = [
    ("LLM Engineering", 90),
    ("RAG / Retrieval", 92),
    ("Agentic AI", 88),
    ("Backend", 82),
    ("Data Engineering", 78),
    ("Cloud / DevOps", 72),
    ("Evaluation", 80),
    ("Observability", 78),
]

OUTPUT = "assets/skill-radar.gif"

WIDTH = 10
HEIGHT = 7
FPS = 12
FRAMES = 72

CENTER_X = 0
CENTER_Y = 0
RADIUS = 1.0

COUNT = len(SKILLS)


def angle(index):
    return math.radians(90 - (360 / COUNT) * index)


def radar_point(index, radius):
    a = angle(index)
    return (
        CENTER_X + radius * math.cos(a),
        CENTER_Y + radius * math.sin(a),
    )


def polygon_points(radius):
    return [
        radar_point(i, radius)
        for i in range(COUNT)
    ]


fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))

ax.set_aspect("equal")
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.35, 1.35)
ax.axis("off")


def draw_frame(frame):
    ax.clear()

    ax.set_aspect("equal")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.35, 1.35)
    ax.axis("off")

    # Background
    ax.set_facecolor("white")

    # Title
    ax.text(
        0,
        1.25,
        "Engineering Focus",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
    )

    ax.text(
        0,
        1.12,
        "AI Engineering · Backend · Data · Cloud",
        ha="center",
        va="center",
        fontsize=10,
    )

    # ---------------------------------------------------------
    # Phase 1: Radar grid
    # ---------------------------------------------------------

    grid_progress = min(1.0, frame / 18)

    for level in range(1, 6):
        r = RADIUS * level / 5

        points = polygon_points(r * grid_progress)

        if grid_progress > 0:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]

            xs.append(xs[0])
            ys.append(ys[0])

            ax.plot(
                xs,
                ys,
                linewidth=0.8,
            )

    # ---------------------------------------------------------
    # Phase 2: Radar axes
    # ---------------------------------------------------------

    axis_progress = min(
        1.0,
        max(0.0, (frame - 12) / 18),
    )

    for i in range(COUNT):
        x, y = radar_point(i, RADIUS * axis_progress)

        ax.plot(
            [0, x],
            [0, y],
            linewidth=0.8,
        )

    # ---------------------------------------------------------
    # Phase 3: Skill polygon
    # ---------------------------------------------------------

    polygon_progress = min(
        1.0,
        max(0.0, (frame - 25) / 22),
    )

    if polygon_progress > 0:

        skill_points = [
            radar_point(
                i,
                RADIUS * (value / 100) * polygon_progress,
            )
            for i, (_, value) in enumerate(SKILLS)
        ]

        xs = [p[0] for p in skill_points]
        ys = [p[1] for p in skill_points]

        xs.append(xs[0])
        ys.append(ys[0])

        ax.fill(
            xs,
            ys,
            alpha=0.15,
        )

        ax.plot(
            xs,
            ys,
            linewidth=2.5,
        )

    # ---------------------------------------------------------
    # Phase 4: Skill points
    # ---------------------------------------------------------

    point_progress = min(
        1.0,
        max(0.0, (frame - 42) / 12),
    )

    for i, (_, value) in enumerate(SKILLS):

        x, y = radar_point(
            i,
            RADIUS * (value / 100) * point_progress,
        )

        if point_progress > 0:
            ax.scatter(
                [x],
                [y],
                s=35,
                zorder=5,
            )

    # ---------------------------------------------------------
    # Phase 5: Labels
    # ---------------------------------------------------------

    label_progress = min(
        1.0,
        max(0.0, (frame - 50) / 10),
    )

    for i, (name, value) in enumerate(SKILLS):

        x, y = radar_point(i, 1.22)

        if x < -0.15:
            alignment = "right"
        elif x > 0.15:
            alignment = "left"
        else:
            alignment = "center"

        ax.text(
            x,
            y,
            name,
            ha=alignment,
            va="center",
            fontsize=9,
            alpha=label_progress,
            fontweight="bold",
        )

        ax.text(
            x,
            y - 0.075,
            f"{value}/100",
            ha=alignment,
            va="center",
            fontsize=8,
            alpha=label_progress,
        )

    # ---------------------------------------------------------
    # Center label
    # ---------------------------------------------------------

    if frame >= 55:
        ax.text(
            0,
            0,
            "AI\nENGINEERING",
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    # ---------------------------------------------------------
    # Final hold
    # ---------------------------------------------------------

    if frame >= 65:
        ax.text(
            0,
            -1.22,
            "Production-oriented AI Engineering",
            ha="center",
            va="center",
            fontsize=9,
        )


animation = FuncAnimation(
    fig,
    draw_frame,
    frames=FRAMES,
    interval=1000 / FPS,
    repeat=True,
)

os.makedirs("assets", exist_ok=True)

animation.save(
    OUTPUT,
    writer=PillowWriter(fps=FPS),
)

plt.close(fig)

print(f"Generated {OUTPUT}")

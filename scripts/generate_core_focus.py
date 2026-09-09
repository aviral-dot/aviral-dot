import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


OUTPUT = "assets/core-focus.gif"

ITEMS = [
    "LLM APPLICATIONS",
    "RAG SYSTEMS",
    "AGENTIC AI",
    "MULTI-AGENT SYSTEMS",
    "PRODUCTION AI ENGINEERING",
]

FPS = 10
FRAMES_PER_ITEM = 15


fig, ax = plt.subplots(
    figsize=(11, 3.2)
)


def draw_frame(frame):

    ax.clear()

    ax.axis("off")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(
        0.5,
        0.85,
        "CORE FOCUS",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
    )

    completed = min(
        len(ITEMS),
        frame // FRAMES_PER_ITEM + 1,
    )

    for index in range(completed):

        y = 0.68 - index * 0.12

        ax.text(
            0.5,
            y,
            ITEMS[index],
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )

        if index < completed - 1:

            ax.text(
                0.5,
                y - 0.055,
                "↓",
                ha="center",
                va="center",
                fontsize=10,
            )


animation = FuncAnimation(
    fig,
    draw_frame,
    frames=len(ITEMS) * FRAMES_PER_ITEM,
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

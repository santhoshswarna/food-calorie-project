# make_algorithm_flowchart.py
# Creates a vertical flowchart image for the Food Calorie Estimation algorithm.

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def new_canvas(w=6, h=12):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig, ax

def draw_box(ax, cx, cy, w, h, text):
    x = cx - w/2
    y = cy - h/2
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.02',
        linewidth=1.6, edgecolor='black', facecolor='white'
    )
    ax.add_patch(rect)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=10)

def draw_down_arrow(ax, x, y_from, y_to):
    # Annotate draws an arrow from xytext -> xy; we go from the upper box bottom to the lower box top
    ax.annotate(
        '', xy=(x, y_to), xytext=(x, y_from),
        arrowprops=dict(arrowstyle='->', lw=1.6, color='black',
                        mutation_scale=14, shrinkA=8, shrinkB=8),
        annotation_clip=False
    )

def make_flow(outfile='algorithm_flowchart.png'):
    fig, ax = new_canvas(7, 13)

    steps = [
        ("Step 1\nImage Acquisition\nRGB photo from camera/upload"),
        ("Step 2\nPreprocessing\nResize 224×224, normalize"),
        ("Step 3\n(Option) Segmentation\nFocus on food ROI"),
        ("Step 4\nCNN Classification\nDenseNet201 + classifier"),
        ("Step 5\nPortion/Volume (opt)\nScale by size/servings"),
        ("Step 6\nCalorie Lookup\nMap label → kcal and display")
    ]

    # Vertical layout (top to bottom)
    x = 0.5
    y_top = 0.90
    dy = 0.14
    box_w, box_h = 0.78, 0.12

    centers = []
    for i, text in enumerate(steps):
        cy = y_top - i * dy
        draw_box(ax, x, cy, box_w, box_h, text)
        centers.append((x, cy))

    # Arrows between boxes
    for i in range(len(centers) - 1):
        x0, y0 = centers[i]
        _, y1 = centers[i + 1]
        draw_down_arrow(ax, x0, y0 - box_h/2, y1 + box_h/2)

    plt.tight_layout()
    plt.savefig(outfile, dpi=220, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {outfile}")

if __name__ == "__main__":
    make_flow("algorithm_flowchart.png")

# Fix the arrow direction and spacing between stacked boxes.

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(4.5, 7))
ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

def box(y, text, x=0.10, w=0.80, h=0.10):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02',
                                  linewidth=1.5, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9)
    return (x, y, w, h)

def connect_down(prev_box, curr_box):
    x_p, y_p, w_p, h_p = prev_box
    x_c, y_c, w_c, h_c = curr_box
    x_center = 0.5
    # Draw from bottom-center of the upper box (xytext) to top-center of the lower box (xy)
    ax.annotate(
        '', 
        xy=(x_center, y_c + h_c),       # target (top of lower box)
        xytext=(x_center, y_p),         # start (bottom of upper box)
        arrowprops=dict(
            arrowstyle='->',
            lw=1.6,
            color='black',
            connectionstyle='arc3',     # straight connector
            shrinkA=8,                  # keep arrow off the box edge
            shrinkB=8,                  # keep arrow off the box edge
            mutation_scale=14           # arrowhead size
        ),
        annotation_clip=False
    )

labels = [
    "input_2\nInputLayer\ninput: [(None, 224, 224, 3)]\noutput: (None, 224, 224, 3)",
    "densenet201\nFunctional\ninput: (None, 224, 224, 3)\noutput: (None, 7, 7, 1920)",
    "gap\nGlobalAveragePooling2D\ninput: (None, 7, 7, 1920)\noutput: (None, 1920)",
    "dense\nDense\ninput: (None, 1920)\noutput: (None, 256)",
    "dropout\nDropout\ninput: (None, 256)\noutput: (None, 256)",
    "dense_1\nDense\ninput: (None, 256)\noutput: (None, 128)",
    "dropout_1\nDropout\ninput: (None, 128)\noutput: (None, 128)",
    "dense_2\nDense\ninput: (None, 128)\noutput: (None, 5)",
]

ys = list(reversed([0.05 + i*0.11 for i in range(len(labels))]))
boxes = []
for y, text in zip(ys, labels):
    boxes.append(box(y, text))

for i in range(1, len(boxes)):
    connect_down(boxes[i-1], boxes[i])

plt.tight_layout()
plt.savefig('model_architecture_fixed_arrows.png', dpi=220, bbox_inches='tight')
plt.show()

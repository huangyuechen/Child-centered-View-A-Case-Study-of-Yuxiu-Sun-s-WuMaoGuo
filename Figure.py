"""
20260624
The code for drawing the relationship figure for "Children's literature",
"the translation of Children's literature", "Child-centered view" and "education-centered view".

"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 8)
ax.set_ylim(0, 6)
ax.axis('off')

# 外矩形：儿童文学
outer = patches.FancyBboxPatch((0.5, 0.5), 7, 5, boxstyle="round,pad=0.1",
                               edgecolor='#2c3e50', facecolor='#aed6f1', alpha=0.3, lw=3)
ax.add_patch(outer)
ax.text(4, 5.2, "Children's Literature", ha='center', fontsize=16, fontweight='bold')
ax.text(4, 4.6, "Fundamental Core: Child‑centered view", ha='center', fontsize=13, color='#1a5276', fontweight='bold')

# 内矩形：儿童文学翻译
inner = patches.FancyBboxPatch((1.2, 1.2), 5.6, 2.6, boxstyle="round,pad=0.1",
                               edgecolor='#c0392b', facecolor='#f5b7b1', alpha=0.5, lw=3)
ax.add_patch(inner)
ax.text(4, 3.2, "Translation of Children's Literature", ha='center', fontsize=14, fontweight='bold')
ax.text(4, 2.5, "• Inherited Core: Child‑centered view", ha='center', fontsize=12, color='#1e8449')
ax.text(4, 1.8, "• Unique Core: Education‑centered view", ha='center', fontsize=12, color='#c0392b')

# 连线说明继承关系（可选箭头）
ax.annotate('inherits', xy=(2.8, 3.5), xytext=(2.8, 4.4),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5), fontsize=10, color='gray')

plt.title('', fontsize=15, pad=18, fontweight='bold')
plt.tight_layout()
plt.savefig('nested_cores.png', dpi=300, bbox_inches='tight')
plt.show()
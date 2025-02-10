import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.family'] = 'SimHei'  # 选择一个支持中文的字体
rcParams['axes.unicode_minus'] = False  # 正常显示负号


def gen_radar(items):
    # 提取数据
    labels = [f"{item['itemname']}（{item.get('itemnameZh', '--')}）" for item in items]
    data = [item['itemscore'] for item in items]

    # 设置雷达图的标签数量和角度
    num_vars = len(labels)

    # 计算雷达图的角度
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # 创建雷达图的闭环
    data += data[:1]  # 使数据闭环
    angles += angles[:1]  # 使角度闭环

    # 设置图形
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 使用 (r, g, b, a) 格式的 RGBA 颜色值
    ax.fill(angles, data, color=(179 / 255, 181 / 255, 198 / 255, 0.2), linewidth=3, linestyle='solid',
            label='测试因子分')
    ax.plot(angles, data, color=(179 / 255, 181 / 255, 198 / 255, 1), linewidth=3)  # 绘制边框
    ax.scatter(angles, data, color=(179 / 255, 181 / 255, 198 / 255, 1), s=100, edgecolor='white', zorder=5)  # 绘制数据点

    # 设置刻度
    ax.set_ylim(0, 5)  # 设置最大值为 5
    ax.set_yticks([1, 2, 3, 4, 5])  # 设置刻度
    ax.set_yticklabels([str(i) for i in range(1, 6)], fontsize=10)

    # 设置标签和标题
    ax.set_xticks(angles[:-1])  # 移除最后一个重复的角度
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_title('测试因子分', size=14, color='black', position=(0.5, 1.1))

    # 添加图例
    ax.legend(loc='upper right', fontsize=10)

    # 显示图形
    plt.show()


# 示例数据
items = [
    {"itemname": "项1", "itemnameZh": "项一", "itemscore": 3},
    {"itemname": "项2", "itemnameZh": "项二", "itemscore": 4},
    {"itemname": "项3", "itemnameZh": "项三", "itemscore": 2},
    {"itemname": "项4", "itemnameZh": "项四", "itemscore": 5},
    {"itemname": "项5", "itemnameZh": "项五", "itemscore": 3}
]

gen_radar(items)

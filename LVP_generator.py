import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


def plot_load_velocity_power(loads, velocities, action_name, time):
    # 使用numpy进行线性拟合，获取斜率和截距
    slope, intercept = np.polyfit(velocities, loads, 1)

    # 定义v0（直线与横坐标相交点的x值）和F0（直线截距）
    v0 = -intercept / slope if slope != 0 else 0
    F0 = intercept

    # 定义x轴上的点，从0到3，并生成更多的点用于绘制平滑的曲线
    fitted_velocities = np.linspace(0, 3, 300)
    fitted_loads = slope * fitted_velocities + intercept

    # 计算功率 = 负荷 * 速度
    powers = [load * velocity for load, velocity in zip(fitted_loads, fitted_velocities)]

    # 找到功率最大时的负荷值（OPL）
    max_power = max(powers)
    OPL_index = powers.index(max_power)
    OPL = fitted_loads[OPL_index]

    # 计算 R^2 值
    y_mean = np.mean(loads)
    ss_total = sum((load - y_mean) ** 2 for load in loads)
    ss_residual = sum((load - (slope * velocity + intercept)) ** 2 for load, velocity in zip(loads, velocities))
    r_squared = 1 - (ss_residual / ss_total)

    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制原始点
    ax.scatter(velocities, loads, color='blue', label='Data Points')

    # 绘制拟合直线
    ax.plot(fitted_velocities, fitted_loads, linestyle='-', color='b', label='Velocity-Load Line')

    # 绘制速度-功率线
    ax.plot(fitted_velocities, powers, linestyle='-', color='r', label='Velocity-Power Curve')

    # 设置图形标题和轴标签
    ax.set_title(f'{action_name} - Velocity-Load and Power Profile at {time}')
    ax.set_xlabel('Velocity')
    ax.set_ylabel('Load')
    ax.legend()

    # 设置横轴每格为10，范围0-3；纵轴每格为0.1，范围0-200
    ax.set_xticks([v / 10.0 for v in range(0, 31, 1)])  # 横轴每10为一格
    ax.set_yticks(range(0, 201, 5))  # 纵轴每5为一格

    # 限制横轴和纵轴范围
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 200)

    # 显示网格
    ax.grid(True)

    # 在图的外面显示v0, F0, OPL 和 R^2
    plt.figtext(0.15, 0.85, f'v0 (Intersection with x-axis) = {v0:.2f}', fontsize=12, ha='left', color='g')
    plt.figtext(0.15, 0.80, f'F0 (Y-intercept) = {F0:.2f}', fontsize=12, ha='left', color='m')
    plt.figtext(0.15, 0.75, f'OPL (Load at Max Power) = {OPL:.2f}', fontsize=12, ha='left', color='c')
    plt.figtext(0.15, 0.70, f'R^2 = {r_squared:.4f}', fontsize=12, ha='left', color='b')

    # 显示图形
    plt.show()


def on_submit():
    try:
        # 获取输入的动作名称和时间
        action_name = entry_action_name.get()
        time = entry_time.get()

        # 获取输入的点数
        num_points = int(entry_num_points.get())

        # 获取每个点的load和velocity值
        loads = []
        velocities = []
        for i in range(num_points):
            load = float(load_entries[i].get())
            velocity = float(velocity_entries[i].get())
            loads.append(load)
            velocities.append(velocity)

        # 调用绘图函数
        plot_load_velocity_power(loads, velocities, action_name, time)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numeric values.")


# 创建主窗口
root = tk.Tk()
root.title("Velocity-Load and Power Profile Generator")

# 动作名称输入框
tk.Label(root, text="Action Name:").grid(row=0, column=0, padx=10, pady=5)
entry_action_name = tk.Entry(root)
entry_action_name.grid(row=0, column=1, padx=10, pady=5)

# 时间输入框
tk.Label(root, text="Time:").grid(row=1, column=0, padx=10, pady=5)
entry_time = tk.Entry(root)
entry_time.grid(row=1, column=1, padx=10, pady=5)

# 输入点数
tk.Label(root, text="Number of Points:").grid(row=2, column=0, padx=10, pady=5)
entry_num_points = tk.Entry(root)
entry_num_points.grid(row=2, column=1, padx=10, pady=5)

# 动态生成点的输入框
load_entries = []
velocity_entries = []

root.geometry("800x350")

def create_input_fields():
    num_points = int(entry_num_points.get())

    # 清除之前生成的输入框
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 2:
            widget.grid_forget()

    load_entries.clear()
    velocity_entries.clear()

    for i in range(num_points):
        tk.Label(root, text=f"Load {i + 1}:").grid(row=i + 3, column=0, padx=10, pady=5)
        load_entry = tk.Entry(root)
        load_entry.grid(row=i + 3, column=1, padx=10, pady=5)
        load_entries.append(load_entry)

        tk.Label(root, text=f"Velocity {i + 1}:").grid(row=i + 3, column=2, padx=10, pady=5)
        velocity_entry = tk.Entry(root)
        velocity_entry.grid(row=i + 3, column=3, padx=10, pady=5)
        velocity_entries.append(velocity_entry)

    submit_button = tk.Button(root, text="Generate Profile", command=on_submit)
    submit_button.grid(row=num_points + 3, columnspan=4, pady=10)


# 创建生成输入框按钮
generate_button = tk.Button(root, text="Generate Input Fields", command=create_input_fields)
generate_button.grid(row=2, column=2, padx=10, pady=5)

# 启动主循环
root.mainloop()

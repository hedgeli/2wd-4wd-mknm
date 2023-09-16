import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from numpy import cos, sin, arccos, arctan2, sqrt, pi
import matplotlib
import webbrowser as web

# >> pyinstaller -F -w ZYRot_2D_Simu_Ctrl.py

matplotlib.rc("font", family='Microsoft YaHei')
plt.rcParams['axes.unicode_minus'] = False

x_pos = 0.0
y_pos = 0.0
v_dir = 0.0
dir_step = 15

v_mmps = 100
v_step = 10
w_degps = 30
w_step = 5
step_max_t_s = 6.0

curve_x = [0]
curve_y = [0]
delta_s = 0.2
flag_update_posxy = 0

v_curve = [0]
w_curve = [0]
t_axis_s = [0]
t_index = 0


def open_zyrot_2wd(event):
    web.open('https://gitee.com/zyrot/2wd-4wd-mknm')
    
def update_position(axes):
    global x_pos
    global y_pos
    global v_dir
    global v_mmps
    global curve_x
    global curve_y
    global delta_s
    global dir_step

    plt.ion() # 开启交互模式不然没有动画效果
#     print('update_position()')
    draw_robot(axes,x_pos,y_pos, v_dir)
    axes.plot(curve_x, curve_y, 'b')
#     plt.pause(delta_s)
    plt.ioff()
    

    
    
def move_to_xy(axes):
    
    global x_pos
    global y_pos
    global v_dir
    global v_mmps
    global curve_x
    global curve_y
    global delta_s
    global dir_step

    plt.ion() # 开启交互模式不然没有动画效果
    print('move_to_xy()')
    for i in range(5):
        x_pos = x_pos + v_mmps*cos(v_dir*pi/180)*delta_s
        y_pos = y_pos + v_mmps*sin(v_dir*pi/180)*delta_s
        curve_x.append(x_pos)
        curve_y.append(y_pos)
        draw_robot(axes,x_pos,y_pos, v_dir)
        axes.plot(curve_x, curve_y, 'b')
        plt.pause(delta_s)
    plt.ioff()

def draw_robot( axes, xpos=0.0, ypos=0.0, dirt=0.0, para1=0):
    axes.clear()
    ax_pos_xy.grid()
    ax_pos_xy.set_xlim(-1500,1500)
    ax_pos_xy.set_ylim(-1500,1500)
    ax_pos_xy.plot([-15, 15], [0, 0], c="red",linewidth=2,zorder=2)
    ax_pos_xy.plot([0, 0], [-15, 15], c="red",linewidth=2,zorder=2)
    axes.scatter(xpos, ypos, s=500, c="green", zorder=1)
    dirt_r = (dirt%360) * pi / 180
    arror_len = 65
    xend = xpos + cos(dirt_r)*arror_len
    yend = ypos + sin(dirt_r)*arror_len
    axes.plot([xpos, xend], [ypos, yend], c="red", linewidth=3,zorder=1)

fig = plt.figure()
plt.get_current_fig_manager().set_window_title("ZYRot_2D_仿真与控制")
ax_pos_xy = fig.add_axes([0.07, 0.05, 0.5, 0.9])
ax_pos_xy.grid()
ax_pos_xy.set_xlim(-1000,1000)
ax_pos_xy.set_ylim(-1000,1000)
ax_pos_xy.plot([-15, 15], [0, 0], c="red",linewidth=2,zorder=2)
ax_pos_xy.plot([0, 0], [-15, 15], c="red",linewidth=2,zorder=2)
ax_curve  = fig.add_axes([0.625, 0.55, 0.35, 0.4])
ax_curve.grid()

widget_dx = 0.07
widget_dy = 0.065
x_space = 0.008
y_space = 0.008
x_base = 0.6
y_base = 0.2
widget_axes = [[0 for i in range(4)] for j in range(4)]
for i in range(4):
    for j in range(4):
        widget_axes[i][j] = [x_base+widget_dx*j, y_base+widget_dy*i,
                             widget_dx-x_space,widget_dy-y_space]

char_width = 0.02
text_area = [0 for i in range(4)]
for i in range(4):
    text_area[i] = [x_base+widget_dx*i+char_width/2, y_base-widget_dy,
                             widget_dx-x_space-char_width/2,widget_dy-y_space]
text_v = TextBox(fig.add_axes(text_area[0]), 'v', textalignment="center")
text_w = TextBox(fig.add_axes(text_area[1]), 'w', textalignment="center")
text_t = TextBox(fig.add_axes(text_area[2]), 't', textalignment="center")
text_3 = TextBox(fig.add_axes(text_area[3]), '', textalignment="center")

text_v.set_val(str(int(v_mmps)))
text_w.set_val(str(int(w_degps)))
text_t.set_val(str(round(step_max_t_s,1)))

def v_edit(v_strin):
    global v_mmps
    try:
        v_int = int(float(v_strin))
        v_mmps = v_int
    except:
        print('Please input a number for v(mmps).')
        text_v.set_val(str(int(v_mmps)))
        
def w_edit(w_strin):
    global w_degps
    try:
        w_int = int(float(w_strin))
        w_degps = w_int
    except:
        print('Please input a number for w(degps).')
        text_w.set_val(str(int(w_degps)))
        
def t_edit(t_strin):
    global step_max_t_s
    try:
        t_float_1 = round(float(t_strin),1)
        step_max_t_s = t_float_1
    except:
        print('Please input a number for t(second).')
        text_t.set_val(str(round(step_max_t_s,1)))

text_v.on_submit(v_edit)
text_w.on_submit(w_edit)
text_t.on_submit(t_edit)

btn_0_0 = Button(fig.add_axes(widget_axes[0][0]), 'V-')
btn_0_1 = Button(fig.add_axes(widget_axes[0][1]), 'W-')
btn_0_2 = Button(fig.add_axes(widget_axes[0][2]), '暂停')
btn_0_3 = Button(fig.add_axes(widget_axes[0][3]), '帮助')
btn_0_3.on_clicked(open_zyrot_2wd)

btn_1_0 = Button(fig.add_axes(widget_axes[1][0]), 'V+')
btn_1_1 = Button(fig.add_axes(widget_axes[1][1]), 'W+')
btn_1_2 = Button(fig.add_axes(widget_axes[1][2]), '启动')
btn_1_3 = Button(fig.add_axes(widget_axes[1][3]), 'Clear')

btn_2_0 = Button(fig.add_axes(widget_axes[2][0]), '左移')
btn_2_1 = Button(fig.add_axes(widget_axes[2][1]), '后退')
btn_2_2 = Button(fig.add_axes(widget_axes[2][2]), '右移')
btn_2_3 = Button(fig.add_axes(widget_axes[2][3]), '停止')

btn_3_0 = Button(fig.add_axes(widget_axes[3][0]), '左转')
btn_3_1 = Button(fig.add_axes(widget_axes[3][1]), '前进')
btn_3_2 = Button(fig.add_axes(widget_axes[3][2]), '右转')
btn_3_3 = Button(fig.add_axes(widget_axes[3][3]), '连接')

def v_add(event, axes=text_v):
    global v_mmps,v_step
    v_mmps += v_step
    axes.set_val(str(int(v_mmps)))
    
def v_sub(event, axes=text_v):
    global v_mmps,v_step
    v_mmps -= v_step
    axes.set_val(str(int(v_mmps)))
    
def w_add(event, axes=text_w):
    global w_degps,w_step
    w_degps += w_step
    axes.set_val(str(int(w_degps)))
    
def w_sub(event, axes=text_w):
    global w_degps,w_step
    w_degps -= w_step
    axes.set_val(str(int(w_degps)))
    
    
def run_vxy_w(event, axes=ax_pos_xy):
    
    global x_pos
    global y_pos
    global v_dir
    global v_mmps
    global curve_x
    global curve_y
    global delta_s
    global step_max_t_s
    global dir_step
    global w_degps
    global t_index, t_axis_s

    plt.ion() # 开启交互模式不然没有动画效果
#     print('run_vxy_w()')
    for i in range(int(step_max_t_s/delta_s)):
        v_dir = v_dir + w_degps*delta_s
        x_pos = x_pos + v_mmps*cos(v_dir*pi/180)*delta_s
        y_pos = y_pos + v_mmps*sin(v_dir*pi/180)*delta_s
        curve_x.append(x_pos)
        curve_y.append(y_pos)
        t_axis_s.append((i+t_index+1) * delta_s)
        ax_curve.clear()
        ax_curve.plot(t_axis_s, curve_x, 'r', label='posX')
        ax_curve.plot(t_axis_s, curve_y, 'g', label='posY')
        ax_curve.grid()
        draw_robot(axes,x_pos,y_pos, v_dir)
        axes.plot(curve_x, curve_y, 'b')
        plt.pause(delta_s)
    ax_curve.legend()
    t_index = t_index + int(step_max_t_s/delta_s)
    plt.ioff()
    
    
btn_1_0.on_clicked(v_add)
btn_0_0.on_clicked(v_sub)
btn_1_1.on_clicked(w_add)
btn_0_1.on_clicked(w_sub)
btn_1_2.on_clicked(run_vxy_w)

def start(event,axes=ax_pos_xy):
    flag_update_posxy = 1
    update_position(axes)
    

def turn_left(event, axes=ax_pos_xy):
    global dir_step
    global v_dir, flag_update_posxy
    v_dir = v_dir + dir_step
    flag_update_posxy = 1
    print('v_dir:', v_dir, 'flag,', flag_update_posxy)
    update_position(axes)
    

def move_front(event, axes=ax_pos_xy):
    global x_pos
    global y_pos
    global v_dir, flag_update_posxy
    global v_mmps
    global curve_x
    global curve_y
    global delta_s
    global dir_step
    global t_axis_s, t_index
    
    x_pos = x_pos + v_mmps*cos(v_dir*pi/180)*delta_s
    y_pos = y_pos + v_mmps*sin(v_dir*pi/180)*delta_s
    curve_x.append(x_pos)
    curve_y.append(y_pos)
    t_index = t_index + 1
    t_axis_s.append((t_index+1) * delta_s)
    flag_update_posxy = 1
    update_position(axes)
    
    
    
def move_back(event, axes=ax_pos_xy):
    global x_pos
    global y_pos
    global v_dir, flag_update_posxy
    global v_mmps
    global curve_x
    global curve_y
    global delta_s
    global dir_step
    global t_axis_s, t_index
    
    x_pos = x_pos - v_mmps*cos(v_dir*pi/180)*delta_s
    y_pos = y_pos - v_mmps*sin(v_dir*pi/180)*delta_s
    curve_x.append(x_pos)
    curve_y.append(y_pos)
    t_index = t_index + 1
    t_axis_s.append((t_index+1) * delta_s)
    flag_update_posxy = 1
    update_position(axes)
    

def turn_right(event, axes=ax_pos_xy):
    global dir_step
    global v_dir, flag_update_posxy
    v_dir = v_dir - dir_step
    flag_update_posxy = 1
    update_position(axes)


def stop_robot(event, axes=ax_pos_xy):
    global v_mmps, flag_update_posxy
    v_mmps = 0
    flag_update_posxy = 1
    
    

btn_3_0.on_clicked(turn_left)
btn_3_1.on_clicked(move_front)
btn_3_2.on_clicked(turn_right)
btn_3_3.on_clicked(stop_robot)
btn_2_1.on_clicked(move_back)


update_position(ax_pos_xy)
while 1:
    if flag_update_posxy == 1:
        print('flag_update_posxy,',flag_update_posxy)
        flag_update_posxy = 0
#         move_to_xy(ax_pos_xy)
    plt.show()
#     print('after plt.show()')


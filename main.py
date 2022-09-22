from tkinter import filedialog
from audio import *
from deef import *
from tkinter import *


class GUI:
    def __init__(self, init_window_name):
        self.type = 'sound'
        self.allowed = True
        self.pause = False
        self.sca_max = 3150
        self.t0 = [100]
        self.k0 = None
        self.tick = 0
        self.init_window_name = init_window_name
        self.photo_start = PhotoImage(file=r'./ico/start.png')
        self.photo_stop = PhotoImage(file=r'./ico/stop.png')
        self.photo_pause = PhotoImage(file=r'./ico/pause.png')
        self.photo_left = PhotoImage(file=r'./ico/left.png')

    def set_init_window(self):  # 设置窗口
        self.init_window_name.title("GIM")  # 窗口名
        self.init_window_name.geometry("350x200")  # 设置窗口大小
        self.init_window_name.resizable(0, 0)  # 窗口大小不可变
        self.init_window_name.iconbitmap('./ico/1.ico')

        # 标签
        self.lbl0 = Label(self.init_window_name, text="Hello")
        self.lbl0.grid(column=0, row=0)
        self.lbl = Label(self.init_window_name, text="Hello")
        self.lbl.grid(column=0, row=2,columnspan=3)
        self.lbl1 = Label(self.init_window_name, text='')  # 时间
        self.lbl1.grid(column=3, row=2, columnspan=1)
        # 按钮
        self.btn = Button(self.init_window_name, text="选择文件", command=self.click_file)  # 选择文件
        self.btn.grid(column=0, row=1, padx=2)

        self.btn4 = self.btn = Button(self.init_window_name, text='try test', relief=FLAT, command=self.try_test)  # 左
        self.btn4.grid(column=3, row=4)

        self.btn3 = self.btn = Button(self.init_window_name, image=self.photo_left, relief=FLAT,
                                      command=self.left)  # 左
        self.btn3.grid(column=1, row=1)

        self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT,
                           command=lambda: self.start_listen(tick=self.tick))  # 开始试听
        self.btn2.grid(column=2, row=1)

        self.btn1 = Button(self.init_window_name, image=self.photo_stop, relief=FLAT, command=self.stop_listen)  # 停止
        self.btn1.grid(column=3, row=1)

        # 滑动条
        self.scale = Scale(self.init_window_name,
                           from_=0,
                           to=self.sca_max,
                           orient=HORIZONTAL,  # 设置Scale控件平方向显示
                           length=345,  # 长度
                           showvalue=False,  # 关闭标签
                           activebackground='black',  # 指向滑块时颜色
                           sliderrelief='flat',  # 滑块样式
                           bg='black',  # 颜色
                           borderwidth=0,  # 边框宽度
                           resolution=0,  # 关闭鼠标左键步进
                           # command=lambda: change_label_number(2)
                           # command=self.sca,
                           )  # 调用执行函数，数值显示在 Label控件中
        self.scale.grid(row=3, columnspan=4)
        # self.scale.focus_set()
        self.scale.bind('<B1-Motion>', self.sca_tap)
        self.scale.bind('<Button-1>', self.sca_tap)
        self.scale.bind('<ButtonRelease-1>', self.sca_release)

        # 单选框（选择模式）
        def select():
            dict = {1: 'sound', 2: 'tap', 3: 'press'}
            strings = dict.get(v.get())
            self.type = strings
            print(strings)

        v = IntVar()
        for name, num1 in [('试听', 1), ('tap', 2), ]:
            self.radio_button = Radiobutton(self.init_window_name, variable=v, text=name, value=num1,
                                            command=select, indicatoron=False)
            self.radio_button.grid(row=4, column=num1 - 1)



    def sca_tap(self, value):
        self.allowed = False  # 关闭滑动条自动移动
        self.stop_thread()
        t_x = min(max(10 * (value.x - 17), 0), 3150)
        if self.k0:
            self.lbl1.configure(text=time_short(round((t_x * round(self.t0[-1])) / 3150)) + '/' + time_short(round(self.t0[-1])))
        self.scale.set(t_x)

    def sca_release(self, value):
        self.stop_thread()
        self.tick = Fraction(self.scale.get(), 3150) * self.t0[-1]
        if self.k0:
            if self.pause:
                def f():
                    if self.k0:
                        self.listen(self.k0, self.t0, self.tick)
                self.thread = Mythread(f)
                self.thread.daemon = True
                self.thread.start()
                self.btn2.grid_forget()
                self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT, command=self.re_listen)
                self.btn2.grid(column=2, row=1)  # 设置为暂停按钮
            else:
                self.start_listen(tick=self.tick)
            self.allowed = True

    def click_file(self):  # 选择文件
        self.file = filedialog.askopenfilename(filetypes=(("txt", "*.txt"), ("all", "*.*")),
                                               initialdir='./music/')
        if self.file:
            print(self.file)
            self.lbl.configure(text=self.file[1+self.file.rindex('/'):-4])  # 设置标签（歌名

            self.stop_thread()
            self.k0, self.t0 = txt_kt_mixed(self.file)  # 读取数据
            self.pause = False
            self.btn2.grid_forget()
            self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT, command=self.start_listen)
            self.btn2.grid(column=2, row=1)  # 设置为开始按钮
            self.scale.set(0)
            self.lbl1.configure(text=time_short(0) + '/' + time_short(round(self.t0[-1])))

    def left(self):
        self.pause = False
        self.stop_thread()
        self.tick = 0
        self.scale.set(0)
        self.lbl1.configure(text=time_short(0) + '/' + time_short(round(self.t0[-1])))
        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT, command=self.start_listen)
        self.btn2.grid(column=2, row=1)  # 设置为开始按钮

    def start_listen(self, tick=0):  # 开始试听
        #print(tick)
        self.pause = False
        self.allowed = True
        self.tick = tick
        self.stop_thread()
        def f():
            if self.k0:
                self.listen(self.k0, self.t0, tick)

        self.thread = Mythread(f)
        self.thread.daemon = True
        self.thread.start()

        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_pause, relief=FLAT, command=self.pause_listen)
        self.btn2.grid(column=2, row=1)  # 设置为暂停按钮

    def stop_thread(self):  # 停止
        try:
            stop_Mythread(self.thread)
        except:
            'False'

    def listen(self, k, t, tick=0):
        if self.type == 'tap':
            sleep(1)
        #print(k)
        #print(t)
        #print(self.type)
        def wait():
            while time() - t0 < t[i]:  # 等待时间
                sleep(0.005)
                if self.allowed:
                    self.scale.set(self.sca_max * (time() - t0) / self.t0[-1])
                    self.lbl1.configure(text=time_short(round(time() - t0)) + '/' + time_short(round(self.t0[-1])))
        i = 0
        while t[i] < tick:  # 定位播放位置
            i += 1

        t0 = time() - tick
        while i < len(k):  # 从指定位置开始播放
            while self.pause:  # 暂停
                t0 = time() - t[i]
                sleep(0.005)
            if self.type == 'sound':  # 试听模式
                for ii in k[i]:
                    sound[abc.index(ii)].play()
                wait()  # 等待时间
                for ii in k[i]:
                    sound[abc.index(ii)].fadeout(667)
            if self.type == 'tap':  # tap模式
                for iii in k[i]:
                    key.tap_key(iii)
                wait()
            i += 1
        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT,
                           command=lambda: self.start_listen(tick=self.tick))
        self.btn2.grid(column=2, row=1)  # 设置为开始按钮

    def pause_listen(self):
        self.pause = True
        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT, command=self.re_listen)
        self.btn2.grid(column=2, row=1)  # 设置为暂停按钮

    def re_listen(self):
        self.pause = False
        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_pause, relief=FLAT, command=self.pause_listen)
        self.btn2.grid(column=2, row=1)  # 设置为开始按钮

    def stop_listen(self):
        self.pause = True
        self.stop_thread()
        self.btn2.grid_forget()
        self.btn2 = Button(self.init_window_name, image=self.photo_start, relief=FLAT,
                           command=lambda: self.start_listen(tick=self.tick))
        self.btn2.grid(column=2, row=1)  # 设置为开始按钮
        self.scale.set(self.sca_max * (self.tick / self.t0[-1]))
        self.lbl1.configure(text=time_short(round(self.tick)) + '/' + time_short(round(self.t0[-1])))

    def try_test(self):
        self.stop_thread()
        self.k0, self.t0 = txt_kt_mixed('./1.txt', p=False)  # 读取数据
        self.start_listen()
def start_win():
    w1 = Tk()
    window = GUI(w1)
    window.set_init_window()
    w1.mainloop()
    window.stop_thread()  # 按X后自动停止播放


start_win()

print('End')

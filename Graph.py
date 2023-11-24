from tkinter import *
from math import *


def partial(function, *a, **b):
    """Возвращает функцию с подставленными параметрами"""

    def func(*c, **d):
        function(*a, *c, **b, **d)

    return func


class BalloonWidget(Menu):
    """Подсказка"""

    def __init__(self, root, text="", delay=1, **args):
        """Инициализация"""
        super().__init__(root, **args)

        self.delay = delay * 1000

        self.label = Label(self, text=text)
        self.label.pack()
        self.master.bind('<Enter>', self.__post__)
        self.master.bind('<Leave>', self.__unpost__)
        self.master.bind('<Motion>', self.__unpost__)
        self.master.bind('<Button>', self.__unpost__)
        self.master.bind('<Key>', self.__unpost__)

    def post(self, x, y):
        """Переопределение"""
        super().post(x, y)

    def __post__(self, *event):
        """Событие"""
        self.after(self.delay, partial(self.post, self.master.winfo_rootx(),
                                       self.master.winfo_rooty() - self.winfo_reqheight()))

    def __unpost__(self, *event):
        """Событие"""
        self.unpost()


class ShowWindow(Toplevel):

    def exit(self):
        self.master.destroy()

    def geometry(self, **args):
        if "width" in args.keys():
            self.width = args["width"]
        super().geometry(str(self.width) + "x" + str(self.width))

    def __init__(self, root, width=600):
        super().__init__(root)
        self.resizable(False, False)
        self.attributes("-type", "dialog")
        self.geometry(width=width)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.canvas = Canvas(self, bd=1, relief=SOLID, highlightthickness=0, bg="#FFFFFF")
        self.canvas.place(x=0, y=0, relw=1, relh=1)

        self.points = dict()

    def clear(self, bg="#FFFFFF"):
        self.points = dict()
        self.canvas.create_rectangle(0, 0, self.width, self.width, fill=bg)

    def create_points(self, points):
        for i in range(len(points)):
            self.points[points[i]] = (self.width // 2 + (self.width // 2 - 50) * cos(2 * pi * i / len(points)),
                                      self.width // 2 - (self.width // 2 - 50) * sin(2 * pi * i / len(points)))
            self.canvas.create_oval(self.points[points[i]][0] - 5, self.points[points[i]][1] - 5,
                                    self.points[points[i]][0] + 5, self.points[points[i]][1] + 5,
                                    width=2, outline="#000000")
            self.canvas.create_text(self.points[points[i]][0] + (15 if self.points[points[i]][0] > self.width // 2 else -15),
                                    self.points[points[i]][1] - (15 if self.points[points[i]][1] < self.width // 2 else -15), text=points[i])

    def create_edge(self, point1, point2):
        self.canvas.create_line(*self.points[point1], *self.points[point2])


class Application(Tk):

    def __add__(self):
        window = Toplevel(self)
        window.resizable(False, False)
        window.geometry("200x130")
        window.attributes("-type", "dialog")
        window.attributes("-topmost", True)
        window.bind('<FocusOut>', lambda event: window.focus_force())
        Label(window, bd=1, relief=SOLID, bg="#FFFFFF", text="Вершина1-Вершина2").place(x=10, y=10, w=180, h=30)
        e = Entry(window, highlightthickness=0, bd=1, relief=SOLID, justify=CENTER)
        e.focus_force()
        e.place(x=10, y=50, w=180, h=30)

        def func(self, entry, window):
            self.box.insert(END, entry.get())
            window.destroy()
        Button(window, bd=1, relief=SOLID, bg="#FFFFFF", text="Добавить",
               command=partial(func, self, e, window)).place(x=10, y=90, w=180, h=30)

    def __remove__(self):
        a = self.box.curselection()
        if a:
            self.box.delete(a[0])

    def __draw__(self):
        points = self.n.get().split(" ")
        edges = list(self.box.get(0, END))
        for i in range(len(edges)):
            edges[i] = edges[i].split("-")
        self.show.clear()
        self.show.create_points(points)
        for i in edges:
            self.show.create_edge(*i)

    def __init__(self):
        super().__init__()
        self.attributes("-type", "dialog")
        self.geometry("310x650")
        self.resizable(False, False)

        self.show = ShowWindow(self)

        Label(self, text="Вершины", bg="#FFFFFF", bd=1, relief=SOLID).place(x=10, y=10, w=290, h=31)
        a = Frame(self, bd=1, relief=SOLID)
        a.place(x=10, y=40, h=50, w=290)
        self.n = Entry(a, justify=CENTER, bd=1, relief=SOLID, highlightthickness=0)
        self.n.place(x=10, y=10, w=-20, h=-20, relw=1, relh=1)
        self.n.focus_force()

        Label(self, text="Ребра", bg="#FFFFFF", bd=1, relief=SOLID).place(x=10, y=100, w=290, h=31)
        b = Frame(self, bd=1, relief=SOLID)
        b.place(x=10, y=130, w=290, h=470)
        yscroll = Scrollbar(b, orient=VERTICAL, relief=SOLID, bd=1)
        yscroll.place(x=260, y=10, w=20, relh=1, h=-60)
        self.box = Listbox(b, bd=1, relief=SOLID, highlightthickness=0, bg="#FFFFFF", yscrollcommand=yscroll.set)
        self.box.place(x=10, y=10, w=-39, h=-60, relw=1, relh=1)
        yscroll.config(command=self.box.yview)

        Button(b, text="Добавить", command=self.__add__, bg="#FFFFFF", bd=1, relief=SOLID, highlightthickness=0).place(x=10, rely=1, y=-40, w=130, h=30)
        Button(b, text="Удалить", command=self.__remove__, bg="#FFFFFF", bd=1, relief=SOLID, highlightthickness=0).place(x=150, rely=1, y=-40, w=130, h=30)
        Button(self, text="Построить", command=self.__draw__, bg="#FFFFFF", bd=1, relief=SOLID, highlightthickness=0).place(x=10, y=610, w=290, h=30)

        self.mainloop()


Application()

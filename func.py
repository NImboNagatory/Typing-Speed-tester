from data.dict import rand_list
import random
from tkinter import Frame, Canvas, RAISED, Text, Label, ttk, END, StringVar, Tk
from PIL import Image, ImageTk
from math import floor


class Word_Hangar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#bac8ff")
        self.Timer = Label(self, text="60", font=("bold", 20), bg="#bac8ff")
        self.canvas = Canvas(self, width=400, relief=RAISED, height=300, border=0, bg="#edf2ff", highlightthickness=0)
        self.separate = ttk.Separator(self, orient='horizontal')
        self.canvas.create_text(200, 150, text="Words")
        self.input_trigger = StringVar()
        self.user_input = Text(self, width=48, height=10, relief=RAISED, highlightthickness=1,
                               highlightbackground="black", bg="#edf2ff")
        self.user_input.tag_configure("center", justify='center', font=("bold", 20))
        self.user_input.insert(1.0, " ")
        self.user_input.tag_add("center", "1.0", "end")
        self.user_input.focus()
        self.hint = Label(self, text="Hint : Use Space-bar, it's faster", bg="#bac8ff")
        self.Timer.grid(row=0)
        self.canvas.grid(padx=5, pady=10, row=1)
        self.separate.grid(row=2, sticky="ew")
        self.user_input.grid(row=3, padx=7)
        self.hint.grid(row=4)
        self.data = None
        self.timer = None
        self.timer_running = False
        self.space_blocked = False
        self.default_time = 60
        self.select_rand_words()
        self.cor_write = 0
        self.wro_write = []
        self.wro_write_dup = []

    def show_resoults(self):
        self.clear_canvas()
        self.hint["text"] = "Hint : Press Space-bar to Continue"
        if len(self.wro_write) == 0:
            self.canvas.create_text(200, 150, text=f"You wrote {self.cor_write} words in 60 seconds", font=("bold", 15),
                                    fill="#748ffc")
        elif len(self.wro_write) > 0:
            self.canvas.create_text(200, 50, text=f"You wrote {self.cor_write} words in 60 seconds", font=("bold", 15),
                                    fill="#748ffc")
            print_data = ''
            for char in self.wro_write:
                print_data += f"{char} You wrote :{self.wro_write_dup[self.wro_write.index(char)][0]}\n"
            self.canvas.create_text(200, 100,
                                    text=f"{len(self.wro_write)} of them Wrong\n{print_data}",
                                    font=("bold", 10),
                                    fill="#748ffc")

    def start_timer(self, event):
        if self.space_blocked is False:
            if self.timer_running is not True:
                self.timer_tick(self.default_time)
                self.timer_running = True

    def rest_timer(self):
        self.Timer["text"] = "60"
        self.after_cancel(self.timer)
        self.timer_running = False

    def timer_tick(self, time):
        time_seconds = round(time % 60, 2)
        if time_seconds <= 9:
            if time_seconds == 0:
                time_seconds = "Start"
            else:
                time_seconds = f"0{time_seconds}"

        self.Timer["text"] = f"{time_seconds}"
        if time > 0:
            self.timer = self.after(1000, self.timer_tick, time - 1)
        else:
            self.rest_timer()
            self.clear_user_input()
            self.data = None
            self.canvas.update()
            self.show_resoults()
            self.disable_space()

    def disable_space(self):
        self.space_blocked = True
        self.canvas.update()
        self.after(5000)
        self.canvas.update()
        self.space_blocked = False

    def clear_canvas(self):
        self.canvas.delete("all")

    def select_rand_words(self):
        self.data = random.sample(rand_list, 1)
        self.clear_canvas()
        self.canvas.create_text(200, 150, text=self.data, font=("bold", 40), fill="#748ffc")

    def clear_user_input(self):
        self.user_input.delete("1.0", END)
        self.user_input.tag_configure("center", justify='center')
        self.user_input.insert(1.0, " ")
        self.user_input.tag_add("center", "1.0", "end")
        self.user_input.focus()

    def check_if_cor(self, event):
        if self.data is not None:
            if self.user_input.get("1.0", END).strip() is not None:
                if self.user_input.get("1.0", END).strip() == self.data[0].strip():
                    self.select_rand_words()
                    self.clear_user_input()
                    self.cor_write += 1
                elif self.user_input.get("1.0", END).strip() != self.data[0].strip():
                    self.wro_write_dup.append(self.data)
                    self.wro_write.append(self.user_input.get("1.0", END).strip())
                    self.select_rand_words()
                    self.clear_user_input()
        elif self.data is None:
            self.select_rand_words()
            self.clear_user_input()
            self.cor_write = 0
            self.wro_write.clear()


def bind_space(gui, func):
    return gui.bind("<space>", func)


def bind_any_kay(gui, func):
    return gui.bind("<KeyPress>", func)


def ico(gui):
    icon = Image.open('data/w.jpg')
    photo = ImageTk.PhotoImage(icon)
    return gui.wm_iconphoto(False, photo)

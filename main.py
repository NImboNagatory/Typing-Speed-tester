from tkinter import Tk
from func import ico, Word_Hangar, bind_space, bind_any_kay
gui = Tk()

ico(gui)

gui.config(bg="#bac8ff")

gui.title("My Speed")

gui.geometry("411x555")

gui.resizable(False, False)

display = Word_Hangar(gui)

bind_space(gui, display.check_if_cor)

bind_any_kay(gui, display.start_timer)

display.grid(row=0, column=0)

gui.mainloop()

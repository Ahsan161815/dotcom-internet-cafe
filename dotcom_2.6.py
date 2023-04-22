from window import Window_stuff
from pc import Pc
import datetime
from os import (path, remove)
from tkinter import (Tk, messagebox)


class App(Window_stuff):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pc6 = Pc(self, 6)
        self.pc7 = Pc(self, 7)
        self.pc8 = Pc(self, 8)
        self.pc9 = Pc(self, 9)
        self.pc10 = Pc(self, 10)
        self.pc11 = Pc(self, 11)
        self.pc12 = Pc(self, 12)
        self.pc13 = Pc(self, 13)
        self.pc14 = Pc(self, 14)
        self.pc15 = Pc(self, 15)
        self.pc16 = Pc(self, 16)
        self.pc17 = Pc(self, 17)
        self.pc18 = Pc(self, 18)
        self.pc19 = Pc(self, 19)
        self.pc20 = Pc(self, 20)
        self.pc27 = Pc(self, 27)
        self.pc28 = Pc(self, 28)
        self.pc29 = Pc(self, 29)
        self.pc30 = Pc(self, 30)
        self.pc31 = Pc(self, 31)
        self.pc32 = Pc(self, 32)
        self.pc33 = Pc(self, 33)
        self.pc34 = Pc(self, 34)
        self.pc35 = Pc(self, 35)
        self.pc36 = Pc(self, 36)
        self.pc37 = Pc(self, 37)
        self.pc38 = Pc(self, 38)
        self.pc39 = Pc(self, 39)
        self.pc40 = Pc(self, 40)
        self.pc41 = Pc(self, 41)

# if not running then run the software      
if __name__ == '__main__':

    root = Tk()
    application = App(root)
    application.dead = False
    root.mainloop()
    
    # Do this when software closed
    application.dead = True

#Stopwatch Program
from tkinter import *
from tkinter import PhotoImage, messagebox
import time
import winsound
import os

class Stopwatch:
    def __init__(self,sw):
        self.sw= sw
        self.sw.title("Stopwatch")
        self.sw.geometry("1050x550")
        self.sw.config(bg="#000000")

        self.run= False
        self.st, self.et = 0,0

        self.buildui()
    def loadimg(self, filen, size=(64,64)):
        if not os.path.exists(filen):
            return None
        try:
            img= PhotoImage(file=filen)
        except Exception:
            return None

        w,h = img.width(), img.height()
        tw, th= size

        sw, sh= max(1, w//tw), max(1, h//th)
        scale= max(sw,sh)
        img= img.subsample(scale,scale)
        return img
        
    def buildui(self):
        fg="#00FFAA"
        msgcol="#FFEE58"

        Label(self.sw, text="Stopwatch".upper(), font=("times new roman",30,"bold"), bg="#000000", fg=fg).pack(pady=10)
        self.timel= Label(self.sw, text="00:00:00.00", font=("times new roman",40,"bold"), bg="#000000", fg=fg)
        self.timel.pack(pady=10)

        self.msg= Label(self.sw, text="Start", font=("times new roman",14), bg="#000000", fg=msgcol)
        self.msg.pack()

        self.si= self.loadimg("start.png")
        self.li= self.loadimg("lap.png")
        self.ri= self.loadimg("reset.png")

        f= Frame(self.sw, bg="#000000")
        f.pack(pady=(6,14))

        if self.si:
            self.sb= Button(f, image=self.si, bd=0, command=self.start, activebackground="#000000")
        else:
            self.sb= Button(f, text="Start", width=8, command= self.start)
        self.sb.grid(row=0,column=0,padx=12)

        if self.li:
            self.lb= Button(f, image=self.li, bd=0, command=self.lap, state="disabled", activebackground="#000000")
        else:
            self.lb= Button(f, text="Lap", width=8, command= self.lap, state="disabled")
        self.lb.grid(row=0,column=1,padx=12)

        if self.ri:
            self.rb= Button(f, image=self.ri, bd=0, command=self.reset, state="disabled", activebackground="#000000")
        else:
            self.rb= Button(f, text="Reset", width=8, command= self.reset, state="disabled")
        self.rb.grid(row=0,column=2,padx=12)

        lapf= Frame(self.sw, bg="#000000")
        lapf.pack(pady=(6,14), fill=X, padx=20)
        self.laplist= Listbox(lapf, width=36, height=10,
                              bg="#111111", fg="#00FFAA",
                              font=("times new roman", 12),
                              activestyle='none', highlightthickness=0, bd=0)
        self.laplist.pack(side=LEFT, fill=BOTH, expand=True)

        scroll= Scrollbar(lapf, orient=VERTICAL, command=self.laplist.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.laplist.config(yscrollcommand=scroll.set)

    def formattime(self,t):
        m, s, h= int(t//60), int(t%60), int((t-int(t))*100)
        return f"{m:02d}:{s:02d}:{h:02d}"

    def beep(self, freq=800, dur=120):
        try:
            winsound.Beep(freq,dur)
        except Exception:
            pass

    def update(self):
        if self.run:
            now= time.time()
            self.et= now - self.st
            self.timel.config(text=self.formattime(self.et))
            self.sw.after(10,self.update)

    def start(self):
        if not self.run:
            self.run= True
            self.st= time.time() - self.et
            self.update()

            self.sb.config(command=self.pause)
            self.lb.config(state='normal')
            self.rb.config(state='normal')
            self.msg.config(text="Stopwatch Running!")
            #messagebox.showinfo("Stopwatch Started","Stopwatch has started.")

            self.beep(900,120)

    def pause(self):
        if self.run:
            self.run= False
            self.sb.config(command=self.start)
            self.msg.config(text="Paused")
            #messagebox.showinfo("Stopwatch Paused","Stopwatch has paused.")

            self.beep(500,120)

    def reset(self):
        if messagebox.askyesno("Reset","Do you want to reset the Stopwatch?"):
            self.run= False
            self.et= 0

            self.timel.config(text="00:00:00.00")
            self.sb.config(command=self.start)
            self.lb.config(state="disabled")
            self.rb.config(state="disabled")

            self.laplist.delete(0,END)
            self.msg.config(text="Reset Complete")
            #messagebox.showinfo("Stopwatch Reset","Stopwatch has restarted.")

            self.beep(300,150)

    def lap(self):
        lapt= self.formattime(self.et)
        self.laplist.insert(END, f"Lap {self.laplist.size()+1}: {lapt}")
        self.msg.config(text= f"Lap {self.laplist.size()} Recorded")
        
        self.beep(700,120)

if __name__=="__main__":
    sw= Tk()
    app= Stopwatch(sw)
    sw.mainloop()

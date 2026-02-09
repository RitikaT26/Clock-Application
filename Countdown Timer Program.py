#Countdown Timer Program
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import winsound

class CountdownTimer:
    def __init__(self,timer):
        self.timer= timer
        self.timer.title("Countdown Timer")
        self.timer.geometry("400x300")
        self.timer.config(bg="#cfa9bf")
        self.timer.resizable(False,False)

        self.timeleft=0
        self.run=False

        #-------------heading and particulars------------
        Label(timer, text="COUNTDOWN TIMER", font=("times new roman",20,"bold"),bg="#cfa9bf", fg="#933d6f").pack(pady=5)
    
        Label(timer, text="Hours: ",bg="#cfa9bf").place(x=30,y=60)
        Label(timer, text="Minutes: ",bg="#cfa9bf").place(x=140,y=60)
        Label(timer, text="Seconds: ",bg="#cfa9bf").place(x=260,y=60)

        self.hh= Entry(timer, width=5, font=("timer new roman",12), justify="center")
        self.hh.place(x=80,y=60)
        self.mm= Entry(timer, width=5, font=("timer new roman",12), justify="center")
        self.mm.place(x=200,y=60)
        self.ss= Entry(timer, width=5, font=("timer new roman",12), justify="center")
        self.ss.place(x=320,y=60)

        self.label= Label(timer,text="00:00:00",font=("times new roman",36,"bold"), fg="#87285f", bg="#cfa9bf")
        self.label.pack(pady=50)

        #-------------------buttons----------------------
        ip= Image.open("pause button.png")
        reip= ip.resize((50,50))
        self.img1= ImageTk.PhotoImage(reip)

        ir= Image.open("resume button.png")
        reir= ir.resize((50,50))
        self.img2= ImageTk.PhotoImage(reir)

        ipl= Image.open("play button.png")
        reipl= ipl.resize((50,50))
        self.img3= ImageTk.PhotoImage(reipl)

        bf= Frame(timer, bg="#cfa9bf")
        bf.pack(pady=10)

        b1= Button(bf, image=self.img3, command=self.start, bd=0)
        b1.grid(row=0,column=0, padx=10)
        b2= Button(bf, image=self.img1, command=self.pause, bd=0)
        b2.grid(row=0,column=1, padx=10)
        b3= Button(bf, image=self.img2, command=self.resume, bd=0)
        b3.grid(row=0,column=2, padx=10)

    def start(self):
        if not self.run:
            try:
                h= int(self.hh.get() or 0)
                m= int(self.mm.get() or 0)
                s= int(self.ss.get() or 0)
            except:
                messagebox.showerror("Error","Enter Valid Numbers!")
                return

            self.timeleft= h*3600 + m*60 + s
            if self.timeleft <= 0:
                messagebox.showerror("Error","Time should be greater than zero.")
                return
            self.run=True
            self.countdown()

    def pause(self):
        self.run=False

    def resume(self):
        self.run=False
        self.timeleft=0
        self.label.config(text="00:00:00")

    def countdown(self):
        if self.run and self.timeleft > 0:
            hr= self.timeleft//3600
            mi= (self.timeleft%3600)//60
            se= self.timeleft%60

            self.label.config(text=f"{hr:02d}:{mi:02d}:{se:02d}")
            self.timeleft -= 1
            self.timer.after(1000,self.countdown)

        elif self.timeleft==0 and self.run:
            self.run= False
            self.label.config(text="00:00:00")
            for i in range(5):
                winsound.Beep(1200,500)
            messagebox.showinfo("Time's Up!","Time's Up! Countdown Finished!")
            self.hh.delete(0,END)
            self.mm.delete(0,END)
            self.ss.delete(0,END)

timer= Tk()
CountdownTimer(timer)
timer.mainloop()

from tkinter import *
from tkinter import messagebox,ttk, filedialog
import time
import threading
import winsound
import mysql.connector as sq
from datetime import datetime, timedelta

con= sq.connect(user='root',passwd='2115',host='localhost',database='project')
cursor= con.cursor()

alarml={}   #time:alarm label pairs
snoozea= set()

#------alarm functions-------
def alarmcheck():
    while True:
        time.sleep(1)
        ct=time.strftime("%H:%M:%S")

        for i in alarml:
            if ct==i and i not in snoozea:
                info= alarml[i]
                playalarm(info["tone"])
                
                resp= messagebox.askyesno("Alarm",f"Alarm Ringing for {alarml[i]['label']} at {i}! Snooze for 5 minutes?")
                cursor.execute("delete from alarm where atime='{}' ".format(i))
                con.commit()
                if resp:
                    snoozealarm(i)
                else:
                    del alarml[i]
                    
                refreshalarmlist()
                break

def setalarm():
    alarmt= f"{hd.get()}:{md.get()}:{sd.get()}"
    alabel= a1.get().strip()
    tp= atunep.get()

    if not alabel:
        messagebox.showwarning("Input Required","Please enter a alarm name.")
        return

    if alarmt in alarml:
        messagebox.showwarning("Duplicate Alarm",f"Alarm already set for {alarmt}")
        return

    alarml[alarmt]= {"label": alabel, "tone": tp}
    refreshalarmlist()
    #updatealarml()
    messagebox.showinfo("Alarm Set",f"Alarm set for {alabel} at {alarmt}")
    cursor.execute("insert into alarm values('{}','{}','{}')".format(alabel,alarmt,tp))
    con.commit()

    a1.delete(0,END)
    hd.set("00")
    md.set("00")
    sd.set("00")

def refreshalarmlist():
    for i in aftree.get_children():
        aftree.delete(i)

    for t,info in alarml.items():
        aftree.insert("",END,values=(info["label"],t, info["tone"] if info["tone"] else "Default"))
    '''
    cursor.execute("select * from alarm")
    fetch= cursor.fetchall()
    aftree.felete(*aftree.get_children())
    '''

def deletealarm():
    s= aftree.selection()
    if not s:
        messagebox.showwarning("No Selection","Please select an alarm to remove.")
        return
    i= aftree.item(s[0])
    l,ts,_= i['values']

    if ts in alarml:
        del alarml[ts]
        cursor.execute("delete from alarm where atime='{}' ".format(ts))
        con.commit()
        refreshalarmlist()
        messagebox.showinfo("Alarm Deleted",f"Alarm '{l}' at {ts} has been removed.")

#-------snooze alarm---------
def snoozealarm(at):
    dt= datetime.strptime(at, "%H:%M:%S") + timedelta(minutes=5)
    nt= dt.strftime("%H:%M:%S")
    if nt in alarml:
        messagebox.showwarning("Alarm Time Conflict", f"Another alarm already set for {nt}.")
        return

    alarml[nt]= alarml[at]
    del alarml[at]
    cursor.execute("update alarm set atime='{}' where atime='{}' ".format(nt,at))
    con.commit()

    #snoozea.add(nt)
    
    messagebox.showinfo("Alarm Snoozed", f"Alarm snoozed to {nt}.")
    refreshalarmlist()
    #alarmcheck()

#----customize alarm tune----
def choosealarmtune():
    fn= filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if fn:
        atunep.set(fn)
        

def playalarm(atune):
    try:
        if atune:
            winsound.PlaySound(atune, winsound.SND_FILENAME)
        else:
            for _ in range(5):
                winsound.Beep(1000,500)
    except:
        for _ in range(5):
            winsound.Beep(1000,500)

clock= Tk()
clock.title("Alarm Clock")
clock.geometry("500x600")
clock.resizable(False,False)
clock.config(background="#ffc0c0")

#----------widgets----------
Label(clock,text="ALARM CLOCK", font=("times new roman",26,"bold"), fg="#ff8080",bg="#ffc0c0").place(x=0,y=0,relwidth=1)

l= Label(clock)
l.place(x=0,y=50,relwidth=1)
def display():
    t=time.strftime("%d.%m.%Y\n%I:%M:%S %p")
    l.config(text=t,font=("times new roman",50,"bold"),bg="#ff8080",fg="#ffc0c0")
    l.after(100,display)
display()

Label(clock, text="Alarm Name: ",font=("times new roman",12), bg="#ffc0c0").place(x=20,y=220)
a1= Entry(clock)
a1.place(x=130,y=220,width=200)

Label(clock, text="Alarm Time (HH:MM:SS): ",font=("times new roman",12), bg="#ffc0c0").place(x=20,y=265)

hd= StringVar(clock)
hd.set("00")
md= StringVar(clock)
md.set("00")
sd= StringVar(clock)
sd.set("00")
OptionMenu(clock, hd, *[f"{i:02d}" for i in range(24)]).place(x=200,y=260)
Label(clock, text="Hr",font=("times new roman",12), bg="#ffc0c0").place(x=260,y=265)
OptionMenu(clock, md, *[f"{i:02d}" for i in range(60)]).place(x=300,y=260)
Label(clock, text="Min",font=("times new roman",12), bg="#ffc0c0").place(x=360,y=265)
OptionMenu(clock, sd, *[f"{i:02d}" for i in range(60)]).place(x=400,y=260)
Label(clock, text="Sec",font=("times new roman",12), bg="#ffc0c0").place(x=460,y=265)

atunep= StringVar(clock)
Button(clock, text="Choose Tone: " ,command= choosealarmtune).place(x=350,y=220)
#Label(clock, textvariable= atunep, bg="#ffc0c0", font=("times new roman",9)).place(x=400,y=220)

Button(clock, text="Set Alarm", command= setalarm, font=("times new roman",12)).place(x=230,y=310)

#----------alarm list--------
alarmf= Frame(clock,relief=RIDGE)
alarmf.place(x=25,y=350,height=230,width=450)

aftree= ttk.Treeview(alarmf, columns=('Alarm Name','Alarm Time'))#, 'Alarm Tune'))
aftree.pack(fill=BOTH, expand=True)
aftree.heading('Alarm Name',text='Alarm Name')
aftree.heading('Alarm Time',text='Alarm Time')
#aftree.heading('Alarm Tune',text='Alarm Tune')
aftree.column('Alarm Name',width=200, anchor='center')
aftree.column('Alarm Time',width=100, anchor='center')
#aftree.column('Alarm Tune',width=100, anchor='center')

aftree.config(show='headings', padding=(5,5,5,5))

cursor.execute('select * from alarm')
row= cursor.fetchall()
for i in row:
    aftree.insert('','end',values=i)

#threading.Thread(target=alarmcheck, daemon=True)

threading.Thread(target= alarmcheck, daemon=True).start()
clock.mainloop()

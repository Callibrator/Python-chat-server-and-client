#------------------------------------------
#Created by Callibrator                   |
#callibrator21@gmail.com                  |
#Using Python 3.2                         |
#Simple (very simple) chat server         |
#------------------------------------------


from socket import *
from tkinter import *
import _thread as thread
import time
from tkinter.messagebox import showinfo

c = socket(AF_INET,SOCK_STREAM)
recv_thread = ''


def connect(ip,port,name):
         global c
         global recv_thread
         
         try:
                  c = socket(AF_INET,SOCK_STREAM)
                  c.connect((ip,int(port)))
                  c.send(name.encode())
                  recv_thread = thread.start_new_thread(receve,())
                  con.config(state='disabled')
                  
         except:
                  showinfo("Error","Unable to connect\nCheck the server-ip,port or your connection")
                  


def receve():
         global c

         while True:
                  buffer = ''
                  while True:
                           try:
                                    buffer = c.recv(1024)
                                    if buffer != None and buffer != "" and buffer !=" ":
                                             chat.config(state="normal")
                                             chat.insert(END,buffer.decode())
                                             chat.config(state="disabled")
                           except:
                                    showinfo("Error","Oups an error have occured please reconnect")
                                    return 0
                           
def send(msg):
         global c
         if msg == "" or msg == None or msg == " ":
                  return 0
         try:
                  c.send(msg.encode()+b"\n")
                  sendbox.delete(0,END)
         except:
                  showinfo("Error","Error: Unable to send message\nTry to reconnect or check your internet connection")
                  

root = Tk()
root.title("Chat client")

frame = Frame(root)
frame.pack()


Label(frame,text="IP: ").pack(side=LEFT)

ipbox = Entry(frame)
ipbox.pack(side=LEFT)

Label(frame,text="Port: ").pack(side=LEFT)

portbox = Entry(frame,width=4)
portbox.pack(side=LEFT)
portbox.insert(0,30)

Label(frame,text="Nick-Name: ").pack(side=LEFT)

namebox = Entry(frame)
namebox.pack(side=LEFT)
namebox.insert(0,"Guest")

con = Button(frame,text="Connect",command=lambda:connect(ipbox.get(),portbox.get(),namebox.get()))
con.pack(side=LEFT)

chatframe = Frame(root)
chatframe.pack()

chat = Text(chatframe,state="disabled")
chat.pack()

sendframe = Frame(root)
sendframe.pack(fill=X)

Label(sendframe,text="Send: ").pack(side=LEFT)
sendbox = Entry(sendframe)
sendbox.pack(fill=X,side=LEFT)
sendbox.bind("<Return>",lambda event:send(sendbox.get()))


Button(sendframe,text="Send",command=lambda:send(sendbox.get())).pack(side=LEFT)
Button(sendframe,text="Show users",command=lambda:send("!users")).pack(side=LEFT)

root.mainloop()

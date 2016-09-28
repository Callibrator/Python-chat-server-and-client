from tkinter import *
from socket import*
import _thread as thread
import time
from tkinter.messagebox import showinfo

#------------------------------------------
#Created by Callibrator                   |
#callibrator21@gmail.com                  |
#Using Python 3.2                         |
#Simple (very simple) chat server         |
#------------------------------------------

class client:
         def __init__(self,client,addr,name):
                  self.client = client
                  self.address = addr
                  self.name = name
                  
         



s = socket(AF_INET,SOCK_STREAM)
clients = []
ip =''
port = 30

def config(): #configure ip port and bind the socket
         global ip
         global port
         global s

         try:
                  ip = ipbox.get()
                  port = int(portbox.get())

                  s.bind((ip,port))
                  s.listen(244)
         except:
                  showinfo("Error","Unable to start server\nCheck your ip or your port")
                  

def listening(): #Waiting for client's to connect
         global s
         global clients
         while True:
                  cl,addr = s.accept()
                  name = cl.recv(1024).decode()
                  log.insert(END,"%s Connected to the server\n"%addr[0])
                  clients.append(client(cl,addr,name))
                  for i in clients:
                           i.client.send(("%s connected to the server\n"%clients[-1].name).encode())
                           #i.client.send(b"Test\n")
                           #print(("%s connected to the server\n"%clients[-1].name).encode())
                  thread.start_new_thread(receving,(clients[-1],))

def terminate_client(name):
         global clients
         for i in clients:
                  try:
                           i.client.send(name.encode() +b" Leave from the server\n")
                  except:
                           pass

                  
def receving(c):
         global s
         global clients
         
         while True:
                  try:
                           buffer = c.client.recv(1024)
                           #print("Received")
                  except:
                           #print("Client error")
                           terminate_client(c.name)
                           clients.remove(c)
                           return 0
                  #print(buffer)
                  if buffer == b"!users\n":
                           #print("aa")
                           c.client.send(b"User List: \n")
                           for i in clients:
                                    c.client.send(i.name.encode() +b"\n")
                           c.client.send(b"End of the list\n")
                           continue
                  
                  if buffer == b"\n":
                           continue
                  
                  for i in clients:
                           try:
                                    #print("Sending Message")
                                    if buffer.decode() != None and buffer.decode() !=" " and buffer.decode() != "":
                                             i.client.send(c.name.encode() +b" Says: "+buffer)
                           except:
                                    #print("Error on send")
                                    pass

                  

                  

def start_server():
         config()
         thread.start_new_thread(listening,())
         log.insert(END,"Server is running\n")




def showusers():
         for i in clients:
                  log.insert(END,"User: %s ip: %s\n"%(i.name,i.address[0]))
def banuser():
         global clients
         win = Toplevel()
         win.title("Ban user from chat box")

         winframe = Frame(win)
         winframe.pack()


         lst = Listbox(winframe)
         lst.pack(fill=X)

         for i in clients:
                  lst.insert(END,"Name: %s, address : %s"%(i.name,i.address[0]))


         def ban(ID):
                  try:
                           clients.remove(clients[int(ID[0])])
                           showinfo("INFO","User banned from the server")
                  except:
                           pass




         Button(winframe,text="Ban user from chat",command=lambda:ban(lst.curselection())).pack(fill=X)


         

         win.mainloop()
         
#Simple GUI
root = Tk()
root.title("Chat Server")

frame = Frame(root)
frame.pack()

Label(frame,text="IP: ").pack(side=LEFT)
ipbox = Entry(frame)
ipbox.pack(side=LEFT)
Label(frame,text="Port: ").pack(side=LEFT)
portbox = Entry(frame)
portbox.pack(side=LEFT)
portbox.insert(0,port)

Button(frame,text="Start Server",command=start_server).pack(side=LEFT)
#Button(frame,text="User Status",command=banuser).pack(side=LEFT)

infoframe = Frame(root)
infoframe.pack()

Label(infoframe,text="Logs").pack()

logframe = Frame(root)
logframe.pack()

log = Text(logframe)
log.pack()


root.mainloop()

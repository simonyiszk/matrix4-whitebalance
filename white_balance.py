import socket
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from time import sleep

IPbase = "10.6."
UDP_PORT = 2000
btColor = "gray"

sock = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP

def sendWbalance(level, col, arr_r, arr_g, arr_b):
    global UDP_PORT
    UDP_IP = IPbase + str(level) + "." + str(col)
    #UDP_IP = "192.168.137.255"
    MESSAGE = bytearray()
    MESSAGE.extend("SEM".encode())
    MESSAGE.extend(bytes([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
    MESSAGE.extend(arr_r)
    MESSAGE.extend(arr_g)
    MESSAGE.extend(arr_b)
    print("IP=" + UDP_IP + ", PORT=" + str(UDP_PORT) + ":")
    print(MESSAGE)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    


szintszam=13
ablakszam=8
arr_r = [0 for x in range(7)]
arr_g = [0 for x in range(7)]
arr_b = [0 for x in range(7)]


root = tk.Tk()
global_select = tk.IntVar()
global_select.set(2)
global_select_last = global_select.get()

win_select = [[0 for x in range(ablakszam)] for y in range(szintszam)]
wb_sliders = [[0 for x in range(8)] for y in range(3)]  #[color(RGB)][threshold]
wb_saves = [[0 for x in range(8)] for y in range(3)]  #[color(RGB)][threshold]
wb_global_sliders = [0 for x in range(3)] #RGB

def update_wb_from_sliders():
    print("TODO")

def color_change(x,y):
    win_select[y][x] = win_select[y][x] ^ 1
    update_colors()
    print(18-y, x+5)
    
def select_all(event):
    print("sel all")
    for x in range(ablakszam):
        for y in range(szintszam):
            win_select[y][x] = 1
    update_colors()
    
def deselect_all(event):
    print("desel all")
    for x in range(ablakszam):
        for y in range(szintszam):
            win_select[y][x] = 0
    update_colors()
    
def send_single(event):
    arr = [[0 for x in range(7)] for y in range(3)]
    for c in range(3):
        for k in range(7):
            arr[c][k] = wb_sliders[c][k].get()
    for x in range(ablakszam):
        for y in range(szintszam):
            if win_select[y][x]:
                sendWbalance(18-y,x+5, arr[0], arr[1], arr[2])

def send_all(event):
    arr = [[0 for x in range(7)] for y in range(3)]
    for c in range(3):
        for k in range(7):
            arr[c][k] = wb_sliders[c][k].get()
    sendWbalance(255, 255, arr[0], arr[1], arr[2])
    

def main():
    global btColor
    frameRooms=tk.Frame(root)
    frameRooms.grid(row=1,column=0, stick='N')
    frameTopBtns=tk.Frame(root)
    frameTopBtns.grid(row=0,column=0)
    frameBotBtns=tk.Frame(root)
    frameBotBtns.grid(row=2,column=0, rowspan=2, stick='N')
    frameSliders=tk.Frame(root)
    frameSliders.grid(row=1,column=1, padx=10, rowspan=2)
    frameGlobalSliders=tk.Frame(root)
    frameGlobalSliders.grid(row=1,column=2, rowspan=2, padx = 10)
    frameGlobalSelect=tk.Frame(root)
    frameGlobalSelect.grid(row=0,column=1, columnspan=2)
    
    btSelectAll = tk.Button(frameTopBtns, text="Select all")
    btColor = btSelectAll.cget('bg')
    btSelectAll.bind('<Button-1>', select_all)
    btSelectAll.grid(column=0, row=0, pady=20, padx = 10)
    btDeselectAll = tk.Button(frameTopBtns, text="Deselect all")
    btDeselectAll.bind('<Button-1>', deselect_all)
    btDeselectAll.grid(column=1, row=0, pady=20, padx = 10)
    
    btSend = tk.Button(frameTopBtns, text="Send")
    btSend.bind('<Button-1>', send_single)
    btSend.grid(column=3, row=0, pady=20, padx = 10)

    btSendAll = tk.Button(frameTopBtns, text="SendAll")
    btSendAll.bind('<Button-1>', send_all)
    btSendAll.grid(column=4, row=0, pady=20, padx = 10)

    btSave = tk.Button(frameTopBtns, text="Save", command=save_conf_dialog)
    btSave.grid(column=5, row=0, pady=20, padx = 10)

    btLoad = tk.Button(frameTopBtns, text="Load", command=load_conf_dialog)
    btLoad.grid(column=6, row=0, pady=20, padx = 10)


    tk.Radiobutton(frameGlobalSelect, text="Manual scale", variable=global_select, value=1, command=update_sliders_en).grid(column=0, row=0)
    tk.Radiobutton(frameGlobalSelect, text="Global scale", variable=global_select, value=2, command=update_sliders_en).grid(column=1, row=0)


    root.btn=  [[0 for x in range(ablakszam)] for y in range(szintszam)] 
    for x in range(ablakszam):
         for y in range(szintszam):
            y2 = 18 - y
            root.btn[y][x] = tk.Button(frameRooms,command= lambda x1=x, y1=y: color_change(x1,y1))
            root.btn[y][x].grid(column=x, row=y+2)
            ss = str(y2)+str(x+5)
            if (x+5 < 10): ss = str(y2) + "0" + str(x+5)
            root.btn[y][x].config(text=ss, width=8, height=1, activebackground=root.btn[y][x].cget('background'))

    for c in range(3):
        for k in range(7):
            wb_sliders[c][k] = tk.Scale(frameSliders, from_=63, to=0, length=150)
            wb_sliders[c][k].grid(column=k, row=c, pady = 20)
            wb_sliders[c][k].set(1 << k)
            wb_sliders[c][k].config(bg=get_color(c))
        wb_global_sliders[c] = tk.Scale(frameGlobalSliders, from_=1, to=0, resolution=0.01, length=150, command= lambda x, c=c: global_slider_update(x, c))
        wb_global_sliders[c].grid(column=0, row=c, pady = 20)
        wb_global_sliders[c].set(1)
        wb_global_sliders[c].config(bg=get_color(c))
    save_sliders()
    global_select.set(2)
    update_sliders_en()
    root.mainloop()

def update_colors():
    for x in range(ablakszam):
         for y in range(szintszam):
            if win_select[y][x]:
                root.btn[y][x].config(bg="#fff176", activebackground="#fff176")
            else:
                root.btn[y][x].config(bg=btColor, activebackground=btColor)
                
def get_color(c):
    if c==0: return "#ef5350"
    if c==1: return "#66bb6a"
    if c==2: return "#29b6f6"
        
def global_slider_update(val, c):
    if global_select.get() == 1: return
    wb_sliders[c][0].config(state="normal")
    wb_sliders[c][0].set(1)
    wb_sliders[c][0].config(state="disabled")
    for k in range(1, 7):
        tmp = round((1 << k) * wb_global_sliders[c].get(), 0)
        tmp = int(tmp)
        wb_sliders[c][k].config(state="normal")
        if tmp > wb_sliders[c][k-1].get(): wb_sliders[c][k].set(tmp)
        else: wb_sliders[c][k].set( wb_sliders[c][k-1].get()+1)
        wb_sliders[c][k].config(state="disabled")
                
def update_sliders_en():
    global global_select_last
    if global_select.get() == 1:
        for c in range(3):
            wb_global_sliders[c].config(state="disabled")
            wb_global_sliders[c].config(bg=btColor)
            for k in range(7):
                wb_sliders[c][k].config(state="normal")
                wb_sliders[c][k].config(bg=get_color(c))
    else:
        for c in range(3):
            wb_global_sliders[c].config(state="normal")
            wb_global_sliders[c].config(bg=get_color(c))
            for k in range(7):
                wb_sliders[c][k].config(state="disabled")
                wb_sliders[c][k].config(bg=btColor)
    if global_select_last != global_select.get():
        if global_select.get() == 1: load_sliders()
        else:
            save_sliders()
            global_slider_update(0, 0)
            global_slider_update(0, 1)
            global_slider_update(0, 2)
    global_select_last = global_select.get()
    
def load_sliders():
    for c in range(3):
        for k in range(7):
            wb_sliders[c][k].set(wb_saves[c][k])

def save_sliders():
    for c in range(3):
        for k in range(7):
            wb_saves[c][k] = wb_sliders[c][k].get()

def save_conf_dialog():
    filepath = asksaveasfilename(initialdir = ".",title = "Save to...",defaultextension=".txt", filetypes = (("TXT files","*.txt"),))
    if filepath != "": save_configs(filepath)

def load_conf_dialog():
    filepath = askopenfilename(initialdir = ".",title = "Open config file.",filetypes = (("TXT files","*.txt"),("all files","*.*")))
    load_configs(filepath)

def save_configs(filepath):
    print("save configs: " + filepath)
    f = open(filepath, "w")
    for y in range(szintszam):
        st = ""
        for x in range(ablakszam):
            if win_select[y][x]: st = st + "1,"
            else: st = st + "0,"
        st = st[:-1] + "\n"
        f.write(st)
    f.write("\n")
    f.write(str(global_select.get()) + "\n")
    f.write("\n")

    if global_select.get() == 1: save_sliders()
    for c in range(3):
        st = ""
        for k in range(7):
            st = st + str(wb_saves[c][k]) + ","
        st = st[:-1] + "\n"
        f.write(st)
    f.write("\n")

    for c in range(3):
        st =str(wb_global_sliders[c].get()) + "\n"
        f.write(st)
    
    f.close()

def load_configs(filepath):
    global global_select_last
    print("load configs: " + filepath)
    f = open(filepath, "r")
    for y in range(szintszam):
        line = f.readline()
        data = line.split(",")
        for x in range(ablakszam):
            win_select[y][x] = int(data[x])
    update_colors()

    f.readline()
    line = f.readline()
    tmp_global_select = int(line)
    f.readline()
    for c in range(3):
        line = f.readline()
        data = line.split(",")
        for k in range(7):
            wb_saves[c][k] = int(data[k])
    f.readline()
    for c in range(3):
        line = f.readline()
        wb_global_sliders[c].config(state="normal")
        wb_global_sliders[c].set(float(line))
        wb_global_sliders[c].config(state="disabled")

    global_select_last = tmp_global_select
    global_select.set(tmp_global_select)
    update_sliders_en()
    if tmp_global_select == 1:
        load_sliders()
    else:
        global_slider_update(0, 0)
        global_slider_update(0, 1)
        global_slider_update(0, 2)

    f.close()

#print("UDP target IP:", UDP_IP)
#print("UDP target port:", UDP_PORT)
#print("message:", MESSAGE)


# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
s = 0
#master = tk.Tk()
main()



        
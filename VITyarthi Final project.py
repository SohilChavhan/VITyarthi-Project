


from tkinter import *
from tkinter import messagebox as msg_box

buk_gener_list={"Fantasy":["The Lord of the Rings","Dune","A Game of Thrones","Mistborn: The Final Empire","The Name of the Wind"],"Classics":["Pride and Prejudice","To Kill a Mockingbird","1984","The Great Gatsby","Moby Dick"],"Science Fiction":["Foundation","Ender's Game","Neuromancer","Do Androids Dream of Electric Sheep?","The Martian"],"Thriller":["The Girl with the Dragon Tattoo","Gone Girl","The Da Vinci Code"],"Biography":["Steve Jobs","Becoming","Long Walk to Freedom"],"Self Help Books":["Rich Dad Poor Dad","Deep Work","Do it Today","Psychology of Money"]}
buk_out_list=[]
see_box_list={}
take_box_list={}
back_box_list=None
win_see_one=None
win_take_one=None
win_back_one=None

def get_all_dem_buk():
    lst=[]
    for k in buk_gener_list: lst.extend(buk_gener_list[k])
    return lst

def rfrsh_dis_box(bx,dt):
    if bx and bx.winfo_exists():
        bx.delete(0,END)
        for i in dt: bx.insert(END,i)

def do_updat_evryting():
    for g,b in see_box_list.items(): rfrsh_dis_box(b,buk_gener_list.get(g,[]))
    for g,b in take_box_list.items(): rfrsh_dis_box(b,buk_gener_list.get(g,[]))
    rfrsh_dis_box(back_box_list,buk_out_list)

def put_new_buk_in(txt_in,opt_in):
    nam_buk=txt_in.get().strip()
    typ_buk=opt_in.get()
    if not nam_buk:
        msg_box.showerror("Error","Put name of the book pls")
        return
    if typ_buk=="Select Genre":
        msg_box.showerror("Error","kindly pick a genre")
        return
    if nam_buk in get_all_dem_buk():
        msg_box.showerror("Book already exists in the system")
        return
    buk_gener_list[typ_buk].append(nam_buk)
    buk_gener_list[typ_buk].sort()
    msg_box.showinfo("Issue success")
    do_updat_evryting()
    txt_in.winfo_toplevel().destroy()

def take_buk_home():
    wat_u_pik=[]
    for g,b in take_box_list.items():
        idx=b.curselection()
        for i in idx:
            n=b.get(i)
            wat_u_pik.append((g,n))
    if not wat_u_pik:
        msg_box.showerror("Kindly pick Something")
        return
    lst_nms=[]
    for g,n in wat_u_pik:
        if n in buk_gener_list[g]:
            buk_gener_list[g].remove(n)
            sStr=f"{n} | {g}"
            buk_out_list.append(sStr)
            lst_nms.append(n)
    msg_box.showinfo("Ok","You've take this:\n"+", ".join(lst_nms))
    do_updat_evryting()

def giv_buk_back(lb):
    pikd=lb.curselection()
    if not pikd:
        msg_box.showerror("Kindly pick a book to return")
        return
    nms_bck=[]
    for i in reversed(pikd):
        txt=lb.get(i)
        try:
            n,g=txt.split(" | ")
        except: continue
        if txt in buk_out_list: buk_out_list.remove(txt)
        if g in buk_gener_list:
            buk_gener_list[g].append(n)
            buk_gener_list[g].sort()
            nms_bck.append(n)
    msg_box.showinfo("Good","you've given back:\n"+", ".join(nms_bck))
    do_updat_evryting()

def mak_da_grid(mom_win,mod):
    global see_box_list,take_box_list
    if mod=='see':
        trgt=see_box_list; sel=NONE
    else:
        trgt=take_box_list; sel=EXTENDED
    trgt.clear()
    frm=Frame(mom_win,bg='lightyellow'); frm.pack(fill='both',expand=True,padx=10,pady=10)
    r=0; c=0
    for k in buk_gener_list:
        f=Frame(frm,bg='lightyellow',padx=5,pady=5)
        f.grid(row=r,column=c,sticky="n",padx=5,pady=5)
        Label(f,text=f"📖 {k}",font=("Arial",10,"bold"),bg='lightyellow',fg='darkblue').pack()
        b=Listbox(f,height=8,width=28,selectmode=sel,relief="groove")
        b.pack()
        trgt[k]=b
        rfrsh_dis_box(b,buk_gener_list[k])
        c+=1
        if c>2: c=0; r+=1
    return frm

def open_put_win():
    w=Toplevel(da_big_win)
    w.title("Add Book"); w.geometry('350x250'); w.configure(bg="lightyellow")
    Label(w,text="Book Title:",fg='blue',bg="lightyellow").pack(pady=(15,5))
    e=Entry(w,width=35); e.pack(pady=5)
    Label(w,text="Genre:",fg='blue',bg="lightyellow").pack(pady=5)
    ops=["Select Genre"]+list(buk_gener_list.keys())
    v=StringVar(w); v.set(ops[0])
    m=OptionMenu(w,v,*ops); m.config(width=20); m.pack(pady=5)
    def do_it(): put_new_buk_in(e,v)
    Button(w,text="Add Book",command=do_it,bg='white').pack(pady=20)

def open_see_win():
    global win_see_one
    if win_see_one and win_see_one.winfo_exists(): win_see_one.lift(); return
    win_see_one=Toplevel(da_big_win)
    win_see_one.title("View Library"); win_see_one.geometry('900x600'); win_see_one.configure(bg='lightyellow')
    Label(win_see_one,text="View Library Inventory",font=("Arial",16,"bold"),bg='lightyellow',fg='darkgreen').pack(pady=10)
    mak_da_grid(win_see_one,'see')

def open_take_win():
    global win_take_one
    if win_take_one and win_take_one.winfo_exists(): win_take_one.lift(); return
    win_take_one=Toplevel(da_big_win)
    win_take_one.title("Issue Books"); win_take_one.geometry('900x600'); win_take_one.configure(bg='lightyellow')
    Label(win_take_one,text="Pick Books (Ctrl/Cmd+Click)",font=("Arial",14),bg='lightyellow').pack(pady=10)
    mak_da_grid(win_take_one,'take')
    Button(win_take_one,text="Issue Selected Books",command=take_buk_home,height=2,width=20,bg='white').pack(pady=10)

def open_back_win():
    global win_back_one,back_box_list
    if win_back_one and win_back_one.winfo_exists(): win_back_one.lift(); return
    win_back_one=Toplevel(da_big_win)
    win_back_one.title("Return Books"); win_back_one.geometry('450x400'); win_back_one.configure(bg='lightyellow')
    Label(win_back_one,text="Return Back Issued Books",font=("Arial",12),bg='lightyellow').pack(pady=15)
    back_box_list=Listbox(win_back_one,height=12,width=50,selectmode=MULTIPLE)
    back_box_list.pack(padx=20,pady=5)
    rfrsh_dis_box(back_box_list,buk_out_list)
    def do_ret(): giv_buk_back(back_box_list)
    Button(win_back_one,text="Give Back",command=do_ret,bg='white').pack(pady=15)

da_big_win=Tk()
da_big_win.title("Library System"); da_big_win.geometry('500x350'); da_big_win.configure(bg='lightblue')
Label(da_big_win,text="Welcom Library",font=("Arial Bold",18),bg='lightblue',fg='navy').pack(pady=25)
frm_btn=Frame(da_big_win,bg='lightblue'); frm_btn.pack(pady=10)
Button(frm_btn,text="➕ Add Book",command=open_put_win,width=25).pack(pady=5)
Button(frm_btn,text="📋 View Book",command=open_see_win,width=25).pack(pady=5)
Button(frm_btn,text="📤 Issue Book",command=open_take_win,width=25).pack(pady=5)
Button(frm_btn,text="📥 Return Book",command=open_back_win,width=25).pack(pady=5)
da_big_win.mainloop()
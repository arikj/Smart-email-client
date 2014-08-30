from Tkinter import *
from yahoo import *
import time
import os
#global vars
mail_id="test start";
selected_folder="INBOX";

def bind(widget, event):
    def decorator(func):
        widget.bind(event, func)
        return func

    return decorator

tk = Tk()
tk.title("MailCat")
tk.geometry("1600x800")

top=Frame(tk,height=30,width=1600)
top.pack(side=TOP, expand=True, fill=BOTH)
top.config(background="#ECF9FF")

# Left frame to hold buttons
left = Frame(tk, width=100)
left.pack(side=LEFT, expand=True, fill=Y)
left.config(background="#E6D8E6")

# Right frame to hold display
right_top = Frame(tk, height=400, width=1200)
right_top.pack(expand=True, fill=BOTH)
right_top.config(background="#FFFFD1")

scrollbar = Scrollbar(right_top)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(right_top,yscrollcommand=scrollbar.set)
listbox.pack(fill=BOTH, expand=True)
listbox.insert(END, "Subject")

#for item in ["one", "two", "three", "two", "three", "four", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four", "two", "three", "four"]:
    #listbox.insert(END, item)
scrollbar.config(command=listbox.yview)  #to move list with scroll

@bind(listbox, '<<ListboxSelect>>')
def onselect(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	mail_id = 'You selected item'+str(index)+"  ,"+ str(value)+"\n";
	area.insert(END,mail_id)
	area.delete("1.0",END)
	for i in range(0,num_folders):
		try:
			if str(mail_header[folders[i]][index])==str(value):
				name_folder=folders[i]
				break
		except:
			pass
	try:
		filename = str(name_folder)+str(index+1)
		path='class_new'+str(i)+'/'+filename; 
		f=open(path).readlines()
		for line in f:
			area.insert(END,line)
	except:
		pass;
right_bottom = Frame(tk, height=400, width=1200)
right_bottom.pack(expand=True, fill=BOTH)
right_bottom.config(background="#ECF9FF")

area=Text(right_bottom, height=400, width=1200)
area.pack(expand=True)
area.config(background="#F2F2F2")


def get_mail_folder(c):
	listbox.delete(0,END)
	for element in mail_header[c]:
		listbox.insert(END, element)

# Buttons
#folders = ['Inbox', 'Sent', 'Trash', 'Intern']
for x in range(0,num_folders):
	print x
	b = Button(left,width=22, text=folders[x], command=lambda selected_folder=folders[x]:get_mail_folder(selected_folder))
	b.pack(side=TOP, expand=True, fill=X)

tk.mainloop()


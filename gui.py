from Tkinter import *


def bind(widget, event):
    def decorator(func):
        widget.bind(event, func)
        return func

    return decorator
    
    
master = Tk()

listbox = Listbox(master)

    
listbox.insert(END, "a list entry")
    
for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

listbox.pack()
@bind(listbox, '<<ListboxSelect>>')
def onselect(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	print 'You selected item %d: "%s"' % (index, value)

mainloop()

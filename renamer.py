import os.path
import os
import glob
from sys import pycache_prefix
import tkinter as tk
from tkinter import Tk, Toplevel, messagebox
from tkinter import filedialog as fd
import tkinter.ttk as ttk
import fitz
from PIL import Image, ImageTk
from fitz.fitz import Widget

def retern():
    if not (new_var.get() == root.file_name or new_var.get() == ''):
        mb = messagebox.askyesno("PDF Renamer", "You entered a new file name. Do you want to save it?")
        if not mb:
            new_var.set(root.file_name)
            retern()
        else:
            save()
    else:
        # Reset the starting parameters so that the program can be restarted without quitting
        root.counter = 0
        root.pathname = ''
        root.file_list = []
        # Destroy existing toplevels to prevent accumulation
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        # Switch back to top frame
        frm_top.grid(
            row=0,
            column=0,
            ipady=5,
            sticky="nsew"
        )
        frm_bottom.grid_remove()

def quit():
    root.destroy()

def next():
    if not (new_var.get() == root.file_name or new_var.get() == ''):
        mb = messagebox.askyesno("PDF Renamer", "You entered a new file name. Do you want to save it?")
        if not mb:
            new_var.set(root.file_name)
            next()
        else:
            save()
    else:
        # Destroy existing toplevels to prevent accumulation
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        # Increment the counter
        root.counter+=1
        # Check whether the last pdf has been viewed 
        if root.counter >= len(root.file_list):
            messagebox.showinfo('PDF Renamer', 'No more pdf files in the specified directory!')
            retern()
        else:
            # Create file_name (without the pdf extension)
            root.file_name = root.file_list[root.counter][len(root.pathname)+1:len(root.file_list[root.counter])-4]
            # Populate text field of lbl_current_is
            lbl_current_is.config(
                text = root.file_name + '.pdf' + '   #' + str(root.counter+1) + '/' + str(root.pdf_count)
            )
            # Populate text field of ent_new
            new_var.set(root.file_name)
            # Create the next pdf image (first page)
            location = root.file_list[root.counter]
            # Get the next pdf
            doc = fitz.open(location)
            # Get first page
            page = doc[0]
            # Render page as a pixmap (raster)image
            pix = page.get_pixmap()
            # Calculate zoom to fit the top-level window width (leaving 5 pixels to a side)
            zoom = 640 / pix.width
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            # Set the mode depending on alpha
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
            tkimage = ImageTk.PhotoImage(img)
            # Create top-level to view the pdf
            tl_next = tk.Toplevel(root, name='tl_next_name')
            tl_next.geometry("%dx%d+%d+%d" % (650, 790, root.winfo_x() + 675, root.winfo_y()))
            tl_next.title('First Page')
            lbl_pdf = tk.Label(master=tl_next, image=tkimage)
            lbl_pdf.image = tkimage
            lbl_pdf.pack(fill="both", expand=1)

def start():
    # Use file dialog to select directory
    root.pathname = fd.askdirectory(
        title='Select directory',
        # Start in current working directory
        initialdir='os.getcwd()'
    )
    # Check for any pdf files in selected directory
    if os.path.isdir(root.pathname):
        root.file_list = glob.glob(root.pathname + '/*.pdf')
        # Save total number of pdf files in the directory
        root.pdf_count = len(root.file_list)
        if root.pdf_count < 1:
            messagebox.showinfo('PDF Renamer', 'There are no pdf files in the specified directory.\n \
Click <Start> to try again or <Quit> to exit.')    
        else:
            if root.pathname and root.file_list:
                # Hide top frame
                frm_top.grid_remove()
                #show frm_bottom
                frm_bottom.grid(
                    row=1,
                    column=0,
                    sticky="nsew"
                )
                # Create file_name (without the pdf extension)
                root.file_name = root.file_list[0][len(root.pathname)+1:len(root.file_list[0])-4]
                # Populate text field of lbl_current_is
                lbl_current_is.config(
                    text = root.file_name + '.pdf' + '   #1' + '/' + str(root.pdf_count)
                )
                # Populate text field of ent_new
                new_var.set(root.file_name)
                # Create the pdf image (first page)
                location = root.file_list[0]
                doc = fitz.open(location)
                # Get first page
                page = doc[0]
                # Render page as a pixmap (raster)image
                pix = page.get_pixmap()
                # Calculate zoom to fit the top-level window width (leaving 5 pixels to a side)
                zoom = 640 / pix.width
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                # Set the mode depending on alpha
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
                tkimage = ImageTk.PhotoImage(img)
                # Destroy existing toplevels to prevent accumulation
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Toplevel):
                        widget.destroy()
                # Create top-level to view the pdf
                tl_start = tk.Toplevel(root, name='tl_start_name')
                tl_start.geometry("%dx%d+%d+%d" % (648, 790, root.winfo_x() + 675, root.winfo_y()))
                tl_start.title('First Page')
                tl_start.resizable(False, False)
                lbl_pdf = tk.Label(master=tl_start, image=tkimage)
                lbl_pdf.image = tkimage
                lbl_pdf.pack(fill="both", expand=1)
                
    else:
        messagebox.showinfo('PDF Renamer', 'That is not a valid directory. Try again.')

def save():
    src = root.pathname + '/' + root.file_list[root.counter][len(root.pathname)+1:len(root.file_list[root.counter])]
    dst = root.pathname + '/' + new_var.get() + '.pdf'
    # print('src: ', src)
    # print('dst: ', dst)
    if os.path.exists(dst):
        mb = messagebox.askyesno('PDF Renamer', 'A file with this name already exists. Overwrite?')
        if mb:
            os.remove(dst)
            os.rename(src, dst)
            messagebox.showinfo('PDF Renamer', 'The file was renamed.')
        else:
            new_var.set('')
            messagebox.showinfo('PDF Renamer', 'File name was not changed.')
    else:
        os.rename(src, dst)
        new_var.set('')
        messagebox.showinfo('PDF Renamer', 'The file was renamed.')
        #next()

# Initialize tk
root= tk.Tk()
style = ttk.Style(root)
style.theme_use('alt')
#root.eval('tk::PlaceWindow . center')
root.title("PDF Renamer")
root.geometry("+%d+%d" % (50, 100))
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, minsize=600, weight=1)
root.counter = 0
root.pdf_count = 0
root.pathname = ''
root.file_list = []

# Set variables for text retrieval
path_var=tk.StringVar()
new_var=tk.StringVar()

print('path: ' + str(os.getcwd()))

#f Create top frame for getting started
frm_top = tk.Frame(
    master=root,
    relief="sunken",
    borderwidth=2,
    background="#99ccff"
)
frm_top.grid(
    row=0,
    column=0,
    ipady=5,
    sticky="nsew"
)
frm_top.rowconfigure(0, weight=1)
frm_top.columnconfigure(0, weight=1)

lbl_start = tk.Label(
    master=frm_top,
    background="#99ccff",
    font=("Arial", 20),
    text="Each pdf file in a selected directory is displayed, along with the \noption to rename it. \
Click <start> to select the directory and let\nthe renaming begin!",
    justify="left"
)
lbl_start.grid(
    row=0, 
    column=0, 
    padx=5,
)

# Create frame for start and quit buttons
frm_top_btns = tk.Frame(
    master=frm_top,
    relief="flat",
    background="#99ccff"
)
frm_top_btns.grid(
    row=1,
    column=0
)
frm_top.rowconfigure(0, weight=1)
frm_top.columnconfigure(0, weight=1)

btn_start = ttk.Button(
    master=frm_top_btns,
    width=5,
    text="Start",
    command=lambda:start()
)
btn_start.focus()
btn_start.grid(
    row=1,
    column=0,
    padx=(5, 10),
    pady=(0, 15),
    sticky='e'
)

btn_top_quit = ttk.Button(
    master=frm_top_btns,
    width=5,
    text="Quit",
    command=lambda:quit()
)
btn_top_quit.grid(
    row=1,
    column=1,
    padx=(10, 5),
    pady=(0, 15),
    sticky='w'
)

# Create bottom frame for viewing and renaming the pdf files  
frm_bottom = tk.Frame(
    master=root,
    background="#99ccff",
    relief="sunken",
    borderwidth=2
)
frm_bottom.rowconfigure(0, weight=1)
frm_bottom.columnconfigure(0, weight=1)

lbl_current=tk.Label(
    master=frm_bottom,
    background="#99ccff",
    font=('Arial', 16),
    text='File name:'
)
lbl_current.grid(
    row=0,
    column=0,
    padx=5,
    pady=(10, 0),
    sticky='nsew'
)

lbl_current_is = tk.Label(
    master=frm_bottom,
    background='#99ccff',
    foreground='#ff0000',
    font=('Arial', 16)
)
lbl_current_is.grid(
    row=1, 
    column=0,
    ipadx=7,
    pady=(2,10)
)

lbl_new = tk.Label(
    master=frm_bottom,
    background="#99ccff",
    text="Change to:",
    font=("Arial", 16)
)
lbl_new.grid(
    row=2,
    column=0,
    padx=5
)

# Create frame for new name entry
frm_new = tk.Frame(
    master=frm_bottom,
    relief='flat',
    background='#99ccff'
)
frm_new.grid(
    row=3,
    column=0,
    ipadx=5,
    ipady=5
)

ent_new=tk.Entry(
    master=frm_new,
    relief="flat",
    textvariable=new_var,
    font=('Arial', 16),
    justify='right',
    width=50
)
ent_new.grid(
    row=0,
    column=0,
    padx=(10,0),
    pady=(2,10),
    sticky='e'
)

lbl_new_ent = tk.Label(
    master=frm_new,
    text='.pdf',
    font=('Arial', 16),
    background='#99ccff'
)
lbl_new_ent.grid(
    row=0,
    column=1,
    pady=(2, 10),
    sticky='w'
)

# Create frame for bottom buttons
frm_bottom_btns=tk.Frame(
    master=frm_bottom,
    relief="flat",
    background="#99ccff"
)
frm_bottom_btns.grid(
    row=4,
    column=0,
    padx=5,
    pady=(5, 10)
)

btn_save = ttk.Button(
    master=frm_bottom_btns,
    width=5,
    text="Save",
    command=lambda:save()
)

btn_next = ttk.Button(
    master=frm_bottom_btns,
    width=5,
    text="Next",
    command=lambda:next()
)

btn_return = ttk.Button(
    master=frm_bottom_btns,
    width=5,
    text="Return",
    command=lambda:retern()
)

btn_save.grid(
    row=0,
    column=0,
    padx=5,
    ipadx=10,
    pady=5,
    sticky="e"
)

btn_next.grid(
    row=0,
    column=1,
    padx=5,
    ipadx=10,
    pady=5,
    sticky="ns"
)

btn_return.grid(
    row=0,
    column=2,
    padx=5,
    ipadx=10,
    pady=5,
    sticky="w"
)

root.mainloop()

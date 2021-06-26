import os.path
import os
import glob
import tkinter as tk
from tkinter import Tk, Toplevel, messagebox
from tkinter import filedialog as fd
from tkinter.constants import END
import tkinter.ttk as ttk
import fitz
from PIL import Image, ImageTk
from fitz.fitz import Widget


# Create flag to tell the next function if it is seeing a request from the back button
def back():
    root.back = True
    next()

# go back to the start window
def retern():
    # Check whether 'entry_new' has changed and if so give option of saving with the new name
    if not (new_var.get() == root.file_name or new_var.get() == ''):
        mb = messagebox.askyesno("PDF Renamer", "You entered a new file name. Do you want to save it?")
        if not mb:
            # Reverse the changes to 'entry_new' and restart to retern
            new_var.set(root.file_name)
            retern()
        else:
            save()
    else:
        # Reset the starting parameters
        root.counter = 0
        root.pathname = ''
        root.file_list = []
        # Destroy existing toplevels to prevent them from accumulating
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
    # Check whether 'entry_new' has changed and if so give option of saving with the new name
    if not (new_var.get() == root.file_name or new_var.get() == ''):
        mb = messagebox.askyesno("PDF Renamer", "You entered a new file name. Do you want to save it?")
        # Reverse the changes to 'entry_new' and restart next
        if not mb:
            new_var.set(root.file_name)
            next()
        else:
            save()
    else:
        # Activate back button 
        btn_back["state"] = "normal"
        # Destroy existing toplevels to prevent them from accumulating.
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        # Increment the counter
        root.counter+=1

        # Check whether this call came from the back function
        if root.back:
            # Reset root.back
            root.back = False
            if root.counter <= 0:
                root.counter == 0
            else:
                # Decrement root.counter by 2, one for the increment above and one to go back
                root.counter -= 2
            # Back button should only be active if root.counter is 1 or higher
            if root.counter > 0:
                # Activate back button 
                btn_back['state'] = 'normal'
            else:
                # Disable the back button
                btn_back['state'] = 'disabled'
        # Check whether the last pdf has been viewed 
        if root.counter >= len(root.file_list):
            messagebox.showinfo('PDF Renamer', 'No more pdf files in the specified directory!')
            retern()
        else:
            # Create file_name (without the pdf extension)
            root.file_name = root.file_list[root.counter][len(root.pathname)+1:len(root.file_list[root.counter])-4]
            # Populate text field of lbl_file_name_is
            lbl_file_is.config(
                #text = '(#' + str(root.counter+1) + '/' + str(root.pdf_count) + ')  ' + \
                text = root.file_name
            )
            
            # # Update file file counter
            # lbl_counter.config(
            #     text='#' + str(root.counter+1) + '/' + str(root.pdf_count)
            # )
            # Populate text field of ent_new
            new_var.set(root.file_name)
            # Hide scroll bar if text doesn't fill ent_new
            print (ent_new.xview())
            if ent_new.xview() == (0.0, 1.0):
                print('len < widthe')
                ent_new_scroll.grid_remove()
            else:
                ent_new_scroll.grid()

            # Create the pdf image (first page)
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
    # Disable the back button
    if btn_back['state'] == 'normal':
        btn_back['state'] = 'disabled'
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
                    column=0
                )
                # Create file_name (without the pdf extension)
                root.file_name = root.file_list[0][len(root.pathname)+1:len(root.file_list[0])-4]
                # Populate text field of lbl_file_is
                lbl_file_is.config(
                    text = root.file_name
                )
                # # Update file file counter
                # lbl_counter.config(
                #     text='#' + str(root.counter+1) + '/' + str(root.pdf_count)
                # )
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
    # name = current name
    name = root.file_list[root.counter][len(root.pathname)+1:len(root.file_list[root.counter])]
    src = root.pathname + '/' + name
    dst = root.pathname + '/' + new_var.get() + '.pdf'
    # Check for dot in new name (no dots - to make sure the .pdf extension is part of the new 
    # name since it is added automatically)
    s = new_var.get()
    if not '.' in s:
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
    else:
        messagebox.showinfo('PDF Renamer', 'Sorry, new name cannot contain a dot. Try again.')
        # Set new entry back to current name (start over)
        new_var.set(name[0:len(name)-4])
        
# Initialize tk
root= tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')
style.configure('Horizontal.TScrollBar', troughcolor='#ff0000')
#root.eval('tk::PlaceWindow . center')
root.title("PDF Renamer")
root.geometry("+%d+%d" % (50, 150))
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.counter = 0
root.pdf_count = 0
root.pathname = ''
root.file_list = []
root.back = False

# Set variables for text retrieval
path_var=tk.StringVar()
new_var=tk.StringVar()

print('path: ' + str(os.getcwd()))

#f Create top frame for getting started
frm_top = tk.Frame(
    master=root,
    relief="groove",
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
    background="#99ccff"
)
frm_top_btns.grid(
    row=1,
    column=0
)

btn_start = ttk.Button(
    master=frm_top_btns,
    width=5,
    text="Start",
    command=lambda:start()
)
#btn_start.focus()
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
########################################################################
# Create bottom frame for viewing and renaming the pdf files  
frm_bottom = tk.Frame(
    master=root,
    background="#99ccff",
    relief='groove',
    borderwidth=2
)
frm_bottom.rowconfigure(0, weight=1)
frm_bottom.columnconfigure(0, weight=1)

lbl_file_name = tk.Label(
    master=frm_bottom,
    background="#99ccff",
    font=('Arial', 16, 'underline'),
    anchor='w',
    width=50,
    text='Current file name:'
)
lbl_file_name.grid(
    row=0,
    column=0,
    padx=8,
    pady=(10, 0),
    sticky='e'
)

lbl_file_is = tk.Label(
    master=frm_bottom,
    background='#99ccff',
    foreground='#ff0000',
    font=('Arial', 16),
    width=50,
    anchor='w'
)
lbl_file_is.grid(
    row=1, 
    column=0,
    padx=8,
    pady=(0,10),
    sticky='e'
)

lbl_new = tk.Label(
    master=frm_bottom,
    background="#99ccff",
    width=50,
    text="Change name to:",
    anchor='w',
    font=('Arial', 16, 'underline')
)
lbl_new.grid(
    row=2,
    column=0,
    padx=8,
    sticky='e'
)

# Create frame to contain ent_new and scroll bar
frm_ent_new = tk.Frame(
    master=frm_bottom,
    background='#99ccff'
)
frm_ent_new.grid(
    row=3,
    column=0,
    padx=8,
    pady=(0,10),
    sticky='e'
)

# Add new file name - ent_new
ent_new=tk.Entry(
    master=frm_ent_new,
    relief="flat",
    borderwidth=0,
    highlightthickness=2,
    highlightbackground='gainsboro',
    bg='gainsboro',
    textvariable=new_var,
    font=('Arial', 16),
    foreground='#ff0000',
    justify='left',
    width=50
)
ent_new.grid(
    row=0,
    column=0,
    #padx=8,
    #sticky='e'
)

# Add scrollbar for ent_new
ent_new_scroll = tk.Scrollbar(
    master=frm_ent_new,
    orient='horizontal',
    command=ent_new.xview,
    troughcolor='gainsboro'
)
ent_new_scroll.grid(
    row=1,
    column=0,
    #padx=8,
    #pady=(0,10)
    sticky='ew'
)
ent_new.config(xscrollcommand=ent_new_scroll.set)

# Create frame for bottom buttons
frm_bottom_btns=tk.Frame(
    master=frm_bottom,
    relief="flat",
    background="#99ccff"
)
frm_bottom_btns.grid(
    row=5,
    column=0,
    columnspan=2,
    padx=8,
    pady=(5, 10)
)

btn_save = ttk.Button(
    master=frm_bottom_btns,
    width=5,
    text="Save",
    command=lambda:save()
)

btn_back = ttk.Button(
    master=frm_bottom_btns,
    width=5,
    text="Back",
    command=lambda:back()
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
    padx=10,
    ipadx=10,
    pady=5,
    sticky="e"
)

btn_back.grid(
    row=0,
    column=1,
    padx=10,
    ipadx=10,
    pady=5,
)

btn_next.grid(
    row=0,
    column=2,
    padx=10,
    ipadx=10,
    pady=5,
)

btn_return.grid(
    row=0,
    column=3,
    padx=10,
    ipadx=10,
    pady=5,
    sticky="w"
)

root.mainloop()

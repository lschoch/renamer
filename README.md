# 📂      PDF_renamer      ⏱️
### A desktop application to quickly view and rename the pdf files in a user-selected directory.
#### Video Demo:
#### GitHub: https://github.com/lschoch/PDF_renamer.git
#### Description:

"PDF_renamer" is a Python script that allows users to iterate through each pdf file in a directory of their choosing. The first page of the file is displayed and this image can be used in deciding whether to rename the file, and what the new name will be, based on the file contents. The GUI is implemented with the Tkinter library and rendering of the pdf images uses the PyMuPDF and Pillow libraries. 

This project consists of three files: the program file is named "PDF_renamer.py". Dependencies are listed in "requirements.txt" and finally there is this "README.md" file.

\
When the program is started, an introductory screen is displayed:

<img src="/images/screen%20shot_1.png" alt="introductory screen">

\
Clicking start takes the user to a file dialog where he or she can select the directory that contains the pdf file(s) of interest. After the directory is selected, the following screen is displayed which allows the user to iterate through each file with the option of renaming:



\
To create "PDF_renamer.py" I had to familiarize myself with three libraries previously unknown to me: Tkinter, Pillow and PyMuPDF. This alone required a considerable investment of time and countless Google searches along the way, a process all too familiar to this novice software developer.

Why a utility for renaming pdf files? Let me explain: I scan numerous documents to maintain a paperless home office. This results in a long queue of pdf files that basically have just a time stamp for a name. Of course, I could go back and rename each file using the functionality provided by the operating system but this would involve the time-consuming process of opening the file to see what it contains before deciding on a name that would be reflective of its contents. With "PDF_renamer" I can rapidly scroll through each file, view the first page and rename it, all in a single step. The image of the first page appears instantaneously along with the input box for entry of a new name. Granted, this is a very narrowly focused task but it is one that is already saving me considerable time and effort, plus I had the expoerience of creating a GUI, something I have wanted to do for years.

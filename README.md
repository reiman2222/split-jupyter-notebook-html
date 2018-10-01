# split-jupyter-notebook-html

Read Me:

This program splits a large jupyter notebook into individual jupyter notebooks and converts them to html
based on first level heading. The first cell is assumed to be the table of contents and is removed.
REQUIRES all fisrt level headings to have a tag of the form: <a id='someID'></a>

Run with: python3 split-notebook.py

The program will ask what notebook you want work on, enter the name of the notebook ff
it is in the same folder as split-notebook.py just enter the name of the 
notebook (rember to include the .ipynb extension), if the notebook is located somwhere else enter the 
absolute path to the notebook instead.

The program expects there to be two folders: topics and html in the same folder as split-notebooks.py.

the split notebooks are written in .ipynb format in the topics folder and
.html format in the html folder.

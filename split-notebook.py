#This program splits a large jupyter notebook into individual jupyter notebooks
#based on first level heading. The first cell is assumed to be the table of contents and is removed.
#REQUIRES all fisrt level headings to have a tag of the form: <a id='someID'></a>

import json
import re
import copy
import os
from lxml import html

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

def getIDFromCellSource(cell):
    if(cell['cell_type'] != 'markdown'):
        return None
    else:
        cellSource = cell['source']
        for line in cellSource:
            if(line != '' and '<a id=\'' in line):
                lineL = re.split('<a id=\'', line)
                lineL = lineL[1].split("'")
                lineID = lineL[0]

                return lineID
        return None

#returns a list of tuples of the form (startCellIndex, endCellIndex, cellId)
def getSubNotebooks(cells):
    i = 0
    startCell = 0
    endCell = 0

    lookingForEnd = False

    outputList = []

    cellID = ''

    while(i < len(cells)):
        cell = cells[i]
        if(isLevel1Header(cell) and not lookingForEnd):
            startCell = i
            lookingForEnd = True

            cellID = getIDFromCellSource(cell)

        elif((isLevel1Header(cell) or ((i + 1)  == len(cells))) and lookingForEnd):
            endCell = i
            i = i - 1
            lookingForEnd = False

            outputList.append((startCell, endCell, cellID))

        i += 1
    return outputList

#returns true if cell has a level 1 header
def isLevel1Header(cell):
    if(cell['cell_type'] != 'markdown'):
        return False

    cellSource = cell['source']
    if(len(cellSource) > 0):
        matches = re.match('^# ', cellSource[0])
        if(matches != None):
            return True
        else:
            return False

    return False

def checkDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def writeSubNotebooks(subNotebooks, js, folderToWriteTo):

    for sn in subNotebooks:
        jsCopy = copy.deepcopy(js)


        start = sn[0]
        end = sn[1]
        fname = sn[2]

        length = len(jsCopy['cells'])

        if(start == 0):
            del jsCopy['cells'][end:]
        else:
            del jsCopy['cells'][end:]
            del jsCopy['cells'][:start]

        checkDir(folderToWriteTo)

        with open(folderToWriteTo + '/' + fname + '.ipynb', 'w+') as outfile:
            json.dump(jsCopy,  outfile)

def formatHTML(body):

    page_html = html.fromstring(body)

    # Remove all style elements
    for style in page_html.xpath('//style[@type="text/css"]'):
        style.getparent().remove(style)

    # link to the style file
    style_custom = html.Element('link', href="/css/notebook.css", rel="stylesheet")
    page_html.xpath('//meta')[0].getparent().append(style_custom)

    # Change custom.css to correct location
    page_html.xpath('//link[@href="custom.css"]')[0].attrib['href'] = "/css/custom.css"

    return html.tostring(page_html, encoding='unicode')

#-----------------------------------#
#               MAIN                #
#-----------------------------------#

def main():
    # notebookName = input('Enter the name of the notebook you would like convert to html:\n')
    notebook_filename = "classification.ipynb"

    with open(notebook_filename,'r') as f:
        js = json.loads(f.read())

    cells = js['cells']

    tableOfContentsCell = cells[0]

    tableOfCSource = tableOfContentsCell['source']

    del cells[0]

    subNotebooks = getSubNotebooks(cells)

    print('\nThe following topics have be identified:')
    for tup in subNotebooks:
        print(tup[2])


    writeSubNotebooks(subNotebooks, js, 'topics')

    print('\nWritting results to folder: html')

    for topic in subNotebooks:
        filename = topic[2]
        notebook_filename = 'topics/' + filename + '.ipynb'

        with open(notebook_filename) as f:
            nb = nbformat.read(f, as_version=4)

        html_exporter = HTMLExporter()
        html_exporter.template_file = 'full'

        (body, resources) = html_exporter.from_notebook_node(nb)

        checkDir('html')

        with open('html/' + filename + '.html', "w+") as nbHTML:
            nbHTML.write(formatHTML(body))

main()

#!\\usr\\bin\\python\\env

import os.path
import os
import xnatutils
import Tkinter
import tkFileDialog
import shutil

root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window

currdir = os.getcwd()
base_path = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select directory where data is saved')
if len(base_path) > 0:
    print "You chose %s" % base_path

# Set unique variables (researcherName, subID, studyID, xnatID, xnatSESS)
#researcherName= raw_input('Reseacher Name (as written in PROJECTS folder): ')

hdd_backup= raw_input('Do you also backup your data to a Hard drive? (y/n): ')

if hdd_backup == 'y':
        root = Tkinter.Tk()
        root.withdraw() #use to hide tkinter window

        currdir = os.getcwd()
        hdd_path = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select backup hard drive')
        if len(hdd_path) > 0:
            print "You chose %s" % hdd_path
    


studyID= raw_input('Study prefix (eg.HUB): ')

subID= raw_input('Subject ID: ').split()

xnatID= raw_input('MBI XNAT project number (eg.MRH001): ')

xnatSESS= raw_input('Session number (eg.EEG01): ')

# Sets xnatutils to never save password
# Keep on always when on shared computer
mbi_xnat = xnatutils.connect(save_netrc=False)


# Sets path. Change if using script on personal computer
#base_path = '/Volumes/RAW_DATA/'  


# Loop over IDs and seacrh for files containing spaces and remove the space
loopText = "LOOPING OVER FILES AND CLEANING FILENAMES FOR: "
dots = "..."

for ID in subID:
    loopPrint = '{}{}{}'.format(loopText, ID, dots)
    print(loopPrint)

    path = os.path.join(base_path, studyID, ID)

    print(path)

    os.chdir(path)

    filenames = os.listdir('.')

    for f in os.listdir("."):

        r = f.replace(" ", "")

        if(r != f):

            os.rename(f, r)

    
    
    for f in filenames:

        if f.startswith(ID):

            os.rename(f, studyID + f)


    source = os.listdir(path)

    temp = 'temp'

    path_temp = os.path.join(path, temp)

    if not os.path.isdir(path_temp):

        os.makedirs(path_temp)

    for files in source:

        if files.startswith("."):

            shutil.move(files, path_temp)



    if hdd_backup == 'y':

        hdd_full_path = os.path.join(hdd_path, studyID, ID)

        if not os.path.isdir(hdd_full_path):

            os.makedirs(hdd_full_path)
   
    if hdd_backup == 'y':

        for files in source:

            shutil.copy2(files, hdd_full_path)


# Loop over IDs and if file begins with ID, place prefix (studyID) at the start


print("FILE NAMES CLEANED....")

if hdd_backup == 'y':
    print("Data being backed up to Hard drive...")


print("BEGINNING UPLOAD...")


# Loop over IDs and upload to xnat

for ID in subID:

    path = os.path.join(base_path, studyID, ID)

    print(path)

    fullsessID = '{}_{}{}_{}'.format(xnatID, studyID, ID, xnatSESS)

    all_fnames = os.listdir(path)

    print(all_fnames)

    all_fname_bases = set(os.path.splitext(f)[0] for f in all_fnames)



    for base in all_fname_bases:

        print(base)

        fnames = [os.path.join(path, f)

                  for f in all_fnames if f.startswith(base)]

        xnatutils.put(

            fullsessID,

            base,

            *fnames,

            create_session=True,

            resource_name='CURRY',

            connection=mbi_xnat)


print("FINISHED")
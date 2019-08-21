#!\\usr\\bin\\python\\env
import os.path
import os
import sys
from xnatutils import put as xnat_put
from xnatutils.base import connect as xnat_connect
import tkinter.filedialog
from tkinter import messagebox
import shutil
from xnat.exceptions import XNATResponseError


def eeg_upload():
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window

    def show_error_and_quit(message):
        messagebox.showinfo("Upload Error", message)
        sys.exit()

    currdir = os.getcwd()
    base_path = tkinter.filedialog.askdirectory(
        parent=root, initialdir=currdir,
        title='Please select directory where data is saved')

    if len(base_path) > 0:
        print("You chose %s" % base_path)

    # Set unique variables (researcherName, subID, studyID, xnatID, xnatSESS)
    # researcherName= input('Reseacher Name (as written in PROJECTS folder): ')

    hdd_backup = input('Do you also backup your data to a Hard drive? (y/n): ')

    if hdd_backup == 'y':
        root = tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        currdir = os.getcwd()
        hdd_path = tkinter.filedialog.askdirectory(
            parent=root, initialdir=currdir,
            title='Please select backup hard drive')
        if len(hdd_path) > 0:
            print("You chose %s" % hdd_path)

    studyID = input('Study prefix (eg.HUB): ')

    dataType = input('Data Type (eg.Cognitive_data or TMS_EEG_data): ')

    subID = input('Subject ID: ').split()

    xnatID = input('MBI XNAT project number (eg.MRH001): ')

    xnatSESS = input('Session number (eg.EEG01): ')

    # Sets xnatutils to never save password
    # Keep on always when on shared computer
    mbi_xnat = xnat_connect(use_netrc=False)

    # Sets path. Change if using script on personal computer
    # base_path = '/Volumes/RAW_DATA/'

    # Loop over IDs and seacrh for files containing spaces and remove the space
    loopText = "LOOPING OVER FILES AND CLEANING FILENAMES FOR: "
    dots = "..."

    for ID in subID:
        loopPrint = '{}{}{}'.format(loopText, ID, dots)
        print(loopPrint)

        path = os.path.join(base_path, studyID, dataType, ID)

        print(path)

        try:
            os.chdir(path)
        except Exception:
            show_error_and_quit(
                ("You have entered the wrong study ID ('{}'), datatype ('{}') "
                 "or ID ('{}') or the directory doesn't exist")
                .format(studyID, dataType, ID))

        filenames = os.listdir('.')

        for f in os.listdir("."):

            r = f.replace(" ", "")

            if(r != f):

                os.rename(f, r)

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

            os.makedirs(hdd_full_path, exist_ok=True)

            for files in source:

                shutil.copy2(files, hdd_full_path)

    # Loop over IDs and if file begins with ID, place prefix (studyID) at the
    # start

    print("FILE NAMES CLEANED....")

    if hdd_backup == 'y':
        print("Data being backed up to Hard drive...")

    print("BEGINNING UPLOAD...")

    # Loop over IDs and upload to xnat

    try:

        for ID in subID:

            path = os.path.join(base_path, studyID, dataType, ID)

            print(path)

            fullsessID = '{}_{}{}_{}'.format(xnatID, studyID, ID, xnatSESS)

            all_fnames = os.listdir(path)

            print(all_fnames)

            all_fname_bases = set(os.path.splitext(f)[0] for f in all_fnames)

            for base in all_fname_bases:

                print(base)

                fnames = [
                    os.path.join(path, f)
                    for f in all_fnames if os.path.splitext(f)[0] == base]

                scan_name = '_'.join(base.split('_')[1:])

                if not scan_name:
                    scan_name = base

                try:
                    xnat_put(

                        fullsessID,

                        scan_name,

                        *fnames,

                        create_session=True,

                        resource_name='CURRY',

                        connection=mbi_xnat)
                except XNATResponseError as e:
                    if '(status 409)' in str(e):
                        print("'{}' scan already exists for '{}' session, "
                              "skipping".format(base, fullsessID))
                    else:
                        raise

    except Exception as e:
        print(e)
        show_error_and_quit(
            "You have entered an incorrect XNAT ID ('{}') or XNAT session "
            "('{}'), the XNAT project ID doesn't exist or there is already "
            "data uploaded with that ID".format(xnatID, xnatSESS))

    print("FINISHED")


if __name__ == '__main__':
    eeg_upload()

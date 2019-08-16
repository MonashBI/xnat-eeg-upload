#!\\usr\\bin\\python\\env

import os.path
import os
import xnatutils

# Set unique variables (researcherName, subID, studyID, xnatID, xnatSESS)
researcherName= raw_input('Reseacher Name (as written in PROJECTS folder): ')

subID= [raw_input('Subject ID: ')]

studyID= raw_input('Study prefix (eg.HUB): ')

xnatID= raw_input('MBI XNAT project number (eg.MRH001): ')

xnatSESS= raw_input('Session number (eg.EEG01): ')

# Sets xnatutils to never save password
# Keep on always when on shared computer
mbi_xnat = xnatutils.connect(save_netrc=False)


# Sets path. Change if using script on personal computer
base_path = 'F:\Users\EEG_ACQ\Desktop\All Data\PROJECTS'


# Loop over IDs and seacrh for files containing spaces and remove the space
loopText = "LOOPING OVER FILES AND CLEANING FILENAMES FOR: "
dots = "..."

for ID in subID:
    loopPrint = '{}{}{}'.format(loopText, ID, dots)
    print(loopPrint)

for ID in subID:

    path = os.path.join(base_path, researcherName, studyID, ID)

    os.chdir(path)

    for f in os.listdir("."):

        r = f.replace(" ", "")

        if(r != f):

            os.rename(f, r)

# Loop over IDs and if file begins with ID, place prefix (studyID) at the start

for ID in subID:
    
    filenames = os.listdir('.')
    
    for f in filenames:
        if f.startswith(ID):
            os.rename(f, studyID + f) 


print("FILE NAMES CLEANED....")

print("BEGINNING UPLOAD...")


# Loop over IDs and upload to xnat

for ID in subID:

    path = os.path.join(base_path, researcherName, studyID, ID)

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
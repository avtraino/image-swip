import os, shutil
from datetime import datetime
import exifread

fmt = "%Y-%m-%d_%H.%M.%S"
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/Data"
inbox = data_path + '/Inbox/'
archive = data_path + '/Archive/'
problem = data_path + '/Problems/'


# moves files from Inbox to Archive so they cant be modified while processing
def protect(title):
    inc_event  = inbox + title + '/'
    archive_event = archive + title
    if not os.path.exists(archive_event):
        os.mkdir(archive_event)
    folders = os.listdir(inc_event)
    for d in folders:
        shutil.move(inc_event+d, archive_event)


# remove directory if empty
def rmdirs(path):
    leftovers = [f for f in os.listdir(path) if not f.startswith('.')]
    if not leftovers:
        shutil.rmtree(path)
    else:
        print(path, "is not empty")


# gets EXIF date from image and returns as datetime object 
def get_stamp(photo):
    with open(photo, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        tag = tags['EXIF DateTimeOriginal']
        strDT = str(tag)
    return datetime.strptime(strDT, "%Y:%m:%d %H:%M:%S")


def process(title):
    inc_event = inbox + title + '/'
    archive_event = archive + title + '/'

    if not os.path.exists(archive_event):
        os.mkdir(archive_event)

    for root, subdir, files in os.walk(archive_event):
        for photo in files:
            if photo.lower().endswith(('.jpg', 'jpeg')):
                oldfile = os.path.join(root,photo)
                
                suffix = 'b'
                try:
                    dt = get_stamp(oldfile)
                    stamp = dt.strftime(fmt)
                    newname = stamp + '__' + title + '.jpg'
                    newfile = os.path.join(root, newname)

                    # if there are identical files, append a suffix
                    while os.path.exists(newfile):
                        newname = stamp + '_' + suffix + '__' + title + '.jpg'
                        newfile = os.path.join(root, newname)
                        suffix = chr(ord(suffix)+1)
                    os.rename(oldfile, newfile)
                    print(newfile)

                    
                except Exception as e:
                    if not os.path.exists(problem):
                        os.mkdir(problem)
                    shutil.move(oldfile, problem)
                    print("Error: " + str(photo))
                    print("  ^--Exception: " + str(e))
            # if file is not a jpeg
            else:
                if not os.path.exists(problem):
                    os.mkdir(problem)
                shutil.move(os.path.join(root,photo) , os.path.join(problem, photo))


    rmdirs(inc_event)


def main():
    folders = [data_path, inbox, archive]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    incoming = os.listdir(inbox)
    for event in incoming:
        path = inbox + event
        if os.path.isdir(path):
            print("\n################################",event,"################################")
            protect(event)
            process(event)
    

def debug():
    folders = [data_path, inbox, archive]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    incoming = os.listdir(inbox)
    for event in incoming:
        path = inbox + event
        if os.path.isdir(path):
            print("\n################################",event,"################################")
            for root, subdirs, files in os.walk(path):
                print(root)
            # photos = [ f for f in photos if f.lower().endswith(('.jpg', 'png')) ]
            

if __name__ == "__main__":
    main()
    # debug()
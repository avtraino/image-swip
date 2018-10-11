import os, shutil
from datetime import datetime
import exifread

fmt = "%Y-%m-%d_%H.%M.%S"
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/Data"
inbox = data_path + '/Inbox/'
working = data_path + '/Working/'
processed = data_path + '/Processed/'


# moves files from Inbox to Working so they cant be modified while processing
def protect(title):
    inc_event  = inbox + title + '/'
    work_event = working + title
    if not os.path.exists(work_event):
        os.mkdir(work_event)
    folders = os.listdir(inc_event)
    for d in folders:
        shutil.move(inc_event+d, work_event)


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
    work_event = working + title + '/'
    processed_event = processed + title + '/'

    if not os.path.exists(processed_event):
        os.mkdir(processed_event)

    photos = os.listdir(work_event)
    photos = [ f for f in photos if f.lower().endswith(('.jpg', 'png')) ]
    
    for photo in photos:
        original = work_event + '/' + photo
        suffix = 'b'
        try:
            dt = get_stamp(original)
            stamp = dt.strftime(fmt)
            nombre = stamp + '__' + title
            newname = processed_event + nombre + '.jpg'

            # if there are identical files, append a suffix
            while os.path.exists(newname):
                newname = stamp + '_' + suffix + '__' + title
                newname = processed_event + newname + '.jpg'
                suffix = chr(ord(suffix)+1)
                
            shutil.move(original, newname)
            print(newname)
        except Exception as e:
            print("Error: " + str(photo))
            print("  ^--Exception: " + str(e))

    rmdirs(work_event)
    rmdirs(inc_event)


def main():
    folders = [data_path, inbox, working, processed]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    incoming = os.listdir(inbox)
    for event in incoming:
        path = inbox + event
        if os.path.isdir(path):
            print("\n################",event,"################")
            protect(event)
            process(event)
    

def debug():
    pass
                


if __name__ == "__main__":
    main()
    # debug()
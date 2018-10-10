import os, shutil
from datetime import datetime
import exifread

fmt = "%Y-%m-%d_%H.%M.%S"
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/Data"
inbox = data_path + '/Inbox/'
working = data_path + '/Working/'
processed = data_path + '/Processed/'
outbox = data_path + '/Outbox/'


# moves files from Inbox to Working so they cant be modified while processing
def protect(title):
    inc_event  = inbox + title + '/'
    work_event = working + title
    if not os.path.exists(work_event):
        os.mkdir(work_event)
    folders = os.listdir(inc_event)
    for d in folders:
        shutil.move(inc_event+d, work_event)


# moves files from Working to Processed when finished processing
def finished(title, photo):
    work_event = working + title
    proc_event = processed + title
    work_f = work_event + '/' + photo
    proc_f = proc_event + '/' + photo
    if not os.path.exists(proc_event):
        os.mkdir(proc_event)
    shutil.move(work_f, proc_f)


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
    outbox_event = outbox + title + '/'

    if not os.path.exists(outbox_event):
        os.mkdir(outbox_event)

    photos = os.listdir(work_event)
    photos = [ f for f in photos if f.lower().endswith(('.jpg', 'png')) ]
    
    for photo in photos:
        original = work_event + '/' + photo
        suffix = 'b'
        try:
            dt = get_stamp(original)
            stamp = dt.strftime(fmt)
            name = stamp + '__' + title
            duplicate = outbox_event + name + '.jpg'
            while os.path.exists(duplicate):
                newname = stamp + '_' + suffix + '__' + title
                duplicate = outbox_event + newname + '.jpg'
                suffix = chr(ord(suffix)+1)
            shutil.copy2(original, duplicate)
            print(duplicate)
            finished(title, photo)
        except Exception as e:
            print("Error: " + str(photo))
            print("  ^--Exception: " + str(e))

    rmdirs(work_event)
    rmdirs(inc_event)


def main():
    folders = [data_path, inbox, working, processed, outbox]
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
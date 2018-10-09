import os, subprocess, shutil
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
    inc_dir  = inbox + title + '/'
    work_dir = working + title
    if not os.path.exists(work_dir):
        subprocess.call(['mkdir', work_dir])
    folders = os.listdir(inc_dir)
    for f in folders:
        shutil.move(inc_dir+f, work_dir)


# moves files from Working to Processed when finished processing
def finished(title, photo):
    work_dir = working + title
    proc_dir = processed + title
    work_f = work_dir + '/' + photo
    proc_f = proc_dir + '/' + photo
    if not os.path.exists(proc_dir):
        subprocess.call(['mkdir', proc_dir])
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
    inc_dir = inbox + title + '/'
    work_dir = working + title + '/'
    outbox_dir = outbox + title + '/'

    if not os.path.exists(outbox_dir):
        subprocess.call(['mkdir', outbox_dir])

    photos = os.listdir(work_dir)
    photos = [ f for f in photos if f.lower().endswith(('.jpg', 'png')) ]
    
    for photo in photos:
        original = work_dir + '/' + photo
        suffix = 'b'
        try:
            dt = get_stamp(original)
            stamp = dt.strftime(fmt)
            name = stamp + '__' + title
            duplicate = outbox_dir + name + '.jpg'
            while os.path.exists(duplicate):
                newname = stamp + '_' + suffix + '__' + title
                duplicate = outbox_dir + newname + '.jpg'
                suffix = chr(ord(suffix)+1)
            shutil.copy2(original, duplicate)
            print(duplicate)
            finished(title, photo)
        except Exception as e:
            print("Error: " + str(photo))
            print("  ^--Exception: " + str(e))

    rmdirs(work_dir)
    rmdirs(inc_dir)


def main():
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
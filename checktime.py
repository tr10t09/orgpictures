import os
import re
from PIL import Image
from datetime import datetime, timedelta


def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

images = r"/mnt/c/Users/ethoren/OneDrive - Ericsson/Pictures/TimestampTest/BilderDuplicates.txt"
imagepath = r"/mnt/c/Users/ethoren/OneDrive - Ericsson/Pictures/TimestampTest/"
pictures  = [os.path.join(imagepath, f) for f in os.listdir(imagepath) if os.path.isfile(os.path.join(imagepath, f)) and is_img(os.path.join(imagepath, f))]
alltime = {}


'''
tformat = re.compile(r'(\d{8})')
cnt = 0
with open(images) as fp:
    Lines = fp.readlines()
    for line in Lines[1:2]:
        line = line.rstrip("\n")
        matching = tformat.search(line)
        if matching is not None:
            time = datetime.strptime(matching.group(1), '%Y%m%d')
            cnt += 1
            print(f"FILE: {cnt} {line} DATE:{time}")
            
'''

#x{file:{filetime:x, mtime:y, exittime:z}}
def preprocess_exif(data):
    data = data.strip()
    data = data.strip('\x00')
    return data


def timecollection(imgfiles):
    tformat = re.compile(r'(\d{8})')

    for fname in imgfiles:

        # get time from filename if exists
        matching = tformat.search(fname)
        try:
            ftime = datetime.strptime(matching.group(1), '%Y%m%d')
            #print(ftime.strftime("%Y-%m"))
        except:
            ftime = None

        # get modification time
        mtime = datetime.fromtimestamp(os.path.getmtime(fname)).strftime('%Y:%m:%d %H:%M:%S')
        mtime = datetime.strptime(mtime, '%Y:%m:%d %H:%M:%S')
        #print(mtime.year )

        # get image time data
        with Image.open(fname) as img:
            exif = img._getexif() 
        
        try:
            exifctime = datetime.strptime(preprocess_exif(exif[306]), '%Y:%m:%d %H:%M:%S')
        
        except:
            #print(f"FILE: {fname} mtime:{mtime} has no exif data!")
            exifctime = None
        
        alltime[fname] = {'ftime': ftime, 'mtime': mtime, 'exiftime': exifctime}
        
    return alltime

    
#timecollection(pictures)
print(timecollection(pictures).items())

                
    
import os
import imagehash
from PIL import Image
from datetime import datetime, timedelta

class Picture():
    n_images = 0

    def __init__(self, fname):
        self.fname = fname
        self.psize = self.get_size()
        self.hash = self.get_hash()
        self.mtime = self.get_mtime()
        self.ptaken = self.get_ptaken()

        Picture.n_images +=1
    
    # class method for counting the number of instances -> pictures
    @classmethod
    def counter(cls):
        return cls.n_images
    
    def get_mtime(self):
        return datetime.fromtimestamp(os.path.getmtime(self.fname)).strftime('%Y:%m:%d %H:%M:%S')
    
    def preprocess_exif(self, data):
        data = data.strip()
        data = data.strip('\x00')
        return data
    
    def get_ptaken(self):
        with Image.open(os.path.join(self.fname)) as img:
            exif = img._getexif() 
            
        ts = self.preprocess_exif(exif[306])
        date = ts.split(' ')[0]
        
        return datetime.strptime(date, '%Y:%m:%d').strftime('%Y:%m:%d %H:%M:%S')

    def get_hash(self):
        return imagehash.average_hash(Image.open(self.fname))
    
    def get_size(self):
        st = os.stat(self.fname)
        return st.st_size

    def __str__(self):
        return '{};{};{};{};{}'.format(self.fname, self.hash, self.mtime, self.ptaken, self.psize)


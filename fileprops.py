import os
import hashlib
from datetime import datetime, timedelta

class FileProps():
    n_images = 0 

    def __init__(self, fname):
        self.fname = fname
        self.fsize = self.get_size()
        self.fmtime = self.get_mtime()
        self.hashval = self.get_hashvalue()
        
        FileProps.n_images +=1
    
    # class method for counting the number of instances -> pictures
    @classmethod
    def counter(cls):
        return cls.n_images

    
    def get_size(self):
        st = os.stat(self.fname)
        return st.st_size
    
    def get_mtime(self):
        return datetime.fromtimestamp(os.path.getmtime(self.fname)).strftime('%Y:%m:%d %H:%M:%S')
    
    def get_hashvalue(self):
        with open(self.fname, 'rb') as f:
            data = f.read()
            md5hash = hashlib.md5(data).hexdigest()
        
        return md5hash
    
    def __str__(self):
        return '{};{};{};{}'.format(self.fname, self.hashval, self.fsize, self.fmtime)
    

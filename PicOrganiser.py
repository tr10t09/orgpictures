import os
from PIL import Image
from datetime import datetime, timedelta
import imagehash
import pandas as pd

def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

class Picture():
    def __init__(self, fname):
        self.fname = fname
        self.psize = self.get_size()
        self.hash = self.get_hash()
        self.mtime = self.get_mtime()
        self.ptaken = self.get_ptaken()
    
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

class OrgImages():

    def __init__(self, folder):
        self.basefolder = folder
        self.pictures = []
        self.imgfolder = [x[0] for x in os.walk(self.basefolder) if "processed" not in x[0]]
    
    def createimagelist(self, props='n'):
        for folder in self.imgfolder[1:4]:
            fnames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and is_img(os.path.join(folder, f))]
            for fname in fnames:
                if props == 'y':
                    self.pictures.append(Picture(os.path.join(folder, fname)))
                else:
                    self.pictures.append(os.path.join(folder, fname))
        print("{} Pictures imported".format(len(self.pictures)))

        lststore = self.basefolder + ".tmp/"
        create_folder(lststore)
        tmpfile = lststore + "imagelist_date.txt"

        with open(tmpfile, 'w') as f:
            for img in self.pictures:
                f.write(str(img) + '\n')
      
        return self.pictures
    
    def getduplicates(self):
        img = {}

        for p in self.pictures:
            img[p.fname] = str(p.hash)
            
        df = pd.DataFrame(list(img.items()),columns = ['image','hash'])
        df['path'] = df['image']
        grouped = df.groupby(by="hash").agg({"image":"size", "path":list}).reset_index()
        #pd.set_option('display.max_colwidth', None)
        #pd.set_option('display.max_rows', None)
        #identical_clusters = grouped[grouped["image"] >= 2]
        identical_clusters = grouped[grouped["image"] >= 2]
        #sorted = grouped.sort_values("image", ascending=False)
        #sorted.reset_index(inplace=True)
        #identical_clusters = sorted[sorted["image"] >= 2]
        #for i in identical_clusters['path'][26]
       
        print(identical_clusters['path'][26])

        


folder = r"/mnt/c/Users/ethoren/Pictures/_temp/"
pics = OrgImages(folder)
pics.createimagelist()
#pics.getduplicates()
    
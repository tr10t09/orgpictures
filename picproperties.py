
import os
from PIL import Image
from datetime import datetime, timedelta
import imagehash
import pandas as pd


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
        return '{} {} {} {} {}'.format(self.fname, self.hash, self.mtime, self.ptaken, self.psize)
    

def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")


class OrgPictures():
    def __init__(self, folder):
        self.folder = folder
        self.pictures = []
        self.imghash = {}
        self.df_imghash = {}

    
    def create_piclist(self):
        dirs = [x[0] for x in os.walk(self.folder) if "processed" not in x[0]]

        for subfolder in dirs:

            #filenames = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f)) and is_img(os.path.join(subfolder, f))]
            filenames = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]

            for fname in filenames:
                srcname = os.path.join(subfolder, fname)
                self.pictures.append(Picture(srcname))
        
        print("... scanning done!")
        
        return self.pictures
    '''
    def get_duplicates(self):

        for dup in self.pictures:
            p = self.imghash.get(dup.hash, [])
            p.append(dup.fname)
            self.imghash[dup.hash] = p

            self.df_imghash[dup.fname] = str(dup.hash)
            
        df = pd.DataFrame(list(self.df_imghash.items()),columns = ['image','hash'])
        
        df['path'] = df['image']
        
        grouped = df.groupby(by="hash").agg({"image":"size", "path":list}).reset_index()
        pd.set_option('display.max_colwidth', None)

        #https://stackoverflow.com/questions/13207697/how-to-remove-square-brackets-from-list-in-python
        #LIST = [1, "foo", 3.5, { "hello": "bye" }]
        #print( ", ".join( repr(e) for e in LIST ) )
        #print(grouped['path'].to_string(index=False))
        for index, row in grouped.iterrows():
            print(", ".join(row['path']))
        
        
        #df_hem = pd.DataFrame(list(df_hashes.items()),columns = ['image','hash'])

        #df['path'] = df.apply(lambda path: self.ffolderimg + path.image, axis = 1)
        #df['path'] = self.ffolderimg + '/' + df['image']

    '''
 
#img = Picture(r"/home/trendel/Bilder/processed_img/DSC_0051_1.jpg")
#img = Picture(r"/mnt/c/Users/ethoren/Pictures/_temp/01_Bilder_A5_26102018/Camera/20180211_120211.jpg")
folder = r"/mnt/c/Users/ethoren/Pictures/_temp/"
picLst = OrgPictures(folder)
print(picLst.create_piclist())
 



#print(img)
#picDir = r"/mnt/c/Users/ethoren/Pictures/_temp/_DUPLICATE"
#picDir = r"/mnt/c/Users/ethoren/Pictures/_temp/"

#images = OrgPictures(picDir)
#imagelist = images.create_piclist()
#print(imagelist)
#images.get_duplicates()




#handler = PictureHandler(picDir)
#print(handler.get_pictures())





'''
class OrgPhotos():
    def __init__(self, folder):
        self.folder = folder
        self.photos = []

    def find_duplicates(self): # photos is an object with all picture properties
        # create list of sub folders
        # go through folders and create list of photo objects
        # compare hashes and create dict
'''
    

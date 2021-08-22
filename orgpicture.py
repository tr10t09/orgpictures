import os
from PIL import Image
from datetime import datetime, timedelta

#picDir = r"/mnt/c/Users/ethoren/Pictures/_temp/"
#lsImg = [f for f in os.listdir(picDir + "processed") if os.path.isfile(os.path.join(picDir + "processed", f)) and is_img(os.path.join(picDir + "processed", f))]           

imagesDir = r"/mnt/c/Users/ethoren/Pictures/_temp/processed" 
sortedDir = r"/mnt/c/Users/ethoren/Pictures/_temp/sorted"


def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def create_sorted(fsorted):
    if not os.path.exists(fsorted):
        os.makedirs(fsorted)


class PicOrg():
    
    def __init__(self, imagepath):
        self.images = [f for f in os.listdir(imagepath) if os.path.isfile(os.path.join(imagepath, f)) and is_img(os.path.join(imagepath, f))]
        self.dirname = imagepath
        
    def preprocess_exif(self,data):
        data = data.strip()
        data = data.strip('\x00')
        
        return data
    
    def sort_by_year(self):
        for fname in self.images:
            
            # ONLY FILES are CONSIDERED, NO VIDEOS!!!!!!
            
            with Image.open(os.path.join(self.dirname,fname)) as img:
                exif = img._getexif() 
            
            ts = self.preprocess_exif(exif[306])
            
            date = ts.split(' ')[0]
            time = ts.split(' ')[1]
            year = datetime.strptime(date, '%Y:%m:%d').strftime('%Y')
            yearm = datetime.strptime(date, '%Y:%m:%d').strftime('%Y_%m')
            
            #print(f"FILE:{fname}, TS: {ts}, {date}, {year}")
            
            if not os.path.exists(os.path.join(sortedDir, year)):
                os.makedirs(os.path.join(sortedDir, year))
                
            shutil.copy2(os.path.join(self.dirname,fname),os.path.join(sortedDir, year))
    
    def chkctmtdeviation(self):
        
        i = 0
        
        for fname in self.images:
                        
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(self.dirname,fname))).strftime('%Y:%m:%d %H:%M:%S')
            mtime = datetime.strptime(mtime, '%Y:%m:%d %H:%M:%S')
            
            with Image.open(os.path.join(self.dirname,fname)) as img:
                exif = img._getexif() 
            
            exifctime = datetime.strptime(self.preprocess_exif(exif[306]), '%Y:%m:%d %H:%M:%S')
            
            #print(type(mtime), type(exifctime))
                        
            if (mtime - exifctime) > timedelta(hours=2):
                delta = mtime - exifctime
                print(f"time deviation: {fname:15s} mtime {mtime}  exif {exifctime}  delta {delta}")
                i += 1
            
                
        print(f"devation for {i} files")
    
   
            
        

            
            
            


    
orderImg = PicOrg(imagesDir)    

#orderImg.sort_by_year()
orderImg.chkctmtdeviation()

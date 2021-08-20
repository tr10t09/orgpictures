import os
import shutil
import imagehash
from PIL import Image

picDir = r"/mnt/c/Users/ethoren/Pictures/_temp/"

def FileMover(imgDir):
    # create list of possible directories 
    dirs = [x[0] for x in os.walk(imgDir) if "processed" not in x[0]]
    
    # create processing folder is not there yet
    imgDirpro = os.path.join(imgDir, "processed")
    
    if not os.path.exists(imgDirpro):
        os.makedirs(imgDirpro)
    
    # loop through all floders
    for folder in dirs:
        
        filenames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        
        # file coutners for validation purposes
        fcnt = 0
        ccnt = 0
        rcnt = 0
        
        # loop through file in the folders
        for fname in filenames:
            fcnt += 1
            #f = filename.lower()
            sname = os.path.join(folder, fname)
            file = os.path.basename(sname)
            dname = os.path.join(imgDirpro, file)
            
            # check if file (or same filename) is already in processed folder
            if not os.path.isfile(dname):
                shutil.copy2(sname, imgDirpro)
                ccnt +=1
                continue
            else:
                i = 1
                base, extension = os.path.splitext(fname)
                dname_new = os.path.join(imgDirpro, base + "_" + str(i) + extension)
                
                while os.path.isfile(dname_new):
                    i += 1
                    dname_new = os.path.join(imgDirpro, base + "_" + str(i) + extension)
                shutil.copy2(sname, dname_new) 
                rcnt += 1
        print(f"{fcnt} files in {folder}, {ccnt} copied, {rcnt} renamed")
    
    #return [f for f in os.listdir(imgDirpro) if os.path.isfile(os.path.join(imgDirpro, f))]
                  
def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")
        

FileMover(picDir)


# make sure that it continues even if mp4 is processed


def checkDuplicates(ListofImages):
    hashes = {}
    
    for img in ListofImages[:]:

        picture = os.path.join(picDir + "processed", img)

        hash = imagehash.average_hash(Image.open(picture))

        #if avghash in hashes:
        #    duplicates.append(img)
        #else:
        #    hashes[avghash] = img


        #print(f"Picture: {img} and hashval {hash}")

        p = hashes.get(hash, [])
        p.append(img)
        hashes[hash] = p


    dst_path = os.path.join(picDir, "DUPL")
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)


    for (h, duplicte) in hashes.items():
        if len(duplicte) > 1:
            for item in duplicte:
                # build dst file first and check if it there already from previous run

                dst_fname = str(h) + '_' + os.path.basename(item)
                dst_initfname = os.path.join(dst_path, os.path.basename(item))

                #print(dst_initfname)

                if not os.path.isfile(os.path.join(dst_path, dst_fname)):
                    shutil.copy2(os.path.join(picDir + "processed", item), dst_path)
                    os.rename(dst_initfname, os.path.join(dst_path, dst_fname))
                else:
                    print(f" File {dst_fname} exists, continue with next")


lsImg = [f for f in os.listdir(picDir + "processed") if os.path.isfile(os.path.join(picDir + "processed", f)) and is_img(os.path.join(picDir + "processed", f))]           

#checkDuplicates(lsImg)


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

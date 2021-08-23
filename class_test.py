import os
#import sys
import argparse
import shutil
import imagehash
from PIL import Image


#imgpath = r"/mnt/c/Users/ethoren/Pictures/_temp/"


def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def is_vid(fname):
    f = fname.lower()
    return f.endswith("mp4") or f.endswith("3gp")

def chkprocess(folder, ftype):
    fldprocess = os.path.join(folder, "processed_" + ftype)
    
    if not os.path.exists(fldprocess):
        os.makedirs(fldprocess)

    print(f"[INFO] {fldprocess} existence checked!")
    
    return fldprocess 

def chkduplicate(folder):
    fldprocess = os.path.join(folder, "_DUPLICATE")
    
    if not os.path.exists(fldprocess):
        os.makedirs(fldprocess)

    print(f"[INFO] {fldprocess} existence checked!")
    
    return fldprocess 



class organiser():
    
    def __init__(self, imagepath):
        self.images = [f for f in os.listdir(imagepath) \
            if os.path.isfile(os.path.join(imagepath, f)) \
                and is_img(os.path.join(imagepath, f))]
        self.videos = [f for f in os.listdir(imagepath) \
            if os.path.isfile(os.path.join(imagepath, f)) \
                and is_video(os.path.join(imagepath, f))]        
        self.dirname = imagepath
        self.subdirs = [x[0] for x in os.walk(self.dirname) if "processed" not in x[0]]
        self.ffolderimg = chkprocess(self.dirname, "img")
        self.ffoldervid = chkprocess(self.dirname, "vid")
        self.ffolderdup = chkduplicate(self.dirname)

        #for x in os.walk(self.dirname):
        #    if "processed" not in x[0]:
        #        print(x[0])

           


    def mover (self, ftype):
        
        #print(self.subdirs[2])

        fcnt = 0
        ccnt = 0 
        rcnt = 0
        
        for fld in self.subdirs:
            
            if ftype == "img":
                filenames = [f for f in os.listdir(fld) if os.path.isfile(os.path.join(fld, f)) \
                                                            and is_img(os.path.join(fld, f))]
            elif ftype == "vid":
                filenames = [f for f in os.listdir(fld) if os.path.isfile(os.path.join(fld, f)) \
                                                            and is_vid(os.path.join(fld, f))]
            else:
                print("[WARN] It is not an image or video!")

        
            fcnt = 0
            ccnt = 0 
            rcnt = 0
                        
            for fname in filenames:
                fcnt += 1
                srcname = os.path.join(fld, fname) 
                fbasename = os.path.basename(srcname)
                
                dstname = os.path.join(self.ffolderimg, fbasename) if ftype == "img" else os.path.join(self.ffoldervid, fbasename) 

                #print(f"{srcname} {fbasename} {dstname}")

                # check if file (or same filename) is already in processed folder
                if not os.path.isfile(dstname):
                    if ftype == "img":
                        shutil.copy2(srcname, self.ffolderimg)
                        ccnt += 1
                    else:
                        shutil.copy2(srcname, self.ffoldervid)
                        ccnt += 1
                    
                    #continue
                    #is continue requires. if IF matches contiune with next in for loop

                else:
                    i = 1
                    base, extension = os.path.splitext(fname)
                    dstname_new = os.path.join(self.ffolderimg, base + "_" + str(i) + extension) if ftype == "img" else os.path.join(self.ffoldervid, base + "_" + str(i) + extension)
                    while os.path.isfile(dstname_new):
                        i += 1
                        dstname_new = os.path.join(self.ffolderimg, base + "_" + str(i) + extension) if ftype == "img" else os.path.join(self.ffoldervid, base + "_" + str(i) + extension)
                    rcnt += 1
                    shutil.copy2(srcname, dstname_new) 

            print(f"[INFO] {fcnt:4d} files in {fld}, {ccnt} copied, {rcnt} renamed")

        
    def duplicator(self):

        lstfiles = [f for f in os.listdir(self.ffolderimg) if os.path.isfile(os.path.join(self.ffolderimg, f))]

        hashes = {}

        for img in lstfiles[:]:

            picture = os.path.join(self.ffolderimg, img)

            hash = imagehash.average_hash(Image.open(picture))

            #if avghash in hashes:
            #    duplicates.append(img)
            #else:
            #    hashes[avghash] = img


            #print(f"Picture: {img} and hashval {hash}")

            p = hashes.get(hash, [])
            p.append(picture)
            hashes[hash] = p

            
        
        for (h, duplicte) in hashes.items():
            if len(duplicte) > 1:
                for item in duplicte:
                    # build dst file first and check if it there already from previous run

                    # '/mnt/c/Users/ethoren/Pictures/_temp/processed_img/20151114_143628.jpg'
                    srcname = item
                    # 20151114_143628.jpg
                    sbasename = os.path.basename(srcname)

                    # '/mnt/c/Users/ethoren/Pictures/_temp/processed_img/_DUPLICATE/20151114_143628.jpg'
                    dstnameinit = os.path.join(self.ffolderdup, sbasename)
                    dstname = os.path.join(self.ffolderdup, str(h) + '_' + os.path.basename(item))

                                  

                    #print(dst_initfname)

                    if not os.path.isfile(dstnameinit):
                        shutil.copy2(srcname, dstnameinit)
                        os.rename(dstnameinit, dstname)
                    else:
                        print(f" File {dst_fname} exists, continue with next")
            
                    
    def similarer(self):

        #https://blog.tattle.co.in/clustering-similar-images-with-phash/
        pass


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", required=True,	type=str, help="path to input image")
parser.add_argument("-t", "--type",	required=True, type=str, help="img|vid")
args = parser.parse_args()

picture = organiser(args.directory)

picture.mover(args.type)
picture.duplicator()





'''
import hashlib

file1 = r'/mnt/c/Users/ethoren/Pictures/_temp/_DUPLICATE/000000bf9bf3fff8_IMG010.jpg'
file2 = r'/mnt/c/Users/ethoren/Pictures/_temp/_DUPLICATE/000000bf9bf3fff8_IMG010_1.jpg'

with open(file1, 'rb') as f:
    print(hashlib.md5(f.read()).hexdigest())
'''

import os
import shutil

mediafolder = r'/mnt/c/Users/ethoren/Pictures/_temp/'


def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def is_vid(fname):
    f = fname.lower()
    return f.endswith("mp4") or f.endswith("3gp")

class MediaOrg():
    def __init__(self, basefolder):
        self.basefolder = basefolder
        self.imgfiles = []
        self.vidfiles = []
        self.equals ={}

    def getimgmedia(self):
        self.imgfiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if is_img(x)]
        return self.imgfiles
    
    def getvidmedia(self):
        self.vidfiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if is_vid(x)]
        return self.vidfiles
    
    def getsamenamings(self, filelist):
     
        for b in filelist:
            p = self.equals.get(os.path.basename(b), [])
            p.append(b)
            self.equals[os.path.basename(b)] = p
        return self.equals
          
    def movemedia(self, type, medialist):
        
        if type == "vid":
            targetdir = self.basefolder + "processed_vid"
        else:
            targetdir = self.basefolder + "processed_img"
            
            
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)

        filecount = 0

        for f, q in medialist.items():
            print(f, q)
            targetfile = targetdir + "/" + f
            
            for it in q:
                filecount += 1
                if not os.path.isfile(targetfile):
                    shutil.copy2(it, targetfile)
                else:
                    base, extension = os.path.splitext(targetfile)
                    #print(base, extension)
                    i = 1
                    targetfileupdate = base + "_" + str(i) + extension
                    while os.path.isfile(targetfileupdate):
                        i += 1    
                        targetfileupdate = base + "_" + str(i) + extension
                    shutil.copy2(q[0], targetfileupdate)
        
        print(f'{filecount} files copied')

#videos = MediaOrg(mediafolder)
#vids = videos.getvidmedia()
#viddict = videos.getsamenamings(vids)
#videos.movemedia("vid", viddict)

photos = MediaOrg(mediafolder)
imgs = photos.getimgmedia()
imgdict = photos.getsamenamings(imgs)
photos.movemedia("img", imgdict)



'''
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



if not os.path.isfile(dstnameinit):
                        shutil.copy2(srcname, dstnameinit)
                        os.rename(dstnameinit, dstname)

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




#if avghash in hashes:
            #    duplicates.append(img)
            #else:
            #    hashes[avghash] = img


            #print(f"Picture: {img} and hashval {hash}")

            p = hashes.get(hash, [])
            p.append(picture)
            hashes[hash] = p




 i = 1
                    base, extension = os.path.splitext(fname)
                    dstname_new = os.path.join(self.ffolderimg, base + "_" + str(i) + extension) if ftype == "img" else os.path.join(self.ffoldervid, base + "_" + str(i) + extension)
                    while os.path.isfile(dstname_new):
                        i += 1
                        dstname_new = os.path.join(self.ffolderimg, base + "_" + str(i) + extension) if ftype == "img" else os.path.join(self.ffoldervid, base + "_" + str(i) + extension)
                    rcnt += 1
                    shutil.copy2(srcname, dstname_new) 



shpfiles = []
for dirpath, subdirs, files in os.walk(path):
    for x in files:
        if x.endswith(".shp"):
            shpfiles.append(os.path.join(dirpath, x))


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
'''
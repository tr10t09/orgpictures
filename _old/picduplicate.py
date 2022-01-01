import os
import shutil
import imagehash
from PIL import Image

picDir = r"/home/trendel/Bilder"

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


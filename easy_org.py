import argparse
import os
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True)
ap.add_argument("-t", "--type", choices = ['img', 'vid'], default = "img")
ap.add_argument("-r", "--recursive", action='store_true')
ap.add_argument("-m", "--movedir")

args = ap.parse_args()

equals = {}
fnum = 0

def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def is_vid(fname):
    f = fname.lower()
    return f.endswith("mp4") or f.endswith("3gp")


def get_filelist(mainfolder, ftype, recursive):
    global fnum
    if not recursive:
        if ftype == "img":
            mediafiles = [os.path.join(mainfolder, f) for f in os.listdir(mainfolder) 
                            if os.path.isfile(os.path.join(mainfolder, f)) and 
                                is_img(os.path.join(mainfolder, f))]
        else:
            mediafiles = [os.path.join(mainfolder, f) for f in os.listdir(mainfolder) 
                            if os.path.isfile(os.path.join(mainfolder, f)) and 
                                is_vid(os.path.join(mainfolder, f))]
    else:
        if ftype == "img":
            mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(mainfolder)
                            for x in f if is_img(x)]
        else:
            mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(mainfolder)
                            for x in f if is_vid(x)]

    fnum = len(mediafiles)

    for b in mediafiles:
        p = equals.get(os.path.basename(b), [])
        p.append(b)
        equals[os.path.basename(b)] = p

    return equals


def mover(movelist, targetdir):
    
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    
    fcnt = 0

    for f, q in movelist.items():
        targetfile = targetdir + f
        
        for it in q:
            fcnt += 1
            #print(f'{fcnt:5d}/{fnum:5d} --- FILE: [{it:100}]', end='\r', flush = True)
            print(f'{fcnt:5d}/{fnum:5d} --- FILE: [{it:100}]', flush=True)
            if not os.path.isfile(targetfile):
                shutil.copy2(it, targetfile)
            else:
                base, extension = os.path.splitext(targetfile)
                i = 1
                targetfileupdate = base + "_" + str(i) + extension
                
                while os.path.isfile(targetfileupdate):
                    i += 1
                    targetfileupdate = base + "_" + str(i) + extension
                shutil.copy2(it, targetfileupdate)

filelist = get_filelist(args.directory, args.type, args.recursive)

if args.movedir is not None:
    mover(filelist, args.movedir)
    


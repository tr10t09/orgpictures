import argparse
import os
import shutil
import pandas as pd
from fileprops import FileProps, FilePropsImg

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True)
ap.add_argument("-t", "--type", choices = ['img', 'vid'], default = "img")
ap.add_argument("-r", "--recursive", action='store_true')
ap.add_argument("-m", "--movedir")
ap.add_argument("-D", "--duplicates", action='store_true')


args = ap.parse_args()

equals = {}
fnum = 0

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*(full_progbar))
    print('\r[{:>7.2%}]'.format(frac), '#'*filled_progbar + '-'*(full_progbar-filled_progbar), end='')

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
            progbar(fcnt, fnum, 50)

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
    print(f' {fnum} files moved')

def get_duplicates(mainfolder):
    # only for images
    mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(mainfolder) 
                    for x in f if is_img(x)]
    medialist = []

    for mfile in mediafiles:
        medialist.append(FileProps(mfile))
    
    mediadict = {}
    for i in medialist:
        mediadict[os.path.basename(i.fname)] = [i.hashval, i.fsize, i.fmtime]
        
    df = pd.DataFrame.from_dict(mediadict, orient='index').reset_index()
    df.columns = ['file','hash', 'size', 'time']
    df = df[['hash', 'file', 'size', 'time']]
    df = df.groupby(['hash', 'size']).agg({'file':['count', list], 'time':list}).reset_index()
    df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df.columns.values]
    df = df[df["file_count"] >= 2]
    df.reset_index(inplace=True)
    df['timeidx'] = df.apply(lambda x: x['time_list'].index(min(x['time_list'])), axis=1)
    df['fselect'] = df.apply(lambda x: x['file_list'][int(x['timeidx'])], axis=1)
    df.apply(lambda x: x['file_list'].remove(x['fselect']), axis=1)
    df = df.explode('file_list')
    df_list = df['file_list'].tolist()

    dup_list = [os.path.join(mainfolder, item) for item in df_list]

    return dup_list

def dup_mover(duplicates, mainfolder):
    targetdir = mainfolder + "_DUPLICATES/"

    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    
    fcnt = 0 

    for i in duplicates:
        tname = targetdir + os.path.basename(i)
        fcnt += 1
        progbar(fcnt, len(duplicates), 50)

        if not os.path.isfile(tname):
            shutil.move(i, tname)
    
        else:
            base, extension = os.path.splitext(tname)
            d = 1
            tnameupdate = base + "_" + str(d) + extension
            
            while os.path.isfile(tnameupdate):
                d += 1
                tnameupdate = base + "_" + str(d) + extension
            
            shutil.move(i, tnameupdate)
    print(f' {len(duplicates)} duplicates are moved')

filelist = get_filelist(args.directory, args.type, args.recursive)

if args.movedir is not None and not args.duplicates:
    mover(filelist, args.movedir)

if args.duplicates and args.movedir is None:
    # only for images
    duplicatelist = get_duplicates(args.directory)
    dup_mover(duplicatelist, args.directory)
    


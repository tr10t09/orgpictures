import os
import shutil
import pandas as pd
import argparse
from mediaorg import MediaOrg
from picture import Picture
from fileprops import FileProps

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True)
ap.add_argument("-t", "--type", choices = ['img', 'vid'], default = "img")
ap.add_argument("-r", "--recursive", action='store_true')
ap.add_argument("-l", "--list", action='store_true')
ap.add_argument("-m", "--move")
args = ap.parse_args()
#print(args.recursive)
#print(args.type)
#print(args.directory)
#print(args.move)
#mediafolder = args.directory
arg = vars(ap.parse_args())
#print(arg)
#print(arg['name'])


#mediafolder = r'/home/trendel/Bilder/_backup_hd/'
photofolder = r'/home/trendel/Bilder/_backup_hd/processed_img'
_DUPLICATES = r'/home/trendel/Bilder/_backup_hd/_DUPLICATES'

media = MediaOrg(args.directory, args.recursive, args.type)
medialist = media.get_mediafilelist()
mediadict = media.get_samefilenames(medialist)

if args.list:
    #BEFORE MOVE PROVIDE DF OF DUPLICATES
    #media.get_mediaduplicatelist(medialist)
    media.get_dfmediafilelist(medialist)

if args.move is not None:
    media.mv_media(args.move, mediadict)
    

     





#print(imgs)
#photos.getdffromdict(imgs)

#print(imgdict['DSC_0001.jpg'])
#temp = {k: v for k, v in imgdict.items() if k == 'DSC_0001.jpg'}
#photos.movemedia(temp)
#photos.movemedia(imgdict)


'''
if not os.path.exists(_DUPLICATES):
    os.makedirs(_DUPLICATES)


#for m in get_duplicates(photofolder):
for m in photos.getduplicates(photofolder):
    #move to _DUPLICATES
    #shutil.move(src, dst, copy_function=copy2)
    shutil.move(m, _DUPLICATES)
'''

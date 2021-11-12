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
args = ap.parse_args()
#print(args.recursive)
#print(args.type)
#print(args.directory)
#mediafolder = args.directory
#arg = vars(ap.parse_args())
#print(arg['name'])


#mediafolder = r'/home/trendel/Bilder/_backup_hd/'
photofolder = r'/home/trendel/Bilder/_backup_hd/processed_img'
_DUPLICATES = r'/home/trendel/Bilder/_backup_hd/_DUPLICATES'

#print(mediafolder)

#videos = MediaOrg(mediafolder, "vid")
#vids = videos.getmedia()
#viddict = videos.getsamenamings(vids)
#videos.movemedia(viddict)

#MediaOrg(folder, recursive, type)
#photos = MediaOrg(mediafolder, "img")
photos = MediaOrg(args.directory, args.recursive, args.type)
imgs = photos.getmedia()
imgdict = photos.getsamenamings(imgs)

#print(imgs)
photos.getdffromdict(imgs)

#print(imgdict['DSC_0001.jpg'])
#temp = {k: v for k, v in imgdict.items() if k == 'DSC_0001.jpg'}
#photos.movemedia(temp)
#photos.movemedia(imgdict)


#pic = FileProps('/mnt/c/Users/ethoren/Pictures/_temp/processed_img/DSC_0001_1.jpg')
#print(pic)

#pic2 = FileProps('/mnt/c/Users/ethoren/Pictures/_temp/processed_img/DSC_0001_2.jpg')
#print(pic2)


'''
if not os.path.exists(_DUPLICATES):
    os.makedirs(_DUPLICATES)


#for m in get_duplicates(photofolder):
for m in photos.getduplicates(photofolder):
    #move to _DUPLICATES
    #shutil.move(src, dst, copy_function=copy2)
    shutil.move(m, _DUPLICATES)
'''
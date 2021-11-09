import os
import shutil
import pandas as pd
from mediaorg import MediaOrg
from picture import Picture
from fileprops import FileProps


mediafolder = r'/home/trendel/Bilder/_backup_hd/'
photofolder = r'/home/trendel/Bilder/_backup_hd/processed_img'
_DUPLICATES = r'/home/trendel/Bilder/_backup_hd/_DUPLICATES'

#videos = MediaOrg(mediafolder, "vid")
#vids = videos.getmedia()
#viddict = videos.getsamenamings(vids)
#videos.movemedia(viddict)

photos = MediaOrg(mediafolder, "img")
imgs = photos.getmedia()
imgdict = photos.getsamenamings(imgs)
#print(imgdict['DSC_0001.jpg'])
#temp = {k: v for k, v in imgdict.items() if k == 'DSC_0001.jpg'}
#photos.movemedia(temp)
photos.movemedia(imgdict)


#pic = FileProps('/mnt/c/Users/ethoren/Pictures/_temp/processed_img/DSC_0001_1.jpg')
#print(pic)


#pic2 = FileProps('/mnt/c/Users/ethoren/Pictures/_temp/processed_img/DSC_0001_2.jpg')
#print(pic2)


'''

def get_duplicates(filefolder):
    mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(filefolder) for x in f]
    mediaprops = []

    # list of media file instances, each representing the properties of each file
    for mfile in mediafiles:
        mediaprops.append(FileProps(mfile))
    
    # create dictory as input for pandas
    mediadict = {}
    for i in mediaprops:
        mediadict[os.path.basename(i.fname)] = [i.hashval, i.fsize, i.fmtime]

    # put data to panda
    df = pd.DataFrame.from_dict(mediadict, orient='index').reset_index()
    df.columns = ['file','hash', 'size', 'time']
    df = df[['hash', 'file', 'size', 'time']]
    

    # do grouping based on hash and file size
    #grouped = df.groupby(['hash', 'size']).size().reset_index(name='counts')
    df = df.groupby(['hash', 'size']).agg({'file':['count', list], 'time':list}).reset_index()
    # flatten the header, caused by agg function
    df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df.columns.values]
    #print(df)
    #df.to_csv('/mnt/c/Users/ethoren/Pictures/_temp/filelist.csv', sep='\t', encoding='utf-8')
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    
    dfd = df[df["file_count"] >= 2]
    dfd.reset_index(inplace=True)
    
    dfd = dfd[['file_list','time_list']]
    print(dfd)
    # check for oldest file
    dfd['timeidx'] = dfd.apply(lambda x: x['time_list'].index(min(x['time_list'])), axis=1)
    
    # select file (not the duplicates) based on previous selection
    #df['new column']=df.apply(lambda x: x.file_list[int(x.oldestidx)], axis=1)
    dfd['fselect'] = dfd.apply(lambda x: x['file_list'][int(x['timeidx'])], axis=1)
    dfd.apply(lambda x: x['file_list'].remove(x['fselect']), axis=1)
    #print(dfd)
    #flat_list = [item for sublist in df['file_list'].tolist() for item in sublist]
    df_flat_list = dfd.explode('file_list')
    flat_list = df_flat_list['file_list'].tolist()
    
    dup_list = [os.path.join(filefolder, item) for item in flat_list]


    return dup_list

#print(get_duplicates(photofolder))
#get_duplicates(photofolder)
'''

'''
if not os.path.exists(_DUPLICATES):
    os.makedirs(_DUPLICATES)


#for m in get_duplicates(photofolder):
for m in photos.getduplicates(photofolder):
    #move to _DUPLICATES
    #shutil.move(src, dst, copy_function=copy2)
    shutil.move(m, _DUPLICATES)
'''
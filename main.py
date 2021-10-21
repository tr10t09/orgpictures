import os
import pandas as pd
from mediaorg import MediaOrg
from picture import Picture
from fileprops import FileProps


mediafolder = r'/mnt/c/Users/ethoren/Pictures/_temp/'
photofolder = r'/mnt/c/Users/ethoren/Pictures/_temp/processed_img'

#videos = MediaOrg(mediafolder, "vid")
#vids = videos.getmedia()
#viddict = videos.getsamenamings(vids)
#videos.movemedia(viddict)

#photos = MediaOrg(mediafolder, "img")
#imgs = photos.getmedia()
#imgdict = photos.getsamenamings(imgs)
#photos.movemedia(imgdict)

photofiles = [os.path.join(d, x) for d, sd, f in os.walk(photofolder) for x in f]
photoprops = []

#for files in photofiles[1:10]:
for files in photofiles:
    photoprops.append(FileProps(files))


picdict = {}
for i in photoprops:
    #print(os.path.basename(i.fname), i.hashval, i.fsize, i.fmtime)
    picdict[os.path.basename(i.fname)] = [i.hashval, i.fsize, i.fmtime]

df = pd.DataFrame.from_dict(picdict, orient='index').reset_index()
df.columns = ['file','hash', 'size', 'time']
df = df[['hash', 'file', 'size', 'time']]
#grouped = df.groupby(['hash', 'size']).size().reset_index(name='counts')
grouped = df.groupby(['hash', 'size']).agg({'file':['count', list], 'time':list}).reset_index()
grouped.columns = ['_'.join(col).strip() if col[1] else col[0] for col in grouped.columns.values]

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

grp_dupl = grouped[grouped["file_count"] >= 2]
grp_dupl.reset_index(inplace=True)
grp_flt = grp_dupl[['file_list','time_list']]
df = grp_flt

#grp_flt['oldest'] = grp_flt['time_list'].apply(lambda x: max(x))
#grp_flt['oldestidx'] = grp_flt['time_list'].apply(lambda x: x.index(max(x)))


#print(grp_flt[['time_list', 'oldest', 'oldestidx']])

#print(grp_flt['time_list'])

#df = pd.DataFrame({'A' : (1,2,3), 'B': ([0,1,2],[3,4,5,],[6,7,8])})
#df['C'] = df['A'] + df['B'].apply(lambda x:x[1])
#df['C'] = df['A'] + df.apply(lambda row: row['B'][1], axis = 1) 




#https://stackoverflow.com/questions/23787895/python-pandas-access-the-element-of-the-list-in-dataframe

#df=pd.DataFrame({'pos': {0: [0.11,0.14,0.46], 1:[1,2,3]},'n': {0: 2.0,1:1}})


#grp_flt['oldest'] = grp_flt['time_list'].apply(lambda x: max(x))
#grp_flt['oldestidx'] = grp_flt['time_list'].apply(lambda x: x.index(max(x)))

df['timeidx'] = df.apply(lambda x: x['time_list'].index(min(x['time_list'])), axis=1)
#df['new column']=df.apply(lambda x: x.file_list[int(x.oldestidx)], axis=1)
df['fselect']=df.apply(lambda x: x['file_list'][int(x['timeidx'])], axis=1)
print(df[['file_list', 'time_list', 'timeidx']])


'''
df_hem["distance"] = df_hem.apply(lambda x: distance.hamming(ahash, x["hash"]),axis=1)

print(distance.hamming(ahash, df_hem["hash"][1]))

        print(df_hem.apply(lambda x: distance.hamming(ahash, x["hash"]),axis=1))

        df_hem["distance"] = df_hem.apply(lambda x: distance.hamming(ahash, x["hash"]),axis=1)




print('-------------------')
for x, y in zip(grp_dupl['file_list'], grp_dupl['time_list']):
    # check oldest element in y and take index from there to select x
    is_min_level = min(y)
    print(y.index(is_min_level))
    print(x[y.index(is_min_level)])



if is_min_level:
    return values.index(min(values))
else:
    return values.index(max(values))       


#temp = [f(x, y) for x, y in zip(grouped['file_list'], grouped['time_list'])]

'''
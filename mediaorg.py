import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from fileprops import FileProps, FilePropsImg


class MediaOrg():
    def __init__(self, basefolder, recursive, mediatype):
        self.basefolder = basefolder
        self.recursive = recursive
        self.type = mediatype
        self.mediafiles = []
        self.equals ={}
    

    @staticmethod
    def is_img(fname):
        f = fname.lower()
        return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

    @staticmethod
    def is_vid(fname):
        f = fname.lower()
        return f.endswith("mp4") or f.endswith("3gp")

    
    def get_mediafilelist(self):
        if not self.recursive:
            for folderitems in os.listdir(self.basefolder):
                fullitem = os.path.join(self.basefolder, folderitems)
                if "processed" not in fullitem:
                    if os.path.isfile(fullitem):
                        f = fullitem.lower()                
                        if self.type == 'img' and (f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")):
                            #print(f'{fullitem} is an image')
                            self.mediafiles.append(fullitem)
                        elif self.type == 'vid' and (f.endswith("mp4") or f.endswith("3gp")):
                            #print(f'{fullitem} is an video')
                            self.mediafiles.append(fullitem)
                        else:
                            continue
                    else:
                        continue

        else:
            if self.type == "vid":
                self.mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if MediaOrg.is_vid(x)]
            else:
                self.mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if MediaOrg.is_img(x)]
        
        return self.mediafiles
    
    def get_samefilenames(self, filelist):
     
        for b in filelist:
            p = self.equals.get(os.path.basename(b), [])
            p.append(b)
            self.equals[os.path.basename(b)] = p
        return self.equals
    
    def get_dfmediafilelist(self, filelist):
        
        imgpathdict = {}

        for b in filelist:
            imgpathdict[b] = os.path.basename(b)

        df = pd.DataFrame(imgpathdict.items(), columns=['fullpath', 'fname'])        
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)

        print(df)
        print(f'Number of mediafile {len(df.index)}')
    
    def get_mediaduplicatelist(self, filelist):
        mediaprops = []

        for mfile in filelist:
            mediaprops.append(FileProps(mfile))
            
        mediadict = {}
        for i in mediaprops:
            mediadict[i.fname] = [i.hashval, i.fsize, i.fmtime]
        
        df = pd.DataFrame.from_dict(mediadict, orient='index').reset_index()
        df.columns = ['file','hash', 'size', 'time']
        df = df[['hash', 'file', 'size', 'time']]
        df = df.groupby(['hash', 'size']).agg({'file':['count', list], 'time':list}).reset_index()
        df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df.columns.values]
        
        dfd = df[df["file_count"] >= 2]
        dfd.reset_index(inplace=True)
        dfd = dfd[['file_list']]        
        
        for index, row in dfd.iterrows():
            print("; ".join(row['file_list']))

        
        def get_timedeviation(self):

                        #SHOW PROGRESS BAR
            #CHECK OLDEST TIMESTAMP IN TIME AND EXIFTIME + ADD COL WITH DELTA
            


            dfd['mtime_old'] = dfd.apply(lambda x: min(x['time_list']), axis=1)
            dfd['exiftime_old'] = dfd.apply(lambda x: min(x['exiftime_list']), axis=1)
            
            dfd['mtime_old'] =  pd.to_datetime(dfd['mtime_old'], format='%Y:%m:%d %H:%M:%S')
            dfd['exiftime_old'] =  pd.to_datetime(dfd['exiftime_old'], format='%Y:%m:%d %H:%M:%S')

            #dfd['mtime_old'] = datetime.strptime(dfd['mtime_old'], '%Y:%m:%d %H:%M:%S')
            #dfd['exiftime_old'] = datetime.strptime(dfd['exiftime_old'], '%Y:%m:%d %H:%M:%S')

            #dfd['delta'] = dfd['exiftime_old'] - dfd['mtime_old']
            #pd.Timedelta(t2 - t1).seconds / 60.0
            #dfd['delta'] = dfd.Timedelta('exiftime_old' - 'mtime_old') / 60.0

            dfd['delta1'] = (dfd.exiftime_old - dfd.mtime_old) / pd.Timedelta(hours=1)
            dfd['delta2'] = (dfd.mtime_old - dfd.exiftime_old) / pd.Timedelta(hours=1)
            dfd.to_csv('/home/ethoren/filelist.csv', sep=';', encoding='utf-8', index = False, float_format='%.2f')
            #print(dfd)
            print(dfd.dtypes)

        
    def mv_media(self, mediadict):
        
        if self.type == "vid":
            targetdir = self.movefolder + "processed_vid"
        elif self.type == "img":
            targetdir = self.movefolder + "processed_img"
        else:
            print("Nothing to move")
            
        # create move to folder if does not exists
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)

        filecount = 0

        for f, q in mediadict.items():
            #print(f, q)
            # target filename /tmp/<file>
            targetfile = targetdir + f
            
            for it in q:
                
                filecount += 1
                print(f'{filecount:5d}/{len(self.mediafiles):5d} --- FILE: [{it:20}]', end='\r', flush = True)                
                if not os.path.isfile(targetfile):
                    shutil.copy2(it, targetfile)
                    #print(f'0: {it} copied to {targetfile}')
                else:
                    base, extension = os.path.splitext(targetfile)
                    #print(base, extension)
                    i = 1
                    targetfileupdate = base + "_" + str(i) + extension
                    
                    while os.path.isfile(targetfileupdate):
                        i += 1    
                        targetfileupdate = base + "_" + str(i) + extension
                    #print(f'{i}: {q[0]} copied to {targetfileupdate}')
                    #print(f'{i}: {it} copied to {targetfileupdate}')
                    #shutil.copy2(q[0], targetfileupdate)
                    shutil.copy2(it, targetfileupdate)
        
        #print(f'{filecount} files copied')
    
    def getduplicates(self, filefolder):
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
        #df.to_csv('/mnt/c/Users/ethoren/Pictures/_temp/filelist.csv', sep='\t', encoding='utf-8')
        
        #pd.set_option('display.max_colwidth', None)
        #pd.set_option('display.max_rows', None)
        
        # get duplicates
        dfd = df[df["file_count"] >= 2]
        dfd.reset_index(inplace=True)
        dfd = dfd[['file_list','time_list']]
        
        # check for oldest file
        dfd['timeidx'] = dfd.apply(lambda x: x['time_list'].index(min(x['time_list'])), axis=1)
        
        # select file (not the duplicates) based on previous selection
        #df['new column']=df.apply(lambda x: x.file_list[int(x.oldestidx)], axis=1)
        dfd['fselect'] = dfd.apply(lambda x: x['file_list'][int(x['timeidx'])], axis=1)
        dfd.apply(lambda x: x['file_list'].remove(x['fselect']), axis=1)
        
        # flatten column with duplicates
        #flat_list = [item for sublist in df['file_list'].tolist() for item in sublist]
        df_flat_list = dfd.explode('file_list')
        flat_list = df_flat_list['file_list'].tolist()
        
        # concate folder and file
        dup_list = [os.path.join(filefolder, item) for item in flat_list]
        
        return dup_list





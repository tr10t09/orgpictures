import os
import shutil
import pandas as pd
from fileprops import FileProps

class MediaOrg():
    def __init__(self, basefolder, mediatype):
        self.basefolder = basefolder
        self.type = mediatype
        self.mediafiles = []
        self.imgfiles = []
        self.vidfiles = []
        self.equals ={}
    
    @staticmethod
    def is_img(fname):
        f = fname.lower()
        return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

    @staticmethod
    def is_vid(fname):
        f = fname.lower()
        return f.endswith("mp4") or f.endswith("3gp")

    
    def getmedia(self):
        if self.type == "vid":
            self.mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if MediaOrg.is_vid(x)]
        else:
            self.mediafiles = [os.path.join(d, x) for d, sd, f in os.walk(self.basefolder) if "processed" not in d for x in f if MediaOrg.is_img(x)]
        return self.mediafiles

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
          
    def movemedia(self, medialist):
        
        if self.type == "vid":
            targetdir = self.basefolder + "processed_vid"
        else:
            targetdir = self.basefolder + "processed_img"
            
            
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)

        filecount = 0

        for f, q in medialist.items():
            #print(f, q)
            targetfile = targetdir + "/" + f
            
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





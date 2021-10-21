import os
import shutil

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




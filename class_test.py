import os

imgpath = r"/home/trendel/Bilder/"


def is_img(fname):
    f = fname.lower()
    return f.endswith("jpg") or f.endswith("jpeg") or f.endswith("png") or f.endswith("gif")

def is_vid(fname):
    f = fname.lower()
    return f.endswith("mp4") or f.endswith("gpd")


class imgorg():
    
    def __init__(self, imagepath):
        self.images = [f for f in os.listdir(imagepath) \
            if os.path.isfile(os.path.join(imagepath, f)) \
                and is_img(os.path.join(imagepath, f))]
        self.dirname = imagepath
    
    def mover (self):
        
        dirs = [x[0] for x in os.walk(self.dirname) if "processed" not in x[0]]

        #for x in os.walk(self.dirname):
        #    if "processed" not in x[0]:
        #        print(x[0])
       
    
        #imgDirpro = os.path.join(imgDir, "processed")
    
        #if not os.path.exists(imgDirpro):
            #os.makedirs(imgDirpro)

picture = imgorg(imgpath)
picture.mover()

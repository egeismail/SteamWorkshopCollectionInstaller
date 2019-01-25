import requests
import sys,json
import os
import zipfile
workshopdir = sys.argv[1] if len(sys.argv) >= 3 else sys.exit()
links = sys.argv[2] if len(sys.argv) >= 3 else sys.exit()
mode =  True if "install" == (sys.argv[3] if len(sys.argv) >= 3 else sys.exit()) else False
#TMPDir = os.path.join(workshopdir,".tmp")
#def CreateWTempFolder():
#    if not os.path.isdir(TMPDir):
#        os.makedirs(TMPDir)
def CreateFolder(dirs):
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
        return dirs
    else:
        return False
def ExtractZip(filename,edir):
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(edir)
    zip_ref.close()
#CreateWTempFolder()
class PluginContent(object):
    """docstring for PluginContent"""
    def __init__(self,data):
        super(PluginContent, self).__init__()
        self.data = data
        self.fid  = data["publishedfileid"]
        self.filename = data["filename"]
        self.file_Size= data["file_size"]
        self.file_url= data["file_url"]
        self.file_title = data["title"]
        self.nfilename = "%s-%s.zip"%(self.fid,self.file_title)
        self.fmid = "M%s-%s"%(self.fid,self.file_title)
        self.mfolder = os.path.join(workshopdir,self.fmid)
    def CreateFolder(self):
        return CreateFolder(self.mfolder)
    def Install(self):
        if(self.CreateFolder()):
            local_filename = os.path.join(self.mfolder,self.nfilename)
            r = requests.get(self.file_url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        #f.flush() commented by recommendation from J.F.Sebastian
            ExtractZip(local_filename,self.mfolder)
            os.remove(local_filename)
            return local_filename
        else:
            return None
    def Download(self):
        if(self.CreateFolder()):
            local_filename = os.path.join(self.mfolder,self.filename)
            r = requests.get(self.file_url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        #f.flush() commented by recommendation from J.F.Sebastian
            return local_filename
        else:
            return None
def GetPluginContent(id):
    m = {'itemcount' : 1, 'publishedfileids[0]' : id}
    r = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",m)
    return PluginContent(json.loads(r.text)["response"]["publishedfiledetails"][0])
def GetPID(url):
    args = [tuple(i.split("=")) for i in url.split("?")[-1].split("&")]
    for name,value in args:
        if(name=="id"):
            return int(value)
    return None
def main():
    plugins = [i for i in open(links,"r").readlines() if i!=""]
    for plugin in plugins:
        pd = GetPID(plugin)
        if(pd):
            d = GetPluginContent(pd)
            if(mode):
                if(d.Install()):
                    print "%s install complete.     \r"%(d.fmid)
                else:
                    print "%s aldready installed.       \r"%(d.fmid)
            else:
                if(d.Download()):
                    print "%s Download complete.     \r"%(d.fmid)
                else:
                    print "%s aldready downloaded.       \r"%(d.fmid)
if __name__ == '__main__':
    main()

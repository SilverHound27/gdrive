import os
import subprocess
from urllib.parse import unquote
import time
from pySmartDL import SmartDL
from random import choice

glitch = ['( ͡° ͜ʖ ͡°)', '¯\_(ツ)_/¯', '̿̿ ̿̿ ̿̿ ̿\̿\'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿', '¯\_(ツ)_/¯','ʕ•ᴥ•ʔ', '(ง ͠° ͟ل͜ ͡°)ง', '(;´༎ຶД༎ຶ`)']


def wget_dl(url):
        try:
            print("Downloading Started")
            # i was facing some problem in filename That's Why i did this ,
            #  i will fix it later :(

            filename = unquote(url.split('/')[-1])
            output = subprocess.check_output("wget '--output-document' '{}' '{}' ".format(filename , url), stderr=subprocess.STDOUT, shell=True)
            
            print("Downloading Complete",filename)
            return filename
        except Exception as e:
            print("DOWNLAOD ERROR :",e)
           
            return "error",filename
        
# wget_dl(url)
def smart_dl(url, sent_message):
    
    temp_name = unquote(url).split("/")[-1]
    dest = os.getcwd()
    obj = SmartDL(url, dest, progress_bar= False)
    obj.start(blocking = False)
    while not obj.isFinished():
        try:
            stats = "FileName: {} \nProgress: {:.2f}% \nSpeed: {} \nDownloaded: {}/{} \nStatus:{} \nEstimated time: {} \n    {}  ".format(
                temp_name, (obj.get_progress()*100), obj.get_speed(human=True), obj.get_dl_size(human=True), obj.get_final_filesize(human=True),
                obj.get_status(), obj.get_eta(human=True), obj.get_progress_bar())
            
            sent_message.edit_text(stats)
            time.sleep(3)
        except:
            sent_message.edit_text(choice(glitch))
            time.sleep(4)

    if obj.isSuccessful():
        filename = obj.get_dest().split('/')[-1]
        download_time = obj.get_dl_time(human=True)
    else:
        filename = False
        download_time = "NA"
    return filename, download_time
import os, os.path as path
os.chdir("C:/Users/ryan.mcgrath/Desktop/jfs/VTT Files")
fileList = [name for name in os.listdir('.') if os.path.isfile(name) and ".vtt" in name ]
print (fileList)
print(os.getcwd())

lastCap = ""

import webvtt
with open('transcript', 'w') as f:
    for vtt in fileList:
        vttName = vtt
        vtt = path.join(os.getcwd(), vtt)
        f.write(vtt + '\n')
        for c,caption in enumerate(webvtt.read(vtt)):
            text = caption.text.replace('\n',' ').strip()

            if text == '':
                continue

            index = text.rfind(lastCap)
          
            if index ==0 and len(text) != len(lastCap):# partial 
                #vtt will keep part of the last spoken sentence in the next scheduled caption
                #I'm only grabbbing the new part of the caption with the newPortion variable
                newPortion = text[len(lastCap)+1:]
                #print(newPortion)
                f.write(newPortion)
                #make the last caption the new portion we sliced
                lastCap = newPortion
            elif index == -1 or c == 0: #last caption not found, print all of this new line
                #print(text)
                f.write(text)
                lastCap = text
            elif len(text) == len(lastCap) and index == 0:#ignore the line, exact dupe of last line
                pass
            else: #catchall, just print
                #print(f'PASSED----vtt:{vtt}, index:{index}, lastCap:{lastCap}, text:{text}')
                #print(text)
                f.write(text)
                lastCap = text
                pass
            #look for word/phrase and link to timestamp
            if ' pill ' in caption.text:
                hour = caption.start[0:2]
                minute = caption.start[3:5]
                second = caption.start[6:8]
                videoID = vttName[-18:-7]
                print(f'[{caption.text}](https://www.youtube.com/watch?v={videoID}&t={hour}h{minute}m{second}s)')
                print('\n')
            
            f.write(' ')
            
        f.write('\n')
               



            #[print(str(caption)[26:])  for caption in webvtt.read(vtt) if '\n' in str(caption)]

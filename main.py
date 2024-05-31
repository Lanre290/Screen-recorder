from tkinter import *
from customtkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
from tktooltip import ToolTip
from PIL import ImageTk,Image,ImageEnhance,ImageGrab
import os,platform,subprocess
import datetime,time
import json
import pyautogui
import cv2
import numpy as np
import math

root = ctk.CTk()
root.title("Socket")
# root.wm_attributes('-fullscreen', True)
root.after(0, lambda:root.state('zoomed'))
root.iconbitmap('assets/ai.ico')

topFrame = ctk.CTkFrame(root,height = 100,fg_color = "#222222")
topFrame.pack(side = "top",fill = "x")


# dumm = Button()
# dumm.bind()

leftFrame = ctk.CTkFrame(root,width = 600)
leftFrame.pack(side = "left",fill = "y")

# tabs = ["home","settings","audio","video","info"]
currentTab = "home"
tabFrames = []

homeTabFrames = []
currentHomeTab = "get started"

filesList = []
currentFile:ctk.CTkFrame = ctk.CTkFrame(root)

isTimerForScreenRec = IntVar()
isPauseHotkeyVar = IntVar()
isPauseHotkeyVar.set(1)
timeForScreenRec = StringVar()
videoFormat = StringVar()
timeForScreenCapture = StringVar()
isScreenCapturekeyVar = IntVar()
isTimerForScreenCapture = IntVar()
imageFormat = StringVar()
frameRateVar= StringVar()



isRecordingActive = False
isRecordingPaused = False
stopRecording = False


homeImg = ImageTk.PhotoImage(Image.open("assets/home.png").resize((30,30)))
headPhonesImg = ImageTk.PhotoImage(Image.open("assets/headphones.png").resize((30,30)))
infoImg = ImageTk.PhotoImage(Image.open("assets/info.png").resize((30,30)))
settingsImg = ImageTk.PhotoImage(Image.open("assets/settings.png").resize((30,30)))
videoImg = ImageTk.PhotoImage(Image.open("assets/video.png").resize((30,30)))
imageImg = ImageTk.PhotoImage(Image.open("assets/picture.png").resize((30,30)))
roundCameraImg = ImageTk.PhotoImage(Image.open("assets/photo-camera.png").resize((70,70)))


screenRecorder = cv2.VideoWriter()

def process(img,value:float = 0.5):
    enhancer = ImageEnhance.Brightness(img)
    enhancer_step_two = enhancer.enhance(value)
    return enhancer_step_two

preHomeTabCameraImg = Image.open("assets/camera.png").resize((30,30))
homeTabCameraImgDulled = ImageTk.PhotoImage(process(preHomeTabCameraImg))

preHomeTabVidImg = Image.open("assets/cctv-camera.png").resize((30,30))
homeTabImgVidDulled = ImageTk.PhotoImage(process(preHomeTabVidImg))

preHomeTabImgImg = Image.open("assets/picture.png").resize((28,30))
homeTabImgImgDulled = ImageTk.PhotoImage(process(preHomeTabImgImg))


homeTabCameraImg = ImageTk.PhotoImage(Image.open("assets/camera.png").resize((30,30)))
vidTabCameraImg = ImageTk.PhotoImage(Image.open("assets/cctv-camera.png").resize((30,30)))
imgTabCameraImg = ImageTk.PhotoImage(Image.open("assets/picture.png").resize((28,30)))
playFileBtnImg = ImageTk.PhotoImage(Image.open("assets/play_.png").resize((70,70)))
deleteFileBtnImg = ImageTk.PhotoImage(Image.open("assets/bin.png").resize((70,70)))

preFilePlayImg = Image.open("assets/play_.png").resize((70,70))
disabledPlayImg = ImageTk.PhotoImage(process(preFilePlayImg))
preFileDelImg = Image.open("assets/bin.png").resize((70,70))
disabledDelImg = ImageTk.PhotoImage(process(preFileDelImg))

fileImage = ImageTk.PhotoImage(Image.open("assets/folder.png").resize((100,100)))
recordImage = ImageTk.PhotoImage(Image.open("assets/photo-camera.png").resize((100,100)))

prePauseRecImg = Image.open("assets/pause (1).png").resize((50,50))
pauseRecImgDulled = ImageTk.PhotoImage(process(prePauseRecImg))
PauseRecImg = ImageTk.PhotoImage(Image.open("assets/pause (1).png").resize((50,50)))

prePlayRecImg = Image.open("assets/play (1).png").resize((50,50))
playRecImgDulled = ImageTk.PhotoImage(process(prePlayRecImg))

screenshotImg = ImageTk.PhotoImage(Image.open("assets/photo-capture.png").resize((70,70)))
anticipateImg = ImageTk.PhotoImage(Image.open("assets/expectations.png").resize((300,300)))


appIcon = ImageTk.PhotoImage(Image.open("assets/app_icon.png").resize((150,150)))
companyIcon = ImageTk.PhotoImage(Image.open("assets/ai.png").resize((30,30)))


def getSetting(key):
    settings = str(open('settings.json','r').read())
    settingsJson = json.loads(settings)
    try:
        return settingsJson[key]
    except KeyError:
        raise KeyError(key," is not a valid key")
    finally:
        pass

def setSetting(key,value):
    settings = open('settings.json','r').read()
    settingsJson = json.loads(settings)
    if key in settingsJson:
        settingsJson[key] = value
        openedFile = open('settings.json','w')
        openedFile.write(str(json.dumps(settingsJson)))
        openedFile.close()
    else:
        print("Key doesn't eexist")


dir = getSetting("outputFolder")

class SideBarTabs(ctk.CTkFrame):
    def __init__(self,image,text = "Label",activeIdBg = "transparent",text_color = "#fafafa", *args,**kwargs):
        super().__init__(master=leftFrame,width = 600,height = 40,fg_color = "transparent",cursor = "hand2")
        self.text = text
        activeId = ctk.CTkFrame(self,width = 4,height = 40,fg_color = activeIdBg)
        activeId.pack(side = "left",padx = (1,0))
        icon = ctk.CTkLabel(self,image = image,fg_color="transparent",text = "")
        icon.pack(side = "left",padx = (15,10))
        text = ctk.CTkLabel(self,text = text,fg_color = "transparent",font = ("Calibri Light",19),text_color = text_color)
        text.pack(side = "left",padx = (0,100))
        tabFrames.append([self,activeId,text])

        ToolTip(self,msg= str(self.text),follow = False,delay = 0.1,fg = "#fafafa",bg="#111111",padx = 7,pady = 7,width = 50)
        ToolTip(activeId,msg= str(self.text),follow = False,delay = 0.1,fg = "#fafafa",bg="#111111",padx = 7,pady = 7,width = 50)
        ToolTip(icon,msg= str(self.text),follow = False,delay = 0.1,fg = "#fafafa",bg="#111111",padx = 7,pady = 7,width = 50)
        ToolTip(text,msg= str(self.text),follow = False,delay = 0.1,fg = "#fafafa",bg="#111111",padx = 7,pady = 7,width = 50)

        def enterSelf(event):
            self.configure(fg_color = "#333333")
        def leaveSelf(event):
            self.configure(fg_color = "transparent")
        def activateSelf(event):
            global currentTab
            currentTab = self.text
            for frame in tabFrames:
                if str(frame[0].text).lower() == currentTab.lower():
                    frame[1].configure(fg_color = "#00ccff")
                    frame[2].configure(text_color = "#00ccff")
                else:
                    frame[1].configure(fg_color = "transparent")
                    frame[2].configure(text_color = "#fafafa")
            for frame in allSideFrameFrames:
                frame.forget()
            if self.text.lower() == "home":
                homeFrame.pack(side = "left",fill = "both")
            elif self.text.lower() == "settings":
                settingsFrame.pack(side = "left",fill = "both")
            elif self.text.lower() == "video":
                videoSettingsFrame.pack(side = "left",fill = "both")
            elif self.text.lower() == "audio":
                audioSettingsFrame.pack(side = "left",fill = "both")
            elif self.text.lower() == "image":
                imageSettingsFrame.pack(side = "left",fill = "both")
            elif self.text.lower() == "info":
                infoFrame.pack(side = "left",fill = "both")
        
        self.bind('<Enter>',enterSelf)
        activeId.bind('<Enter>',enterSelf)
        icon.bind('<Enter>',enterSelf)
        text.bind('<Enter>',enterSelf)

        self.bind('<Button-1>',activateSelf)
        activeId.bind('<Button-1>',activateSelf)
        icon.bind('<Button-1>',activateSelf)
        text.bind('<Button-1>',activateSelf)

        self.bind('<Leave>',leaveSelf)
    def pack(self):
        super().pack(fill = "x",pady = (10,0),ipady = 5)


class homeTabs(ctk.CTkFrame):
    def __init__(self,image,attachedFrame,dull_image,text = "Label",text_color = "#777777",active = False, *args,**kwargs):
        super().__init__(master = homeTopnav,width = 600,height = 40,fg_color = "transparent",cursor = "hand2")
        self.text = text
        self.attached_frame = attachedFrame
        out_image = image
        if active == False:
            out_image = dull_image
            text_color = "#777777"
        icon = ctk.CTkLabel(self,image = out_image,fg_color="transparent",text = "",text_color = text_color)
        icon.pack(side = "left",padx = (15,10))
        text = ctk.CTkLabel(self,text = text,fg_color = "transparent",font = ("Calibri Light",19),text_color = text_color)
        text.pack(side = "left",padx = (0,100))

        homeTabFrames.append([icon,text,image,dull_image,attachedFrame])

        def enterSelf(event):
            icon.configure(image = image)
            text.configure(text_color = "#fafafa")
        def leaveSelf(event):
            if currentHomeTab.lower() != self.text.lower():
                icon.configure(image = dull_image)
                text.configure(text_color = "#777777")
        def activateSelf(event):
            global currentHomeTab,homeTabFrames
            currentHomeTab = self.text.lower()
            for frame in homeTabFrames:
                if str(frame[0].cget("text")).lower() == currentHomeTab.lower():
                    frame[0].configure(image = frame[2])
                    frame[1].configure(text_color = "#fafafa")
                else:
                    frame[0].configure(image = frame[3])
                    frame[1].configure(text_color = "#777777")
                    frame[4].forget()
            icon.configure(image = image)
            text.configure(text_color = "#fafafa")
            attachedFrame.pack(side = "top",fill = "both")
            if self.text == "Images":
                listImageFiles()
            if self.text == "Videos":
                listVideoFiles()
        
        self.bind('<Enter>',enterSelf)
        icon.bind('<Enter>',enterSelf)
        text.bind('<Enter>',enterSelf)

        self.bind('<Button-1>',activateSelf)
        icon.bind('<Button-1>',activateSelf)
        text.bind('<Button-1>',activateSelf)

        self.bind('<Leave>',leaveSelf)
    def pack(self):
        super().pack(side = "left",fill = "x",pady = (10,0),ipady = 5)

class seperator(ctk.CTkFrame):
    def __init__(self,master,height = 10,width = 3,orient = "vertical",color = "#333333", *args,**kwargs):
        try:
            if orient == "vertical":
                super().__init__(master  = master,height = height,width = 3,fg_color = color)
            elif orient == "horizontal":
                super().__init__(master  = master,height = 3,fg_color = color,width = width)
            else:
                raise ValueError("Unknown value for orient")
        except ValueError as e:
            print(e)
        finally:
            pass

class fileFrameFile(ctk.CTkFrame):
    def __init__(self,master,height = 15,cursor = "hand2",color = "transparent",corner_radius = 6,text = "",size = "", *args,**kwargs):
        super().__init__(master  = master,height = height,width = 3,fg_color = color,cursor = cursor,corner_radius=corner_radius)
        self.path = f"{dir}\{text}"
        self.fileName = ctk.CTkLabel(self,text = text,text_color = "#fafafa",font = ("Calibri Light",19))
        self.fileName.pack(side = "left",padx = (20,0))
        self.fileSize = ctk.CTkLabel(self,text = size,text_color = "#fafafa",font = ("Calibri Light",19))
        self.fileSize.pack(side = "right",padx = (0,20))
        # fileFrame,text = "Bandicam.mp4",text_color = "#fafafa",font = ("Calibri Light",19)
        def func(event):
            global currentFile
            currentFile.configure(fg_color = "transparent")
            currentFile = self
            for widget in filesList:
                widget.fileName.configure(fg_color = "transparent",text_color = "#fafafa")
                widget.fileSize.configure(fg_color = "transparent",text_color = "#fafafa")
            if text.endswith(".mp4") or text.endswith(".avi"):
                playBtn.configure(state = "enabled")
                delBtn.configure(state = "enabled")
                playBtn.configure(image = playFileBtnImg)
                delBtn.configure(image = deleteFileBtnImg)
            else:
                playBtn_2.configure(state = "enabled")
                delBtn_2.configure(state = "enabled")
                playBtn_2.configure(image = playFileBtnImg)
                delBtn_2.configure(image = deleteFileBtnImg)
            self.configure(fg_color = "#0099cc")
        
        def enterSelf(event):
            if currentFile != self:
                self.configure(fg_color = "#333333")
        def leaveSelf(event):
            global currentFile
            if currentFile != self:
                self.configure(fg_color = "transparent")

        
        
        

        self.bind('<Button-1>',func)
        self.bind('<Double-Button-1>',self.openFile)
        self.bind('<Enter>',enterSelf)
        self.bind('<Leave>',leaveSelf)
        self.fileSize.bind('<Button-1>',func)
        self.fileName.bind('<Button-1>',func)
        filesList.append(self)

    def openFile(self,event):
        path = self.path
        if platform.system() == 'Darwin':
            subprocess.call(('open',path))
        elif platform.system() == 'Windows':
            os.startfile(path)
        else:
            subprocess.call(('xdg-open',path))


def hover(widget):
    def func(event):
        widget.configure(fg_color = "#333333")
    def func_2(event):
        widget.configure(fg_color = "transparent")
    widget.bind('<Enter>',func)
    widget.bind('<Leave>',func_2)

def textHover(widget):
    def func(event):
        widget.configure(text_color = "#fafafa")
    def func_2(event):
        widget.configure(text_color = "#777777")
    widget.bind('<Enter>',func)
    widget.bind('<Leave>',func_2)

def hoverTransparent(widget):
    def func(event):
        widget.configure(fg_color = "transparent")
    widget.bind('<Enter>',func)

def addTooltip(widget,text,width = 50,delay = 0.1,fg = "#fafafa",bg = "#111111",padx= 7,pady= 7):
    ToolTip(widget,msg= str(text),follow = False,delay = delay,fg = fg,bg = bg,padx = padx,pady = pady,width = width)

def openFolder(url = dir):
    subprocess.Popen(f'explorer /select,"{url}"')

def darkScreen(duration = 0):
    window = ctk.CTkToplevel()
    window.attributes('-alpha',0.7)
    window.configure(bg_color = "#000000")
    window.focus_force()
    window.wm_attributes('-fullscreen', True)
    window.attributes('-topmost', 'true')
    duration = int(duration)
    def flash():
        root.update()
        window = ctk.CTkToplevel()
        window.attributes('-alpha',0.7)
        window.configure(bg_color = "#000000")
        window.focus_force()
        window.wm_attributes('-fullscreen', True)
        window.attributes('-topmost', 'true')
        window.after(370,window.destroy)
    if duration == 0:
        time.sleep(0.38)
        flash()
    else:
        window.after(duration*1000,window.destroy)
        timeLabel = ctk.CTkLabel(window,text = str(duration),text_color = "#fafafa",font = ("Calibri Light",250))
        timeLabel.pack(pady = (100,0))
        
        while duration > 0:
            root.update()
            duration -= 1
            timeLabel.configure(text = str(duration))
            time.sleep(1)

        time.sleep(0.38)
        root.update()
        flash()

def screenShot(event):
    def capture():
        capturedImg = ImageGrab.grab()
        fileName = str(datetime.datetime.now())[0:23]
        fileName = fileName.replace(":","-")
        location = getSetting("outputFolder")
        format_ = str(getSetting("imageFormat")).lower()
        capturedImg.save(f"{location}\{fileName}.{format_}")
        capturedImg.close()
    isSet = getSetting("isTimerForScreenCapture")
    if isSet == "True":
        time_ = getSetting("timeForScreenCapture")
        time_ = str(time_[:2]).strip()
        darkScreen(time_)
        time.sleep(0.38)
        root.update()
        capture()
    else:
        capture()

def openCurrentFile(event,path = ""):
    global currentFile
    if path == "":
        path = currentFile.path
    if platform.system() == 'Darwin':
        subprocess.call(('open',path))
    elif platform.system() == 'Windows':
        os.startfile(path)
    else:
        subprocess.call(('xdg-open',path))

def screenRecord(event):
    def record():
        global pauseBtn,isRecordingPaused,isRecordingActive,screenRecorder
        isRecordingPaused = False
        if isRecordingActive == True:
            isRecordingActive = False
            screenRecorder.release()
            pauseBtn.configure(image = pauseRecImgDulled)
        else:
            isRecordingActive = True
            pauseBtn.configure(image = PauseRecImg)

            x = pyautogui.size()[0] # getting the width of the screen
            y = pyautogui.size()[1] # getting the height of the screen
            resolution = (x, y)
        
            # Specify video codec
            codec = cv2.VideoWriter_fourcc(*'MP42')
            if getSetting('videoFormat') == 'AVI':
                codec = cv2.VideoWriter_fourcc(*'XVID')
            
            # Specify name of Output file
            location = getSetting("outputFolder")
            fileName_ = str(datetime.datetime.now())[0:23]
            fileName_ = fileName_.replace(":","-")
            format_ = str(getSetting("videoFormat")).lower()
            # if format_.lower() == "mp4":
            #     format_ = "mp4v"
            print(format_)
            fileName_ = f"{location}\{fileName_}.{format_}"
            
            # Specify frames rate. We can choose any 
            # value and experiment with it
            fps = float(getSetting('frameRate')[:2])
            print("fps: ",fps)
            
            
            # Creating a VideoWriter object
            screenRecorder  = cv2.VideoWriter(fileName_, codec, fps, resolution)
        
            def record_():
                while True:
                    if isRecordingPaused == True:
                        continue
                    if isRecordingActive == False:
                        break
                    # Take screenshot using PyAutoGUI
                    img = pyautogui.screenshot()
                    # img = cv2.imread('screen.png',cv2.IMREAD_COLOR)'
                    # img = cv2.resize(img,(x,y),interpolation = cv2.INTER_AREA)
                
                    # Convert the screenshot to a numpy array
                    frame = np.array(img)
                
                    # Convert it from BGR(Blue, Green, Red) to
                    # RGB(Red, Green, Blue)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                    # Write it to the   output file
                    screenRecorder.write(frame)
                    
                    # # Stop recording when we press 'q'
                    if cv2.waitKey(10) and 0xFF == ord('q'):
                        break
                    root.update()
            record_()
            screenRecorder.release()
            cv2.destroyAllWindows()
        
    isSet = getSetting("isTimerForScreenRecord")
    print(isSet)
    if isSet == "True" and isRecordingActive == False:
        time_ = getSetting("timeForScreenRecord")
        time_ = str(time_[:2]).strip()
        darkScreen(time_)
        time.sleep(0.38)
        root.update()
        record()
    else:
        record()

def pauseRecording(event):
    global isRecordingPaused,pauseBtn
    print(isRecordingPaused)
    if isRecordingActive == True:
        if isRecordingPaused == True:
            isRecordingPaused = True
            pauseBtn.configure(image = pauseRecImgDulled)
        else:
            isRecordingPaused = False
            pauseBtn.configure(image = PauseRecImg)

def convertSize(size:int):
    out_size = 0
    if size > 1024:
        print("size",1024)
        out_size = f"{round(size/1024,1)}KB"
    if size > 1048576:
        out_size = f"{round(size/1048576,1)}MB"
    return out_size


if getSetting("firstTime") == "True":
    setSetting("outputFolder",f"C:\\users\\{os.getlogin()}\\videos\\socket")
if os.path.isdir(getSetting("firstTime")) == False:
    setSetting("outputFolder",f"C:\\users\\{os.getlogin()}\\videos\\socket")


#topframe comonents
def openOutputFolder(event):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    openFolder(dir)


fileButton = ctk.CTkLabel(topFrame,image = fileImage,text = "",cursor = "hand2",fg_color = "transparent")
fileButton.pack(side = "left",padx = (30,5),pady = (10,10))
addTooltip(fileButton,text = "Open output folder",width = 150)
fileButton.bind('<Button-1>',openOutputFolder)
centerFrame = ctk.CTkFrame(topFrame,fg_color = "transparent")
centerFrame.pack(pady = (10,10))
pauseBtn = ctk.CTkLabel(centerFrame,image = pauseRecImgDulled,cursor = "hand2",fg_color = "transparent",text = "")
pauseBtn.pack(side = "left",padx = (10,10))
recordBtn = ctk.CTkLabel(centerFrame,image = recordImage,cursor = "hand2",fg_color = "transparent",text = "")
recordBtn.pack(side = "left",padx = (10,10))
captureBtn = ctk.CTkLabel(centerFrame,image = screenshotImg,cursor = "hand2",fg_color = "transparent",text = "")
captureBtn.pack(side = "left",padx = (0,10))
addTooltip(recordBtn,text = "Start recording",width  = 150)
addTooltip(pauseBtn,text = "pause recording",width  = 150)
addTooltip(captureBtn,text = "Capture screenshot",width  = 150)
captureBtn.bind('<Button-1>',screenShot)
recordBtn.bind('<Button-1>',screenRecord)
pauseBtn.bind('<Button-1>',pauseRecording)



homeSideFrame = SideBarTabs(image = homeImg,text = "Home",activeIdBg="#00ccff",text_color="#00ccff")
homeSideFrame.pack()
settingsSideFrame = SideBarTabs(image = settingsImg,text = "Settings")
settingsSideFrame.pack()
videoSideFrame = SideBarTabs(image = videoImg,text = "Video")
videoSideFrame.pack()
audioSideFrame = SideBarTabs(image = headPhonesImg,text = "Audio")
audioSideFrame.pack()
imageSideFrame = SideBarTabs(image = imageImg,text = "Image")
imageSideFrame.pack()
infoSideFrame = SideBarTabs(image = infoImg,text = "Info")
infoSideFrame.pack()



homeFrame = ctk.CTkFrame(root,fg_color="transparent")
homeFrame.pack(side = "left",fill = "both")




homeTopnav = ctk.CTkFrame(homeFrame,fg_color="transparent")
homeTopnav.pack(side = "top",padx = (50,10),pady = (20,10),anchor = "w")

homeTabFrame = ctk.CTkFrame(homeFrame,fg_color = "transparent")
homeTabFrame.pack(side = "top",fill = "both")
homeLabel1 = ctk.CTkLabel(homeTabFrame,text = "Screen recording - Fullscreen",font = ("Calibri Light",29),text_color = "#fafafa")
homeLabel1.pack(side = "top",pady = (15,15),padx = (20,10),anchor = "w")
homeLabel2 = ctk.CTkLabel(homeTabFrame,text = "This mode allows you to record the whole screen of your display.",font = ("Calibri Light",20),text_color = "#fafafa")
homeLabel2.pack(pady = (10,10),padx = (20,10),anchor = "w")
homeLabel3 = ctk.CTkLabel(homeTabFrame,text = "Click the camera icon at the top to start.",font = ("Calibri Light",20),text_color = "#fafafa")
homeLabel3.pack(pady = (10,10),padx = (20,10),anchor = "w")


videoTabFrame = ctk.CTkFrame(homeFrame,fg_color = "transparent")
# videoTabFrame.pack(side = "top",fill = "both")
outFolder = ctk.CTkLabel(videoTabFrame,text_color = "#777777",text = dir,font = ("Calibri Light",23),cursor = "hand2")
outFolder.pack(side = "top",padx = (20,10),pady = (10,0),anchor = "w")
textHover(outFolder)
def clickOutFolder(event):
    openFolder()
outFolder.bind('<Button-1>',clickOutFolder)


vidsCont = ctk.CTkScrollableFrame(videoTabFrame,scrollbar_button_hover_color="#0099cc",height = 350,corner_radius=12)
vidsCont.pack(side = "top",fill = "x",pady = (10,5),padx = (20,10))

bottomSideFrame = ctk.CTkFrame(videoTabFrame,height = 70,fg_color = "transparent")
bottomSideFrame.pack(side = "bottom",fill = "y",pady = (10,0))
playBtn = ctk.CTkButton(bottomSideFrame,image = disabledPlayImg,width = 75,height = 75,state="disabled",hover_color="#232323",corner_radius = 8,fg_color = "transparent",text = "",cursor = "hand2")
playBtn.pack(side  = "left")
delBtn = ctk.CTkButton(bottomSideFrame,image = disabledDelImg,width = 75,height = 75,state="disabled",hover_color="#232323",corner_radius = 8,fg_color = "transparent",text = "",cursor = "hand2")
delBtn.pack(side  = "left")

def delVideoFile(event):
    ask = messagebox.askyesno("Delete File ?","Are you sure to delete this file ?")
    if ask == True:
        os.remove(currentFile.path)
        listVideoFiles()

playBtn.bind('<Button-1>',openCurrentFile)
delBtn.bind('<Button-1>',delVideoFile)
hoverTransparent(playBtn)
hoverTransparent(delBtn)
addTooltip(playBtn,text = "Open file")
addTooltip(delBtn,text = "Delete file",width = 70)

vidErrIcon = ctk.CTkLabel(root)
vidErrLabel = ctk.CTkLabel(root)
def listVideoFiles():
    global vidErrIcon,vidErrLabel
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    files = os.listdir(dir)
    fileFound = False
    for file in filesList:
        file.forget()
    for file in files:
        try:
            if str(file).endswith(".mp4") or str(file).endswith(".avi"):
                vidErrLabel.forget()
                vidErrIcon.forget()
                fileFound = True
                fileFrame = fileFrameFile(master = vidsCont,fg_color="transparent",height = 25,text = f"{file}",size = str(convertSize(os.path.getsize(f"{dir}\{file}"))))
                fileFrame.pack(side = "top",fill = "x")
        except FileNotFoundError:
            pass
        finally:
            pass
    
    if fileFound == False:
        vidErrLabel.forget()
        vidErrIcon.forget()
        errIcon  = ImageTk.PhotoImage(Image.open("assets/assets\problem.png").resize((200,200)))
        errLabel = ctk.CTkLabel(vidsCont,image = errIcon,text = "")
        errLabel.pack(pady = (40,0))
        label = ctk.CTkLabel(vidsCont,text = "No Files",font = ("Calibri Light",25),text_color = "#fafafa")
        label.pack()
        vidErrIcon = errLabel
        vidErrLabel = label


imageTabFrame = ctk.CTkFrame(homeFrame,fg_color = "transparent")
# imageTabFrame.pack(side = "top",fill = "both")
outFolder_2 = ctk.CTkLabel(imageTabFrame,text_color = "#777777",text = dir,font = ("Calibri Light",23),cursor = "hand2")
outFolder_2.pack(side = "top",padx = (20,10),pady = (10,0),anchor = "w")
textHover(outFolder_2)
def clickOutFolder(event):
    openFolder()
outFolder_2.bind('<Button-1>',clickOutFolder)
imgsCont = ctk.CTkScrollableFrame(imageTabFrame,height = 350,corner_radius=12)
imgsCont.pack(side = "top",fill = "x",pady = (10,0),padx = (20,10))


# ['JPG','PNG','BMP']
imgErrIcon = ctk.CTkLabel(root)
imgErrLabel = ctk.CTkLabel(root)
def listImageFiles():
    global imgErrIcon,imgErrLabel
    if os.path.isdir(dir) == False:
        os.mkdir(dir)
    files = os.listdir(dir)
    fileFound = False
    for file in filesList:
        file.forget()
    for file in files:
        try:
            if str(file).endswith(".png") or str(file).endswith(".bmp") or str(file).endswith(".jpg"):
                fileFound = True
                imgErrIcon.forget()
                imgErrLabel.forget()
                fileFrame_1 = fileFrameFile(master = imgsCont,fg_color="transparent",height = 25,text = f"{file}",size = str(convertSize(os.path.getsize(f"{dir}\{file}"))))
                fileFrame_1.pack(side = "top",fill = "x")
        except FileNotFoundError:
            pass
        finally:
            pass
    if fileFound == False:
        imgErrIcon.forget()
        imgErrLabel.forget()
        errIcon  = ImageTk.PhotoImage(Image.open("assets/assets\problem.png").resize((200,200)))
        errLabel = ctk.CTkLabel(imgsCont,image = errIcon,text = "")
        errLabel.pack(pady = (40,0))
        label = ctk.CTkLabel(imgsCont,text = "No Files",font = ("Calibri Light",25),text_color = "#fafafa")
        label.pack()
        imgErrIcon = errLabel
        imgErrLabel = label


homeTab = homeTabs(master = homeTopnav,attachedFrame=homeTabFrame,image = homeTabCameraImg,dull_image=homeTabCameraImgDulled,text = "Get started",text_color="#fafafa",active = True)
homeTab.pack()
sep_1 = seperator(master = homeTopnav,color = "#555555",height = 40)
sep_1.pack(side = "left")
videosTab = homeTabs(master = homeTopnav,attachedFrame=videoTabFrame,image = vidTabCameraImg,dull_image=homeTabImgVidDulled,text = "Videos",text_color="#fafafa")
videosTab.pack()
sep_1 = seperator(master = homeTopnav,color="#555555",height = 40)
sep_1.pack(side = "left")
ImageTab = homeTabs(master = homeTopnav,attachedFrame=imageTabFrame,image = imgTabCameraImg,dull_image=homeTabImgImgDulled,text = "Images",text_color="#fafafa")
ImageTab.pack()

bottomSideFrame_2 = ctk.CTkFrame(imageTabFrame,height = 70,fg_color = "transparent")
bottomSideFrame_2.pack(side = "bottom",fill = "y",pady = (10,30))
playBtn_2 = ctk.CTkButton(bottomSideFrame_2,image = disabledPlayImg,width = 75,height = 75,state="disabled",hover_color="#232323",corner_radius = 8,fg_color = "transparent",text = "",cursor = "hand2")
playBtn_2.pack(side  = "left")
delBtn_2 = ctk.CTkButton(bottomSideFrame_2,image = disabledDelImg,width = 75,height = 75,state="disabled",hover_color="#232323",corner_radius = 8,fg_color = "transparent",text = "",cursor = "hand2")
delBtn_2.pack(side  = "left")

def delImgFile(event):
    ask = messagebox.askyesno("Delete File ?","Are you sure to delete this file ?")
    if ask == True:
        os.remove(currentFile.path)
        listImageFiles()
playBtn_2.bind('<Button-1>',openCurrentFile)
delBtn_2.bind('<Button-1>',delImgFile)
hoverTransparent(playBtn_2)
hoverTransparent(delBtn_2)
addTooltip(playBtn_2,text = "Open file")
addTooltip(delBtn_2,text = "Delete file",width = 70)





############################
#ettings frame
############################
settingsFrame = ctk.CTkFrame(root,fg_color="transparent")
optionsLabel = ctk.CTkLabel(settingsFrame,text = "Options",font = ("Calibri Light",20,"bold"),anchor = "w",text_color = "#ffffff",fg_color = "transparent")
optionsLabel.pack(padx = (10,0),pady = (30,3),anchor = "w")
seperator_1 = seperator(settingsFrame,orient = "horizontal",width = 400)
seperator_1.pack(pady = (5,10),padx = (10,0),fill = "x")
output_folder_text = ctk.CTkLabel(settingsFrame,text = "Output Folder",font = ("Calibri Light",17),text_color = "#eeeeee",anchor = "w")
output_folder_text.pack(pady = (10,5),anchor = "w",padx = (10,0))
entryFrame = ctk.CTkFrame(settingsFrame,fg_color = "transparent")
entryFrame.pack(anchor = "w",padx = (10,0))
currentFolderEntry = ctk.CTkEntry(entryFrame,fg_color = "#fafafa",text_color = "#090909",font = ("Calibri Light",25),corner_radius = 0,width = 400,border_width=0.1,border_color = "#111111")
currentFolderEntry.pack(side = "left")
currentFolderEntry.insert(0,dir)
currentFolderEntry.configure(state = "readonly")
changeButton = ctk.CTkLabel(entryFrame,text = "...",text_color = "#fafafa",fg_color = "#444444",width = 50,height = 37)
changeButton.pack(side = "left",padx = (5,0))
openButton = ctk.CTkLabel(entryFrame,text = "Open",text_color = "#fafafa",fg_color = "#444444",width = 70,height = 37)
openButton.pack(side = "left",padx = (5,0))

addTooltip(changeButton,text = "Change default directory",width = 150)
addTooltip(openButton,text = "Open directory",width = 150)

def changeDefaultDirectory(event):
    global dir
    folder = filedialog.askdirectory(title = "Open Folder")
    if len(folder) > 0:
        dir = folder
        currentFolderEntry.configure(state = "normal")
        currentFolderEntry.delete(0,END)
        currentFolderEntry.insert(0,dir)
        currentFolderEntry.configure(state = "readonly")
        messagebox.showinfo("Info","You need to restart the application for changes to take place")
        messagebox.askyesno("Restart?","Do you want to restart ?")
changeButton.bind('<Button-1>',changeDefaultDirectory)
openButton.bind('<Button-1>',openOutputFolder)


def specialHover(element):
    def func(event):
        element.configure(fg_color = "#555555")
    def func_2(event):
        element.configure(fg_color = "#444444")
    element.bind('<Enter>',func)
    element.bind('<Leave>',func_2)

specialHover(changeButton)
specialHover(openButton)

languageLabel = ctk.CTkLabel(settingsFrame,text = "Language",font = ("Calibri Light",18),text_color = "#fafafa")
languageLabel.pack(anchor = "w",padx = (10,0))
languageVar = StringVar()
languageOption = ctk.CTkOptionMenu(settingsFrame,variable=languageVar,dynamic_resizing=False,values = ['English'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
languageOption.pack(padx = (10,0),anchor = "w",pady = (5,0))
languageOption.set("English")
def regLanguage(*args):
    setSetting("language",languageVar.get())
languageVar.trace_add(['write'],regLanguage)


################################
#video settings frame
################################
videoSettingsFrame = ctk.CTkFrame(root,fg_color="transparent")
recordLabel = ctk.CTkLabel(videoSettingsFrame,text = "Record",font = ("Calibri Light",20,"bold"),anchor = "w",text_color = "#ffffff",fg_color = "transparent")
recordLabel.pack(padx = (10,0),pady = (30,3),anchor = "w")
seperator_2 = seperator(videoSettingsFrame,orient = "horizontal",width = 400)
seperator_2.pack(pady = (5,10),padx = (10,0),fill = "x")
frame_1 = ctk.CTkFrame(videoSettingsFrame,fg_color = "transparent")
frame_1.pack(pady = (5,10),padx = (10,0),anchor = "w")

timerCheck = ctk.CTkCheckBox(frame_1,variable = isTimerForScreenRec,cursor = "hand2",text = "",checkbox_height=30,checkbox_width = 30,hover_color="#3a3a3a",width = 30,height =30,border_width= 1.2,border_color = "#777777",corner_radius = 0)
timerCheck.pack(side = "left",padx = (0,5))
videoTimerLabel = ctk.CTkLabel(frame_1,text = "Place timer for screen record ?",font = ("Calibri Light",19),text_color = "#fafafa")
videoTimerLabel.pack(side = "left",padx = (0,10))
timerOptions = ctk.CTkOptionMenu(frame_1,variable=timeForScreenRec,dynamic_resizing=False,values = ['3 seconds','5 seconds','10 seconds'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
timerOptions.pack(anchor = "e",pady = (5,0),side = "right")
timerOptions.set(getSetting("timeForScreenRecord"))

def regIsTimerForScreenRec(*args):
    val = ""
    if isTimerForScreenRec.get() == 0:
        val = "False"
    else:
        val = "True"
    setSetting("isTimerForScreenRecord",val)
isTimerForScreenRec.trace_add(['write'],regIsTimerForScreenRec)
if getSetting("isTimerForScreenRecord") == "False":
    isTimerForScreenRec.set(0)
else:
    isTimerForScreenRec.set(1)
regIsTimerForScreenRec()



def regVideoTimer(*args):
    setSetting("timeForScreenRecord",timeForScreenRec.get())
timeForScreenRec.trace_add(['write'],regVideoTimer)

def manageIsTimer():
    if isTimerForScreenRec.get() == 0:
        timerOptions.configure(state = "disabled")
    else:
        timerOptions.configure(state = "normal")

def isTimer(event):
    manageIsTimer()

manageIsTimer()
timerCheck.bind('<Button-1>',isTimer)

frame_2 = ctk.CTkFrame(videoSettingsFrame,fg_color = "transparent")
frame_2.pack(pady = (5,10),padx = (10,0),anchor = "w",fill = "x")

isPauseHotkey = ctk.CTkCheckBox(frame_2,variable = isPauseHotkeyVar,cursor = "hand2",text = "",checkbox_height=30,checkbox_width = 30,hover_color="#3a3a3a",width = 30,height =30,border_width= 1.2,border_color = "#777777",corner_radius = 0)
isPauseHotkey.pack(side = "left",padx = (0,5))
isPauseHotkeyLabel = ctk.CTkLabel(frame_2,text = "Record/Stop Hotkey",font = ("Calibri Light",19),text_color = "#fafafa")
isPauseHotkeyLabel.pack(side = "left",padx = (0,10))

pauseHotkeyValue = ctk.CTkLabel(frame_2,text = "F12",text_color = "#fafafa",fg_color = "#444444",width = 70,height = 37)
pauseHotkeyValue.pack(side = "right",padx = (5,0))

def regIsRecordHotkey(*args):
    setSetting("isScreenRecordHotkey",isPauseHotkeyVar.get())
isPauseHotkeyVar.trace_add(['write'],regIsRecordHotkey)

specialHover(pauseHotkeyValue)
def focusPauseHotkey(event):
    pauseHotkeyValue.focus()
    def getKey(event):
        if isPauseHotkeyVar.get() == 1:
            pauseHotkeyValue.configure(text = event.keysym)
            setSetting("RecordKotkey",str(event.keysym))
    def loseFocus(event):
        pauseHotkeyValue.unbind("<Key>")
    pauseHotkeyValue.bind('<Key>',getKey)
    pauseHotkeyValue.bind('<FocusOut>',loseFocus)

pauseHotkeyValue.bind('<Button-1>',focusPauseHotkey)

def managePauseHotKey():
    if isPauseHotkeyVar.get() == 1:
        pauseHotkeyValue.configure(state = "disabled")
    else:
        pauseHotkeyValue.configure(state = "normal")

def isPauseHotkeyFunc(event):
    managePauseHotKey
isPauseHotkey.bind('<Button-1>',isPauseHotkeyFunc)

frame_3 = ctk.CTkFrame(videoSettingsFrame,fg_color = "transparent")
frame_3.pack(pady = (5,10),padx = (10,0),anchor = "w",fill = "x")
formatLabel = ctk.CTkLabel(frame_3,text = "Video format",font = ("Calibri Light",19),text_color = "#fafafa")
formatLabel.pack(side = "left",padx = (10,0))
formatOptions = ctk.CTkOptionMenu(frame_3,variable=videoFormat,dynamic_resizing=False,values = ['MP4','AVI'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
formatOptions.pack(anchor = "e",pady = (5,0),side = "right")
formatOptions.set(getSetting("videoFormat"))

def regVideoFormat(*args):
    setSetting("videoFormat",videoFormat.get())
videoFormat.trace_add(['write'],regVideoFormat)

frame_9 = ctk.CTkFrame(videoSettingsFrame,fg_color = "transparent")
frame_9.pack(pady = (5,10),padx = (10,0),anchor = "w",fill = "x")
frameRateLabel = ctk.CTkLabel(frame_9,text = "Frame Rate",font = ("Calibri Light",19),text_color = "#fafafa")
frameRateLabel.pack(side = "left",padx = (10,0))
frameRateOption = ctk.CTkOptionMenu(frame_9,variable = frameRateVar,dynamic_resizing=False,values = ['30 fps','50 fps','60 fps'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
frameRateOption.pack(anchor = "e",pady = (5,0),side = "right")
frameRateOption.set(getSetting("frameRate"))
def regFrameRate(*args):
    setSetting("frameRate",frameRateVar.get())
frameRateVar.trace_add(['write'],regFrameRate)



##############################################
# audio tab
################################################
audioSettingsFrame = ctk.CTkFrame(root,fg_color="transparent")
anticipateLabel = ctk.CTkLabel(audioSettingsFrame,image = anticipateImg,fg_color = "transparent",text = "")
anticipateLabel.pack(pady = (15,10))
label_3 = ctk.CTkLabel(audioSettingsFrame,text = "Feature not yet available.",font = ("Calibri Light",27),text_color = "#fafafa")
label_3.pack(pady = (10,10),padx = (60,10))
label_4 = ctk.CTkLabel(audioSettingsFrame,text = "Please anticipate while our team of experienced developers work on it.",font = ("Calibri Light",19),text_color = "#fafafa")
label_4.pack(pady = (15,10),padx = (60,10))



#############################################
#image tab
#############################################
imageSettingsFrame = ctk.CTkFrame(root,fg_color="transparent")
captureLabel = ctk.CTkLabel(imageSettingsFrame,text = "Capture",font = ("Calibri Light",20,"bold"),anchor = "w",text_color = "#ffffff",fg_color = "transparent")
captureLabel.pack(padx = (10,0),pady = (30,3),anchor = "w")
seperator_4 = seperator(imageSettingsFrame,orient = "horizontal",width = 400)
seperator_4.pack(pady = (5,10),padx = (10,0),fill = "x")
frame_4 = ctk.CTkFrame(imageSettingsFrame,fg_color = "transparent")
frame_4.pack(pady = (5,10),padx = (10,0),anchor = "w")

timerCheck_1 = ctk.CTkCheckBox(frame_4,variable = isTimerForScreenCapture,cursor = "hand2",text = "",checkbox_height=30,checkbox_width = 30,hover_color="#3a3a3a",width = 30,height =30,border_width= 1.2,border_color = "#777777",corner_radius = 0)
timerCheck_1.pack(side = "left",padx = (0,5))
imageTimerLabel = ctk.CTkLabel(frame_4,text = "Place timer for screen capture ?",font = ("Calibri Light",19),text_color = "#fafafa")
imageTimerLabel.pack(side = "left",padx = (0,10))
timerOptions_1 = ctk.CTkOptionMenu(frame_4,variable = timeForScreenCapture,dynamic_resizing=False,values = ['3 seconds','5 seconds','10 seconds'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
timerOptions_1.pack(anchor = "e",pady = (5,0),side = "right")
timerOptions_1.set(getSetting("timeForScreenCapture"))

def regIsTimerForScreenCapture(*args):
    val = ""
    if isTimerForScreenCapture.get() == 0:
        val = "False"
    else:
        val = "True"
    setSetting("isTimerForScreenCapture",val)
isTimerForScreenCapture.trace_add(['write'],regIsTimerForScreenCapture)


def regTimerForScreenCapture(*args):
    setSetting("timeForScreenCapture",timeForScreenCapture.get())
timeForScreenCapture.trace_add(['write'],regTimerForScreenCapture)


def manageIsTimerForScreenCapture():
    if isTimerForScreenCapture.get() == 1:
        timerOptions_1.configure(state = "normal")
    else:
        timerOptions_1.configure(state = "disabled")

def isTimerEnabled(event):
    manageIsTimerForScreenCapture()
manageIsTimerForScreenCapture()
timerCheck_1.bind('<Button-1>',isTimerEnabled)

if getSetting("isTimerForScreenCapture") == "False":
    isTimerForScreenCapture.set(0)
else:
    isTimerForScreenCapture.set(1)
manageIsTimerForScreenCapture()

def regTimerForScreenCapture(*args):
    setSetting("timeForScreenCapture",timeForScreenCapture.get())
timeForScreenCapture.trace_add(['write'],regTimerForScreenCapture)
def regIsTimerForScreenCapture(*args):
    setSetting("isTimerForScreenCapture",isTimerForScreenCapture.get())
isTimerForScreenCapture.trace_add(['write'],regIsTimerForScreenCapture)

frame_5 = ctk.CTkFrame(imageSettingsFrame,fg_color = "transparent")
frame_5.pack(pady = (5,10),padx = (10,0),anchor = "w",fill = "x")

isScreenCapturekey = ctk.CTkCheckBox(frame_5,variable = isScreenCapturekeyVar,cursor = "hand2",text = "",checkbox_height=30,checkbox_width = 30,hover_color="#3a3a3a",width = 30,height =30,border_width= 1.2,border_color = "#777777",corner_radius = 0)
isScreenCapturekey.pack(side = "left",padx = (0,5))
isScreenCapturekeyLabel = ctk.CTkLabel(frame_5,text = "Screen capture Hotkey",font = ("Calibri Light",19),text_color = "#fafafa")
isScreenCapturekeyLabel.pack(side = "left",padx = (0,10))

ScreenCapturekeyValue = ctk.CTkLabel(frame_5,text = "F12",text_color = "#fafafa",fg_color = "#444444",width = 70,height = 37)
ScreenCapturekeyValue.pack(side = "right",padx = (5,0))

def regIsScreenCaptureKey(*args):
    setSetting("isScreenCaptureHotkey",isScreenCapturekeyVar.get())
isScreenCapturekeyVar.trace_add(['write'],regIsScreenCaptureKey)

specialHover(ScreenCapturekeyValue)
def focusScreenCapturekey(event):
    ScreenCapturekeyValue.focus()
    def getKey(event):
        if isScreenCapturekeyVar.get() == 1:
            ScreenCapturekeyValue.configure(text = event.keysym)
            setSetting("screenCaptureHotkey",str(event.keysym))
    def loseFocus(event):
        ScreenCapturekeyValue.unbind("<Key>")
    ScreenCapturekeyValue.bind('<Key>',getKey)
    ScreenCapturekeyValue.bind('<FocusOut>',loseFocus)

ScreenCapturekeyValue.bind('<Button-1>',focusScreenCapturekey)

def manageScreenCaptureKey():
    if isScreenCapturekeyVar.get() == 1:
        ScreenCapturekeyValue.configure(state = "disabled")
    else:
        ScreenCapturekeyValue.configure(state = "normal")

def isScreenCapturekeyFunc(event):
    manageScreenCaptureKey()
isScreenCapturekey.bind('<Button-1>',isScreenCapturekeyFunc)


frame_6 = ctk.CTkFrame(imageSettingsFrame,fg_color = "transparent")
frame_6.pack(pady = (5,10),padx = (10,0),anchor = "w",fill = "x")
formatLabel_1 = ctk.CTkLabel(frame_6,text = "Image format",font = ("Calibri Light",19),text_color = "#fafafa")
formatLabel_1.pack(side = "left",padx = (10,0))
formatOptions_1 = ctk.CTkOptionMenu(frame_6,variable=imageFormat,dynamic_resizing=False,values = ['JPG','PNG','BMP'],anchor="w",fg_color = "#555555",button_color="#555555",button_hover_color="#666666")
formatOptions_1.pack(anchor = "e",pady = (5,0),side = "right")
formatOptions_1.set(getSetting('imageFormat'))

def checkImageFormat(*args):
    setSetting("imageFormat",imageFormat.get())
imageFormat.trace_add(['write'],checkImageFormat)



#############################################
#info tab
#############################################
infoFrame = ctk.CTkFrame(root,fg_color="transparent")
frame_7 = ctk.CTkFrame(infoFrame,fg_color = "transparent")
frame_7.pack(pady = (30,10),padx = (40,10),fill = "y")
gemini_icon = ctk.CTkLabel(frame_7,image = appIcon,fg_color = "transparent",text = "")
gemini_icon.pack(side = "left",padx = (20,10))
gemini_label = ctk.CTkLabel(frame_7,text = "Socket",text_color = "#00ccff",font = ("Chiller",100))
gemini_label.pack(side = "left",padx = (10,0))
gemini_version = ctk.CTkLabel(frame_7,text = "V 1.0.0",text_color = "#00ccff",font = ("Chiller",20),anchor = "sw")
gemini_version.pack(side = "left",padx = (10,0),pady = (36,0))

frame_8 = ctk.CTkFrame(infoFrame,fg_color = "transparent")
frame_8.pack(pady = (10,80))
gemini_label_2 = ctk.CTkLabel(frame_8,image = companyIcon,fg_color = "transparent",text = "")
gemini_label_2.pack(side = "left",padx = (10,0),pady = (20,0))
gemini_version_2 = ctk.CTkLabel(frame_8,text = "©2024 Gemini",text_color = "#00ccff",font = ("Chiller",26),anchor = "sw")
gemini_version_2.pack(side = "left",padx = (10,0),pady = (36,0))



allSideFrameFrames = [homeFrame,settingsFrame,videoSettingsFrame,audioSettingsFrame,imageSettingsFrame,infoFrame]
def rootLeftClickFunction(event):
    currentFile.isFocused = False
root.bind('<Button-1>',rootLeftClickFunction)
root.mainloop()
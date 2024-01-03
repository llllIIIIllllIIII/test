import sys
import datetime
from ppadb.client import Client
import cv2
import keyboard
import numpy
from PIL import Image
import pytesseract
import time
import os
import threading
from save import save
# import difflib

#
# C:\Program Files\Tesseract-OCR\tesseract.exe
# X:\Tesseract-OCR\tesseract.exe
try:
    limit_time = datetime.date(2022,1,16)
    path = "r'X:\Tesseract-OCR\tesseract.exe'"
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    adb = Client(host="127.0.0.1", port=5037)
    devices = adb.devices()
    device = devices[0]
    pause = False
    db = save()
except Exception as e:
    print("裝置連線發生狀況 可能的解決方法可參照DC群內使用前注意事項")
    os.system(pause)
def main():
    # id_img = screenshot()
    # idimg = id_img[720:765,385:605]
    # cv2.imshow('img',idimg)
    # cv2.waitKey(0)
    # print(resourceOcr(idimg,False))
    # print(difflib.SequenceMatcher(None,'IQNMS6843',resourceOcr(idimg,False)).quick_ratio())
    # os.system("pause")
    # # 0.8571428571428571
    
    t = threading.Thread(target=Mpause)
    t.start()
    try:
        print("腳本執行中 若要暫停請按**Scroll Lock**")
        while True:
            global pause
            
            while pause == False:
                check_time()
                # cls()
                time.sleep(0.2)
                img = screenshot()
                imgname = img[150:200, 1440:1800]
                # imgname = img[790:870, 1440:1800]
                # cv2.imshow('img',imgname)
                # cv2.waitKey(0)
                imglimit = img[25:80, 1050:1145]
                limittext = resourceOcr(imglimit, True)
                limittext = "".join(limittext.split())
                try:
                    limittext = int(limittext)
                except Exception as e:
                    limittext = 1
                # print(limittext)
                nametext = resourceOcr(imgname, False)
                nametext = "".join(nametext.split())
                # print(nametext)
                # print(db.limit(db, nametext))

                if db.is_metirial(nametext):
                    if nametext == "BiscuitFlour" or nametext == "Jellyberry":
                        if limittext < db.limit(nametext):
                            device.shell('input touchscreen swipe 1600 670 1600 670 2000')
                    elif limittext < db.limit(nametext):
                        device.shell('input touchscreen swipe 1600 350 1600 350 2000')

                device.shell("input touchscreen tap 1020 530")
            cls()
            print("已暫停")
            print("按 F12以重新開始，F11來查看或修改數量上限")
            # keyboard.add_hotkey('F11',adjust)
            keyboard.wait("F12")
            cls()
            print("重新開始")
            print("若要暫停請按Scroll Lock")
            pause = False
    except Exception as e:
        print(e)
        os.system("pause")


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def Mpause():
    global pause
    while True:
        keyboard.wait("scroll lock")
        print('scroll lock pressed')
        pause = True


def resourceOcr(img, isdigit:bool):
    threshold = 180
    _, img_binarized = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    pil_img = Image.fromarray(img_binarized)
    if isdigit == True:
        text = pytesseract.image_to_string(
            pil_img, lang="eng", config="--psm 10 -c tessedit_char_whitelist=0123456789"
        )
    else:
        text = pytesseract.image_to_string(pil_img, lang="eng")
    return text


def screenshot():
    result = device.screencap()
    img = numpy.array(result)
    imga = cv2.imdecode(img, cv2.COLOR_RGBA2BGR)
    img = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
    return img




def adjust():
    df = db.list_all()
    cls()
    keyboard.remove_hotkey('F11')   
    while True:
        try:
            cls()
            print(df)
            index = int(input("輸入想修改材料數量左方的數字(0-61): "))
        except:
            print("輸入錯誤 輸入內容限定為(0-61)的數字")
            ans = str(input('是否再輸入一次?(Y/N) :') or 'N')
            if ans.upper() != "Y":
                break
        if 0<= index <= 61:
            name =  df.iloc[index, df.columns.get_loc('名稱')]
            while True:
                print("要修改的素材為: "+name)
                new_limit = input("請輸入修改後的數量上限:")
                if new_limit.isdigit():
                    int(new_limit)
                    break
                else:
                    print("請輸入數字")
            db.update(db,name,new_limit)
            cls()
            print("修改完成，"+name+"數量調整為"+str(new_limit))
            os.system("pause")
            break
        else:
            print("輸入錯誤 輸入內容限定為(0-61)的數字")
            ans = str(input('是否再輸入一次?(Y/N) :') or 'N')
            if ans.upper() != "Y":
                break
            
    cls()       
    print("請按F12繼續使用腳本")       
    

def check_time():
    global limit_time
    if datetime.date.today() >= limit_time:
        sys.exit("腳本已過期")

if __name__ == "__main__":
    main()

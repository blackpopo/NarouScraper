from pywinauto import Desktop, mouse, keyboard
from subprocess import Popen
from time import sleep
import pywinauto
class Parameter():
    def __init__(self, x_position,  start_value, highest_value, lowest_value, start_position, highest_position = 790, lowest_position = 955, x_scale=1.0, y_scale=1.0):
        self.x_position = int(x_position * x_scale)
        self.start_position = int(start_position * y_scale)
        self.highest_position = int(highest_position * y_scale)
        self.lowest_position = int(lowest_position * y_scale)
        self.start_value = start_value
        self.highest_value = highest_value
        self.lowest_value = lowest_value

    def set_value(self, value):
        assert self.lowest_value <= value <= self.highest_value
        if  value >= self.start_value:
            target_y = - ((value - self.start_value) / (self.highest_value - self.lowest_value)) * ( - self.highest_position + self.start_position) + self.start_position
        else:
            target_y = ((self.start_value - value)/ (self.start_value - self.lowest_value)) * (- self.start_position + self.lowest_position) + self.start_position
        target_position = (self.x_position, int(target_y))
        mouse.press(coords=(self.x_position, self.start_position))
        mouse.release(coords=target_position)

class AutoYukarin():
    def __init__(self,  scale='1920x1080'):
        self.initialize()
        # self.save_initilalize()
        self.scale = scale.split('x')
        self.x_scale = float(self.scale[0]) / 1920
        self.y_scale = float(self.scale[1]) / 1080
        self.volume = Parameter(x_position = 275, start_value=1.0, highest_value=2.0, lowest_value=0.0, start_position=875)
        self.speed = Parameter(x_position = 350, start_value=1.0, highest_value=4.0, lowest_value=0.5, start_position=930)
        self.height = Parameter(x_position = 425, start_value=1.0, highest_value=2.0, lowest_value=0.5, start_position=900)
        self.intonation = Parameter(x_position = 500, start_value=1.0, highest_value=2.0, lowest_value=0.0, start_position=875)
        self.joy = Parameter(x_position = 730, start_value=0.0, highest_value=1.0, lowest_value=0.0, start_position=955)
        self.anger = Parameter(x_position = 805, start_value=0.0, highest_value=1.0, lowest_value=0.0, start_position=955)
        self.sad = Parameter(x_position = 880, start_value=0.0, highest_value=1.0, lowest_value=0.0, start_position=955)


    def initialize(self):
        # Popen("C:\Program Files (x86)\AHS\VOICEROID2\VoiceroidEditor.exe")
        self.yukarin_window = Desktop(backend='uia')['VOICEROID2*']
        # self.yukarin_window['最大化'].click()

    def save_initilalize(self):
        self.parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()

        # voiceroidを捜索する
        voiceroid2 = self.search_child_byname("VOICEROID2", self.parentUIAElement)
        # *がついている場合
        if voiceroid2 == False:
            voiceroid2 = self.search_child_byname("VOICEROID2*", self.parentUIAElement)

        # ここから変更
        # テキスト要素のElementInfoを取得
        TextEditViewEle = self.search_child_byclassname("TextEditView", voiceroid2)
        # ボタン取得
        buttonsEle = self.search_child_byclassname("Button", TextEditViewEle, target_all=True)
        # 保存ボタンを探す
        playButtonEle = ""
        for buttonEle in buttonsEle:
            # テキストブロックを捜索
            textBlockEle = self.search_child_byclassname("TextBlock", buttonEle)
            if textBlockEle.name == "音声保存":
                playButtonEle = buttonEle
                break

        # ボタンコントロール取得
        self.playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(playButtonEle)

    def init_param(self, init_left=175, init_right=1000):
        mouse.click(coords=(int(self.x_scale * init_left), int(self.x_scale * init_right)))

    def set_param(self, volume=1.0, speed=1.0,  height=1.0, intonation=1.0, joy=0.0, anger=0.0, sad=0.0):
        self.init_param()
        if volume != 1.0: self.volume.set_value(volume) ; sleep(0.3)
        if speed != 1.0: self.speed.set_value(speed); sleep(0.3)
        if height != 1.0: self.height.set_value(height); sleep(0.3)
        if intonation != 1.0: self.intonation.set_value(intonation); sleep(0.3)
        if joy != 0.0: self.joy.set_value(joy); sleep(0.3)
        if anger != 0.0: self.anger.set_value(anger); sleep(0.3)
        if sad != 0.0: self.sad.set_value(sad); sleep(0.3)

    def set_text(self, text):
        self.yukarin_window['Edit'].set_edit_text(text)
        sleep(0.5)
        mouse.click(coords=(int(self.x_scale * 900), int(self.y_scale * 450)))
        keyboard.send_keys(' ^a ^c')

    def playback(self):
        self.yukarin_window['Button'].click()

    def print_identifers(self, filename=None):
        self.yukarin_window.print_control_identifiers(filename=filename)

    def save_file(self, save_file_name):
        # self.playButtonControl.click() #保存のところを押す。
        # sleep(0.5)
        # self.yukarin_window['OKButton'].click()
        # self.yukarin_window['ファイル名:Edit'].set_edit_text(save_file_name + '.wav')
        # self.yukarin_window['保存(S)'].click()
        # self.yukarin_window['OK'].click()
        mouse.click(coords=(int(self.x_scale * 25), int(self.y_scale * 25))) #File(F)
        mouse.click(coords=(int(self.x_scale * 135), int(self.y_scale * 150))) #保存
        sleep(1.0)
        mouse.click(coords=(int(self.x_scale * 1070), int(self.y_scale * 730))) #OK
        sleep(0.5)
        keyboard.send_keys('^v')
        sleep(1.0)
        mouse.click(coords=(int(self.x_scale * 1200), int(self.y_scale * 820)))#保存(S)
        sleep(1.5)
        mouse.click(coords=(int(self.x_scale * 1050), int(self.y_scale * 600)))
        sleep(1.0)

    def search_child_byclassname(self, class_name, uiaElementInfo, target_all = False):
        target = []
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():

            # ClassNameの一致確認
            if childElement.class_name == class_name:
                if target_all == False:
                    return childElement
                else:
                    target.append(childElement)
        if target_all == False:
            # 無かったらFalse
            return False
        else:
            return target

    def search_child_byname(self, name, uiaElementInfo):
        # 全ての子要素検索
        for childElement in uiaElementInfo.children():

            # Nameの一致確認
            if childElement.name == name:
                return childElement
        # 無かったらFalse
        return False

    def yukarin(self, text="こんにちは。", volume=1.0, speed=1.0,  height=1.0, intonation=1.0, joy=0.0, anger=0.0, sad=0.0, is_set_param = True):
        if is_set_param: self.set_param( volume=volume, speed=speed,  height=height, intonation=intonation, joy=joy, anger=anger, sad=sad)
        self.set_text(text)
        self.save_file(text)

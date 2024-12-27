from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.selectioncontrol import MDCheckbox


import io
#import chardet
import os
import codecs
import re
#import keyboard
import time
#from pynput.keyboard import Key, Listener

#Имя файла исходящего текста
filename = 'voyna-i-mir-tom-1.txt'
#Имя файла для сохранения
filesave = 'out.txt'

# #Имя файла исходящего текста
# filename = 'text_eng.txt'
# #Имя файла для сохранения
# filesave = 'out_eng.txt'


#Данные файла
data = ''

#Длина вывода строки
length_line = 80

text="Вы так красноречивы. Вы дадите мне чаю?– Сейчас."

lineToSearch=''

error=0
error_index = []

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        pass

    def on_enter(self):
        global text
        #print(self.ids)
        try:            
            self.ids.Label_out.text = text
        except:
            print("не сработало")

    def on_start(self):
        print("работает")

    def oNfocus(instance, value):

        print(value.focus)
        if value.focus:
            print('User focused')
            #print(value.parent.children[1].text)
            start_key_radar(value)
            
        else:
            print('User defocused')
            stop_key_radar(value)

    def render(self, _):
        global text,error

        #print(text)
        try:
            inputext=self.ids.inputText.text
            self.ids.Label_out.text = lastsybol(text,inputext)
            #print(lastsybol(text,inputext))
        except:
            inputext=''
        #print(inputext[-1]+' '+str(len(inputext)))
        lastsybol(text,inputext)
        error = search_error(inputext,text)
        #print("ошибки- "+str(error))
        
        if error==1:
            self.ids.inputText.error = True
        else:
            self.ids.inputText.error = False


        if inputext!='':
            if len(inputext)<=len(text)-1 and error >= 0:

                key_visard(self,text[len(inputext)])

                if text[len(inputext)-1] != inputext[-1]:
                    #print("ошибка "+text[len(inputext)-1]+' '+inputext[-1]) 
                    #self.ids.inputText.error = True   
                    pass                
                else:
                    #print(str(len(inputext))+' '+str(len(text)) )
                    #print(text[len(inputext)])
                    pass
            elif error==0:
                save(text)
                findline2(text)
                self.ids.Label_out.text = text
                self.ids.inputText.text=''

            
        #print()
        #print(text[len(inputext)])
        
        #self.ids.keyVisard.canvas.clear()

sm = ScreenManager()
sm.add_widget(MainScreen(name='Main'))


#Загружаем фаил
def loadfile(file):
    # bytes = min(32, os.path.getsize(file))
    # raw = open(filename, 'rb').read(bytes)

    # if raw.startswith(codecs.BOM_UTF8):
    #     encoding = 'utf-8-sig'
    # else:
    #     result = chardet.detect(raw)
    #     encoding = result['encoding']

    # infile = io.open(file, 'r', encoding=encoding)
    # print(infile)
    # data_out = infile.read()
    # infile.close()

    data_out = open(file, 'r').read()
    print(data_out)

    return data_out

# Поиск строки
def findline():
    global data,length_line,text,lineToSearch
    outdata=[]
    serch = lineToSearch
    #serch = "поместья, de la famille Buonaparte. Non, "
    #print(len(data))
    
    
    for x in range(0,len(data),length_line):
        line = data[x:x+length_line].replace("\n","")
        outdata.append(line)

    for i in range(len(outdata)): 

        if serch != '':
            index = outdata[i].find(serch)
            if index != -1:
                print(str(i+1) + " "+outdata[i+1])
                #text = re.sub(r"[#%!@*]", "", outdata[i+1])
                text = outdata[i+1]
                break
        else:
            text = outdata[0]
            break
            
    #print(outdata[75])

def findline2(serch):
    global data,length_line,text
    outdata=[]
    
    for x in range(0,len(data),length_line):
        line = data[x:x+length_line].replace("\n","")
        outdata.append(line)

    for i in range(len(outdata)): 

        index = outdata[i].find(serch)
        if index != -1:
            print(str(i+1) + " "+outdata[i+1])
            #text = outdata[i+1]
            #text_b = outdata[i+1]
            text = outdata[i+1]
            break

def last_line(mydata):
    #print('последняя строка'+mydata)
    #print(mydata[12])
    outdata = mydata.split('\n')
    #print(outdata[-1])
    try:
        if outdata[-1]!= '':
            return outdata[-1]
        else:
            return outdata[-2]
    except:
        return ''

# Подсветка символов и ошибок
def lastsybol(text,inputext):
    global error_index
    out = [x for x in text]
    
    out.insert(0, '[color=999]')
    out.insert(len(inputext)+1, '[/color][u][color=333fff]')
    out.insert(len(inputext)+3, '[/color][/u]')

    #print(error_index)
    if bool(error_index):
        for i in range(len(error_index)):
            out.insert(error_index[i]+1, '[color=ff0000]')
            out.insert(error_index[i]+3, '[/color]')
            #print("+")

    return "".join(out)

#Проверка на ошибки
def search_error(inputext,text):
    global error,error_index
    o=0
    if inputext != '':
        # text[0:len(inputext)]
        for i in range(len(inputext)):
            if text[i] != inputext[i]:
                error=1
                o=1

                if error_index.count(i) == 0:
                    error_index.append(i)
                
                #print('есть ошибки- '+text[i]+' '+inputext[i])
            else :
                #print('нет ошибки')
                pass
        if o==0:
            error=0
            error_index.clear()

    return error

#Запускаем отслеживание клавиш
def start_key_radar(value):
    #print('Запускаем')
    Clock.schedule_interval(value.parent.parent.render, 0.1)
    
#Запускаем отслеживание клавиш
def stop_key_radar(value):
    print('Остонавливаем')
    Clock.unschedule(value.parent.parent.render)

# Сохраняем введенную строку
def save(text):
    text_out = open(filesave, 'a')
    text_out.write(text + '\n')
    text_out.close()

# Клавиатура
def key_visard(self,key):
    #key = "k"
    #print(keyz)
    #print("work")

    key_lat = [[None,-50,-50],

                # Латинская
               ['~',25,215],['!',77,215],['@',129,215],['#',181,215],
               ['$',233,215],['%',285,215],['^',337,215],['&',389,215],
               ['*',441,215],['(',493,215],[')',545,215],['_',597,215],
               ['+',649,215],

               ['`',25,215],['1',77,215],['2',129,215],['3',181,215],
               ['4',233,215],['5',285,215],['6',337,215],['7',389,215],
               ['8',441,215],['9',493,215],['0',545,215],['-',597,215],
               ['=',649,215],

               ['<-',701,215],
               ['–',597,215],

               
               ['q',103,167],['w',155,167],['e',207,167],['r',259,167],
               ['t',311,167],['y',363,167],['u',415,167],['i',467,167],
               ['o',519,167],['p',571,167],['[',623,167],[']',675,167],

               ['a',115,119],['s',167,119],['d',219,119],['f',271,119],
               ['g',323,119],['h',375,119],['j',427,119],['k',479,119],
               ['l',531,119],[';',583,119],["'",635,119],

               ['z',142,72],['x',194,72],['c',246,72],['v',298,72],
               ['b',350,72],['n',402,72],['m',453,72],[',',506,72],
               ['.',558,72],['/',610,72],
                ]


    key_cir=[[None,-50,-50],

               # Кирилица
               ['[',25,215],['!',77,215],['"',129,215],['№',181,215],
               ['%',233,215],[':',285,215],[',',337,215],['.',389,215],
               [';',441,215],['(',493,215],[')',545,215],['_',597,215],
               ['+',649,215],

               [']',25,215],['1',77,215],['2',129,215],['3',181,215],
               ['4',233,215],['5',285,215],['6',337,215],['7',389,215],
               ['8',441,215],['9',493,215],['0',545,215],['-',597,215],
               ['=',649,215],

               ['<-',701,215],
               ['–',597,215],

               ['й',103,167],['ц',155,167],['у',207,167],['к',259,167],
               ['е',311,167],['н',363,167],['г',415,167],['ш',467,167],
               ['щ',519,167],['з',571,167],['х',623,167],['ъ',675,167],

               ['ф',115,119],['ы',167,119],['в',219,119],['а',271,119],
               ['п',323,119],['р',375,119],['о',427,119],['л',479,119],
               ['д',531,119],['ж',583,119],["э",635,119],

               ['я',142,72],['ч',194,72],['с',246,72],['м',298,72],
               ['и',350,72],['т',402,72],['ь',453,72],['б',506,72],
               ['ю',558,72],['/',610,72],

            ]

    #print(key_language())

    if key_language() == 'Eng':
        key_out =  key_lat       
        self.ids.keyVisard.canvas.children[2].source = 'key_en.jpg'
    else:  
        key_out =  key_cir  
        self.ids.keyVisard.canvas.children[2].source = 'key_ru.jpg'

    #self.ids.keyVisard.canvas.clear()
    #print(self.ids.keyVisard.canvas.children[5].pos)
    
    key_x = None
    key_y = None

    for x in range(len(key_out)):
        if key.lower() == key_out[x][0]:
            key_x = key_out[x][1]   
            key_y = key_out[x][2]
    
    if key_x == None:
        key_x = -50
        key_y = -50

    self.ids.keyVisard.canvas.children[5].pos = (key_x , key_y)

    if key == ' ' or key == ' ':
        self.ids.keyVisard.canvas.children[8].pos = (216,25)
        #print(self.ids.keyVisard.canvas.children)
    else:
        self.ids.keyVisard.canvas.children[8].pos = (-50,-50)

    if key.isupper() or not set("_+)(*^?!").isdisjoint(key):
        self.ids.keyVisard.canvas.children[10].pos = (26,72)
        self.ids.keyVisard.canvas.children[12].pos = (660,72)
    else:
        self.ids.keyVisard.canvas.children[10].pos = (-50,-50)
        self.ids.keyVisard.canvas.children[12].pos = (-50,-50)

    if key.isupper() or not set("_+)(*^?!.,").isdisjoint(key) and key_language() == 'Rus':
        self.ids.keyVisard.canvas.children[10].pos = (26,72)
        self.ids.keyVisard.canvas.children[12].pos = (660,72)
    else:
        self.ids.keyVisard.canvas.children[10].pos = (-50,-50)
        self.ids.keyVisard.canvas.children[12].pos = (-50,-50)

    if not set("– ").isdisjoint(key):
        self.ids.keyVisard.canvas.children[14].pos = (537,25)
    else:
        self.ids.keyVisard.canvas.children[14].pos = (-50,-50)
        
# Проверяем раскладку
def key_language():
    command = 'defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources'
    line = []
    outdata = []
    out = os.popen(command).read()
    


    for x in range(0,len(out),30):
        line = out[x:x+30].replace("\n","")
        outdata.append(line)


    index = outdata[-1].find('U.S.')

    #print(outdata)

    if index>-1:
        
        return "Eng"
    else:
        
        return "Rus"

# Основа приложения
class MainApp(MDApp):
    def build(self):        
        buildKV = Builder.load_file("template/main.kv")
        sm.switch_to(MainScreen())
        return sm

    def on_start(self):    	
        '''Creates a list of cards.'''
        #print(LoadScreen().ids)
        #print("работает1")
        global data,lineToSearch

        data = loadfile(filename)
        lineToSearch = last_line(loadfile(filesave))
        findline()
        #pass

# Run the App 
if __name__ == "__main__": 
    MainApp().run() 




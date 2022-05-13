from PyQt5 import QtCore, QtGui, QtWidgets






#IDEI VIITOR
#scraping mai bun, sa ia toate rezultatele nu doar 10 cate ia acum - sau un nr de rezultate, 50
#functie de cut al clipului - sa fac cumva sa il decarc in tempfile apoi sa fie cut
#functie de descarcare playlisturi - trebuie sa fac GUI-ul mai frumos intai 
#lucrat la layout-uri. sa vina elementele mai bine. asta in alt program, sa semene cu mediahuman 
#https://github.com/kokoko3k/xt7-player-mpv -- imi place cum arata si asta
#facut programu executabil .exe
#functionalitate mai avansata de download - selectare calitate/format/etc 









import mpv
import requests
from bs4 import BeautifulSoup
import re
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import locale
import subprocess
from PyQt5.QtGui import QIcon, QPixmap
from urllib.request import urlopen
import base64
import tempfile
import os
from yt_dlp import YoutubeDL

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1104, 431)
        locale.setlocale(locale.LC_NUMERIC,"C")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textCautare = QtWidgets.QTextEdit(self.centralwidget)
        self.textCautare.setGeometry(QtCore.QRect(230, 20, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textCautare.setFont(font)
        self.textCautare.setObjectName("textCautare")
        self.labelCautare = QtWidgets.QLabel(self.centralwidget)
        self.labelCautare.setGeometry(QtCore.QRect(10, 30, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelActiune = QtWidgets.QLabel(self.centralwidget)
        self.labelActiune.setGeometry(QtCore.QRect(560, 20, 310, 41))
        self.labelActiune.setObjectName("labelActiune")
        self.labelActiune.setFont(font)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelCautare.setFont(font)
        self.labelCautare.setObjectName("labelCautare")
        self.pushButtonCautare = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCautare.setGeometry(QtCore.QRect(490, 20, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCautare.setFont(font)
        self.pushButtonCautare.setObjectName("pushButtonCautare")
        self.scrollAreaClipuri = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaClipuri.setGeometry(QtCore.QRect(10, 70, 531, 311))
        self.scrollAreaClipuri.setWidgetResizable(True)
        self.scrollAreaClipuri.setObjectName("scrollAreaClipuri")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 525, 305))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaClipuri.setWidget(self.scrollAreaWidgetContents)
        self.widgetVideo = QtWidgets.QWidget(self.centralwidget)
        self.widgetVideo.setGeometry(QtCore.QRect(550, 70, 531, 311))
        self.widgetVideo.setObjectName("widgetVideo")
        self.pushButtonDescarca = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDescarca.setGeometry(QtCore.QRect(979, 20, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        
        self.pushButtonDescarca.setFont(font)
        self.pushButtonDescarca.setObjectName("pushButtonDescarca")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1104, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #####################################
        #Butoane
        #####################################    
        self.pushButtonCautare.clicked.connect(self.clickCautare)
        self.pushButtonDescarca.clicked.connect(self.clickDescarcaVideo)
        #####################################
        #Pentru MPV
        #https://github.com/jaseg/python-mpv
        #####################################    
        self.container = self.widgetVideo
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.player = mpv.MPV(wid=str(int(self.container.winId())),
                vo='x11', # You may not need this
                log_handler=print,
                loglevel='debug',
                input_default_bindings=True,
                input_vo_keyboard=True,
                osc=True
                )
        #####################################


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelCautare.setText(_translate("MainWindow", "Cautati clipuri pe YouTube:"))
        self.pushButtonCautare.setText(_translate("MainWindow", "OK"))
        self.pushButtonDescarca.setText(_translate("MainWindow", "Descarca"))
        self.labelActiune.setText(_translate("MainWindow", "Actiune:"))

    ####################################
    #scrape
    def scrapeCautare(self, cautare):
        #impartim cautarea pe cuvinte
        #punem + intre cuvinte pentru query-ul youtube
        query = '+'.join(str(x) for x in cautare)

        response = requests.get("https://www.youtube.com/results?search_query=" + query + "&sp=EgIQAQ%253D%253D").text
        #n-o sa vreau sa arate si canalele
        #"&sp=EgIQAQ%253D%253D" il adaug ca sa imi dea doar clipuri

        soup = BeautifulSoup(response, 'lxml')
        #Cu asta scriem continutul soup-ului intr-un fisier
        #with open("script.txt", "w", encoding="utf-8") as output:
            #output.write(soup.prettify())

        #Informatiile de care avem nevoie se gasesc in variabila videoRenderer
        #Informatiile din videoRenderer sunt inauntrul unui String JSON 
        #Avem nevoie sa gasim tag-ul HTML in care se afla variabila asta. 
        #Se afla inauntrul al 35-lea tag <script> 
        #au mai modificat intre timp pentru ca in trecut era 33)
        script = soup.find_all("script")[34]
        #print(script)

        #Ne trebuie doar String-ul JSON din acest script (tot ce este dupa variabila ytInitialData)
        #https://stackoverflow.com/questions/47515137/extracting-data-from-javascript-var-inside-script-with-python
        json_text = re.search('var ytInitialData =(.+)[,;]{1}', str(script)).group(1)
        #Putem scrie aici continutul json_text variabilei String JSON
        #with open("script.txt", "w", encoding="utf-8") as output:
            #output.write(json_text)
        #aici se poate vizualiza String-ul JSON in JSON data care e usor de citit
        #https://jsonformatter.curiousconcept.com/# - copiem json_text din fisier si punem acolo

        #Convertim String-ul JSON in JSON data penru a fi mai usor de gasit informatia
        json_data = json.loads(json_text)

        #tot ce avem nevoie (videoID, thumbnail, titlu, etc) se afla in variablila videoRenderer.
        #in JSON data, putem vedea ca variabila asta se afla inauntrul cheii  "contents"
        #accesam in jos de la contents pana la ce ne trebuie
        content = (
            json_data
            ['contents']['twoColumnSearchResultsRenderer']
            ['primaryContents']['sectionListRenderer']
            ['contents'][0]['itemSectionRenderer']['contents']
        )

        return content
    #####################################
   
    #####################################
    #rezolvarePoza
    def rezolvarePoza(self, url):
        image = base64.b64encode(urlopen(url).read()).decode("ascii")
        imgdata = base64.b64decode(image)
        with tempfile.NamedTemporaryFile(mode="wb") as imagine:
            imagine.write(imgdata)
            pixmap = QPixmap(imagine.name)
            smaller_pixmap = pixmap.scaled(170, 100, Qt.KeepAspectRatio, Qt.FastTransformation)
            return smaller_pixmap
            #fila temporara se distruge dupa ce iesim din clauza "with"
    #####################################
    
    #####################################
    #playVideo
    def playVideo(self, v):
        self.labelActiune.setText("Actiune: Incarcare videoclip...")
        self.labelActiune.repaint()
        self.video_curent = "https://www.youtube.com/watch?v=" + v
        self.player.play(self.video_curent)
    #####################################    

    #####################################
    #adaugareContent
    def adaugareContent(self, content):
        self.labelActiune.setText("Actiune: Adaugare clipuri...")
        self.labelActiune.repaint()
        top_widget = QtWidgets.QWidget()
        top_vertical_layout = QtWidgets.QVBoxLayout()
        titlu = ""

        #Facem PARSE la data
        #accesam lista content 
        for data in content:
            for key, value in data.items():
                #group box, adaugat la vertical layout
                group_box = QtWidgets.QGroupBox()
                group_box.setCheckable(True)
                group_box.setGeometry(QtCore.QRect(10, 20, 521, 141))
                top_vertical_layout.addWidget(group_box)
                #label imagine
                label_image = QtWidgets.QLabel()
                #buton play
                push_button = QtWidgets.QPushButton()
                push_button.setFixedSize(50, 50)
                push_button.setText("▶︎")
                font = QtGui.QFont()
                font.setPointSize(20)
                push_button.setFont(font)
                #horizontal layout al group box
                groupbox_horizontal_layout = QtWidgets.QHBoxLayout()
                groupbox_horizontal_layout.addWidget(label_image)
                groupbox_horizontal_layout.addWidget(push_button)
                #Elementele nu vor avea spatii mari intre ele cu urmatoarele doua linii
                groupbox_horizontal_layout.setSpacing(10) 
                groupbox_horizontal_layout.addStretch(1) 
                #vertical layout
                group_box.setLayout(groupbox_horizontal_layout)
                top_vertical_layout.addLayout(groupbox_horizontal_layout) 

                for k, v in value.items():
                    #print(f"{k} : {v}") - cheie si valoare ex: videoID : id-ul videoului
                    #extragere videoID, thumbnail la fiecare iteratie se adauga un clip nou
                    if k == "title" and "runs" in v or k == "thumbnail" and "thumbnails" in v or k == "longBylineText" and "runs" in v or k == "videoId" and len(v) == 11: 
                        ####################################                            
                        #Titlul clipului si autorul 
                        if k == "title" and "runs" in v:
                            titlu = v["runs"][0]["text"]
                        if k == "longBylineText" and "runs" in v:
                            group_box.setTitle(v["runs"][0]["text"] + " - " + titlu)
                        ####################################
                        #butonul play va avea Id-ul videoId. cand dam click, se va lua Id-ul
                        if k == "videoId" and len(v) == 11:
                            push_button.clicked.connect(lambda checked, index=v: self.playVideo(index))
                            #URL-ul thumbnail-ului, care e compus din ID-ul clipului
                            #Nu mai fac scrape la URL direct pentru ca thumbnailurile #shorts nu merg
                            #2.jpg, 1.jpg la shorts nu merg, dar 0.jpg merge. 
                            #scrape-ul ia mereu 2.jpg, nu ma complic si o sa lucrez doar cu video ID 
                            #https://i.ytimg.com/vi/ "ID_VIDEO" /0.jpg 
                            url = "https://i.ytimg.com/vi/" + v + "/0.jpg" 
                            smaller_pixmap = self.rezolvarePoza(url)
                            label_image.setPixmap(smaller_pixmap)
        ####################################
        top_widget.setLayout(top_vertical_layout)
        self.scrollAreaClipuri.setWidget(top_widget) 
        self.labelActiune.setText("Actiune:")
        self.labelActiune.repaint()
    ####################################
    
    #butoane
    #####################################
    #####################################
    def clickCautare(self):
        cautare = self.textCautare.toPlainText()
        content = self.scrapeCautare(cautare)
        self.adaugareContent(content)
    #####################################
    #clickDescarcaVideo
    def clickDescarcaVideo(self):
        #https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
        try:
            self.labelActiune.setText("Actiune: Descarcare videoclip...")
            self.labelActiune.repaint()
            with YoutubeDL() as ydl:
                ydl.download(self.video_curent)
            self.labelActiune.setText("Descarcat in: " + os.getcwd())
            self.labelActiune.repaint()
            print("Descarcat in " + os.getcwd())
        except Exception as e:
            print("Nu se poate descarca clipul. Eroare YT-DLP")
            self.labelActiune.setText("Nu se poate descarca videoclipul. Eroare yt-dlp")
            self.labelActiune.repaint()
    ##################################### 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

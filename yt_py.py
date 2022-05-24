from PyQt5 import QtCore, QtGui, QtWidgets

#IDEI VIITOR
#scraping mai bun, sa ia toate rezultatele nu doar 10 cate ia acum - sau un nr de rezultate, 50
#functie de cut al clipului - sa fac cumva sa il decarc in tempfile apoi sa fie cut
#functie de descarcare playlisturi - trebuie sa fac GUI-ul mai frumos intai 
#lucrat la layout-uri. sa vina elementele mai bine. asta in alt program, sa semene cu mediahuman 
#https://github.com/kokoko3k/xt7-player-mpv -- imi place cum arata si asta
#facut programu executabil .exe
#functionalitate mai avansata de download - selectare calitate/format/etc 
#functionalitate memorare playlisturi, memorare numaru de clipuri din playlist daca exista 
#-daca nr clipuri s-a marit, atunci incepe descarcarea playlistului 
#-memorare URL clipuri - daca exista URL atunci se da skip se ia urmatoru (cred ca e mai rapid decat daca las yt-dlp sa vada el),
#Threaduri in python - in timp ce se descarca un clip sau un playlist, utilizatoru sa poate  
#urmari clipuri https://realpython.com/python-pyqt-qthread/
#baza de date pentru LIbrarie (link playlisturi, nr videouri la descarcare playlist, si ce o sa mai fie)
#https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL ----- aici mai multe despre optiunile Youtube-Dl
#--^ ca sa ia formatu dorit (vad ca le face webm din oficiu), calitatea cea mai buna sau selectata, etc 
#in cod mai sunt idei, ctrl+f "idee"
#posibil ca sa scot diferitele playeruri din taburi, sa fac taburile pe jumate si playeru sa fie doar unu singur
#la cautare clipuri - pus buton descarca pt fiecare-sa se duca apoi pe tabu Desarcare unde are mai multe optiuni, sau optiunile sa fie ca la MediaHuman si in setari sa se puna si conventia de nume
#la cautare clipuri buton de copiere link si taiere
#https://github.com/oleksis/youtube-dl-gui
#https://www.youtube.com/watch?v=tGbl6a8a7ME
#https://www.reddit.com/r/youtubedl/comments/tme3xv/help_using_youtube_dlp_in_python_desktop_app/ - de vazut. pt descarcare clipuri in format si nume fila, autentificare


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
import re
from pytube import YouTube
from pytube import Playlist

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1146, 465)
        locale.setlocale(locale.LC_NUMERIC,"C")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.taburi = QtWidgets.QTabWidget(self.centralwidget)
        self.taburi.setGeometry(QtCore.QRect(10, 10, 1121, 421))
        self.taburi.setObjectName("taburi")
        self.tabCautare = QtWidgets.QWidget()
        self.tabCautare.setObjectName("tabCautare")
        self.pushButtonDescarca = QtWidgets.QPushButton(self.tabCautare)
        self.pushButtonDescarca.setGeometry(QtCore.QRect(979, 0, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonDescarca.setFont(font)
        self.pushButtonDescarca.setObjectName("pushButtonDescarca")
        self.widgetVideo = QtWidgets.QWidget(self.tabCautare)
        self.widgetVideo.setGeometry(QtCore.QRect(550, 50, 531, 311))
        self.widgetVideo.setObjectName("widgetVideo")
        self.labelActiune = QtWidgets.QLabel(self.tabCautare)
        self.labelActiune.setGeometry(QtCore.QRect(560, 0, 221, 41))
        self.labelActiune.setObjectName("labelActiune")
        self.pushButtonCautare = QtWidgets.QPushButton(self.tabCautare)
        self.pushButtonCautare.setGeometry(QtCore.QRect(490, 0, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCautare.setFont(font)
        self.pushButtonCautare.setObjectName("pushButtonCautare")
        self.labelCautare = QtWidgets.QLabel(self.tabCautare)
        self.labelCautare.setGeometry(QtCore.QRect(10, 10, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelCautare.setFont(font)
        self.labelCautare.setObjectName("labelCautare")
        self.textCautare = QtWidgets.QTextEdit(self.tabCautare)
        self.textCautare.setGeometry(QtCore.QRect(230, 0, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textCautare.setFont(font)
        self.textCautare.setObjectName("textCautare")
        self.scrollAreaClipuri = QtWidgets.QScrollArea(self.tabCautare)
        self.scrollAreaClipuri.setGeometry(QtCore.QRect(10, 50, 531, 311))
        self.scrollAreaClipuri.setWidgetResizable(True)
        self.scrollAreaClipuri.setObjectName("scrollAreaClipuri")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 525, 305))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaClipuri.setWidget(self.scrollAreaWidgetContents)
        self.taburi.addTab(self.tabCautare, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.taburi.addTab(self.tab_3, "")
        self.tabDescarcaPlaylist = QtWidgets.QWidget()
        self.tabDescarcaPlaylist.setObjectName("tabDescarcaPlaylist")
        self.scrollAreaClipuriPlaylist = QtWidgets.QScrollArea(self.tabDescarcaPlaylist)
        self.scrollAreaClipuriPlaylist.setGeometry(QtCore.QRect(0, 50, 531, 311))
        self.scrollAreaClipuriPlaylist.setWidgetResizable(True)
        self.scrollAreaClipuriPlaylist.setObjectName("scrollAreaClipuriPlaylist")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 525, 305))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaClipuriPlaylist.setWidget(self.scrollAreaWidgetContents_2)
        self.textLinkPlaylist = QtWidgets.QTextEdit(self.tabDescarcaPlaylist)
        self.textLinkPlaylist.setGeometry(QtCore.QRect(120, 0, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textLinkPlaylist.setFont(font)
        self.textLinkPlaylist.setObjectName("textLinkPlaylist")
        self.labelActiunePlaylist = QtWidgets.QLabel(self.tabDescarcaPlaylist)
        self.labelActiunePlaylist.setGeometry(QtCore.QRect(550, 0, 221, 41))
        self.labelActiunePlaylist.setObjectName("labelActiunePlaylist")
        self.widgetVideoPlaylist = QtWidgets.QWidget(self.tabDescarcaPlaylist)
        self.widgetVideoPlaylist.setGeometry(QtCore.QRect(540, 50, 531, 311))
        self.widgetVideoPlaylist.setObjectName("widgetVideoPlaylist")
        self.pushButtonLinkPlaylist = QtWidgets.QPushButton(self.tabDescarcaPlaylist)
        self.pushButtonLinkPlaylist.setGeometry(QtCore.QRect(480, 0, 51, 41))
        font = QtGui.QFont() 
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonLinkPlaylist.setFont(font)
        self.pushButtonLinkPlaylist.setObjectName("pushButtonLinkPlaylist")
        self.labelLinkPlaylist = QtWidgets.QLabel(self.tabDescarcaPlaylist)
        self.labelLinkPlaylist.setGeometry(QtCore.QRect(0, 10, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelLinkPlaylist.setFont(font)
        self.labelLinkPlaylist.setObjectName("labelLinkPlaylist")
        self.taburi.addTab(self.tabDescarcaPlaylist, "")
        self.tabTaieVideo = QtWidgets.QWidget()
        self.tabTaieVideo.setObjectName("tabTaieVideo")
        self.textTaieClip = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textTaieClip.setGeometry(QtCore.QRect(110, 10, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textTaieClip.setFont(font)
        self.textTaieClip.setObjectName("textTaieClip")
        self.pushButtonOkTaie = QtWidgets.QPushButton(self.tabTaieVideo)
        self.pushButtonOkTaie.setGeometry(QtCore.QRect(490, 10, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonOkTaie.setFont(font)
        self.pushButtonOkTaie.setObjectName("pushButtonOkTaie")
        self.labelTaie = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelTaie.setGeometry(QtCore.QRect(10, 20, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelTaie.setFont(font)
        self.labelTaie.setObjectName("labelTaie")
        self.textInceputOra = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textInceputOra.setGeometry(QtCore.QRect(130, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textInceputOra.setFont(font)
        self.textInceputOra.setObjectName("textInceputOra")
        self.labelInceput = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelInceput.setGeometry(QtCore.QRect(10, 90, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelInceput.setFont(font)
        self.labelInceput.setObjectName("labelInceput")
        self.labelSfarsit = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelSfarsit.setGeometry(QtCore.QRect(10, 140, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelSfarsit.setFont(font)
        self.labelSfarsit.setObjectName("labelSfarsit")
        self.textInceputMinut = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textInceputMinut.setGeometry(QtCore.QRect(180, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textInceputMinut.setFont(font)
        self.textInceputMinut.setObjectName("textInceputMinut")
        self.textInceputSecunda = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textInceputSecunda.setGeometry(QtCore.QRect(230, 80, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textInceputSecunda.setFont(font)
        self.textInceputSecunda.setObjectName("textInceputSecunda")
        self.textSfarsitOra = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textSfarsitOra.setGeometry(QtCore.QRect(130, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textSfarsitOra.setFont(font)
        self.textSfarsitOra.setObjectName("textSfarsitOra")
        self.textSfarsitSecunda = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textSfarsitSecunda.setGeometry(QtCore.QRect(230, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textSfarsitSecunda.setFont(font)
        self.textSfarsitSecunda.setObjectName("textSfarsitSecunda")
        self.textSfarsitMinut = QtWidgets.QTextEdit(self.tabTaieVideo)
        self.textSfarsitMinut.setGeometry(QtCore.QRect(180, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textSfarsitMinut.setFont(font)
        self.textSfarsitMinut.setObjectName("textSfarsitMinut")
        self.labelH = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelH.setGeometry(QtCore.QRect(140, 60, 21, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelH.setFont(font)
        self.labelH.setObjectName("labelH")
        self.labelM = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelM.setGeometry(QtCore.QRect(190, 60, 21, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelM.setFont(font)
        self.labelM.setObjectName("labelM")
        self.labelS = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelS.setGeometry(QtCore.QRect(240, 60, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelS.setFont(font)
        self.labelS.setObjectName("labelS")
        self.pushButonTaieClip = QtWidgets.QPushButton(self.tabTaieVideo)
        self.pushButonTaieClip.setGeometry(QtCore.QRect(130, 180, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButonTaieClip.setFont(font)
        self.pushButonTaieClip.setObjectName("pushButonTaieClip")
        self.labelActiuneTaie = QtWidgets.QLabel(self.tabTaieVideo)
        self.labelActiuneTaie.setGeometry(QtCore.QRect(560, 10, 221, 41))
        self.labelActiuneTaie.setObjectName("labelActiuneTaie")
        self.widgetVideoTaie = QtWidgets.QWidget(self.tabTaieVideo)
        self.widgetVideoTaie.setGeometry(QtCore.QRect(550, 60, 531, 301))
        self.widgetVideoTaie.setObjectName("widgetVideoTaie")
        self.taburi.addTab(self.tabTaieVideo, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.taburi.addTab(self.tab_2, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.taburi.addTab(self.tab_6, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #####################################
        #Butoane
        #####################################    
        self.pushButtonCautare.clicked.connect(self.clickCautare)
        self.pushButtonDescarca.clicked.connect(self.clickDescarcaVideo)
        self.pushButtonOkTaie.clicked.connect(self.clickPlayVideoTaie)
        self.pushButonTaieClip.clicked.connect(self.clickTaieVideo)
        self.pushButtonLinkPlaylist.clicked.connect(self.clickOkPlaylist)
        #####################################
        #Pentru MPV
        #https://github.com/jaseg/python-mpv
        #####################################    
        #player cautare
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
        #player taie
        self.container = self.widgetVideoTaie
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.playerTaie = mpv.MPV(wid=str(int(self.container.winId())),
                vo='x11', # You may not need this
                log_handler=print,
                loglevel='debug',
                input_default_bindings=True,
                input_vo_keyboard=True,
                osc=True
                )
        #player playlist
        self.container = self.widgetVideoPlaylist
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.playerPlaylist = mpv.MPV(wid=str(int(self.container.winId())),
                vo='x11', # You may not need this
                log_handler=print,
                loglevel='debug',
                input_default_bindings=True,
                input_vo_keyboard=True,
                osc=True
                )
        #playlist
        self.numar_clipuri_playlist = 0
        #####################################


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonDescarca.setText(_translate("MainWindow", "Descarca"))
        self.labelActiune.setText(_translate("MainWindow", "Actiune:..."))
        self.pushButtonCautare.setText(_translate("MainWindow", "OK"))
        self.labelCautare.setText(_translate("MainWindow", "Cautati clipuri pe YouTube:"))
        self.taburi.setTabText(self.taburi.indexOf(self.tabCautare), _translate("MainWindow", "Cauta pe YouTube"))
        self.taburi.setTabText(self.taburi.indexOf(self.tab_3), _translate("MainWindow", "Librarie"))
        self.labelActiunePlaylist.setText(_translate("MainWindow", "Actiune:..."))
        self.pushButtonLinkPlaylist.setText(_translate("MainWindow", "OK"))
        self.labelLinkPlaylist.setText(_translate("MainWindow", "Link playlist:"))
        self.taburi.setTabText(self.taburi.indexOf(self.tabDescarcaPlaylist), _translate("MainWindow", "Descarca Playlist"))
        self.pushButtonOkTaie.setText(_translate("MainWindow", "OK"))
        self.labelTaie.setText(_translate("MainWindow", "Taie clipul"))
        self.textInceputOra.setPlaceholderText(_translate("MainWindow", "00"))
        self.labelInceput.setText(_translate("MainWindow", "Timp inceput"))
        self.labelSfarsit.setText(_translate("MainWindow", "Timp sfarsit"))
        self.textInceputMinut.setPlaceholderText(_translate("MainWindow", "00"))
        self.textInceputSecunda.setPlaceholderText(_translate("MainWindow", "00"))
        self.textSfarsitOra.setPlaceholderText(_translate("MainWindow", "00"))
        self.textSfarsitSecunda.setPlaceholderText(_translate("MainWindow", "00"))
        self.textSfarsitMinut.setPlaceholderText(_translate("MainWindow", "00"))
        self.labelH.setText(_translate("MainWindow", "H"))
        self.labelM.setText(_translate("MainWindow", "M"))
        self.labelS.setText(_translate("MainWindow", "S"))
        self.pushButonTaieClip.setText(_translate("MainWindow", "Taie clipul"))
        self.labelActiuneTaie.setText(_translate("MainWindow", "Actiune:..."))
        self.taburi.setTabText(self.taburi.indexOf(self.tabTaieVideo), _translate("MainWindow", "Taie videoclip"))
        self.taburi.setTabText(self.taburi.indexOf(self.tab_2), _translate("MainWindow", "Descarca videoclip"))
        self.taburi.setTabText(self.taburi.indexOf(self.tab_6), _translate("MainWindow", "Setari"))

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
                        #indexul este URL-ul video-ului (v)
                        if k == "videoId" and len(v) == 11:
                            push_button.clicked.connect(lambda checked, index=v: self.clickPlayVideo(index))
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
    ################################################################
    ################################################################
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
    #clickPlayVideo
    def clickPlayVideo(self, v):
        self.labelActiune.setText("Actiune: Incarcare videoclip...")
        self.labelActiune.repaint()
        self.video_curent = "https://www.youtube.com/watch?v=" + v
        self.player.play(self.video_curent)
    #####################################
    def clickPlayVideoPlaylist(self, v):
        self.labelActiunePlaylist.setText("Actiune: Incarcare videoclip...")
        self.labelActiunePlaylist.repaint()
        self.video_curent = "https://www.youtube.com/watch?v=" + v
        self.playerPlaylist.play(self.video_curent)
    #####################################
    def clickPlayVideoTaie(self):
        link = self.textTaieClip.toPlainText()
        self.video_curent_taie = link
        self.labelActiuneTaie.setText("Actiune: Incarcare videoclip...")
        self.labelActiuneTaie.repaint()
        self.playerTaie.play(link)
    #####################################
    #clickTaieVideo
    def clickTaieVideo(self):
        try:
            self.labelActiuneTaie.setText("Actiune: Descarcare videoclip...")
            self.labelActiuneTaie.repaint()
            #idee
            #Asta cu extract e util pentru formatarea numelui filei. Utilizatoru sa aleaga cum vrea sa fie fila descarcata
            #Sau cred ca mai rapid ar fi facand scraping linkului
            with YoutubeDL() as ydl: 
                info_dict = ydl.extract_info(self.video_curent_taie, download=True)
                video_id = info_dict.get("id", None)
                video_title = info_dict.get('title', None)
                print("Titlu: " + video_title)
                print("ID: " + video_id)
            #Numele clipului descarcat, default este in formatul "nume_clipSPATIU[id_clip].ext"
            filename = video_title + " " + "[" + video_id + "]"
            #Acu verificam extensia ca sa vedem ce nume final are clipul descarcat
            if os.path.isfile(filename+'.mkv'):
                extension = '.mkv'
                filename= filename+extension
            elif os.path.isfile(filename+'.mp4'):
                extension = '.mp4'
                filename= filename+extension
            elif os.path.isfile(filename+'.webm'):
                extension = '.webm'
                filename= filename+extension
            #pentru a descarca in temp- nu utilizez
            #cale = tempfile.gettempdir()
            #try:
            #    os.chdir(cale)
            #except Exception as e:
            #    print("Directorul: {0} nu exista".format(cale))
            #
            #ydl_opts = {'outtmpl': cale + 'nume_pt_video_descarcat'} -- calea setata + nume video ca argumente
            #ydl_opts = {'outtmpl': 'nume_pt_video_descarcat'} -- doar numele ce-l vrem noi
             #with YoutubeDL(ydl_opts) as ydl:
            #    ydl.download(self.video_curent_taie)
            #
            self.labelActiuneTaie.setText("Actiune: Taiere videoclip...")
            self.labelActiuneTaie.repaint()
            os.system("ffmpeg -i " + "'" + filename + "'" + " -ss " + self.textInceputOra.toPlainText() + ":" + self.textInceputMinut.toPlainText() + ":" + self.textInceputSecunda.toPlainText() + " -to " + self.textSfarsitOra.toPlainText() + ":" + self.textSfarsitMinut.toPlainText() + ":" + self.textSfarsitSecunda.toPlainText() + " -c:v copy -c:a copy" + " 'Taiat_"+filename+"'")
            self.labelActiuneTaie.setText("Actiune: Stergere videoclip initial...")
            self.labelActiuneTaie.repaint()
            #idee
            #eventual o bifa daca vrea sa stearga si clipul original
            #os.remove(filename)
            self.labelActiuneTaie.setText("Videoclip taiat in: " + os.getcwd())
            self.labelActiuneTaie.repaint()
           
            #self.labelActiuneTaie.setText("Actiune: Taiere videoclip...")
            #self.labelActiuneTaie.repaint()


        except Exception as e:
            print("Eroare. Nu se poate taia clipul.")
            self.labelActiuneTaie.setText("Eroare. Nu se poate taia clipul.")
            self.labelActiuneTaie.repaint()
            print(e)
    #####################################
    def clickOkPlaylist(self):
        link_playlist = self.textLinkPlaylist.toPlainText()
        playlist = Playlist(link_playlist)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        self.numar_clipuri_playlist = len(playlist.video_urls)
        print('Numar de clipuri in playlist: %s' %self.numar_clipuri_playlist)
        self.adaugareContentPlaylist(playlist)
    #####################################
    #adaugareContentPlaylist
    def adaugareContentPlaylist(self, playlist):
        self.labelActiunePlaylist.setText("Actiune: Adaugare clipuri..."+str(self.numar_clipuri_playlist))
        self.labelActiunePlaylist.repaint()
        top_widget = QtWidgets.QWidget()
        top_vertical_layout = QtWidgets.QVBoxLayout()
        titlu = ""

        #accesam lista playlist 
        for url in playlist.video_urls:
            #Asezat elemente
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
            
            #Data pentru elemente
            yt = YouTube(url) #pytube
            titlu = yt.author + " - " + yt.title
            group_box.setTitle(titlu)
            push_button.clicked.connect(lambda checked, index=yt.video_id: self.clickPlayVideoPlaylist(index))
            #URL-ul thumbnail-ului, care e compus din ID-ul clipului
            #https://i.ytimg.com/vi/ "ID_VIDEO" /0.jpg  
            #url = "https://i.ytimg.com/vi/" + yt.video_id + "/0.jpg"
            #poate nu e nevoie de ^ si merge cu link-ul generat de pytube si pentru #shorts
            smaller_pixmap = self.rezolvarePoza(yt.thumbnail_url)
            label_image.setPixmap(smaller_pixmap)
            self.numar_clipuri_playlist = self.numar_clipuri_playlist - 1
            self.labelActiunePlaylist.setText("Actiune: Adaugare clipuri..."+str(self.numar_clipuri_playlist))
            self.labelActiunePlaylist.repaint()
            ####################################
        ####################################
        top_widget.setLayout(top_vertical_layout)
        self.scrollAreaClipuriPlaylist.setWidget(top_widget) 
        self.labelActiunePlaylist.setText("Actiune:")
        self.labelActiunePlaylist.repaint()
    ####################################




############### Librarie, baza de date, adaugare playlist in librarie buton descarcare playlist




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

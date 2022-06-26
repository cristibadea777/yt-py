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

#In "Librarie" sa se poata vizualiza metadatele playlistului (nr clipuri, autor (de bagat in in BD), ultima descarcare, nume playlist) sub forma de tabel
#si doua butoane "descarca" si "vizualizeaza" - vizualizeaza te trimite la tabu "playlist" unde se incarca acolo playlistu si buton (copiaza link)

# de revazut functia de cut ca vad ca nu merge mereu 
#exemplu nu merge pt https://www.youtube.com/watch?v=45odEv_1DAY dar nu da nicio eroare
#sa folosesc https://zulko.github.io/moviepy/ https://www.youtube.com/watch?v=8XSNmKYxBTk

#playlist are Playlist.last_updated, de lucrat cu asta pe viitor, sa fac sa se verifice la fiecare start de aplicatie si sa se faca update.
#si daca data ultima descarcare (care depinde de noi) e mai veche decat Playlist.last_updated atunci sa apara ca trebuie descarcat (alt tab sau ceva)
#la fel sa se faca si cu thumbnailu, daca s-a modificat playlistu sa se faca update si la thumbnail (de pus thumbnail_url in Clasa_Playlist, sa fie luat atunci cand il inseram) 

#in librarie/playlist functie cautare video
#in librarie buton "schimba folder descarcare" - sau facut ca la media human, playlistu sa se salveze in folder diferit automat
#in librarie radiobuton rosu/verde daca playlistu are videouri noi (si pop-up message pe radiobuton -"clipuri noi" cand pui mouseul)

#de marit label-urile ca sa se vada tot unde s-a descarcat calea

#pentru NUMAR CLIPURI atunci cand se incarca libraria, sa se ia playlisturile si sa se verifice nr clipuri, daca nr != nr_clipuri_playlist atunci nr_clipuri_paylist e updatat in BD cu nr


#pentru atunci cand se descarca un playlist...as putea sa pun un LABEL pt fiecare video din playlist. cu ID Label = ID videoclip. Si atunci cand se descarca,
#sa se updateze fiecare label "se descarca..." si eventual si procentu

#adaugare optiune de descarcare playlist DUPA un anumit video ex incepere descarcare dupa 300 de videouri

        ##de vazut daca imi mai trebuie numarClipuriPlaylist, cred ca e degeaba, cred ca nici nu se actualizeaza nicaieri. de scos sau de facut sa faca update
        #la fel si cu nr cliputi playlist, sa se actualizeze sau sa fie scos

#DE FACUT URMATORII PASI:
#buton "Descarca" in librarie, functionalitate descarcare playlist, si librarie facuta mai mare sa incarce si butonu
#splashscreen
#https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QSplashScreen.html
#functie actualizare librarie dupa ce se descarca playlistu sa dispara labelu 

#labelurile din librarie ar putea fi puse si sa aiba id-ul playlistului 'label_id_playlist'
#ca sa pot lucra mai usor cu ele fara sa fac actualizarea librariei cand se incarca aplicatia ci doar cand se da click pe buton
#deci cand pornim aplicatia labelurile sa nu fie (daca nu s-a facut actualizarea automata)
#sa fie ascunse, dar sa existe cu 'label_id_playlist', si abia dupa ce se face actualizarea, sa apara cu textu daca necesita etc 
#la setari utilizatoru aa poata bifa actualizarea automata la deschiderea aplicatiei

#Buton "Verifica actualizarile"                        
#Cand se apasa, se cheama aceeasi functie de incarcare librarie - dar in functie sa bag inca un argument 
#Si daca e chemat argumentu atunci sa fie pusa si partea cu label_actualizare_playlist
#iar numar_clipuri sa ramana, se baga la inserare, si se verifica doar cand se actioneaza butonu
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
import sqlite3
from datetime import datetime
import clipboard
from QLed import QLed
from playlist import Playlist as Clasa_Playlist
from librarie import Librarie as ClasaLibrarie
from videoclip import Videoclip as Clasa_Videoclip




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1149, 463)
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
        self.tabLibrarie = QtWidgets.QWidget()
        self.tabLibrarie.setObjectName("tabLibrarie")
        self.scrollAreaTabelLibrarie = QtWidgets.QScrollArea(self.tabLibrarie)
        self.scrollAreaTabelLibrarie.setGeometry(QtCore.QRect(10, 10, 851, 361))
        self.scrollAreaTabelLibrarie.setWidgetResizable(True)
        self.scrollAreaTabelLibrarie.setObjectName("scrollAreaTabelLibrarie")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 845, 355))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollAreaTabelLibrarie.setWidget(self.scrollAreaWidgetContents_3)
        self.labelClipuriRamase = QtWidgets.QLabel(self.tabLibrarie)
        self.labelClipuriRamase.setGeometry(QtCore.QRect(870, 10, 231, 21))
        self.labelClipuriRamase.setObjectName("labelClipuriRamase")
        self.labelVideoCurent1 = QtWidgets.QLabel(self.tabLibrarie)
        self.labelVideoCurent1.setGeometry(QtCore.QRect(870, 50, 231, 21))
        self.labelVideoCurent1.setObjectName("labelVideoCurent1")
        self.labelVideoCurent2 = QtWidgets.QLabel(self.tabLibrarie)
        self.labelVideoCurent2.setGeometry(QtCore.QRect(870, 80, 231, 21))
        self.labelVideoCurent2.setObjectName("labelVideoCurent2")
        self.taburi.addTab(self.tabLibrarie, "")
        self.tabPlaylist = QtWidgets.QWidget()
        self.tabPlaylist.setObjectName("tabPlaylist")
        self.scrollAreaClipuriPlaylist = QtWidgets.QScrollArea(self.tabPlaylist)
        self.scrollAreaClipuriPlaylist.setGeometry(QtCore.QRect(0, 90, 531, 281))
        self.scrollAreaClipuriPlaylist.setWidgetResizable(True)
        self.scrollAreaClipuriPlaylist.setObjectName("scrollAreaClipuriPlaylist")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 525, 275))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaClipuriPlaylist.setWidget(self.scrollAreaWidgetContents_2)
        self.textLinkPlaylist = QtWidgets.QTextEdit(self.tabPlaylist)
        self.textLinkPlaylist.setGeometry(QtCore.QRect(110, 0, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textLinkPlaylist.setFont(font)
        self.textLinkPlaylist.setObjectName("textLinkPlaylist")
        self.labelActiunePlaylist = QtWidgets.QLabel(self.tabPlaylist)
        self.labelActiunePlaylist.setGeometry(QtCore.QRect(550, 0, 221, 41))
        self.labelActiunePlaylist.setObjectName("labelActiunePlaylist")
        self.widgetVideoPlaylist = QtWidgets.QWidget(self.tabPlaylist)
        self.widgetVideoPlaylist.setGeometry(QtCore.QRect(540, 50, 531, 311))
        self.widgetVideoPlaylist.setObjectName("widgetVideoPlaylist")
        self.pushButtonLinkPlaylist = QtWidgets.QPushButton(self.tabPlaylist)
        self.pushButtonLinkPlaylist.setGeometry(QtCore.QRect(0, 50, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonLinkPlaylist.setFont(font)
        self.pushButtonLinkPlaylist.setObjectName("pushButtonLinkPlaylist")
        self.labelLinkPlaylist = QtWidgets.QLabel(self.tabPlaylist)
        self.labelLinkPlaylist.setGeometry(QtCore.QRect(0, 10, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelLinkPlaylist.setFont(font)
        self.labelLinkPlaylist.setObjectName("labelLinkPlaylist")
        self.pushButtonDescarcaPlaylist = QtWidgets.QPushButton(self.tabPlaylist)
        self.pushButtonDescarcaPlaylist.setGeometry(QtCore.QRect(100, 50, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonDescarcaPlaylist.setFont(font)
        self.pushButtonDescarcaPlaylist.setObjectName("pushButtonDescarcaPlaylist")
        self.pushButtonAdaugaInLibrarie = QtWidgets.QPushButton(self.tabPlaylist)
        self.pushButtonAdaugaInLibrarie.setGeometry(QtCore.QRect(200, 50, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAdaugaInLibrarie.setFont(font)
        self.pushButtonAdaugaInLibrarie.setObjectName("pushButtonAdaugaInLibrarie")
        self.taburi.addTab(self.tabPlaylist, "")
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

        self.retranslateUi(MainWindow)
        self.taburi.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonDescarca.setText(_translate("MainWindow", "Descarca"))
        self.labelActiune.setText(_translate("MainWindow", "Actiune:..."))
        self.pushButtonCautare.setText(_translate("MainWindow", "OK"))
        self.labelCautare.setText(_translate("MainWindow", "Cautati clipuri pe YouTube:"))
        self.taburi.setTabText(self.taburi.indexOf(self.tabCautare), _translate("MainWindow", "Cauta pe YouTube"))
        self.labelClipuriRamase.setText(_translate("MainWindow", "Clipuri ramase de descarcat: "))
        self.labelVideoCurent1.setText(_translate("MainWindow", "Video curent:"))
        self.labelVideoCurent2.setText(_translate("MainWindow", "Video curent..."))
        self.taburi.setTabText(self.taburi.indexOf(self.tabLibrarie), _translate("MainWindow", "Librarie"))
        self.labelActiunePlaylist.setText(_translate("MainWindow", "Actiune:..."))
        self.pushButtonLinkPlaylist.setText(_translate("MainWindow", "Vizualizare"))
        self.labelLinkPlaylist.setText(_translate("MainWindow", "Link playlist:"))
        self.pushButtonDescarcaPlaylist.setText(_translate("MainWindow", "Descarca"))
        self.pushButtonAdaugaInLibrarie.setText(_translate("MainWindow", "Adauga in librarie"))
        self.taburi.setTabText(self.taburi.indexOf(self.tabPlaylist), _translate("MainWindow", "Playlist"))
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
        ######################
        self.initializareElemente()
        
    def initializareElemente(self):
        locale.setlocale(locale.LC_NUMERIC,"C")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.labelClipuriRamase.setHidden(True)
        self.labelVideoCurent1.setHidden(True) 
        self.labelVideoCurent2.setHidden(True) 
        self.labelClipuriRamase.setFont(font)
        self.labelVideoCurent1.setFont(font)
        self.labelVideoCurent2.setFont(font)
        #####################################
        #Butoane
        #####################################    
        self.pushButtonCautare.clicked.connect(self.clickCautare)
        self.pushButtonDescarca.clicked.connect(self.clickDescarcaVideo)
        self.pushButtonOkTaie.clicked.connect(self.clickPlayVideoTaie)
        self.pushButonTaieClip.clicked.connect(self.clickTaieVideo)
        self.pushButtonLinkPlaylist.clicked.connect(self.clickOkPlaylist)
        self.pushButtonAdaugaInLibrarie.clicked.connect(self.clickAdaugaInLibrarie)
        self.pushButtonDescarcaPlaylist.clicked.connect(self.clickDescarcaPlaylist)
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
        #Baza de Date
        #####################################
        #Conexiune BD
        conexiune = sqlite3.connect('librarie.db') #fisier pt baza de date. daca nu exista se creaza gol
        cursor = conexiune.cursor()#cursor - ne permite sa executam comenzi SQL pentru conexiune
        #Librarie
        self.librarie = ClasaLibrarie(conexiune, cursor)
        self.adaugareContentLibrarie()
        #####################################

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
    #adaugare content cautare
    def adaugareContentCautare(self, content):
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
                            push_button.clicked.connect(lambda checked, index=v: self.clickPlayVideoCautare(index))
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
        self.adaugareContentCautare(content)
    ##########################################################################
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
    ##########################################################################
    #clickPlayVideoCautare
    def clickPlayVideoCautare(self, v):
        self.labelActiune.setText("Actiune: Incarcare videoclip...")
        self.labelActiune.repaint() 

        self.video_curent = "https://www.youtube.com/watch?v=" + v
        self.player.play(self.video_curent)
    ##########################################################################
    def clickPlayVideoPlaylist(self, v):
        self.labelActiunePlaylist.setText("Actiune: Incarcare videoclip...")
        self.labelActiunePlaylist.repaint()
        self.video_curent = "https://www.youtube.com/watch?v=" + v
        self.playerPlaylist.play(self.video_curent)
    ##########################################################################
    def clickPlayVideoTaie(self):
        link = self.textTaieClip.toPlainText()
        self.video_curent_taie = link
        self.labelActiuneTaie.setText("Actiune: Incarcare videoclip...")
        self.labelActiuneTaie.repaint()
        self.playerTaie.play(link)
    ##########################################################################
    def clickCopiazaLink(self, url):
        clipboard.copy(url)
        #self.labelActiuneLibrarie.setText("Link copiat in clipboard")
    ##########################################################################
    def clickStergePlaylistLibrarie(self, url):
        msg_box = QMessageBox()    
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Sterge playlist")
        msg_box.setText("Esti sigur ca vrei sa stergi playlistul?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg_box.exec_()
        if retval == QMessageBox.Yes:
                self.librarie.deletePlaylist(url)
                self.adaugareContentLibrarie()
    ##########################################################################
    #Descarcare playlist
    def clickDescarcaPlaylist(self):
        url_playlist = self.textLinkPlaylist.toPlainText()
        msg_box = QMessageBox()    
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Informatie Descarcare Playlist")
        msg_box.setInformativeText("Playlisturile descarcate de aici si nu din sectiunea Librarie, nu vor fi salvate in Baza de Date, iar videoclipurile nu vor fi verificate daca au fost deja descarcate.")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg_box.exec_()
        if retval == QMessageBox.Ok:
            try:
                #se face scraping si pt fiecare clip se verifica/descarca etc
                playlist = Playlist(url_playlist)
                nume_playlist = playlist.title
                self.numar_clipuri_playlist = len(playlist.video_urls)
                for url_videoclip in playlist.video_urls:
                    #descarca link cu link
                    self.labelActiunePlaylist.setText("Descarcare clipuri, ramase " + str(self.numar_clipuri_playlist))
                    self.labelActiunePlaylist.repaint()
                    with YoutubeDL() as ydl:
                        ydl.download(url_videoclip)
                    self.numar_clipuri_playlist = self.numar_clipuri_playlist - 1
                self.labelActiunePlaylist.setText("Descarcat in " + os.getcwd())
                self.labelActiunePlaylist.repaint()
                print("Descarcat in " + os.getcwd())
            except Exception as e:
                print(e)
                self.labelActiunePlaylist.setText("Eroare - Playlist privat sau link invalid.")
                self.labelActiunePlaylist.repaint()
    #Descarcare playlist pentru Librarie
    def clickDescarcaPlaylistLibrarie(self, url_playlist):
        self.labelClipuriRamase.setHidden(False)
        self.labelVideoCurent1.setHidden(False) 
        self.labelVideoCurent2.setHidden(False) 
        #se face scraping si pt fiecare clip se verifica/descarca etc
        playlist = Playlist(url_playlist)
        self.numar_clipuri_playlist = len(playlist.video_urls)
        nume_playlist = playlist.title
        print(url_playlist)
        print(nume_playlist)
        print(self.numar_clipuri_playlist)
        for url_videoclip in playlist.video_urls:
            #putem avea acelas videoclip in mai multe playlisturi, de aceea dau si url_playlist\
            lista_rezultate = self.librarie.gasesteVideo(url_videoclip, url_playlist)
            if len(lista_rezultate) == 0:
                #descarca link cu link
                try:
                    print(url_videoclip)
                    self.labelClipuriRamase.setText("Descarcare clipuri, ramase " + str(self.numar_clipuri_playlist))
                    self.labelClipuriRamase.repaint()
                    yt = YouTube(url_videoclip)
                    autor_videoclip = yt.author
                    nume_videoclip = yt.title
                    self.labelVideoCurent2.setText(autor_videoclip + " - " + nume_videoclip)
                    self.labelVideoCurent2.repaint()
                    with YoutubeDL() as ydl:
                        ydl.download(url_videoclip)
                    self.numar_clipuri_playlist = self.numar_clipuri_playlist - 1
                    print("Descarcat in " + os.getcwd())
                    #punere in BD - in tabelul Videoclip - daca a fost descarcat cu succes
                    #nume_playlist, url_playlist, url_videoclip, nume_videoclip, autor_videoclip, stare_descarcare
                    self.librarie.adaugaVideoclip(Clasa_Videoclip(nume_playlist, url_playlist, url_videoclip, nume_videoclip, autor_videoclip, 'Descarcat'))
                    #incrementarea numarului de clipuri descarcate - in tabelul Playlist -
                    self.librarie.updateIncrementareNumarClipuriDescarcate(url_playlist)
                except Exception as e:
                    print("Eroare: ")
                    print(e)
        self.labelClipuriRamase.setText("Playlist descarcat in " + os.getcwd())
        self.labelVideoCurent1.setHidden(True) 
        self.labelVideoCurent2.setHidden(True) 

##########################################################################
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
        self.adaugareContentPlaylist(playlist)
    #####################################
    def clickAdaugaInLibrarie(self):
        self.labelActiunePlaylist.setText("Adaugare playlist...")
        self.labelActiunePlaylist.repaint()
        url = self.textLinkPlaylist.toPlainText()
        playlist_adaugat = Playlist(url)
        now = datetime.now()
        now.strftime("%d/%B/%Y, %H:%M:%S")
        try:
                executie = self.librarie.adaugaPlaylist(Clasa_Playlist(playlist_adaugat.title, url, len(playlist_adaugat.video_urls), now.strftime("%d/%B/%Y, %H:%M"), 'Niciodata', 0))
                if executie == "exista":
                        self.labelActiunePlaylist.setText("Playlist deja existent in librarie")
                        self.labelActiunePlaylist.repaint()
                        return
                self.adaugareContentLibrarie()
                self.labelActiunePlaylist.setText("Playlist adaugat")
                self.labelActiunePlaylist.repaint()

        except Exception as e:
                print(e)
                self.labelActiunePlaylist.setText("Eroare - Playlist privat sau Link invalid.")
                self.labelActiunePlaylist.repaint()

    #####################################
    def clickRedarePlaylistDinLibrarie(self, url):
        self.taburi.setCurrentIndex(2) #miscare pe tab playlist
        self.textLinkPlaylist.setText(url)
        playlist = Playlist(url)
        self.adaugareContentPlaylist(playlist)

    #####################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #De facut - sa se incarce progresiv nu toate odata
    #########################################################################################################################################################################################
    #adaugareContentPlaylist
    def adaugareContentPlaylist(self, playlist):
        try:
            #pentru nr clipuri playlist ramase
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            self.numar_clipuri_playlist = len(playlist.video_urls)
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
        except Exception as e:
            print(e)
            self.labelActiunePlaylist.setText("Eroare. Link playlist invalid sau privat")
    ####################################
    ####################################

    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################
    #########################################################################################################################################################################################


    #Incarcare Librarie
    def adaugareContentLibrarie(self):
        #Din BD incarcam in variabila librarie informatiile din tabelul Playlist
        librarie = self.librarie.incarcaLibrarie()
        top_widget = QtWidgets.QWidget()
        top_vertical_layout = QtWidgets.QVBoxLayout()
        titlu = ""
        #accesam libraria
        for playlist in librarie:
                #playlist[0] - nume_playlist    
                #playlist[1] - url_playlist
                #playlist[2] - numar_clipuri
                #playlist[3] - data_adaugare
                #playlist[4] - data_ultima_descarcare            
                #Asezat elemente
                #group box, adaugat la vertical layout
                group_box = QtWidgets.QGroupBox()
                group_box.setGeometry(QtCore.QRect(10, 20, 521, 141))
                top_vertical_layout.addWidget(group_box)
                #label imagine
                label_image = QtWidgets.QLabel()
                #buton play
                push_button = QtWidgets.QPushButton()
                push_button.setFixedSize(100, 50)
                push_button.setText("Reda playlist")
                font = QtGui.QFont()
                font.setPointSize(11)
                push_button.setFont(font)
                #buton copiere link playlist
                push_button_linkplaylist = QtWidgets.QPushButton()
                push_button_linkplaylist.setFixedSize(100, 50)
                push_button_linkplaylist.setText("Copiaza link")
                push_button_linkplaylist.setFont(font)
                #buton sterge playlist din librarie
                push_button_sterge = QtWidgets.QPushButton()
                push_button_sterge.setFixedSize(100, 50)
                push_button_sterge.setText("Sterge")
                push_button_sterge.setFont(font)
                #buton descarca playlist
                push_button_descarca = QtWidgets.QPushButton()
                push_button_descarca.setFixedSize(100, 50)
                push_button_descarca.setText("Descarca")
                push_button_descarca.setFont(font)
                #label pentru atentionare utilizator pentru actualizare playlisturi 
                font = QtGui.QFont()
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                label_actualizare_playlist = QLabel("- necesita actualizat")
                label_actualizare_playlist.setFont(font)
                label_actualizare_playlist.setStyleSheet('color: red')

                #horizontal layout al group box
                groupbox_horizontal_layout = QtWidgets.QHBoxLayout()
                groupbox_horizontal_layout.addWidget(label_image)
                groupbox_horizontal_layout.addWidget(push_button)
                groupbox_horizontal_layout.addWidget(push_button_linkplaylist)
                groupbox_horizontal_layout.addWidget(push_button_sterge)
                groupbox_horizontal_layout.addWidget(push_button_descarca)

                #Elementele nu vor avea spatii mari intre ele cu urmatoarele doua linii
                groupbox_horizontal_layout.setSpacing(10) 
                groupbox_horizontal_layout.addStretch(1) 
                
                #vertical layout
                group_box.setLayout(groupbox_horizontal_layout)
                top_vertical_layout.addLayout(groupbox_horizontal_layout) 
                    
                #Data pentru elemente
                titlu = playlist[0]
                group_box.setTitle(titlu)
                push_button.clicked.connect(lambda checked, index=playlist[1]: self.clickRedarePlaylistDinLibrarie(index))
                push_button_linkplaylist.clicked.connect(lambda checked, index=playlist[1]: self.clickCopiazaLink(index)) 
                push_button_sterge.clicked.connect(lambda checked, index=playlist[1]: self.clickStergePlaylistLibrarie(index)) 
                push_button_descarca.clicked.connect(lambda checked, index=playlist[1]: self.clickDescarcaPlaylistLibrarie(index)) 
                try:
                        p = Playlist(playlist[1])
                        y = YouTube(p.video_urls[0])
                        ##################################################

                        #URL-ul thumbnail-ului primului video din thumbnail
                        url_thumbnail_playlist = y.thumbnail_url 
                        #luam thumbnailul dintr-un obiect YouTube pe care il luam inainte dintr-un obiect Playlist(primul clip din playlist)
                        smaller_pixmap = self.rezolvarePoza(url_thumbnail_playlist)
                        label_image.setPixmap(smaller_pixmap)

                        #Verificare actualizari playlisturi
                        numar_clipuri_curente = len(p.video_urls)
                        numar_clipuri_descarcate = self.librarie.numarClipuriDescarcate(playlist[1])[0] 
                        #rezultatul este tuplu ex: (2,) de aia iau primu element care e int
                        if numar_clipuri_curente > numar_clipuri_descarcate:
                            groupbox_horizontal_layout.addWidget(label_actualizare_playlist)
                        ##################################################
                except Exception as e:
                        print(e)
                ####################################
        ####################################
        top_widget.setLayout(top_vertical_layout)
        self.scrollAreaTabelLibrarie.setWidget(top_widget) 

        ####################################


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

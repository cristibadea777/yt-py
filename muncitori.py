from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from urllib.request import urlopen
import base64
from PIL import Image
import tempfile
import time
from pytube import YouTube
from pytube import Playlist
import re

class ThreadPlaylist(QThread):
    
    semnal = pyqtSignal(str)

    def setarePlaylist(self, playlist):
    	self.playlist = playlist
    	

    def run(self):
    	print(len(self.playlist.video_urls))
    	for url in self.playlist.video_urls:
            time.sleep(1)
            print(url)
            self.semnal.emit(url)
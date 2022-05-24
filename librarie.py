import sqlite3
from playlist import Playlist as Clasa_Playlist
from datetime import datetime

#Clasa serviciu pentru clasa model Playlist

class Librarie:
        ##################################################
        def __init__(self, conexiune, cursor):
                self.conexiune = conexiune
                self.cursor = cursor
                cursor.execute("""CREATE TABLE IF NOT EXISTS playlist (
                        nume_playlist TEXT,
                        url_playlist TEXT NOT NULL PRIMARY KEY,
                        numar_clipuri INTEGER,
                        data_adaugare TEXT,
                        data_ultima_descarcare TEXT
                        )""")
        ##################################################
        #Functii CRUD
        ##################################################
        #Insert 
        def adaugaPlaylist(self, playlist):
                with self.conexiune:
                        try:
                                self.cursor.execute("INSERT INTO playlist VALUES (:nume_playlist, :url_playlist, :numar_clipuri, :data_adaugare, :data_ultima_descarcare)", 
                                        {'nume_playlist':playlist.nume_playlist, 'url_playlist':playlist.url_playlist, 'numar_clipuri':playlist.numar_clipuri, 'data_adaugare': playlist.data_adaugare, 'data_ultima_descarcare':playlist.data_ultima_descarcare})
                        except Exception as e:
                                print(e)
        ##################################################
        #Update
        def updateNumePlaylist(self, playlist, nume):
                with self.conexiune:
                        self.cursor.execute("""UPDATE playlist SET nume_playlist = :nume_playlist 
                                                 WHERE url_playlist = :url_playlist""", 
                                                 {'nume_playlist':nume, 'url_playlist':playlist.url_playlist})
        def updateDataUltimaDescarcare(self, playlist, data_ultima_descarcare):
                with self.conexiune:
                        self.cursor.execute("""UPDATE playlist SET data_ultima_descarcare = :data_ultima_descarcare
                                                 WHERE url_playlist = :url_playlist""", 
                                                 {'data_ultima_descarcare':data_ultima_descarcare, 'url_playlist':playlist.url_playlist})
        ##################################################
        #Delete
        def deletePlaylist(self, playlist):
                with self.conexiune:
                        self.cursor.execute("""DELETE FROM playlist  
                                                 WHERE url_playlist = :url_playlist""",
                                                 {'url_playlist':playlist.url_playlist})
        ##################################################
        #Select
        def arataLibrarie(self):
                self.cursor.execute("SELECT * FROM playlist")
                print(self.cursor.fetchall())
        ##################################################
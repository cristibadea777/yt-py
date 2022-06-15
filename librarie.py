import sqlite3
from playlist import Playlist as Clasa_Playlist
from videoclip import Videoclip as Clasa_Video
from datetime import datetime

#Clasa serviciu pentru clasa model Playlist

class Librarie:
        ##################################################
        def __init__(self, conexiune, cursor):
                self.conexiune = conexiune
                self.cursor = cursor
                #Creare Tabel Playlist daca nu exista
                cursor.execute("""CREATE TABLE IF NOT EXISTS playlist (
                        nume_playlist TEXT,
                        url_playlist TEXT NOT NULL PRIMARY KEY,
                        numar_clipuri INTEGER,
                        data_adaugare TEXT,
                        data_ultima_descarcare TEXT
                        )""")
                #Creare Tabel Videoclip daca nu exista 
                cursor.execute("""CREATE TABLE IF NOT EXISTS videoclip (
                        nume_playlist TEXT,
                        url_playlist TEXT,
                        url_videoclip TEXT NOT NULL PRIMARY KEY,
                        nume_videoclip TEXT,
                        autor_videoclip TEXT,
                        stare_descarcare TEXT
                        )""")
        ##################################################
        #Functii CRUD
        ##################################################
        #Select
        def incarcaLibrarie(self):
                with self.conexiune:
                        try:
                                self.cursor.execute("SELECT * FROM playlist")
                                librarie = self.cursor.fetchall()
                                return librarie
                        except Exception as e:
                                print(e)
        ##################################################
        def gasesteVideo(self, url_videoclip, url_playlist):
                with self.conexiune:
                        try:
                                #Selecteaza videoul ce are linkul...
                                self.cursor.execute(""" SELECT * FROM videoclip
                                                        WHERE url_videoclip = :url_videoclip 
                                                        AND url_playlist = :url_playlist""",
                                                        {'url_videoclip':url_videoclip, 'url_playlist':url_playlist})
                                rezultat = self.cursor.fetchall()
                                return rezultat
                        except Exception as e:
                                print(e)
        ##################################################
        def numarClipuriPlaylist(self, url_playlist):
                try:
                        #Selecteaza nr clipurilor playlistului din BD
                        self.cursor.execute(""" SELECT numar_clipuri FROM playlist
                                                WHERE url_playlist = :url_playlist  """, {'url_playlist':url_playlist})
                        rezultat = self.cursor.fetchone()
                        return rezultat
                except Exception as e:
                        print(e)
        ##################################################
        #Insert 
        def adaugaPlaylist(self, playlist):
                with self.conexiune:
                        try:
                                self.cursor.execute("INSERT INTO playlist VALUES (:nume_playlist, :url_playlist, :numar_clipuri, :data_adaugare, :data_ultima_descarcare)", 
                                        {'nume_playlist':playlist.nume_playlist, 'url_playlist':playlist.url_playlist, 'numar_clipuri':playlist.numar_clipuri, 'data_adaugare': playlist.data_adaugare, 'data_ultima_descarcare':playlist.data_ultima_descarcare})
                        except Exception as e:
                                print(e)
                                return "exista"
                                                        

        def adaugaVideoclip(self, videoclip):
                with self.conexiune:
                        try:
                                self.cursor.execute("INSERT INTO videoclip VALUES (:nume_playlist, :url_playlist, :url_videoclip, :nume_videoclip, :autor_videoclip, :stare_descarcare)", 
                                        {'nume_playlist':videoclip.nume_playlist, 'url_playlist':videoclip.url_playlist, 'url_videoclip':videoclip.url_videoclip, 'nume_videoclip':videoclip.nume_videoclip, 'autor_videoclip': videoclip.autor_videoclip, 'stare_descarcare':videoclip.stare_descarcare})
                        except Exception as e:
                                print(e)
                                return "exista"
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
        def deletePlaylist(self, url):
                with self.conexiune:
                        self.cursor.execute("""DELETE FROM playlist  
                                                 WHERE url_playlist = :url_playlist""",
                                                 {'url_playlist':url})
        ##################################################

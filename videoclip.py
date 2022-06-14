class Videoclip:

	def __init__(self, nume_playlist, url_playlist, url_videoclip, nume_videoclip, autor_videoclip, stare_descarcare):
		#(campul "stare_descarcat" e cam degeaba, e mai mult vizual, pentru ca daca nu il gaseste atunci nu a fost descarcat)
		self.nume_playlist = nume_playlist
		self.url_playlist = url_playlist
		self.url_videoclip = url_videoclip
		self.nume_videoclip = nume_videoclip
		self.autor_videoclip = autor_videoclip
		self.stare_descarcare = stare_descarcare  
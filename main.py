from pytube import YouTube
from pytube import Playlist
from pytube.helpers import safe_filename
from moviepy.video.io.VideoFileClip import *
import tkinter
import os
import re
import PySimpleGUI as sg

isPlaylist = False

def bulk_download(videosUrls, tries,maxTries):
	print("Iniciando download da(s) musica(s), tentativa número " + str(tries))
	dumpList = []
	path = os.path.abspath(os.getcwd())
	for video in videosUrls:
		try:
			yt = YouTube(video)
			title = yt.title
			print("Baixando \'" + title + "\'")
			audioStream = yt.streams
			audioStream[0].download(path + "\\tmp\\")
			print("Video baixado")
			print("Convertendo para mp3")
		
			mp4_file = safe_filename(yt.title) + ".mp4"
			mp3_file = safe_filename(yt.title) + ".mp3"
			
			videoClip =  VideoFileClip(path + "\\tmp\\" + mp4_file)
			audioClip = videoClip.audio
		
			audioClip.write_audiofile(path + "\\tmp\\" + mp3_file,logger=None)
			audioClip.close()
			videoClip.close()
			print("Video convertido para mp3\nApagando video original")
			
			if os.path.exists(path + "\\tmp\\" + mp4_file):
				os.remove(path + "\\tmp\\" + mp4_file)		
			else:
				print("The file does not exist")
		except:
			print("Download sem sucesso, tentativas: " + str(tries) + " de " + maxTries )
			dumpList.append(video)
		yt = ''
		url = ''
	
	if len(dumpList) > 0 and tries < int(maxTries):
		nTries = tries + 1
		bulk_download(dumpList, nTries, maxTries) 
	if tries >= int(maxTries) and len(dumpList) > 0:
		createDump(dumpList)

def createDump(dumpList):
	f = open("dump.txt", "a")
	for video in dumpList:
		f.write(video.split('\n', 1)[0] + '\n')
	f.close()

def getVideosFromPlaylist(link, maxTries):
	URL = link
	playlist = Playlist(URL)
	playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

	print(len(playlist.video_urls))
	videosUrls = []
	for url in playlist.video_urls:
		print(url)
		videosUrls.append(url)
	print("------------------------------------------")
	bulk_download(videosUrls,0,maxTries)

def getVideosFromText(link,maxTries):
	fileName = link
	videosUrls = []
	f = open(fileName,"r")
	link = f.readline()
	while link != "":
		print(link)
		videosUrls.append(link)
		link = f.readline()
	bulk_download(videosUrls,0,maxTries)

def getVideoFromLink(link,maxTries):
	URL = link
	videosUrls = []
	videosUrls.append(URL)
	bulk_download(videosUrls,0,maxTries)

os.chmod(os.path.abspath(os.getcwd()) + "\\main.py", 0o777)
#os.remove( os.path.abspath(os.getcwd()) + "\\tmp\\"+"かぐや様は告らせたい？～天才たちの恋愛頭脳戦～ OP Full『DADDY! DADDY! DO!鈴木雅之 (feat 鈴木愛理)』Drum Cover (叩いてみた).mp4")

def managerSelect(type,link,maxTries):
	if os.path.exists((os.path.abspath(os.getcwd()) + "\\tmp")) == False:
		os.mkdir((os.path.abspath(os.getcwd()) + "\\tmp"))
	if type == "Playlist":
		getVideosFromPlaylist(link,maxTries)
	elif type == "Texto": 
		getVideosFromText(link,maxTries)
	else: 
		getVideoFromLink(link,maxTries)

	print("Operação concluida.")


sg.theme('BluePurple')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Insira link de uma musica ou uma playlist do Youtube')],
			[sg.Text('Selecione o tipo: '),sg.Combo(["Musica","Playlist"],key="combo")],
			[sg.Text('Numero maximo de tentativas de download'), sg.InputText(key="maxTries")],
            [sg.Text('Insira o link ou local do arquivo'), sg.InputText(key="link")],
            [sg.Button('Avançar'), sg.Button('Cancel')],
            [sg.Output(size=(80,10))] 
            ]

# Create the Window
window = sg.Window('Download de musica', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	# if user closes window or clicks cancel
	if event == sg.WIN_CLOSED or event == 'Cancel':
		break

	if event == 'Avançar':
		managerSelect(values["combo"],values["link"],values["maxTries"])
  	
    #print('You entered ', values[0])
window.close()

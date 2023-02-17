import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse

# Función para transformar oraciones con 
# tildes a sin-tildes, y llevarlas a 
# minúsculas. 
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    s = s.lower()
    return s

# La siguiente función es empleada para 
# tomar y reconocer comandos extraidos 
# como texto desde el modulo de 
# speech_recognition
def takeCommand():

	r = sr.Recognizer()

	# Usa el micrófono predeterminado 
	# para registrar un mensaje
	with sr.Microphone() as source:
		print('Escuchando')
		
		# Segundos que espera el programa 
		# para considerar una frase como completa
		r.pause_threshold = 0.7
		# Sensibilidad del micrófono (influye 
		# en lo que reconoce como silencio)
		# se sugiere entre 50 y 4000
		r.energy_threshold = 2500
		audio = r.listen(source)
		
		
		# Prueba si el audio proporcionado 
		# es reconocido por el modulo, de no serlo 
		# produce una excepción
		try:
			print("Reconociendo")
			
			# Se usa como método un reconocimiento en línea 
			# dado por Google, límitando el programa a 
			# trabajar con conexión a internet
			Query = r.recognize_google(audio, language='es-VE', show_all=False)
			# Transforma el comando ingresado a un string 
			# en minúsculas y sin tildes
			Query = normalize(Query)
			print("El comando ingresado fue: ", Query)
			
		except Exception as e:
			print(e)
			print("No se reconoció, intente de nuevo")
			return "None"
		
		return Query

# La siguiente función se encarga de transformar mensajes
# de texto a voz. Con esto habla 'SAIL'
def speak(audio):
	
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	
	# En la siguiente línea se selecciona las propiedades 
	# de la voz. Se selecciona a partir de las voces 
	# instaladas en el sistema operativo, para windows 
	# trabaja con los lenguajes con soporte de TTS 
	# instalados
	engine.setProperty('voice', voices[1].id)
	# La siguiente línea ajusta la velocidad de la voz
	engine.setProperty('rate', 175)
	# Método para la lectura del texto
	engine.say(audio)
	# Muestra en pantalla el audio reproducido
	print(audio)
	
	# Espera mientras se ingresan comandos
	engine.runAndWait()

def tellDay():
	
	# Esta función dice el día actual
	day = datetime.datetime.today().weekday() + 1
	
	# El siguiente diccionario sirve para traducir 
	# el día obtenido de forma númerica en la 
	# línea anterior a su equivalente en texto
	Day_dict = {1: 'Lunes', 2: 'Martes',
				3: 'Miércoles', 4: 'Jueves',
				5: 'Viernes', 6: 'Sábado',
				7: 'Domingo'}
	
	if day in Day_dict.keys():
		day_of_the_week = Day_dict[day]
		print(day_of_the_week)
		speak("Hoy es " + day_of_the_week)


def tellTime():
	
	# Este método da la fecha y hora actual
	time = str(datetime.datetime.now())
	# 'time' se presenta de la siguiente
	# forma: "2020-06-05 17:50:14.582630"
	# Se secciona para la lectura
	hour = time[11:13]
	min = time[14:16]
	speak("Son las " + hour + "horas y " + min + "minutos")

def Hello():
	
	# Esta función sirve como mensaje inicial 
	# del asistente al ejecutarse el código
	speak("Saludos estimado usuario. Digame en que puedo ayudarle")


def Take_query():

	# Llamando al mensaje de inicio de 'SAIL'
	Hello()
	# Definiendo algunos grupos de palabras
	# Para poder activar una rutina con 
	# varias frases
	identidad=['dime tu nombre', 'como te llamas', 'con quien hablo']
	despedida=['chao', 'adios', 'hasta luego']
	# El siguiente loop infinito toma los 
	# comandos continuamente hasta que se 
	# pida salir o se cancele el programa
	# Nótese que para maximizar las 
	# posibilidades de que el comando 
	# introducido sea igual a los strings 
	# preparados para el programa, todos 
	# se encuentran en minúsculas y sin 
	# tildes
	while(True):

		query=takeCommand()
		if "busca en google" in query:
			speak("Abriendo Google ")
			# Busca en google solo lo que está a la derecha de "busca en google"
			query = query.replace("busca en google", "")
			url = "https://www.google.com.tr/search?q={}".format(query)
			webbrowser.open(url)
			continue

		elif "busca en youtube" in query:
			speak("Abriendo Youtube ")
			# Busca en google solo lo que está a la derecha de "busca en google"
			query = query.replace("busca en youtube", "")
			input = urllib.parse.urlencode({'search_query': query})
			html = urllib.request.urlopen("http://www.youtube.com/results?" + input)
			video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
			webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
			continue
			
		elif "que dia es" in query:
			tellDay()
			continue
		
		elif "dime la hora" in query:
			tellTime()
			continue
		
		# Este caso sale y termina el programa
		elif (any(word in query for word in despedida)):
			speak("Chao.")
			exit()
		
		# Por si se quiere una busqueda desde Wikipedia
		elif "busca en wikipedia" in query:
			
			speak("Buscando en wikipedia ")
			query = query.replace("busca en wikipedia", "")
			# Busca en wikipedia en español
			wikipedia.set_lang('es')
			# Entrega las primeras 2 líneas de Wikipedia
			print(query)
			result = wikipedia.summary(query, sentences=2)
			speak("De acuerdo a wikipedia")
			speak(result)
		
		elif (any(word in query for word in identidad)):
			speak("Soy SAIL. Tu asistente virtual")
		
		elif "dolar" in query:
			try:
				page = urllib.request.urlopen("https://www.bcv.org.ve")
				
			except:
				print("Error")
			# Busca el precio del dólar
			soup = BeautifulSoup(page, 'html.parser')
			content_lis = soup.find("div", {"id": "dolar"})
			dolar = content_lis.div.strong.text.strip()
			# Cambia el separador decimal del dólar a . 
			# y lo redondea a 4 decimales
			dolar = str(round(float(dolar.replace(',', '.')),4))
			speak("El precio del dólar según el BCV es: " + dolar)

if __name__ == '__main__':
	
	# main para la ejecución
	# de las funciones
	Take_query()
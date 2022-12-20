# -*- Coding: utf-8 -*-
import speech_recognition as sr
import pyaudio
import wave
#frame
import numpy as np



class AudioHelp(object):
    """ Clase para grabar, reproducir y reconocer audio en texto. """

    def __init__(self, chunk=3024 , channel =1):
        self.CHUNK = chunk
        self.CHUNK2 = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channel
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.P_AUD = pyaudio.PyAudio()
        self.FRAMES = []
        self.STATUS = 1
        #parameter frame
        self.pause = False

        self.STREAM = self.P_AUD.open(
            format=self.FORMAT, 
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            frames_per_buffer=self.CHUNK
        )
        #self.start_plot()

    def start_plot(self):
        while not self.pause:
            data = self.STREAM.read(self.CHUNK2)
            data_int = np.frombuffer(data, dtype='h')
            data_np = np.array(data_int, dtype='h')    
            if 1000 <= np.amax(data_np) <= 4033:
              print("estas hablando= " + str(np.amax(data_np)))

    def start_recording(self, url_path, callback_refresh, callback_final):
        """ 
            Método para comenzar grabación con pyaudio. 
            callback_refresh: Método para hacer el refresco de nuestra interfaz.
            callback_final: Método para indicar que la grabación ya se guardo y se puede hacer el siguiente paso.
        """
        self.STATUS = 1
        self.FRAMES = []
        stream = self.P_AUD.open(
            format=self.FORMAT, 
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            frames_per_buffer=self.CHUNK
        )
        # INICIANDO GRABACION
        while self.STATUS == 1:
            # print("grabando ...")
            data = stream.read(self.CHUNK)
            self.FRAMES.append(data)
            callback_refresh()

        stream.close()

        wf = wave.open(url_path, 'wb')  # NAME URL_PATH
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.P_AUD.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.FRAMES))
        wf.close()

        self.P_AUD.terminate()
        callback_final()



    def stop_recording(self):
        """ Método para cambiar el estado de grabación a False. """
        self.STATUS = 0

    def play_audio(self, url_path):
        """ Método para reproducir audio en una ruta especifica. """
        rf = wave.open(url_path, "rb")

        stream = self.P_AUD.open(
            format=self.P_AUD.get_format_from_width(rf.getsampwidth()),  
            channels=rf.getnchannels(),  
            rate=rf.getframerate(),  
            output=True
        )

        data = rf.readframes(self.CHUNK)
        # Reproducir Audio
        while data:  
            stream.write(data)  
            data = rf.readframes(self.CHUNK)  
  
        stream.stop_stream()  
        stream.close()  
        self.P_AUD.terminate()
    

    def start_recording2(self, url_path, callback_refresh, callback_final):
        """ 
            Método para comenzar grabación con pyaudio. 
            callback_refresh: Método para hacer el refresco de nuestra interfaz.
            callback_final: Método para indicar que la grabación ya se guardo y se puede hacer el siguiente paso.
        """
        self.STATUS = 1
        self.FRAMES = []
        stream = self.P_AUD.open(
            format=self.FORMAT, 
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            frames_per_buffer=self.CHUNK
        )
        # INICIANDO GRABACION
        for i in range(0, int(self.RATE/ self.CHUNK * self.RECORD_SECONDS)):
            # print("grabando ...")
            data = stream.read(self.CHUNK)
            self.FRAMES.append(data)
        #    callback_refresh()
        
        stream.close()

        wf = wave.open(url_path, 'wb')  # NAME URL_PATH
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.P_AUD.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.FRAMES))
        wf.close()

        self.P_AUD.terminate()
        callback_final()


    def stop_recording(self):
        """ Método para cambiar el estado de grabación a False. """
        self.STATUS = 0

    def play_audio(self, url_path):
        """ Método para reproducir audio en una ruta especifica. """
        rf = wave.open(url_path, "rb")

        stream = self.P_AUD.open(
            format=self.P_AUD.get_format_from_width(rf.getsampwidth()),  
            channels=rf.getnchannels(),  
            rate=rf.getframerate(),  
            output=True
        )

        data = rf.readframes(self.CHUNK)
        # Reproducir Audio
        while data:  
            stream.write(data)  
            data = rf.readframes(self.CHUNK)  
  
        stream.stop_stream()  
        stream.close()  
        self.P_AUD.terminate()
    

    def read_audio(self, url_path, language='es-ES'):
        """ Método para leer un audio y devolver el texto. """
        try:
            text = None
            url_path = f"{url_path}".format(url_path=url_path)
            r = sr.Recognizer()
            with sr.AudioFile(url_path) as source:
                audio = r.listen(source)
                text = str(r.recognize_google(audio, language=language))
            
            return text
        except Exception as e:
            return e


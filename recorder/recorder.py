# -*- Coding: utf-8 -*-
# Utiles
from .utils import file_exists, random_name, write_file, remove_file
from .models import Audio  # IMPORTAMOS .models.py y asignamos
from .services import AudioService
from .plugins.audio_help2 import AudioHelp
from config import Settings, Routes 

class Record():
    """ Clase de grabación de audio. """
    def __init__(self, interface):
        self.routes = Routes()
        self.interface = interface
        self.audio_h = AudioHelp() # LLAMANDO A LA CLASE DE  AUDIO_HELP.PY
        self.listAudios()
        self.filename = None


    def saveAudio(self, filename, text):
        """ Método para guardar registro de audios. """
        try:
            # Guardar archivos
            write_file(
                base_url=self.routes.base_text_audio_url,
                filename=filename + ".txt", 
                content=text.encode()
            )
            # Guardar registros
            audio = Audio(filename, text[:30])
            audio_service = AudioService(self.routes.table_name)
            audio_service.create_audio(audio)
            # Refrescar vista
            self.listAudios()
            self.interface.showMessageInfo("Audio guardado en el sistema.")

        except Exception as e:
            self.interface.showMessageInfo("Error al guardar los archivos.")
            return e


    def listAudios(self):
        """ Método para listar grabaciones. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        for audio in audios:
            audio = audio.update(
                dict(
                    methods=[
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_delete),
                            action=self.deleteAudio
                        ),
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_play),
                            action=self.playAudio
                        )
                    ]
                )
            )

        self.interface.updateTable(
            headers=Audio.schema() + ["Acciones"],
            data=audios, 
        )

    def getAudio(self, uid):
        """ Método para obtener un audio por UID. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        audio = [audio for audio in audios if audio['uid'] == uid]
        if audio == []:
            return None
        return audio[0]


    def recordAudio(self, callback):
        """ Método de grabación de audio. """
        try:
            self.filename = random_name("record") # SEGUIDO DE LA FECHA
            url_path = self.routes.base_audio_url + self.filename + ".wav"
            self.interface.updateInfoBox("Grabando ...")
            #self.audio_h.start_recording(url_path=url_path, callback_refresh=callback, callback_final=self.finalAudio)
            self.audio_h.start_recording2(url_path=url_path , callback_refresh=callback, callback_final=self.finalAudio)
                   
        except Exception as e:
            self.interface.showMessageInfo("Error de grabación.")
        print("GRABANDO AUDIO")

    def stopAudio(self):
        """ Método de grabación de audio. """
        try:
            self.audio_h.stop_recording()
        except:
            self.interface.showMessageInfo("Error de grabación.")
        print("Detener audio")

    def finalAudio(self):
        """ Método de finalización de grabación. """
        try:
            if self.filename is not None:
                text = self.audio_h.__class__().read_audio(
                    url_path=self.routes.base_audio_url + self.filename + ".wav",
                    language=Settings.language    
                )
                self.interface.updateInfoBox("Has dicho: \n{}".format(text))
                self.saveAudio(filename=self.filename, text=text)
        except:
            self.interface.showMessageInfo("Error de grabación.")
        finally:
            self.filename = None



    def deleteAudio(self, uid):
        """ Método para eliminar audio. """
        audio_service = AudioService(self.routes.table_name)
        audio = self.getAudio(uid)
        if audio:
            audio_service.delete_audio(audio["uid"])
            remove_file(self.routes.base_audio_url + audio["filename"] + ".wav")
            remove_file(self.routes.base_text_audio_url + audio["filename"] + ".txt")
            self.listAudios()
            self.interface.showMessageInfo("Audio eliminado del sistema.") 
        else:
            self.interface.showMessageInfo("El uid no existe en el sistema.") 


    def playAudio(self, uid):
        """ Método para reproducir audio. """
        try:
            audio = self.getAudio(uid)
            if audio:
                audio_url = self.routes.base_audio_url + audio["filename"] + ".wav" 
                if file_exists(audio_url):
                    audio_h = self.audio_h.__class__(chunk=1024)
                    audio_h.play_audio(audio_url)
                else:
                    self.interface.showMessageInfo("Audio no encontrado.")
            else:
                self.interface.showMessageInfo("Audio no seleccionado.")

        except Exception as e:
            self.interface.showMessageInfo("No se puede reproducir el Audio.")
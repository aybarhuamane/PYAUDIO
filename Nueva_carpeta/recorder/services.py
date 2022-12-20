# -*- Coding: utf-8 -*-
import csv
import os

from .models import Audio

class AudioService():
    """ Clase de servicios para la tabla audio. """
    
    def __init__(self, table_name):
        self.table_name = table_name

    def create_audio(self, audio):
        with open(self.table_name, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Audio.schema())
            writer.writerow(audio.to_dict())

    def list_audios(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=Audio.schema())

            return list(reader)

    def delete_audio(self, uid_audio):
        audios = self.list_audios()
        delete_audios = []
        for audio in audios:
            if audio['uid'] == uid_audio:
                continue
            else:
                delete_audios.append(audio)

        self._save_to_disk(delete_audios)

    def _save_to_disk(self, audios):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Audio.schema())
            writer.writerows(audios)

        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
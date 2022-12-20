"""
    Notebook for streaming data from a microphone in realtime

    audio is captured using pyaudio
    then converted from binary data to ints using struct
    then displayed using matplotlib

    scipy.fftpack computes the FFT

    if you don't have pyaudio, then run

    pip install pyaudio

    note: with 2048 samples per chunk, I'm getting 20FPS
    when also running the spectrum, its about 15FPS
"""
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import threading
# from pyqtgraph.Qt import QtGui, QtCore
# import pyqtgraph as pg
import struct
# from scipy.fftpack import fft
import sys
import time
import datetime
import wave
import time


class AudioStream(object):
    def __init__(self):

        self.FRAMES = []
        # stream constants
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False
        self.CHUNK2 = 1024
        self.STATUS = 0
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = str(datetime.datetime.now().strftime("%y%m%d_%H%M%S")) + "_output.wav"
        self.p = pyaudio.PyAudio()
        self.ESTADO = 0
        # stream object

        self.STREAM = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        #print("* recording")

        # self.init_plots()
        self.start_frame()

    def start_plot(self):

        print('stream started')
        frame_count = 0
        start_time = time.time()

        while not self.pause:

            # Leendo valores del microfono
            data = self.STREAM.read(self.CHUNK)
            # Convirtiendo estos valores a entero para poder usarlos
            # data_int = struct.unpack(str(2 * self.CHUNK) + 'B', data)
            data_int = np.frombuffer(data, dtype='h')
            # print("int : "+str(data_int))
            # Poniendo los valores enteros de data_int en un arreglo
            # data_np = np.array(data_int, dtype='b')[::2] + 128
            data_np = np.array(data_int, dtype='h')

            if 1000 <= np.amax(data_np) <= 4033:
                print("estas hablando= " + str(np.amax(data_np)))
                self.ESTADO = 1
                self.start_frame()
            '''
            elif  np.amax(data_np) <= 1000:
                t = threading.Timer(10, self.stop_frame())
                t.start()
            '''

    def start_frame(self):
     
        FRAMES = []
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            # output=True,
            frames_per_buffer=self.CHUNK)

        # while  self.ESTADO == 1:

         #while not self.pause:

        data = stream.read(self.CHUNK)
        data_int = np.frombuffer(data, dtype='h')
        data_np = np.array(data_int, dtype='h')

        if 1000 <= np.amax(data_np) <= 4033:
            print("estas hablando= " + str(np.amax(data_np)))
            #self.ESTADO = 1
            #self.start_frame()
            print(" recording 5 seg" )
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):

                data = stream.read(self.CHUNK)
                FRAMES.append(data)
            print(" record end ")
            #print("* done recording")
            stream.stop_stream()
            stream.close()
            self.p.terminate()
            wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(FRAMES))
            wf.close()



    # def stop_frame(self):
    #     self.ESTADO = 0
    #     print("RETURN STATUS 0 ")


if __name__ == '__main__':
    while True:
        AudioStream()



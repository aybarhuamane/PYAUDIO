# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import  QApplication
from recorder import Record, RecordingAppInterface
#from framer.rec import AudioStream

class Aplicacion(QApplication):
	
	def __init__(self):
		
		QApplication.__init__(self, sys.argv)
		interface = RecordingAppInterface()
		record = Record(interface)
		interface.btnRecord.param = self.refresh_app
		#record.recordAudio
		#Record.recordAudio() # new
		interface.btnRecord.setAction(record.recordAudio)
		interface.btnStop.setAction(record.stopAudio)
		#AudioStream()
		sys.exit(self.exec_())
        
	def refresh_app(self):
		self.processEvents()
		
		

def main():
	app = Aplicacion()
	
	return 0


if __name__ == '__main__':
    main()
	
	
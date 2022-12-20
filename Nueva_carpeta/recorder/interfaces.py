# -*- Coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel,  QGridLayout
from .plugins.pyqt5_custom import MessageCustom, InputCustom, ButtonCustom, BoxInfoCustom, TableWidgetCustom, MultipleLayoutWidgetCustom
from config import Settings, Routes

class RecordingAppInterface(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Grabadora Custom'
        self.left = 0
        self.top = 0
        self.width = 1050
        self.height = 550
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createForm() 
        self.infoGroupBox = BoxInfoCustom(title=".:: Información de grabación ::.")
        self.tableWidget = TableWidgetCustom()
 
        # BOX - LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.formGroupBox) 
        self.layout.addWidget(self.infoGroupBox) 
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
        # MOSTRAR WIDGET
        self.show()

    def createForm(self):
        layout = QFormLayout()

        self.formGroupBox = QGroupBox("Grabación de audio")
        self.btnRecord = ButtonCustom("Grabar ", styles=Settings.style_btn_info, path_icon=Routes.icon_microphone)
        self.btnStop = ButtonCustom("Detener ", styles=Settings.style_btn_danger, path_icon=Routes.icon_stop)
        self.btnClean = ButtonCustom(path_icon=Routes.icon_clean, styles=Settings.style_btn_danger)
        self.btnClean.setAction(self.cleanInfoBox)
        self.btnClean.setSize(28, 28)

        self.btnActions = ButtonCustom("")

        layout.addRow(MultipleLayoutWidgetCustom(elements=[self.btnRecord, self.btnStop, self.btnClean]))

        self.formGroupBox.setLayout(layout)  

    def updateInfoBox(self, info=None, styles=None):
        self.infoGroupBox.updateBox(info=info, styles=styles)

    def cleanInfoBox(self):
        self.infoGroupBox.cleanBox()
    
    def updateTable(self, headers=None, data=None):
        self.tableWidget.updateInfoTable(headers=headers, data=data)
    
    def showMessageInfo(self, text):
        msgBox = MessageCustom()
        msgBox.showMessage(text)

    


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Orientation(object):
    def setupUi(self, Orientation):
        Orientation.setObjectName("Orientation")
        Orientation.resize(666, 380)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/icons/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Orientation.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Orientation)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Orientation)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Orientation)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Orientation)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Orientation)
        self.buttonBox.accepted.connect(Orientation.accept)
        self.buttonBox.rejected.connect(Orientation.reject)
        QtCore.QMetaObject.connectSlotsByName(Orientation)

    def retranslateUi(self, Orientation):
        _translate = QtCore.QCoreApplication.translate
        Orientation.setWindowTitle(_translate("Orientation", "Orientation"))
        self.textBrowser.setHtml(_translate("Orientation", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">La evaluación de la asignatura Complementos de Compilación, inscrita en el programa del 4to año de la Licenciatura en Ciencia de la Computación de la Facultad de Matemática y Computación de la Universidad de La Habana, consiste este curso en la implementación de un compilador completamente funcional para el lenguaje COOL.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">COOL (</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">C</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">lassroom </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">bject-</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">riented </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; text-decoration: underline;\">L</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">anguage) es un pequeño lenguaje que puede ser implementado con un esfuerzo razonable en un semestre del curso. Aun así, COOL mantiene muchas de las características de los lenguajes de programación modernos, incluyendo orientación a objetos, tipado estático y manejo automático de memoria.</span></p></body></html>"))
        self.label.setText(_translate("Orientation", "<html><head/><body><p align=\"center\">Orientation</p></body></html>"))

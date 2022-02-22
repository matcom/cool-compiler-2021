# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uis/orientation.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Orientation(object):
    def setupUi(self, Orientation):
        Orientation.setObjectName("Orientation")
        Orientation.resize(670, 336)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./uis/../../img/icons/python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">The evaluation of the subject Compilation Complements, enrolled in the program of the 4th year of the Computer Science of the Faculty of Mathematics and Computing of the University of Havana, this course consists of the implementation of a fully functional compiler for COOL language.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">COOL (</span><span style=\" font-size:16pt; text-decoration: underline;\">C</span><span style=\" font-size:16pt;\">lassroom </span><span style=\" font-size:16pt; text-decoration: underline;\">O</span><span style=\" font-size:16pt;\">bject-</span><span style=\" font-size:16pt; text-decoration: underline;\">O</span><span style=\" font-size:16pt;\">riented </span><span style=\" font-size:16pt; text-decoration: underline;\">L</span><span style=\" font-size:16pt;\">anguage) is a small language that can be implemented with reasonable effort in one semester of the course. Still, COOL maintains many of the features of modern programming languages, including object orientation, static typing, and automatic memory management.</span></p></body></html>"))
        self.label.setText(_translate("Orientation", "<html><head/><body><p align=\"center\">Orientation</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Orientation = QtWidgets.QDialog()
    ui = Ui_Orientation()
    ui.setupUi(Orientation)
    Orientation.show()
    sys.exit(app.exec_())

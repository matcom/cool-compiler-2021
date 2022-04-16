# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uis/help.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(733, 527)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./uis/../../img/icons/python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Help.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Help)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Help)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Help)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Help)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Help)
        self.buttonBox.accepted.connect(Help.accept)
        self.buttonBox.rejected.connect(Help.reject)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "Help"))
        self.textBrowser.setHtml(_translate("Help", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">To compile a file with a COOL (</span><span style=\" font-size:14pt; font-weight:600; text-decoration: underline;\">C</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">lassroom </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">bject-</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600; text-decoration: underline;\">O</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">riented </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600; text-decoration: underline;\">L</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">anguage</span><span style=\" font-size:14pt; font-weight:600;\">) program follow the steps below</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">1. Write a valid program in COOL. For example:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">class  Main  inherits  IO  {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">    main()  :  SELF_TYPE  {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">        out_string(quot;Hello World!!!\\nquot;)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">    };</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">};</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">2. </span><span style=\" font-size:14pt;\">To carry out the compilation process, continue with \'Analyze/Run (F5)\'</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:14pt; color:#000000;\"> </span><span style=\" font-size:14pt;\">You will see the results in the respective tabs</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">3. Y</span><span style=\" font-size:14pt;\">ou can load (Ctrl+O) the COOL programs and save the results in different formats for future use</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">4. T</span><span style=\" font-size:14pt;\">he options \'Help (F1)\', \'Orientation\'(F7), \'Report\'(F8) and \'About authors (F11)\' are also offered.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Orientation: Show the orientation of the compiler.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Report: </span><span style=\" font-size:14pt;\">Shows the report proposed by the developers</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">About authors (F11): S</span><span style=\" font-size:14pt;\">how basic developer information</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Help (F1): Show this help.</span></p></body></html>"))
        self.label.setText(_translate("Help", "<html><head/><body><p align=\"center\">Help</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Help = QtWidgets.QDialog()
    ui = Ui_Help()
    ui.setupUi(Help)
    Help.show()
    sys.exit(app.exec_())

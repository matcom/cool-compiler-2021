# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './uis/about_authors.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutAuthors(object):
    def setupUi(self, AboutAuthors):
        AboutAuthors.setObjectName("AboutAuthors")
        AboutAuthors.resize(871, 604)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./uis/../../img/icons/python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutAuthors.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(AboutAuthors)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutAuthors)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(AboutAuthors)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(AboutAuthors)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(AboutAuthors)
        self.buttonBox.accepted.connect(AboutAuthors.accept)
        self.buttonBox.rejected.connect(AboutAuthors.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutAuthors)

    def retranslateUi(self, AboutAuthors):
        _translate = QtCore.QCoreApplication.translate
        AboutAuthors.setWindowTitle(_translate("AboutAuthors", "About Authors"))
        self.textBrowser.setHtml(_translate("AboutAuthors", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Students :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\"> Juan José López Martínez</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\">                   Juan Carlos Esquivel Lamis</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7pt; color:#000000;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\">                   Ariel Plasencia Díaz</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; color:#005500;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Emails :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\"> j.lopez2@estudiantes.matcom.uh.cu</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7pt; color:#000000;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\">               j.esquivel@estudiantes.matcom.uh.cu</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7pt; color:#000000;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\">               a.plasencia@estudiantes.matcom.uh.cu</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; color:#005500;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Faculty :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\"> MatCom</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; color:#005500;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Profession :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\"> Computer Science</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; color:#005500;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Course :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\"> Complements of Compilation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; color:#005500;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:600; color:#000000;\">Date :</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#005500;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; color:#000000;\">2022</span></p></body></html>"))
        self.label.setText(_translate("AboutAuthors", "<html><head/><body><p align=\"center\">About Authors</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AboutAuthors = QtWidgets.QDialog()
    ui = Ui_AboutAuthors()
    ui.setupUi(AboutAuthors)
    AboutAuthors.show()
    sys.exit(app.exec_())

import os
import sys
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from uis.help import Ui_Help
from uis.orientation import Ui_Orientation
from uis.about_authors import Ui_AboutAuthors
from uis.compiler_COOL import Ui_COOLCompiler

from utils.errors import *
from lexing.lexer import Lexer
from parsing.parser import Parser
from semantic.semantic import SemanticAnalyzer
from utils.notification import NotificationWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_COOLCompiler()
        self.ui.setupUi(self)

        self.ui.actionNewCode.triggered.connect(self.new_code)
        self.ui.actionLoadCode.triggered.connect(self.load_code)
        self.ui.actionCode.triggered.connect(self.save_code)
        self.ui.actionLexer.triggered.connect(self.save_lexer)
        self.ui.actionParser.triggered.connect(self.save_parser)
        self.ui.actionContext.triggered.connect(self.save_context)
        self.ui.actionScope.triggered.connect(self.save_scope)
        self.ui.actionCIL.triggered.connect(self.save_cil)
        self.ui.actionMIPS.triggered.connect(self.save_mips)
        self.ui.actionErrors.triggered.connect(self.save_errors)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionOrientation.triggered.connect(self.orientation)
        self.ui.actionReport.triggered.connect(self.report)
        self.ui.actionAboutAuthors.triggered.connect(self.about_authors)

        self.new_code()

    def clear_windows(self):
        self.ui.textLexer.setPlainText('')
        self.ui.textParser.setPlainText('')
        self.ui.textContext.setPlainText('')
        self.ui.textScope.setPlainText('')
        self.ui.textCIL.setPlainText('')
        self.ui.textMIPS.setPlainText('')
        self.ui.textErrors.setPlainText('')
    
    def update_status(self):
        self.ui.tabCode.setStatusTip(self.path if self.path else '* New code')

    def new_code(self):
        self.path = None
        self.ui.textCode.setPlainText('')
        self.update_status()
        self.ui.tabCOOLMenu.setTabEnabled(0, True)
        self.ui.tabCOOLMenu.setCurrentIndex(0)
        self.clear_windows()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def load_code(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Load code', '../examples/', '*.cl')

        if not path:
            return

        try:
            with open(path, 'r') as file:
                code = file.read()
        except Exception as exception:
            self.DialogCritical(str(exception))
        else:
            self.path = path
            self.ui.textCode.setPlainText(code)
            self.update_status()
            self.clear_windows()
    
    def save(self, path, text):
        try:
            with open(file=path, mode='w') as file:
                file.write(text)
        except Exception as exception:
            self.dialog_critical(str(exception))
        else:
            self.path = path
            self.update_status()

    def save_code(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save code', '../examples/', '*.cl')
        code = self.ui.textCode.toPlainText()

        if not path:
            return
        elif not path.endswith('.cl'):
            path += '.cl'
        
        self.save(path, code)
    
    def save_lexer(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save lexer', '../examples/', '*.lexer')
        lexer = self.ui.textLexer.toPlainText()

        if not path:
            return
        elif not path.endswith('.lexer'):
            path += '.lexer'
        
        self.save(path, lexer)

    def save_parser(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save parser', '../examples/', '*.parser')
        parser = self.ui.textParser.toPlainText()

        if not path:
            return
        elif not path.endswith('.parser'):
            path += '.parser'
        
        self.save(path, parser)

    def save_context(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save context', '../examples/', '*.context')
        context = self.ui.textContext.toPlainText()

        if not path:
            return
        elif not path.endswith('.context'):
            path += '.context'
        
        self.save(path, context)

    def save_scope(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save scope', '../examples/', '*.scope')
        scope = self.ui.textScope.toPlainText()

        if not path:
            return
        elif not path.endswith('.scope'):
            path += '.scope'
        
        self.save(path, scope)

    def save_cil(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save cil', '../examples/', '*.cil')
        cil = self.ui.textCIL.toPlainText()

        if not path:
            return
        elif not path.endswith('.cil'):
            path += '.cil'
        
        self.save(path, cil)

    def save_mips(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save mips', '../examples/', '*.mips')
        mips = self.ui.textMIPS.toPlainText()

        if not path:
            return
        elif not path.endswith('.mips'):
            path += '.mips'
        
        self.save(path, mips)

    def save_errors(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save errors', '../examples/', '*.errors')
        errors = self.ui.textErrors.toPlainText()

        if not path:
            return
        elif not path.endswith('.errors'):
            path += '.errors'
        
        self.save(path, errors)

    def go_dialog(self, id):
        self.ui.tabCOOLMenu.setTabEnabled(id, True)
        self.ui.tabCOOLMenu.setCurrentIndex(id)

    def run(self):
        self.clear_windows()
        code = self.ui.textCode.toPlainText()
        NotificationWindow.info('Analizando', 
            '''
                <html>
                    <body>
                        <span style="color:gray;">
                            <p>El código está siendo analizado en estos momentos.</p>
                            <p>Por favor, espere unos instantes.</p>
                            <p></p>
                        </span>
                    </body>
                </html>
            ''')
        
        ok, lexer = self.lexing(code)
        if ok:
            ok, ast = self.parsing(code, lexer)
            if ok:
                ok, ast, context, scope = self.semantic(ast)
                if ok:
                    # TODO : la parte de generacion de codigo
                    pass
                    # self.code_generation(ast, context, scope)

                    # NotificationWindow.success('Listo', 
                    #     '''
                    #         <html>
                    #             <body>
                    #                 <span style="color:green;">
                    #                     <p>El análisis ha termiando.</p>
                    #                     <p>Todos los resultados están listos.</p>
                    #                     <p></p>
                    #                 </span>
                    #             </body>
                    #         </html>
                    #     ''')
                    # self.go_dialog(6)

    def code_generation(self, ast, context, scope):
        # code_generation = CodeGeneration(ast, context, scope, '', debug=False)
        # mips_code, cil_ast = code_generation.code_generation()
        
        # self.ui.textCIL.setPlainText(f'{self.ui.textCIL.toPlainText()}{cil_ast}')
        # self.ui.textMIPS.setPlainText(f'{self.ui.textMIPS.toPlainText()}{mips_code}')

        NotificationWindow.success('Listo', 
                '''
                    <html>
                        <body>
                            <span style="color:green;">
                                <p>La generación de código ha termiando.</p>
                                <p>Todos los resultados están listos en las pestañas CIL y MIPS.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''')

    def semantic(self, ast):
        semantic_analyzer = SemanticAnalyzer(ast, '', debug=False)
        ast, context, scope = semantic_analyzer.analyze()

        if len(semantic_analyzer.errors) > 0:
            errors_list = '\n'.join(repr(error) for error in semantic_analyzer.errors)
            self.ui.textErrors.setPlainText(f'{self.ui.textErrors.toPlainText()}{errors_list}')
            NotificationWindow.error('Error', 
                '''
                    <html>
                        <body>
                            <span style=" font-style:italic; color:teal;">
                                <p>Ha ocurrido error(es) en el análisis semántico.</p>
                                <p>Revise la pestaña Errors para más información.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''', callback=lambda: self.help())
            self.go_dialog(7)
            return False, ast, context, scope
        else:
            self.ui.textContext.setPlainText(f'{self.ui.textContext.toPlainText()}{context}')
            self.ui.textScope.setPlainText(f'{self.ui.textScope.toPlainText()}{scope}')
            NotificationWindow.success('Listo', 
                '''
                    <html>
                        <body>
                            <span style="color:green;">
                                <p>El análisis semántico ha termiando.</p>
                                <p>Todos los resultados están listos en las pestañas Context y Scope.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''')
            return True, ast, context, scope

    def parsing(self, code, lexer):
        parser = Parser(lexer=lexer)
        ast = parser(code)

        if len(parser.errors) > 0:
            errors_list = '\n'.join(repr(error) for error in parser.errors)
            self.ui.textErrors.setPlainText(f'{self.ui.textErrors.toPlainText()}{errors_list}')
            NotificationWindow.error('Error', 
                '''
                    <html>
                        <body>
                            <span style=" font-style:italic; color:teal;">
                                <p>Ha ocurrido error(es) en el análisis sintáctico.</p>
                                <p>Revise la pestaña Errors para más información.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''', callback=lambda: self.help())
            self.go_dialog(7)
            return False, ast
        else:
            path = './parsing/parser.out'
            file = open(path)
            parser_list = []
            
            for _ in range(0, 4):
                file.readline()
            while True:
                line = file.readline().strip()
                if line.split(' ')[0] != 'Rule':
                    break
                parser_list.append(line)

            file.close()
            parser_list = '\n'.join(repr(parser) for parser in parser_list)
            self.ui.textParser.setPlainText(f'{self.ui.textParser.toPlainText()}{parser_list}')
            NotificationWindow.success('Listo', 
                '''
                    <html>
                        <body>
                            <span style="color:green;">
                                <p>El análisis sintáctico ha termiando.</p>
                                <p>Todos los resultados están listos en la pestaña Parser.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''')
            # print(ast)
            return True, ast

    def lexing(self, code):
        lexer = Lexer()
        tokens = lexer.tokenizer(code)

        tokens_list = '\n'.join(repr(token) for token in tokens)
        self.ui.textLexer.setPlainText(f'{self.ui.textLexer.toPlainText()}{tokens_list}\n')

        if len(lexer.errors) > 0:
            errors_list = '\n'.join(repr(error) for error in lexer.errors)
            self.ui.textErrors.setPlainText(f'{self.ui.textErrors.toPlainText()}{errors_list}')
            NotificationWindow.error('Error', 
                '''
                    <html>
                        <body>
                            <span style=" font-style:italic; color:teal;">
                                <p>Ha ocurrido error(es) en el análisis lexicográfico.</p>
                                <p>Revise la pestaña Errors para más información.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''', callback=lambda: self.help())
            self.go_dialog(7)
            return False, lexer
        elif len(tokens) == 0:
            error_text = SyntacticError.ERROR % 'EOF'
            self.ui.textErrors.setPlainText(f'{self.ui.textErrors.toPlainText()}{SyntacticError(0, 0, error_text)}')
            NotificationWindow.error('Error', 
                '''
                    <html>
                        <body>
                            <span style=" font-style:italic; color:teal;">
                                <p>Ha ocurrido error(es) en el análisis lexicográfico.</p>
                                <p>Revise la pestaña Errors para más información.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''', callback=lambda: self.help())
            self.go_dialog(7)
            return False, lexer
        else:
            NotificationWindow.success('Listo', 
                '''
                    <html>
                        <body>
                            <span style="color:green;">
                                <p>El análisis lexicográfico ha termiando.</p>
                                <p>Todos los resultados están listos en la pestaña Lexer.</p>
                                <p></p>
                            </span>
                        </body>
                    </html>
                ''')
            return True, lexer

    def exit(self):
        self.close()

    def help(self):
        dialog = QDialog()
        ui_dialog = Ui_Help()
        ui_dialog.setupUi(dialog)
        dialog.exec()

    def orientation(self):
        dialog = QDialog()
        ui_dialog = Ui_Orientation()
        ui_dialog.setupUi(dialog)
        dialog.exec()

    def report(self):
        path = '../doc/report.pdf'
        webbrowser.open_new(path)

    def about_authors(self):
        dialog = QDialog()
        ui_dialog = Ui_AboutAuthors()
        ui_dialog.setupUi(dialog)
        dialog.exec()

def main() -> None:

    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

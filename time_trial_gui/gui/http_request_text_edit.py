from PyQt4 import QtGui
from pygments import highlight, lex
from pygments.lexers import HttpLexer
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
import re


class HttpRequestTextEdit(QtGui.QTextEdit):

    def __init__(self, parent):
        super(HttpRequestTextEdit, self).__init__(parent)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setAcceptRichText(False)
        self.setTabChangesFocus(True)




    def focusOutEvent(self, QFocusEvent):
        self.highlight()

    def highlight(self):
        request = self.toPlainText()
        highlighted = highlight(request, HttpLexer(), HtmlFormatter(full=True, style="friendly"))
        self.setHtml(highlighted)


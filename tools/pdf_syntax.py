"""Selectable, token-coloured PDF code without screenshots or rasterized text.
The underlying source is never rewritten. Long lines soft-wrap for the page;
exact unwrapped files remain in the companion downloads.
"""
import math
from pygments import lex
from pygments.lexers import HtmlLexer,get_lexer_by_name
from pygments.token import Token
from reportlab.platypus import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor

TOKEN_PALETTE={
    Token.Comment:'#58675e',
    Token.Keyword:'#70387d',
    Token.Name.Tag:'#005f57',
    Token.Name.Attribute:'#893c26',
    Token.Name.Builtin:'#304c9e',
    Token.Name.Function:'#70387d',
    Token.Literal.String:'#234e96',
    Token.Literal.Number:'#843867',
    Token.Operator:'#705100',
    Token.Punctuation:'#30433b',
    Token.Text:'#20352c'
}
def token_colour(token):
    while token not in TOKEN_PALETTE and token.parent is not None:token=token.parent
    return TOKEN_PALETTE.get(token,'#20352c')

def source_tokens(source,language="html"):
    tokens=list(lex(source,get_lexer_by_name(language,ensurenl=False,stripnl=False)))
    assert ''.join(value for _,value in tokens)==source,'Syntax tokenization changed the source.'
    return tokens

class SyntaxCodeBlock(Flowable):
    padding=14
    header=28
    leading=12.2
    font_size=8.5
    spaceBefore=12
    spaceAfter=16
    def __init__(self,source='',label='HTML / example',rows=None,continued=False,continues=False,language='html'):
        super().__init__();self.source=source;self.label=label;self.prepared=rows
        self.language=language;self.continued=continued;self.continues=continues;self._cache={}
        self.hAlign='LEFT'
    def _rows(self,width):
        if self.prepared is not None:return self.prepared
        key=round(width,3)
        if key in self._cache:return self._cache[key]
        limit=width-2*self.padding
        rows=[];row=[];used=0
        def push(colour,value):
            if row and row[-1][0]==colour:row[-1]=(colour,row[-1][1]+value)
            else:row.append((colour,value))
        for token,value in source_tokens(self.source,self.language):
            colour=token_colour(token)
            for char in value.expandtabs(2):
                if char=='\n':rows.append(row);row=[];used=0;continue
                advance=pdfmetrics.stringWidth(char,'Mono',self.font_size)
                if row and used+advance>limit:rows.append(row);row=[];used=0
                push(colour,char);used+=advance
        if row or not rows:rows.append(row)
        self._cache[key]=rows;return rows
    def wrap(self,availWidth,availHeight):
        self.width=availWidth;self.rows=self._rows(availWidth)
        self.height=self.header+2*self.padding+len(self.rows)*self.leading+(12 if self.continues else 0)
        return self.width,self.height
    def split(self,availWidth,availHeight):
        rows=self._rows(availWidth)
        available=math.floor((availHeight-self.header-2*self.padding-12)/self.leading)
        if available<min(3,len(rows)):return []
        if available>=len(rows):return [self]
        return [SyntaxCodeBlock(label=self.label,rows=rows[:available],continued=self.continued,continues=True,language=self.language),SyntaxCodeBlock(label=self.label,rows=rows[available:],continued=True,continues=self.continues,language=self.language)]
    def draw(self):
        c=self.canv;c.saveState()
        c.setFillColor(HexColor('#f1f5f0'));c.setStrokeColor(HexColor('#cbd6ca'));c.setLineWidth(.55)
        c.roundRect(0,0,self.width,self.height,5,stroke=1,fill=1)
        c.setStrokeColor(HexColor('#cbd6ca'));c.line(0,self.height-self.header,self.width,self.height-self.header)
        c.setFillColor(HexColor('#4d6156'));c.setFont('Mono',7.2)
        c.drawString(self.padding,self.height-18,self.label+(' / continued' if self.continued else ''))
        y=self.height-self.header-self.padding-self.font_size
        for row in self.rows:
            tx=c.beginText(self.padding,y);tx.setFont('Mono',self.font_size)
            for colour,value in row:tx.setFillColor(HexColor(colour));tx.textOut(value)
            c.drawText(tx);y-=self.leading
        if self.continues:
            c.setFont('Body',6.7);c.setFillColor(HexColor('#58675e'));c.drawRightString(self.width-self.padding,9,'Code continues on the next page')
        c.restoreState()

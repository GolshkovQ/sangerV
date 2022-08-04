from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.glyphs import Text, Rect
import numpy as np

def DrawBokehPlot(seqs,ids,seqPos,inID):
    colors = get_colors(seqs)   ### reference seq is in the seqs[-1]
    seqLen = len(seqs[-1])
    seqNum = len(ids)
    text = [bases for sequenceUnit in list(seqs) for bases in sequenceUnit]
    x = np.arange(1,seqLen+1) + seqPos
    y = np.arange(0,seqNum,1)
    xx, yy = np.meshgrid(x,y)
    gx = xx.ravel()
    gy = yy.flatten()
    recty = gy + 0.5
    source = ColumnDataSource(dict(x=gx, y=gy, recty=recty, text=text, colors=colors))
    x_range = Range1d(seqPos,seqPos+seqLen,bounds='auto')
    p = figure(title=inID,plot_width=30*seqLen,plot_height=40*seqNum,x_range=x_range,y_range=ids,min_border = 0)
    glyph = Text(x="x",y="y",text="text",text_align="center",text_color="black",text_font_size="15px",text_font_style="bold",text_font="Segoe UI")
    rects = Rect(x="x",y="recty",width=1,height=1,fill_color="colors",fill_alpha=0.3,line_color="grey")
    p.add_glyph(source,glyph)
    p.add_glyph(source,rects)
    p.yaxis.visible = True
    return p

def get_colors(seqList):
    seqlen = len(seqList[-1])
    colorbox = list((seqlen*len(seqList))*"C")
    for pos in range(0,len(seqList[0])):
        for seqID in range(0,len(seqList)-1):
            if seqList[seqID][pos] == seqList[-1][pos]:
                colorbox[(len(seqList)-1)*seqlen+pos] = "white"
                colorbox[seqID*seqlen+pos] = "white"
            else:
                colorbox[(len(seqList)-1)*seqlen+pos] = "white"
                colorbox[seqID*seqlen+pos] = "red"
    return colorbox

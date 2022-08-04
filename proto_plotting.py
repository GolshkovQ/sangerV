from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Plot, Grid, Range1d
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot
from bokeh.io import show
import numpy as np

def get_colors(ref,sub):
    refbox = []
    subbox = []
    for i in range(0,len(ref)):
        if ref[i] == sub[i]:
            refbox.append("white")
            subbox.append("white")
        else:
            refbox.append("white")
            subbox.append("red")
    colorbox = refbox + subbox 
    return colorbox

def get_colors(seqList):
    seqlen = len(seqList[-1])
    test = list((seqlen*len(seqList))*"C")
    for pos in range(0,len(seqList[0])):
        for seqID in range(0,len(seqList)-1):
            if seqList[seqID][pos] == seqList[-1][pos]:
                test[(len(seqList)-1)*seqlen+pos] = "white"
                test[seqID*seqlen+pos] = "white"
            else:
                if seqList[seqID][pos] == "-" and seqList[-1][pos] != "-": 
                    ### its a deletion
                    test[(len(seqList)-1)*seqlen+pos] = "white"
                    test[seqID*seqlen+pos] = "blue"
                elif seqList[seqID][pos] != "-" and seqList[-1][pos] == "-":
                    ### its a insertion
                    test[(len(seqList)-1)*seqlen+pos] = "white"
                    test[seqID*seqlen+pos] = "green"
                else:
                    test[(len(seqList)-1)*seqlen+pos] = "white"
                    test[seqID*seqlen+pos] = "red"
    return test

def get_colors2(seqList):
    base = [i for  s in list(seqs) for i in s]
    clrs = {"A":"red","T":"green","C":"blue","G":"orange","-":"gray"}
    colors = [clrs[i] for i in base]
    return colors

querySeqs = "AGTAGTCGTGATGTGCTAATCGTAGCTAGCTGATCGTGC-AGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCA"
subjectSeqs = "AGTAGTCGTGTTGTGCTAATCGTAGCTAGCTGATCGTGCTAACTGATCGTAGCTGCTGATCGTAGCTGATAGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCA"
subject3Seqs = "AGTAGTCGTGATGTGCTAATCGGAGCTA-CTGACCGTGCTAGCTGATCGCAGCTGCTGATCGTAGCAGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCA"
subject4Seqs = "AGTAGTCGTGATGTGCTTATCGTAGCTAGCTGGTCGTGCTAGCTGATAGTAGCTGCTGATCGTAGCTGATCGCGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCAAGCTGATCGTAGCTGCTGATCGTAGCTGATCGTGATCGTGTCA"
seqs_raw = [querySeqs, subjectSeqs, subject3Seqs,subject4Seqs]
seqs = seqs_raw[::-1]
queryIDs = "query2"
sbjctIDs = "subjec2"
sbjctID3 = "subjec3"
sbjctID4 = "hahaha"
ids_raw = [queryIDs, sbjctIDs, sbjctID3, sbjctID4]
ids = ids_raw[::-1]
colors = get_colors(seqs)   ### seqs[0] is reference sequence
#print(colors)
seqLen = len(querySeqs)
seqNum = len(seqs)
text = [i for s in list(seqs) for i in s]
x = np.arange(1,seqLen+1)
y = np.arange(0,seqNum,1)
xx, yy = np.meshgrid(x,y)
gx = xx.ravel()
gy = yy.flatten()
recty = gy + .5
h = 1/seqNum
source = ColumnDataSource(dict(x=gx, y=gy, recty=recty, text=text, colors=colors))
plot_height_text = seqNum*20+50
plot_height_full = seqNum*10+50
x_range = Range1d(0,seqLen+1,bounds = 'auto')

### Check viewlen
if seqLen >= 40:
    viewlen = 40
else:
    viewlen = seqLen

tools = "xpan,xwheel_zoom,reset,save"

### entire sequence view
p = figure(title="Full view",plot_width=800,plot_height=plot_height_full,x_range = x_range,y_range = ids,tools = tools, min_border=0, toolbar_location='below')
rects = Rect(x="x",y="recty",width=1,height=1,fill_color="colors",line_color=None,fill_alpha=0.5)
p.add_glyph(source,rects)
p.yaxis.visible = False
view_range = (0,viewlen)

### sequence text view
pe = figure(title="Sequence view", plot_width = 800, plot_height = plot_height_text, x_range = view_range, y_range = ids, min_border = 0, tools="xpan,reset")
glyph = Text(x="x",y="y",text="text",text_align = "center", text_color="black",text_font="Courier",text_font_size="15px",text_font_style = "bold")
rects = Rect(x="x", y="recty",  width=1, height=1, fill_color="colors",line_color="None", fill_alpha=0.5)
pe.add_glyph(source, rects)
pe.add_glyph(source, glyph)
pe.yaxis.visible = True
pe.grid.visible = False
pe.xaxis.major_label_text_font_style = "bold"

p = gridplot([[p],[pe]],toolbar_location='below')
show(p)

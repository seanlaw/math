#!/usr/bin/env python

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, LabelSet, CustomJS, TapTool
from bokeh.layouts import widgetbox, column, row, layout
from random import randint

circle_cds = ColumnDataSource({'x': [], 'y': []})
equation_cds = ColumnDataSource({'x': [], 'y': [], 'text': [], 'size': []})
choices_cds = ColumnDataSource({'x': range(25, 125, 10), 
                                'y': [0]*10, 
                                'square_x': range(27, 127, 10),
                                'square_y': [0.2]*10,
                                'text': range(10), 
                                'size': [70]*10 })
counts_cds = ColumnDataSource({'x': [40, 80], 
                               'y': [-0.75, -0.75], 
                               'color': ['green', 'red'],
                               'text': [u'\u2714', u'\u2716']
                               })
answer = None
last_high_num = None
last_low_num = None

def generate_data():
    global circle_cds
    global equation_cds
    global answer
    global last_high_num
    global last_low_num

    high_num = randint(1, 9)
    low_num = randint(1, high_num)
    if (last_high_num == high_num and last_low_num == low_num):
        print("HERE")
        generate_data()
    else:
        answer = high_num - low_num
        text = str(high_num) + ' - ' + str(low_num) + ' = '

        circle_data = {'x': range(0, high_num*10, 10),
    				   'y': [1] * high_num,
    				   'selected': [False] * high_num
    				  }

        equation_data = {'x': [-0.5],
    					 'y': [0],
    					 'text': [text],
    					}

        circle_cds.data = circle_data
        equation_cds.data = equation_data

        last_high_num = high_num
        last_low_num = low_num

generate_data()

# Detect when circles are deselected and reset `selected` column in cds
circle_cds.callback = CustomJS(code="""
    if (cb_obj.selected['1d'].indices.length == 0){
        for (i=0; i< cb_obj.data['selected'].length; i++){
            cb_obj.data['selected'][i] = false        
        }
    }
    """)

choices_cds.callback = CustomJS(code="""
    var answer = {}
    var idx = cb_obj.selected['1d'].indices
    if (idx.length == 1 && idx == answer){{
        setTimeout(function () {{
            document.location.reload(true)
        }}, 500);
    }}
    else{{
        console.log(cb_obj.data)
    }}
    """.format(answer))

taptool_callback = CustomJS(args=dict(cds=circle_cds), code="""
	var selected_idx = cds.selected['1d'].indices
	cds.data['selected'][selected_idx] = !cds.data['selected'][selected_idx]

    cds.selected['1d'].indices = []
    for (i=0; i< cds.data['selected'].length; i++){
        if (cds.data['selected'][i] == true){
            cds.selected['1d'].indices.push(i)
        }
    }
	""")

taptool = TapTool(callback=taptool_callback)

p = figure(plot_width=1200, plot_height=600, x_range=(-5, 130), y_range=(-1.5,1.5), tools=[taptool])
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False
p.circle(x='x', y='y', source=circle_cds, size=50,
         selection_color='#1F77B4', 
         selection_line_color=None, 
         selection_fill_alpha=0.25,
         nonselection_fill_alpha=1.0,
        )
p.square(x='square_x', y='square_y', source=choices_cds, size='size', fill_alpha=0.25, line_color=None,
         selection_color='#1F77B4',
         selection_line_color=None, 
         selection_fill_alpha=1.0,
         nonselection_fill_alpha=0.25,
        )
p.circle(x='x', y='y', source=counts_cds, size=200, line_width=5.0, color='color')

equation = LabelSet(x='x', y='y', text='text', source=equation_cds, text_font_size='50pt')
choices = LabelSet(x='x', y='y', text='text', source=choices_cds, text_font_size='50pt', text_color='white')
counts = LabelSet(x='x', y='y', text='text', source=counts_cds, text_font_size='50pt', text_color='white', x_offset=-25, y_offset=-35)

p.add_layout(equation)
p.add_layout(choices)
p.add_layout(counts)
l = layout([[p]])

curdoc().add_root(l)

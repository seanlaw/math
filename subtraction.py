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
answer = None

def generate_data():
    global circle_cds
    global equation_cds
    global answer

    high_num = randint(1, 9)
    low_num = randint(1, high_num)
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
    console.log(idx)
    console.log(answer)
    if (idx.length == 1 && idx == answer){{
        setTimeout(function () {{
            document.location.reload(true)
        }}, 1000);
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

p = figure(plot_width=1200, plot_height=300, x_range=(-5, 130), y_range=(0.0,1.5), tools=[taptool])
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

equation = LabelSet(x='x', y='y', text='text', source=equation_cds, text_font_size='50pt')
choices = LabelSet(x='x', y='y', text='text', source=choices_cds, text_font_size='50pt', text_color='white')

p.add_layout(equation)
p.add_layout(choices)
l = layout([[p]])

curdoc().add_root(l)

#!/usr/bin/env python

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, LabelSet, CustomJS, TapTool
from bokeh.models.widgets import Button
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import widgetbox, column, row, layout
from random import randint

def handler(attr, old, new):
  """
  Do Nothing
  """
  return

circle_cds = ColumnDataSource({'x': [], 'y': []})
equation_cds = ColumnDataSource({'x': [], 'y': [], 'text': [], 'size': []})

def generate_data():
	global circle_cds
	global equation_cds

	high_num = randint(1, 9)
	low_num = randint(1, high_num)
	text = str(high_num) + ' - ' + str(low_num) + ' = ___'

	circle_data = {'x': range(high_num),
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

p = figure(plot_width=1200, plot_height=500, x_range=(-1, 11), y_range=(0.0,1.5), tools=[taptool])
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False
c = p.circle(x='x', y='y', source=circle_cds, size=50,
             selection_color='#1F77B4', 
             selection_line_color=None, 
             selection_fill_alpha=0.25,
             nonselection_fill_alpha=1.0,
            )

# Detect when circles are deselected and reset `selected` column in cds
circle_cds.callback = CustomJS(code="""
    if (cb_obj.selected['1d'].indices.length == 0){
        for (i=0; i< cb_obj.data['selected'].length; i++){
            cb_obj.data['selected'][i] = false        
        }
        console.log(cb_obj.data['selected'])
    }
    """)

equation = LabelSet(x='x', y='y', text='text', source=equation_cds, text_font_size='100pt')

p.add_layout(equation)
button = Button(label='Next', button_type='success')
radio_button_group = RadioButtonGroup(labels=list(map(str, range(0,10))))
l = layout([[p], [radio_button_group, button]], sizing_mode='stretch_both')

curdoc().add_root(l)

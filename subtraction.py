#!/usr/bin/env python

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.models.widgets import Button
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import widgetbox, column, row, layout
from random import randint

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
				   }

	equation_data = {'x': [-0.5],
					 'y': [0],
					 'text': [text],
					 }

	circle_cds.data = circle_data
	equation_cds.data = equation_data

generate_data()

p = figure(plot_width=1200, plot_height=500, x_range=(-1, 11), y_range=(0,1.5))
p.circle(x='x', y='y', source=circle_cds, size=50)
equation = LabelSet(x='x', y='y', text='text', source=equation_cds, text_font_size='100pt')
p.add_layout(equation)
button = Button(label='Next', button_type='success')
radio_button_group = RadioButtonGroup(labels=list(map(str, range(0,10))))
l = layout([[p], [radio_button_group, button]], sizing_mode='stretch_both')
curdoc().add_root(l)
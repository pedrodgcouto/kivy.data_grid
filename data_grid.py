import kivy
import urllib2
import json
import pprint
kivy.require('1.7.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import  ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.window import Window

Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
)

class CLabel(ToggleButton):
	bgcolor = ListProperty([1,1,1])

class HeaderLabel(Label):
	bgcolor = ListProperty([0.108,0.476,0.611])


data_json = open('data.json')
data = json.load(data_json)

header = ['ID', 'Nome', 'Preco', 'IVA']
col_size = [0.1, 0.5, 0.2, 0.2]
body_alignment = ["center", "left", "right", "right"]

products_list = []

# [UIColor colorWithWhite:1.000 alpha:1.000]
#	[UIColor colorWithRed:0.108 green:0.476 blue:0.611 alpha:1.000]

class DataGrid(GridLayout):

	def add_row():
		pass

	def remove_row():
		pass

	def update_row():
		pass

	def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
		super(DataGrid, self).__init__(**kwargs)
		self.cols = len(header_data)
		self.rows = len(body_data) + 1
		self.spacing = [1,1]
		n = 0
		for hcell in header_data:
			header_str = "[b]" + str(hcell) + "[/b]"
			self.add_widget(HeaderLabel(text=header_str, 
																	markup=True, 
																	size_hint_x=cols_size[n]))
			n+=1
		counter = 0
		for bcell in body_data:
			n = 0
			for item in bcell:

				cell = CLabel(text=('[color=1b799c]' + item + '[/color]'), 
											_background_color=(0,0,0,0), 
											background_normal="background_normal.png",
											background_down="background_pressed.png",
											halign=b_align[n],
											markup=True, 
											text_size=(300, None),
											size_hint_x=cols_size[n], 
											id=("row_" + str(counter) + "_col_" + str(n)))
				
				cell_width = Window.size[0] * cell.size_hint_x
				cell.text_size=(cell_width - 30, None)
				# print cell.id
				# print cell.size_hint_x
				# print Window.size[0]
				# print (Window.size[0] * cell.size_hint_x)
				# def on_pressed_cell(self):
				# 	self.row_10_col_1.bind(state = "Down")
				# 	print self
				cell.texture_update()
				self.add_widget(cell)
				n+=1
				# cell.bind(on_press=partial(on_pressed_cell))
			counter += 1

grid = DataGrid(header, data, body_alignment, col_size)

# class Interface(BoxLayout):
# 	def __init__(self, **kwargs):
# 		super(Interface, self).__init__(**kwargs)
# 		self.add_widget(grid)
# 		botao = Button(text="Adicionar Registo")
# 		self.add_widget(botao)


class MainApp(App):
	def build(self):
		grid = DataGrid(header, data, body_alignment, col_size)
		# interface = Interface()
		print Window.size
		return grid

if __name__=='__main__':
	MainApp().run()
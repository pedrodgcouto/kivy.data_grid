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
from kivy.uix.listview import ListView
from functools import partial
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

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
#body_alignment = ["center", "left", "right", "right"]
body_alignment = ["center", "center", "center", "center"]

products_list = []

counter = 0
class DataGrid(GridLayout):
	def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
		global counter
		#self.rows = 2
		##########################################################
		def change_on_press(self):
			childs = self.parent.children
			for ch in childs:
				if ch.id == self.id:
					print ch.id
					print len(ch.id)
					row_n = 0
					if len(ch.id) == 11:
						row_n = ch.id[4:5]
					else:
						row_n = ch.id[4:6]
					for c in childs:
						if ('row_'+str(row_n)+'_col_0') == c.id:
							if c.state == "normal":
								c.state="down"
							else:	
								c.state="normal"
						if ('row_'+str(row_n)+'_col_1') == c.id:
							if c.state == "normal":
								c.state="down"
							else:	
								c.state="normal"
						if ('row_'+str(row_n)+'_col_2') == c.id:
							if c.state == "normal":
								c.state="down"
							else:	
								c.state="normal"
						if ('row_'+str(row_n)+'_col_3') == c.id:
							if c.state == "normal":
								c.state="down"
							else:
								c.state="normal"
		def change_on_release(self):
			if self.state == "normal":
				self.state = "down"
			else:
				self.state = "normal"
		##########################################################
		n = 0
		for item in row_data:
			cell = CLabel(text=('[color=000000]' + item + '[/color]'), 
										background_normal="background_normal.png",
										background_down="background_pressed.png",
										halign=row_align[n],
										markup=True,
										on_press=partial(change_on_press),
										on_release=partial(change_on_release),
										text_size=(0, None),
										size_hint_x=cols_size[n], 
										size_hint_y=None,
										height=40,
										id=("row_" + str(counter) + "_col_" + str(n)))
			cell_width = Window.size[0] * cell.size_hint_x
			cell.text_size=(cell_width - 30, None)
			cell.texture_update()
			self.add_widget(cell)
			n+=1
		counter += 1
		#self.rows += 1
	def remove_row(self, n_cols, instance, **kwargs):
		childs = self.parent.children
		selected = 0
		for ch in childs:
			for c in reversed(ch.children):
				if c.id != "Header_Label":
					if c.state == "down":
						self.remove_widget(c)
						print str(c.id) + '   -   ' + str(c.state)
						selected += 1
		if selected == 0:
			for ch in childs:
				count_01 = n_cols
				count_02 = 0
				for c in reversed(ch.children):
					if c.id != "Header_Label":
						print str(n_cols)
					 	self.remove_widget(c)
					 	count_02 += 1
					if count_01 == count_02:
						break
							

			

	def select_all(self, instance, **kwargs):
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					c.state = "down"

	def unselect_all(self, instance, **kwargs):
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					c.state = "normal"

	def show_log(self, instance, **kwargs):
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					print str(c.id) + '   -   ' + str(c.state) +  '   -   ' + str(c.text)
		
	def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
		super(DataGrid, self).__init__(**kwargs)
		self.size_hint_y=None
		self.bind(minimum_height=self.setter('height'))
		self.cols = len(header_data)
		self.rows = len(body_data) + 1
		self.spacing = [1,1]
		n = 0
		for hcell in header_data:
			header_str = "[b]" + str(hcell) + "[/b]"
			self.add_widget(HeaderLabel(text=header_str, 
																	markup=True, 
																	size_hint_y=None,
																	height=40,
																	id="Header_Label",
																	size_hint_x=cols_size[n]))
			n+=1



grid = DataGrid(header, data, body_alignment, col_size)
grid.rows = 500

scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), pos_hint={'center_x':.5, 'center_y':.5})
scroll.add_widget(grid)
scroll.do_scroll_y = True
scroll.do_scroll_x = False

pp = partial(grid.add_row, ['001', 'Teste', '4.00', '4.00'], body_alignment, col_size)
add_row_btn = Button(text="Add Row", on_press=pp)
del_row_btn = Button(text="Delete Row", on_press=partial(grid.remove_row, len(header)))
upt_row_btn = Button(text="Update Row")
slct_all_btn = Button(text="Select All", on_press=partial(grid.select_all))
unslct_all_btn = Button(text="Unselect All", on_press=partial(grid.unselect_all))

show_grid_log = Button(text="Show log", on_press=partial(grid.show_log))

add_custom_row = Button(text="Add Custom Row", on_press=partial(grid.show_log))



def json_fill(self):
	for d in data:
		print d
		grid.add_row(d, body_alignment, col_size, self)
	# for row in datalist:
	# 	for cell in row:
	# 		print cell
	# 	print row
		#grid.add_row(row, body_alignment, col_size)

json_fill_btn = Button(text="JSON fill", on_press=json_fill)

btn_grid = BoxLayout(orientation="vertical")
btn_grid.add_widget(json_fill_btn)
btn_grid.add_widget(add_row_btn)
btn_grid.add_widget(del_row_btn)
btn_grid.add_widget(upt_row_btn)
btn_grid.add_widget(slct_all_btn)
btn_grid.add_widget(unslct_all_btn)
btn_grid.add_widget(show_grid_log)
btn_grid.add_widget(add_custom_row)

root = BoxLayout(orientation="horizontal")

root.add_widget(scroll)
root.add_widget(btn_grid)




class MainApp(App):
	def build(self):
		# grid = DataGrid(header, data, body_alignment, col_size)
		# interface = Interface()
		# print Window.size
		# return grid
		return root

if __name__=='__main__':
	MainApp().run()
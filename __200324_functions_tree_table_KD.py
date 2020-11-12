import pandas as pd 
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

from PyQt5.Qt import Qt
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


def round_df_numeric_values(df, precision):
	for header in df:
		for index, value in enumerate(df[header]):		
			try: 
				value = float(value)
				value = round(value,precision)
			except:
				value =value
			df.at[index,header]=value
	# Convert the dataframe back to string (necessary to populate the table)
	df = df.applymap(str)
	return(df)

def convert_str_to_num (df, variable_list):
	for header in variable_list:
		for index, value in enumerate(df[header]):		
			try: 
				value = float(value)
			#Convert non-numeric values to None type
			except:
				value =None
			df.at[index,header]=value

	# Remove any rows containig None values
	df_return = df.dropna()
	return(df_return)

def populate_tree(tree, df, table, plot):#, table):
	# Create the top level tree items (the same as the table headers)
	for name in df.columns:
		top_level_item_KD = QTreeWidgetItem([name])
		top_level_item_KD.setFlags(top_level_item_KD.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsTristate )
							
		#Populate each header with the appropriate data (i.e. add the tree children objects)
		for data_point in sorted(set(df[name])):
			child_KD = QTreeWidgetItem([str(data_point)])
			#Create a 'tristate' check box per chlide item
			child_KD.setFlags(child_KD.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
			#Default the child object un-checked
			child_KD.setCheckState(0, Qt.Checked)
			#Add the child object to the column header
			top_level_item_KD.addChild(child_KD)
		#Add the top level tree object (the column header) to the tree, once the header is populated with the childre object
		tree.addTopLevelItem(top_level_item_KD)
	# tree.itemClicked.connect(lambda item, column_index: view_selected_headers_on_table(tree, table, plot, df, item, column_index))
	tree.itemClicked.connect(lambda: view_selected_headers_on_table(tree, table, plot, df))

def make_headers_list(tree):
	my_selected_columns = []
	#Identify how many data columns have been generated
	top_level_count = tree.topLevelItemCount()
		
	#Loop through the top level items and append them to the list
	for index in  range(tree.topLevelItemCount()):			
		tree_item = tree.topLevelItem(index)
		#Make the header visible in the table if it is checked or semi-checked
		if tree_item.checkState(0) !=0:
			my_header = tree_item.text(0)
			my_selected_columns.append(my_header)
	return my_selected_columns	

# def filter_data(tree, table, master_df):#, table, df, item, column_index):
def filter_data(tree, master_df):
	#Create a list of the selected headers
	my_columns = make_headers_list(tree)
	#Create an dataframe for viewing and plotting data
	# view_df = master_df[my_columns].copy()
	view_df = master_df[my_columns]

	#Iterate through the headings list
	k = 0
	while k< len(my_columns):
		for parent_index in range(tree.topLevelItemCount()):
			w_parent = tree.topLevelItem(parent_index)
			tree_heading = w_parent.text(0)
			if tree_heading in my_columns:
				children_count = w_parent.childCount()
				filter_list = []
				#Put the heading into a list, to ensure that pandas returns a dataframe rather than a list
				active_column = []
				active_column.append(tree_heading)
				
				for child_index in range(children_count):
					w_child= w_parent.child(child_index)
					#check if the child is selected
					if w_child.checkState(0)==2:
						filter_list.append(w_child.text(0))
				view_df =view_df[view_df[tree_heading].isin(filter_list)]
				k +=1
	return my_columns,view_df

def populate_table(viewing_df, headers, table):
	column_count = len(headers)
	row_count = len(viewing_df)
	
	#Update row and column numbers to reflect input data
	table.setRowCount(len(viewing_df.index))
	table.setColumnCount(len(headers))

	#Create the column headings
	table.setHorizontalHeaderLabels(headers)
	#Transfer data
	for row_number, row_data in enumerate(viewing_df.values):
		for column_number, datum in enumerate(row_data):
			#Make empty cells look empty
			if datum == 'nan':
				datum = ''

			entry = QTableWidgetItem(datum)
			entry.setTextAlignment(Qt.AlignCenter)
			table.setItem(row_number, column_number,entry)		

def view_selected_headers_on_table( tree, table, my_canvas_list, master_df):
	my_columns,view_df = filter_data(tree, master_df)
	populate_table(view_df, my_columns, table)
	# Update the Pressure Plot
	print ('\n you are now in the function')
	print (f'the list is of type {type(my_canvas_list)}')	
	print (f'my_canvas_list is of type {type(my_canvas_list)}')
	print (my_canvas_list)
	
	plot_data(my_canvas_list.canvas, tree, view_df, 'Well', 'Formation Pressure','test_title') 
	# for k in my_canvas_list:
		# plot_data(k.canvas, tree, view_df, 'Well', 'Formation Pressure','test_title') 
      

# def plot(self,data, variable ,title_KD):
def plot_data(plot, tree, dataframe, primary_identifier, x_variable ,title_KD):
	#Extract the plotting dataframe
	my_columns,data= filter_data(tree, dataframe)
	#Remove any non-numeric or empty values
	plotting_df = dataframe[[primary_identifier, x_variable, 'TVDSL']]
	data=convert_str_to_num (plotting_df, [x_variable, 'TVDSL'])

	x = data[x_variable]
	y = data['TVDSL']
	#Clear previoys plots
	plot.figure.clear()

	#Create new plots subplot
	ax = plot.figure.add_subplot(111, title = title_KD)
	#Create a list of traces
	trace_list = np.unique(data[primary_identifier])
	
 	# Create a plot per primaty identifier
	for trace in trace_list:
		
		print ("\n8888888888888888888888*********")
		print ("x_variable is " +str(x_variable))
		print ("primary_identifier is " +str(primary_identifier))
		print (" value= "+str(np.array(data[x_variable][data[primary_identifier]==trace])))
		print ("8888888888888888888888*********\n")

		

		x = np.array(data[x_variable][data[primary_identifier]==trace], dtype=np.float32)
		y = np.array(data['TVDSL'][data[primary_identifier]==trace], dtype=np.float32)
		ax.scatter(x,y, label = trace, edgecolors = 'k', s = 100)
	ax.invert_yaxis()
	ax.set_xlabel(x_variable +'\n(psia)', size= 16)
	ax.set_ylabel('TVDSL' +'\n(psia)',size= 16)

	ax.legend()
	plt.subplots_adjust(bottom = .15)
	plot.draw()

class PlotCanvas(FigureCanvas):
	def __init__(self,parent, data, x_var, title_KD):
		fig = Figure()
		FigureCanvas.__init__(self, fig)

class WidgetPlot(QWidget):
    def __init__(self, parent,data , x_var, title_KD_2):
        QWidget.__init__(self)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self, data, x_var, title_KD_2)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)


######################################################################################################################################
#Create a dataframe
#Define a testing dataframe
# starting = {'First Heading':[3.245,		6.4234,		6.423,		'something',	1.45,		2.3425643,	6.345432,	'everything'],
# 			'TVDSL':[		4.146,		'Pambos',	5.8612,		'Lambros',		4.4646,		5.8721,		None,		3.145],
# 			'Formation Pressure':[5.435,		None,		1.425,		5.4326,			None,		1.435,		1.45,		1.534],
# 			'Well':[		'Well 1',	'Well 2',	'Well 1',	'Well 3',		'Well 1',	'Well 3',	'Well 2',	'Well 3' ]}
# df = pd.DataFrame(starting)

# df = pd.read_excel(r"C:\Users\DellAdmin\Dropbox\Tools\Python\RFT Analysis\PyQt5\19.10.25 Dummy Data KD.xlsx", skiprows =2).iloc[1:,1:]
# # Convert the dataframe back to string (necessary to populate the table)
# df= round_df_numeric_values(df, 2)

# # df = df.applymap(str)

# #Replace all None values with empty string
# df.replace(to_replace=[None], value='', inplace=True)

# class My_test(QtWidgets.QFrame):
# 	def __init__ (self, df,*args, **kw):
# 		super(My_test, self).__init__(*args, **kw)
# 		self.filter_data = filter_data
# 		# Import the datafrarme
# 		self.df = df
# 		self.horizontalLayout = QtWidgets.QVBoxLayout()
# 		#Define the table
# 		self.table = QtWidgets.QTableWidget()
# 		#Define the tree
# 		self.tree = QtWidgets.QTreeWidget(self)
# 		self.tree.setHeaderLabel("Station Data")
# 		#Define the plot
# 		self.plot = WidgetPlot("","","2","")
		
# 		#Complete the Gui
# 		self.horizontalLayout.addWidget(self.plot)
# 		self.horizontalLayout.addWidget(self.table)
# 		self.horizontalLayout.addWidget(self.tree)

# 		self.setLayout(self.horizontalLayout)
# 		populate_tree(self.tree,self.df, self.table, self.plot)

# # Run the GUI		
# app = QtWidgets.QApplication (sys.argv)
# my_window = My_test(df)
# my_window.show()
# app.exec_()
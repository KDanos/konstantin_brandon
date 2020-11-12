import pandas as pd
from pandas import DataFrame

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMainWindow, QVBoxLayout,QWidget, QTreeView
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt

# from __200307_demo_RFT_Table_plots_trees_KD import *
from __200305_RFT_GUI_KD import *
from __200324_functions_tree_table_KD import *

##############################################################################################################################
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

# # Import the spreadsheet data to a datframe
# loaded_df = pd.read_excel(r"C:\Users\DellAdmin\Dropbox\Tools\Python\RFT Analysis\PyQt5\19.10.25 Dummy Data KD.xlsx", skiprows =2).iloc[1:,1:]
loaded_df = pd.read_excel(r"C:\Users\DellAdmin\Dropbox\Tools\Python\Python Projects\RFT Analysis\PyQt5\June Return\19.10.25 Dummy Data KD.xlsx", skiprows =2).iloc[1:,1:]


#Replace all None values with empty string
 loaded_df.replace(to_replace=[None], value='', inplace=True)
 round_df_numeric_values(loaded_df, 2)
 loaded_df = loaded_df.applymap(str)

class My_Table(QMainWindow):
#*************************************
 #EXAMPLE OF SETTING A WIDGET IN A CELL
 #cb2  = QtWidgets.QCheckBox( parent=self.table )
 #self.table.setCellWidget(0, 1, cb0)
 #*************************************
	def __init__(self, data):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.show()
	

		my_columns,view_df = filter_data(self.ui.treeWidget_Stations, data) #self.ui.tableWidget_Stations, data)
		plotting_df = view_df.copy()

		self.my_Layout = QtWidgets.QGridLayout(self.ui.frame_Pressure_Plot)
		self.pressure_canvas= WidgetPlot(self.ui.frame_Pressure_Plot,view_df, 'Formation Pressure' ,'Pressure Plot')
		self.my_Layout.addWidget(self.pressure_canvas)
				
		#creare a Excess Pressure plot
		self.my_Layout2 = QtWidgets.QGridLayout(self.ui.frame_Excess_Pressure)
		# self.my_x_var = 'Excess Pressure'
		self.exs_pr_canvas= WidgetPlot(self.ui.frame_Excess_Pressure,view_df,'Excess Pressure', 'Excess Pressure Plot')
		self.my_Layout2.addWidget(self.exs_pr_canvas)

		#create Logs plot
		self.my_Layout3 = QtWidgets.QGridLayout(self.ui.frame_Logs_Plot)
		m3= WidgetPlot(self.ui.frame_Logs_Plot,view_df,[], 'Well Log')
		self.my_Layout3.addWidget(m3)
		
		# Populate the stations tree
		populate_tree(self.ui.treeWidget_Stations,  data, self.ui.tableWidget_Stations, self.pressure_canvas) 
		
		
		self.ui.treeWidget_Stations.setHeaderLabel("Station Data")
		self.ui.layout_treeWidget_Stations = QtWidgets.QGridLayout()
		self.ui.layout_treeWidget_Stations.addWidget(self.ui.treeWidget_Stations)
		
		# self.ui.treeWidget_Stations.itemClicked.connect(lambda item, column_index: view_selected_headers_on_table(self.ui.treeWidget_Stations, self.ui.tableWidget_Stations, self.pressure_canvas,data, item, column_index))
		
		# Update Graphs when filtering
		# list_plots = [self.pressure_canvas, self.exs_pr_canvas]
		# my_list = [1,2,3]
		# print (f'list_plots is of type {type(list_plots)}')
		# print (f'list_plots is of type {type(my_list)}')
		# print (list_plots)

		# self.ui.treeWidget_Stations.itemClicked.connect(lambda: view_selected_headers_on_table(self.ui.treeWidget_Stations, self.ui.tableWidget_Stations, self.pressure_canvas,data))
		# self.ui.treeWidget_Stations.itemClicked.connect(lambda: view_selected_headers_on_table(self.ui.treeWidget_Stations, self.ui.tableWidget_Stations, self.exs_pr_canvas,data))
		# self.ui.treeWidget_Stations.itemClicked.connect(lambda: view_selected_headers_on_table(self.ui.treeWidget_Stations, self.ui.tableWidget_Stations, list_plots, data))
		# self.ui.treeWidget_Stations.itemClicked.connect(lambda: view_selected_headers_on_table(self.ui.treeWidget_Stations, self.ui.tableWidget_Stations, my_list, data))

		

		

#Run the application 
if __name__=="__main__":
	app = QApplication(sys.argv)
	w = My_Table(loaded_df)
	w.show()
	sys.exit(app.exec_())

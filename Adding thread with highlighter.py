import sublime, sublime_plugin
from .datastructure_plugin import *

global layout_flag 
global layout_region

layout_flag = False
layout_region = "0"

list_of_threads = []

# class ExampleCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, 0, "Hello, World!")


class PrintTestCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		for x in list_of_threads:
			print (x.list_of_comments[0].comment_string)


class CreateNewThreadCommand(sublime_plugin.TextCommand):

	def run(self,edit):
		# global comment_view_obj
		# comment_view_obj = self.view
		self.view.window().show_input_panel("Enter your comment:", '', self.on_done, None, None)
		#sublime.set_timeout(self.close_view,1000)

	def on_done(self, user_input):
		global comment,window

		comment = str(user_input)
		tobj = Thread("17,18", comment_string = comment, list_of_comments = [])
		for region in self.view.sel():
			self.view.add_regions(tobj.thread_key, [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)
		tobj.add_thread(list_of_threads)

		print(list_of_threads[0].list_of_comments[0].comment_string)


# class AddNewComment(sublime_plugin.TextCommand):
	#TODO add comment modue from google keep
	 

	# def close_view(self):
	# 	self.window.focus_view(self.view)
	# 	self.window.run_command("close_file")


# class ThreadObjectCreation()






# Command runs when cursor position is changed. Displays comments corresponding to the region in file
# NEED TO FIX HIGHLIGHT AFTER CLOSING LAYOUT 
class HighlightChange(sublime_plugin.EventListener):
	def on_selection_modified_async(self,view):
		global layout_flag
		global layout_region

		#need window obj to call other commands
		window = sublime.active_window()
		current_view_obj = view

		#change color of all regions to 'comment' ignoring the region currently open
		# for id in Ux:
		# 	if layout_region != id or layout_region == "0":

		# 		region1 = view.get_regions(id)
		# 		view.add_regions(id, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

		#if current cursor position is contained in a region in file and no layout is open then open layout 
		for x in list_of_threads:
			region2 = view.get_regions(x.thread_key)
			region = view.sel()
			if region2[0].contains(region[0]):
				view.add_regions(x.thread_key, region2, 'string', 'dot', sublime.HIDE_ON_MINIMAP)

				if layout_region != x.thread_key :
					if layout_region != "0" :
						window.run_command("close_layout")


				if layout_flag == False :

					layout_flag = True
					layout_region = x.thread_key
					comment = x.thread_key
					command_name = "set_layout"
					command_arguments = { "cols": [0, 0.72, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], [1,0,2,1] ]	}
					window.run_command(command_name, command_arguments)
					window.run_command("display_user_input", {"comment" : comment})
		
		window.focus_view(current_view_obj)
		
		#fixed the dual highlight problem
		for x in list_of_threads:
			if layout_region != x.thread_key:

				region1 = view.get_regions(x.thread_key)
				view.add_regions(x.thread_key, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)


#displays content from the datastructure
class DisplayUserInputCommand(sublime_plugin.TextCommand):
	def run(self,edit, comment):

		global comment_view_obj

		comment_view_obj = self.view

		comment = "testing for : " + comment 
		#window.focus_view(comment_view_obj)
		self.view.insert(edit, 0, comment)
		self.view.set_scratch(True)
		self.view.set_read_only(True)

#keybind ctrl+shft+4 to close the layout manually
class CloseLayoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		global comment_view_obj
		global layout_flag
		global layout_region
		layout_flag = False
		layout_region = "0"
		
		self.window.focus_view(comment_view_obj)
		self.window.run_command("close_file")

		command_name = "set_layout"
		command_arguments = { "cols": [0, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], ] }
		self.window.run_command(command_name, command_arguments)






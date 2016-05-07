import sublime, sublime_plugin
from .datastructure_plugin import *

#global layout_flag
global layout_region



#layout_flag = False
layout_region = "0"

list_of_threads = []

# class ExampleCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, 0, "Hello, World!")


class PrintTestCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		for x in list_of_threads:
			print (x.list_of_comments[0].comment_string)


class AddThreadCommentCommand(sublime_plugin.TextCommand):




	def run(self,edit):
		global current_editing_file
		current_editing_file = self.view

		self.view.window().show_input_panel("Enter your comment:", 'hi test comment', self.on_done, None, None)
		#sublime.set_timeout(self.close_view,1000)


	def add_new_thread(self, puser_input):

		global comment,window

		comment = str(puser_input)


		tobj = Thread(self.view.sel()[0], comment_string = comment, list_of_comments = [])
		for region in self.view.sel():
			self.view.add_regions(tobj.thread_key, [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)
		tobj.add_thread(list_of_threads)

		#print(list_of_threads[0].list_of_comments[0].comment_string)


	def add_new_comment(self, puser_input):

		comment = str(puser_input)


		for x in list_of_threads:
			if (x.thread_key == layout_region):
				
				x.add_comment(comment)



	def on_done(self, user_input):

		# comment = str(user_input)
		# print comment

		in_highlight = False


		# add_new_thread(comment)
		global current_editing_file


		for thread_object in list_of_threads:
			region2 = current_editing_file.get_regions(thread_object.thread_key)		#thread_key gives the UUID
			region = current_editing_file.sel()
			if region2[0].contains(region[0]):
				in_highlight = True




		if in_highlight == False:
			self.add_new_thread(user_input)
		else:
			self.add_new_comment(user_input)




# class AddNewComment(sublime_plugin.TextCommand):
	#TODO add comment modue from google keep


	# def close_view(self):
	# 	self.window.focus_view(self.view)
	# 	self.window.run_command("close_file")


# class ThreadObjectCreation()


# Command runs when cursor position is changed. Displays comments corresponding to the region in file
# NEED TO FIX HIGHLIGHT AFTER CLOSING LAYOUT
class HighlightChange(sublime_plugin.EventListener):
	def on_selection_modified(self,view):
		#global layout_flag			#boolean which tells if layout(UI) is on or off (open or not)
		global layout_region		# if the layout is open, tells you which region it corresponds to
		global current_editing_file

		#print(layout_flag)
		#need window obj to call other commands
		window = sublime.active_window()
		#current_view_obj = current_editing_file

		#if current cursor position is contained in a region in file and no layout is open then open layout
		#list_of_threads contains a list of objects of the thread class

		for thread_object in list_of_threads:

			region2 = current_editing_file.get_regions(thread_object.thread_key)		#thread_key gives the UUID
			region = current_editing_file.sel()
			# print(current_editing_file.id())
			# print(view.id())
			# print(thread_object.thread_key)
			# print(region2)
			if region2[0].contains(region[0]):
				thread_index = list_of_threads.index(thread_object)
				current_editing_file.add_regions(thread_object.thread_key, region2, 'string', 'dot', sublime.HIDE_ON_MINIMAP)

				if layout_region != thread_object.thread_key :
					if layout_region != "0" :
						window.run_command("close_layout")


				if layout_region == "0" :

					#layout_flag = True
					layout_region = thread_object.thread_key
					#thread_uuid = thread_object.thread_key
					command_name = "set_layout"
					command_arguments = { "cols": [0, 0.72, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], [1,0,2,1] ]	}
					window.run_command(command_name, command_arguments)
					window.run_command("display_user_input", {"selected_thread_object" : thread_index})
					window.focus_view(current_editing_file)
			else:
				current_editing_file.add_regions(thread_object.thread_key, region2, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)





		#fixed the dual highlight problem
		# for thread_object in list_of_threads:
		# 	if layout_region != thread_object.thread_key:

		# 		region1 = current_editing_file.get_regions(thread_object.thread_key)
		# 		current_editing_file.add_regions(thread_object.thread_key, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)


#displays content from the datastructure
class DisplayUserInputCommand(sublime_plugin.TextCommand):
	def run(self,edit, selected_thread_object):

		global comment_view_obj

		comment_view_obj = self.view

		current_thread = list_of_threads[selected_thread_object]
		sum_of_chars = 0
		com_list= current_thread.list_of_comments

		for comment in reversed(com_list):
			#self.view.insert(edit, 0, "comment")
			sum_of_chars = self.view.insert(edit, 0, "\n"+comment.comment_string)
			print(sum_of_chars)
			self.view.insert(edit, 0, "\n\n\n@"+comment.username + "\t" + comment.timestamp)

		self.view.set_scratch(True)
		self.view.set_read_only(True)

#keybind ctrl+shft+4 to close the layout manually
class CloseLayoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		global comment_view_obj
		#global layout_flag
		global layout_region
		#layout_flag = False
		layout_region = "0"

		self.window.focus_view(comment_view_obj)
		self.window.run_command("close_file")

		command_name = "set_layout"
		command_arguments = { "cols": [0, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], ] }
		self.window.run_command(command_name, command_arguments)

import sublime, sublime_plugin
from .datastructureplugin import *

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
		global comment_view_obj
		comment_view_obj = self.view
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


class AddNewComment(sublime_plugin.TextCommand):
	#TODO add comment modue from google keep
	pass

	# def close_view(self):
	# 	self.window.focus_view(self.view)
	# 	self.window.run_command("close_file")


# class ThreadObjectCreation()
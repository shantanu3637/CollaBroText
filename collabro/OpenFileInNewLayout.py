import sublime, sublime_plugin


class FileLayoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		command_name = "set_layout"
		command_arguments = {"cols": [0, 0.72, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]}
		window = self.window
		window.run_command(command_name, command_arguments)
		window.run_command("in_new_layout")

class InNewLayoutCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")
		# self.view.set_scratch(True)
		#self.view.insert(edit,0,"hello")
		window = sublime.active_window()
		package_directory = sublime.packages_path() + '/' + 'collabro'

		with open(package_directory + '/test.cbrt', 'w') as fl:
			fl.write("@testing for write")
		window.open_file("test.cbrt")
		# sublime.message_dialog(str(window.views()))
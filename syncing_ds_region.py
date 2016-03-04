import sublime, sublime_plugin
from .datastructure_plugin import *

global UUID 
UUID = []
global list_of_threads 
list_of_threads = []

class AddToDsCommand(sublime_plugin.TextCommand):
	def run(self, edit, region):

		global list_of_threads
		global UUID


		t = Thread(region, comment_string = "testing", list_of_comments = [])
		
		list_of_threads.append(t)

		UUID.append(t.thread_key)
		global uuid 
		uuid = t.thread_key

class AddToSublimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		window = sublime.active_window()

		for region in self.view.sel():

			str_region = str(region)[1:-1]
			UUID = window.run_command("add_to_ds", {"region" : str_region})

			global uuid
			self.view.add_regions(uuid, [region], 'string', 'dot', sublime.HIDE_ON_MINIMAP)
			print("done")



class SyncingDataStrutureWithFile(sublime_plugin.EventListener):
	def on_post_save(self, view):
		global UUID
		global list_of_threads

		for id in UUID :
			region_from_sublime = view.get_regions(id)
			print("before sync")
			print(id)
			print(str(region_from_sublime)[1:-1])

		for thread in list_of_threads :
			region_from_ds =  thread.region
			print(thread.thread_key)
			print(region_from_ds)

		for id in UUID:
			region_from_sublime = view.get_regions(id)

			for thread in list_of_threads :
				region_from_ds = thread.region
				if thread.thread_key == id :
					thread.region = region_from_sublime

		for id in UUID :
			region_from_sublime = view.get_regions(id)
			print("after sync")
			print(id)
			print(str(region_from_sublime)[1:-1])

		for thread in list_of_threads :
			region_from_ds =  thread.region
			print(thread.thread_key)
			print(str(region_from_ds)[1:-1])


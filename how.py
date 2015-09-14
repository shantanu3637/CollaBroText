import sublime, sublime_plugin, ast


class Comment():
	
	

	# def __init__(self, thread_key, commentstring):
	# 	self.thread_key = 0
	# 	self.resolve =  False
	# 	self.region = sublime.Region(0,0)
	# 	self.commentstring = commentstring

	def InsertInFile(self):
		f = open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile','a')
		attribute_list = [self.username, self.thread_key, self.comment_string, self.resolve, self.region, self.timestamp]
		f.write(str(attribute_list)+'\n')
		f.close()


	def CreateNewThread(self):
		f = open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile','a')
		f.write('\n'+ str(self.thread_key)+ '\n')
		f.close()
		self.InsertInFile()





	def AccessFromFile(self):
		f = open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile','r')
		temp_attribute_list = ast.literal_eval(f.readline()) #.split(',~'))
		print(temp_attribute_list)


		self.username = temp_attribute_list[0]
		self.thread_key = temp_attribute_list[1]
		self.comment_string = temp_attribute_list[2]
		self.resolve = temp_attribute_list[3]
		self.region = sublime.Region(temp_attribute_list[4][0],temp_attribute_list[4][1])
		self.timestamp = temp_attribute_list[5]
		f.close()




	def InsertFromUI(self, username, thread_key, comment_key, comment_string, resolve, region, timestamp):
		self.username = username
		self.resolve = resolve
		self.thread_key = thread_key
		self.comment_key = comment_key
		self.comment_string = comment_string
		self.region = sublime.Region(region[0],region[1])
		self.timestamp = timestamp
		self.CreateNewThread()







	def printing(self):
		print(self.username)
		print(self.thread_key)
		print(self.comment_key)
		print(self.comment_string)
		print(self.resolve)
		print(self.region)
		print(self.timestamp)
		print(type(self.region))


	def highlighter(self):
		pass



 
	# def thread_of_comments(self, textstring):
	# 	f = open('datafile', 'a')
	# 	f.write(textstring + '\n')
	# 	f.close()



	# def retrieve_data(self):
	# 	f = open('datafile', 'r')
	# 	rettextstring = f.readline()



	# str = 'strin'









class WhatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
# 		for region in self.view.sel():
# 			print(region)
# 			print(type(region))
# 			self.view.add_regions('x', [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)


		# print(self.view.sel())   



		x = Comment()
		x.InsertFromUI("MyUsername", 4,0, "This is a comment", False, (35,60), [24,30,45])
		#x.InsertInFile()
		# x.AccessFromFile()
		# x.printing()

		x.InsertFromUI("2ndUsername", 5,0, "This is a secondary comment", False, (35,60), [24,30,49])
		# x.InsertInFile()
		# x.AccessFromFile()
		# x.printing()

  #           
import sublime, sublime_plugin, json

list_of_threads = []
new_list_of_threads = []


class Thread:

	def __init__(self,thread_key, region, list_of_comments, is_resolved = False):
		self.thread_key = thread_key
		self.region = region
		self.is_resolved = is_resolved
		self.list_of_comments = list_of_comments
		#write_thread()


	@staticmethod
	def write_list_threads(plist_of_threads):	 
		#jsonlist = [self.thread_key, self.region, self.list_of_comments]
		with open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile.json', 'w') as f:
			#f.write('[\n')
			#self.write_thread()
			json.dump([ThreadEncoder(indent = 1).default(x) for x in plist_of_threads], f, cls = ThreadEncoder, indent = 1)
			#f.write('\n')
			#f.write(']')


	@staticmethod
	def read_thread():
		with open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile.json', 'r') as fl:
			new_list_of_threads = json.load(fl)
			return(new_list_of_threads)

			# self.thread_key = data["thread_key"]
			# self.region = data["region"]
			# self.is_resolved = data["is_resolved"]
			# self.list_of_comments = data["list_of_comments"]

	@staticmethod
	def converting_from_file_to_new_list_of_threads(pnew_list_of_threads):
		# print(pnew_list_of_threads)
		pnewer_list_of_threads = [Thread(x["thread_key"], x["region"], x["list_of_comments"], x["is_resolved"]) for x in pnew_list_of_threads]
		return pnewer_list_of_threads






	def add_thread(self, plist_of_threads):
		plist_of_threads.append(self)


	def add_comment(self, comment_obj):
		self.list_of_comments.append(comment_obj)



	# def write__new_thread(self):	 
	# 	#jsonlist = [self.thread_key, self.region, self.list_of_comments]
	# 	with open('/home/shantanu/.config/sublime-text-3/Packages/User/datafile.json', 'a') as f:
	# 		json.dump(self, f, cls = ThreadEncoder, indent = 1)
	# 		f.write('\n')



	# def as_Thread(self,dic):
	# 	return Thread(dic["thread_key"], dic["region"], dic["list_of_comments"], dic["is_resolved"])



class Comment:
	
	def __init__(self, username, comment_key, comment_string, timestamp):
		self.username = username
		self.comment_key = comment_key
		self.comment_string = comment_string
		self.timestamp = timestamp




class ThreadEncoder(json.JSONEncoder):
	# def getting_comments_list(self, obj):
	# 	thislist = []
	# 	for w in obj.list_of_comments:
	# 		thislist.append(CommentEncoder.default(w))
	# 	return thislist



	def default(self, obj):
		if isinstance(obj, Thread):
			return {"thread_key":obj.thread_key, "region":obj.region, "is_resolved":obj.is_resolved, "list_of_comments":[CommentEncoder(indent = 1).default(x) for x in obj.list_of_comments]}#json.dumps(obj.list_of_comments, cls=CommentEncoder)}
		return json.JSONEncoder.default(self, obj)




class CommentEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Comment):
			return {"username":obj.username,"comment_key":obj.comment_key, "comment_string":obj.comment_string, "timestamp":obj.timestamp}
		return json.JSONEncoder.default(self, obj)





class WritetestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		c = Comment('mr3',123456, 'third Comment', 7)
		d = Comment('mr4',456789, '4th Comment', 8)
		t = Thread(16, 17, [c, d])
		u = Thread(18, 19, [c, d])
		v = Thread(20, 21, [c, d])

		t.add_thread(list_of_threads)
		# print(list_of_threads)
		u.add_thread(list_of_threads)
		# print(list_of_threads)
		v.add_thread(list_of_threads)
		# print(list_of_threads)


		Thread.write_list_threads(list_of_threads)
		yo = Thread.read_thread()
		new_list_of_threads = Thread.converting_from_file_to_new_list_of_threads(yo)

		print(new_list_of_threads)



		# t.create_list_threads()
		# t.write_thread()

		# newobj = Thread('','',[])
		# newobj.read_thread()
		# print(newobj.list_of_comments)
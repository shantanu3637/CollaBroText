

import  sublime,sublime_plugin, json, uuid, subprocess
from datetime import datetime

list_of_threads = []
new_list_of_threads = []


class Thread:

	def __init__(self, region, comment_string = None,list_of_comments = [], is_resolved = False):
		self.thread_key = str(uuid.uuid4())

		getting_region = list(region.split(','))
		self.region = sublime.Region(int(getting_region[0]),int(getting_region[1]))

		self.is_resolved = is_resolved



		if (comment_string == None):
			self.list_of_comments = list_of_comments
		else:
			cobj = Comment(comment_string)
			list_of_comments.append(cobj)
			self.list_of_comments = list_of_comments


	def find_thread(name_of_region): #TODO check if it works
		for x in list_of_threads:
			if (x.thread_key == name_of_region):
				return x





	@staticmethod
	def write_list_threads(plist_of_threads):	 
		with open('/home/shantanu/Desktop/datastructurework/datafile.json', 'w') as f:
			json.dump([ThreadEncoder(indent = 1).default(x) for x in plist_of_threads], f, cls = ThreadEncoder, indent = 1)

	@staticmethod
	def read_thread():
		with open('/home/shantanu/Desktop/datastructurework/datafile.json', 'r') as fl:
			new_list_of_threads = json.load(fl)
			return(new_list_of_threads)



	@staticmethod
	def converting_from_file_to_new_list_of_threads(pnew_list_of_threads):
		pnewer_list_of_threads = [Thread( x["region"], list_of_comments = [ Comment(y["comment_string"],y["comment_key"],y["username"],y["timestamp"]) for y in x["list_of_comments"] ] , is_resolved = x["is_resolved"]) for x in pnew_list_of_threads]
		return pnewer_list_of_threads


	def add_thread(self, plist_of_threads):
		plist_of_threads.append(self)


	def add_comment(self, comment_string):
		cobj = Comment(comment_string)
		self.list_of_comments.append(cobj)




class Comment:

	def __init__(self, comment_string = None, comment_key = None, username = None, timestamp =None):

		if(comment_key == None):
			git_uname = subprocess.Popen("git config user.name", shell=True, stdout=subprocess.PIPE).stdout.read()
			self.username = git_uname.decode("utf-8")
			
			self.comment_key = str(uuid.uuid4())

			self.comment_string = comment_string

			timestamp_string = str(datetime.now())
			self.timestamp = timestamp_string[0:timestamp_string.rfind(".")]
		else:
			self.username = username
			self.comment_key = comment_key
			self.comment_string = comment_string
			self.timestamp = timestamp





class ThreadEncoder(json.JSONEncoder):
	
	def default(self, obj):
		changed_region = str(obj.region)[1:-2]
		if isinstance(obj, Thread):
			return {"thread_key":obj.thread_key, "region":changed_region, "is_resolved":obj.is_resolved, "list_of_comments":[CommentEncoder(indent = 1).default(x) for x in obj.list_of_comments]}#json.dumps(obj.list_of_comments, cls=CommentEncoder)}
		return json.JSONEncoder.default(self, obj)




class CommentEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Comment):
			return {"username":obj.username,"comment_key":obj.comment_key, "comment_string":obj.comment_string, "timestamp":obj.timestamp}
		return json.JSONEncoder.default(self, obj)










class WritetestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		

		t = Thread( "17,18", "This is a first comment")

		t.add_thread(list_of_threads)
		t.add_comment("second comment")

		Thread.write_list_threads(list_of_threads)
		yo = Thread.read_thread()
		new_list_of_threads = Thread.converting_from_file_to_new_list_of_threads(yo)

		print(new_list_of_threads[0].list_of_comments[0].comment_string)





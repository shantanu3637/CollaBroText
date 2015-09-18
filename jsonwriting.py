import sublime, sublime_plugin
import json
import pprint






class Thread():
	def __init__(self, thread_key, region, list_of_comments):
		self.thread_key = thread_key
		self.region = region
		self.is_resolved = False
		self.list_of_comments = list_of_comments

	def write_to_file(self):
		data = {'a':str(self.thread_key), 'b':2}
		with open('/home/shantanu/Desktop/datastructurework/changemaker.json', 'w') as f:
			json.dump(self, f, cls=ThreadEncoder)

class Comment():
	def __init__(self, comment_key, comment):
		self.comment_key = comment_key
		self.comment = comment


class ThreadEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Thread):
			return {"is_resolved":obj.is_resolved, "thread_key":obj.thread_key, "region":obj.region, "list_of_comments":json.dumps(obj.list_of_comments, cls=CommentEncoder)}#CommentEncoder().encode(obj.list_of_comments)}
		return json.JSONEncoder.default(self, obj)

class CommentEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Comment):
			return {"comment_key":obj.comment_key, "comment_string":obj.comment}
		return json.JSONEncoder.default(self, obj)



class IsitworkingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		c = Comment(123, 'First Comment')
		d = Comment(456, 'Second Comment')
		t = Thread('12thread', 3, [c,d])
		t.write_to_file()
		with open('/home/aaron/data.json', 'r') as f:
			data = json.load(f)
		print(data)
		s = data['list_of_comments']
		print(s)
		jdata = json.loads(s)
		print(jdata[0]['comment_key'])
		data['list_of_comments'] = jdata
		print(data['list_of_comments'][0])
		print(data['list_of_comments'][0]['comment_key'])
		#print(json.dumps(data['list_of_comments'], indent=4, sort_keys=True))

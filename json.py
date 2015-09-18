import sublime, sublime_plugin
import json






class Thread():
	def __init__(self, thread_key, region, list_of_comments):
		self.thread_key = thread_key
		self.region = region
		self.is_resolved = False
		self.list_of_comments = list_of_comments

	def write_to_file(self):
		data = {'a':str(self.thread_key), 'b':2}
		with open('/home/aaron/data.json', 'w') as f:
			json.dump(self, f, cls=ThreadEncoder)

class Comment():
	def __init__(self, comment_key, comment):
		self.comment_key = comment_key
		self.comment = comment


class ThreadEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Thread):
			return {"thread_key":obj.thread_key, "region":obj.region, "is_resolved":obj.is_resolved, "list_of_comments":CommentEncoder().encode(obj.list_of_comments)}#json.dumps(obj.list_of_comments, cls=CommentEncoder)}
		return json.JSONEncoder.default(self, obj)

class CommentEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Comment):
			return {"comment_key":obj.comment_key, "comment_string":obj.comment}
		return json.JSONEncoder.default(self, obj)



class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		c = Comment(123, 'First Comment')
		d = Comment(456, 'Second Comment')
		t = Thread('12thread', 3, [c, d])
		t.write_to_file()
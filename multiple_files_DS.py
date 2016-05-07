import os, uuid

thread_path = '/home/aaron/Desktop/Comments' + str(uuid.uuid4())
if not os.path.exists(thread_path):
	os.makedirs(thread_path)

comment_number = 0
with open(thread_path + '/' + comment_number + '.txt', 'r') as fl:
	fl.write("")

import  sublime,sublime_plugin, json, uuid, subprocess, os, string
from datetime import datetime
import time

import shutil

#Global list of thread objects
list_of_threads = []
new_list_of_threads = []



class Thread:

	def __init__(self, region,thread_key = None , comment_string = None,list_of_comments = [], is_resolved = False):
		#When reading from the file
		if ( thread_key == None):
			self.thread_key = str(uuid.uuid4())
		#when initializing from plugin
		else:
			self.thread_key = thread_key

		# #region changing from string to sublime region object
		# getting_region = list(region.split(','))
		# self.region = sublime.Region(int(getting_region[0]),int(getting_region[1]))

		self.region = region

		self.is_resolved = is_resolved

		#When reading from the file
		if (comment_string == None):
			self.list_of_comments = list_of_comments
		#when initializing from plugin
		else:
			cobj = Comment(comment_string)
			list_of_comments.append(cobj)
			self.list_of_comments = list_of_comments

	#find thread object by region
	def find_thread(name_of_region): #TODO check if it works
		for x in list_of_threads:
			if (x.thread_key == name_of_region):
				return x



	#Encode to JSON using Thread and comment Encoder and write to file
	@staticmethod
	def write_list_threads(plist_of_threads):
		with open('/home/aaron/Desktop/datafile.json', 'w') as f:
			json.dump([ThreadEncoder(indent = 1).default(x) for x in plist_of_threads], f, cls = ThreadEncoder, indent = 1)


	# @staticmethod
	# def WriteCreateThreadFolder(pcurrent_file_directory, plist_of_threads):

	# 	thread_path = pcurrent_file_directory + '/Comments' #Checks if a Comments folder is present

	# 	if os.path.exists(thread_path):
	# 		shutil.rmtree(thread_path)
	# 		os.makedirs(thread_path)

	# 	for x in plist_of_threads:
	# 		# Shantanu while redoing, check this line to see if it is needed.
			
	# 		thread_path = pcurrent_file_directory + '/Comments' #Checks if a Comments folder is present



	# 		# if not os.path.exists(thread_path):
	# 		# 	os.makedirs(thread_path)
	# 		# else:
	# 		# 	shutil.rmtree(thread_path)
	# 		# 	os.makedirs(thread_path)

	# 		thread_path = pcurrent_file_directory + '/' + 'Comments' + '/' + str(x.thread_key) #Creates a folder for a thread

	# 		if not os.path.exists(thread_path):
	# 			os.makedirs(thread_path)
	# 		else:
	# 			shutil.rmtree(thread_path)
	# 			os.makedirs(thread_path)

	# 		#os.makedirs(thread_path)

	# 		with open(thread_path + '/' + '1' + '.txt', 'w') as fl:
	# 			fl.write( str(x.region) +"\n" + x.thread_key + "\n" + str(x.is_resolved))
	# 		for y in x.list_of_comments:
	# 			with open(thread_path + '/' + y.timestamp + '.txt', 'w') as fl:
	# 				fl.write(y.username + '\n' + y.comment_key + '\n' + y.comment_string + "\n" +y.timestamp)







	@staticmethod
	def WriteCreateThreadFolder(pcurrent_file_directory, plist_of_threads, pProject_directory):



		# for dirpath, dirnames, filenames in os.walk (str(pProject_directory)): 
		# 	if not os.path.exists(os.path.join (str(pProject_directory) + '/Project_Comments', dirpath[1+len (str(pProject_directory)):])):
		# 		if not(os.path.exists(pProject_directory+"/Project_Comments")):
		# 		os.mkdir (os.path.join (str(pProject_directory) + '/Project_Comments', dirpath[1+len (str(pProject_directory)):]))



		# print(pProject_directory)
		# for dirpath, dirnames, filenames in os.walk ('/home/shantanu/Documents/TestingGit'): 
		# 	os.mkdir (os.path.join ('/home/shantanu/Documents/TestingGit' + '/Project_Comments', dirpath[1+len ('/home/shantanu/Documents/TestingGit'):]))

		

		for dirpath, dirnames, filenames in os.walk (str(pProject_directory)):


			#dirnames[:] = [d for d in dirnames if d not in Project_Comments] 


			#print("This is dirpath"+str(dirpath))
			#print(dirnames)
			#print("This is filenames"+str(filenames))


			if ("Project_Comments" not in dirpath):
				if not os.path.exists(os.path.join (str(pProject_directory) + '/Project_Comments', dirpath[1+len (str(pProject_directory)):])):
					os.mkdir (os.path.join (str(pProject_directory) + '/Project_Comments', dirpath[1+len (str(pProject_directory)):]))















		#print("This is Project directory path" + pProject_directory)
		#print("This is current file directory path" + pcurrent_file_directory)

		testingvariable  =  pcurrent_file_directory

		#testingvariable = string.replace(testingvariable, pProject_directory, "", 1)


		#print("This is testing variable" + testingvariable)
		filevariable  = pcurrent_file_directory.split('/')[-1] 

		#print ("This is filevariable" + filevariable)
		#filevariable = pProject_directory + '/Project_Comments'




		#thread_path = pcurrent_file_directory + filevariable + 'Comments' #Checks if a Comments folder is present

		thread_path = pProject_directory + "/Project_Comments" +  ((pcurrent_file_directory.split(pProject_directory)[1]).split("/"+filevariable)[0])
		#print ("This is thread path " + thread_path) 
		



		# This erased commments of other files
		# if os.path.exists(thread_path):
		# 	shutil.rmtree(thread_path)
		# 	os.makedirs(thread_path)

		for x in plist_of_threads:
			# Shantanu while redoing, check this line to see if it is needed.
			
			#thread_path = pcurrent_file_directory + filevariable +  'Comments' #Checks if a Comments folder is present



			# if not os.path.exists(thread_path):
			# 	os.makedirs(thread_path)
			# else:
			# 	shutil.rmtree(thread_path)
			# 	os.makedirs(thread_path)




			#thread_path = pcurrent_file_directory + filevariable + 'Comments' + '/' + str(x.thread_key) #Creates a folder for a thread


			thread_path2 = thread_path+ "/" + filevariable.split(".")[0] + 'Comments' + '/' + str(x.thread_key)
			#print("This is 2 thread path " + thread_path2)

			# if not os.path.exists(thread_path):
			# 	os.makedirs(thread_path)
			# else:
			# 	shutil.rmtree(thread_path)
			# 	os.makedirs(thread_path)

			if not os.path.exists(thread_path2):
			 	os.makedirs(thread_path2)


			# print("Outside if")
			# print(plist_of_threads)
			# print(plist_of_threads[0].thread_key)
			# print(plist_of_threads[0].list_of_comments[0])

			with open(thread_path2 + '/' + '1' + '.txt', 'w') as fl:
				fl.write( str(x.region) +"\n" + x.thread_key + "\n" + str(x.is_resolved))
			for y in x.list_of_comments:
				with open(thread_path2 + '/' + y.timestamp + '.txt', 'w') as fl:
					fl.write(y.username + '\n' + y.comment_key + '\n' + y.comment_string + "\n" +y.timestamp)



















	#@staticmethod

	#Reading thread from file
	@staticmethod #TODO
	def read_thread():
		with open('/home/aaron/Desktop/datafile.json', 'r') as fl:
			new_list_of_threads = json.load(fl)
			return(new_list_of_threads)


	#Coverting JSON data from string back to Thread and Comment Class objects
	@staticmethod
	def converting_from_file_to_new_list_of_threads(pnew_list_of_threads):

		# pnewer_list_of_threads = [Thread( x["region"], list_of_comments = [ Comment(y["comment_string"],y["comment_key"],y["username"],y["timestamp"]) for y in x["list_of_comments"] ] , is_resolved = x["is_resolved"]) for x in pnew_list_of_threads]


		pnewer_list_of_threads = [Thread( sublime.Region(int(list(x["region"].split(','))[0]),int(list(x["region"].split(','))[1])),
			list_of_comments = [ Comment(y["comment_string"],y["comment_key"],y["username"],y["timestamp"]) for y in x["list_of_comments"] ],
			is_resolved = x["is_resolved"]) for x in pnew_list_of_threads]
		return pnewer_list_of_threads


		# return pnewer_list_of_threads


	#add thread to list of thread objects
	def add_thread(self, plist_of_threads):
		plist_of_threads.append(self)


	#add new comment to thread
	def add_comment(self, comment_string):
		cobj = Comment(comment_string)
		self.list_of_comments.append(cobj)



def read_multiple_files(pcurrent_file_directory, pProject_directory): #reading from multiple files directly into sublime DS


	
		# for root, dirs, files in os.walk(pcurrent_file_directory + '/' + 'Comments'):
		# 	local_list_of_comments = []
		# 	for name in files:

		# 		if (name !=  '1.txt'):
		# 			with open(os.path.join(root,name), 'r') as fl:
		# 				content = fl.readlines()
		# 				c = Comment(str(content[2])[0:-1],str(content[1])[0:-1],str(content[0])[0:-1],str(content[3])[0:])
		# 				local_list_of_comments.append(c)

		# 	for name in files:
		# 		if (name == '1.txt'):
		# 			with open(os.path.join(root,name), 'r') as fl:
		# 				content = fl.readlines()
		# 				reg = str(content[0])[1:-2]
		# 				t = Thread( (sublime.Region(int(list(reg.split(','))[0]),int(list(reg.split(','))[1]))), thread_key = str(content[1])[0:-1],  comment_string = None, list_of_comments = local_list_of_comments, is_resolved = str(content[2])[0:])
		# 				t.add_thread(list_of_threads)
		# return list_of_threads


		#pProject_directory = "/home/shantanu/Documents/TestingGit"
		filevariable  = pcurrent_file_directory.split('/')[-1]
		thread_path = pProject_directory + "/Project_Comments" +  ((pcurrent_file_directory.split(pProject_directory)[1]).split("/"+filevariable)[0]) + "/" + filevariable.split(".")[0] + 'Comments'
		local_list_of_threads = []

		#print("This is thread_path for read" + str(thread_path))
		for root, dirs, files in os.walk(thread_path):
			local_list_of_comments = []
			for name in files:

				if (name !=  '1.txt'):
					#print("root and file name" + str(root) + str(name))
					with open(os.path.join(root,name), 'r') as fl:
						content = fl.readlines()
						c = Comment(str(content[2])[0:-1],str(content[1])[0:-1],str(content[0])[0:-1],str(content[3])[0:])
						local_list_of_comments.append(c)

			for name in files:
				if (name == '1.txt'):
					with open(os.path.join(root,name), 'r') as fl:
						content = fl.readlines()
						reg = str(content[0])[1:-2]
						t = Thread( (sublime.Region(int(list(reg.split(','))[0]),int(list(reg.split(','))[1]))), thread_key = str(content[1])[0:-1],  comment_string = None, list_of_comments = local_list_of_comments, is_resolved = str(content[2])[0:])
						t.add_thread(local_list_of_threads)
		#print("list in datastruct" + str(local_list_of_threads))
		return local_list_of_threads






class Comment:

	def __init__(self, comment_string = None, comment_key = None, username = None, timestamp =None):

		#while adding comment for for first time in thread
		if(comment_key == None):

			#getting username from terminal
			git_uname = subprocess.Popen("git config user.name", shell=True, stdout=subprocess.PIPE).stdout.read()
			self.username = str(git_uname.decode("utf-8"))[0:-1]


			self.comment_key = str(uuid.uuid4())

			self.comment_string = comment_string

			#getting timestamp and doing string manipulation to truncate
			timestamp_string = str(datetime.now())
			self.timestamp = timestamp_string[0:timestamp_string.rfind(".")]


		#while adding comment from  .comments file
		else:
			self.username = username
			self.comment_key = comment_key
			self.comment_string = comment_string
			self.timestamp = timestamp





class ThreadEncoder(json.JSONEncoder):

	def default(self, obj):

		#getting rid of "" marks
		changed_region = str(obj.region)[1:-2]

		#Encoding into JSON
		if isinstance(obj, Thread):
			return {"thread_key":obj.thread_key, "region":changed_region, "is_resolved":obj.is_resolved, "list_of_comments":[CommentEncoder(indent = 1).default(x) for x in obj.list_of_comments]}#json.dumps(obj.list_of_comments, cls=CommentEncoder)}
		return json.JSONEncoder.default(self, obj)



#similar to ThreadEncoder function
class CommentEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Comment):
			return {"username":obj.username,"comment_key":obj.comment_key, "comment_string":obj.comment_string, "timestamp":obj.timestamp}
		return json.JSONEncoder.default(self, obj)










class WritetestCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		reg1 = sublime.Region(12,45)

		t = Thread( reg1,  comment_string = "This is a first comment", list_of_comments = [])
		time.sleep(5)
		t.add_thread(list_of_threads)
		t.add_comment("second comment")
		time.sleep(5)
		t.add_comment("third comment")




		Thread.WriteCreateThreadFolder(list_of_threads)


		#read_multiple_files(pass)



		# Thread.write_list_threads(list_of_threads)
		# yo = Thread.read_thread()
		# new_list_of_threads = Thread.converting_from_file_to_new_list_of_threads(yo)

		# print(new_list_of_threads[0].list_of_comments[0].comment_string)
		# print(new_list_of_threads[0].list_of_comments[1].comment_string)
		# print(new_list_of_threads[0].list_of_comments[2].comment_string)

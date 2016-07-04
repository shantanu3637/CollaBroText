import sublime
import sublime_plugin
import os
import subprocess
from .datastructure import *

from datetime import *
from functools import wraps

#global layout_fla
global layout_region

global run_plugin
run_plugin = False


#layout_flag = False
layout_region = "0"

global list_of_threads
list_of_threads = []


global data_struct
data_struct = {}

# class ExampleCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, 0, "Hello, World!")

# Throttle class to run on selection modifier

class ShiftView(sublime_plugin.EventListener):
    def on_activated(self,view):
        # print("View File name is : "+ str(view.file_name()))
        if (view.file_name()!='/home/ssk/.config/sublime-text-3/Packages/CollaBroText/comments.cbrt'):
            if (view.file_name() is not None):
                window = sublime.active_window()
                window.run_command('view_changed')

            

class ViewChangedCommand(sublime_plugin.TextCommand):
    def run(self, view):
        current_view_id = self.view.id()


        global data_struct, list_of_threads, current_editing_file
            
        current_editing_file = self.view
        # print("Current editing file was set again . with view id "+str(current_editing_file.id()))
        try :
            list_of_threads = data_struct[current_view_id]
        except KeyError :
            pass #does this need to be changed?




class throttle(object):
    """
    Decorator that prevents a function from being called more than once every
    time period.
    To create a function that cannot be called more than once a minute:
        @throttle(minutes=1)
        def my_fun():
            pass
    """

    def __init__(self, seconds=0, minutes=0, hours=0):
        self.throttle_period = timedelta(
            seconds=seconds, minutes=minutes, hours=hours
        )
        self.time_of_last_call = datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            time_since_last_call = now - self.time_of_last_call

            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                return fn(*args, **kwargs)

        return wrapper


class PrintTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for x in list_of_threads:
            print (x.list_of_comments[0].comment_string)


class AddThreadCommentCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global current_editing_file, list_of_threads
        current_editing_file = self.view
        self.in_highlight = False
        self.current_highlighted_region = current_editing_file.sel()
        # print("current highlight = "+str(self.current_highlighted_region[0]))



        for thread_object in list_of_threads:
            region_from_object = current_editing_file.get_regions(thread_object.thread_key)  # thread_key gives the UUID
            if region_from_object[0].contains(self.current_highlighted_region[0]):
                self.in_highlight = True

        current_editing_file = self.view
        if(self.current_highlighted_region[0].a==self.current_highlighted_region[0].b):
            if (self.in_highlight == True):
                self.view.window().show_input_panel("Enter your comment:", '', self.on_done, None, None)
            else:
                sublime.message_dialog("You are trying to add a comment without selecting a region! Please select a region.")
        else:
            self.view.window().show_input_panel("Enter your comment:", '', self.on_done, None, None)


    def add_new_thread(self, puser_input):

        global comment, window, list_of_threads, data_struct

        if self.view.id() not in data_struct.keys():
            list_of_threads = []

        comment = str(puser_input)

        tobj = Thread(self.view.sel()[0], comment_string=comment, list_of_comments=[])
        for region in self.view.sel():
            self.view.add_regions(
                tobj.thread_key, [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)
        tobj.add_thread(list_of_threads)

        data_struct[self.view.id()] = list_of_threads
        #print(str(data_struct[self.view.id()]))

        #move cursor in and out of newly created region(highlight) so that it gets highlighted properly
        window = sublime.active_window()
        row_number = self.view.rowcol(self.view.sel()[0].begin())[0]
        #print("row no" + str(row_number))

        col_number = self.view.rowcol(self.view.sel()[0].begin())[1]

        #print("col_no"+str(col_number))
        window.run_command(
                    "goto_row_col",
                    {"row": row_number+1, "col":col_number+1 }
                )
        window.run_command(
            "goto_row_col",
            {"row": row_number+1, "col":col_number+2 }
        )


        # print(list_of_threads[0].list_of_comments[0].comment_string)

    def add_new_comment(self, puser_input):

        comment = str(puser_input)

        global list_of_threads

        for x in list_of_threads:
            if (x.thread_key == layout_region):

                x.add_comment(comment)

    def on_done(self, user_input):
        window = sublime.active_window()

        if self.in_highlight == False:
            self.add_new_thread(user_input)
        else:
            self.add_new_comment(user_input)
            window.run_command("close_layout")

        window.run_command("highlight_and_display")



class GotoRowColCommand(sublime_plugin.TextCommand):
        def run(self, edit, row, col):
                #print("INFO: Input: " + str({"row": row, "col": col}))
                # rows and columns are zero based, so subtract 1
                # convert text to int
                (row, col) = ( int( row ) - 1 , int( col ) - 1 )
                if row > -1 and col > -1:
                        # col may be greater than the row length
                        currentRowLength = len( self.view.substr( self.view.full_line( self.view.text_point( row , 0 ) ) ) ) -1
                        col = min( col , currentRowLength )
                        #print("INFO: Calculated: " + str({"row": row, "col": col}))
                        self.view.sel().clear()
                        self.view.sel().add(sublime.Region(self.view.text_point(row, col)))
                        self.view.show(self.view.text_point(row, col))
                else:
                        print("ERROR: The Row or the Column arguments are less than one. Both must be >=1")

# Command is called to highlight and display the comments
# Called by on_selection_modified and add_thread_comment
class HighlightAndDisplayCommand(sublime_plugin.TextCommand):
    def run(self, view):
        # global layout_flag                      #boolean which tells if
        # layout(UI) is on or off (open or not)
        global layout_region        # if the layout is open, tells you which region it corresponds to
        global current_editing_file
        global window, list_of_threads


        # need window obj to call other commands
        window = sublime.active_window()

        if self.view.id() not in data_struct.keys():
            list_of_threads = []

        else :
            list_of_threads = data_struct[self.view.id()]

        # print(str(current_editing_file))
        
        # current_editing_file = self.view
        # print(str(list_of_threads))
        #current_view_obj = current_editing_file

        # if current cursor position is contained in a region in file and no layout is open then open layout
        # list_of_threads contains a list of objects of the thread class

        # Need to iterate through the full list due to the case when moving from one highlighted region to another`
        for thread_object in list_of_threads:
            region_from_object = current_editing_file.get_regions(thread_object.thread_key)  # thread_key gives the UUID
            currently_selected_region = current_editing_file.sel()
            # print(current_editing_file.id())
            # print(view.id())
            if region_from_object[0].contains(currently_selected_region[0]):
                thread_index = list_of_threads.index(thread_object)
                current_editing_file.add_regions(
                    thread_object.thread_key, region_from_object, 'string', 'dot', sublime.HIDE_ON_MINIMAP)

                if layout_region != thread_object.thread_key:
                    if layout_region != "0":
                        window.run_command("close_layout")

                if layout_region == "0":

                    #layout_flag = True
                    layout_region = thread_object.thread_key
                    #thread_uuid = thread_object.thread_key
                    command_name = "set_layout"
                    command_arguments = {"cols": [0, 0.72, 1.0], "rows": [
                        0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]    }
                    window.run_command(command_name, command_arguments)
                    window.run_command("display_comments", {
                                       "selected_thread_object": thread_index})
                    window.focus_view(current_editing_file)
            else:
                current_editing_file.add_regions(
                    thread_object.thread_key, region_from_object, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

        # fixed the dual highlight problem
        # for thread_object in list_of_threads:
        #   if layout_region != thread_object.thread_key:

        #       region1 = current_editing_file.get_regions(thread_object.thread_key)
        #       current_editing_file.add_regions(thread_object.thread_key, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)



# Command runs when cursor position is changed. Displays comments corresponding to the region in file
# NEED TO FIX HIGHLIGHT AFTER CLOSING LAYOUT
class HighlightChange(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        # print("View in on_selection_mod"+str(view)+" and id is "+str(view.id()))
        window = sublime.active_window()
        window.run_command("highlight_and_display")


    thro = throttle(seconds=0.5)
    on_selection_modified = thro(on_selection_modified)


# displays content from the datastructure
#called by highlight_and_display
class DisplayCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit, selected_thread_object):

        global comment_view_obj, list_of_threads


        # sublime.status_message("view id of UI is set here: "+str(comment_view_obj))
        current_thread = list_of_threads[selected_thread_object]
        sum_of_chars = 0
        com_list = current_thread.list_of_comments
        package_directory = sublime.packages_path() + '/' + 'CollaBroText'

        # for comment in reversed(com_list):
        #     #self.view.insert(edit, 0, "comment")
        #     sum_of_chars = self.view.insert(
        #         edit, 0, "\n" + comment.comment_string)
        #     split_timestamp = comment.timestamp.split(' ')
        #     split_only_date = split_timestamp[0].split('-')
        #     if(split_timestamp[0] == str(date.today())):
        #         final_timestamp = "Today @ " + split_timestamp[1]
        #     elif(split_timestamp[0] == str(date.today() - timedelta(days=1))):
        #         final_timestamp = "Yesterday @ " + split_timestamp[1]
        #     elif(split_only_date[0] == str(date.today().year)):
        #         final_timestamp = split_only_date[1] + "-" + split_only_date[2] + " @ " + split_timestamp[1]
        #     self.view.insert(edit, 0, "\n\n\n@" +
        #                      comment.username + "\t" + final_timestamp)

        with open(package_directory + '/comments.cbrt', 'w') as fl :

            for comment in (com_list):

                split_timestamp = comment.timestamp.split(' ')
                split_only_date = split_timestamp[0].split('-')
                if(split_timestamp[0] == str(date.today())):
                    timeperiod = "Today "
                elif(split_timestamp[0] == str(date.today() - timedelta(days=1))):
                    timeperiod = "Yesterday "
                elif(split_only_date[0] == str(date.today().year)):
                    timeperiod = split_only_date[1] + "-" + split_only_date[2]
                else :
                    timeperiod = split_only_date[1] + "-" + split_only_date[2] + "-" + split_only_date[0]
                
                fl.write("\n\n" + timeperiod)
                fl.write("\n@" + comment.username + "\t" + split_timestamp[1])
                fl.write("\n" + ' ' +comment.comment_string)

        #print("current view" + str(self.view))
        comment_view_obj = window.open_file(package_directory + '/comments.cbrt')
        #print("layout_view " + str(comment_view_obj))

        comment_view_obj.set_read_only(True)
        #self.view.set_scratch(True)
        #self.view.set_read_only(True)

# keybind alt+x to close the layout manually

# closes the comments layout and resets control variables
# called by highlight_and_display, on_pre_close, add_new_comment
class CloseLayoutCommand(sublime_plugin.WindowCommand):
    def run(self):
        global comment_view_obj
        #global layout_flag
        global layout_region
        #layout_flag = False
        layout_region = "0"

        self.window.focus_view(comment_view_obj)
        self.window.run_command("close")

        command_name = "set_layout"
        command_arguments = {"cols": [0, 1.0], "rows": [
            0.0, 1.0], "cells": [[0, 0, 1, 1], ]}
        self.window.run_command(command_name, command_arguments)


class InitialCheckOnLoad(sublime_plugin.EventListener):
    def on_load_async(self, view):
        global run_plugin
        global current_editing_file, data_struct

        list_of_threads = []

        file_directory = view.file_name()
        forward_slash_index_temp = file_directory.rfind('/', 0, len(file_directory))
        file_name = file_directory[forward_slash_index_temp + 1:len(file_directory)]
        #print("file name " + file_name)

        if file_name != "comments.cbrt" :
            current_editing_file = view
            #print("current editing on load " + str(current_editing_file))
            current_file_name_path = view.file_name()
            forward_slash_index = current_file_name_path.rfind(
                '/', 0, len(current_file_name_path))  # finds index of last forward slash
            # assigns the directory of the file to the variable
            # current_file_directory
            current_file_directory = current_file_name_path[0:forward_slash_index]
            #print ("path of file loaded is " + current_file_directory)
            check_for_git_repo = subprocess.Popen("git rev-parse --is-inside-work-tree", cwd=current_file_directory,
                                                  universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            if check_for_git_repo == "true\n":
                #print ("In a valid Git repo")
                run_plugin = True

                directory_of_git_folder = subprocess.Popen("git rev-parse --show-toplevel", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
                pProject_directory = directory_of_git_folder[:-1]

                # pProject_directory = "/home/shantanu/Documents/TestingGit"  #get project directory
                # pcurrent_file_directory = "/home/shantanu/Documents/TestingGit/FINAL INTEGRATION TESTING/clocksync.py"

                filevariable  =  current_file_name_path.split('/')[-1]      
                check_comments_path = pProject_directory + "/Project_Comments" +  ((current_file_name_path.split(pProject_directory)[1]).split("/"+filevariable)[0]) + "/" +filevariable.split(".")[0] + 'Comments'
                #print("This is check_comments_path"+ check_comments_path)

                #check_comments_path = current_file_directory + "/Comments"
                if os.path.exists(check_comments_path):  # check if Comments folder exists
                    list_of_threads = read_multiple_files(current_file_name_path, pProject_directory)
                    # print("on load list " + str(list_of_threads))
                    # print(str(current_file_name_path))
                    # print(str(pProject_directory))
                    data_struct[current_editing_file.id()] = list_of_threads
                    #print("keys from data_struct after updating" + str(data_struct.keys()))
                    # templist = Thread.read_thread()
                    # list_of_threads = Thread.converting_from_file_to_new_list_of_threads(templist)
            else:
                print ("Not in a Git repo")

            for thread in list_of_threads:
                view.add_regions(thread.thread_key, [
                                 thread.region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)



class SyncingDataStrutureWithFile(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        global list_of_threads
        global run_plugin
        for thread in list_of_threads:
            region_from_sublime = view.get_regions(thread.thread_key)
            thread.region = region_from_sublime[0]

        if (run_plugin == True):
            #view.run_command("call_git_stuff")
            current_file_name_path = view.file_name()
            forward_slash_index = current_file_name_path.rfind(
                '/', 0, len(current_file_name_path))  # finds index of last forward slash
            # assigns the directory of the file to the variable
            # current_file_directory
            current_file_directory = current_file_name_path[
                0:forward_slash_index]

            directory_of_git_folder = subprocess.Popen("git rev-parse --show-toplevel", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            directory_of_git_folder = directory_of_git_folder[:-1]

            Thread.WriteCreateThreadFolder(current_file_name_path, list_of_threads, directory_of_git_folder)

            sublime.status_message(str(subprocess.Popen("git status", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()))


            subprocess.Popen("git add --all", cwd=directory_of_git_folder, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message("Git add is done")

            sublime.status_message(str(subprocess.Popen("git status", cwd=directory_of_git_folder, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()))

            commit_message = subprocess.Popen("git commit -m\"Collabrotext Commit\"", cwd=directory_of_git_folder, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message(str(commit_message))
            pull_message = subprocess.Popen("git pull origin master", cwd=directory_of_git_folder, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message(str(pull_message))
            push_returned_message = subprocess.Popen("git push origin master", cwd=directory_of_git_folder, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message("Synced with Git")

    # def on_pre_close(self, view):
    #     global comment_view_obj
    #     global current_editing_file

    #     #print("editing file " + str(current_editing_file) + "\nclosed view " + str(view) + "\ncomment_view" + str(comment_view_obj))

    #     if (view == comment_view_obj):
    #         sublime.status_message("Closing UI so no action")
    #     elif(view == current_editing_file):
    #         current_window = sublime.active_window()
    #         current_window.run_command("close_layout")

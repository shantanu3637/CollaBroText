import sublime
import sublime_plugin
import os
import subprocess
from .Multiple_file import *

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

# class ExampleCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.insert(edit, 0, "Hello, World!")

# Throttle class to run on selection modifier


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
        global current_editing_file
        current_editing_file = self.view

        self.view.window().show_input_panel("Enter your comment:",
                                            'hi test comment', self.on_done, None, None)
        # sublime.set_timeout(self.close_view,1000)

    def add_new_thread(self, puser_input):

        global comment, window

        comment = str(puser_input)

        tobj = Thread(self.view.sel()[
                      0], comment_string=comment, list_of_comments=[])
        for region in self.view.sel():
            self.view.add_regions(
                tobj.thread_key, [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)
        tobj.add_thread(list_of_threads)

        # print(list_of_threads[0].list_of_comments[0].comment_string)

    def add_new_comment(self, puser_input):

        comment = str(puser_input)

        for x in list_of_threads:
            if (x.thread_key == layout_region):

                x.add_comment(comment)

    def on_done(self, user_input):

        # comment = str(user_input)
        # print comment

        in_highlight = False

        # add_new_thread(comment)
        global current_editing_file

        for thread_object in list_of_threads:
            region2 = current_editing_file.get_regions(
                thread_object.thread_key)  # thread_key gives the UUID
            region = current_editing_file.sel()
            if region2[0].contains(region[0]):
                in_highlight = True

        if in_highlight == False:
            self.add_new_thread(user_input)
        else:
            self.add_new_comment(user_input)





# Command runs when cursor position is changed. Displays comments corresponding to the region in file
# NEED TO FIX HIGHLIGHT AFTER CLOSING LAYOUT
class HighlightChange(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        # global layout_flag                      #boolean which tells if
        # layout(UI) is on or off (open or not)
        global layout_region		# if the layout is open, tells you which region it corresponds to
        global current_editing_file
        global window

        # need window obj to call other commands
        window = sublime.active_window()
        #current_view_obj = current_editing_file

        # if current cursor position is contained in a region in file and no layout is open then open layout
        # list_of_threads contains a list of objects of the thread class

        for thread_object in list_of_threads:

            region2 = current_editing_file.get_regions(
                thread_object.thread_key)  # thread_key gives the UUID
            region = current_editing_file.sel()
            # print(current_editing_file.id())
            # print(view.id())
            # print(thread_object.thread_key)
            # print(region2)
            if region2[0].contains(region[0]):
                thread_index = list_of_threads.index(thread_object)
                current_editing_file.add_regions(
                    thread_object.thread_key, region2, 'string', 'dot', sublime.HIDE_ON_MINIMAP)

                if layout_region != thread_object.thread_key:
                    if layout_region != "0":
                        window.run_command("close_layout")

                if layout_region == "0":

                    #layout_flag = True
                    layout_region = thread_object.thread_key
                    #thread_uuid = thread_object.thread_key
                    command_name = "set_layout"
                    command_arguments = {"cols": [0, 0.72, 1.0], "rows": [
                        0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]	}
                    window.run_command(command_name, command_arguments)
                    window.run_command("display_user_input", {
                                       "selected_thread_object": thread_index})
                    window.focus_view(current_editing_file)
            else:
                current_editing_file.add_regions(
                    thread_object.thread_key, region2, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

        # fixed the dual highlight problem
        # for thread_object in list_of_threads:
        # 	if layout_region != thread_object.thread_key:

        # 		region1 = current_editing_file.get_regions(thread_object.thread_key)
        # 		current_editing_file.add_regions(thread_object.thread_key, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

    thro = throttle(seconds=0.3)
    on_selection_modified = thro(on_selection_modified)


# displays content from the datastructure
class DisplayUserInputCommand(sublime_plugin.TextCommand):
    def run(self, edit, selected_thread_object):

        global comment_view_obj

        comment_view_obj = self.view
        sublime.status_message("view id of UI is set here: "+str(comment_view_obj))
        current_thread = list_of_threads[selected_thread_object]
        sum_of_chars = 0
        com_list = current_thread.list_of_comments

        for comment in reversed(com_list):
            #self.view.insert(edit, 0, "comment")
            sum_of_chars = self.view.insert(
                edit, 0, "\n" + comment.comment_string)
            split_timestamp = comment.timestamp.split(' ')
            split_only_date = split_timestamp[0].split('-')
            if(split_timestamp[0] == str(date.today())):
                final_timestamp = "Today @ " + split_timestamp[1]
            elif(split_timestamp[0] == str(date.today() - timedelta(days=1))):
                final_timestamp = "Yesterday @ " + split_timestamp[1]
            elif(split_only_date[0] == str(date.today().year)):
                final_timestamp = split_only_date[1] + "-" + split_only_date[2] + " @ " + split_timestamp[1]
            self.view.insert(edit, 0, "\n\n\n@" +
                             comment.username + "\t" + final_timestamp)

        self.view.set_scratch(True)
        self.view.set_read_only(True)

# keybind ctrl+shft+4 to close the layout manually


class CloseLayoutCommand(sublime_plugin.WindowCommand):
    def run(self):
        global comment_view_obj
        #global layout_flag
        global layout_region
        #layout_flag = False
        layout_region = "0"

        self.window.focus_view(comment_view_obj)
        self.window.run_command("close_file")

        command_name = "set_layout"
        command_arguments = {"cols": [0, 1.0], "rows": [
            0.0, 1.0], "cells": [[0, 0, 1, 1], ]}
        self.window.run_command(command_name, command_arguments)


class InitialCheckOnLoad(sublime_plugin.EventListener):
    def on_load_async(self, view):
        global list_of_threads
        global run_plugin
        global current_editing_file
        current_editing_file = view
        current_file_name_path = view.file_name()
        forward_slash_index = current_file_name_path.rfind(
            '/', 0, len(current_file_name_path))  # finds index of last forward slash
        # assigns the directory of the file to the variable
        # current_file_directory
        current_file_directory = current_file_name_path[0:forward_slash_index]
        print ("path of file loaded is " + current_file_directory)
        check_for_git_repo = subprocess.Popen("git rev-parse --is-inside-work-tree", cwd=current_file_directory,
                                              universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
        if check_for_git_repo == "true\n":
            print ("In a valid Git repo")
            run_plugin = True
            check_comments_path = current_file_directory + "/Comments"
            if os.path.exists(check_comments_path):  # check if Comments folder exists
                list_of_threads = read_multiple_files(current_file_directory)

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

            Thread.WriteCreateThreadFolder(
            current_file_directory, list_of_threads)

            sublime.status_message(str(subprocess.Popen("git status", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()))

            pull_message = subprocess.Popen("git pull origin master", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message(str(pull_message))
            subprocess.Popen("git add --all", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message("Git add is done")

            sublime.status_message(str(subprocess.Popen("git status", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()))

            commit_message = subprocess.Popen("git commit -m\"commit to git staging area\"", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.status_message(str(commit_message))

            push_returned_message = subprocess.Popen("git push origin master", cwd=current_file_directory, universal_newlines=True, shell=True, stdout=subprocess.PIPE).stdout.read()
            sublime.message_dialog("Pushed to Git")

    def on_pre_close(self, view):
        global comment_view_obj
        global current_editing_file
        if (view == comment_view_obj):
            sublime.status_message("Closing UI so no action")
        elif(view == current_editing_file):
            current_window = view.window()
            current_window.run_command("close_layout")

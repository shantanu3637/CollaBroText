# CollaBroText Plugin Summary

This plugin is used to enhance collaboration between software developers working on same project remotely in Sublime Text.
Main functionality is commenting on a file in a similar way to how Google Docs does it.   
We are using git to keep the comments synced via Github or any other site you may wish to use for your project.  

## Installation instructions
1) Clone source code to Sublime Text packages folder.



## Usage instructions

☐ Highlight text you wish to comment upon.

☐ <kbd>Alt + d</kbd>: Add new comment or reply to comment

☐ <kbd>Alt + x</kbd>: Close comment tab

☐ Click on any highlight to view its comments.

☐ To sync your comments (background Git pull & push) press <kbd> Ctrl + s</kbd> (Normal save via keyboard)


## Themes
There is an option to change the theme of the comments tab
The default theme is notebook

We have three other options in themes
  1) india
  2) forest
  3) road


<<pic of notebook theme>>

To change theme

 ☐ Go to Preferences menu in Sublime Text
  
 ☐ Go to Package Settings -> CollaBroText -> Settings-Default

 ☐ Copy contents of this file into Preferences -> Package Settings -> CollaBroText -> Settings-User
  
 ☐ Replace "notebook" to name of the theme you want and save. The theme of the comments tab will change. 

  
These are the screen shots of the working plugin


Start
![start](5.jpg?raw=true "start")

Selection
![start](4.jpg?raw=true "start")

After command alt+d entering comment
![start](3.jpg?raw=true "start")

After highlight has been added how it will look
![start](2.jpg?raw=true "start")

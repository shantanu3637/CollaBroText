# CollaBroText Plugin for Sublime Text

This plugin is used to enhance collaboration between software developers working on the same project remotely in Sublime Text.
The main functionality is commenting on a file in a similar way to how Google Docs does it.   
We are using git to keep the comments synced via Github or any other platform you may wish to use for your project.  


## Installation instructions
- Clone source code to Sublime Text `Packages` folder. (We recommend cloning via `SSH` as automatic pushing to GitHub will not be possible via `HTTPS`)



## Usage instructions

- Highlight text you wish to comment upon.

- <kbd>Alt + d</kbd>: Add new comment or reply to comment

- <kbd>Alt + x</kbd>: Close comment tab

- Click on any highlight to view its comments.

- To sync your comments (background Git pull & push) press <kbd> Ctrl + s</kbd> (Normal save via keyboard)


## Important
1) Plugin only works if file present in ssh enabled git-versioned folder.
2) Make sure that <kbd>Alt + x</kbd>: Close comment tab is used to close the comments tab.
   DO NOT CLOSE COMMENTS TAB MANUALLY by clicking on close button


## Themes
There is an option to change the theme of the comments tab
The default theme is notebook

We have three other options in themes
  1) india
  2) forest
  3) road


<pic of notebook theme>

To change theme

 - Go to Preferences menu in Sublime Text

 - Go to Package Settings -> CollaBroText -> Settings-Default

 - Copy contents of this file into Preferences -> Package Settings -> CollaBroText -> Settings-User

 - Replace "notebook" to name of the theme you want and save. The theme of the comments tab will change.


These are the screen shots of the working plugin


Start
![start](5.jpg?raw=true "start")

Selection
![selection](4.jpg?raw=true "selection")

After command alt+d entering comment
![enterComment](3.jpg?raw=true "enterComment")

After highlight has been added how it will look
![result](2.jpg?raw=true "result")

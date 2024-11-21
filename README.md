# **RANDOMLY**

Video demo: [Randomly on YouTube](https://youtu.be/8Z-FFNlgyRc)<br>
Short description: Randomly moving pixels in Python.<br><br>

---
## Running the script

The script is written in **Python 3** and requires 3 pip-installable libraries: **sys**, **random** and **pygame**.<br><br>

---
### Description

Randomly moving pixels is an old project of mine – originally brought to life in Turbo Pascal – and now implemented and improved over many iterations in Python. This might be the last version of it; an earlier version was used to act as my final project for CS50P.<br>

Randomly is not a game as such, even though it has some similarities as the speed of movement and also the colour trail of randomly moving pixels can be controlled with the cursor keys.<br>
When the program is executed, it displays the control keys:<br>

***ESC: Exit from program***<br>
***UP/DOWN: Change speed of moving pixels***<br>
***LEFT/RIGHT: Change colour of moving pixels***<br>
***SPACE: Pause/Resume***<br>

And also requests two numerical inputs from the user:<br>

***Enter the number of pixels:***<br>
***Enter the pixel size:***<br>

This later input will determine the size of the randomly moving pixel(s) on the screen – whereas size 1 is exactly the size of a single pixel.<a href="#note1" id="note1ref"><sup>1</sup></a><br>
These two inputs have soft error handling – in terms of the values – as the program will display a warning message if the number and/or the size of the pixels are above a predetermined threshold, but would still allow those higher numbers to be entered and will attempt to run the code.<a href="#note1" id="note1ref"><sup>2</sup></a><br>
Once the number and the size of pixel(s) are entered, the pixel(s) will start to move randomly and colour the black background with the default greyish colour or randomly selected colours via the left and right cursor keys.<br>
The up and down cursor keys can change the speed of the randomly moving pixel(s). Press and hold on these up and down keys will change the speed without the need of repeated key presses.<br>

When pixels collide, they change their movement randomly and would not go through each other. They cannot leave the boundary of the full screen either. Otherwise, they move freely, though randomly.<br>

Running of the program – pixel movement – can be paused and resumed with the spacebar.<br>

The program will quit if the user closes the application or hits the Esc key, or when the pixel(s) manage to paint all of the black background with their trail.<br><br>

---
### Additional information / License

There is only a single file called ***project.py*** which contains all the code.<br><br>
The repository and script have the **'None License'** option, therefore, represents this default, non-permissive state, where the work remains under full control of the creator, with no granted permissions to others. All rights to the source code retained by the owner and no one may reproduce, distribute, or create derivative works from it.<br><br>

---
### Limitations

There are some limitations as per the below warning messages from Randomly:

***Warning: Above 1000 pixels expect performance degradation!***<br>
***Warning: Above 50 pixel size the program might end suddenly!***<br>

If the number of pixels is greater than 1000, the program's performance might suffer and the random pixel movements would be slower than expected.<br>
It is possible to enter hundreds for the pixel size value (and not just anything below 50) as long as the screen's resolution is high enough or the number of pixels is very low or just one. Otherwise the screen will be filled very quickly – maybe even at the very first frame – and then the app would close abruptly.<br>
The warning messages are just rough guidelines and the combination of number and size of pixels will determine the performance of Randomply.py<br><br>

---
#### Footnote

<a id="note1" href="#note1ref"><sup>1</sup></a> About 30+ years ago, single pixel movements looked a lot more spirited on a CRT monitor with VGA (640 x 480) or SVGA (800 x 600) resolutions, as you could clearly see the individual pixels – even though CRT monitors don't have discrete pixels due to their Cathode Ray Tube technology.<br>

<a id="note1" href="#note1ref"><sup>2</sup></a> If the requested number of pixels and their sizes cannot be fitted in the start area (as they will be outside of the actual full screen), the program will exit with a fatal error message.

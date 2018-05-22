# Neuron Find Tool

This tool is used to circle ROI (regions of interest) in Neuron images

## Getting Started

Please download the zip file for this directory and unpack it.

### Prerequisites

You must have `python3`.

To check which version of python you are running simply type `python3 --version` in your terminal.
Output should look like:
```
Python 3.X.X 
```

If you do not have `python3` (any version of 3) then download `python3` and `pip` for your operating system.

Make sure the project interpreter and all of the code is Python 3.

You must have Pygame. If you do not, follow the instructions here:
http://kidscancode.org/blog/2015/09/pygame_install/

### Installing
Make sure the command is searching in the right location. Type `cd`
followed by the location where requirements.txt is stored. For example, if it's stored in your user, A, in your desktop:
```
cd /Users/A/Desktop/
```

In your terminal/bash-window call:
```
pip install -r requirements.txt
```


## Running the Tool

Now you should be able to call:
```
python3 src/main.py
```



## This will bring up a `pygame` window which you will see an image on the left and buttons on the right

![Alt Text](https://media.giphy.com/media/3gWIfrVa37glvztGOh/giphy.gif)

# Things to know about the tool

There are two stages to each image evaluation:
*   Stage 1) - "Playing" (Annotating)
      * While playing you can click on the image on the left to mark neurons with a circle
      * Hold `x` and click on a circle to remove it! (I think this should be very helpful)
      * You can `skip` a Neuron and I will not get the output for it
      * You can `undo` a change (This tool is kinda useless after I added remove but its still here)
      * And you can hit `DONE` which puts you in "Seeing Mode"
      
      Note: if you do not select any neurons, select `skip` and not `DONE`.
      
*   Stage 2) - "Seeing" (Validating)
      * In this stage you can see your ROIs on left vs Auto Generated ROIs on right
      * On the top left you can see the calculated Sensitivity and Specificity of the Auto Generated ROIs using yours as a gold standard
      * If you click `FILTER` or `RAW` you can switch between which Auto Generated ROIs you compare against
      * If you click `FIX` you can go back to "Playing" mode and output will not be saved
      * If you hit `Next` the output will be saved and you will move to the next neuron
      
### Note that all data is always saved as `(time)_file.csv`) so we know which is the most recent one

Once you are done please send me the `out_files` folder. This contains the ROIs you generated as well as the metrics.













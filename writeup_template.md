## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

Sorry for this late submission, but I was back in China and couldn't get the environment and programing set up for a long time-- at least that is one of the reasons. Here I will demonstrate how I made my approach to this project request and my comments and thought in doing so.

I will briefly talk about my feeling of toughness in each part of the project and go details in the following sections.

#### 2. Image capturing, Calibration Data, Perspective Transform and Color Thresholding

The difficult parts are about understanding the geometry. Actually, in the view of coding, it is uncessary to fully get the idea how the transforms work, whcih makes this part some what easier. What I did was just finding the four reference points of caliberating figures, figuring out what rgb values are for ground, rocks and navigable roads. There are some minor changes to identity the obstacle object in the color thresholding function that I will mention later.

#### 3. Coordinate Transformations and process_image function

Coordinate Transformation is almost the same as what I learnt in the class. I was using for loop to complete imgage coordinate transfer but it turned out to be too slow when doing autonomous driving. Instead I applied rint in translate_pix and process_image functions to get rid of loops.

#### 4. Autonomous driving and decision making

In this part, I was using a simple navigating stratrgy: follow the navigable path with mean steering angle. 
There are some special conditions set: once a rock is found, the rover will stop and try to find the rock and pick it up first. An anti-stuck setting wad made that the rover will try back up when tried to move forward but got no acceleration. But no map memorying or planing function was designed. The rover will just try to march for the navigable ground ahead.

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

I will skip the test data part since it is similar to my own data resuls. But I still usded the provided caliberating pictures to generate the perspective transform coordinates. Some of the results of the notebook are shown below.

##### 1. Results by notebook on test data

Exaple figures for caliberating:
[Example_grid figure]: Robot_project_1-master/report_folder/color_thresh.png
[Example_rock figure]: ./report_folders/rock_grid.jpg

##### 2. Perspective Transform Results 

Here are the perspective transform results of the recorded data. The sencond figure is obtained by transforming a whole white figure with the same size as captured figure. The purpose of the second figure is to cancel out the 'out of sight' part for obstacle identification in the color_thresh function.

[Perspective transform results on recorded data]: ./report_folders/perspect_trans_color.png

##### 3. Color Thresholding Results

The color thresholding resuts are shown below. Here we can see the figures ditinguished obstacle and navigable lands in a clear way. The figure on bottom left is all black since there was no rock in the original figure. The obstacle figure was captured using the same threshold values as navigable one, just in the opposite direction. And the 'out of sight' part obtained in the perspective transform function were all set to 'nonobstacle' after it.

[Color Thresholding Results of recorded data]: ./report_folders/color_thresh.png

##### 4. Coordinate Transformations results

A sample coordinate transformations result is shown below, during which rotate_pix and translate_pix functions are modified.
In the translate_pix function I used np.rint function instead of np.int so that it could handle array data, which helped getting rid of loop functons.

[Coordinate Transformations results of recorded data]: ./report_folders/Coordinate_transformations.png

##### 5. Processing stored images

Here shows the image processing function resuts. This function uses Perspective Transform funtion to tranform its captured image (from the front camera) to a top-of-view image, then uses color thresholding function to identify navigable lands and obstacle objects. After that, it will perform the coordinate transfromation function to map each point on its captured image to the world map using other telemetry information (position, yaw angle, scale).

Similar to the previous part, here I used np.rint to eliminate loops. The output image seemed to have 'opposite color' compared to its original one but turned out to be fine in the final videos. Not sure why that was happening.

[Coordinate Transformations results of recorded data]: ./report_folders/process_image.png
 
 Haven't figure out how to embed a video into this file so...
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]



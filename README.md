## Project: Search and Sample Return

This is my first robot project. It's a small project provided by Udacity robot and machine learning course. The goal of this proejct to set up a simualtion environment for a Mars Rover and develop a navigating strategy for it using its captured image. Our main task to design a navigating logic that could lead the Rover exploring as much land as possible in the given landscape.

The project report is attached below.


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

[image1]: ./misc/rover_image.jpg?raw=true
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[Example_grid figure]: ./report_folder/example_grid.png
[Example_rock figure]: ./report_folder/example_grid.png
[Perspective transform]: ./report_folder/perspect_trans_color.png
[Color Thresholding]: ./report_folder/color_thresh.png
[Coordinate]: ./report_folder/Coordinate_transformations.png 
[Processing stored images]: ./report_folder/process_image.png
[good]: ./report_folder/good.png

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

![Example grid figure][Example_grid figure]

##### 2. Perspective Transform Results 

Here are the perspective transform results of the recorded data. The sencond figure is obtained by transforming a whole white figure with the same size as captured figure. The purpose of the second figure is to cancel out the 'out of sight' part for obstacle identification in the color_thresh function.

![Perspective transform results][Perspective transform]

##### 3. Color Thresholding Results

The color thresholding resuts are shown below. Here we can see the figures ditinguished obstacle and navigable lands in a clear way. The figure on bottom left is all black since there was no rock in the original figure. The obstacle figure was captured using the same threshold values as navigable one, just in the opposite direction. And the 'out of sight' part obtained in the perspective transform function were all set to 'nonobstacle' after it.

![Color Thresholding results][Color Thresholding]

##### 4. Coordinate Transformations results

A sample coordinate transformations result is shown below, during which rotate_pix and translate_pix functions are modified.
In the translate_pix function I used np.rint function instead of np.int so that it could handle array data, which helped getting rid of loop functons.

![Coordinate Transformations results of recorded data][Coordinate]

##### 5. Processing stored images

Here shows the image processing function resuts. This function uses Perspective Transform funtion to tranform its captured image (from the front camera) to a top-of-view image, then uses color thresholding function to identify navigable lands and obstacle objects. After that, it will perform the coordinate transfromation function to map each point on its captured image to the world map using other telemetry information (position, yaw angle, scale).

Similar to the previous part, here I used np.rint to eliminate loops. The output image seemed to have 'opposite color' compared to its original one but turned out to be fine in the final videos. Not sure why that was happening.

![Processing stored images results][Processing stored images]
 
 I haven't figure out how to embed a video in md file so it is not attached. :p
 
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

##### 1. Perception function

The perception function I used was quite alike the one I came out with in the notebook. Aside from small modification such as image sources and putting transform coordinates inside function, the major change I have made is to sets thresholds for the map updating fucntion. 
Because the perspective transform accuracy is depends on the rover pitch and roll angles, the rover controller should update its map information only when these two parameters are close to zeros (or 360 degrees). Therefore, a conditional statement was made that:

if Rover.pitch and Rover.roll satisfy conditions:
   update Rover.worldmap
   
 It was set to both navigable and obstacle mapping.
 
 Another variable I introduced in the perception function is a rock detection indicator Rover.samples_insight, which tells if there is a rock being detected by the rover in its view. The indicator will be set to 1 if any pix in rover's captured figure is identified as 'rock'.
 
 ##### 2. Decision function
 
 A simple navigating algorithm was applied in the decision function: the rover will follow the mean value of its detected navigable angles most of the time, but there are some small modifications that were made in the decision making process.
 
 ###### 1. Rock detecting and approaching
 
 The rover will stop immediately once its rock detecing indicator is triggered, and turns its driving mode to 'rock'. In this mode, the rover will reduce both its default throttle and maximum speed to their half and trying to locate the rock. The steering angle will be controlled by the detected rock image angles. Once the Rover.near_sample is true, the rover will stop and pick the rock. After picking up one rock, the rover will shift back to 'forward' mode.
 
 ###### 2. Anti-Stuck operation
 
 An counter called Rover.stuck_count is set for the rover to calculate how long it has been trying to move but failed. Once it reaches the preset value, the rover will set its throttle to a negative value, wag the steer and try to back up and get out. It is quite helpful when the rover was driving towards the walls with specifical angles and get stuck on the slopes. But it won't help when rover was caught in the big rocks. 
 
 ###### 3. Shift steer when backing
 
 A small modification: change the steer to its opposite direction when the rover celocity is negative. This will help the rover to turn a little faster when operating the anti-stuck moves.
 
 

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

I have run the automous mode simulation severals time. The screen resolution was 1024*768, graphics quality was set to 'good'. The FPS observed during the simulation was around 10 (which was 1 when I using loops in decision and perspective functions).

Sometimes the rover can map  more than 60% of the surface and some times just 30% denpending on the initial facing and location. And there is a big chance the rover keep circulating in a large open area. I have introduce some random steering in to preventing that but it still occurs.

The fidelity highly depends on the threshold I set in the perception function. With the pitch and roll angle thresholds set to 0.2, the rover can always have a fidelity over 60%. The rover can pick up the rock samples almost evey time. 

One big issue is that the rover is easily get stucked in the 'rock cluster' area in the middle of the map, which is mainly caused by their steering strategy.
A screen shot of the rover is shown below:

![Rover performance (good one)][good]


To improve the performance of the rover, I have come up with several thoughts:

##### 1. Building a map navigating system
 
 This system will allow rover to read information from its known map and decide its 'large' driving direction, so that it will not revisit the known place and tend to explore the unexplored lands. This process is related to both path searching and plannning, which takes more memory and computing ability.

##### 2. More information of rover

 Often times the rover was stucked between rocks and 'rock clusters' on the ground. Therefore, it might be better if the rover has the following information: height and width of the rover, clearance between ground and its underpan, height of camera and distances betwwen camera and its edges. With these infomation it maybe easir for the rover to decide if it can make it through a slit or run safely over a bunch of gallets.
 
##### 3.Better computing method
 
 In my simulation the fps is about 10, which requires the rover to maintain a slow speed so that it does not have to react fast. If there are some other programing tricks we can play and make that processing speed double, it is possible to have the rover running at a higher speed and efficiency.
 
 That is what came out of my mind for now.
 Thank you!



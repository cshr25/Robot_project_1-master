import numpy as np
import random


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):
    # get roll and pitch angles
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward' and not Rover.picking_up:
            Rover.brake = 0
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good
                # set driving direction
                if Rover.vel > 0:
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi)-random.randint(-5,5)-5, -15, 15)
                else:
                    Rover.steer = - np.clip(np.mean(Rover.nav_angles * 180/np.pi)-random.randint(-5,5)-5, -15, 15)
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    # count how long we have been in 'slow motion' mode
                    if Rover.vel < 0.2:
                        Rover.stuck_count += 1
                    else:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.vel < -1:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.stuck_count < 50 or Rover.back > 50: # if we haven't been 'slow' for long or have been drive back for a while
                        # Set throttle value to throttle setting and not stucked
                        Rover.throttle = Rover.throttle_set
                        
                    else:
                        Rover.throttle = - Rover.throttle_set # try drive back
                        Rover.steer = random.randint(-10,10) #try different steer
                        Rover.back += 1
                        
                elif Rover.vel >= Rover.max_vel: # Else coast
                    Rover.throttle = 0
                    Rover.brake = 0
                    # everything goes well
                    Rover.stuck_count = 0
                    Rover.back += 1
                
                    
                
                
                    
            if Rover.samples_insight==1: #rock found
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'rock' #enter rock searching mode
                
            elif len(Rover.nav_angles) < Rover.stop_forward:
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'stop'
                
        elif Rover.mode == 'rock':
            # find the rock direction
            # far detecting
                    
            Rover.brake = 0
            if Rover.samples_insight == 1:
                if Rover.vel > 0:
                    Rover.steer=np.mean(Rover.rock_angle * 180/np.pi)
                else: 
                    Rover.steer= - np.mean(Rover.rock_angle * 180/np.pi)
                Rover.rockcount = 0
                if Rover.vel < Rover.max_vel/2:
                    Rover.throttle = Rover.throttle_set/2
                    Rover.brake = 0
                else:
                    Rover.throttle = 0
                    Rover.brake = 0
                
            else:                
                Rover.rockcount += 1
                if Rover.rockcount >=10:
                    Rover.brake = Rover.brake_set
                else:
                    Rover.brake = 0
                    Rover.steer = 15 * np.sign(np.mean(Rover.rock_angle)) #lost track of rock? keep searching!
                    Rover.rockcount = 0
                    
            
            if Rover.near_sample: #close enough?
                Rover.brake=1
                Rover.throttle = 0
                Rover.rockcount = 0
                
                
            # anti_block operation       
            if Rover.vel < Rover.max_vel:
                    # count how long we have been in 'slow motion' mode
                    if Rover.vel < 0.5:
                        Rover.stuck_count += 1
                    else:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.vel < -0.5:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.stuck_count < 50 or Rover.back > 50: # if we haven't been 'slow' for long or have been drive back for a while
                        # Set throttle value to throttle setting and not stucked
                        Rover.throttle = Rover.throttle_set/2
                        
                        
                    else:
                        Rover.throttle = - Rover.throttle_set # try drive back
                        Rover.steer = random.randint(-10,10) #try different steer
                        Rover.back += 1
                        Rover.mode = 'forward'
                        
                    

      # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward or np.mean(Rover.nav_dist) < 100:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 15
                    Rover.mode = 'forward'    
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
   
    
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.brake = 0
        Rover.mode = 'forward'
    
    return Rover


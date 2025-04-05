import cv2
import numpy as np
from Lib.Graphics.AnalogGauge import AnalogGauge

class Speedometer:
    def __init__(self, image: np.ndarray, type="analog", MaxValue=240):
        """
        Initializes the Speedometer instance.

        Parameters:
            image (np.ndarray): The main window image (background).
            type (str): The type of speedometer ("analog" or other types).
            MaxValue (int): The maximum speed value.
            MinValue (int): The minimum speed value.
        """
        self.type = type
        self.base_image = image
        self.MaxSpeed = MaxValue
        self.current_speed = 0

        if self.type == "analog":
            self.speed_gauge = AnalogGauge(
                image=self.base_image,
                max_value=self.MaxSpeed,
                min_value=0,
                minor_marks=20,
                units='km/h',
                arch=180,
                phase=180)
            self.speed_gauge.SetValue(self.current_speed)
        self.speed_gauge.update_display()

    def draw(self):
        """
        Updates the display of the speedometer.

        Returns:
            np.ndarray: The updated base image with the speedometer overlayed.
        """
        self.speed_gauge.update_display()

        
    
    def set_speed(self, speed):
        """
        Updates the speed value.

        Parameters:
            speed (int): The new speed value.
        """
        if( self.current_speed != speed):
            self.current_speed = speed
            self.speed_gauge.SetValue(speed) 
            self.speed_gauge.update_display()



if __name__ == "__main__":
    # Define the size of the main window
    imagename = 'speedometer'
    window_size = (500, 800, 3)
    MaxSpeed = 240
    MinSpeed = 0
    speed = 0
    imagecontainer= np.zeros(window_size, dtype=np.uint8)
    imagecontainer[:, :] = (0, 0, 0)  # Black background

    # Create the Speedometer instance
    speedometer = Speedometer(image=imagecontainer, type = "analog", MaxValue = MaxSpeed)
    # Create window image
    cv2.namedWindow(imagename)
    cv2.imshow(imagename, imagecontainer)

    while True:
        # Display the updated image in the window
        #cv2.imshow(imagename, imagecontainer)
        # Wait for a key press
        # 0xFF is used to mask the key value to get the last 8 bits
        key = cv2.waitKey(1) & 0xFF

        # Exit if 'q' is pressed
        if key == ord('q'):
            break
        if key == ord('a'):
            # set speedometer speed value to 0
            speed = int(0)

        if key == ord('b'):
            # Update speedometer speed value to 25
            speed = int((MaxSpeed * 0.25))

        if key == ord('c'):
            # Update speedometer speed value
            speed = int((MaxSpeed * 0.50))

        if key == ord('d'):
            # Update speedometer speed value
            speed = int((MaxSpeed * 0.75))

        if key == ord('e'):
            # Update speedometer speed value
            speed = int(MaxSpeed)

        if key == ord('+'):
            # Update speedometer speed value
            speed = speed + 5
            if speed > MaxSpeed:
                speed = MaxSpeed

        if key == ord('-'):
            # Update speedometer speed value
            speed = speed - 5
            if speed < MinSpeed:
                speed = MinSpeed
        
        # Update speedometer speed value    
        speedometer.set_speed(speed)
        cv2.imshow(imagename, imagecontainer)

    
    cv2.destroyAllWindows()
import cv2
import numpy as np
from .Lib.Graphics.AnalogGauge import AnalogGauge

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
                image=base_image,
                max_value=self.MaxSpeed,
                min_value=0,
                minor_marks=20,
                units='km/h',
                arch=180,
                phase=180)
            self.speed_gauge.needle_position_range = self.current_speed
        

    def draw(self):
        """
        Updates the display of the speedometer.

        Returns:
            np.ndarray: The updated base image with the speedometer overlayed.
        """
        # Draw the speedometer gauge
        speed_img = self.speed_gauge.update_display()

        return speed_img
    
    def set_speed(self, speed):
        """
        Updates the speed value.

        Parameters:
            speed (int): The new speed value.
        """
        if( self.current_speed != speed):
            self.current_speed = speed

        self.speed_gauge.update_value(speed)



if __name__ == "__main__":
    # Define the size of the main window
    window_size = (500, 800, 3)
    base_image = np.zeros(window_size, dtype=np.uint8)
    base_image[:, :] = (0, 0, 0)  # Black background

    # Create the Speedometer instance
    speedometer = Speedometer(image=base_image, type = "analog", MaxValue=240)
    base_image = speedometer.draw()

    cv2.imshow("speedometer", base_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
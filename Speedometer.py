import cv2
import keyboard
import numpy as np
from Lib.Graphics.AnalogGauge import AnalogGauge

class Speedometer:
    def __init__(self, height=500, width=800, type="analog"):
        self.type = type
        self.MaxSpeed = 180
        self.MaxRPM = 8000
        self.width = width
        self.height = height
        
        #define the size (width,height) of the windows
        self.GaugeSize = (300,300)

        self.base_image = np.zeros((height, width, 3), dtype=np.uint8)
        self.bg_color = (0, 0, 0)
        self.base_image[:] = self.bg_color

        if self.type == "analog":
            self.speed_gauge = AnalogGauge(
                width = self.GaugeSize[0], height = self.GaugeSize[1], max_value=self.MaxSpeed, min_value= 0, minor_marks = 20, units='km/h',
                arch=180, phase=180
                )
            self.tachometer_gauge = AnalogGauge(
                width = self.GaugeSize[0], height = self.GaugeSize[1], max_value=self.MaxRPM, minor_marks = 2000, units='RPM',
                arch=180, phase=180
                )
        
        self.speed_pos = (width//2 - 320, 50)
        self.tacho_pos = (width//2 + 20, 50)
        
        cv2.namedWindow("Speedometer", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Speedometer", self.width, self.height)
    
    def update_display(self):
        self.base_image[:] = self.bg_color
        
        speed_img = self.speed_gauge.update_display()
        tacho_img = self.tachometer_gauge.update_display()
        
        x1, y1 = self.speed_pos
        self.base_image[y1: y1 + self.GaugeSize[1], x1: x1 + self.GaugeSize[0]] = speed_img
        
        x2, y2 = self.tacho_pos
        self.base_image[y2: y2 + self.GaugeSize[1], x2: x2 + self.GaugeSize[0]] = tacho_img
        
        return self.base_image


if __name__ == "__main__":
    speedometer = Speedometer(height=500, width=800)
    speed = 0
    rpm = 0
    while True:
        speedometer.speed_gauge.needle_angle = speed
        speedometer.tachometer_gauge.needle_position_range = rpm

        img = speedometer.update_display()
        
        cv2.imshow("Speedometer", img)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('+'):
            speed = speed +10
            rpm = rpm + 1000
        elif key == ord('-'):
            speed = speed - 10
            rpm = rpm - 1000

    cv2.destroyAllWindows()
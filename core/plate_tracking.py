from core.plate_detect import *
from core.IFrame import *
import math as math

boxes_distance_threshold = 10

undetectableTime = 500

class FramesStorage:
    detected_plates = []
    last_index = 0

    def __init__(self):
        self.detected_plates = []

    def AddPlate(self, frame):
        plate_id = self.last_index
        self.last_index += 1

        detected_plate = DetectedCar(plate_id, frame)

        self.detected_plates.append(detected_plate)

        return plate_id

    def ClearLongTimeUndetectableCars(self, current_time):

        # Reverse loop
        for i in range(len(self.detected_plates), 0, -1):
            cur_ind = i - 1

            plate = self.detected_plates[cur_ind]
            last_frame = plate.GetLastFrame()
            if last_frame.GetTime() + undetectableTime < current_time:
                self.detected_plates.pop(cur_ind)


    def GetCarId(self, time, bounding_box, crop_img):

        plate_frame = CarFrame(time, bounding_box, crop_img)

        newBoxCenter = [bounding_box[0] + (int(bounding_box[2] - bounding_box[0]) / 2), bounding_box[1] + (int(bounding_box[3] - bounding_box[1]) / 2)]

        if len(self.detected_plates) > 0:

            near_plate = None
            near_dist = 999

            for i in range(len(self.detected_plates)):
                plate = self.detected_plates[i]

                lastBox = plate.GetLastFrame().GetBoundingBox()
                lastCarCenter = [lastBox[0] + (int(lastBox[2] - lastBox[0]) / 2), lastBox[1] + (int(lastBox[3] - lastBox[1]) / 2)]

                distanceToCenter = math.sqrt((lastCarCenter[0] - newBoxCenter[0])**2 + (lastCarCenter[1] - newBoxCenter[1])**2)

                if distanceToCenter < near_dist:
                    near_plate = plate
                    near_dist = distanceToCenter

            if near_dist < boxes_distance_threshold:
                plate_id = near_plate.GetId()
                near_plate.AddFrame(plate_frame)
            else:
                plate_id = self.AddPlate(plate_frame)
        else:
            plate_id = self.AddPlate(plate_frame)

        return plate_id

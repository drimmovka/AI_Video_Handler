from ultralytics import YOLO
from copy import copy
import cv2
import csv
import numpy
import torch

INTERRUPT_FRAMES_NUMBER       = 4
DETECTION_ERROR_FRAMES_NUMBER = 1
PAPER_CLASS                   = 2


class ShowTime:
    # the class used to display the time of occurrence of the detection object
    
    def __init__(self):
        self.start = None
        self.end = None


class Object:
    # the class for describing detection object
    
    def __init__(self, name: str):
        self.name = name                # the name of the object to be recorded in the report file
        
        self.show_times = [ShowTime()]  # the object may appear several times per video initially. The show_times contains ShowTime() 
                                        # with (start, end) == (None, None) showing that the object has not appeared yet


    def reappeared(self, frame_number: int) -> bool:
        # checks if the object has appeared in the video again (or first time)

        return (len(self.show_times) == 1 or frame_number - self.show_times[-1].end > INTERRUPT_FRAMES_NUMBER)


class VideoHandler:
    # the class to process video and record a report
    
    def __init__(self):
        
        self.object_detection_model = YOLO("../models/objects_640.pt")
        self.digit_detection_model = YOLO("../models/digits_640.pt")
        
        self.objects = {
            0:  Object("SSD накопитель"),
            1:  Object("Колонка"),
            2:  Object("Лист"),
            3:  Object("Лист с цифрой 0"),
            4:  Object("Лист с цифрой 1"),
            5:  Object("Лист с цифрой 2"),
            6:  Object("Лист с цифрой 3"),
            7:  Object("Лист с цифрой 4"),
            8:  Object("Лист с цифрой 5"),
            9:  Object("Лист с цифрой 6"),
            10: Object("Лист с цифрой 7"),
            11: Object("Лист с цифрой 8"),
            12: Object("Лист с цифрой 9"),
        }
    
    
    def process_video(self, input_file_path: str, output_file_path: str, report_path: str) -> None:
        # opens input/output files and processes video frames in a loop,
        # records information about the show time of objects
        
        # open input video
        fin = cv2.VideoCapture(input_file_path)
        
        # check if input video hasn't been opened
        if not fin.isOpened():
            raise Exception("Error: couldn't open input video.")
        
        # get input video fps and dimensions
        fps = int(fin.get(cv2.CAP_PROP_FPS))
        width = int(fin.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(fin.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")        
        fout = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))
        
        
        frame_number = 0
        
        while fin.isOpened():

            # read frame from input video
            success, frame = fin.read()

            if not success:
                break
            
            self.__process_frame(frame, frame_number)
            fout.write(frame)
            frame_number += 1
        
        # release the input video capture and output video writer
        fin.release()
        fout.release()
        
        self.__write_report(report_path, fps)

    

    def __process_frame(self, frame: numpy.ndarray, frame_number: int) -> None:
        # runs the model to find objects on the entire frame and starts processing bounded area,
        # where the found objects are located
        
        results = self.object_detection_model(frame, conf=0.65, imgsz=640, verbose=False)
        result = results[0]
        
        for boundings in result.boxes.xyxy:
            self.__process_segment(frame, boundings, frame_number)



    def __process_segment(self, frame: numpy.ndarray, boundings: torch.Tensor, frame_number: int) -> None:
        # finds objects on a bounded area of the frame, applies a mask, 
        # inverts the color by it, updates the show_time of objects
        
        # get boundings
        x0, y0, x1, y1 = map(int, boundings)
        k = 0.65
        x0 -= round((x1 - x0) * k)
        x1 += round((x1 - x0) * k)
        y0 -= round((y1 - y0) * k)
        y1 += round((y1 - y0) * k)
        
        # extract the bounding box from the frame
        bounding_box = frame[y0:y1, x0:x1]
        
        results = self.object_detection_model(bounding_box, imgsz=640, conf=0.65, iou=0, retina_masks=True)
        result = results[0]
        
        # check if smth was found
        if (result.masks == None or result.boxes == None):
            return

        masks = result.masks.data.cpu().numpy().astype(int)
        detected_classes = result.boxes.cls.cpu().numpy().astype(int)

        # applying masks and calculating time for report
        for mask, detected_class in zip(masks, detected_classes):
            
            # inverse color in mask
            bounding_box[mask > 0] = cv2.bitwise_not(bounding_box)[mask > 0]
            frame[y0:y1, x0:x1] = bounding_box
            
            # if the object is a piece of paper, func runs a second model to find the digits
            if detected_class == PAPER_CLASS:
                self.__detect_digits(bounding_box, frame_number)

            self.__update_object_show_times(detected_class, frame_number)
    
    
    
    def __detect_digits(self, bounding_box: numpy.ndarray, frame_number: int) -> None:
        # finds the numbers on a bounded area of the frame
        # updates the show_time of a digit objects
        
        digit_detection_results = self.digit_detection_model(bounding_box, imgsz=640, conf=0.8, iou=0, verbose=False)
        digit_detection_result = digit_detection_results[0]
        
        if digit_detection_result.boxes != None:
            
            detected_classes = digit_detection_result.boxes.cls.cpu().numpy().astype(int)
            for detected_class in detected_classes:
                self.__update_object_show_times(detected_class + PAPER_CLASS + 1, frame_number)
    
    
    
    def __update_object_show_times(self, class_idx: int, frame_number: int) -> None:
        # records for the detected object its appearance time
        
        object = self.objects[class_idx]
        
        if object.reappeared(frame_number):
            object.show_times.append( copy(object.show_times[-1]) )
            object.show_times[-1].start = frame_number
        
        object.show_times[-1].end = frame_number
    


    def __write_report(self, report_path: str, fps: int) -> None:
        # output information about the show time (in ms) of detected objects to the report file
        
        report = open(report_path, "w")
        writer = csv.writer(report, lineterminator='\n')
        
        for object_class in self.objects:
            for show_time in self.objects[object_class].show_times[1:]:
                if (show_time.end - show_time.start > DETECTION_ERROR_FRAMES_NUMBER):
                    row = [f"{self.objects[object_class].name} появилось на видео в {show_time.start * 1000 / fps}, исчезло из кадра в {show_time.end * 1000 / fps}"]
                    writer.writerow(row)
        
        report.close()
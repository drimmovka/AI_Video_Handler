import cv2
from ultralytics import YOLO
import numpy as np


# remove extra modules
def process_video(model, input_video_path, show_video=True, save_video=False, output_video_path="output.mp4"):
    # open input video
    source = cv2.VideoCapture(input_video_path)

    # check if input video hasn't been opened
    if not source.isOpened():
        raise Exception("Error: couldn't open input video.")

    # get input video fps and dimensions
    fps = int(source.get(cv2.CAP_PROP_FPS))
    width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        output = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while source.isOpened():
        success, frame = source.read()
        if not success:
            break

        # for testing without model (comment "for usage with model" and uncomment this section)
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (0, 0), (800, 600), 255, -1)

        frame[mask > 0] = cv2.bitwise_not(frame)[mask > 0]

        # for usage with model (comment "for testing without model" and uncomment this section)
        """
        results = model.track(frame, iou = 0.5, conf = 0.8, persist = True, imgsz = 640, verbose = False, traker = "botsort.yaml")
        # model - our trained model
        # iou - intersection over union (the degree of overlap between two bounding boxes of true and predicted object (lower == more strict))
        # conf - confidence (in guessing the object from 0 to 1)
        # persist is used for tracking
        # imgsz - image size used in model
        # verbose - show logs in terminal
        # tracker file can be configured
        # add "classes = n" to track class with number "n" or don't to track all

        if results[0].boxes.id != None: # if the are objects to track
            #getting mask from model
            masks = results[0].masks.data.cpu().numpy().astype(int)
            
            # for each tracked object inverting it's colors by mask
            for mask in masks:
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation = cv2.INTER_NEAREST)
                
                frame[mask > 0] = cv2.bitwise_not(frame)[mask > 0]
        """

        if save_video:
            output.write(frame)

        if show_video:
            cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    source.release()
    if save_video:
        output.release()

    cv2.destroyAllWindows()


# for testing

# with model
# model = YOLO("path_to_best.pt")

# without model
model = "model"

process_video(model, "input.mp4", show_video=False, save_video=True)

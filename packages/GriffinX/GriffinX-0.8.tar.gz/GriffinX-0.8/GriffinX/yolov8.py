import torch
import os
import cv2

def initialize_yolov8():
    print("hellov8!!!!!")
    model_yolov8 = YOLO('yolov8n.pt')

def detect_and_save_cars_v8(partition, output_folder):
    # Detect cars using YOLOv8
    print("hellov8 detect!")
    results = model_yolov8(partition.copy())  # copy of the partition to avoid altering 

    for r in results.pred:
        boxes = r['boxes']
        for box in boxes:
            left, top, right, bottom = map(int, box[:4])

        # Draw rectangle and label on the frame
            cv2.rectangle(partition, (left, top), (right, bottom), (0, 255, 0), 2) 
            label = model_yolov8.names[int(box[5])]
            confidence = float(box[4])
            text = f"{label} {confidence:.2f}"
            cv2.putText(partition, text, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA) 

# Save the partition with detected cars
    cv2.imwrite(os.path.join(output_folder, f"partition_{selected_partition_index}_yolov8.jpg"), partition)
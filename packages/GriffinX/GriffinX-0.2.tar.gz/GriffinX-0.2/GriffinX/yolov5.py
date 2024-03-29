def initialize_yolov5():
        model_yolov5 = torch.hub.load("ultralytics/yolov5:v6.0", "yolov5s", pretrained=True)
        model_yolov5.eval()

def detect_and_save_cars(self, partition, output_folder, conf_threshold=0.5):
    # Detect cars using YOLOv5
        results = model_yolov5(partition)

    # Filter bounding boxes based on confidence threshold
        mask = results.xyxy[0][:, 4] >= conf_threshold
        boxes = results.xyxy[0][mask, :4]
    
    # Draw bounding boxes around detected cars
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(partition, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Save the partition with detected cars
        cv2.imwrite(os.path.join(output_folder, f"partition_{selected_partition_index}_yolov5.jpg"), partition)
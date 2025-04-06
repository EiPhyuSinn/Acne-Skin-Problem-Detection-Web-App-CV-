import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
model = YOLO("/Users/eiphyusinn/Desktop/Acne_detection/train2/weights/best.pt") # Load model at startup

@app.post("/detect")
async def detect(file: UploadFile):
    # Process the uploaded image for object detection
    image_bytes = await file.read()
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Perform object detection with YOLOv8
    detections = model.predict(image)

    # Extract bounding box data
    boxes = detections[0].boxes.xyxy.cpu().numpy()
    scores = detections[0].boxes.conf.cpu().numpy()
    classes = detections[0].boxes.cls.cpu().numpy()

    # Format the results as a list of dictionaries
    # results = []
    # for box, score, cls in zip(boxes, scores, classes):
    #     results.append({
    #         'x1': box[0],
    #         'y1': box[1],
    #         'x2': box[2],
    #         'y2': box[3],
    #         'confidence': score,
    #         'class': int(cls)
    #     })

    return {'detections': boxes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
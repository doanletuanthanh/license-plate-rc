from ultralytics import YOLO
from paddleocr import PaddleOCR, draw_ocr
import cv2

custom_rec_model_dir = "en_PP-OCRv3_rec_slim_infer.tar"
ocr = PaddleOCR(rec_model_dir=custom_rec_model_dir, use_angle_cls=True, lang='en', det=False, cls=False, rec=True, use_gpu=False)
model = YOLO("train/kaggle/working/runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    if cv2.waitKey(1) == ord('a'):
        results = list(model(frame, stream=True, conf=0.5))
        if results:
            boxes = results[0].boxes.xyxy.int().cpu().numpy()
            cropped_images = [frame[y1:y2, x1:x2] for x1, y1, x2, y2 in boxes]
            if cropped_images:
                result = ocr.ocr(cropped_images[0])
                if result and result[0]:  # check that result[0] is not None
                    for line in result[0]:
                        text = line[1][0]
                        confidence = line[1][1]
                        print(f"Detected text: {text}, Confidence: {confidence}")
        else:
            print("No text detected.")
        
    cv2.imshow('Webcam', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

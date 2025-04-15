from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
import os
from io import BytesIO

app = FastAPI()

# Load models
ocr = PaddleOCR(rec_model_dir='models/en_PP-OCRv3_rec_slim_infer', use_angle_cls=True, lang='en', det=False, cls=False, rec=True, use_gpu=False)
detector = YOLO("train/kaggle/working/runs/detect/train/weights/best.pt")

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recognize/")
async def recognize_plate(file: UploadFile = File(...)):
    contents = await file.read()
    image_np = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

    results = detector(image_np)
    if not results or not results[0].boxes:
        return JSONResponse({"text": "No plates detected."})

    boxes = results[0].boxes.xyxy.int().cpu().numpy()
    cropped_images = [image_np[y1:y2, x1:x2] for x1, y1, x2, y2 in boxes]

    text_results = []
    for img in cropped_images:
        ocr_result = ocr.ocr(img)
        if ocr_result and ocr_result[0]:
            for line in ocr_result[0]:
                text = line[1][0]
                conf = line[1][1]
                text_results.append({"text": text, "confidence": conf})

    return JSONResponse({"results": text_results})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # default to 8000 locally
    print(f"🚀 App is running on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
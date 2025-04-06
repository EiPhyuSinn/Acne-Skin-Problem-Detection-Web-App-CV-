from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
import uvicorn
from datetime import datetime
from ultralytics import YOLO


app = FastAPI()
CLASS_NAMES = ['Hidden acne', 'Cysts', 'Blackhead', 'Whitehead', 'Pustules', 'Nodular acne', 'Acne', 'Birthmark', 'Milium', 'Papular', 'Purulent', 'Scars']
problems = []
templates = Jinja2Templates(directory="templates")

# Mount static files (for CSS, JS, and images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the YOLOv8 model
model = YOLO("/Users/eiphyusinn/Desktop/Acne_detection/train2/weights/best.pt")  # Load model at startup

def detect_skin_problems(image_np):
    global problems
    problems = []  # Reset problems list for each request

    # Perform inference
    results = model(image_np)

    # Process results
    annotated_images = []
    for result in results:
        # Extract detected problems
        for i in result.boxes.cls.numpy():
            problem = CLASS_NAMES[int(i)]
            if problem not in problems:
                problems.append(problem)

        # Generate annotated image
        annotated_image = result.plot()  # Get the annotated image (BGR format)
        annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        annotated_images.append(annotated_image_rgb)

    return problems, annotated_images

def recommend_products(problems):
    recommendations = {
        "Hidden acne": [
            "Salicylic Acid Cleanser",
            "Niacinamide Serum",
            "Retinol Cream"
        ],
        "Cysts": [
            "Benzoyl Peroxide Spot Treatment",
            "Tea Tree Oil",
            "Warm Compress"
        ],
        "Blackhead": [
            "Charcoal Face Mask",
            "Salicylic Acid Toner",
            "Clay Cleanser"
        ],
        "Whitehead": [
            "Glycolic Acid Exfoliator",
            "Salicylic Acid Cleanser",
            "Non-comedogenic Moisturizer"
        ],
        "Pustules": [
            "Benzoyl Peroxide Gel",
            "Sulfur Spot Treatment",
            "Aloe Vera Gel"
        ],
        "Nodular acne": [
            "Prescription Retinoids",
            "Oral Antibiotics (consult a dermatologist)",
            "Cortisone Injection (consult a dermatologist)"
        ],
        "Acne": [
            "Salicylic Acid Cleanser",
            "Benzoyl Peroxide Cream",
            "Tea Tree Oil"
        ],
        "Birthmark": [
            "Laser Treatment (consult a dermatologist)",
            "Concealer for Cosmetic Coverage",
            "Sunscreen to Prevent Darkening"
        ],
        "Milium": [
            "Exfoliating Cleanser",
            "Retinol Cream",
            "Professional Extraction (consult a dermatologist)"
        ],
        "Papular": [
            "Salicylic Acid Toner",
            "Azelaic Acid Cream",
            "Non-comedogenic Moisturizer"
        ],
        "Purulent": [
            "Antibacterial Cleanser",
            "Warm Compress",
            "Topical Antibiotics (consult a dermatologist)"
        ],
        "Scars": [
            "Silicone Scar Gel",
            "Vitamin C Serum",
            "Microneedling (consult a dermatologist)"
        ],
        "No significant skin issues detected!": [
            "Gentle Cleanser",
            "Hydrating Moisturizer",
            "Broad-Spectrum Sunscreen"
        ]}
    return [recommendations.get(problem, []) for problem in problems]

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    # Read and process the image
    image_bytes = await file.read()
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Detect skin problems and get annotated images
    problems, annotated_images = detect_skin_problems(image_np)

    if not problems:
        problems = ["No significant skin issues detected!"]

    # Save the annotated image
    output_path = "static/annotated_image.jpg"
    cv2.imwrite(output_path, cv2.cvtColor(annotated_images[0], cv2.COLOR_RGB2BGR))  # Save as BGR for OpenCV

    # Recommend products
    product_recommendations = recommend_products(problems)
    timestamp = int(datetime.now().timestamp())
    annotated_image_url = f"/static/annotated_image.jpg?t={timestamp}"

    return JSONResponse({
        "problems": problems,
        "recommendations": product_recommendations,
        "annotated_image_url": annotated_image_url,  # URL to the annotated image
    })

@app.get("/")
async def home():
    return templates.TemplateResponse("index.html", {"request": {}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
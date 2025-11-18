from fastapi import UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import time
import os

from app.liveness.src.anti_spoof_predict import AntiSpoofPredict
from app.liveness.src.generate_patches import CropImage
from app.liveness.src.utility import parse_model_name

MODEL_DIR = "./app/liveness/resources/anti_spoof_models"
DEVICE_ID = 0

model_test = AntiSpoofPredict(DEVICE_ID)
image_cropper = CropImage()


def check_image(image):
    height, width, channel = image.shape
    if abs((width / height) - (3/4)) > 0.01:
        return False, "Image is not appropriate! Height/Width should be 4/3."
    return True, ""


def predict_liveness(image):
    result, msg = check_image(image)
    if not result:
        return {"status": "error", "message": msg}

    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    test_speed = 0

    for model_name in os.listdir(MODEL_DIR):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": image,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False

        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, f"{MODEL_DIR}/{model_name}")
        test_speed += time.time() - start

    label = int(np.argmax(prediction))
    value = float(prediction[0][label] / 2)
    result_text = "RealFace" if label == 1 else "FakeFace"

    return {
        "status": "success",
        "result": result_text,
        "score": value,
        "bbox": image_bbox,
        "prediction_time": test_speed,
    }




def resize_to_aspect_ratio(image, target_ratio=3 / 4):
    """
    Resize image to match target aspect ratio (width/height).
    Uses intelligent cropping to maintain the center of the image.

    Args:
        image: Input image
        target_ratio: Target width/height ratio (default 3/4)

    Returns:
        Resized image with correct aspect ratio
    """
    height, width = image.shape[:2]
    current_ratio = width / height

    if abs(current_ratio - target_ratio) < 0.01:  # Already correct ratio
        return image

    if current_ratio > target_ratio:
        # Image is too wide, crop width
        new_width = int(height * target_ratio)
        start_x = (width - new_width) // 2
        cropped = image[:, start_x:start_x + new_width]
    else:
        # Image is too tall, crop height
        new_height = int(width / target_ratio)
        start_y = (height - new_height) // 2
        cropped = image[start_y:start_y + new_height, :]

    return cropped


async def detect_liveness(image):
    try:
        corped_image = resize_to_aspect_ratio(image, target_ratio=3 / 4)
        result = predict_liveness(corped_image)
        return result
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

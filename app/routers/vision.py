from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
from app.schemas import FaceRecognitionResponse, ProductClassifierResponse
from app.pipeline import pipeline
from app.services import cv_utils

router = APIRouter(prefix="", tags=["Computer Vision"])

@router.post("/recognize-face", response_model=FaceRecognitionResponse, summary="Recognize returning customer via face image")
async def recognize_face(
    file: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None)
):
    """
    Accepts an uploaded face image file or base64 string.
    Generates 128D facial encodings, compares against stored customer database,
    and logs customer visit with timestamp and loyalty status.
    """
    if file is not None:
        contents = await file.read()
    elif image_base64 is not None:
        img_arr = cv_utils.decode_base64_image(image_base64)
        _, buffer = cv_utils.cv2.imencode('.jpg', img_arr)
        contents = buffer.tobytes()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either an image 'file' upload or 'image_base64' string."
        )
        
    try:
        res = pipeline.recognize_face(contents)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing face recognition: {str(e)}"
        )

@router.post("/classify-product", response_model=ProductClassifierResponse, summary="Classify retail product image into categories")
async def classify_product(
    file: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None)
):
    """
    Accepts an uploaded product image file or base64 string.
    Extracts visual feature representations and predicts product category
    (clothing, shoes, electronics, bags, groceries) with confidence probabilities.
    """
    if file is not None:
        contents = await file.read()
    elif image_base64 is not None:
        img_arr = cv_utils.decode_base64_image(image_base64)
        _, buffer = cv_utils.cv2.imencode('.jpg', img_arr)
        contents = buffer.tobytes()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either an image 'file' upload or 'image_base64' string."
        )
        
    try:
        res = pipeline.classify_product(contents)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error classifying product image: {str(e)}"
        )

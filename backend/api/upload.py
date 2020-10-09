import time
import uuid

import cv2
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import APIRouter, HTTPException
import numpy as np
from PIL import Image


router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    image = np.array(Image.open(file.file))
    height, width = int(image.shape[0]), int(image.shape[1])
    new_width = int((640 / height) * width)
    resized_image = cv2.resize(image, (new_width, 640), interpolation=cv2.INTER_AREA)
    name = f"/storage/CHECK_THIS_OUT{str(uuid.uuid4())}.jpg"
    cv2.imwrite(name, resized_image)
    return {"filename": name}


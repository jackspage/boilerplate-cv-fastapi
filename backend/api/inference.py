import time
import uuid
import logging

from fastapi import File
from fastapi import UploadFile
from fastapi import APIRouter, HTTPException
from redis import Redis
from rq import Queue

# import api.inference as inference
import api.config as config
import cv2
import numpy as np
from PIL import Image

router = APIRouter()

gunicorn_error_logger = logging.getLogger("gunicorn.error")
logging.root.handlers.extend(gunicorn_error_logger.handlers)
logging.root.setLevel(gunicorn_error_logger.level)
logger = logging.getLogger(__name__)

redis_conn = Redis(host='redis', port=6379, db=0)
q = Queue('inference', connection=redis_conn)


def inference(image_uuid, style, file):
    image = np.array(Image.open(file.file))

    model_name = f"{config.MODEL_PATH}{style}.t7"
    model = cv2.dnn.readNetFromTorch(model_name)

    height, width = int(image.shape[0]), int(image.shape[1])
    new_width = int((640 / height) * width)
    resized_image = cv2.resize(image, (new_width, 640), interpolation=cv2.INTER_AREA)
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Create our blob from the image
    # Then perform a forward pass run of the network
    # The Mean values for the ImageNet training set are R=103.93, G=116.77, B=123.68

    inp_blob = cv2.dnn.blobFromImage(
        resized_image,
        1.0,
        (new_width, 640),
        (103.93, 116.77, 123.68),
        swapRB=False,
        crop=False,
    )

    model.setInput(inp_blob)
    output = model.forward()

    # Reshape the output Tensor,
    # add back the mean substruction,
    # re-order the channels
    output = output.reshape(3, output.shape[2], output.shape[3])
    output[0] += 103.93
    output[1] += 116.77
    output[2] += 123.68

    output = output.transpose(1, 2, 0)
    name = f"/storage/{image_uuid}_{style}.jpg"
    cv2.imwrite(name, output)

    return output, resized_image


@router.post("/")
async def get_image(file: UploadFile = File(...)):
    image_uuid = str(uuid.uuid4())
    models = config.STYLES.copy()
    task_ids = []

    for model in models:
        task = q.enqueue(inference, image_uuid=image_uuid, style=models[model], file=file)
        task_ids.append(task.get_id())

    return {"image_uuid": image_uuid}

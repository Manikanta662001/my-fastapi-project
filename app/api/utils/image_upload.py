from uuid import uuid4
import os

UPLOAD_DIR = "uploads"


def image_upload(image):
    file_ext = image.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    # save file
    with open(file_path, "wb") as f:
        f.write(image.file.read())
    return file_name

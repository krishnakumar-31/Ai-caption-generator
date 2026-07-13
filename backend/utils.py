import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size(filepath):
    size = os.path.getsize(filepath)
    return round(size / 1024, 2)
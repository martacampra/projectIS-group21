import os
from PIL import Image
from flaskblog import app


def save_picture(form_picture):

    fname, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = fname + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    output_size = (325, 325)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

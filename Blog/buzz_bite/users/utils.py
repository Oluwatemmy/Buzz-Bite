import os
import secrets
from PIL import Image
from flask import url_for, current_app
import yagmail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_email(user):
    token = user.get_reset_token()
    content = f''' To reset your password, Please visit the link below
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    yagmail.SMTP('temmyghold00@gmail.com', 'kldlswnfuummvgrb').send(user.email, 'Password Reset Request', content)

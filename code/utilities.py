from logger import logger
from config import configs
from werkzeug.utils import secure_filename
import os
import numpy as np
import cv2
import json

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in configs['allowed_extensions']


def validate_file(request):
    """
    check provided file by user
    :param request:
    :return file_path, if file is valid. otherwise empty str '':
    """
    full_path = ''

    data = request.data
    logger.info(data)
    encoded_data = data.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow(img)
    cv2.waitKey(0)

    if 'file' not in request.files:
        logger.error('file does not exists in request')

    try:
        logger.info('request json is {}'.format(request.json))

        #file = request.files['file']
    except Exception as e:
        logger.error('except {}'.format(e))

    if not file:
        logger.error('file is empty')

    elif file.filename == '':
        logger.error('filename is empty')

    elif not allowed_file(file.filename):
        logger.error('invalid file extension')

    else:
        filename = secure_filename(file.filename)
        full_path = os.path.join('./uploads', filename)
        file.save(full_path)
        logger.info('file {} has been saved successfully'.format(filename))

    return full_path

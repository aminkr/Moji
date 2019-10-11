from logger import logger
from config import configs
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in configs['allowed_extensions']


def validate_file(request):
    """
    check provided file by user
    :param request:
    :return file_path, if file is valid. otherwise empty str '':
    """
    full_path = ''

    if 'file' not in request.files:
        logger.error('file does not exists in request')

    file = request.files['file']

    if not file:
        logger.error('fil is empty')

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

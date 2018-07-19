from flask import url_for, request
from flask import send_from_directory
import os

app = None
upload_dir = None
filelist=None

ALLOWED_EXTENSIONS = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'rtf', 'txt',
                      'pdf', 'png', 'bmp', 'jpg']  # 允许上传的文件格式
ALLOWED_FILE_SIZE = 10 * 1024 * 1024  # 允许上传的文件大小MB
html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>文件上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''  # 创建post表单


def init(_app):
    global app
    global upload_dir
    app = _app
    # upload_dir = os.path.join(
    #     app.instance_path, 'upload'
    # )
    # if not os.path.exists(upload_dir):
    #     os.makedirs(upload_dir)
    upload_dir = r'D:\Users\蛮小白\Desktop\test\upload'


def allowed_file(filename):  # 检查文件格式是否合法
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_size(size):  # 检查文件大小是否合法
    return size <= ALLOWED_FILE_SIZE


def upload_file():  # 文件上传
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if allowed_size(len(file.read())):
                file.seek(0)
                file.save(os.path.join(upload_dir, file.filename))
                file_url = url_for('upload_file', filename=file.filename)
                return html + '<br><img src=' + file_url + '>' + '<h1>success</h1>'
            else:
                return html + '<h1>上传失败：文件大小限制为<=10M</h1>'
        else:
            return html + '<h1>上传失败：文件格式只能使用office格式及图片</h1>'
    return html


def file_list():  # 文件下载
    for parent, dirname, filenames in os.walk(upload_dir):
        filelist = filenames
    return filelist


def download_file(filename):
    return send_from_directory(upload_dir, filename, mimetype='application/octet-stream')
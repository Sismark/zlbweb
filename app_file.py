from flask import render_template, Flask, flash, redirect, url_for
from forms.login_form import LoginForm
from forms.watermark_form import WatermarkForm
from flask import send_from_directory
from werkzeug.exceptions import HTTPException, NotFound
import os

app = Flask('__name__')

app.secret_key = 'LearnFlaskTheHardWay2017'
upload_dir = os.path.join(
    app.instance_path, 'upload'
)

# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, mode=0o755)

ALLOWED_EXTENSIONS = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'rtf', 'txt',
                      'png', 'bmp', 'jpg']  # 允许上传的文件格式
ALLOWED_FILE_SIZE = 1 * 1024 * 1024  # 允许上传的文件大小


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_size(size):
    return size <= ALLOWED_FILE_SIZE


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@lfthw.com' and form.password.data == 'adminpwd':
            return redirect(url_for('watermark'))

    return render_template('signin.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def watermark():
    form = WatermarkForm()
    if form.validate_on_submit():
        f = form.image.data
        size = len(f.read())
        if allowed_file(f.filename):
            if allowed_size(size):
                f.seek(0)
                f.save(os.path.join(upload_dir, f.filename))
                flash('Upload success。')
                return redirect(url_for('watermark'))
            else:
                flash('上传失败，文件大小：<=10M')
        else:
            flash('上传失败，允许上传的文件类型：office文档、常见图片类型')
    return render_template('upload.html', form=form)


@app.route("/download/<path:filename>")
def downloader(filename):
    print("file", filename)
    dirpath = os.path.join(app.root_path, r'instance\upload')  # 下载目录，默认从工程的根目录写起
    return send_from_directory(dirpath, filename, mimetype='application/octet-stream')


if __name__ == "__main__":
    app.run()

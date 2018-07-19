from flask import Flask, request
import mail
import file

app = Flask(__name__)


@app.route('/test_mail')
def test_mail():
    email = request.args.get('email')
    return mail.test_mail(email)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    return file.upload_file()


@app.route('/file_list', methods=['GET', 'POST'])
def file_list():
    filelist=file.file_list()
    return file.download_file(filelist)


def main():
    mail.init(app)
    file.init(app)
    app.run(host='zlbweb.cn', port=443, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    main()

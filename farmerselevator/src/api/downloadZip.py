from farmerselevator import application
import pathlib
import io
import zipfile

from flask import send_file

@application.route('/download-zipi+cqK+JpM4g=')
def request_zip():
    base_path = pathlib.Path('./farmerselevator/uploads')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='data.zip'
    )
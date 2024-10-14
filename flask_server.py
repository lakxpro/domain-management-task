from flask import Flask, jsonify, send_file, abort
from datetime import datetime
import mimetypes
import os

app = Flask(__name__)

def get_file_metadata(file_name):
    file_path = f"mock_files/{file_name}"
    
    creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
    
    file_size = os.path.getsize(file_path)
    
    mime_type, _ = mimetypes.guess_type(file_path)
    
    return {
        "create_datetime": creation_time,
        "size": file_size,
        "mimetype": mime_type or "application/octet-stream",
        "name": file_name
    }

files_metadata = {
    "123e4567-e89b-12d3-a456-426614174000": get_file_metadata("example.txt"),
    "123e4567-e89b-12d3-a456-426614174001": get_file_metadata("example2.txt")
}

FILES_DIR = './mock_files'

@app.route('/file/<uuid:file_uuid>/stat/', methods=['GET'])
def file_stat(file_uuid):
    file_uuid_str = str(file_uuid)
    if file_uuid_str in files_metadata:
        return jsonify(files_metadata[file_uuid_str])
    else:
        return abort(404, description="File not found")

@app.route('/file/<uuid:file_uuid>/read/', methods=['GET'])
def file_read(file_uuid):
    file_uuid_str = str(file_uuid)
    if file_uuid_str in files_metadata:
        file_path = os.path.join(FILES_DIR, files_metadata[file_uuid_str]['name'])
        if os.path.exists(file_path):
            return send_file(file_path, mimetype=files_metadata[file_uuid_str]['mimetype'])
        else:
            return abort(404, description="File content not found")
    else:
        return abort(404, description="File not found")

if __name__ == '__main__':
    app.run(debug=True)

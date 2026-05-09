import json
import urllib.request
import urllib.error
from PySide6.QtCore import QThread, Signal

BASE_URL = "https://api.pahrul.my.id/api/posts"

class FetchPostsWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def run(self):
        try:
            req = urllib.request.Request(BASE_URL, headers={"Accept": "application/json"})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            if data.get('success'):
                self.finished.emit(data.get('data', []))
            else:
                self.error.emit(data.get('message', 'Unknown error'))
        except Exception as e:
            self.error.emit(f"Connection Error: {str(e)}")

class FetchPostDetailWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, post_id):
        super().__init__()
        self.post_id = post_id

    def run(self):
        try:
            url = f"{BASE_URL}/{self.post_id}"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            if data.get('success'):
                self.finished.emit(data.get('data', {}))
            else:
                self.error.emit(data.get('message', 'Unknown error'))
        except Exception as e:
            self.error.emit(f"Connection Error: {str(e)}")

class CreatePostWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    validation_error = Signal(dict)

    def __init__(self, post_data):
        super().__init__()
        self.post_data = post_data

    def run(self):
        try:
            data_bytes = json.dumps(self.post_data).encode('utf-8')
            req = urllib.request.Request(
                BASE_URL, 
                data=data_bytes, 
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method='POST'
            )
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            self.finished.emit(data.get('data', {}))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            try:
                err_data = json.loads(body)
                if e.code == 422:
                    self.validation_error.emit(err_data.get('errors', {}))
                else:
                    self.error.emit(err_data.get('message', str(e)))
            except:
                self.error.emit(f"HTTP Error {e.code}: {str(e)}")
        except Exception as e:
            self.error.emit(f"Connection Error: {str(e)}")

class UpdatePostWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)
    validation_error = Signal(dict)

    def __init__(self, post_id, post_data):
        super().__init__()
        self.post_id = post_id
        self.post_data = post_data

    def run(self):
        try:
            data_bytes = json.dumps(self.post_data).encode('utf-8')
            req = urllib.request.Request(
                f"{BASE_URL}/{self.post_id}", 
                data=data_bytes, 
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method='PUT'
            )
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            self.finished.emit(data.get('data', {}))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            try:
                err_data = json.loads(body)
                if e.code == 422:
                    self.validation_error.emit(err_data.get('errors', {}))
                else:
                    self.error.emit(err_data.get('message', str(e)))
            except:
                self.error.emit(f"HTTP Error {e.code}: {str(e)}")
        except Exception as e:
            self.error.emit(f"Connection Error: {str(e)}")

class DeletePostWorker(QThread):
    finished = Signal(bool)
    error = Signal(str)

    def __init__(self, post_id):
        super().__init__()
        self.post_id = post_id

    def run(self):
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/{self.post_id}", 
                headers={"Accept": "application/json"},
                method='DELETE'
            )
            response = urllib.request.urlopen(req, timeout=10)
            self.finished.emit(True)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            try:
                err_data = json.loads(body)
                self.error.emit(err_data.get('message', str(e)))
            except:
                self.error.emit(f"HTTP Error {e.code}: {str(e)}")
        except Exception as e:
            self.error.emit(f"Connection Error: {str(e)}")

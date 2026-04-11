import falcon

def send_response(resp, status_code, message, data=None):
    resp.status = status_code
    resp.media = {
        "status": "success" if status_code == falcon.HTTP_200 else "error",
        "message": message,
        "data": data
    }
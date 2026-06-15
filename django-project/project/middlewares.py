from datetime import datetime
from pathlib import Path

from django.utils.deprecation import MiddlewareMixin


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        base_dir = Path(__file__).resolve().parent
        log_dir = base_dir / 'Log' / "usersActivity.log"
        request_user = request.user
        request_url = request.get_full_path()
        log_string = f"REQUEST | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {request_user} | URL={request_url} | {request.method} \n"
        with log_dir.open(mode='a', encoding='utf-8') as log:
            log.write(log_string)
        response = self.get_response(request)
        log_string = f"RESPONSE | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {request_user} | URL={request_url} | {response.status_code} \n"
        with log_dir.open(mode='a', encoding='utf-8') as log:
            log.write(log_string)
        return response

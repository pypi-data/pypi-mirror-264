import json
import logging
import requests
from telegraph import Telegraph
from django.conf import settings
logger = logging.getLogger('request')

class TelegramBotHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.send_telegram_message(log_entry)

    def send_telegram_message(self, message):
        telegraph = Telegraph(settings.TELEGRAPH_TOKEN)

        txt = message
        if message is not None:
            text = message.split("@ ")
            head = text[0]
            if len(text) == 2:
                body = text[1] 
                print(body)
                try:
                    if body.strip():
                        wtf = json.loads(body)
                        titles = (head.replace('*','')).replace('`','').split('\n')
                        response = telegraph.create_page(
                            titles[0],
                            html_content=f"<h4>{titles[2]}</h4><pre>{body}</pre>"
                        )
                        uri = 'https://telegra.ph/{}'.format(response['path'])
                        txt = f"{head}*{wtf['method']}* `{wtf['path']}` *{wtf['error_code']}* - _{wtf['error_message']}_\n*IP:* `{wtf['client_ip']}`\n\n[👁 Show logs]({uri})"
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                except Exception as e:
                    print(f"other exception: {e}")

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {"chat_id": self.chat_id, "text": txt, 'parse_mode': 'markdown', 'disable_web_page_preview': 'true'}
        try:
            requests.post(url, json=params)
        except Exception as e:
            print(f"TG send error: {e}")
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            params = {"chat_id": self.chat_id, "text": e, 'parse_mode': 'markdown', 'disable_web_page_preview': 'true'}
            requests.post(url, json=params)


class requestHandleMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            if request.method == "GET":
                body = {}
            try:
                body = request.body.decode('utf-8')
                print(f"body on request: {body}")
            except Exception as e:
                print(f"Exception body: {e}")
                logger.error(e)
            try:
                if body.strip():
                    body = dict(json.loads(body.replace('\r\n', '')))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                logger.error(e)
            except Exception as e:
                print(f"other exception: {e}")
                logger.error(e)
            error_message = response.reason_phrase if response.reason_phrase else "Unknown Error"
            error_txt = {
                "path": request.get_full_path(),
                "method": request.method,
                "error_code": response.status_code,
                "error_message": error_message,
                "client_ip": request.headers.get('X-Forwarded-For', request.META.get('REMOTE_ADDR')),
                "client": {
                    "headers": dict(request.headers),
                    "body": body
                }
            }
            logger.error(json.dumps(error_txt, indent=2))

        return response
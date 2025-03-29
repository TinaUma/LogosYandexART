import requests
import random
import time
import base64
import os
import json
import config as cfg

def generate_logo(forma, style, description):
    iam_token = get_iam_token()
    if not iam_token:
        print("IAM-токен не получен")
        return None

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "x-folder-id": cfg.catalog_id,
    }
    data = {
        "modelUri": f"art://{cfg.catalog_id}/yandex-art/latest",
        "generationOptions": {
            "seed": str(random.randint(0, 1000000)),
            "aspectRatio": {"widthRatio": "1", "heightRatio": "1"},
        },
        "messages": [
            {"weight": "1", "text": f"Нарисуй логотип в форме {forma} под описание: {description}, в стиле: {style}"}
        ],
    }

    try:
        print(f"Отправляем запрос с токеном: {iam_token[:10]}...")
        response = requests.post(cfg.url_1, headers=headers, json=data)
        if response.status_code == 401:
            print("Токен устарел, обновляем...")
            iam_token = update_iam_token()
            if not iam_token:
                return None
            headers["Authorization"] = f"Bearer {iam_token}"
            response = requests.post(cfg.url_1, headers=headers, json=data)
        response.raise_for_status()
        request_id = response.json().get("id")
        if not request_id:
            print("Не получен request_id")
            return None

        print(f"Ждём генерацию, request_id: {request_id}")
        time.sleep(20)
        result_url = f"{cfg.url_2}/{request_id}"
        result_response = requests.get(result_url, headers=headers)
        result_response.raise_for_status()

        image_base64 = result_response.json()["response"]["image"]
        image_data = base64.b64decode(image_base64)
        image_path = os.path.join("static", "generated_logo.jpeg")
        with open(image_path, "wb") as f:
            f.write(image_data)
        print(f"Логотип сохранён: {image_path}")
        return image_path
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        return None

def get_iam_token():
    try:
        with open("generated/iam_token.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Токен из файла: {data['iam_token'][:10]}...")
            return data["iam_token"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Файл не найден или повреждён: {e}")
        return update_iam_token()

def update_iam_token():
    OAUTH_TOKEN = "YOUR_OAUTH_TOKEN"  # Замените на ваш OAuth-токен
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {"Content-Type": "application/json"}
    data = {"yandexPassportOauthToken": OAUTH_TOKEN}
    try:
        print("Обновляем IAM-токен...")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        iam_token = response.json().get("iamToken")
        with open("generated/iam_token.json", "w", encoding="utf-8") as f:
            json.dump({"iam_token": iam_token}, f, ensure_ascii=False, indent=4)
        print(f"Новый IAM-токен получен: {iam_token[:10]}...")
        return iam_token
    except Exception as e:
        print(f"Ошибка обновления IAM-токена: {e}")
        return None
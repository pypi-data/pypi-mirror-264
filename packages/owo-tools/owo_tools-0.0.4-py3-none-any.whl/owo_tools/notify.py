import requests


def send_line_notify(token: str, message: str = "Hello World"):
    """
    使用 Line Notify 服務傳送訊息的函數

    參數：
    token (str): 存取權杖（Access Token），從 Line Notify 的官方網站申請取得
    message (str): 欲傳送的訊息內容

    回傳：
    dict: Line Notify API 回應的 JSON 資料

    範例：
    response = send_line_notify("aaaa", "Hello World")
    print(response)
    """
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    payload = {
        'message': message
    }
    r = requests.post(url, headers=headers, params=payload)
    return r.json()

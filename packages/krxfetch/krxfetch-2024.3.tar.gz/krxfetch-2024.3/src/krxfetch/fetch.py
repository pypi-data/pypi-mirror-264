import requests


def get_json_data(payload: dict) -> list[dict]:
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    r = requests.post(url=url, data=payload)
    json = r.json()

    keys = list(json)
    k = keys[1] if keys[0] == 'CURRENT_DATETIME' else keys[0]

    if k != 'output' and k != 'OutBlock_1' and k != 'block1':
        raise NotImplementedError(k)

    return json[k]


def download_csv(payload: dict) -> str:
    # 1. Generate OTP
    otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'

    r = requests.post(url=otp_url, data=payload)
    otp = {
        'code': r.text
    }

    # 2. Download CSV
    url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'

    r = requests.post(url=url, data=otp)
    csv = r.content.decode(encoding='euc_kr')

    return csv

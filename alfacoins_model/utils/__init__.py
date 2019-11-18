from hashlib import md5
from alfacoins_model.alfacoin import AlfaCoinsProvider
from requests import post

# self._encoded_password = md5(raw_password.encode('utf-8')) \
#             .hexdigest() \
#             .upper()


def create_hash_data(**kwargs):
    coins_provider_instance = AlfaCoinsProvider.coinsprovider()
    password = coins_provider_instance.password
    name = coins_provider_instance.name
    params = f"{name}:{kwargs.get('coin_received_amount')}" \
        f":{kwargs.get('received_amount')}:{kwargs.get('currency')}:{kwargs.get('id')}" \
        f":{kwargs.get('order_id')}:{kwargs.get('status')}:{kwargs.get('modified')}:{password}"
    return md5(params.encode('utf-8')).hexdigest().upper()


def generate_qr_code_url(data, **kwargs):
    # https://developers.google.com/chart/infographics/docs/qr_codes
    """
       :param data Required less than 2k
       :param kwargs:
           cht   Required Specifies a QR code.
           chs   Required <width>x<height> Image size.
           choe  Optionally <output_encoding> How to encode the data in the QR code.
                 UTF-8 [Default]
           chld  Optionally <error_correction_level>|<margin>
                 L - [Default] Allows recovery of up to 7% data loss
                 M - Allows recovery of up to 15% data loss
                 Q - Allows recovery of up to 25% data loss
                 H - Allows recovery of up to 30% data loss
                 margin: default value is 4.
       :return: `QR code url`
       """
    params = dict(cht='qr', chs='150x150', choe='UTF-8', chld='L|1',)
    params.update(**kwargs)
    base_url = "https://chart.googleapis.com/chart?"
    url = f"cht={params.get('cht')}&chl={data}&choe={params.get('choe')}&" \
        f"chs={params.get('chs')}&chld={params.get('chld')}"
    return f"{base_url}{url}"


def request_handle(url: str, params: dict = dict(), json_data: dict = dict()):
    response = post(
        url=url,
        data=params,
        json=json_data
    )
    return response.content.decode('utf-8')


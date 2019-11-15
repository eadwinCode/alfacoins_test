from hashlib import md5
# self._encoded_password = md5(raw_password.encode('utf-8')) \
#             .hexdigest() \
#             .upper()


def CoinsProviderInstance():
    from .alfacoin import CoinsProviderInstance
    return CoinsProviderInstance

def create_hash_data(**kwargs):
    password = CoinsProviderInstance.password
    name = CoinsProviderInstance.name
    params = dict(name=name, password=password)
    params.update(**kwargs)
    return md5(params).hexdigest().upper()
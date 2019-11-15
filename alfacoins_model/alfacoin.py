from alfacoins_api_python import ALFACoins
from django.conf import settings, ImproperlyConfigured


class AlfaCoinsProvider:

    def __init__(self):
        if not getattr(settings, 'ALFACOINS_SECRET_KEY', None) or \
                not getattr(settings, 'ALFACOINS_BUSINESS_NAME', None) or \
                not getattr(settings, 'ALFACOINS_PASSWORD', None):
            raise ImproperlyConfigured('ALFACOINS_SECRET_KEY, ALFACOINS_BUSINESS_NAME '
                                       'and ALFACOINS_PASSWORD are required!')

        self._secret_key = getattr(settings, 'ALFACOINS_SECRET_KEY')
        self._name = getattr(settings, 'ALFACOINS_BUSINESS_NAME')
        self._password = getattr(settings, 'ALFACOINS_PASSWORD')
        self._notification_url = getattr(settings, 'ALFACOINS_NOTIFICATION_URL', None)
        self._redirect_url = getattr(settings, 'ALFACOINS_REDIRECT_URL', None)

    def get_instance(self):
        alfacoins_instance = ALFACoins(name=self._name, secret_key=self._secret_key, password=self._password)
        return alfacoins_instance


CoinsProvider = AlfaCoinsProvider()
CoinsProviderInstance = CoinsProvider.get_instance()

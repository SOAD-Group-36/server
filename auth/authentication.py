from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from delivery.models import LogisticServices
from sellers.models import Seller


class ApiKeyAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = None
    related_name = None
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 1:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError as unicode_err:
            msg = 'Invalid token header. Token string should not contain invalidcharacters.'
            raise AuthenticationFailed(msg) from unicode_err

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """
        Authenticate the api key for the User
        """
        model = self.model
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist as no_model:
            raise AuthenticationFailed('Invalid token.') from no_model

        if not token.business and not hasattr(token.business, self.related_name):
            raise AuthenticationFailed('User inactive or deleted.')

        return (getattr(token.business, self.related_name), token)

    def authenticate_header(self, request):
        return self.keyword


class LogisticServicesAuthentication(ApiKeyAuthentication):
    keyword = 'Delivery'
    related_name = 'logistic_services'
    model = LogisticServices


class SellerServicesAuthentication(ApiKeyAuthentication):
    keyword = 'Seller'
    related_name = 'seller'
    model = Seller

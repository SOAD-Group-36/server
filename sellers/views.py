from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from sellers.serializers import SellerSerializer


class SellerCreateView(APIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    @swagger_auto_schema(request_body=SellerSerializer)
    def post(self, request):
        print(request.data)
        return Response({"hi": [10, 19.3]})

from rest_framework.generics import CreateAPIView
from .serializers import BlasterIOSerializer
from .models import blaster
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class BlasterIOApiView(CreateAPIView):
    serializer_class = BlasterIOSerializer
    queryset = blaster.objects.all()

    def dispatch(self, request, *args, **kwargs):
        request1 = self.initialize_request(self.request, *args, **kwargs)
        print("1:", request1.data)
        return super().dispatch(request, *args, **kwargs)
    # def initial(self, request, *args, **kwargs):
    #     print(request.user)

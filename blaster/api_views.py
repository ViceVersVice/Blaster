from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .serializers import BlasterIOSerializer
from .models import blaster
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class BlasterIOApiView(CreateAPIView):
    serializer_class = BlasterIOSerializer
    queryset = blaster.objects.all()
    #permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        complemented_data = serializer.data
        for key in serializer.validated_data.keys():
            """Adding non model field validated data to response (like in Django model forms)"""
            if key not in complemented_data.keys():
                complemented_data[key] = serializer.validated_data[key]
        return Response(complemented_data, status=status.HTTP_201_CREATED, headers=headers)

    def dispatch(self, request, *args, **kwargs):
        request1 = self.initialize_request(self.request, *args, **kwargs)
        #print("ALL:", vars(request1))
        print("Session:", request1.session)
        #print("META:", request1.META)
        print("USER:", request1.user.is_authenticated)
        print("AUTH:", request1.auth)
        #print("AUTH:", request1.authenticators)
        return super().dispatch(request, *args, **kwargs)
    # def initial(self, request, *args, **kwargs):
    #     print(request.user)

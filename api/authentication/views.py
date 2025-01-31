from rest_framework import generics
from .serializers import RegisterCompanySerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterCompanyView(generics.CreateAPIView):
    serializer_class = RegisterCompanySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Company registered successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

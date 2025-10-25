from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsProfessor, IsStudent

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})
    return Response(serializer.errors, status=400)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add role and username in token payload
        token['role'] = user.role
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#All this views are here for test purpose of auth system. please import the permissions in the required app and use them there.
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_dashboard(request):
    return Response({"message": "Welcome Admin!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsProfessor])
def professor_dashboard(request):
    return Response({"message": "Welcome Professor!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def student_dashboard(request):
    return Response({"message": "Welcome Student!"})
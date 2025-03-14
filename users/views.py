from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import status
from .models import User  
from rest_framework import status
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=401)

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.role  # Ensure role is sent in response
    })

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not username or not email or not password or not role:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure everything succeeds or nothing is saved
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password, role=role)
                
                # Additional profile creation (if applicable)
                # UserProfile.objects.create(user=user, role=role)  # Uncomment if using profiles

                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Registration failed. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    # serializer_class = UserRegisterSerializer
    # permission_classes = [AllowAny]

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_profile(request):
    # user = request.user
    # serializer = UserSerializer(user)
    # return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "role": user.role  # Ensure role is included
    })

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

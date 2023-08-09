from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import *
from account.send_email import send_confirmation_email
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, generics, status
from account.serializers import RegisterSerializer, \
    ActivationSerializer, UserSerializer, RegisterPhoneSerializer, ChangePasswordSerializer, ProfileSerializer

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_confirmation_email(user.email, user.activation_code)
        if user:
            print(user, '!!!!')
            try:
                send_confirmation_email(user.email,
                                       user.activation_code)
            except:
                return Response({'message':'Зарегистрировался но на почту код не отправился',
                                'data': serializer.data},status=201)
        return Response(serializer.data, status=201)

class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Успешно активирован', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class RegistrationPhoneView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterPhoneSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('good', status=201)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('pk')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        if self.action in ['retrieve_profile', 'update_profile', 'change_password']:
            return self.request.user
        return super().get_object()

    @action(
        methods=['get'],
        detail=False,
        url_path='profile',
        serializer_class=ProfileSerializer,
        permission_classes=[IsAuthenticated]
    )
    def retrieve_profile(self, request):
        return super().retrieve(request)

    @action(
        methods=['put'],
        detail=False,
        url_path='change-password',
        serializer_class=ChangePasswordSerializer,
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request):
        return super().update(request)

    @retrieve_profile.mapping.put
    def update_profile(self, request):
        return super().update(request)


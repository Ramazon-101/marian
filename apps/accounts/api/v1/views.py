from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.accounts.api.v1.permissions import IsOwnUserOrReadOnly
from apps.accounts.api.v1.serializers import RegisterSerializer, LoginSerializer, AccountUpdateSerializer, \
    AccountOwnImageUpdateSerializer, SetNewPasswordSerializer
from apps.accounts.models import Account


class AccountRegisterView(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/register/
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data=user)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        user_data = serializers.data
        username = serializers.data.get('username')
        tokens = Account.objects.get(username=username).tokens
        user_data['tokens'] = tokens
        return Response({'success': True, 'data': user_data}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)


class AccountView(generics.RetrieveUpdateAPIView):
    # http//127.0.0.1:8000/api/accounts/v1/get-account/
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated,)
    serializer_class = AccountUpdateSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        query = Account.objects.get(id=user.id)
        serializers = self.get_serializer(query)
        return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)


class AccountRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/retrieve-update/<id>/
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializers = self.get_serializer(query)
            return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'success': False, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)


class AccountOwnImageUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/accounts/v1/image-retrieve-update//<id>/
    serializer_class = AccountOwnImageUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.get_serializer(query)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'query does not match'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class AccountListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/list/
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')

        q_condition = Q()
        if q:
            q_condition = Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(username__icontains=q) or Q(
                email__icontains=q)

        return q

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            count = queryset.count()
            return Response({'success': True, 'count': count, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'data': 'queryset does not matching'}, status=status.HTTP_404_NOT_FOUND)


class SetNewPasswordView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/api/account/v1/set-password/
    serializer_class = SetNewPasswordSerializer
    permission_classes = (IsOwnUserOrReadOnly, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'message': 'Successfully changed password'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_400_BAD_REQUEST)

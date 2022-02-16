from rest_framework import viewsets, status
from rest_framework.response import Response
from account.models import Account
from account.apis.serializers import CreateUserSerializer
from django.conf import settings
from ev.auth import FirebaseAuthentication
from django.contrib.auth import get_user_model
import firebase_admin.auth as auth


def get_firebase_user_id(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["user_id"]
        print("uid is ", uid)
        return uid
    except Exception as e:
        return None


class UserViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateUserSerializer

    def list(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication is required"}, status=status.HTTP_403_FORBIDDEN)
        firebase_uid = get_firebase_user_id(token)
        if not firebase_uid:
            return Response({"detail": "Invalid Authentication Token"}, status=status.HTTP_403_FORBIDDEN)
        User = get_user_model()
        try:
            user = User.objects.get(firebase_uid=firebase_uid)
            return Response({"status": True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication is required"}, status=status.HTTP_403_FORBIDDEN)
        firebase_uid = get_firebase_user_id(token)
        if not firebase_uid:
            return Response({"detail": "Invalid Authentication Token"}, status=status.HTTP_403_FORBIDDEN)
        full_name = request.data.pop("full_name", None)
        if not full_name:
            return Response({"detail": "full_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data["firebase_uid"] = firebase_uid
        data["first_name"] = full_name.split(" ")[0]
        data["last_name"] = full_name.split(data["first_name"])[1]
        print("data is ", data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=(True)):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

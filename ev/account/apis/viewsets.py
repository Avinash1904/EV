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
        phone_number = request.GET.get("phone_number", None)
        if not phone_number:
            return Response({"detail": "phone_number is required"}, status=status.HTTP_400_BAD_REQUEST)
        User = get_user_model()
        try:
            User.objects.get(phone_number=phone_number)
            return Response({"status": True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"status": False, "detail": "You need to register to proceed", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "detail": "You need to register to proceed", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        op = {}
        op["status"] = False
        op["data"] = {}
        token = request.headers.get('Authorization')
        if not token:
            op["detail"] = "Authentication Token is required"
            return Response(op, status=status.HTTP_403_FORBIDDEN)
        bearer = token.split("Bearer ")
        try:
            token = bearer[1]
        except Exception as e:
            op["detail"] = "Authentication Token is required"
            return Response(op, status=status.HTTP_403_FORBIDDEN)
        firebase_uid = get_firebase_user_id(token)
        if not firebase_uid:
            op["detail"] = "Invalid Authentication Token"
            return Response(op, status=status.HTTP_403_FORBIDDEN)
        full_name = request.data.pop("full_name", None)
        if not full_name:
            op["detail"] = "full_name is required"
            return Response(op, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data["firebase_uid"] = firebase_uid
        data["first_name"] = full_name.split(" ")[0]
        data["last_name"] = full_name.split(data["first_name"])[1]
        print("data is ", data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            op["status"] = True
            op["detail"] = "Profile created"
            op["data"] = serializer.data
        else:
            op["status"] = True
            op["detail"] = serializer.errors
            op["data"] = {}
        return Response(op, status=status.HTTP_201_CREATED)

from rest_framework import viewsets, status
from rest_framework.response import Response
from account.models import Account
from account.apis.serializers import CreateUserSerializer
from django.conf import settings
from ev.auth import FirebaseAuthentication
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

    def create(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication is required"}, status=status.HTTP_403_FORBIDDEN)
        firebase_uid = get_firebase_user_id(token)
        if not firebase_uid:
            return Response({"detail": "Invalid Authentication Token"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data["firebase_uid"] = firebase_uid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=(True)):
            serializer.save()
            # custom claim for user
            auth.set_custom_user_claims(firebase_uid, {'registered': True})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

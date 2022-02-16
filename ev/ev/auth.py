from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
import firebase_admin as admin
import firebase_admin.auth as auth
from account.models import Account


def create_user_firebase(email, password):
    user = auth.create_user(email=email, password=password)
    return user


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("checking auth .. ")

        token = request.headers.get('Authorization', None)
        if not token:
            return None

        try:
            bearer = token.split("Bearer ")
            try:
                token = bearer[1]
            except Exception as e:
                return None
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["user_id"]
            print("uid is ", uid)
        except Exception as e:
            return None

        try:
            print("getting user")
            User = get_user_model()
            user = User.objects.get(firebase_uid=uid)
            print("user is ", user)
            return (user, None)

        except Exception as e:
            return None

from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
import firebase_admin as admin
import firebase_admin.auth as auth
from account.models import Account
from django.db.models.functions import Concat
from django.db.models import Value


def create_user_firebase(email, password):
    user = auth.create_user(email=email, password=password)
    return user


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("checking auth .. ")
        User = get_user_model()

        token = request.headers.get('Authorization', None)
        #print("token is -- ", token)
        if not token:
            return None

        try:
            bearer = token.split("Bearer ")
            try:
                token = bearer[1]
            except Exception as e:
                return None
            decoded_token = auth.verify_id_token(token)
            print("decoded token ", decoded_token)
            uid = decoded_token.get("user_id", None)
            phone_number = decoded_token.get("phone_number", None)
            email = decoded_token.get("email", None)
            print("uid is ", uid)
        except Exception as e:
            return None

        try:
            user = User.objects.get(firebase_uid=uid)
            print("user is ", user)
            return (user, None)

        except User.DoesNotExist:
            # check if the phone number or email exists in our record
            if phone_number:
                try:
                    qs = User.objects.annotate(
                        search_phone_number=Concat(
                            'country_code', Value(''), 'phone_number')
                    )
                    user = qs.get(search_phone_number=phone_number)
                    return (user, None)
                except User.DoesNotExist:
                    pass
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return (user, None)
            return None

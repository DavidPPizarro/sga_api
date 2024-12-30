from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework import generics
from . serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@login_required
def google_login_callback(request):
    user = request.user

    social_account = SocialAccount.objects.filter(user=user)
    print(f"Social Account: {social_account}")

    social_account = social_account.first()

    if not social_account:
        print(f"No social account found for user: {user}")
        return redirect("http://localhost:3000/login/callback/?error=NoSocialAccount")

    token = SocialToken.objects.filter(
        account=social_account, account__provider='google').first()

    if token:
        print(f"Google Token found: {token}")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return redirect(f"http://localhost:3000/login/callback/?access_token={access_token}")
    else:
        print(f"No Google Token found for user: {user}")
        return redirect("http://localhost:3000/login/callback/?error=NoGoogleToken")


@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gooogle_access_token = data.get('access_token')
            print(f"Google Access Token: {gooogle_access_token}")

            if not gooogle_access_token:
                return JsonResponse({'detail': 'Access token is missing'}, status=400)
            return JsonResponse({'detail': 'Token is valid'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

import hashlib

from django.http import JsonResponse
from coreapi.compat import force_text
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import EmailMessage
from rest_framework import status
from twilio.rest import Client

from .forms import RegistrationForm
from .models import *
from .tokens import *

account_sid = ""
auth_token = ""
verify_sid = ""


@api_view(['POST'])
def register_user(request):

    user = request.user
    if user.is_authenticated:
        return JsonResponse({'Message': "You are already authenticated."}, status=status.HTTP_400_BAD_REQUEST)

    form = RegistrationForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

    else:
        return JsonResponse({'msg': form.errors.values()}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'msg': "User Registration Successful."}, status=status.HTTP_201_CREATED)


@api_view(["get"])
def generate_email_verification(request):
    user = UserProfile.objects.get(pk=request.user.pk)
    try:
        mail_subject = 'Forum Account activation link.'
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': "http://127.0.0.1:1234",
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.POST["email"]
        email = EmailMessage(
            mail_subject,
            message,
            to=[to_email]
        )
        email.send()
    except Exception:
        return JsonResponse({"response": "Verification email generation failed"}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"response": "Verification email sent"}, status=status.HTTP_200_OK)

@api_view(["get"])
def email_verification(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'msg': "Email verified."}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': "Email verification failed."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["post"])
def generate_mobile_otp(request):
    client = Client(account_sid, auth_token)
    phone_number = request.POST["phone"]

    try:
        verification = client.verify.v2.services(verify_sid).verifications.create(to=phone_number, channel="sms")
    except Exception as e:
        return JsonResponse({"response": "failed to send otp"}, status=status.HTTP_408_REQUEST_TIMEOUT)

    return JsonResponse({"response": "otp sent successfully"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def mobile_verification(request):
    client = Client(account_sid, auth_token)
    otp_code = request.POST["otp"]
    phone_number = request.POST["phone"]

    try:
        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=phone_number,
            code=otp_code
        )
        print("verification_check ", verification_check.status)
    except Exception as e:
        return JsonResponse({"response": "mobile verification failed"}, status=status.HTTP_401_UNAUTHORIZED)

    return JsonResponse({"response": "mobile verified"}, status=200)



def generate_ssh_key(request):



    return JsonResponse({"response": "ssh_key"}, status=200)


def validate_totp(request):
    otp = request.POST["otp"]




    return JsonResponse({"response": "totp_verified"}, status=200)



@api_view(["POST"])
def generate_sha1_key(request):
    key_string = "TOTPGENERATOR"
    sha_key = hashlib.sha1(key_string.encode()).hexdigest()
    return JsonResponse({"response": sha_key}, status=200)


@api_view(["POST"])
def generate_sha256_key(request):
    key_string = "TOTPGENERATOR"
    sha_key = hashlib.sha256(key_string.encode()).hexdigest()
    return JsonResponse({"response": sha_key}, status=200)


@api_view(["POST"])
def generate_sha512_key(request):
    key_string = "TOTPGENERATOR"
    sha_key = hashlib.sha512(key_string.encode()).hexdigest()
    return JsonResponse({"response": sha_key}, status=200)

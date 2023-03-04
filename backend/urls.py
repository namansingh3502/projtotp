from django.urls import path

from . import views

urlpatterns = [
    path('user_regisration/', views.register_user, name="User_Registration"),
    path('generate_email_verification/', views.generate_email_verification, name="Email_Verification"),
    path('verify_email/<uidb64>/<token>/', views.email_verification, name="Mobile_Verification"),
    path('generate_mobile_verification_otp/', views.generate_mobile_otp, name="Mobile_Verification"),
    path('user_mobile_verification/', views.mobile_verification, name="Mobile_Verification"),
    path('SHA1_key/', views.generate_sha1_key, name="Generate_SHA1_Key"),
    path('SHA256_key/', views.generate_sha256_key, name="Generate_SHA256_Key"),
    path('SHA512_key/', views.generate_sha512_key, name="Generate_SHA512_Key"),
    path('validate/', views.validate_totp, name="Validate_TOTP")
]

from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner, SignatureExpired
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from app_user.handlers import OtpHandler
from app_user.models import AppUser, TempUser
from app_user.validator import Validators


# --------------------------------@mit-------------------------------------
# View for user register
@csrf_exempt
@api_view(['POST'])
def register(request):
    try:
        # Extracting the user data from the request
        user_data = request.data

        # Checking if user data is present or not
        if not user_data:
            no_user_data_res = {
                'status': "failed",
                'message': "Please provide all the details",
            }
            return Response(no_user_data_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if first name is present or not
        if 'first_name' not in user_data:
            no_first_name_res = {
                'status': "failed",
                'message': "Please provide your first name!",
            }
            return Response(no_first_name_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if username is present or not
        if 'username' not in user_data:
            no_username_res = {
                'status': "failed",
                'message': "Please provide your username!",
            }
            return Response(no_username_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if email is present or not
        if 'email' not in user_data:
            no_email_res = {
                'status': "failed",
                'message': "Please provide your email!",
            }
            return Response(no_email_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if email is valid or not
        if not Validators.validate_email(user_data['email']):
            invalid_email_res = {
                'status': "failed",
                'message': "Please provide valid email!",
            }
            return Response(invalid_email_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if password is present or not
        if 'password' not in user_data:
            no_password_res = {
                'status': "failed",
                'message': "Please provide password!",
            }
            return Response(no_password_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if password is valid or not
        if not Validators.validate_password(user_data['password']):
            invalid_password_res = {
                'status': "failed",
                'message': "Password is too short!",
            }
            return Response(invalid_password_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if gender is present or not
        if 'gender' not in user_data:
            no_gender_res = {
                'status': "failed",
                'message': "Please provide your gender!",
            }
            return Response(no_gender_res, status=status.HTTP_400_BAD_REQUEST)

        # If everything is present
        first_name = user_data['first_name']
        last_name = user_data['last_name'] if 'last_name' in user_data else ''
        username = user_data['username']
        email = user_data['email']
        gender = user_data['gender']
        password = user_data['password']
        c_password = user_data['c_password'] if 'c_password' in user_data else ''

        # If password and confirmation password is not equal
        if password != c_password:
            not_match_res = {
                'status': "failed",
                'message': "Password doesn't match!",
            }
            return Response(not_match_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if user already exists
        if User.objects.filter(username=username).exists():
            user_exists_res = {
                'status': "failed",
                'message': "User already exists with this username!",
            }
            return Response(user_exists_res, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            user_exists_res = {
                'status': "failed",
                'message': "User already exists with this email!",
            }
            return Response(user_exists_res, status=status.HTTP_400_BAD_REQUEST)

        # Extra data to pass to the user object to create new user
        extra = {
            'first_name': first_name,
            'last_name': last_name,
            'is_active': False
        }
        # Creating new user
        user = User.objects.create_user(username=username, email=email, password=password, **extra)

        if user:
            # Creating new app user
            app_user = AppUser.objects.create(gender=gender, user=user)

            # Sending otp to the user
            OtpHandler.generate_n_send_otp(to=user)

            # Creating res
            res = {
                'status': 'success',
                'message': 'User registered successfully!, Please check your email for OTP',
            }
            return Response(res, status=status.HTTP_201_CREATED)

        # If something went wrong
        user.delete()
        res = {
            'status': 'failed',
            'message': "Something went wrong!"
        }
        return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        error_res = {
            'status': 'error',
            'message': e.__str__(),
        }
        return Response(error_res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------------------@mit-------------------------------------
# View for otp verification
@csrf_exempt
@api_view(['POST'])
def otp_verify(request):
    try:
        # Extracting the otp data
        otp_data = request.data

        # Checking if otp data is present or not
        if not otp_data:
            no_otp_data_res = {
                'status': "failed",
                'message': "Please provide otp details",
            }
            return Response(no_otp_data_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if otp is present or not
        if 'otp' not in otp_data:
            no_otp_res = {
                'status': "failed",
                'message': "Please provide otp!",
            }
            return Response(no_otp_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if otp is valid or not
        if not Validators.validate_otp(otp_data['otp']):
            invalid_otp_res = {
                'status': "failed",
                'message': "Please provide valid otp!",
            }
            return Response(invalid_otp_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if username or email is present or not
        if 'username' not in otp_data and 'email' not in otp_data:
            no_username_or_email_res = {
                'status': "failed",
                'message': "Please provide username or email!",
            }
            return Response(no_username_or_email_res, status=status.HTTP_400_BAD_REQUEST)

        # Getting the temporary user
        username = otp_data['username'] if 'username' in otp_data else None
        email = otp_data['email'] if 'email' in otp_data else None
        otp = otp_data['otp']
        if type(otp) == str:
            otp = int(otp)

        # Checking if user exists or not
        temp_users = TempUser.objects.filter(username=username) if username else TempUser.objects.filter(email=email)
        if not temp_users.exists():
            user_not_found_res = {
                'status': "failed",
                'message': "You are not registered with us! or Already verified!",
            }
            return Response(user_not_found_res, status=status.HTTP_400_BAD_REQUEST)

        # Getting the temporary user
        temp_user = temp_users.first()

        # getting signed otp from the temporary user
        signed_otp = temp_user.otp

        # Unsigned the otp with timestamp signer
        otp_signer = TimestampSigner(salt='otp_signer')
        unsigned_otp = otp_signer.unsign(signed_otp, max_age=settings.OTP_EXPIRY_TIME)

        # Checking if otp is correct or not
        if int(unsigned_otp) != otp:
            invalid_otp_res = {
                'status': "failed",
                'message': "Invalid otp!",
            }
            return Response(invalid_otp_res, status=status.HTTP_400_BAD_REQUEST)

        # If everything is correct
        # Deleting the temporary user
        temp_user.delete()

        # Getting the user
        users = User.objects.filter(username=username) if username else User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            user.is_active = True
            user.save()

            # Generating token to the user
            token, created = Token.objects.get_or_create(user=user)
            res = {
                'status': 'success',
                'message': 'User verified successfully!',
                'data': {
                    'token': token.key,
                }
            }
            return Response(res, status=status.HTTP_201_CREATED)

        # If something went wrong
        res = {
            'status': 'failed',
            'message': "Something went wrong!"
        }
        return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except SignatureExpired:
        error_res = {
            'status': 'unauthorized',
            'message': "Otp expired!",
        }
        return Response(error_res, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        error_res = {
            'status': 'error',
            'message': e.__str__(),
        }
        return Response(error_res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------------------@mit-------------------------------------
# View for user login
@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        # Extracting the login data from the request
        login_data = request.data

        # Checking if login data is present or not
        if not login_data:
            no_login_data_res = {
                'status': "failed",
                'message': "Please provide all the details",
            }
            return Response(no_login_data_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if username or email is present or not
        if 'username' not in login_data and 'email' not in login_data:
            no_username_or_email_res = {
                'status': "failed",
                'message': "Please provide your username or email!",
            }
            return Response(no_username_or_email_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if email is valid or not if email is present
        if 'email' in login_data and not Validators.validate_email(login_data['email']):
            invalid_email_res = {
                'status': "failed",
                'message': "Please provide valid email!",
            }
            return Response(invalid_email_res, status=status.HTTP_400_BAD_REQUEST)

        # Checking if password is present or not
        if 'password' not in login_data:
            no_password_res = {
                'status': "failed",
                'message': "Please provide password!",
            }
            return Response(no_password_res, status=status.HTTP_400_BAD_REQUEST)

        # If everything is present
        username = login_data['username'] if 'username' in login_data else None
        email = login_data['email'] if 'email' in login_data else None
        password = login_data['password']

        # Creating variable to store user
        user = None

        # Checking if user exists
        users = User.objects.filter(username=username) if username else User.objects.filter(email=email)
        if not users.exists():
            user_not_found_res = {
                'status': "failed",
                'message': "User not found!",
            }
            return Response(user_not_found_res, status=status.HTTP_400_BAD_REQUEST)

        # If user exists
        user = users.first()

        # Checking if password is correct or not
        if not user.check_password(password):
            invalid_password_res = {
                'status': "failed",
                'message': "Invalid password!",
            }
            return Response(invalid_password_res, status=status.HTTP_400_BAD_REQUEST)

        # Generating token to the user
        token, created = Token.objects.get_or_create(user=user)
        res = {
            'status': 'success',
            'message': 'User logged in successfully!',
            'data': {
                'token': token.key,
            }
        }
        return Response(res, status=status.HTTP_200_OK)

    except Exception as e:
        error_res = {
            'status': 'failed',
            'message': e.__str__(),
        }
        return Response(error_res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

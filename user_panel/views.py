from random import randint

from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from Web_zabanup.settings import KAVENEGAR_APIKEY
from . import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user in system"""
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.validated_data['generated_token'] = randint(100000, 999999)
            serializer.save()
        try:
            api = KavenegarAPI(KAVENEGAR_APIKEY)
            params = {'sender': '1000596446', 'receptor': serializer.validated_data['phone_number'],
                      'message': 'کالا نگار\n' + 'کد تایید:' + str(serializer.validated_data['generated_token'])}
            api.sms_send(params)
            return Response({"user": "signed up successfully",})

        except APIException:
            return Response(
                {
                    'error': 'ارسال کد تایید با مشکل مواجه شده است',
                    'type': 'APIException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except HTTPException:
            return Response(
                {
                    'error': 'ارسال کد تایید با مشکل مواجه شده است',
                    'type': 'HTTPException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = serializers.UserDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


#
# class UserPhoneRegisterAPIView(APIView):
#
#     def put(self, request):
#         data = request.data
#         user = get_object_or_404(get_user_model(), phone_number=data['phone_number'])
#         if user:
#             serializer = serializers.UserPhoneRegisterSerializer(user, data=data)
#             if serializer.is_valid():
#                 if serializer.data['generated_token'] == int(data.get("generated_token")):
#                     user.is_verified = True
#                     user.save()
#                     return Response({"user": "verified successfully"})
#                 else:
#                     return Response(
#                         {'error': 'The entered token is invalid'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



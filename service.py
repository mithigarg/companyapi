from rest_framework.response import Response
from companyapi.settings import CLIENT_SECRET
from rest_framework import status 


def is_client_secret_token(function):
    def wrap(request, *args, **kwargs):
        try:
            if request.headers['Client-Secret']:
                token = request.headers['Client-Secret']
                # validating access token
                if token == CLIENT_SECRET:
                    return function(request, *args, **kwargs)
                else:
                    return Response({'error': 'CLIENT_SECRET_NOT_FOUND'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'AUTH_CRED_NOT_PROVIDED'}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as exception:
            return Response({'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    return wrap
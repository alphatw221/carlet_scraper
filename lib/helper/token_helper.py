
import hashlib, hmac
import json, base64
import traceback
from datetime import datetime, timedelta
import uuid
import os



import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
class V1TokenHelper:

#     {
#   "typ": "JWT",
#   "alg": "RS256"
# }
    

#     {
#   "iat": 1702621063,
#   "exp": 2147483647,
#   "iss": "https://service.beta.carlet.com.tw",
#   "roles": [
#     "ROLE_MEMBER"
#   ],
#   "sid": "880a2ae0fe82ce70bd7354a792c78e74",
#   "evt": "token.decoded.member",
#   "id": 2308080035406412
# }
    @classmethod
    def __generate_token(cls, payload_data, secret_key):
        header_json = json.dumps(cls.header_data)
        header = base64.urlsafe_b64encode(header_json.encode('utf-8')).rstrip(b'=').decode('utf-8')

        payload_json = json.dumps(payload_data)
        payload = base64.urlsafe_b64encode(payload_json.encode('utf-8')).rstrip(b'=').decode('utf-8')

        head_and_claim = header+'.'+payload
        signature = hmac.new(secret_key.encode(), msg=head_and_claim.encode(), digestmod=hashlib.sha256).hexdigest()
        return head_and_claim+'.'+signature

    # @classmethod
    # def generate_user_token(cls, user):
            
    #     payload_data = {
    #         'token_type':'user',
    #         'id':user.id, 
    #         'uuid':str(user.uuid),
    #         # 'read_permissions':user.read_permissions,
    #         # 'write_permissions':user.write_permissions,
    #         # 'auth_perm':user.authorize_permissions,
    #         'exp':int((datetime.now()+timedelta(days=1)).timestamp())
    #     }
    #     return cls.__generate_token(payload_data, os.environ.get("SECRET_KEY",""))
       
    # @classmethod
    # def generate_customer_token(cls, customer):
            
    #     payload_data = {
    #         'token_type':'customer',
    #         'id':customer.id, 
    #         'uuid':str(customer.uuid),
    #         'first_name':customer.first_name,
    #         'last_name':customer.last_name,
    #         'email':customer.email,
    #         'exp':int((datetime.now()+timedelta(days=1)).timestamp())
    #     }
    #     return cls.__generate_token(payload_data, os.environ.get("SECRET_KEY",""))
    
    # @classmethod
    # def generate_guest_token(cls, first_name='', last_name='', cellphone='', email=''):
            
    #     payload_data = {
    #         'token_type':'guest',
    #         'uuid':str(uuid.uuid4()),
    #         'first_name':first_name,
    #         'last_name':last_name,
    #         'cellphone':cellphone,
    #         'email':email,
    #         'exp':int((datetime.now()+timedelta(days=7)).timestamp())
    #     }
    #     return cls.__generate_token(payload_data, os.environ.get("SECRET_KEY",""))
       
    def __sign_data(data, private_key_pem:bytes):
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )

        signature = private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return signature
    
    @classmethod
    def validate_token(cls, token):

        try:

            decoded_token = jwt.decode(
                token,
                key=os.environ.get('RSA_PUBLIC_KEY'),
                algorithms=["RS256"],
                audience="https://service.beta.carlet.com.tw",  
            )
            return True, decoded_token

        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return True, None
        except jwt.InvalidAudienceError:
            print("Invalid audience.")
            return True, None
        except jwt.InvalidIssuerError:
            print("Invalid issuer.")
            return True, None
        except jwt.InvalidTokenError:
            print("Invalid token.")
            return True, None




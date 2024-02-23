import time  # Importing the time module for time-related operations
import requests  # Importing the requests module for making HTTP requests
from jose import jwk, jwt  # Importing modules for JSON Web Key (JWK) and JWT handling
from jose.exceptions import JOSEError  # Importing exception classes for JOSE errors
from jose.utils import base64url_decode  # Importing utility function for decoding base64url-encoded strings

# Custom exception classes for Flask AWS Cognito errors and token verification errors
class FlaskAWSCognitoError(Exception):
    pass

class TokenVerifyError(Exception):
    pass

# Function to extract the access token from request headers
def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get("Authorization")  # Extracting the Authorization header from request headers
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()  # Splitting the header to extract the token part
    return access_token

# Class for handling AWS Cognito JWT tokens
class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region  # Setting the AWS region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")  # Raising an error if no AWS region is provided
        self.user_pool_id = user_pool_id  # Setting the Cognito user pool ID
        self.user_pool_client_id = user_pool_client_id  # Setting the Cognito user pool client ID
        self.claims = None  # Initializing claims attribute to None
        if not request_client:
            self.request_client = requests.get  # Using requests.get as the default request client
        else:
            self.request_client = request_client  # Using the provided request client
        self._load_jwk_keys()  # Loading JWK keys from Cognito

    # Method to load JWK keys from Cognito
    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)  # Sending a GET request to the JWK keys URL
            self.jwk_keys = response.json()["keys"]  # Extracting and storing the JWK keys from the response
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e  # Raising an error if there's an issue with the request

    # Static method to extract JWT headers
    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)  # Extracting JWT headers using jose library
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    # Method to find the public key based on JWT headers
    def _find_pkey(self, headers):
        kid = headers["kid"]  # Extracting the Key ID (kid) from headers
        # Searching for the key ID in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")  # Raising an error if key ID is not found
        return self.jwk_keys[key_index]  # Returning the public key data

    # Static method to verify JWT signature
    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            public_key = jwk.construct(pkey_data)  # Constructing the public key object
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        message, encoded_signature = str(token).rsplit(".", 1)  # Splitting token to extract message and signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))  # Decoding the signature
        # Verifying the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")  # Raising an error if signature verification fails

    # Static method to extract JWT claims
    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)  # Extracting JWT claims using jose library
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    # Method to check token expiration
    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()  # Getting current time if not provided
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # Raising an error if token is expired

    # Method to check token audience
    def _check_audience(self, claims):
        audience = claims["aud"] if "aud" in claims else claims["client_id"]  # Extracting audience from claims
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")  # Raising an error if audience doesn't match

    # Method to verify JWT token
    def verify(self, token, current_time=None):
        if not token:
            raise TokenVerifyError("No token provided")  # Raising an error if no token is provided

        headers = self._extract_headers(token)  # Extracting JWT headers
        pkey_data = self._find_pkey(headers)  # Finding public key based on headers
        self._verify_signature(token, pkey_data)  # Verifying JWT signature

        claims = self._extract_claims(token)  # Extracting JWT claims
        self._check_expiration(claims, current_time)  # Checking token expiration
        self._check_audience(claims)  # Checking token audience

        self.claims = claims  # Storing the claims for future reference
        return claims  # Returning the claims

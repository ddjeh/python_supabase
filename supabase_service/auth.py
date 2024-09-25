from typing import Literal

from gotrue import AuthResponse, SignUpWithEmailAndPasswordCredentialsOptions, SignInWithPasswordCredentialsOptions, \
    SignOutOptions, ResendEmailCredentialsOptions

from supabase_service.config import SupabaseClient
from supabase_service.types import GenericResponse


class SupabaseAuth(SupabaseClient):

    def __init__(self):
        super().__init__()
        self.__client_auth = self._get_client

    def sign_in(self, email: str, password: str, options: SignInWithPasswordCredentialsOptions) -> GenericResponse:
        """
        :param email: str
        :param password: str
        :param options: SignInWithPasswordCredentialsOptions
        :return:
        """
        if not email or not email.strip():
            return GenericResponse(status=400, message="Email is required")

        if not password or not password.strip():
            return GenericResponse(status=400, message="Password is required")

        try:
            auth_response: AuthResponse = self.__client_auth.sign_in_with_password(
                credentials={"email": email, "password": password, "options": options})
            return GenericResponse(status=200, message="Sign in successful", data={
                "user_id": auth_response.user.id,
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token,
                "expires_in": auth_response.session.expires_in,
                "token_type": auth_response.session.token_type,
                "status": 200
            })
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def sign_up(self, email: str, password: str,
                options: SignUpWithEmailAndPasswordCredentialsOptions) -> GenericResponse:
        """
        :param email: str
        :param password: str
        :param options: SignUpWithEmailAndPasswordCredentialsOptions
        :return: AuthResponse | str
        """
        if not email or not email.strip():
            return GenericResponse(status=400, message="Email is required")

        if not password or not password.strip():
            return GenericResponse(status=400, message="Password is required")

        try:
            sign_up_response = self.__client_auth.sign_up(
                credentials={"email": email, "password": password, "options": options})

            return GenericResponse(status=201, message="Sign up successful", data=sign_up_response)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def sign_out(self, options: SignOutOptions):
        """
        :param options: SignOutOptions
        :return: None
        """
        self.__client_auth.sign_out(options=options)

    def get_user(self, access_token: str) -> GenericResponse:
        """
        :param access_token: str
        :return: UserResponse | str
        """

        if not access_token or not access_token.strip():
            return GenericResponse(status=400, message="Access token is required")

        try:
            user = self.__client_auth.get_user(jwt=access_token)

            return GenericResponse(status=200, message="User retrieved successfully", data=user)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def resend_mail(self, email: str, type: Literal["signup", "email_change"],
                    options: ResendEmailCredentialsOptions) -> GenericResponse:
        """
        :param email: str
        :param type: str
        :param options: ResendEmailCredentialsOptions
        :return:
        """
        if not email or not email.strip():
            return GenericResponse(status=400, message="Email is required")

        resend_mail = self.__client_auth.resend(email=email, type=type, options=options)

        return GenericResponse(status=200, message="Email sent successfully", data=resend_mail)

    def refresh_token(self, refresh_token: str) -> GenericResponse:
        """
        :param refresh_token: str
        :return: GenericResponse
        """
        if not refresh_token or not refresh_token.strip():
            return GenericResponse(status=400, message="Refresh token is required")
        try:
            refresh_session = self.__client_auth.refresh_session(refresh_token=refresh_token)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

        return GenericResponse(status=200, message="Session refreshed successfully", data=refresh_session)

    def is_logged_in(self, access_token: str) -> bool:
        """
        :param access_token: str
        :return: bool
        """
        if not access_token or not access_token.strip():
            return False

        user = self.get_user(access_token=access_token)

        return user is not None

# Authentication App

This app handles user authentication and authorization for the LMS.

## Features
- **Custom User Model**: Uses email as the primary identifier instead of a username.
- **JWT Authentication**: Implements JSON Web Tokens via `djangorestframework-simplejwt`.
- **Endpoints**:
    - `/api/auth/login/`: Obtain access and refresh tokens.
    - `/api/auth/token/refresh/`: Refresh an expired access token.
    - `/api/auth/token/verify/`: Verify the validity of a token.

## Components
- `models.py`: Defines the `User` and `UserManager`.
- `serializers.py`: Handles user data serialization.
- `urls.py`: Routes for auth-related actions.

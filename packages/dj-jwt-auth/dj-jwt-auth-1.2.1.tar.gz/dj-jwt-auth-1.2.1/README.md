# Django-JWT

This is a package to verify and validate JSON Web Tokens (JWT) in Django.

### Installation
1. Install the package using pip.

2. Add "django_jwt" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'django_jwt',
    ]
```

3. Add "django_jwt.middleware.JWTAuthMiddleware" to your MIDDLEWARE setting like this::
```
    MIDDLEWARE = [
        ...
        'django_jwt.middleware.JWTAuthMiddleware',
    ]
```

### Configuration:
Required variables:
- OIDC_CONFIG_ROUTES - dict of 'algorithm': 'config_url', by default is empty. If filled will be used instead of OIDC_CERTS_URL
```
   OIDC_CONFIG_ROUTES = {
       'RS256': 'https://keyCloak/realms/h/.well-known/openid-configuration',
       'HS256': 'https://keyCloak/realms/h/.well-known/openid-configuration',
   } 
```

Optional variables:
- OIDC_AUDIENCE - by default ["account", "broker"]
User retated variables:
- OIDC_USER_UPDATE - if True, user model will be updated from userinfo endpoint if MODIFIED date has changed, by default True
- OIDC_USER_MODIFIED_FIELD - user model field to store last modified date, by default `modified_timestamp`
- OIDC_TOKEN_MODIFIED_FIELD - access token field to store last modified date, by default `updated_at`
- OIDC_USER_UID - User model' unique identifier, by default `kc_id`
- OIDC_USER_MAPPING - mapping between JWT claims and user model fields, by default:
```
    OIDC_USER_MAPPING = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'username': 'username',
    }
```
- OIDC_USER_DEFAULTS - default values for user model fields, by default:
```
    OIDC_USER_DEFAULTS = {
        'is_active': True,
    }
```

- OIDC_USER_ON_CREATE and OIDC_USER_ON_UPDATE - functions to be called on user creation and update, by default:
```
    OIDC_USER_ON_CREATE = None
    OIDC_USER_ON_UPDATE = None
```
- OIDC_ADMIN_ISSUER - URL of the OIDC provider, by default None
These functions should accept two arguments: user and request.

### Testing:
Run command `python runtests.py` to run tests.
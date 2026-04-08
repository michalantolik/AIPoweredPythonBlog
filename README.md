## ⚙️ Application Settings

### Settings Flow

- `settings.base.py` contains the shared default settings
- `settings.dev.py` imports everything from `base.py` and overrides only a few settings for local development
- `settings.prod.py` imports everything from `base.py` and overrides/adds production-specific settings

```mermaid
graph TD
    subgraph EP[Entry Points]
        A[manage.py]
        C[wsgi.py]
        E[asgi.py]
    end

    subgraph ES[Environment Settings]
        B[settings.dev]
        D[settings.prod]
    end

    F[settings.base]

    A --> B
    C --> D
    E --> D
    B --> F
    D --> F

    %% Node styles
    classDef entry fill:#e3f2fd,stroke:#1e88e5;
    classDef config fill:#e8f5e9,stroke:#43a047;
    classDef base fill:#fff3e0,stroke:#fb8c00;

    class A,C,E entry;
    class B,D config;
    class F base;

    %% ✅ THIS NOW WORKS
    style EP fill:#f8f9fa,stroke:#ddd
    style ES fill:#f8f9fa,stroke:#ddd
```

### Settings Values

| Variable | Values (base / dev / prod) | Description |
|---|---|---|
| `BASE_DIR` | **base:** `Path(__file__).resolve().parents[2]`<br>**dev:** `-`<br>**prod:** `-` | Root directory of the project |
| `SECRET_KEY` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Secret key used for cryptographic signing |
| `DEBUG` | **base:** `get_bool_env(..., False)`<br>**dev:** `True`<br>**prod:** `False` | Enables debug mode |
| `ALLOWED_HOSTS` | **base:** `get_list_env(..., ["127.0.0.1","localhost"])`<br>**dev:** `["127.0.0.1","localhost"]`<br>**prod:** `get_list_env(..., [])` | Allowed hosts/domains |
| `INSTALLED_APPS` | **base:** `[...]`<br>**dev:** `-`<br>**prod:** `-` | Installed Django apps |
| `AUTH_USER_MODEL` | **base:** `"users.User"`<br>**dev:** `-`<br>**prod:** `-` | Custom user model |
| `MIDDLEWARE` | **base:** `[...]`<br>**dev:** `-`<br>**prod:** `-` | Middleware stack |
| `ROOT_URLCONF` | **base:** `"ai_powered_blog.urls"`<br>**dev:** `-`<br>**prod:** `-` | URL routing config |
| `TEMPLATES` | **base:** `[...]`<br>**dev:** `-`<br>**prod:** `-` | Template engine config |
| `WSGI_APPLICATION` | **base:** `"ai_powered_blog.wsgi.application"`<br>**dev:** `-`<br>**prod:** `-` | WSGI entry |
| `ASGI_APPLICATION` | **base:** `"ai_powered_blog.asgi.application"`<br>**dev:** `-`<br>**prod:** `-` | ASGI entry |
| `DATABASE_ENGINE` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Database engine |
| `DATABASES` | **base:** `dynamic config`<br>**dev:** `-`<br>**prod:** `-` | DB connection settings |
| `AUTH_PASSWORD_VALIDATORS` | **base:** `[...]`<br>**dev:** `-`<br>**prod:** `-` | Password validation rules |
| `LANGUAGE_CODE` | **base:** `"en-us"`<br>**dev:** `-`<br>**prod:** `-` | Default language |
| `TIME_ZONE` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Timezone |
| `USE_I18N` | **base:** `True`<br>**dev:** `-`<br>**prod:** `-` | Internationalization |
| `USE_TZ` | **base:** `True`<br>**dev:** `-`<br>**prod:** `-` | Timezone-aware datetimes |
| `STATIC_URL` | **base:** `"/static/"`<br>**dev:** `-`<br>**prod:** `-` | Static URL prefix |
| `STATICFILES_DIRS` | **base:** `[BASE_DIR / "static"]`<br>**dev:** `-`<br>**prod:** `-` | Static dirs |
| `STATIC_ROOT` | **base:** `BASE_DIR / "staticfiles"`<br>**dev:** `-`<br>**prod:** `-` | Collected static dir |
| `STATICFILES_STORAGE` | **base:** `"whitenoise..."`<br>**dev:** `-`<br>**prod:** `-` | Static storage backend |
| `DEFAULT_AUTO_FIELD` | **base:** `"BigAutoField"`<br>**dev:** `-`<br>**prod:** `-` | Default PK type |
| `EMAIL_BACKEND` | **base:** `-`<br>**dev:** `"console backend"`<br>**prod:** `-` | Email backend |
| `INTRO_OVERLAY_ENABLED` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | UI intro toggle |
| `INTRO_OVERLAY_DURATION_MS` | **base:** `get_int_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Intro duration |
| `INTRO_OVERLAY_IMAGE` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Intro image |
| `SHOW_SIDEBAR_ON_HOME_STARTUP` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Sidebar toggle |
| `LIVE_POST_FILTER_ENABLED` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Live filter toggle |
| `SECURE_CONTENT_TYPE_NOSNIFF` | **base:** `True`<br>**dev:** `-`<br>**prod:** `-` | MIME sniff protection |
| `X_FRAME_OPTIONS` | **base:** `"DENY"`<br>**dev:** `-`<br>**prod:** `-` | Clickjacking protection |
| `SESSION_COOKIE_HTTPONLY` | **base:** `True`<br>**dev:** `-`<br>**prod:** `-` | HTTP-only session cookie |
| `SESSION_COOKIE_SAMESITE` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | SameSite session policy |
| `SESSION_COOKIE_SECURE` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_bool_env(...)` | HTTPS-only cookie |
| `CSRF_COOKIE_HTTPONLY` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | HTTP-only CSRF cookie |
| `CSRF_COOKIE_SAMESITE` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | SameSite CSRF policy |
| `CSRF_COOKIE_SECURE` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_bool_env(...)` | Secure CSRF cookie |
| `CSRF_TRUSTED_ORIGINS` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_list_env(...)` | Trusted CSRF origins |
| `SECURE_REFERRER_POLICY` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Referrer policy |
| `SECURE_CROSS_ORIGIN_OPENER_POLICY` | **base:** `get_env(...)`<br>**dev:** `-`<br>**prod:** `-` | COOP policy |
| `SECURE_SSL_REDIRECT` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_bool_env(...)` | Force HTTPS |
| `SECURE_HSTS_SECONDS` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_int_env(...)` | HSTS duration |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_bool_env(...)` | HSTS subdomains |
| `SECURE_HSTS_PRELOAD` | **base:** `-`<br>**dev:** `-`<br>**prod:** `get_bool_env(...)` | HSTS preload |
| `SECURE_PROXY_SSL_HEADER` | **base:** `-`<br>**dev:** `-`<br>**prod:** `("HTTP_X_FORWARDED_PROTO","https")` | Proxy SSL header |
| `USE_X_FORWARDED_HOST` | **base:** `-`<br>**dev:** `-`<br>**prod:** `True` | Use proxy host |
| `APP_CSP_ENABLED` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Enable CSP |
| `APP_CSP_DIRECTIVES` | **base:** `{...}`<br>**dev:** `-`<br>**prod:** `extended {...}` | CSP rules |
| `APP_CSP_EXCLUDE_PATH_PREFIXES` | **base:** `("/admin/",)`<br>**dev:** `-`<br>**prod:** `-` | CSP exclusions |
| `APP_PERMISSIONS_POLICY_ENABLED` | **base:** `get_bool_env(...)`<br>**dev:** `-`<br>**prod:** `-` | Enable permissions policy |
| `APP_PERMISSIONS_POLICY` | **base:** `{...}`<br>**dev:** `-`<br>**prod:** `-` | Browser feature restrictions |

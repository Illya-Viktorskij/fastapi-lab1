from prometheus_client import Gauge, Counter, Histogram

# === Бізнес-метрики ===

TOTAL_USERS = Gauge(
    "app_total_users",
    "Total number of registered users"
)

TOTAL_POSTS = Gauge(
    "app_total_posts",
    "Total number of posts"
)

TOTAL_COMMENTS = Gauge(
    "app_total_comments",
    "Total number of comments"
)

AUTH_LOGINS_TOTAL = Counter(
    "app_auth_logins_total",
    "Total number of successful logins"
)

AUTH_FAILURES_TOTAL = Counter(
    "app_auth_failures_total",
    "Total number of failed login attempts"
)

# === Кастомні метрики ===

CRUD_OPERATIONS_TOTAL = Counter(
    "app_crud_operations_total",
    "Total number of CRUD operations",
    ["operation", "entity"]
)

HTTP_REQUEST_DURATION = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint", "status_code"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ERRORS_TOTAL = Counter(
    "app_errors_total",
    "Total number of application errors",
    ["error_type", "endpoint"]
)

ACTIVE_DB_SESSIONS = Gauge(
    "app_active_db_sessions",
    "Number of currently active database sessions"
)
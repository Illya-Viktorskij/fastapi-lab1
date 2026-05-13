from prometheus_client import Gauge

TOTAL_USERS = Gauge("app_total_users", "Total number of registered users")
TOTAL_POSTS = Gauge("app_total_posts", "Total number of posts")
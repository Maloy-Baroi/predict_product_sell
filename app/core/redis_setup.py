# Create a Redis client instance
from redis import Redis
import os


def get_redis_client():
    redis_host = 'localhost'
    redis_port = 6380
    redis_username = None
    redis_password = None
    

    return Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password
    )

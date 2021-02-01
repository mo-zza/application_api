"""
flask의 환경변수 저장

"""

import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "sample-secret"
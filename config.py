import pymysql
pymysql.install_as_MySQLdb()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3307/language'
    SECRET_KEY = b'm\xd6\xf0\xad\xc6\xe0\xfa\xcc\xc8 \x8b\n\xa23\xc9\xe9%s\xc6S\x9a{\xed\xa7'  # Chuỗi bí mật để bảo mật session


# import os
# print(os.urandom(24))

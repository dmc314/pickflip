import hashlib

def create_user_uuid(user_id, user_name):
    user_id = user_name + user_id
    user_id = hashlib.md5(user_id.encode()).hexdigest()[0:16]
    return user_id
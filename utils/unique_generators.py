import shortuuid
import random


class GenerateUUIDCode():
    def alpha_numeric_uid(length):
        code = shortuuid
        uid_code = code.ShortUUID(alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        _code = uid_code.uuid()[:length]
        return _code

    def numeric_uid(length):
        code = shortuuid
        uid_code = code.ShortUUID(alphabet="0123456789")
        _code = uid_code.uuid()[:length]
        return _code


def generate_token(len):
    token = [random.randint(1, 9) for _ in range(len)]
    clean_token = ''.join(str(e) for e in token)
    return clean_token
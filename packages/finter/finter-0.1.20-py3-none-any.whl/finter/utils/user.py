import time
from finter.api.user_api import UserApi
import uuid
import hashlib
from finter.rest import ApiException
from finter.settings import logger


def user_event(name, source="", method="", category=""):
    def _random_hash():
        random_uuid = uuid.uuid4()
        uuid_bytes = str(random_uuid).encode()
        hash_object = hashlib.sha256(uuid_bytes)
        return hash_object.hexdigest()

    params = {
        "name": name,
        "source": source,
        "method": method,
        "category": category,
        "rand": _random_hash()
    }
    try:
        UserApi().log_usage_retrieve(**params)
    except ApiException as e:
        logger.error("Exception when calling UserApi->log_usage_retrieve: %s\n" % e)

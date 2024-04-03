import logging

from users.models import User

logger = logging.getLogger(__name__)


def process_user_updated_event(user_data: dict) -> dict:
    try:
        user = User.objects.get(public_id=user_data["public_id"])
    except User.DoesNotExist:
        return

    user.first_name = user_data["first_name"]
    user.last_name = user_data["last_name"]
    user.role = user_data["role"]
    user.save()

    logger.info(f'updated user: {user.public_id}')


def process_user_deleted_event(user_data: dict) -> dict:
    try:
        user = User.objects.get(public_id=user_data["public_id"])
    except User.DoesNotExist:
        return

    user_id = user.public_id

    user.delete()

    logger.info(f'deleted user: {user_id}')


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def find_index(post_id, posts_list):
    return next((index for (index, item) in enumerate(posts_list) if item['id'] == post_id), None)


def hash_text(text: str):
    return pwd_context.hash(text)

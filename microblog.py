from app import create_app, db
from app.models import User, Post
from app.data_access import UserDAO

microblog_app = create_app()

@microblog_app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'UserDAO': UserDAO,
    }
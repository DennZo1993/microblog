from app import db, login
from app.models import User


class UserDAO:

    @staticmethod
    @login.user_loader
    def get_by_id(user_id):
        return User.query.get(int(user_id))

    @staticmethod
    def get_by_credentials(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return None
        return user

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def create(username, password, email):
        user = User(username=username)
        user.set_password(password)
        user.set_email(email)

        db.session.add(user)
        db.session.commit()

        return user
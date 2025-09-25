from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    user = User(username='test', email='test@test', password='secret')

    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.username == 'test'
    assert user.email == 'test@test'
    assert user.password == 'secret'

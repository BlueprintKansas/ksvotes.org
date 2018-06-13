## Conftest from https://stackoverflow.com/questions/26555125/rollback-transactions-not-working-with-py-test-and-flask/26624146

import pytest

from app import create_app
from app import db as _db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def app(request):
    app = create_app("testing")
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()

@pytest.fixture(scope="session")
def client(app, request):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def db_session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()

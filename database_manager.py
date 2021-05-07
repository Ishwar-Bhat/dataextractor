from contextlib import contextmanager

import psycopg2


@contextmanager
def db_connection(config: dict):
    """
    Creates a  session object for DB interactions from given config
    Args:
        config: Database configs

    Returns:
        session for db interaction
    """
    session = None

    # Close connection function
    def close_connection(c): return c.close() if c else None

    try:
        # create a session
        session = psycopg2.connect(**config)

        # Return the session
        yield session

        # Commit and close the session after exit
        session.commit()
        session.close()

    except Exception as e:
        # When exception occurs close connection if exists and raise the error
        print(f"{e}")
        close_connection(session)
        raise e

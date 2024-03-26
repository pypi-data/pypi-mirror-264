from sqlalchemy import create_engine


def get_data_db_connection(data_db_URL: str):
    engine = create_engine(
        url=data_db_URL,
        connect_args={
            "options": "-c timezone=utc",
            "application_name": "deriver-test",
        },
    )

    connection = engine.connect()

    connection.execution_options(readonly=True)

    return connection

import oracledb
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker

from ..config import settings


class OracleAPI:
    def __init__(self):
        self.pool = oracledb.create_pool(
            user=settings.ORACLE_USERNAME,
            password=settings.ORACLE_PASSWORD,
            host=settings.ORACLE_HOST,
            port=settings.ORACLE_PORT,
            service_name=settings.ORACLE_SERVICE_NAME,
            min=100,
            max=100,
            increment=0
        )

        self.engine = create_engine("oracle+oracledb://", creator=self.pool.acquire, poolclass=NullPool)

        # Create a session to the database
        self.session = sessionmaker(bind=self.engine)()

    def read(self, sql):
        return self.session.execute(sql).fetchone()

    def all(self, sql):
        return self.session.execute(sql).fetchall()

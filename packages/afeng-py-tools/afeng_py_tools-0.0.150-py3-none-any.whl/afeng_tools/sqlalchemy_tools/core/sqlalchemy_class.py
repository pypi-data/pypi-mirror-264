import re
from sqlalchemy import Column, DateTime, Boolean, Float, func, BigInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from afeng_tools.sqlalchemy_tools.core.sqlalchemy_items import DatabaseInfoItem
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_meta_class import ModelMetaClass


class SqlalchemyDb:
    """数据库对象"""

    def __init__(self, database_info: DatabaseInfoItem):
        self.database_info = database_info
        self.Base = declarative_base()
        self.BaseModel = self._create_base_model()
        self.is_postgresql = True if re.match('^postgresql', self.database_info.database_uri) else False
        self.Base.is_postgresql = self.is_postgresql
        self.engine = create_engine(self.database_info.database_uri,
                                    echo=self.database_info.echo_sql,
                                    pool_size=self.database_info.pool_size,
                                    pool_pre_ping=self.database_info.pool_pre_ping,
                                    pool_recycle=self.database_info.pool_recycle,
                                    pool_use_lifo=self.database_info.pool_use_lifo, )
        self.session_maker = sessionmaker(bind=self.engine,
                                          autocommit=self.database_info.auto_commit,
                                          autoflush=self.database_info.auto_flush,
                                          expire_on_commit=self.database_info.expire_on_commit)

    def _create_base_model(self):
        class BaseModel(self.Base, metaclass=ModelMetaClass):
            """模型根类"""
            __abstract__ = True

            id = Column(BigInteger, comment='主键', primary_key=True, index=True, autoincrement=True)
            add_time = Column(DateTime, comment='添加时间', default=func.now())
            update_time = Column(DateTime, comment='修改时间', default=func.now(), onupdate=func.now())
            is_enable = Column(Boolean, comment='是否可用', default=True)
            order_num = Column(Float, comment='排序值', default=100)

        return BaseModel

    def get_session(self) -> Session:
        """获取Session"""
        return self.session_maker()

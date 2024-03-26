import json
import time

from .kafka2mysql_models import Message, MessageFlag

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
class KafkaProducer:
    def __init__(self,drivername,username,password,host,port,database,query={"charset":"utf8mb4"}):
        middleware_url = URL(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query=query,
        )
        middleware_engine = create_engine(middleware_url, pool_timeout=20, pool_recycle=299)
        MiddlewareSessionFactory = sessionmaker(bind=middleware_engine, autocommit=False, autoflush=True)
        self.session = MiddlewareSessionFactory()
    def send(self, topic, message):
        new_message = Message(topic=topic,message=json.loads(message))
        self.session.add(new_message)
        self.session.commit()

    def close(self):
        self.session.close()

class ResultMessage:
    def __init__(self,value):
        self.value = value

class KafkaConsumer:
    def __init__(self,topic,drivername,username,password,host,port,database,group_id=-1,query={"charset":"utf8mb4"}):
        middleware_url = URL(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query=query,
        )
        self.topic = topic
        self.group_id = group_id
        middleware_engine = create_engine(middleware_url, pool_timeout=20, pool_recycle=299)
        MiddlewareSessionFactory = sessionmaker(bind=middleware_engine, autocommit=False, autoflush=True)
        self.session = MiddlewareSessionFactory()

    def __next__(self):
        while True:
            self.session.commit()
            min_message_id = self.session.query(MessageFlag.message_id).filter(MessageFlag.group_id==self.group_id).order_by(-MessageFlag.message_id).first()
            if min_message_id:
                min_message_id = min_message_id[0]
            else:
                min_message_id = 0
            row = self.session.query(Message).filter(Message.id>min_message_id).first()
            if row:
                try:
                    message_flag = MessageFlag(message_id=row.id, group_id=self.group_id)
                    message = ResultMessage(row.message)
                    self.session.add(message_flag)
                    self.session.commit()
                    return message
                except Exception as e:
                    self.session.rollback()
                    # print('消费者冲突,sleep')
                    time.sleep(0.5)
                    return None
            else:
                # print('无数据，sleep')
                time.sleep(0.5)
                return None



    def __iter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.session:
            self.session.close()



if __name__ == '__main__':
    pass

import json
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from .redis2mysql_models import StringData,HashData

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


class Redis2MySQL:
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
    def set(self, key, value, ex=None):
        record = self.session.query(StringData).filter_by(key=key).first()
        if isinstance(ex,timedelta):
            ex = ex.total_seconds()
        expiretime = datetime.now() + timedelta(seconds=ex) if ex else None
        if record:
            record.value = value
            record.expiretime = expiretime
        else:
            record = StringData(key=key, value=value,expiretime=expiretime)
            self.session.add(record)
        self.session.commit()

    def get(self, key):
        self.session.commit()
        time_now = datetime.now()
        record = self.session.query(StringData).filter(
            StringData.key == key,
            or_(StringData.expiretime >= time_now, StringData.expiretime.is_(None))
        ).first()
        return record.value.encode('utf-8') if record else None

    def delete(self, key):
        # 删除string的key
        record = self.session.query(StringData).filter_by(key=key).first()
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        # 删除hash的key
        record = self.session.query(HashData).filter_by(key=key).first()
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        return False

    def exists(self, key):
        # 检查string的key是否存在
        time_now = datetime.now()
        record = self.session.query(StringData).filter(
            StringData.key == key,
            or_(StringData.expiretime >= time_now, StringData.expiretime.is_(None))
        ).first()
        if record:
            return True

        # 检查hash的key是否存在
        record = self.session.query(HashData).filter(
            HashData.key == key
        ).first()
        if record:
            return True
        return False

    def keys(self,pattern):
        time_now = datetime.now()
        record = self.session.query(StringData.key).filter(func.regexp_like(StringData.key,pattern),
                                                           or_(StringData.expiretime >= time_now,
                                                               StringData.expiretime.is_(None))
                                                           ).all()
        hash_reocrd = self.session.query(HashData.key).filter(func.regexp_like(HashData.key,pattern)
                                                           ).all()
        record = [x[0] for x in record]
        hash_reocrd = [x[0] for x in hash_reocrd]
        record.extend(hash_reocrd)
        return record
    def hset(self, key, field, value):
        value_json = json.dumps(value)
        record = self.session.query(HashData).filter_by(key=key, field=field).first()
        if record:
            record.value = value_json
        else:
            record = HashData(key=key, field=field, value=value_json)
            self.session.add(record)
        self.session.commit()

    def hincrby(self, key, field, increment):
        record = self.session.query(HashData).filter_by(key=key, field=field).first()
        if record:
            current_value = json.loads(record.value)
            new_value = int(current_value) + increment
            record.value = json.dumps(new_value)
        else:
            new_value = increment
            record = HashData(key=key, field=field, value=json.dumps(new_value))
            self.session.add(record)
        self.session.commit()


    def hmset(self, key, mapping):
        for field, value in mapping.items():
            value_json = json.dumps(value)
            record = self.session.query(HashData).filter_by(key=key, field=field).first()
            if record:
                record.value = value_json
            else:
                record = HashData(key=key, field=field, value=value_json)
                self.session.add(record)
        self.session.commit()


    def hget(self, key, field):
        record = self.session.query(HashData).filter_by(key=key, field=field).first()
        return json.loads(record.value) if record else None

    def hgetall(self, key):
        records = self.session.query(HashData).filter_by(key=key).all()
        result = {}
        for record in records:
            result[record.field] = json.loads(record.value)
        return result

    def hdel(self, key, *fields):
        record = self.session.query(HashData).filter(HashData.key == key, HashData.field.in_(fields))
        if record:
            record.delete()
            self.session.commit()
            return True
        else:
            return False
    def close(self):
        self.session.close()


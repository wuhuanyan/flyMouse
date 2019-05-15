from os import path
import sqlalchemy.exc
from database.models import Base
import sqlalchemy as sqla
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import reflection


basePath, filename = path.split(path.split(path.abspath(__file__))[0])


class DataBase:
    """
    数据库操作类
    """
    def __init__(self, ip_address=None, username=None, password=None,
                 schema=None, port=None, database_type=None, sqlite3_path=None):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.schema = schema
        self.port = port
        if sqlite3_path is None:
            self.uri = database_type_dict[database_type][1]
            self.uri = self.uri.format(username, password, ip_address, port, schema)
            self.database_type = database_type_dict[database_type][0]
        else:
            self.uri = self.uri = sqlite3_path
        self.engine = self.create_engine(self.uri)

    def test_connect(self):
        try:
            c = self.engine.connect()
            c.close()
            return True, '连接成功!'
        except Exception as e:
            return False, '连接失败!\n失败原因:'+str(e)

    @staticmethod
    def create_engine(uri):
        """
        除mysql外,其他数据库创建engine都自动带cursor
        cursor用于查询sql时候分批读取数据,而不是一次性把数据加载到内存中
        :param uri: 数据库连接uri
        :return: 带cursor的engine
        """
        if 'mysql' not in str(uri):
            if 'sqlite' in str(uri):
                engine = sqla.create_engine(uri,
                                            connect_args={'check_same_thread': False},
                                            poolclass=StaticPool)
            else:
                engine = sqla.create_engine(uri)
        else:
            # 创建带server_side_cursors的engine
            engine = sqla.create_engine(uri, server_side_cursors=True)
            # engine = sqla.create_engine(uri)
        return engine

    def init_database(self):
        """
        初始化本地数据库的表,当表已经存在时,不会重新初始化
        :return:
        """
        try:
            Base.metadata.create_all(self.engine)
            return True, '初始化成功!'
        except Exception as e:
            return False, '初始化失败!\n失败原因:' + str(e)

    @staticmethod
    def get_model_columns(class_, language='cn'):
        """
        获取中文|英文字段名称的列表
        :param class_: sqla的类
        :param language: 'en' 英文,'cn' 中文
        :return:
        """
        return class_.get_columns(language)

    @staticmethod
    def get_model_columns_by_relation(class_, language='cn'):
        """
        获取中文|英文字段名称的列表 当需要关联的时候
        :param class_: sqla的类
        :param language: 'en' 英文,'cn' 中文
        :return:
        """
        return class_.get_columns_by_relation(language)

    def select_table(self, class_, id_=None, filter_dict=None):
        """
        查询整张表
        :param class_:sqla的类
        :param id_:sqla的类的ID,表的ID
        :param filter_dict:过滤的字典{models.DataBase.local_database: 1}
        :return: 列表
        """
        columns_list = self.get_model_columns(class_, 'en')
        select_list = list()
        for c in columns_list:
            select_list.append(getattr(class_, c))
        session = Session(self.engine)
        q_obj = session.query(*select_list)
        if id_ is not None:
            q_obj = q_obj.filter(class_.id == id_)
        if filter_dict is not None:
            for k, v in dict(filter_dict).items():
                q_obj = q_obj.filter(k == v)
        q_obj_list = q_obj.all()
        session.close()
        return q_obj_list

    def select_table_by_relation(self, class_, id_=None, filter_dict=None):
        """
        查询整张表 当要关联的时候
        :param class_:sqla的类
        :param id_:sqla的类的ID,表的ID
        :param filter_dict:过滤的字典
        :return: 列表
        """
        columns_list = self.get_model_columns_by_relation(class_, 'en')
        session = Session(self.engine)
        q_obj = session.query(class_)
        if id_ is not None:
            q_obj = q_obj.filter(class_.id == id_)
        if filter_dict is not None:
            for k, v in dict(filter_dict).items():
                q_obj = q_obj.filter(k == v)
        q_obj_list = list()
        for r in q_obj:
            tmp_list = list()
            for cl in columns_list:
                if isinstance(cl, str):
                    data = getattr(r, cl)
                    tmp_list.append(data)
                elif isinstance(cl, list):
                    try:
                        data = getattr(getattr(r, cl[0]), cl[1])
                    except AttributeError:
                        data = None
                    tmp_list.append(data)
            q_obj_list.append(tmp_list)
        return q_obj_list

    def insert_table(self, class_, data_key, data_value):
        """
        插入数据
        :param class_:sqla的类
        :param data_key: 字段名
        :param data_value: 值,与字段名对应
        :return: 批量插入后的ID列表
        """
        if data_key is None:
            data_key = self.get_model_columns(class_, language='en')
        session = Session(self.engine)
        if 'sqlite' in self.uri:  # 如果是sqlite数据库,需要执行启用外键语句
            session.execute("PRAGMA foreign_keys=ON")
        id_list = []
        for i in range(0, len(data_value)):
            d = dict(zip(data_key, data_value[i]))
            c = class_(d)
            session.add(c)
            session.commit()
            id_list.append(int(c.id))
        session.close()
        return id_list

    def delete_table_by_id(self, class_, id_):
        """
        根据id删除表
        :param class_: sqla的类
        :param id_: sqla的类的ID, 表的ID
        :return:
        """
        session = Session(self.engine)
        if 'sqlite' in self.uri:  # 如果是sqlite数据库,需要执行启用外键语句
            session.execute("PRAGMA foreign_keys=ON")
        try:
            session.query(class_).filter(class_.id == id_).delete()
            session.commit()
        except sqla.exc.IntegrityError as e:
            return False, str(e)
        finally:
            session.close()
        return True, ''

    def updata_table_by_id(self, class_, id_, data_key, data_value):
        """
        根据ID更新表的信息
        :param class_: sqla的类
        :param id_: sqla的类的ID, 表的ID
        :param data_key:字段名列表 :[]
        :param data_value:值,与字段名对应 :[[]]
        :return:
        """
        if data_key is None:
            data_key = self.get_model_columns(class_, language='en')
        d = None
        for i in range(0, 1):
            d = dict(zip(data_key, data_value[i]))
        session = Session(self.engine)
        if 'sqlite' in self.uri:  # 如果是sqlite数据库,需要执行启用外键语句
            session.execute("PRAGMA foreign_keys=ON")
        session.query(class_).filter(class_.id == id_).\
            update(d, synchronize_session=False)
        session.commit()
        session.close()
        return id_

    def execute(self, sql):
        """
        执行SQL语句
        :param sql:
        :return:
        """
        session = Session(self.engine)
        try:
            session.execute(sql)
        except Exception as e:
            return False, str(e)
        finally:
            session.commit()
            session.close()
        return True, '执行成功!'

    def execute_to_table(self, sql):
        """
        执行sql返回表
        :param sql:
        :return:
        """
        # 注意如果是mysql数据库不能使用服务端游标进行查询
        # 如果是mysql数据库,这里不使用带服务端游标的engine进行查询
        if 'mysql' in self.uri:
            engine = sqla.create_engine(self.uri)
        else:
            engine = self.engine
        session = Session(engine)
        try:
            ll = list(session.execute(sql))
            return True, ll
        except Exception as e:
            return False, str(e)
        finally:
            session.commit()
            session.close()

    def execute_to_table_header(self, sql, chunksize=0):
        """
        执行sql返回表
        :param sql:
        :param chunksize: 返回行数，0表示不限制
        :return:
        """
        # 注意如果是mysql数据库不能使用服务端游标进行查询
        # 如果是mysql数据库,这里不使用带服务端游标的engine进行查询
        if 'mysql' in self.uri:
            engine = sqla.create_engine(self.uri)
        else:
            engine = self.engine
        session = Session(engine)
        try:
            res = session.execute(sql)
            header = []
            for k in res.keys():
                header.append(k.encode('utf-8').decode('utf-8'))
            if chunksize != 0:
                res = res.fetchmany(chunksize)
            ll = [header] + list(res)
            return True, ll
        except Exception as e:
            return False, str(e)
        finally:
            session.commit()
            session.close()

    def delete_table_data(self, table_name, parameter_dict):
        """
        根据参数字典删除目标表的数据
        :param table_name: 目标表名称
        :param parameter_dict: 参数字典
        :return:
        """
        # metadata = sqla.MetaData()
        # table = sqla.Table(table_name, metadata, autoload=True, autoload_with=self.engine)
        # del_obj = table.delete()
        # for k, v in parameter_dict.items():
        #     value = v.split()
        #     del_obj = del_obj.where(table.c.get(k).in_(value))
        del_obj = 'delete {} where 1 = 1'.format(table_name)
        for k, v in parameter_dict.items():
            del_obj += ' and {} in ({})'.format(k, v)
        session = Session(self.engine)
        try:
            rc = session.execute(del_obj).rowcount
        except Exception as e:
            return False, str(e)
        finally:
            session.commit()
            session.close()
        return True, rc

    def get_table_columns(self, table_name):
        """
        获取engine的table_name表的字段属性
        :param table_name: 表的名称
        :return: table_name表中字段属性
        """
        insp = reflection.Inspector.from_engine(self.engine)
        try:
            colums = insp.get_columns(table_name)  # 这里是写的表名
            column_list = []
            for i, c in enumerate(colums):
                column_dict = dict()
                column_dict['id'] = i
                column_dict['name'] = c['name'].encode('utf-8').decode('utf-8')
                column_dict['type'] = str(c['type'])
                column_list.append(column_dict)
            return column_list
        except Exception as e:
            print(e)
            return []


# 数据库类型字典
database_type_dict = {
    0: ('MySQL', 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'),
    1: ('Oracle', 'oracle+cx_oracle://{}:{}@{}:{}/{}'),
    2: ('SqlServer', 'mssql+pymssql://{}:{}@{}:{}/{}')
    }


# def get_local_database():
#     """
#     获取本地数据库实例
#     :return:
#     """
#     db = get_sqlite3_db()
#     filter_dict = {models.DataBase.local_database: 1}
#     local_database = db.select_table(models.DataBase, None, filter_dict)
#     if len(local_database) == 0:
#         return None
#     ip_address = local_database[0][2]
#     username = local_database[0][3]
#     password = local_database[0][4]
#     schema = local_database[0][5]
#     port = local_database[0][6]
#     database_type = local_database[0][7]
#     local_db = DataBase(ip_address=ip_address, username=username, password=password,
#                         schema=schema, port=port, database_type=database_type)
#     return local_db


# def get_database(database_id):
#     """
#     获取数据库实例
#     :param database_id: models.DataBase.id  数据库信息表的ID
#     :return:
#     """
#     db = get_sqlite3_db()
#     database = db.select_table(models.DataBase, database_id)
#     ip_address = database[0][2]
#     username = database[0][3]
#     password = database[0][4]
#     schema = database[0][5]
#     port = database[0][6]
#     database_type = database[0][7]
#     db = DataBase(ip_address=ip_address, username=username, password=password,
#                   schema=schema, port=port, database_type=database_type)
#     return db


def get_sqlite3_db():
    sqlite3_path = 'sqlite:{}'.format('///../flymouse.db')
    db = DataBase(database_type=3, sqlite3_path=sqlite3_path)
    db.init_database()
    return db


def get_test_db():
    # 'sqlite+pysqlcipher3://:testing@/foo.db'
    import os
    sqlite3_path = 'sqlite:{}'.format(f'///{basePath}/aa.db')
    # sqlite3_path = 'sqlite+pysqlcipher://:testing@/foo.db'
    print(os.path.abspath(sqlite3_path))
    db = DataBase(database_type=3, sqlite3_path=sqlite3_path)
    db.init_database()
    return db


def main():
    pass
    # from sqlalchemy.engine.url import URL
    # import mmap
    #
    # # f = open('aa.db', 'rb+')
    # # m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
    # with open('aa.db', 'rb+') as f:
    #     data = f.read()
    # url = URL('sqlite', database=data)
    # engine = sqla.create_engine(url)
    # Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()

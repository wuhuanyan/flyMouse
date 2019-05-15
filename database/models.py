from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, BOOLEAN

Base = declarative_base()


class Script(Base):
    """
    脚本表
    这里涉及到的方法,其他的model都需要重写
    """
    __tablename__ = 't_script'
    id = Column(Integer, primary_key=True)  # 主键
    sort = Column(Integer, unique=False, nullable=True)  # 运行顺序
    command = Column(TEXT, unique=False, nullable=True)  # 脚本内容
    remark = Column(String(100), unique=False, nullable=True)  # 备注
    enable = Column(BOOLEAN, unique=False, nullable=True)  # 是否启用

    @staticmethod
    def get_columns(language='cn'):
        """
        获取中文|英文字段名称的列表
        :param language:'en' 英文,'cn' 中文
        :return:
        """
        if language == 'en':
            return ['id', 'sort', 'command', 'remark', 'enable']
        elif language == 'cn':
            return ['ID', '运行顺序', '脚本内容', '备注', '是否启用']

    def __init__(self, dict1):
        for k, v in dict1.items():
            setattr(self, k, v)

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.__tablename__


def main():
    pass


if __name__ == '__main__':
    main()

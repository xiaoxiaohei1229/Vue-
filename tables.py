#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by Oscar White
# at 2017-10-12
# ver 0.1

from peewee import *
from flask_peewee.auth import BaseUser
from flask_login import UserMixin
import datetime
import ConfigParser

# 解析配置文件函数


def parse_config(args, section="General", filename="config.ini"):
    try:
        config = ConfigParser.ConfigParser()
        config.read(filename)
        r = config.get(section, args)
    except BaseException, e:
        print e
    else:
        return r


# 指定配置文件
CONFIG_FILE = "conf/config.ini"

# 读取配置文件内容

DB_TYPE = parse_config("DB_TYPE", "DataBase", CONFIG_FILE)

# MYSQL 类型
if str(DB_TYPE) == "0":
    DB_HOST = parse_config('DB_HOST', 'DataBase', CONFIG_FILE)
    DB_PORT = parse_config('DB_PORT', 'DataBase', CONFIG_FILE)
    DB_USER = parse_config('DB_USER', 'DataBase', CONFIG_FILE)
    DB_PASSWORD = parse_config('DB_PASSWORD', 'DataBase', CONFIG_FILE)
    DB_NAME = parse_config('DB_NAME', 'DataBase', CONFIG_FILE)
    db = MySQLDatabase(DB_NAME, **{
        'host': DB_HOST,
        'password': DB_PASSWORD,
        'port': int(DB_PORT),
        'user': DB_USER})
# SQLITE 类型
elif str(DB_TYPE) == "1":
        # 数据库名称
    DB_NAME = parse_config('DB_NAME', 'DataBase', CONFIG_FILE)
    DATABASE_NAME = DB_NAME + ".db"
    db = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):

    class Meta:
        database = db

    @classmethod
    def getOne(cls, *query, **kwargs):
        # 为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None


class Vendors(BaseModel):
    vendor_name = CharField(max_length=128, null=False)
    model_type = CharField(max_length=128, null=False)
    comment = TextField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class City(BaseModel):
    city_name = CharField(max_length=128, null=False)
    city_tag = CharField(max_length=128, null=False)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class Devices(BaseModel):
    area = ForeignKeyField(City, related_name='city2area')
    dev_name = CharField(max_length=128, null=False)
    dev_ip = CharField(max_length=128, null=False)
    dev_type = CharField(max_length=128, null=False)
    login_type = IntegerField()
    vendor_id = ForeignKeyField(Vendors, related_name='dev2vendor')
    login_user = CharField(max_length=64, null=False)
    login_password = CharField(max_length=64, null=False)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class Batch(BaseModel, BaseUser):
    dev_id = ForeignKeyField(Devices, related_name='batch2dev')
    status = IntegerField(default=0)
    create_time = DateTimeField(default=datetime.datetime.now)


# class Interfaces(BaseModel):
#     dev_id = ForeignKeyField(Devices, related_name="int2dev")
#     interface_name = CharField(max_length=128, null=False)
#     interface_desc = CharField(max_length=256, null=False)
#     create_time = DateTimeField(default=datetime.datetime.now)
#     update_time = DateTimeField(default=datetime.datetime.now)


class DevSysInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='sysinfo2batch')
    dev_id = ForeignKeyField(Devices, related_name='sys_info2dev')
    cpu_usage = IntegerField()
    mem_usage = IntegerField()
    power_stat = IntegerField()
    fru_stat = IntegerField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class DevInterfaceInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='intinfo2batch')
    dev_id = ForeignKeyField(Devices, related_name='if2dev')
    interface_name = CharField(max_length=128, null=False)
    interface_desc = CharField(max_length=256, null=False)
    bandwidth = FloatField(default=1)
    int_stat = IntegerField()
    range_stat = CharField() # rx 光功率数值
    in_usage = FloatField()
    out_usage = FloatField()
    in_err = IntegerField()
    out_err = CharField() # 出向错报数不统计，改为 tx 光功率数值
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class DevBGPInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='bgpinfo2batch')
    dev_id = ForeignKeyField(Devices, related_name='bgp2dev')
    bgp_ip = CharField(max_length=128, null=False)
    bgp_as = CharField(max_length=128, null=False)
    bgp_stat = CharField(max_length=128, null=False)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class DevISISInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='isisinfo2batch')
    dev_id = ForeignKeyField(Devices, related_name='isis2dev')
    peer_name = CharField(max_length=128, null=False)
    local_int = CharField(max_length=128, null=False)
    isis_stat = CharField(max_length=128, null=False)
    isis_type = CharField(max_length=128, null=False)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class DevLDPInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='ldpinfo2batch')
    dev_id = ForeignKeyField(Devices, related_name='ldp2dev')
    ldp_neighbor = CharField(max_length=128, null=False)
    ldp_stat = CharField(max_length=128, null=False)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class User(BaseModel, BaseUser, UserMixin):
    username = CharField()
    password = CharField()
    email = CharField(default="admin@example.com")
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)
    phone = IntegerField(default=13800138000)
    desc = TextField(default="None")


class DevConfigs(BaseModel):
    dev_id = ForeignKeyField(Devices, related_name="config2dev")
    backup_name = CharField(max_length=128, null=False)
    context = TextField()
    tips = TextField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class CollectionScheduler(BaseModel):
    dev_id = ForeignKeyField(Devices, related_name="scheduler2dev")
    schedule_type = IntegerField(default=0)
    cycle_tag = CharField()
    appoint_date = DateTimeField()
    appoint_time = TimeField()
    devsysinfo = IntegerField(default=0)
    devinterfaceinfo = IntegerField(default=0)
    devprotocolinfo = IntegerField(default=0)
    devalarminfo = IntegerField(default=0)
    devnatpoolinfo = IntegerField(default=0)
    devroutingtableinfo = IntegerField(default=0)
    devconfiginfo = IntegerField(default=0)
    devinterfacecount = IntegerField(default=0)
    comment = TextField()
    create_time = DateTimeField(default=datetime.datetime.now)

class DevNATPoolInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='natpool2batch')
    dev_id = ForeignKeyField(Devices, related_name='natpool2dev')
    pool_name = CharField()
    vpn_instance = CharField()
    gateway = CharField()
    mask = CharField()
    total = IntegerField(default=0)
    used = IntegerField(default=0)
    free = IntegerField(default=0)
    disable = IntegerField(default=0)
    create_time = DateTimeField(default=datetime.datetime.now)

class DevRoutingTableInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='route2batch')
    dev_id = ForeignKeyField(Devices, related_name='route2dev')
    protocol = CharField()
    total = IntegerField(default=0)
    active = IntegerField(default=0)
    create_time = DateTimeField(default=datetime.datetime.now)

class DevAlarmInfo(BaseModel):
    batch_id = ForeignKeyField(Batch, related_name='alarm2batch')
    dev_id = ForeignKeyField(Devices, related_name='alarm2dev')
    timestamp = CharField()
    alarminfo = TextField(default="")
    create_time = DateTimeField(default=datetime.datetime.now)

class DevInterfaceCount(BaseModel):
    batch_id = ForeignKeyField(Batch,related_name='count2batch')
    dev_id =ForeignKeyField(Devices, related_name='count2dev')
    create_time = DateTimeField(default=datetime.datetime.now)
    count_100ge_up = IntegerField(default=0) 
    count_100ge_down = IntegerField(default=0) 
    total_100ge = IntegerField(default=0) 
    count_10ge_up = IntegerField(default=0) 
    count_10ge_down = IntegerField(default=0) 
    total_10ge = IntegerField(default=0) 
    count_1ge_up = IntegerField(default=0) 
    count_1ge_down = IntegerField(default=0) 
    total_1ge = IntegerField(default=0) 
    



if __name__ == '__main__':
    # 建表操作
    tables = ('Vendors',
              'City',
              'Devices',
              'Batch',
              'DevSysInfo',
              'DevInterfaceInfo',
              'DevBGPInfo',
              'DevISISInfo',
              'DevLDPInfo',
              'User',
              'DevConfigs',
              'CollectionScheduler',
              'DevRoutingTableInfo',
              'DevAlarmInfo',
              'DevNATPoolInfo',
              'DevInterfaceCount'
              )

    print "--- Create Tables ---"
    for table in tables:
        try:
            eval(table + '.create_table()')
        except Exception, e:
            print e[1]
        else:
            print "Table '" + table + "' is created"
    print "--- Table created successfuly ---"
    # 建立管理员用户
    User.create(username="admin", password="admin", email="admin@example.com")
    print "--- Create Admin User ---"
    try:
        user_get = User.get(username="admin")
        user_get.set_password("admin")
        user_get.save()
    except Exception, e:
        print e
    else:
        print "--- Admin User created successfuly ---"

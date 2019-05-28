#!/usr/bin/env python3
# --*-- coding:utf-8 --*--
# __Author__ Aaron


from datetime import datetime, timedelta


class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.blacked = False

        data_str, time_str = self.expire_str.split(' ')
        year, month, day = data_str.split("-")
        hour, minute, second = time_str.split(":")
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                                    second=int(second))  # 把ip过期时间（如：“2019-1-10 12:20:45”）转成时间模式

        # https://ip:prot
        self.proxy = "https://{}:{}".format(self.ip, self.proxy)

    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=5): #seconds=5 5s后过期
            return True
        else:
            return False

# encoding: utf-8

import math
import gconf


class PageList(object):
    # 默认分页大小
    _default_page_size = gconf.PAGESIZE
    # 最大页数
    _max_page_select = 5

    @classmethod
    def create_pagelist(cls, pagenum, pagesize, totalnum):
        # 分页大小
        _page_size = int(pagesize) if str(pagesize).isdigit() else cls._default_page_size
        _page_size = cls._default_page_size if int(_page_size) < 5 or int(_page_size) > 50 else _page_size
        # 总页数
        _max_page_num = int(math.ceil(totalnum * 1.0 / _page_size))
        # 当前页
        _page_num = int(pagenum) if str(pagenum).isdigit() else 1
        _page_num = 1 if _page_num < 1 or _page_num > _max_page_num else _page_num
        # DB偏移量
        _offset = (_page_num - 1) * _page_size
        # 结束页码
        _end_page_num = _page_num + 2
        _end_page_num = _end_page_num if _end_page_num < _max_page_num and _max_page_num > cls._max_page_select \
            else _max_page_num
        _end_page_num = cls._max_page_select if _max_page_num > cls._max_page_select > _end_page_num else _end_page_num
        # 起始页码
        _start_page_num = _end_page_num - 4
        _start_page_num = 1 if _end_page_num <= cls._max_page_select else _start_page_num

        return cls(_page_num, _page_size, totalnum, _max_page_num, _start_page_num, _end_page_num), _offset

    def __init__(self, pagenum, pagesize, totalnum, maxpagenum, startpagenum, endpagepum):
        self.pageNum = pagenum
        self.pageSize = pagesize
        self.totalNum = totalnum
        self.maxPageNum = maxpagenum
        self.startPageNum = startpagenum
        self.endPageNum = endpagepum

    def set_contents(self, contents=[]):
        self.contents = contents

    def __str__(self):
        return str(self.__dict__)

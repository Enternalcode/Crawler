# -*- coding:utf-8 -*-
import re


# 处理月薪函数,返回平均值
from qcwy.settings import logger


def convert_salary(str_salary):
    """
    提取薪酬当中的数字信息对信息进行换算，并去掉符号
    然后分别放置到item[salary]、item[salary_min]、item[salary_max]
    方便以后做表格取用
    换算标准：千/月、 float类型 
    """

    try:
        # 正则提取薪酬数字
        comp = re.compile('(\d\.?\d?)')
        salary_list = comp.findall(str_salary)
        # 初始化局部变量，减少在if else语句中的重定义；便于函数返回
        # None为空类型， 可以赋值任意类型数据
        salary_min = None
        salary_max = None
        if '千/月' in str_salary:
            # print(type(salary_list))
            salary = str(float(salary_list[0])) + '-' + str(float(salary_list[1]))
            salary_min = float(salary_list[0])
            salary_max = float(salary_list[1])
            # print(salary, salary_min, salary_max, type(salary_list[1]))
        elif '万/月' in str_salary:
            # print(type(salary_list))
            # 此处salary_list[0]类型为'str'
            salary = str(float(salary_list[0]) * 10) + '-' + str(float(salary_list[1]) * 10)
            salary_min = float(salary_list[0]) * 10
            salary_max = float(salary_list[1]) * 10
            # print(salary, salary_min, salary_max, )
        elif '万/年' in str_salary:
            # item['salary']保存原生数据
            # 四舍五入限制小数位
            salary = str(float(salary_list[0]) * 10 / 12) + '-' + str(float(salary_list[1]) * 10 / 12)
            salary_min = round(float(salary_list[0]) * 10 / 12, 2)
            salary_max = round(float(salary_list[1]) * 10 / 12, 2)
            # print(salary, salary_min, salary_max, type(salary), type(salary_max))
        salary = (salary_max + salary_min) // 2
        return {
            'salary': salary,
        }
    except:
        logger.warning('薪酬数据出错')
        return False


# 提取城市信息
def extract_city(str_city):
    # 初始化空字符串
    city = ''
    try:
        if '-' in str_city:
            comp = re.compile('(.*?)-')
            city = comp.findall(str_city)[0]
            return city
        else:
            city = str_city
            return city
        # print(city, type(city))
    # 纯粹练习，并没有什么用
    except:
        print('城市信息出错')
        return False
    finally:
        return city


# 提取工作经验要求数字
"""
因为工作经验需求变量侧重于下限
即必须满足最少工作经验才算满足条件
故选取其中最少工作经验数字
"""


def extract_ExpNum(str_exp):
    # 初始化局部变量
    try:
        if '无' in str_exp:  # '无工作经验'
            return '无工作经验'
        else:  # 若为范围要求则取最小值
            exp_num = str_exp[0]  # 截取第一个数字
        return int(exp_num)
    except:
        logger.warning('经验要求出错')


# 提取招聘人数
def extract_recnum(str_rec):
    try:
        if '若干' in str_rec:
            return '招若干人'
        else:
            rec_num = str_rec[1]
            return int(rec_num)
    except:
        logger.warning('招聘人数出错')


# Bloom Filter算法

# 基本散列函数，将一个值经过散列运算后映射到一个m位位数组的某一位上（保证m值相同，输入不同的seed生成不同的散列函数）
# class HashMap(object):
#     # 传入种子数字seed，位数组的位数m
#     def __init__(self, m, seed):
#         self.seed = seed
#         self.m = m
#
#     def hash(self, value):
#         """
#         Hash Algorithm
#         :param value: Value
#         :return: Hash Value
#         """
#         ret = 0
#         # 通过ord()获取value每一位的ASCII码，然后进行乘加迭代，最后与m进行换位与运算，得到m位位数组的映射结果
#         for i in range(len(value)):
#             ret += ret * self.seed + ord(value[i])
#         return (self.m - 1) & ret


# Bloom Filter
# BLOOM_FILTER_HASH_NUMBER = 6
# BLOOM_FILTER_BIT = 30
#
#
# class BloomFilter(object):
#     def __init__(self, server, key, bit=BLOOM_FILTER_BIT, hash_number=BLOOM_FILTER_HASH_NUMBER):
#         """
#         Initialize BloomFilter
#         :param server: Redis server
#         :param key: BloomFilter key
#         :param hash_number: The number of hash functions
#         :param bit: m = 2 ^ bit
#         """
#         # default to 1 << 30 = 10,7374,1824 = 2^30 = 128MB, max filter (2 ^ 30) / hash_number = 1,7895, 6970 fingerprints
#         self.server = server  # Redis连接对象
#         self.key = key  # m位位数组的名称
#         self.m = 1 << bit
#         self.seeds = range(hash_number)
#         self.maps = [HashMap(self.m, seed) for seed in self.seeds]
#
#     # 判断元素是否存在
#     def exists(self, value):
#         """
#         if value exists
#         :param value: element need to be judged
#         :return: exist(0 or 1)
#         """
#         if not value:
#             return False
#         exist = 1  # 定义变量exist
#         for map in self.maps:  # 遍历所有散列函数
#             offset = map.hash(value)            # 获取映射位置
#             # getbit()方法取得该映射位置的结果，循环进行与运算。
#             # 这样只有每次getbit()得到的值为1时，最后的exist才为1(后用bool()转换为True)，
#             # 只要有一次getbit()得到的值为0，即m位位数组中有对应的0位，最后的exist就为0(后用bool()转化为False)
#             exist = exist & self.server.getbit(self.key, offset)
#         return exist
#
#     # 逐个调用self.maps中的散列函数，计算集合中的元素，得到在m位位数组中的映射位置
#     def insert(self, value):
#         """
#         Add value to bloom key
#         :param value: element need to be inserted
#         """
#         for f in self.maps:
#             offset = f.hash(value)
#             self.server.setbit(self.key, offset, 1)


if __name__ == '__main__':
    # 测试用例

    # 月薪
    # a = convert_salary('20-30万/月')
    a = convert_salary('9-17万/年')
    # a = convert_salary('9-17千/月')
    # print(a['salary']), type(a)

    # 城市
    # a = extract_city('成都-新城区')
    # a = extract_city('成都')
    # a = extract_city('asd')
    print(a, type(a))

    # 工作经验
    # a = extract_ExpNum('2年工作经验')
    # a = extract_ExpNum('2-3年工作经验')
    # print(a, type(a))

    # 提取招聘人数
    # a = extract_RecNum('招1人')
    # a = extract_RecNum('招若干人')
    # print(a)

    # Bloom Filter测试
    # conn = StrictRedis(host='localhost', port=6379, password=None)
    # bf = BloomFilter(conn, 'testbf', 5, 6)
    # bf.insert('Hello')
    # bf.insert('World')
    # result = bf.exists('Hello')
    # print(bool(result))
    # result = bf.exists('name')
    # print(bool(result))





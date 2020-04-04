import datetime
import yagmail
from conf import setting
import os
import unittest
from BeautifulReport import BeautifulReport as bf


# 方法makeCase用于读取指定用例模板，生成py文件，文件类名和文件名以yaml测试用例文件名命名，py文件中的驱动文件为yaml文件，这么一个转换
def makeCase():
    # 获取指定目录下的所有文件
    all_yaml = os.listdir(setting.YAML_PATH)
    # 读取用例模板，(就是打开文件并读取全部内容，用例模板就是python文件中的内容拷贝到txt文件中)
    base_case_str = open(setting.CASE_TEMPLATE, encoding='utf-8').read()
    # 遍历获取每一个用例文件(yaml文件)
    for yaml in all_yaml:
        # 判断是否是yml文件
        if yaml.endswith('.yaml') or yaml.endswith('.yml'):
            # 获取类名，并首字母大写
            class_name = yaml.replace('.yml', '').replace('.yaml', '').capitalize()
            # 拼接获取yaml文件的绝对路径
            file_name = os.path.join(setting.YAML_PATH, yaml)
            # 替换用例模板中%s占位符为指定的类名和路径(类名为yaml文件的文件名，路径为yaml文件的路径，该路径用于ddt驱动读取yaml文件)
            content = base_case_str % (class_name, file_name)
            # 拼接python文件的绝对路径，并将替换占位符之后的用例模板写入到文件并指定以py为文件后缀
            py_file_name = os.path.join(setting.CASE_PATH, class_name)
            open('%s.py' % py_file_name, 'w', encoding='utf-8').write(content)


# 运行所有测试，生成测试报告并返回成功和失败的个数以及测试报告的绝对路径(用于发邮件附件)
def run_all_case():
    # 获取测试套件
    suite = unittest.TestSuite()
    # 加载指定路径下所有以py为后缀的测试文件
    all_py = unittest.defaultTestLoader.discover(setting.CASE_PATH, '*.py')
    # 列表生成式，遍历这些文件添加到测试组件中
    [suite.addTests(py) for py in all_py]
    # 实例化一个BeautifulReport,基于这个测试套件
    run = bf(suite)
    today = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    title = '%s_接口测报告.html' % today
    # 拼接存储测试报告的路径
    report_abs_path = os.path.join(setting.REPORT_PATH, title)
    # 运行测试套件中的所以测试，并生成测试报告
    run.report(title, filename=title, log_path=setting.REPORT_PATH)
    # 返回执行测试成功和失败的数量一级测试报告的绝对路径
    return run.success_count, run.failure_count, report_abs_path


# 发送邮件的方法
def sendmail(title, content, attrs=None):
    m = yagmail.SMTP(host=setting.MAIL_HOST,
                     user=setting.MAIL_USER
                     , password=setting.MAIL_PASSWRD
                     )
    m.send(to=setting.TO,
           subject=title,
           contents=content,
           attachments=attrs)

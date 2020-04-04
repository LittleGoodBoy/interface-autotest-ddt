import os, sys
import datetime

'''
    配置项目环境变量,用于各个模块之间的调用,系统可用找到对应的模块位置
'''
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from lib import tools

'''
	主函数,自动化测试启动函数
		执行测试,并发送测试报告,将相应的测试用例执行之后记录通过与否
'''


def main():
    # 自动产生python文件
    tools.makeCase()
    # 运行用例
    pass_count, fail_count, abs_path = tools.run_all_case()

    # 邮件内容
    msg = '''
	        各位好！
		        本次接口测试结果如下：
			        通过用例：%s条
			        失败用例：%s条
			        详细信息见附件【%s】。
	    ''' % (pass_count, fail_count, os.path.basename(abs_path))
    # 当前日期的指定格式字符串
    today = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    # 邮件标题
    title = '接口测试报告_%s' % today
    # 发送邮件
    tools.sendmail(title, msg, abs_path)


# 指定该py文件默认调main方法，也就是当前文件是可执行文件
main()

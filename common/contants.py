import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
case_file = os.path.join(base_dir,'data','cases11111.xlsx')
# print(case_file)
global_conf_file = os.path.join(base_dir,'config','global.conf')
# print(global_conf_file)
online_conf_file = os.path.join(base_dir,'config','online.conf')
# print(online_conf_file)
test_conf_file = os.path.join(base_dir,'config','test.conf')
# print(test_conf_file)
log_dir = os.path.join(base_dir,'log')

case_dir = os.path.join(base_dir,'testcases')

report_dir = os.path.join(base_dir,'reports')
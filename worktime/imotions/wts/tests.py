from django.test import TestCase
from common.db import DB
# Create your tests here.


def test():
    start_time = '2021-05-01 00:00:00.000000'    # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
    end_time = '2021-06-01 00:00:00.000000'
    params= [start_time, end_time]
    db = DB()
    conn = db.get_connection("wjtech")
    sql = """
    SELECT m_main_department_preset_working_hours FROM wjtech.m_main_department where m_main_department_preset_start_at>= '{0}' and m_main_department_preset_end_at <= '{1}'

    """
    sql_main = sql.format(start_time, end_time)
    print(sql_main)

    cursor = conn.cursor()
    data = cursor.execute(sql_main)

    data_departments = cursor.fetchall()
    print(data_departments)
    s = 0
    for data_cont in data_departments:
        for data_cont_str in data_cont:
            s+= int(data_cont_str)

    print(s)





    db.close_connection(conn)
    # if len(data_departments) != 0:
    #     s = 0
    #     for data_department in data_departments:
    #         data_list = data_department[-1]
    #         data_dep = data_department[0]
    #         data_lists = data_list.split(',')
    #         for hour in data_lists:
    #             s = s + int(float(hour))
    #         department_dict_time[data_dep] = s
    #     print(department_dict_time)
    #     company_list = department_dict_time.values()
    #     wjtech_dict['无界工场(上海)设计科技有限公司'] = sum(company_list)
    #     print(wjtech_dict)
    #     company_worktime_dict.update(wjtech_dict)
    # else:
    #     wjtech_dict['无界工场(上海)设计科技有限公司'] = 0
    #     company_worktime_dict.update(wjtech_dict)
test()
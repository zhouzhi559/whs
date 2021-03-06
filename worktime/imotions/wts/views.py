from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import json
from common.get_companys import get_company_list
import logging
from pymysql import connect
from common.db import DB
import requests

logger = logging.getLogger(__name__)

# Create your views here.

class RedisView(View):

    """
    带参数的sql语句执行函数

    """

    def execute_sql(self, conn, sql, params):
        try:
            sql = sql.lstrip()  # 去sql语句左边空格
            typeName = sql[0]  # 取sql第1个字母判断执行指令：select\insert\update\delete
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if typeName == 'i' or typeName == 'I':
                conn.commit()
                return typeName
            elif typeName == 'd' or typeName == 'D':
                conn.commit()
                return typeName
            elif typeName == 'u' or typeName == 'U':
                conn.commit()
                return typeName
            elif typeName == 's' or typeName == 'S':
                rows = cursor.fetchall()
                logger.info("company worktime get data is ok :%s" % str(rows))
                return rows
        except Exception as e:
            logger.error("company worktime get data is not ok %s" % e)

            return "error"



    """
    得到所有公司在哪一时间段的工时，以json的形式返回，例如：{'时新(上海)产品设计有限公司': 22475}
    """

    def get_company_worktime(self, start_time, end_time):

        try:

            company_worktime_dict = {}
            department_dict_time = {}

            # list_company = tuple()
            start_time = start_time
            end_time = end_time

            # start_time = '2021-05-01 00:00:00.000000'    # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            # end_time = '2021-06-01 00:00:00.000000'       # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            params = [start_time, end_time]
            db = DB()
            companys = get_company_list()
            company_list = companys.get_all_databases()

            for data_company in company_list:

                if data_company == "imotion":
                    imotion_dict = {}
                    conn = db.get_connection("imotion")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM imotion.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        department_dict_time['imotion'] = s
                        imotion_dict['时新(上海)产品设计有限公司'] = s
                        print(imotion_dict)
                        company_worktime_dict.update(imotion_dict)
                        print(company_worktime_dict)

                    else:
                        imotion_dict['时新(上海)产品设计有限公司'] = 0
                        company_worktime_dict.update(imotion_dict)

                    # print(company_worktime_dict)
                    #
                    # return company_worktime_dict

                if data_company == "software":
                    software_dict = {}
                    conn = db.get_connection("software")

                    sql = """
                        SELECT 
                        m_main_department_preset_working_hours FROM software.m_main_department 
                        where m_main_department_preset_start_at >= '{0}' 
                        and m_main_department_preset_end_at <= '{1}'            
                    """
                    sql = sql.format(start_time, end_time)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        department_dict_time['software'] = s

                        print(department_dict_time)
                        software_dict['无界工场(上海)软件科技有限公司'] = s
                        print(software_dict)
                        company_worktime_dict.update(software_dict)
                    else:
                        software_dict['无界工场(上海)软件科技有限公司'] = 0
                        company_worktime_dict.update(software_dict)

                if data_company == "wjtech":
                    wjtech_dict = {}
                    conn = db.get_connection("wjtech")
                    sql = """
                    SELECT
                    m_main_department_preset_working_hours
                    FROM wjtech.m_main_department where m_main_department_preset_start_at >= '{0}'
                    and m_main_department_preset_end_at <= '{1}'
                    
                    """
                    sql = sql.format(start_time, end_time)

                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s +=int(float(data_department_str))

                        department_dict_time['wjtech'] = s

                        print(department_dict_time)
                        wjtech_dict['无界工场(上海)设计科技有限公司'] = s
                        print(wjtech_dict)
                        company_worktime_dict.update(wjtech_dict)
                    else:
                        wjtech_dict['无界工场(上海)设计科技有限公司'] = 0
                        company_worktime_dict.update(wjtech_dict)

                if data_company == "pawithub":
                    pawithub_dict = {}
                    conn = db.get_connection("pawithub")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                     FROM pawithub.m_main_department where m_main_department_preset_start_at >= '{0}' 
                     and m_main_department_preset_end_at <= '{1}'              
                    """
                    sql = sql.format(start_time, end_time)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s +=int(float(data_department_str))

                        department_dict_time['pawithub'] = s
                        pawithub_dict['上海慧瞰科技有限公司'] = s
                    #     print(pawithub_dict)
                        company_worktime_dict.update(pawithub_dict)
                    else:
                        pawithub_dict['上海慧瞰科技有限公司'] = 0
                        company_worktime_dict.update(pawithub_dict)

                if data_company == "wjchin":
                    wjchin_dict = {}
                    conn = db.get_connection("wjchin")
                    sql = """
                    SELECT m_main_department_preset_working_hours 
                    FROM wjchin.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'
                    """
                    sql = sql.format(start_time, end_time)
                    data_departments = db.execute_sql(conn, sql)
                    print("***")
                    print(data_departments)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s +=int(float(data_department_str))

                        department_dict_time['wjchin'] = s
                        wjchin_dict['无界国创（成都）科技有限公司'] = s
                        print(wjchin_dict)
                        company_worktime_dict.update(wjchin_dict)
                    else:
                        wjchin_dict['无界国创（成都）科技有限公司'] = 0
                        company_worktime_dict.update(wjchin_dict)

                if data_company == "wjip":
                    wjip_dict = {}
                    conn = db.get_connection("wjip")
                    sql = """
                    SELECT m_main_department_preset_working_hours 
                    FROM wjip.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'
                    """
                    sql = sql.format(start_time, end_time)
                    data_departments = db.execute_sql(conn, sql)
                    print("***")
                    print(data_departments)
                    db.close_connection(conn)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        department_dict_time['wjip'] = s
                        wjip_dict['无界工场（上海）知识产权服务有限公司'] = s
                        print(wjip_dict)
                        company_worktime_dict.update(wjip_dict)
                    else:
                        wjip_dict['无界工场（上海）知识产权服务有限公司'] = 0
                        company_worktime_dict.update(wjip_dict)

            print(company_worktime_dict)

            logger.info("get company all worktime successful:%s" % str(company_worktime_dict))

            return company_worktime_dict

        except Exception as e:

            logger.error("this run has error: %s" % e)

            return "error"

    def get(self, request):
        """处理GET请求，查询"""

        start_time = request.GET.get("startTime")
        # print(type(start_time))
        # start_time = str(start_time)
        # print(start_time)
        # print(type(start_time))
        end_time = request.GET.get("endTime")
        # print(start_time)
        # print(end_time)

        data = self.get_company_worktime(start_time, end_time)

        if data != "error":

            data = json.dumps(data)

            logger.info("respose data is ok %s " % data)

        return HttpResponse(data)


class ReadProject(View):

    def execute_sql(self, conn, sql, params):

        try:
            sql = sql.lstrip()  # 去sql语句左边空格
            typeName = sql[0]  # 取sql第1个字母判断执行指令：select\insert\update\delete
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if typeName == 'i' or typeName == 'I':
                conn.commit()
                return typeName
            elif typeName == 'd' or typeName == 'D':
                conn.commit()
                return typeName
            elif typeName == 'u' or typeName == 'U':
                conn.commit()
                return typeName
            elif typeName == 's' or typeName == 'S':
                rows = cursor.fetchall()

                logger.info("sql get data is :%s" % str(rows))
                return rows
        except Exception as e:

            logger.error("sql get data is not successful:%s" % e)
            return "error"

    def get_project_worktime(self):

        try:
            start_time = '2021-02-01 00:00:00.000000'    # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            end_time = '2021-06-01 00:00:00.000000'
            params = [start_time, end_time]
            company_project_worktime = {}

            # company_list = ['software', 'imotion', 'wjtech', 'pawithub', 'wjchin', 'wjip']

            db = DB()
            companys = get_company_list()
            company_list = companys.get_all_databases()
            for company in company_list:
                if company == "imotion":
                    imotion_pro_dict = {}
                    conn = db.get_connection("imotion")
                    sql = """
                            SELECT project_id,project_name FROM imotion.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("imotion")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM imotion.m_main where m_m_project_id = "{0}" and
                          m_main_preset_start_at >= "{1}" and
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM imotion.m_main_department where m_main_code = '{0}'
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in imotion_pro_dict.keys():
                                        imotion_pro_dict[project_ids[1]] = s
                                    else:
                                        imotion_pro_dict[project_ids[1]] = s + int(imotion_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(imotion_pro_dict)

                    company_project_worktime['imotion'] = imotion_pro_dict

                if company == "software":
                    software_pro_dict = {}
                    conn = db.get_connection("software")
                    sql = """
                            SELECT project_id,project_name FROM software.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("software")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM software.m_main where m_m_project_id = "{0}" and 
                          m_main_preset_start_at >= "{1}" and 
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM software.m_main_department where m_main_code = '{0}' 
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in software_pro_dict.keys():
                                        software_pro_dict[project_ids[1]] = s
                                    else:
                                        software_pro_dict[project_ids[1]] = s + int(software_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(software_pro_dict)

                    company_project_worktime['software'] = software_pro_dict

                if company == "wjtech":
                    wjtech_pro_dict = {}
                    conn = db.get_connection("wjtech")
                    sql = """
                            SELECT project_id,project_name FROM wjtech.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("wjtech")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM wjtech.m_main where m_m_project_id = "{0}" and 
                          m_main_preset_start_at >= "{1}" and 
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM wjtech.m_main_department where m_main_code = '{0}' 
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in wjtech_pro_dict.keys():
                                        wjtech_pro_dict[project_ids[1]] = s
                                    else:
                                        wjtech_pro_dict[project_ids[1]] = s + int(wjtech_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(wjtech_pro_dict)

                    company_project_worktime['wjtech'] = wjtech_pro_dict

                if company == "pawithub":
                    pawithub_pro_dict = {}
                    conn = db.get_connection("pawithub")
                    sql = """
                            SELECT project_id,project_name FROM pawithub.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("pawithub")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM pawithub.m_main where m_m_project_id = "{0}" and 
                          m_main_preset_start_at >= "{1}" and 
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM pawithub.m_main_department where m_main_code = '{0}' 
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in pawithub_pro_dict.keys():
                                        pawithub_pro_dict[project_ids[1]] = s
                                    else:
                                        pawithub_pro_dict[project_ids[1]] = s + int(pawithub_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(pawithub_pro_dict)

                    company_project_worktime['pawithub'] = pawithub_pro_dict

                if company == "wjchin":
                    wjchin_pro_dict = {}
                    conn = db.get_connection("wjchin")
                    sql = """
                            SELECT project_id,project_name FROM wjchin.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("wjchin")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM wjchin.m_main where m_m_project_id = "{0}" and 
                          m_main_preset_start_at >= "{1}" and 
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM wjchin.m_main_department where m_main_code = '{0}' 
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in wjchin_pro_dict.keys():
                                        wjchin_pro_dict[project_ids[1]] = s
                                    else:
                                        wjchin_pro_dict[project_ids[1]] = s + int(wjchin_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(wjchin_pro_dict)

                    company_project_worktime['wjchin'] = wjchin_pro_dict

                if company == "wjip":
                    wjip_pro_dict = {}
                    conn = db.get_connection("wjip")
                    sql = """
                            SELECT project_id,project_name FROM wjip.project_info
                        """

                    project_id_names = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    print(project_id_names)
                    conn = db.get_connection("wjip")

                    for project_ids in project_id_names:
                        # for project_id in project_ids:
                        sql_main1 = """
                          SELECT m_main_code FROM wjip.m_main where m_m_project_id = "{0}" and 
                          m_main_preset_start_at >= "{1}" and 
                          m_main_preset_end_at <= "{2}"
                        """
                        print(project_ids[0])
                        print(type(project_ids[0]))
                        sql_main = sql_main1.format(project_ids[0], start_time, end_time)
                        print("----------------")
                        print(sql_main)
                        # print(sql_main)

                        project_code = db.execute_sql(conn, sql_main)

                        if len(project_code) != 0:
                            for m_main_code in project_code:
                                for main_code_str in m_main_code:
                                    print("======")
                                    print(project_ids[0])
                                    print(main_code_str)
                                    sql_code = """
                                        SELECT m_main_department_preset_working_hours FROM wjip.m_main_department where m_main_code = '{0}' 
                                        """
                                    sql = sql_code.format(main_code_str)
                                    project_time = db.execute_sql(conn, sql)
                                    s = 0
                                    for one_code_time_tuple in project_time:
                                        for one_code_time in one_code_time_tuple:
                                            s += int(float(one_code_time))
                                    if project_ids[1] not in wjip_pro_dict.keys():
                                        wjip_pro_dict[project_ids[1]] = s
                                    else:
                                        wjip_pro_dict[project_ids[1]] = s + int(wjip_pro_dict[project_ids[1]])
                    db.close_connection(conn)
                    print("-------")
                    print(wjip_pro_dict)

                    company_project_worktime['wjip'] = wjip_pro_dict

                    logger.info("project time get data is ok %s"% str(company_project_worktime))

                    return company_project_worktime

        except Exception as e:

            logger.error("project get data is error %s"% e)

            return "error"



    def get(self, request):

        data = self.get_project_worktime()
        data_test = {"message": "ok"}

        if data != "error":
            data = json.dumps(data)
            logger.info("response data successful::::%s"% data)
        else:
            logger.error("response data not successful %s")

        return HttpResponse(data)



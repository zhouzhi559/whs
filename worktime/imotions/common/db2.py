from common.db import DB



#  数据库的相关参数

host = "10.0.0.103"
user = 'imds'
password = 'imotionflow'
# database = 'zhitest'


class db:
    # connect mysql  连接数据库函数

    def get_connect_db(self):
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password
                               )
        # cursor = conn.cursor()

        return conn
    # get databases  得到mysql里面所有的数据库

    def get_all_databases(self):
        cursor = self.get_connect_db()    #连接mysql
        con = cursor.cursor()             # 游标
        cont = con.execute("show databases")  # 数据库的个数
        result = con.fetchall()               # 得到所有的数据库
        cursor.close()
        con.close()
        return result



db = db()

class get_data:


    def handle_database(self):
        """
        得到各个公司的工时数，以字典的形式输出
        

        
        """
        company_worktime_dict = {}
        start_time = '2021-05-01 00:00:00.000000'    # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
        end_time = '2021-06-01 00:00:00.000000'       # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
        params = [start_time,end_time]               # sql里面的定义参数

        databases = db.get_all_databases()           # 得到所有的数据库
        for database in databases:                   # 循坏数据库
            for data in database:
                if data == 'imotion':                # 选取imotion
                    cursor = db.get_connect_db()
                    conn = cursor.cursor()
                    conn_imotion = conn.execute("use imotion")
                    use_imotion = conn.fetchall()
                    print(conn_imotion)
                    print(use_imotion)
                    imoton_cont = conn.execute("show tables")
                    imoton_tables = conn.fetchall()
                    data_department_cont = conn.execute("SELECT m_main_department,m_main_department_preset_start_at,group_concat(m_main_department_preset_working_hours) FROM imotion.m_main_department where m_main_department_preset_start_at >= %s and m_main_department_preset_start_at < %s group by m_main_department",params)
                    data_departments = conn.fetchall()
                    cursor.close()
                    conn.close()
                    department_dict_time = {}
                    s = 0
                    for data_department in data_departments:
                        data_list = data_department[-1]
                        data_dep = data_department[0]
                        data_lists = data_list.split(',')
                        for hour in data_lists:
                            s= s+int(float(hour))                           
                        department_dict_time[data_dep] = s
                    print(department_dict_time)
                    company_list = department_dict_time.values()
                    company_worktime_dict['imotion'] = sum(company_list)
                    print(company_worktime_dict)
                if data == "software":
                    conn = db




get_data = get_data()
get_data.handle_database()











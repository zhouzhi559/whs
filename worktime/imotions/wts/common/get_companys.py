from db import DB

class get_company_list:
    # 从数据库里面取出imotion集团下面的所有子公司 并且以列表的形式返回
    def get_all_databases(self):
        print('start')
        _flag = "@imotion.group"
        company_list = []
        db = DB()
        conn = db.get_connection("imotionwhs")
        sql = "select companyname, suffix, mail from companyregister"
        dr = db.execute_sql(conn, sql)
        print(dr)
        print('end')

        if len(dr) > 0:
            for data in dr:
                if _flag in data[-1]:
                    company_list.append(data[1])
            print(company_list)
        return company_list

class get_all_company_worktime:

    def get_all_company_worktime(self):

        print("ooookkkk")

        return "oookkk"


 

  


# class get_company_worktimes:
#
#     def get_company_times(self):
#
#         self.get_all




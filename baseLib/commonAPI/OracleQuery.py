# https://cx-oracle.readthedocs.io/en/latest/
import cx_Oracle
from configuration import const


def sqlOne(sql):
    # sql='select id from merchant where merchant_code = \'CSSH\''
    # connector = cx_Oracle.connect('tvpay2/tvpay@172.16.219.99/sumapay')
    connector = cx_Oracle.connect(const._global_configuration().OracleConnectUri)
    curs=connector.cursor()
    curs.execute(sql)
    row=curs.fetchone()
    # print(row[0])
    curs.close()
    connector.close()
    return row

def sqlAll(sql):
    # sql='select id from merchant where merchant_code = \'CSSH\''
    # connector = cx_Oracle.connect('tvpay2/tvpay@172.16.219.99/sumapay')
    connector = cx_Oracle.connect(const._global_configuration().OracleConnectUri)
    curs=connector.cursor()
    curs.execute(sql)
    rows=curs.fetchall()
    # print(row[0])
    curs.close()
    connector.close()
    return rows

def select_table(table_name, list_view = None, where_condition = None):
    if list_view != None:
        str_view = str(list_view[0]) + ''.join([',' + str(list_view[i]) for i in range(1,len(list_view))])
    else:
        str_view = '*'
    sql = "select %s from %s where %s" %(str_view, table_name, where_condition)\
        if where_condition !=None else \
        "select %s from %s" %(str_view, table_name)
    print(sql)
    return sqlAll(sql)

# strSQL = 'select id from MERCHANT_FEE_REQUEST where merchant_id =46170 and type = 5 and status = 0 order by id desc'
# strSQL = 'select id from MERCHANT_FEE_REQUEST where merchant_id = %s and type = %s and status = %s order by id desc'%('46','5', '0')
# print(strSQL)
# print(sqlAll(strSQL)[0][0])


# # 创建数据库连接的三种方式：
# #
# # 方法一：用户名、密码和监听分开写
# db = cx_Oracle.connect('username/password@host/orcl')
# db.close()
# # 方法二：用户名、密码和监听写在一起
# db = cx_Oracle.connect('username', 'password', 'host/orcl')
# db.close()
# # 方法三：配置监听并连接
# tns = cx_Oracle.makedsn('host', 1521, 'orcl')
# db = cx_Oracle.connect('username', 'password', tns)
# db.close()



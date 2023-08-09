
import pymysql
#链接数据库
pymysql.install_as_MySQLdb()
#python3 manage.py migrate   # 创建表结构

# python3 manage.py makemigrations login  # 让 Django 知道我们在我们的模型有一些变更
# python3 manage.py migrate login   # 创建表结构
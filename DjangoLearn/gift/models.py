from django.db import models

class UserInfo(models.Model):
    """用户"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    tel = models.CharField(max_length=20, verbose_name='手机号')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    last_visit = models.DateTimeField(null=True, verbose_name='最后登录时间')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'




class Department(models.Model):
    title = models.CharField(max_length=32,verbose_name='部门名称')

class Admin(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    gender =models.IntegerField(choices=((0,'男'),(1,'女')),verbose_name='性别')
    # null=True,blank=True,表示在数据库中可以为空
    age = models.SmallIntegerField(verbose_name='年龄',blank=True, null=True)
    depart = models.ForeignKey(to='Department',on_delete=models.CASCADE,verbose_name='所属部门')

class Phone(models.Model):
    mobie = models.CharField(max_length=11,verbose_name='手机号')
    price = models.PositiveIntegerField(verbose_name='价格',default=0)
    level = models.SmallIntegerField(verbose_name="手机等级",choices=((0,'高'),(1,'中'),(2,'低')),default=2)
    status = models.BooleanField(verbose_name='状态',default=True)
    admin = models.ForeignKey(to='Admin',on_delete=models.CASCADE,verbose_name='所属管理员')


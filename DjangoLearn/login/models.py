from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateField()
    #一对多关系
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    #多对多关系
    authors = models.ManyToManyField("Author")


class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    email = models.EmailField()


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    #一对一关系
    au_detail = models.OneToOneField("AuthorDetail", on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    gender_choices = (
        (0, "女"),
        (1, "男"),
        (2, "保密"),
    )
    gender = models.SmallIntegerField(choices=gender_choices)
    tel = models.CharField(max_length=32)
    addr = models.CharField(max_length=64)
    birthday = models.DateField()

class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=64,verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    #一对多关系
    # user_type = models.ForeignKey("UserType", on_delete=models.CASCADE,verbose_name="用户类型")
    #多对多关系
    # roles = models.ManyToManyField("Role",verbose_name="角色")
class Department(models.Model):
    title = models.CharField(max_length=32,verbose_name="部门名称")
    count = models.IntegerField(verbose_name="部门人数")
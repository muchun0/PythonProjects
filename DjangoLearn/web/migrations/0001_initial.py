# Generated by Django 3.0 on 2023-08-26 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别')),
                ('age', models.SmallIntegerField(blank=True, null=True, verbose_name='年龄')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='部门名称')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobie', models.CharField(max_length=11, verbose_name='手机号')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(0, '高'), (1, '中'), (2, '低')], default=2, verbose_name='手机等级')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Admin', verbose_name='所属管理员')),
            ],
        ),
        migrations.AddField(
            model_name='admin',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Department', verbose_name='所属部门'),
        ),
    ]
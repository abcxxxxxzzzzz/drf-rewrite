from operator import mod
from django.db import models

# Create your models here.
class DmGroupsModel(models.Model):
    group_name = models.CharField("域名组", unique=True,max_length=32, db_index=True, help_text="域名组")

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "resources_group"



class DmModel(models.Model):
    domain          = models.CharField("域名",unique=True, max_length=32, db_index=True, help_text="域名")
    looks           = models.PositiveIntegerField("访问量",default=0,help_text="访问量")
    rewrite_url     = models.CharField("跳转地址", max_length=32, help_text="跳转地址") 
    group           = models.ForeignKey(DmGroupsModel, on_delete=models.CASCADE, verbose_name="所属域名组", related_name="groups",help_text="所属域名组")
    ct_time         = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.domain

    def increase_looks(self):
            self.looks += 1
            self.save(update_fields=['looks'])

    class Meta:
        db_table = "resources_domain"
        ordering = ["id"]
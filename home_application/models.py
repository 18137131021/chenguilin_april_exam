# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
from django.db import models


# 任务模板表
class TASK_MODULE(models.Model):
    module_name = models.CharField(verbose_name=u"模板名称", max_length=100)
    biz_name = models.CharField(verbose_name=u"业务名称", max_length=100)
    biz_id = models.CharField(verbose_name=u"业务id", max_length=100)
    module_type = models.CharField(verbose_name=u"模板类型", max_length=100)
    hands_user = models.CharField(verbose_name=u"创建者", max_length=100)
    module_time = models.CharField(verbose_name=u"创建时间", max_length=100)
    updata_hands_user = models.CharField(verbose_name=u"更新者", max_length=100)
    updata_module_time = models.CharField(verbose_name=u"更新时间", max_length=100)
    is_delete = models.IntegerField(verbose_name=u"是否删除", default=0)

    class Meta:
        verbose_name = u"任务模板"
        db_table = 'task_module'


# 任务表
class T_SCRIPT_DATA(models.Model):
    task_module = models.ForeignKey(TASK_MODULE, verbose_name=u"对应模板")
    operation_id = models.CharField(verbose_name=u"操作序号", max_length=500, null=True)
    operation = models.CharField(verbose_name=u"操作事项", max_length=500, null=True)
    remarks = models.CharField(verbose_name=u"备注", max_length=500, null=True)
    people_name = models.CharField(verbose_name=u"负责人", max_length=500, null=True)
    updata_time = models.CharField(verbose_name=u"完成时间", max_length=100)
    status = models.CharField(verbose_name=u"是否完成", max_length=500, null=True)
    class Meta:
        verbose_name = u"模板对应任务"
        db_table = 't_script_data'
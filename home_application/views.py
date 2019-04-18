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
import sys
import datetime
import xlwt
import xlrd
import os
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from common.mymako import render_mako_context
from home_application import models
from unins import ESB
from django.db.models import Q
from common.mymako import render_json



def home(request):
    """
    首页
    """
    all_script_task = models.TASK_MODULE.objects.filter(is_delete=0)
    #
    result = job_data(request)
    all_pid = result.get('data')
    return render_mako_context(request, 'home_application/search_tasks.html', {'all_pid': all_pid,
                                                                               'all_script_task': all_script_task})


# 新增模板页面
def add_module_html(request):
    result = job_data(request)
    all_pid = result.get('data')
    return render_mako_context(request, 'home_application/script_supervise.html', {'all_pid': all_pid})

from django.views.decorators.csrf import csrf_exempt
from conf.default import SITE_URL
# 新增模板
@csrf_exempt
def add_module(request):
    if request.method == "POST":
        biz_id = int(request.POST.get('select_business2').split(',')[0])
        biz_name = request.POST.get('select_business2').split(',')[1]
        module_type = request.POST.get('module_type', '')
        module_name = request.POST.get('module_name', '')
        number = request.POST.get('number', '')
        obj = request.FILES.get('task_file', '')
        print obj
        baseDir = os.path.dirname(os.path.abspath(__name__))  # 获取运行路径
        jpgdir = os.path.join(baseDir, 'static')  # 加上static路径
        filename = os.path.join(jpgdir, obj.name)
        fobj = open(filename, 'wb+')  # 打开上传文件
        for x in obj.chunks():
            fobj.write(x)  # request.FILES,文件专用
        fobj.close()
        print filename

        module = models.TASK_MODULE.objects.create(
            biz_name=biz_name,
            biz_id=biz_id,
            module_name=module_name,
            module_type=module_type,
            hands_user=request.user.username,
            module_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updata_hands_user=request.user.username,
            updata_module_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_delete=0
        )
        s = obj.name.encode('utf-8')
        # f = open(os.path.join('/upload', '/task_file.xls'), 'wb')
        # for line in obj.chunks():
        #     f.write(line)
        # f.close()
        # print f
        workbook = xlrd.open_workbook(filename)
        print workbook
        # # wb = xlwt.Workbook()
        # # ws = wb.add_sheet(s)
        # sheet1_name = workbook.sheet_names()[0]
        # print sheet1_name
        a = 0
        b = 0
        # for a in sheet1_name:
        #     data = sheet1_name.cell(a, b).value.encode('utf-8')
        #     print data
    # return redirect(reverse(home))


# 删除模板
def del_model(request, o_id):
    module_data = models.TASK_MODULE.objects.filter(id=int(o_id)).first()
    module_data.is_delete = 1
    module_data.save()
    return redirect(reverse(home))


def job_data(request):
    """
    获取当前用户下的业务
    :param request:
    :return:
    """

    response = {}

    try:
        result = ESB.ESBApi(request).search_business()
        if result['result']:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = {}
            if len(result['data']['info']) > 0:
                for item in result['data']['info']:
                    dic = {}
                    dic[item['bk_biz_id']] = item['bk_biz_name']
                    response['data'].update(dic)
            else:
                response['result'] = True
                response['code'] = 0
                response['message'] = u'该用户下无业务'
                response['data'] = {}
        else:
            response = result

    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = u'获取业务列表失败：%s' % e
        response['data'] = {}

    return response


# 根据条件查询模板
def search_all_job(request):
    biz_name = request.GET.get('biz_name', '')
    module_type = request.GET.get('module_type', '')
    inputCount3 = request.GET.get('inputCount3', '')
    q = Q(is_delete__contains=0)
    if biz_name:
        q.add(Q(biz_name=biz_name), q.AND)
    if module_type:
        q.add(Q(module_type=module_type), q.AND)
    if inputCount3:
        q.add(Q(module_name=inputCount3), q.AND)
    search_data = models.TASK_MODULE.objects.filter(q)
    print search_data
    list = []
    for one_data in search_data:
        listDic = {}
        listDic['id'] = one_data.id
        listDic['module_name'] = one_data.module_name
        listDic['biz_name'] = one_data.biz_name
        listDic['module_type'] = one_data.module_type
        listDic['hands_user'] = one_data.hands_user
        listDic['module_time'] = one_data.module_time
        listDic['updata_hands_user'] = one_data.updata_hands_user
        listDic['updata_module_time'] = one_data.updata_module_time
        list.append(listDic)
    data = {
        'massage': True,
        'data': list
    }
    return render_json(data)


def test_data(request):
    data1 = request.GET.dict()
    print data1
    data = {}
    for a in data1:
        data[a] = data1['a']
    print data1
    return render_json({
        "result": True,
        "message": "success",
        "data": data
    })
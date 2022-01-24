
from warnings import filters
from django.http.response import HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect
from .serializers import DmModelSerializer, DmGroupsModelSerializer
from .models import DmModel, DmGroupsModel
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import re
from .filter import DmModelFilter
import xlwt
from io import BytesIO


class DmModelViewset(viewsets.ModelViewSet):
    """
    retrieve: 返回域名信息
    
    list: 返回域名列表
    
    update: 更新域名信息
    
    destroy: 删除域名记录
    
    create: 创建域名资源
    
    partial_update: 更新部分字段
    """

    queryset = DmModel.objects.all()
    serializer_class = DmModelSerializer
    filter_class = DmModelFilter
    filter_fields = ("domain", "group")

    # 通过many=True直接改造原有的API，使其可以批量创建
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download(self, request, *args, **kwargs):
        obj_data = DmModel.objects.all()
        ws = xlwt.Workbook(encoding='utf-8')
        st = ws.add_sheet('sheet1')
        # 写标题行
        st.write(0, 0, 'ID')
        st.write(0, 1, '域名')
        st.write(0, 2, '访问量')
        st.write(0, 3, '跳转地址')
        st.write(0, 4, '域名组')
        st.write(0, 5, '添加时间')
        # 写入数据，从第一行开始
        excel_row = 1
        for obj in obj_data:
            st.write(excel_row, 0, obj.id)
            st.write(excel_row, 1, obj.domain)
            st.write(excel_row, 2, obj.looks)
            st.write(excel_row, 3, obj.rewrite_url)
            st.write(excel_row, 4, obj.group.group_name)
            st.write(excel_row, 5, str(obj.ct_time))

            excel_row += 1

                # 将数据写入io数据流，不用在本地生成excel文件，不然效率就低了
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        # print(sio.getvalue())
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=xx.xls'
        response.write(output.getvalue())

        return response
        # return Response({'code': 200})

class DmGroupsModelViewset(viewsets.ModelViewSet):
    """
    retrieve: 返回域名组信息
    
    list: 返回域名组列表
    
    update: 更新域名组信息
    
    destroy: 删除域名组记录
    
    create: 创建域名组资源
    
    partial_update: 更新部分字段

    multiple_update： 批量更新
    """

    queryset = DmGroupsModel.objects.all()
    serializer_class = DmGroupsModelSerializer



    # 批量更新
    @action(methods=['post'], detail=False)
    def multiple_update(self, request, *args, **kwargs):
        data = request.data
        query = DmGroupsModel.objects.get(id=int(data.get('id')))
        try:
            query.groups.all().filter(rewrite_url=data.get('old_url')).update(rewrite_url=data.get('new_url'))
            return Response({'code':200})
        except:
            return Response({'code':400})


from django.shortcuts import get_object_or_404
def rewrites(request):
    source_dm = request.GET.get('u')
    if source_dm:
        source_dm = source_dm.replace("http://", '').split('/')
        zz = '^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$'
        obj_sh = re.search(zz, source_dm[0])
        if obj_sh:
            obj = get_object_or_404(DmModel, domain=obj_sh.group())
            obj.increase_looks()
            return redirect(obj.rewrite_url, permanent=True)
        # return HttpResponseRedirect(reverse(obj.rewrite_url))
    return HttpResponseNotFound()


from warnings import filters
from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect
from .serializers import DmModelSerializer, DmGroupsModelSerializer
from .models import DmModel, DmGroupsModel
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import re
from .filter import DmModelFilter

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
            return redirect(obj.rewrite_url)
        # return HttpResponseRedirect(reverse(obj.rewrite_url))
    return HttpResponseNotFound()
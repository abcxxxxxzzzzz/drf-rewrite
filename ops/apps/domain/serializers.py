from .models import DmGroupsModel, DmModel
from rest_framework import serializers


class DmGroupsModelSerializer(serializers.ModelSerializer):
    """
    域名组序列化类
    """

    def to_representation(self, instance):
        ret = super(DmGroupsModelSerializer, self).to_representation(instance)
        ret['count'] = instance.groups.all().count()
        return ret


    class Meta:
        model = DmGroupsModel
        fields = '__all__'

class DmModelSerializer(serializers.ModelSerializer):
    """
    域名序列化类
    """
    def to_representation(self, instance):
        dmgroup_obj = instance.group
        ret =  super(DmModelSerializer, self).to_representation(instance)
        ret['group'] = {
            "id": dmgroup_obj.id,
            "group_name": dmgroup_obj.group_name
        }
        return ret

    class Meta:
        model = DmModel
        fields = '__all__'


    
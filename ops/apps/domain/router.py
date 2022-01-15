from rest_framework.routers import DefaultRouter
from .views import DmGroupsModelViewset,DmModelViewset


dm_router = DefaultRouter()
dm_router.register(r'dm', DmModelViewset, base_name='dm')
dm_router.register(r'dmgp', DmGroupsModelViewset, base_name='dmgp' )
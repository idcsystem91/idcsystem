from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ImportMixin,ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
# NerimaStockData, SouthSaitamaStockData, KawaguchiTodaStockData
from stocks.models import Service, Type, Device, Status, StockData
from users.models import User


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    pass


@admin.register(Type)
class AdminType(admin.ModelAdmin):
    pass


@admin.register(Device)
class AdminDevice(admin.ModelAdmin):
    class Meta:
        model = Device
        fields = ('id', 'name')


@admin.register(Status)
class AdminStatus(admin.ModelAdmin):
    pass


class StockDataResource(ModelResource):
    """StockDataモデルのリソース"""
    area = Field(attribute='area', column_name='コープ名')
    device = Field(attribute='device', column_name='型名',
                   widget=ForeignKeyWidget(Device, 'name'))
    serial = Field(attribute='serial', column_name='機器ID')
    arrival = Field(attribute='arrival', column_name='納品日')
    delivery = Field(attribute='delivery', column_name='持出日')
    use = Field(attribute='use', column_name='使用日')
    staff = Field(attribute='staff', column_name='使用者',
                  widget=ForeignKeyWidget(User, 'username'))
    customer = Field(attribute='customer', column_name='顧客番号')
    job = Field(attribute='job', column_name='業種')
    status = Field(attribute='status', column_name='状態',
                   widget=ForeignKeyWidget(Status, 'name'))

    class Meta:
        model = StockData
        fields = ('area', 'device', 'serial',
                  'arrival', 'delivery', 'use', 'staff', 'customer', 'job', 'status')
        import_id_fields = ('serial',)


class StockDataAdmin(ImportExportModelAdmin):
    """StockDataAdminのベース"""
    list_display = ('id', 'area', 'device', 'serial', 'arrival',
                    'delivery', 'use', 'staff', 'customer', 'job', 'status')
    resource_class = StockDataResource
    formats = [base_formats.CSV]
    search_fields = ['serial', 'customer']


admin.site.register(StockData, StockDataAdmin)


# """練馬在庫データ"""


# class NerimaStockDataResource(StockDataResource):
#    """StockDataResourceを継承"""
#    class Meta:
#        model = NerimaStockData
#
#    """StockDataAdminを継承"""


# class NerimaStockDataAdmin(StockDataAdmin):
#    resource_class = NerimaStockDataResource


#admin.site.register(NerimaStockData, NerimaStockDataAdmin)


# """さいたま南在庫データ"""


# class SouthSaitamaStockDataResource(StockDataResource):
#    """StockDataResourceを継承"""
#    class Meta:
#        model = SouthSaitamaStockData
#
#    """StockDataAdminを継承"""


# class SouthSaitamaStockDataAdmin(StockDataAdmin):
#    resource_class = SouthSaitamaStockDataResource


#admin.site.register(SouthSaitamaStockData, SouthSaitamaStockDataAdmin)


# """川口・戸田在庫データ"""


# class KawaguchiTodaStockDataResource(StockDataResource):
#    """StockDataResourceを継承"""
#   class Meta:
#        model = KawaguchiTodaStockData

#    """StockDataAdminを継承"""


# class KawaguchiTodaStockDataAdmin(StockDataAdmin):
#    resource_class = KawaguchiTodaStockDataResource


#admin.site.register(KawaguchiTodaStockData, KawaguchiTodaStockDataAdmin)

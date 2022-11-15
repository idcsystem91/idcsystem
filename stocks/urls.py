from django.urls import path
from . import views

#app_name = 'stocks'

urlpatterns = [
     path('list/', views.StockList.as_view(), name='list'),
     path('detail/<int:pk>/', views.StockDetail.as_view(), name='detail'),
     path('create/', views.StockCreate.as_view(), name='create'),
     path('update/<int:pk>/', views.StockUpdate.as_view(), name='update'),
     path('delete/<int:pk>/', views.StockDelete.as_view(), name='delete'),

     path('manager/', views.ManagerIndex.as_view(), name='manager_index'),
     path('manager_stock_list/',views.ManagerStockList.as_view(), name='ManagerStockList'),
     path('manager_stock_count/',views.ManagerStockCount.as_view(), name='ManagerStockCount'),

     path("instore/", views.StockInStoreView.as_view(), name="instore"),
     path("defective/", views.DefectiveList.as_view(), name="defective"),

     path('', views.Index.as_view(), name='index'),
     path('find/', views.FindView.as_view(), name='find'),
     #path('detail/<int:pk>', views.StockDataDetailView.as_view()),
     path('delivery/', views.DeliveryView.as_view(), name='delivery'),
     path('use/', views.UseView.as_view(), name='use'),
     path('return/', views.ReturnView.as_view(), name='return'),
     path('/', views.CreateView.as_view(), name='create'),
     path('admin_stockdata_list/', views.StockDataListView.as_view(),
          name='admin_stockdata_list'),
     path('count/', views.StockDataCountView.as_view()),
     path('<str:device>/device_stock_list/',
          views.StockDataDeviceStockListView.as_view()),
     path('used_list/', views.UsedDeviceListView.as_view(), name='used_list'),
     path('use_device_correct/<int:pk>/', views.UseDeviceUpdateView.as_view()),
     path('tanaoroshi/',views.InventoryCSVExport.as_view(), name='tanaoroshi'),
     path('inventory_CSV_export/', views.inventory_CSV_export, name='inventory_CSV_export'),
     path('use_device/',views.UsedDevice.as_view(), name='use_device'),
]

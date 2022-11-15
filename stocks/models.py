from django.db import models
from users.models import User, Job


class Service(models.Model):
    """サービス種別"""
    name = models.CharField('サービス名', max_length=30)
    sort_no = models.IntegerField('表示順')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'サービス'
        verbose_name_plural = 'サービス'


class Type(models.Model):
    """機種種別"""
    name = models.CharField(max_length=30)
    sort_no = models.IntegerField('表示順')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '種別'
        verbose_name_plural = '種別'


class Device(models.Model):
    """機種リスト"""
    name = models.CharField('機種名', max_length=30)
    service = models.ForeignKey(
        Service, verbose_name='サービス', on_delete=models.CASCADE)
    type = models.ForeignKey(Type, verbose_name='種別', on_delete=models.CASCADE)
    is_active = models.BooleanField(('有効'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '機器'
        verbose_name_plural = '機器'


class Status(models.Model):
    """状態"""
    status_name = models.CharField(max_length=30)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = '状態'
        verbose_name_plural = '状態'


class StockData(models.Model):
    """在庫リストモデルクラス　このクラスを継承して使用する"""
    area = models.CharField('コープ名', max_length=30)
    device = models.ForeignKey(
        Device, verbose_name='機種名', on_delete=models.CASCADE)
    serial = models.CharField('機器ID', max_length=50)
    arrival = models.DateField('入荷日')
    delivery = models.DateField('持出日', null=True, blank=True)
    use = models.DateField('使用日', null=True, blank=True)
    staff = models.ForeignKey(
        User, verbose_name='担当者', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.CharField('顧客', max_length=30, blank=True)
    job = models.ForeignKey(
        Job, verbose_name='業種', on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(
        Status, verbose_name='状態', on_delete=models.CASCADE, default=1)
    comment = models.TextField('コメント', blank=True)
    log = models.TextField('ログ', blank=True)

    class Meta:
        verbose_name = '在庫リスト'
        verbose_name_plural = '在庫リスト'


# class NerimaStockData(StockData):
#    """練馬の在庫データ　StockDataクラスを継承"""
#
#    class Meta:
#        verbose_name = '●練馬在庫'
#        verbose_name_plural = '●練馬在庫'


# class SouthSaitamaStockData(StockData):
#    """さいたま南の在庫データ　StockDataクラスを継承"""
#
#    class Meta:
#        verbose_name = '●さいたま南在庫'
#        verbose_name_plural = '●さいたま南在庫'


# class KawaguchiTodaStockData(StockData):
#    """川口・戸田の在庫データ　StockDataクラスを継承"""
#
#    class Meta:
#        verbose_name = '●川口・戸田在庫'
#        verbose_name_plural = '●川口・戸田在庫'

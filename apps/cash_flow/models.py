from datetime import date

from django.db import models


class CashFlowType(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Тип денежного потока',
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Тип денежного потока'
        verbose_name_plural = 'Типы денежного потока'
        db_table = 'cash_flow_types'

class CashFlowCategory(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='subcategories',
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Категория (подкатегория) денежного потока',
        unique=True,
    )
    type = models.ForeignKey(
        'CashFlowType',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='subcategories',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория (подкатегория) денежного потока'
        verbose_name_plural = 'Категории (подкатегории) денежного потока'
        db_table = 'cash_flow_categories'

class CashFlowStatus(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        verbose_name='Статус денежного потока',
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Статус денежного потока'
        verbose_name_plural = 'Статусы денежного потока'
        db_table = 'cash_flow_statuses'

class CashFlow(models.Model):
    type = models.ForeignKey(
        'CashFlowType',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='types'
    )
    category = models.ForeignKey(
        'CashFlowCategory',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='categories'
    )
    amount = models.DecimalField(
        null=False,
        blank=False,
        max_digits=19,
        decimal_places=2,
        verbose_name='Сумма денежного потока',
    )
    status = models.ForeignKey(
        'CashFlowStatus',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='statuses'
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    creation_date = models.DateField(
        null=False,
        verbose_name='Дата создания записи',
        default=date.today,
    )

    def __str__(self):
        return f"{self.type} {self.amount} р."

    class Meta:
        verbose_name = 'Денежный поток'
        verbose_name_plural = 'Денежные потоки'
        ordering = ['creation_date']
        db_table = 'cash_flows'

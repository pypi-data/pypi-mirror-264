from dekdjtools.models.base import ModelBasic
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MigrationRecord(ModelBasic):
    mid = models.CharField(_('mid'), max_length=100, unique=True)
    content = models.BinaryField(verbose_name=_('数据块'))
    datetime_created = models.DateTimeField(verbose_name=_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('记录')

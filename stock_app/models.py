from django.db import models


class DailyDataManager(models.Manager):
    def create_daily_data(self, code, date, open_p, high, low, close, volume):
        daily_data = self.create(code=code,
                                 date=date,
                                 open=open_p,
                                 high=high,
                                 low=low,
                                 close=close,
                                 volume=volume)
        return daily_data


class DailyData(models.Model):
    code = models.IntegerField()
    date = models.DateField()
    open = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    close = models.IntegerField()
    volume = models.IntegerField()

    objects = DailyDataManager()

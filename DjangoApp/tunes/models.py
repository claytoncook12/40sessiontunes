from django.db import models

class TuneType(models.Model):
    tune_type_char = models.CharField('Tune Type', max_length=50, unique=True)

    def __str__(self):
        return self.tune_type_char

class Key(models.Model):
    key_type_char = models.CharField('Key', max_length=15, unique=True)

    def __str__(self):
        return self.key_type_char

class Composer(models.Model):
    name = models.CharField('Name', max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

class Tune(models.Model):
    name = models.CharField('Tune Name', max_length=300)
    tune_type = models.ForeignKey(TuneType, on_delete=models.CASCADE, verbose_name="Tune Type")
    parts = models.IntegerField('Number of Parts', default=2)
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, verbose_name="Composer",
                                 null=True, blank=True)
    tune_info = models.CharField('Information about the tune', max_length=300, null=True, blank=True)

    def __str__(self):
        return  f'{self.name} ({self.tune_type.tune_type_char})'
   
class ABCText(models.Model):
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune")
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name="Key of Tune")
    text = models.TextField('Abc Text', null=True, blank=True)

    def __str__(self):
        return f'{self.tune} ({self.key})'
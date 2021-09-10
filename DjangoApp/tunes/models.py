from django.db import models
from django.urls import reverse

class TuneType(models.Model):
    tune_type_char = models.CharField('Tune Type', max_length=50, unique=True)

    def __str__(self):
        return self.tune_type_char

class Key(models.Model):
    key_type_char = models.CharField('Key', max_length=15, unique=True)

    def __str__(self):
        return self.key_type_char

class Meter(models.Model):
    meter_type_char = models.CharField('Meter', max_length=15, unique=True, default="4/4")

    def __str__(self):
        return self.meter_type_char

class Composer(models.Model):
    name = models.CharField('Name', max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

class UnitNoteLength(models.Model):
    unit_note_length = models.CharField('Unit Note Length', max_length=50, unique=True, default="1/4")

    def __str__(self):
        return self.unit_note_length

class Tune(models.Model):
    name = models.CharField('Tune Name', max_length=300)
    tune_type = models.ForeignKey(TuneType, on_delete=models.CASCADE, verbose_name="Tune Type")
    parts = models.IntegerField('Number of Parts', default=2)
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE, verbose_name="Composer",
                                 null=True, blank=True)
    tune_info = models.CharField('Information about the tune', max_length=300, null=True, blank=True)

    def __str__(self):
        return  f'{self.name} ({self.tune_type.tune_type_char})'
    
    def get_absolute_url(self):
        return reverse('tunes:detail', kwargs={"id": self.id})
   
class ABCTune(models.Model):
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune")
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name="Key of Tune")
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, verbose_name="Meter")

    def __str__(self):
        return f'{self.tune} ({self.key})'
    
    def abc_line_title(self):
        return f'T:{self.tune.name}'
    
    def abc_line_composer(self):
        return f'C:{self.tune.composer}'
    
    def abc_line_key(self):
        return f'K:{self.key}'

    def abc_line_meter(self):
        return f'M:{self.meter.meter_type_char}'
    
    def abc_full(self):
        return (
            f'{self.abc_line_title()}\n'
            f'{self.abc_line_composer()}\n'
            f'{self.abc_line_meter()}\n'
            f'{self.abc_line_key()}\n'
        )

class ABCTunePiece(models.Model):
    tune = models.ForeignKey(ABCTune, on_delete=models.CASCADE, verbose_name="ABC Tune")
    part_order = models.IntegerField('Part Number', default=1)
    part_title = models.CharField('Title of Part', max_length=30,
        default="Part #", null=True, blank=True)
    default = models.BooleanField('Default Part?', default=True)
    abc_piece = models.TextField('ABC text for part of Tune')
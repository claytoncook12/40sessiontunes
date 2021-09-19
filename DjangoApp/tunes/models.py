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
    
class BPM(models.Model):
    bpm = models.CharField("Beats Per Minute", max_length=50, unique=True, default="1/4=120")

    def __str__(self):
        return f'BPM: {self.bpm}'

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
    
    def first_two_bars(self):
        return ABCTune.objects.get(tune=self).abc_piece_and_bars(1, 2)
   
class ABCTune(models.Model):
    tune = models.ForeignKey(Tune, on_delete=models.CASCADE, verbose_name="Tune")
    key = models.ForeignKey(Key, on_delete=models.CASCADE, verbose_name="Key of Tune")
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, verbose_name="Meter")
    unit_note_length = models.ForeignKey(UnitNoteLength, on_delete=models.CASCADE, verbose_name="Unit Note Length")
    bpm = models.ForeignKey(BPM, on_delete=models.CASCADE, verbose_name="Beats Per Minute", null=True, blank=True)

    def __str__(self):
        return f'{self.tune} ({self.key})'
    
    # Methods to Return ABC from model
    def abc_line_title(self):
        return f'T:{self.tune.name}'
    
    def abc_line_composer(self):
        return f'C:{self.tune.composer}'
    
    def abc_line_key(self):
        return f'K:{self.key}'

    def abc_line_meter(self):
        return f'M:{self.meter.meter_type_char}'
    
    def abc_line_unit_note_length(self):
        return f'L:{self.unit_note_length.unit_note_length}'
    
    def abc_line_bpm(self):
        if self.bpm:
            return f'Q:{self.bpm.bpm}'
        else:
            return f''
    
    def abc_default_notes(self):
        """
        Return only default parts from ABCTunePiece
        for ABCTune
        """
        abc_pieces = ABCTunePiece.objects.filter(abc_tune=self)
        abc_pieces_text = ""
        for piece in abc_pieces:
            abc_pieces_text += piece.abc_piece
            abc_pieces_text += "\n"
        
        return abc_pieces_text
    
    def abc_full_default(self):
        """
        Return full abc with just the parts that are marked default
        """
        
        return (
            f'{self.abc_line_title()}\n'
            f'{self.abc_line_composer()}\n'
            f'{self.abc_line_meter()}\n'
            f'{self.abc_line_key()}\n'
            f'{self.abc_line_unit_note_length()}\n'
            f'{self.abc_default_notes()}'
        )
    
    def abc_full_default_bpm(self):
        """
        Return full abc with just the parts that are marked default
        with bpm
        """
        
        return (
            f'{self.abc_line_title()}\n'
            f'{self.abc_line_composer()}\n'
            f'{self.abc_line_meter()}\n'
            f'{self.abc_line_key()}\n'
            f'{self.abc_line_unit_note_length()}\n'
            f'{self.abc_line_bpm()}\n'
            f'{self.abc_default_notes()}'
        )

    def abc_piece_and_bars(self, part_order=1, bars=2):
        """
        Returns the numbers of bars from a ABCTunePiece
        """
        try:
            abc_piece = ABCTunePiece.objects.get(abc_tune=self, part_order=part_order).abc_piece
        except  ABCTunePiece.DoesNotExist:
            return None

        # Remove initial bar information before splitting
        if abc_piece[0] == "|":
            abc_piece = abc_piece[1:]
        if abc_piece[0] == ":":
            abc_piece = abc_piece[1:]
        if abc_piece[-1] == "|":
            abc_piece = abc_piece[:-1]
        if abc_piece[-1] == ":":
            abc_piece = abc_piece[:-1]

        # Split ABC text into bars
        abc_piece_bars = abc_piece.split("|")
        if bars > len(abc_piece_bars):
            raise ValueError(f'Only {len(abc_piece_bars)} in abc text and {bars} bars were requested.')
        
        # Return bars from text
        abc_return = ""
        for abc_bars in abc_piece_bars[:bars]:
            abc_return += abc_bars + "|"
        # Add back bar symbol at beginning
        abc_return = "|" + abc_return

        return abc_return


class ABCTunePiece(models.Model):
    abc_tune = models.ForeignKey(ABCTune, on_delete=models.CASCADE, verbose_name="ABC Tune")
    part_order = models.IntegerField('Part Number', default=1)
    part_title = models.CharField('Title of Part', max_length=30,
        default="Part #", null=True, blank=True)
    default = models.BooleanField('Default Part?', default=True)
    abc_piece = models.TextField('ABC text for part of Tune')
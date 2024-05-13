from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


def attachment_path(instance, filename):
    return 'film/' + str(instance.film.id) + '/attachments/' + filename


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Název předmětu',
    help_text='Zapiš o jaký předmět se jedná (PVY OS...)')

    class Meta:
        verbose_name = 'Předmět'
        verbose_name_plural = 'Předměty'
        ordering = ['name']

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Název')
    plot = models.TextField(blank=True, null=True, verbose_name='Obsah')
    release_date = models.DateField(blank=True, null=True,
                                    help_text='Zadej datum vydání textu: <em>YYYYMM-DD</em>.',
                                    verbose_name='Vydání textu')
    runtime = models.IntegerField(blank=True, null=True,
                                  help_text='Prosím zadej v hodinách',
                                  verbose_name='Jak dlouho bude trvat se naučit:')
    poster = models.ImageField(upload_to='film/posters/%Y/%m/%d/', blank=True, null=True,
                               verbose_name="Logo")
    rate = models.FloatField(default=5.0,
                             validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
                             null=True, help_text='Ohodnoť svůj výukový materiál (1 - 10)',
                             verbose_name='Ohodnoť')
    genres = models.ManyToManyField(Genre, help_text='Vyber předmět pro tvůj výukový materiál.')

    class Meta:
        verbose_name = 'Výukový materiál'
        verbose_name_plural = 'Výukový materiál'
        ordering = ['-release_date', 'title']

    def __str__(self):
        return f'{self.title}, year: {str(self.release_date.year)}, rate:{str(self.rate)}'

    def get_absolute_url(self):
        return reverse('film-detail', args=[str(self.id)])


class Attachment(models.Model):
    title = models.CharField(max_length=200, verbose_name='Nazev')
    last_update = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name='Soubor')
    TYPE_OF_ATTACHMENT = (
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )
    type = models.CharField(max_length=10, choices=TYPE_OF_ATTACHMENT, blank=True,
        default='image', help_text='Select allowed attachment type',
        verbose_name='Attachment type')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Příloha'
        verbose_name_plural = 'Přílohy'
        ordering = ['-last_update', 'type']

    def __str__(self):
        return f'{self.title}, ({self.type})'


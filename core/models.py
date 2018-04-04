# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Cachedreport(models.Model):
    id = models.CharField(db_column='ID', max_length=50, primary_key=True)
    path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'CachedReport'


class Gov(models.Model):
    govid = models.AutoField(db_column='GovID', primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(db_column='Code', max_length=50)
    parentgovid = models.ForeignKey('self', models.DO_NOTHING,
                                    db_column='parentGovID',
                                    blank=True, null=True)
    gcid = models.ForeignKey('Govcat', models.DO_NOTHING, db_column='GCID')
    originid = models.IntegerField(db_column='OriginID')
    mdbcode = models.CharField(db_column='mdbCode', max_length=20,
                               blank=True, null=True)
    metadata = models.CharField(db_column='Metadata', blank=True,
                                null=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'Gov'

    def __str__(self):
        return self.name


class Govcat(models.Model):
    gcid = models.AutoField(db_column='GCID', primary_key=True)
    description = models.CharField(db_column='Description', max_length=150)

    class Meta:
        managed = False
        db_table = 'GovCat'

    def __str__(self):
        return self.description


class Govindicator(models.Model):
    giid = models.AutoField(db_column='GIID', primary_key=True)
    value = models.CharField(max_length=50)
    iid = models.ForeignKey('Indicator', models.DO_NOTHING, db_column='IID')
    govid = models.ForeignKey(Gov, models.DO_NOTHING, db_column='GovID')
    yearid = models.ForeignKey('Yearref', models.DO_NOTHING,
                               db_column='YearID')

    class Meta:
        managed = False
        db_table = 'GovIndicator'


class Govindicatorrank(models.Model):
    girid = models.AutoField(db_column='GIRID', primary_key=True)
    iid = models.ForeignKey('Indicator', models.DO_NOTHING,
                            db_column='IID')
    ranking = models.IntegerField(db_column='Ranking')
    score = models.FloatField(db_column='Score')
    govid = models.ForeignKey(Gov, models.DO_NOTHING,
                              db_column='GovID')
    yearid = models.ForeignKey('Yearref', models.DO_NOTHING,
                               db_column='YearID')

    class Meta:
        managed = False
        db_table = 'GovIndicatorRank'


class Govmeta(models.Model):
    govid = models.ForeignKey(Gov, models.DO_NOTHING, db_column='GovID')
    mdid = models.ForeignKey('Metadescriptor', models.DO_NOTHING,
                             db_column='MDID')
    value = models.CharField(max_length=50)
    gmid = models.AutoField(db_column='GMID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'GovMeta'


class Govrank(models.Model):
    rankid = models.AutoField(db_column='RankID', primary_key=True)
    ranking = models.IntegerField(db_column='Ranking')
    govid = models.ForeignKey(Gov, models.DO_NOTHING,
                              db_column='GovID')
    idpscore = models.FloatField(db_column='idpScore', blank=True,
                                 null=True)
    servicedelscore = models.FloatField(db_column='serviceDelScore',
                                        blank=True, null=True)
    financescore = models.FloatField(db_column='financeScore', blank=True,
                                     null=True)
    hrscore = models.FloatField(db_column='hrScore', blank=True, null=True)
    govscore = models.FloatField(db_column='govScore', blank=True, null=True)
    combinedscore = models.FloatField(db_column='combinedScore', blank=True,
                                      null=True)
    yearid = models.ForeignKey('Yearref', models.DO_NOTHING,
                               db_column='YearID')

    class Meta:
        managed = False
        db_table = 'GovRank'


class Govyear(models.Model):
    yearid = models.ForeignKey('Yearref', models.DO_NOTHING,
                               db_column='YearID')
    govid = models.ForeignKey(Gov, models.DO_NOTHING, db_column='GovID')

    class Meta:
        managed = False
        db_table = 'GovYear'
        unique_together = (('yearid', 'govid'),)


class Grouping(models.Model):
    gid = models.AutoField(db_column='GID', primary_key=True)
    name = models.CharField(max_length=50)
    parentgid = models.ForeignKey('self', models.DO_NOTHING,
                                  db_column='parentGID', blank=True, null=True)
    comp = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Grouping'

    def __str__(self):
        return '{}'.format(self.name)


class Indicator(models.Model):
    iid = models.AutoField(db_column='IID', primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    parentgid = models.ForeignKey(Grouping, models.DO_NOTHING,
                                  db_column='parentGID', blank=True, null=True)
    unitid = models.ForeignKey('Unit', models.DO_NOTHING, db_column='unitID')
    scale = models.CharField(db_column='Scale', max_length=1, blank=True,
                             null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    mgid = models.ForeignKey('Mandategroup', models.DO_NOTHING,
                             db_column='MGID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Indicator'

    def __str__(self):
        return '{}'.format(self.name)


class Mandategroup(models.Model):
    mgid = models.AutoField(db_column='MGID', primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MandateGroup'


class Metadescriptor(models.Model):
    mdid = models.AutoField(db_column='MDID', primary_key=True)
    description = models.CharField(db_column='Description', max_length=255)

    class Meta:
        managed = False
        db_table = 'MetaDescriptor'


class Unit(models.Model):
    unitid = models.AutoField(db_column='unitID', primary_key=True)
    unit = models.CharField(max_length=25)
    isd = models.BooleanField(db_column='isD')

    class Meta:
        managed = False
        db_table = 'Unit'

    def __str__(self):
        return '{}'.format(self.unit)


class Yearref(models.Model):
    yearid = models.AutoField(db_column='YearID', primary_key=True)
    yr = models.IntegerField(db_column='Yr')
    geojson = models.CharField(db_column='GeoJson', max_length=50)

    class Meta:
        managed = False
        db_table = 'YearRef'

    def __str__(self):
        return '{}'.format(self.yr)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)

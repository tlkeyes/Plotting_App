from django.db import models

# Create your models here.
class RawMonthlyCurrent2(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nhsn = models.CharField(db_column='NHSN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    jarid = models.CharField( db_column='JarID', max_length=5, null=True, blank=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    measure_name = models.CharField(db_column='Measure_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    measure_type = models.CharField(db_column='Measure_Type', max_length=25, blank=True, null=True)  # Field name made lowercase.
    process_outcome = models.CharField(db_column='Process_Outcome', max_length=10, blank=True, null=True)  # Field name made lowercase.
    loccdc = models.CharField(db_column='locCDC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    unit_type = models.CharField(db_column='Unit_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    unit_name = models.CharField(db_column='Unit_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numerator = models.FloatField(db_column='Numerator', blank=True, null=True)  # Field name made lowercase.
    denominator = models.FloatField(db_column='Denominator', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Raw_Monthly_Current2'
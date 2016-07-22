# Create your models here.

import datetime
from django.db import models
from django.utils import timezone
from django import forms
from django.forms import ModelForm
import django_tables2 as tables


class Sampleview(models.Model):

    #db_table = 'geldbx_samplelist'

    gmc_clinic_id = models.CharField('GMC clinic ID', max_length=10, blank=True, default='')
    clinical_sample_id = models.CharField('Sample set ID', max_length=10, unique=True, primary_key=True)
    pid_fk = models.CharField('Participant ID', max_length=12, unique=True, default='')
    pname = models.CharField('Participant name', max_length=50, blank=True, default='')
    blood_specimen_id = models.CharField('Blood specimen ID',max_length=15, null=True, blank=True)
    blood_specimen_taken_dtm = models.DateTimeField('Blood specimen taken time', null=True, blank=True)
    tissue_specimen_id = models.CharField('Tissue specimen ID',max_length=15, null=True, blank=True)
    tissue_specimen_taken_dtm = models.DateTimeField('Tissue specimen taken time', null=True, blank=True)
    lab_sample_sent_date = models.DateTimeField('Samples sent date', null=True, blank=True)
    xml_status = models.CharField('Data and rack ready', max_length=1, null=True, blank=True)

class SampleviewTable(tables.Table):
    class Meta:
        model = Sampleview
        #exclude = ['pname']
        managed = False
        db_table = 'test'
        verbose_name = "pizza"
        #sequence = ('gmc_clinic_id','clinical_sample_id','pid_fk','blood_specimen_id','blood_specimen_taken_dtm', 'tissue_specimen_id','tissue_specimen_taken_dtm','...')    # see http://django-tables2.readthedocs.org/en/latest/pages/swapping-columns.html
        orderable = True
        attrs = {"class": "paleblue"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

class Familyview(models.Model):

    family_id = models.CharField('Family No.', max_length=12, default='')
    pid = models.CharField('Participant ID', max_length=12, unique=True, default='')
    nhs = models.CharField('NHS', max_length=10,  blank=True, default='')
    pas = models.CharField('MRN', max_length=10,  blank=True, default='')
    forename = models.CharField('Forename', max_length=35, blank=True, default='')
    surname = models.CharField('Surname',max_length=35, blank=True, default='')
    sex = models.CharField('Gender',max_length=1, blank=True, default='')

    class Meta:
         ordering = ['family_id']

class FamilyviewTable(tables.Table):

    class Meta:
        model = Familyview
        exclude = ['chi']
        managed = False
        orderable = True
        attrs = {"class": "paleblue"}

class Sampleviewomic(models.Model):

    clinical_sample_id = models.CharField('Sample set ID', max_length=14, unique=True)
    gmc_clinic_id = models.CharField('Clinic ID', max_length=10, blank=True, default='')
    omic_sample_id = models.CharField('Omic sample ID',max_length=15, null=True, blank=True)
    omic_sample_rack_well = models.CharField('Omic sample rack well',max_length=20, null=True, blank=True)
    omic_sample_type = models.CharField('Omic sample type',max_length=30, null=True, blank=True)
    gmc_omic_lab_id = models.CharField('GMC omic lab ID', max_length=10, null=True, blank=True)
    omic_lab_method = models.CharField('Laboratory method', max_length=50, null=True, blank=True)
    omic_sample_sent_date = models.DateTimeField('Omic samples sent date', null=True, blank=True)
    omic_sample_consignment_number = models.CharField('Consignment number',max_length=20, null=True, blank=True)
    omic_sample_rack_id = models.CharField('Rack ID',max_length=20, null=True, blank=True)
    omic_volume_for_sending = models.PositiveSmallIntegerField('Volume for sending (\u03bcl)', null=True, blank=True)
    omic_volume_for_banking = models.PositiveSmallIntegerField('Volume for banking (\u03bcl)', null=True, blank=True)
    data_ready = models.CharField(max_length=1, null=True, blank=True)
    rack_ready = models.CharField(max_length=1, null=True, blank=True)
    file_ready = models.CharField(max_length=1, null=True, blank=True)
    file_sent = models.CharField(max_length=1, null=True, blank=True)
    family_ready = models.CharField('family ready', max_length=1, null=True, blank=True)

class SampleviewomicTable(tables.Table):
    class Meta:
        model = Sampleviewomic
        exclude = ['gmc_clinic_id','gmc_omic_lab_id','omic_lab_method','omic_volume_for_sending','omic_volume_for_banking']
        managed = False
        #db_table = 'test'
        #verbose_name = "pizza"
        #sequence = ('gmc_clinic_id','clinical_sample_id','pid_fk','blood_specimen_id','blood_specimen_taken_dtm', 'tissue_specimen_id','tissue_specimen_taken_dtm','...')    # see http://django-tables2.readthedocs.org/en/latest/pages/swapping-columns.html
        orderable = True
        attrs = {"class": "paleblue"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

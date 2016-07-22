# Create your models here.

import datetime
from django.db import models
from django.utils import timezone
from django import forms
from django.forms import ModelForm
import django_tables2 as tables
from ModelConfig import *



class DemogsManager(models.Manager):
    def get_queryset(self):
        return super(DemogsManager, self).get_queryset().filter(location='CUH')

class Family(models.Model):
    family_id = models.CharField('Family ID', max_length=12, unique=True, default='')
    family_expected_number  = models.PositiveSmallIntegerField('Family expected number', null=True, blank=True)

class Demogs(models.Model):

    #objects = DemogsManager()

    db_table = 'geldbx_demogs'

    sex_choices = (('1', 'Male'), ('2', 'Female'), ('X', 'Not known'), ('9', 'Not specified'))
    ethnicity_choices = (
        ('A', 'White: British'), ('B', 'White: Irish'),('C', 'White: Any other White background'),('D', 'Mixed: White and Black Caribbean'),('E', 'Mixed: White and Black African'),
        ('F', 'Mixed: White and Asian'),('G', 'Mixed: Any other mixed background'),('H', 'Asian or Asian British: Indian'),('J', 'Asian or Asian British: Pakistani'),('K', 'Asian or Asian British: Bangladeshi'),
        ('L', 'Asian or Asian British: Any other Asian background'),('M', 'Black or Black British: Caribbean'),('N', 'Black or Black British: African'),('P', 'Black or Black British: Any other Black background'),
        ('R', 'Other Ethnic Groups: Chinese'),('S', 'Other Ethnic Groups: Any other ethnic group'),('Z', 'Not stated')
    )
    pheno_choices = (('1', 'Male'), ('2', 'Female'), ('9', 'Indeterminate'))
    yesNoUnk_choices = (('Y', 'Yes'), ('N', 'No'), ('9', 'Unknown'))

    pid = models.CharField('Participant ID', max_length=12, unique=True, default='')
    nhs = models.CharField('NHS', max_length=10,  blank=True, default='')
    chi = models.CharField('CHI', max_length=10,  blank=True, default='')
    pas = models.CharField('MRN', max_length=10,  blank=True, default='')
    surname = models.CharField('Surname',max_length=35, blank=True, default='')
    forename = models.CharField('Forename', max_length=35, blank=True, default='')
    sex = models.CharField('Stated gender',max_length=1, choices=sex_choices, blank=True, default='')
    ethnicity = models.CharField(max_length=1, choices=ethnicity_choices, blank=True, default='')
    consent_date = models.DateField('Date consented', null=True)
    consent_status =  models.CharField('Status',max_length=20, blank=True, default='')
    last_update_epic = models.DateTimeField('Last updated', null=True, blank=True)
    pisform = models.BooleanField('Consent form and PIS used', default=False, blank=True)
    icd10 = models.CharField(max_length=10, blank=True, default='')
    sampleid = models.CharField('Sample ID', max_length=10, blank=True, default='')
    surname_birth = models.CharField('Surname at birth',max_length=35, blank=True, default='')
    sex_pheno = models.CharField('Birth gender', max_length=1, choices=pheno_choices, blank=True, default='')
    dob = models.DateField('Date of Birth', blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, default='')
    telephone_home = models.CharField('Telephone (home)', max_length=15, blank=True, default='')
    telephone_mob =  models.CharField('Telephone (mob)', max_length=15, blank=True, default='')
    address1 =  models.CharField('Address',max_length=60, blank=True, default='')
    address2 =  models.CharField('<br>', max_length=60, blank=True, default='')
    address3 =  models.CharField('<br>',max_length=60, blank=True, default='')
    address4 =  models.CharField('<br>',max_length=60, blank=True, default='')
    address5 =  models.CharField('<br>',max_length=60, blank=True, default='')
    postcode =  models.CharField('Postcode',max_length=10, blank=True, default='')
    ethnic_origin_mat = models.CharField('Ethnic origin',max_length=1, choices=ethnicity_choices, blank=True, default='')
    ethnic_origin_pat = models.CharField('Ethnic origin',max_length=1, choices=ethnicity_choices, blank=True, default='')
    ethnic_origin_other_mat = models.CharField('Ethnic origin (other)',max_length=1, choices=ethnicity_choices, blank=True, default='')
    ethnic_origin_other_pat = models.CharField('Ethnic origin (other)',max_length=1, choices=ethnicity_choices, blank=True, default='')
    ancestry_mat = models.CharField('Ancestry', max_length=60, blank=True, default='')
    ancestry_pat = models.CharField('Ancestry', max_length=60, blank=True, default='')
    famhist_brtova_mat =  models.CharField('Breast/Ovarian', max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_brtova_pat =  models.CharField('Breast/Ovarian', max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_colo_mat =  models.CharField('Ccolorectal',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_colo_pat =  models.CharField('Colorectal',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_isch_mat =  models.CharField('Ischaemic heart disease', max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_isch_pat =  models.CharField('Ischaemic heart disease', max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_endo_mat =  models.CharField('Endochrine tumours',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_endo_pat =  models.CharField('Endochrine tumours',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_other_mat =  models.CharField('Other history',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    famhist_other_pat =  models.CharField('Other history',max_length=1, choices=yesNoUnk_choices, blank=True, default='')
    demog_conflict = models.CharField('Conflict',max_length=10, blank=True, default='')
    location = models.CharField('Location',max_length=5, blank=True, default='')
    family_id = models.CharField('Family No.', max_length=12, default='')

    def __str__(self):              # tells python how the display this object - this is an example of adding behaviour to models!
        return self.PID

    class Meta:
        ordering = ['surname', 'forename'] # default ordering

class DemogsTable(tables.Table):

    #name=tables.column(order_by=("pid"))

    class Meta:

        model = Demogs
        db_table = 'geldbx_demogs'
        exclude = ['location','pisform','sampleid','id','surname_birth','sex_pheno','email','telephone_home','telephone_mob','ethnicity',
                   'address1','address2','address3','address4','address5','postcode', 'ethnic_origin_mat', 'ethnic_origin_pat', 'ethnic_origin_other_mat',
                   'ethnic_origin_other_pat', 'ancestry_mat', 'ancestry_pat', 'famhist_brtova_mat', 'famhist_brtova_pat', 'famhist_colo_mat',
                   'famhist_colo_pat', 'famhist_isch_mat', 'famhist_isch_pat', 'famhist_endo_mat', 'famhist_endo_pat', 'famhist_other_mat',
                   'famhist_other_pat','icd10','consent_date','last_update_epic']
        orderable = True
        order_by="pid"                                    # see http://django-tables2.readthedocs.org/en/latest/pages/api-reference.html
        sequence = ("pid","forename","surname","pas","nhs","chi","dob","sex")
        attrs = {"id":"demogstable","class": "paleblue"}  # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

class Sample(models.Model):

    tumour_type_choices = ('Primary', 'Primary'),('Metastatic', 'Metastatic'),('Recurrence', 'Recurrence'),
    tumour_content_choices = ('Low','Low (<30%)'),('Medium','Medium (30-50%)'),('High','High (>50%)'),
    sample_type_choices = ('DNA Blood Germline','DNA Blood Germline (CONSTUTIONAL DNA)'), ('DNA Saliva','DNA Saliva (CONSTITUTIONAL DNA)'), \
    ('DNA FF Germline','DNA FF Germline (CONSTITUTIONAL DNA) - non tumour tissue'), ('DNA FFPE Tumour','DNA FFPE Tumour (TUMOUR DNA)'),\
    ('DNA FF Tumour','DNA FF Tumour (TUMOUR DNA)'), \
    ('DNA Blood Tumour','DNA Blood from blood in Haematological malignancy Tumour (TUMOUR DNA)'), \
    ('EDTA Plasma','EDTA Plasma (OMICS SAMPLES)'), ('LiHep Plasma','LiHep Plasma (OMICS SAMPLES)'), \
    ('Tumour Scrapings','FFPE Tumour scrapings or slides (OMICS)'), ('Serum','Serum (OMICS SAMPLES)'), \
    ('RNA Blood','RNA Blood (OMICS SAMPLES)'), ('Buffy Coat','Buffy Coats (OMICS SAMPLES)'), \
    ('Lysed Tumour Cells','Deparaffinised Lysed Tumour Cells in RNA-stabilised buffer  (OMICS SAMPLES)')
    time_choices = ('less than 2 min', '<2 min'),('2 to 10 min', '2-10 mins'),('10 to 20 min', '10-20 mins'),('20 to 30 min', '20-30 mins'),('30 to 60 min', '30-60 mins'),('greater than 60 min', '>60 mins'),('unknown', 'Unknown'),
    time_choices_ffpe = ('less than 12 hours', '<12 hrs'),('12 to 24 hours', '12-24 hrs'),('24 to 48 hours', '24-48 hrs'),('more than 48 hours', '48-72 hrs'),('more than 72 hours', '>72 hrs'),('unknown', 'Unknown')
    #schedule_choices = ('urgent','Urgent (same day)'),('overnight','Overnight'),('extended','Extended (>24 hrs)'),('extra_large_program','Extra large program')
    schedule_choices = ('urgent','Rapid run'),('overnight','Overnight'),('urgent','Urgent'),('extended','Extended (>48hrs)'),('extra_large_program','Extra large program')
    cellularity_choices = ('Very Low','Very low (<700)'),('Low','Low (<4000)'),('Medium','Medium (4000-10000)'),('High','High (> 10000)'),('Very High','Very high (>50000'),('Unknown','Unknown')
    cellularity_choices_froz = ('Very Low','Very low (<700)'),('Low','Low (<4000)'),('Medium','Medium (4000-10000)'),('High','High (> 10000)'),('Very High','Very high (>50000'),('Unknown','Unknown')
    sect_type_choices = ('FFPE','Formalin fixed'),('FF','Fresh frozen'),
    provenance_choices = ('USS-guided biopsy','USS-guided biopsy'),('non-guided biopsy','Non-guided biopsy'),('CT-guided biopsy','CT-guided biopsy'),\
    ('endoscopic biopsy','Endoscopic biopsy'),('surgical resection','Surgical resection'), ('Stereotactically guided biopsy','Stereotactically guided biopsy'), ('MRI-guided biopsy','MRI-guided biopsy')
    excision_margin_choices = ('01','Margins are clear (distance from margin not stated)'),('02','Margins are clear (tumour >5mm from the margin)'),('03','Margins are clear (tumour >1mm but <=5mm from the margin'),('04','Tumour is <=1mm the margin, but does not reach margin'),('05','Tumour reaches excision margin'),('06','Uncertain'),('07','Margin not involved =>1mm'),('08','Margin not involved <1mm'),('09','Margin not involved 1-5mm'),('98','Not applicable'),('99','Not known')
    yes_no_choices = ('Y','Yes'),('N','No')
    no_yes_choices = ('N','No'),('Y','Yes')
    pass_fail_choices = ('Pass','Pass'),('Fail','Fail')
    storage_choices = ('refrigeration','Refrigeration (2-8 C)'),('vac_pack','Vacuum pack at room temperature'),('refrigeration_and_vac_pack','Refrigeration (2-8 C) and vacuum pack'),('room_temp','Room temperature')
    tumour_sample_type_choices = (('sections','Sections'),('cores','Cores'),('scrolls','Scrolls'),('blocks','Blocks'))
    blood_lab_method_choices = (('Gel_SOP469 v1.0','Gel_SOP469 v1.0'),('v1','v1 of GEL sample protocol'),('v2','v2 of GEL sample protocol'))
    tissue_lab_method_choices = (('v1','v1 of GEL sample protocol'),('v2','v2 of GEL sample protocol'),('v3','v3 of GEL sample protocol'))
    ff_extract_method_choices = (('CMDL_LP_003_DNA v1.0','CMDL_LP_003_DNA v1.0'),('fresh_frozen','Fresh frozen'))
    ffpe_extract_method_choices = (('CMDL_LP_020_DNA v1.0','CMDL_LP_020_DNA v1.0'),('Covaris','GEL Covaris 65 (FFPE)'),('Qiagen_80','GEL Qiagen 80 (FFPE)'),('Qiagen_90','GEL Qiagen 90 (FFPE)'))
    tumour_site_choices = ('b','Breast'),('c','Colorectal'),('o','Ovarian'),('p','Prostate')
    topography_choices = ('T04000', 'Breast'), ('T04040', 'Male breast'), ('T04100', 'Nipple'), ('TY81001', 'Axilla'), ('T87000', 'Ovary')
    morphology_choices = ('M81403','Breast - adenocarcinoma NOS'),('M89823','Breast - adenomyoepithelioma malignant'),('M91203','Breast - angiosarcoma'),('M85002','Breast - carcinoma ductal in situ NOS'),('M85732','Breast - apocrine DCIS'),('M82402','Breast - neuroendocrine DCIS'),('M82602','Breast - aarcinoma papillary in situ/encysted'),('M85202','Breast - carcinoma lobular in situ'),('M82003','Breast - carcinoma adenoid cystic'),('M85603','Breast - carcinoma adenosquamous'),('M85733','Breast - carcinoma apocrine'),('M83103','Breast - carcinoma clear cell'),('M83013','Breast - carcinoma cribriform'),('M85003','Breast - carcinoma infiltrating ductal/NST'),('M85203','Breast - carcinoma infiltrating lobular'),('M85103','Breast - carcinoma medullary'),('M80333','Breast - carcinoma metaplastic'),('M80106','Breast - carcinoma metastatic'),('M80715','Breast - carcinoma microinvasive'),('M85303','Breast - carcinoma inflammatory'),('M85033','Breast - carcinoma invasive micropapillary'),('M84803','Breast - carcinoma mucinous'),('M84303','Breast - carcinoma mucoepidermoid'),('M85623','Breast - carcinoma myoepithelial'),('M82403','Breast - carcinoma neuroendocrine'),('M82603','Breast - carcinoma papillary invasive'),('M85023','Breast - carcinoma secretory'),('M84903','Breast - carcinoma signet ring'),('M80323','Breast - carcinoma spindle cell'),('M82113','Breast - carcinoma tubular'),('M85213','Breast - carcinoma tubular mixed'),('M80203','Breast - carcinoma undifferentiated'),('M95903','Breast - lymphoma (extranodal)'),('M85403','Breast - Paget’s disease of nipple'),('M90203','Breast - phyllodes malignant'),('84413','Ovarian - serous adenocarcinoma'),('84613','Ovarian - serous surface papillary adenocarcinoma'),('90143','Ovarian - serous adenocarcinofibroma'),('84421','Ovarian - serous borderline'),('84621','Ovarian - serous papillary cystic tumour'),('84631','Ovarian - serous surface papillary tumour'),('90141','Ovarian - serous adenofibroma and cystadenofibroma'),('84803','Ovarian - mucinous adenocarcinoma'),('90153','Ovarian - mucinous adenocarcinofibroma'),('84721','Ovarian - mucinous borderline'),('83803','Ovarian - endometrioid adenocarcinoma NOS'),('83813','Ovarian - endometrioid adenocarcinofibroma'),('89503','Ovarian - endometrioid malignant Mullerian mixed tumour'),('89333','Ovarian - endometrioid adenosarcoma'),('89313','Ovarian - endometrioid endometrioid stromal sarcoma (low grade)'),('88053','Ovarian - endometrioid undifferentiated sarcoma'),('83801','Ovarian - endometrioid cystic tumour'),('83811','Ovarian - endometrioid adenofibroma and cystadenofibroma'),('83103','Ovarian - clear cell adenocarcinoma'),('83133','Ovarian - clear cell adenocarcinofibroma'),('83101','Ovarian - clear cell cystic tumour'),('83130','Ovarian - clear cell adenofibroma and cystadenofibroma'),('81203','Ovarian - transitional cell carcinoma (non-Brenner type)'),('90003','Ovarian - transitional cell malignant Brenner tumour'),('90011','Ovarian - transitional cell borderline Brenner tumour'),('90011','Ovarian - transitional cell proliferating variant'),('80703','Ovarian - squamous cell carcinoma'),('83233','Ovarian - mixed epithelial malignant'),('83231','Ovarian - mixed epithelial borderline'),('80203','Ovarian - undifferentiated carcinoma'),('81403','Ovarian - adenocarcinoma NOS')
    fixative_type_choices = ('Formal saline','Formal saline'),('Neutral buffered formalin','Neutral buffered formalin'),('UMFix','UMFix'),('Paxgene','Paxgene'),('Other','Other')
    not_sent_reason_choices = ('Tumour sample not taken','Tumour sample not taken'),('Tumour type not eligible','Tumour type not eligible'),\
    ('Poorly cellular tumour','Poorly cellular tumour'),('Insufficient tumour post neoadjuvant chemotherapy','Insuff. tumour p.neoadj. chemo.'),\
    ('Insufficient DNA','Insufficient DNA'),('No Cancer Diagnosed','No cancer diagnosed')


    clinical_sample_id = models.CharField('Sample set ID', max_length=14, unique=True)
    gmc_clinic_id = models.CharField('Clinic ID', max_length=10, blank=True, default='')
    blood_specimen_id = models.CharField('Blood specimen ID',max_length=15, null=True, blank=True)
    tissue_specimen_id = models.CharField('Tissue specimen ID',max_length=15, null=True, blank=True)
    ff_sample_id = models.CharField('Fresh frozen sample ID',max_length=15, null=True, blank=True)
    ff_sample_type = models.CharField('Tumour sample type',max_length=10, choices=tumour_sample_type_choices, null=True, blank=True)
    ff_sample_type_count = models.PositiveSmallIntegerField('sample type count', null=True, blank=True)
    ff_sample_type_measure = models.DecimalField('sample type measure', max_digits=4, decimal_places=1, null=True, blank=True)
    ff_dna_sample_id = models.CharField('FluidX tube ID',max_length=10, null=True, blank=True)
    ff_dna_sample_rack_well = models.CharField('FF DNA sample rack well',max_length=20, null=True, blank=True)
    ff_dna_extraction_method = models.CharField('Extraction method', max_length=50, choices=ff_extract_method_choices, null=True, blank=True)
    ff_dna_volume_for_sending = models.PositiveSmallIntegerField('Volume for sending (µl)', null=True, blank=True)
    ff_dna_volume_for_banking = models.PositiveSmallIntegerField('Volume for banking (µl)', null=True, blank=True)
    ff_dna_qubit = models.DecimalField('Qubit (ng/ul)', max_digits=4, decimal_places=1, null=True, blank=True)   # μ
    ff_dna_qubit_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ff_dna_delta_cq = models.PositiveSmallIntegerField('Delta Cq', null=True, blank=True)
    ff_dna_delta_cq_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ff_dna_agarose = models.CharField('Agarose', max_length=4, choices=pass_fail_choices, null=True, blank=True)
    ff_dna_agarose_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ff_dna_summary = models.CharField('Summary', max_length=4, choices=pass_fail_choices, null=True, blank=True)
    ff_dna_summary_dtm = models.DateTimeField('Summary time', null=True, blank=True)
    ff_snap_freezing_start_dtms = models.DateTimeField('FF snap start - label set in forms', null=True, blank=True)
    ff_snap_freezing_end_dtms = models.DateTimeField('FF snap end - label set in forms', null=True, blank=True)
    ff_section_cut_by = models.CharField('Section cut by', max_length=50, null=True, blank=True)
    ff_section_cut_date = models.DateField('Section cut date', null=True, blank=True)
    ff_section_assessed_by = models.CharField('Section assessed by', max_length=50, null=True, blank=True)
    ff_section_assessed_date = models.DateField('Section assessed date', null=True, blank=True)
    ff_used = models.CharField('Fresh frozen used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    ff_dna_used = models.CharField('DNA used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    ff_dna_lab_method = models.CharField('Laboratory method', max_length=50, choices=tissue_lab_method_choices, null=True, blank=True)
    ffpe_sample_id = models.CharField('Formalin fixed sample ID',max_length=15, null=True, blank=True)
    ffpe_sample_type = models.CharField('Tumour sample type',max_length=10, choices=tumour_sample_type_choices, null=True, blank=True)
    ffpe_sample_type_count = models.PositiveSmallIntegerField('sample type count', null=True, blank=True)
    ffpe_sample_type_measure = models.DecimalField('sample type measure', max_digits=4, decimal_places=1, null=True, blank=True)
    ffpe_dna_qubit = models.DecimalField('Qubit (ng/ul)', max_digits=4, decimal_places=1, null=True, blank=True)
    ffpe_dna_qubit_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ffpe_dna_delta_cq = models.PositiveSmallIntegerField('Delta Cq', null=True, blank=True)
    ffpe_dna_delta_cq_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ffpe_dna_agarose = models.CharField('Agarose', max_length=4, choices=pass_fail_choices, null=True, blank=True)
    ffpe_dna_agarose_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    ffpe_dna_summary = models.CharField('Summary', max_length=4, choices=pass_fail_choices, null=True, blank=True)
    ffpe_dna_summary_dtm = models.DateTimeField('Summary time', null=True, blank=True)
    ffpe_fixation_start_dtm = models.DateTimeField('Fixation start time', null=True, blank=True)
    ffpe_fixation_end_dtm = models.DateTimeField('Fixation end time', null=True, blank=True)
    ffpe_fixative_type = models.CharField('Fixative type',max_length=50, choices=fixative_type_choices, null=True, blank=True, default='Neutral buffered formalin')
    ffpe_fixation_comments = models.CharField('Fixation comments',max_length=100, null=True, blank=True)
    #ffpe_time_in_formalin = models.DecimalField('Time in formalin on processor', max_digits=4, decimal_places=1, null=True, blank=True)
    ffpe_time_in_formalin = models.CharField('Time in formalin on processor', max_length=5, null=True, blank=True)
    ffpe_processing_schedule = models.CharField('Processing schedule', max_length=30, choices=schedule_choices, null=True, blank=True)
    ffpe_slide_marked_by = models.CharField('Slide marked by', max_length=50, null=True, blank=True)
    ffpe_slide_marked_date = models.DateField('Slide marked date', null=True, blank=True)
    ffpe_dna_extraction_method = models.CharField('Extraction method', max_length=50, choices=ffpe_extract_method_choices, null=True, blank=True)
    ffpe_dna_volume_for_sending = models.PositiveSmallIntegerField('Volume for sending (µl)', null=True, blank=True)
    ffpe_dna_volume_for_banking = models.PositiveSmallIntegerField('Volume for banking (µl)', null=True, blank=True)
    ffpe_dna_sample_id = models.CharField('DNA FluidX tube ID',max_length=10, null=True, blank=True)
    ffpe_dna_sample_rack_well = models.CharField('FFPE DNA sample rack well',max_length=20, null=True, blank=True)
    ffpe_used = models.CharField('Formalin fixed used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    ffpe_dna_used = models.CharField('DNA used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    ffpe_dna_lab_method = models.CharField('Laboratory method', max_length=50, choices=tissue_lab_method_choices, null=True, blank=True)
    blood_dna_sample_id = models.CharField('FluidX tube ID',max_length=10, null=True, blank=True)
    blood_specimen_taken_dtm = models.DateTimeField('Blood specimen taken time', null=True, blank=True)
    blood_dna_sample_rack_well = models.CharField('Blood DNA sample rack well',max_length=20, null=True, blank=True)
    blood_dna_extraction_method = models.CharField('Blood DNA extraction method', max_length=50, null=True, blank=True)
    blood_dna_volume_for_sending = models.PositiveSmallIntegerField('Volume for sending (µl)', null=True, blank=True)
    blood_dna_volume_for_banking = models.PositiveSmallIntegerField('Volume for banking (µl)', null=True, blank=True)
    blood_dna_trinean_od_260_280 = models.DecimalField('Trinean OD 260/280', max_digits=4, decimal_places=2, null=True, blank=True)
    blood_dna_trinean_od_260_280_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    blood_dna_nanodrop_concentration = models.DecimalField('NanoDrop conc. (ng/µl)', max_digits=4, decimal_places=1, null=True, blank=True)
    blood_dna_nanodrop_concentration_result_dtm = models.DateTimeField('Result time', null=True, blank=True)
    blood_dna_summary = models.CharField('Summary', max_length=4, choices=pass_fail_choices, null=True, blank=True)
    blood_dna_summary_dtm = models.DateTimeField('Summary time', null=True, blank=True)
    blood_dna_lab_method = models.CharField('Laboratory method', max_length=50, choices=blood_lab_method_choices, null=True, blank=True)
    tissue_specimen_taken_dtm = models.DateTimeField('Tissue specimen taken time', null=True, blank=True)
    haem_malignancy = models.CharField('Haematological malignancy', max_length=1, choices=no_yes_choices, null=True, blank=True)
    const_tissue_yn = models.CharField('Constitutional tissue', max_length=1, choices=no_yes_choices, null=True, blank=True)
    macrodissection_details = models.CharField('Macrodissection details', max_length=100, null=True, blank=True)
    macrodissection_used = models.CharField('Macrodissection used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    microdissection_details = models.CharField('Microdissection details', max_length=100, null=True, blank=True)
    microdissection_used = models.CharField('Microdissection used', max_length=1, choices=yes_no_choices, null=True, blank=True)
    #pid_fk = models.CharField('Participant ID', max_length=12,  blank=True, default='')
    pid_fk = models.ForeignKey(Demogs, to_field='pid', db_column="pid_fk", on_delete=models.CASCADE, verbose_name='Participant ID')
    lab_sample_sent = models.CharField('Samples to be sent', max_length=1, choices=yes_no_choices, null=True, blank=True)
    lab_sample_sent_date = models.DateTimeField('Samples to be sent date', null=True, blank=True)
    lab_sample_not_sent_reason = models.CharField('Samples not sent reason',max_length=60, choices=not_sent_reason_choices, null=True, blank=True)
    pathology_comments = models.CharField(max_length=100, null=True, blank=True)
    morphology = models.CharField(max_length=10, choices=morphology_choices, null=True, blank=True)
    topography = models.CharField(max_length=10, choices=topography_choices, null=True, blank=True)
    tumour_type = models.CharField(max_length=10, choices=tumour_type_choices, null=True, blank=True)
    tumour_size = models.PositiveSmallIntegerField('Tumour size (mm)',null=True, blank=True)
    tumour_content = models.CharField(max_length=6, choices=tumour_content_choices, null=True, blank=True)
    non_invasive_elements = models.CharField('Pre-invasive elements',max_length=50, null=True, blank=True)
    xml_status = models.CharField('Data and rack ready', max_length=1, null=True, blank=True)
    xml_generated_date = models.DateTimeField(null=True, blank=True)
    xml_sent_date = models.DateTimeField(null=True, blank=True)
    gmc_lab_id = models.CharField('GMC blood lab ID', max_length=10, null=True, blank=True)
    gmc_tissue_lab_id = models.CharField('GMC tissue lab ID', max_length=10, null=True, blank=True)
    lab_sample_consignment_number = models.CharField('Consignment number',max_length=20, null=True, blank=True)
    lab_sample_rack_id = models.CharField('Rack ID',max_length=20, null=True, blank=True)
    sample_provenance = models.CharField('Tissue source', max_length=30, choices=provenance_choices, null=True, blank=True)
    excision_margin = models.CharField(max_length=2, choices=excision_margin_choices, null=True, blank=True)
    biopsy_count = models.PositiveSmallIntegerField('Number of biopsies', null=True, blank=True)
    biopsy_guage =  models.PositiveSmallIntegerField('Gauge of biopsies', null=True, blank=True)
    prolonged_sample_storage = models.CharField('Prolonged sample storage', max_length=30, choices=storage_choices, null=True, blank=True)
    data_ready = models.CharField(max_length=1, null=True, blank=True)
    rack_ready = models.CharField(max_length=1, null=True, blank=True)
    file_ready = models.CharField(max_length=1, null=True, blank=True)
    file_sent = models.CharField(max_length=1, null=True, blank=True)
    family_ready = models.CharField(max_length=1, null=True, blank=True)
    #dna_quality = models.CharField('DNA quality', max_length=10, choices=dna_quality_choices, null=True, blank=True)



    def __str__(self):
        return self.clinical_sample_id

    class Meta:
        ordering = ['pid_fk', 'clinical_sample_id'] # default ordering

class SampleOmic(models.Model):

    sample_type_choices = ('DNA Blood Germline','DNA Blood Germline (CONSTUTIONAL DNA)'), ('DNA Saliva','DNA Saliva (CONSTITUTIONAL DNA)'), \
    ('DNA FF Germline','DNA FF Germline (CONSTITUTIONAL DNA) - non tumour tissue'), ('DNA FFPE Tumour','DNA FFPE Tumour (TUMOUR DNA)'),\
    ('DNA FF Tumour','DNA FF Tumour (TUMOUR DNA)'), \
    ('DNA Blood Tumour','DNA Blood from blood in Haematological malignancy Tumour (TUMOUR DNA)'), \
    ('EDTA Plasma','EDTA Plasma (OMICS SAMPLES)'), ('LiHep Plasma','LiHep Plasma (OMICS SAMPLES)'), \
    ('Tumour Scrapings','FFPE Tumour scrapings or slides (OMICS)'), ('Serum','Serum (OMICS SAMPLES)'), \
    ('RNA Blood','RNA Blood (OMICS SAMPLES)'), ('Buffy Coat','Buffy Coats (OMICS SAMPLES)'), \
    ('Lysed Tumour Cells','Deparaffinised Lysed Tumour Cells in RNA-stabilised buffer  (OMICS SAMPLES)')
    tissue_lab_method_choices = (('v1','v1 of GEL sample protocol'),('v2','v2 of GEL sample protocol'))

    sample_table_fk = models.ForeignKey(Sample, on_delete=models.CASCADE)
    omic_sample_id = models.CharField('Omic sample ID',max_length=15, null=True, blank=True)
    omic_sample_type = models.CharField('Omic sample type',max_length=30, choices=sample_type_choices, null=True, blank=True)
    gmc_omic_lab_id = models.CharField('GMC omic lab ID', max_length=10, null=True, blank=True)
    omic_lab_method = models.CharField('Laboratory method', max_length=50, choices=tissue_lab_method_choices, null=True, blank=True)
    omic_volume_for_sending = models.PositiveSmallIntegerField('Volume for sending (µl)', null=True, blank=True)
    omic_volume_for_banking = models.PositiveSmallIntegerField('Volume for banking (µl)', null=True, blank=True)
    omic_sample_consignment_number = models.CharField('Consignment number',max_length=20, null=True, blank=True)
    omic_sample_rack_id = models.CharField('Rack ID',max_length=20, null=True, blank=True)
    omic_sample_rack_well = models.CharField('Omic sample rack well',max_length=20, null=True, blank=True)
    omic_sample_sent_date = models.DateTimeField('Omic samples sent date', null=True, blank=True)
    data_ready = models.CharField(max_length=1, null=True, blank=True)
    rack_ready = models.CharField(max_length=1, null=True, blank=True)
    file_ready = models.CharField(max_length=1, null=True, blank=True)
    file_sent = models.CharField(max_length=1, null=True, blank=True)

class RackException(models.Model):
        sample_rack_id = models.CharField('Rack ID',max_length=20, null=True, blank=True)
        sample_id = models.CharField('FluidX tube ID',max_length=10, null=True, blank=True)
        sample_rack_well = models.CharField('Rack well',max_length=20, null=True, blank=True)

class audit(models.Model):
    log_dtm  = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=20, null=True, blank=True)
    event = models.CharField(max_length=20, null=True, blank=True)
    data_key = models.CharField(max_length=30, null=True, blank=True)
    data_updated = models.CharField(max_length=500, null=True, blank=True)

class SampleTable(tables.Table):
    class Meta:
        model = Sample
        exclude = SampleTableExclude

        sequence = ('gmc_clinic_id','clinical_sample_id','pid_fk','blood_specimen_id','blood_specimen_taken_dtm', 'tissue_specimen_id','tissue_specimen_taken_dtm','...')    # see http://django-tables2.readthedocs.org/en/latest/pages/swapping-columns.html

        orderable = True

        attrs = {"class": "paleblue"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

class SampleCollationTable(tables.Table):
    class Meta:
        model = Sample
        exclude = SampleCollationTableExclude
        ordering = ['clinical_sample_id']
        sequence = ('clinical_sample_id','blood_dna_sample_id','blood_dna_sample_rack_well','ff_dna_sample_id','ff_dna_sample_rack_well','ffpe_dna_sample_id',
                    'ffpe_dna_sample_rack_well','lab_sample_sent_date','lab_sample_consignment_number','lab_sample_rack_id','data_ready','rack_ready','file_ready','file_sent')
        attrs = {"id":"collationtbl","class":"paleblue collation"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

class OmicsSampleCollationTable(tables.Table):
    class Meta:
        model = SampleOmic
        #exclude = OmicSampleCollationTableExclude
        ordering = ['omic_sample_id']
        sequence = ('omic_sample_id','omic_sample_rack_well','omic_sample_sent_date','omic_sample_consignment_number')
        attrs = {"class": "paleblue"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css

class RackExceptionTable(tables.Table):
    class Meta:
        model = RackException
        orderable = False
        ordering = ['sample_rack_id']
        attrs = {"id":"rackexcept","class": "paleblue"}   # see http://stackoverflow.com/questions/18822999/django-tables2-and-css


class Params(models.Model):
    org_code = models.CharField(max_length=5)
    hub_name = models.CharField('Collection Hub', max_length=20)
    gmc_clinic_id = models.CharField(max_length=20, blank=True)
    gmc_blood_lab_id = models.CharField(max_length=20, blank=True)
    gmc_tissue_lab_id = models.CharField(max_length=20, blank=True)
    xml_out = models.CharField(max_length=100, null=True, blank=True)
    XML_sent = models.CharField(max_length=100, null=True, blank=True)
    XML_ftp = models.CharField(max_length=100, null=True, blank=True)
    temp  = models.CharField('temp', max_length=20, null=True)
    epic_last_update = models.DateTimeField(null=True, blank=True)



    def __str__(self):              # __unicode__ on Python 2
        return self.org_code

class file_transfer_log(models.Model):
    log_type = models.CharField(max_length=30, blank=True, default='')
    log_time = models.DateTimeField(null=True, blank=True)
    file_path = models.CharField(max_length=100, blank=True, default='')
    user = models.CharField(max_length=35, blank=True, default='')
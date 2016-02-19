from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import csv

class ApiKey(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=50, blank=True)
    key = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return "%s - %s"%(self.name, self.key)
        
class ApiKeyAcceptValue(models.Model):
    api_key = models.ForeignKey(ApiKey, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    value = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return "%s : %s - %s"%(self.api_key.name, self.name, self.value)

class ProjectionSetting(models.Model):
    srid = models.IntegerField(help_text="A Spatial Reference System Identifier (SRID) is a unique value used to unambiguously identify projected, unprojected, and local spatial coordinate system definitions. You will get lat_prj, and lon_prj in your files")

    def __unicode__(self):
        return "projection %s"%(self.srid)

class ProjectField(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField(max_length=50, blank=True)
    match_option = models.CharField(max_length=30, blank=True, null=True,
                   help_text='(required) Select AddressID, Street, City, State, Zip',
                   choices=(('ADDRESS_ID', 'AddressID'),
                            ('STREET', 'Street'),
                            ('CITY', 'City'),
                            ('STATE', 'State'),
                            ('ZIP', 'Zip'),)
    )
    def __unicode__(self):
        return "%s - %s"%(self.name, self.match_option)

class Project(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    csv_file = models.FileField(upload_to='file_data')
    history_line = models.CharField(max_length=50, blank=True, default=0)
    finish_input_data = models.BooleanField(default=False)
    match_option = models.CharField(max_length=30, default='AUTO_UNMATCHED',
                   verbose_name="For addresses unmatched in ProvPlan's database:",
                   help_text='(required) Note: online services may return vague matches (e.g., "US" with lat/long in the middle of the country).',
                   choices=(('LEAVE_UNMATCHED', 'Leave unmatched for manual matching later'),
                            ('AUTO_UNMATCHED', 'Automatically attempt to match via online services'))
    )
    match_score = models.DecimalField(max_digits=11,decimal_places=2, blank=True, null=True, default=85,
                                     verbose_name="For addresses geo_score lower then this score in ProvPlan's database:",
                                     help_text='use online services geo_score will be blank')
    def save(self, *args, **kwargs):
        if ProjectField.objects.filter(project=self).count() == 0:
            try:
                f = open(self.csv_file.path, 'rb')
                reader = csv.reader(f)
                headers = reader.next()
                for i in headers:
                    try:
                       ProjectField.objects.get_or_create(project=self, name=i)
                    except:
                       pass
            except IOError:
                pass

        super(Project, self).save(*args, **kwargs)


class ProjectProjectionOption(models.Model):
    project = models.ForeignKey('Project')
    srid = models.ForeignKey(ProjectionSetting, help_text="A Spatial Reference System Identifier (SRID) is a unique value used to unambiguously identify projected, unprojected, and local spatial coordinate system definitions. You will get lat_prj, and lon_prj in your files")
    #srid = models.IntegerField(help_text="A Spatial Reference System Identifier (SRID) is a unique value used to unambiguously identify projected, unprojected, and local spatial coordinate system definitions. You will get lat_prj, and lon_prj in your files")

    def __unicode__(self):
        return "projection %s"%(self.srid)


class ProjectResult(models.Model):
    project = models.ForeignKey('Project')
    file_name = models.CharField(max_length=120, blank=True)
    total_records = models.IntegerField(default=0)
    result_file = models.FileField(blank=True, upload_to='result')
    created_at = models.DateTimeField(auto_now_add=True)
    #record_filter = models.ManyToManyField("Record", through=IndividualResultAddress, related_name="record_filter")
    #file_filter = models.ManyToManyField("File")
    quoting = models.CharField(max_length=30, blank=True, null=True,
                   help_text='Use QUOTE_NONNUMERIC for excel. https://docs.python.org/2/library/csv.html#csv.QUOTE_ALL',
                   choices=(('QUOTE_ALL', 'QUOTE_ALL'),
                            ('QUOTE_MINIMAL', 'QUOTE_MINIMAL'),
                            ('QUOTE_NONNUMERIC', 'QUOTE_NONNUMERIC'),
                            ('QUOTE_NONE', 'QUOTE_NONE'),
                            (None, 'NONE')),
                   default=None
    )
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.created_at)

class ProjectRecordIndex(models.Model):
    address_row_id = models.CharField(max_length=180, blank=True) #use file row number
    project = models.ForeignKey('Project')
    record = models.ForeignKey('Record')

    def __unicode__(self):
        return '%s - %s'%(self.address_row_id, self.project.name)

class Record(models.Model):
    project = models.ManyToManyField("Project", through=ProjectRecordIndex, related_name="project_filter", blank=True)
    user_defind_id = models.CharField(max_length=256, blank=True)

class RecordAddressIndex(models.Model):
    address_row_id = models.CharField(max_length=180, blank=True) #use file row number
    record = models.ForeignKey('Record')
    address = models.ForeignKey('Address')

    def __unicode__(self):
        return '%s - %s'%(self.address_row_id, self.project.name)

class Address(models.Model):
    record = models.ManyToManyField("Record", through=RecordAddressIndex, related_name="record_filter", blank=True)
    address_id = models.CharField(max_length=256, blank=True)
    street = models.CharField(max_length=80, blank=True)
    ignore_street = models.BooleanField(default=False)
    city = models.CharField(max_length=80, blank=True)
    ignore_city = models.BooleanField(default=False)
    state = models.CharField(max_length=80, blank=True)
    ignore_state = models.BooleanField(default=False)
    zip = models.CharField(max_length=80, blank=True)
    geo_score = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, help_text="Online Resource (GoogleV3, Bing, MapQuest) and User Edit own't have Geo score")
    geo_address = models.CharField(max_length=180, blank=True)
    geo_lat = models.CharField(max_length=80, blank=True, help_text="projection 4326")
    geo_lon = models.CharField(max_length=80, blank=True, help_text="projection 4326")
    coordinates = models.PointField(blank=True,null=True, geography=True)
    have_value = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    resource = models.CharField(max_length=80, blank=True, default="")

    def __unicode__(self):
       return '%s'%(self.address_id)
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task
from geocode.models import ProjectField, Project, Record, Address
import csv

@shared_task
def ImportTask(project=None, project_id=None):
    if project_id != None:
       project = Project.objects.get(id=project_id)
    path = project.csv_file.path
    
    fields = ProjectField.objects.filter(project=project)
    
    user_defind_id = fields.get(match_option="ADDRESS_ID").name
    street = fields.get(match_option="STREET").name
    city = fields.get(match_option="CITY").name
    state = fields.get(match_option="STATE").name
    zip = fields.get(match_option="ZIP").name
    

    with open(path) as f:
        reader = csv.reader(f)
        headers = reader.next()
        
        user_defind_id_index = headers.index(user_defind_id)
        street_index = headers.index(street)
        city_index = headers.index(city)
        state_index = headers.index(state)
        zip_index = headers.index(zip)
        
        print user_defind_id_index, street_index, city_index, state_index, zip_index
        
        
        for row in reader:
            print "--- Import Row ---"
            print "User Address ID: %s"%row[user_defind_id_index]
            print "Street: %s"%row[street_index]
            print "City: %s"%row[city_index]
            print "State: %s"%row[street_index]
            print "zip: %s"%row[zip_index]
            
            record = Record(project=project, user_defind_id=row[user_defind_id_index]).save()
            address_id = "%s %s %s %s"%(row[street_index], row[city_index], row[state_index],row[zip_index])
            address_id = address_id.lower()
            address, created = Address.objects.get_or_create(
                record=record,
                address_id = address_id
                )
            if created:
                address.street = row[street_index]
                address.city = row[city_index]
                address.state = row[state_index]
                address.zip = row[zip_index]
                address.geo_score = -1
                address.save()
            
        
    
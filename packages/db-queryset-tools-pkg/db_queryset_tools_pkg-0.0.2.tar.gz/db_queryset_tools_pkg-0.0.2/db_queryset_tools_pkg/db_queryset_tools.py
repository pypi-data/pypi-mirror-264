import json
import datetime
import logging

# Custom JSON encoder
class DTENC(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DTENC, self).default(obj)

class DB_queryset_tools:
    
    # Logger configuration
    log = logging.getLogger(__name__)
        
    # convert queryset to list
    def queryset_to_list(self, queryset):
        try:
            if(queryset.__class__.__name__  != 'QuerySet'):
                self.log.error('Invalid queryset type %s', queryset.__class__.__name__ )
                raise Exception('Invalid queryset')
            else:
                return list(queryset.values())
        except Exception as e:
            return e
    
    # convert queryset to dictionary
    def queryset_to_dict(self, queryset):
        try:
            if(queryset.__class__.__name__  != 'QuerySet'):
                self.log.error('Invalid queryset type %s', queryset.__class__.__name__ )
                raise Exception('Invalid queryset')
            else:
                return {item.id: item for item in queryset}
        except Exception as e:
            return e

    # convert queryset to json
    def queryset_to_json(self, queryset):
        try:
            if(queryset.__class__.__name__  != 'QuerySet'):
                self.log.error('Invalid queryset type %s', queryset.__class__.__name__ )
                raise Exception('Invalid queryset')
            else:
                return json.dumps(list(queryset.values()),cls=DTENC)
        except Exception as e:
            return e
        
    # get dataset for charts
    def get_dataset_for_charts(self,queryset,identifier_x=None,identifier_y=None):
        try:
            if(queryset.__class__.__name__  != 'QuerySet'):
                self.log.error('Invalid queryset type %s', queryset.__class__.__name__ )
                raise Exception('Invalid queryset')
            if(identifier_x.__class__.__name__  != 'str'):
                self.log.error('Invalid identifier_x type %s Expected string', identifier_x.__class__.__name__ )
                raise Exception('Invalid identifier_x')
            if(identifier_y.__class__.__name__  != 'str'):
                self.log.error('Invalid identifier_y type %s Expected string', identifier_y.__class__.__name__ )
                raise Exception('Invalid identifier_y')
            else:
            
                dataset1 = json.dumps([x[identifier_x].strftime('%B') for x in queryset],cls=DTENC)
                dataset2 = json.dumps([x[identifier_y] for x in queryset],cls=DTENC)
                return {
                    'dataset1': dataset1,
                    'dataset2': dataset2
                }
        except Exception as e:
            return e
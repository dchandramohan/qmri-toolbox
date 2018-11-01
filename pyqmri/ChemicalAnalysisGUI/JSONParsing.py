import json, collections
import datetime


def load_json(filepath):
    
    json_data = open(filepath).read()
    
    orig_data = json.loads(json_data, object_pairs_hook=collections.OrderedDict)
    
    new_data = collections.OrderedDict()

    for key in orig_data.keys():
        temp = collections.OrderedDict()
        temp1 = collections.OrderedDict()
        temp2 = collections.OrderedDict()
        
        temp2['C'] = 0.0
        temp2['H'] = 0.0
        temp2['N'] = 0.0

        temp1['combustion percent by mass'] = temp2
        temp1['percent water content by mass'] = 0.0
        temp1['physical density (g per cm3)'] = 0.0
    
        temp['data'] = temp1
        label = orig_data[key]['label']
        temp['label'] = label
        
        date = datetime.datetime.now()
        day = str(date.day)
        month = str(date.month)
        year = str(date.year)
        
        if len(day) == 1:
            day = "0" + day 
        elif len(month) == 1:
            month = "0" + month
            
        temp['date'] = "%s%s%s" % (year, month, day)
    
        new_data[key] = temp
            
    return json.dumps(new_data, indent=4, sort_keys=True)
    
def write_json(json_string):   
    return

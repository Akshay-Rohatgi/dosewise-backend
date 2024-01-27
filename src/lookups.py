import tools
import urllib.parse

def lookup_medicine_fda(name):
    return tools.get_data(f'https://api.fda.gov/drug/ndc.json?search=generic_name:"{name}"&limit=1')

def raw_get_medscape_info(name):
    return tools.get_data(f'https://www.medscape.com/api/quickreflookup/LookupService.ashx?q={name}&sz=500&type=10417&metadata=has-interactions&format=json')

def lookup_medicine_medscape(name):
    name = name.lower()
    if len(raw_get_medscape_info(name)["types"]) == 0:
        if len(raw_get_medscape_info(str(name.split()[0]))["types"]) == 0:
            return 'no results'
        else:
            return raw_get_medscape_info(str(name.split()[0]))["types"][0]["references"][0]["id"]
    else:
        return raw_get_medscape_info(name)["types"][0]["references"][0]["id"]
    
def get_interactions(med1, med2):
    med1 = lookup_medicine_medscape(med1)
    med2 = lookup_medicine_medscape(med2)

    if med1 == 'no results' or med2 == 'no results':
        return 'failed to lookup medicine in interactions database'
    data = tools.get_data(f'https://reference.medscape.com/druginteraction.do?action=getMultiInteraction&ids={med1},{med2}')
    if data["multiInteractions"] == []:
        return 'no interactions found!'
    else:
        return data["multiInteractions"][0]["text"]    

if __name__ == '__main__':
    #print(lookup_medicine_medscape('oseltamivir phosphate'))
    print(get_interactions('oseltamivir phosphate', 'ciprofloxacin'))
    print(get_interactions('Fluconazole', 'simvastatin'))
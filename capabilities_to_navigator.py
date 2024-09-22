import csv
import json
import getopt
import sys
import os
from datetime import datetime

def parse_csv(file_path):
  data_structure = {}
  
  with open(file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
      technique_id = row['ID']
      tactic = row['Tactic']
      capability = row['Level']
      influence_energy = int(row['IEL'])
      comment = row['Description']
      links = row['Examples']
      
      if technique_id not in data_structure:
        data_structure[technique_id] = {"tactic": tactic}
      
      data_structure[technique_id][capability] = {
        "required_energy": influence_energy,
        "description": comment,
        "examples": links.split(',') if links else []
      }
  
  return data_structure

# "T1620": {
#     "1 Public": {
#       "required_energy": 2,
#       "description": "",
#       "examples": []
#     },
#     "2 Altered": {
#       "required_energy": 4,
#       "description": "",
#       "examples": []
#     },
#     "3 Bespoke": {
#       "required_energy": 5,
#       "description": "",
#       "examples": []
#     }
#   }

def main(argv):
  file_path = ''
  energy_level = 0

  try:
    opts, args = getopt.getopt(argv, "l:", ["energy_level="])
  except getopt.GetoptError:
    print(f'{os.path.basename(__file__)} -l <energy_level> <capabilities_file>')
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-l", "--energy_level"):
      energy_level = int(arg)

  if len(args) != 1:
    print(f'{os.path.basename(__file__)} -l <energy_level> <capabilities_file>')
    sys.exit(2)

  file_path = args[0]

  output = parse_csv(file_path)

  navigator_techniques = []

  for technique_id, capabilities in output.items():
    enabled = True
    score = 0

    if capabilities["3 Bespoke"]["required_energy"] < 0 or capabilities["2 Altered"]["required_energy"] < 0 or capabilities["1 Public"]["required_energy"] < 0:
      enabled = False
    elif capabilities["1 Public"]["required_energy"] > energy_level:
      enabled = False
    elif capabilities["3 Bespoke"]["required_energy"] <= energy_level:
      capability_level = "3 Bespoke"
      score = 100
    elif capabilities["2 Altered"]["required_energy"] <= energy_level:
      capability_level = "2 Altered"
      score = 50
    elif capabilities["1 Public"]["required_energy"] <= energy_level:
      capability_level = "1 Public"
      score = 1

    tactics = capabilities["tactic"].split(', ')

    example_links = capabilities[capability_level]["examples"] if capabilities[capability_level]["examples"] else []
    example_links_array = [{"label": "example", "url": link.strip()} for link in example_links]

    for tactic in tactics:
      navigator_techniques.append({
        "techniqueID": technique_id,
        "tactic": tactic.lower().replace(' ', '-'),
        "score": score,
        "color": "",
        "comment": capabilities[capability_level]["description"] if capabilities[capability_level]["description"] else "",
        "links": example_links_array,
        "enabled": enabled,
        "metadata": [{"name": "capability_level", "value": capability_level.split(' ')[1]}],
        "showSubtechniques": False
      })

  layer_template_path = os.path.join(os.path.dirname(file_path), 'layer_template.json')
  layer_output_path = os.path.join(os.path.dirname(file_path), 'ie' + str(energy_level) + '_layer.json')

  with open(layer_template_path, 'r') as template_file:
    layer_template = json.load(template_file)

  layer_template['techniques'] = navigator_techniques
  layer_template['name'] = 'Influence Energy Level ' + str(energy_level)
  layer_template['description'] = 'Techniques that require Influence Energy Level ' + str(energy_level)
  
  layer_template['links'] = [
    {
      "label": "Influence Energy",
      "url": "https://www.optimizer.llc"
    },
    {
      "label": "Source Repository",
      "url": "'https://github.com/BoogleCloud/influence-energy'"
    }
  ]
  
  layer_template['metadata'] = [
    {
      "name": "version",
      "value": "1.0"
    },
    {
      "name": "author",
      "value": "Optimizer LLC"
    },
    {
      "name": "date",
      "value": datetime.now().strftime("%Y-%m-%d")
    }
  ]

  with open(layer_output_path, 'w') as output_file:
    json.dump(layer_template, output_file, indent='\t')

if __name__ == "__main__":
  main(sys.argv[1:])

# print(json.dumps(output, indent=2))
# print("=====================================")
# print(json.dumps(navigator_techniques, indent=2))

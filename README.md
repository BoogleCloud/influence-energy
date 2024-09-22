# influence-energy
Influence Energy Mappings for MITRE ATT&amp;CK and visualization layers for ATT&CK Navigator.

## Background

If you are new to the concept of Security and Influence energy, please check out: https://optimizer.llc/blogs/post/security-energy

## 
This repository contains MITRE ATT&CK navigator layers. They can be visualized here: https://mitre-attack.github.io/attack-navigator/

You can load them directly from the github raw view by using URLs:

https://raw.githubusercontent.com/BoogleCloud/influence-energy/refs/heads/main/ie1_layer.json
https://raw.githubusercontent.com/BoogleCloud/influence-energy/refs/heads/main/ie2_layer.json
https://raw.githubusercontent.com/BoogleCloud/influence-energy/refs/heads/main/ie3_layer.json
https://raw.githubusercontent.com/BoogleCloud/influence-energy/refs/heads/main/ie4_layer.json
https://raw.githubusercontent.com/BoogleCloud/influence-energy/refs/heads/main/ie5_layer.json

## Updates

To generate new visualization templates, start by editing the attack_capabilities.csv file to change energy level mappings and/or example links. Once update, run the following commands to regenerate all the layers:

```bash
python3 capabilities_to_navigator.py -l 1 attack_capabilities.csv
python3 capabilities_to_navigator.py -l 2 attack_capabilities.csv
python3 capabilities_to_navigator.py -l 3 attack_capabilities.csv
python3 capabilities_to_navigator.py -l 4 attack_capabilities.csv
python3 capabilities_to_navigator.py -l 5 attack_capabilities.csv
```

## Future Work

I noted some skilli prerequisites on the CSV for why some capabilities were mapped to the energy level they are. These could be further expanded upon to improve the consistency of mappings and then included in the navigator layer as metadata.

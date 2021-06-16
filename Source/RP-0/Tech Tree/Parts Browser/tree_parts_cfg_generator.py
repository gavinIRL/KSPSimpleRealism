import part_data
import os
from string import Template

output_dir = os.getenv('PB_OUTPUT_DIR', "../../../GameData/RP-0/Tree/")

tree_parts_header = """
//*********************************************************************************************
//  PARTS TECH TREE PLACEMENT
//	This places all parts in the tech tree
//  
//	DO NOT EDIT THIS FILE DIRECTLY!!!
//	This file is generated from the RP-0 Parts Browser
//
//*********************************************************************************************
"""

module_part_config_template = Template("""
@PART[${name}]:FOR[xxxRP0]
{
    %TechRequired = ${technology}
    %cost = ${cost}
    %entryCost = ${entry_cost}
    RP0conf = ${rp0_conf}
    @description ^=:$$: <b><color=green>From ${mod} mod</color></b>${module_tags}
}""")
module_template = Template("""
    MODULE
    { name = Module${module_tag} }""")

def generate_parts_tree(parts, module_tags_with_prefixes):
    part_configs = ""
    for part in parts:
        if part['name'] is not None and len(part['name']) > 0:
            if part['mod'] != 'Engine_Config' and not part['orphan']:
                part_configs += generate_part_config(part, module_tags_with_prefixes)
    text_file = open(output_dir + "TREE-Parts.cfg", "w", newline='\n')
    text_file.write(tree_parts_header)
    text_file.write(part_configs)
    text_file.close()
        
def generate_part_config(part, module_tags_with_prefixes):
    module_tags = ''
    for module_tag in part['module_tags']:
        # some module tags have a prefix (usually 'Tag') so if it has a prefix, prefix it.
        prefix = module_tags_with_prefixes[module_tag].strip()
        module_tags += module_template.substitute(module_tag=prefix + module_tag)
    if len(module_tags) > 0:
        module_tags = "\n" + module_tags + "\n"
    return module_part_config_template.substitute(name=part['name'], mod=part['mod'], technology=part['technology'], cost=part['cost'], entry_cost=part['entry_cost'], rp0_conf=str(part['rp0_conf']).lower(), module_tags=module_tags)


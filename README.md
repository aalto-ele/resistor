# Resistor
This project is structured example of how to generate a single resistor 
with BAG

OBS: Requires bag_ecd package and ecd compliant BAG process ans promiteive 
definition

Howto:
1) git clone this module to your BAG installation directory
2) Add the transistor_templates library definition to your cds.lib
3) Use python3 (or your favourite python run method) in BAG installation directory
    python3 transistor/transistor/__init__.py

4) Schematic and layout are generated to default_lib_path; usually "${BAG_WORK_DIR}/gen_libs" 


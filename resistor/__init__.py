'''
Resistor
======

'''
import os

from bag_ecd import bag_startup 
from bag_ecd.bag_design import bag_design
import bag
from bag.layout import RoutingGrid, TemplateDB

#This is mandatory
from resistor.layout import layout 

#For debugging
import pdb

class resistor(bag_design):

    @property
    def _classfile(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/"+__name__

    def __init__(self):

        #You must define self.min_lch 
        self.draw_params={
               'sub_type' : 'ntap',
               'threshold' : 'standard',
               'nx': 1,
               'ny': 1,
               'grid_type': 'standard',
               'em_specs' : dict(),
               'ext_dir': '',
               'show_pins': True,
               'connect_up': True,
               'top_layer': 5,
               'add_dnw' : False
               }
               #'top_layer': 8,


        self.sch_params={ 
               'l' : 1100*self.min_lch,
               'w' : 200*self.min_lch,
               'res_type' :'standard'
               } 
        self.layout=layout
    
if __name__ == '__main__':
    from resistor import resistor
    inst=resistor()
    inst.generate()


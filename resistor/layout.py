''' Resistor layout generator '''
import abc
from abs_templates_ec.resistor.core import ResArrayBase, TerminationCore
from abs_templates_ec.analog_core.substrate import SubstrateContact, DeepNWellRing

from bag.layout.util import BBox
from bag.layout.routing import TrackID, WireArray
from bag.layout.template import TemplateBase, TemplateDB


from pprint import pprint
import pdb

class resistor_core(ResArrayBase):
    '''
    This is the resistor core construct. Everything is presented in resistor
    routing grid generally not compatible with general routing greid. 

    Parameters
    ----------
    temp_db : :class:`bag.layout.template.TemplateDB`
            the template database.
    lib_name : str
        the layout library name.
    params : dict[str, any]
        the parameter values.
    used_names : set[str]
        a set of already used cell names.
    **kwargs :
        dictionary of optional parameters.  See documentation of
        :class:`bag.layout.template.TemplateBase` for details.
    '''

    def __init__(self, temp_db, lib_name, params, used_names, **kwargs):
        # type: (TemplateDB, str, Dict[str, Any], Set[str], **Any) -> None
        ResArrayBase.__init__(self, temp_db, lib_name, params, used_names, **kwargs)

    @classmethod
    def get_default_param_values(cls):
        """Returns a dictionary containing default parameter values.
        Override this method to define default parameter values.  As good practice,
        you should avoid defining default values for technology-dependent parameters
        (such as channel length, transistor width, etc.), but only define default
        values for technology-independent parameters (such as number of tracks).
        Returns
        -------
        default_params : Dict[str, Any]
            dictionary of default parameter values.
        """
        return dict(
            nx=2,
            ny=1,
            res_type='standard',
            grid_type='standard',
            em_specs={},
            ext_dir='',
            show_pins=True,
            top_layer=None,
            add_dnw=False,
        )

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary containing parameter descriptions.
        Override this method to return a dictionary from parameter names to descriptions.
        Returns
        -------
        param_info : Dict[str, str]
            dictionary from parameter name to description.
        """
        return dict(
            l='unit resistor length, in meters.',
            w='unit resistor width, in meters.',
            sub_type='the substrate type.',
            threshold='the substrate threshold flavor.',
            nx='number of resistors in a row.  Must be even.',
            ny='number of resistors in a column.',
            res_type='the resistor type.',
            grid_type='the resistor routing grid type.',
            em_specs='EM specifications for the termination network.',
            ext_dir='resistor core extension direction.',
            show_pins='True to show pins.',
            top_layer='The top level metal layer.  None for primitive template.',
        )

    def draw_layout(self):
        # draw array
        nx = self.params['nx']
        ny = self.params['ny']
        em_specs = self.params.pop('em_specs')
        show_pins = self.params.pop('show_pins')

        div_em_specs = em_specs.copy()
        self.draw_array(em_specs={}, **self.params)
        # Ports of the resistor in resistor array location 0,0 

        warr=self.get_res_ports(0,0)[0]
        ports_l=self.get_res_ports(0,0)
        loc_bot = ports_l[0].get_bbox_array(self.grid).bottom
        loc_left = ports_l[0].get_bbox_array(self.grid).left
        loc_right = ports_l[0].get_bbox_array(self.grid).right
        loc_center = (loc_left + loc_right)/2


        # Todo, resolve layer
        idx=self.grid.coord_to_nearest_track(3, loc_center)
        #hor_p = TrackID(layer_id=4, track_idx=idy, width=2)
        ver_p = TrackID(layer_id=3, track_idx=idx, width=2)
        ver_warr_m=self.connect_to_tracks(ports_l[0],ver_p)
        ver_warr_p=self.connect_to_tracks(ports_l[1],ver_p)
        self.add_pin('M', ver_warr_m, label='M', show=show_pins)
        self.add_pin('P', ver_warr_p, label='P',  show=show_pins)

class resistor_unit(TemplateBase):
    '''
    This class is needed to isolate resistor routing grid from general routing grid.
    Place the resistor_core to origo. All other placements most likely result
    in problems of finding and defining pin locations at some point od the design.

    Parameters
    ----------
    temp_db : :class:`bag.layout.template.TemplateDB`
            the template database.
    lib_name : str
        the layout library name.
    params : dict[str, any]
        the parameter values.
    used_names : set[str]
        a set of already used cell names.
    **kwargs :
        dictionary of optional parameters.  See documentation of
        :class:`bag.layout.template.TemplateBase` for details.
    '''

    def __init__(self, temp_db, lib_name, params, used_names, **kwargs):
        # type: (TemplateDB, str, Dict[str, Any], Set[str], **Any) -> None
        TemplateBase.__init__(self, temp_db, lib_name, params, used_names, **kwargs)

    @classmethod
    def get_default_param_values(cls):
        '''Returns a dictionary containing default parameter values.
        Override this method to define default parameter values.  As good practice,
        you should avoid defining default values for technology-dependent parameters
        (such as channel length, transistor width, etc.), but only define default
        values for technology-independent parameters (such as number of tracks).
        Returns
        -------
        default_params : Dict[str, Any]
            dictionary of default parameter values.
        '''
        return dict(
            nx=2,
            ny=1,
            res_type='standard',
            grid_type='standard',
            em_specs={},
            ext_dir='',
            show_pins=True,
            connect_up=True,
            top_layer=None,
        )

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        '''Returns a dictionary containing parameter descriptions.
        Override this method to return a dictionary from parameter names to descriptions.
        Returns
        -------
        param_info : Dict[str, str]
            dictionary from parameter name to description.
        '''
        return dict(
            l='unit resistor length, in meters.',
            w='unit resistor width, in meters.',
            sub_type='the substrate type.',
            threshold='the substrate threshold flavor.',
            nx='number of resistors in a row.  Must be even.',
            ny='number of resistors in a column.',
            res_type='the resistor type.',
            grid_type='the resistor routing grid type.',
            em_specs='EM specifications for the termination network.',
            ext_dir='resistor core extension direction.',
            show_pins='True to show pins.',
            top_layer='The top level metal layer.  None for primitive template.',
        )

    def draw_layout(self):
        # type: () -> None

        # draw array
        nx = self.params['nx']
        ny = self.params['ny']
        sub_type=self.params['sub_type']
        res_type=self.params['res_type']
        em_specs = self.params.pop('em_specs')
        show_pins = self.params.pop('show_pins')
        #add_dnw=self.params.pop('add_dnw')

        div_em_specs = em_specs.copy()
        res_master=self.new_template(params=self.params.copy(),temp_cls=resistor_core)

        top_layer, nx_arr, ny_arr = res_master.size
        w_pitch, h_pitch = self.grid.get_size_pitch(top_layer,unit_mode=True)
         
        self.size = top_layer, nx_arr, ny_arr
        res_inst=self.add_instance(res_master,inst_name='XRES',
                loc=(0,0), 
                unit_mode=True)

        # connect implant layers of resistor array and substrate contact together
        for lay in self.grid.tech_info.get_implant_layers(sub_type, res_type=res_type):
            self.add_rect(lay, self.get_rect_bbox(lay))

        # recompute array_box/size
        #self.array_box = bot_inst.array_box.merge(top_inst.array_box)
        self.add_cell_boundary(self.bound_box)
            
        # connect implant layers of resistor array and substrate contact together
        for lay in ['NW']:
            self.add_rect(lay, self.get_rect_bbox(lay),unit_mode=True)

        # This is required because ResArrayBase is in different routing grid than
        # self, and I have no Idea how to map tracks correctly.
        # Problem: Port TrackID's are according to ResArrayBase
        for name in [ 'M', 'P' ]:
            port=res_inst.get_port(name)
            box=port.get_bounding_box(res_master.grid)
            layer_id=port.get_pins()[0].layer_id
            loc_v = self.grid.coord_to_nearest_track(layer_id,box.xc, 
                    half_track=False, mode=0, unit_mode=False)
            tid_v=TrackID(layer_id=layer_id, track_idx=loc_v, width=1)
            port_warr=WireArray(tid_v, box.bottom, box.top, res=self.grid.resolution, 
                    unit_mode=False)
            self.add_pin(self.get_pin_name(name),port_warr, show=True)

class layout(TemplateBase):
    '''
    This class uses resistor_unit that is in the same routing gird as self.

    Parameters
    ----------
    temp_db : :class:`bag.layout.template.TemplateDB`
            the template database.
    lib_name : str
        the layout library name.
    params : dict[str, any]
        the parameter values.
    used_names : set[str]
        a set of already used cell names.
    **kwargs :
        dictionary of optional parameters.  See documentation of
        :class:`bag.layout.template.TemplateBase` for details.
    '''

    def __init__(self, temp_db, lib_name, params, used_names, **kwargs):
        # type: (TemplateDB, str, Dict[str, Any], Set[str], **Any) -> None
        TemplateBase.__init__(self, temp_db, lib_name, params, used_names, **kwargs)

    @classmethod
    def get_default_param_values(cls):
        """Returns a dictionary containing default parameter values.
        Override this method to define default parameter values.  As good practice,
        you should avoid defining default values for technology-dependent parameters
        (such as channel length, transistor width, etc.), but only define default
        values for technology-independent parameters (such as number of tracks).
        Returns
        -------
        default_params : Dict[str, Any]
            dictionary of default parameter values.
        """
        return dict(
            nx=2,
            ny=1,
            res_type='standard',
            grid_type='standard',
            em_specs={},
            ext_dir='',
            show_pins=True,
            connect_up=True,
            top_layer=None,
            add_dnw= False,
        )

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary containing parameter descriptions.
        Override this method to return a dictionary from parameter names to descriptions.
        Returns
        -------
        param_info : Dict[str, str]
            dictionary from parameter name to description.
        """
        return dict(
            l='unit resistor length, in meters.',
            w='unit resistor width, in meters.',
            sub_type='the substrate type.',
            threshold='the substrate threshold flavor.',
            nx='number of resistors in a row.  Must be even.',
            ny='number of resistors in a column.',
            res_type='the resistor type.',
            grid_type='the resistor routing grid type.',
            em_specs='EM specifications for the termination network.',
            ext_dir='resistor core extension direction.',
            show_pins='True to show pins.',
            top_layer='The top level metal layer.  None for primitive template.',
            add_dnw='Add deep_nwell ring False | True',
        )

    def draw_layout(self):
        # type: () -> None

        # draw array
        nx = self.params['nx']
        ny = self.params['ny']
        sub_type=self.params['sub_type']
        res_type=self.params['res_type']
        em_specs = self.params.pop('em_specs')
        show_pins = self.params.pop('show_pins')
        add_dnw=self.params.pop('add_dnw')

        div_em_specs = em_specs.copy()
        res_master=self.new_template(params=self.params.copy(),
                temp_cls=resistor_unit)
        top_layer, nx_arr, ny_arr = res_master.size
        w_pitch, h_pitch = self.grid.get_size_pitch(top_layer,unit_mode=True)
         
        # draw contact and move array up
        top_layer=self.params['top_layer']
        sub_lch=30e-9
        sub_w=4*sub_lch
        sub_params = dict(
            top_layer=top_layer,
            lch=sub_lch,
            w=sub_w,
            sub_type=self.params['sub_type'],
            threshold=self.params['threshold'],
            well_width=res_master.bound_box.width,
            show_pins=True,
            is_passive=True,
            tot_width_parity=1 % 2,
        )
        #Define the substrate contact master cell
        sub_master = self.new_template(params=sub_params, 
                temp_cls=SubstrateContact)
        _, nx_sub, ny_sub = sub_master.size
        #print(sub_master.size)
        nx_shift = (nx_arr - nx_sub ) // 2
        x_pitch, y_pitch = self.grid.get_size_pitch(top_layer,unit_mode=True)
        resx_pitch, resy_pitch = res_master.grid.get_size_pitch(top_layer,
                unit_mode=True)

        #self.size = top_layer, nx_arr, ny_arr + 2 * ny_sub
        #Add substrate contact or Deep Nwell Ring
        if not add_dnw:
            self.size = top_layer, nx_arr, ny_arr + 2 * ny_sub
            top_yo = ( ny_arr +2*ny_sub) * h_pitch
            top_inst = self.add_instance(sub_master, inst_name='XTSUB', 
                    loc=(nx_shift, top_yo), orient='MX',
                                 unit_mode=True)
            bot_inst = self.add_instance(sub_master, inst_name='XBSUB', 
                    loc=(nx_shift*x_pitch, 0), unit_mode=True)
            res_inst=self.add_instance(res_master,inst_name='XRES',
                    loc=(0,ny_sub*h_pitch), 

                    unit_mode=True)

            # connect implant layers of resistor array and substrate contact together
            for lay in self.grid.tech_info.get_implant_layers(sub_type, 
                    res_type=res_type):
                self.add_rect(lay, self.get_rect_bbox(lay))

            # recompute array_box/size
            self.array_box = bot_inst.array_box.merge(top_inst.array_box)
            self.add_cell_boundary(self.bound_box)
            
            # Add pins for substrate contact
            self.add_pin(self.get_pin_name('B'),top_inst.get_port('VDD'),show=True)
            self.add_pin(self.get_pin_name('B'),bot_inst.get_port('VDD'),show=True)
        else: 
            # This is how to add DNW
            # Location computation not performed
            
            # OBS: This size happens to be in grid by accident.
            # Other sizes will fail
            # I do not  know how to define the height for deep_nwell correctly

            # This works
            self.size = top_layer, nx_arr, ny_arr+2*ny_sub
            
            # This does not
            # self.size = top_layer, nx_arr, ny_arr

            dnw_params = dict(
                top_layer=top_layer, #'the top layer of the template.',
                bound_box=self.bound_box, #'bounding box of the inner template',
                w=sub_w, #'substrate tap width, in meters/number of fins.',
                fg_side= 1, #'number of fingers in vertical substrate ring.',
                threshold='standard', #'substrate threshold flavor.',
                show_pins=True, #'True to show pin labels.',
                dnw_mode='normal'  #'deep N-well mode string.  This determines the DNW space to             adjacent blocks.',
                )
            dnw_master=self.new_template(params=dnw_params, temp_cls=DeepNWellRing)
            dnw_inst=self.add_instance(dnw_master,inst_name='XDNW',
                    loc=(0,0),
                    unit_mode=True)
             #DNW ends here

            #res_inst=self.add_instance(res_master,inst_name='XRES', orient='R0',
            #        loc=dnw_master.blk_loc_unit, 
            #        unit_mode=True)

            #self.add_cell_boundary(self.bound_box)

            ## Add pins for substrate contact
            #self.add_pin(self.get_pin_name('B'),dnw_inst.get_port('VDD'),show=True)
            #self.add_pin(self.get_pin_name('VSS'),dnw_inst.get_port('VSS'),show=True)

            ## connect implant layers of resistor array and substrate contact together
            #for lay in ['NW']:
            #    self.add_rect(lay, self.get_rect_bbox(lay),unit_mode=True)

        # This is required because ResArrayBase is in different routing grid than
        # self, and I have no Idea how to map tracks correctly.
        # Problem: Port TrackID's are according to ResArrayBase
        for name in [ 'M', 'P' ]:
            port=res_inst.get_port(name)
            self.reexport(res_inst.get_port(name),net_name=name,label=name,show=True)
        self.sch_params = dict()
        for key in ('l', 'w', 'res_type' ): 
          self.sch_params[key] = self.params[key]

        sch_dummy_info = dict() 
        self.sch_dummy_info = sch_dummy_info


class resistor(layout):
    '''This class is the template class to be used as a master within
       the other layout classes. For some reason currently unknown to me, the layout class
       can not be used directly.
       
       '''
    def __init__(self, temp_db, lib_name, params, used_names, **kwargs):
        TemplateBase.__init__(self, temp_db, lib_name, params, used_names, **kwargs)



import os
import pkg_resources

from bag.design import Module
#The module path shold be global. Is it?
yaml_file = pkg_resources.resource_filename(__name__, os.path.join('../../BagModules/resistor_templates', 'netlist_info', 'resistor.yaml'))


# noinspection PyPep8Naming
class schematic(Module):
    """Module for library resistor_templates cell resistor.

    Fill in high level description here.
    """

    def __init__(self, bag_config, parent=None, prj=None, **kwargs):
        Module.__init__(self, bag_config, yaml_file, parent=parent, prj=prj, **kwargs)
       
    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            l='Lengtth in meters',
            w='Width in meters',
            res_type='resistor_type',
        )

    def design(self, **kwargs):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        # Could define defaults here
        l = kwargs.get('l')
        w = kwargs.get('w')
        res_type = kwargs.get('res_type','standard')
        self.instances['R1'].design(w=w, l=l, intent=res_type)


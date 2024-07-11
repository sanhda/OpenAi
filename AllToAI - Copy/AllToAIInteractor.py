#import allplan default library
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService

from .gui import GUI

def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True

def create_element(build_ele, doc):
    return ([], None, None)

def create_interactor(coord_input, pyp_path, boolean, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    #create new pythonpart
    if modify_uuid_list[0] == "00000000-0000-0000-0000-000000000000--0":
       return AlltoAI(coord_input, pyp_path, str_table_service)
    #modify pythonpart
    return AlltoAI(coord_input, pyp_path, str_table_service, build_ele_list=build_ele_list, modify_uuid_list=modify_uuid_list)

class AlltoAI():
    def __init__(self, coord_input: AllplanIFW.CoordinateInput, pyp_path, str_table_service, build_ele_list=[], modify_uuid_list=[]):
        #input parameter from pythonpart
        self.doc                    = coord_input.GetInputViewDocument()
        self.coord_input            = coord_input
        self.pyp_path               = pyp_path
        self.str_table_service      = str_table_service
        self.build_ele_list         = build_ele_list
        self.build_ele_service      = BuildingElementService()
        self.modify_uuid_list       = modify_uuid_list
        self.palette_service        = None
        self.show_gui()

    def on_cancel_function(self):
        return True

    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        return True

    def on_control_event(self, event_id):
        pass

    def on_preview_draw(self):
        pass

    def on_mouse_leave(self):
        pass

    def show_gui(self):
        app = GUI(self.doc)
        app.MainLoop()
        app.Destroy()
        del app


import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from .objects.allplan_object import AllplanObject
from .objects.wall_object import WallObject

from typing import List

class DataProcess():
    def __init__(self, doc):
        self.doc = doc
        self.wall_objects: List[WallObject] = []
        self.get_all_objects()

    def get_all_objects(self):
        all_elements = AllplanBaseElements.ElementsSelectService.SelectAllElements(self.doc)
        self.wall_objects = [WallObject(element) for element in all_elements if element in WallObject.get_adapters()]

    def process_action(self, action, obj, conditions, details) -> str:
        return "Process action"
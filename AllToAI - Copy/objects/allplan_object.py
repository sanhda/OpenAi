import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_ArchElements as AllplanArchElements

class AllplanObject():
    def __init__(self, base_element: AllplanElementAdapter.BaseElementAdapter) -> None:
        self.base_element = base_element

    @staticmethod
    def get_adapters():
        return []
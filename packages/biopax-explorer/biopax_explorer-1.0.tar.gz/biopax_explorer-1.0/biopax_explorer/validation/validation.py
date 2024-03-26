import  rdfobj.validation as va
import biopax_explorer.biopax as biopax
 
from biopax_explorer.biopax.utils import gen_utils


 
class Validator(va.Validator):
    
    """
    This class facilitate the BIOPAX entities /instances validation process.

    """
        
    def __init__(self, cfg): 
         modules=[biopax]
         super().__init__(cfg,modules)
    
 
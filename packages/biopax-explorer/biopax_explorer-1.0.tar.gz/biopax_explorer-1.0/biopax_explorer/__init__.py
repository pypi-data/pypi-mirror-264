 
__version__='1.0' 
 
be_disable_thirdp_warnings=True #disable third party warnings for unnecessary features
be_use_message_warnings_filters=False # manage 2 methods of warning filters
import warnings
 
###################

if be_disable_thirdp_warnings==True: 
  
  if be_use_message_warnings_filters==True: 
     warnings.filterwarnings("ignore", message="networkx backend defined more than once: nx-loopback", module="networkx")
     warnings.filterwarnings("ignore", message="Error importing cairo. Graph drawing will not work.", module="graph_tool")
     warnings.filterwarnings("ignore", message="Error importing draw module, proceeding nevertheless: No module named 'cairo'", module="graph_tool")
  else:
     warnings.filterwarnings( action='ignore' ,category=RuntimeWarning, module=r'networkx.utils.*')
     warnings.filterwarnings( action='ignore' ,category=RuntimeWarning, module=r'graph_tool.draw.*')
     warnings.filterwarnings( action='ignore' ,category=RuntimeWarning, module=r'graph_tool.all.*')


###################import sub packages
from .biopax import *

from .pattern import *

from .query import *

from .graph import *

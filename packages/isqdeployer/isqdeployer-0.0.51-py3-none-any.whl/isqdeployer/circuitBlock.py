from __future__ import annotations
from .circuitDeployer.abcDeployer import BaseDeployer
from .circuitDeployer.gateDeployer import Deployer as GateDeployer
from .circuit import Circuit

class BlockError(Exception):pass 






class AbcBlock():

    def __init__(self, nParams:int = 0 ):
        # self._gateDeployer = GateDeployer(circuit=circuit,qMap=qMap)
        self.nParams = nParams

    def setTheta(self,theta:list):
        r"""before deploy gates onto circuit, one can reset theta by this function.

        Args:
            theta (list): element can be float or circuit.args

        Returns:
            _type_: _description_
        """   
        if len(theta) != self.nParams:
            raise BlockError("number of theta donot match nParams")  
        self._THETA = theta 
        return self 

    def deploy(self,circuit:Circuit,qMap:list|None=None):
        """deploy gates into circuit

        Args:
            circuit (Circuit): circuit
            qMap (list | None, optional): _description_. Defaults to None.

        Raises:
            BlockError: _description_

        Returns:
            _type_: self
        """        
        if not hasattr(self,'_THETA'):
            if self.nParams > 0:
                raise BlockError('''theta is not set in ansatz, use method "setTheta(theta)" to set it.''')    
            else:
                self._THETA = []   
        _gateDeployer = GateDeployer(circuit=circuit,qMap=qMap)
        self.definition( _gateDeployer, self._THETA )  
        return self 
    
    #-------------------------------------------------------
    def definition(self,gate:GateDeployer,theta:list):
        '''
        Define a block contains a set of gates.
        For advanced usage, circuit = gate.getCircuit()  
        '''
        raise BlockError(f"method definition is not defined in class {self.__class__.__name__}")


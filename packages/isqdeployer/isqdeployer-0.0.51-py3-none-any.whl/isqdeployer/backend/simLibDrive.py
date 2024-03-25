from __future__ import annotations

import numpy as np
import ctypes
from .abcInteractiveBackend import InteractiveBackend


class SimDriveError(Exception):pass 








# gfortran -O3 -shared -fPIC -o libfcircuit.so test.f90
    
class FCircuit:
    def __init__(self, nq: int ,libPath:str) -> None:
        self.nq = nq
        self.dim = 2**nq
        self.iparas = []
        self.fparas = []

        self.libfcircuit = ctypes.cdll.LoadLibrary(libPath)

        GateParaIntLen = ctypes.c_int32()
        GateParaRealLen = ctypes.c_int32()
        self.libfcircuit.get_para_size(
            ctypes.byref(GateParaIntLen),
            ctypes.byref(GateParaRealLen),
        )
        self.doubleptr = ctypes.POINTER(ctypes.c_double)
        self.int64ptr = ctypes.POINTER(ctypes.c_int64)
        self.ilen = GateParaIntLen.value
        self.flen = GateParaRealLen.value

    def H(self, i: int):
        self.iparas.append([72, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def S(self, i: int):
        self.iparas.append([83, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def T(self, i: int):
        self.iparas.append([84, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def X(self, i: int):
        self.iparas.append([88, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def Y(self, i: int):
        self.iparas.append([89, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def Z(self, i: int):
        self.iparas.append([90, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def CX(self, i: int, j: int):
        self.iparas.append([6788, i, j] + [0] * (self.ilen - 3))
        self.fparas.append([0.0] * self.flen)
        return self

    CNOT = CX

    def CZ(self, i: int, j: int):
        self.iparas.append([6790, i, j] + [0] * (self.ilen - 3))
        self.fparas.append([0.0] * self.flen)
        return self

    def RX(self, i: int, theta: float):
        self.iparas.append([8288, i] + [0] * (self.ilen - 2))
        self.fparas.append([float(theta)] + [0.0] * (self.flen - 1))
        return self

    def RY(self, i: int, theta: float):
        self.iparas.append([8289, i] + [0] * (self.ilen - 2))
        self.fparas.append([float(theta)] + [0.0] * (self.flen - 1))
        return self

    def RZ(self, i: int, theta: float):
        self.iparas.append([8290, i] + [0] * (self.ilen - 2))
        self.fparas.append([float(theta)] + [0.0] * (self.flen - 1))
        return self

    def SD(self, i: int):
        self.iparas.append([8368, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def TD(self, i: int):
        self.iparas.append([8468, i] + [0] * (self.ilen - 2))
        self.fparas.append([0.0] * self.flen)
        return self

    def state(self) -> np.complex128:
        iparas_array = np.array(self.iparas, dtype=ctypes.c_int64, order="C")
        fparas_array = np.array(self.fparas, dtype=ctypes.c_double, order="C")
        state_real = np.array(np.empty(self.dim), dtype=ctypes.c_double)
        state_imag = np.array(np.empty(self.dim), dtype=ctypes.c_double)

        self.libfcircuit.simulation_state(
            ctypes.byref(ctypes.c_int32(self.nq)),
            ctypes.byref(ctypes.c_int64(self.dim)),
            ctypes.byref(ctypes.c_int64(len(self.iparas))),
            iparas_array.ctypes.data_as(self.int64ptr),
            fparas_array.ctypes.data_as(self.doubleptr),
            state_real.ctypes.data_as(self.doubleptr),
            state_imag.ctypes.data_as(self.doubleptr),
        )
        return (state_real + state_imag * 1j).astype(np.complex128)

    def probs(self) -> np.float64:
        iparas_array = np.array(self.iparas, dtype=ctypes.c_int64, order="C")
        fparas_array = np.array(self.fparas, dtype=ctypes.c_double, order="C")
        probalibity = np.array(np.empty(self.dim), dtype=ctypes.c_double)
        self.libfcircuit.simulation_probability(
            ctypes.byref(ctypes.c_int32(self.nq)),
            ctypes.byref(ctypes.c_int64(self.dim)),
            ctypes.byref(ctypes.c_int64(len(self.iparas))),
            iparas_array.ctypes.data_as(self.int64ptr),
            fparas_array.ctypes.data_as(self.doubleptr),
            probalibity.ctypes.data_as(self.doubleptr),
        )
        return probalibity.astype(np.float64)







class Backend(InteractiveBackend):


    def __init__(self,libPath:str,**kw):
        super().__init__(**kw)
        self.libPath = libPath 

    # ---------------------------------------------
    def initCalc(self, nq, qMap):
        self.cir = FCircuit(nq=nq, libPath=self.libPath)

    def getFinalState(self) -> list[complex]:
        """
        return complex [0:2**n-1]
        """
        return self.cir.state()

    def X(self, i):
        return self.cir.X(i) 
    
    def Y(self, i):
        return self.cir.Y(i) 

    def Z(self, i):
        return self.cir.Z(i) 

    def H(self, i):
        return self.cir.H(i) 

    def S(self, i):
        return self.cir.S(i) 

    def T(self, i):
        return self.cir.T(i) 

    def Rx(self, i, phi):
        return self.cir.RX(i, phi) 

    def Ry(self, i, phi):
        return self.cir.RY(i, phi) 

    def Rz(self, i, phi):
        return self.cir.RZ(i, phi) 

    RX=Rx 
    RY=Ry 
    RZ=Rz 


    def X2P(self, i):
        return self.Rx(i, np.pi / 2)

    def X2M(self, i):
        return self.Rx(i, -np.pi / 2)

    def Y2P(self, i):
        return self.Ry(i, np.pi / 2)

    def Y2M(self, i):
        return self.Ry(i, -np.pi / 2)

    def SD(self, i):
        return self.cir.SD(i) 

    def TD(self, i):
        return self.cir.TD(i) 

    def CX(self, i, j):
        return self.cir.CX(i,j) 

    def CZ(self, i, j):
        return self.cir.CZ(i,j) 

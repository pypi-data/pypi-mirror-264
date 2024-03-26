import numpy as np
import numpy.typing as npt
from typing import Dict, TypeAlias, Union, Tuple, List, TypedDict


pyCFSparam: TypeAlias = int | float | str
pyCFSparamVec: TypeAlias = (
    npt.NDArray[np.int32]
    | npt.NDArray[np.int64]
    | npt.NDArray[np.float32]
    | npt.NDArray[np.float64]
    | npt.NDArray[np.str_]
)
resultScalar: TypeAlias = int | float
resultVec: TypeAlias = Union[
    npt.NDArray[np.float32],
    npt.NDArray[np.float64],
    npt.NDArray[np.complex64],
]
resultDict: TypeAlias = Dict[str, resultVec | resultScalar | Tuple[resultScalar]]
nestedResultDict: TypeAlias = Dict[str, Dict[str, Dict[str, Dict[str, resultDict]]]]


class sensorArrayResult(TypedDict):
    data: resultVec
    columns: List[str]


sensorArrayResultPacket = Dict[str, sensorArrayResult]

__all__ = [
    "pyCFSparam",
    "pyCFSparamVec",
    "resultVec",
    "resultDict",
    "nestedResultDict",
    "sensorArrayResult",
]

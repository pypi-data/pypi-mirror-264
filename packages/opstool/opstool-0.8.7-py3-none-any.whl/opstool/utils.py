import sys
import numpy as np
from pathlib import Path
from typing import Union
from .EleClassTags import (EleTypeTags, ELE_TAG_Beam, ELE_TAG_Tetrahedron, ELE_TAG_Link,
                           ELE_TAG_PFEM, ELE_TAG_Brick, ELE_TAG_Joint, ELE_TAG_Plane, ELE_TAG_Truss)


class EleClassTags:
    TypeTags = EleTypeTags
    BeamTags = ELE_TAG_Beam
    TetTags = ELE_TAG_Tetrahedron
    LinkTags = ELE_TAG_Link
    TrussTags = ELE_TAG_Truss
    PFEMTags = ELE_TAG_PFEM
    BrickTags = ELE_TAG_Brick
    JointTags = ELE_TAG_Joint
    PlaneTags = ELE_TAG_Plane


# shape dict used to subplots
shape_dict = {
    1: (1, 1),
    2: (1, 2),
    3: (1, 3),
    4: (2, 2),
    5: (2, 3),
    6: (2, 3),
    7: (3, 3),
    8: (3, 3),
    9: (3, 3),
    10: (3, 4),
    11: (3, 4),
    12: (3, 4),
    13: (4, 4),
    14: (4, 4),
    15: (4, 4),
    16: (4, 4),
    17: (4, 5),
    18: (4, 5),
    19: (4, 5),
    20: (4, 5),
    21: (5, 5),
    22: (5, 5),
    23: (5, 5),
    24: (5, 5),
    25: (5, 5),
    26: (5, 6),
    27: (5, 6),
    28: (5, 6),
    29: (5, 6),
    30: (5, 6),
    31: (6, 6),
    32: (6, 6),
    33: (6, 6),
    34: (6, 6),
    35: (6, 6),
    36: (6, 6),
    37: (6, 7),
    38: (6, 7),
    39: (6, 7),
    40: (6, 7),
    41: (6, 7),
    42: (6, 7),
    43: (7, 7),
    44: (7, 7),
    45: (7, 7),
    46: (7, 7),
    47: (7, 7),
    48: (7, 7),
    49: (7, 7),
}


def check_file(file_name: str, file_type: Union[str, list, tuple]):
    """Check file type.

    Parameters
    ----------
    file_name: str
        The file to be checked.
    file_type: Union[str, list, tuple]
        The target file type.

    Returns
    -------
    None
    """
    if file_name:
        if isinstance(file_type, str):
            if not file_name.endswith(file_type):
                raise ValueError(f"file must be endswith {file_type}!")
        elif isinstance(file_type, list) or isinstance(file_type, tuple):
            check = False
            for type_ in file_type:
                if file_name.endswith(type_):
                    check = True
            if not check:
                raise ValueError(f"file must be endswith in {file_type}!")
        else:
            raise ValueError("file_type must be str or list or tuple!")


def load_ops_examples(name: str):
    """load the examples.

    Parameters:
    -----------
    name: str,
        Optional, "ArchBridge", "ArchBridge2", "CableStayedBridge", "Dam",
        "Frame3D", "Frame3D2", "Igloo", "Pier", "SuspensionBridge", "SDOF",
        "DamBreak", "GridFrame", "Shell3D".

    Returns:
    --------
    None
    """
    if name.lower() == "archbridge":
        from .examples.ArchBridge import ArchBridge

        ArchBridge()
        # exec("from opstool.examples.ArchBridge import *")
    elif name.lower() == "archbridge2":
        from .examples.ArchBridge2 import ArchBridge2

        ArchBridge2()
        # exec("from opstool.examples.ArchBridge2 import *")
    elif name.lower() == "cablestayedbridge":
        from .examples.CableStayedBridge import CableStayedBridge

        CableStayedBridge()
        # exec("from opstool.examples.CableStayedBridge import *")
    elif name.lower() == "dam":
        from .examples.Dam import Dam

        Dam()
        # exec("from opstool.examples.Dam import *")
    elif name.lower() == "frame3d":
        from .examples.Frame3D import Frame3D

        Frame3D()
        # exec("from opstool.examples.Frame3D import *")
    elif name.lower() == "frame3d2":
        from .examples.Frame3D2 import Frame3D2

        Frame3D2()
    elif name.lower() == "igloo":
        from .examples.Igloo import Igloo

        Igloo()
        # exec("from opstool.examples.Igloo import *")
    elif name.lower() == "pier":
        from .examples.Pier import Pier

        Pier()
        # exec("from opstool.examples.Pier import *")
    elif name.lower() == "suspensionbridge":
        from .examples.SuspensionBridge import SuspensionBridge

        SuspensionBridge()
        # exec("from opstool.examples.SuspensionBridge import *")
    elif name.lower() == "sdof":
        from .examples.SDOF import SDOF

        SDOF()
        # exec("from opstool.examples.SDOF import *")
    elif name.lower() == "dambreak":
        from .examples.DamBreak import DamBreak

        DamBreak()
        # exec("from opstool.examples.DamBreak import *")
    elif name.lower() == "gridframe":
        from .examples.GridFrame import GridFrame

        GridFrame()
    elif name.lower() == "shell3d":
        from .examples.shell3D import Shell3D

        Shell3D()
    else:
        print(f"Not supported example {name}!")
        print(f"Now try treating {name} as your own model file and run it!")
        run_model(name)


def run_model(file_name: str):
    """
    Run your OpenSees model python file.

    Parameters
    ----------
    file_name: str
        OpenSees python file name.

    Returns
    --------
    None
    """
    # if not file_name.endswith(".py"):
    #     file_name += ".py"
    # with open(file_name, 'r') as f:
    #     exec(f.read())
    exec(f"from {file_name} import *")


def add_ops_hints_file():
    """Added the openseespy hints file.
    """
    src_file = Path(__file__).resolve().parent / "opensees.pyi"
    if sys.platform.startswith('linux'):
        import openseespylinux.opensees as ops
        tar_file = Path(ops.__file__).resolve().parent / "opensees.pyi"
    elif sys.platform.startswith('win'):
        import openseespywin.opensees as ops
        tar_file = Path(ops.__file__).resolve().parent / "opensees.pyi"
    elif sys.platform.startswith('darwin'):
        import openseespymac.opensees as ops
        tar_file = Path(ops.__file__).resolve().parent / "opensees.pyi"
    else:
        raise RuntimeError(sys.platform + ' is not supported yet')
    tar_file.write_text(src_file.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"opstool:: opensees.pyi file has been created to {tar_file}!")


def print_version():
    from .__about__ import __version__
    print(__version__)


def _get_random_color():
    colors = [
        "#00aeff",
        "#3369e7",
        "#8e43e7",
        "#b84592",
        "#ff4f81",
        "#ff6c5f",
        "#ffc168",
        "#2dde98",
        "#1cc7d0",
        "#ce181e",
        "#007cc0",
        "#ffc20e",
        "#0099e5",
        "#ff4c4c",
        "#34bf49",
        "#d20962",
        "#f47721",
        "#00c16e",
        "#7552cc",
        "#00bce4",
    ]
    idx = np.random.choice(15)
    return colors[idx]

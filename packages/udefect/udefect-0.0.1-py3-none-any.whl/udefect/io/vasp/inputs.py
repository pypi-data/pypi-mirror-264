# -*- coding: utf-8-*-

# This module contains all the necessary functionality for dealing with VASP input files


class Incar:
    """
    This class is used to read and write incar file and contains all the attribute associated with Incar and
    related methods.
    """

    def __init__(self):
        self.incar_data = {}  # Dictionary of uncommented tag
        self.incar_raw = []  # Raw info from INCAR
        # Global Paramter
        # self.SYSTEM = system

    def read_raw(self, file_path):
        """
        This function reads the information in an INCAR file and returns
        a incar_data dictionary with key value pair that will be used for calculations.
        It also returns a list containing all the comment line and also a raw list of lines.

        Params:
        -------
        self_path: string : path of the incar file


        Return:
        ------
        incar_data: dict : information in INCAR file
        incar_opt: dict : information in INCAR, which are commented
        incar_comments: list : Pure comments
        incar_raw: list : raw list containing each line of incar as elements


        Usage:
        ------
        >>> from udefect.io.vasp.inputs import Incar
        >>> incar_data, incar_opt, incar_comments, incar_raw = Incar.read_raw("./INCAR")

        """
        with open(file_path, "r") as f:
            incar_raw = f.read().split("\n")
        incar_comment = []
        incar_data = {}
        incar_opt = {}  # Optional Tags
        for ir in incar_raw:
            if "=" not in ir:
                incar_comment.append(ir)
            elif "=" in ir and "#" not in ir:
                d = ir.split("=")
                # Modify for magmom and other tag that takes more than one value separated by space
                incar_data[d[0].replace(" ", "")] = d[1].split()[0].replace(" ", "")
            elif "#" in ir and "=" in ir:
                d = ir.split("=")
                incar_opt[d[0].replace(" ", "").replace("#", "")] = d[1].split()[0]
        return incar_data, incar_opt, incar_comment, incar_raw

    def read(self, file_path):
        return self.read_raw(file_path)[0]

    def write(self, incar_data, file_path="./INCAR"):
        """
        This function writes the incar file in the specified path (default is current
        directory), given a dictionary of data where both the key and value are strings.
        """
        # file_path = os.path(file_path)
        write_info = ""
        for key in incar_data.keys():
            write_info += key + " = " + incar_data[key] + "\n"
        with open(file_path, "w") as f:
            f.write(write_info)

        return 0


class Poscar:
    """
    This class is used to deal with POSCAR files.
    """

    pass


class Potcar:
    """
    This class is used for dealing with POTCARs
    """

    pass


class Kpoints:
    """
    This class is used for dealing with KPOINTS file.
    """

    pass

elements = {"Ag": 106.905095,
            "Al": 26.981541,
            "Ar": 39.962383,
            "As": 74.921596,
            "Au": 196.96656,
            "B": 11.009305,
            "Ba": 137.905236,
            "Be": 9.012183,
            "Bi": 208.980388,
            "Br": 78.918336,
            "C": 12,
            "Ca": 39.962591,
            "Cd": 113.903361,
            "Ce": 139.905442,
            "Cl": 34.968853,
            "Co": 58.933198,
            "Cr": 51.94051,
            "Cs": 132.905433,
            "Cu": 62.929599,
            "D": 2.01355321274,
            "Dy": 163.929183,
            "e": 0.00054858,
            "Er": 165.930305,
            "Eu": 152.921243,
            "F": 18.998403,
            "Fe": 55.934939,
            "Ga": 68.925581,
            "Gd": 157.924111,
            "Ge": 73.921179,
            "H": 1.007825,
            "He": 4.002603,
            "Hf": 179.946561,
            "Hg": 201.970632,
            "Ho": 164.930332,
            "I": 126.904477,
            "In": 114.903875,
            "Ir": 192.962942,
            "K": 38.963708,
            "Kr": 83.911506,
            "La": 138.906355,
            "Li": 7.016005,
            "Lu": 174.940785,
            "Mg": 23.985045,
            "Mn": 54.938046,
            "Mo": 97.905405,
            "N": 14.003074,
            "Na": 22.98977,
            "Nb": 92.906378,
            "Nd": 141.907731,
            "Ne": 19.992439,
            "Ni": 57.935347,
            "O": 15.994915,
            "Os": 191.961487,
            "P": 30.973763,
            "Pb": 207.976641,
            "Pd": 105.903475,
            "Pr": 140.907657,
            "Pt": 194.964785,
            "Rb": 84.9118,
            "Re": 186.955765,
            "Rh": 102.905503,
            "Ru": 101.904348,
            "S": 31.972072,
            "Sb": 120.903824,
            "Sc": 44.955914,
            "Se": 79.916521,
            "Si": 27.976928,
            "Sm": 151.919741,
            "Sn": 119.902199,
            "Sr": 87.905625,
            "Ta": 180.948014,
            "Tb": 158.92535,
            "Te": 129.906229,
            "Th": 232.038054,
            "Ti": 47.947947,
            "Tl": 204.97441,
            "Tm": 168.934225,
            "U": 238.050786,
            "V": 50.943963,
            "W": 183.950953,
            "Xe": 131.904148,
            "Y": 88.905856,
            "Yb": 173.938873,
            "Zn": 63.929145,
            "Zr": 89.904708}


class Actions():
    def make_element(self, text, start, end):
        # print("element mass", text[start:end], elements[text[start:end]])
        return elements[text[start:end]]

    def make_term(self, _text, _start, _end, elements):
        if elements[1].text == "":
            # print("term mass:", elements[0])
            return elements[0]
        # print("term mass:", int(elements[1].text) * elements[0])
        return int(elements[1].text) * elements[0]

    def make_sub_formula(self, _text, _start, _end, elements):
        total = 0.0
        for e in elements[1]:
            total += e
        # print("sub_formula mass:", total)
        return total

    def make_ion_type(self, text, start, end, elements):
        total = 0.0
        for component in elements[3]:
            plus_minus = component.elements[0].text
            other_part = component.elements[1]
            if isinstance(other_part, float):
                if plus_minus == "+":
                    total += other_part
                else:
                    total -= other_part
            else:
                if other_part.elements[0].text == "":
                    multiplier = 1
                else:
                    multiplier = int(other_part.elements[0].text)
                if other_part.elements[1].text == "(":
                    sub_total = other_part.elements[2]
                else:
                    sub_total = 0.0
                    for e in other_part.elements[1]:  # TODO: Deal with case of count "(" mass ")"
                        # print("sub_total:", e)
                        sub_total += e
                if plus_minus == "+":
                    total += multiplier * sub_total
                else:
                    total -= multiplier * sub_total
                # for e in other_part.elements:
                #     print("subpart", e.text)
        mol_count = 1
        if elements[1].text != "":
            mol_count = int(elements[1].text)
        return {"molecular_ion": elements[2].text, "molecular_ion_count": mol_count, "delta_formula": elements[3].text, "delta": total, "z": elements[5].text}

    def make_mass(self, text, start, end, elements):
        # print("make mass:", self, text, start, end, elements)
        return float(text[start:end])

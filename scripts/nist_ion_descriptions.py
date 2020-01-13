from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self.count = elements[1]
        self.molecular_ion = elements[2]
        self.formulae = elements[3]
        self.charge_state = elements[5]
        self.radical = elements[6]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.plus_minus = elements[0]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self.count = elements[0]
        self.formula = elements[1]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.count = elements[0]
        self.mass = elements[2]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self.count = elements[0]
        self.plus_minus = elements[1]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self.count = elements[1]


class TreeNode7(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode7, self).__init__(text, offset, elements)
        self.formula = elements[1]


class TreeNode8(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode8, self).__init__(text, offset, elements)
        self.non_zero_digit = elements[0]


class TreeNode9(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode9, self).__init__(text, offset, elements)
        self.decimal = elements[1]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[1-9]')
    REGEX_2 = re.compile('^[0-9]')

    def _read_ion_type(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ion_type'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '[':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"["')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_count()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_molecular_ion()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_formulae()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 1]
                        if chunk1 == ']':
                            address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address5 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"]"')
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read_charge_state()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                address7 = self._read_radical()
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_ion_type(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['ion_type'][index0] = (address0, self._offset)
        return address0

    def _read_radical(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['radical'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '.':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"."')
        if address0 is FAILURE:
            address0 = TreeNode(self._input[index1:index1], index1)
            self._offset = index1
        self._cache['radical'][index0] = (address0, self._offset)
        return address0

    def _read_molecular_ion(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['molecular_ion'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == 'M':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"M"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 3]
            if chunk1 == 'Cat':
                address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                self._offset = self._offset + 3
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"Cat"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == 'An':
                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                    self._offset = self._offset + 2
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"An"')
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['molecular_ion'][index0] = (address0, self._offset)
        return address0

    def _read_formulae(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['formulae'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            index2, elements1 = self._offset, []
            address2 = FAILURE
            address2 = self._read_plus_minus()
            if address2 is not FAILURE:
                elements1.append(address2)
                address3 = FAILURE
                index3 = self._offset
                index4, elements2 = self._offset, []
                address4 = FAILURE
                address4 = self._read_count()
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_formula()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index4
                else:
                    elements2 = None
                    self._offset = index4
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode3(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                if address3 is FAILURE:
                    self._offset = index3
                    index5, elements3 = self._offset, []
                    address6 = FAILURE
                    address6 = self._read_count()
                    if address6 is not FAILURE:
                        elements3.append(address6)
                        address7 = FAILURE
                        chunk0 = None
                        if self._offset < self._input_size:
                            chunk0 = self._input[self._offset:self._offset + 1]
                        if chunk0 == '(':
                            address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address7 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"("')
                        if address7 is not FAILURE:
                            elements3.append(address7)
                            address8 = FAILURE
                            address8 = self._read_mass()
                            if address8 is not FAILURE:
                                elements3.append(address8)
                                address9 = FAILURE
                                chunk1 = None
                                if self._offset < self._input_size:
                                    chunk1 = self._input[self._offset:self._offset + 1]
                                if chunk1 == ')':
                                    address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address9 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('")"')
                                if address9 is not FAILURE:
                                    elements3.append(address9)
                                else:
                                    elements3 = None
                                    self._offset = index5
                            else:
                                elements3 = None
                                self._offset = index5
                        else:
                            elements3 = None
                            self._offset = index5
                    else:
                        elements3 = None
                        self._offset = index5
                    if elements3 is None:
                        address3 = FAILURE
                    else:
                        address3 = TreeNode4(self._input[index5:self._offset], index5, elements3)
                        self._offset = self._offset
                    if address3 is FAILURE:
                        self._offset = index3
                        address3 = self._read_mass()
                        if address3 is FAILURE:
                            self._offset = index3
                if address3 is not FAILURE:
                    elements1.append(address3)
                else:
                    elements1 = None
                    self._offset = index2
            else:
                elements1 = None
                self._offset = index2
            if elements1 is None:
                address1 = FAILURE
            else:
                address1 = TreeNode2(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['formulae'][index0] = (address0, self._offset)
        return address0

    def _read_charge_state(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['charge_state'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_count()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_plus_minus()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode5(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['charge_state'][index0] = (address0, self._offset)
        return address0

    def _read_plus_minus(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['plus_minus'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '+':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"+"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 1]
            if chunk1 == '-':
                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"-"')
            if address0 is FAILURE:
                self._offset = index1
        self._cache['plus_minus'][index0] = (address0, self._offset)
        return address0

    def _read_formula(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['formula'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            address1 = self._read_term()
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['formula'][index0] = (address0, self._offset)
        return address0

    def _read_term(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['term'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_element()
        if address1 is FAILURE:
            self._offset = index2
            address1 = self._read_sub_formula()
            if address1 is FAILURE:
                self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_count()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_term(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['term'][index0] = (address0, self._offset)
        return address0

    def _read_element(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['element'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'Zr':
            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"Zr"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'Zn':
                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"Zn"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == 'Yb':
                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                    self._offset = self._offset + 2
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"Yb"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == 'Y':
                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"Y"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 2]
                        if chunk4 == 'Xe':
                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                            self._offset = self._offset + 2
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"Xe"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == 'W':
                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                self._offset = self._offset + 1
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"W"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 1]
                                if chunk6 == 'V':
                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                    self._offset = self._offset + 1
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"V"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 1]
                                    if chunk7 == 'U':
                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                        self._offset = self._offset + 1
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"U"')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8 = None
                                        if self._offset < self._input_size:
                                            chunk8 = self._input[self._offset:self._offset + 2]
                                        if chunk8 == 'Tm':
                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                            self._offset = self._offset + 2
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('"Tm"')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9 = None
                                            if self._offset < self._input_size:
                                                chunk9 = self._input[self._offset:self._offset + 2]
                                            if chunk9 == 'Tl':
                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                self._offset = self._offset + 2
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('"Tl"')
                                            if address0 is FAILURE:
                                                self._offset = index1
                                                chunk10 = None
                                                if self._offset < self._input_size:
                                                    chunk10 = self._input[self._offset:self._offset + 2]
                                                if chunk10 == 'Ti':
                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                    self._offset = self._offset + 2
                                                else:
                                                    address0 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append('"Ti"')
                                                if address0 is FAILURE:
                                                    self._offset = index1
                                                    chunk11 = None
                                                    if self._offset < self._input_size:
                                                        chunk11 = self._input[self._offset:self._offset + 2]
                                                    if chunk11 == 'Th':
                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                        self._offset = self._offset + 2
                                                    else:
                                                        address0 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append('"Th"')
                                                    if address0 is FAILURE:
                                                        self._offset = index1
                                                        chunk12 = None
                                                        if self._offset < self._input_size:
                                                            chunk12 = self._input[self._offset:self._offset + 2]
                                                        if chunk12 == 'Te':
                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                            self._offset = self._offset + 2
                                                        else:
                                                            address0 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append('"Te"')
                                                        if address0 is FAILURE:
                                                            self._offset = index1
                                                            chunk13 = None
                                                            if self._offset < self._input_size:
                                                                chunk13 = self._input[self._offset:self._offset + 2]
                                                            if chunk13 == 'Tb':
                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                self._offset = self._offset + 2
                                                            else:
                                                                address0 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append('"Tb"')
                                                            if address0 is FAILURE:
                                                                self._offset = index1
                                                                chunk14 = None
                                                                if self._offset < self._input_size:
                                                                    chunk14 = self._input[self._offset:self._offset + 2]
                                                                if chunk14 == 'Ta':
                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                    self._offset = self._offset + 2
                                                                else:
                                                                    address0 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append('"Ta"')
                                                                if address0 is FAILURE:
                                                                    self._offset = index1
                                                                    chunk15 = None
                                                                    if self._offset < self._input_size:
                                                                        chunk15 = self._input[self._offset:self._offset + 2]
                                                                    if chunk15 == 'Sr':
                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                        self._offset = self._offset + 2
                                                                    else:
                                                                        address0 = FAILURE
                                                                        if self._offset > self._failure:
                                                                            self._failure = self._offset
                                                                            self._expected = []
                                                                        if self._offset == self._failure:
                                                                            self._expected.append('"Sr"')
                                                                    if address0 is FAILURE:
                                                                        self._offset = index1
                                                                        chunk16 = None
                                                                        if self._offset < self._input_size:
                                                                            chunk16 = self._input[self._offset:self._offset + 2]
                                                                        if chunk16 == 'Sn':
                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                            self._offset = self._offset + 2
                                                                        else:
                                                                            address0 = FAILURE
                                                                            if self._offset > self._failure:
                                                                                self._failure = self._offset
                                                                                self._expected = []
                                                                            if self._offset == self._failure:
                                                                                self._expected.append('"Sn"')
                                                                        if address0 is FAILURE:
                                                                            self._offset = index1
                                                                            chunk17 = None
                                                                            if self._offset < self._input_size:
                                                                                chunk17 = self._input[self._offset:self._offset + 2]
                                                                            if chunk17 == 'Sm':
                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                self._offset = self._offset + 2
                                                                            else:
                                                                                address0 = FAILURE
                                                                                if self._offset > self._failure:
                                                                                    self._failure = self._offset
                                                                                    self._expected = []
                                                                                if self._offset == self._failure:
                                                                                    self._expected.append('"Sm"')
                                                                            if address0 is FAILURE:
                                                                                self._offset = index1
                                                                                chunk18 = None
                                                                                if self._offset < self._input_size:
                                                                                    chunk18 = self._input[self._offset:self._offset + 2]
                                                                                if chunk18 == 'Si':
                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                    self._offset = self._offset + 2
                                                                                else:
                                                                                    address0 = FAILURE
                                                                                    if self._offset > self._failure:
                                                                                        self._failure = self._offset
                                                                                        self._expected = []
                                                                                    if self._offset == self._failure:
                                                                                        self._expected.append('"Si"')
                                                                                if address0 is FAILURE:
                                                                                    self._offset = index1
                                                                                    chunk19 = None
                                                                                    if self._offset < self._input_size:
                                                                                        chunk19 = self._input[self._offset:self._offset + 2]
                                                                                    if chunk19 == 'Se':
                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                        self._offset = self._offset + 2
                                                                                    else:
                                                                                        address0 = FAILURE
                                                                                        if self._offset > self._failure:
                                                                                            self._failure = self._offset
                                                                                            self._expected = []
                                                                                        if self._offset == self._failure:
                                                                                            self._expected.append('"Se"')
                                                                                    if address0 is FAILURE:
                                                                                        self._offset = index1
                                                                                        chunk20 = None
                                                                                        if self._offset < self._input_size:
                                                                                            chunk20 = self._input[self._offset:self._offset + 2]
                                                                                        if chunk20 == 'Sc':
                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                            self._offset = self._offset + 2
                                                                                        else:
                                                                                            address0 = FAILURE
                                                                                            if self._offset > self._failure:
                                                                                                self._failure = self._offset
                                                                                                self._expected = []
                                                                                            if self._offset == self._failure:
                                                                                                self._expected.append('"Sc"')
                                                                                        if address0 is FAILURE:
                                                                                            self._offset = index1
                                                                                            chunk21 = None
                                                                                            if self._offset < self._input_size:
                                                                                                chunk21 = self._input[self._offset:self._offset + 2]
                                                                                            if chunk21 == 'Sb':
                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                self._offset = self._offset + 2
                                                                                            else:
                                                                                                address0 = FAILURE
                                                                                                if self._offset > self._failure:
                                                                                                    self._failure = self._offset
                                                                                                    self._expected = []
                                                                                                if self._offset == self._failure:
                                                                                                    self._expected.append('"Sb"')
                                                                                            if address0 is FAILURE:
                                                                                                self._offset = index1
                                                                                                chunk22 = None
                                                                                                if self._offset < self._input_size:
                                                                                                    chunk22 = self._input[self._offset:self._offset + 1]
                                                                                                if chunk22 == 'S':
                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                    self._offset = self._offset + 1
                                                                                                else:
                                                                                                    address0 = FAILURE
                                                                                                    if self._offset > self._failure:
                                                                                                        self._failure = self._offset
                                                                                                        self._expected = []
                                                                                                    if self._offset == self._failure:
                                                                                                        self._expected.append('"S"')
                                                                                                if address0 is FAILURE:
                                                                                                    self._offset = index1
                                                                                                    chunk23 = None
                                                                                                    if self._offset < self._input_size:
                                                                                                        chunk23 = self._input[self._offset:self._offset + 2]
                                                                                                    if chunk23 == 'Ru':
                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                        self._offset = self._offset + 2
                                                                                                    else:
                                                                                                        address0 = FAILURE
                                                                                                        if self._offset > self._failure:
                                                                                                            self._failure = self._offset
                                                                                                            self._expected = []
                                                                                                        if self._offset == self._failure:
                                                                                                            self._expected.append('"Ru"')
                                                                                                    if address0 is FAILURE:
                                                                                                        self._offset = index1
                                                                                                        chunk24 = None
                                                                                                        if self._offset < self._input_size:
                                                                                                            chunk24 = self._input[self._offset:self._offset + 2]
                                                                                                        if chunk24 == 'Rh':
                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                            self._offset = self._offset + 2
                                                                                                        else:
                                                                                                            address0 = FAILURE
                                                                                                            if self._offset > self._failure:
                                                                                                                self._failure = self._offset
                                                                                                                self._expected = []
                                                                                                            if self._offset == self._failure:
                                                                                                                self._expected.append('"Rh"')
                                                                                                        if address0 is FAILURE:
                                                                                                            self._offset = index1
                                                                                                            chunk25 = None
                                                                                                            if self._offset < self._input_size:
                                                                                                                chunk25 = self._input[self._offset:self._offset + 2]
                                                                                                            if chunk25 == 'Re':
                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                self._offset = self._offset + 2
                                                                                                            else:
                                                                                                                address0 = FAILURE
                                                                                                                if self._offset > self._failure:
                                                                                                                    self._failure = self._offset
                                                                                                                    self._expected = []
                                                                                                                if self._offset == self._failure:
                                                                                                                    self._expected.append('"Re"')
                                                                                                            if address0 is FAILURE:
                                                                                                                self._offset = index1
                                                                                                                chunk26 = None
                                                                                                                if self._offset < self._input_size:
                                                                                                                    chunk26 = self._input[self._offset:self._offset + 2]
                                                                                                                if chunk26 == 'Rb':
                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                    self._offset = self._offset + 2
                                                                                                                else:
                                                                                                                    address0 = FAILURE
                                                                                                                    if self._offset > self._failure:
                                                                                                                        self._failure = self._offset
                                                                                                                        self._expected = []
                                                                                                                    if self._offset == self._failure:
                                                                                                                        self._expected.append('"Rb"')
                                                                                                                if address0 is FAILURE:
                                                                                                                    self._offset = index1
                                                                                                                    chunk27 = None
                                                                                                                    if self._offset < self._input_size:
                                                                                                                        chunk27 = self._input[self._offset:self._offset + 2]
                                                                                                                    if chunk27 == 'Pt':
                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                        self._offset = self._offset + 2
                                                                                                                    else:
                                                                                                                        address0 = FAILURE
                                                                                                                        if self._offset > self._failure:
                                                                                                                            self._failure = self._offset
                                                                                                                            self._expected = []
                                                                                                                        if self._offset == self._failure:
                                                                                                                            self._expected.append('"Pt"')
                                                                                                                    if address0 is FAILURE:
                                                                                                                        self._offset = index1
                                                                                                                        chunk28 = None
                                                                                                                        if self._offset < self._input_size:
                                                                                                                            chunk28 = self._input[self._offset:self._offset + 2]
                                                                                                                        if chunk28 == 'Pr':
                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                            self._offset = self._offset + 2
                                                                                                                        else:
                                                                                                                            address0 = FAILURE
                                                                                                                            if self._offset > self._failure:
                                                                                                                                self._failure = self._offset
                                                                                                                                self._expected = []
                                                                                                                            if self._offset == self._failure:
                                                                                                                                self._expected.append('"Pr"')
                                                                                                                        if address0 is FAILURE:
                                                                                                                            self._offset = index1
                                                                                                                            chunk29 = None
                                                                                                                            if self._offset < self._input_size:
                                                                                                                                chunk29 = self._input[self._offset:self._offset + 2]
                                                                                                                            if chunk29 == 'Pd':
                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                self._offset = self._offset + 2
                                                                                                                            else:
                                                                                                                                address0 = FAILURE
                                                                                                                                if self._offset > self._failure:
                                                                                                                                    self._failure = self._offset
                                                                                                                                    self._expected = []
                                                                                                                                if self._offset == self._failure:
                                                                                                                                    self._expected.append('"Pd"')
                                                                                                                            if address0 is FAILURE:
                                                                                                                                self._offset = index1
                                                                                                                                chunk30 = None
                                                                                                                                if self._offset < self._input_size:
                                                                                                                                    chunk30 = self._input[self._offset:self._offset + 2]
                                                                                                                                if chunk30 == 'Pb':
                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                else:
                                                                                                                                    address0 = FAILURE
                                                                                                                                    if self._offset > self._failure:
                                                                                                                                        self._failure = self._offset
                                                                                                                                        self._expected = []
                                                                                                                                    if self._offset == self._failure:
                                                                                                                                        self._expected.append('"Pb"')
                                                                                                                                if address0 is FAILURE:
                                                                                                                                    self._offset = index1
                                                                                                                                    chunk31 = None
                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                        chunk31 = self._input[self._offset:self._offset + 1]
                                                                                                                                    if chunk31 == 'P':
                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                        self._offset = self._offset + 1
                                                                                                                                    else:
                                                                                                                                        address0 = FAILURE
                                                                                                                                        if self._offset > self._failure:
                                                                                                                                            self._failure = self._offset
                                                                                                                                            self._expected = []
                                                                                                                                        if self._offset == self._failure:
                                                                                                                                            self._expected.append('"P"')
                                                                                                                                    if address0 is FAILURE:
                                                                                                                                        self._offset = index1
                                                                                                                                        chunk32 = None
                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                            chunk32 = self._input[self._offset:self._offset + 2]
                                                                                                                                        if chunk32 == 'Os':
                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                        else:
                                                                                                                                            address0 = FAILURE
                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                self._failure = self._offset
                                                                                                                                                self._expected = []
                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                self._expected.append('"Os"')
                                                                                                                                        if address0 is FAILURE:
                                                                                                                                            self._offset = index1
                                                                                                                                            chunk33 = None
                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                chunk33 = self._input[self._offset:self._offset + 1]
                                                                                                                                            if chunk33 == 'O':
                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                self._offset = self._offset + 1
                                                                                                                                            else:
                                                                                                                                                address0 = FAILURE
                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                    self._failure = self._offset
                                                                                                                                                    self._expected = []
                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                    self._expected.append('"O"')
                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                self._offset = index1
                                                                                                                                                chunk34 = None
                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                    chunk34 = self._input[self._offset:self._offset + 2]
                                                                                                                                                if chunk34 == 'Ni':
                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                else:
                                                                                                                                                    address0 = FAILURE
                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                        self._failure = self._offset
                                                                                                                                                        self._expected = []
                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                        self._expected.append('"Ni"')
                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                    self._offset = index1
                                                                                                                                                    chunk35 = None
                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                        chunk35 = self._input[self._offset:self._offset + 2]
                                                                                                                                                    if chunk35 == 'Ne':
                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                    else:
                                                                                                                                                        address0 = FAILURE
                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                            self._failure = self._offset
                                                                                                                                                            self._expected = []
                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                            self._expected.append('"Ne"')
                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                        self._offset = index1
                                                                                                                                                        chunk36 = None
                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                            chunk36 = self._input[self._offset:self._offset + 2]
                                                                                                                                                        if chunk36 == 'Nd':
                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                        else:
                                                                                                                                                            address0 = FAILURE
                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                self._expected = []
                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                self._expected.append('"Nd"')
                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                            self._offset = index1
                                                                                                                                                            chunk37 = None
                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                chunk37 = self._input[self._offset:self._offset + 2]
                                                                                                                                                            if chunk37 == 'Nb':
                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                            else:
                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                    self._expected = []
                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                    self._expected.append('"Nb"')
                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                self._offset = index1
                                                                                                                                                                chunk38 = None
                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                    chunk38 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                if chunk38 == 'Na':
                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                else:
                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                        self._expected = []
                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                        self._expected.append('"Na"')
                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                    self._offset = index1
                                                                                                                                                                    chunk39 = None
                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                        chunk39 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                    if chunk39 == 'N':
                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                        self._offset = self._offset + 1
                                                                                                                                                                    else:
                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                            self._expected = []
                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                            self._expected.append('"N"')
                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                        self._offset = index1
                                                                                                                                                                        chunk40 = None
                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                            chunk40 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                        if chunk40 == 'Mo':
                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                        else:
                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                self._expected = []
                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                self._expected.append('"Mo"')
                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                            self._offset = index1
                                                                                                                                                                            chunk41 = None
                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                chunk41 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                            if chunk41 == 'Mn':
                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                            else:
                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                    self._expected.append('"Mn"')
                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                chunk42 = None
                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                    chunk42 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                if chunk42 == 'Mg':
                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                else:
                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                        self._expected.append('"Mg"')
                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                    chunk43 = None
                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                        chunk43 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                    if chunk43 == 'Lu':
                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                    else:
                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                            self._expected.append('"Lu"')
                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                        chunk44 = None
                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                            chunk44 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                        if chunk44 == 'Li':
                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                        else:
                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                self._expected.append('"Li"')
                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                            chunk45 = None
                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                chunk45 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                            if chunk45 == 'La':
                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                            else:
                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                    self._expected.append('"La"')
                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                chunk46 = None
                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                    chunk46 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                if chunk46 == 'Kr':
                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                else:
                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                        self._expected.append('"Kr"')
                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                    chunk47 = None
                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                        chunk47 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                    if chunk47 == 'K':
                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                        self._offset = self._offset + 1
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                            self._expected.append('"K"')
                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                        chunk48 = None
                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                            chunk48 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                        if chunk48 == 'Ir':
                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                self._expected.append('"Ir"')
                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                            chunk49 = None
                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                chunk49 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                            if chunk49 == 'In':
                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                    self._expected.append('"In"')
                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                chunk50 = None
                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                    chunk50 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                if chunk50 == 'I':
                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                    self._offset = self._offset + 1
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                        self._expected.append('"I"')
                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                    chunk51 = None
                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                        chunk51 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                    if chunk51 == 'Ho':
                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                            self._expected.append('"Ho"')
                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                        chunk52 = None
                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                            chunk52 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                        if chunk52 == 'Hg':
                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                self._expected.append('"Hg"')
                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                            chunk53 = None
                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                chunk53 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                            if chunk53 == 'Hf':
                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                    self._expected.append('"Hf"')
                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                chunk54 = None
                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                    chunk54 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                if chunk54 == 'He':
                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                        self._expected.append('"He"')
                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                    chunk55 = None
                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                        chunk55 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                    if chunk55 == 'H':
                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                        self._offset = self._offset + 1
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                            self._expected.append('"H"')
                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                        chunk56 = None
                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                            chunk56 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                        if chunk56 == 'Ge':
                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                self._expected.append('"Ge"')
                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                            chunk57 = None
                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                chunk57 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                            if chunk57 == 'Gd':
                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                    self._expected.append('"Gd"')
                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                chunk58 = None
                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                    chunk58 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                if chunk58 == 'Ga':
                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                        self._expected.append('"Ga"')
                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                    chunk59 = None
                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                        chunk59 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                    if chunk59 == 'Fe':
                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                            self._expected.append('"Fe"')
                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                        chunk60 = None
                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                            chunk60 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                                        if chunk60 == 'F':
                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                                            self._offset = self._offset + 1
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                self._expected.append('"F"')
                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                            chunk61 = None
                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                chunk61 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                            if chunk61 == 'Eu':
                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                    self._expected.append('"Eu"')
                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                chunk62 = None
                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                    chunk62 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                if chunk62 == 'Er':
                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                        self._expected.append('"Er"')
                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                    chunk63 = None
                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                        chunk63 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                    if chunk63 == 'Dy':
                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                            self._expected.append('"Dy"')
                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                        chunk64 = None
                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                            chunk64 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                                                        if chunk64 == 'D':
                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                                                            self._offset = self._offset + 1
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                self._expected.append('"D"')
                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                                            chunk65 = None
                                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                chunk65 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                            if chunk65 == 'Cu':
                                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                                    self._expected.append('"Cu"')
                                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                                chunk66 = None
                                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                    chunk66 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                if chunk66 == 'Cs':
                                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                                        self._expected.append('"Cs"')
                                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                                    chunk67 = None
                                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                        chunk67 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                    if chunk67 == 'Cr':
                                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                                            self._expected.append('"Cr"')
                                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                                        chunk68 = None
                                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                            chunk68 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                        if chunk68 == 'Co':
                                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                self._expected.append('"Co"')
                                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                                                            chunk69 = None
                                                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                chunk69 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                            if chunk69 == 'Cl':
                                                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                    self._expected.append('"Cl"')
                                                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                                                chunk70 = None
                                                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                    chunk70 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                if chunk70 == 'Ce':
                                                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                        self._expected.append('"Ce"')
                                                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                                                    chunk71 = None
                                                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                        chunk71 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                    if chunk71 == 'Cd':
                                                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                            self._expected.append('"Cd"')
                                                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                                                        chunk72 = None
                                                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                            chunk72 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                        if chunk72 == 'Ca':
                                                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                self._expected.append('"Ca"')
                                                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                                                                            chunk73 = None
                                                                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                chunk73 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                                                                                            if chunk73 == 'C':
                                                                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                                                                                                self._offset = self._offset + 1
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                    self._expected.append('"C"')
                                                                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                                                                chunk74 = None
                                                                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                    chunk74 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                if chunk74 == 'Br':
                                                                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                        self._expected.append('"Br"')
                                                                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                                                                    chunk75 = None
                                                                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                        chunk75 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                    if chunk75 == 'Bi':
                                                                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                            self._expected.append('"Bi"')
                                                                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                                                                        chunk76 = None
                                                                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                            chunk76 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                        if chunk76 == 'Be':
                                                                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                self._expected.append('"Be"')
                                                                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                                                                                            chunk77 = None
                                                                                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                chunk77 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                            if chunk77 == 'Ba':
                                                                                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                    self._expected.append('"Ba"')
                                                                                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                                                                                chunk78 = None
                                                                                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                    chunk78 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                                                                                                                if chunk78 == 'B':
                                                                                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                                                                                                                    self._offset = self._offset + 1
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                        self._expected.append('"B"')
                                                                                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                                                                                    chunk79 = None
                                                                                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                        chunk79 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                                    if chunk79 == 'Au':
                                                                                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                            self._expected.append('"Au"')
                                                                                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                                                                                        chunk80 = None
                                                                                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                            chunk80 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                                        if chunk80 == 'As':
                                                                                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                                self._expected.append('"As"')
                                                                                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                            self._offset = index1
                                                                                                                                                                                                                                                                                                                                            chunk81 = None
                                                                                                                                                                                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                                chunk81 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                                            if chunk81 == 'Ar':
                                                                                                                                                                                                                                                                                                                                                address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                                    self._expected.append('"Ar"')
                                                                                                                                                                                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                                                                                                                                                                                chunk82 = None
                                                                                                                                                                                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                                    chunk82 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                                                if chunk82 == 'Al':
                                                                                                                                                                                                                                                                                                                                                    address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                                        self._expected.append('"Al"')
                                                                                                                                                                                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                                                                                                                                                                                    chunk83 = None
                                                                                                                                                                                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                                        chunk83 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                                                                                                                                                                                    if chunk83 == 'Ag':
                                                                                                                                                                                                                                                                                                                                                        address0 = self._actions.make_element(self._input, self._offset, self._offset + 2)
                                                                                                                                                                                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                                            self._expected.append('"Ag"')
                                                                                                                                                                                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                                        self._offset = index1
                                                                                                                                                                                                                                                                                                                                                        chunk84 = None
                                                                                                                                                                                                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                                                                                                                                                                                                            chunk84 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                                                                                                                                                                                                        if chunk84 == 'e':
                                                                                                                                                                                                                                                                                                                                                            address0 = self._actions.make_element(self._input, self._offset, self._offset + 1)
                                                                                                                                                                                                                                                                                                                                                            self._offset = self._offset + 1
                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                                                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                                                                                                                                                                                                self._expected = []
                                                                                                                                                                                                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                                                                                                                                                                                                self._expected.append('"e"')
                                                                                                                                                                                                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                                                                                                                                                                                                            self._offset = index1
        self._cache['element'][index0] = (address0, self._offset)
        return address0

    def _read_sub_formula(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['sub_formula'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_formula()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 == ')':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('")"')
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_sub_formula(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['sub_formula'][index0] = (address0, self._offset)
        return address0

    def _read_count(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['count'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_n()
        if address0 is FAILURE:
            address0 = TreeNode(self._input[index1:index1], index1)
            self._offset = index1
        self._cache['count'][index0] = (address0, self._offset)
        return address0

    def _read_n(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['n'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_non_zero_digit()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_digit()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode8(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['n'][index0] = (address0, self._offset)
        return address0

    def _read_non_zero_digit(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['non_zero_digit'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[1-9]')
        self._cache['non_zero_digit'][index0] = (address0, self._offset)
        return address0

    def _read_digit(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['digit'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_2.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[0-9]')
        self._cache['digit'][index0] = (address0, self._offset)
        return address0

    def _read_mass(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['mass'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '0':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"0"')
        if address1 is FAILURE:
            self._offset = index2
            address1 = self._read_n()
            if address1 is FAILURE:
                self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_decimal()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_mass(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['mass'][index0] = (address0, self._offset)
        return address0

    def _read_decimal(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['decimal'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '.':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"."')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_digit()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            address0 = TreeNode(self._input[index1:index1], index1)
            self._offset = index1
        self._cache['decimal'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_ion_type()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()

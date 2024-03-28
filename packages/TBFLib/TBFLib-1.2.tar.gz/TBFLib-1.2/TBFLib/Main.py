class Formula:
    """(formula, *args)"""

    def __init__(self, formula, *args):
        self.formula: str = formula
        self.args = args

    def calc(self, *args):
        if len(self.args) != len(args):
            raise ValueError()
        for n in range(len(self.args)):
            exec(f"{self.args[n]} = {args[n]}")
        ans = eval(self.formula)
        return ans

    def getargs(self):
        return self.args

    def getformula(self):
        return self.formula


class Limit:
    """(min_limit, value, max_limit, mode_min="e", mode_max="e")"""

    def __init__(self, min_limit, value, max_limit, mode_min="e", mode_max="e"):
        self.min = min_limit
        self.mode_min = mode_min
        self.value = value
        self.mode_max = mode_max
        self.max = max_limit
        if type(self.mode_min) != str and type(self.mode_max) != str:
            if self.max < self.min:
                raise ValueError()
        if not (self.mode_min == "n" or self.mode_min == "e"):
            raise ValueError()
        if not (self.mode_max == "n" or self.mode_max == "e"):
            raise ValueError()

    def getvalue(self):
        return self.value

    def check(self, value, num):
        if value != self.value:
            raise ValueError()
        if self.max == "infinity":
            if self.min == "infinity":
                return True
            else:
                if self.mode_min == "e":
                    return self.min <= num
                else:
                    return self.min < num
        else:
            if self.min == "infinity":
                if self.mode_max == "e":
                    return self.max > num
                else:
                    return self.max >= num
            else:
                if self.mode_max == "e":
                    if self.max >= num:
                        if self.mode_min == "e":
                            return self.min <= num
                        else:
                            return self.min < num
                    else:
                        return False
                else:
                    if self.max > num:
                        if self.mode_min == "e":
                            return self.min <= num
                        else:
                            return self.min < num
                    else:
                        return False

    def getlimit(self):
        if self.mode_max == "n":
            mode_max = "<"
        elif self.mode_max == "e":
            mode_max = "<="
        if self.mode_min == "n":
            mode_min = "<"
        elif self.mode_min == "e":
            mode_min = "<="
        limit = [str(self.min), mode_min, self.value, mode_max, str(self.max)]
        if self.min == "infinity":
            limit[0] = None
            limit[1] = None
        if self.max == "inifnity":
            limit[3] = None
            limit[4] = None
        limit = [i for i in limit if i is not None]
        if len(limit) == 1:
            limit[0] = "NoLimit"
        return "".join(limit)


class LimitedFormula:
    """(formula, *limits)"""

    def __init__(self, formula, *limits):
        self.formula: formula = formula
        self.limits = limits

    def calc(self, *args):
        for i in range(len(self.limits)):
            if not self.limits[i].check(self.formula.args[i], args[i]):
                return None
        ans = self.formula.calc(*args)
        return ans

    def getargs(self):
        return self.formula.getargs()

    def getformula(self):
        return self.formula.getformula()


class Formulas:
    """
    (*formulas) \n
    Don't mind Formula or LimitedFormula
    """

    def __init__(self, *formulas):
        self.formulas = formulas

    def calc(self, *args):
        answers = []
        for m in range(len(self.formulas)):
            answers.append(self.formulas[m].calc(*args))
        answers = [p for p in answers if p is not None]
        if len(answers) == 0:
            return None
        if len(answers) == 1:
            return answers[0]
        return tuple(answers)

    def getfomulas(self):
        return self.formulas


def get_formula_with_value(formulas, *values):
    ans = []
    for formula in formulas:
        if formula.calc(*values) is not None:
            ans.append(formula)
    return ans
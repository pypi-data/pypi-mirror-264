# ToriBird's Formula library (TBFLib)

This is ToriBird's Formula Library.  
You can use formula with limit, and Case-wise formulas.  
Link : https://pypi.org/project/TBFLib/

# How to use

* Normal Formula -> TBFLib.Formula("Your formula:str","Args in your formula:str")
* Limit -> TBFLib.Limit("min:number","value:str",max:number,"n(This means "<") or e(This means "<="):str","n or e")
* Limited Formula -> TBFLib.LimitedFormula("Your formula:Formula","Formula's Limit:Limit")
* Formulas -> TBFLib.Formulas("Formula","Formula"........)

# Sample

~~~python:sample.py
f = TBFLib.Formula("x**2 + 4 * x + 4", "x")
print(f.calc(4))
limit1 = TBFLib.Limit(2, "x", 10)
print(limit1.check("x", 1))
g = TBFLib.LimitedFormula(f, TBFLib.Limit(2, "x", 5))
print(g.calc(4))
fs = TBFLib.Formulas(f, g)
print(fs.calc(10))
f.getformula()
limit1.getlimit()
fs.getargs()
~~~

~~~
>>>36
>>>False
>>>36
>>>144
>>>x**2 + 4 * x + 4
>>>2<=x<=10
>>>"x"
~~~

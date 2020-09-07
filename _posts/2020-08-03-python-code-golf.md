---
layout: post
title: Python Roman Numeral Code Golf
excerpt: Some quick tips and tricks for code golfing Python. This challenge is to implement Roman Numeral to integer conversion and then back again in the shortest number of bytes.
---

A while back, a friend challenged me to a Python code golf. For those who don't know, [code golfing](https://www.wikiwand.com/en/Code_golf) is a competition to see who can achieve a goal with the shortest amount of source code. My friend challenged me to write two Python functions. One function takes a number and returns its roman numeral equivalent as a string. The second function takes a roman numeral string as an argument and returns its numerical equivalent. A number of test cases were also given:

```
cases = {
        5: "V",
        9: "IX",
        12: "XII",
        16: "XVI",
        29: "XXIX",
        44: "XLIV",
        45: "XLV",
        68: "LXVIII",
        83: "LXXXIII",
        97: "XCVII",
        99: "XCIX",
        500: "D",
        501: "DI",
        649: "DCXLIX",
        798: "DCCXCVIII",
        891: "DCCCXCI",
        1000: "M",
        1004: "MIV",
        1006: "MVI",
        1023: "MXXIII",
        2014: "MMXIV",
        3999: "MMMCMXCIX"
}
```

My method is to first write code that accomplishes the goal, then attempt to shorten it and try other methods to accomplish the goal. The first code I came up with was:

```
def toRomanNumeral(input): # 560 Bytes
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    text = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    endText = []
    if not isinstance(input, int):
        raise Exception("[-] Error: expected int")
    if (input <= 0) or (input > 3999):
        raise Exception("[-] This function only works from 1 to 3999")
    for i in range(len(values)):
        endText.append(text[i] * int(input / values[i]))
        input -= values[i] * int(input / values[i])
    return ''.join(endText)

def fromRomanNumeral(input): # 637 Bytes
    valuesDict = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    endValue = 0
    if not isinstance(input, basestring):
        raise Exception("[-] Error: Needs a string passed")
    input = input.upper()
    for i in range(len(input)):
        try:
            currentValue = valuesDict[input[i]]
            if (i + 1 < len(input)) and (valuesDict[input[i+1]] > currentValue):
                endValue -= currentValue
            else:
                endValue += currentValue
        except:
             raise Exception("[-] Error: input is not a valid roman numeral")
    return endValue
```

Understanding this code is left for the reader, it's fairly simple and the goal of post is to learn about golfing techniques. `fromRomanNumeral` is 638 bytes in length, and `toRomanNumeral` is 561 bytes in length. Not very good. But this is only the initial starting code, and lots can be improved. First, we have all our test cases already, which means we know what the function arguments will be so there is no need for error checking the function inputs or values generated.

```
def toRomanNumeral(input): # 364 Bytes
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    text = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    endText = []
    for i in range(len(values)):
        endText.append(text[i] * int(input / values[i]))
        input -= values[i] * int(input / values[i])
    return ''.join(endText)

def fromRomanNumeral(input): # 408 Bytes
    valuesDict = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    endValue = 0
    input = input.upper()
    for i in range(len(input)):
        currentValue = valuesDict[input[i]]
        if (i + 1 < len(input)) and (valuesDict[input[i+1]] > currentValue):
            endValue -= currentValue
        else:
            endValue += currentValue
    return endValue
```

That's a bit better. 408 bytes and 364 bytes. Next thing, variable and function names are taking up lots of unnecessary space, so we can reduce each name down to one letter.

```
def r(n): # 286 Bytes
    v = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    t = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    e = []
    for i in range(len(v)):
        e.append(t[i] * int(n / v[i]))
        n -= v[i] * int(n / v[i])
    return ''.join(e)

def s(n): # 266 Bytes
    v = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    e = 0
    n = n.upper()
    for i in range(len(n)):
        c = v[n[i]]
        if (i + 1 < len(n)) and (v[n[i+1]] > c):
            e -= c
        else:
            e += c
    return e
```

Sweet, now they are both below 300 bytes already. But there is still much room for improvement. How we currently assign variables uses a lot of unneeded space. In the function `toRomanNumerals()`, now simply named `r()`, we define variables on separate lines. this means we use three spaces, three equal signs, then 3 more spaces. Fortunately, Python allows us to do this a different way. Instead of writing:

```
v = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
t = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
e = []
```

We can instead declare the variables on a single line like this:

```
v,t,e=(1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'),[]
```

The current way of defining variables uses 141 bytes. Defining them on the same line uses 123 bytes. While we're at it, `('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')` can be shortened. Those repeated quotes use a lot of bytes. Instead of directly declaring an array (71 bytes), we can make a single string with spaces and use `.split()` to create an array like this: `'M CM D CD C XC L XL X IX V IV I'.split()` (41 bytes). We can also remove spaces from between the numbers defined in `v`.

In the other function `fromRomanNumeral()`, now named `s()`, we can shorten the variable declaration there too in the same way. Right now the function declares variables like this:

```
v = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
e = 0
n = n.upper()
```

`n = n.upper()` is not needed, it was just a sanity check for the input to the function. `v` and `e` can be declared on the same line. Instead of declaring a dictionary for `v` with brackets and then strings and ints, we can use `dict()` to declare a dictionary like `dict(M:1000,D:500...)`. This saves bytes from having to use quotes, and we can again remove spaces. This leaves us with:

```
v,e=dict(M=1000,D=500,C=100,L=50,X=10,V=5,I=1),0
```

We can also save an extra byte here by using exponential notation for declaring the dictionary value `M`. Instead of `M=1000`, it can be written like `M=1e3`. Now the functions look like this:

```
def r(n): # 230 Bytes
    v,t,e=(1000,900,500,400,100,90,50,40,10,9,5,4,1),'M CM D CD C XC L XL X IX V IV I'.split(),[]
    for i in range(len(v)):
        e.append(t[i] * int(n / v[i]))
        n -= v[i] * int(n / v[i])
    return ''.join(e)

def s(n): # 223 Bytes
    v,e=dict(M=1e3,D=500,C=100,L=50,X=10,V=5,I=1),0
    for i in range(len(n)):
        c = v[n[i]]
        if (i + 1 < len(n)) and (v[n[i+1]] > c):
            e -= c
        else:
            e += c
    return e
```

All of the test cases still pass. Looking at function `r()`, it's logic can be greatly improved. Instead of using `for i in range(len(v)):`, we can simply loop over `v` and define `i` above. This saves space and allows us to shorten the logic below. Also, instead of declaring `t` as an empty array and using `.join()` later, we can just declare `t` as an empty string and append to that.

```
def r(n): # 194 Bytes
    v,t,e,i=(1000,900,500,400,100,90,50,40,10,9,5,4,1),'M CM D CD C XC L XL X IX V IV I'.split(),'',0
    for a in v:
        e += n/a * t[i]
        n %= a
        i += 1
    return e
```

Furthermore, we can remove spaces from between the operators inside the `for` loop. Then we can add semicolons to the end of each line to get the entire for loop and operations within it onto the same line. This gets us to 162 bytes from the original 560!

```
def r(n): # 560 Bytes
    v,t,e,i=(1000,900,500,400,100,90,50,40,10,9,5,4,1),'M CM D CD C XC L XL X IX V IV I'.split(),'',0
    for a in v:e+=n/a*t[i];n%=a;i+=1;
    return e
```

Now we turn our attention back to function `s()`. Again, instead of `for i in range(len(input)):`, we can just declare `i` above and in this case loop over the input `n`. Changing the logic below results with:

```
def s(n): # 215 Bytes
    v,e,i=dict(M=1e3,D=500,C=100,L=50,X=10,V=5,I=1),0,0
    for a in n:
        if i+1<len(n) and v[n[i+1]]>v[a]:
            e = e - v[a]
        else:
            e = e + v[a]
        i += 1
    return e
```

Once again, we can remove space from operators. Then we can use [ternary operators](https://www.wikiwand.com/en/%3F:#/Python) to move the if and else statement to one line. Ternary operators work in the form of `result = x if a > b else y`. Using this, we can put most of the logic and `for` loop on the same line. Also on the same line, we can add a semicolon and add our `i+=1;` and have the entire `for` loop and logic on the same line!

```
def s(n): # 153 Bytes
    v,e,i=dict(M=1e3,D=500,C=100,L=50,X=10,V=5,I=1),0,0
    for a in n:e=e-v[a] if i+1<len(n) and v[n[i+1]]>v[a] else e+v[a];i+=1;
    return e
```

And finally, conditionals following parentheses, brackets, or braces do not to have a space between them. This leaves us with the following golfed functions.

```
def r1(n): # 163 Bytes
    v,e,t,i=(1000,900,500,400,100,90,50,40,10,9,5,4,1),'','M CM D CD C XC L XL X IX V IV I'.split(),0
    for a in v:e+=n/a*t[i];n%=a;i+=1;
    return e

def s1(n): # 151 Bytes
    v,e,i=dict(M=1e3,D=500,C=100,L=50,X=10,V=5,I=1),0,0
    for a in n:e=e-v[a]if i+1<len(n)and v[n[i+1]]>v[a]else e+v[a];i+=1;
    return e
```

163 and 151 bytes is significantly better than the 560 and 637 bytes we started out with. Happy code golfing!
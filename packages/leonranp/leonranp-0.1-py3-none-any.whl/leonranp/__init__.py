# --coding:UTF-8-- #
#Code by LeonMMcoset
'''
This is Leon Random Plus,that add more functions to the random!
To use it,code "import leonranp"

Copyright LeonMMcoset.All rights reserved.

Star my github project!
I will update more and more!
'''
#Code Running Info Start
print('-------------Leon Random Plus-------------')
print('You are using Leon Random Plus')
print('PyPI:https://pypi.org/project/leonranp/')
print('Wiki:http://leonmmcoset.jjmm.ink:8002/doku.php?id=leonranp')
print('Github:https://github.com/Leonmmcoset/leonranp/')
print('To upgrade,use "upgrade()" on your shell')
print('To have help,use "lrphelp()"')
print('To delete Leon Random Plus,use "dellrp()"')
print('------------------------------------------')
#Code Running Info End
from random import *
from os import *
#Start Code#
#randstr:just code "randstr()".
def randstr():
    randstrlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    randstr = choice(randstrlist)
    print(randstr)
#randcode:if you want to print code,code "print(randcode())"
#The randcode() values can be assigned in variables.
#To print randcode,code "print(randcode())"
def rcrandstr():
    rcrandstrlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    rcrandstr = choice(rcrandstrlist)
    return rcrandstr
def randcode(digits):
    randcode = ''
    for i in range(digits):
        if randint(0,1)==0:
            randcode = randcode + str(randint(0,9))
        else:
            randcode = randcode + str(rcrandstr())
    return randcode

#randbool:if you want to print on,code "randbool()"
#The randbool() values can be assigned in variables.
def randbool():
    randbool = randint(0,1)
    return bool(randbool)
#randspace:this is so unclear explanation!
#Please see on:http://leonmmcoset.jjmm.ink:8002/doku.php?id=leonranp#what_is_randspace
#To see,use "print(leonranp.randspace())"
def randspace(first,last):
    a = randint(0,100)
    if a >= first and a<= last:
        rsbool = 1
    else:
        rsbool = 0
    return bool(rsbool)
#randlistint/str/code:Random list int or str.
#To print it,"print(randlistint/str/code())"
def randlistint(list,intfirst,intlast):
    rlint = []
    for rli in range(list):
        rlint.append(randint(intfirst,intlast))
    return rlint
def randliststr(list):
    str = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    rlsa = []
    for rls in range(list):
        rlsa.append(choice(str))
    return rlsa
def randlistcode(list):
    rlc = []
    rlca = ''
    for rlcr in range(list):
        if randint(0, 1) == 0:
            rlc.append(str(rlca) + str(randint(0, 9)))
        else:
            rlc.append(str(rlca) + str(rcrandstr()))
    return rlc
#randstrbs:random string that is big and small.
#To print it,"print(randstrbs())"
def randstrbs():
    rsbsA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    rsbs = choice(rsbsA)
    return rsbs
#randcodebs:random code string that is big and small.
#To print it,"print(randcodebs())"
def randcodebs(digits):
    randcodebs = ''
    for rsbs in range(digits):
        rcbsR = randint(0,2)
        if rcbsR==0:
            randcodebs = randcodebs + str(randint(0, 9))
        elif rcbsR==1:
            randcodebs = randcodebs + str(rcrandstr())
        else:
            randcodebs = randcodebs + str(randstrbs())
    return randcodebs
#THIS MAY CRASH YOUR IDLE,PLEASE SAVE YOUR ALL FILES!!!
def crashidle():
    print('This may crash your IDLE!!!')
    print('Please sure you save your code!')
    input('Press <Enter> to begin crash.')
    while True:
        randcode(6)
#End Code#
#Start Upgrade Code(use "upgrade()" to upgrade Leon Random Plus)
def upgrade():
    system(f'pip install leonranp')
#End Upgrade Code
#You can use "leonranp.help()" to get help!
def lrphelp():
    print('---Leon Random Plus Help Start---')
    print('randstr() -> Random string')
    print('randcode(digits) -> Random code(such as print a675a or 687dsa or 7s8 and more)')
    print('upgrade() -> Upgrade Leon Random Plus')
    print('randbool() -> Random bool')
    print('dellrp() -> Delete Leon Random Plus')
    print('sample() -> Sample code')
    print('crashidle() -> Crash my IDLE')
    print('randstrbs() -> Random string that is big and small')
    print('randcodebs() -> Random code string that is big and small')
    print('---Leon Random Plus Help End---')
#Del. Leon Random Plus
#OMG you are gonna delete Leon Random Plus???
def dellrp():
    system(f'pip uninstall leonranp')
    print('Thanks for using Leon Random Plus!')
    print('Please restart your IDLE.')
#Sample code:
def sample():
    print('---Sample code section---')
    print('This is only for running sample code!')
    print('To check the source code of sample,go to http://http://leonmmcoset.jjmm.ink:8002/doku.php?id=leonranpsamplecode')
    print('1.Sample Captcha (6 digits)')
    print('2.Lucky Or Not')
    sample = int(input('Choose section:'))
    print('-------------------------')
    if sample == 1:
        a = randcode(6)
        print(a)
        b = input('Captcha code:')
        if a == b:
            print('True')
        else:
            print('False')
    if sample == 2:
        sam2 = randspace(0,30)
        if sam2 == True:
            print('You are so lucky today!')
        else:
            print('Oh no!You are not lucky today!')
            print('Go to http://leonmmcoset.jjmm.ink:8002/doku.php?id=iamnotlucky')
    print('--------------------------')
    print('Thanks for use!')
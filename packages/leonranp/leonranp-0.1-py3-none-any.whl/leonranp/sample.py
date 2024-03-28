#This is a sample code.
#To start,use "from leonranp import sample"
from leonranp import *
print('---Sample code section---')
print('1.Sample Captcha (6 digits)')
a = int(input('Choose section:'))
if a == 1:

    a = randcode(6)
    print(a)
    b = input('Captcha code:')
    if a == b:
        print('True')
    else:
        print('False')
print('--------------------------')
print('Thanks for use!')
import sys
import functools

_ascii = {'blue': '\033[34m',
          'yellow': '\033[33m',
          'green': '\033[32m',
          'red' :  '\033[31m',
          'black' :  '\033[30m',
          'cyan' :  '\033[36m',
          'white' :  '\033[37m',
          'purple' :  '\033[35m'
         }

def print_color(color,msg) :
    sys.stdout.write(_ascii[color]+msg+_ascii['white']+"\n")

# populate the namespace with all the different color functions
for k in _ascii :
    locals()[k] = functools.partial(print_color,k)

say = yellow

def test_print() :
    print_color("blue","yup")
    print_color("green","yup")
    print_color("red","yup")
    print_color("yellow","yup")
    print_color("black","yup")
    print_color("white","yup")


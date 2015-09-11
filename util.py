import sys
import functools

def ident(s) :
    def _(*args,**kwargs) :
        return s
    return _

def prompt(q,opts=['y','n']) :
    resp = "nopenopenope"
    while resp not in opts :
        print q+" [%s]"%''.join(opts)
        resp = raw_input().lower()
    return resp

_ascii = {  'blue': '\033[0;34m'
          , 'yellow': '\033[0;33m'
          , 'green': '\033[0;32m'
          , 'red' :  '\033[0;31m'
          , 'black' :  '\033[0;30m'
          , 'cyan' :  '\033[0;36m'
          , 'white' :  '\033[0;37m'
          , 'purple' :  '\033[0;35m'
          , 'hiyellow' :  '\033[1;33m'
          , 'hiwhite' :  '\033[1;37m'
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


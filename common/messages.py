# (c) 2014 jano <janoh@ksp.sk> 
# Various types of messages, with colors
import sys

__sow = sys.stdout.write
__sew = sys.stderr.write

__codemap = {
    'OK':'green', 'WA':'red', 'TLE':'purple', 'EXC':45, 'INT':41,
    'bad':'red', 'good':'green', 'ok':'yellow', 'fine':'blue', 'terrible':'INT',
    'red':91, 'green':92, 'yellow':93, 'blue':94, 'purple':95, 'cyan':96, 'white':37,
    'bold':1, 'dim':2, 'underlined':4, 'blink':5, 'invert':7,
}

# compile __codemap
changed = True
while changed:
    changed = False
    for key in __codemap:
        if isinstance(__codemap[key], str):
            __codemap[key] = __codemap[__codemap[key]]
            changed = True

def __testscore(p, m):
    __sew("%s%2s/%2s%s\n" % (scorecolor(p,m), p, m, resetcolor()))

def color_test():
    args = lambda: None
    setattr(args, 'colorful', True)
    messages_setup(args)

    info("white")
    infob("blue")
    infog("green")
    warning("warning")
    error("error", doquit=False)
    __sew(colorize('OK', 'ok') + colorize('WA', 'wa') + colorize('TLE', 'tle') +
          colorize('EXC', 'exc') + colorize('INT', 'int') + '\n')
    __sew(colorize('OK', 'ok', True) + colorize('WA', 'wa', True) + 
                    colorize('TLE', 'tle', True) + colorize('EXC', 'exc', True) +
                    colorize('INT', 'int', True) + '\n')
    for i in range(11):
        __testscore(i, 10)

def messages_setup(args):
    global __good,__fine,__ok,__bad,__terrible,__normal
    if args.colorful:
        __normal = '\033[0m'
    else:
        __normal = ''
    __good = __construct(code='good')
    __fine = __construct(code='fine')
    __ok = __construct(code='ok')
    __bad = __construct(code='bad')
    __terrible = __construct(code='terrible')
    
def error(text, doquit=True):
    __sew("%s%s%s\n" % (__terrible, text, __normal))
    if doquit: quit(1)
def warning(text):
    __sew("%s%s%s\n" % (__bad, text, __normal))
def infob(text):
    __sew("%s%s%s\n" % (__fine, text, __normal))
def infog(text):
    __sew("%s%s%s\n" % (__good, text, __normal))
def info(text):
    __sew("%s\n" % text)

def __construct(code=None, color=None, bold=None, underlined=None, blink=None):
    if __normal == '': return ''
    modifiers = []
    if code:
        modifiers.append(str(__codemap.get(code,'')))
        color = None 
    if color:
        modifiers.append(str(__codemap.get(color,'')))
    if bold is not None:
        modifiers.append(str((0 if bold else 20) + __codemap['bold']))
    if underlined is not None:
        modifiers.append(str((0 if underlined else 20) + __codemap['underlined']))
    if blink is not None:
        modifiers.append(str((0 if blink else 20) + __codemap['blink'])) 

    modifiers = [x for x in modifiers if x]
    if len(modifiers) == 0: return __normal
    return '\033[%sm' % ';'.join(modifiers)

def colorize(status, text, emph=None):
    return "%s%s%s" % (
        __construct(code=status, bold=emph), 
        text, 
        __normal)

def scorecolor(points, maxpoints):
    if __normal == '': return ''
    codes = [196, 208, 226, 228, 46]
    if points >= maxpoints: code = codes[4]
    elif 5*points >= maxpoints*4: code = codes[3]
    elif 2*points >= maxpoints: code = codes[2]
    elif points > 0: code = codes[1]
    else: code = codes[0]
    return '\033[38;5;%dm' % code

def headercolor():
    if __normal == '': return ''
    return __construct(color='blue')
     

def resetcolor():
    return __normal

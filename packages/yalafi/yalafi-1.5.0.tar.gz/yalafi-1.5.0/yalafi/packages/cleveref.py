"""
YaLafi module for LaTeX package cleveref
Contributed by @torik42 (at GitHub) in pull request #171
"""

import re
from yalafi.defs import InitModule, Macro
from yalafi import utils


require_packages = []

MACRO_READ_SED = '\\YYCleverefInput'


reference_commands = [
    ('\\cref', False),
    ('\\Cref', False),
    ('\\crefrange', True),
    ('\\Crefrange', True),
    ('\\cpageref', False),
    ('\\Cpageref', False),
    ('\\cpagerefrange', True),
    ('\\Cpagerefrange', True),
    ('\\labelcref', False),
    ('\\labelcpageref', False),
    ('\\namecref', False),
    ('\\nameCref', False),
    ('\\namecrefs', False),
    ('\\nameCrefs', False),
    ('\\lcnamecref', False),
    ('\\lcnamecrefs', False),
]
"""
Commands whose replacements are read from sed file based on given arguments.
The boolean value indicates, whether it is a usual command taking only one
argument or a range command taking two arguments.
"""

usual_commands = []
range_commands = []
for name, is_range in reference_commands:
    if is_range:
        range_commands.append('\\' + name)
    else:
        usual_commands.append('\\' + name)

# Regular Expressions used to read sed file:
re_ref = re.compile(r'''
s/\\
(                   # group 1: match usual commands
''' + '|'.join(usual_commands) + r'''
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^}{]+)        # group 3: the label of the reference
\}
/
    (.*)            # group 4: the replacement string
/g
''', re.VERBOSE)
r"""
Regular expression capturing cleverefs single reference commands.

Only the commands taking one argument are included. Others taking two
arguments like ``\crefrange`` are captured by :obj:`re_ref_range`.
"""

re_ref_range = re.compile(r'''
s/\\
(                   # group 1: match range commands
''' + '|'.join(range_commands) + r'''
)
(?:\\)?             # non capturing group
(\*?)               # group 2: '*' if present, '' else
\{
    ([^}{]+)        # group 3: the label of the first reference
\}
\{
    ([^}{]+)        # group 4: the label of the second reference
\}
/
    (.*)            # group 5: the replacement string
/g
''', re.VERBOSE)
r""" Regular expression capturing cleverefs range reference commands.

Only the commands taking two arguments are included. The standard
commands taking one arguments, like ``\cref``, are captured by
:obj:`re_ref`.
"""

re_command = re.compile(r'''
s/\\
(                   # group 1: command
    \\
    (               # group 2: capturing cC
        \[cC\]
    )?
    [a-zA-Z@]+
)
(                   # group 3: possible arguments
    (?:\{\.\*\})+
)?
\s*                 # possible whitespaces inbetween
/
    (.*)            # group 4: replacement
/g
''', re.VERBOSE)

re_cC = re.compile(r'(\[cC\])')
re_escaped_symbols = re.compile(r'\\([\[\]*\^$.\\])')


def unescape_sed(string):
    r"""
    Replaces certain strings that are escaped in sed file.
    Escaped are: ``. \ [ ] * ^ $``
    """
    return re_escaped_symbols.sub(r'\1', string)


# Error messages
MSG_POORMAN_OPTION = f'''To use cleveref with YaLafi, you need to use
*** the 'poorman' option and {MACRO_READ_SED}
*** to load the sed file.
'''
MSG_SED_NOT_LOADED = f'''To use cleveref with YaLafi, you should use
*** {MACRO_READ_SED} to load the sed file, e.g.
*** '{MACRO_READ_SED}{{main.sed}}' if your LaTeX
*** document is called 'main.tex'.
'''
MSG_CREF_UNDEFINED = r'''No replacement for {:}{{{:}}} known.
*** Run LaTeX again to build a new sed file.
'''
MSG_CREFRANGE_UNDEFINED = r'''No replacement for {:}{{{:}}}{{{:}}} known.
*** Run LaTeX again to build a new sed file.
'''


def init_module(parser, options, position):
    parms = parser.parms
    parms.newcommand_ignore.append(MACRO_READ_SED)

    macros_latex = r'''
        \newcommand{\crefname}[3]{}
        % \crefname is wrongly replaced by sed file!
        \newcommand{\Crefname}[3]{}
        \newcommand{\crefalias}[2]{}
    '''

    macros_python = [

        Macro(parms, MACRO_READ_SED, args='A', repl=h_read_sed),
        Macro(parms, '\\label', args='OA', repl=''),

    ]

    # Define functions which warn the User, whenever cleveref
    # is used without invoking \YYCleverefInput. These will be overwritten
    # by invoking \YYCleverefInput.
    for name, is_range in reference_commands:
        args = '*A' + 'A'*is_range
        macro = Macro(parms, name, args=args, repl=h_cref_warning)
        macros_python.append(macro)

    environments = []

    # Warn the user, whenever cleveref is used
    # without the poorman option:
    inject_tokens = []
    if not is_poorman_used(options):
        inject_tokens = utils.latex_error(parser, MSG_POORMAN_OPTION, position)

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                      environments=environments, inject_tokens=inject_tokens)


def h_read_sed(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler function for ``\YYCleverefInput``.

    Load the given sed file, generate all necessary replacements and
    recreate all cleveref reference commands.
    """
    if not parser.read_macros:
        return []

    # Read sed file into sed:
    file = parser.get_text_expanded(args[0])
    ok, sed = parser.read_macros(file)

    # Throw LaTeX error if the file could not be loaded:
    if not ok:
        return utils.latex_error(parser, 'could not read file ' + repr(file),
                                 pos)

    # Nested Dictionary in which all arguments and replacements are stored.
    # The structure is as follows
    #     '<command name>':
    #         '*':
    #             '<argument>' or ('<first argument>', '<second argument>'):
    #                 '<replacement>'
    #         '':
    #             '<argument>' or ('<first argument>', '<second argument>'):
    #                 '<replacement>'
    # The command name is any of the commands in reference_commands. The '*' or
    # '' says, whether a certain command is given with or without a star. The
    # argument is one particular argument given to the command. If the command
    # is a \…range command which takes to arguments a tuple of arguments is
    # given. The replacement is the string with which the particular command
    # should be replaced.
    refs = {}
    for name, is_range in reference_commands:
        refs[name] = {'': {}, '*': {}}

    for rep in sed.split('\n'):
        # only consider non-empty lines:
        if rep == '':
            continue

        # Match usual reference commands (e.g. \cref) and
        # save the replacement string:
        m = re_ref.match(rep)
        if m:
            refs[m.group(1)][m.group(2)][unescape_sed(m.group(3))] \
                = unescape_sed(m.group(4))
            continue

        # Match range reference command (e.g. \crefrange) and
        # save the replacement string:
        m = re_ref_range.match(rep)
        if m:
            key = (unescape_sed(m.group(3)), unescape_sed(m.group(4)))
            refs[m.group(1)][m.group(2)][key] \
                = unescape_sed(m.group(5))
            continue

        # Match any other command and create Macro objects for them.
        # See definition of re_command for more details:
        m = re_command.search(rep)
        # We need regexp.search here, because cleveref adds ranges
        # `<begin>,<end> s/…` to these sed commands in multi-language
        # documents. We only parse the first occurrence to get the versions
        # for the main language.
        if m:
            args = 'A'*int((m.end(3)-m.start(3))/4)
            string = unescape_sed(m.group(4))
            if m.group(2):
                name = re_cC.sub('c', m.group(1))
                if name not in parser.the_macros:
                    parser.the_macros[name] = Macro(parser.parms, name,
                                                    args=args, repl=string)
                name = re_cC.sub('C', m.group(1))
                if name not in parser.the_macros:
                    parser.the_macros[name] = Macro(parser.parms, name,
                                                    args=args, repl=string)
            else:
                name = m.group(1)
                if name not in parser.the_macros:
                    parser.the_macros[name] = Macro(parser.parms, name,
                                                    args=args, repl=string)

    # Make the Macro objects for all commands in reference_commands:
    for name, is_range in reference_commands:
        if is_range:
            parser.the_macros[name] = Macro(parser.parms,
                                            name, args='*AA',
                                            repl=h_make_crefrange(refs[name]))
        else:
            parser.the_macros[name] = Macro(parser.parms,
                                            name, args='*A',
                                            repl=h_make_cref(refs[name]))

    # \YYCleverefInput should not produce any output:
    return []


# TODO: Rename in next major release to g_make_cref
#   reflecting that it generates a macro handler function `handler`.
def h_make_cref(cref):
    "Create a Macro handler function for cleverefs single reference commands."
    def handler(parser, buf, mac, args, delim, pos):
        star = parser.get_text_direct(args[0])
        rep = parser.get_text_direct(args[1])
        if rep in cref[star]:
            toks = parser.parms.scanner.scan(cref[star][rep])
            for t in toks:
                t.pos = pos
            return toks
        return utils.latex_error(parser,
                                 MSG_CREF_UNDEFINED.format(mac.name,rep), pos)
    return handler


# TODO: Rename in next major release to g_make_crefrange
#   reflecting that it generates a macro handler function `handler`.
def h_make_crefrange(cref):
    "Create a Macro handler function for cleverefs range reference commands."
    def handler(parser, buf, mac, args, delim, pos):
        star = parser.get_text_direct(args[0])
        rep = (parser.get_text_direct(args[1]), parser.get_text_direct(args[2]))
        if rep in cref[star]:
            toks = parser.parms.scanner.scan(cref[star][rep])
            for t in toks:
                t.pos = pos
            return toks
        return utils.latex_error(parser,
                                 MSG_CREFRANGE_UNDEFINED.format(mac.name,*rep),
                                 pos)
    return handler


def h_cref_warning(parser, buf, mac, args, delim, pos):
    r"""
    Macro handler function for all cleveref commands before sed file is
    loaded.  These will be replaced, as soon as ``\YYCleverefInput`` is
    found in the file.  See :func:`h_read_sed`.
    """
    return utils.latex_error(parser, MSG_SED_NOT_LOADED, pos)


def is_poorman_used(options):
    r"Check whether ``'poorman'`` is contained in the given list of options."
    for opt in reversed(options):
        if 'poorman' in opt:
            return True
    return False

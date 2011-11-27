# InputTemplate class - A template for Python input requests.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A template for user input requests.

@author: Dario Giovannetti
@copyright: Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.com>
@license: GPLv3
@version: 1.0
@date: 2011-11-26

@todo: Permettere di impostare un timer per selezionare il valore di default
    (non quello di auto!) dopo un certo tempo.
@todo: Permettere di inserire piu' valori in prompt successivi, generando cosi'
    una lista.
@todo: Mostrare automaticamente, accanto a prompt o a wrong, tutti i valori
    possibili per l'input.

@var automode: If True, don't ask the user but use the auto input instead.
"""

automode = False


class InputTemplate():
    """
    A template for user input requests.
    
    @ivar group: The name of the group with the input string.
    @ivar string: The original input string.
    """
    def __init__(self, prompt='', inputs={}, default=None, auto=None, wrong='',
                                                              ignorecase=True):
        """
        Store a value from user input according to a dictionary, and also store
        the user input itself.
        
        @param prompt: The prompt message.
        @type prompt: string
        @param inputs: A dictionary with the possible input strings as tuples,
            structured this way::
            
              group: (input, input, ...),
              group: (input, input, ...),
              ...
                       
            Note that if an input belongs to more groups, only the last
            occurrence will be considered (cascading mode).
        @type inputs: dictionary
        @param default: The value returned if the input string does not belong
            to any group or is an empty string (the user pressed enter without
            writing anything); if unset, or set to None, the prompt will be
            showed again (possibly after the 'wrong' message); default can
            store any value, independently of the inputs dictionary.
        @type default: any
        @param auto: The value returned if automode (global) is True. If it's
            left unset, or set to None, and automode is True, this will raise a
            L{NoAutoInputValueError} exception; auto can store any value,
            independently of the inputs dictionary.
        @type auto: any
        @param wrong: If set, and default is unset or set to None, this message
            is returned if the input is not in the inputs dictionary, before
            displaying the prompt again.
        @type wrong: string
        @param ignorecase: If True (default) ignore input case, if False use
            case.
        @type ignorecase: boolean
        
        @raise NoAutoInputValueError: Raised if L{auto} is left unset, or set
            to None, and automode (global) is True.
        """
        inverted = {}
        for g in inputs:
            for v in inputs[g]:
                if ignorecase:
                    v = v.lower()
                inverted[v] = g
        
        if automode:
            if auto != None:
                self.group = auto
                self.string = auto
            else:
                raise NoAutoInputValueError('AutoInput mode is on, but there '
                                            'is no \'auto\' value set')
        elif default == None:
            while True:
                ans = input(prompt)
                if ignorecase:
                    key = ans.lower()
                else:
                    key = ans
                if key in inverted:
                    self.group = inverted[key]
                    self.string = ans
                    break
                elif wrong != '':
                    print(wrong)
        else:
            ans = input(prompt)
            if ignorecase:
                key = ans.lower()
            else:
                key = ans
            if key in inverted:
                self.group = inverted[key]
                self.string = ans
            else:
                self.group = default
                self.string = ans


class NoAutoInputValueError(ValueError):
    """
    Exception raised if auto (L{InputTemplate} constructor parameter) is left
    unset, or set to None, and L{automode} is True.
    """
    pass

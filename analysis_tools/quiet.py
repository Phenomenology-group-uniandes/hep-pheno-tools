import ROOT


class Quiet:
    ''' Context manager for silencing certain ROOT operations.  Usage:
    with Quiet(level = ROOT.kInfo+1):
       foo_that_makes_output

    You can set a higher or lower warning level to ignore different
    kinds of messages.  After the end of indentation, the level is set
    back to what it was previously.
    '''
    def __init__(self, level=ROOT.kError+1):
        self.oldlevel = ROOT.gErrorIgnoreLevel
        self.level = level

    def __enter__(self):
        ROOT.gErrorIgnoreLevel = self.level

    def __exit__(self, type, value, traceback):
        ROOT.gErrorIgnoreLevel = self.oldlevel

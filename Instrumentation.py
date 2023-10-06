from CParser import cparser

class Instrumentation:
    def instr(self, filename):
        cp = cparser.CParser()
        cp.parse(filename)
        '''
        with open(filename) as file:
            content = file.read()
            print(content)
        '''
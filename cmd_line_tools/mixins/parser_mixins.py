import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
       
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})
        # why not just doing arguments = {} ?
        # '''
        # if hasattr(self, self.ARGUMENTS_ATTR_NAME):
        #     arguments = self._arguments
        # else:
        #     arguments = {}
        # '''
        # 1) self._arguments = {}
        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments) 
        # 2) ===> self._arguments = arguments

# Can you implement an argparse version?

class AdvancedCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):   
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})
        
        # print(my_object.my_attribute)
        # print(get_attr(my_object, 'my_attribute', 'Hello'))
        
        parser = argparse.ArgumentParser()
        
        for argv in sys.argv:
            if '--' in argv:
                parser.add_argument(argv)
                
        parsed_args = parser.parse_args()  
        
        arguments.update(vars(parsed_args))
      
        
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)
      
        
          # for op in OPERATIONS:
        #     parser.add_argument("--{}".format(op))
            
        # python cmd.py arg1 arg2
        # python cmd.py --arg1=val1
# """
# python my_command.py username=bob paassword=12345
# python my_command.py --username bob --password 12345
# """
import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
       
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})
      
        # if hasattr(self, self.ARGUMENTS_ATTR_NAME):
        #     arguments = self._arguments
        # else:
        #     arguments = {}
        
       
        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments) 
        
        

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
      
        

    
#  # why not just doing arguments = {} ?
        # 1) self._arguments = {}
        # 2) ===> self._arguments = arguments

# python my_command.py username=bob paassword=12345
# python my_command.py --username bob --password 12345
# 
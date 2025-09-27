import re

from ...errors import Error


class Generator(object):

    def __init__(self):
        # self.namespace = 'a'
        self.asn1_members_backtrace = []
        self.dart_members_backtrace = []
        self.module_name = None
        self.type_name = None
        self.helper_lines = []
        self.base_variables = set()
        self.used_suffixes_by_base_variables = {}
        self.encode_variable_lines = []
        self.decode_variable_lines = []
        self.used_user_types = []

    def reset_type(self):
        self.helper_lines = []
        self.base_variables = set()
        self.used_suffixes_by_base_variables = {}
        self.encode_variable_lines = []
        self.decode_variable_lines = []
        self.used_user_types = []



    def generate_helpers(self, definitions):
        raise NotImplementedError('To be implemented by subclasses.')

    def generate(self, compiled):
        
        user_types = []

        types_code = '\n'.join(types_code)
        helpers = '\n'.join(self.generate_helpers(types_code))

        return helpers, types_code
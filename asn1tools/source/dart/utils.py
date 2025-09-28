import re

from ...errors import Error

TYPE_DECLARATION_FMT = '''\
/// Type {type_name} in module {module_name}.
{members}
'''

DEFINITION_FMT = '''
impl {module_name}{type_name} {{
    pub fn encode(&mut self, mut dst: &mut [u8]) -> Result<usize, Error> {{
        let mut encoder = Encoder::new(&mut dst);

        self.encode_inner(&mut encoder);

        encoder.get_result()
    }}

    pub fn decode(&mut self, src: &[u8]) -> Result<usize, Error> {{
        let mut decoder = Decoder::new(&src);

        self.decode_inner(&mut decoder);

        decoder.get_result()
    }}

    fn encode_inner(&mut self, encoder: &mut Encoder) {{
{encode_body}\
    }}

    fn decode_inner(&mut self, decoder: &mut Decoder) {{
{decode_body}\
    }}
}}
'''

ENCODER_AND_DECODER_STRUCTS = '''\
#[derive(Debug, PartialEq, Copy, Clone)]
pub enum Error {
    BadChoice,
    BadEnum,
    BadLength,
    OutOfData,
    OutOfMemory
}

struct Encoder<'a> {
    buf: &'a mut [u8],
    size: usize,
    pos: usize,
    error: Option<Error>
}

struct Decoder<'a> {
    buf: &'a[u8],
    size: usize,
    pos: usize,
    error: Option<Error>
}
'''

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


    def generate_type_declaration_process(self, type_, checker):
        raise NotImplementedError('To be implemented by subclasses.')

    def generate_definition_inner_process(self, type_, checker):
        raise NotImplementedError('To be implemented by subclasses.')

    def generate_helpers(self, definitions):
        raise NotImplementedError('To be implemented by subclasses.')

    def generate_type_declaration(self, compiled_type):
        type_ = compiled_type.type
        checker = compiled_type.constraints_checker.type

        lines = self.generate_type_declaration_process(type_, checker)

        if not lines:
            lines = ['dummy: u8;']

        if self.helper_lines:
            self.helper_lines.append('')

        return TYPE_DECLARATION_FMT.format(module_name=self.module_name,
                                           type_name=self.type_name,
                                           members='\n'.join(lines))

    def generate_definition(self, compiled_type):
        encode_lines, decode_lines = self.generate_definition_inner_process(
            compiled_type.type,
            compiled_type.constraints_checker.type)

        if self.encode_variable_lines:
            encode_lines = self.encode_variable_lines + [''] + encode_lines

        if self.decode_variable_lines:
            decode_lines = self.decode_variable_lines + [''] + decode_lines

        encode_lines = indent_lines(indent_lines(encode_lines)) + ['']
        decode_lines = indent_lines(indent_lines(decode_lines)) + ['']

        return DEFINITION_FMT.format(module_name=self.module_name,
                                     type_name=self.type_name,
                                     encode_body='\n'.join(encode_lines),
                                     decode_body='\n'.join(decode_lines))

    def generate(self, compiled):
        
        user_types = []

        for module_name, module in sorted(compiled.modules.items()):
            self.module_name = module_name

            for type_name, compiled_type in sorted(module.items()):
                self.type_name = type_name
                self.reset_type()

                print (f'Generating {module_name}.{type_name},{compiled_type}...')

                type_declaration = self.generate_type_declaration(compiled_type)
                definition = self.generate_definition(compiled_type)
                
                # user_type = _UserType(type_name,
                #                       module_name,
                #                       type_declaration + definition,
                #                       self.used_user_types)
                # user_types.append(user_type)

        user_types = sort_user_types_by_used_user_types(user_types)

        types_code = []

        for user_type in user_types:
            types_code.append(user_type.type_code)

        types_code = '\n'.join(types_code)
        helpers = '\n'.join(self.generate_helpers(types_code))

        return helpers, types_code
    
def strip_blank_lines(lines):
    try:
        while lines[0] == '':
            del lines[0]

        while lines[-1] == '':
            del lines[-1]
    except IndexError:
        pass

    stripped = []

    for line in lines:
        if line == '' and stripped[-1] == '':
            continue

        stripped.append(line)

    return stripped

def indent_lines(lines, width=4):
    indented_lines = []

    for line in lines:
        if line:
            indented_line = width * ' ' + line
        else:
            indented_line = line

        indented_lines.append(indented_line)

    return strip_blank_lines(indented_lines)


def dedent_lines(lines, width=4):
    return [line[width:] for line in lines]

def sort_user_types_by_used_user_types(user_types):
    reversed_sorted_user_types = []

    for user_type in user_types:
        user_type_name_tuple = (user_type.type_name, user_type.module_name)

        # Insert first in the reversed list if there are no types
        # using this type.
        insert_index = 0

        for i, reversed_sorted_user_type in enumerate(reversed_sorted_user_types, 1):
            if user_type_name_tuple in reversed_sorted_user_type.used_user_types:
                if i > insert_index:
                    insert_index = i

        reversed_sorted_user_types.insert(insert_index, user_type)

    return reversed(reversed_sorted_user_types)

"""Json Encoding Rules (JER) Dart source code codec generator.

"""

from .utils import ENCODER_AND_DECODER_STRUCTS
# from .utils import ENCODER_ABORT
# from .utils import DECODER_ABORT
from .utils import Generator
# from .utils import is_user_type
# from .utils import indent_lines
# from .utils import dedent_lines
# from .utils import make_camel_case
from ...codecs import jer



class _Generator(Generator):

    def format_real(self):
        return []

    def get_enumerated_values(self, type_):
        return sorted(type_.root_data_to_index)

    def get_choice_members(self, type_):
        return type_.root_index_to_member.values()

    def generate_encoder(self, definitions):
        functions = [
            # ('encoder.init(', ENCODER_INIT),
            # ('encoder.get_result(', ENCODER_GET_RESULT),
            # ('encoder.abort(', ENCODER_ABORT),
            # ('encoder.append_bit(', ENCODER_ALLOC),
            # ('encoder.append_bit(', ENCODER_APPEND_BIT),
            # ('encoder.append_bytes(', ENCODER_APPEND_BYTES),
            # ('encoder.append_u8(', ENCODER_APPEND_U8),
            # ('encoder.append_u16(', ENCODER_APPEND_U16),
            # ('encoder.append_u32(', ENCODER_APPEND_U32),
            # ('encoder.append_u64(', ENCODER_APPEND_U64),
            # ('encoder.append_i8(', ENCODER_APPEND_I8),
            # ('encoder.append_i16(', ENCODER_APPEND_I16),
            # ('encoder.append_i32(', ENCODER_APPEND_I32),
            # ('encoder.append_i64(', ENCODER_APPEND_I64),
            # ('encoder.append_bool(', ENCODER_APPEND_BOOL),
            # (
            #     'encoder.append_non_negative_binary_integer(',
            #     ENCODER_APPEND_NON_NEGATIVE_BINARY_INTEGER
            # )
        ]

        helpers = [
            # "impl<'a> Encoder<'a> {",
            # "    fn new(dst: &'a mut [u8]) -> Encoder {",
            # '        Encoder {',
            # '            size: 8 * dst.len(),',
            # '            buf: dst,',
            # '            pos: 0,',
            # '            error: None',
            # '        }',
            # '    }'
        ]

        for pattern, definition in functions:
            if pattern in definitions:
                helpers.append(definition)

        return helpers + ['}', '']

    def generate_decoder(self, definitions):
        functions = [
            # ('decoder.init(', DECODER_INIT),
            # ('decoder.get_result(', DECODER_GET_RESULT),
            # ('decoder.abort(', DECODER_ABORT),
            # ('decoder.read_bit(', DECODER_FREE),
            # ('decoder.read_bit(', DECODER_READ_BIT),
            # ('decoder.read_bytes(', DECODER_READ_BYTES),
            # ('decoder.read_u8(', DECODER_READ_U8),
            # ('decoder.read_u16(', DECODER_READ_U16),
            # ('decoder.read_u32(', DECODER_READ_U32),
            # ('decoder.read_u64(', DECODER_READ_U64),
            # ('decoder.read_i8(', DECODER_READ_I8),
            # ('decoder.read_i16(', DECODER_READ_I16),
            # ('decoder.read_i32(', DECODER_READ_I32),
            # ('decoder.read_i64(', DECODER_READ_I64),
            # ('decoder.read_bool(', DECODER_READ_BOOL),
            # (
            #     'decoder.read_non_negative_binary_integer(',
            #     DECODER_READ_NON_NEGATIVE_BINARY_INTEGER
            # )
        ]

        helpers = [
            # "impl<'a> Decoder<'a> {",
            # "    fn new(src: &'a[u8]) -> Decoder {",
            # '        Decoder {',
            # '            buf: src,',
            # '            size: 8 * src.len(),',
            # '            pos: 0,',
            # '            error: None',
            # '        }',
            # '    }'
        ]

        for pattern, definition in functions:
            if pattern in definitions:
                helpers.append(definition)

        return helpers + ['}']

    def generate_type_declaration_process(self, type_, checker):
        pass

    def generate_definition_inner_process(self, type_, checker):
        pass

    # Generate helper functions for encoding and decoding
    # override in subclasses to add more helpers.
    def generate_helpers(self, definitions):
        helpers = [ENCODER_AND_DECODER_STRUCTS]
        helpers += self.generate_encoder(definitions)
        helpers += self.generate_decoder(definitions)

        return helpers + ['']

def generate(compiled):
    return _Generator().generate(compiled)
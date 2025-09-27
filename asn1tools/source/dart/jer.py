"""Json Encoding Rules (JER) Dart source code codec generator.

"""

# from .utils import ENCODER_AND_DECODER_STRUCTS
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


def generate(compiled):
    return _Generator().generate(compiled)
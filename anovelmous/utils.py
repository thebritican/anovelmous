from models import NovelToken
import time


def substitute_bit_stream(result, available_tokens):
    available_token_indices = [token.id for token in available_tokens]
    bit_stream = []
    last_index = 0
    for token_index in available_token_indices:
        num_zeroes = token_index - last_index - 1
        zeroes = ['0' for i in range(num_zeroes)]
        bit_stream.extend(zeroes)
        bit_stream.append('1')
        last_index = token_index

    last_available_token_index = available_token_indices[-1]
    trailing_zeroes = ['0' for i in range(result['num_results'] - last_available_token_index)]
    bit_stream.extend(trailing_zeroes)
    bit_stream = ''.join(bit_stream)
    result['bit_stream'] = bit_stream


def get_candidate_ordinal(chapter_id):
    current_novel_token = NovelToken.query.filter_by(chapter_id=chapter_id).order_by('-ordinal').first()
    return current_novel_token.ordinal + 1


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f seconds' % (f.func_name, (time2-time1))
        # TODO: Eventually log this timing decorator
        return ret
    return wrap
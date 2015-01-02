import arrow
from models import NovelToken, db
import utils


def select_new_novel_token(chapter_id):
    """
    Will select the most popular, grammatically correct vote during the last 10 seconds.
    :return: a novel token object
    """
    # TODO: make time-sensitive
    query = '''SELECT V.token, COUNT(V.id) as token_count
               FROM vote V
               GROUP BY V.token
               ORDER BY token_count DESC
               LIMIT 1'''

    result = db.engine.execute(query)
    most_popular_vote = result[0]

    new_story_token = NovelToken(
        token=most_popular_vote.token,
        ordinal=utils.get_candidate_ordinal(chapter_id),
        chapter_id=chapter_id
    )

    db.session.add(new_story_token)
    db.session.commit()

    return new_story_token

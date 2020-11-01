# pylint: disable=c0111

from nbhosting.courses import (
    Track, Section, Notebook,
    notebooks_by_patterns, track_by_directory)

def tracks(coursedir):
    """
    coursedir is a CourseDir object that points
    at the root directory of the filesystem tree
    that holds notebooks

    result is a list of Track instances
    """

    track_specs = [
        ('Python avancé', 'Python avancé', 'python', [
            ('1/9: jeux', 'notebooks/1-*.md', 'tps/games/README.md'),
            ('2/9: types de base',
               'quiz/2*.md',
               'notebooks/2-0[0-4]*.md',
               'notebooks/2-09*.md',
            ),
            ('3/9: hash tables',
             # les quiz (le quiz sur le snake était en panne)
              'quiz/2*.md',
              'quiz/3*.md',
              # intro
              'notebooks/3-00*.md',
              # rappel exos semaine passée
              'notebooks/2-09*.md',
              # containers 2/2
              'notebooks/2-05*.md',
              'notebooks/3-1*.md',
              'tps/dijkstra/README.md',
              'notebooks/3-9*.md',
            ),
            ('4/9: itérations',
             'quiz/4*.md',
             'notebooks/4-00*.md',
             'tps/dijkstra/README.md',
             'notebooks/4-11*.md',
             # exos
             'notebooks/4-90*.md',
            ),
            ('5/9: itérations et classes',
             'quiz/5*.md',
             'notebooks/5-00*.md',
             'notebooks/4-90*.md',
             'notebooks/4-12*.md',
             'notebooks/4-91*.md',
             'notebooks/5-1*.md',
             'notebooks/5-9*.md',
             ),
            ('6/9: ???', 'quiz/6*.md', 'notebooks/6-*.md'),
            ('7/9: ???', 'quiz/7*.md', 'notebooks/7-*.md'),
            ('8/9: ???', 'quiz/8*.md', 'notebooks/8-*.md'),
            ('9/9: ???', 'quiz/9*.md', 'notebooks/9-*.md'),
        ])]

    return [Track(coursedir,
                  [Section(coursedir=coursedir,
                           name=section_name,
                           notebooks=notebooks_by_patterns(
                               coursedir, patterns))
                   for section_name, *patterns in section_specs],
                  name=track_name,
                  description=track_description,
                  id=track_id)
            for (track_name, track_description, track_id, section_specs) in track_specs]

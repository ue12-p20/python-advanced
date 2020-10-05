# pylint: disable=c0111

from nbhosting.courses import (
    Track, Section, Notebook,
    notebooks_by_pattern, track_by_directory)

def tracks(coursedir):
    """
    coursedir is a CourseDir object that points
    at the root directory of the filesystem tree
    that holds notebooks

    result is a list of Track instances
    """

    track_specs = [
        ('Python avancé', 'Python avancé', 'python',
         [ ('jeux', 'notebooks/1-*.md'), ]),
        ]

    return [Track(coursedir,
                  [Section(coursedir=coursedir,
                           name=section_name,
                           notebooks=notebooks_by_pattern(
                               coursedir, pattern))
                   for section_name, pattern in section_specs],
                  name=track_name,
                  description=track_description,
                  id=track_id)
            for (track_name, track_description, track_id, section_specs) in track_specs]

from IPython.nbconvert.preprocessors import *

# quick and dirty - that must exist some place else
def indent(text, space=4):
    sep = space * ' '
    return ''.join( f"{sep}{line}\n" for line in text.split("\n"))
 
def html_rule(color):
    return f'<hr style="height:10px; border-width: 0px;background-color: {color}">'

level_colors = {
    'level_basic': "#b2f7ef",
    'level_intermediate': "#7bdff2",
    'level_advanced': "#f92a82",
}

class CourseLevels(Preprocessor):
    """
    decorate courselevels cells with colors
    using hard-wired html styles for now
    """

    def preprocess_cell(self, cell, resources, index):
        # leave code unchanged
        if cell.cell_type != "markdown":
             return cell, resources
        if 'tags' in cell.metadata:
            tags = cell.metadata['tags']
            for l, c in level_colors.items():
                if l in tags:
                    rule = html_rule(c)
                    cell.source = (f".. raw:: html\n\n{indent(rule, 3)}\n\n"
                                   f"{cell.source}\n\n"
                                   f".. raw:: html\n\n{indent(rule, 3)}\n\n")
                    break
        return cell, resources

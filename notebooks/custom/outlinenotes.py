from IPython.nbconvert.preprocessors import *

# quick and dirty - that must exist some place else
def indent(text, space=4):
    sep = space * ' '
    return ''.join( f"{sep}{line}\n" for line in text.split("\n"))
    

class OutlineNotes(Preprocessor):
    """
    decorate cells marked as 'notes' with a 'slide-notes' 
    CSS class
    """

    def preprocess_cell(self, cell, resources, index):
        """
        embed 'notes' cells as a ReST note
        """
        # leave code unchanged
        if cell.cell_type != "markdown":
             return cell, resources
        if ('slideshow' in cell.metadata and 
             cell.metadata['slideshow']['slide_type'] == 'notes'):
            cell.source = f".. note::\n\n{indent(cell.source)}\n"
        return cell, resources

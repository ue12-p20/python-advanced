---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed
  formats: md:myst
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
notebookname: "quiz it\xE9rations"
version: '1.0'
---

# quiz

**évaluez la cellule suivante** pour faire apparaitre le quiz sur les itérations

```{code-cell} ipython3
:hide_input: false
:tags: [raises-exception]

from nbautoeval import run_yaml_quiz
run_yaml_quiz("iters", "quiz")
```

****

```{code-cell} ipython3
from nbautoeval import quiz_help
quiz_help("fr")
```

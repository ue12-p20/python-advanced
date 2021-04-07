---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
nbhosting:
  title: 'TP: progressbars'
---

```{code-cell} ipython3
import asyncio
```

```{code-cell} ipython3
import aiohttp
```

# TP : un downloader http avec des progressbar

+++

On va reprendre l'idée démontrée dans la séquence sur `async with` et `async for` pour fabriquer un downloader qui peut s'occuper de plusieurs URLs à la fois et qui nous donne une idée de où on en est dans le téléchargement.

Je commence par vous montrer quelques briques technologiques qui vont nous servir

+++

## ipywidgets

```{code-cell} ipython3
from ipywidgets import FloatProgress, HTML, Layout, VBox, HBox, Valid
```

En guise de rappel par rapport à la dernière fois, voici quelques widgets de la ménagerie `ipywidgets` qui vont nous servir

pour retrouver le lien vous pouvez googler juste `ipywidgets list`

+++

### la progress bar

```{code-cell} ipython3
w1 = FloatProgress(value=0, description='file1', layout=Layout(width='100%'))
```

```{code-cell} ipython3
display(w1)
```

```{code-cell} ipython3
w1.value = 10
```

```{code-cell} ipython3
w1.description
```

### la tick box

+++

j'ai hésité entre deux options, finalement j'ai choisi `HTML` mais à vous de voir

```{code-cell} ipython3
:cell_style: split

w2 = Valid(value=False); display(w2)
```

```{code-cell} ipython3
:cell_style: split

w2.value = True
```

ou alors

```{code-cell} ipython3
:cell_style: split

w3 = HTML("truc"); display(w3)
```

```{code-cell} ipython3
:cell_style: split

w3.value = "bidule"
```

### les assemblages

+++

je vous rappelle aussi qu'on peut faire des assemblages simples avec `VBox` et `HBox`, 
d'ailleurs il n'y a pas que cette option là,
je vous laisse regarder la doc

+++

## ce qu'on vous demande de faire

```{code-cell} ipython3
urls = ["https://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "https://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "https://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "https://www.irs.gov/pub/irs-pdf/f1040sb.pdf",
]
```

<span style='background-color: #9EBC9E; padding:5px;'>↓↓↓↓↓ ↓↓↓↓↓ assurez-vous de **bien évaluer la cellule cachée** ici ↓↓↓↓↓ ↓↓↓↓↓</span>

```{code-cell} ipython3
:hide_input: true
:tags: []

class VisualDownloader:
    
    def __init__(self, urls):
        self.urls = urls
        self.task = None
        
    def name(self, url):
        return url.split('/')[-1]

    def create_dashboard(self):
        self.tickboxes = {
            url: HTML("<span style='color:red;'>&cross;</span>") 
            for url in urls
        }
        self.sliders = {
            url: FloatProgress(value=0, 
                                description=self.name(url),
                                layout=Layout(width='100%'))
            for url in urls
        }
        self.dashboard = VBox(
            [HBox([tickbox, slider])
             for tickbox, slider in zip(self.tickboxes.values(), self.sliders.values())
            ]
        )
        display(self.dashboard)
        
    def download(self):
        async def fetch(url):
            total_length = 0
            read_so_far = 0
            async with aiohttp.ClientSession() as session:
                
                async with session.get(url) as response:
                    if response.status == 200:
                        self.tickboxes[url].value = "<span style='color:green;'>&#10003;</span>"
                    #print(f"{url} returned status {response.status}")
                    total_length = int(response.content_length)
                    async for line in response.content:
                        read_so_far += len(line)
                        self.sliders[url].value = 100 * (read_so_far / total_length)
                    if read_so_far == total_length:
                        self.sliders[url].bar_style = 'info'
                    else:
                        self.sliders[url].bar_style = 'danger'                    
            return read_so_far, total_length
        self.task = asyncio.ensure_future(
            asyncio.gather(
                *(fetch(url) for url in self.urls)
            )
        )
        
    def troubleshoot(self):
        # check self.task
        # TODO: check if self.task is ready and in the proper state
        print(f"{self.task.result()=}")
        print(f"{self.task.exception()=}")
```

<span style='background-color: #9EBC9E; padding:5px;'>↑↑↑↑↑ ↑↑↑↑↑ assurez-vous de **bien évaluer la cellule cachée** ici ↑↑↑↑↑ ↑↑↑↑↑</span>

+++

Voici l'interface que j'ai implémentée dans la classe `VisualDownloader`

mais vous pouvez bien entendu broder pour faire complètement autrement

```{code-cell} ipython3
d = VisualDownloader(urls)
```

```{code-cell} ipython3
# cette cellule crée juste le dashboard
d.create_dashboard()
```

```{code-cell} ipython3
### et celle-ci lance le download
d.download()
```

```{code-cell} ipython3
:tags: []

##### j'ai ajouté ceci pour donner du feedback 
# parce que sinon pour débugger c'est très compliqué
d.troubleshoot()
```

## quelques précisions

+++

### codes http 300+n : redirections

+++

il se passe un truc louche pour l'url `http://www.irs.gov/pub/irs-pdf/f1040ez.pdf`; 
il se trouve que cette url est obsolète, mais justement c'est intéressant...

https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages

et c'est le cas justement pour l'url `http://www.irs.gov/pub/irs-pdf/f1040ez.pdf`

  
on peut le voir avec par exemple
  
```bash
$ curl -i http://www.irs.gov/pub/irs-pdf/f1040ez.pdf | less
HTTP/2 301
content-length: 0
location: https://www.irs.gov/forms-pubs/about-form-1040-ez
cache-control: max-age=86400
expires: Thu, 08 Apr 2021 06:59:48 GMT
date: Wed, 07 Apr 2021 06:59:48 GMT
server-timing: cdn-cache; desc=HIT
server-timing: edge; dur=1
strict-transport-security: max-age=31536000
```
  
vous pouvez aussi le voir en ouvrant l'URL dans chrome, l'adresse se fait récrire par quelque chose d'autre, ici justement https://www.irs.gov/forms-pubs/about-form-1040-ez

mon code aurait besoin d'être adapté pour traiter ça...

+++

## v2

```{code-cell} ipython3
import time
from ipywidgets import Button
```

+++ {"hide_input": true, "tags": []}

on rajoute un bouton pour démarrer, et un affichage du temps passé

dans ma solution à ce stade j'ai fait un petit refactoring en découpant ça en deux classes distinctes

aussi j'ai été amené à modifier un peu la méthode de lecture; dans le notebook on faisait

```python
async for line in response.content:
```

mais si vous essayez avec cette forme de lecture vous allez constater que la montre n'avance guère...

du coup je suis allé farfouiller [dans cette page](https://docs.aiohttp.org/en/stable/streams.html) pour trouver un mode de lecture plus adapté à notre cas d'usage.

+++

<span style='background-color: #9EBC9E; padding:5px;'>↓↓↓↓↓ ↓↓↓↓↓ assurez-vous de **bien évaluer la cellule cachée** ici ↓↓↓↓↓ ↓↓↓↓↓</span>

```{code-cell} ipython3
:hide_input: false
:tags: []

class UrlDownloader:
    
    def __init__(self, url):
        self.url = url
        
    def widget(self):
        hbox = HBox([
            tickbox := HTML("<span style='color:red;'>&cross;</span>"),
            slider := FloatProgress(value=0, 
                                description=self.name(),
                                layout=Layout(width='100%')),
        ])
        self.tickbox, self.slider = tickbox, slider
        return hbox

    def name(self):
        return self.url.split('/')[-1]

    async def fetch(self):
        total_length = 0
        read_so_far = 0
        async with aiohttp.ClientSession() as session:

            async with session.get(self.url) as response:
                if response.status == 200:
                    self.tickbox.value = "<span style='color:green;'>&#10003;</span>"
                #print(f"{url} returned status {response.status}")
                total_length = int(response.content_length)
                async for data in response.content.iter_chunked(1024):
                    read_so_far += len(data)
                    self.slider.value = 100 * (read_so_far / total_length)
                if read_so_far == total_length:
                    self.slider.bar_style = 'info'
                else:
                    self.slider.bar_style = 'danger'                    
        return read_so_far, total_length

class VisualDownloaderV2:
    
    def __init__(self, urls):
        self.downloaders = {url : UrlDownloader(url) for url in urls}
        self.task = None
        self.button = None
        self.status = None
        self.active = False
        
    def create_dashboard(self):
        self.button = Button(description='Start', button_style='info',
                             layout = Layout(width='50%'))
        self.status = HTML("---", layout = Layout(width='50%'))
                             
        
        self.dashboard = VBox([
            HBox([self.button, self.status]),
            *(downloader.widget() for downloader in self.downloaders.values())
        ])
        
        self.button.on_click(lambda change: self.start())
        display(self.dashboard)

    async def show_time(self):
        start_time = time.time()
        while self.active:
            self.status.value = f"{time.time() - start_time:.3f}s"
            await asyncio.sleep(0.05)
        self.status.value = f"{time.time() - start_time:.3f}s"
        return time.time() - start_time

    async def download(self):
        results = await asyncio.gather(
          *(downloader.fetch() for downloader in self.downloaders.values()))
        self.active = False
        return results
        
    def start(self):
        self.button.disabled = True
        self.button.button_style = 'danger'
        self.active = True
        self.task = asyncio.ensure_future(
            asyncio.gather(self.download(), self.show_time()))
        
    def troubleshoot(self):
        # check self.task
        # TODO: check if self.task is ready and in the proper state
        print(f"{self.task.result()=}")
        print(f"{self.task.exception()=}")
```

<span style='background-color: #9EBC9E; padding:5px;'>↑↑↑↑↑ ↑↑↑↑↑ assurez-vous de **bien évaluer la cellule cachée** ici ↑↑↑↑↑ ↑↑↑↑↑</span>

```{code-cell} ipython3
d = VisualDownloaderV2(urls)
```

```{code-cell} ipython3
# cette cellule crée juste le dashboard
# il faut appuyer sur le bouton pour lancer le download
d.create_dashboard()
```

```{code-cell} ipython3
:tags: []

##### j'ai ajouté ceci pour donner du feedback 
# arrangez-vous pour que ça donne des infos utiles au debug
d.troubleshoot()
```

## aller plus loin

+++

### quelques URLs de test

+++

j'ai quelques URLs de test qui contiennent des fichiers dont la taille est une puissance de 2

par exemple http://planete.inria.fr/Thierry.Parmentelat/dummy/b10 est un fichier de $2ˆ{10}=1024$

ça va jusqu'à b27 qui fait donc 134217728 octets

```{code-cell} ipython3
2**27
```

```{code-cell} ipython3
urls = [ ]
```

```{code-cell} ipython3
d = VisualDownloaderV2(
  [f"http://planete.inria.fr/Thierry.Parmentelat/dummy/b{i:02d}" for i in range(10, 24)]
)
d.create_dashboard()
```

du coup on peut voir que mon code est loin d'être parfait ...

```{code-cell} ipython3
d.troubleshoot()
```

### autres idées pour continuer

+++

peut-être qu'à ce stade vous allez avoir envie d'ajouter un bouton Stop ... ou encore mieux un bouton suspend

vous pouvez aussi imaginer sauver les urls sur disque (je ne le fais pas du tout) et voir l'impact que ça a sur les performances; c'est peut-être le moment de regarder le module `aiofiles` pour faire aussi la sauvegarde de manière asynchrone..

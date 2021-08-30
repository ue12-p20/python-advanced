---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  name: python
  pygments_lexer: ipython3
nbhosting:
  title: visu de champs de vitesse
---

# Tracés de champs de vitesses

On se propose dans ce notebook d'utiliser le mécanisme d'`interact` pour réprésenter des champs de vitesse dérivant de potentiels complexes. Pour rappel, on écrit un potentiel complexe comme suit : 

\begin{equation}
 f(z) = \phi(z) + i \psi (z)
\end{equation}

Où les fonctions $\phi$ et $\psi$ sont harmoniques (à Laplacien nul). Cette écriture permet de représenter des écoulants plans incompressibles et irrotationnels. En dérivant ce potentiel par rappord à la variable complexe $z=x + iy$ on obtient les composantes du champ des vitesses associé : 
\begin{equation}
 f'(z) = \frac{\partial f}{\partial x} = -i \frac{\partial f}{\partial y}=u - i v
\end{equation}

On peut directement remonter à $u$ et $v$ à partir de la partie réelle ou imaginaire du potentiel:
\begin{eqnarray}
 u = \frac{\partial \phi}{\partial x} = \frac{\partial \psi}{\partial y}\\
 v = \frac{\partial \phi}{\partial y} = -\frac{\partial \psi}{\partial x}
\end{eqnarray}


## Un exemple en statique

On s'intéresse ici à un potentiel exponentiel à la forme extrêmement simple. Il se met sous la forme : 
\begin{equation}
f(z) = V_0 \exp(-i\theta)z = \phi(z) + i \psi(z)
\end{equation}
alors on a : 
\begin{equation}
f'(z) = V_0\exp(-i\theta) = V_0(\cos\theta - i\sin\theta) = u -iv
\end{equation}
et le champ de vitesse est de la forme : 
\begin{equation}
u = V_0\cos(\theta) \quad ; \quad v = V_0\sin(\theta)
\end{equation}

```{code-cell} ipython3
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# Les deux paramètres de notre champ
V0 = 1.
alpha = np.pi/4.

# On va tracer dans le carré [-1, 1]x[-1, 1] 
X = np.linspace(-1., 1., 20)

# Construction d'un maillage. Ce sera un tableau dont la forme sera (X.size, X.size).
XX, YY = np.meshgrid(X, X)

# Dans ce cas très particulier, le vecteur vitesse ne dépend pas de la position.
u = np.full_like(XX, V0*np.cos(alpha))
v = np.full_like(YY, V0*np.sin(alpha))

# Calcul de la norme, ici on pourrait remplir directement le tableau avec V0 mais c'est
# un cas très particulier.
n = np.sqrt(np.square(u)+np.square(v))

# Création de la figure
fig = plt.figure(figsize=(10., 10.))
ax = fig.add_subplot(111, aspect=1.)
ax.grid(True)
ax.set_xlabel("Position x", fontsize=16.)
ax.set_ylabel("Position y", fontsize=16.) 
# Quiver = carquois en anglais
# ax.quiver(posx, posy, dx, dy, n)
# posx, posy position du vecteur
# dx, dy coordonnées du vecteur
# n norme (pour la coloration)
# Ici on ne trace que des vecteur de norme 1 pour plus de lisibilité.
ax.quiver(XX, YY, u/n, v/n, n)
plt.show()
```

## Passage en interactif
Comme première partie d'exercice, vous pouvez passer le tracé de ce graphe en interactif. Puisque l'on trace des vecteurs normalisés, vous ne verrez pas d'impact de la valeur de $V0$.

```{code-cell} ipython3
from ipywidgets import interact, FloatSlider

# À vous de jouer ! 
```

## Implémentations des potentiels

L'objectif du TP est de construire des interfaces de visualisations de champs de vitesses, obtenus en superposant plusieurs champs issus de différents potentiels. La première étape est d'implémenter les différents potentiels. Suivez l'exemple du potentiel `flow` ci-dessous.

```{code-cell} ipython3
def flow(x, y, V0, alpha):
    # Le potentiel précédent, déjà implémenté.
    u = np.full_like(x, V0*np.cos(np.radians(alpha)))
    v = np.full_like(y, V0*np.sin(np.radians(alpha)))
    return u, v
```

### Source ponctuelle ou puit ponctuel
Considérons maintenant un potentiel de la forme
\begin{equation}
f(z) = \frac{\varepsilon D}{2\pi}\log(z-z_0) = \frac{\varepsilon D}{2\pi}\left(\log(|z-z_0|)+i(\arg(z)-\arg(z_0))\right)
\end{equation}
Il vient :
\begin{equation}
 u = \frac{\partial \varphi}{\partial x} = \frac{\varepsilon D}{2\pi} \frac{x}{x^2+y^2} \quad ; \quad v = \frac{\partial \varphi}{\partial y} = \frac{\varepsilon D}{2\pi} \frac{y}{x^2+y^2} 
\end{equation}
En fonction du signe de $\varepsilon\in\{1, -1\}$ on a soit un puits soit une source de débit $D>0 $.

```{code-cell} ipython3
def ponctual(x, y, eps=1.,  D=1., hx=0., hy=0.):
    # À vous de jouer ! 
    return u, v
```

## Le tourbillon
Considérons maintenant un potentiel de la forme
\begin{equation}
f(z) = i\frac{\varepsilon\Gamma}{2\pi}\log(z-z_0) = \frac{\varepsilon\Gamma}{2\pi}\left(i\log(|z-z_0|)-(\arg(z)-\arg(z_0))\right)
\end{equation}
Il vient :
\begin{equation}
 u = \frac{\partial \psi}{\partial y} = \frac{\varepsilon\Gamma}{2\pi} \frac{y}{x^2+y^2} \quad ; \quad v = -\frac{\partial \psi}{\partial x} = -\frac{\varepsilon\Gamma}{2\pi} \frac{y}{x^2+y^2} 
\end{equation}
Ici, on a un tourbillon de circulation $\Gamma>0$. Le signe de $\varepsilon\in\{1, -1\}$ donne le sens de rotation du tourbillon.

```{code-cell} ipython3
def vortex(x, y, eps=1., gamma=1., hx=0., hy=0.):
    # À vous de jouer ! 
    return u, v
```

## Doublet
Avec une potentiel de la forme suivante : 
\begin{equation}
f(z) = - \frac{\varepsilon K}{2\pi z} = -\frac{\varepsilon K}{2\pi} \left(\frac{x}{r^2} - i \frac{y}{r^2}\right)
\end{equation}
On détermine : 
\begin{equation}
u = \frac{\varepsilon K}{2\pi} \frac{x^2-y^2}{r^4} \quad ; \quad v = \frac{\varepsilon K}{2\pi}\frac{2xy}{r^4}
\end{equation}

```{code-cell} ipython3
def doublet(x, y, eps=1., K=1., hx=0., hy=0.):
    # À vous de jouer ! 
    return u, v
```

## Une usine à  *dashboard* 
Dans cette première partie, on cherche à créer automatiquement un *dashboard* seulement à partir d'une chaîne de caractères. Par example, on souhaite qu'en tapant `make_dashboard("vortex")` apparaisse une figure avec le champ de vitesses d'un tourbillon et les sliders associés. 

**Note :** Il serait judicieux de stocker dans le conteneur le mieux adapté une référence vers la fonction permettant de calculer les composantes du champ des vitesses ainsi que toutes les données nécessaires sur les paramètres du modèle.

```{code-cell} ipython3
# À vous de jouer ! 
```

```{code-cell} ipython3
make_dashboard("flow")
```

## Superposition de champs

Imaginons maintenant que l'on veuille superposer plusieurs potentiels pour créer des champs plus complexes. On peut dans un premier temps utiliser une approche fonctionnelle comme précédemment. Cependant, puisqu'il faut stocker un grand nombre de données (quels sont les arguments de quel potentiel, etc...) écrire une classe permettrait sûrement d'y voir plus clair.

```{code-cell} ipython3
# À vous de jouer ! 
```

```{code-cell} ipython3

```

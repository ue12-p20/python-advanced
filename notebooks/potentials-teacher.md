---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
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

def function(V0, alpha):
    u = np.full_like(XX, V0*np.cos(np.radians(alpha)))
    v = np.full_like(YY, V0*np.sin(np.radians(alpha)))

    # Calcul de la norme
    n = np.sqrt(np.square(u)+np.square(v))
    fig = plt.figure(figsize=(10., 10.))
    ax = plt.gca()
    ax.set_aspect(1.)
    plt.quiver(XX, YY, u/n, v/n, n)

Vslider = FloatSlider(min=0.1, max=1., step=0.1, continuous_update=False)
alphaslider = FloatSlider(min=0, max=360., step=2., continuous_update=False)

interact(function, V0=Vslider, alpha=alphaslider)
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
    r2 = np.square(x-hx) + np.square(y-hy)
    c = eps*D/(2.*np.pi)
    u = c*(x-hx)/r2
    v = c*(y-hy)/r2
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
    r2 = np.square(x-hx) + np.square(y-hy)
    c = eps*gamma/(2.*np.pi)
    u = c*(y-hy)/r2
    v = -c*(x-hx)/r2
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
    r4 = np.square(np.square(x-hx) + np.square(y-hy))
    c = -eps*K/(2.*np.pi)
    u = c*(np.square(x-hx)-np.square(y-hy))/r4
    v = c*2*(x-hx)*(y-hy)/r4
    return u, v
```

## Une usine à  *dashboard* 
Dans cette première partie, on cherche à créer automatiquement un *dashboard* seulement à partir d'une chaîne de caractères. Par example, on souhaite qu'en tapant `make_dashboard("vortex")` apparaisse une figure avec le champ de vitesses d'un tourbillon et les sliders associés. 

**Note :** Il serait judicieux de stocker dans le conteneur le mieux adapté une référence vers la fonction permettant de calculer les composantes du champ des vitesses ainsi que toutes les données nécessaires sur les paramètres du modèle.  

```{code-cell} ipython3
from ipywidgets import Dropdown

posx = (FloatSlider, dict(min=-1., max=1., step=0.05, description='PosX'))
posy = (FloatSlider, dict(min=-1., max=1., step=0.05, description='PosY'))

factory = dict()
factory["flow"] = (flow,
                   {"V0": (FloatSlider, dict(min=0.1, max=1., step=0.05, description='V0')),
                    "alpha": (FloatSlider, dict(min=0, max=360., step=2., description='Angle'))}
                  )

factory["ponctual"] = (ponctual,
                      {"eps": (Dropdown, dict(options={"source" : 1., "puits": -1.}, description='Type')),
                       "D": (FloatSlider, dict(min=0.1, max=1., step=0.05, description='Débit')),
                       "hx": posx,
                       "hy": posy}
                      )

factory["vortex"] = (vortex,
                      {"eps": (Dropdown, dict(options={"horaire" : 1., "anti-horaire": -1.}, description='Rotation')),
                       "gamma": (FloatSlider, dict(min=0.1, max=1., step=0.05, description='Circulation')),
                       "hx": posx,
                       "hy": posy}
                      )

factory["doublet"] = (doublet,
                      {"eps": (Dropdown, dict(options={"horaire" : 1., "anti-horaire": -1.}, description='Rotation')),
                       "K": (FloatSlider, dict(min=0.1, max=1., step=0.05, description='Circulation')),
                       "hx": posx,
                       "hy": posy}
                      )

def make_dashboard(keyword):
    function, sliders_data = factory[keyword]
    X = np.linspace(-1., 1., 20)
    XX, YY = np.meshgrid(X, X)
    
    def inner(**kwargs):
        u, v = function(XX, YY, **kwargs)
    
        # Calcul de la norme
        n = np.sqrt(np.square(u)+np.square(v))
        fig = plt.figure(figsize=(10., 10.))
        ax = plt.gca()
        ax.set_aspect(1.)
        plt.quiver(XX, YY, u/n, v/n, n)
    
    sliders = dict()
    for key, (cons, kwargs) in sliders_data.items():
        sliders[key] = cons(**kwargs, continuous_update=False)
    
    interact(inner, **sliders)
```

```{code-cell} ipython3
make_dashboard("flow")
```

## Superposition de champs

Imaginons maintenant que l'on veuille superposer plusieurs potentiels pour créer des champs plus complexes. On peut dans un premier temps utiliser une approche fonctionnelle comme précédemment. Cependant, puisqu'il faut stocker un grand nombre de données (quels sont les arguments de quel potentiel, etc...) écrire une classe permettrait sûrement d'y voir plus clair. 

```{code-cell} ipython3
from ipywidgets import Label, HBox, VBox, interactive_output
from IPython.display import display
from copy import deepcopy

class VelocityFieldPlotter:
    def __init__(self, *potentials, nb_points=20):
        # generating the mesh grid once and for all
        x = np.linspace(-1., 1., nb_points)
        self._XX, self._YY = np.meshgrid(x, x)
        # x-coordinate of the velocity field
        self._u = np.zeros_like(self._XX)
        # y-coordinate of the velocity field
        self._v = np.zeros_like(self._XX)
        # List of the functions that will compute the elementary components of the field
        self._functions = []
        # Dictionnary with the sliders
        self._sliders = {}
        # List of mappings local argname -> global slider name
        self._maps = []
        
        # Lines in the dashboard 
        dashboard_elements = []
        
        for i, pot in enumerate(potentials):
            # Cosmetic
            dashboard_elements.append(HBox([Label(f'Potential of type {pot}')]))
            
            # Getting data from the factory
            func, slider_data = factory[pot]
            
            # Storing the function
            self._functions.append(func)
            
            # Here we need to build the needed sliders and 
            # map their local and global names
            local_map = dict()
            sliders = []
            for key, (cons, kwargs) in slider_data.items():
                # Building the slider
                sli = cons(**kwargs, continuous_update=False)
                # Storing it globally
                self._sliders[f"{key}_{i}"] = sli
                # Mapping local argname -> global slider name
                local_map[key] = f"{key}_{i}"
                # Temporary for dashboard
                sliders.append(sli)
            self._maps.append(local_map)
            
            # Line with all the sliders linked to the current potential
            dashboard_elements.append(HBox(sliders))
            
        # Grouping all the lines
        self._dashboard = VBox(dashboard_elements)

    @staticmethod
    def make_axes():
        """
        Static method to set up the axes.
        """
        fig = plt.figure(figsize=(10., 10.))
        ax = fig.add_subplot(111, aspect=1.)
        ax.grid(True)
        ax.set_xlabel('Position X', fontsize=16.)
        ax.set_ylabel('Position Y', fontsize=16.)
        ax.set_title('Velocity field', fontsize=16.)
        ax.tick_params(axis="x", labelsize=16)
        ax.tick_params(axis="y", labelsize=16)
        return ax
        
    def interact(self):
        # Displaying the dashboard
        display(self._dashboard)
        
        # Closure 
        def inner(**kwargs):
            # Reseting components
            self._u = 0.
            self._v = 0.
            for func, loc_map in zip(self._functions, self._maps):
                # Elementary call to the potentials
                local_kwargs = {key: kwargs[globkey] for key, globkey in loc_map.items()}
                du, dv = func(self._XX, self._YY, **local_kwargs)
                self._u += du
                self._v += dv
            n = np.sqrt(np.square(self._u)+np.square(self._v))
            
            ax = VelocityFieldPlotter.make_axes()
            ax.quiver(self._XX, self._YY, self._u/n, self._v/n, n)

        # Displaying the whole thing ! 
        display(interactive_output(inner, self._sliders))
```

```{code-cell} ipython3
plot = VelocityFieldPlotter("flow", "vortex", "vortex", "ponctual", nb_points=20)
plot.interact()
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

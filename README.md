Fork of Premise Componere
=================
Configuration and diagram generation of the architecture diagrams. There are a few diagrams that are generated.

1.  Detail /wiki/detail.png
    * Shows every component
    * Groups by area
2.  Area (For Each) /wiki/${area}/area.png
    * Shows every component in an area
    * Shows components directly connected to/from a component in this area
    * Shows the area around connected components outside this area
3.  Overview /wiki/overview.png
    * Shows every application component and above
    * Rolls up transitive dependencies for lower order dependencies
    * Groups by area

Installing Componere
--------------------
We assume you have `pyenv` and Graphviz executables installed and configured (skip ahead if you don't).

1.  Clone this repo and `cd granular-componere`
2.  Setup your local python environment:
    ```bash
    pyenv install 2.7.15
    pyenv local 2.7.15
    ```
3.  Install pipenv via `pip install -U pipenv`
4.  Install componere via `pipenv install '-e .'`

Using Componere
---------------
Now that you have componere installed into a pipenv you can run it via `pipenv shell`.
```bash
> pipenv shell
(granular-componere) > cd ~/my/graph/definitions/
(granular-componere) > componere ./src --all ./output
(granular-componere) > exit
> echo yay!
```

Oh, you don't have `pyenv` and `graphviz`?
---------------------------------------------

Install graphviz via `brew install graphviz` or from the [download page](https://www.graphviz.org/download/)

Install pyenv via `brew install pyenv` and then make sure it's initialized by adding the following to your shell profile:
```bash
eval "$(pyenv init -)"
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

Support for Shapes
------------------
Componere now supports shapes! You can define them on a `type` and `component`. All components of a type will use the type's shape by default.  A shape defined on a component will override the shape of the type.

```yaml
types:
    my-awesome-type:
        name: Super Cool Type
        shape: star
        
components:
    my-even-better-component:
        name: The Coolest Component
        shape: tripleoctagon
```

The default shape of everything is `rect`.  You should be able to use any of the fun [shapes that Graphviz supports](https://www.graphviz.org/doc/info/shapes.html).
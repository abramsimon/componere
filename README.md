Premise Componere
=================
Configuration and diagram generation of the architecture diagrams. There are a few diagrams that generated.

1. BAD (Big Arse Diagram) /wiki/bad.png
    * Shows every component
    * Groups by area
2. Area (For Each) /wiki/${area}/area.png
    * Shows every component in an area
    * Shows components directly connected to/from a component in this area
    * Shows the area around connected components outside this area
3. Overview
    * Shows every application component and above
    * Rolls up transitive dependencies for lower order dependencies
    * Groups by area

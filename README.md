Multiple sections is an Allplan PythonPart Script for creating multiple associative sections from 2D lines.
The script allows users to generate section views based on drawn 2D lines, with options for numbering, direction, and automatic deletion of source lines.

**Features**
Automatic creation of section views from selected 2D lines.
Layer filtering: Only lines on the specified layer are used.
Customizable section depth, top and bottom levels.
Section numbering: Start number can be set.
Option to consider line direction for section orientation.
Option to delete source lines after section creation.
Associative views are created using Allplan's API.

**Usage**
Draw 2D lines in the locations where you want to create section views.
Set parameters in the PythonPart palette:
Section depth, top and bottom levels
Layer filter (the layer containing your 2D lines)
First section number
Consider line direction (optional)
Run the script in Allplan.
Use the palette buttons to:
Create sections 
Create sections and delete lines
Sections will be numbered sequentially, starting from the specified number.

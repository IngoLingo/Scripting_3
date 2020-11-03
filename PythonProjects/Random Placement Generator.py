import maya.cmds as cmds
import random

def RandomPlacement(numOfDupes, minX, maxX, minY, maxY, minZ, maxZ ):
    selectionsToDuplicat = cmds.ls( selection=True );

    # For / in loop selecting each uniqe object
    for selected in selectionsToDuplicat:
        # For loop duplicating each uniqe object
        for value in range(numOfDupes):
            print value
            cmds.duplicate(selected);
            randX = random.randrange(minX, maxX);
            randY = random.randrange(minY, maxY);
            randZ = random.randrange(minZ, maxZ);

            cmds.xform( selected, translation=(randX, randY, randZ) );
            print value;


RandomPlacement(50, -10, 10, -10, 10, -10, 10);
# Script created by Simon Nagel - 2019.11.07


def deleteVariantBlendGroups():
    allVarSets = getGroupedVariantSets()
    for i in allVarSets:
        varSetsInOneGroup = allVarSets[i]
        varGroupName= str(i)
        #print varGroupName
        print varGroupName[-6:]
        if varGroupName[-6:] =="_blend":
            deleteVariantSetGroup(str(varGroupName))
            print( str(varGroupName)+ "should be deleted ")
        for j in varSetsInOneGroup:
            varSetName = str(j)
            if varSetName[-6:] =="_blend":
                deleteVariantSet(varSetName)
            


def createVariantBlendGroups():
    allVarSets = getGroupedVariantSets()      
        

    for i in allVarSets:
        varSetsInOneGroup = allVarSets[i]
        varGroupName= str(i)
        #print varGroupName
        newVarGroupName = "_"+varGroupName+"_blend"
        varGroup = createVariantSetGroup(newVarGroupName)
        
        #print varSetsInOneGroup
        for j in varSetsInOneGroup:
            varSetName = str(j)
            #print varSetName
            newVar = createVariantSet(varSetName+"_blend")
            moveVariantSetToGroup(varSetName+"_blend",newVarGroupName)
            script = 'HTMLBlendVariant("'+varSetName+'")'
            newVar.addScript(str(script))
        #print "\n"

        
deleteVariantBlendGroups()                        
createVariantBlendGroups()



timer = vrTimer()

transValue = 0

def HTMLBlendVariant(vSet):
    global transValue
    global sceneplate
    global sceneplateToDelete
    width = getRenderWindowWidth(-1)
    height = getRenderWindowHeight(-1)
    
    createSnapshotFastInit(width, height, 0)
    filepathRendering = "c:/temp/"
    createSnapshotFast(filepathRendering+"HTMLVariantBlend.png")
    createSnapshotFastTerminate()
    
    allSceneplates = vrSceneplateService.getAllSceneplates()
    sceneplateToDelete = []
    del sceneplateToDelete[:]
    for i in range(len(allSceneplates)):
        sceneplateName = allSceneplates[i].getName()
        if sceneplateName[0:18] == "HTMLVariantBlend":
             sceneplateToDelete.append(allSceneplates[i])
    
    vrSceneplateService.removeNodes(sceneplateToDelete)
    
    sceneplate = vrSceneplateService.createNode(vrSceneplateService.getRootNode(), vrSceneplateTypes.NodeType.Frontplate, "HTMLVariantBlend")
    sceneplate.setWidth(width)
    sceneplate.setHeight(height)
    sceneplate.setPosition(vrSceneplateTypes.Position.Center)
    sceneplate.setContentType(vrSceneplateTypes.ContentType.Image)
    sceneplate.setSize(1)
    image = vrImageService.loadImage(filepathRendering+"HTMLVariantBlend.png")
    sceneplate.setImage(image)    
  
    
    selectVariantSet(vSet)
    timer.setActive(1)
    
    
    
    

def fade():
    global transValue
    global sceneplate
    global sceneplateToDelete
    transValue = transValue +0.04
    sceneplate.setTransparency(transValue)
    
    if transValue > 1:
        vrSceneplateService.removeNodes(sceneplateToDelete)
        timer.setActive(0)
        transValue = 0
        sceneplate.setTransparency(1)
        
        
timer.connect(fade)
#timer.setActive(0)

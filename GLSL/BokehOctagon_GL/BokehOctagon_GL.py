# -*- coding: utf-8 -*-
# DO NOT EDIT THIS FILE
# This file was automatically generated by Natron PyPlug exporter version 10.

# Hand-written code should be added in a separate file named BokehOctagon_GLExt.py
# See http://natron.readthedocs.org/en/master/devel/groups.html#adding-hand-written-code-callbacks-etc
# Note that Viewers are never exported

import NatronEngine
import sys

# Try to import the extensions file where callbacks and hand-written code should be located.
try:
    from BokehOctagon_GLExt import *
except ImportError:
    pass

def getPluginID():
    return "fr.inria.BokehOctagon"

def getLabel():
    return "BokehOctagon_GL"

def getVersion():
    return 1

def getGrouping():
    return "Community/GLSL/Blur"

def getPluginDescription():
    return "4-pass bokeh from https://www.shadertoy.com/view/lst3Df (implementation of http://ivizlab.sfu.ca/papers/cgf2012.pdf ). Author: F. Devernay."

def createInstance(app,group):
    # Create all nodes in the group

    # Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    lastNode.setColor(0.7, 0.7, 0.7)

    # Create the user parameters
    lastNode.Controls = lastNode.createPageParam("Controls", "Controls")
    param = lastNode.createDoubleParam("BufAparamValueFloat0", "Blur Size")
    param.setMinimum(0, 0)
    param.setMaximum(64, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(64, 0)
    param.setDefaultValue(64, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.Controls.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.BufAparamValueFloat0 = param
    del param

    param = lastNode.createIntParam("BufAparamValueInt1", "No. Samples")
    param.setMinimum(1, 0)
    param.setMaximum(32, 0)
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(32, 0)
    param.setDefaultValue(16, 0)
    param.restoreDefaultValue(0)

    # Add the param to the page
    lastNode.Controls.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.BufAparamValueInt1 = param
    del param

    param = lastNode.createBooleanParam("BufAparamValueBool2", "Modulate")

    # Add the param to the page
    lastNode.Controls.addParam(param)

    # Set param properties
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.BufAparamValueBool2 = param
    del param

    # Refresh the GUI with the newly created parameters
    lastNode.setPagesOrder(['Controls', 'Node', 'Settings'])
    lastNode.refreshUserParamsGUI()
    del lastNode

    # Start of node "BufA"
    lastNode = app.createNode("net.sf.openfx.Shadertoy", 1, group)
    lastNode.setScriptName("BufA")
    lastNode.setLabel("BufA")
    lastNode.setPosition(440, 205)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupBufA = lastNode

    param = lastNode.getParam("mouseClick")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("paramValueFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramValueInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramValueBool2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("imageShaderFileName")
    if param is not None:
        param.setValue("[Project]/BufA.frag")
        del param

    param = lastNode.getParam("imageShaderSource")
    if param is not None:
        param.setValue("// iChannel0: Source, filter=mipmap, wrap=clamp\n// iChannel1: Modulate (Image containing a factor to be applied to the Blur size in the first channel), filter=linear, wrap=clamp\n// Bbox: iChannel0\n\nconst vec2 blurdir = vec2( 1.0, 0.0 );\n\nuniform float blurdist_px = 64.0; // Blur Size (Blur distance in pixels), min=0., max=64\nuniform int NUM_SAMPLES = 16; // No. Samples (Number of samples per pass), min=1, max=32\nuniform bool perpixel_size = false; // Modulate (Modulate the blur size by multiplying it by the first channel of the Modulate input)\n\nconst vec2 iRenderScale = vec2(1.,1.);\n\n//note: uniform pdf rand [0;1[\nfloat hash12n(vec2 p)\n{\n    p  = fract(p * vec2(5.3987, 5.4421));\n    p += dot(p.yx, p.xy + vec2(21.5351, 14.3137));\n    return fract(p.x * p.y * 95.4307);\n}\n\nvoid mainImage( out vec4 fragColor, in vec2 fragCoord )\n{\n    vec2 blurvec = normalize(blurdir);\n    vec2 uv = fragCoord / iResolution.xy;\n    float blurdist = blurdist_px * iRenderScale.x;\n    if (perpixel_size) {\n        blurdist *= texture2D(iChannel1, (fragCoord.xy-iChannelOffset[1].xy)/iChannelResolution[1].xy).x;\n    }\n\n    vec2 p0 = fragCoord - 0.5 * blurdist * blurvec;\n    vec2 p1 = fragCoord + 0.5 * blurdist * blurvec;\n    vec2 stepvec = (p1-p0) / float(NUM_SAMPLES) / iResolution.xy;\n    vec2 p = p0 / iResolution.xy  + (hash12n(uv+iGlobalTime)-0.5) * stepvec;\n\n    vec4 sumcol = vec4(0.0);\n    for (int i=0;i<NUM_SAMPLES;++i)\n    {\n        vec4 sample = texture2D( iChannel0, p, -10.0 );\n        sumcol += sample;\n        p += stepvec;\n    }\n    sumcol /= float(NUM_SAMPLES);\n    sumcol = max( sumcol, 0.0 );\n\n    fragColor = sumcol;\n}\n")
        del param

    param = lastNode.getParam("wrap0")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel0")
    if param is not None:
        param.setValue("Source")
        del param

    param = lastNode.getParam("mipmap1")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap1")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel1")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("inputHint1")
    if param is not None:
        param.setValue("Image containing a factor to be applied to the Blur size in the first channel")
        del param

    param = lastNode.getParam("inputEnable2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("inputEnable3")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("bbox")
    if param is not None:
        param.set("iChannel0")
        del param

    param = lastNode.getParam("mouseParams")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("paramCount")
    if param is not None:
        param.setValue(3, 0)
        del param

    param = lastNode.getParam("paramType0")
    if param is not None:
        param.set("float")
        del param

    param = lastNode.getParam("paramName0")
    if param is not None:
        param.setValue("blurdist_px")
        del param

    param = lastNode.getParam("paramLabel0")
    if param is not None:
        param.setValue("Blur Size")
        del param

    param = lastNode.getParam("paramHint0")
    if param is not None:
        param.setValue("Blur distance in pixels")
        del param

    param = lastNode.getParam("paramDefaultFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramMinFloat0")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("paramMaxFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramType1")
    if param is not None:
        param.set("int")
        del param

    param = lastNode.getParam("paramName1")
    if param is not None:
        param.setValue("NUM_SAMPLES")
        del param

    param = lastNode.getParam("paramLabel1")
    if param is not None:
        param.setValue("No. Samples")
        del param

    param = lastNode.getParam("paramHint1")
    if param is not None:
        param.setValue("Number of samples per pass")
        del param

    param = lastNode.getParam("paramDefaultInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramMinInt1")
    if param is not None:
        param.setValue(1, 0)
        del param

    param = lastNode.getParam("paramMaxInt1")
    if param is not None:
        param.setValue(32, 0)
        del param

    param = lastNode.getParam("paramType2")
    if param is not None:
        param.set("bool")
        del param

    param = lastNode.getParam("paramName2")
    if param is not None:
        param.setValue("perpixel_size")
        del param

    param = lastNode.getParam("paramLabel2")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("paramHint2")
    if param is not None:
        param.setValue("Modulate the blur size by multiplying it by the first channel of the Modulate input")
        del param

    del lastNode
    # End of node "BufA"

    # Start of node "BufB"
    lastNode = app.createNode("net.sf.openfx.Shadertoy", 1, group)
    lastNode.setScriptName("BufB")
    lastNode.setLabel("BufB")
    lastNode.setPosition(440, 313)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupBufB = lastNode

    param = lastNode.getParam("mouseClick")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("paramValueFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramValueInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramValueBool2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("imageShaderFileName")
    if param is not None:
        param.setValue("[Project]/BufB.frag")
        del param

    param = lastNode.getParam("imageShaderSource")
    if param is not None:
        param.setValue("// iChannel0: BufA, filter=linear, wrap=clamp\n// iChannel1: Modulate (Image containing a factor to be applied to the Blur size in the first channel), filter=linear, wrap=clamp\n// Bbox: iChannel0\n\nconst vec2 blurdir = vec2( 0.0, 1.0 );\n\nuniform float blurdist_px = 64.0; // Blur Size (Blur distance in pixels), min=0., max=64\nuniform int NUM_SAMPLES = 16; // No. Samples (Number of samples per pass), min=1, max=32\nuniform bool perpixel_size = false; // Modulate (Modulate the blur size by multiplying it by the first channel of the Modulate input)\n\nconst vec2 iRenderScale = vec2(1.,1.);\n\n//note: uniform pdf rand [0;1[\nfloat hash12n(vec2 p)\n{\n    p  = fract(p * vec2(5.3987, 5.4421));\n    p += dot(p.yx, p.xy + vec2(21.5351, 14.3137));\n    return fract(p.x * p.y * 95.4307);\n}\n\nvoid mainImage( out vec4 fragColor, in vec2 fragCoord )\n{\n    vec2 blurvec = normalize(blurdir);\n    vec2 uv = fragCoord / iResolution.xy;\n    float blurdist = blurdist_px * iRenderScale.x;\n    if (perpixel_size) {\n        blurdist *= texture2D(iChannel1, (fragCoord.xy-iChannelOffset[1].xy)/iChannelResolution[1].xy).x;\n    }\n\n    vec2 p0 = fragCoord - 0.5 * blurdist * blurvec;\n    vec2 p1 = fragCoord + 0.5 * blurdist * blurvec;\n    vec2 stepvec = (p1-p0) / float(NUM_SAMPLES)/ iResolution.xy;\n    vec2 p = p0 / iResolution.xy + (hash12n(uv+iGlobalTime)-0.5) * stepvec;\n\n    vec4 sumcol = vec4(0.0);\n    for (int i=0;i<NUM_SAMPLES;++i)\n    {\n     \tsumcol += texture2D( iChannel0, p, -10.0 );\n        p += stepvec;\n    }\n    sumcol /= float(NUM_SAMPLES);\n\n    fragColor = sumcol;\n}\n")
        del param

    param = lastNode.getParam("mipmap0")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap0")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel0")
    if param is not None:
        param.setValue("BufA")
        del param

    param = lastNode.getParam("mipmap1")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap1")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel1")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("inputHint1")
    if param is not None:
        param.setValue("Image containing a factor to be applied to the Blur size in the first channel")
        del param

    param = lastNode.getParam("inputEnable2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("inputEnable3")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("bbox")
    if param is not None:
        param.set("iChannel0")
        del param

    param = lastNode.getParam("mouseParams")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("paramCount")
    if param is not None:
        param.setValue(3, 0)
        del param

    param = lastNode.getParam("paramType0")
    if param is not None:
        param.set("float")
        del param

    param = lastNode.getParam("paramName0")
    if param is not None:
        param.setValue("blurdist_px")
        del param

    param = lastNode.getParam("paramLabel0")
    if param is not None:
        param.setValue("Blur Size")
        del param

    param = lastNode.getParam("paramHint0")
    if param is not None:
        param.setValue("Blur distance in pixels")
        del param

    param = lastNode.getParam("paramDefaultFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramMinFloat0")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("paramMaxFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramType1")
    if param is not None:
        param.set("int")
        del param

    param = lastNode.getParam("paramName1")
    if param is not None:
        param.setValue("NUM_SAMPLES")
        del param

    param = lastNode.getParam("paramLabel1")
    if param is not None:
        param.setValue("No. Samples")
        del param

    param = lastNode.getParam("paramHint1")
    if param is not None:
        param.setValue("Number of samples per pass")
        del param

    param = lastNode.getParam("paramDefaultInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramMinInt1")
    if param is not None:
        param.setValue(1, 0)
        del param

    param = lastNode.getParam("paramMaxInt1")
    if param is not None:
        param.setValue(32, 0)
        del param

    param = lastNode.getParam("paramType2")
    if param is not None:
        param.set("bool")
        del param

    param = lastNode.getParam("paramName2")
    if param is not None:
        param.setValue("perpixel_size")
        del param

    param = lastNode.getParam("paramLabel2")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("paramHint2")
    if param is not None:
        param.setValue("Modulate the blur size by multiplying it by the first channel of the Modulate input")
        del param

    del lastNode
    # End of node "BufB"

    # Start of node "BufC"
    lastNode = app.createNode("net.sf.openfx.Shadertoy", 1, group)
    lastNode.setScriptName("BufC")
    lastNode.setLabel("BufC")
    lastNode.setPosition(731, 205)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupBufC = lastNode

    param = lastNode.getParam("mouseClick")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("paramValueFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramValueInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramValueBool2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("imageShaderFileName")
    if param is not None:
        param.setValue("[Project]/BufC.frag")
        del param

    param = lastNode.getParam("imageShaderSource")
    if param is not None:
        param.setValue("// iChannel0: Source, filter=mipmap, wrap=clamp\n// iChannel1: Modulate (Image containing a factor to be applied to the Blur size in the first channel), filter=linear, wrap=clamp\n// Bbox: iChannel0\n\nconst vec2 blurdir = vec2( 1.0, 1.0 );\n\nuniform float blurdist_px = 64.0; // Blur Size (Blur distance in pixels), min=0., max=64\nuniform int NUM_SAMPLES = 16; // No. Samples (Number of samples per pass), min=1, max=32\nuniform bool perpixel_size = false; // Modulate (Modulate the blur size by multiplying it by the first channel of the Modulate input)\n\nconst vec2 iRenderScale = vec2(1.,1.);\n\n//note: uniform pdf rand [0;1[\nfloat hash12n(vec2 p)\n{\n    p  = fract(p * vec2(5.3987, 5.4421));\n    p += dot(p.yx, p.xy + vec2(21.5351, 14.3137));\n    return fract(p.x * p.y * 95.4307);\n}\n\nvoid mainImage( out vec4 fragColor, in vec2 fragCoord )\n{\n    vec2 blurvec = normalize(blurdir);\n    vec2 uv = fragCoord / iResolution.xy;\n    float blurdist = blurdist_px * iRenderScale.x;\n    if (perpixel_size) {\n        blurdist *= texture2D(iChannel1, (fragCoord.xy-iChannelOffset[1].xy)/iChannelResolution[1].xy).x;\n    }\n\n    vec2 p0 = fragCoord - 0.5 * blurdist * blurvec;\n    vec2 p1 = fragCoord + 0.5 * blurdist * blurvec;\n    vec2 stepvec = (p1-p0) / float(NUM_SAMPLES) / iResolution.xy;\n    vec2 p = p0 / iResolution.xy  + (hash12n(uv+iGlobalTime)-0.5) * stepvec;\n\n    vec4 sumcol = vec4(0.0);\n    for (int i=0;i<NUM_SAMPLES;++i)\n    {\n        vec4 sample = texture2D( iChannel0, p, -10.0 );\n        sumcol += sample;\n        p += stepvec;\n    }\n    sumcol /= float(NUM_SAMPLES);\n    sumcol = max( sumcol, 0.0 );\n\n    fragColor = sumcol;\n}\n")
        del param

    param = lastNode.getParam("wrap0")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel0")
    if param is not None:
        param.setValue("Source")
        del param

    param = lastNode.getParam("mipmap1")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap1")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel1")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("inputHint1")
    if param is not None:
        param.setValue("Image containing a factor to be applied to the Blur size in the first channel")
        del param

    param = lastNode.getParam("inputEnable2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("inputEnable3")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("bbox")
    if param is not None:
        param.set("iChannel0")
        del param

    param = lastNode.getParam("mouseParams")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("paramCount")
    if param is not None:
        param.setValue(3, 0)
        del param

    param = lastNode.getParam("paramType0")
    if param is not None:
        param.set("float")
        del param

    param = lastNode.getParam("paramName0")
    if param is not None:
        param.setValue("blurdist_px")
        del param

    param = lastNode.getParam("paramLabel0")
    if param is not None:
        param.setValue("Blur Size")
        del param

    param = lastNode.getParam("paramHint0")
    if param is not None:
        param.setValue("Blur distance in pixels")
        del param

    param = lastNode.getParam("paramDefaultFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramMinFloat0")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("paramMaxFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramType1")
    if param is not None:
        param.set("int")
        del param

    param = lastNode.getParam("paramName1")
    if param is not None:
        param.setValue("NUM_SAMPLES")
        del param

    param = lastNode.getParam("paramLabel1")
    if param is not None:
        param.setValue("No. Samples")
        del param

    param = lastNode.getParam("paramHint1")
    if param is not None:
        param.setValue("Number of samples per pass")
        del param

    param = lastNode.getParam("paramDefaultInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramMinInt1")
    if param is not None:
        param.setValue(1, 0)
        del param

    param = lastNode.getParam("paramMaxInt1")
    if param is not None:
        param.setValue(32, 0)
        del param

    param = lastNode.getParam("paramType2")
    if param is not None:
        param.set("bool")
        del param

    param = lastNode.getParam("paramName2")
    if param is not None:
        param.setValue("perpixel_size")
        del param

    param = lastNode.getParam("paramLabel2")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("paramHint2")
    if param is not None:
        param.setValue("Modulate the blur size by multiplying it by the first channel of the Modulate input")
        del param

    del lastNode
    # End of node "BufC"

    # Start of node "BufD"
    lastNode = app.createNode("net.sf.openfx.Shadertoy", 1, group)
    lastNode.setScriptName("BufD")
    lastNode.setLabel("BufD")
    lastNode.setPosition(731, 295)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupBufD = lastNode

    param = lastNode.getParam("mouseClick")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("paramValueFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramValueInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramValueBool2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("imageShaderFileName")
    if param is not None:
        param.setValue("[Project]/BufD.frag")
        del param

    param = lastNode.getParam("imageShaderSource")
    if param is not None:
        param.setValue("// iChannel0: BufC, filter=linear, wrap=clamp\n// iChannel1: Modulate (Image containing a factor to be applied to the Blur size in the first channel), filter=linear, wrap=clamp\n// Bbox: iChannel0\n\nconst vec2 blurdir = vec2( 1.0, -1.0 );\n\nuniform float blurdist_px = 64.0; // Blur Size (Blur distance in pixels), min=0., max=64\nuniform int NUM_SAMPLES = 16; // No. Samples (Number of samples per pass), min=1, max=32\nuniform bool perpixel_size = false; // Modulate (Modulate the blur size by multiplying it by the first channel of the Modulate input)\n\nconst vec2 iRenderScale = vec2(1.,1.);\n\n//note: uniform pdf rand [0;1[\nfloat hash12n(vec2 p)\n{\n    p  = fract(p * vec2(5.3987, 5.4421));\n    p += dot(p.yx, p.xy + vec2(21.5351, 14.3137));\n    return fract(p.x * p.y * 95.4307);\n}\n\nvoid mainImage( out vec4 fragColor, in vec2 fragCoord )\n{\n    vec2 blurvec = normalize(blurdir);\n    vec2 uv = fragCoord / iResolution.xy;\n    float blurdist = blurdist_px * iRenderScale.x;\n    if (perpixel_size) {\n        blurdist *= texture2D(iChannel1, (fragCoord.xy-iChannelOffset[1].xy)/iChannelResolution[1].xy).x;\n    }\n\n    vec2 p0 = fragCoord - 0.5 * blurdist * blurvec;\n    vec2 p1 = fragCoord + 0.5 * blurdist * blurvec;\n    vec2 stepvec = (p1-p0) / float(NUM_SAMPLES)/ iResolution.xy;\n    vec2 p = p0 / iResolution.xy + (hash12n(uv+iGlobalTime)-0.5) * stepvec;\n\n    vec4 sumcol = vec4(0.0);\n    for (int i=0;i<NUM_SAMPLES;++i)\n    {\n     \tsumcol += texture2D( iChannel0, p, -10.0 );\n        p += stepvec;\n    }\n    sumcol /= float(NUM_SAMPLES);\n\n    fragColor = sumcol;\n}\n")
        del param

    param = lastNode.getParam("mipmap0")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap0")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel0")
    if param is not None:
        param.setValue("BufC")
        del param

    param = lastNode.getParam("mipmap1")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap1")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel1")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("inputHint1")
    if param is not None:
        param.setValue("Image containing a factor to be applied to the Blur size in the first channel")
        del param

    param = lastNode.getParam("inputEnable2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("inputEnable3")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("bbox")
    if param is not None:
        param.set("iChannel0")
        del param

    param = lastNode.getParam("mouseParams")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("paramCount")
    if param is not None:
        param.setValue(3, 0)
        del param

    param = lastNode.getParam("paramType0")
    if param is not None:
        param.set("float")
        del param

    param = lastNode.getParam("paramName0")
    if param is not None:
        param.setValue("blurdist_px")
        del param

    param = lastNode.getParam("paramLabel0")
    if param is not None:
        param.setValue("Blur Size")
        del param

    param = lastNode.getParam("paramHint0")
    if param is not None:
        param.setValue("Blur distance in pixels")
        del param

    param = lastNode.getParam("paramDefaultFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramMinFloat0")
    if param is not None:
        param.setValue(0, 0)
        del param

    param = lastNode.getParam("paramMaxFloat0")
    if param is not None:
        param.setValue(64, 0)
        del param

    param = lastNode.getParam("paramType1")
    if param is not None:
        param.set("int")
        del param

    param = lastNode.getParam("paramName1")
    if param is not None:
        param.setValue("NUM_SAMPLES")
        del param

    param = lastNode.getParam("paramLabel1")
    if param is not None:
        param.setValue("No. Samples")
        del param

    param = lastNode.getParam("paramHint1")
    if param is not None:
        param.setValue("Number of samples per pass")
        del param

    param = lastNode.getParam("paramDefaultInt1")
    if param is not None:
        param.setValue(16, 0)
        del param

    param = lastNode.getParam("paramMinInt1")
    if param is not None:
        param.setValue(1, 0)
        del param

    param = lastNode.getParam("paramMaxInt1")
    if param is not None:
        param.setValue(32, 0)
        del param

    param = lastNode.getParam("paramType2")
    if param is not None:
        param.set("bool")
        del param

    param = lastNode.getParam("paramName2")
    if param is not None:
        param.setValue("perpixel_size")
        del param

    param = lastNode.getParam("paramLabel2")
    if param is not None:
        param.setValue("Modulate")
        del param

    param = lastNode.getParam("paramHint2")
    if param is not None:
        param.setValue("Modulate the blur size by multiplying it by the first channel of the Modulate input")
        del param

    del lastNode
    # End of node "BufD"

    # Start of node "Image"
    lastNode = app.createNode("net.sf.openfx.Shadertoy", 1, group)
    lastNode.setScriptName("Image")
    lastNode.setLabel("Image")
    lastNode.setPosition(599, 391)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupImage = lastNode

    param = lastNode.getParam("mouseClick")
    if param is not None:
        param.setValue(0, 0)
        param.setValue(0, 1)
        del param

    param = lastNode.getParam("imageShaderFileName")
    if param is not None:
        param.setValue("[Project]/Image.frag")
        del param

    param = lastNode.getParam("imageShaderSource")
    if param is not None:
        param.setValue("// iChannel0: BufA, filter=linear, wrap=clamp\n// iChannel1: BufB, filter=linear, wrap=clamp\n// iChannel2: BufC, filter=linear, wrap=clamp\n// iChannel3: BufD, filter=linear, wrap=clamp\n// Bbox: iChannel1\n\nvoid mainImage( out vec4 fragColor, in vec2 fragCoord )\n{\n    vec2 uv = fragCoord.xy / iResolution.xy;\n\t\n    //vec4 s0 = texture2D( iChannel0, uv, -10.0 );\n    vec4 s1 = texture2D( iChannel1, uv, -10.0 );\n\n    //vec4 s2 = texture2D( iChannel2, uv, -10.0 );\n    vec4 s3 = texture2D( iChannel3, uv, -10.0 );\n    \n    fragColor = min( s1, s3 ); //octagon\n    //fragColor = max( s1, s3 ); //star\n}\n")
        del param

    param = lastNode.getParam("inputEnable0")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("mipmap0")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap0")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel0")
    if param is not None:
        param.setValue("BufA")
        del param

    param = lastNode.getParam("mipmap1")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap1")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel1")
    if param is not None:
        param.setValue("BufB")
        del param

    param = lastNode.getParam("inputEnable2")
    if param is not None:
        param.setValue(False)
        del param

    param = lastNode.getParam("mipmap2")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap2")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel2")
    if param is not None:
        param.setValue("BufC")
        del param

    param = lastNode.getParam("mipmap3")
    if param is not None:
        param.set("linear")
        del param

    param = lastNode.getParam("wrap3")
    if param is not None:
        param.set("clamp")
        del param

    param = lastNode.getParam("inputLabel3")
    if param is not None:
        param.setValue("BufD")
        del param

    param = lastNode.getParam("mouseParams")
    if param is not None:
        param.setValue(False)
        del param

    del lastNode
    # End of node "Image"

    # Start of node "Dot5"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot5")
    lastNode.setLabel("Dot5")
    lastNode.setPosition(706, 124)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot5 = lastNode

    del lastNode
    # End of node "Dot5"

    # Start of node "Dot6"
    lastNode = app.createNode("fr.inria.built-in.Dot", 1, group)
    lastNode.setScriptName("Dot6")
    lastNode.setLabel("Dot6")
    lastNode.setPosition(576, 111)
    lastNode.setSize(15, 15)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupDot6 = lastNode

    del lastNode
    # End of node "Dot6"

    # Start of node "Source"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Source")
    lastNode.setLabel("Source")
    lastNode.setPosition(705, -13)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupSource = lastNode

    del lastNode
    # End of node "Source"

    # Start of node "Modulate"
    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Modulate")
    lastNode.setLabel("Modulate")
    lastNode.setPosition(477, -8)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.3, 0.5, 0.2)
    groupModulate = lastNode

    del lastNode
    # End of node "Modulate"

    # Start of node "Output1"
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setLabel("Output1")
    lastNode.setPosition(599, 443)
    lastNode.setSize(104, 26)
    lastNode.setColor(0.7, 0.7, 0.7)
    groupOutput1 = lastNode

    del lastNode
    # End of node "Output1"

    # Now that all nodes are created we can connect them together, restore expressions
    groupBufA.connectInput(0, groupDot5)
    groupBufA.connectInput(1, groupDot6)
    groupBufB.connectInput(0, groupBufA)
    groupBufB.connectInput(1, groupDot6)
    groupBufC.connectInput(0, groupDot5)
    groupBufC.connectInput(1, groupDot6)
    groupBufD.connectInput(0, groupBufC)
    groupBufD.connectInput(1, groupDot6)
    groupImage.connectInput(0, groupBufD)
    groupImage.connectInput(1, groupBufB)
    groupImage.connectInput(3, groupBufD)
    groupDot5.connectInput(0, groupSource)
    groupDot6.connectInput(0, groupModulate)
    groupOutput1.connectInput(0, groupImage)

    param = groupBufA.getParam("paramValueFloat0")
    group.getParam("BufAparamValueFloat0").setAsAlias(param)
    del param
    param = groupBufA.getParam("paramValueInt1")
    group.getParam("BufAparamValueInt1").setAsAlias(param)
    del param
    param = groupBufA.getParam("paramValueBool2")
    group.getParam("BufAparamValueBool2").setAsAlias(param)
    del param
    param = groupBufB.getParam("paramValueFloat0")
    param.slaveTo(groupBufA.getParam("paramValueFloat0"), 0, 0)
    del param
    param = groupBufB.getParam("paramValueInt1")
    param.slaveTo(groupBufA.getParam("paramValueInt1"), 0, 0)
    del param
    param = groupBufB.getParam("paramValueBool2")
    param.slaveTo(groupBufA.getParam("paramValueBool2"), 0, 0)
    del param
    param = groupBufC.getParam("paramValueFloat0")
    param.slaveTo(groupBufA.getParam("paramValueFloat0"), 0, 0)
    del param
    param = groupBufC.getParam("paramValueInt1")
    param.slaveTo(groupBufA.getParam("paramValueInt1"), 0, 0)
    del param
    param = groupBufC.getParam("paramValueBool2")
    param.slaveTo(groupBufA.getParam("paramValueBool2"), 0, 0)
    del param
    param = groupBufD.getParam("paramValueFloat0")
    param.slaveTo(groupBufA.getParam("paramValueFloat0"), 0, 0)
    del param
    param = groupBufD.getParam("paramValueInt1")
    param.slaveTo(groupBufA.getParam("paramValueInt1"), 0, 0)
    del param
    param = groupBufD.getParam("paramValueBool2")
    param.slaveTo(groupBufA.getParam("paramValueBool2"), 0, 0)
    del param

    try:
        extModule = sys.modules["BokehOctagon_GLExt"]
    except KeyError:
        extModule = None
    if extModule is not None and hasattr(extModule ,"createInstanceExt") and hasattr(extModule.createInstanceExt,"__call__"):
        extModule.createInstanceExt(app,group)

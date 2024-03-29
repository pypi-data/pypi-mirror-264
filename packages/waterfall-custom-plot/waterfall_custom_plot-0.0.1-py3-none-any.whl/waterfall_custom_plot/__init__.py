import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _waterfall_plot = components.declare_component(
        "waterfall_plot",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _waterfall_plot = components.declare_component("waterfall_plot", path=build_dir)

def waterfall_plot(data=None, styles=None, heightSet=None, useImg=None, useAboveBarShape=None, tooltipHtml=None, tooltipConfig=None, key=None, default=None):

    component_value = _waterfall_plot( 
        data=data, 
        styles=styles, 
        heightSet=heightSet, 
        useImg=useImg, 
        useAboveBarShape=useAboveBarShape, 
        tooltipHtml=tooltipHtml,
        tooltipConfig=tooltipConfig,
        key=key, 
        default=default
        )

    return component_value

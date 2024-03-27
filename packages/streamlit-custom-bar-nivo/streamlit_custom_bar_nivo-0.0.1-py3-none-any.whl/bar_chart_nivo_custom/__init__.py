import os
import streamlit.components.v1 as components

_RELEASE = True  

if not _RELEASE:
    _nivo_bar = components.declare_component(
        
        "nivo_bar",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _nivo_bar = components.declare_component("nivo_bar", path=build_dir)

def nivo_bar( 
        barChartCustomComponent=None,
        barChartCustomColor=None,
        barChartCustomColorsToSet=None,
        customChartTextLayout=None,
        chartData=None, 
        styles=None, 
        chartLayout=None, 
        key=None, 
        default=None
        ):
    
    component_value = _nivo_bar(
        barChartCustomComponent=barChartCustomComponent,
        barChartCustomColor=barChartCustomColor,
        barChartCustomColorsToSet=barChartCustomColorsToSet,
        customChartTextLayout=customChartTextLayout,
        chartData=chartData, 
        chartLayout=chartLayout, 
        styles=styles, 
        key=key, 
        default=default
        )

    return component_value

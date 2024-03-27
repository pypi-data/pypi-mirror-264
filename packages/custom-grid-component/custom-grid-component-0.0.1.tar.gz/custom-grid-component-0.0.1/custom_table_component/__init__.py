import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _grid_plot = components.declare_component(
        "grid_plot",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _grid_plot = components.declare_component("grid_plot", path=build_dir)


def grid_plot(tableData=None, chartType=None, Legends=None, styles=None, key=None):
    
    component_value = _grid_plot(tableData=tableData, chartType=chartType, Legends=Legends, styles=styles, key=key, default=0)

    return component_value

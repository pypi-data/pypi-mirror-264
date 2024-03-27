import os
import streamlit as st
import streamlit.components.v1 as components
import requests
from arcgis.gis import GIS
from arcgis.gis import User
from arcgis.features import FeatureLayerCollection, FeatureLayer
import os
import json


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("streamlit_arcgis_map"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_arcgis_map",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_arcgis_map", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_arcgis_map(layers_urls=None, layer_data=None, layer_styling=None, api_key=None, key=None):
    """Create a new instance of "streamlit_arcgis_map".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(layers_urls=layers_urls, layer_data=layer_data, layer_styling=layer_styling, api_key=api_key, key=key, default=None)
    

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value




if not _RELEASE:
    
    layers_urls = None
    reference_data = None
    point_markerSymbol = None
    shp_item = None
    polygon_markerSymbol = None
    response = None
    token = None
    
    # uploaded_shapefile = st.file_uploader("Upload shapefile", type="zip")

    # if st.button("Click Me"):
    #     st.write("Button clicked!")
    #     layers_urls = "https://services2.arcgis.com/HlCEjEqEP9GdOQeZ/arcgis/rest/services/python_interpolated_predictions_2024_03_11_16_26_06/FeatureServer/0"
        
    #     gis = GIS(url="https://wfid.maps.arcgis.com/", username="diliadis", password="esriwfid2024", api_key="iVaiHMdl_a1rqBZNe2hh8NoQP71Ld9v99OKyfGIoHnkO3gPjpw4_-N754ZK-FfwfTNaw0z4g8N1gVUibWZ-HXAg02lvPOyEVlW95bs9x0zWnnUR30BO0QaMnKcw_LhlBN1DTlOx8wrM08DBQPtv9gg..")
    #     user = User(gis,'diliadis')
    #     token = gis._con.token
        
    #     genus_name = 'Betula'
    #     analysis_type = 'SIRA'

    #     reference_data_layer = FeatureLayer("https://services2.arcgis.com/HlCEjEqEP9GdOQeZ/arcgis/rest/services/analyzed_unanalyzed_combined_data_dev/FeatureServer/0")
    #     reference_data = reference_data_layer.query(where="Category = 'CAT3' AND Analyzed = 'analyzed' AND Genus = '"+genus_name+"' AND Technique = '"+analysis_type+"'", out_fields='*', return_geometry=True).to_dict()
    #     # st.write('reference_data: '+str(reference_data))
    #     # print(str(reference_data))
        
    #     point_markerSymbol = {
    #         "type": "simple-marker",  #  autocasts as new SimpleMarkerSymbol()
    #         "style": "circle",
    #         "color": "red",
    #         "size": "10px",  #  pixels
    #         "outline": {  #  autocasts as new SimpleLineSymbol()
    #         "color": "red",
    #         "width": 5  #  points
    #         }
    #     }
        
    #     polygon_markerSymbol = {
    #         "type": "simple-fill",  #  autocasts as new SimpleFillSymbol()
    #         "color": [227, 139, 79, 0.8],
    #         "outline": {  #  autocasts as new SimpleLineSymbol()
    #             "color": [255, 255, 255],
    #             "width": 1
    #         }
    #     }
        
        
    #     # # Set the portal URL and the endpoint for the generate operation
    #     # portal_url = "https://www.arcgis.com/sharing/rest/content/features/generate"
    #     # # Prepare the parameters as a dictionary
    #     # params = {
    #     #     'name': 'fileName',  # Replace this with the actual name of your file
    #     #     'targetSR': 'mapView.spatialReference',  # You'll need to replace this with actual spatial reference
    #     #     'maxRecordCount': 1000,
    #     #     'enforceInputFileSizeLimit': True,
    #     #     'enforceOutputJsonSizeLimit': True,
    #     #     'generalize': True,
    #     #     'maxAllowableOffset': 10,
    #     #     'reducePrecision': True,
    #     #     'numberOfDigitsAfterDecimal': 0
    #     # }

    #     # # Additional content parameters for the request
    #     # my_content = {
    #     #     'filetype': 'shapefile',
    #     #     'publishParameters': json.dumps(params),
    #     #     'f': 'json',
    #     # }

    #     # # The 'files' parameter should include the actual file you want to upload
    #     # # Here 'file' is the parameter name expected by the ArcGIS REST API, adjust if necessary
    #     # files = {'file': ('filename.zip', uploaded_shapefile, 'application/zip')}

    #     # # Make the request
    #     # response = requests.post(portal_url, data=my_content, files=files)

    #     # # Check if the request was successful
    #     # if response.status_code == 200:
    #     #     # Print the feature collection
    #     #     # st.write('reference_data: '+json.dumps(reference_data))
    #     #     # st.write('Feature Collection:', json.dumps(response.json()['featureCollection']['layers'][0]['featureSet']))
    #     #     pass
    #     # else:
    #     #     st.write('Failed to generate feature collection', response.text)
    # layers_urls = "https://services2.arcgis.com/HlCEjEqEP9GdOQeZ/arcgis/rest/services/python_interpolated_predictions_2024_03_11_16_26_06/FeatureServer/0"
    # st.info("The layer_url is:"+str(layers_urls))
    # # streamlit_arcgis_map(layer_data=json.dumps(reference_data) if reference_data else None, layer_styling=json.dumps(point_markerSymbol))
    # st.info('iVaiHMdl_a1rqBZNe2hh8NoQP71Ld9v99OKyfGIoHnkO3gPjpw4_-N754ZK-FfwfTNaw0z4g8N1gVUibWZ-HXAg02lvPOyEVlW95bs9x0zWnnUR30BO0QaMnKcw_LhlBN1DTlOx8wrM08DBQPtv9gg..')
    # streamlit_arcgis_map(layers_urls=[layers_urls, "https://services2.arcgis.com/HlCEjEqEP9GdOQeZ/arcgis/rest/services/analyzed_unanalyzed_combined_data_dev/FeatureServer/0"], api_key=token, layer_styling=json.dumps(point_markerSymbol))
    # if response:
    #     st.write('response: '+str(response))
        
    # # streamlit_arcgis_map(layer_data=json.dumps(response.json()['featureCollection']['layers'][0]['featureSet']) if response else None, layer_styling=json.dumps(polygon_markerSymbol))


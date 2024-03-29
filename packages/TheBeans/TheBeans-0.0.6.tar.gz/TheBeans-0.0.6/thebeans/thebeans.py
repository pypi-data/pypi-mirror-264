"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    """Map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    
    def __init__(self, center = (47.7511, -120.7401), zoom = 6, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to WA [47.7511, -120.7401].
            zoom (int, optional): Set the zoom level of the map. Defaults to 6.
        """
        super().__init__(center = center, zoom = zoom, **kwargs)
        self.add_control(ipyleaflet.LayerControl())

          
    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add_layer(layer)
    
    #This block means you can call up a basemap based on a string.
    #You can call up the basemap without knowing the url
    def add_basemap(self, name):
        """
        Adds a basemap to the current map.

        Args:
            name (str or object): The name of the basemap as a string, or an object representing the basemap.

        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.

        Returns:
            None
        """
        # if isinstance(name, str):
        #     basemap = eval(f"basemaps.{name}").build_url() #eval is a function that evaluates a string as a python expression or turns string into object
        #     self.add(basemap)
        # else:
        #     self.add(name)
        if instance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_layers_control(self, position='topright'):
        """Adds a layers control to the map.

        Args:
            position (str, optional): The position of the layers control. Defaults to "topright".
        """
        self.add_control(ipyleaflet.LayersControl(position=position))


#3/18 lecuture
    def add_geojson(self, data, name="geojson", **kwargs):
        self.add_control(ipyleaflet.GeoJSON(data=data, name=name, **kwargs))
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)
        
        if "style" not in kwargs:
          kwargs['style'] = {
              "color": "green",
              "weight": 1,
              "fillColor": "ff0000",
              "fillOpacity": 0.0
          }

        if "hover_style" not in kwargs:
            kwargs['hover_style'] = {
                "fillColor": "#ff0000",
                "fillOpacity": 0.5
            }

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    def add_shp(self, data, name="shp", **kwargs):
        """
        Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string, or a dictionary representing the shapefile.
            name (str, optional): The name of the layer. Defaults to "shp".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is neither a string nor a dictionary representing a shapefile.

        Returns:
            None
        """
        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)

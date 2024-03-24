from setuptools import setup

if __name__ == "__main__":
    setup(
        entry_points={
            "console_scripts": [
                "convert_geojson = ml_dronebase_data_utils.geo.convert_geojson_cli:convert_geojson_cli",
                "visualize_converted_geojson = ml_dronebase_data_utils.geo.visualize_converted_geojson:visualize_converted_geojson",
            ]
        }
    )

import json
import os
import pyarrow as pa

from .const import PA_TYPE_MAP, GP_TYPE_MAP
from .util import log, load_fiboa_schema, load_file
from .geopandas import to_parquet
from geopandas import GeoDataFrame
from shapely.geometry import shape

def create(config):
    output_file = config.get("out")

    # Add a STAC collection to the fiboa property to the Parquet metadata
    collection = load_file(config.get("collection"))
    if "id" not in collection or not collection["id"]:
        collection["id"] = os.path.basename(output_file)
    if "fiboa_version" not in collection:
        raise Exception("No fiboa_version found in collection metadata")
    else:
        config["fiboa_version"] = collection["fiboa_version"]
    # todo: fill with more/better metadata

    # Load all features from the GeoJSON files
    features = []
    files = config.get("files")
    for file in files:
        geojson = load_file(file)
        if geojson["type"] == "Feature":
            features.append(geojson)
        elif geojson["type"] == "FeatureCollection":
            features += geojson["features"]
        else:
            log(f"{file}: Skipped - Unsupported GeoJSON type, must be Feature or FeatureCollection")

    if len(features) == 0:
        raise Exception("No valid features provided as input files")

    properties = {}

    # Load the data schema
    fiboa_schema = load_fiboa_schema(config)
    properties.update(fiboa_schema["properties"])

    # Load all extension schemas
    extensions = {}
    if "fiboa_extensions" in collection and isinstance(collection["fiboa_extensions"], list):
        ext_map = config.get("extension_schemas", [])
        for ext in collection["fiboa_extensions"]:
            try:
                if ext in ext_map:
                    path = ext_map[ext]
                    log(f"Redirecting {ext} to {path}", "info")
                else:
                    path = ext
                extensions[ext] = load_file(path)
                properties.update(extensions[ext]["properties"])
            except Exception as e:
                log(f"Extension schema for {ext} can't be loaded: {e}", "warning")

    # Get a list of the properties/columns (without duplicates)
    columns = set(["id", "geometry"])
    for feature in features:
        keys = feature["properties"].keys()
        columns.update(keys)

    columns = list(columns)
    columns.sort()

    # Define the fields for the schema
    pq_fields = []
    for name in columns:
        if not name in properties:
            log(f"{name}: No schema defined", "warning")
            continue
        prop_schema = properties[name]
        pa_type = create_type(prop_schema)
        nullable = not prop_schema.get("required", False)
        field = pa.field(name, pa_type, nullable = nullable)
        pq_fields.append(field)

    # Define the schema for the Parquet file
    pq_schema = pa.schema(pq_fields)
    pq_schema = pq_schema.with_metadata({"fiboa": json.dumps(collection).encode("utf-8")})

    # Create GeoDataFrame from the features
    data = create_dataframe(features, columns, fiboa_schema)

    # Write the data to the Parquet file
    # Proprietary function exported from geopandas to solve
    # https://github.com/geopandas/geopandas/issues/3182
    to_parquet(
        data,
        output_file,
        schema = pq_schema,
        index = False,
        coerce_timestamps = "ms"
    )

    log(f"Wrote to {output_file}", "success")

def create_dataframe(features, columns, schema):
    # Create a list of shapes
    rows = []
    for feature in features:
        id = feature["id"] if "id" in feature else None
        geometry = shape(feature["geometry"]) if "geometry" in feature else None
        row = {
            "id": id,
            "geometry": geometry,
        }
        properties = feature["properties"] if "properties" in feature else {}
        row.update(properties)
        rows.append(row)

    # Create the GeoDataFrame
    data = GeoDataFrame(rows, columns=columns, geometry="geometry", crs="EPSG:4326")

    # Convert the data to the correct types
    for column in columns:
        if column not in schema["properties"]:
            continue
        dtype = schema["properties"][column].get("type", None)
        if dtype == "geometry":
            continue

        gp_type = GP_TYPE_MAP.get(dtype, None)
        if gp_type is None:
            log(f"{column}: No type conversion available for {dtype}")
        elif callable(gp_type):
            data[column] = gp_type(data[column])
        else:
            data[column] = data[column].astype(gp_type)

    return data

def create_type(schema):
    dtype = schema.get("type", None)
    if dtype is None:
        raise Exception("No type specified")

    pa_type = PA_TYPE_MAP.get(dtype, None)
    if pa_type is None:
        raise Exception(f"{dtype} is not supported yet")
    elif callable(pa_type):
        if dtype == "array":
            pa_subtype = create_type(schema["items"])
            pa_type = pa_type(pa_subtype)
        elif dtype == "object":
            log(f"Creation of object-typed properties not supported yet", "warning")
            pass # todo

    return pa_type

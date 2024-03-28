import sys
from collections import Counter

from loguru import logger

from . import checks_invalid, checks_problematic
from .geometry_utils import prepare_geometries_for_checks

logger.remove()
logger_format = "{time:YYYY-MM-DD_HH:mm:ss.SSS} | {message}"
logger.add(sink=sys.stderr, format=logger_format, level="INFO")


ALL_ACCEPTED_GEOMETRY_TYPES = POI, MPOI, LS, MLS, POL, MPOL = [
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]

VALIDATION_CRITERIA = {
    "invalid_geometries": {
        "unclosed": {"relevant": [POL, MPOL], "input": "json_geometry"},
        "duplicate_nodes": {
            "relevant": [LS, MLS, POL, MPOL],
            "input": "json_geometry",
        },
        "less_three_unique_nodes": {
            "relevant": [POL, MPOL],
            "input": "json_geometry",
        },
        "exterior_not_ccw": {
            "relevant": [POL, MPOL],
            "input": "shapely_geom",
        },
        "interior_not_cw": {
            "relevant": [POL, MPOL],
            "input": "shapely_geom",
        },
        "inner_and_exterior_ring_intersect": {
            "relevant": [POL, MPOL],
            "input": "shapely_geom",
        },
        "outside_lat_lon_boundaries": {
            "relevant": ALL_ACCEPTED_GEOMETRY_TYPES,
            "input": "json_geometry",
        },
        "crs_defined": {
            "relevant": ["FeatureCollection"],
            "input": "json_geometry",
        },
        # "zero-length": {"relevant": ["LineString"], "input": "json_geometry"},
    },
    "problematic_geometries": {
        "holes": {"relevant": [POL, MPOL], "input": "shapely_geom"},
        "self_intersection": {
            "relevant": [POL, MPOL],
            "input": "shapely_geom",
        },
        "excessive_coordinate_precision": {
            "relevant": ALL_ACCEPTED_GEOMETRY_TYPES,
            "input": "json_geometry",
        },
        "excessive_vertices": {
            "relevant": [LS, MLS, POL, MPOL],
            "input": "json_geometry",
        },
        "more_than_2d_coordinates": {
            "relevant": ALL_ACCEPTED_GEOMETRY_TYPES,
            "input": "json_geometry",
        },
        "crosses_antimeridian": {
            "relevant": [LS, MLS, POL, MPOL],
            "input": "json_geometry",
        },
        # "wrong_bbox_order: {}"
    },
}


def check_criteria(selected_criteria, criteria_type):
    if selected_criteria:
        for criterium in selected_criteria:
            if criterium not in VALIDATION_CRITERIA[criteria_type]:
                raise ValueError(
                    f"The selected criterium {criterium} is not a valid argument for {criteria_type}"
                )
        logger.info(f"Validation criteria '{criteria_type}': {selected_criteria}")


def apply_check(
    criterium, geometry, shapely_geom, geometry_type, criteria_type="invalid_geometries"
):
    """Applies the correct check for the criteria"""
    geometry_input_options = {"json_geometry": geometry, "shapely_geom": shapely_geom}
    relevant_geometry_type = VALIDATION_CRITERIA[criteria_type][criterium]["relevant"]
    if geometry_type in relevant_geometry_type:
        check_module = (
            checks_invalid if criteria_type == "invalid_geometries" else checks_problematic
        )
        check_func = getattr(check_module, f"check_{criterium}")
        required_input_type = VALIDATION_CRITERIA[criteria_type][criterium]["input"]
        return check_func(geometry_input_options[required_input_type])


def process_validation(geometries, criteria_invalid, criteria_problematic):
    results_invalid, results_problematic = {}, {}
    skipped_validation = []
    geometry_types = []

    for i, geometry in enumerate(geometries):
        geometry_type = geometry.get("type", None)
        if geometry_type is None:
            raise ValueError("no 'geometry' field found in GeoJSON Feature")
        geometry_types.append(geometry_type)
        if geometry_type not in ALL_ACCEPTED_GEOMETRY_TYPES:
            logger.info(
                f"Geometry of type {geometry_type} currently not supported, skipping."
            )
            skipped_validation.append(i)  # TODO: Improve skipped_validation result
            continue

        # Handle Multi-Geometries:
        # Explode the single geometries in the multi-geometry to a featurecollection, run a seperate validation.
        # Output results as {3: [1,2]} (fourth geometry, the multigeometry is invalid_geometries, because the second and third
        # subgeometries in it are invalid_geometries.
        if "Multi" in geometry_type:
            single_type = geometry_type.split("Multi")[1]
            single_geometries = [
                {"type": single_type, "coordinates": g} for g in geometry["coordinates"]
            ]
            results_mp = process_validation(
                single_geometries, criteria_invalid, criteria_problematic
            )
            # Take all invalid_geometries criteria from the e.g. Polygons inside the Multipolygon and indicate them
            # as the positional index of the MultiPolygon.
            for criterium in results_mp["invalid_geometries"]:
                results_invalid.setdefault(criterium, []).append(
                    {i: results_mp["invalid_geometries"][criterium]}
                )
            for criterium in results_mp["problematic_geometries"]:
                results_problematic.setdefault(criterium, []).append(
                    {i: results_mp["problematic_geometries"][criterium]}
                )
                # results_problematic.setdefault(criterium, []).append(i)  # TODO: Really better?
            continue

        # Handle Single-Geometries
        geometry, shapely_geom = prepare_geometries_for_checks(geometry)
        if criteria_invalid:
            for criterium in criteria_invalid:
                if apply_check(
                    criterium, geometry, shapely_geom, geometry_type, "invalid_geometries"
                ):
                    results_invalid.setdefault(criterium, []).append(i)
        if criteria_problematic:
            for criterium in criteria_problematic:
                if apply_check(
                    criterium, geometry, shapely_geom, geometry_type, "problematic_geometries"
                ):
                    results_problematic.setdefault(criterium, []).append(i)

    # TODO: Results format better: feature1: flaws, feature4: flaws, feature9: flaws?
    results = {
        "invalid_geometries": results_invalid,
        "problematic_geometries": results_problematic,
        "count_geometry_types": dict(Counter(geometry_types)),
        "skipped_validation": skipped_validation,
    }

    return results

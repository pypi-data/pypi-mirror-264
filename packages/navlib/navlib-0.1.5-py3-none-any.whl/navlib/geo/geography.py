"""
CoMPAS Navlib - Geography Module

This module provides functions for working with geographic coordinates.

Functions:
    latlon_to_zone_number: Determines the UTM zone number for a given latitude and longitude.
    latlon_to_zone_letter: Determines the UTM zone letter for a given latitude.
    ll2utm: Converts latitude and longitude to UTM coordinates.
    utm2ll: Converts UTM coordinates to latitude and longitude.
    deg2m_lat: Converts latitude from degrees to meters.
    deg2m_lon: Converts longitude from degrees to meters.
    ll2xy: Converts latitude and longitude to xy mercator coordinates from an origin.
    xy2ll: Converts xy mercator coordinates to latitude and longitude from an origin.

Authors: Sebastián Rodríguez-Martínez and Giancarlo Troni
Contact: srodriguez@mbari.org
Last Update: 2024-03-26
"""

__all__ = [
    "latlon_to_zone_number",
    "latlon_to_zone_letter",
    "ll2utm",
    "utm2ll",
    "deg2m_lat",
    "deg2m_lon",
    "ll2xy",
    "xy2ll",
]

import numpy as np
import pyproj


def latlon_to_zone_number(latitude: float, longitude: float) -> int:
    """
    Determines the UTM zone number for a given latitude and longitude.

    Args:
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.

    Returns:
        int: UTM zone number.

    Raise:
        ValueError: If the latitude and longitude are not within the valid range.

    Example:
        >>> latlon_to_zone_number(37.7749, -122.4194)
        10
    """
    # Check if the latitude and longitude are within the valid range.
    if not (-80.0 <= latitude <= 84.0) or not (-180.0 <= longitude <= 180.0):
        raise ValueError("Latitude and longitude must be within the valid range.")

    if 56.0 <= latitude < 64.0 and 3.0 <= longitude < 12.0:
        return 32
    if 72.0 <= latitude < 84.0 and 0.0 <= longitude < 42.0:
        return 31
    return int((longitude + 180) / 6) + 1


def latlon_to_zone_letter(latitude: float) -> str:
    """
    Determines the UTM zone letter for a given latitude.

    Args:
        latitude (float): Latitude in degrees.

    Returns:
        str: UTM zone letter.

    Raise:
        ValueError: If the latitude is not within the valid range.

    Example:
        >>> latlon_to_zone_letter(37.7749)
        'T'
    """
    # Check if the latitude is within the valid range.
    if not (-80.0 <= latitude <= 84.0):
        raise ValueError("Latitude must be within the valid range.")

    if 84 >= latitude >= 72:
        return "X"
    if 72 > latitude >= 64:
        return "W"
    if 64 > latitude >= 56:
        return "V"
    if 56 > latitude >= 48:
        return "U"
    if 48 > latitude >= 40:
        return "T"
    if 40 > latitude >= 32:
        return "S"
    if 32 > latitude >= 24:
        return "R"
    if 24 > latitude >= 16:
        return "Q"
    if 16 > latitude >= 8:
        return "P"
    if 8 > latitude >= 0:
        return "N"
    if 0 > latitude >= -8:
        return "M"
    if -8 > latitude >= -16:
        return "L"
    if -16 > latitude >= -24:
        return "K"
    if -24 > latitude >= -32:
        return "J"
    if -32 > latitude >= -40:
        return "H"
    if -40 > latitude >= -48:
        return "G"
    if -48 > latitude >= -56:
        return "F"
    if -56 > latitude >= -64:
        return "E"
    if -64 > latitude >= -72:
        return "D"
    if -72 > latitude >= -80:
        return "C"
    return "Z"


def ll2utm(latitude: float, longitude: float) -> tuple:
    """
    Converts latitude and longitude to UTM coordinates.

    In this case we will use ENU (not following NED): x-axis is pointing EAST
    y-axis is pointing NORTH and z-axis is pointing UP.

    Args:
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.

    Returns:
        tuple: UTM coordinates. Easting, northing, zone number, and hemisphere.

    Raise:
        ValueError: If the latitude and longitude are not within the valid range.

    Example:
        >>> ll2utm(37.7749, -122.4194)
        (551730.0, 4163834.0, 10, 'north')
    """
    # Check if the latitude and longitude are within the valid range.
    if not (-80.0 <= latitude <= 84.0) or not (-180.0 <= longitude <= 180.0):
        raise ValueError("Latitude and longitude must be within the valid range.")

    zone_number = latlon_to_zone_number(latitude, longitude)
    hemisphere = "north" if latitude > 0 else "south"
    if hemisphere == "north":
        utm_proj = pyproj.Proj(
            proj="utm", zone=f"{zone_number}", ellps="WGS84", datum="WGS84", units="m"
        )
    else:
        utm_proj = pyproj.Proj(
            proj="utm",
            zone=f"{zone_number}",
            ellps="WGS84",
            datum="WGS84",
            units="m",
            south=True,
        )

    # utm_x and utm_y hold the UTM coordinates corresponding to the given latitude and longitude, i.e., easting and
    # northing, respectively.
    easting, northing = utm_proj(longitude, latitude)

    return easting, northing, zone_number, hemisphere


def utm2ll(northing: float, easting: float, zone_str: str) -> tuple:
    """
    Converts the UTMx (easting) and UTMy (northing) and UTM zone coordinates to
    the latitude and longitude mercator projection.

    Args:
        northing (float): Northing in meters.
        easting (float): Easting in meters.
        zone_str (str): UTM zone string. Example: '10N'.

    Returns:
        tuple: Latitude and longitude.

    Raise:
        ValueError: If the UTM zone is not valid.

    Example:
        >>> utm2ll(4163834.0, 551730.0, '10N')
        (37.7749, -122.4194)
    """
    # Check if the zone is a valid UTM zone.
    if not zone_str[0].isdigit() or not zone_str[-1].isalpha():
        raise ValueError("Invalid UTM zone.")

    zone_number = zone_str[: len(zone_str) - 1]

    if int(zone_number) > 60 or int(zone_number) < 1:
        raise ValueError("Invalid UTM zone.")

    if zone_str[-1].upper() == "N":
        ll_proj = pyproj.Proj(
            proj="utm",
            zone=zone_number,
            ellps="WGS84",
            datum="WGS84",
            units="m",
            no_defs=True,
        )
    elif zone_str[-1].upper() == "S":
        ll_proj = pyproj.Proj(
            proj="utm",
            zone=zone_number,
            ellps="WGS84",
            datum="WGS84",
            units="m",
            south=True,
            no_defs=True,
        )
    else:
        raise ValueError("Invalid UTM zone.")

    longitude, latitude = ll_proj(easting, northing, inverse=True)

    return latitude, longitude


def deg2m_lat(latitude: float) -> float:
    """
    Converts latitude from degrees to meters.

    Args:
        latitude (float): Latitude in degrees.

    Returns:
        float: Latitude in meters.

    Example:
        >>> deg2m_lat(1)
        1.1057e+05
    """
    latrad = np.deg2rad(latitude)
    dy = (
        111132.09
        - 566.05 * np.cos(2.0 * latrad)
        + 1.20 * np.cos(4.0 * latrad)
        - 0.002 * np.cos(6.0 * latrad)
    )
    return dy


def deg2m_lon(longitude: float) -> float:
    """
    Converts longitude from degrees to meters.

    Args:
        latitude (float): Latitude in degrees.

    Returns:
        float: Longitude in meters.

    Example:
        >>> deg2m_lon(1)
        1.1113e+05
    """
    latrad = np.deg2rad(longitude)
    dx = (
        111415.13 * np.cos(latrad)
        - 94.55 * np.cos(3.0 * latrad)
        + 0.12 * np.cos(5.0 * latrad)
    )
    return dx


def ll2xy(
    latitude: float,
    longitude: float,
    origin_latitude: float = 0.0,
    origin_longitude: float = 0.0,
) -> tuple:
    """
    Converts latitude and longitude to xy mercator coordinates from an origin.

    In this case we will use ENU (not following NED): x-axis is pointing EAST
    y-axis is pointing NORTH and z-axis is pointing UP.

    Args:
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.
        origin_latitude (float): Origin latitude in degrees.
        origin_longitude (float): Origin longitude in degrees.

    Returns:
        tuple: xy coordinates.

    Example:
        >>> ll2xy(37.7749, -122.4194)
        (551730.0, 4163834.0)
    """
    x = (longitude - origin_longitude) * deg2m_lon(origin_latitude)
    y = (latitude - origin_latitude) * deg2m_lat(origin_latitude)
    return x, y


def xy2ll(
    x: float, y: float, origin_latitude: float = 0.0, origin_longitude: float = 0.0
) -> tuple:
    """
    Converts xy mercator coordinates to latitude and longitude from an origin.

    Args:
        x (float): x coordinate in meters.
        y (float): y coordinate in meters.
        origin_latitude (float): Origin latitude in degrees.
        origin_longitude (float): Origin longitude in degrees.

    Returns:
        tuple: Latitude and longitude.

    Example:
        >>> xy2ll(551730.0, 4163834.0)
        (37.7749, -122.4194)
    """
    latitude = y / deg2m_lat(origin_latitude) + origin_latitude
    longitude = x / deg2m_lon(origin_longitude) + origin_longitude
    return latitude, longitude

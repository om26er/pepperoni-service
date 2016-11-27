from geopy.distance import vincenty


def get_location_from_string(location_string):
    split = location_string.split(',')
    return split[0], split[1]


def are_locations_within_radius(base_location, remote_location, radius):
    return vincenty(
        get_location_from_string(base_location),
        get_location_from_string(remote_location)).kilometers <= float(radius)

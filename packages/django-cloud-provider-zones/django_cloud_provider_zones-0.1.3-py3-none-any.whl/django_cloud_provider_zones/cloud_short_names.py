from enum import Enum, unique

@unique
class CardinalityShortNames(Enum):
    central = "c"
    north = "n"
    south = "s"
    east = "e"
    west = "w"
    northeast = "ne"
    northwest = "nw"
    southeast = "se"
    southwest = "sw"
    northcentral = "nc"
    southcentral = "sc"
    eastcentral = "ec"
    westcentral = "wc"

def get_cardinality_short_name(cardinality: str) -> str:
    return CardinalityShortNames[cardinality].value

def get_region_short_name(region: str) -> str:
    """ GCP and AWS region names """
    match region:
        case "af" | "africa":
            return "af"
        case "ap" | "asiapacific":
            return "ap"
        case "as" | "asia":
            return "as"
        case "au" | "australia":
            return "au"
        case "ca" | "canada":
            return "ca"
        case "eu" | "europe":
            return "eu"
        case "il":
            return "il"
        case "me":
            return "me"
        case "northamerica":
            return "na"
        case "sa" | "southamerica":
            return "sa"
        case "us" | "unitedstates":
            return "us"
    raise ValueError(f"region: {region} not found")
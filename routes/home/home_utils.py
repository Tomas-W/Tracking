def get_2025_weight_dict() -> dict[str, str]:
    """Returns a dictionary of weight image paths for 2025."""
    data = {
        "July": "weight_july_2025_",
        "August": "weight_august_2025_",
    }
    return data


def get_weight_image_paths(month: str) -> tuple[str, str]:
    """Returns a tuple of weight image paths for a given month."""
    if month:
        path_s = f"images/weight_{month.lower()}_2025_s.png"
        path_l = f"images/weight_{month.lower()}_2025_l.png"
    else:
        path_s = "images/weight_july_2025_s.png"
        path_l = "images/weight_july_2025_l.png"
    
    return path_s, path_l


def get_weight_image_title(path_s: str) -> str:
    """Returns the capitalized month of the weight image path."""
    return " ".join(path_s.split("/")[-1].split("_")[:-1]).title()

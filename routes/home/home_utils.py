all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def get_2025_weight_dict() -> dict[str, str]:
    """Returns a dictionary of weight image paths for 2025."""
    data = {
        "July": "weight_july_2025_",
        "August": "weight_august_2025_",
    }
    return data


def get_2025_calories_dict() -> dict[str, str]:
    """Returns a dictionary of calories image paths for 2025."""
    data = {
        "July": "calories_july_2025_",
        "August": "calories_august_2025_",
    }
    return data



def get_weight_image_paths(month: str | None) -> tuple[str, str]:
    """Returns a tuple of weight image paths for a given month."""
    if month is None:
        path_s = "images/weight_2025_s.png"
        path_l = "images/weight_2025_l.png"
    
    else:
        path_s = f"images/weight_{month.lower()}_2025_s.png"
        path_l = f"images/weight_{month.lower()}_2025_l.png"
    
    return path_s, path_l


def get_calories_image_paths(month: str | None) -> tuple[str, str]:
    """Returns a tuple of calories image paths for a given month."""
    if month is None:
        path_s = "images/calories_2025_s.png"
        path_l = "images/calories_2025_l.png"
    
    else:
        path_s = f"images/calories_{month.lower()}_2025_s.png"
        path_l = f"images/calories_{month.lower()}_2025_l.png"

    return path_s, path_l


def get_image_title(path_s: str, month: str) -> str:
    """Returns the capitalized month of the weight image path."""
    if month not in all_months:
        return " ".join(path_s.split("/")[-1].split("_")[1:-1]).title()
    return " ".join(path_s.split("/")[-1].split("_")[1:-1]).title()

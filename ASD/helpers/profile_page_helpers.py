"""Small helpers used in profile page and sidebar (avoid circular imports)."""


def get_initials(name: str) -> str:
    parts = (name or "").strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return (name[:2].upper() if name else "??")


COLOR_MAP = {
    "Ocean Blue": "#1565a0",
    "Emerald":    "#16a34a",
    "Crimson":    "#dc2626",
    "Violet":     "#7c3aed",
    "Teal":       "#0891b2",
    "Slate":      "#475569",
    "Amber":      "#d97706",
    "Rose":       "#e11d48",
}

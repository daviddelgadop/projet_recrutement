ID_COLUMNS = ["Name", "url"]
MAIN_STATS = ["OVR", "PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
GLOBAL_CATEGORICAL = ["League", "Nation", "Position", "Team", "Preferred.foot", "gender", "Alternative.positions"]
GLOBAL_NUMERIC = ["OVR", "Age", "PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
GK_STATS = ["GK.Diving", "GK.Handling", "GK.Kicking", "GK.Positioning", "GK.Reflexes"]
PROFILE_GROUPS = {
    "Général": MAIN_STATS,
    "Attaque": ["Positioning", "Finishing", "Shot.Power", "Long.Shots", "Volleys", "Penalties"],
    "Création": ["Vision", "Crossing", "Free.Kick.Accuracy", "Short.Passing", "Long.Passing", "Curve"],
    "Technique": ["Dribbling", "Agility", "Balance", "Reactions", "Ball.Control", "Composure"],
    "Défense": ["Interceptions", "Heading.Accuracy", "Def.Awareness", "Standing.Tackle", "Sliding.Tackle"],
    "Physique": ["Acceleration", "Sprint.Speed", "Jumping", "Stamina", "Strength", "Aggression"],
    "Gardien": GK_STATS,
}

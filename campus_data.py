"""Campus route data.

The included graph is starter data for demonstrating DSA. Replace distances and
connections with verified pedestrian paths for each real campus before relying
on it for real-world navigation.
"""

CAMPUS_OPTIONS = [
    "Sample Campus (starter route graph)",
    "Ramdeobaba University (map data to configure)",
]

# These are place names only; no unverified GPS coordinates are invented.
LOCATIONS = [
    "Main Gate",
    "Admin Block",
    "ECE Department",
    "Computer Lab",
    "Central Library",
    "Canteen",
    "Auditorium",
    "Sports Ground",
    "Parking",
    "Hostel",
]

# Each edge is (location A, location B, verified walkable distance in metres).
# Current values are starter/sample values for demonstrating the algorithms.
# Replace them with actual measured walking paths for your campus.
EDGES = [
    ("Main Gate", "Admin Block", 120),
    ("Main Gate", "Parking", 60),
    ("Admin Block", "ECE Department", 80),
    ("Admin Block", "Central Library", 140),
    ("ECE Department", "Computer Lab", 35),
    ("ECE Department", "Canteen", 100),
    ("Computer Lab", "Central Library", 90),
    ("Central Library", "Canteen", 70),
    ("Central Library", "Auditorium", 110),
    ("Canteen", "Sports Ground", 160),
    ("Auditorium", "Sports Ground", 130),
    ("Parking", "Hostel", 180),
    ("Hostel", "Sports Ground", 150),
    ("Admin Block", "Auditorium", 170),
]

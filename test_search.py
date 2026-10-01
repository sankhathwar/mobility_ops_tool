from services.data_loader import DataLoader
from services.search_engine import SearchEngine
from models.zone import Zone


loader = DataLoader()

drivers = loader.load_drivers("data/Drivers.csv")
trips = loader.load_trips("data/Trips.csv")


# Create Zone objects from unique pickup zones
zone_names = sorted(
    set(
        trip.pickup_zone
        for trip in trips
        if trip.pickup_zone
    )
)

zones = [
    Zone(zone_id=zone_name, city="Bangalore")
    for zone_name in zone_names
]


search_engine = SearchEngine(
    drivers,
    trips,
    zones
)


print("\nDRIVER SEARCH")
print("=" * 40)

driver = search_engine.search_driver("D101")

if driver:
    print(driver.get_profile())
else:
    print("Driver not found")


print("\nTRIP SEARCH")
print("=" * 40)

trip = search_engine.search_trip("T1001")

if trip:
    print(trip)
    print("Trip ID:", trip.trip_id)
    print("Driver ID:", trip.driver_id)
else:
    print("Trip not found")


print("\nZONE SEARCH")
print("=" * 40)

zone = search_engine.search_zone("Koramangala")

if zone:
    print(zone.get_profile())
else:
    print("Zone not found")


print("\nINVALID SEARCH")
print("=" * 40)

print("Driver:", search_engine.search_driver("D999"))
print("Trip:", search_engine.search_trip("T9999"))
print("Zone:", search_engine.search_zone("Unknown Zone"))
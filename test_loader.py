from services.data_loader import DataLoader


loader = DataLoader()

drivers = loader.load_drivers("data/Drivers.csv")
trips = loader.load_trips("data/Trips.csv")
activities = loader.load_driver_activity("data/Driver_activity.csv")


print("Drivers:", len(drivers))
print("Trips:", len(trips))
print("Activities:", len(activities))

print("\nFirst Driver:")
print(drivers[0].get_profile())

print("\nFirst Trip:")
print(trips[0])

print("\nFirst Activity:")
print(activities[0])
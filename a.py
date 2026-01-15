
def build_baggage_map(flight_manifest):

    baggage_map = {}
    baggage_map = {manifest['tag_id'] : manifest['passenger_name'] for manifest in flight_manifest }   
    return baggage_map


def reconcile_bags(bag_map, scanned_tags):
   
    manifest_tags = set(bag_map.keys())
    scanned_tags_set = set(scanned_tags)

    lost_bags = manifest_tags - scanned_tags_set
    mystery_bags = scanned_tags_set - manifest_tags

    return lost_bags, mystery_bags


def generate_lost_report(bag_map, lost_tag_set):
   
    report = [
        f"MISSING: Bag {tag} (Owner: {bag_map[tag]})"
        for tag in lost_tag_set
    ]
    report.sort(key=lambda x: x.split("Owner: ")[1][:-1])
    return report


manifest = [
    {'tag_id': "BAG-001", 'passenger_name': "Wei Chen"},
    {'tag_id': "BAG-002", 'passenger_name': "Anita Roy"},
    {'tag_id': "BAG-003", 'passenger_name': "Leo Das"}
]

scanned = ["BAG-001", "BAG-003", "BAG-999"]

bag_map = build_baggage_map(manifest)
lost_bags, mystery_bags = reconcile_bags(bag_map, scanned)
report = generate_lost_report(bag_map, lost_bags)

print("Lost Bags:", lost_bags)
print("Mystery Bags:", mystery_bags)
print("Report:", report)

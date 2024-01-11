def get_vehicle(license_plate, vehicle_track_ids):
    x1_lp, y1_lp, x2_lp, y2_lp, score_lp, lp_class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        x1_v, y1_v, x2_v, y2_v, vehicle_id = vehicle_track_ids[j]

        if x1_lp > x1_v and y1_lp > y1_v and x2_lp < x2_v and y2_lp < y2_v:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1

def write_csv(results, output_path):
    with open(output_path, "w") as f:
        f.write(
            "{},{},{},{},{},{},{},{},{},{},{}\n".format(
                "frame_number",
                "vehicle_id",
                "date_detection",
                "time_detection",
                "vehicle_bbox",
                "vehicle_type",
                "license_plate_bbox",
                "license_plate_bbox_score",
                "license_plate_text",
                "license_plate_text_score",
                "license_plate_color",
            )
        )

        for frame_number in results.keys():
            for vehicle_id in results[frame_number].keys():
                if (
                    "vehicle" in results[frame_number][vehicle_id].keys()
                    and "license_plate" in results[frame_number][vehicle_id].keys()
                    and "license_plate_text"
                    in results[frame_number][vehicle_id]["license_plate"].keys()
                ):
                    f.write(
                        "{},{},{},{},{},{},{},{},{},{},{}\n".format(
                            frame_number,
                            vehicle_id,
                            results[frame_number][vehicle_id]["date_detection"],
                            results[frame_number][vehicle_id]["time_detection"],
                            "[{} {} {} {}]".format(
                                results[frame_number][vehicle_id]["vehicle"][
                                    "vehicle_bbox"
                                ][0],
                                results[frame_number][vehicle_id]["vehicle"][
                                    "vehicle_bbox"
                                ][1],
                                results[frame_number][vehicle_id]["vehicle"][
                                    "vehicle_bbox"
                                ][2],
                                results[frame_number][vehicle_id]["vehicle"][
                                    "vehicle_bbox"
                                ][3],
                            ),
                            results[frame_number][vehicle_id]["vehicle"][
                                "vehicle_type"
                            ],
                            "[{} {} {} {}]".format(
                                results[frame_number][vehicle_id]["license_plate"][
                                    "license_plate_bbox"
                                ][0],
                                results[frame_number][vehicle_id]["license_plate"][
                                    "license_plate_bbox"
                                ][1],
                                results[frame_number][vehicle_id]["license_plate"][
                                    "license_plate_bbox"
                                ][2],
                                results[frame_number][vehicle_id]["license_plate"][
                                    "license_plate_bbox"
                                ][3],
                            ),
                            results[frame_number][vehicle_id]["license_plate"][
                                "license_plate_bbox_score"
                            ],
                            results[frame_number][vehicle_id]["license_plate"][
                                "license_plate_text"
                            ],
                            results[frame_number][vehicle_id]["license_plate"][
                                "license_plate_text_score"
                            ],
                            results[frame_number][vehicle_id]["license_plate"][
                                "license_plate_color"
                            ],
                        )
                    )
        f.close()

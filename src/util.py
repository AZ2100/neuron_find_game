import csv
import os
import sys

"""
Returns a dictionary of the form:
data:
    Mecp2Het_170610_DIV44_c1_Fr2_170610:
        filtered-circles: [(x1,y1,r1),(x2,y2,r2),...,(xn,yn,rn))]
        raw-circles: [(x1,y1,r1),(x2,y2,r2),...,(xn,yn,rn))]
        image-clean: path to clean image
        image-raw: path to raw circled image
        image-filtered: path to filtered circled image

    Mecp2KO_170612_DIV41_c1_Fr4_170612:
        filtered-circles: [(x1,y1,r1),(x2,y2,r2),...,(xn,yn,rn))]
        raw-circles: [(x1,y1,r1),(x2,y2,r2),...,(xn,yn,rn))]
        image-clean: path to clean image
        image-raw: path to raw circled image
        image-filtered: path to filtered circled image
    ....
"""


def load_data(path_to_files="game_data"):
    if not os.path.isdir(path_to_files):
        path_to_files = os.path.join("..", "game_data")
        if not os.path.isdir(path_to_files):
            path_to_files = "game_data"
            if not os.path.isdir(path_to_files):
                print("COULD NOT FIND PATH TO FILES")
                sys.exit()

    out_folder = os.path.join(os.path.dirname(path_to_files), "out_files")
    safe_folder(out_folder)

    data = {}
    for subject in os.listdir(path_to_files):
        subj_path = os.path.join(path_to_files, subject)
        if not os.path.isdir(subj_path):
            continue
        out_sub_folder = os.path.join(out_folder, subject)
        safe_folder(out_sub_folder)
        subj_dict = {"root_path": subj_path, "title": subject, "out_path": out_sub_folder}
        for subj_data in os.listdir(subj_path):
            if subj_data[0] == ".":
                continue
            if subj_data == "filtered-circles.csv":
                with open(os.path.join(subj_path, subj_data)) as open_file:
                    subj_dict["filtered-circles"] = [list(map(int, row)) for row in csv.reader(open_file)]

            elif subj_data == "raw-circles.csv":
                with open(os.path.join(subj_path, subj_data)) as open_file:
                    subj_dict["raw-circles"] = [list(map(int, row)) for row in csv.reader(open_file)]
            else:
                subj_dict[subj_data[:-4]] = os.path.join(subj_path, subj_data)
        data[subject] = subj_dict
    return data


def csv_save(signals, file_path):
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(signals)


def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def circle_collide(point, circles, radius=5):
    return any(distance(point, circle) < (min(circle[2], 20) + radius) for circle in circles)


def close_circle(point, circles, radius=10):
    return next((i for i, circle in enumerate(circles) if distance(point, circle) < radius), None)


def score(gold_circles, calculated_circles):
    overlap = list(map(int, [circle_collide(circle, calculated_circles) for circle in gold_circles]))
    TP = sum(overlap)
    FP = max(0.0, len(calculated_circles) - TP)
    sensitivity = TP / float(len(gold_circles))
    specificity = 1.0 - (FP / float(len(calculated_circles)))
    return sensitivity * 100.0, specificity * 100.0


def score_string(gold_circles, calculated_circles):
    try:
        return ("Sensitivity: %.1f%%, Specificity: %.1f%%" % (score(gold_circles, calculated_circles)))
    except Exception as e:
        print((e.message))
        return ("Could Not Calculate Metrics")


def save_string(line, file_path):
    with open(file_path, "a") as f:
        f.write(line + '\n')


def safe_folder(folder):
    """Checks if folder exists and if it does not creates the folder"""
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_gold(folder, suffix="gold_circles.csv"):
    if not os.path.isdir(folder):
        return None
    for file_name in sorted(os.listdir(folder))[::-1]:
        if file_name.endswith(suffix):
            with open(os.path.join(folder, file_name)) as open_file:
                return [list(map(int, row)) for row in csv.reader(open_file)]
    return None

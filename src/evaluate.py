import util
import numpy as np
data_path = "../game_data"
data = util.load_data(data_path)

raw_sensitivities = []
raw_specificities = []

filtered_sensitivities = []
filtered_specificities = []

for sample in data:
    print((data[sample]))
    gold_circles = util.get_gold(data[sample]["out_path"])
    if gold_circles is not None:
        raw_score = util.score(gold_circles, data[sample]["raw-circles"])
        raw_sensitivities.append(raw_score[0])
        raw_specificities.append(raw_score[1])

        try:
            filtered_score = util.score(gold_circles, data[sample]["filtered-circles"])
            filtered_sensitivities.append(filtered_score[0])
            filtered_specificities.append(filtered_score[1])

        except ZeroDivisionError as e:
            print(sample, "does not have filtered circles")

print(("raw sensitivity mean {} std {}".format(np.mean(raw_sensitivities), np.std(raw_sensitivities))))
print(("raw specificity mean {} std {}".format(np.mean(raw_specificities), np.std(raw_specificities))))
print((
"filtered sensitivity mean {} std {}".format(np.mean(filtered_sensitivities), np.std(filtered_sensitivities))))
print((
"filtered specificity mean {} std {}".format(np.mean(filtered_specificities), np.std(filtered_specificities))))

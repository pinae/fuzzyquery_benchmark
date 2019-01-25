import json
import os


def generate_prob_file():
    keyboard = """
        1 2 3 4 5 6 7 8 9 0
        q w e r t z u i o p
         a s d f g h j k l
           y x c v b n m
           ,           .
        """
    keyboard = "\n".join([l[4:] if len(l) > 4 else "" for l in keyboard.strip("\n").splitlines()])
    char_list = "".join(keyboard.split())
    probabilities = {}
    for line_c in char_list:
        def char_pos_in_keyboard(char, kb):
            for i, line in enumerate(kb.splitlines()):
                index_pos = line.find(char)
                if index_pos >= 0:
                    return i, index_pos

        prob_line = {}
        line_sum = 0.0
        for prob_c in char_list:
            lcy, lcx = char_pos_in_keyboard(line_c, keyboard)
            pcy, pcx = char_pos_in_keyboard(prob_c, keyboard)
            square_dist = (lcy - pcy) ** 2 + (lcx / 2 - pcx / 2) ** 2
            if square_dist == 0:
                prob_estimate = 10
            else:
                prob_estimate = 1 / square_dist
            prob_line[prob_c] = prob_estimate
            line_sum += prob_estimate
        for prob_c in char_list:
            prob_line[prob_c] = prob_line[prob_c] / line_sum
        probabilities[line_c] = prob_line
    with open(filename, "w") as prob_file:
        json.dump(probabilities, prob_file)
    return probabilities


filename = "typo_prob_est_de.json"
if os.path.exists(filename):
    with open(filename, "r") as f:
        probabilities = json.load(f)
else:
    probabilities = generate_prob_file()


def levensteinish_probability(original, typed):
    probability = 1.0
    orig_pos = 0
    typed_pos = 0
    while typed_pos < len(typed) and orig_pos < len(original):
        if typed_pos < len(typed) - 1:
            # the char at typed[typed_pos] could be an additional wrong character
            if typed[typed_pos + 1:typed_pos + 3] == original[orig_pos:orig_pos + 2]:
                typed_pos += 1
                probability *= 0.07
                continue
        if orig_pos < len(original) - 1:
            # the user could have forgotten to type char
            if typed[typed_pos:typed_pos + 2] == original[orig_pos + 1:orig_pos + 3]:
                orig_pos += 1
                probability *= 0.07
                continue
        # the typed char could be wrong
        if original[orig_pos] in probabilities and typed[typed_pos] in probabilities[original[orig_pos]]:
            probability *= probabilities[original[orig_pos]][typed[typed_pos]]
        else:
            probability *= 0.69
        typed_pos += 1
        orig_pos += 1
    return probability


def get_typo_candidates(typed_string, k=50):
    candidates = [("", 1.0)]
    for char in typed_string.lower():
        if char in probabilities.keys():
            new_candidates = []
            for candi_str, candi_prob in candidates:
                for c in probabilities[char]:
                    new_candidates.append((candi_str + c, candi_prob * probabilities[char][c]))
            candidates = sorted(new_candidates, key=lambda x: x[1], reverse=True)[:k]
        else:
            for i in range(len(candidates)):
                candidates[i] = (candidates[i][0] + char, candidates[i][1])
    return [c[0] for c in candidates]


if __name__ == "__main__":
    tcandi = get_typo_candidates("Frühstückstlocken", 200)
    print("frühstücksflocken" in tcandi)
    for candi in tcandi:
        print(candi)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


TABLE_DIR = "table-data"
FIGURE_DIR = "figure-data"
RESPONSES_FILE = "responses.tsv"

HOW_OFTEN_VALS = {
    "Never": 0, "A few times a year": 1, "Monthly": 2, "Weekly": 3, "Daily": 4
}

EXPERIENCE_VALS = {
    "0 - 1": 0, "2 - 4": 1, "5 - 8": 2, "9 - 12": 3, "13 +": 4
}

AGREE_VALS = {
    "Strongly disagree": 0, "Disagree": 1, "Agree": 2, "Strongly agree": 3
}

FREQ_VALS = {
    "Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3
}

IMPACTS_LABS = [
    "{\\bf SQ4.1: Reliability}", "{\\bf SQ4.2: Efficiency}", 
    "{\\bf SQ4.3: Productivity}", "{\\bf SQ4.4: Confidence}", 
    "{\\bf SQ4.5: CI}", "{\\bf SQ4.6: Ignore}", "{\\bf SQ4.7: Reproduce}", 
    "{\\bf SQ4.8: Differentiate}"
]

CAUSES_LABS = [
    "{\\bf SQ5.1: Waiting}", "{\\bf SQ5.2: Concurrency}", 
    "{\\bf SQ5.3: Setup/teardown}", "{\\bf SQ5.4: Resources}", 
    "{\\bf SQ5.5: Network}", "{\\bf SQ5.6: Random}", "{\\bf SQ5.7: Time/date}", 
    "{\\bf SQ5.8: Floating point}", "{\\bf SQ5.9: Unordered}", 
    "{\\bf SQ5.10: Unknown}"
]

ACTIONS_LABS = [
    "{\\bf SQ7.1: No action}", "{\\bf SQ7.2: Re-run}", 
    "{\\bf SQ7.3: Document}", "{\\bf SQ7.4: Delete}", 
    "{\\bf SQ7.5: Quarantine}", "{\\bf SQ7.6: Mark skip}", 
    "{\\bf SQ7.7: Mark re-run}", "{\\bf SQ7.8: Repair}"
]


def iter_responces():
    with open(RESPONSES_FILE, "r") as fd:
        for l_no, line in enumerate(fd):
            if l_no == 0: continue
            responces = line.strip().split("\t")
            if responces[1] == "Yes, I consent.": yield responces


def update_counts(responces, values, counts):
    if not all(responces): return
    
    for i, responces_i in enumerate(responces):
        counts[i][values[responces_i]] += 1


def write_bar_chart(file_name, values, counts):
    with open(os.path.join(FIGURE_DIR, file_name), "w") as fd:
        for i in range(len(values)):
            fd.write(f"\\addplot coordinates {{({counts[i]},y)}};\n")

        legend = ",".join(values.keys())
        fd.write(f"\\legend{{{legend}}}\n")


def write_languages_chart(languages):
    coords = sorted(languages.items(), key=lambda x: -x[1])[:10]
    coords = " ".join([f"({x},{y})" for x, y in coords])

    with open(os.path.join(FIGURE_DIR, "languages.tex"), "w") as fd:
        fd.write(f"\\addplot coordinates {{{coords}}};\n")


def get_box(style, x1, x2):
    points = f"({x1},0) -- ({x1},1) -- ({x2},1) -- ({x2},0) -- cycle"
    return f"\\draw [{style}] {points}; "


def get_boxes(n_row, counts):
    boxes = [""] * n_row
    n_responces = sum(counts[0])
    opts = "xscale=7.7,yscale=0.25"

    for i, counts_i in enumerate(counts):
        x1 = 0

        for j, counts_j in enumerate(counts_i):
            if counts_j == 0: continue
            x2 = x1 + counts_j / n_responces
            boxes[i] += get_box(f"fill=gray!{30 * (j + 1)}", x1, x2)
            x1 = x2

        boxes[i] = (
            "\\cellcolor{white} " +
            f"\\begin{{tikzpicture}}[{opts}] {boxes[i]} \\end{{tikzpicture}}"
        )

    return boxes


def get_scores_ranks(n_row, counts):
    scores = [0] * n_row
    n_responces = sum(counts[0])

    for i, counts_i in enumerate(counts):
        for j, counts_j in enumerate(counts_i):
            scores[i] += j * counts_j
            
        scores[i] /= n_responces

    scores_sorted = sorted(scores, reverse=True)
    ranks = [scores_sorted.index(s) + 1 for s in scores]
    return ["%.2f (%s)" % (s_i, ranks[i]) for i, s_i in enumerate(scores)]


def get_counts_table(counts_all):
    n_col = len(counts_all)
    n_row = len(counts_all[0])
    b = get_boxes(n_row, counts_all[4])
    sr = [get_scores_ranks(n_row, counts) for counts in counts_all]
    return [[sr[j][i] for j in range(n_col)] + [b[i]] for i in range(n_row)]


def write_counts_table(file_name, labels, counts_all):
    table = get_counts_table(counts_all)

    with open(os.path.join(TABLE_DIR, file_name), "w") as fd:
        for i, table_i in enumerate(table):
            row = [labels[i], *[str(val) for val in table_i]]
            if i % 2: fd.write("\\rowcolor{gray!20}\n")
            fd.write(" & ".join(row) + " \\\\\n")


if __name__ == "__main__":
    os.makedirs(TABLE_DIR, exist_ok=True)
    os.makedirs(FIGURE_DIR, exist_ok=True)

    how_often = [0] * len(HOW_OFTEN_VALS)
    experience = [0] * len(EXPERIENCE_VALS)
    languages = {}

    impacts = [[[0] * len(AGREE_VALS) for _ in IMPACTS_LABS] for _ in range(5)]
    causes = [[[0] * len(FREQ_VALS) for _ in CAUSES_LABS] for _ in range(5)]
    actions = [[[0] * len(FREQ_VALS) for _ in ACTIONS_LABS] for _ in range(5)]

    for responces in iter_responces():
        profile = [None, None, 4]

        if responces[4]:
            how_often_val = HOW_OFTEN_VALS[responces[4]]
            profile[0] = 0 if how_often_val > 1 else 1
            how_often[how_often_val] += 1

        if responces[34]:
            experience_val = EXPERIENCE_VALS[responces[34]]
            profile[1] = 2 if experience_val == 4 else 3
            experience[experience_val] += 1

        if responces[33]:
            for lang in responces[33].split(", "):
                lang = lang.replace("#", "\\#")
                languages[lang] = languages.get(lang, 0) + 1

        for p in profile:
            if p is None: continue
            update_counts(responces[5:13], AGREE_VALS, impacts[p])
            update_counts(responces[13:23], FREQ_VALS, causes[p])
            update_counts(responces[24:32], FREQ_VALS, actions[p])

    write_bar_chart("how_often.tex", HOW_OFTEN_VALS, how_often)
    write_bar_chart("experience.tex", EXPERIENCE_VALS, experience)
    write_languages_chart(languages)

    write_counts_table("impacts.tex", IMPACTS_LABS, impacts)
    write_counts_table("causes.tex", CAUSES_LABS, causes)
    write_counts_table("actions.tex", ACTIONS_LABS, actions)
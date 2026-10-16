import math, json

RATIO = 0.72  # labeled norm: 2019-scale pints per 2012-scale pint
DAMP = ["damp", "very damp", "wet", "extremely wet"]
BASE = [10, 12, 14, 16]  # labeled norm: pints a day at 500 square feet, 2012 scale
RATE = [4, 5, 6, 7]  # labeled norm: added pints per further 500 square feet

def tenths(x):
    return math.floor(x * 10 + 0.5) / 10

def fixed1(x):
    return f"{tenths(x):.1f}"

def room_need(sqft, level):
    if sqft <= 500:
        return BASE[level] * sqft / 500
    return BASE[level] + RATE[level] * (sqft - 500) / 500

def label_truth(pints, dir):
    if not (pints > 0):
        raise ValueError("the labeled pints must be above zero")
    if dir == "o2n":
        return f"A {pints}-pint 2012 label reads about {fixed1(pints * RATIO)} pints on a 2019 box honestly."
    return f"A {pints}-pint 2019 label reads about {fixed1(pints / RATIO)} pints on a 2012 box honestly."

def room_truth(sqft, level, pints, std):
    if not (sqft > 0):
        raise ValueError("the room size must be above zero")
    if not (pints > 0):
        raise ValueError("the unit pints must be above zero")
    need = room_need(sqft, level)
    offer = pints if std == "2012" else pints / RATIO
    dm = tenths(offer - need)
    if dm > 0:
        verdict = f"a margin of {fixed1(dm)} pints honestly"
    elif dm < 0:
        verdict = f"{fixed1(-dm)} pints short honestly"
    else:
        verdict = "exactly matched honestly"
    return f"A {sqft}-square-foot {DAMP[level]} room asks for {fixed1(need)} pints a day on the 2012 scale; the {pints}-pint {std} unit offers {fixed1(offer)} pints - {verdict}."

def bucket_truth(pull, bucket):
    if not (pull > 0):
        raise ValueError("the daily pull must be above zero")
    if not (bucket > 0):
        raise ValueError("the bucket size must be above zero")
    hours = bucket / pull * 24
    word = "hour" if fixed1(hours) == "1.0" else "hours"
    return f"Pulling {fixed1(pull)} pints a day into a {bucket}-pint bucket asks for an emptying every {fixed1(hours)} {word} honestly."

FNS = {"labelTruth": label_truth, "roomTruth": room_truth, "bucketTruth": bucket_truth}

CASES = [
    ("labelTruth", [70, "o2n"]),
    ("labelTruth", [50, "o2n"]),
    ("labelTruth", [30, "o2n"]),
    ("labelTruth", [50, "n2o"]),
    ("labelTruth", [35, "n2o"]),
    ("labelTruth", [20, "n2o"]),
    ("labelTruth", [1, "o2n"]),
    ("labelTruth", [0, "o2n"]),
    ("labelTruth", [-5, "n2o"]),
    ("roomTruth", [900, 1, 35, "2019"]),
    ("roomTruth", [500, 0, 20, "2012"]),
    ("roomTruth", [2000, 2, 30, "2019"]),
    ("roomTruth", [1500, 3, 30, "2012"]),
    ("roomTruth", [2500, 3, 20, "2019"]),
    ("roomTruth", [300, 0, 20, "2019"]),
    ("roomTruth", [100, 0, 10, "2012"]),
    ("roomTruth", [4000, 3, 70, "2012"]),
    ("roomTruth", [750, 1, 25, "2019"]),
    ("roomTruth", [0, 1, 35, "2019"]),
    ("roomTruth", [900, 1, 0, "2019"]),
    ("bucketTruth", [22, 14]),
    ("bucketTruth", [50, 10]),
    ("bucketTruth", [10, 16]),
    ("bucketTruth", [12, 12]),
    ("bucketTruth", [200, 10]),
    ("bucketTruth", [250, 10]),
    ("bucketTruth", [0, 14]),
    ("bucketTruth", [22, 0]),
]

out = []
for fn, args in CASES:
    rec = {"fn": fn, "args": args}
    try:
        rec["out"] = FNS[fn](*args)
    except ValueError as e:
        rec["err"] = str(e)
    out.append(rec)
    print(fn, args, "->", rec.get("out") or ("ERR: " + rec["err"]))

with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(f"{len(out)} cases written to expected.json")

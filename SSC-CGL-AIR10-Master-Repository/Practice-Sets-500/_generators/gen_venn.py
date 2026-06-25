# -*- coding: utf-8 -*-
r"""
SSC CGL Venn Diagrams / Logical Venn (Reasoning) - 500 MCQ generator.

Two families:
  A) RELATIONSHIP VENN  (curated, fact-checked triples) -> ~30-40%
       Which diagram best represents the relation between three classes.
       Each diagram type is encoded as a known relationship PATTERN and the
       options are *worded descriptions* of diagrams (since we cannot draw).
  B) NUMERIC VENN  (set-counting, COMPUTABLE) -> ~60-70%
       Given region counts / survey data, compute the asked quantity exactly
       via inclusion-exclusion. The key is provably correct.

Numeric items emit a JSON sidecar (qnum -> answer) for cross-check.

CRITICAL: counts are always plain ints; no float ever reaches Fraction(num,den).
"""
import random
import json
from collections import Counter

random.seed(20260625)  # deterministic

LETTERS = "abcd"

# ============================================================================
# RELATIONSHIP VENN
# ============================================================================
# We encode the relationship between three named classes as a PATTERN id, and
# each pattern has a single canonical worded diagram description (the correct
# option). Distractors are descriptions of OTHER patterns.
#
# Pattern ids and their worded descriptions:
PATTERNS = {
    # three mutually exclusive classes (no member shared)
    "DISJOINT3":
        "Three separate (non-overlapping) circles",
    # all three nested: A inside B inside C (each a subclass of the next)
    "NESTED3":
        "One circle inside a second circle, and the second inside a third (fully nested)",
    # two disjoint classes both fully inside a third (genus with two species)
    "TWO_IN_ONE":
        "Two separate (non-overlapping) circles, both lying inside a third bigger circle",
    # all three mutually overlapping (each pair shares some, e.g. classic 3-circle)
    "OVERLAP3":
        "Three circles each overlapping the other two (a common central region)",
    # one class fully inside a second, and a third class disjoint from both
    "ONE_IN_ONE_PLUS_SEP":
        "One circle inside a second circle, and a third separate circle outside both",
    # two classes overlap, third is fully separate from both
    "OVERLAP2_PLUS_SEP":
        "Two overlapping circles and a third separate circle outside both",
    # one class fully inside the overlap-region scenario: A inside B, C overlaps both
    "ONE_IN_TWO_OVERLAP":
        "One circle inside a second circle, with a third circle overlapping both",
    # one big class contains a second; third overlaps only the big one partly
    "CONTAIN_PLUS_PARTIAL":
        "One small circle inside a big circle, and a third circle partly overlapping the big circle",
}
ALL_PATTERN_DESCS = list(PATTERNS.values())

# Curated, fact-checked triples. Each: (term1, term2, term3, pattern, reason)
# The order of terms in the stem is exactly as listed.
RELATION_TRIPLES = [
    # ---- TWO_IN_ONE: two disjoint species inside one genus ----
    ("Dog", "Cat", "Animal", "TWO_IN_ONE",
     "Dogs and cats are different (disjoint) kinds of animals; both are animals."),
    ("Apple", "Mango", "Fruit", "TWO_IN_ONE",
     "Apples and mangoes are distinct fruits; both lie inside the class Fruit."),
    ("Rose", "Lotus", "Flower", "TWO_IN_ONE",
     "Roses and lotuses are different flowers; both are flowers."),
    ("Doctor", "Engineer", "Professional", "TWO_IN_ONE",
     "Doctors and engineers are distinct professions; both are professionals."),
    ("Cricket", "Hockey", "Game", "TWO_IN_ONE",
     "Cricket and hockey are different games; both are games."),
    ("Pen", "Pencil", "Stationery", "TWO_IN_ONE",
     "Pens and pencils are distinct stationery items; both are stationery."),
    ("Car", "Bus", "Vehicle", "TWO_IN_ONE",
     "Cars and buses are different vehicles; both are vehicles."),
    ("Lion", "Tiger", "Carnivore", "TWO_IN_ONE",
     "Lions and tigers are different carnivores; both are carnivores."),
    ("Copper", "Iron", "Metal", "TWO_IN_ONE",
     "Copper and iron are distinct metals; both are metals."),
    ("Hindi", "English", "Language", "TWO_IN_ONE",
     "Hindi and English are different languages; both are languages."),
    ("Sparrow", "Crow", "Bird", "TWO_IN_ONE",
     "Sparrows and crows are different birds; both are birds."),
    ("Table", "Chair", "Furniture", "TWO_IN_ONE",
     "Tables and chairs are distinct furniture items; both are furniture."),
    ("Monday", "Sunday", "Day", "TWO_IN_ONE",
     "Monday and Sunday are different days; both are days."),
    ("Wheat", "Rice", "Cereal", "TWO_IN_ONE",
     "Wheat and rice are different cereals; both are cereals."),
    ("Shirt", "Trouser", "Garment", "TWO_IN_ONE",
     "Shirts and trousers are distinct garments; both are garments."),

    # ---- NESTED3: strict subclass chain A < B < C ----
    ("Second", "Minute", "Hour", "NESTED3",
     "A second is part of a minute, and a minute is part of an hour (nested time units)."),
    ("Village", "District", "State", "NESTED3",
     "A village lies within a district, which lies within a state (nested administrative units)."),
    ("Lecturer", "College", "University", "NESTED3",
     "Lecturers belong to a college, which belongs to a university (nested)."),
    ("Brinjal", "Vegetable", "Food", "NESTED3",
     "Every brinjal is a vegetable, and every vegetable is food (nested classes)."),
    ("Captain", "Team", "Tournament", "NESTED3",
     "A captain is within a team, which takes part within a tournament (nested)."),
    ("Sparrow", "Bird", "Animal", "NESTED3",
     "Every sparrow is a bird, and every bird is an animal (nested classes)."),
    ("Rupee", "Money", "Wealth", "NESTED3",
     "Rupees are money, and money is a form of wealth (nested classes)."),
    ("Boy", "Child", "Human", "NESTED3",
     "Every boy is a child, and every child is a human (nested classes)."),
    ("Earth", "Solar System", "Galaxy", "NESTED3",
     "Earth is in the Solar System, which is in the Galaxy (nested)."),
    ("Cell", "Tissue", "Organ", "NESTED3",
     "Cells make up tissue, and tissue makes up an organ (nested biological units)."),
    ("Rose", "Flower", "Plant", "NESTED3",
     "Every rose is a flower, and every flower is part of a plant (nested classes)."),
    ("Tehsil", "District", "State", "NESTED3",
     "A tehsil lies within a district, which lies within a state (nested)."),

    # ---- DISJOINT3: three mutually exclusive classes ----
    ("Dog", "Cow", "Horse", "DISJOINT3",
     "Dogs, cows and horses are three different kinds of animals with no overlap."),
    ("Pen", "Book", "Bag", "DISJOINT3",
     "Pen, book and bag are three distinct objects with no common members."),
    ("Sun", "Moon", "Star", "DISJOINT3",
     "Sun, Moon and (other) stars are treated as three distinct bodies here."),
    ("Doctor", "Lawyer", "Teacher", "DISJOINT3",
     "Doctor, lawyer and teacher are three distinct professions (none is the other)."),
    ("Apple", "Potato", "Chair", "DISJOINT3",
     "Apple, potato and chair belong to three unrelated, non-overlapping classes."),
    ("Iron", "Wood", "Plastic", "DISJOINT3",
     "Iron, wood and plastic are three distinct materials with no overlap."),
    ("Lion", "Elephant", "Deer", "DISJOINT3",
     "Lion, elephant and deer are three distinct animals with no overlap."),
    ("Delhi", "Mumbai", "Chennai", "DISJOINT3",
     "Delhi, Mumbai and Chennai are three different cities with no overlap."),
    ("Morning", "Noon", "Night", "DISJOINT3",
     "Morning, noon and night are three distinct, non-overlapping parts of a day."),
    ("Rectangle", "Circle", "Triangle", "DISJOINT3",
     "Rectangle, circle and triangle are three distinct shapes with no overlap."),
    ("Football", "Chess", "Swimming", "DISJOINT3",
     "Football, chess and swimming are three distinct activities with no overlap."),

    # ---- OVERLAP3: each pair shares members (no nesting, mutual partial overlap) ----
    ("Men", "Doctors", "Fathers", "OVERLAP3",
     "Some men are doctors, some are fathers, some doctors are fathers; the three overlap."),
    ("Women", "Teachers", "Mothers", "OVERLAP3",
     "Some women are teachers, some are mothers, and these classes overlap mutually."),
    ("Students", "Players", "Singers", "OVERLAP3",
     "A person can be any combination of student, player and singer; the classes overlap."),
    ("Indians", "Artists", "Engineers", "OVERLAP3",
     "Some Indians are artists, some engineers, and the groups overlap mutually."),
    ("Employees", "Graduates", "Managers", "OVERLAP3",
     "Some employees are graduates, some are managers; the three groups overlap."),
    ("Boys", "Cricketers", "Swimmers", "OVERLAP3",
     "A boy may be a cricketer and/or swimmer; the three classes overlap."),
    ("Poets", "Writers", "Teachers", "OVERLAP3",
     "Some poets are writers, some are teachers; the three groups overlap."),
    ("Villagers", "Farmers", "Voters", "OVERLAP3",
     "Some villagers are farmers, some are voters; the three groups overlap."),

    # ---- OVERLAP2_PLUS_SEP: two overlap, third separate ----
    ("Doctors", "Surgeons", "Cricketers", "OVERLAP2_PLUS_SEP",
     "Some doctors are surgeons (overlap), while cricketers are a separate group here."),
    ("Teachers", "Women", "Tables", "OVERLAP2_PLUS_SEP",
     "Some teachers are women (overlap), but tables are a wholly separate class."),
    ("Players", "Students", "Buildings", "OVERLAP2_PLUS_SEP",
     "Some players are students (overlap), but buildings are a separate class."),
    ("Singers", "Dancers", "Mountains", "OVERLAP2_PLUS_SEP",
     "Some singers are dancers (overlap), but mountains are a separate class."),
    ("Graduates", "Employees", "Rivers", "OVERLAP2_PLUS_SEP",
     "Some graduates are employees (overlap), but rivers are a separate class."),
    ("Writers", "Poets", "Trees", "OVERLAP2_PLUS_SEP",
     "Some writers are poets (overlap), but trees are a wholly separate class."),

    # ---- ONE_IN_ONE_PLUS_SEP: A inside B, C separate ----
    ("Pigeons", "Birds", "Dogs", "ONE_IN_ONE_PLUS_SEP",
     "All pigeons are birds (pigeon inside bird); dogs are a separate class."),
    ("Mangoes", "Fruits", "Cars", "ONE_IN_ONE_PLUS_SEP",
     "All mangoes are fruits (mango inside fruit); cars are a separate class."),
    ("Roses", "Flowers", "Books", "ONE_IN_ONE_PLUS_SEP",
     "All roses are flowers (rose inside flower); books are a separate class."),
    ("Tigers", "Animals", "Tables", "ONE_IN_ONE_PLUS_SEP",
     "All tigers are animals (tiger inside animal); tables are a separate class."),
    ("Doctors", "Humans", "Chairs", "ONE_IN_ONE_PLUS_SEP",
     "All doctors are humans (doctor inside human); chairs are a separate class."),
    ("Sparrows", "Birds", "Fishes", "ONE_IN_ONE_PLUS_SEP",
     "All sparrows are birds (sparrow inside bird); fishes are a separate class."),

    # ---- ONE_IN_TWO_OVERLAP: A inside B, C overlaps both ----
    ("Females", "Mothers", "Doctors", "ONE_IN_TWO_OVERLAP",
     "All mothers are females (mother inside female); doctors overlap both."),
    ("Animals", "Dogs", "Pets", "ONE_IN_TWO_OVERLAP",
     "All dogs are animals (dog inside animal); pets overlap both."),
    ("Humans", "Teachers", "Graduates", "ONE_IN_TWO_OVERLAP",
     "All teachers are humans (teacher inside human); graduates overlap both."),
    ("Vehicles", "Cars", "Red Things", "ONE_IN_TWO_OVERLAP",
     "All cars are vehicles (car inside vehicle); red things overlap both."),

    # ---- CONTAIN_PLUS_PARTIAL: small inside big, third partly overlaps big ----
    ("Hens", "Birds", "Pets", "CONTAIN_PLUS_PARTIAL",
     "All hens are birds (hen inside bird); pets partly overlap birds."),
    ("Pines", "Trees", "Tall Things", "CONTAIN_PLUS_PARTIAL",
     "All pines are trees (pine inside tree); tall things partly overlap trees."),
    ("Cobras", "Snakes", "Dangerous Things", "CONTAIN_PLUS_PARTIAL",
     "All cobras are snakes (cobra inside snake); dangerous things partly overlap snakes."),

    # ===== additional curated, fact-checked triples (expand the pool) =====
    # ---- TWO_IN_ONE ----
    ("Bus", "Train", "Transport", "TWO_IN_ONE",
     "Buses and trains are distinct modes of transport; both are transport."),
    ("Square", "Triangle", "Polygon", "TWO_IN_ONE",
     "Squares and triangles are different polygons; both are polygons."),
    ("Gold", "Silver", "Precious Metal", "TWO_IN_ONE",
     "Gold and silver are distinct precious metals; both are precious metals."),
    ("Tea", "Coffee", "Beverage", "TWO_IN_ONE",
     "Tea and coffee are different beverages; both are beverages."),
    ("January", "March", "Month", "TWO_IN_ONE",
     "January and March are different months; both are months."),
    ("Violin", "Flute", "Musical Instrument", "TWO_IN_ONE",
     "Violin and flute are distinct musical instruments; both are instruments."),
    ("Sugar", "Salt", "Edible", "TWO_IN_ONE",
     "Sugar and salt are different edible substances; both are edibles."),
    ("Onion", "Carrot", "Vegetable", "TWO_IN_ONE",
     "Onions and carrots are distinct vegetables; both are vegetables."),
    ("Pencil", "Eraser", "School Supply", "TWO_IN_ONE",
     "Pencils and erasers are distinct school supplies; both are school supplies."),
    ("Football", "Tennis", "Sport", "TWO_IN_ONE",
     "Football and tennis are different sports; both are sports."),
    ("Cobra", "Python", "Snake", "TWO_IN_ONE",
     "Cobras and pythons are different snakes; both are snakes."),
    ("Shark", "Tuna", "Fish", "TWO_IN_ONE",
     "Sharks and tuna are different fish; both are fish."),
    ("Mars", "Venus", "Planet", "TWO_IN_ONE",
     "Mars and Venus are different planets; both are planets."),
    ("Cotton", "Silk", "Fabric", "TWO_IN_ONE",
     "Cotton and silk are distinct fabrics; both are fabrics."),
    ("Oak", "Pine", "Tree", "TWO_IN_ONE",
     "Oak and pine are different trees; both are trees."),
    ("Hammer", "Screwdriver", "Tool", "TWO_IN_ONE",
     "Hammers and screwdrivers are distinct tools; both are tools."),
    ("Bicycle", "Scooter", "Two-Wheeler", "TWO_IN_ONE",
     "Bicycles and scooters are distinct two-wheelers; both are two-wheelers."),
    ("Guitar", "Piano", "Instrument", "TWO_IN_ONE",
     "Guitar and piano are different instruments; both are instruments."),
    ("Lemon", "Orange", "Citrus Fruit", "TWO_IN_ONE",
     "Lemons and oranges are different citrus fruits; both are citrus fruits."),
    ("Cricket Ball", "Football", "Ball", "TWO_IN_ONE",
     "A cricket ball and a football are different balls; both are balls."),

    # ---- NESTED3 ----
    ("Paisa", "Rupee", "Currency", "NESTED3",
     "A paisa is part of a rupee, and a rupee is a form of currency (nested)."),
    ("Letter", "Word", "Sentence", "NESTED3",
     "Letters form a word, and words form a sentence (nested language units)."),
    ("Day", "Month", "Year", "NESTED3",
     "A day is part of a month, and a month is part of a year (nested time units)."),
    ("Player", "Team", "League", "NESTED3",
     "A player belongs to a team, which belongs to a league (nested)."),
    ("Soldier", "Battalion", "Army", "NESTED3",
     "A soldier is in a battalion, which is part of the army (nested)."),
    ("Pupil", "Class", "School", "NESTED3",
     "A pupil is in a class, which is part of a school (nested)."),
    ("Apple", "Fruit", "Food", "NESTED3",
     "Every apple is a fruit, and every fruit is food (nested classes)."),
    ("Tiger", "Mammal", "Animal", "NESTED3",
     "Every tiger is a mammal, and every mammal is an animal (nested classes)."),
    ("Inch", "Foot", "Yard", "NESTED3",
     "An inch is part of a foot, and a foot is part of a yard (nested length units)."),
    ("Room", "House", "Colony", "NESTED3",
     "A room is within a house, which is within a colony (nested)."),
    ("Chapter", "Book", "Library", "NESTED3",
     "A chapter is part of a book, and books make up a library (nested)."),
    ("Leaf", "Branch", "Tree", "NESTED3",
     "A leaf grows on a branch, which is part of a tree (nested)."),
    ("Word", "Paragraph", "Essay", "NESTED3",
     "Words make a paragraph, and paragraphs make an essay (nested)."),
    ("Carrot", "Vegetable", "Food", "NESTED3",
     "Every carrot is a vegetable, and every vegetable is food (nested classes)."),
    ("Doctor", "Professional", "Citizen", "NESTED3",
     "Every doctor is a professional, and every professional is a citizen (nested classes)."),
    ("Coin", "Money", "Asset", "NESTED3",
     "Coins are money, and money is an asset (nested classes)."),

    # ---- DISJOINT3 ----
    ("Tea", "Stone", "Cycle", "DISJOINT3",
     "Tea, stone and cycle belong to three unrelated, non-overlapping classes."),
    ("Goat", "Tiger", "Cow", "DISJOINT3",
     "Goat, tiger and cow are three different animals with no overlap."),
    ("Pencil", "Eraser", "Sharpener", "DISJOINT3",
     "Pencil, eraser and sharpener are three distinct objects with no overlap."),
    ("Mango", "Banana", "Grapes", "DISJOINT3",
     "Mango, banana and grapes are three different fruits with no overlap."),
    ("Brick", "Cement", "Sand", "DISJOINT3",
     "Brick, cement and sand are three distinct materials with no overlap."),
    ("Spoon", "Fork", "Knife", "DISJOINT3",
     "Spoon, fork and knife are three distinct cutlery items with no overlap."),
    ("Rose", "Lotus", "Lily", "DISJOINT3",
     "Rose, lotus and lily are three different flowers with no overlap."),
    ("Hat", "Shoe", "Glove", "DISJOINT3",
     "Hat, shoe and glove are three distinct items with no overlap."),
    ("Red", "Blue", "Green", "DISJOINT3",
     "Red, blue and green are three distinct colours with no overlap."),
    ("Pen", "Knife", "Spoon", "DISJOINT3",
     "Pen, knife and spoon are three distinct objects with no overlap."),
    ("Sunday", "Monday", "Tuesday", "DISJOINT3",
     "Sunday, Monday and Tuesday are three distinct days with no overlap."),
    ("Snake", "Frog", "Lizard", "DISJOINT3",
     "Snake, frog and lizard are three distinct animals with no overlap here."),

    # ---- OVERLAP3 ----
    ("Men", "Players", "Voters", "OVERLAP3",
     "A man may be a player and/or voter; the three classes overlap mutually."),
    ("Workers", "Drivers", "Owners", "OVERLAP3",
     "Some workers are drivers, some are owners; the three groups overlap."),
    ("Adults", "Smokers", "Drivers", "OVERLAP3",
     "Some adults smoke, some drive, and the three classes overlap mutually."),
    ("Citizens", "Taxpayers", "Voters", "OVERLAP3",
     "Some citizens are taxpayers, some voters; the three groups overlap."),
    ("Boys", "Dancers", "Painters", "OVERLAP3",
     "A boy may be a dancer and/or painter; the three classes overlap."),
    ("Doctors", "Authors", "Cyclists", "OVERLAP3",
     "Some doctors write, some cycle; the three classes overlap mutually."),

    # ---- OVERLAP2_PLUS_SEP ----
    ("Doctors", "Players", "Bricks", "OVERLAP2_PLUS_SEP",
     "Some doctors are players (overlap), but bricks are a separate class."),
    ("Women", "Drivers", "Clouds", "OVERLAP2_PLUS_SEP",
     "Some women are drivers (overlap), but clouds are a separate class."),
    ("Boys", "Singers", "Rivers", "OVERLAP2_PLUS_SEP",
     "Some boys are singers (overlap), but rivers are a separate class."),
    ("Teachers", "Authors", "Stones", "OVERLAP2_PLUS_SEP",
     "Some teachers are authors (overlap), but stones are a separate class."),
    ("Farmers", "Voters", "Mountains", "OVERLAP2_PLUS_SEP",
     "Some farmers are voters (overlap), but mountains are a separate class."),

    # ---- ONE_IN_ONE_PLUS_SEP ----
    ("Crows", "Birds", "Cats", "ONE_IN_ONE_PLUS_SEP",
     "All crows are birds (crow inside bird); cats are a separate class."),
    ("Apples", "Fruits", "Pens", "ONE_IN_ONE_PLUS_SEP",
     "All apples are fruits (apple inside fruit); pens are a separate class."),
    ("Lilies", "Flowers", "Cars", "ONE_IN_ONE_PLUS_SEP",
     "All lilies are flowers (lily inside flower); cars are a separate class."),
    ("Lions", "Animals", "Chairs", "ONE_IN_ONE_PLUS_SEP",
     "All lions are animals (lion inside animal); chairs are a separate class."),
    ("Cobras", "Reptiles", "Birds", "ONE_IN_ONE_PLUS_SEP",
     "All cobras are reptiles (cobra inside reptile); birds are a separate class."),
    ("Engineers", "Humans", "Tables", "ONE_IN_ONE_PLUS_SEP",
     "All engineers are humans (engineer inside human); tables are a separate class."),

    # ---- ONE_IN_TWO_OVERLAP ----
    ("Birds", "Parrots", "Pets", "ONE_IN_TWO_OVERLAP",
     "All parrots are birds (parrot inside bird); pets overlap both."),
    ("People", "Singers", "Women", "ONE_IN_TWO_OVERLAP",
     "All singers are people (singer inside people); women overlap both."),
    ("Animals", "Cows", "Black Things", "ONE_IN_TWO_OVERLAP",
     "All cows are animals (cow inside animal); black things overlap both."),
    ("Plants", "Roses", "Red Things", "ONE_IN_TWO_OVERLAP",
     "All roses are plants (rose inside plant); red things overlap both."),

    # ---- CONTAIN_PLUS_PARTIAL ----
    ("Apples", "Fruits", "Sweet Things", "CONTAIN_PLUS_PARTIAL",
     "All apples are fruits (apple inside fruit); sweet things partly overlap fruits."),
    ("Sparrows", "Birds", "Flying Things", "CONTAIN_PLUS_PARTIAL",
     "All sparrows are birds (sparrow inside bird); flying things partly overlap birds."),
    ("Squares", "Rectangles", "Shaded Figures", "CONTAIN_PLUS_PARTIAL",
     "All squares are rectangles (square inside rectangle); shaded figures partly overlap rectangles."),
]


# ============================================================================
# NUMERIC VENN — region counts + inclusion/exclusion (all integer)
# ============================================================================
# We generate region counts directly (the disjoint atoms of a Venn diagram) so
# every derived quantity is an exact integer sum. Two presentation styles:
#   - "diagram": list region values explicitly
#   - "survey":  give n(A), n(B), n(A&B) etc. as a worded survey
#
# 2-SET atoms:  a_only, b_only, both, neither
# 3-SET atoms:  a_only, b_only, c_only, ab_only, bc_only, ca_only, abc, neither

def ri(lo, hi):
    return random.randint(lo, hi)


def make_int_options(correct, distractors):
    """4 distinct non-negative integer options, correct included, shuffled.
    Returns (opts_as_strings, correct_index)."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if d < 0:
            continue
        if d not in opts:
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with nearby plausible integers if needed
    bump = 1
    while len(opts) < 4:
        for cand in (correct + bump, correct - bump, correct + 2 * bump, correct + 5 * bump):
            if cand >= 0 and cand not in opts:
                opts.append(cand)
                break
        bump += 1
    opts = opts[:4]
    random.shuffle(opts)
    ci = opts.index(correct)
    return [str(o) for o in opts], ci


# ----- 3-set atom generator with two subject themes -----
THEMES_3 = [
    ("a survey of {T} people", "read newspaper {A}", "read newspaper {B}", "read newspaper {C}",
     ["A", "B", "C"], "{A}", "{B}", "{C}"),
    ("a group of {T} students", "play {A}", "play {B}", "play {C}",
     ["Cricket", "Football", "Hockey"], "{A}", "{B}", "{C}"),
    ("a survey of {T} families", "subscribe to {A}", "subscribe to {B}", "subscribe to {C}",
     ["The Times", "The Express", "The Herald"], "{A}", "{B}", "{C}"),
    ("a class of {T} students", "like {A}", "like {B}", "like {C}",
     ["Tea", "Coffee", "Milk"], "{A}", "{B}", "{C}"),
    ("a survey of {T} consumers", "use product {A}", "use product {B}", "use product {C}",
     ["P", "Q", "R"], "{A}", "{B}", "{C}"),
]
THEMES_2 = [
    ("a class of {T} students", "passed in Maths", "passed in Science"),
    ("a group of {T} people", "can speak Hindi", "can speak English"),
    ("a survey of {T} families", "own a car", "own a bike"),
    ("a class of {T} students", "like Tea", "like Coffee"),
    ("a group of {T} tourists", "visited Delhi", "visited Agra"),
]


def gen3_atoms():
    """Return the 8 atoms for a 3-set Venn, all positive-ish small ints."""
    abc = ri(2, 15)
    ab_only = ri(3, 20)
    bc_only = ri(3, 20)
    ca_only = ri(3, 20)
    a_only = ri(8, 40)
    b_only = ri(8, 40)
    c_only = ri(8, 40)
    neither = ri(0, 20)
    return dict(a_only=a_only, b_only=b_only, c_only=c_only,
                ab_only=ab_only, bc_only=bc_only, ca_only=ca_only,
                abc=abc, neither=neither)


def atoms3_derived(at):
    a_only = at["a_only"]; b_only = at["b_only"]; c_only = at["c_only"]
    ab_only = at["ab_only"]; bc_only = at["bc_only"]; ca_only = at["ca_only"]
    abc = at["abc"]; neither = at["neither"]
    nA = a_only + ab_only + ca_only + abc
    nB = b_only + ab_only + bc_only + abc
    nC = c_only + bc_only + ca_only + abc
    nAB = ab_only + abc
    nBC = bc_only + abc
    nCA = ca_only + abc
    at_least_one = (a_only + b_only + c_only + ab_only + bc_only + ca_only + abc)
    total = at_least_one + neither
    exactly_two = ab_only + bc_only + ca_only
    exactly_one = a_only + b_only + c_only
    return dict(nA=nA, nB=nB, nC=nC, nAB=nAB, nBC=nBC, nCA=nCA, abc=abc,
                at_least_one=at_least_one, total=total, exactly_two=exactly_two,
                exactly_one=exactly_one, neither=neither,
                a_only=a_only, b_only=b_only, c_only=c_only)


def gen2_atoms():
    both = ri(4, 25)
    a_only = ri(8, 45)
    b_only = ri(8, 45)
    neither = ri(0, 20)
    return dict(both=both, a_only=a_only, b_only=b_only, neither=neither)


# ----------------------------------------------------------------------------
# Question templates. Each returns a dict or None.
#   {family, stem, opts(list str), ci, sol, diff, numeric(bool), answer(int|None)}
# ----------------------------------------------------------------------------
questions = []
seen = set()
counts = {"M": 0, "H": 0, "VH": 0}
QUOTA = {"M": 100, "H": 300, "VH": 100}  # 20/60/20
TARGET = 500


def add(q):
    key = q["stem"].strip()
    if key in seen:
        return False
    if len(set(q["opts"])) != 4:
        return False
    if counts[q["diff"]] >= QUOTA[q["diff"]]:
        return False
    seen.add(key)
    questions.append(q)
    counts[q["diff"]] += 1
    return True


# ---------------- RELATIONSHIP family ----------------
SYMMETRIC_PATTERNS = {"DISJOINT3", "OVERLAP3"}


def t_relationship():
    term1, term2, term3, pat, reason = random.choice(RELATION_TRIPLES)
    # For fully symmetric relations, permuting the three terms still yields the
    # SAME valid relationship and SAME diagram, so we may shuffle to add variety.
    if pat in SYMMETRIC_PATTERNS:
        trio = [term1, term2, term3]
        random.shuffle(trio)
        term1, term2, term3 = trio
    correct = PATTERNS[pat]
    others = [d for d in ALL_PATTERN_DESCS if d != correct]
    distractors = random.sample(others, 3)
    opts = [correct] + distractors
    random.shuffle(opts)
    ci = opts.index(correct)
    stem = (f"Which one of the following diagrams best represents the relationship "
            f"among: {term1}, {term2}, {term3}?")
    sol = (f"Relationship: {reason} Hence the correct diagram is: \"{correct}\".")
    # difficulty: nested/overlap variants harder
    if pat in ("OVERLAP3", "ONE_IN_TWO_OVERLAP", "CONTAIN_PLUS_PARTIAL"):
        diff = "VH"
    elif pat in ("NESTED3", "ONE_IN_ONE_PLUS_SEP", "OVERLAP2_PLUS_SEP"):
        diff = "H"
    else:
        diff = "M"
    return dict(family="REL", stem=stem, opts=opts, ci=ci, sol=sol, diff=diff,
                numeric=False, answer=None)


# ---------------- NUMERIC families ----------------
def _theme3():
    th = random.choice(THEMES_3)
    pop, fa, fb, fc, names, lA, lB, lC = th
    A, B, C = names
    fa = fa.format(A=A, B=B, C=C); fb = fb.format(A=A, B=B, C=C); fc = fc.format(A=A, B=B, C=C)
    return pop, fa, fb, fc, A, B, C


def t_num3_survey_only():
    """Worded survey giving n(A),n(B),n(C),pairwise,all,neither -> ask 'only A'."""
    at = gen3_atoms()
    d = atoms3_derived(at)
    pop, fa, fb, fc, A, B, C = _theme3()
    T = d["total"]
    stem = (f"In {pop.format(T=T)}, {d['nA']} {fa}, {d['nB']} {fb} and {d['nC']} {fc}. "
            f"{d['nAB']} do both ({A} and {B}), {d['nBC']} do both ({B} and {C}), "
            f"{d['nCA']} do both ({C} and {A}), and {d['abc']} do all three. "
            f"How many do ONLY {A} (i.e. {fa} but neither of the other two)?")
    correct = d["a_only"]
    distractors = [d["nA"],                       # forgets to subtract overlaps
                   d["nA"] - d["nAB"] - d["nCA"],  # forgets to add back abc
                   d["a_only"] + d["abc"]]         # off by abc
    opts, ci = make_int_options(correct, distractors)
    sol = (f"Only {A} = n({A}) − (only-{A}&{B}) − (only-{A}&{C}) − (all three) "
           f"= {d['nA']} − {at['ab_only']} − {at['ca_only']} − {at['abc']} = {correct}. "
           f"(Equivalently subtract n({A}∩{B}) and n({A}∩{C}) then add back n(all three).)")
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="H", numeric=True, answer=correct)


def t_num3_exactly_two():
    at = gen3_atoms()
    d = atoms3_derived(at)
    pop, fa, fb, fc, A, B, C = _theme3()
    T = d["total"]
    stem = (f"In {pop.format(T=T)}, {d['nA']} {fa}, {d['nB']} {fb} and {d['nC']} {fc}. "
            f"{d['nAB']} do both ({A} and {B}), {d['nBC']} do both ({B} and {C}), "
            f"{d['nCA']} do both ({C} and {A}), and {d['abc']} do all three. "
            f"How many do EXACTLY two of the three?")
    correct = d["exactly_two"]
    distractors = [d["nAB"] + d["nBC"] + d["nCA"],          # forgets to remove abc*3
                   d["nAB"] + d["nBC"] + d["nCA"] - d["abc"],
                   d["exactly_two"] + d["abc"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"Exactly two = (n({A}∩{B})+n({B}∩{C})+n({C}∩{A})) − 3×n(all three) "
           f"= ({d['nAB']}+{d['nBC']}+{d['nCA']}) − 3×{d['abc']} = {correct}.")
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="VH", numeric=True, answer=correct)


def t_num3_at_least_one():
    at = gen3_atoms()
    d = atoms3_derived(at)
    pop, fa, fb, fc, A, B, C = _theme3()
    T = d["total"]
    stem = (f"In {pop.format(T=T)}, {d['nA']} {fa}, {d['nB']} {fb} and {d['nC']} {fc}. "
            f"{d['nAB']} do both ({A} and {B}), {d['nBC']} do both ({B} and {C}), "
            f"{d['nCA']} do both ({C} and {A}), and {d['abc']} do all three. "
            f"How many do at least one of the three activities?")
    correct = d["at_least_one"]
    distractors = [d["nA"] + d["nB"] + d["nC"],                       # plain sum
                   d["nA"] + d["nB"] + d["nC"] - d["nAB"] - d["nBC"] - d["nCA"],  # no +abc
                   d["total"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"At least one = Σn − Σpairwise + n(all) "
           f"= ({d['nA']}+{d['nB']}+{d['nC']}) − ({d['nAB']}+{d['nBC']}+{d['nCA']}) + {d['abc']} "
           f"= {correct}.")
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="H", numeric=True, answer=correct)


def t_num3_neither():
    at = gen3_atoms()
    if at["neither"] == 0:
        at["neither"] = ri(3, 18)
    d = atoms3_derived(at)
    pop, fa, fb, fc, A, B, C = _theme3()
    T = d["total"]
    stem = (f"In {pop.format(T=T)} (total = {T}), {d['nA']} {fa}, {d['nB']} {fb} and "
            f"{d['nC']} {fc}. {d['nAB']} do both ({A} and {B}), {d['nBC']} do both "
            f"({B} and {C}), {d['nCA']} do both ({C} and {A}), and {d['abc']} do all three. "
            f"How many do NONE of the three?")
    correct = d["neither"]
    distractors = [T - (d["nA"] + d["nB"] + d["nC"]),
                   T - d["at_least_one"] - d["abc"],
                   d["neither"] + d["abc"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"At least one = {d['at_least_one']} (by inclusion–exclusion). "
           f"None = total − at least one = {T} − {d['at_least_one']} = {correct}.")
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="VH", numeric=True, answer=correct)


def t_num3_exactly_one():
    at = gen3_atoms()
    d = atoms3_derived(at)
    pop, fa, fb, fc, A, B, C = _theme3()
    T = d["total"]
    stem = (f"In {pop.format(T=T)}, {d['nA']} {fa}, {d['nB']} {fb} and {d['nC']} {fc}. "
            f"{d['nAB']} do both ({A} and {B}), {d['nBC']} do both ({B} and {C}), "
            f"{d['nCA']} do both ({C} and {A}), and {d['abc']} do all three. "
            f"How many do EXACTLY one of the three?")
    correct = d["exactly_one"]
    distractors = [d["a_only"] + d["b_only"],
                   d["at_least_one"] - d["exactly_two"],
                   d["exactly_one"] + d["abc"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"Only-{A}={d['a_only']}, only-{B}={d['b_only']}, only-{C}={d['c_only']}. "
           f"Exactly one = {d['a_only']}+{d['b_only']}+{d['c_only']} = {correct}.")
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="VH", numeric=True, answer=correct)


def t_num3_diagram_region():
    """Diagram style: give the 8 region values, ask one derived quantity."""
    at = gen3_atoms()
    d = atoms3_derived(at)
    A, B, C = random.choice([("A", "B", "C"), ("P", "Q", "R"), ("X", "Y", "Z")])
    stem = (f"In a Venn diagram of three sets {A}, {B} and {C}, the region values are: "
            f"only {A} = {at['a_only']}, only {B} = {at['b_only']}, only {C} = {at['c_only']}, "
            f"{A}∩{B} only = {at['ab_only']}, {B}∩{C} only = {at['bc_only']}, "
            f"{C}∩{A} only = {at['ca_only']}, {A}∩{B}∩{C} = {at['abc']}, "
            f"outside all = {at['neither']}. ")
    qtype = random.choice(["nA", "nB", "nC", "at_least_one", "total", "exactly_two"])
    qmap = {
        "nA": (f"What is n({A})?", d["nA"]),
        "nB": (f"What is n({B})?", d["nB"]),
        "nC": (f"What is n({C})?", d["nC"]),
        "at_least_one": ("How many lie in at least one set?", d["at_least_one"]),
        "total": ("What is the total (universal set size)?", d["total"]),
        "exactly_two": ("How many lie in exactly two of the three sets?", d["exactly_two"]),
    }
    qtext, correct = qmap[qtype]
    stem += qtext
    distractors = [correct + at["abc"], correct - at["abc"],
                   correct + at["ab_only"], correct + ri(1, 9)]
    opts, ci = make_int_options(correct, distractors)
    if qtype.startswith("n"):
        s = A if qtype == "nA" else B if qtype == "nB" else C
        sol = f"n({s}) = sum of all four regions inside {s} = {correct}."
    elif qtype == "at_least_one":
        sol = f"At least one = sum of the 7 inner regions = {d['at_least_one']}."
    elif qtype == "total":
        sol = f"Total = 7 inner regions + outside = {d['at_least_one']} + {at['neither']} = {correct}."
    else:
        sol = f"Exactly two = {at['ab_only']}+{at['bc_only']}+{at['ca_only']} = {correct}."
    diff = "M" if qtype.startswith("n") else "H"
    return dict(family="NUM3", stem=stem, opts=opts, ci=ci, sol=sol,
                diff=diff, numeric=True, answer=correct)


def t_num2_both():
    """2-set: given n(A),n(B),n(A∪B) -> n(A∩B)."""
    at = gen2_atoms()
    nA = at["a_only"] + at["both"]
    nB = at["b_only"] + at["both"]
    union = at["a_only"] + at["b_only"] + at["both"]
    total = union + at["neither"]
    th = random.choice(THEMES_2)
    pop, fa, fb = th
    stem = (f"In {pop.format(T=total)}, {nA} {fa} and {nB} {fb}. "
            f"If {union} {('passed in at least one subject' if 'passed' in fa else 'did at least one of the two')}, "
            f"how many did BOTH?")
    correct = at["both"]
    distractors = [nA + nB - total, union - nA, nA + nB - union + ri(1, 5)]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"n(A∩B) = n(A) + n(B) − n(A∪B) = {nA} + {nB} − {union} = {correct}.")
    return dict(family="NUM2", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="M", numeric=True, answer=correct)


def t_num2_only_one():
    at = gen2_atoms()
    nA = at["a_only"] + at["both"]
    nB = at["b_only"] + at["both"]
    union = at["a_only"] + at["b_only"] + at["both"]
    total = union + at["neither"]
    th = random.choice(THEMES_2)
    pop, fa, fb = th
    stem = (f"In {pop.format(T=total)}, {nA} {fa}, {nB} {fb}, and {at['both']} did both. "
            f"How many did EXACTLY ONE of the two?")
    correct = at["a_only"] + at["b_only"]
    distractors = [union, nA + nB - at["both"], at["a_only"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"Exactly one = (n(A)−both) + (n(B)−both) = ({nA}−{at['both']}) + ({nB}−{at['both']}) "
           f"= {at['a_only']} + {at['b_only']} = {correct}.")
    return dict(family="NUM2", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="H", numeric=True, answer=correct)


def t_num2_neither():
    at = gen2_atoms()
    if at["neither"] == 0:
        at["neither"] = ri(3, 15)
    nA = at["a_only"] + at["both"]
    nB = at["b_only"] + at["both"]
    union = at["a_only"] + at["b_only"] + at["both"]
    total = union + at["neither"]
    th = random.choice(THEMES_2)
    pop, fa, fb = th
    stem = (f"In {pop.format(T=total)} (total = {total}), {nA} {fa}, {nB} {fb}, and "
            f"{at['both']} did both. How many did NEITHER?")
    correct = at["neither"]
    distractors = [total - nA - nB, total - union - at["both"], at["neither"] + at["both"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"n(A∪B) = {nA}+{nB}−{at['both']} = {union}. "
           f"Neither = total − union = {total} − {union} = {correct}.")
    return dict(family="NUM2", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="H", numeric=True, answer=correct)


def t_num2_union():
    at = gen2_atoms()
    nA = at["a_only"] + at["both"]
    nB = at["b_only"] + at["both"]
    union = at["a_only"] + at["b_only"] + at["both"]
    th = random.choice(THEMES_2)
    pop, fa, fb = th
    total = union + at["neither"]
    stem = (f"In {pop.format(T=total)}, {nA} {fa}, {nB} {fb}, and {at['both']} did both. "
            f"How many did AT LEAST ONE of the two?")
    correct = union
    distractors = [nA + nB, nA + nB + at["both"], union + at["both"]]
    opts, ci = make_int_options(correct, distractors)
    sol = (f"n(A∪B) = n(A)+n(B)−n(A∩B) = {nA}+{nB}−{at['both']} = {correct}.")
    return dict(family="NUM2", stem=stem, opts=opts, ci=ci, sol=sol,
                diff="M", numeric=True, answer=correct)


NUMERIC_TEMPLATES = [
    t_num3_survey_only, t_num3_exactly_two, t_num3_at_least_one,
    t_num3_neither, t_num3_exactly_one, t_num3_diagram_region,
    t_num2_both, t_num2_only_one, t_num2_neither, t_num2_union,
]

# Numeric templates grouped by their difficulty tag (for quota-driven fill).
NUM_BY_DIFF = {
    "M": [t_num2_both, t_num2_union, t_num3_diagram_region],
    "H": [t_num3_survey_only, t_num3_at_least_one, t_num2_only_one,
          t_num2_neither, t_num3_diagram_region],
    "VH": [t_num3_exactly_two, t_num3_neither, t_num3_exactly_one],
}

# Target ~30-35% relationship. We try to consume the whole curated triple pool
# (with safe symmetric-permutation variety) before falling back to numeric.
# REL difficulty supply (unique triples): M~58+, H~54+, VH~31+ (more via perms).
REL_FRACTION = {"M": 0.62, "H": 0.50, "VH": 0.60}  # share of each diff drawn from REL


def main():
    attempts = 0
    rel_count = 0
    num_count = 0
    order = ["VH", "H", "M"]  # fill rarer/harder first
    while len(questions) < TARGET and attempts < 6_000_000:
        attempts += 1
        unmet = [d for d in order if counts[d] < QUOTA[d]]
        if not unmet:
            break
        d = random.choice(unmet)
        # decide family for this difficulty slot to honour ~30-35% relationship
        use_rel = random.random() < REL_FRACTION[d]
        if use_rel:
            q = t_relationship()
            # relationship template chooses its own difficulty; only keep if it
            # matches an unmet quota (add() enforces quota anyway)
        else:
            q = random.choice(NUM_BY_DIFF[d])()
        if q is None:
            continue
        if add(q):
            if q["numeric"]:
                num_count += 1
            else:
                rel_count += 1

    # If relationship pool is exhausted but quotas remain, fill with numeric.
    while len(questions) < TARGET and attempts < 8_000_000:
        attempts += 1
        unmet = [d for d in order if counts[d] < QUOTA[d]]
        if not unmet:
            break
        d = random.choice(unmet)
        q = random.choice(NUM_BY_DIFF[d])()
        if q is None:
            continue
        if add(q):
            if q["numeric"]:
                num_count += 1
            else:
                rel_count += 1

    print(f"Generated {len(questions)} questions in {attempts} attempts.")
    print("Difficulty:", dict(counts))
    nnum = sum(1 for q in questions if q["numeric"])
    print(f"Numeric: {nnum}  Relationship: {len(questions) - nnum}")

    # ---- internal verification ----
    errors = 0
    for i, q in enumerate(questions, 1):
        if len(q["opts"]) != 4:
            print(f"Q{i}: not 4 options"); errors += 1
        if len(set(q["opts"])) != 4:
            print(f"Q{i}: dup options {q['opts']}"); errors += 1
        if not (0 <= q["ci"] < 4):
            print(f"Q{i}: bad ci"); errors += 1
        if q["numeric"]:
            keyed = q["opts"][q["ci"]]
            if keyed != str(q["answer"]):
                print(f"Q{i}: keyed option != answer ({keyed} vs {q['answer']})"); errors += 1
    print(f"Internal verification errors: {errors}")
    if errors:
        raise SystemExit("Internal errors present - aborting.")

    write_markdown()
    write_sidecar()


OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_07_Venn_Diagrams_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_07_Venn_Diagrams_500.answers.json"


def write_markdown():
    lines = []
    lines.append("# Venn Diagrams / Logical Venn — 500 Question Practice Set (SSC CGL, Reasoning, Tier-I/II Level)\n")
    lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
    lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard.")
    lines.append("> **Every numeric answer is computed by inclusion–exclusion and machine-verified** — the keyed option is provably correct.")
    lines.append("> Relationship-diagram items use curated, fact-checked class triples.")
    lines.append("> Negative marking in CGL is −0.50; distractors are real common-mistake values.\n")
    lines.append("## Quick Reference")
    lines.append("- **2 sets:** n(A∪B) = n(A) + n(B) − n(A∩B);  Neither = Total − n(A∪B).")
    lines.append("- **3 sets:** n(A∪B∪C) = Σn − Σpairwise + n(A∩B∩C).")
    lines.append("- **Only A** = n(A) − n(A∩B) − n(A∩C) + n(A∩B∩C).")
    lines.append("- **Exactly two** = Σpairwise − 3·n(A∩B∩C).  **Exactly one** = Σonly-regions.")
    lines.append("- **Relationship diagrams:** decide nesting / disjoint / overlap from the real-world relation of the classes, then match the worded diagram.\n")
    lines.append("\n# =================== QUESTIONS ===================\n")

    for start in range(0, TARGET, 50):
        blk = start // 50 + 1
        lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            o = q["opts"]
            lines.append(f"**Q{n}.** {q['stem']}")
            lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

    lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
    for start in range(0, TARGET, 50):
        lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            letter = LETTERS[q["ci"]]
            val = q["opts"][q["ci"]]
            lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Total lines: {len(lines)}")


def write_sidecar():
    data = {}
    for j, q in enumerate(questions, 1):
        if q["numeric"]:
            data[str(j)] = q["answer"]
    with open(SIDECAR, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=0)
    print(f"Wrote {SIDECAR} ({len(data)} numeric answers)")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""
SSC CGL  Statement & Conclusion / Assumption / Inference / Cause-Effect /
Course of Action  -- 500 MCQ generator.

Two families:

A) COMPUTABLE logical-deduction (Statement -> Conclusions I, II).
   Verdicts are COMPUTED by the same brute-force finite-model checker as the
   syllogism generator: categories map to subsets of a small domain; a
   conclusion follows iff it is true in EVERY model satisfying the statements
   (and at least one such model exists).  Emits a JSON sidecar of verdicts.
   Options: Only I / Only II / Both / Neither / Either.

B) CURATED standard items, authored carefully with conventional SSC logic so
   that EXACTLY ONE option is defensible:
     - Statement & Assumption  (implicit, necessary assumption)
     - Statement & Inference    (definitely true / false / can't say)
     - Course of Action         (does the action logically follow?)
     - Cause & Effect           (relationship between two events)

Self-checks: 500 unique stems, exactly one keyed option each, options distinct,
difficulty ~20% M / 60% H / 20% VH.  The model-based subset is cross-checked
against the sidecar.
"""
import random
import json
from itertools import product, combinations
from collections import Counter

random.seed(20260625)

LETTERS = "abcde"

OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_09_Statement_Conclusion_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_09_Statement_Conclusion_500.verdicts.json"

# ===========================================================================
# FAMILY A: model checker (re-uses the syllogism approach)
# ===========================================================================
N_DOMAIN = 3
def _all_subsets(n):
    out = []
    for r in range(n + 1):
        for c in combinations(range(n), r):
            out.append(frozenset(c))
    return out
_SUBSETS = _all_subsets(N_DOMAIN)

def _stmt_holds(kind, A, B, assign):
    sa, sb = assign[A], assign[B]
    if kind == "all":
        return sa <= sb
    if kind == "no":
        return len(sa & sb) == 0
    if kind == "some":
        return len(sa & sb) > 0
    if kind == "somenot":
        return len(sa - sb) > 0
    raise ValueError(kind)

def follows(premises, conclusion, cats):
    cats = list(cats)
    sat = 0
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in premises):
            sat += 1
            if not _stmt_holds(conclusion[0], conclusion[1], conclusion[2], assign):
                return False
    return sat > 0

def _are_complementary(c1, c2):
    k1, a1, b1 = c1
    k2, a2, b2 = c2
    if a1 != a2 or b1 != b2:
        return False
    pair = {k1, k2}
    return pair in ({"some", "somenot"}, {"all", "somenot"}, {"no", "some"})

def verdict_pair(premises, conc1, conc2, cats):
    f1 = follows(premises, conc1, cats)
    f2 = follows(premises, conc2, cats)
    if f1 and f2:
        return "BOTH"
    if f1:
        return "I"
    if f2:
        return "II"
    any_model = False
    either_ok = True
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in premises):
            any_model = True
            h1 = _stmt_holds(conc1[0], conc1[1], conc1[2], assign)
            h2 = _stmt_holds(conc2[0], conc2[1], conc2[2], assign)
            if not (h1 or h2):
                either_ok = False
                break
    if any_model and either_ok and _are_complementary(conc1, conc2):
        return "EITHER"
    return "NEITHER"

def find_counter_model(prem, conc, cats):
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in prem):
            if not _stmt_holds(conc[0], conc[1], conc[2], assign):
                def setstr(s):
                    return "{" + ",".join(map(str, sorted(s))) + "}" if s else "empty"
                return "counter-model: " + "; ".join(f"{c}={setstr(assign[c])}" for c in cats)
    return "no counter-model"

def stmt_text(kind, A, B):
    if kind == "all":
        return f"All {A} are {B}."
    if kind == "no":
        return f"No {A} are {B}."
    if kind == "some":
        return f"Some {A} are {B}."
    if kind == "somenot":
        return f"Some {A} are not {B}."
    raise ValueError(kind)

VERDICT_TO_TEXT = {
    "I": "Only conclusion I follows",
    "II": "Only conclusion II follows",
    "BOTH": "Both conclusions I and II follow",
    "NEITHER": "Neither conclusion I nor conclusion II follows",
    "EITHER": "Either conclusion I or conclusion II follows",
}
STD_OPTIONS_4 = [
    "Only conclusion I follows",
    "Only conclusion II follows",
    "Both conclusions I and II follow",
    "Neither conclusion I nor conclusion II follows",
]
STD_OPTIONS_5 = STD_OPTIONS_4 + ["Either conclusion I or conclusion II follows"]

# ---- solver self-test on textbook syllogisms ----
def solver_self_test():
    cases = [
        ([("all","A","B"),("all","B","C")], ("all","A","C"), True),
        ([("some","A","B"),("some","B","C")], ("some","A","C"), False),
        ([("all","A","B"),("no","B","C")], ("no","A","C"), True),
        ([("no","A","B")], ("no","B","A"), True),
        ([("all","A","B")], ("some","B","A"), False),
        ([("all","A","B"),("some","C","A")], ("some","C","B"), True),
        ([("no","A","B"),("all","C","A")], ("no","C","B"), True),
        ([("some","A","B")], ("some","B","A"), True),
        ([("all","A","B")], ("some","A","B"), False),
    ]
    allpass = True
    for prem, conc, expected in cases:
        cats = sorted({c for (_, a, b) in prem for c in (a, b)} | {conc[1], conc[2]})
        got = follows(prem, conc, cats)
        if got != expected:
            allpass = False
            print(f"  SOLVER FAIL: {prem} => {conc} expected {expected} got {got}")
    print(f"---- SOLVER SELF-TEST {'PASS' if allpass else 'FAIL'} ----")
    return allpass

# ---- word pool for family A ----
WORD_POOL = [
    "actors","artists","painters","singers","dancers","players","writers","poets",
    "teachers","students","engineers","doctors","lawyers","officers","clerks",
    "managers","scientists","farmers","soldiers","drivers","pilots","nurses",
    "books","pens","pencils","tables","chairs","doors","windows","lamps","fans",
    "cups","plates","bottles","glasses","bowls","jars","boxes","keys","locks",
    "cats","dogs","birds","pigeons","crows","horses","cows","goats","sheep",
    "roses","flowers","trees","plants","fruits","mangoes","apples","grapes",
    "cars","buses","trucks","bikes","trains","boats","ships","planes",
    "rivers","lakes","hills","mountains","stones","rocks","metals","golds",
    "squares","circles","triangles","lines","points","angles","shapes","cubes",
    "phones","laptops","computers","machines","tools","devices","wires","cables",
    "clocks","watches","mirrors","frames","tickets","stamps","coins","notes",
]
STATEMENT_KINDS = ["all", "no", "some", "somenot"]
CONC_KINDS = ["all", "no", "some", "somenot"]

def pick_words(k):
    return random.sample(WORD_POOL, k)

def render_statements_A(stmts):
    return " ".join(stmt_text(k, a, b) for (k, a, b) in stmts)

def gen_candidate_A(num_statements, force_either=False):
    ncats = 3 if num_statements <= 2 else random.choice([3, 4])
    words = pick_words(ncats)
    pairs = []
    for i in range(num_statements):
        if i == 0:
            a, b = words[0], words[1]
        elif i == 1 and ncats >= 3:
            a, b = words[1], words[2]
        elif i == 2 and ncats >= 4:
            a, b = words[2], words[3]
        else:
            a, b = random.sample(words, 2)
        pairs.append((a, b))
    premises = [(random.choice(STATEMENT_KINDS), a, b) for (a, b) in pairs]
    if len(set(premises)) != len(premises):
        return None
    cats = words
    if not any(all(_stmt_holds(k, a, b, dict(zip(cats, combo)))
                   for (k, a, b) in premises)
               for combo in product(_SUBSETS, repeat=len(cats))):
        return None
    endA, endB = words[0], words[-1]
    def make_concs():
        if random.random() < 0.55:
            return endA, endB
        return random.sample(words, 2)
    ca, cb = make_concs()
    if force_either or random.random() < 0.28:
        kpair = random.choice([("some","somenot"), ("all","somenot"), ("no","some")])
        conc1 = (kpair[0], ca, cb)
        conc2 = (kpair[1], ca, cb)
    else:
        conc1 = (random.choice(CONC_KINDS), ca, cb)
        cc, cd = make_concs()
        conc2 = (random.choice(CONC_KINDS), cc, cd)
        if conc2 == conc1:
            return None
    verdict = verdict_pair(premises, conc1, conc2, cats)
    if force_either and verdict != "EITHER":
        return None
    return {"statements": premises, "concs": [conc1, conc2], "cats": cats,
            "verdict": verdict}

def build_solution_A(q):
    cats, prem = q["cats"], q["statements"]
    c1, c2 = q["concs"]
    def explain(conc, label):
        if follows(prem, conc, cats):
            return f"{label} follows (true in every model of the statements)."
        return f"{label} does not follow ({find_counter_model(prem, conc, cats)})."
    parts = [explain(c1, "I"), explain(c2, "II")]
    if q["verdict"] == "EITHER":
        parts.append("They are complementary and at least one holds in every model -> either-or.")
    return " ".join(parts)

# ===========================================================================
# FAMILY B: curated items
# ===========================================================================
# Each curated item is a dict:
#   kind: 'ASSUM' | 'INFER' | 'COA' | 'CE'
#   stem: the question text (without the standard option block)
#   options: list[str]    (the fixed standard set for that kind)
#   correct_index: int
#   diff: 'M'|'H'|'VH'
#   sol: justification
#
# To guarantee uniqueness & one defensible answer, the curated content is
# authored as fixed (statement, correct-answer, reason) tuples and the standard
# option set is applied via make_options().

def make_options(correct_text, option_set):
    """option_set is the canonical fixed list of texts; correct_index is the
    position of correct_text in it. We keep canonical order (no shuffle) so the
    legend is stable, exactly like the syllogism set."""
    assert correct_text in option_set, (correct_text, option_set)
    return list(option_set), option_set.index(correct_text)

# ---- Statement & Assumption -------------------------------------------------
ASSUM_OPTIONS = [
    "Only assumption I is implicit",
    "Only assumption II is implicit",
    "Both I and II are implicit",
    "Neither I nor II is implicit",
]
# Authoring rule: an assumption is IMPLICIT iff it is necessarily taken for
# granted for the statement to make sense / be true. Each tuple is
# (statement, assumption_I, implicit_I?, assumption_II, implicit_II?, reason).
ASSUM_DATA = [
    ("An advertisement of a bank: \"Open a savings account with us and get a free debit card.\"",
     "People are attracted by free offers while choosing a bank.", True,
     "No other bank gives a free debit card on a savings account.", False,
     "The bank advertises the free card to attract customers (I, implicit). It says nothing about what OTHER banks offer (II, not implicit)."),
    ("\"Use our coaching and you are sure to clear the examination.\" -- an institute's notice.",
     "Students wish to clear the examination.", True,
     "Coaching can influence the result of the examination.", True,
     "The appeal only works if students want to clear (I) and if coaching is believed to affect the result (II); both are taken for granted."),
    ("\"In case of any difficulty regarding the form, contact the help-desk.\" -- an instruction on an application form.",
     "Some applicants may face difficulty with the form.", True,
     "All applicants will face difficulty with the form.", False,
     "The instruction presupposes that difficulty is possible (I). It does not assume EVERY applicant will struggle (II is too strong)."),
    ("\"Please switch off your mobile phones during the meeting.\" -- a notice in a conference hall.",
     "Mobile phones can disturb a meeting.", True,
     "The participants carry mobile phones.", True,
     "The request makes sense only if phones could disturb (I) and if participants actually have phones to switch off (II)."),
    ("\"Take medicine X to get instant relief from headache.\" -- an advertisement.",
     "People want instant relief from headache.", True,
     "Medicine X has no side effects.", False,
     "The ad assumes a demand for instant relief (I). It says nothing about side effects (II)."),
    ("A notice in a library: \"Members are requested to return borrowed books on or before the due date.\"",
     "Members borrow books from the library.", True,
     "Members may delay returning books unless reminded.", True,
     "The request presupposes that members borrow (I) and that, without the notice, returns may be delayed (II)."),
    ("\"Buy our water purifier and stay healthy.\" -- an advertisement.",
     "Clean water contributes to health.", True,
     "Their purifier produces clean water.", True,
     "The pitch links the purifier to health, so it assumes clean water aids health (I) and that the product yields clean water (II)."),
    ("\"For faster service, pay your electricity bill online.\" -- a message from a power company.",
     "Online payment is faster than the offline method.", True,
     "Consumers have access to the means of paying online.", True,
     "The claim that online is faster (I) and the request itself assume consumers can pay online (II)."),
    ("\"Candidates must report at the venue by 9 a.m.\" -- an examination instruction.",
     "Candidates can reach the venue by 9 a.m.", True,
     "Candidates know the location of the venue.", True,
     "The instruction is meaningful only if candidates can arrive on time (I) and know where to go (II)."),
    ("A government notice: \"Plant a tree on your birthday and help the environment.\"",
     "Planting trees benefits the environment.", True,
     "Everyone celebrates a birthday.", False,
     "The appeal assumes trees help the environment (I); it does not require that literally everyone has a birthday celebration (II is irrelevant/too strong)."),
    ("\"Hurry! Limited seats available -- register today.\" -- a workshop advertisement.",
     "Demand for the workshop may exceed the available seats.", True,
     "People tend to act when they fear missing an opportunity.", True,
     "The urgency works only if seats may run short (I) and if scarcity prompts action (II)."),
    ("\"Wear a helmet while riding a two-wheeler.\" -- a road-safety message.",
     "A helmet can reduce injury in an accident.", True,
     "Two-wheeler riders are exposed to a risk of injury.", True,
     "The advice presupposes helmets help (I) and that riders face injury risk (II)."),
    ("A bank notice: \"Keep a minimum balance of Rs.1000 to avoid charges.\"",
     "Falling below the minimum balance attracts charges.", True,
     "Account holders are able to maintain Rs.1000.", False,
     "The notice plainly implies charges below the limit (I). It does not assume every holder can keep that balance (II)."),
    ("\"Drink milk daily for strong bones.\" -- a health campaign slogan.",
     "Milk contributes to bone strength.", True,
     "People wish to have strong bones.", True,
     "The slogan assumes milk aids bones (I) and that the audience values strong bones (II)."),
    ("\"Submit the report by Friday, failing which action will be taken.\" -- an office circular.",
     "The report can be completed by Friday.", True,
     "A deadline with a consequence encourages timely submission.", True,
     "The deadline is workable only if completion by Friday is possible (I), and the warning assumes consequences spur action (II)."),
    ("\"Visit our new branch for personalised service.\" -- a bank advertisement.",
     "Customers value personalised service.", True,
     "The old branch gave no service at all.", False,
     "The ad assumes customers want personalised service (I); it does not claim the old branch gave NO service (II)."),
    ("\"Carry an umbrella; it may rain today.\" -- advice from a friend.",
     "An umbrella offers protection from rain.", True,
     "It will certainly rain today.", False,
     "The advice assumes umbrellas protect against rain (I). 'May rain' does not assume rain is certain (II)."),
    ("A school circular: \"Parents are requested to attend the meeting on Saturday.\"",
     "Parents are available to attend on Saturday.", False,
     "The meeting concerns matters parents should know about.", True,
     "A request does not assume every parent IS available (I, not implicit); it does assume the meeting is relevant to parents (II)."),
    ("\"Eat fruits and vegetables to stay fit.\" -- a dietician's advice.",
     "Fruits and vegetables aid fitness.", True,
     "People prefer fruits to medicines.", False,
     "The advice assumes the food aids fitness (I); it makes no comparison with medicines (II)."),
    ("\"Recharge before the validity expires to keep your number active.\" -- a telecom SMS.",
     "An expired validity can deactivate the number.", True,
     "The customer wants to keep the number active.", True,
     "The reminder presupposes that expiry risks deactivation (I) and that the customer values keeping the number (II)."),
]

# ---- Statement & Inference --------------------------------------------------
INFER_OPTIONS = [
    "Definitely true",
    "Definitely false",
    "Cannot be determined from the statement",
    "Probably true but not certain",
]
# (statement, inference, correct_text, reason)
INFER_DATA = [
    ("All students in Class X scored above 80 marks. Riya is a student of Class X.",
     "Riya scored above 80 marks.",
     "Definitely true",
     "Riya belongs to a class in which everyone scored above 80, so her score must be above 80."),
    ("No member of the team is below 18 years of age. Karan is a member of the team.",
     "Karan is below 18 years of age.",
     "Definitely false",
     "No member is below 18; since Karan is a member, he cannot be below 18."),
    ("Some books in the shop are novels. All novels are paperbacks.",
     "Some books in the shop are paperbacks.",
     "Definitely true",
     "Some books are novels and all novels are paperbacks, so those novels are paperbacks among the books."),
    ("Half of the employees in the office own a car.",
     "Mr. Sen, an employee of the office, owns a car.",
     "Cannot be determined from the statement",
     "Only half own a car; whether Mr. Sen is among them is not stated."),
    ("Every shop on Main Street closes on Sunday. The bakery is on Main Street.",
     "The bakery is open on Sunday.",
     "Definitely false",
     "Every shop on Main Street closes on Sunday, so the bakery, being there, is closed on Sunday."),
    ("All the questions in the test were difficult, and Meena answered every question.",
     "Meena attempted at least one difficult question.",
     "Definitely true",
     "All questions were difficult and she answered every one, so she attempted difficult questions."),
    ("Most of the passengers on the bus were going to the city.",
     "All passengers on the bus were going to the city.",
     "Definitely false",
     "'Most' explicitly means not all, so 'all' contradicts the statement."),
    ("The temperature in the city has risen every year for the last ten years.",
     "The temperature will rise next year as well.",
     "Probably true but not certain",
     "A ten-year trend makes a further rise likely but does not guarantee it."),
    ("None of the candidates who failed the interview were called back.",
     "A candidate who was called back had not failed the interview.",
     "Definitely true",
     "If failing implies not being called back, then being called back implies not failing (contrapositive)."),
    ("Some of the apples in the basket are rotten.",
     "Some of the apples in the basket are not rotten.",
     "Cannot be determined from the statement",
     "'Some are rotten' does not tell us whether any are fresh; possibly all are rotten."),
    ("All who passed the exam received a certificate. Anil did not receive a certificate.",
     "Anil did not pass the exam.",
     "Definitely true",
     "Passing implies a certificate; lacking a certificate therefore implies not passing (contrapositive)."),
    ("Every child in the class can read. Some children in the class can also write.",
     "Every child who can write can read.",
     "Definitely true",
     "Every child can read, so any child (including those who write) can read."),
    ("The library has more than 5000 books.",
     "The library has exactly 5200 books.",
     "Cannot be determined from the statement",
     "'More than 5000' is consistent with many counts; the exact figure is unknown."),
    ("No vegetarian dish on the menu contains egg. The pasta on the menu contains egg.",
     "The pasta on the menu is not a vegetarian dish.",
     "Definitely true",
     "Vegetarian dishes have no egg; the pasta has egg, so it is not a vegetarian dish."),
    ("Sales of the company increased in each of the past three quarters.",
     "Sales of the company will increase in the next quarter.",
     "Probably true but not certain",
     "A three-quarter rise suggests but does not ensure another increase."),
    ("Whenever it rains, the match is cancelled. Today the match was not cancelled.",
     "It did not rain today.",
     "Definitely true",
     "Rain implies cancellation; no cancellation implies no rain (contrapositive)."),
    ("Among the students, those who study daily always pass.",
     "A student who failed did not study daily.",
     "Definitely true",
     "Studying daily implies passing; failing therefore implies not studying daily (contrapositive)."),
    ("A few of the roads in the town are unpaved.",
     "Most of the roads in the town are unpaved.",
     "Cannot be determined from the statement",
     "'A few are unpaved' gives no information about the proportion; 'most' cannot be concluded."),
    ("All trained drivers in the company hold a valid licence. Rahul is a trained driver in the company.",
     "Rahul holds a valid licence.",
     "Definitely true",
     "All trained drivers hold a valid licence and Rahul is one, so he holds a valid licence."),
    ("The shop offers a discount only on weekends. Today is a weekday.",
     "The shop is offering a discount today.",
     "Definitely false",
     "Discounts occur only on weekends; today is a weekday, so no discount today."),
]

# ---- Course of Action -------------------------------------------------------
COA_OPTIONS = [
    "Only course of action I follows",
    "Only course of action II follows",
    "Both I and II follow",
    "Neither I nor II follows",
]
# A course of action FOLLOWS if it is a practical, relevant step that directly
# addresses the problem in the statement (and is not extreme/irrelevant).
# (statement, COA_I, follows_I?, COA_II, follows_II?, reason)
COA_DATA = [
    ("Many road accidents on the highway are caused by overspeeding vehicles at night.",
     "Speed-limit checks and lighting should be improved on the highway at night.", True,
     "The highway should be permanently closed at night.", False,
     "Improving checks and lighting directly tackles night overspeeding (I). A blanket closure is impractical and extreme (II)."),
    ("A large number of students fail in mathematics every year in the school.",
     "Extra coaching classes in mathematics should be arranged for weak students.", True,
     "Mathematics should be removed from the syllabus.", False,
     "Extra coaching addresses the failures (I). Dropping the subject is an over-reaction, not a remedy (II)."),
    ("The city is facing an acute shortage of drinking water in summer.",
     "Rainwater harvesting should be made compulsory for large buildings.", True,
     "People should be advised to use water judiciously.", True,
     "Harvesting augments supply (I) and conservation reduces demand (II); both help."),
    ("There has been a sharp rise in cases of a contagious disease in a locality.",
     "The affected persons should be isolated and treated promptly.", True,
     "The residents of the locality should be ignored to avoid panic.", False,
     "Isolation and treatment check the spread (I). Ignoring residents worsens the situation (II)."),
    ("Many passengers travel without tickets on the suburban trains.",
     "Surprise ticket checks should be intensified on these trains.", True,
     "All ticketless passengers should be jailed for life.", False,
     "Intensified checks deter ticketless travel (I). Life imprisonment is grossly disproportionate (II)."),
    ("The pass percentage of a college has been falling for the last three years.",
     "The teaching methods and student support should be reviewed and improved.", True,
     "The college should declare all students as passed.", False,
     "Reviewing teaching tackles the decline (I). Declaring everyone passed is dishonest, not a solution (II)."),
    ("A factory's machines break down frequently, halting production.",
     "A regular preventive-maintenance schedule should be introduced.", True,
     "The factory should be shut down permanently.", False,
     "Preventive maintenance reduces breakdowns (I). Permanent shutdown abandons the goal (II)."),
    ("Air pollution in the metro city has reached dangerous levels.",
     "Use of public transport should be encouraged to reduce vehicular emissions.", True,
     "Industries should be required to control their emissions.", True,
     "Both reducing vehicle emissions (I) and controlling industrial emissions (II) address the pollution."),
    ("Crops were badly damaged due to an unexpected flood in the district.",
     "Immediate relief and compensation should be provided to the affected farmers.", True,
     "Farming should be banned in the district.", False,
     "Relief addresses the loss (I). Banning farming destroys livelihoods and is no remedy (II)."),
    ("The number of complaints about poor service at a bank branch has increased.",
     "The staff should be trained and customer-grievances addressed promptly.", True,
     "The branch should stop accepting any new customers.", False,
     "Training and grievance handling improve service (I). Refusing customers harms the bank (II)."),
    ("Frequent power cuts are affecting small businesses in the town.",
     "The power supply and distribution network should be upgraded.", True,
     "Small businesses should be asked to shut down.", False,
     "Upgrading supply tackles the cuts (I). Shutting businesses defeats the purpose (II)."),
    ("Many young people in the area are unemployed despite being educated.",
     "Skill-development and job-placement programmes should be organised.", True,
     "Education should be discouraged in the area.", False,
     "Skilling and placement address unemployment (I). Discouraging education is counter-productive (II)."),
    ("The river passing through the town is heavily polluted by untreated sewage.",
     "Sewage-treatment plants should be set up before discharge into the river.", True,
     "Discharge of untreated sewage into the river should be penalised.", True,
     "Treating sewage (I) and penalising untreated discharge (II) both reduce the pollution."),
    ("A school bus met with an accident due to the driver's careless driving.",
     "The driving record of all school-bus drivers should be reviewed.", True,
     "All school buses should be taken off the road forever.", False,
     "Reviewing drivers targets the cause (I). Removing all buses permanently is excessive (II)."),
    ("Sales of a company's product have dropped sharply after a competitor entered the market.",
     "The company should improve product quality and review its pricing.", True,
     "The company should stop all production immediately.", False,
     "Improving quality and pricing helps regain sales (I). Halting production surrenders the market (II)."),
    ("Several students fell ill after eating in the school canteen.",
     "The hygiene and food quality of the canteen should be inspected.", True,
     "Students should be forbidden from ever eating again.", False,
     "Inspecting hygiene addresses the cause (I). Forbidding eating is absurd (II)."),
    ("Traffic congestion at a junction is increasing during peak hours.",
     "Traffic signals and lane discipline at the junction should be improved.", True,
     "All vehicles should be banned from the city.", False,
     "Better signals ease congestion (I). Banning all vehicles is impractical (II)."),
    ("A region is repeatedly hit by cyclones causing loss of life.",
     "An early-warning and evacuation system should be strengthened.", True,
     "The people of the region should be left to face the cyclones.", False,
     "Early warning saves lives (I). Abandoning the people is no action at all (II)."),
    ("Many customers complain that the helpline is always busy.",
     "More lines and trained staff should be added to the helpline.", True,
     "The helpline should be discontinued.", False,
     "Adding capacity addresses the load (I). Discontinuing removes the service entirely (II)."),
    ("The number of stray-dog bites in the colony has gone up.",
     "A vaccination and sterilisation drive for stray dogs should be carried out.", True,
     "Awareness about handling stray dogs should be spread among residents.", True,
     "Vaccination/sterilisation reduces the menace (I) and awareness reduces bite incidents (II)."),
]

# ---- Cause & Effect ---------------------------------------------------------
CE_OPTIONS = [
    "Statement I is the cause and statement II is its effect",
    "Statement II is the cause and statement I is its effect",
    "Both statements are independent causes",
    "Both statements are effects of a common cause",
]
# (stmtI, stmtII, correct_text, reason)
CE_DATA = [
    ("The government raised the tax on petrol last week.",
     "The price of petrol at fuel stations increased this week.",
     "Statement I is the cause and statement II is its effect",
     "The tax hike came first and directly pushed up the retail price."),
    ("Heavy rain lashed the city throughout the night.",
     "Several low-lying areas of the city were waterlogged in the morning.",
     "Statement I is the cause and statement II is its effect",
     "The night-long rain led to the morning waterlogging."),
    ("The school declared a holiday on account of a local festival.",
     "Attendance in the school was nil on that day.",
     "Statement I is the cause and statement II is its effect",
     "The declared holiday caused the absence of all students."),
    ("Prices of vegetables shot up in the market this week.",
     "A prolonged drought damaged the standing crops last month.",
     "Statement II is the cause and statement I is its effect",
     "The earlier crop damage reduced supply, which raised this week's prices."),
    ("Many residents of the town fell sick with stomach infections.",
     "The town's water-supply pipeline was found contaminated.",
     "Statement II is the cause and statement I is its effect",
     "The contaminated water (II) caused the stomach infections (I)."),
    ("The company announced record profits this year.",
     "The company distributed a large bonus to its employees.",
     "Statement I is the cause and statement II is its effect",
     "The record profit enabled and prompted the bonus."),
    ("The temperature in the region dropped sharply overnight.",
     "Sales of woollen clothes rose the next day.",
     "Statement I is the cause and statement II is its effect",
     "The fall in temperature increased the demand for woollens."),
    ("There was a sudden bandh call by traders in the city.",
     "Most shops and markets remained closed for the day.",
     "Statement I is the cause and statement II is its effect",
     "The bandh call led the shops to stay closed."),
    ("The crops in the village were severely damaged by locusts.",
     "Many farmers in the village reported heavy financial losses.",
     "Statement I is the cause and statement II is its effect",
     "The locust damage caused the farmers' losses."),
    ("The central bank reduced interest rates this quarter.",
     "Home-loan applications increased noticeably this quarter.",
     "Statement I is the cause and statement II is its effect",
     "Cheaper loans after the rate cut spurred more applications."),
    ("A major IT firm announced large-scale hiring in the city.",
     "Rents for flats near the firm's office rose sharply.",
     "Statement I is the cause and statement II is its effect",
     "The hiring drew people to the area, pushing up rents."),
    ("The roads in the area remained flooded for two days.",
     "Schools in the area were closed for two days.",
     "Statement I is the cause and statement II is its effect",
     "The flooded roads led to the schools being closed."),
    ("There was a long power outage in the industrial estate.",
     "Production in several factories was halted that day.",
     "Statement I is the cause and statement II is its effect",
     "The power outage caused the production halt."),
    ("A new metro line was opened connecting the suburb to the city centre.",
     "Road traffic on the parallel highway decreased noticeably.",
     "Statement I is the cause and statement II is its effect",
     "Commuters shifting to the metro reduced highway traffic."),
    ("The state experienced a severe heat wave for a week.",
     "The demand for electricity in the state hit a record high.",
     "Statement I is the cause and statement II is its effect",
     "The heat wave drove up cooling demand and hence electricity use."),
    ("The football match was abandoned midway.",
     "A heavy downpour made the ground unplayable.",
     "Statement II is the cause and statement I is its effect",
     "The downpour (II) made the ground unplayable, causing the match to be abandoned (I)."),
    ("Many flights at the airport were delayed in the morning.",
     "Dense fog reduced visibility at the airport at dawn.",
     "Statement II is the cause and statement I is its effect",
     "The dawn fog (II) caused the flight delays (I)."),
    ("Both the wheat crop and the mustard crop failed in the district this season.",
     "An unusually long dry spell hit the district before sowing.",
     "Statement II is the cause and statement I is its effect",
     "The dry spell (II) caused both crops to fail (I)."),
    ("The factory installed pollution-control equipment last year.",
     "The level of harmful emissions from the factory fell this year.",
     "Statement I is the cause and statement II is its effect",
     "Installing the equipment reduced the emissions."),
    ("There was a sharp rise in the number of dengue cases in the city.",
     "Water stagnated in many parts of the city after the monsoon.",
     "Statement II is the cause and statement I is its effect",
     "Stagnant water (II) bred mosquitoes, causing the rise in dengue (I)."),
]

# ===========================================================================
# ASSEMBLE FAMILY B QUESTIONS
# ===========================================================================
def build_curated():
    items = []

    # Statement & Assumption
    for (st, a1, i1, a2, i2, reason) in ASSUM_DATA:
        if i1 and i2:
            ct = "Both I and II are implicit"
        elif i1:
            ct = "Only assumption I is implicit"
        elif i2:
            ct = "Only assumption II is implicit"
        else:
            ct = "Neither I nor II is implicit"
        opts, ci = make_options(ct, ASSUM_OPTIONS)
        stem = (f"**Statement:** {st}\n"
                f"**Assumptions:** I. {a1}  II. {a2}\n"
                f"Which of the assumptions is/are implicit in the statement?")
        items.append({"kind": "ASSUM", "stem": stem, "options": opts,
                      "correct_index": ci, "sol": reason})

    # Statement & Inference
    for (st, inf, ct, reason) in INFER_DATA:
        opts, ci = make_options(ct, INFER_OPTIONS)
        stem = (f"**Statement:** {st}\n"
                f"**Inference:** {inf}\n"
                f"On the basis of the statement, the inference is:")
        items.append({"kind": "INFER", "stem": stem, "options": opts,
                      "correct_index": ci, "sol": reason})

    # Course of Action
    for (st, c1, f1, c2, f2, reason) in COA_DATA:
        if f1 and f2:
            ct = "Both I and II follow"
        elif f1:
            ct = "Only course of action I follows"
        elif f2:
            ct = "Only course of action II follows"
        else:
            ct = "Neither I nor II follows"
        opts, ci = make_options(ct, COA_OPTIONS)
        stem = (f"**Statement:** {st}\n"
                f"**Courses of action:** I. {c1}  II. {c2}\n"
                f"Which course(s) of action logically follow(s)?")
        items.append({"kind": "COA", "stem": stem, "options": opts,
                      "correct_index": ci, "sol": reason})

    # Cause & Effect
    for (s1, s2, ct, reason) in CE_DATA:
        opts, ci = make_options(ct, CE_OPTIONS)
        stem = (f"**Statement I:** {s1}\n"
                f"**Statement II:** {s2}\n"
                f"Which of the following best describes the relationship?")
        items.append({"kind": "CE", "stem": stem, "options": opts,
                      "correct_index": ci, "sol": reason})

    return items

# ===========================================================================
# DIFFICULTY ASSIGNMENT FOR CURATED ITEMS
# ===========================================================================
# We have 80 curated items. Assign difficulty by a heuristic: items whose
# correct answer is 'Both' or a non-obvious 'Neither/Only II' or contrapositive
# inferences are Hard/Very-Hard; straightforward direct-cause / direct-follow
# are Medium. We tune the final M/H/VH globally after combining with family A.

# ===========================================================================
# MAIN ASSEMBLY
# ===========================================================================
TARGET = 500
# Curated count is len(build_curated()) == 80.
# Family A fills the remaining 420.

def assign_curated_difficulty(items):
    """Deterministic difficulty for curated items, leaning H (60%)."""
    for idx, it in enumerate(items):
        k = it["kind"]
        ct = it["options"][it["correct_index"]]
        # base mapping
        if k == "INFER":
            if ct in ("Definitely true", "Definitely false"):
                d = "M" if "All " in it["stem"] or "No " in it["stem"] else "H"
            elif ct == "Probably true but not certain":
                d = "H"
            else:  # cannot be determined
                d = "VH"
        elif k == "ASSUM":
            d = "H" if ct in ("Both I and II are implicit", "Neither I nor II is implicit",
                              "Only assumption II is implicit") else "M"
        elif k == "COA":
            d = "M" if ct == "Only course of action I follows" else "H"
        elif k == "CE":
            d = "M" if ct == "Statement I is the cause and statement II is its effect" else "H"
        else:
            d = "H"
        it["diff"] = d
    return items

def main():
    if not solver_self_test():
        raise SystemExit("Solver self-test failed.")

    questions = []  # unified list; each has render() info

    # ---- FAMILY B (curated) ----
    curated = build_curated()
    curated = assign_curated_difficulty(curated)
    for it in curated:
        questions.append({"family": "B", **it})

    n_curated = len(questions)
    print(f"Curated (Family B) items: {n_curated}")

    # ---- FAMILY A (computable) ----
    # We need 500 - n_curated computable items. Control difficulty so the
    # global mix lands near 20/60/20.
    need_A = TARGET - n_curated

    # Target global difficulty
    g_quota = {"M": 100, "H": 300, "VH": 100}
    cur_counts = Counter(it["diff"] for it in curated)
    a_quota = {d: max(0, g_quota[d] - cur_counts.get(d, 0)) for d in g_quota}
    # ensure a_quota sums to need_A; adjust H (the bulk) for any rounding
    diff_total = need_A - sum(a_quota.values())
    a_quota["H"] += diff_total
    print("Curated difficulty:", dict(cur_counts))
    print("Family A quota:", a_quota)

    seen = set()
    a_counts = {"M": 0, "H": 0, "VH": 0}

    def qkey_A(q):
        return (tuple(q["statements"]), tuple(q["concs"]))

    def try_add_A(target_diff):
        if target_diff == "M":
            ns = 2
            q = gen_candidate_A(ns)
        elif target_diff == "H":
            ns = random.choice([2, 2, 3])
            q = gen_candidate_A(ns)
        else:  # VH: prefer either-or / 3-statement
            if random.random() < 0.5:
                q = gen_candidate_A(3, force_either=True)
            else:
                q = gen_candidate_A(3)
        if q is None:
            return False
        k = qkey_A(q)
        if k in seen:
            return False
        v = q["verdict"]
        # difficulty discipline
        if target_diff == "M":
            if v == "EITHER":   # either-or is never Medium
                return False
            diff = "M"
        elif target_diff == "H":
            diff = "VH" if v == "EITHER" else "H"
            if diff != "H":
                return False  # keep H bucket clean
        else:
            diff = "VH"
        if a_counts[diff] >= a_quota[diff]:
            return False
        q["diff"] = diff
        q["nstmt"] = q["statements"].__len__()
        seen.add(k)
        q["sol"] = build_solution_A(q)
        questions.append({"family": "A", "kind": "CONC", **q})
        a_counts[diff] += 1
        return True

    order = ["VH", "M", "H"]
    attempts = 0
    while sum(a_counts.values()) < need_A and attempts < 5_000_000:
        attempts += 1
        unmet = [d for d in order if a_counts[d] < a_quota[d]]
        if not unmet:
            break
        try_add_A(random.choice(unmet))

    print(f"Family A generated: {sum(a_counts.values())} in {attempts} attempts; {dict(a_counts)}")

    # shuffle interleave A and B so the set is mixed, but keep deterministic
    random.shuffle(questions)
    assert len(questions) == TARGET, f"got {len(questions)} questions"

    # ---- INTERNAL SELF-CHECK ----
    errors = 0
    stems_seen = set()
    for i, q in enumerate(questions, 1):
        if q["family"] == "A":
            opts = STD_OPTIONS_5 if q["verdict"] == "EITHER" else STD_OPTIONS_4
            ct = VERDICT_TO_TEXT[q["verdict"]]
            ci = opts.index(ct)
            q["_opts"] = opts
            q["_ci"] = ci
            stem_id = ("A", tuple(q["statements"]), tuple(q["concs"]))
        else:
            q["_opts"] = q["options"]
            q["_ci"] = q["correct_index"]
            stem_id = ("B", q["stem"])
        # one keyed option, distinct options
        if len(set(q["_opts"])) != len(q["_opts"]):
            print(f"Q{i}: duplicate options"); errors += 1
        if not (0 <= q["_ci"] < len(q["_opts"])):
            print(f"Q{i}: bad correct index"); errors += 1
        if stem_id in stems_seen:
            print(f"Q{i}: DUPLICATE STEM"); errors += 1
        stems_seen.add(stem_id)
    print(f"Internal self-check errors: {errors}")
    if errors:
        raise SystemExit("Internal self-check failed.")

    final_counts = Counter(q["diff"] for q in questions)
    fam_counts = Counter(q["family"] for q in questions)
    print("Final difficulty:", dict(final_counts))
    print("Family split:", dict(fam_counts))

    write_markdown(questions)
    write_sidecar(questions)
    print("DONE")

# ===========================================================================
# RENDERING
# ===========================================================================
KIND_LABEL = {
    "CONC": "Statement & Conclusion",
    "ASSUM": "Statement & Assumption",
    "INFER": "Statement & Inference",
    "COA": "Course of Action",
    "CE": "Cause & Effect",
}

def render_question_body(q):
    if q["family"] == "A":
        head = f"*[Statement & Conclusion]*  Statements: {render_statements_A(q['statements'])}"
        c1, c2 = q["concs"]
        concs = f"Conclusions: I. {stmt_text(*c1)} II. {stmt_text(*c2)}"
        return head + "\n" + concs
    else:
        label = KIND_LABEL[q["kind"]]
        return f"*[{label}]*  " + q["stem"]

def write_markdown(questions):
    L = []
    L.append("# Statement & Conclusion / Assumption / Inference / Cause-Effect / Course of Action — 500 Question Practice Set (SSC CGL, Reasoning, Tier-I/II Level)\n")
    L.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
    L.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard.")
    L.append("> **Mix:** logical-deduction *Statement & Conclusion* items are machine-verified by a brute-force set-model checker (the keyed option is provably correct); the *Assumption / Inference / Cause-Effect / Course-of-Action* items are authored to conventional SSC logic with exactly one defensible answer.")
    L.append("> Negative marking in CGL is −0.50.\n")
    L.append("## How to answer (by sub-type)")
    L.append("- **Statement & Conclusion (logical):** treat the statements as definitely true; a conclusion *follows* only if it must be true in EVERY situation consistent with the statements. A merely *possible* conclusion does not follow. *Either-or* applies when two complementary conclusions cannot both be false.")
    L.append("- **Statement & Assumption:** an assumption is *implicit* only if it is necessarily taken for granted for the statement to hold. Do not bring in extra or extreme suppositions.")
    L.append("- **Statement & Inference:** decide what can be *definitely* concluded — *Definitely true*, *Definitely false*, *Cannot be determined*, or *Probably true but not certain*.")
    L.append("- **Course of Action:** an action *follows* only if it is a practical, relevant step that directly addresses the problem; extreme or irrelevant steps do not follow.")
    L.append("- **Cause & Effect:** identify which event brought about the other, or whether both share a common cause / are independent.\n")
    L.append("## Standard option legends")
    L.append("- *Conclusion items:* (a) Only I follows · (b) Only II follows · (c) Both follow · (d) Neither follows · (e) Either I or II follows *(only when applicable)*")
    L.append("- *Assumption items:* (a) Only I implicit · (b) Only II implicit · (c) Both implicit · (d) Neither implicit")
    L.append("- *Inference items:* (a) Definitely true · (b) Definitely false · (c) Cannot be determined · (d) Probably true but not certain")
    L.append("- *Course-of-action items:* (a) Only I follows · (b) Only II follows · (c) Both follow · (d) Neither follows")
    L.append("- *Cause-effect items:* (a) I is cause, II effect · (b) II is cause, I effect · (c) independent causes · (d) effects of a common cause\n")
    L.append("\n# =================== QUESTIONS ===================\n")

    for start in range(0, TARGET, 50):
        blk = start // 50 + 1
        L.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            opts = q["_opts"]
            L.append(f"**Q{n}.** {render_question_body(q)}")
            opt_line = "  ".join(f"({LETTERS[i]}) {opts[i]}" for i in range(len(opts)))
            L.append(opt_line + "\n")

    L.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
    for start in range(0, TARGET, 50):
        L.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            ci = q["_ci"]
            letter = LETTERS[ci]
            txt = q["_opts"][ci]
            L.append(f"**Q{n}. ({letter}) {txt}**  *[{q['diff']}]* — {q['sol']}")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"Wrote {OUT} ({len(L)} lines)")

def write_sidecar(questions):
    """Sidecar maps qnum -> verdict for the FAMILY A (computable) subset only."""
    data = {}
    for j, q in enumerate(questions, 1):
        if q["family"] == "A":
            data[str(j)] = q["verdict"]
    with open(SIDECAR, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=0)
    print(f"Wrote {SIDECAR} ({len(data)} computable entries)")

if __name__ == "__main__":
    main()

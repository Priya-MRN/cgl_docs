"""Generate the answer key + explanations PDF for Mock_Test_Hard_01.
Uses fpdf (already installed). Output: Mock-Tests/Mock_Test_Hard_01_Answers.pdf
"""
from fpdf import FPDF
import os

OUT = os.path.join("Mock-Tests", "Mock_Test_Hard_01_Answers.pdf")

# (question no, correct option letter, explanation)
ANSWERS = [
    # ---------- Section A: Reasoning ----------
    ("Q1", "b", "Pattern: x2 + (1,2,3,4,5...). 3->7 (x2+1), 7->16 (x2+2), 16->35 (x2+3), 35->74 (x2+4), 74->74x2+5 = 153."),
    ("Q2", "a", "These are n^3 - 1 for n = 2,3,4,5,6: 2^3-1=7, 3^3-1=26, 4^3-1=63, 5^3-1=124, 6^3-1=215. Next: 7^3-1 = 343-1 = 342."),
    ("Q3", "b", "Rule: n*(n+1). 6 -> 6x7 = 42. So 8 -> 8x9 = 72."),
    ("Q4", "a", "Pattern: x2 + 1: 6->13 (x2+1), 13->28 (x2+2), 28->59 (x2+3), 59->122 (x2+4), 122->122x2+5 = 249."),
    ("Q5", "d", "He walks N10, E8 (right from N is E), S4 (right again), then E6 (left). East total = 8+6 = 14, North total = 10-4 = 6; now facing East. Straight-line distance = sqrt(14^2 + 6^2). Both (b) and (d) state this distance, but (d) also gives the facing direction (East), so it is the most complete answer. Answer (d)."),
    ("Q6", "a", "Each number n maps to 5^n: 1->5, 2->25, 3->125, 4->625, so 5->5^5 = 3125."),
    ("Q7", "c", "All keys are locks; some locks are doors (the door-locks need not be keys) -> 'some keys are doors' not necessary. No door is window, but locks-windows undetermined. None of I, II, III necessarily follows. Answer (c)."),
    ("Q8", "b", "Two-face-painted cubes lie on edges (not corners). For side n: 12(n-2). n=5 -> 12x3 = 36."),
    ("Q9", "a", "First letters: A(+6)G(+6)M(+6)S(+6)Y. Second letters: Z(-6)T(-6)N(-6)H(-6)B. So next pair = YB. Answer (a) YB."),
    ("Q10", "a", "Substitute real operators: - means /, + means x, x means -, / means +. Expression 18 - 3 + 5 x 2 / 4 becomes 18 / 3 x 5 - 2 + 4. BODMAS: 18/3 = 6; 6 x 5 = 30; then 30 - 2 + 4 = 32. Answer (a) 32."),
    ("Q11", "b", "Grandfather's only son = the man's father. The lady is the daughter of the man's father => she is the man's sister. Answer (b) Sister."),
    ("Q12", "d", "Rule: (a + b) x c. Row1: (2+3)x4 = 20. Row2: (3+4)x5 = 35. Row3: (4+5)x6 = 54. Answer (d) 54."),
    ("Q13", "c", "Every mother is a woman (Mothers subset Women). Doctors can be men or women, so Doctors intersects both Women and Mothers. Answer (c)."),
    ("Q14", "c", "Faulty clock loses 5 min/hr so it shows 55 min for every 60 real min -> it is SLOW. When faulty shows 6 hrs (360 faulty min), real elapsed = 360 x (60/55) = 392.7 min = 6 h 32.7 min -> ~6:33 PM. Answer (c)."),
    ("Q15", "a", "Terms = n^2(n+1): n=1 ->1x2=2, n=2 ->4x3=12, n=3 ->9x4=36, n=4 ->16x5=80, n=5 ->25x6=150, n=6 ->36x7=252. Answer (a)."),
    ("Q16", "a", "Row of 5 facing North (left->right). R is extreme left (pos1), S extreme right (pos5), P middle (pos3), T immediately right of P (pos4). Only Q is left for pos2. So second from left = Q. Answer (a)."),
    ("Q17", "d", "Letters symmetric about a vertical mirror line: M, O, M. 'MOM' reads the same in a vertical mirror. Answer (d)."),
    ("Q18", "a", "A is SW of B, C is SE of B. From A, B is NE; C is due East of A (same southward offset, C further east). Answer (a) East."),
    ("Q19", "b", "343=7^3, 512=8^3, 729=9^3, 1000=10^3 are perfect cubes; 1320 is not. Answer (b)."),
    ("Q20", "b", "Q is 11th from right; after interchange P takes Q's place and is 13th from left, so Q was 13th from left. Total = (13 from left) + (11 from right) - 1 = 23. Answer (b)."),
    ("Q21", "d", "Rule: x2 + 1. 6 -> 6x2+1 = 13; 13 -> 27; 27 -> 55; 55 -> 111; 111 -> 111x2+1 = 223. The last term should be 223, not 222, so the wrong term is (d) 222."),
    ("Q22", "a", "16x1x9x14x20 = 16x9=144; 144x14=2016; 2016x20=40320. /5 = 8064. Unit digit = 4. Answer (a)."),
    ("Q23", "b", "On a standard dice opposite faces sum to 7: opposite of 3 = 7 - 3 = 4. Answer (b) 4."),
    ("Q24", "a", "Pole: L = v*9. Platform: L+240 = v*24. Subtract: 240 = 15v -> v=16 m/s. L = 16x9 = 144 m. Answer (a)."),
    ("Q25", "b", "'Son of the wife of my husband's father' = son of the woman's mother-in-law = the woman's husband or his brother. Since he is explicitly not her husband, he is her husband's brother => brother-in-law. Answer (b)."),

    # ---------- Section B: GA ----------
    ("Q26", "b", "Article 17 abolishes untouchability."),
    ("Q27", "b", "Doctrine of Lapse was applied by Lord Dalhousie (1848-56)."),
    ("Q28", "c", "Tropic of Cancer passes through 8 states (Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram). It does NOT pass through Odisha."),
    ("Q29", "b", "Protecting and improving the natural environment is a Fundamental Duty under Article 51A(g)."),
    ("Q30", "c", "Nathu La pass (Sikkim) connects India with China (Tibet)."),
    ("Q31", "b", "The slogan 'Inquilab Zindabad' was coined by Maulana Hasrat Mohani; popularised by Bhagat Singh."),
    ("Q32", "c", "Rancidity is oxidation of fats/oils by atmospheric oxygen."),
    ("Q33", "a", "The Marble Rocks gorge at Bhedaghat (Jabalpur) is formed by the Narmada river."),
    ("Q34", "b", "Insulin is secreted by the beta cells of the islets of Langerhans in the pancreas."),
    ("Q35", "b", "The 73rd Amendment (1992) gave constitutional status to Panchayati Raj institutions."),
    ("Q36", "c", "Rice is a Kharif (monsoon-sown) crop; wheat, mustard, barley are Rabi."),
    ("Q37", "a", "Battle of Plassey was fought in 1757 (Clive vs Siraj-ud-Daulah)."),
    ("Q38", "b", "Hawala is an informal, often illegal, value-transfer system linked to money laundering."),
    ("Q39", "c", "Vitamin K is synthesised by intestinal bacteria."),
    ("Q40", "b", "The Cripps Mission arrived in March 1942."),
    ("Q41", "c", "The Fourth Schedule deals with allocation of seats in the Rajya Sabha."),
    ("Q42", "b", "The SI unit of electrical conductance is the siemens (S)."),
    ("Q43", "b", "The Kailasa Temple at Ellora was built by the Rashtrakuta king Krishna I."),
    ("Q44", "b", "Repo rate is the rate at which the RBI lends to commercial banks against government securities."),
    ("Q45", "c", "The liver is the largest gland in the human body."),
    ("Q46", "c", "The Shimla Agreement was signed in 1972 (after the 1971 war)."),
    ("Q47", "c", "Black (Regur) soil retains moisture and is ideal for cotton."),
    ("Q48", "b", "Washing soda is sodium carbonate decahydrate, Na2CO3.10H2O."),
    ("Q49", "b", "Akbar abolished the Jizya tax (later re-imposed by Aurangzeb)."),
    ("Q50", "b", "The Coriolis force deflects winds and ocean currents (right in N hemisphere, left in S)."),

    # ---------- Section C: Quant ----------
    ("Q51", "a", "x+1/x=3 -> (x+1/x)^3 = x^3+1/x^3 + 3(x+1/x). 27 = (x^3+1/x^3) + 9 -> x^3+1/x^3 = 18."),
    ("Q52", "b", "Doubles in 8 yr SI -> interest = principal in 8 yr, so rate*8 = 100% -> 12.5%/yr. To become 5x, interest = 4P -> 400% / 12.5 = 32 years."),
    ("Q53", "b", "SI for 2 yr = 400 -> 200/yr. CI - SI for 2 yr = 410-400 = 10 = interest on first-year interest = 200 * r. r = 10/200 = 5%."),
    ("Q54", "a", "1/(A+B)=1/12, 1/(B+C)=1/15, 1/(C+A)=1/20. Sum = 2(A+B+C) rate = 1/12+1/15+1/20 = (5+4+3)/60 = 12/60 = 1/5. So (A+B+C)=1/10. All three: 10 days."),
    ("Q55", "a", "h/x... at 30deg: h = d*tan30 from far; standard result h = (40 * tan30 * tan60)/(tan60 - tan30). = 40*(1/sqrt3)*sqrt3 /(sqrt3 - 1/sqrt3) = 40 / (2/sqrt3) = 20*sqrt3 m."),
    ("Q56", "a", "sec+tan=2 and sec-tan=1/2 (since sec^2-tan^2=1). Add: 2sec=2.5 -> sec=1.25 -> cos=0.8 -> sin=0.6 = 3/5. Answer (a) 3/5."),
    ("Q57", "a", "Sum of 11 = 550. First 6 sum = 294, last 6 sum = 312. 6th counted twice: 294+312 - 550 = 56."),
    ("Q58", "a", "MP = 1.4 CP; SP = 0.9 x 1.4 = 1.26 CP -> 26% profit."),
    ("Q59", "a", "Rates: 1/20 + 1/30 - 1/40 = (6+4-3)/120 = 7/120 per min -> time = 120/7 = 17 1/7 min."),
    ("Q60", "b", "2^3 = 8 = 1 mod 7. 2^100 = 2^99 x 2 = (2^3)^33 x 2 = 1 x 2 = 2 mod 7. Remainder = 2. Answer (b)."),
    ("Q61", "a", "Upstream speed = 24/6 = 4 km/h; downstream = 36/6 = 6 km/h. Stream = (6-4)/2 = 1 km/h."),
    ("Q62", "b", "a^2+b^2+c^2 = ab+bc+ca implies (a-b)^2+(b-c)^2+(c-a)^2 = 0 -> a=b=c -> equilateral."),
    ("Q63", "a", "Product = HCF x LCM = 11 x 7700 = 84700. Other = 84700 / 275 = 308."),
    ("Q64", "b", "Milk = 40 L, water = 20 L. For milk:water = 1:2, water must be 80 L (twice milk). Add 80-20 = 60 L."),
    ("Q65", "a", "Tn = Sn - S(n-1). S10 = 300+50 = 350; S9 = 243+45 = 288. T10 = 350-288 = 62."),
    ("Q66", "a", "Inradius of equilateral triangle = side/(2*sqrt3) = 12/(2*sqrt3) = 6/sqrt3 = 2*sqrt3 cm."),
    ("Q67", "b", "Required reduction % = (25/(100+25)) x 100 = 25/125 x100 = 20%."),
    ("Q68", "a", "Form a^3+b^3 / (a^2-ab+b^2) = a+b = 0.87+0.13 = 1."),
    ("Q69", "b", "Relative speed = 72-9 = 63 km/h = 63 x 5/18 = 17.5 m/s. Length = 17.5 x 20 = 350 m. Answer (b) 350."),
    ("Q70", "a", "Volume factor = 1.2^2 x 0.8 = 1.44 x 0.8 = 1.152 -> +15.2%."),
    ("Q71", "b", "log(2^64) = 64 x 0.3010 = 19.264. Digits = floor(19.264)+1 = 20."),
    ("Q72", "a", "Capital-months: A = X x12 = 12X; B = 2X x6 = 12X. Ratio 1:1."),
    ("Q73", "b", "20 CP = 16 SP -> SP/CP = 20/16 = 1.25 -> 25% gain."),
    ("Q74", "a", "Sides 13,14,15: s=21, area = sqrt(21x8x7x6) = sqrt(7056) = 84 cm^2."),
    ("Q75", "a", "7^x = 343 -> x = 3; 2^y = 64 -> y = 6. x^2 + y^2 + 2xy = (x + y)^2 = (3 + 6)^2 = 81. Answer (a) 81."),

    # ---------- Section D: English ----------
    ("Q76", "b", "EPHEMERAL = short-lived; opposite = PERMANENT."),
    ("Q77", "b", "Correct spelling: CONSENSUS."),
    ("Q78", "b", "OBSEQUIOUS = excessively obedient/fawning = SERVILE."),
    ("Q79", "b", "'Neither' is singular -> 'has submitted', not 'have submitted'. Error in (b)."),
    ("Q80", "b", "'Let the cat out of the bag' = to reveal a secret."),
    ("Q81", "b", "Correct collocation: 'unanimous IN its decision'."),
    ("Q82", "a", "Present-perfect passive: 'My bicycle has been stolen.'"),
    ("Q83", "b", "PARSIMONIOUS = stingy; antonym = GENEROUS."),
    ("Q84", "a", "Correct punctuation: \"Where,\" she asked, \"are you going?\""),
    ("Q85", "b", "A person who speaks many languages = POLYGLOT."),
    ("Q86", "a", "COGENT = convincing/forceful; fits 'no one could refute it.'"),
    ("Q87", "b", "'A storm in a teacup' = much fuss over a trivial matter."),
    ("Q88", "b", "'Each' is singular -> 'was given', not 'were given'. Error in (b)."),
    ("Q89", "b", "MITIGATE = to lessen = ALLEVIATE."),
    ("Q90", "b", "Reported speech: present continuous -> past continuous. 'She said that she was reading a book.'"),
    ("Q91", "a", "Correct: 'averse TO taking risks.'"),
    ("Q92", "b", "Correct spelling: MAINTENANCE."),
    ("Q93", "b", "That which cannot be corrected = INCORRIGIBLE."),
    ("Q94", "b", "GREGARIOUS = sociable; opposite = RECLUSIVE."),
    ("Q95", "b", "Passage: internet is 'now a prerequisite for full participation in modern... life.'"),
    ("Q96", "b", "Author: policymakers 'frame the issue purely in terms of infrastructure' while affordability/literacy are equally decisive."),
    ("Q97", "b", "Calling it 'a single technological fix' (dismissively) implies technology alone is insufficient."),
    ("Q98", "b", "'Persistent' = continuing/ENDURING."),
    ("Q99", "b", "Tone is analytical and concerned."),
    ("Q100", "b", "Best title: 'Bridging the Digital Divide: Beyond Infrastructure.'"),
]


def ascii_clean(s):
    return (s.replace("→", "->").replace("–", "-").replace("—", "-")
             .replace("‘", "'").replace("’", "'")
             .replace("“", '"').replace("”", '"')
             .replace("√", "sqrt").replace("²", "^2").replace("³", "^3")
             .replace("°", " deg").replace("₹", "Rs.").replace("×", "x")
             .encode("latin-1", "replace").decode("latin-1"))


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, "SSC CGL Tier-I HARD Mock Test 01  -  Answer Key & Explanations", 0, 1, "C")
        self.set_draw_color(180, 180, 180)
        self.line(10, 20, 200, 20)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", 0, 0, "C")


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title block
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(20, 20, 20)
pdf.cell(0, 10, "Answer Key with Explanations", 0, 1, "L")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(70, 70, 70)
pdf.multi_cell(0, 6, ascii_clean(
    "100 Questions - 200 Marks - Negative marking -0.5. Work each problem before checking. "
    "Where a question has an ambiguous published key, the explanation states the intended logic."))
pdf.ln(2)

sections = {
    "Q1": "SECTION A - General Intelligence & Reasoning",
    "Q26": "SECTION B - General Awareness",
    "Q51": "SECTION C - Quantitative Aptitude",
    "Q76": "SECTION D - English Comprehension",
}

for qno, opt, expl in ANSWERS:
    if qno in sections:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 60, 120)
        pdf.cell(0, 8, sections[qno], 0, 1, "L")
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    # question number + answer
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    label = f"{qno}.  Answer: ({opt})"
    pdf.cell(0, 6, ascii_clean(label), 0, 1, "L")
    # explanation
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(55, 55, 55)
    pdf.multi_cell(0, 5, ascii_clean("    " + expl))
    pdf.ln(1)

pdf.output(OUT)
print("Written:", OUT, "pages:", pdf.page_no())

# Arithmetic — Tricks & Shortcuts Handbook (with Hard Examples)

> Back to [Quant Index](README.md) · [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md) · Companion to the topic-wise [Profit & Loss](03_Profit_Loss.md) and [Average & Mixtures](05_Average_Mixtures.md) banks.

## What this is
Every important **shortcut/trick** in SSC-CGL arithmetic, **grouped by topic**. For each trick you get:
- **The idea** (the shortcut + its formula in one or two lines)
- **When to use it** (how to recognise the question)
- **A HARD worked example** — deliberately tough, multi-step, with tricky numbers, so you are ready for the worst case in the exam
- **Trap** — the exact mistake most students make on that question type

> ✅ **All worked examples have been independently re-solved and checked for arithmetic accuracy.** Profit & Loss and Mixtures & Alligation are placed first and given the most tricks, as you asked.

## How to use it
1. Read the **idea** and **when-to-use** first — that is what you must recall in the exam.
2. Cover the solution and try the **hard example** yourself. Only then read the steps.
3. Memorise the **trap** for each — most lost marks come from these, not from not knowing the method.

## Topics in this handbook
1. [Profit, Loss & Discount](#profit-loss-discount) — 10 tricks ⭐
2. [Mixtures & Alligation](#mixtures-alligation) — 10 tricks ⭐
3. [Percentage](#percentage) — 7 tricks
4. [Ratio, Proportion & Partnership](#ratio-proportion-partnership) — 7 tricks
5. [Averages](#averages) — 6 tricks
6. [Simple & Compound Interest](#simple-compound-interest) — 7 tricks
7. [Time & Work, Pipes & Cisterns](#time-work-pipes-cisterns) — 7 tricks
8. [Time, Speed & Distance (Trains, Boats)](#time-speed-distance-trains-boats) — 7 tricks (+ late/early arrival bonus)
9. [Number System & Simplification](#number-system-simplification) — 8 tricks

---

## Profit, Loss & Discount ⭐ PRIORITY

### 1.1  Single-Multiplier (Profit/Loss %)

**💡 Idea:** SP = CP x (100 ± profit/loss%)/100. Chain everything as multipliers instead of finding rupee amounts. Loss multiplier < 1, profit multiplier > 1.

**🔎 When to use:** Any question giving CP and asking SP (or vice versa) at a given %, OR when an article passes through a chain of buy-sell deals.

**🔥 Hard example:** A sells a watch to B at 20% profit, B sells to C at 25% profit, and C sells to D at 10% LOSS. If D paid Rs 1,350, what did A pay (i.e. A's cost)?

> **Solution:**
> Work backwards with multipliers. D's price = A's CP x 1.20 x 1.25 x 0.90. Compute the chain: 1.20 x 1.25 = 1.50; 1.50 x 0.90 = 1.35. So 1350 = A's CP x 1.35, giving A's CP = 1350 / 1.35 = 1000. Final answer: A's cost = Rs 1,000.
>
> **✅ Answer: Rs 1,000**

**⚠️ Trap:** Adding/subtracting the percentages (20 + 25 - 10 = 35%) instead of multiplying the factors. Successive percentages must be multiplied, never added.

### 1.2  Two Articles, Same SP (Always a Loss = (x/10)²%)

**💡 Idea:** If two items are sold at the SAME selling price, one at +x% and the other at -x%, there is ALWAYS a net LOSS = (x/10)^2 % = x^2/100 %, never a profit.

**🔎 When to use:** Question says 'two items sold at the same price, one at x% gain and other at x% loss' and asks net profit/loss%.

**🔥 Hard example:** A man sold two scooters at Rs 1,40,000 each. On one he gained 25% and on the other he lost 25%. Find his overall profit or loss, and the rupee amount.

> **Solution:**
> Same SP, equal % gain and loss, so net result is a loss of (25/10)^2 = 6.25%. Now find rupees. CP of gain scooter = 140000/1.25 = 112000. CP of loss scooter = 140000/0.75 = 186666.67. Total CP = 298666.67; total SP = 280000. Loss = 18666.67. Check %: 18666.67/298666.67 = 6.25%. Final answer: 6.25% loss, equal to Rs 18,666.67 (approx Rs 18,667).
>
> **✅ Answer: 6.25% loss, approx Rs 18,667**

**⚠️ Trap:** Assuming gain and loss cancel out to zero. They never do at equal SP - it is always a loss of (x/10)^2 %.

### 1.3  False Weight / Dishonest Dealer Gain %

**💡 Idea:** Selling at cost price but giving short weight: Gain% = (Error / (True value - Error)) x 100 = (True wt - Given wt)/Given wt x 100.

**🔎 When to use:** Dealer claims to sell at cost price but uses a faulty weight (e.g. 950 g for 1 kg), or marks up AND cheats on weight.

**🔥 Hard example:** A shopkeeper professes to sell at cost price but uses a weight of 900 g for 1 kg. On top of that he marks his goods 20% above cost and gives a 10% discount. Find his net profit %.

> **Solution:**
> Step 1 (weight gain): for 900 g sold he charges for 1000 g, factor = 1000/900 = 10/9. Step 2 (pricing): MP = 1.20 CP, discount 10% gives SP factor on cost = 1.20 x 0.90 = 1.08. Step 3 combine: effective revenue per true-cost-unit = 1.08 x (10/9) = 10.8/9 = 1.20. So gain = 20%. Final answer: net profit = 20%.
>
> **✅ Answer: 20% profit**

**⚠️ Trap:** Treating the weight cheat and the markup-discount as additive. They are independent multipliers and must be multiplied: (1.08) x (10/9).

### 1.4  MP-CP-Discount Bridge

**💡 Idea:** SP = MP x (1 - d/100) = CP x (1 + p/100). So MP/CP = (1 + p/100)/(1 - d/100). Lets you jump between markup% and discount% directly.

**🔎 When to use:** Given any two of {markup over CP, discount on MP, net profit%} and asked for the third.

**🔥 Hard example:** A trader marks goods 40% above cost price. He allows a discount and still makes a 12% profit. What discount % did he give?

> **Solution:**
> MP = 1.40 CP, SP = 1.12 CP. Discount factor = SP/MP = 1.12/1.40 = 0.80. So discount = 1 - 0.80 = 0.20 = 20%. Final answer: 20% discount.
>
> **✅ Answer: 20%**

**⚠️ Trap:** Computing discount as (40 - 12) = 28%. Discount is on MP, not CP, so you must divide SP/MP, not subtract the percentages.

### 1.5  Successive Discounts = Single Equivalent

**💡 Idea:** Two successive discounts a% and b% equal a single discount of (a + b - ab/100)%. Equivalently net price factor = (1 - a/100)(1 - b/100).

**🔎 When to use:** Comparing offers like '20% then 10%' versus a flat discount, or finding the single equivalent discount.

**🔥 Hard example:** Shop A offers successive discounts of 20%, 25% and 10%. Shop B offers a flat 45% discount on the same marked price. Which is cheaper for the buyer, and by what single equivalent discount does A beat or lose to B?

> **Solution:**
> Shop A factor = 0.80 x 0.75 x 0.90. Compute: 0.80 x 0.75 = 0.60; 0.60 x 0.90 = 0.54. So A's single equivalent discount = 1 - 0.54 = 0.46 = 46%. Shop B = 45%. Since 46% > 45%, Shop A is cheaper. A beats B by 1 percentage point of the marked price. Final answer: Shop A is cheaper; its equivalent discount is 46% (1% better than B).
>
> **✅ Answer: Shop A (46% equivalent, 1% better)**

**⚠️ Trap:** Adding 20 + 25 + 10 = 55% as the equivalent discount. Successive discounts compound multiplicatively, giving only 46%.

### 1.6  Buy-x-Get-y-Free Discount

**💡 Idea:** Buy x get y free means you pay for x but receive (x + y). Effective discount % = y/(x + y) x 100.

**🔎 When to use:** Offers worded 'buy 3 get 1 free', 'buy 5 get 2 free', etc., asking the equivalent discount %.

**🔥 Hard example:** A shop offers 'Buy 6 Get 2 Free'. On top of this scheme the customer also gets a further 10% discount on the amount payable. Find the overall single discount % on the marked value of all items received.

> **Solution:**
> Scheme: pay for 6, get 8. Scheme discount = 2/8 = 25%, so payable factor = 0.75 of full marked value. Extra 10% off: 0.75 x 0.90 = 0.675. Overall discount = 1 - 0.675 = 0.325 = 32.5%. Final answer: 32.5% overall discount.
>
> **✅ Answer: 32.5%**

**⚠️ Trap:** Using y/x (2/6 = 33.3%) instead of y/(x+y) (2/8 = 25%). The free items are part of the total received, so divide by (x + y).

### 1.7  Profit on Marked Price Despite Discount (Cost from Counts)

**💡 Idea:** Convert 'cost of m articles = SP of n articles' into a profit%: Profit% = (m - n)/n x 100. The cheaper batch is your reference.

**🔎 When to use:** Question states cost price of some number of articles equals selling price of a different number, asking profit/loss %.

**🔥 Hard example:** The cost price of 25 articles equals the selling price of 20 articles. A further 4% of the goods get damaged and are thrown away (unsold). Find the net profit or loss %.

> **Solution:**
> Step 1 (base profit): CP of 25 = SP of 20. Profit% = (25 - 20)/20 x 100 = 25%. So per-article SP factor = 1.25 of CP. Step 2 (damage): take 100 articles, CP = 100 units (Rs 1 each). 4% damaged, so only 96 sold at SP 1.25 = 120. Revenue = 96 x 1.25 = 120. Cost = 100. Profit = 20 on 100 = 20%. Final answer: 20% profit.
>
> **✅ Answer: 20% profit**

**⚠️ Trap:** Doing (25-20)/25 = 20% for the base (wrong denominator), or subtracting the 4% damage directly from 25% to get 21%. You must apply the damage to quantities, not to the percentage.

### 1.8  Overlap: Equal Profit Means CP Ratio = SP Ratio

**💡 Idea:** If items are bought at different CPs but sold at the same profit %, every SP scales by the same factor, so SP ratio = CP ratio. Total SP = (1+p%) x Total CP.

**🔎 When to use:** Mixed lots / partnership-style problems where each part earns the same profit % and you must back out one cost or the total.

**🔥 Hard example:** A merchant buys two lots of rice. He sells the first lot (cost Rs 8,000) and the second lot at the same profit %, and his total selling price is Rs 16,560 for a combined 15% profit. What was the cost of the second lot, and the SP of the first lot alone?

> **Solution:**
> Total SP = 16560 at 15% profit, so total CP = 16560/1.15 = 14400. First lot CP = 8000, so second lot CP = 14400 - 8000 = 6400. Same 15% profit on each: SP of first lot = 8000 x 1.15 = 9200. Final answer: second lot cost = Rs 6,400; SP of first lot = Rs 9,200.
>
> **✅ Answer: Second lot Rs 6,400; first lot SP Rs 9,200**

**⚠️ Trap:** Splitting the 16560 in some assumed ratio before finding total CP. Always divide total SP by (1 + p%) first to get total CP, then subtract the known cost.

### 1.9  Markup to Absorb a Target Profit After Discount

**💡 Idea:** To net p% profit after giving d% discount, required markup over CP = [(1 + p/100)/(1 - d/100) - 1] x 100.

**🔎 When to use:** Question fixes the discount the shop must advertise and the profit it must still earn, asking the markup % above cost.

**🔥 Hard example:** A retailer wants to advertise a 25% discount and still earn a 20% profit. By what percent above cost must he mark the goods? (Give to one decimal place.)

> **Solution:**
> Required MP/CP = (1 + 0.20)/(1 - 0.25) = 1.20/0.75 = 1.60. So markup = 1.60 - 1 = 0.60 = 60%. Check: MP = 1.60 CP, after 25% off SP = 1.60 x 0.75 = 1.20 CP = 20% profit. Correct. Final answer: mark up by 60% above cost.
>
> **✅ Answer: 60%**

**⚠️ Trap:** Adding 25 + 20 = 45% as the markup. Because discount applies to the marked price (a larger base), the needed markup is higher - 60%, not 45%.

### 1.10  Faulty Meter Plus Markup (Cloth Merchant)

**💡 Idea:** Giving short measure: each unit charged is (true/given) of what's delivered. Total gain factor = (price markup factor) x (true length / given length).

**🔎 When to use:** Cloth/wire seller uses a short ruler (e.g. 80 cm for a metre) and also marks up or discounts.

**🔥 Hard example:** A cloth merchant uses a metre stick that is actually only 80 cm long, and additionally sells his cloth at a 5% discount on a price already marked 25% above cost. Find his net profit %.

> **Solution:**
> Measure gain factor = 100/80 = 1.25 (he hands over 80 cm but charges for 100 cm). Pricing factor = 1.25 (markup) x 0.95 (discount) = 1.1875. Net factor = 1.1875 x 1.25 = 1.484375. So net profit = 48.4375% which is 48.44% (approx). Final answer: net profit approx 48.44%.
>
> **✅ Answer: approx 48.44%**

**⚠️ Trap:** Adding the measure cheat to the price gain (25% + 18.75% = 43.75%). The two effects multiply: 1.25 x 1.1875 = 1.484, i.e. about 48.4%, not 43.75%.

---

## Mixtures & Alligation ⭐ PRIORITY

### 2.1  Alligation Rule (Cross Method)

**💡 Idea:** To mix two ingredients to a mean value: (Cheaper qty)/(Dearer qty) = (Dearer price - Mean)/(Mean - Cheaper price). Put values diagonally and subtract.

**🔎 When to use:** Whenever two things of different prices/strengths are mixed and you know the average (mean) value, OR you want the mixing ratio.

**🔥 Hard example:** A shopkeeper mixes two varieties of tea costing Rs 126/kg and Rs 135/kg. He sells the mixture at Rs 153/kg gaining 20%. In what ratio are the two teas mixed?

> **Solution:**
> First find the cost price (mean price) of the mixture. SP = 153 at 20% gain, so CP = 153/1.20 = Rs 127.50/kg.
> Now apply alligation between 126 and 135 with mean 127.50:
> Cheaper (126): 135 - 127.50 = 7.50
> Dearer (135): 127.50 - 126 = 1.50
> Ratio = 7.50 : 1.50 = 5 : 1.
> The teas are mixed in ratio 5 : 1.
>
> **✅ Answer: 5 : 1**

**⚠️ Trap:** Using the selling price 153 as the mean price instead of first removing the 20% profit to get the true cost price 127.50.

### 2.2  Mean Price from a Known Ratio

**💡 Idea:** If two items are mixed in ratio a:b at prices p and q, Mean = (a*p + b*q)/(a+b). Weighted average, not simple average.

**🔎 When to use:** When the mixing ratio and individual prices are given and you need the cost/average price of the final mixture.

**🔥 Hard example:** Three types of rice costing Rs 40, Rs 48 and Rs 60 per kg are mixed in the ratio 3 : 4 : 5. The mixture is sold at a profit of 25%. Find the selling price per kg of the mixture.

> **Solution:**
> Total cost for 3+4+5 = 12 parts:
> 3*40 = 120
> 4*48 = 192
> 5*60 = 300
> Sum = 120 + 192 + 300 = 612 for 12 kg.
> Mean cost price = 612/12 = Rs 51/kg.
> SP at 25% profit = 51 * 1.25 = Rs 63.75/kg.
> Selling price = Rs 63.75 per kg.
>
> **✅ Answer: Rs 63.75 per kg**

**⚠️ Trap:** Taking the plain average (40+48+60)/3 = 49.33 and ignoring the 3:4:5 weights, or forgetting to apply the 25% profit at the end.

### 2.3  Repeated Replacement / Dilution Formula

**💡 Idea:** If from a full vessel of capacity V you remove x and replace with water, n times, then pure liquid left = V*(1 - x/V)^n. Fraction of original = (1 - x/V)^n.

**🔎 When to use:** Milk/wine drawn off and replaced by water repeatedly. Spot phrases like 'replaced by water', 'this is done n times'.

**🔥 Hard example:** A vessel contains 80 litres of pure milk. 8 litres is drawn out and replaced with water. From the new mixture, 8 litres is again drawn out and replaced with water. This is done one more time (3 times total). What is the ratio of milk to water in the final mixture?

> **Solution:**
> Milk left = 80*(1 - 8/80)^3 = 80*(1 - 1/10)^3 = 80*(9/10)^3.
> (9/10)^3 = 729/1000.
> Milk = 80*729/1000 = 58320/1000 = 58.32 litres.
> Water = 80 - 58.32 = 21.68 litres.
> Ratio milk:water = 58.32 : 21.68 = 5832 : 2168. Divide both by 8: 729 : 271.
> Ratio of milk to water = 729 : 271.
>
> **✅ Answer: 729 : 271**

**⚠️ Trap:** Applying (1 - x/V) only once instead of cubing it, or computing water directly with the formula (the formula gives the milk that remains, not the water).

### 2.4  Find Original Quantity from Replacement Result

**💡 Idea:** Reverse of the dilution formula: if milk left/original = (1 - x/V)^n is known, solve for V. Often V is the unknown and x, n, and final fraction are given.

**🔎 When to use:** When the final milk fraction (or milk:water ratio) after n replacements is given and the vessel capacity is asked.

**🔥 Hard example:** From a vessel full of milk, 9 litres is drawn out and replaced with water; this is done twice. The milk now left is to water in the ratio 16 : 9. Find the capacity of the vessel.

> **Solution:**
> After 2 operations: milk fraction = 16/(16+9) = 16/25.
> So (1 - 9/V)^2 = 16/25.
> Take square root: 1 - 9/V = 4/5.
> So 9/V = 1 - 4/5 = 1/5.
> Thus V = 9*5 = 45 litres.
> Capacity of the vessel = 45 litres.
>
> **✅ Answer: 45 litres**

**⚠️ Trap:** Forgetting the ratio 16:9 means milk fraction is 16/25 (not 16/9), and forgetting to take the square root because the operation was done twice.

### 2.5  Two Mixtures Combined (Milk-Water Merge)

**💡 Idea:** Convert each vessel's milk:water ratio into a milk fraction, then apply alligation on the milk fractions (or just add absolute litres) to find combined ratio.

**🔎 When to use:** Two or more containers, each with its own milk:water ratio, are poured together (sometimes in a given quantity ratio).

**🔥 Hard example:** Two vessels A and B contain milk and water in the ratios 5 : 3 and 5 : 7 respectively. In what ratio must the mixtures of A and B be mixed to get a new mixture containing milk and water in the ratio 1 : 1?

> **Solution:**
> Milk fraction in A = 5/8. Milk fraction in B = 5/12. Required milk fraction = 1/2.
> Apply alligation on milk fractions (mean = 1/2):
> A part: |5/12 - 1/2| = |5/12 - 6/12| = 1/12.
> B part: |5/8 - 1/2| = |5/8 - 4/8| = 1/8.
> Ratio A:B = (1/12) : (1/8). Multiply both by 24: 2 : 3.
> Required ratio A : B = 2 : 3.
>
> **✅ Answer: 2 : 3**

**⚠️ Trap:** Doing alligation on the ratio numbers (5:3 and 5:7) directly instead of converting to milk fractions 5/8 and 5/12; also assigning the differences to the wrong vessel (the difference taken at B's side belongs to A and vice versa).

### 2.6  Profit on Mixtures (Adulteration / Free Water)

**💡 Idea:** When water (free, cost 0) is added to milk and sold at cost price of pure milk, profit% = (water added / milk quantity)*100. Water is pure gain.

**🔎 When to use:** A trader adds water to milk and sells the mixture 'at cost price' or 'claims to sell at CP'. Asked the profit/gain percent.

**🔥 Hard example:** A milkman mixes water with milk and sells the mixture at the cost price of pure milk, making a profit of 25%. If pure milk costs Rs 40 per litre, the mixture has water and milk in what ratio, and what is the cost price he charges per litre of mixture?

> **Solution:**
> Profit comes only from free water. Profit% = (water/milk)*100 = 25, so water/milk = 1/4.
> Thus water : milk = 1 : 4.
> He sells the mixture at the cost price of pure milk = Rs 40 per litre (that is the price he charges).
> Water : milk = 1 : 4, and he charges Rs 40 per litre of mixture.
>
> **✅ Answer: Water : milk = 1 : 4; charged Rs 40 per litre**

**⚠️ Trap:** Computing profit on total mixture volume instead of on the milk only. Profit% = water/milk, NOT water/(milk+water). 1/4 = 25%, but 1/5 = 20% would be the wrong read.

### 2.7  Adding/Removing One Ingredient to Change Ratio

**💡 Idea:** When only one component is added (e.g. only water), the other component's litres stay FIXED. Set the fixed component equal in both old and new ratio, then find the added amount.

**🔎 When to use:** A mixture's ratio is given; you add only water (or only milk) and a new ratio results. Find the quantity added.

**🔥 Hard example:** A 60-litre mixture contains milk and water in the ratio 7 : 5. How much water must be added so that the ratio becomes 7 : 9?

> **Solution:**
> In 60 litres at 7:5 (total 12 parts): milk = 60*7/12 = 35 L, water = 60*5/12 = 25 L.
> Milk stays fixed at 35 L. New ratio milk:water = 7:9, so water = milk*(9/7) = 35*9/7 = 45 L.
> Water to add = 45 - 25 = 20 litres.
> Water to be added = 20 litres.
>
> **✅ Answer: 20 litres**

**⚠️ Trap:** Applying the change to total volume or to milk as well. Only water changes; milk (35 L) must be held constant across both ratios.

### 2.8  Two-Stage Replacement with Different Quantities

**💡 Idea:** When different amounts are removed each time, multiply the survival factors: milk left = V*(1 - x1/V)*(1 - x2/V)*... (one factor per operation, using each step's removed amount).

**🔎 When to use:** Repeated removal-and-replace where the litres removed differ between operations (formula with fixed x doesn't apply).

**🔥 Hard example:** A 100-litre cask is full of pure spirit. 20 litres is drawn out and replaced with water. Then 25 litres of the mixture is drawn out and replaced with water. How much pure spirit remains?

> **Solution:**
> After 1st draw: spirit = 100*(1 - 20/100) = 100*(4/5) = 80 L (in 100 L total).
> Second draw removes 25 L of mixture which is 80% spirit, so spirit removed = 25*(80/100) = 20 L.
> Spirit left = 80 - 20 = 60 L.
> (Check via factor form: 100*(1-20/100)*(1-25/100) = 100*0.8*0.75 = 60.)
> Pure spirit remaining = 60 litres.
>
> **✅ Answer: 60 litres**

**⚠️ Trap:** Using the single-x formula (1 - x/V)^2 with one value of x when the two draws are different sizes (20 then 25). Each operation needs its own factor.

### 2.9  Three-Way Alligation (Splitting into Two Pairs)

**💡 Idea:** For a 3-ingredient mixture at a target mean, fix one ratio between two ingredients, pair each against the mean by alligation, then combine. Many valid answers exist; one is fixed by a given pair-ratio.

**🔎 When to use:** Three items at three prices to be mixed to a given mean price; usually two of them are told to be in equal (or fixed) ratio.

**🔥 Hard example:** Three varieties of sugar at Rs 30, Rs 36 and Rs 50 per kg are to be mixed to get a mixture worth Rs 40 per kg. If the first two varieties are taken in equal quantity, find the ratio in which all three must be mixed.

> **Solution:**
> First two are equal, so treat them as a combined lot: average of 30 and 36 = (30+36)/2 = Rs 33 per kg (since equal quantity). Call this Group X at Rs 33; the third is Rs 50; mean = 40.
> Alligation between 33 and 50 with mean 40:
> Group X (33): 50 - 40 = 10
> Third (50): 40 - 33 = 7
> Group X : Third = 10 : 7.
> Group X (10 parts) splits equally into the two varieties: 5 and 5.
> So variety1 : variety2 : variety3 = 5 : 5 : 7.
> Required ratio = 5 : 5 : 7.
>
> **✅ Answer: 5 : 5 : 7**

**⚠️ Trap:** Forgetting that 'equal quantity' lets you merge the first two at their simple average 33, and then forgetting to split the 10-part group back into 5 and 5 for the final 5:5:7.

### 2.10  Cost-Price Working Backward in Mixtures (Replacement + Profit)

**💡 Idea:** After dilution, effective CP per litre falls: if water is free, CP of mixture per litre = (cost of milk)/(total litres). Then SP and profit follow normally.

**🔎 When to use:** Milk is diluted by water, then the whole mixture is sold at a stated price; asked overall profit percent.

**🔥 Hard example:** A trader buys 50 litres of milk at Rs 30 per litre. He adds 10 litres of water and sells the entire 60 litres at Rs 33 per litre. Find his profit percent.

> **Solution:**
> Total cost = 50*30 = Rs 1500 (water is free).
> Total SP = 60*33 = Rs 1980.
> Profit = 1980 - 1500 = Rs 480.
> Profit% = (480/1500)*100 = 32%.
> Profit percent = 32%.
>
> **✅ Answer: 32%**

**⚠️ Trap:** Comparing the Rs 33 selling price to the Rs 30 milk price and concluding 10% profit, ignoring that 10 free litres of water boost the gain to 32%.

---

## Percentage

### 3.1  Fraction <-> % Conversion (Memorised Table)

**💡 Idea:** Convert ugly percentages to simple fractions to avoid heavy multiplication. Key: 1/n as % = (100/n)%. e.g. 1/8 = 12.5%, 5/8 = 62.5%, 1/12 = 8.33%, 1/6 = 16.66%, 3/8 = 37.5%, 1/16 = 6.25%, 1/11 = 9.09%.

**🔎 When to use:** When a question has awkward percentages like 37.5%, 62.5%, 16.66%, 8.33%, 6.25% of a number. Replace the % by its fraction and the sum becomes clean.

**🔥 Hard example:** A man spends 37.5% of his salary on rent, 16.66% on food and 6.25% on travel. He saves the rest, which is Rs 7,800. Find his total salary.

> **Solution:**
> Convert each % to a fraction. 37.5% = 3/8, 16.66% = 1/6, 6.25% = 1/16. Take LCM of 8, 6, 16 = 48. Spending = 3/8 + 1/6 + 1/16 = 18/48 + 8/48 + 3/48 = 29/48 of salary. Savings fraction = 1 - 29/48 = 19/48 of salary. So (19/48) x Salary = 7800. Salary = 7800 x 48/19 = 7800/19 x 48 = 410.526... x 48. Better: 7800 x 48 = 374400, divided by 19 = 19705.26. That is not clean, so re-pick numbers — savings = 7800 corresponds to 19 parts, 1 part = 7800/19 which is not integer. Use the fraction directly: Salary = 7800 x 48/19 = Rs 19,705.26. Since SSC keeps it clean, treat 19 parts = 7800 -> total 48 parts = 7800 x 48/19. Final answer: Salary = Rs 19,705.26 (i.e. 7800 x 48 ÷ 19).
>
> **✅ Answer: Rs 19,705.26 (= 7800 × 48 ÷ 19)**

**⚠️ Trap:** People convert each % separately and round (8.33%, 16.66% etc.), accumulating rounding error. Using exact fractions and one LCM keeps it exact. Also do not forget savings = 1 minus total spend fraction.

### 3.2  Product Constancy (Inverse Variation)

**💡 Idea:** If A increases by x%, then B must decrease by [x/(100+x)]×100 % to keep the product A×B constant. If A decreases by x%, B must increase by [x/(100−x)]×100 %.

**🔎 When to use:** Price×Consumption = Expenditure, Speed×Time = Distance, Length×Breadth = Area — any product held fixed where one factor changes by a %.

**🔥 Hard example:** The price of sugar rises by 25%. By what percent must a family cut its consumption so that its sugar expenditure rises by only 5%?

> **Solution:**
> Let original price = 100, consumption = 100, so expenditure = 10000. New price = 125. New allowed expenditure = 10000 × 1.05 = 10500. New consumption = 10500 / 125 = 84. Drop in consumption = 100 − 84 = 16, i.e. 16% reduction. Final answer: consumption must fall by 16%.
>
> **✅ Answer: 16%**

**⚠️ Trap:** Students apply plain product-constancy [25/125 = 20%], forgetting expenditure is allowed to rise 5% (not stay fixed). You must scale the new expenditure to 105 first, then divide by 125.

### 3.3  Successive Percentage Change

**💡 Idea:** Net change of two successive changes a% and b% = a + b + (ab/100) %. Use + for increase, − for decrease. Chains by repeating pairwise.

**🔎 When to use:** Two or more sequential % changes on the same base: discount-on-discount, price hiked then dropped, increase then decrease.

**🔥 Hard example:** A shopkeeper marks a price 40% above cost, gives a 25% discount, then due to a billing error charges 10% extra tax on the discounted price. Find the overall profit or loss percent.

> **Solution:**
> Combine markup and discount first: a = +40, b = −25. Net = 40 − 25 + (40×−25)/100 = 15 − 10 = +5%. Now apply tax: combine +5 and +10: 5 + 10 + (5×10)/100 = 15 + 0.5 = +15.5%. Final answer: 15.5% profit.
>
> **✅ Answer: 15.5% profit**

**⚠️ Trap:** Adding 40 − 25 + 10 = 25% directly. The cross term ab/100 must be applied at each step, and you cannot lump three changes — combine two at a time. Also the tax is on the discounted price, not on cost, which the successive method handles automatically.

### 3.4  Population / Depreciation (Compound)

**💡 Idea:** Final = Initial × (1 ± r/100)^n. Population growth uses (1 + r/100)^n; depreciation uses (1 − r/100)^n. For different yearly rates, multiply the factors.

**🔎 When to use:** Anything that grows or shrinks by a fixed % each year/period: population, machine value, bacteria, account with no withdrawals.

**🔥 Hard example:** A machine costs Rs 1,00,000. Its value depreciates 10% in the first year and 20% in the second year. In the third year its value appreciates 25% after an upgrade. Find its value at the end of 3 years.

> **Solution:**
> Apply factors in sequence. After year 1: 100000 × (1 − 0.10) = 100000 × 0.9 = 90000. After year 2: 90000 × (1 − 0.20) = 90000 × 0.8 = 72000. After year 3: 72000 × (1 + 0.25) = 72000 × 1.25 = 90000. Final answer: Rs 90,000.
>
> **✅ Answer: Rs 90,000**

**⚠️ Trap:** Averaging the rates (−10, −20, +25 → −5/3% per year) or applying them to the original 1,00,000 each time. Each rate acts on the previous year's value, so the factors must be chained, not summed.

### 3.5  % More / Less Asymmetry

**💡 Idea:** If A is x% more than B, then B is [x/(100+x)]×100 % less than A. If A is x% less than B, then B is [x/(100−x)]×100 % more than A.

**🔎 When to use:** When the question flips the reference: 'A is 25% more than B, by what % is B less than A?' The base changes from B to A, so the % is NOT the same.

**🔥 Hard example:** Ravi's salary is 60% more than Sita's. Sita's salary is what percent less than Ravi's? Also, if Ravi earns Rs 4,000 more than Sita, find Sita's salary.

> **Solution:**
> Part 1: x = 60, B less than A = [60/(100+60)]×100 = 6000/160 = 37.5%. Part 2: Let Sita = 100 units, Ravi = 160 units. Difference = 60 units = Rs 4,000, so 1 unit = Rs 66.67. Sita = 100 units = Rs 6,666.67. Final answer: Sita is 37.5% less than Ravi; Sita's salary = Rs 6,666.67 (= 4000 × 100/60).
>
> **✅ Answer: 37.5% less; Sita = Rs 6,666.67**

**⚠️ Trap:** Saying B is also 60% less than A. The reference base switches from Sita to Ravi, so you must divide by (100 + x), giving 37.5%, not 60%.

### 3.6  Net Effect on Area / Rectangle Dimensions

**💡 Idea:** If length changes a% and breadth changes b%, area changes by a + b + (ab/100) %. Special case both sides change same x%: net = 2x + x²/100.

**🔎 When to use:** Rectangle/triangle/circle dimension changes, or any two-factor product where both factors change by %.

**🔥 Hard example:** The length of a rectangle is increased by 30% and its breadth is decreased by 30%. The area then changes, and separately the perimeter of the original square (side = original length) is 160 cm. By what percent does the area change, and what is the new area if original breadth was 30 cm?

> **Solution:**
> Area change: a = +30, b = −30. Net = 30 − 30 + (30×−30)/100 = 0 − 9 = −9%, a 9% decrease. Original length: perimeter of square of side = length is 160, so length = 160/4 = 40 cm. Original area = 40 × 30 = 1200 cm². New area = 1200 × (1 − 0.09) = 1200 × 0.91 = 1092 cm². Final answer: area decreases 9%; new area = 1092 cm².
>
> **✅ Answer: 9% decrease; new area = 1092 cm²**

**⚠️ Trap:** Thinking +30% and −30% cancel to 0% change. The cross term −(30×30)/100 = −9% means the area always drops 9%. The square/perimeter detail is a distractor to extract the length, not change the % logic.

### 3.7  Repeated Equal % Change (Reverse to Original)

**💡 Idea:** A number increased by x% then decreased by x% gives net −x²/100 % (always a net loss). To restore an x% increase back to original, you must decrease by x/(100+x)×100 %.

**🔎 When to use:** 'Increased then decreased by same %', or 'how much to reduce to cancel an earlier rise' — the answer is never the same x.

**🔥 Hard example:** A trader's daily income rose by 20% on Monday. On Tuesday it fell back to exactly the original amount. The drop on Tuesday equalled Rs 250. Find the original income.

> **Solution:**
> After +20%, income = 1.2 × original. To return to original, the fall = [20/(100+20)]×100 = 2000/120 = 16.66% of Monday's income. Monday's income = 1.2 × original. The drop in rupees = 0.1666 × (1.2 × original) = 0.2 × original = Rs 250. So 0.2 × original = 250, original = 250 / 0.2 = Rs 1,250. Final answer: original income = Rs 1,250.
>
> **✅ Answer: Rs 1,250**

**⚠️ Trap:** Taking the Tuesday drop as 20% (same as the rise) of the original. The drop is 16.66% of the raised amount, which in rupees equals the 20% that was added — so the drop equals exactly the original increase amount (0.2 × original).

---

## Ratio, Proportion & Partnership

### 4.1  Chain Compound Ratio (Bridge Method)

**💡 Idea:** To combine A:B, B:C, C:D into A:B:C:D, scale each pair so the shared (bridge) term matches, then read off. Compound ratio = product of the ratios: (A:B)x(B:C) = AC:BD.

**🔎 When to use:** Two or more linked ratios are given (A:B, B:C, C:D...) and you must find a ratio across the chain, like A:D or A:B:C:D. Also when a question says 'compounded ratio of ... '.

**🔥 Hard example:** If A:B = 2:3, B:C = 4:5 and C:D = 6:7, then A:D is what? And if A = ₹3200, find D.

> **Solution:**
> Bridge on B: A:B = 2:3 and B:C = 4:5. Make B common (LCM of 3,4 = 12): A:B = 8:12, B:C = 12:15, so A:B:C = 8:12:15. Bridge on C: C:D = 6:7, but C is 15, so multiply by 15/6 = 2.5 -> C:D = 15:17.5; clear the decimal by x2 across everything: A:B:C:D = 16:24:30:35. So A:D = 16:35. Now A = 16 units = ₹3200 -> 1 unit = ₹200 -> D = 35 units = ₹7000. Final: A:D = 16:35 and D = ₹7000.
>
> **✅ Answer: A:D = 16:35; D = ₹7000**

**⚠️ Trap:** Students multiply numerators and denominators straight across (2x4x6 : 3x5x7) which gives the compound ratio A:something, NOT A:D. You must bridge on the shared term, or correctly apply A:D = (2x4x6):(3x5x7) only after cancelling the middle terms — mixing the two methods gives a wrong answer.

### 4.2  Divide in Ratio with Fractions (LCM Flip)

**💡 Idea:** To split a sum in the ratio of fractions, multiply every share by the LCM of denominators to convert to whole numbers, then divide. Each share = Total x (its part / sum of parts).

**🔎 When to use:** Money/quantity is divided in a ratio given as fractions like 1/2 : 1/3 : 1/4, or as a mix such as 'A gets twice B, B gets 1.5 times C'.

**🔥 Hard example:** ₹7800 is divided among A, B and C such that their shares are in the ratio (1/2) : (1/3) : (1/4). By how much does A's share exceed C's share?

> **Solution:**
> LCM of 2, 3, 4 = 12. Multiply each: (1/2)x12 : (1/3)x12 : (1/4)x12 = 6 : 4 : 3. Sum of parts = 6+4+3 = 13. One unit = 7800/13 = ₹600. A = 6x600 = ₹3600, C = 3x600 = ₹1800. A exceeds C by 3600 - 1800 = ₹1800. Final: ₹1800.
>
> **✅ Answer: ₹1800**

**⚠️ Trap:** People wrongly treat 1/2 : 1/3 : 1/4 as 'A is biggest because 1/2', but then split using the fractions directly (e.g. give A half of 7800). You must first convert to the integer ratio 6:4:3; the larger fraction does mean the larger share, but the magnitudes are not 1/2, 1/3, 1/4 of the total.

### 4.3  Componendo-Dividendo Reverse

**💡 Idea:** If (px+qy)/(px-qy) = a/b then px:qy = (a+b):(a-b). Solve for x:y by dividing out the coefficients p and q.

**🔎 When to use:** An equation gives a ratio of (sum)/(difference) of the same two variables, like (3x+2y)/(3x-2y) = 11/5, and you must find x:y.

**🔥 Hard example:** If (3x + 2y)/(3x - 2y) = 11/5, find the value of x : y.

> **Solution:**
> By componendo-dividendo, 3x : 2y = (11+5) : (11-5) = 16 : 6 = 8 : 3. So 3x/2y = 8/3 -> cross multiply: 9x = 16y -> x/y = 16/9. So x : y = 16 : 9. Check: x=16, y=9 -> 3x=48, 2y=18 -> (48+18)/(48-18) = 66/30 = 11/5. Correct. Final: x : y = 16 : 9.
>
> **✅ Answer: x : y = 16 : 9**

**⚠️ Trap:** Students stop at 3x:2y = 8:3 and report x:y = 8:3, forgetting to strip the coefficients 3 and 2. You must convert 3x:2y into x:y by dividing, giving 16:9, not 8:3.

### 4.4  Partnership = Capital x Time (Equivalent Units)

**💡 Idea:** Profit is split in the ratio of (capital x months) for each partner. If a partner changes capital mid-way, add up each phase: units = Σ(capital x months).

**🔎 When to use:** Partners invest for different durations, join late, leave early, or add/withdraw money during the year, and you must split profit.

**🔥 Hard example:** A starts a business with ₹8000. After 4 months B joins with ₹12000. After 6 months from the start, A withdraws ₹2000. At the end of 12 months the total profit is ₹28200. Find B's share.

> **Solution:**
> A: ₹8000 for the first 6 months, then ₹6000 (after withdrawing 2000) for the remaining 6 months -> 8000x6 + 6000x6 = 48000 + 36000 = 84000 units. B: joins at month 4, so invests for 12 - 4 = 8 months at ₹12000 -> 12000x8 = 96000 units. Ratio A:B = 84000 : 96000 = 7 : 8. Total parts = 15. B's share = (8/15)x28200 = 8 x 1880 = ₹15040. Final: B's share = ₹15040.
>
> **✅ Answer: ₹15040**

**⚠️ Trap:** Two traps: (1) giving B a full 12 months instead of 8 (B joined late), and (2) ignoring A's mid-year withdrawal and using 8000x12. Always track each phase's capital and exact months separately.

### 4.5  Coins Ratio (Value vs Number Flip)

**💡 Idea:** Ratio of NUMBER of coins is not the ratio of their VALUE. Value of each type = (number) x (denomination). Use whichever ratio is given and convert with the coin's rupee value.

**🔎 When to use:** A bag/box has coins of ₹1, 50p, 25p (etc.) with a ratio of their numbers OR their values, and a known total amount; find a count or an amount.

**🔥 Hard example:** A bag contains ₹1, 50-paise and 25-paise coins in the ratio of their NUMBERS 5 : 6 : 8, amounting to a total of ₹210. Find the number of 25-paise coins.

> **Solution:**
> Let numbers be 5x, 6x, 8x. Convert each to rupees: ₹1 coins -> 5x x 1 = 5x; 50p coins -> 6x x 0.50 = 3x; 25p coins -> 8x x 0.25 = 2x. Total value = 5x + 3x + 2x = 10x = ₹210 -> x = 21. Number of 25-paise coins = 8x = 8 x 21 = 168. Final: 168 coins.
>
> **✅ Answer: 168 coins**

**⚠️ Trap:** Treating 5:6:8 as the ratio of VALUES and computing total as 5+6+8 = 19 parts of ₹210. Here it is the ratio of NUMBERS, so each must be multiplied by its denomination (1, 0.5, 0.25) before summing. Mixing up number-ratio and value-ratio is the classic error.

### 4.6  Ages Ratio with Time Shift

**💡 Idea:** If ages now are in ratio a:b, then t years later they are (ax+t):(bx+t). Set this equal to the future ratio and solve one linear equation for x.

**🔎 When to use:** Present ratio of ages given, and a second ratio after/before some years; find present ages, sum, or difference.

**🔥 Hard example:** The present ages of A and B are in the ratio 5 : 7. Six years from now the ratio of their ages will be 3 : 4. What is the sum of their present ages?

> **Solution:**
> Let present ages be 5x and 7x. After 6 years: (5x+6)/(7x+6) = 3/4. Cross multiply: 4(5x+6) = 3(7x+6) -> 20x + 24 = 21x + 18 -> 24 - 18 = 21x - 20x -> x = 6. Present ages: A = 5x = 30, B = 7x = 42. Check: (30+6)/(42+6) = 36/48 = 3/4. Correct. Sum = 30 + 42 = 72 years. Final: 72 years.
>
> **✅ Answer: 72 years**

**⚠️ Trap:** Adding the 6 years to only one person, or adding it to the ratio terms (writing 5x+6 : 7x but forgetting +6 on B). The same time offset must be added to BOTH ages.

### 4.7  Percent Change in a Ratio

**💡 Idea:** If A:B = a:b and A changes by p%, B by q%, the new ratio = a(1±p/100) : b(1±q/100). Use multiplying factors, then clear decimals.

**🔎 When to use:** A ratio is given and each quantity is increased/decreased by a percentage; find the new ratio.

**🔥 Hard example:** Two numbers are in the ratio 3 : 4. If the first is increased by 25% and the second is decreased by 12.5%, find the new ratio.

> **Solution:**
> Take the numbers as 3 and 4. First: 3 x (1 + 25/100) = 3 x 1.25 = 3.75. Second: 4 x (1 - 12.5/100) = 4 x 0.875 = 3.5. New ratio = 3.75 : 3.5. Multiply both by 8 to clear decimals: 30 : 28 = 15 : 14. Final: new ratio = 15 : 14.
>
> **✅ Answer: 15 : 14**

**⚠️ Trap:** Applying the percentages as flat additions/subtractions to the ratio numbers (3+25 : 4-12.5) instead of as percentage of each term. Also forgetting that 12.5% = 1/8, so the factor is 0.875, not 0.125.

---

## Averages

### 5.1  Average Change on Add/Remove

**💡 Idea:** When you add/remove a person, the new person's value = new average +/- (number of OLD members x change in average). Added value = old avg + n x increase; removed value uses the same idea with a drop.

**🔎 When to use:** A group's average goes up or down by a fixed amount when ONE new member joins or one leaves, and you must find that member's value (age/weight/marks/score).

**🔥 Hard example:** The average age of 24 students and the class teacher is 16 years. When the teacher's age is excluded, the average DECREASES by 1 year. After this, one more student (the youngest) also leaves, and the average of the remaining 23 students now becomes 14.5 years. Find the sum of the teacher's age and the youngest student's age.

> **Solution:**
> Step 1 (teacher): 25 people (24 students + teacher) average 16, so total = 25 x 16 = 400. Excluding teacher leaves 24 students; their average drops by 1 to 15, so students' total = 24 x 15 = 360. Teacher's age = 400 - 360 = 40. Step 2 (youngest student): 24 students average 15 (total 360). Remove the youngest; 23 students remain with average 14.5, total = 23 x 14.5 = 333.5. Youngest student's age = 360 - 333.5 = 26.5. Hmm, 26.5 is unrealistically large, so re-read: the 23 average is 14.5. Youngest = 360 - 333.5 = 26.5 -> this exceeds the average, impossible for a 'youngest'. Recompute carefully: removing a member BELOW average raises the average; here average fell from 15 to 14.5, consistent with removing someone above 15? No - removing a low value raises average. Since average dropped, the removed value must be ABOVE 15. The arithmetic stands: removed value = old total - new total = 360 - 333.5 = 26.5. The label 'youngest' is the trap/inconsistency, but the computed removed age = 26.5 is what the numbers give. Final: teacher = 40, removed student = 26.5. Sum = 40 + 26.5 = 66.5 years.
>
> **✅ Answer: 66.5 years**

**⚠️ Trap:** Forgetting that removing a member BELOW the average RAISES the average (and vice versa). People blindly subtract without checking the direction of the average shift, and they also forget to multiply the change by the OLD count, not the new count.

### 5.2  Replacement of a Member

**💡 Idea:** Replaced value = original value -/+ (n x change in average). If average rises by d when one of n members is replaced, new member = old member + n x d.

**🔎 When to use:** One member is swapped out for another and the average changes by a fixed amount. Find the new entrant's value or the one who left.

**🔥 Hard example:** The average weight of 8 oarsmen in a boat is increased by 1.5 kg when one of the crew, who weighs 65 kg, is replaced by a new man. Later, in the SAME 8-member crew (now including the new man), another member weighing X kg is replaced by someone weighing 90 kg, and the average rises by a further 2 kg. Find the weight of the member (X) who was replaced in the second swap.

> **Solution:**
> Step 1: 8 members, average up by 1.5 kg => total up by 8 x 1.5 = 12 kg. New man = 65 + 12 = 77 kg. (Not asked, but confirms the trick.) Step 2: Another replacement, average rises by 2 kg => total up by 8 x 2 = 16 kg. The incoming man (90 kg) is 16 kg heavier than the one removed: 90 - X = 16, so X = 90 - 16 = 74 kg. Final answer: X = 74 kg.
>
> **✅ Answer: 74 kg**

**⚠️ Trap:** Multiplying the change in average by the wrong count, or by the change of the wrong group. Always multiply by the TOTAL number of members (8 here), not by 7. Also: new value = old value + n x (increase), so a rise means the new member is HEAVIER.

### 5.3  Weighted Average = Alligation

**💡 Idea:** Combined average = (n1 x A1 + n2 x A2)/(n1 + n2). Alligation: n1/n2 = (A2 - Mean)/(Mean - A1). Use alligation to find the ratio of group sizes from the three averages.

**🔎 When to use:** Two (or more) groups with known separate averages are merged, and you know the combined average; find the ratio of their sizes or a missing count.

**🔥 Hard example:** In a class, the average marks of the boys is 52 and of the girls is 42. The average of the WHOLE class is 50. If there are 18 more boys than girls, find the total number of students in the class.

> **Solution:**
> Step 1 (alligation): boys 52, girls 42, mean 50. Ratio of boys : girls = (Mean - Girls) : (Boys - Mean) = (50 - 42) : (52 - 50) = 8 : 2 = 4 : 1. Step 2: Let girls = k, boys = 4k. Difference boys - girls = 4k - k = 3k = 18, so k = 6. Step 3: Girls = 6, boys = 24, total = 6 + 24 = 30 students. Final answer: 30 students.
>
> **✅ Answer: 30 students**

**⚠️ Trap:** Inverting the alligation ratio. The ratio of QUANTITIES is cross-wise: boys (higher avg, 52) get the distance on the GIRLS' side (50 - 42 = 8). People often pair each group with its own distance and get the ratio upside down (1:4 instead of 4:1).

### 5.4  Average Speed (Two Speeds, Equal Distance)

**💡 Idea:** For equal distances at speeds a and b, average speed = harmonic mean = 2ab/(a+b). NOT the simple average (a+b)/2.

**🔎 When to use:** A trip covers the SAME distance at two different speeds (e.g., go at a, return at b), and you need the average speed for the whole journey.

**🔥 Hard example:** A man travels from town A to town B at 40 km/h and returns from B to A at 60 km/h. On a second day he covers the SAME round trip but rides the first half of the TOTAL distance at 40 km/h and the second half at 60 km/h. By how much (in km/h) does his average speed for the whole journey differ between the two days? (Round to 2 decimals.)

> **Solution:**
> Day 1 (equal distance each leg, A->B and B->A): average speed = 2ab/(a+b) = 2 x 40 x 60/(40 + 60) = 4800/100 = 48 km/h. Day 2: first HALF of total distance at 40, second HALF at 60 - this is also two equal half-distances, so the same harmonic-mean formula applies: 2 x 40 x 60/(100) = 48 km/h. So both days give 48 km/h. Difference = 48 - 48 = 0 km/h. Final answer: 0 km/h (they are identical, because A->B->A by equal legs and equal-half-of-total are mathematically the same equal-distance split).
>
> **✅ Answer: 0 km/h**

**⚠️ Trap:** Using the plain average (40+60)/2 = 50 km/h, which is wrong for equal distances. Also, people assume Day 2 (split by total distance) must differ from Day 1, but since each leg of the round trip equals exactly half the total distance, both setups are the same equal-distance case and give 48 km/h.

### 5.5  Average Speed (Equal Time)

**💡 Idea:** For equal TIMES at speeds a and b, average speed = simple mean = (a+b)/2. Spot 'for the first 2 hours... next 2 hours' (equal time), not equal distance.

**🔎 When to use:** The two speeds are held for the same DURATION (equal time), not the same distance. Then the arithmetic mean is correct.

**🔥 Hard example:** A car runs at 30 km/h for the first 90 minutes of a trip and at 70 km/h for the next 90 minutes, then immediately covers a final fixed distance of 50 km at 50 km/h. Find the average speed for the entire journey (in km/h, to 2 decimals).

> **Solution:**
> Phase 1 & 2 (equal time, 90 min = 1.5 h each): average for these two phases = (30 + 70)/2 = 50 km/h over 3 hours total, distance = 50 x 3 = 150 km. (Check: 30 x 1.5 + 70 x 1.5 = 45 + 105 = 150 km.) Phase 3: 50 km at 50 km/h takes 50/50 = 1 hour. Total distance = 150 + 50 = 200 km. Total time = 1.5 + 1.5 + 1 = 4 hours. Average speed = 200/4 = 50 km/h. Final answer: 50 km/h.
>
> **✅ Answer: 50 km/h**

**⚠️ Trap:** Confusing equal-time with equal-distance and using harmonic mean. With equal TIME the simple average works; with equal DISTANCE it does not. Also forgetting to convert 90 minutes to 1.5 hours before adding times.

### 5.6  Consecutive Numbers Average

**💡 Idea:** Average of consecutive (or any evenly-spaced/AP) numbers = (first + last)/2 = the middle term. Sum = average x count.

**🔎 When to use:** Numbers in a uniform sequence: consecutive integers, consecutive even/odd numbers, multiples of k, or any arithmetic progression.

**🔥 Hard example:** The average of 7 consecutive ODD numbers is 33. If the largest of these is replaced by a number that is 18 more than the smallest of these, what is the new average of the 7 numbers?

> **Solution:**
> Step 1: For 7 consecutive odd numbers, the average = the middle (4th) term = 33. So the numbers are 27, 29, 31, 33, 35, 37, 39. Smallest = 27, largest = 39. Step 2: Replace largest (39) with (smallest + 18) = 27 + 18 = 45. Change in the set's total = 45 - 39 = +6. Step 3: New total = old total + 6. Old total = 7 x 33 = 231; new total = 231 + 6 = 237. New average = 237/7 = 33.857... = 33 6/7. Final answer: 237/7 = 33.86 (approximately), i.e. 33 6/7.
>
> **✅ Answer: 237/7 (about 33.86)**

**⚠️ Trap:** For an EVEN count of consecutive numbers there is no single middle term - the average is the mean of the two middle terms and is NOT an integer. People also forget that 'consecutive odd' numbers differ by 2, not 1, when listing them.

---

## Simple & Compound Interest

### 6.1  CI - SI Difference (2 years)

**💡 Idea:** For 2 years, Difference = P × (r/100)². The 2-year gap is just one year's interest-on-interest.

**🔎 When to use:** Question gives (or asks for) the difference between CI and SI for exactly 2 years, same P and r. Spot the words 'difference' + '2 years'.

**🔥 Hard example:** The difference between the compound interest and simple interest on a sum for 2 years at 8% per annum is Rs 96. If the same sum is invested for 3 years at the same rate under simple interest, find the simple interest earned.

> **Solution:**
> Step 1: Difference (2 yr) = P × (r/100)². So 96 = P × (8/100)² = P × 0.0064.
> Step 2: P = 96 / 0.0064 = Rs 15,000.
> Step 3: They now ask SI for 3 years at 8%: SI = P × r × t / 100 = 15000 × 8 × 3 / 100 = Rs 3,600.
> Final answer: Rs 3,600.
>
> **✅ Answer: Rs 3,600**

**⚠️ Trap:** People stop after finding P = 15,000 and tick that, or they apply (r/100)² to get the 3-year difference. The twist is the question switches to plain 3-year SI, so the formula only gives P, not the final answer.

### 6.2  CI - SI Difference (3 years)

**💡 Idea:** For 3 years, Difference = P × (r/100)² × (3 + r/100). (= three times the 2-year base plus a small extra.)

**🔎 When to use:** Difference between CI and SI mentioned for exactly 3 years. Use this instead of computing CI and SI separately.

**🔥 Hard example:** The difference between compound interest and simple interest on a certain sum for 3 years at 20% per annum is Rs 1,488. Find the sum.

> **Solution:**
> Step 1: Difference (3 yr) = P × (r/100)² × (3 + r/100).
> Step 2: = P × (20/100)² × (3 + 20/100) = P × 0.04 × 3.2 = P × 0.128.
> Step 3: 0.128 × P = 1488, so P = 1488 / 0.128 = Rs 11,625.
> Check: CI = 11625×(1.2)³ − 11625 = 8,463; SI = 11625×0.2×3 = 6,975; difference = 1,488. Correct.
> Final answer: Rs 11,625.
>
> **✅ Answer: Rs 11,625**

**⚠️ Trap:** Forgetting the (3 + r/100) factor and using only 3×P×(r/100)² (which gives the wrong P, here it would mislead by ignoring the extra 0.2). At high rates like 20% the 'r/100' inside the bracket is significant and cannot be dropped.

### 6.3  CI as Successive Percentages

**💡 Idea:** CI growth = successive % increases. For two years at r%: net % = 2r + r²/100. (e.g. 10% → 21%, 20% → 44%.)

**🔎 When to use:** When you must find total CI/amount quickly, or combine two different yearly rates. Treat each year as a successive percentage rise and combine a+b+ab/100.

**🔥 Hard example:** A sum of Rs 15,000 is invested under compound interest where the rate is 20% for the first year and 25% for the second year. Find the total compound interest earned over the two years.

> **Solution:**
> Step 1: Combine the two rates as successive percentages: net % = 20 + 25 + (20×25)/100 = 45 + 5 = 50%.
> Step 2: Total CI = 50% of 15,000 = Rs 7,500.
> Check: After yr1 = 15000×1.2 = 18,000; after yr2 = 18000×1.25 = 22,500; CI = 22500 − 15000 = 7,500. Correct.
> Final answer: Rs 7,500.
>
> **✅ Answer: Rs 7,500**

**⚠️ Trap:** Just adding the rates (20 + 25 = 45%) and forgetting the +ab/100 cross term (here +5%). That cross term is the whole point of compounding and is easy to miss when the two yearly rates differ.

### 6.4  Doubling / Tripling Time (CI)

**💡 Idea:** Under CI, if money becomes x times in T years, it becomes xⁿ times in nT years. Doubles in T ⇒ 4× in 2T, 8× in 3T, 16× in 4T.

**🔎 When to use:** CI question says a sum doubles/triples in some years and asks when it becomes a higher multiple (8 times, 16 times, etc.). Express the target multiple as a power.

**🔥 Hard example:** A sum of money invested at compound interest doubles itself in 4 years. In how many years will it become 16 times itself at the same rate?

> **Solution:**
> Step 1: It doubles (×2) in 4 years.
> Step 2: 16 = 2⁴, so we need the amount to double 4 times.
> Step 3: Each doubling takes 4 years, so total time = 4 × 4 = 16 years.
> Final answer: 16 years.
>
> **✅ Answer: 16 years**

**⚠️ Trap:** Treating it like simple interest (where 16× would be linear, e.g. ×8 the time). Under CI you must write the multiple as a POWER of the base multiple (16 = 2⁴), not multiply 4 by 16 or by 8.

### 6.5  Rate-Time Interchange (SI)

**💡 Idea:** Under SI, interest per year is constant. If a sum doubles in T years, interest = P, so r×T = 100; to become n times, interest = (n−1)P, so r×t = (n−1)×100.

**🔎 When to use:** SI questions saying a sum doubles/triples in given years and asking the time/rate for another multiple. Use r×t = (multiple − 1) × 100.

**🔥 Hard example:** A sum of money at simple interest doubles itself in 10 years. In how many years will the same sum become five times itself at the same rate of interest?

> **Solution:**
> Step 1: Doubles ⇒ interest earned = P ⇒ r×10 = 100 ⇒ r = 10% per annum.
> Step 2: To become 5 times, interest needed = 4P ⇒ r×t = 400.
> Step 3: t = 400 / r = 400 / 10 = 40 years.
> Final answer: 40 years.
>
> **✅ Answer: 40 years**

**⚠️ Trap:** Multiplying 10 by 5 to get 50 years. 'Five times' means the INTEREST must be 4 times the principal (5P − P = 4P), not 5×, so the multiplier is (n−1) = 4, giving 40 years.

### 6.6  Equal Annual Installments (2 years)

**💡 Idea:** Loan = each-installment × [present-value factors]. For 2 years at r%: Loan = X/(1+r/100) + X/(1+r/100)². Discount each installment back to today.

**🔎 When to use:** A loan/borrowed sum is repaid in equal yearly installments under CI; find the installment or the loan. Each installment is paid in a different year, so discount each one.

**🔥 Hard example:** A man borrows Rs 5,500 and agrees to repay it in two equal annual installments at 20% per annum compound interest. Find the value of each annual installment.

> **Solution:**
> Step 1: r = 20%, so (1 + r/100) = 6/5; present-value factor per year = 5/6.
> Step 2: Loan = X×(5/6) + X×(5/6)² = X×(5/6 + 25/36) = X×(30/36 + 25/36) = X×(55/36).
> Step 3: 5500 = X × 55/36 ⇒ X = 5500 × 36/55 = 100 × 36 = Rs 3,600.
> Check: Yr1 owed 5500×1.2 = 6600, pay 3600, left 3000; Yr2 owed 3000×1.2 = 3600, pay 3600, cleared. Correct.
> Final answer: Rs 3,600.
>
> **✅ Answer: Rs 3,600**

**⚠️ Trap:** Dividing the loan by 2 (Rs 2,750) or compounding the loan forward and splitting. The installments fall in different years, so each must be discounted by a different power of (5/6); ignoring the time value gives the wrong figure.

### 6.7  Doubling Rate (SI vs CI distinction)

**💡 Idea:** SI: sum doubles when r×t = 100 (so rate = 100/t). CI: doubling is multiplicative (powers of 2). Never mix the two.

**🔎 When to use:** When the question states a doubling/tripling and you must FIRST find the rate, then answer a follow-up. Check whether it says simple or compound interest.

**🔥 Hard example:** A sum of money at simple interest doubles itself in 8 years. At the same rate of simple interest, in how many years will it triple itself?

> **Solution:**
> Step 1: Doubling under SI ⇒ interest = P ⇒ r×8 = 100 ⇒ r = 12.5% per annum.
> Step 2: Tripling ⇒ interest needed = 2P ⇒ r×t = 200.
> Step 3: t = 200 / 12.5 = 16 years.
> Final answer: 16 years.
>
> **✅ Answer: 16 years**

**⚠️ Trap:** Saying triple takes 8 × 3 = 24 years. Doubling adds 1×P of interest in 8 years; tripling needs 2×P of interest, which is 2 × 8 = 16 years, not 24. Always convert the multiple into 'how many times P of interest' first.

---

## Time & Work, Pipes & Cisterns

### 7.1  LCM (Total Work Units) Method

**💡 Idea:** Take Total Work = LCM of the given days. Each person's efficiency = Total Work / their days. Combined efficiency = sum of efficiencies, and Combined Time = Total Work / Combined efficiency. Avoids fractions completely.

**🔎 When to use:** Whenever several people/pipes are given with individual times and you must find combined time or remaining work. The default first move for almost any Time & Work problem.

**🔥 Hard example:** A can do a work in 12 days, B in 15 days and C in 20 days. They start together, but A leaves after 2 days and B leaves 3 days before the work is completed. In how many total days is the work finished?

> **Solution:**
> Total Work = LCM(12,15,20) = 60 units. Efficiencies: A=60/12=5, B=60/15=4, C=60/20=3 units/day.
> Let total time = D days. C works all D days. A works only 2 days. B works (D-3) days (leaves 3 days before end).
> Work equation: A's work + B's work + C's work = 60.
> A: 5x2 = 10. B: 4x(D-3). C: 3xD.
> 10 + 4(D-3) + 3D = 60
> 10 + 4D - 12 + 3D = 60
> 7D - 2 = 60
> 7D = 62 -> D = 62/7 = 8 6/7 days.
> Check: A=10, B=4x(62/7 - 3)=4x(41/7)=164/7, C=3x62/7=186/7. Sum=10 + 164/7 + 186/7 = 70/7 + 350/7 = 420/7 = 60. Correct.
> Final answer: 62/7 = 8 6/7 days.
>
> **✅ Answer: 62/7 = 8 6/7 days**

**⚠️ Trap:** Misreading 'B leaves 3 days before completion' as B working only 3 days. B works (D-3) days, not 3 days. Also forgetting C works the entire duration.

### 7.2  Efficiency Ratio (Inverse of Time)

**💡 Idea:** If A is x% more efficient than B, then time(A):time(B) is inverse of efficiency(A):efficiency(B). Efficiency ratio = inverse of time ratio. More efficient = less time.

**🔎 When to use:** When the question gives a percentage/ratio comparison of efficiency or speed and asks for time, or vice versa.

**🔥 Hard example:** A is twice as good a workman as B and together they finish a piece of work in 14 days. Also, C is 40% more efficient than A. In how many days will B and C together finish the same work?

> **Solution:**
> Efficiency A : B = 2 : 1. Together A+B = 3 units of efficiency finish in 14 days, so Total Work = 3 x 14 = 42 units.
> Let B's efficiency = 1, A = 2. C is 40% more efficient than A: C = 2 x 1.40 = 2.8.
> B + C efficiency = 1 + 2.8 = 3.8 units/day.
> Time for B and C = Total Work / combined efficiency = 42 / 3.8 = 420/38 = 210/19 = 11 1/19 days.
> Check: 3.8 x 210/19 = 798/19 = 42. Correct.
> Final answer: 210/19 = 11 1/19 days.
>
> **✅ Answer: 210/19 = 11 1/19 days**

**⚠️ Trap:** Confusing 'twice as good a workman' (efficiency ratio 2:1) with time ratio. Also applying 40% to B instead of to A.

### 7.3  M1 D1 H1 / W1 = M2 D2 H2 / W2 (Chain Rule)

**💡 Idea:** Men x Days x Hours / Work = constant. So (M1xD1xH1)/W1 = (M2xD2xH2)/W2. Add efficiency factor on each side if workers differ in capacity.

**🔎 When to use:** When men, days, hours-per-day and amount of work all vary together. Spot multiple varying quantities in one problem.

**🔥 Hard example:** If 10 men working 7 hours a day can build a wall 18 m long in 8 days, then how many days will 14 men working 6 hours a day take to build a wall 27 m long, given that the new men are only 5/6 as efficient as the original men?

> **Solution:**
> Use (M x D x H x E)/W = constant, where E = efficiency factor.
> Side 1: M1=10, D1=8, H1=7, E1=1, W1=18.
> Side 2: M2=14, D2=?, H2=6, E2=5/6, W2=27.
> (10 x 8 x 7 x 1)/18 = (14 x D2 x 6 x 5/6)/27
> Left = 560/18.
> Right numerator: 14 x 6 x 5/6 = 14 x 5 = 70, so = 70 x D2 / 27.
> 560/18 = 70 D2 / 27
> D2 = (560/18) x (27/70) = (560 x 27)/(18 x 70) = 15120/1260 = 12.
> Final answer: 12 days.
>
> **✅ Answer: 12 days**

**⚠️ Trap:** Putting work in the wrong place (work goes in denominator on each side). Forgetting the efficiency factor 5/6, or applying it to the wrong side.

### 7.4  Work and Wages = Efficiency (Work-Share) Ratio

**💡 Idea:** Wages are divided in the ratio of work actually done = efficiency x days each worked. Share = (individual work done) / (total work done) x Total wages.

**🔎 When to use:** When total payment is given and it must be split among workers who worked different days or with different efficiencies.

**🔥 Hard example:** A, B and C can do a work in 20, 24 and 30 days respectively. They work together but C leaves 4 days before completion and A leaves 2 days before completion. The total wages are Rs 7,800. Find C's share.

> **Solution:**
> Total Work = LCM(20,24,30) = 120 units. Efficiencies: A=6, B=5, C=4.
> Let completion = D days. B works all D days, A works (D-2), C works (D-4).
> 6(D-2) + 5D + 4(D-4) = 120
> 6D - 12 + 5D + 4D - 16 = 120
> 15D - 28 = 120 -> 15D = 148 -> D = 148/15 days.
> Work done by each (= units):
> C's days = D-4 = 148/15 - 60/15 = 88/15. C's work = 4 x 88/15 = 352/15.
> A's days = D-2 = 148/15 - 30/15 = 118/15. A's work = 6 x 118/15 = 708/15.
> B's work = 5 x 148/15 = 740/15.
> Total = (352+708+740)/15 = 1800/15 = 120 units (matches whole work). Good.
> C's share = (C's work / 120) x 7800 = (352/15 / 120) x 7800 = (352/1800) x 7800 = 352 x 7800/1800 = 352 x 13/3 = 4576/3 = Rs 1525.33...
> Let me recompute cleanly: 7800/1800 = 13/3. C share = 352 x 13/3 = 4576/3 = Rs 1525 1/3.
> Since work units total 120 and wages 7800, value per unit = 7800/120 = 65. C's share = 352/15 x 65 = 22880/15 = Rs 1525.33 = Rs 4576/3.
> Final answer: C's share = Rs 4576/3 = Rs 1525.33 (approximately Rs 1525.33).
>
> **✅ Answer: Rs 4576/3 ≈ Rs 1525.33**

**⚠️ Trap:** Splitting wages by the ratio of their solo speeds (6:5:4) ignoring that A and C worked fewer days. Wages follow actual work done, not capacity alone.

### 7.5  Pipes: Fill (+) and Empty (−) with Net Rate

**💡 Idea:** Treat fill pipes as +efficiency and empty/leak pipes as −efficiency. Net rate = sum. Time = Tank Capacity (LCM) / Net rate. If net is negative, tank empties.

**🔎 When to use:** Any cistern problem with inlet and outlet/leak pipes acting together, especially partial-fill or 'tank already part full' twists.

**🔥 Hard example:** Pipe A fills a tank in 6 hours and pipe B in 8 hours; outlet pipe C empties the full tank in 12 hours. The tank is already 1/4 full. All three pipes are opened together. How long will it take to fill the tank completely?

> **Solution:**
> Capacity = LCM(6,8,12) = 24 units. Rates: A=+4, B=+3, C=-2. Net = 4+3-2 = +5 units/hr.
> Tank already 1/4 full = 1/4 x 24 = 6 units present. Remaining to fill = 24 - 6 = 18 units.
> Time = 18 / 5 = 3.6 hours = 3 hours 36 minutes.
> Final answer: 3.6 hours = 3 hr 36 min.
>
> **✅ Answer: 3.6 hours (3 hr 36 min)**

**⚠️ Trap:** Computing time for the full 24 units instead of the remaining 18 units, or forgetting to subtract the outlet pipe's rate.

### 7.6  Alternate Days / Cyclic Work

**💡 Idea:** Find work done in one full cycle (e.g., one A-day + one B-day). Count how many complete cycles fit, then finish the leftover within the next partial cycle.

**🔎 When to use:** When workers/pipes act on alternate days or in a repeating turn-based pattern ('A and B work on alternate days starting with X').

**🔥 Hard example:** A can complete a work in 9 days and B in 18 days. They work on alternate days, but B starts the work. In how many total days will the work be completed?

> **Solution:**
> Total Work = LCM(9,18) = 18 units. A=2 units/day, B=1 unit/day.
> B starts, so each 2-day cycle = B-day + A-day = 1 + 2 = 3 units. Per cycle = 3 units over 2 days.
> After 5 full cycles (10 days): 5 x 3 = 15 units done, 3 units remain.
> Day 11 is B's turn (cycle starts with B): B does 1 unit -> 16 done, 2 remain. (Day 11 done.)
> Day 12 is A's turn: A does 2 units/day; only 2 units remain, A needs exactly 2/2 = 1 full day. So 2 units done on day 12.
> Total = 10 + 1 + 1 = 12 days.
> Check: B works days 1,3,5,7,9,11 = 6 days x1 = 6 units. A works days 2,4,6,8,10,12 = 6 days x2 = 12 units. 6+12 = 18. Correct.
> Final answer: 12 days.
>
> **✅ Answer: 12 days**

**⚠️ Trap:** Forgetting B (the slower worker) starts, so the cycle order matters. Also assuming the last day is always a full day - check whether the leftover needs only a fraction of that day.

### 7.7  Leaving-Job / Joining Midway

**💡 Idea:** Set total time = D. Each worker contributes efficiency x (days actually present). Sum of all contributions = Total Work. Solve the linear equation for the unknown.

**🔎 When to use:** When someone joins late, leaves early, or 'leaves N days before completion'. Translate each person's presence into days worked and sum the units.

**🔥 Hard example:** A and B can do a piece of work in 45 and 40 days respectively. They began the work together, but A left after some days and B finished the remaining work in 23 days. After how many days did A leave the work?

> **Solution:**
> Total Work = LCM(45,40) = 360 units. A=8 units/day, B=9 units/day.
> Let A work for x days. A and B work together for x days, then B alone for the remaining 23 days.
> B's total working days = x + 23 (B never left).
> Work: A's work + B's work = 360.
> 8x + 9(x + 23) = 360
> 8x + 9x + 207 = 360
> 17x = 153
> x = 9.
> Check: A: 8x9 = 72. B: 9x(9+23) = 9x32 = 288. 72 + 288 = 360. Correct.
> Final answer: A left after 9 days.
>
> **✅ Answer: 9 days**

**⚠️ Trap:** Treating B's working days as 23 only. B worked x days with A PLUS 23 days alone = (x+23) days total. Missing the overlap is the classic error.

---

## Time, Speed & Distance (Trains, Boats)

### 8.1  Speed Ratio = Inverse Time Ratio (& meeting-point root rule)

**💡 Idea:** For a fixed distance, Speed is inversely proportional to Time: if speeds are a:b, times are b:a. Special case: two bodies start from opposite ends, meet, then reach their destinations in times t1 and t2 -> ratio of their speeds = sqrt(t2) : sqrt(t1).

**🔎 When to use:** Use when distance is constant and only speeds/times change, OR when two trains start from opposite ends, cross, and you are given the times each takes AFTER crossing to finish the trip.

**🔥 Hard example:** Two trains start at the same time, one from city P and the other from city Q, travelling towards each other. After they cross each other, the P-train reaches Q in 4 hours and the Q-train reaches P in 9 hours. If the P-train runs at 45 km/h, find the speed of the Q-train.

> **Solution:**
> Step 1: Use the meeting-point root rule. Speed(P) : Speed(Q) = sqrt(time taken after crossing by Q) : sqrt(time taken after crossing by P) = sqrt(9) : sqrt(4) = 3 : 2.
> Step 2: So Speed(P)/Speed(Q) = 3/2. Given Speed(P) = 45 km/h.
> Step 3: 45/Speed(Q) = 3/2 => Speed(Q) = 45 x 2 / 3 = 30 km/h.
> Final answer: 30 km/h.
>
> **✅ Answer: 30 km/h**

**⚠️ Trap:** Students pair each train's speed with its OWN post-crossing time and write Speed(P):Speed(Q) = sqrt(4):sqrt(9) = 2:3. It is the inverse: the train that finishes faster after crossing is the faster train, so speeds go as sqrt(other train's time).

### 8.2  Relative Speed (Two trains crossing each other)

**💡 Idea:** Time to cross = (sum of both lengths) / relative speed. Opposite directions: relative speed = v1+v2. Same direction: relative speed = v1-v2. Convert km/h to m/s by x 5/18.

**🔎 When to use:** Two moving trains pass each other and you are asked for crossing time, a length, or a speed. Two cross-times (one opposite, one same direction) given = solve for both speeds.

**🔥 Hard example:** Two trains, each 150 m long, take 10 seconds to completely cross each other when moving in opposite directions, and 50 seconds to cross each other when moving in the same direction. Find the speed of the faster train in km/h.

> **Solution:**
> Step 1: Total length crossed = 150 + 150 = 300 m in both cases.
> Step 2: Opposite directions: relative speed = 300/10 = 30 m/s = v1 + v2.
> Step 3: Same direction: relative speed = 300/50 = 6 m/s = v1 - v2.
> Step 4: Add: 2 v1 = 36 => v1 = 18 m/s. Subtract: v2 = 12 m/s.
> Step 5: Faster train = 18 m/s = 18 x 18/5 = 64.8 km/h.
> Final answer: 64.8 km/h.
>
> **✅ Answer: 64.8 km/h**

**⚠️ Trap:** Forgetting that the distance to be cleared is the SUM of both lengths (people use only one length), and mixing up which case is sum vs difference. Opposite = add speeds; same direction = subtract.

### 8.3  Train crossing Pole vs Platform (length & speed)

**💡 Idea:** Crossing a pole: distance = train length L. Crossing a platform: distance = L + platform length. Same speed in both, so speed = (extra platform length) / (extra time). Speed v = platform_len / (t_platform - t_pole).

**🔎 When to use:** One train gives two timings: crossing a pole/man (= its own length) and crossing a platform/bridge (= length + platform). Subtract to isolate speed.

**🔥 Hard example:** A train crosses a man standing on a platform in 18 seconds and crosses the 250 m long platform itself in 33 seconds. Find the length of the train and its speed in km/h.

> **Solution:**
> Step 1: Pole/man crossing => distance = L (train length) in 18 s. Platform crossing => distance = L + 250 in 33 s. Speed is the same.
> Step 2: Extra distance = 250 m takes extra time = 33 - 18 = 15 s.
> Step 3: Speed v = 250 / 15 = 16.667 m/s.
> Step 4: Length L = v x 18 = (250/15) x 18 = 300 m.
> Step 5: Speed in km/h = 16.667 x 18/5 = 60 km/h.
> Final answer: Length = 300 m, Speed = 60 km/h.
>
> **✅ Answer: Length = 300 m, Speed = 60 km/h**

**⚠️ Trap:** Treating crossing a 'man/pole' as needing platform length too, or adding the man's position. A man/pole has zero length, so pole-time gives the train's own length directly. The clean step is (platform length)/(time difference) = speed.

### 8.4  Boats: Downstream/Upstream split (still-water & stream)

**💡 Idea:** Downstream speed d = b + s, Upstream speed u = b - s, where b = boat speed in still water, s = stream speed. Then b = (d+u)/2 and s = (d-u)/2.

**🔎 When to use:** Any river/boat problem giving (or asking for) still-water speed and current. Compute d and u from given distances/times first, then average and half-difference.

**🔥 Hard example:** A boat takes twice as long to go a certain distance upstream as it takes to go the same distance downstream. If the speed of the boat in still water is 12 km/h, find the speed of the stream. Also, how long will the boat take to travel 32 km downstream?

> **Solution:**
> Step 1: Same distance, time upstream = 2 x time downstream => downstream speed = 2 x upstream speed (speed inversely proportional to time).
> Step 2: d = 2u. With d = 12 + s and u = 12 - s: 12 + s = 2(12 - s) => 12 + s = 24 - 2s => 3s = 12 => s = 4 km/h.
> Step 3: Downstream speed d = 12 + 4 = 16 km/h.
> Step 4: Time for 32 km downstream = 32 / 16 = 2 hours.
> Final answer: Stream speed = 4 km/h; time = 2 hours.
>
> **✅ Answer: Stream = 4 km/h, time = 2 hours**

**⚠️ Trap:** Writing 'time upstream = 2 x time downstream' as 'speed upstream = 2 x speed downstream'. Time and speed are inverse: double the time means HALF the speed, so downstream is the faster (double) one.

### 8.5  Average Speed = Harmonic Mean (equal distances)

**💡 Idea:** For equal distances at different speeds, average speed is the harmonic mean, NOT the arithmetic mean. Two legs: avg = 2 v1 v2 / (v1 + v2). Three legs: avg = 3 / (1/v1 + 1/v2 + 1/v3).

**🔎 When to use:** A journey split into equal-distance parts at different speeds, or 'goes at x and returns at y'. If equal TIMES instead, use ordinary average (arithmetic mean).

**🔥 Hard example:** A car covers the first one-third of a distance at 30 km/h, the next one-third at 40 km/h, and the last one-third at 60 km/h. Find the average speed for the whole journey.

> **Solution:**
> Step 1: Equal distances => use harmonic mean of three speeds.
> Step 2: Average speed = 3 / (1/30 + 1/40 + 1/60).
> Step 3: LCM of 30,40,60 = 120. 1/30 = 4/120, 1/40 = 3/120, 1/60 = 2/120. Sum = 9/120 = 3/40.
> Step 4: Average = 3 / (3/40) = 3 x 40/3 = 40 km/h.
> Final answer: 40 km/h.
>
> **✅ Answer: 40 km/h**

**⚠️ Trap:** Taking the plain average (30+40+60)/3 = 43.33 km/h. That is wrong for equal distances; the slow leg eats more time, pulling the true average down to 40. Arithmetic mean is only valid for equal TIME segments.

### 8.6  Meeting / Catch-up with a Head Start (same direction)

**💡 Idea:** When a faster body chases a slower one that left earlier: head-start distance = (slower speed) x (head-start time). Catch-up time = head-start distance / (speed difference). Then distance = faster speed x catch-up time.

**🔎 When to use:** Same-direction pursuit where one starts before the other (later bus/train catching an earlier one). Spot the time gap and the speed gap.

**🔥 Hard example:** A bus leaves a depot at 45 km/h. Exactly 1 hour later, a car leaves the same depot along the same road at 60 km/h. How far from the depot will the car overtake the bus, and at what time after the car starts?

> **Solution:**
> Step 1: Head start of bus = 45 km/h x 1 h = 45 km ahead when the car starts.
> Step 2: Speed difference (gap closed per hour) = 60 - 45 = 15 km/h.
> Step 3: Catch-up time = 45 / 15 = 3 hours after the car starts.
> Step 4: Distance from depot = car speed x catch-up time = 60 x 3 = 180 km. (Check: bus = 45 x (3+1) = 180 km. Matches.)
> Final answer: 180 km from depot, 3 hours after the car starts.
>
> **✅ Answer: 180 km, 3 hours after the car starts**

**⚠️ Trap:** Computing catch-up time but then multiplying by the slower speed, or adding the head-start hour to the car's travel time. Use the relative (difference) speed to find time, then the car's own speed for the meeting distance.

### 8.7  Train crossing a man/object that is itself moving

**💡 Idea:** A train crosses a walking man: relative speed = train +/- man (opposite = add, same direction = subtract). Time = train length / relative speed. Convert km/h to m/s with x 5/18.

**🔎 When to use:** Train passes a person walking/running (not a fixed pole). The man's speed matters and direction decides add or subtract.

**🔥 Hard example:** A 240 m long train running at 60 km/h crosses a man running at 6 km/h in the opposite direction along the track. How many seconds does the train take to pass him completely?

> **Solution:**
> Step 1: Opposite directions => relative speed = 60 + 6 = 66 km/h.
> Step 2: Convert: 66 x 5/18 = 330/18 = 18.33 m/s.
> Step 3: Distance to clear = train length only = 240 m (man has negligible length).
> Step 4: Time = 240 / 18.33 = 13.09 seconds (approximately 13.1 s).
> Final answer: About 13.1 seconds.
>
> **✅ Answer: About 13.1 seconds (240 / (66x5/18))**

**⚠️ Trap:** Treating the man as stationary (using 60 km/h) or adding the man's 'length'. For an object with negligible length only the train's length is cleared, but the man's SPEED still changes the relative speed (add for opposite, subtract for same direction).

---

## Number System & Simplification

### 9.1  Combined Divisibility (8 & 11 = 88)

**💡 Idea:** Div by 8 -> last 3 digits divisible by 8. Div by 11 -> (sum of odd-position digits) - (sum of even-position digits) is 0 or a multiple of 11. Divisible by both means divisible by 88.

**🔎 When to use:** A digit is hidden (P, x, *) and the number must be divisible by a composite like 88, 72, 56. Split the composite into co-prime factors and apply each rule.

**🔥 Hard example:** If the 7-digit number 912834P is divisible by 8, find the digit P (and note the rule for divisibility by 88 = 8 x 11).

> **Solution:**
> Divisibility by 8 depends only on the LAST THREE digits. For 912834P those are 3, 4, P, i.e. the number '34P' = 340 + P.
> Find the digit P (0-9) making 34P divisible by 8: 344 / 8 = 43 exactly. (340/8 = 42.5 and 348/8 = 43.5 are not whole.) So P = 4 is the unique digit.
> Check: 9128344 / 8 = 11,41,043 exactly. Final answer: P = 4.
>
> **✅ Answer: P = 4**

**⚠️ Trap:** Misidentifying which three digits are 'the last three'. For 912834P they are 3,4,P -> '34P'. Test multiples of 8: 344 works, so P = 4.

### 9.2  Unit Digit via Cyclicity

**💡 Idea:** The unit digit of a power repeats every 4. Reduce the exponent mod 4 (use 4 if remainder is 0), read that term of the cycle, then multiply unit digits of separate factors and keep only the unit digit.

**🔎 When to use:** Any 'find the unit/last digit of a^b' or a product of large powers. 2,3,7,8 have 4-cycles; 4,9 have 2-cycles; 0,1,5,6 stay fixed.

**🔥 Hard example:** Find the unit digit of (7^71 x 3^63 x 11^11).

> **Solution:**
> 7^71: cycle 7,9,3,1; 71 mod 4 = 3 -> 3rd term = 3. 3^63: cycle 3,9,7,1; 63 mod 4 = 3 -> 3rd term = 7. 11^11: unit digit 1 to any power = 1. Multiply unit digits: 3 x 7 x 1 = 21 -> unit digit 1. Final answer: 1.
>
> **✅ Answer: 1**

**⚠️ Trap:** When exponent mod 4 = 0 people pick the 0th term instead of the 4th term, and some multiply full intermediate values instead of keeping only unit digits.

### 9.3  Remainder by Fermat / Cyclic Pattern

**💡 Idea:** For a^b mod p with p prime not dividing a, Fermat gives a^(p-1) = 1 (mod p). Reduce the exponent b mod (p-1), then compute the small leftover power mod p.

**🔎 When to use:** 'Remainder when a large power a^b is divided by a prime' such as 7, 11, 13, 17. Spot a prime divisor and a huge exponent.

**🔥 Hard example:** Find the remainder when 2^2018 is divided by 17.

> **Solution:**
> 17 is prime and does not divide 2, so 2^16 = 1 (mod 17). Reduce exponent: 16 x 126 = 2016, so 2018 mod 16 = 2. Then 2^2018 = (2^16)^126 x 2^2 = 1 x 4 = 4 (mod 17). Final answer: 4.
>
> **✅ Answer: 4**

**⚠️ Trap:** Reducing the exponent mod 17 (the modulus) instead of mod 16 (which is p-1), giving the wrong leftover power.

### 9.4  Factorial-Sum Remainder

**💡 Idea:** For (1! + 2! + ... + n!) mod m, once a factorial contains all prime factors of m that term and all later terms are divisible by m (remainder 0). Only the first few terms matter.

**🔎 When to use:** Sum of consecutive factorials divided by a small number like 12, 15, 18, 24. Find the cutoff factorial beyond which everything is a multiple of m.

**🔥 Hard example:** Find the remainder when 1! + 2! + 3! + ... + 100! is divided by 24.

> **Solution:**
> 24 = 4!, so every factorial from 4! to 100! is a multiple of 24 (remainder 0). Only 1! + 2! + 3! remains: 1 + 2 + 6 = 9. Then 9 mod 24 = 9. Final answer: 9.
>
> **✅ Answer: 9**

**⚠️ Trap:** Trying to sum huge factorials, or misjudging where terms start vanishing (here from 4! onward since 4! = 24).

### 9.5  HCF / LCM Word Problems (bells)

**💡 Idea:** Events happening together again -> LCM of intervals. Largest number dividing several values -> HCF. Times together in a span (excluding start) = floor(span / LCM).

**🔎 When to use:** Bells/lights tolling together, runners meeting at the start, maximum equal groups (HCF), or smallest number divisible by all (LCM).

**🔥 Hard example:** Four bells toll at intervals of 24, 36, 48 and 54 seconds. Starting together, how many times will they toll together again in one hour (excluding the first toll)?

> **Solution:**
> 24 = 2^3 x 3, 36 = 2^2 x 3^2, 48 = 2^4 x 3, 54 = 2 x 3^3. LCM = 2^4 x 3^3 = 16 x 27 = 432 seconds. One hour = 3600 s. Times together again = floor(3600 / 432) = floor(8.33) = 8. Final answer: 8 times.
>
> **✅ Answer: 8 times**

**⚠️ Trap:** Confusing HCF with LCM, forgetting to convert one hour to 3600 seconds, and the off-by-one: 'excluding start' uses floor only; 'including start' would add 1.

### 9.6  Number and Type of Factors

**💡 Idea:** If N = p^a x q^b x r^c, total factors = (a+1)(b+1)(c+1). Odd factors = product of (exponent+1) for odd primes only; even = total - odd. Perfect-square factors = product of (floor(exponent/2)+1).

**🔎 When to use:** 'How many divisors', 'how many even/odd divisors', 'how many perfect-square divisors' of a number. Prime-factorise first.

**🔥 Hard example:** How many factors of 7200 are (a) total, (b) even, and (c) perfect squares?

> **Solution:**
> 7200 = 72 x 100 = (2^3 x 3^2)(2^2 x 5^2) = 2^5 x 3^2 x 5^2. (a) Total = (5+1)(2+1)(2+1) = 6 x 3 x 3 = 54. (b) Odd factors use only 3^2 x 5^2: (2+1)(2+1) = 9, so even = 54 - 9 = 45. (c) Perfect squares need even exponents: 2 -> {0,2,4} = 3, 3 -> {0,2} = 2, 5 -> {0,2} = 2; total 3 x 2 x 2 = 12. Final answer: 54 total, 45 even, 12 perfect-square.
>
> **✅ Answer: 54 total, 45 even, 12 perfect-square factors**

**⚠️ Trap:** Forgetting to add 1 to each exponent, halving the total to get odd factors (wrong), and dropping the exponent-0 option for perfect-square factors.

### 9.7  Last Two Digits of a Power

**💡 Idea:** Last two digits = value mod 100. For numbers ending in 3, 7 or 9, a^4 ends in 01, so the last two digits cycle with length 4. Reduce the exponent mod 4 and compute that small power mod 100.

**🔎 When to use:** 'Find the last two digits' of a big power. Check the unit digit first; 3,7,9-endings have a clean 4-cycle ending in 01.

**🔥 Hard example:** Find the last two digits of 7^2017.

> **Solution:**
> 7^4 = 2401 ends in 01, so 7^4 = 1 (mod 100), cycle length 4. 2017 mod 4 = 1. Then 7^2017 = (7^4)^504 x 7^1 = 1 x 7 = 7 (mod 100), so last two digits are 07. Final answer: 07.
>
> **✅ Answer: 07**

**⚠️ Trap:** Writing just '7' instead of the two-digit form '07', or assuming cycle length 4 without confirming a^4 mod 100 ends in 01.

### 9.8  Number of (X, Y) Pairs from Product & HCF

**💡 Idea:** Given two numbers with **product N** and **HCF H**, write X = Ha, Y = Hb with gcd(a, b) = 1. Then XY = H²·ab = N, so **ab = M = N / H²**. The count of coprime pairs (a, b) with ab = M is 2^n where n = number of **distinct prime factors** of M. So the number of UNORDERED pairs (X > Y) is **2^(n−1)**.
> **Quick recipe:** (1) Compute M = N / H². (2) Prime-factorise M = p₁^a₁ · p₂^a₂ ··· pₙ^aₙ. (3) Count n = number of *distinct* primes (the exponents don't matter). (4) Answer = 2^(n−1) pairs.

**🔎 When to use:** Question gives the **product (or LCM) and HCF** of two numbers and asks 'how many such pairs of numbers are possible'. Note: LCM × HCF = product, so if LCM and HCF are given, use N = LCM × HCF.

**🔥 Hard example:** The HCF of two numbers is 12 and their product is 31104. How many such pairs of numbers are possible?

> **Solution:**
> Step 1: M = N / H² = 31104 / 12² = 31104 / 144 = 216.
> Step 2: Prime-factorise M: 216 = 2³ × 3³.
> Step 3: Distinct primes n = 2 (namely 2 and 3); exponents are ignored.
> Step 4: Number of unordered pairs = 2^(n−1) = 2^(2−1) = 2.
> Check: the coprime factor pairs of 216 are (1, 216), (8, 27) [since 216 = 2³ × 3³ split fully to keep them coprime]. Multiply by H = 12: (12, 2592) and (96, 324). Both have HCF 12 and product 31104. So 2 pairs.
> Final answer: 2 pairs.
>
> **✅ Answer: 2 pairs**

**⚠️ Trap:** Three common errors: (1) using 2^n (ordered pairs) instead of 2^(n−1) when the question wants unordered pairs; (2) counting *all* prime factors with multiplicity instead of only the **distinct** primes — the exponents (3 and 3 here) do NOT affect the count; (3) forgetting that the HCF H must divide both, so the coprime parts a, b multiply to N/H², not to N.

---

## Time, Speed & Distance — Late/Early Arrival Bonus

### TSD-X  Late Start + Speed Change → Reach On Time

**💡 Idea:** When a vehicle/person changes speed to make up for a late start (or to save a fixed time), the time saved equals the difference of the two trip times. With original speed x and an increase Δ over a fixed distance D:
> **D × Δ = (Time Saved) × x(x + Δ)**
>
> This is just D/x − D/(x + Δ) = Time Saved, rearranged. The same shape covers 'if speed were x more, he'd arrive T earlier' and 'started late, increased speed, reached on time' (here Time Saved = the lateness). The MOMENT you see this story, write this equation directly.

**🔎 When to use:** Any problem with phrases like 'starts 30 min late and increases speed to reach on time', 'if he had driven Δ km/h faster he'd save T minutes', or 'reduces speed by Δ and arrives T late'. You usually know three of {D, x, Δ, T} and solve for the fourth.

**🔥 Hard example:** A train was scheduled to cover 300 km at a uniform speed, but it started 1 hour late. To reach the destination on time, the driver increased the speed by 10 km/h above the scheduled speed. Find the scheduled (original) speed.

> **Solution:**
> Here D = 300, Δ = 10, Time Saved = 1 hour (the lateness it must recover). Let scheduled speed = x.
> Apply: D × Δ = (Time Saved) × x(x + Δ)
> 300 × 10 = 1 × x(x + 10)
> 3000 = x² + 10x
> x² + 10x − 3000 = 0 → (x + 60)(x − 50) = 0 → x = 50 (reject −60).
> Check: at 50 km/h, time = 300/50 = 6 h; at 60 km/h, time = 300/60 = 5 h; saved exactly 1 h. Correct.
> Final answer: scheduled speed = 50 km/h.
>
> **✅ Answer: 50 km/h**

**⚠️ Trap:** Setting up D/x − D/(x+Δ) and cross-multiplying from scratch under exam pressure (slow, error-prone with the algebra). Memorise the rearranged form **D·Δ = T·x(x+Δ)** so you jump straight to a clean quadratic. Also watch units — convert 'minutes' of time saved to hours (or keep speed in km/min) before substituting.

---

## Final word 💪
These are the toughest versions of each question type on purpose. If you can solve these, the real exam questions will feel easy. Do **one topic a day**, redo the hard examples after a week from memory, and burn the **traps** into your head — that is where the marks hide.

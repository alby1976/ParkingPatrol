# 90-second rehearsal script

## Slide 4 — Getting the data ready

“Every time staff walk the lot, they record which vehicles they see. Sometimes the same vehicle gets entered twice during one patrol, so I count it once for that patrol.

Then I turn those sightings into numbers the models can use. For example, how many patrols saw the vehicle that day? And how many days was it seen over the past 30 days? Those numbers give us a consistent way to compare parking patterns.”

*[Next slide]*

## Slide 5 — The simple rule

“Once the data is clean, I start with a simple rule. If staff see the same vehicle in two separate patrols on the same day, it gets flagged for review.

Say we see a car at nine in the morning and again at three in the afternoon. We know it was there at both checks. It could have left and come back. That’s why the flag is a cue for someone to look closer.”

*[Next slide]*

## Slide 6 — What the models found

“Then I compared the rule with two machine learning methods. Out of 315 examples from fictional parking records, the rule flagged 133 and Isolation Forest flagged 32.

The other method, L-O-F, looks at how similar each example is to the ones around it. Too many examples had identical numbers, so L-O-F produced no usable scores for this run.

On the next slide, I’ll show what those results tell us about which parking patterns get flagged for review.”

"""
woe — Weight-of-Evidence and Information Value for feature screening.

Empty for now — this is the core of Section 5. We'll build it together, one
tested function at a time, so you understand every line rather than calling a
black box. Keep computation here separate from any plotting.

Convention to enforce when we build it (from the project brief):
  * Good = non-default (TARGET == 0), Bad = default (TARGET == 1).
  * WOE_i  = ln( (Good_i / Good_total) / (Bad_i / Bad_total) )
  * IV     = sum_i (Good%_i - Bad%_i) * WOE_i
  * Guard empty/tiny bins (epsilon or merge) so WOE never blows up.

Planned / likely contents (add when needed):
  * woe_table   — per-bin Good/Bad counts, WOE and bin IV for one feature.
  * iv          — single IV number for a feature.
  * rank_iv     — assemble the ranked IV table across all screened features.
  * iv_band     — label an IV against the standard thresholds.
"""

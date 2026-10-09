"""
Sec. VI uncertainty. Two independent bounds on how large a difference in Table 4
has to be before it means anything.

(1) SAMPLING BOUND. GSM8K is scored on its 1,319-item test split. For a paired
    comparison -- the same questions under two containers -- the McNemar standard
    deviation of the accuracy difference is sqrt(d/n) with d the discordance rate,
    the fraction of items the two containers answer differently. The source
    reports point estimates only and no discordance counts, so we bound d rather
    than knowing it, taking 5% to 15% as the plausible span for containers this
    close. This is the smallest the uncertainty can be: it counts sampling alone.

(2) ATTRIBUTION BOUND, from the table's own content. Q5_0 and Q5_K_S are
    indistinguishable on both metrics the framework can check -- identical 5.57
    effective bits per weight, identical 7.43 perplexity -- yet their task scores
    differ. That difference cannot be attributed to bit width, because bit width
    is held fixed. It is therefore a direct empirical floor on how large a gap
    must be before "bit width caused it" is a defensible reading.

The second bound is the one that matters for Sec. VI-D's claim, and it is the
stricter of the two.
"""
import pandas as pd, numpy as np
q = pd.read_csv("/home/claude/review/t4_quality.csv").set_index("quant")

N_GSM8K = 1319                      # openai/gsm8k, main config, test split
def mcnemar_sd(n, d):  return 100.0 * np.sqrt(d / n)

sd_lo, sd_hi = mcnemar_sd(N_GSM8K, 0.05), mcnemar_sd(N_GSM8K, 0.15)
print(f"(1) GSM8K paired sampling SD at n={N_GSM8K}: "
      f"{sd_lo:.2f} pp (5% discordance) to {sd_hi:.2f} pp (15%)")
p = q.loc["F16","GSM8K"]/100
print(f"    unpaired binomial SE for one arm: "
      f"{100*np.sqrt(p*(1-p)/N_GSM8K):.2f} pp; for a difference of two: "
      f"{100*np.sqrt(2*p*(1-p)/N_GSM8K):.2f} pp (pairing can only shrink this)\n")

a, b = q.loc["Q5_0"], q.loc["Q5_K_S"]
floor_g, floor_a = abs(a.GSM8K-b.GSM8K), abs(a.avg-b.avg)
print(f"(2) Q5_0 vs Q5_K_S -- same {a.bpw:.2f} bits, same {a.ppl:.2f} perplexity:")
print(f"    GSM8K differs by {floor_g:.2f} pp, five-task mean by {floor_a:.2f} pp")
print(f"    the GSM8K floor is {floor_g/sd_hi:.1f}x the most conservative sampling SD,")
print(f"    so sampling is NOT the dominant source of variation in this column\n")

print("Significance of each GSM8K difference against both bounds:")
print(f"{'container':10s} {'bits':>5s} {'loss pp':>8s} {'sampling sigma':>16s} {'vs floor':>9s}  verdict")
rows=[]
for k, r in q.iterrows():
    if k == "F16": continue
    d = r.d_gsm8k_pp
    s_lo, s_hi = abs(d)/sd_hi, abs(d)/sd_lo          # conservative .. optimistic
    ratio = abs(d)/floor_g
    if d < 0:                       v = "improves (noise)"
    elif s_lo >= 2.5 and ratio >= 1: v = "ROBUST"
    elif s_lo >= 2.5:                v = "sampling-significant only"
    else:                            v = "within noise"
    rows.append((k, r.bpw, d, s_lo, s_hi, ratio, v))
    print(f"{k:10s} {r.bpw:5.2f} {d:+8.2f} {s_lo:7.1f}-{s_hi:<7.1f} {ratio:9.2f}  {v}")

rob = [r for r in rows if r[6]=="ROBUST"]
print(f"\nRows surviving BOTH bounds: {', '.join(r[0] for r in rob) or 'none'}")
print(f"  all at or below {max(r[1] for r in rob):.2f} effective bits per weight")

# VI-C: the k-quant vs legacy claim
k_, l_ = q.loc["Q4_K_S"], q.loc["Q4_0"]
diff = l_.d_avg_pp - k_.d_avg_pp
pa = q.loc["F16","avg"]/100
se_avg = 100*np.sqrt(2*pa*(1-pa)/N_GSM8K)   # deliberately pessimistic: smallest task n
print(f"\nVI-C: Q4_0 loses {l_.d_avg_pp:.2f} pp vs Q4_K_S {k_.d_avg_pp:.2f} pp "
      f"at {l_.bpw:.2f} vs {k_.bpw:.2f} bits")
print(f"  difference {diff:.2f} pp; five-task-mean attribution floor from the "
      f"Q5_0/Q5_K_S pair is {floor_a:.2f} pp")
print(f"  ratio {diff/floor_a:.2f}x the floor -> {'supported' if diff/floor_a>=1.5 else 'suggestive, must be hedged'}")

pd.DataFrame(rows, columns=["quant","bpw","d_gsm8k","sigma_lo","sigma_hi",
                            "vs_floor","verdict"]).to_csv(
    "/home/claude/review/t_uncertainty.csv", index=False)

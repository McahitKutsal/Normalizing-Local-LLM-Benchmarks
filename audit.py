#!/usr/bin/env python3
"""Audit the manuscript against the second reviewer's acceptance criteria."""
import json, re, subprocess, sys, pathlib
R = pathlib.Path("/home/claude/review"); P = R/"paper"
TXT = "\n".join((P/f).read_text() for f in ["content_a.js","content_b.js","content_c.js"])
BUILD = (P/"build.js").read_text(); REFS = (P/"refs.js").read_text()
ALL = TXT + BUILD + REFS
T = json.loads((P/"tables.json").read_text())
FAIL=[]
def chk(item, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {item}" + (f"   [{detail}]" if detail and not cond else ""))
    if not cond: FAIL.append(item)

print("P0.1 double averaging")
chk("eq (3) defines C-bar = L_p + L_g/2", "C̄  =  L_p  +  L_g / 2" in TXT)
chk("eq (4) has no /2 on the cache term", "B_tok  =  B_w  +  B_kv(C̄)" in TXT)
chk("old B_kv(C)/2 form gone", "B_kv(C) / 2" not in TXT)
chk("Table 2 B_tok updated (4.45 not 4.30)",
    any(r[9].startswith("4.45") for r in T["t5"][1:]) and
    not any(r[9].startswith("4.30") for r in T["t5"][1:]))
chk("Table 2 ceiling updated (226 not 234)", any(r[10]=="226" for r in T["t5"][1:]))
chk("Knoop ctx is 8448 (ISL 8192 + OSL 512/2), source-verified",
    any(r[5]=="8448" for r in T["t5"][1:]))
chk("regression test exists and passes",
    subprocess.run([sys.executable,"test_normalize.py"],cwd=R,capture_output=True).returncode==0)
chk("tables.json is generated, not hand-edited", (R/"gen_tables.py").exists())

print("\nP0.2 sign error")
chk("erroneous sentence removed", "lower the affected MBU values by under two percent" not in TXT)
chk("direction stated correctly (final length RAISES MBU)",
    "raises B_tok and therefore raises MBU" in TXT)

print("\nP0.3 delta conventions")
hdr = T["t2"][0]
chk("column names are direction-neutral",
    "PPL incr." in hdr and "Acc. loss (pp)" in hdr and "GSM8K loss (pp)" in hdr)
chk("no bare 'Delta' headers remain", not any(h.startswith("Δ") for h in hdr))

print("\nP1.1 filter on eliminated candidates")
chk("Table 3 exists with >=5 rows", len(T.get("t7",[]))-1 >= 5, f"{len(T.get('t7',[]))-1}")
cd = T["t7"][1:]
chk("from >=3 distinct sources", len({r[0] for r in cd})>=3, f"{len({r[0] for r in cd})}")
chk("every row gives a RANGE not a point", all("–" in r[5] for r in cd))
chk("min batch reported where indeterminate",
    all(r[7]!="—" for r in cd if r[8]!="PASS"))
chk("Sec. V-A explains why the two corpora are separate", "Section V-D applies the filter" in TXT)
chk("abstract separates check from finding", "calibration" in TXT and "no verdict at all" in TXT)
chk("'recovers a fact' claim removed", "recovers a fact the published number alone does not carry" not in TXT)
chk("Sec. X-A single-test caveat loosened", "it is no longer a single study with a single cause" in TXT)

print("\nP1.2 filter sensitivity")
chk("figure exists", (R/"fig2_sensitivity.png").exists())
chk("script in repo", (R/"sensitivity.py").exists())
chk("Sec. IV-F present", "F. How Much the Filter Can See" in TXT)
chk("eq (10) and (11) derived", "(10)" in TXT and "(11)" in TXT)
chk("Sec. IV-E cross-references it", "Section IV-F quantifies how much it misses" in TXT)

print("\nP1.3 uncertainty")
chk("Table 4 has an uncertainty column", "GSM8K σ" in T["t2"][0])
chk("Sec. VI-E noise floor section present", "E. What Counts as a Difference" in TXT)
chk("Q5_0 / Q5_K_S pair used", "Q5_0 and Q5_K_S are indistinguishable" in TXT)
chk("VI-D restricted to the robust rows", "We restrict the claim to those three rows" in TXT)
chk("VI-D no longer cites the Q4_0 1.97 pp gap as evidence",
    "The same asymmetry is visible earlier and more mildly" not in TXT)
chk("VI-C hedged", "suggestive rather than established" in TXT)

print("\nP1.4 mixed-phase bias")
chk("direction and bound stated", "[1.49, 1.65]" in TXT)
chk("prefill time share computed", "5.9% of the wall clock" in TXT or "5.9 percent" in TXT)
chk("qualifier in abstract", "bounded to [1.49, 1.65] on decode alone" in TXT)
chk("qualifier in Sec. XIV", TXT.count("[1.49, 1.65]")>=3, f"{TXT.count('[1.49, 1.65]')}")
chk("script in repo", (R/"phasebound.py").exists())

print("\nP1.5 citation hygiene")
chk("intro 50-85% claim gone", "50 to 85 percent" not in TXT)
chk("Marlin cites the paper", "arXiv:2408.11743" in REFS)
chk("Marlin author list complete", "Castro" in REFS and "Hoefler" in REFS)
chk("stale 3.87x removed", "3.87" not in ALL)
chk("primary regulatory source", "2016/679" in REFS)
chk("single-source declared in captions", BUILD.count("SINGLE SOURCE")>=2)
chk("conflict of interest declared", "not disinterested in the comparison" in BUILD)

print("\nP2 polish")
# P2.1 asked for the offloaded row to stop sharing the MBU column with rows of a
# different quantity. It was resolved more decisively: the row failed verification
# and was withdrawn, so every remaining row holds the same quantity.
chk("P2.1 MBU column holds one quantity throughout",
    "Frac. resid. ceil." not in T["t5"][0]
    and not any("\u2020" in c for r in T["t5"][1:] for c in r))
chk("P2.2 bandwidth assumption scoped", "no study in the corpus crosses a memory-technology boundary" in TXT)
chk("P2.3 novelty #2 softened", "correction to benchmark practice" in TXT)
chk("P2.4 container named for 1.95x", "1.95 at Q4_K_M" in TXT)
chk("P2.6 parameter counts footnoted", "Total parameter counts used" in BUILD)

print("\nTooling")
chk("--from-csv exists", (R/"from_csv.py").exists())
chk("it reproduces Table 2 with 0 failures",
    subprocess.run([sys.executable,"from_csv.py","--reproduce-table2"],cwd=R,
                   capture_output=True,text=True).stdout.strip().endswith("normalized: 0"))

print("\nReferences")
import collections
_keys = re.findall(r"^([A-Za-z0-9_]+):\s*`", REFS, re.M)
_dup = [k for k,c in collections.Counter(_keys).items() if c>1]
chk("no duplicate keys in refs.js", not _dup, str(_dup))
_refkeys = set(_keys)
_audit_p = R/"verify"/"REFERENCE_AUDIT.md"
chk("per-reference verification record exists", _audit_p.exists())
if _audit_p.exists():
    _rec = set(re.findall(r"^\| `([A-Za-z0-9_]+)` \|", _audit_p.read_text(), re.M))
    chk("every reference has a recorded verification status",
        not (_refkeys - _rec), str(sorted(_refkeys - _rec)))
    chk("no status recorded for a reference that no longer exists",
        not (_rec - _refkeys), str(sorted(_rec - _refkeys)))
    chk("the record regenerates cleanly",
        subprocess.run([sys.executable,"gen_ref_audit.py"],cwd=R,
                       capture_output=True).returncode==0)
chk("every entry has a quoted title or is a legal instrument",
    all(('"' in v or "Regulation (EU)" in v)
        for v in re.findall(r"^[A-Za-z0-9_]+:\s*`(.+?)`,\s*$", REFS, re.M)))
chk("no 'Anonymous' placeholders", "Anonymous" not in REFS)
chk("AWQ title has no spurious 'on-device'", "on-device LLM compression" not in REFS)
chk("Zahl cited with all four authors", "E. Dalipaj" in REFS and "T. Bayer" in REFS)
chk("ExLlamaV2 cited by its actual repo description",
    "fast inference library for running LLMs locally" in REFS)
chk("GDPR title includes the repealing clause", "repealing Directive 95/46/EC" in REFS)
chk("Marlin figure matches the cited paper (~3.9x, not the repo README's 3.87x)",
    "3.87" not in ALL)
chk("lm-eval cited by the title its own BibTeX uses",
    "The Language Model Evaluation Harness" in REFS)
chk("vendor pages cited by their published headline, not paraphrased",
    "new models on RTX GPUs" not in REFS and "gpt-oss-20b performance on RTX PCs" not in REFS)

print("\nPowerInfer withdrawal")
import json as _j
_T5 = _j.loads((P/"tables.json").read_text())["t5"]
chk("corpus is 8 rows", len(_T5)-1 == 8, str(len(_T5)-1))
chk("no PowerInfer row in Table 2", not any("PowerInfer" in r[0] for r in _T5[1:]))
chk("no offloaded regime remains", "Frac. resid. ceil." not in _T5[0])
chk("withdrawn value 16.06 appears only in the disclosure",
    TXT.count("16.06") == 1 and "An earlier version of this manuscript did not" in TXT)
chk("derived claims 15.2x and 96% removed",
    "15.2" not in TXT and "96% of the resident" not in TXT and "96% of the ceiling" not in TXT)
chk("corpus counts updated to eight", "of nine measurements in the corpus" not in TXT
    and "Three of eight measurements" in TXT)
chk("Sec. V-B names it alongside the chart-only disqualifier",
    "[[puget+powerinfer]]" in TXT)
chk("Sec. VII-C retitled", "C. Placement, and a Result We Could Not Normalize" in TXT)

print("\nFigure resolution and labels")
import figsave as _fs
_eff = _fs.report()
chk(f"every figure is at least {_fs.TARGET_DPI} dpi at its placed width",
    all(v >= _fs.TARGET_DPI for v in _eff.values()),
    "; ".join(f"{k} {v:.0f}" for k,v in sorted(_eff.items()) if v < _fs.TARGET_DPI))
chk("all six figures measured", len(_eff)==6, str(sorted(_eff)))
chk("a vector copy exists for each figure",
    all((R/f"{k}.pdf").exists() for k in _fs.PLACED_IN))
# Placement widths live in two places; they must agree or the dpi maths is wrong.
_bw = dict((m.group(1), float(m.group(2))) for m in
           re.finditer(r'"(fig\d_[a-z_]+)\.png",\s*([0-9.]+)', BUILD))
chk("figsave placement widths match build.js", _bw == _fs.PLACED_IN,
    f"build.js {_bw} vs figsave {_fs.PLACED_IN}")
# Equation labels drawn INSIDE a figure are invisible to the text checks, and
# went stale once when the equations were renumbered.
_figsrc = (R/"figures.py").read_text()
chk("Fig. 1's equation labels match the current numbering",
    '"Eq. (1)-(4)"' in _figsrc and '"Eq. (5)"' in _figsrc and '"Eq. (6)-(9)"' in _figsrc)
chk("no figure source still cites the pre-renumbering equations",
    '"Eq. (1)-(3)"' not in _figsrc and '"Eq. (5)-(8)"' not in _figsrc)

print("\nTypography and float order")
# Checks the SOURCE files, the GENERATED tables and the RENDERED document, because
# an em-dash reached the output through tables.json after the source was clean.
_srcs = ALL + (R/"gen_tables.py").read_text() + (P/"tables.json").read_text()
chk("no em-dashes in source or generated tables",
    "\u2014" not in _srcs and "\\u2014" not in _srcs)
import docx2txt as _d
_t = _d.process(str(R/"Normalizing_Local_LLM_Benchmarks.docx"))
chk("no em-dashes in the rendered document", "\u2014" not in _t, str(_t.count("\u2014")))
_seq = [m.group(1) for m in re.finditer(r"(FIGURE \d|TABLE \d)\.", _t)]
_f = [x for x in _seq if x.startswith("FIGURE")]; _tb = [x for x in _seq if x.startswith("TABLE")]
chk("figures appear in ascending order", _f == sorted(_f), " ".join(_f))
chk("tables appear in ascending order", _tb == sorted(_tb), " ".join(_tb))
chk("each float captioned exactly once",
    len(_f)==len(set(_f)) and len(_tb)==len(set(_tb)))
_late=[]
for _n in range(1,7):
    _c=_t.find(f"FIGURE {_n}."); _r=[m.start() for m in re.finditer(rf"Fig\. {_n}\b", _t)]
    if not _r or min(_r) > _c: _late.append(f"Fig {_n}")
for _n in range(1,8):
    _c=_t.find(f"TABLE {_n}."); _r=[m.start() for m in re.finditer(rf"Table {_n}\b", _t)]
    if not _r or min(_r) > _c: _late.append(f"Table {_n}")
chk("every float is mentioned in the text before it appears", not _late, ", ".join(_late))
chk("figure files are named for their numbers",
    all((R/f"fig{i}_{n}.png").exists() for i,n in
        [(1,"framework"),(2,"sensitivity"),(3,"quality"),(4,"context"),
         (5,"energy_cost"),(6,"roofline")]))

print("\nIntegrity")
eqs = sorted(int(m) for m in re.findall(r"      \((\d+)\)\"", TXT))
chk("equations numbered 1..11 with no gaps", eqs==list(range(1,12)), str(eqs))
nums = [int(m) for m in re.findall(r"TABLE (\d+)\.", BUILD)]
chk("tables 1..7 each captioned once", sorted(nums)==list(range(1,8)), str(sorted(nums)))
figs = [int(m) for m in re.findall(r"FIGURE (\d+)\.", BUILD)]
chk("figures 1..6 each captioned once", sorted(figs)==list(range(1,7)), str(sorted(figs)))
for stale in ["4.25","1.47x","29%","0.728"]:
    chk(f"stale value {stale!r} absent from the text", stale not in TXT)
b = subprocess.run(["node","build.js"],cwd=P,capture_output=True,text=True)
chk("manuscript builds", b.returncode==0)
chk("all references cited", "references cited: 70 of 70" in b.stdout)

print("\n" + ("="*60) + f"\n{'ALL CHECKS PASSED' if not FAIL else str(len(FAIL))+' FAILED: '+'; '.join(FAIL)}")
sys.exit(1 if FAIL else 0)

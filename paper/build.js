const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, ImageRun,
  PageOrientation, Footer, PageNumber, convertInchesToTwip,
  Tab, TabStopType
} = require("docx");

const A = require("./content_a.js");
const B = require("./content_b.js");
const C = require("./content_c.js");
const REFS = require("./refs.js");

// Citations are written in the content as [[key]] and resolved here, in order
// of first appearance, which is what IEEE wants. Numbering by hand across three
// content files is how reference lists drift; this makes drift impossible and
// makes an uncited reference detectable rather than invisible.
// refs.js is a JS object literal, so a repeated key is overwritten in silence.
// That happened once: a second `gptoss` entry was added and the first discarded
// without any error, and the uncited-reference check below could not see it
// because the object still had one key per name. Parse the source text instead.
{
  const src = fs.readFileSync(__dirname + "/refs.js", "utf8");
  const seen = new Map();
  for (const m of src.matchAll(/^([A-Za-z0-9_]+):\s*`/gm))
    seen.set(m[1], (seen.get(m[1]) || 0) + 1);
  const dups = [...seen].filter(([, n]) => n > 1).map(([k]) => k);
  if (dups.length) throw new Error(
    `refs.js defines these key(s) more than once: ${dups.join(", ")}. ` +
    `A duplicate key silently discards the earlier entry; keep one.`);
  const defined = seen.size, exported = Object.keys(REFS).length;
  if (defined !== exported) throw new Error(
    `refs.js defines ${defined} keys but exports ${exported}.`);
}

const CITE_ORDER = [];
function citeNum(key) {
  if (!(key in REFS)) {
    throw new Error(`Citation [[${key}]] has no entry in refs.js`);
  }
  let i = CITE_ORDER.indexOf(key);
  if (i === -1) { CITE_ORDER.push(key); i = CITE_ORDER.length - 1; }
  return i + 1;
}
// [[key]] -> [n]. [[a+b+c]] -> a sorted group, "[2], [7], [9]". IEEE wants
// citations within a group in ascending order; sorting at render time means the
// order cannot be wrong whatever order the keys were written in. Numbers are
// still assigned in written order, so the reference list follows the text.
function resolveCites(text) {
  return String(text).replace(/\[\[([a-zA-Z0-9_+]+)\]\]/g, (_, keys) => {
    const nums = keys.split("+").map(citeNum);
    nums.sort((x, y) => x - y);
    return nums.map(n => `[${n}]`).join(", ");
  });
}
const T = JSON.parse(fs.readFileSync(__dirname + "/tables.json", "utf8"));

const FONT = "Times New Roman";
const PAGE_W = 12240, PAGE_H = 15840, MARGIN = 1080;   // US Letter, 0.75in
const CONTENT_W = PAGE_W - 2 * MARGIN;                  // 10080 DXA

// ---------- helpers ----------
const body = (raw, opts = {}) => { const text = resolveCites(raw); return new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: opts.after ?? 100, line: 240 },
  indent: opts.noIndent ? undefined : { firstLine: 240 },
  children: [new TextRun({ text, font: FONT, size: 20 })],
}); };

const h1 = (text) => new Paragraph({
  spacing: { before: 280, after: 140 },
  children: [new TextRun({ text, font: FONT, size: 20, bold: true, allCaps: false })],
});

const h2 = (text) => new Paragraph({
  spacing: { before: 200, after: 110 },
  children: [new TextRun({ text, font: FONT, size: 20, italics: true })],
});

// Display equation, IEEE style: the body centred in the text column and the
// number flush with the right margin. A centred paragraph cannot do both, so
// the paragraph is left-aligned with a CENTER tab stop at mid-column and a
// RIGHT tab stop at the margin, and the runs are [tab] body [tab] (n).
const EQ_CENTER = Math.round(CONTENT_W / 2);
const eq = (text) => {
  const m = String(text).match(/^(.*?)\s*\((\d+)\)\s*$/);
  const bodyTxt = (m ? m[1] : String(text)).trim();
  const num = m ? m[2] : null;
  const runs = [new TextRun({ children: [new Tab()] }),
                new TextRun({ text: bodyTxt, font: "Cambria Math", size: 20, italics: true })];
  if (num) {
    runs.push(new TextRun({ children: [new Tab()] }));
    runs.push(new TextRun({ text: `(${num})`, font: FONT, size: 20 }));
  }
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    tabStops: [
      { type: TabStopType.CENTER, position: EQ_CENTER },
      { type: TabStopType.RIGHT,  position: CONTENT_W },
    ],
    spacing: { before: 150, after: 150 },
    children: runs,
  });
};

const caption = (raw, opts = {}) => new Paragraph({
  alignment: AlignmentType.LEFT,
  keepNext: opts.keepNext ?? false,
  spacing: { before: opts.before ?? 70, after: opts.after ?? 190 },
  children: [new TextRun({ text: resolveCites(raw), font: FONT, size: 16 })],
});

function makeTable(rows, widths, fontSize = 13, keepTogether = true) {
  const total = widths.reduce((a, b) => a + b, 0);
  const scale = CONTENT_W / total;
  const w = widths.map(x => Math.round(x * scale));
  // fix rounding drift on the last column
  w[w.length - 1] += CONTENT_W - w.reduce((a, b) => a + b, 0);

  return new Table({
    columnWidths: w,
    width: { size: CONTENT_W, type: WidthType.DXA },
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0,
      cantSplit: true,
      children: cells.map((cell, ci) => new TableCell({
        width: { size: w[ci], type: WidthType.DXA },
        shading: ri === 0
          ? { type: ShadingType.CLEAR, fill: "E8EAED", color: "auto" }
          : undefined,
        margins: { top: 40, bottom: 40, left: 70, right: 70 },
        borders: {
          top:    { style: ri === 0 ? BorderStyle.SINGLE : BorderStyle.NONE, size: 6, color: "000000" },
          bottom: { style: (ri === 0 || ri === rows.length - 1) ? BorderStyle.SINGLE : BorderStyle.NONE, size: 6, color: "000000" },
          left:   { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
        },
        children: [new Paragraph({
          alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
          keepNext: keepTogether && ri < rows.length - 1,
          spacing: { before: 0, after: 0, line: 220 },
          children: [new TextRun({ text: String(cell), font: FONT, size: fontSize * 2, bold: ri === 0 })],
        })],
      })),
    })),
  });
}

function figure(file, widthIn, capText) {
  const data = fs.readFileSync(file);
  const out = [];
  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    keepNext: true,
    spacing: { before: 190, after: 60 },
    children: [new ImageRun({
      data, type: "png",
      transformation: { width: widthIn * 96, height: Math.round(widthIn * 96 * imgRatio(file)) },
    })],
  }));
  out.push(caption(capText));
  return out;
}
const RATIOS = {};
function imgRatio(file) {
  if (RATIOS[file]) return RATIOS[file];
  const buf = fs.readFileSync(file);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  return (RATIOS[file] = h / w);
}

const pageFooter = () => new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })],
  })],
});

// Render one subsection: heading, then the prose/equation fields in order.
// Both the part-A and part-B loops use this, so no field can be dropped by one
// loop and rendered by the other.
// Renders a subsection as the interleaved sequence p, eq, p2, eq2, p3, eq3, ...
// for as many rungs as the object actually defines, then THROWS if any key was
// left unrendered. An earlier revision hardcoded the rungs up to p4 and silently
// dropped every equation past it; the manuscript shipped without equations and
// nothing in the build complained. The guard below is what makes that
// unrepeatable -- adding a rung to the content needs no change here, and
// mistyping one fails the build.
const SUB_META = new Set(["h"]);
function renderSub(sink, sub) {
  sink.push(h2(sub.h));
  const used = new Set(SUB_META);
  let first = true;
  for (let rung = 1; rung <= 24; rung++) {
    const pk = rung === 1 ? "p" : `p${rung}`;
    const ek = rung === 1 ? "eq" : `eq${rung}`;
    if (Array.isArray(sub[pk])) {
      sub[pk].forEach(t => { sink.push(body(t, { noIndent: first })); first = false; });
      used.add(pk);
    }
    if (Array.isArray(sub[ek])) {
      sub[ek].forEach(t => sink.push(eq(t)));
      used.add(ek);
    }
  }
  const orphans = Object.keys(sub).filter(k => !used.has(k));
  if (orphans.length) {
    throw new Error(
      `Subsection "${sub.h}" has unrendered key(s): ${orphans.join(", ")}. ` +
      `Body keys must be p, p2, p3, ... and equations eq, eq2, eq3, ... with no gaps ` +
      `in the rung numbering before the highest one used.`);
  }
}

// ---------- assemble ----------
const kids = [];        // section 1: portrait
const land = [];        // section 2: landscape (wide corpus table)
const tail = [];        // section 3: portrait

// Title block
kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 160 },
  children: [new TextRun({ text: A.title, font: FONT, size: 32, bold: true })],
}));
kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: A.authors, font: FONT, size: 22 })],
}));
kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: A.affil, font: FONT, size: 18, italics: true })],
}));
kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: A.corresponding, font: FONT, size: 18 })],
}));
if (A.funding) kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: A.funding, font: FONT, size: 18 })],
}));
if (A.artifact) kids.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: A.artifact, font: FONT, size: 18 })],
}));

// Abstract
kids.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED, spacing: { after: 130 },
  children: [
    new TextRun({ text: "ABSTRACT  ", font: FONT, size: 20, bold: true }),
    new TextRun({ text: resolveCites(A.abstract), font: FONT, size: 20 }),
  ],
}));
kids.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED, spacing: { after: 240 },
  children: [
    new TextRun({ text: "INDEX TERMS  ", font: FONT, size: 20, bold: true }),
    new TextRun({ text: A.indexTerms, font: FONT, size: 20 }),
  ],
}));

// ---------- document assembly ----------
// Three physical sections: portrait (I-V), one landscape page (the wide corpus
// table), portrait (VI onward). Tables are numbered in order of first citation,
// which also fixes where each one is placed.
//
//   Table 1  hardware substrate        Sec. V-C   portrait
//   Table 2  the verified corpus       Sec. V-C   landscape
//   Table 4  quantization accuracy     Sec. VI    portrait
//   Table 5  kernel multipliers        Sec. VII   portrait
//   Table 6  VRAM frontier             Sec. VIII  portrait
//   Table 7  energy and cost           Sec. IX    portrait

const FIG = {
  framework: ["fig1_framework.png", 6.5,
    "FIGURE 1. The normalization pipeline. A reported figure enters with the parameters its source provides; three computed stages reduce it to a device-independent basis; the validity filter tests whether the stated conditions can hold."],
  quality: ["fig3_quality.png", 6.7,
    "FIGURE 3. Accuracy against compression. Panel (a) gives the five-task mean and GSM8K alone; panel (b) the traffic-implied ceiling. Accuracy is near-free to about 4.6 bits per weight and falls sharply below four, with reasoning degrading first and fastest."],
  context: ["fig4_context.png", 6.2,
    "FIGURE 4. The key-value cache as a share of total footprint at Q4_K_M. Interleaved sliding-window attention caps cache growth past the window, so the models that pay the context wall are the full-attention ones, not the largest ones."],
  energy: ["fig5_energy_cost.png", 6.7,
    "FIGURE 5. Panel (a): measured energy per token against decode throughput; the near-linear inverse relation is the signature of a bandwidth-bound workload drawing roughly constant power. Panel (b): cost decomposed into electricity and hardware amortization."],
  sensitivity: ["fig2_sensitivity.png", 7.0,
    "FIGURE 2. How large a mislabelling the filter can see. A measurement really taken at batch B with true per-stream efficiency \u03b7 and presented as single-stream yields a computed MBU above one only in the shaded region. The boundary falls as roughly 1/B, so detection needs better than 50% efficiency at batch two and better than 31% at batch eight. Below the dotted line no batch size is large enough: a run whose cache dominates its traffic can never be caught this way. The three flagged corpus rows sit 34 to 50 percent above the boundary. Computed at the cache share of those rows (0.270); a smaller share moves the boundary down."],
  roofline: ["fig6_roofline.png", 6.3,
    "FIGURE 6. Every verified measurement against its computed ceiling. Points on the diagonal achieve their bandwidth-bound limit; points above it cannot be single-stream decoding, and all three such points are documented by their source as concurrency eight. The corpus holds no offloaded measurement: the candidate was withdrawn because its source publishes the throughput only inside a figure image, which Sec. VII-C discusses."],
};
const putFig = (sink, key) => {
  const [f, w, cap] = FIG[key];
  sink.push(...figure(__dirname + "/../" + f, w, cap));
};
const putTable = (sink, cap, rows, widths, fs) => {
  sink.push(caption(cap, { before: 190, after: 90, keepNext: true }));
  sink.push(makeTable(rows, widths, fs));
  sink.push(new Paragraph({ spacing: { after: 190 }, children: [] }));
};

// What follows each section, keyed by its leading numeral.
const AFTER = {
  "IV.": (k) => { putFig(k, "framework"); putFig(k, "sensitivity"); },
  "V.":  (k) => putTable(k,
    "TABLE 1. Consumer GPU hardware substrate. Bandwidth per dollar is the governing figure of merit for bandwidth-bound decoding; MSRP is the launch price and does not reflect subsequent market conditions.",
    T.t1, [20, 14, 11, 11, 8, 11, 12, 13]),
  "VI.": (k) => { putTable(k,
    "TABLE 4. Quantization containers on a common basis, from a unified evaluation of Llama-3.1-8B-Instruct [[unifiedquant]]. Effective bits per weight are derived from published size reduction, not assumed. Perplexity is WikiText-2; the five-task mean covers GSM8K, HellaSwag, IFEval, MMLU and TruthfulQA. All three delta columns are cost columns: positive means worse than the F16 baseline, and a negative entry marks a container that scored above it, which Sec. VI-E reads as noise rather than improvement. GSM8K sigma is the conservative end of the paired sampling bound (15% discordance on n = 1319); a dagger marks the rows that also clear the attribution floor of Sec. VI-E, and only those three support a claim about bit width. Roofline is the traffic-implied ceiling ratio on an RTX 4090 at mean cache occupancy 4096. SINGLE SOURCE: every accuracy value in this table comes from one single-author preprint, which reports point estimates without repeated runs; the uncertainty columns are our own bounds, not the source's.",
    T.t2, [12, 11, 8, 7, 8, 11, 11, 11, 9, 10]); putFig(k, "quality"); },
  "VII.": (k) => putTable(k,
    "TABLE 5. Kernel and algorithmic multipliers, traced to their primary sources. None of these lowers per-token traffic, so none is captured by MBU; they raise the achieved fraction of the ceiling, or amortize one weight sweep across several tokens.",
    T.t3, [22, 20, 17, 41]),
  "VIII.": (k) => { putTable(k,
    "TABLE 6. VRAM demand in GiB at 32k context: weights, key-value cache at 16-bit precision computed by equation (2), and 1 GiB of runtime overhead. Architectures were read from each model's published configuration file. Values at or below 24 admit a flagship consumer card, at or below 16 the volume tier. Total parameter counts used, in billions: Llama-3.1-8B 8.03, Qwen3-8B 8.19, Gemma-3-12B 12.2, Gemma-3-27B 27.4, Qwen2.5-32B 32.8, Llama-3.3-70B 70.6; a reader assuming the round nominal counts instead will differ by up to 1 GiB per cell. Where no artifact has been measured for a given model-container pair, the generic container width of Sec. VI-A is used. That substitution is the weakest assumption in this table and it is not neutral: a model with a large vocabulary carries a bigger share of its weights in the tensors k-quants keep at higher precision, so the true width for such a pair is above the generic value and these cells understate its footprint. Gemma-3's 262k-token vocabulary makes its rows the ones most exposed to this.",
    T.t4, [19, 11, 10, 10, 10, 10, 10, 10, 10]); putFig(k, "context"); },
  "IX.": (k) => { putTable(k,
    "TABLE 7. Measured energy and derived cost [[zahl]], on an RTX 4060 Ti 16GB with Ollama, decode-only throughput and measured board power at batch one. Energy per token is the source's measured value, integrated over the inference window; cost uses 0.16 USD per kWh, a three-year horizon and a 25% duty cycle. Model identifiers are the Ollama registry tags exactly as the source prints them. SINGLE SOURCE: all nine energy measurements come from one study on one device; the cost columns inherit that dependency, and Sec. XII states what it bounds.",
    T.t6, [26, 11, 13, 10, 13, 13, 14]); putFig(k, "energy"); },
  "X.":  (k) => putFig(k, "roofline"),
};

function renderSections(sink, sections) {
  for (const sec of sections) {
    sink.push(h1(sec.h));
    (sec.intro || []).forEach(t => sink.push(body(t, { noIndent: true })));
    (sec.p || []).forEach((t, i) => sink.push(body(t, { noIndent: i === 0 })));
    for (const sub of (sec.sub || [])) renderSub(sink, sub);
    const key = Object.keys(AFTER).find(k => sec.h.startsWith(k));
    if (key) AFTER[key](sink);
  }
}

renderSections(kids, A.sections);   // I-V      -> first portrait section
renderSections(tail, B);            // VI-VII   -> final portrait section
renderSections(tail, C);            // VIII-XIV -> same

// References
tail.push(h1("REFERENCES"));
const uncited = Object.keys(REFS).filter(k => !CITE_ORDER.includes(k));
if (uncited.length) {
  throw new Error(
    `${uncited.length} reference(s) never cited in the body: ${uncited.join(", ")}.\n` +
    `Cite them with [[key]] or remove them from refs.js.`);
}
CITE_ORDER.forEach((k, i) => tail.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 55, line: 220 },
  indent: { left: 400, hanging: 400 },
  children: [new TextRun({ text: `[${i + 1}] ${REFS[k]}`, font: FONT, size: 17 })],
})));
console.log(`references cited: ${CITE_ORDER.length} of ${Object.keys(REFS).length}`);

// ---------- landscape section: the wide normalized corpus table ----------
const LAND_W = PAGE_H, LAND_H = PAGE_W, LAND_M = 900;
const LAND_CONTENT = LAND_W - 2 * LAND_M;   // 14040 DXA

function makeWideTable(rows, widths, halfPt) {
  const total = widths.reduce((a, b) => a + b, 0);
  const w = widths.map(x => Math.round(x / total * LAND_CONTENT));
  w[w.length - 1] += LAND_CONTENT - w.reduce((a, b) => a + b, 0);
  return new Table({
    columnWidths: w,
    width: { size: LAND_CONTENT, type: WidthType.DXA },
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0,
      children: cells.map((cell, ci) => new TableCell({
        width: { size: w[ci], type: WidthType.DXA },
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: "E8EAED", color: "auto" } : undefined,
        margins: { top: 30, bottom: 30, left: 60, right: 60 },
        borders: {
          top:    { style: ri === 0 ? BorderStyle.SINGLE : BorderStyle.NONE, size: 6, color: "000000" },
          bottom: { style: (ri === 0 || ri === rows.length - 1) ? BorderStyle.SINGLE : BorderStyle.NONE, size: 6, color: "000000" },
          left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
        },
        children: [new Paragraph({
          alignment: ci === 0 || ci === 2 ? AlignmentType.LEFT : AlignmentType.CENTER,
          spacing: { before: 0, after: 0, line: 200 },
          children: [new TextRun({ text: String(cell), font: FONT, size: halfPt, bold: ri === 0 })],
        })],
      })),
    })),
  });
}

land.push(new Paragraph({
  spacing: { after: 90 },
  children: [new TextRun({
    text: "TABLE 2. The verified corpus, reduced to a common basis by equations (1)-(6). Every value was read from its primary source; measurements that could not be verified in full were excluded rather than estimated. MBU values marked with an asterisk exceed unity and therefore cannot describe batch-1 decoding; all three are documented by their source as concurrency eight. Ceiling is the bandwidth-bound limit at batch one, in tokens per second. Phase \"mixed\" means prefill and decode tokens share the numerator and the denominator of the reported rate; \"decode/total\" means only generated tokens are counted but the measurement window still includes prefill, so the rate understates decode speed and the MBU derived from it is a lower bound. Ctx is mean cache occupancy C-bar from equation (3), derived from the prompt and generation lengths each source states, not a configured maximum context. \u2020 The offloaded row is held out of the MBU column: its B_tok is resident-equivalent traffic and its ratio is to a ceiling the hardware never had, which is a different quantity from the other rows' achieved bandwidth utilization and is reported separately in the last column. Sec. VII-C explains why the two differ and by how much. SINGLE SOURCE AND INTEREST: the engine result of Sec. VII-A rests entirely on the four Menlo rows, which are a company technical report rather than a peer-reviewed measurement, published by a vendor of its own local inference product (Jan/Cortex) and therefore not disinterested in the comparison; we use it because it is the only source we found that holds model, container, batch and sequence lengths fixed across two engines on two cards, and we treat its absolute values as provisional.",
    font: FONT, size: 16 })],
}));
land.push(makeWideTable(T.t5, [10, 7, 10, 8, 11, 6, 5, 8, 6, 8, 6, 6, 9], 16));
// Sec. V-C cites this as Table 2; it sits on its own landscape page because
// twelve columns do not fit the portrait measure at a legible size.

land.push(new Paragraph({
  spacing: { before: 260, after: 90 },
  children: [new TextRun({
    text: "TABLE 3. The validity filter applied to measurements it CANNOT normalize: the set eliminated by the inclusion rule of Sec. V-A, which is the filter's actual test domain. B_tok range spans every reading consistent with what each source states; MBU at batch 1 is the corresponding range under the single-stream reading each presentation invites. Min. batch is the smallest concurrency that would reconcile the least favourable reading with the device. PASS means no admissible reading exceeds the bandwidth bound; INDETERMINATE means some do and some do not, so the measurement can be neither confirmed nor refuted as batch-1 decoding from its published description. No row asserts that a measurement is wrong. Single-source dependency: four of the nine rows come from one site, and the two NVIDIA items share an author.",
    font: FONT, size: 16 })],
}));
land.push(makeWideTable(T.t7, [11, 7, 19, 20, 6, 11, 10, 6, 10], 15));

const doc = new Document({
  creator: "Systematic Review",
  title: A.title,
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [
    { properties: { page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.PORTRAIT },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } } },
      footers: { default: pageFooter() },
      children: kids },
    { properties: { page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.LANDSCAPE },
        margin: { top: LAND_M, right: LAND_M, bottom: LAND_M, left: LAND_M } } },
      footers: { default: pageFooter() },
      children: land },
    { properties: { page: {
        size: { width: PAGE_W, height: PAGE_H, orientation: PageOrientation.PORTRAIT },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } } },
      footers: { default: pageFooter() },
      children: tail },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = "/home/claude/review/Normalizing_Local_LLM_Benchmarks.docx";
  fs.writeFileSync(out, buf);
  console.log("written:", out, (buf.length / 1024).toFixed(0) + " KB");
});

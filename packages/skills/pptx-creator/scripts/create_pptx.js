#!/usr/bin/env node
"use strict";

/**
 * create_pptx.js  slides.json → .pptx
 *
 * Usage:
 *   node create_pptx.js slides.json output.pptx
 *   node create_pptx.js slides.json output.pptx style_guide.json   (後方互換)
 *
 * Slide types: title, section, content, two_column, stat, chart, image, closing
 */

const PptxGenJS = require("pptxgenjs");
const fs        = require("fs");
const path      = require("path");

const SKILL_DIR  = path.resolve(__dirname, "..");
const ASSETS_DIR = path.join(SKILL_DIR, "assets");

const W = 10;       // LAYOUT_16x9 width  (inches)
const H = 5.625;    // LAYOUT_16x9 height (inches)

// ────────────────────────────────────────────────────────────────────
// ユーティリティ
// ────────────────────────────────────────────────────────────────────

const hex = c => (c || "FFFFFF").replace("#", "").toUpperCase();

function resolveAsset(filename) {
  if (!filename) return null;
  if (path.isAbsolute(filename) && fs.existsSync(filename)) return filename;
  function search(dir) {
    if (!fs.existsSync(dir)) return null;
    for (const f of fs.readdirSync(dir)) {
      const full = path.join(dir, f);
      if (fs.statSync(full).isDirectory()) { const r = search(full); if (r) return r; }
      else if (f === filename || f === path.basename(filename)) return full;
    }
    return null;
  }
  return search(ASSETS_DIR);
}

function buildPalette(styleGuide, styleOverride = {}) {
  const c  = styleGuide.colors_nohash      || [];
  const sg = styleGuide.extracted_colors   || [];
  const s  = v => (v || "").replace("#", "").toUpperCase() || null;

  return {
    primary:   s(styleOverride.primary_color)   || c[0] || s(sg[0]) || "1A1A2E",
    secondary: s(styleOverride.secondary_color) || c[1] || s(sg[1]) || "16213E",
    accent:    s(styleOverride.accent_color)    || c[2] || s(sg[2]) || "E94560",
    white:     "FFFFFF",
    snow:      "F8FAFC",
    altBg:     "EDF2F8",
    warmBg:    "FFF0F3",
    text:      s(styleOverride.text_color) || "1A1A2E",
    dim:       "64748B",
    slate:     "94A3B8",
    border:    "CBD5E1",
  };
}

function resolveFont(styleGuide, styleOverride = {}) {
  const override = styleOverride.heading_font || styleOverride.body_font;
  if (override && override !== "游ゴシック") return override;
  const fonts = styleGuide.fonts || [];
  const jp = fonts.filter(f => /meiryo|noto|hiragino|gothic|mincho|游|mplus/i.test(f));
  return jp[0] || fonts[0] || "Meiryo";
}

// ────────────────────────────────────────────────────────────────────
// 描画プリミティブ
// ────────────────────────────────────────────────────────────────────

function SHAPE(s, x, y, w, h, fillColor, lineColor, dashType) {
  const fc      = hex(fillColor);
  const noBorder = !lineColor || lineColor === "none";
  const lc      = noBorder ? fc : hex(lineColor);
  const lineOpts = { color: lc, width: noBorder ? 0.01 : 0.75,
                     ...(dashType ? { dashType } : {}) };
  s.addShape("rect", { x, y, w, h, fill: { color: fc }, line: lineOpts });
}

function TXT(s, text, x, y, w, h, opts = {}) {
  s.addText(text, {
    x, y, w, h,
    fontSize:  opts.size    || 16,
    bold:      opts.bold    || false,
    italic:    opts.italic  || false,
    color:     hex(opts.color || "1A1A2E"),
    align:     opts.align   || "left",
    valign:    opts.valign  || "middle",
    wrap:      opts.wrap !== false,
    fontFace:  opts.font    || "Meiryo",
  });
}

function addHeader(s, title, C, font) {
  SHAPE(s, 0, 0, W, 0.6,   C.primary, "none");
  SHAPE(s, 0, 0.6, W, 0.035, C.accent, "none");
  s.addText(title, { x: 0.4, y: 0.04, w: W - 0.8, h: 0.55,
    fontSize: 22, bold: true, color: "FFFFFF",
    align: "left", valign: "middle", wrap: true, fontFace: font });
}

function addLogo(s, logoPath) {
  const p = resolveAsset(logoPath);
  if (!p) return;
  s.addImage({ path: p, x: W - 1.6, y: 0.07, w: 1.4, h: 0.46 });
}

// ────────────────────────────────────────────────────────────────────
// スライドタイプ別生成関数
// ────────────────────────────────────────────────────────────────────

// ── title ──────────────────────────────────────────────────────────
function makeTitleSlide(pptx, data, C, font, globalLogo) {
  const s = pptx.addSlide();
  s.background = { color: C.primary };
  SHAPE(s, 0.6, 1.2, W - 1.2, 3.3, C.white, "none");
  SHAPE(s, 0, H - 0.35, W, 0.35, C.accent, "none");
  s.addText(data.title || "", { x: 0.9, y: 1.35, w: W - 1.8, h: 1.5,
    fontSize: 36, bold: true, color: C.primary,
    align: "center", valign: "middle", wrap: true, fontFace: font });
  if (data.subtitle)
    s.addText(data.subtitle, { x: 0.9, y: 2.9, w: W - 1.8, h: 1.3,
      fontSize: 18, color: C.dim, align: "center", valign: "top", wrap: true, fontFace: font });
  const logo = data.logo || globalLogo;
  if (logo) { const p = resolveAsset(logo); if (p) s.addImage({ path: p, x: W/2-1, y: 0.4, w: 2, h: 0.68 }); }
}

// ── section ────────────────────────────────────────────────────────
function makeSectionSlide(pptx, data, C, font) {
  const s = pptx.addSlide();
  s.background = { color: C.secondary };
  SHAPE(s, 0,     0,     0.18, H,    C.accent, "none");
  SHAPE(s, 0, H - 0.18, W,   0.18,  C.accent, "none");
  const title = data.title || "";
  const lines = title.split("\n");
  const hasNum = lines.length > 1 && lines[0].length <= 14;
  if (hasNum) {
    s.addText(lines[0], { x: 0.5, y: 1.1, w: W - 1.0, h: 0.45,
      fontSize: 16, color: C.slate, italic: true, align: "center", fontFace: font });
    s.addText(lines.slice(1).join("\n"), { x: 0.5, y: 1.6, w: W - 1.0, h: 2.0,
      fontSize: 34, bold: true, color: C.white, align: "center", valign: "middle", wrap: true, fontFace: font });
  } else {
    s.addText(title, { x: 0.5, y: 1.3, w: W - 1.0, h: 2.5,
      fontSize: 32, bold: true, color: C.white, align: "center", valign: "middle", wrap: true, fontFace: font });
  }
  if (data.subtitle)
    s.addText(data.subtitle, { x: 0.5, y: H - 1.2, w: W - 1.0, h: 0.6,
      fontSize: 18, color: C.slate, align: "center", fontFace: font });
}

// ── content ────────────────────────────────────────────────────────
function makeContentSlide(pptx, data, C, font, globalLogo, logoSlides) {
  const s = pptx.addSlide();
  s.background = { color: C.white };
  addHeader(s, data.title || "", C, font);
  if (logoSlides === "header" && globalLogo) addLogo(s, globalLogo);

  const imgPath = resolveAsset(data.image || "");
  const imgPos  = data.image_position || "right";
  const hasImg  = !!imgPath;
  const contentW = hasImg && imgPos === "right" ? W * 0.57 : W - 0.65;
  let y = 0.72;
  const yMax = H - 0.15;

  for (const item of (data.content || [])) {
    if (y >= yMax - 0.3) break;
    const text  = typeof item === "string" ? item : (item.text || "");
    const level = typeof item === "string" ? 0 : (item.level || 0);
    if (!text) { y += 0.12; continue; }
    if (level === 0) {
      s.addShape("rect", { x: 0.4, y: y + 0.09, w: 0.07, h: 0.3,
        fill: { color: C.accent }, line: { color: C.accent, width: 0.01 } });
      s.addText(text, { x: 0.55, y, w: contentW - 0.2, h: 0.48,
        fontSize: 18, bold: true, color: C.primary,
        align: "left", valign: "middle", wrap: true, fontFace: font });
      y += 0.53;
    } else {
      s.addText(text, { x: 0.7, y, w: contentW - 0.35, h: 0.38,
        fontSize: 14, color: C.dim, align: "left", valign: "middle", wrap: true, fontFace: font });
      y += 0.41;
    }
  }

  if (hasImg && imgPos === "right") {
    const ix = contentW + 0.45;
    s.addImage({ path: imgPath, x: ix, y: 0.72, w: W - ix - 0.2, h: H - 0.9 });
  } else if (hasImg) {
    s.addImage({ path: imgPath, x: 0.4, y: y + 0.1, w: W - 0.8, h: yMax - y - 0.15 });
  } else if (data.image && !hasImg) {
    SHAPE(s, contentW + 0.5, 0.72, W - contentW - 0.7, H - 0.9, C.snow, C.slate, "dash");
    TXT(s, `【図】${data.image_alt || data.image}`, contentW + 0.5, 0.72,
      W - contentW - 0.7, H - 0.9, { size: 13, color: C.dim, italic: true, align: "center", font });
  }
}

// ── two_column ─────────────────────────────────────────────────────
function makeTwoColumnSlide(pptx, data, C, font, globalLogo, logoSlides) {
  const s = pptx.addSlide();
  s.background = { color: C.white };
  addHeader(s, data.title || "", C, font);
  if (logoSlides === "header" && globalLogo) addLogo(s, globalLogo);

  const colW = 4.25, colH = H - 0.78, colY = 0.7;
  const leftX = 0.35, rightX = 5.4;

  SHAPE(s, leftX,  colY, colW, colH, C.altBg,  C.border);
  SHAPE(s, leftX,  colY, colW, 0.4,  C.primary, "none");
  SHAPE(s, rightX, colY, colW, colH, C.warmBg,  C.border);
  SHAPE(s, rightX, colY, colW, 0.4,  C.accent,  "none");

  TXT(s, data.left_title  || "", leftX,  colY + 0.02, colW, 0.38,
    { size: 14, bold: true, color: "FFFFFF", align: "center", font });
  TXT(s, data.right_title || "", rightX, colY + 0.02, colW, 0.38,
    { size: 14, bold: true, color: "FFFFFF", align: "center", font });

  function renderCol(items, ox, startY) {
    let iy = startY;
    const maxY = colY + colH - 0.1;
    for (const item of (items || [])) {
      if (iy >= maxY - 0.3) break;
      const text = typeof item === "string" ? item : (item.text || "");
      if (!text) { iy += 0.1; continue; }
      s.addText("▸ " + text, { x: ox + 0.12, y: iy, w: colW - 0.24, h: 0.4,
        fontSize: 14, color: C.text, align: "left", valign: "middle", wrap: true, fontFace: font });
      iy += 0.42;
    }
  }
  renderCol(data.left  || [], leftX,  colY + 0.44);
  renderCol(data.right || [], rightX, colY + 0.44);
}

// ── stat ───────────────────────────────────────────────────────────
function makeStatSlide(pptx, data, C, font) {
  const s = pptx.addSlide();
  s.background = { color: C.primary };
  SHAPE(s, 0, H - 0.25, W, 0.25, C.accent, "none");

  // タイトル
  s.addText(data.title || "", { x: 0.5, y: 0.18, w: W - 1.0, h: 0.65,
    fontSize: 22, bold: true, color: C.white, align: "center", fontFace: font });
  if (data.subtitle)
    s.addText(data.subtitle, { x: 0.5, y: 0.85, w: W - 1.0, h: 0.4,
      fontSize: 14, color: C.slate, align: "center", fontFace: font });

  const stats = (data.stats || []).slice(0, 4);
  const n     = stats.length;
  const colW  = (W - 0.6) / n;
  const startX = 0.3;

  for (let i = 0; i < n; i++) {
    const st = stats[i];
    const cx = startX + i * colW;
    const isHighlight = st.highlight === true;

    // カードボックス
    SHAPE(s, cx + 0.1, 1.35, colW - 0.2, 3.6,
      isHighlight ? C.accent : "1E293B", "none");

    // 数値
    s.addText(st.value || "", { x: cx + 0.1, y: 1.55, w: colW - 0.2, h: 1.6,
      fontSize: n <= 2 ? 56 : 42, bold: true,
      color: isHighlight ? C.white : C.accent,
      align: "center", valign: "middle", wrap: true, fontFace: font });

    // 区切り線
    SHAPE(s, cx + 0.4, 3.25, colW - 0.8, 0.02, isHighlight ? C.white : C.accent, "none");

    // ラベル
    s.addText(st.label || "", { x: cx + 0.1, y: 3.35, w: colW - 0.2, h: 1.3,
      fontSize: 13, color: isHighlight ? C.white : C.slate,
      align: "center", valign: "top", wrap: true, fontFace: font });
  }
}

// ── chart ──────────────────────────────────────────────────────────
function makeChartSlide(pptx, data, C, font) {
  const s = pptx.addSlide();
  s.background = { color: C.white };
  addHeader(s, data.title || "", C, font);

  const chartType = (data.chart_type || "bar").toLowerCase();
  const opts = data.chart_options || {};
  const rawData = data.chart_data || [];

  const CHART_COLORS = [C.accent, C.primary, C.dim, "94A3B8", "6366F1"];

  // PptxGenJS chart data format
  const pptxData = rawData.map(series => ({
    name:   series.name   || "",
    labels: series.labels || [],
    values: series.values || [],
  }));

  if (pptxData.length === 0) return;

  const isPie  = chartType === "pie" || chartType === "doughnut";
  const isLine = chartType === "line";

  const chartX = isPie ? 0.5 : 0.4;
  const chartY = 0.72;
  const chartW = isPie ? 5.5 : W - 0.8;
  const chartH = H - chartY - 0.18;

  const commonOpts = {
    x: chartX, y: chartY, w: chartW, h: chartH,
    showLegend:   opts.show_legend !== false,
    legendPos:    isPie ? "r" : "b",
    legendFontSize: 12,
    showTitle:    false,
    dataLabelFontSize: 11,
    catAxisLabelColor:  C.dim,
    valAxisLabelColor:  C.dim,
    catAxisLabelFontSize: 11,
    valAxisLabelFontSize: 11,
  };

  if (isPie) {
    Object.assign(commonOpts, {
      chartColors:  CHART_COLORS,
      showLabel:    true,
      showPercent:  opts.show_percent !== false,
      showValue:    opts.show_value === true,
      dataLabelColor: C.white,
      dataLabelFontFace: font,
    });
    const pptxChartType = chartType === "doughnut" ? pptx.ChartType.doughnut : pptx.ChartType.pie;
    s.addChart(pptxChartType, pptxData, commonOpts);
  } else if (isLine) {
    Object.assign(commonOpts, {
      chartColors:   CHART_COLORS,
      lineDataSymbol: "none",
      showValue:     opts.show_value === true,
    });
    s.addChart(pptx.ChartType.line, pptxData, commonOpts);
  } else {
    // bar
    const barDir = opts.bar_dir === "bar" ? "bar" : "col";
    Object.assign(commonOpts, {
      barDir,
      barGapWidthPct: 50,
      chartColors:    CHART_COLORS,
      showValue:      opts.show_value !== false,
      dataLabelColor: C.white,
      dataLabelFontFace: font,
      valAxisMinVal:  0,
    });
    s.addChart(pptx.ChartType.bar, pptxData, commonOpts);
  }

  // サブタイトル／注記
  if (data.subtitle) {
    TXT(s, data.subtitle, 0.4, H - 0.38, W - 0.8, 0.3,
      { size: 11, color: C.dim, align: "center", font });
  }
}

// ── image ──────────────────────────────────────────────────────────
function makeImageSlide(pptx, data, C, font) {
  const s = pptx.addSlide();
  s.background = { color: C.white };
  addHeader(s, data.title || "", C, font);
  const caption = data.caption || "";
  const captH   = caption ? 0.38 : 0;
  const imgPath = resolveAsset(data.image || "");
  if (imgPath) {
    s.addImage({ path: imgPath, x: 0.4, y: 0.72, w: W - 0.8, h: H - 0.9 - captH });
  } else {
    SHAPE(s, 0.4, 0.72, W - 0.8, H - 0.9 - captH, C.snow, C.slate, "dash");
    TXT(s, `【図解】${data.image_alt || data.image || ""}`, 0.4, 0.72, W - 0.8, H - 0.9 - captH,
      { size: 14, color: C.dim, italic: true, align: "center", font });
  }
  if (caption) TXT(s, caption, 0.4, H - captH - 0.08, W - 0.8, captH,
    { size: 11, color: C.dim, align: "center", font });
}

// ── closing ────────────────────────────────────────────────────────
function makeClosingSlide(pptx, data, C, font, globalLogo) {
  const s = pptx.addSlide();
  s.background = { color: C.primary };
  SHAPE(s, 0.6, 1.1, W - 1.2, 3.4, C.white, "none");
  SHAPE(s, 0, H - 0.35, W, 0.35, C.accent, "none");
  s.addText(data.title || "", { x: 0.9, y: 1.25, w: W - 1.8, h: 1.6,
    fontSize: 30, bold: true, color: C.primary,
    align: "center", valign: "middle", wrap: true, fontFace: font });
  if (data.subtitle) s.addText(data.subtitle, { x: 0.9, y: 2.9, w: W - 1.8, h: 1.35,
    fontSize: 16, color: C.dim, align: "center", valign: "top", wrap: true, fontFace: font });
  const logo = data.logo || globalLogo;
  if (logo) { const p = resolveAsset(logo); if (p) s.addImage({ path: p, x: W/2-1, y: 0.25, w: 2, h: 0.7 }); }
}

// ────────────────────────────────────────────────────────────────────
// メイン
// ────────────────────────────────────────────────────────────────────

async function createPptx(slidesJsonPath, outputPath, styleGuidePath) {
  const data       = JSON.parse(fs.readFileSync(slidesJsonPath, "utf8"));
  const styleGuide = styleGuidePath && fs.existsSync(styleGuidePath)
    ? JSON.parse(fs.readFileSync(styleGuidePath, "utf8"))
    : { has_references: false, extracted_colors: [], fonts: [] };

  const C    = buildPalette(styleGuide, data.style || {});
  const font = resolveFont(styleGuide, data.style || {});
  const meta = data.metadata || {};
  const globalLogo = meta.logo || "";
  const logoSlides = meta.logo_slides || "none";

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_16x9";
  pptx.title  = meta.title || "";

  const placeholders = [];

  for (let i = 0; i < (data.slides || []).length; i++) {
    const slide = data.slides[i];
    const type  = slide.type || "content";
    switch (type) {
      case "title":      makeTitleSlide(pptx, slide, C, font, globalLogo); break;
      case "section":    makeSectionSlide(pptx, slide, C, font); break;
      case "content":
        makeContentSlide(pptx, slide, C, font, globalLogo, logoSlides);
        if (slide.image && !resolveAsset(slide.image))
          placeholders.push({ slide: i+1, file: slide.image, alt: slide.image_alt || "" });
        break;
      case "two_column": makeTwoColumnSlide(pptx, slide, C, font, globalLogo, logoSlides); break;
      case "stat":       makeStatSlide(pptx, slide, C, font); break;
      case "chart":      makeChartSlide(pptx, slide, C, font); break;
      case "image":
        makeImageSlide(pptx, slide, C, font);
        if (slide.image && !resolveAsset(slide.image))
          placeholders.push({ slide: i+1, file: slide.image, alt: slide.image_alt || "" });
        break;
      case "closing":    makeClosingSlide(pptx, slide, C, font, globalLogo); break;
      default:           makeContentSlide(pptx, slide, C, font, globalLogo, logoSlides);
    }
  }

  await pptx.writeFile({ fileName: outputPath });

  const slideCount = (data.slides || []).length;
  console.log(`✅ 生成完了: ${outputPath}`);
  console.log(`   スライド枚数: ${slideCount}`);
  console.log(`   スタイル: primary=#${C.primary}  accent=#${C.accent}`);
  console.log(`   フォント: ${font}`);
  if (placeholders.length > 0) {
    console.log(`\n📌 プレースホルダー: ${placeholders.length} 件`);
    for (const ph of placeholders) {
      console.log(`   スライド ${ph.slide}: assets/${ph.file}`);
      if (ph.alt) console.log(`     → ${ph.alt}`);
    }
    console.log('\n画像の準備ができたら「画像差し替えお願いします」と送信してください。');
  }
  return { outputPath, slideCount, placeholders };
}

// ── CLI ──────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length < 2) {
  console.error("Usage: node create_pptx.js slides.json output.pptx [style_guide.json]");
  process.exit(1);
}
const [slidesJson, outPptx, styleGuideJson] = args;

createPptx(slidesJson, outPptx, styleGuideJson || null).catch(err => {
  console.error("❌ エラー:", err.message);
  process.exit(1);
});

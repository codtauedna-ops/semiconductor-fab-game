#!/usr/bin/env node
/**
 * Semiconductor Engineering Game (半导体工程小游戏)
 * Node.js Dual-Track E2E Test Suite Runner (Tiers 1, 2, 3)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const GAME_ROOT = path.resolve(__dirname, '..');
const HANT_DIR = path.join(GAME_ROOT, 'g', 'zh-Hant');

let total = 0;
let passed = 0;
let failed = 0;

function assertTest(name, cond, details = '') {
  total++;
  if (cond) {
    passed++;
    console.log(`  \x1b[32m[PASS]\x1b[0m ${name}`);
  } else {
    failed++;
    console.log(`  \x1b[31m[FAIL]\x1b[0m ${name} ${details ? '- ' + details : ''}`);
  }
}

console.log('\n======================================================================');
console.log('   半导体工程小游戏 NODE.JS E2E TEST RUNNER (TIERS 1 - 3)');
console.log('======================================================================\n');

// --- Tier 1: Syntax & Static Integrity ---
console.log('\x1b[36m\x1b[1m--- Tier 1: Syntax & Static Integrity ---\x1b[0m');
function getJsFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getJsFiles(fullPath));
    } else if (file.endsWith('.js')) {
      results.push(fullPath);
    }
  });
  return results;
}

const allJsFiles = getJsFiles(path.join(GAME_ROOT, 'g'));
assertTest(`File count validation (Found ${allJsFiles.length} JS files)`, allJsFiles.length === 47);

let syntaxErrors = [];
for (const file of allJsFiles) {
  try {
    execSync(`node --check "${file}"`, { stdio: 'pipe' });
  } catch (err) {
    syntaxErrors.push({ file: path.relative(GAME_ROOT, file), err: err.message });
  }
}
assertTest(`Automated node --check across all ${allJsFiles.length} JavaScript files`, syntaxErrors.length === 0);

// --- Tier 2: Narrative & Schema Coverage ---
console.log('\n\x1b[36m\x1b[1m--- Tier 2: Narrative & Schema Coverage ---\x1b[0m');
const c2lr = fs.readFileSync(path.join(HANT_DIR, 'c-2LRXZS7F.js'), 'utf8');
const ctqd = fs.readFileSync(path.join(HANT_DIR, 'c-TQDJ64WG.js'), 'utf8');
const cpuj = fs.readFileSync(path.join(HANT_DIR, 'c-PUJY3LHM.js'), 'utf8');
const cqba = fs.readFileSync(path.join(HANT_DIR, 'c-QBAOZAHQ.js'), 'utf8');
const cdhz = fs.readFileSync(path.join(HANT_DIR, 'c-DHZ6C35K.js'), 'utf8');
const ckx2 = fs.readFileSync(path.join(HANT_DIR, 'c-KX2QCJCP.js'), 'utf8');
const cmain = fs.readFileSync(path.join(HANT_DIR, 'main-QUKU62T2.js'), 'utf8');
const czh = fs.readFileSync(path.join(GAME_ROOT, 'g', 'zh-convert.js'), 'utf8');
const chtml = fs.readFileSync(path.join(GAME_ROOT, 'index.html'), 'utf8');

assertTest('Chapter 1 (c1: 12片怎麼分)', ['24電科（閩台）1班 3246117007', '唐敬堯老師', '趙泓博nb666', '螢火'].every(k => c2lr.includes(k)));
assertTest('Chapter 2 (c13: 一站一站)', ctqd.includes('終點後偷磨 5 秒，此生無悔 —— nb666') && ctqd.includes('趙泓博nb666') && ctqd.includes('螢火'));
assertTest('Chapter 3 (c2: 壞的形狀)', ['壞的形狀', '唐敬堯', '趙泓博', 'WAT'].every(k => c2lr.includes(k)));
assertTest('Chapter 4 (c3: 提早兩週)', ['提早兩週', '唐敬堯', '趙泓博', 'HTOL'].every(k => c2lr.includes(k)));
assertTest('Chapter 5 (c4: 最後一格)', cpuj.includes('# Tuned by ZhaoHongbo (nb666)') && cpuj.includes('趙泓博nb666') && cpuj.includes('螢火'));
assertTest('Chapter 6 (c5: 那通電話)', ['02:47', 'ETCH-03', 'nb666_esc_dechuck.rcp', '唐敬堯', '趙泓博'].every(k => cqba.includes(k)));
assertTest('Chapter 7 (c6: 救火)', ['開腔的人', '18nm', '唐敬堯', '趙泓博', '15Nm'].every(k => cqba.includes(k)));
assertTest('Chapter 8 (c7: 趕時間)', ['MES', '18nm', '唐敬堯', '趙泓博', '軟蝕刻'].every(k => cqba.includes(k)));
assertTest('Chapter 9 (c8: 下班未遂)', ['下班未遂', 'Cpk', '唐敬堯', '趙泓博', 'VCR'].every(k => cqba.includes(k)));
assertTest('Chapter 10 (c9: 待機電流)', ['待機電流', 'PAT', '趙泓博nb666', '離群點'].every(k => cdhz.includes(k)));
assertTest('Chapter 11 (c10: 球掀起來了)', ['球掀起來了', '紫斑', 'Reverse Bumping', '趙泓博nb666'].every(k => cdhz.includes(k)));
assertTest('Chapter 12 (c11: 出貨前一晚)', ['出貨前一晚', '早期失效', '24電科', '趙泓博nb666', '螢火'].every(k => cdhz.includes(k)));
assertTest('Chapter 13 (c12: 交到他手上)', ['鋅空氣電池', '4.2ms', '梳狀濾波', '唐敬堯', '趙泓博nb666', '螢火'].every(k => ckx2.includes(k)));

assertTest('ALT shifts (c5..c8: mfg, ee, pie, fac)', [
  'c5:{job:"mfg",sh:"night",seat:"製造部・深夜班",title:"打電話的那一邊"',
  'c6:{job:"ee",sh:"am",seat:"設備・蝕刻・早班",title:"開腔的人"',
  'c7:{job:"pie",sh:"pm",seat:"製程整合・午班",title:"開指示的人"',
  'c8:{job:"fac",sh:"eve",seat:"廠務・晚班",title:"同一個接頭"'
].every(k => cqba.includes(k)));

assertTest('ROLE definition (tang, zhao)', cqba.includes('tang:{name:"唐敬堯老師",role:"高校產研導師"') && cqba.includes('zhao:{name:"趙泓博nb666",role:"資深架構師"'));
assertTest('PSEUDO mappings (mtang, ttang, mzhao, tzhao)', ['mtang:[', 'ttang:[', 'mzhao:[', 'tzhao:['].every(k => cqba.includes(k)));
assertTest('EVS registration (ev_tang_quiz, ev_zhao_rescue)', cmain.includes('ev_tang_quiz') && cmain.includes('ev_zhao_rescue'));
assertTest('zh-convert.js PHRASES & PHRASES_REV', czh.includes('24電科（閩台）1班 3246117007') && czh.includes('PHRASES_REV') && czh.includes('showEasterEggModal'));
assertTest('index.html easterEggModal & #hLed binding', ['id="easterEggModal"', 'showEasterEggModal()', '24电科（闽台）1班 3246117007 重点产研专案', '赵泓博nb666'].every(k => chtml.includes(k)));

// --- Tier 3: State Machine & Causal Ending Simulation ---
console.log('\n\x1b[36m\x1b[1m--- Tier 3: State Machine & Causal Ending Simulation ---\x1b[0m');
const mockStore = {};
function chipGet(k) { return mockStore[k] || {}; }
const fnStart = cqba.indexOf('function chipFate(');
const fnEnd = cqba.indexOf('var JOBS=', fnStart);
const chipFateFn = new Function('chipGet', 'mockStore', cqba.slice(fnStart, fnEnd) + '; return chipFate();');

// Baseline -> Ending B
mockStore['a1am'] = {ff: 2}; mockStore['a1pm'] = {key: 0}; mockStore['a1ev'] = {risk: 0};
mockStore['a1me'] = {lim: 12}; mockStore['a3cp'] = {v: ''}; mockStore['a3wb'] = {stop: 1}; mockStore['a3sh'] = {elfr: 0};
const v1 = chipFateFn(chipGet, mockStore);
assertTest('Vector 1 [Baseline]: risk=0, stop=1, elfr=0, lim=12 -> late=2.5, ontime=false -> Ending B', v1.end === 'B' && v1.late === 2.5 && !v1.ontime);

// Ending A
mockStore['a1ev'] = {risk: 1};
const v2 = chipFateFn(chipGet, mockStore);
assertTest('Vector 2 [Perfect]: risk=1, stop=1, elfr=0 -> late=0.5, ontime=true -> Ending A', v2.end === 'A' && v2.late === 0.5 && v2.ontime);

// Ending C (leak)
mockStore['a3cp'] = {v: 'loose'};
const v3 = chipFateFn(chipGet, mockStore);
assertTest('Vector 3 [Defect]: cp.v="loose" -> leak=true, ret=true -> Ending C', v3.end === 'C' && v3.leak && v3.ret);

// Ending C (bond)
mockStore['a3cp'] = {v: ''}; mockStore['a3wb'] = {stop: 0}; mockStore['a3sh'] = {elfr: 0};
const v4 = chipFateFn(chipGet, mockStore);
assertTest('Vector 4 [Defect]: stop=0, elfr=0 -> bond=true, ret=true -> Ending C', v4.end === 'C' && v4.bond && v4.ret);

// Boundary
mockStore['a1ev'] = {risk: 1}; mockStore['a3cp'] = {v: 'tight'}; mockStore['a3wb'] = {stop: 1}; mockStore['a3sh'] = {elfr: 0};
const v5 = chipFateFn(chipGet, mockStore);
assertTest('Vector 5 [Boundary]: late=1.5 -> ontime=true (Ending A)', v5.late === 1.5 && v5.end === 'A');

console.log('\n----------------------------------------------------------------------');
console.log(`Node.js Total: ${total} | Passed: \x1b[32m${passed}\x1b[0m | Failed: ${failed ? '\x1b[31m' + failed + '\x1b[0m' : '0'}`);
console.log('======================================================================\n');

process.exit(failed === 0 ? 0 : 1);

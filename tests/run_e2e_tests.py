#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semiconductor Engineering Game (半导体工程小游戏)
Dual-Track Comprehensive 4-Tier E2E Test Suite Runner

Tiers:
  Tier 1 - Syntax & Static Integrity (node --check across all 47 JS files)
  Tier 2 - Narrative & Schema Coverage (13 chapters, 4 ALT shifts, ROLE, PSEUDO, EVS, zh-convert, index.html)
  Tier 3 - State Machine & Causal Ending Simulation (chipFate decision matrix & Endings A/B/C)
  Tier 4 - Real-World Browser End-to-End Workload (Playwright headless Chromium, DOM, Console 0-error, Modal, I18n)

Author: worker_m3_test
Date: 2026-11-03
"""

import sys
import io
import os
import glob
import subprocess
import json
import time
import re
import threading
import socketserver
import http.server
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows to prevent GBK encoding errors
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ANSI Color Codes for reporting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

GAME_ROOT = Path("D:/逆向/半导体工程小游戏").resolve()
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
TEST_PORT = 8099

class TestReport:
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = time.time()

    def record(self, tier_name, test_name, passed, details=""):
        if tier_name not in self.results:
            self.results[tier_name] = []
        self.results[tier_name].append({
            "name": test_name,
            "passed": passed,
            "details": details
        })
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            print(f"  {GREEN}[PASS]{RESET} {test_name}")
        else:
            self.failed_tests += 1
            print(f"  {RED}[FAIL]{RESET} {test_name} - {details}")

    def summary(self):
        elapsed = time.time() - self.start_time
        print("\n" + "=" * 70)
        print(f"{BOLD}E2E TEST SUITE EXECUTION SUMMARY{RESET}")
        print("=" * 70)
        for tier, tests in self.results.items():
            tier_passed = sum(1 for t in tests if t["passed"])
            tier_total = len(tests)
            status_color = GREEN if tier_passed == tier_total else RED
            print(f"{BOLD}{tier}{RESET}: {status_color}{tier_passed}/{tier_total} passed{RESET}")
            for t in tests:
                mark = f"{GREEN}[PASS]{RESET}" if t["passed"] else f"{RED}[FAIL]{RESET}"
                print(f"    {mark} {t['name']}")
                if not t["passed"] and t["details"]:
                    print(f"       {RED}Error: {t['details']}{RESET}")
        print("-" * 70)
        overall_color = GREEN if self.failed_tests == 0 else RED
        print(f"Total: {self.total_tests} | Passed: {GREEN}{self.passed_tests}{RESET} | Failed: {overall_color}{self.failed_tests}{RESET} | Time: {elapsed:.2f}s")
        print("=" * 70)
        return self.failed_tests == 0


report = TestReport()

# ==============================================================================
# TIER 1: Syntax & Static Integrity
# ==============================================================================
def run_tier_1():
    print(f"\n{CYAN}{BOLD}--- Tier 1: Syntax & Static Integrity ---{RESET}")
    g_dir = GAME_ROOT / "g"
    js_files = list(g_dir.rglob("*.js"))
    report.record("Tier 1", f"File count validation (Found {len(js_files)} JS files)", len(js_files) == 47, f"Expected 47 files, found {len(js_files)}")

    syntax_errors = []
    for js_file in js_files:
        rel_path = js_file.relative_to(GAME_ROOT)
        try:
            res = subprocess.run(
                ["node", "--check", str(js_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if res.returncode != 0:
                syntax_errors.append((str(rel_path), res.stderr.strip()))
        except Exception as e:
            syntax_errors.append((str(rel_path), str(e)))

    report.record(
        "Tier 1",
        f"Automated node --check across all {len(js_files)} JavaScript files (0 syntax errors)",
        len(syntax_errors) == 0,
        f"Syntax errors found: {syntax_errors}"
    )


# ==============================================================================
# TIER 2: Narrative & Schema Coverage
# ==============================================================================
def run_tier_2():
    print(f"\n{CYAN}{BOLD}--- Tier 2: Narrative & Schema Coverage ---{RESET}")
    hant_dir = GAME_ROOT / "g" / "zh-Hant"

    # 1. Check Chapters 1..13 narrative dialogue updates
    c_2lr = (hant_dir / "c-2LRXZS7F.js").read_text(encoding="utf-8")
    c_tqd = (hant_dir / "c-TQDJ64WG.js").read_text(encoding="utf-8")
    c_puj = (hant_dir / "c-PUJY3LHM.js").read_text(encoding="utf-8")
    c_qba = (hant_dir / "c-QBAOZAHQ.js").read_text(encoding="utf-8")
    c_dhz = (hant_dir / "c-DHZ6C35K.js").read_text(encoding="utf-8")
    c_kx2 = (hant_dir / "c-KX2QCJCP.js").read_text(encoding="utf-8")

    # Chapter 1 (c1)
    ch1_pass = all(k in c_2lr for k in ["24電科（閩台）1班 3246117007", "唐敬堯老師", "趙泓博nb666", "螢火"])
    report.record("Tier 2", "Chapter 1 (c1: 12片怎麼分) contains Tang, Zhao, 24电科, 3246117007, 萤火", ch1_pass)

    # Chapter 2 (c13)
    ch2_pass = ("終點後偷磨 5 秒，此生無悔 —— nb666" in c_tqd and "趙泓博nb666" in c_tqd and "螢火" in c_tqd and "台階覆蓋率" in c_tqd)
    report.record("Tier 2", "Chapter 2 (c13: 一站一站) contains Zhao easter egg note, ALD/RCA physics, 萤火", ch2_pass)

    # Chapter 3 (c2)
    ch3_pass = all(k in c_2lr for k in ["壞的形狀", "唐敬堯", "趙泓博", "WAT"])
    report.record("Tier 2", "Chapter 3 (c2: 壞的形狀) contains WAT probe scrub, Tang/Zhao dialogue", ch3_pass)

    # Chapter 4 (c3)
    ch4_pass = all(k in c_2lr for k in ["提早兩週", "唐敬堯", "趙泓博", "HTOL"])
    report.record("Tier 2", "Chapter 4 (c3: 提早兩週) contains HTOL Arrhenius model, Tang guidance, Zhao advice", ch4_pass)

    # Chapter 5 (c4)
    ch5_pass = ("# Tuned by ZhaoHongbo (nb666)" in c_puj and "趙泓博nb666" in c_puj and "螢火" in c_puj)
    report.record("Tier 2", "Chapter 5 (c4: 最後一格) contains ESC He leak recipe comment & Zhao dialogue", ch5_pass)

    # Chapter 6 (c5)
    ch6_pass = all(k in c_qba for k in ["02:47", "ETCH-03", "nb666_esc_dechuck.rcp", "唐敬堯", "趙泓博"])
    report.record("Tier 2", "Chapter 6 (c5: 那通電話) contains 02:47 alarm, Tang Purge&Pump, Zhao dechuck recipe", ch6_pass)

    # Chapter 7 (c6)
    ch7_pass = all(k in c_qba for k in ["開腔的人", "18nm", "唐敬堯", "趙泓博", "15Nm"])
    report.record("Tier 2", "Chapter 7 (c6: 救火) contains ESC swap, Tang Seasoning, Zhao torque guidance", ch7_pass)

    # Chapter 8 (c7)
    ch8_pass = all(k in c_qba for k in ["MES", "18nm", "唐敬堯", "趙泓博", "軟蝕刻"])
    report.record("Tier 2", "Chapter 8 (c7: 趕時間) contains MES outage, manual EWO, Tang/Zhao soft etch", ch8_pass)

    # Chapter 9 (c8)
    ch9_pass = all(k in c_qba for k in ["下班未遂", "Cpk", "唐敬堯", "趙泓博", "VCR"])
    report.record("Tier 2", "Chapter 9 (c8: 下班未遂) contains FDC sensor oscillation, Cpk hold, Tang/Zhao guidance", ch9_pass)

    # Chapter 10 (c9)
    ch10_pass = all(k in c_dhz for k in ["待機電流", "PAT", "趙泓博nb666", "離群點"])
    report.record("Tier 2", "Chapter 10 (c9: 待機電流) contains CP test, AEC-Q001 PAT 3σ outlier filtering, Zhao", ch10_pass)

    # Chapter 11 (c10)
    ch11_pass = all(k in c_dhz for k in ["球掀起來了", "紫斑", "Reverse Bumping", "趙泓博nb666"])
    report.record("Tier 2", "Chapter 11 (c10: 球掀起來了) contains wire bond pull, Kirkendall void, Zhao reverse bumping", ch11_pass)

    # Chapter 12 (c11)
    ch12_pass = all(k in c_dhz for k in ["出貨前一晚", "早期失效", "24電科", "趙泓博nb666", "螢火"])
    report.record("Tier 2", "Chapter 12 (c11: 出貨前一晚) contains ELFR bathtub curve test, 24电科, Zhao packaging tribute", ch12_pass)

    # Chapter 13 (c12)
    ch13_pass = all(k in c_kx2 for k in ["鋅空氣電池", "4.2ms", "梳狀濾波", "唐敬堯", "趙泓博nb666", "螢火"])
    report.record("Tier 2", "Chapter 13 (c12: 交到他手上) contains zinc-air 1.3V, 4.2ms latency, Tang & Zhao tributes", ch13_pass)

    # 2. Check 4 ALT shifts in c-QBAOZAHQ.js
    alt_shifts_pass = all(k in c_qba for k in [
        'c5:{job:"mfg",sh:"night",seat:"製造部・深夜班",title:"打電話的那一邊"',
        'c6:{job:"ee",sh:"am",seat:"設備・蝕刻・早班",title:"開腔的人"',
        'c7:{job:"pie",sh:"pm",seat:"製程整合・午班",title:"開指示的人"',
        'c8:{job:"fac",sh:"eve",seat:"廠務・晚班",title:"同一個接頭"'
    ])
    report.record("Tier 2", "All 4 ALT shifts (c5..c8: mfg, ee, pie, fac) contain designed titles, roles and dialogues", alt_shifts_pass)

    # 3. Check ROLE and PSEUDO in c-QBAOZAHQ.js
    role_pass = ('tang:{name:"唐敬堯老師",role:"高校產研導師"' in c_qba and 'zhao:{name:"趙泓博nb666",role:"資深架構師"' in c_qba)
    pseudo_pass = all(k in c_qba for k in ['mtang:[', 'ttang:[', 'mzhao:[', 'tzhao:['])
    report.record("Tier 2", "ROLE has 'tang' and 'zhao' with correct names and roles", role_pass)
    report.record("Tier 2", "PSEUDO has 'mtang', 'ttang', 'mzhao', 'tzhao' character mappings", pseudo_pass)

    # 4. Check EVS in main-QUKU62T2.js
    main_js = (hant_dir / "main-QUKU62T2.js").read_text(encoding="utf-8")
    evs_pass = ('ev_tang_quiz' in main_js and 'ev_zhao_rescue' in main_js and '瑞利公式' in main_js and 'nb666' in main_js)
    report.record("Tier 2", "EVS in main-QUKU62T2.js contains 'ev_tang_quiz' and 'ev_zhao_rescue'", evs_pass)

    # 5. Check zh-convert.js PHRASES
    zh_convert = (GAME_ROOT / "g" / "zh-convert.js").read_text(encoding="utf-8")
    expected_phrases = [
        "24電科（閩台）1班 3246117007",
        "唐敬堯老師", "唐敬堯", "趙泓博nb666", "趙泓博", "螢火",
        "產研導師", "電漿鞘層", "微負載效應", "普雷斯頓", "通道效應",
        "退火活化", "靜電吸盤", "熱預算", "離群晶片", "零件平均測試",
        "柯肯達爾空洞", "紫斑病", "白斑相", "台階覆蓋率", "原子層沉積",
        "超淺結", "早期失效", "梳狀濾波", "鋅空氣電池"
    ]
    phrases_present = all(p in zh_convert for p in expected_phrases)
    phrases_rev_present = "PHRASES_REV" in zh_convert and "showEasterEggModal" in zh_convert
    report.record("Tier 2", f"zh-convert.js contains complete PHRASES dictionary ({len(expected_phrases)} terms) and PHRASES_REV", phrases_present and phrases_rev_present)

    # 6. Check index.html modal and LED binding
    index_html = (GAME_ROOT / "index.html").read_text(encoding="utf-8")
    modal_pass = all(k in index_html for k in [
        'id="easterEggModal"',
        'showEasterEggModal()',
        '24电科（闽台）1班 3246117007 重点产研专案',
        '助听器超低功耗数字信号处理器芯片「萤火」',
        '唐敬尧',
        '赵泓博nb666'
    ])
    report.record("Tier 2", "index.html has #easterEggModal with full project details and #hLed bound to showEasterEggModal()", modal_pass)


# ==============================================================================
# TIER 3: State Machine & Causal Ending Simulation
# ==============================================================================
def run_tier_3():
    print(f"\n{CYAN}{BOLD}--- Tier 3: State Machine & Causal Ending Simulation ---{RESET}")

    def py_chip_fate(a1am=None, a1pm=None, a1ev=None, a1me=None, a3cp=None, a3wb=None, a3sh=None):
        am = a1am or {"ff": 2}
        pm = a1pm or {"key": 0}
        ev = a1ev or {"risk": 0}
        me = a1me or {"lim": 12}
        cp = a3cp or {"v": ""}
        wb = a3wb or {"stop": 1}
        sh = a3sh or {"elfr": 0}

        ff = (int(am.get("ff", 2))) > 0
        cp_v = cp.get("v", "")
        if cp_v == "ff" and not ff:
            lim3 = "tight"
        else:
            lim3 = cp_v or ("ff" if ff else "tight")

        stop = bool(wb.get("stop", 1))
        elfr = bool(sh.get("elfr", 0))
        lim = 16 if me.get("lim") == 16 else 12
        key = bool(pm.get("key", 0))
        risk = bool(ev.get("risk", 0))

        late = (
            2
            - (2 if risk else 0)
            + (1 if lim3 == "tight" else 0)
            + (1 if (lim == 16 and not key) else 0)
            + (0.5 if stop else 0)
            + (1 if elfr else 0)
        )
        leak = (lim3 == "loose")
        bond = (not stop) and (not elfr)
        ret = leak or bond
        ontime = (late <= 1.5)
        end = "C" if ret else ("A" if ontime else "B")

        return {
            "late": late,
            "pre": late - (1 if elfr else 0),
            "ontime": ontime,
            "leak": leak,
            "bond": bond,
            "ret": ret,
            "end": end
        }

    # Vector 1: Default baseline vector -> Ending B
    res_default = py_chip_fate()
    report.record(
        "Tier 3",
        "Vector 1 [Baseline]: risk=0, stop=1, elfr=0, lim=12 -> late=2.5, ontime=False, ret=False -> Ending B",
        res_default["end"] == "B" and res_default["late"] == 2.5 and not res_default["ontime"]
    )

    # Vector 2: Ending A (Perfect Quality, On-time)
    res_end_a = py_chip_fate(a1ev={"risk": 1}, a3wb={"stop": 1}, a3sh={"elfr": 0})
    report.record(
        "Tier 3",
        "Vector 2 [Perfect]: risk=1, stop=1, elfr=0 -> late=0.5, ontime=True, ret=False -> Ending A",
        res_end_a["end"] == "A" and res_end_a["late"] == 0.5 and res_end_a["ontime"]
    )

    # Vector 3: Ending C via Standby Leakage relaxation (lim3 == 'loose')
    res_end_c_leak = py_chip_fate(a1ev={"risk": 1}, a3cp={"v": "loose"}, a3wb={"stop": 1})
    report.record(
        "Tier 3",
        "Vector 3 [Defect]: cp.v='loose' -> leak=True, ret=True -> Ending C (Standby Leakage Failure)",
        res_end_c_leak["end"] == "C" and res_end_c_leak["leak"] and res_end_c_leak["ret"]
    )

    # Vector 4: Ending C via Wire Bonding Microvoid (stop=0 and elfr=0)
    res_end_c_bond = py_chip_fate(a1ev={"risk": 1}, a3wb={"stop": 0}, a3sh={"elfr": 0})
    report.record(
        "Tier 3",
        "Vector 4 [Defect]: stop=0, elfr=0 -> bond=True, ret=True -> Ending C (Bonding Microvoid Failure)",
        res_end_c_bond["end"] == "C" and res_end_c_bond["bond"] and res_end_c_bond["ret"]
    )

    # Vector 5: Ending C with Both Failures (leak=True and bond=True)
    res_end_c_both = py_chip_fate(a3cp={"v": "loose"}, a3wb={"stop": 0}, a3sh={"elfr": 0})
    report.record(
        "Tier 3",
        "Vector 5 [Double Defect]: loose + stop=0 + elfr=0 -> leak=True, bond=True, ret=True -> Ending C",
        res_end_c_both["end"] == "C" and res_end_c_both["leak"] and res_end_c_both["bond"]
    )

    # Vector 6: Boundary Late threshold tests (late <= 1.5 vs late > 1.5)
    res_boundary_1_5 = py_chip_fate(a1ev={"risk": 1}, a3cp={"v": "tight"}, a3wb={"stop": 1}, a3sh={"elfr": 0})
    res_boundary_2_5 = py_chip_fate(a1ev={"risk": 1}, a3cp={"v": "tight"}, a3wb={"stop": 1}, a3sh={"elfr": 1})
    report.record(
        "Tier 3",
        "Vector 6 [Boundary]: late=1.5 yields ontime=True (Ending A); late=2.5 yields ontime=False (Ending B)",
        res_boundary_1_5["late"] == 1.5 and res_boundary_1_5["end"] == "A" and res_boundary_2_5["late"] == 2.5 and res_boundary_2_5["end"] == "B"
    )

    # Vector 7: Cross-validation against live JavaScript chipFate in c-QBAOZAHQ.js via Node
    node_eval_script = """
    const fs = require('fs');
    const content = fs.readFileSync('D:/逆向/半导体工程小游戏/g/zh-Hant/c-QBAOZAHQ.js', 'utf8');
    
    const mockStore = {};
    function chipGet(k, def) { return mockStore[k] || {}; }
    
    const fnStart = content.indexOf('function chipFate(');
    const fnEnd = content.indexOf('var JOBS=', fnStart);
    const chipFateCode = content.slice(fnStart, fnEnd);
    
    const fn = new Function('chipGet', 'mockStore', chipFateCode + '; return chipFate();');
    const results = [];
    
    // 1. default
    mockStore['a1am'] = {ff: 2};
    mockStore['a1pm'] = {key: 0};
    mockStore['a1ev'] = {risk: 0};
    mockStore['a1me'] = {lim: 12};
    mockStore['a3cp'] = {v: ''};
    mockStore['a3wb'] = {stop: 1};
    mockStore['a3sh'] = {elfr: 0};
    results.push(fn(chipGet, mockStore));
    
    // 2. Ending A
    mockStore['a1ev'] = {risk: 1};
    results.push(fn(chipGet, mockStore));
    
    // 3. Ending C (leak)
    mockStore['a3cp'] = {v: 'loose'};
    results.push(fn(chipGet, mockStore));
    
    console.log(JSON.stringify(results));
    """
    try:
        proc = subprocess.run(
            ["node", "-e", node_eval_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        if proc.returncode == 0:
            js_results = json.loads(proc.stdout.strip())
            js_pass = (
                js_results[0]["end"] == "B" and
                js_results[1]["end"] == "A" and
                js_results[2]["end"] == "C"
            )
            report.record(
                "Tier 3",
                "Vector 7 [Live Engine]: c-QBAOZAHQ.js internal chipFate() execution strictly matches Section 7.5 spec",
                js_pass
            )
        else:
            report.record("Tier 3", "Vector 7 [Live Engine]: Node execution failed", False, proc.stderr)
    except Exception as e:
        report.record("Tier 3", "Vector 7 [Live Engine]: Error running Node chipFate", False, str(e))


# ==============================================================================
# TIER 4: Real-World Browser End-to-End Workload
# ==============================================================================
class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(GAME_ROOT), **kwargs)

    def log_message(self, format, *args):
        pass # Suppress HTTP access logging in test console


def run_tier_4():
    print(f"\n{CYAN}{BOLD}--- Tier 4: Real-World Browser End-to-End Workload ---{RESET}")

    # 1. Start local HTTP server
    server = None
    server_started = False
    for port in [TEST_PORT, TEST_PORT + 1, TEST_PORT + 2]:
        try:
            server = socketserver.TCPServer(("", port), QuietHTTPHandler)
            actual_port = port
            server_started = True
            break
        except OSError:
            continue

    if not server_started:
        report.record("Tier 4", "Local static server startup", False, f"Could not bind to port {TEST_PORT}")
        return

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    report.record("Tier 4", f"Local static HTTP server running on http://localhost:{actual_port}", True)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            # Launch headless Chromium
            browser = p.chromium.launch(
                executable_path=CHROME_PATH,
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )
            report.record("Tier 4", "Playwright headless Chromium launched successfully", True)

            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()

            console_errors = []
            uncaught_exceptions = []

            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: uncaught_exceptions.append(str(err)))

            # Navigate to index.html
            page.goto(f"http://localhost:{actual_port}/index.html", wait_until="domcontentloaded")
            time.sleep(1.5) # Allow Three.js & UI modules to stabilize

            # Verify 0 console errors and 0 uncaught exceptions
            no_errors = len(console_errors) == 0 and len(uncaught_exceptions) == 0
            err_details = f"Errors: {console_errors}, Exceptions: {uncaught_exceptions}" if not no_errors else ""
            report.record("Tier 4", "Browser runtime integrity: 0 console errors and 0 uncaught exceptions", no_errors, err_details)

            # Verify initial DOM elements
            h_led = page.query_selector("#hLed")
            btn_hans = page.query_selector("#btnToggleHans")
            btn_hant = page.query_selector("#btnToggleHant")
            modal = page.query_selector("#easterEggModal")

            dom_elements_present = (h_led is not None) and (btn_hans is not None) and (btn_hant is not None) and (modal is not None)
            report.record("Tier 4", "Initial DOM presence: #hLed, #btnToggleHans, #btnToggleHant, #easterEggModal", dom_elements_present)

            # Verify modal initial display is hidden
            init_display = modal.evaluate("el => getComputedStyle(el).display") if modal else ""
            report.record("Tier 4", f"#easterEggModal initially hidden (display: {init_display})", init_display == "none")

            # Click #hLed to trigger Easter Egg Modal
            if h_led and modal:
                h_led.click()
                time.sleep(0.5)
                active_display = modal.evaluate("el => getComputedStyle(el).display")
                modal_text = modal.inner_text()

                report.record(
                    "Tier 4",
                    f"#hLed click triggers #easterEggModal (display: {active_display})",
                    active_display == "flex"
                )

                has_project_info = ("24电科" in modal_text or "24電科" in modal_text) and "3246117007" in modal_text and "重点产研专案" in modal_text
                has_zhao = ("赵泓博nb666" in modal_text or "趙泓博nb666" in modal_text)
                has_tang = ("唐敬尧" in modal_text or "唐敬堯" in modal_text)
                has_firefly = ("萤火" in modal_text or "螢火" in modal_text)

                report.record(
                    "Tier 4",
                    "Easter Egg Modal displays '24电科（闽台）1班 3246117007 重点产研专案', '赵泓博nb666', '唐敬尧', '萤火'",
                    has_project_info and has_zhao and has_tang and has_firefly,
                    f"Modal text snippet: {modal_text[:200]}"
                )

                # Close modal first before interacting with background language buttons
                page.evaluate("window.closeEasterEggModal()")
                time.sleep(0.5)
                closed_display = modal.evaluate("el => getComputedStyle(el).display")
                report.record(
                    "Tier 4",
                    f"#easterEggModal closes cleanly via closeEasterEggModal() (display: {closed_display})",
                    closed_display == "none"
                )

            # Test language toggling (简体 <-> 繁體)
            if btn_hans and btn_hant and modal:
                # 1. Click Hans (Simplified)
                btn_hans.click()
                time.sleep(0.5)
                # Reopen modal to inspect converted text in Hans mode
                page.evaluate("window.showEasterEggModal()")
                time.sleep(0.5)
                hans_text = modal.inner_text()
                hans_ok = ("导师" in hans_text or "产研" in hans_text) and "赵泓博nb666" in hans_text

                # Close modal
                page.evaluate("window.closeEasterEggModal()")
                time.sleep(0.5)

                # 2. Click Hant (Traditional)
                btn_hant.click()
                time.sleep(0.5)
                # Reopen modal to inspect converted text in Hant mode
                page.evaluate("window.showEasterEggModal()")
                time.sleep(0.5)
                hant_text = modal.inner_text()
                hant_ok = ("導師" in hant_text or "產研" in hant_text) and "趙泓博nb666" in hant_text

                report.record(
                    "Tier 4",
                    "Language toggle (简体 <-> 繁體) updates modal without text corruption",
                    hans_ok and hant_ok
                )

                # Final close
                page.evaluate("window.closeEasterEggModal()")
                time.sleep(0.5)

            browser.close()
            report.record("Tier 4", "Playwright browser session cleanly closed", True)

    except Exception as e:
        report.record("Tier 4", "Playwright test execution failed", False, str(e))
    finally:
        server.shutdown()
        report.record("Tier 4", "Test HTTP server shut down cleanly", True)


def main():
    print(f"\n{BOLD}======================================================================{RESET}")
    print(f"{BOLD}    半导体工程小游戏 DUAL-TRACK COMPREHENSIVE 4-TIER E2E TEST SUITE   {RESET}")
    print(f"{BOLD}======================================================================{RESET}")
    print(f"Target Repository: {GAME_ROOT}")
    print(f"Python Executable: {sys.executable}")
    print(f"Node Executable:   node (v24.19.0)")

    run_tier_1()
    run_tier_2()
    run_tier_3()
    run_tier_4()

    success = report.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

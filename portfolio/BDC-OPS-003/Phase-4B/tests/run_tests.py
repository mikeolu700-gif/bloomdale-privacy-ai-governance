import json, os, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROTO = pathlib.Path(os.environ.get("PROTOTYPE", ROOT / "BDC-OPS-003_Consent_Prototype_v1.1.html")).resolve()
EVID = pathlib.Path(os.environ.get("EVIDENCE_DIR", ROOT / "evidence")); EVID.mkdir(parents=True, exist_ok=True)
URL = PROTO.as_uri()
results = []
def run(tid, title, region, steps, expect, gpc=False, note=""):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1100, "height": 900})
        reqs = []
        page = ctx.new_page()
        page.on("request", lambda r: reqs.append(r.url) if ".invalid" in r.url else None)
        q = f"?region={region}" + ("&gpc=1" if gpc else "")
        page.goto(URL + q); page.wait_for_timeout(300)
        for s in steps:
            s(page); page.wait_for_timeout(250)
        mark = len(reqs)
        page.click("#pageview"); page.wait_for_timeout(300)
        post = sorted({u.split('/')[2] for u in reqs[mark:]})
        css = page.evaluate("""()=>['accept','reject','manage'].map(i=>{const s=getComputedStyle(document.getElementById(i));return [s.backgroundColor,s.color,s.borderTopWidth,s.borderTopColor,s.fontWeight,s.fontSize,document.getElementById(i).offsetWidth>=150].join('|')})""")
        eff = json.loads(page.evaluate("document.body.dataset.effective"))
        banner = page.is_visible("#banner")
        honored = page.inner_text("#honored") if page.is_visible("#honored") else ""
        dnss = page.is_visible("#link-dnss")
        keys = page.evaluate("Object.keys(localStorage).sort()")
        hosts = sorted({u.split('/')[2] for u in reqs})
        obs = {"effective": eff, "banner_visible": banner, "honored_text": honored, "dnss_link": dnss, "tracker_hosts": hosts, "final_view_hosts": post, "button_styles": css, "storage_keys": keys}
        ok, why = expect(obs)
        shot = str(EVID / f"{tid}.png")
        page.screenshot(path=shot, full_page=True)
        b.close()
    results.append({"test_id": tid, "title": title, "region": region, "gpc": gpc, "observed": obs, "result": "Pass" if ok else "Fail", "detail": why, "screenshot": f"evidence/{tid}.png"})
    print(tid, "PASS" if ok else "FAIL", why)

ADS = "ads.adpartner-demo.invalid"; AN = "analytics.mdh-demo.invalid"
click = lambda sel: (lambda pg: pg.click(sel))
def reload(pg): pg.reload(); pg.wait_for_timeout(300)

run("F01","EEA first visit: no optional trackers before choice","eea",[],
    lambda o:(o["banner_visible"] and not any(o["effective"].values()) and o["tracker_hosts"]==[] and o["storage_keys"]==["mdh_session"], f"banner={o['banner_visible']} hosts={o['tracker_hosts']} storage={o['storage_keys']}"))
run("F02","EEA Reject all blocks optional trackers and persists","eea",[click("#reject"),reload],
    lambda o:(not o["banner_visible"] and not any(o["effective"].values()) and o["tracker_hosts"]==[], f"banner={o['banner_visible']} hosts={o['tracker_hosts']}"))
run("F03","EEA Accept all fires analytics and advertising","eea",[click("#accept")],
    lambda o:(all(o["effective"].values()) and AN in o["tracker_hosts"] and ADS in o["tracker_hosts"], f"hosts={o['tracker_hosts']}"))
def sel(pg):
    pg.click("#manage"); pg.check("#analytics"); pg.click("#save")
run("F04","EEA selective consent: analytics only","eea",[sel],
    lambda o:(o["effective"]=={"functional":False,"analytics":True,"advertising":False} and o["tracker_hosts"]==[AN], f"eff={o['effective']} hosts={o['tracker_hosts']}"))
def withdraw(pg):
    pg.click("#accept"); pg.wait_for_timeout(200); pg.click("#link-choices"); pg.uncheck("#advertising"); pg.uncheck("#analytics"); pg.click("#save")
run("F05","EEA withdrawal from footer link stops trackers on next page view","eea",[withdraw],
    lambda o:(o["effective"]["advertising"] is False and o["effective"]["analytics"] is False and o["final_view_hosts"]==[], f"eff={o['effective']} final_view={o['final_view_hosts']}"))
run("F06","UK first visit: exempt statistics on, advertising off","uk",[],
    lambda o:(o["banner_visible"] and o["effective"]["analytics"] and not o["effective"]["advertising"] and ADS not in o["tracker_hosts"], f"eff={o['effective']} hosts={o['tracker_hosts']}"))
run("F07","California with GPC: ads off and honored message shown","ca",[],
    lambda o:(not o["effective"]["advertising"] and ADS not in o["tracker_hosts"] and "Honored" in o["honored_text"], f"honored='{o['honored_text']}' hosts={o['tracker_hosts']}"), gpc=True)
run("F08","California without GPC: notice, Do Not Sell or Share link","ca",[],
    lambda o:(not o["banner_visible"] and o["dnss_link"] and o["effective"]["advertising"], f"dnss={o['dnss_link']} eff={o['effective']}"))
run("F09","California DNSS link opts out and shows confirmation","ca",[click("#link-dnss")],
    lambda o:(not o["effective"]["advertising"] and "Honored" in o["honored_text"] and ADS not in o["final_view_hosts"], f"honored='{o['honored_text']}' final_view={o['final_view_hosts']}"))
run("F10","Connecticut/Texas with GPC: targeted advertising off","ctx",[],
    lambda o:(not o["effective"]["advertising"] and ADS not in o["tracker_hosts"], f"hosts={o['tracker_hosts']}"), gpc=True)
def gpc_conflict(pg):
    pg.goto(URL+"?region=eea&gpc=1"); pg.wait_for_timeout(300); pg.click("#accept")
run("F11","GPC overrides Accept all for advertising (EEA)","eea",[gpc_conflict],
    lambda o:(not o["effective"]["advertising"] and ADS not in o["tracker_hosts"], f"eff={o['effective']}"), gpc=True)
def expire(pg):
    pg.click("#accept"); pg.wait_for_timeout(200)
    pg.evaluate("""()=>{const k='bdc003_consent_eea';const r=JSON.parse(localStorage.getItem(k));r.expiresAt='2020-01-01T00:00:00Z';localStorage.setItem(k,JSON.stringify(r));}""")
    pg.reload(); pg.wait_for_timeout(300)
run("F12","Expired consent record triggers re-prompt and blocks trackers","eea",[expire],
    lambda o:(o["banner_visible"] and not any(o["effective"].values()) and o["final_view_hosts"]==[], f"banner={o['banner_visible']} final_view={o['final_view_hosts']}"))
run("F13","Accept and Reject buttons have equal visual weight","eea",[],
    lambda o:(len(set(o["button_styles"]))==1, f"styles={o['button_styles'][0]} identical={len(set(o['button_styles']))==1}"))
def bad_date(pg):
    pg.click("#accept"); pg.wait_for_timeout(200)
    pg.evaluate("""()=>{const k='bdc003_consent_eea';const r=JSON.parse(localStorage.getItem(k));r.expiresAt='not-a-date';localStorage.setItem(k,JSON.stringify(r));}""")
    pg.reload(); pg.wait_for_timeout(300)
run("F14","Unreadable expiry date is treated as expired","eea",[bad_date],
    lambda o:(o["banner_visible"] and not any(o["effective"].values()) and o["final_view_hosts"]==[], f"banner={o['banner_visible']} final_view={o['final_view_hosts']}"))
def damaged(pg):
    pg.evaluate("""()=>localStorage.setItem('bdc003_consent_eea', JSON.stringify({policyVersion:'v1.1',expiresAt:'2099-01-01T00:00:00Z'}))""")
    pg.reload(); pg.wait_for_timeout(300)
run("F15","Damaged saved record is discarded without breaking the page","eea",[damaged],
    lambda o:(o["banner_visible"] and not any(o["effective"].values()) and o["final_view_hosts"]==[], f"banner={o['banner_visible']} final_view={o['final_view_hosts']}"))
json.dump(results, open(EVID / "fixture_results.json","w"), indent=2)
print(sum(r["result"]=="Pass" for r in results), "of", len(results), "passed")

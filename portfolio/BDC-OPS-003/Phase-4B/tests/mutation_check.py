"""Plants known defects in copies of the prototype and confirms the test suite catches each one.
Run from the package root:  python3 tests/mutation_check.py"""
import os, pathlib, subprocess, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "BDC-OPS-003_Consent_Prototype_v1.1.html").read_text()
MUTANTS = {
    "Reject all leaves advertising on": ("commit(allOff(), 'reject_all')", "commit({functional:false,analytics:false,advertising:true}, 'reject_all')"),
    "GPC check removed": ("if (c === 'advertising' && gpc) on = false;", ""),
    "Accept button highlighted": ("$('accept').onclick", "$('accept').style.background='#101D32';$('accept').style.color='#fff';$('accept').onclick"),
    "Expiry check accepts unreadable dates": ("!(Date.parse(record.expiresAt) > Date.now())", "Date.parse(record.expiresAt) < Date.now()"),
}
ok = True
with tempfile.TemporaryDirectory() as tmp:
    for name, (a, b) in MUTANTS.items():
        assert a in SRC, f"mutation anchor missing: {name}"
        page = pathlib.Path(tmp) / "mutant.html"; page.write_text(SRC.replace(a, b))
        env = dict(os.environ, PROTOTYPE=str(page), EVIDENCE_DIR=str(pathlib.Path(tmp) / "ev"))
        out = subprocess.run([sys.executable, str(ROOT / "tests" / "run_tests.py")], env=env, capture_output=True, text=True).stdout
        failed = [l.split()[0] for l in out.splitlines() if " FAIL " in l]
        print(f"{name}: caught by {', '.join(failed) if failed else 'NOTHING'}")
        ok &= bool(failed)
print("All planted defects caught." if ok else "Some defects were not caught.")

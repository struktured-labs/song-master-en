"""Repo-relative paths shared by the build tools.
The original ROM is never stored in this repository: pass it via SONGMASTER_ROM (tools/build.sh does this),
or place it at rom/Song Master (Japan).sfc (ignored by git)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROM = os.environ.get('SONGMASTER_ROM', os.path.join(ROOT, 'rom', 'Song Master (Japan).sfc'))
BUILD = os.path.join(ROOT, 'build')
GEN = os.path.join(BUILD, 'gen')
JP = os.path.join(BUILD, 'jp')   # JP script dump (regenerated from your ROM, never committed)
for d in (GEN,): os.makedirs(d, exist_ok=True)

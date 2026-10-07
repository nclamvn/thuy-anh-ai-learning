from pathlib import Path
import importlib.util,json,shutil,tempfile,unittest
from unittest.mock import patch
P=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('public_dream',P/'tools/build_dream.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class PublicDreamFaults(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='public-dream-fault-');self.root=Path(self.tmp.name);shutil.copytree(P/'app/dream',self.root/'app/dream');shutil.copytree(P/'docs/dream',self.root/'docs/dream');shutil.copytree(P/'source/dream-backend',self.root/'source/dream-backend');self.patches=[patch.object(m,'P',self.root),patch.object(m,'D',self.root/'app/dream'),patch.object(m,'S',self.root/'docs/dream/SOURCE.json'),patch.object(m,'BUILD',self.root/'docs/dream/BUILD.json')]
  for p in self.patches:p.start()
 def tearDown(self):
  for p in reversed(self.patches):p.stop()
  self.tmp.cleanup()
 def test_exact_static_projection_and_canonical_kit_reproduction(self):self.assertEqual(m.run()['liveAI'],'PERMANENTLY_OFF_STATIC')
 def test_changed_off_entry_function_fails_exact_source_recovery(self):
  f=m.D/'main.js';f.write_text(f.read_text().replace('async function requestLivePlan(){applyPublicOff(lab,LAB_COPY);refreshProposal();}','async function requestLivePlan(){fetch("/api/planner");}',1))
  with self.assertRaisesRegex(ValueError,'static OFF function drift'):m.run()
 def test_changed_observation_download_fails_generated_freshness(self):
  f=m.D/'kit/observation.csv';f.write_bytes(f.read_bytes()+b'forged outcome')
  with self.assertRaisesRegex(ValueError,'generated drift'):m.run()
 def test_backend_module_cannot_enter_static_runtime_inventory(self):
  (m.D/'provider.mjs').write_text('// counterfeit static provider')
  with self.assertRaisesRegex(ValueError,'private/backend'):m.inventory()

 def test_direct_network_call_with_whitespace_in_public_helper_fails(self):
  f=m.D/'public-mode.js';f.write_text(f.read_text()+'\nfetch \n("/api/planner");')
  with self.assertRaisesRegex(ValueError,'adapter not permanently OFF'):m.run()

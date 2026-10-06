"""Adversarial tests for the separate public-reference protocol, no raw corpus."""
import importlib.util,json,pathlib,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('references_protocol',ROOT/'tools/build_references.py');protocol=importlib.util.module_from_spec(spec);spec.loader.exec_module(protocol)
class ReferenceBuildTests(unittest.TestCase):
 def setUp(self):
  self.source=protocol.recover((ROOT/'app/references/report.html').read_bytes());self.temp=tempfile.TemporaryDirectory();self.out=pathlib.Path(self.temp.name)
  for name,value in protocol.outputs(self.source).items():(self.out/name).write_bytes(value)
 def tearDown(self):self.temp.cleanup()
 def test_frozen_reversal_and_determinism(self):
  self.assertEqual(protocol.sha(self.source),protocol.FROZEN);self.assertTrue(protocol.check(self.out));self.assertEqual(protocol.outputs(self.source),protocol.outputs(self.source));self.assertEqual(protocol.derivative(self.source),(self.out/'report.html').read_bytes())
 def test_report_body_modification_fails(self):
  p=self.out/'report.html';p.write_bytes(p.read_bytes().replace(b'63%',b'64%',1));self.assertRaises(ValueError,protocol.check,self.out)
 def test_unexpected_integration_addition_fails(self):
  p=self.out/'report.html';p.write_bytes(p.read_bytes().replace(b'</body>',b'<script>alert(1)</script></body>'));self.assertRaises(ValueError,protocol.check,self.out)
 def test_integration_block_modification_fails(self):
  p=self.out/'report.html';p.write_bytes(p.read_bytes().replace(b'Return to project references',b'Forged return link',1));self.assertRaises(ValueError,protocol.check,self.out)
 def test_catalog_semantic_and_receipt_drift_fail(self):
  for name in ['catalog.json','build.json']:
   original=(self.out/name).read_bytes();(self.out/name).write_bytes(original+b' ');self.assertRaises(ValueError,protocol.check,self.out);(self.out/name).write_bytes(original)
 def test_wrong_explicit_source_fails_before_outputs(self):
  self.assertRaises(ValueError,protocol.outputs,self.source+b' ')
 def test_claim_population_and_counts(self):
  data=protocol.source_data(self.source);self.assertEqual(len(data['cards']),14);self.assertEqual(sum(data['meta']['sourceClaims'].values()),92);self.assertEqual(data['meta']['r03Claims'],57)
  findings=next(c for c in data['cards']if c['id']=='R02-03')['findings'];self.assertTrue(all('n = 665' in f['en']and'n = 665'in f['vi']for f in findings if '63%'in f['en']or'66%'in f['en']))
 def test_hosted_derivative_has_safe_locale_source_and_return_contract(self):
  html=protocol.derivative(self.source).decode();self.assertIn("['vi','en'].includes(requested)",html);self.assertIn("cards.some(c=>'source-'+c.id===id)",html);self.assertIn("back.href='../#references?lang='+lang",html);self.assertIn('position:sticky',html);self.assertIn('section[id],#main,[id^="source-"]{scroll-margin-top:150px}',html)
if __name__=='__main__':unittest.main()

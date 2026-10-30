const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const PP = require('../apps-script/Core.gs');
const round = (id, hour, platesText, complete = true, area = 'Whole Lot', day = '29') => ({
  id, at: `2026-10-${day}T${hour}:00:00Z`, platesText, complete, area
});
const analyze = rows => PP.analyze(rows, key => key.replace('|', '_'));

test('absence then reappearance creates two visits with no departure time', () => {
  const data = analyze([round('a','09','ABC, AB'), round('b','12','ABC, AB'), round('c','15',''), round('d','09','ABC, AB',true,'Whole Lot','30')]);
  const v = data.vehicles[0];
  assert.equal(v.visits.length, 2);
  assert.equal(v.visits[0].last_seen_at, '2026-10-29T12:00:00Z');
  assert.equal(v.visits[0].first_absent_check_at, '2026-10-29T15:00:00Z');
  assert.equal(v.visits[0].absent_check_id, 'c');
  assert.ok(!('departure_time' in v.visits[0]));
});
test('incomplete or other-area check never establishes departure', () => {
  for (const missing of [round('b','12','',false), round('b','12','',true,'Other Lot')]) {
    assert.equal(analyze([round('a','09','ABC, AB'), missing]).vehicles[0].visits[0].first_absent_check_at,null);
  }
});
test('midnight and skipped dates do not close visits', () => {
  assert.equal(analyze([round('a','09','ABC, AB',true,'Whole Lot','27'), round('b','09','ABC, AB')]).vehicles[0].visits.length,1);
});
test('uncertain reading blocks absence but preserves certain sightings', () => {
  const d = analyze([round('a','09','ABC, AB'), round('b','12','?\nXYZ, AB')]);
  assert.equal(d.vehicles.find(v=>v.vehicle_id==='AB_ABC').visits[0].first_absent_check_at,null);
  assert.equal(d.checks[1].complete,false);
  assert.equal(d.issues.length,1);
  assert.equal(d.vehicles.length,2);
});
test('deduplicates plates, preserves province and O/0 distinctions', () => {
  assert.deepEqual(PP.parsePlates('ABC, AB\nabc, ab\nABC, BC\nAO0, AB\nA00, AB').keys, ['AB|A00','AB|ABC','AB|AO0','BC|ABC']);
});
test('backdated rounds are sorted before inference', () => {
  const d = analyze([round('b','12',''),round('a','09','ABC, AB')]);
  assert.equal(d.vehicles[0].visits[0].absent_check_id,'b');
});
test('conflicting duplicate area/time cannot establish absence', () => {
  const d = analyze([round('a','09','ABC, AB'),round('b','12',''),round('c','12','')]);
  assert.equal(d.vehicles[0].visits[0].first_absent_check_at,null);
  assert.equal(d.checks[1].complete,false);
});
test('malformed metadata and duplicate response IDs stop analysis', () => {
  assert.throws(()=>analyze([round('a','09',''),round('a','12','')]));
  assert.throws(()=>analyze([{id:'a',at:'bad',area:'Lot',platesText:''}]));
});
const candidate = () => ({vehicle_id:'AB_ABC',priority:'medium',summary:'Possible routine',evidence_check_ids:['a'],alternative_explanation:'Customer visits',next_check:'Verify current use'});
test('accepts supported evidence including first-absent check', () => {
  const data = analyze([round('a','09','ABC, AB'),round('b','12','')]);
  const c = candidate(); c.evidence_check_ids.push('b');
  assert.equal(PP.validateResult({candidates:[c]},data).candidates.length,1);
});
test('rejects hallucinated vehicle/evidence and unsupported higher priority', () => {
  const data = analyze([round('a','09','ABC, AB'),round('b','12','XYZ, AB')]);
  for(const change of [{vehicle_id:'fake'},{evidence_check_ids:['fake']},{evidence_check_ids:[]},{priority:'higher'},{summary:''}]) {
    assert.throws(()=>PP.validateResult({candidates:[Object.assign(candidate(),change)]},data));
  }
  // b is a legitimate first-absence reference for ABC, but not an invented reference.
  data.vehicles.find(v=>v.vehicle_id==='AB_ABC').verified_prohibited_association = true;
  const c=candidate(); c.priority='higher';
  assert.doesNotThrow(()=>PP.validateResult({candidates:[c]},data));
});
test('empty candidate list is valid; duplicate candidates are rejected', () => {
  const data=analyze([round('a','09','ABC, AB')]);
  assert.doesNotThrow(()=>PP.validateResult({candidates:[]},data));
  assert.throws(()=>PP.validateResult({candidates:[candidate(),candidate()]},data));
});
test('spreadsheet cells cannot execute model-provided formulas', () => {
  for(const s of ['=IMPORTXML("x")',' +cmd','@SUM(1)','-1']) assert.ok(PP.safeCell(s).startsWith("'"));
  assert.equal(PP.safeCell('ordinary text'),'ordinary text');
});

function apiContext(fetch) {
  const ctx = {PP, UrlFetchApp:{fetch}};
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(require.resolve('../apps-script/Code.gs'),'utf8'),ctx);
  return ctx;
}
const props={getProperty:k=>({OPENAI_API_KEY:'test-secret',OPENAI_MODEL:'test-model'}[k])};
test('Responses request uses strict schema and parses output_text', () => {
  let request;
  const ctx=apiContext((url, options)=>{
    request={url,options};
    return {getResponseCode:()=>200,getContentText:()=>JSON.stringify({status:'completed',output:[{content:[{type:'output_text',text:'{"candidates":[]}'}]}]})};
  });
  const result=ctx.requestAI_('{"vehicles":[]}',props);
  assert.equal(result.candidates.length,0);
  const b=JSON.parse(request.options.payload);
  assert.equal(b.store,false);
  assert.equal(b.text.format.strict,true);
  assert.equal(b.model,'test-model');
  assert.equal(request.options.headers.Authorization,'Bearer test-secret');
});
test('HTTP failures never expose server response or key', () => {
  const ctx=apiContext(()=>({getResponseCode:()=>401,getContentText:()=>{throw Error('must not read error body');}}));
  assert.throws(()=>ctx.requestAI_('{}',props),/HTTP_401/);
});
test('refusal, incomplete, invalid JSON and network failure are rejected', () => {
  for(const body of [{status:'incomplete'},{status:'completed',output:[{content:[{type:'refusal'}]}]},{status:'completed',output:[]}]) {
    const ctx=apiContext(()=>({getResponseCode:()=>200,getContentText:()=>JSON.stringify(body)}));
    assert.throws(()=>ctx.requestAI_('{}',props),/AI_/);
  }
  assert.throws(()=>apiContext(()=>{throw Error('secret');}).requestAI_('{}',props),/AI_NETWORK_ERROR/);
});

test('worker pseudonymizes plates, writes private results, and skips unchanged input', () => {
  const state={ENABLE_AI:'true',OPENAI_API_KEY:'secret',OPENAI_MODEL:'test',LOOKBACK_DAYS:'60',MAX_CALLS_PER_DAY:'12',VEHICLE_SALT:'private-salt'};
  const writes={}, logs=[]; let calls=0, payload;
  const ctx=apiContext(()=>{throw Error('unexpected network');});
  ctx.PropertiesService={getScriptProperties:()=>({getProperty:k=>state[k]??null,setProperty:(k,v)=>{state[k]=v;},setProperties:o=>Object.assign(state,o)})};
  ctx.LockService={getScriptLock:()=>({tryLock:()=>true,releaseLock:()=>{}})};
  ctx.Utilities={DigestAlgorithm:{SHA_256:'sha256'},Charset:{UTF_8:'utf8'},computeDigest:(_,s)=>Array.from(crypto.createHash('sha256').update(s).digest()),formatDate:()=> '2026-10-29'};
  ctx.readRounds_=()=>[round('a','09','SECRET123, AB')];
  ctx.readAssociations_=()=>({});
  ctx.write_=(name,headers,rows)=>{writes[name]={headers,rows};};
  ctx.log_=(s,d)=>logs.push([s,d]);
  ctx.requestAI_=(body)=>{
    calls++; payload=JSON.parse(body);
    return {candidates:[Object.assign(candidate(),{vehicle_id:payload.vehicles[0].vehicle_id})]};
  };
  ctx.runAnalysis_();
  assert.equal(calls,1);
  assert.ok(!JSON.stringify(payload).includes('SECRET123'));
  assert.ok(!JSON.stringify(payload).includes('private-salt'));
  assert.equal(writes.Review.rows[0][2],'SECRET123');
  assert.equal(logs[0][0],'SUCCESS');
  ctx.runAnalysis_();
  assert.equal(calls,1);
  assert.equal(state.CALL_COUNT,'1');
  state.ENABLE_AI='false';
  ctx.runAnalysis_();
  assert.equal(calls,1);
  assert.ok(writes.CurrentRoundReview);
  assert.match(writes.Review.rows[0][0],/AI disabled/);
  state.ENABLE_AI='true'; state.LAST_SUCCESS_HASH='';
  ctx.requestAI_=()=>{throw Error('HTTP_429');};
  ctx.book_=()=>({getSheetByName:()=>({getRange:()=>({setNote:()=>{}})})});
  ctx.runAnalysis_();
  assert.ok(writes.CurrentRoundReview);
  assert.equal(logs[logs.length-1][0],'ERROR');
});

test('basic review excludes presumed absent vehicles and flags recurring current sightings',()=>{
  const ctx=apiContext(()=>{throw Error('unexpected network');});
  const d=analyze([round('a','09','ABC, AB',true,'Whole Lot','27'),round('b','09','ABC, AB',true,'Whole Lot','28'),round('c','09','ABC, AB\nXYZ, AB'),round('d','12','ABC, AB')]);
  const rows=ctx.basicRows_(d,{'AB_ABC':'AB|ABC','AB_XYZ':'AB|XYZ'});
  assert.equal(rows.length,1);
  assert.equal(rows[0][1],'ABC');
  assert.equal(rows[0][5],3);
  assert.match(rows[0][7],/3 or more/);
});

const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
function core(){const c={Date};vm.createContext(c);vm.runInContext(fs.readFileSync('apps-script/Retention.gs','utf8'),c);return c;}
test('three calendar months clamps month-end and leap-year dates',()=>{
 const c=core(); for(const [a,b] of [['2026-10-30','2026-07-30'],['2026-05-31','2026-02-28'],['2024-05-31','2024-02-29'],['2026-01-31','2025-10-31']])assert.equal(c.retentionDate_(a),b);
});
test('cutoff boundary retained; strictly older records deleted',()=>{
 const c=core(),cut=Date.parse('2026-07-30T06:00:00Z');
 assert.equal(c.retentionOld_('2026-07-30T05:59:59Z',cut),true);
 assert.equal(c.retentionOld_('2026-07-30T06:00:00Z',cut),false);
 assert.throws(()=>c.retentionOld_('invalid',cut),/INVALID_DATE/);
});
test('ambiguous linked sheet aborts before source deletion',()=>{
 const c=core();let deleted=0;
 c.LockService={getScriptLock:()=>({tryLock:()=>true,releaseLock(){}})};
 c.props_=()=>({getProperty:()=> 'form'});c.book_=()=>({getSheets:()=>[],getSheetByName:()=>null});c.readAssociations_=()=>({});
 c.FormApp={openById:()=>({getResponses:()=>[],deleteResponse:()=>deleted++})};
 c.Utilities={formatDate:()=> '2026-10-30',parseDate:()=>new Date('2026-07-30T06:00:00Z')};
 assert.throws(()=>c.cleanupRetention(),/NOT_UNIQUE/);assert.equal(deleted,0);
});
test('manual mode never auto-deletes; automatic runs once per local day',()=>{
 const c=core();
 assert.equal(c.retentionAutomaticDue_('Manual','yesterday','today'),false);
 assert.equal(c.retentionAutomaticDue_('Automatic','today','today'),false);
 assert.equal(c.retentionAutomaticDue_('Automatic','yesterday','today'),true);
 assert.throws(()=>c.retentionAutomaticDue_('typo','','today'),/INVALID_MODE/);
});

test('retention preserves recurring and confirmed vehicles; explicit customer correction releases protection',()=>{
 const c=core();c.PP=require('../apps-script/Core.gs');
 c.props_=()=>({getProperty:()=> 'salt'});c.digest_=s=>s; c.readAssociations_=()=>({});
 c.Utilities={formatDate:d=>new Date(d).toISOString().slice(0,10)};
 const response=(day)=>({getTimestamp:()=>new Date(day),getItemResponses:()=>[{getItem:()=>({getTitle:()=> 'Plates present'}),getResponse:()=> 'ABC, AB'}]});
 const rs=['2026-01-01','2026-01-02','2026-01-03'].map(response);
 const ss={getSheetByName:()=>null};
 assert.equal(c.retentionProtectedKeys_(rs,ss)['AB|ABC'],true);
 const tagSheet=status=>({getSheetByName:n=>n==='ManualTags'?{getDataRange:()=>({getValues:()=>[[],['ABC','AB',status,'Verified',new Date('2026-01-01')]]})}:null});
 assert.equal(c.retentionProtectedKeys_([rs[0]],tagSheet('Confirmed offender'))['AB|ABC'],true);
 assert.equal(c.retentionProtectedKeys_(rs,tagSheet('Assumed customer'))['AB|ABC'],undefined);
 assert.equal(c.retentionProtectedKeys_([rs[0]],ss)['AB|ABC'],undefined);
});

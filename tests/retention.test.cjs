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
 c.props_=()=>({getProperty:()=> 'form'});c.book_=()=>({getSheets:()=>[]});
 c.FormApp={openById:()=>({getResponses:()=>[],deleteResponse:()=>deleted++})};
 c.Utilities={formatDate:()=> '2026-10-30',parseDate:()=>new Date('2026-07-30T06:00:00Z')};
 assert.throws(()=>c.cleanupRetention(),/NOT_UNIQUE/);assert.equal(deleted,0);
});

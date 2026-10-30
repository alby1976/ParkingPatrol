/** Rolling three-calendar-month retention. All dates use Edmonton calendar days. */
function retentionDate_(localDay) {
  var p = localDay.split('-').map(Number), month = p[1] - 1 - 3;
  var first = new Date(Date.UTC(p[0], month, 1));
  var last = new Date(Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 0)).getUTCDate();
  return first.getUTCFullYear() + '-' + ('0' + (first.getUTCMonth() + 1)).slice(-2) + '-' + ('0' + Math.min(p[2], last)).slice(-2);
}
function retentionOld_(value, cutoff) {
  var date = value instanceof Date ? value : new Date(String(value));
  if (!Number.isFinite(date.getTime())) throw new Error('RETENTION_INVALID_DATE');
  return date.getTime() < cutoff;
}
function cleanupRetention() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('RETENTION_BUSY');
  try {
    var p = props_(), ss = book_(), form = FormApp.openById(p.getProperty('FORM_ID'));
    var day = Utilities.formatDate(new Date(), 'America/Edmonton', 'yyyy-MM-dd');
    var cutoff = Utilities.parseDate(retentionDate_(day) + ' 00:00', 'America/Edmonton', 'yyyy-MM-dd HH:mm').getTime();
    var responses = form.getResponses(), deletions = [], active = {};
    responses.forEach(function (r) {
      var answers = {};
      r.getItemResponses().forEach(function (i) { answers[i.getItem().getTitle()] = String(i.getResponse()); });
      var at = (answers['Observation time (optional)'] || '').trim() || r.getTimestamp();
      if (retentionOld_(at, cutoff)) deletions.push(r.getId());
      else PP.parsePlates(answers['Plates present']).keys.forEach(function (k) { active[k] = true; });
    });
    // Identify the actual linked response sheet, never a guessed tab name.
    var linked = ss.getSheets().filter(function (s) {
      var url = s.getFormUrl(); return url && url.indexOf(p.getProperty('FORM_ID')) >= 0;
    });
    if (linked.length !== 1) throw new Error('RETENTION_RESPONSE_SHEET_NOT_UNIQUE');
    var raw = linked[0], rows = raw.getDataRange().getValues(), header = rows[0];
    var obs = header.indexOf('Observation time (optional)'), expiredRows = [];
    if (obs < 0) throw new Error('RETENTION_RESPONSE_HEADER_MISSING');
    rows.slice(1).forEach(function (r, i) {
      if (r.every(function (v) { return v === ''; })) return;
      var at = String(r[obs] || '').trim() || r[0];
      if (retentionOld_(at, cutoff)) expiredRows.push(i + 2);
    });
    var assoc = ss.getSheetByName('VerifiedAssociations'), assocRows = [];
    if (assoc) assoc.getDataRange().getValues().slice(1).forEach(function (r, i) {
      if (!r[0] && !r[1]) return;
      var keys = PP.parsePlates(r[0] + ', ' + r[1]).keys;
      if (keys.length !== 1) throw new Error('RETENTION_INVALID_ASSOCIATION');
      if (!active[keys[0]]) assocRows.push(i + 2);
    });
    var tags = ss.getSheetByName('ManualTags'), tagRows = [];
    if (tags) tags.getDataRange().getValues().slice(1).forEach(function (r, i) {
      if (r.every(function (v) { return v === ''; })) return;
      if (retentionOld_(r[4], cutoff)) tagRows.push(i + 2);
    });
    // Validation above completes before any irreversible source deletion.
    // Clear derived history first so a later failure cannot leave expired reports visible.
    ['Review','CurrentRoundReview','RoundStatus','Sessions','DataIssues','Runs'].forEach(function (name) {
      var s = ss.getSheetByName(name); if (s) { s.clearContents(); s.getRange('A1').setValue('Retention cleanup ran; awaiting next successful analysis.'); }
    });
    p.deleteProperty('LAST_SUCCESS_HASH');
    p.deleteProperty('LAST_AI_FLAGS');
    expiredRows.reverse().forEach(function (n) { raw.deleteRow(n); });
    tagRows.reverse().forEach(function (n) { tags.deleteRow(n); });
    assocRows.reverse().forEach(function (n) { assoc.deleteRow(n); });
    deletions.forEach(function (id) { form.deleteResponse(id); });
    p.setProperty('LAST_RETENTION_DAY', day);
    log_('RETENTION', 'Cutoff ' + retentionDate_(day) + '; removed ' + deletions.length + ' Form responses and ' + expiredRows.length + ' response-sheet rows.');
  } finally { lock.releaseLock(); }
}

/** Sheet-controlled deletion; automatic is the initial default only. */
function setupRetentionSettings_() {
  var ss = book_(), s = ss.getSheetByName('Settings');
  if (!s) {
    s = ss.insertSheet('Settings');
    s.getRange('A1:B4').setValues([
      ['Setting', 'Value'],
      ['Retention deletion mode', 'Automatic'],
      ['Retention period', '3 calendar months'],
      ['Manual cleanup', 'ParkingPatrol menu > Delete expired records now']
    ]);
    s.getRange('B2').setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['Automatic', 'Manual'], true).setAllowInvalid(false).build());
    s.setFrozenRows(1);
  }
}
function retentionMode_() {
  var s = book_().getSheetByName('Settings');
  if (!s) throw new Error('RETENTION_SETTINGS_MISSING_RUN_SETUP');
  return String(s.getRange('B2').getValue()).trim();
}
function retentionAutomaticDue_(mode, lastDay, today) {
  if (mode !== 'Automatic' && mode !== 'Manual') throw new Error('RETENTION_INVALID_MODE');
  return mode === 'Automatic' && lastDay !== today;
}
/** A Sheets drawing/button can also be assigned this public function name. */
function manualRetentionCleanup() {
  var ui = SpreadsheetApp.getUi();
  var answer = ui.alert('Delete expired parking records?',
    'Permanently delete Form responses older than three calendar months and remove their linked rows. Generated reports will be rebuilt. This cannot be undone in Google Forms.',
    ui.ButtonSet.YES_NO);
  if (answer !== ui.Button.YES) return;
  cleanupRetention();
  runAnalysis_();
  book_().toast('Expired records deleted. Check Runs and CurrentRoundReview.');
}

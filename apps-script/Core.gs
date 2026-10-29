/** Pure parking/session logic. No Google services or network calls. */
var PP = (function () {
  'use strict';
  function parsePlates(text) {
    var keys = [], issues = [];
    String(text || '').split(/\r?\n/).forEach(function (line, i) {
      if (!line.trim()) return;
      var parts = line.trim().toUpperCase().split(',').map(function (s) { return s.trim(); });
      if (parts.length !== 2 || !/^[A-Z0-9-]{1,12}$/.test(parts[0]) || !/^[A-Z]{2,3}$/.test(parts[1])) {
        issues.push('Line ' + (i + 1) + ': use PLATE, PROVINCE; uncertain readings invalidate absence inference.');
      } else {
        var key = parts[1] + '|' + parts[0];
        if (keys.indexOf(key) < 0) keys.push(key);
      }
    });
    return {keys: keys.sort(), issues: issues};
  }

  function analyze(input, idFor) {
    var issues = [], seenIDs = {}, timeAreas = {}, vehicles = {}, open = {};
    var rounds = input.map(function (r) {
      var parsed = parsePlates(r.platesText);
      var n = Object.assign({}, r, {keys: parsed.keys, validComplete: r.complete === true && !parsed.issues.length});
      if (!r.id || seenIDs[r.id]) throw new Error('Duplicate/missing response ID.');
      seenIDs[r.id] = true;
      if (!r.area || !Number.isFinite(Date.parse(r.at))) throw new Error('Invalid check metadata: ' + r.id);
      parsed.issues.forEach(function (s) { issues.push(r.id + ': ' + s); });
      var k = r.area + '|' + r.at;
      (timeAreas[k] = timeAreas[k] || []).push(n);
      return n;
    }).sort(function (a, b) { return Date.parse(a.at) - Date.parse(b.at) || a.id.localeCompare(b.id); });
    Object.keys(timeAreas).forEach(function (k) {
      if (timeAreas[k].length > 1) timeAreas[k].forEach(function (r) {
        r.validComplete = false;
        issues.push(r.id + ': duplicate area/time; absence inference disabled.');
      });
    });
    rounds.forEach(function (r) {
      var present = {};
      r.keys.forEach(function (key) {
        var id = idFor(key), v = vehicles[id];
        if (!v) v = vehicles[id] = {vehicle_id: id, sightings: [], visits: []};
        present[id] = true;
        v.sightings.push({check_id: r.id, at: r.at, local_time: r.localTime || r.at, area: r.area});
        var slot = id + '|' + r.area;
        if (!open[slot]) {
          open[slot] = {area: r.area, first_seen_at: r.at, last_seen_at: r.at, first_absent_check_at: null,
            absent_check_id: null, sighting_check_ids: []};
          v.visits.push(open[slot]);
        }
        open[slot].last_seen_at = r.at;
        open[slot].sighting_check_ids.push(r.id);
      });
      if (r.validComplete) Object.keys(open).forEach(function (slot) {
        var visit = open[slot], id = slot.split('|')[0];
        if (visit.area === r.area && !present[id]) {
          visit.first_absent_check_at = r.at;
          visit.absent_check_id = r.id;
          delete open[slot];
        }
      });
    });
    return {vehicles: Object.keys(vehicles).sort().map(function (id) { return vehicles[id]; }),
      checks: rounds.map(function (r) { return {check_id: r.id, at: r.at, local_time: r.localTime || r.at,
        area: r.area, complete: r.validComplete, vehicle_count: r.keys.length}; }), issues: issues};
  }

  function schema() {
    return {type: 'object', additionalProperties: false, required: ['candidates'], properties: {
      candidates: {type: 'array', items: {type: 'object', additionalProperties: false,
        required: ['vehicle_id', 'priority', 'summary', 'evidence_check_ids', 'alternative_explanation', 'next_check'],
        properties: {vehicle_id: {type: 'string'}, priority: {type: 'string', enum: ['higher', 'medium', 'low']},
          summary: {type: 'string'}, evidence_check_ids: {type: 'array', items: {type: 'string'}},
          alternative_explanation: {type: 'string'}, next_check: {type: 'string'}}}}
    }};
  }

  function validateResult(result, data) {
    if (!result || !Array.isArray(result.candidates)) throw new Error('Invalid AI output.');
    var seen = {};
    result.candidates.forEach(function (c) {
      var v = data.vehicles.find(function (x) { return x.vehicle_id === c.vehicle_id; });
      if (!v || seen[c.vehicle_id]) throw new Error('Unknown/duplicate AI vehicle.');
      seen[c.vehicle_id] = true;
      if (['higher', 'medium', 'low'].indexOf(c.priority) < 0) throw new Error('Invalid AI priority.');
      if (c.priority === 'higher' && !v.verified_prohibited_association) throw new Error('Unsupported higher priority.');
      var evidence = v.sightings.map(function (x) { return x.check_id; }).concat(v.visits.map(function (x) { return x.absent_check_id; }));
      if (!Array.isArray(c.evidence_check_ids) || !c.evidence_check_ids.length ||
          c.evidence_check_ids.some(function (id) { return !id || evidence.indexOf(id) < 0; })) throw new Error('Unsupported AI evidence.');
      ['summary', 'alternative_explanation', 'next_check'].forEach(function (f) {
        if (typeof c[f] !== 'string' || !c[f].trim() || c[f].length > 3000) throw new Error('Invalid AI explanation.');
      });
    });
    return result;
  }

  function safeCell(value) {
    var s = String(value == null ? '' : value);
    return /^[\s]*[=+@-]/.test(s) ? "'" + s : s;
  }
  return {parsePlates: parsePlates, analyze: analyze, schema: schema, validateResult: validateResult, safeCell: safeCell};
})();
if (typeof module !== 'undefined') module.exports = PP;

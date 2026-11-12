/** Tests for the optional per-vehicle status Form installer; no Google access. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { test } = require('node:test');
const path = require('node:path');

class Item {
  constructor(title, type) {
    this.title = title; this.type = type; this.required = false; this.options = [];
  }
  getTitle() { return this.title; }
  setTitle(x) { this.title = x; return this; }
  setHelpText(x) { this.help = x; return this; }
  setRequired(x) { this.required = x; return this; }
  setChoiceValues(x) { this.options = x; return this; }
  asTextItem() { assert.equal(this.type, 'TEXT'); return this; }
  asListItem() { assert.equal(this.type, 'LIST'); return this; }
}
class FakeForm {
  constructor() { this.items = []; this.published = true; }
  setPublished(x) { this.published = x; }
  supportsAdvancedResponderPermissions() { return true; }
  setDestination(x, id) { this.destination = id; }
  setDescription(x) { this.description = x; }
  setAllowResponseEdits(x) { this.edits = x; }
  setPublishingSummary(x) { this.summary = x; }
  setConfirmationMessage(x) { this.confirmation = x; }
  getId() { return 'FORM-FICTION'; }
  getPublishedUrl() { return 'https://example.invalid/form'; }
  getEditUrl() { return 'https://example.invalid/edit'; }
  getItems() { return this.items; }
  addTextItem() { const x = new Item('', 'TEXT'); this.items.push(x); return x; }
  addListItem() { const x = new Item('', 'LIST'); this.items.push(x); return x; }
}
function fixture() {
  const form = new FakeForm();
  const values = {};
  const properties = {
    getProperty(k) { return values[k] ?? null; },
    setProperty(k,v) { values[k] = v; }
  };
  const context = {
    FormApp: {
      create: () => form,
      openById: () => form,
      DestinationType: { SPREADSHEET: 'SHEET' }
    }
  };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'apps-script', 'PlateStatus.gs'), 'utf8'), context);
  return {form, properties, context};
}

test('per-plate form requires an explicit status from three supported choices', () => {
  const {form, properties, context} = fixture();
  assert.equal(context.setupPlateStatusForm_({getId: () => 'SHEET-1'}, properties), form);
  assert.equal(form.destination, 'SHEET-1');
  assert.equal(form.published, false);
  assert.deepEqual(form.items.map(x => x.title), ['Plate', 'Province', 'Staff-reported status']);
  assert.equal(form.items.every(x => x.required), true);
  assert.deepEqual(Array.from(form.items[2].options), ['Unknown', 'Suspicious', 'Violator']);
  assert.match(form.items[2].help, /earlier ticket is confirmed/);
  assert.match(form.description, /confirmed historical violator/);
  assert.match(form.confirmation, /previously ticketed vehicle/);
  assert.equal(properties.getProperty('PLATE_STATUS_FORM_ID'), 'FORM-FICTION');
});

test('repeated setup repairs the same Form without duplicating questions', () => {
  const {form, properties, context} = fixture();
  context.setupPlateStatusForm_({getId: () => 'SHEET-1'}, properties);
  context.setupPlateStatusForm_({getId: () => 'SHEET-1'}, properties);
  assert.equal(form.items.length, 3);
});

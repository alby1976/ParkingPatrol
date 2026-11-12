/**
 * Create a private one-vehicle staff-status form without altering parking-round collection.
 * The Violator option means a confirmed prior ticket; current conduct is not inferred.
 * This module never blacklists, tickets, tows, or trains a model.
 */
function setupPlateStatusForm_(spreadsheet, properties) {
  var formId = properties.getProperty('PLATE_STATUS_FORM_ID');
  var form = formId ? FormApp.openById(formId) : FormApp.create('ParkingPatrol — per-vehicle staff status');
  if (!formId) {
    properties.setProperty('PLATE_STATUS_FORM_ID', form.getId());
    // Keep the new form unpublished until administrators restrict responder access.
    if (form.supportsAdvancedResponderPermissions()) form.setPublished(false);
    else form.setAcceptingResponses(false);
    form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheet.getId());
  }
  form.setDescription('Internal staff reporting: one plate per response. Unknown = unclassified; Suspicious = requires review; Violator = confirmed historical violator with an issued prior ticket. Staff must check the prior ticket record before choosing Violator. Prior ticket status alone does not establish a new violation.');
  form.setAllowResponseEdits(false);
  form.setPublishingSummary(false);
  var items = form.getItems();
  function find(title) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].getTitle() === title) return items[i];
    }
    return null;
  }
  function requiredText(title, help) {
    var old = find(title);
    var item = old ? old.asTextItem() : form.addTextItem().setTitle(title);
    item.setHelpText(help).setRequired(true);
    return item;
  }
  requiredText('Plate', 'Record one plate only. This is sensitive information; restrict form access.');
  requiredText('Province', 'Issuing province or jurisdiction, e.g. AB.');
  var oldStatus = find('Staff-reported status');
  var status = oldStatus ? oldStatus.asListItem() : form.addListItem().setTitle('Staff-reported status');
  status.setChoiceValues(['Unknown', 'Suspicious', 'Violator'])
    .setHelpText('Required for every plate. Unknown when evidence is insufficient. Select Violator ONLY when an earlier ticket is confirmed in the private ticket record. This documents historical confirmation, not a new incident or permission to tow.')
    .setRequired(true);
  form.setConfirmationMessage('Status saved privately. Violator means a previously ticketed vehicle; confirm its historical ticket record. A new enforcement action requires fresh authorization and evidence.');
  return form;
}

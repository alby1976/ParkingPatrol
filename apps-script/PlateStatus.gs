/**
 * Create a private one-vehicle staff-status form without altering parking-round collection.
 * Staff categories are reports, NOT independently verified violations.
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
  form.setDescription('Internal staff reporting ONLY. Submit one plate per response. Choose Unknown, Suspicious, or Violator. A staff-reported Violator selection is NOT a confirmed violation; independently review evidence before any blacklist or enforcement action.');
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
    .setHelpText('Required for EVERY plate. Unknown when evidence is insufficient. Violator is staff-reported and does not automatically blacklist or authorize enforcement.')
    .setRequired(true);
  form.setConfirmationMessage('Staff status report saved privately. A Violator selection requires separate independent verification before any blacklist or action.');
  return form;
}

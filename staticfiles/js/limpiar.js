$(document).ready(function() {
    $(':input').not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
});

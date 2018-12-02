$(function() {
  $('#submit').bind('click', function() {
    $.getJSON(
      $SCRIPT_ROOT + '/calc_nums',
      {
        convert_from: $('input[name="convert_from"]').val(),
        convert_to: $('input[name="convert_to"]').val(),
        amount: $('input[name="amount"]').val()
      },
      function(data) {
        $('#converted_result').text(data.result);
        if (data.calculated) {
          $('#calculated_list').append('<li>' + data.calculated + '</li>');
        }
      }
    );
    return false;
  });
});

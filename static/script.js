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
        $('#calculated_list').empty();
        if (data.calculated) {
          for (let calculation_idx in data.calculated) {
            $('#calculated_list').append(
              '<li>' + data.calculated[calculation_idx] + '</li>'
            );
          }
        }
      }
    );
    return false;
  });
});

$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
    var string          = $(".add_field_button").val();
    // var x = 1;

    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
          // x++;
          $(wrapper).append(`<div class="row">
                              <div class="col-25">
                              </div>
                              <div class="col-75">
                                `+string+`<a style="color:black;" class="remove_field">X</a>
                              </div>
                            </div>`);

    });

    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').parent('div').remove();
        // x++;
    })
});

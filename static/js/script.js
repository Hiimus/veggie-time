$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    
    // Credit to https://www.sanwebcorner.com/2017/02/dynamically-generate-form-fields-using.html for adding new field to ingredients

    var max_fields      = 10;
    var wrapper         = $(".container1");
    var add_button      = $(".add_form_field");
 
    var x = 1;
    $(add_button).click(function(e){
        e.preventDefault();
        if(x < max_fields){
            x++;
            $(wrapper).append("<div class='input-field col s12 m8 l8'><input id='ingredients' name='ingredients' type='text' maxlength='100' class='validate_me'><label for='ingredients'>Ingredients</label><button type='button' class='delete btn-floating btn-small waves-effect waves-light red'><i class='fas fa-minus prefix'></i></button></div>"); //add input box
        }
  else
  {
  alert('You Reached the limits')
  }
    });
 
    $(wrapper).on("click",".delete", function(e){
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
  });

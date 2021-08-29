$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.modal').modal(); // Modal that appears when clicking delete button.
    $('.tooltipped').tooltip(); // Tooltip that explains that product link is fake

    // Credit to https://www.sanwebcorner.com/2017/02/dynamically-generate-form-fields-using.html for adding new field to ingredients

    let max_fields      = 10;
    let wrapper         = $(".container1");
    let add_button      = $(".add_form_field");
    let x = 1;
    let appendIngredient = `<div class='input-field col s12 m8 l8'>
        <input id='ingredients' name='ingredients' type='text' maxlength='100' class='validate_me'>
        <label for='ingredients'>Ingredients</label>
        <button type='button' class='delete btn-floating btn-small waves-effect waves-light red'><i class='fas fa-minus'></i></button>
    </div>`

    $(add_button).click(function(e) {
        e.preventDefault();
        if (x < max_fields) {
            x++;
            $(wrapper).append(appendIngredient); //add input box
        }
  else
  {
  alert('You Reached the limits')
  }
    });
 
    $(wrapper).on("click",".delete", function(e){
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })
  


  // Credit to: https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+DCP101+2017_T3/courseware/9e2f12f5584e48acb3c29e9b0d7cc4fe/6449dcd23ca14016aa83dc7313d91a02/?child=first
  validateMaterializeSelect();

  function validateMaterializeSelect() {
      let classValid = {
          "border-bottom": "1px solid #4caf50",
          "box-shadow": "0 1px 0 0 #4caf50"
      };
      let classInvalid = {
          "border-bottom": "1px solid #f44336",
          "box-shadow": "0 1px 0 0 #f44336"
      };
      if ($("select.validate").prop("required")) {
          $("select.validate").css({
              "display": "block",
              "height": "0",
              "padding": "0",
              "width": "0",
              "position": "absolute"
          });
      }
      $(".select-wrapper input.select-dropdown").on("focusin", function () {
          $(this).parent(".select-wrapper").on("change", function () {
              if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                  $(this).children("input").css(classValid);
              }
          });
      }).on("click", function () {
          if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
              $(this).parent(".select-wrapper").children("input").css(classValid);
          } else {
              $(".select-wrapper input.select-dropdown").on("focusout", function () {
                  if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                      if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                          $(this).parent(".select-wrapper").children("input").css(classInvalid);
                      }
                  }
              });
          }
      });
  }
  });




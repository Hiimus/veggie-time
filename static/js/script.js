$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.modal').modal(); // Modal that appears when clicking delete button.
    $('.tooltipped').tooltip(); // Tooltip that explains that product link is fake

    
    


    // Credit to https://www.sanwebcorner.com/2017/02/dynamically-generate-form-fields-using.html for adding new field to ingredients
    let max_fields      = 20;
    let wrapper1         = $(".container1");
    let wrapper2         = $(".container2");
    let add_button_ingredient      = $(".add_form_field_ingredient");
    let add_button_instruction      = $(".add_form_field_instruction");
    let x = 1;
    let appendIngredient = `<div class='input-field col s12 m8 l8'>
        <input id='ingredients' name='ingredients' type='text' maxlength='100' class='validate_me'>
        <label for='ingredients'>Ingredients</label>
        <button type='button' class='delete btn-floating btn-small waves-effect waves-light red'><i class='fas fa-minus'></i></button>
    </div>`
    let appendInstruction = `<div class='input-field col s12 m8 l8'>
    <input id='instructions' name='instructions' type='text' maxlength='100' class='validate_me'>
    <label for='instructions'>Instructions</label>
    <button type='button' class='delete btn-floating btn-small waves-effect waves-light red'><i class='fas fa-minus'></i></button>
</div>`

    // Adds new ingredient field 
    $(add_button_ingredient).click(function(e) {
        e.preventDefault();
        if (x < max_fields) {
            x++;
            $(wrapper1).append(appendIngredient); //add input box
        }
  else
  {
  alert('You Reached the limits')
  }
    });
 
    $(wrapper1).on("click",".delete", function(e){
        e.preventDefault(); 
        $(this).parent('div').remove(); x--;
    })
  
    // Adds new instruction field
    $(add_button_instruction).click(function(e) {
        e.preventDefault();
        if (x < max_fields) {
            x++;
            $(wrapper2).append(appendInstruction); //add input box
        }
  else
  {
  alert('You Reached the limits')
  }
    });
 
    $(wrapper2).on("click",".delete", function(e){
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })

    // $('.add-instruction-edit').click(function (event) {
    //             let buttonClass = $(event.target).parent().attr("class");

    //             if (buttonClass.includes("delete-edit")) {
    //                 let item = $(event.target).closest(".recipe-item");
    //                 item.remove();
    //             }
    //         })

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

  const el = document.createElement('div');
    el.innerHTML = "Here's a <a href='http://google.com'>link</a>";


  function sweetalertclick() {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: `<a href="{{ url_for('delete_recipe', recipe_id=recipe._id) }}">LINK</a>`
       }).then((result) => {
         if (result.value) {
         Swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success'
        )
       }
       })
  }


  {{ url_for('delete_recipe', recipe_id=recipe._id) }}

  `<a href="{{ url_for('delete_recipe', recipe_id=recipe._id) }}">LINK</a>`
$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();

    var elem = document.querySelector('.collapsible.expandable');
    var instance = M.Collapsible.init(elem, {
    accordion: false
    });
  });

  
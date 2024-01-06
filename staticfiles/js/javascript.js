(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()



// this is for the dropdown menu--------------------------------------------
function toggleDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}
// this is for the dropdown menu close when click outside
document.addEventListener('click', function (event) {
    var dropdown = document.getElementById('userDropdown');
    var triggerElement = document.querySelector('.navdrop2');

    if (!triggerElement.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});





// ---------------------------------------------
const filters = document.querySelectorAll(".filter");
const currentPath = window.location.pathname;

// when icon click autometic link click
let checkbox = document.getElementById("flexSwitchCheckDefault");


checkbox.addEventListener("click", () => {
    let taxe = document.getElementsByClassName("taxe-icon");
    console.log("It's working for 5555", taxe);
    for (info of taxe) {
        info.style.display = "block";
        if (checkbox.checked == false) {
            info.style.display = "none";
        }

    }
});

// when icon click autometic link click

filters.forEach((filter) => {
    const link = filter.querySelector("a");
    filter.addEventListener("click", () => {
        console.log("It's working for 5555");
        link.click();
    });
});

//  this is for add active class after refresh page
filters.forEach((filter) => {
    const linkElement = filter.querySelector("a");
    const filterPath = new URL(linkElement.href).pathname;

    if (currentPath === filterPath) {
        console.log("It's working for", filterPath);
        filter.classList.add("active");
    }
});




// ---------------------------------------------- this is for the taxe icon for display tax in the index page
const taxe = document.querySelectorAll('.taxe-icon');
const buttone = document.querySelector('#flexSwitchCheckDefault');
buttone.addEventListener('click', () => {
    taxe.forEach((tax) => {
        if (buttone.checked) {
            tax.style.display = 'block';
        } else {
            tax.style.display = 'none';
        }
    })
})



var myModal = document.getElementById('myModal')
    var myInput = document.getElementById('myInput')
    
    myModal.addEventListener('shown.bs.modal', function () {
      myInput.focus()
    })
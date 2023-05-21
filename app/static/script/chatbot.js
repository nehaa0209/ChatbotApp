/*$('#register-btn').click(function(event){
    alert('hi in file');
    // Prevent redirection with AJAX for contact form
    var form = $('#form_register');
    var form_id = 'form_register';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getContactFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData);
});

function getContactFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}



function send_form(form, form_id, url, type, inner_ajax, formData) {
    // form validation and sending of form items

    if ( form[0].checkValidity() && isFormDataEmpty(formData) == false ) { // checks if form is empty
        event.preventDefault();

        // inner AJAX call
        inner_ajax(url, type, formData);

    }
    else {
    
    }
}


function isFormDataEmpty(formData) {
    // checks for all values in formData object if they are empty
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value != '' && value != []) {
                return false;
            }
        }
    }
    return true;
}


function modular_ajax(url, type, formData) {
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function() {
            // show the preloader (progress bar)
            $('#form-response').html("<div class='progress'><div class='indeterminate'></div></div>");
        },
        complete: function () {
            // hide the preloader (progress bar)
            $('#form-response').html("");
        },
        success: function ( data ){
            if ( !$.trim( data.feedback )) { // response from Flask is empty
                toast_error_msg = "An empty response was returned.";
                toast_category = "danger";
            }
            else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = data.category;
            }
        },
        error: function(xhr) {console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = "An error occured";
            toast_category = "danger";
        },
    }).done(function() {
        M.toast({html: toast_error_msg, classes: 'bg-' +toast_category+ ' text-white'});
    });
};

var csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

*/

$('#form_register').on('submit', function(e) {
	e.preventDefault();
	calculateQTc();
});



function getContactFormData(form) {
	// creates a FormData object and adds chips text
	var formData = new FormData(document.getElementById(form));
	//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
	return formData
}

function calculateQTc() {
	alert("hi");
	var server_side_errors = document.getElementById("server_side_errors");

	var name = document.getElementById("name").value.trim();
	var username = document.getElementById("username").value.trim();
	var email = document.getElementById("email").value.trim();
	var phonenumber = document.getElementById("phonenumber").value.trim();
	var password = document.getElementById("password").value.trim();

	alert(name);

	checkname = validateName(name);
	checkusername = validateUsername(username);
	checkemail = validateEmail(email);
	checknumber = validatePhoneNumber(phonenumber);
	checkpassword = ValidatePassword(password);
	if (checkname && checkusername && checkemail && checknumber && checkpassword) {
		// If all fields are valid, you can proceed with form submission
		if (name !== '' && username !== '' && email !== '' && phonenumber !== '' && password !== '') {

			var form_id = 'form_register';

			var formData = getContactFormData(form_id);

			//var url = form.prop('action');
			var form = $('#form_register');
			var type = form.prop('method');
			var url = form.prop('action');
			alert('only');


			$.ajax({
				url: url,
				type: type,
				data: formData,
				processData: false,
				contentType: false,
				success: function(result) {
					alert(result.flag);
					alert(result.error_msg);
					if (result.flag == 1) {
						window.location.replace("/");
					} else {
						$("#server_side_errors").css("display", "none");
						//alert(result.error_message_email);
						server_side_errors.innerHTML = result.error_msg;
						$("#server_side_errors").css("display", "block");
					}


				}
			});
		}
	}



}

/*const form = document.getElementById('form_register');
   
 form.addEventListener('submit', function (e) {

     const name = document.getElementById("name").value.trim();
     const username = document.getElementById("username").value.trim();
     const email = document.getElementById("email").value.trim();
     const phonenumber = document.getElementById("phonenumber").value.trim();
     const password = document.getElementById("password").value.trim();

     e.preventDefault(); // Prevent form submission

     validateName(name);
     validateUsername(username);
     validateEmail(email);
     validatePhoneNumber(phonenumber);
     ValidatePassword(password);
     
         // If all fields are valid, you can proceed with form submission
     if (name !== '' && username !== ''&& email !== ''&& phonenumber !== ''&& password !== ''  ) {
         alert('only');
         form.submit();
     }

     });
*/

// Function to validate first name
function validateName(name) {
	const errorElement = document.getElementById("nameErrorMsg");
	if (name === '') {
		errorElement.innerHTML = 'Name is required';
		$("#nameErrorMsg").css("display", "block");
		return false;
	} else {
		errorElement.innerHTML = "";
		$("#nameErrorMsg").css("display", "none");
		return true;
	}
}

function validateUsername(username) {
	const errorElement = document.getElementById("usernameErrorMsg");
	if (username === '') {
		alert("hiiii");
		errorElement.innerHTML = 'Username is required';
		$("#usernameErrorMsg").css("display", "block");
		return false;
	} else {
		alert(" vooooo");
		errorElement.innerHTML = "";
		$("#usernameErrorMsg").css("display", "none")
		return true;
	}
}

function validateEmail(email) {
	const errorElement = document.getElementById("emailErrorMsg");
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	if (email === '') {
		errorElement.innerHTML = 'Email is required';
		$("#emailErrorMsg").css("display", "block");
		return false;
	} else if (!emailRegex.test(email)) {
		errorElement.innerHTML = 'Invalid Email Format';
		$("#emailErrorMsg").css("display", "block");
		return false;
	} else {
		errorElement.innerHTML = "";
		$("#emailErrorMsg").css("display", "none")
		return true;
	}
}

function validatePhoneNumber(phonenumber) {
	alert(phonenumber);
	const errorElement = document.getElementById("phonenumberErrorMsg");
	if (phonenumber === '') {
		alert("hiiii phone");
		errorElement.innerHTML = 'Phone Number is required';
		$("#phonenumberErrorMsg").css("display", "block");
		return false;
	} else if (phonenumber.length < 10) {
		alert("phoe");
		errorElement.innerHTML = 'Number should be 10 Digit long';
		$("#phonenumberErrorMsg").css("display", "block");
		return false;
	} else {
		errorElement.innerHTML = "";
		$("#phonenumberErrorMsg").css("display", "none");
		return true;
	}
}


function ValidatePassword(password) {
	const errorElement = document.getElementById("passwordErrorMsg");
	if (password === '') {
		errorElement.innerHTML = 'Password is required';
		$("#passwordErrorMsg").css("display", "block");
		return false;
	} else if (password.length < 8) {
		errorElement.innerHTML = 'Password should be at least 8 characters long';
		$("#passwordErrorMsg").css("display", "block");
		return false;
	} else {
		errorElement.innerHTML = "";
		$("#passwordErrorMsg").css("display", "none");
		return true;
	}
}
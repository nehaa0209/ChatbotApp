// form submit jquery
$('#form_register').on('submit', function(e) {
    e.preventDefault();
    submitForm();
});

// function to get formdata
function getSignupFormData(form) {
    var formData = new FormData(document.getElementById(form));
    return formData
}

// submit form through ajax
function submitForm(){
    var server_side_errors = document.getElementById("server_side_errors");

    var name = document.getElementById("name").value.trim();
    var username = document.getElementById("username").value.trim();
    var email = document.getElementById("email").value.trim();
    var phonenumber = document.getElementById("phonenumber").value.trim();
    var password = document.getElementById("password").value.trim();

    checkname = validateName(name);
    checkusername = validateUsername(username);
    checkemail = validateEmail(email);
    checknumber = validatePhoneNumber(phonenumber);
    checkpassword = ValidatePassword(password);
    if(checkname && checkusername && checkemail && checknumber && checkpassword){
         // If all fields are valid, you can proceed with form submission
     if (name !== '' && username !== ''&& email !== ''&& phonenumber !== ''&& password !== ''  ) {
       
        var form_id = 'form_register';
        var formData = getSignupFormData(form_id);
        var form = $('#form_register');
        var type = form.prop('method');
        var url = form.prop('action');
    
           $.ajax({
            url: url,
            type: type,
            data: formData,
            processData: false,
            contentType: false,
             success: function(result) {
                if(result.flag == 1){
                    window.location.replace("/");
                }else{
                    $("#server_side_errors").css("display", "none");
                    server_side_errors.innerHTML = result.error_msg; 
                    $("#server_side_errors").css("display", "block");
                }
             

             } 
           });
        }
    }  
}

 
 // Function to validate name
 function validateName(name) {
    const errorElement = document.getElementById("nameErrorMsg");
    if (name === '') {
        errorElement.innerHTML = 'Name is required';
        $("#nameErrorMsg").css("display", "block");
        return false;
    } else {
        errorElement.innerHTML="";
        $("#nameErrorMsg").css("display", "none");
        return true;
    }
  }
 // Function to validate username
  function validateUsername(username) {
    const errorElement = document.getElementById("usernameErrorMsg");
    if (username === '') {
        errorElement.innerHTML = 'Username is required';
        $("#usernameErrorMsg").css("display", "block");
        return false;
    } else {
        errorElement.innerHTML="";
        $("#usernameErrorMsg").css("display", "none")
        return true;
    }
  }
  // Function to validate email
  function validateEmail(email) {
    const errorElement = document.getElementById("emailErrorMsg");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === '') {
        errorElement.innerHTML = 'Email is required';
        $("#emailErrorMsg").css("display", "block");
        return false;
    }else if(!emailRegex.test(email)){
         errorElement.innerHTML = 'Invalid Email Format';
         $("#emailErrorMsg").css("display", "block");
         return false;
    } 
    else {
        errorElement.innerHTML="";
        $("#emailErrorMsg").css("display", "none")
        return true;
    }
  }

  // Function to validate phone number
  function validatePhoneNumber(phonenumber) {
    const errorElement = document.getElementById("phonenumberErrorMsg");
    if (phonenumber === '') {
        errorElement.innerHTML = 'Phone Number is required';
        $("#phonenumberErrorMsg").css("display", "block");
        return false;
    }
    else if(phonenumber.length < 10){
        errorElement.innerHTML = 'Number should be 10 Digit long';
        $("#phonenumberErrorMsg").css("display", "block");
        return false;
    }else {
        errorElement.innerHTML="";
        $("#phonenumberErrorMsg").css("display", "none");
        return true;
    }
  }

  // Function to validate Password
  function ValidatePassword(password) {
    const errorElement = document.getElementById("passwordErrorMsg");
    if (password === '') {
        errorElement.innerHTML = 'Password is required';
        $("#passwordErrorMsg").css("display", "block");
        return false;
    }else if(password.length < 8){
     errorElement.innerHTML = 'Password should be at least 8 characters long';
     $("#passwordErrorMsg").css("display", "block");
     return false;
    } else {
        errorElement.innerHTML="";
        $("#passwordErrorMsg").css("display", "none");
        return true;
    }
  }

  
  // search functionality
  $(document).ready(function () {
    $("#filterCards").keyup(function () {
      var filter = $(this).val();
      $(".chat_div").each(function () {
        var $i = 0;
        $(this)
          .find(".searchable")
          .each(function () {
            if ($(this).text().search(new RegExp(filter, "i")) >= 0) {
              $i++;
            }
          });
        if ($i > 0) {
          $(this).closest(".chat_div").show();
        } else {
          $(this).closest(".chat_div").hide();
        }
      });
    });
  });
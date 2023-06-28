// function to validate a registration form
function formValidationRegister() {
  // get email, password and repetition of the password to validate them
  let email = document.registration.email;
  let password = document.registration.password;
  let rep_password = document.registration.rep_password;

  // get elements with errors to hide/show them, put them to an array to iterate through
  let email_error = document.getElementById('email_error');
  let password_error_empty = document.getElementById('password_error_empty');
  let password_error_mismatch = document.getElementById('password_error_mismatch');
  const errors = [email_error, password_error_empty, password_error_mismatch];

  // alert(email);

  // for an every error check whether it is shown on the page, if yes, hide it
  for (let error of errors) {
    if (error.style.display == 'block') {
      error.style.display = 'none';
    }
  }

  // if the email and the passwords are valid, process the registration form on the backend,
  // if not, show an error
  if (validateEmail(email) && validatePassword(password, rep_password)) {
    return true;
  } else {
    return false;
  }
}

// function to check a login form
function formValidationLogin() {
  // get email and password to validate them
  let email = document.login.email;
  let password = document.login.password;
  console.log(email);

  // if email is valid, process the form, if not, show an error
  if (validateEmail(email)) {
    return true;
  } else {
    return false;
  }
}

// function to validate email
function validateEmail(email) {
  // set a format of an email address
  let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

  // validate passed email address
  // if valid -> return true,
  // if not -> display an error
  if (email.value.match(mailformat)) {
    return true;
  } else {
    console.log('Im here');
    email.focus();
    document.getElementById('email_error').style.display = 'block';
    return false;
  }
}

// function to validate password and password repetition
function validatePassword(password, rep_password) {
  // if passwords don't match or length of password is less than 7 characters, show an error and don't process further
  let password_length = password.value.length;
  if (password.value != rep_password.value) {
    rep_password.focus();
    document.getElementById('password_error_mismatch').style.display = 'block';
    return false;
  } else if (password_length < 7) {
    password.focus();
    document.getElementById('password_error_empty').style.display = 'block';
    return false;
  }
  return true;
}
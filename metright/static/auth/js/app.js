// For Demo Purpose [Changing input group text on focus]
$(function () {
    $('input, select').on('focus', function () {
        $(this).parent().find('.input-group-text').css('border-color', '#80bdff');
    });
    $('input, select').on('blur', function () {
        $(this).parent().find('.input-group-text').css('border-color', '#ced4da');
    });
});


// For the registeration functionality
const usernameField = document.querySelector("#Username");
const feedbackField = document.querySelector(".invalid-feedback");
const EmailfeedbackField = document.querySelector(".email-feedback");
const emailField = document.querySelector("#email");
const userNameOutput = document.querySelector(".userNameOutput");


emailField.addEventListener('keyup', (e) =>{
    // saving the username in a variable
    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid');
    EmailfeedbackField.style.display="none";

   if (emailVal.length > 0){
        // making an API call to the server
    fetch("/auth/validate-email", {
        body: JSON.stringify({email: emailVal }),
        method: "POST"
    })
        .then((res)=>res.json())
        .then((data) =>{
            console.log('data', data);
            if(data.email_error){
                emailField.classList.add('is-invalid');
                EmailfeedbackField.innerHTML = `<p>${data.email_error}</p>`;
                EmailfeedbackField.style.display="inline-block";
                emailField.classList.add('text-danger');
            }

        });
   }

});

usernameField.addEventListener('keyup', (e) => {
    // saving the username in a variable
    const usernameVal = e.target.value;
    
    userNameOutput.style.display = "block"
    userNameOutput.textContent = `Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedbackField.style.display="none";

   if (usernameVal.length > 0) {
        // making an API call to the server
    fetch("/auth/validate-username", {
        body: JSON.stringify({username: usernameVal }),
        method: "POST"
    })
        .then((res)=>res.json())
        .then((data) =>{
            userNameOutput.style.display='none'
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;
                feedbackField.style.display="block";
            }

        });
   }
});
import { registrationAPI } from './registrationAPI.js';

document.addEventListener('DOMContentLoaded', () => 
{
    setupRegistrationFormHandler();
});

function setupRegistrationFormHandler() 
{
  const form = document.getElementById('registrationForm');
  form.addEventListener('submit', async e => 
  {
        e.preventDefault();
        clearPasswordError(form);

        const register = getFormData();

        if(!register.name || !register.mail || !register.password){
            createErrorMessage("registrationForm", "All fields must be filled in.");
            return;
        }

        if(register.name.length > 20){
            createErrorMessage("container-user-name", "User name too long.");
            return;
        }

        if(!isValidEmail(register.mail)){
            createErrorMessage("container-mail", "Invalid email.");
            return;
        }

        /*
        if(!isValidPassword(register.password)){
            createErrorMessage("container-password", "It must contain 8 characters and at least one lowercase letter, one uppercase letter, one number, and one special character..");
            return;
        }
        */

        try 
        { 
            const result = await registrationAPI.create(register);
            form.reset();
            
            // Guardar token
            localStorage.setItem("token", result.access_token)
            localStorage.setItem("token_type", result.token_type)

            // Redireccionar
            window.location.href = "tournament.html"
        }
        catch (err)
        {
            console.log("ERROR: ", err);
            alert("It couldn't create the user.");
        }
  });
}

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function isValidPassword(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/;
    return regex.test(password);
}

function createErrorMessage(containerId, message) {
    const container = document.getElementById(containerId);
    const p = document.createElement("p");
    p.classList.add("error-message");
    p.textContent = message;
    container.appendChild(p);
}

function clearPasswordError(container) {
    const error = container.querySelector(".error-message");
    if (error) error.remove();
}

function getFormData() {
    return {
        name: document.getElementById('user_name').value.trim(),
        mail: document.getElementById('mail').value.trim(),
        password: document.getElementById('user_password').value.trim()
        };
}
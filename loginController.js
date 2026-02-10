import { loginAPI } from './loginAPI.js';

document.addEventListener('DOMContentLoaded', () => 
{
    setupLoginFormHandler();
});

function setupLoginFormHandler() 
{
  const form = document.getElementById('loginForm');
  form.addEventListener('submit', async e => 
  {
        e.preventDefault();
        clearPasswordError(form);
        const register = getFormData();

        if(!register.mail || !register.password){
            createErrorMessage("loginForm", "All fields must be filled in.");
            return;
        }

        if(!isValidEmail(register.mail)){
            createErrorMessage("loginForm", "Invalid credentials.");
            return;
        }

        /*
        if(!isValidPassword(register.password)){
            createErrorMessage("loginForm", "Invalid credentials.");
            return;
        }
        */
        
        try 
        {
            const result = await loginAPI.create(register);
            form.reset();
            
            // Guardar token
            localStorage.setItem("token", result.access_token)
            localStorage.setItem("token_type", result.token_type)

            // Redireccionar
            window.location.href = `tournament.html?view=general`;
        }
        catch (err)
        {
            console.log("ERROR: ", err);
            alert("It couldn't login the user.");
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
        mail: document.getElementById('mail').value.trim(),
        password: document.getElementById('user_password').value.trim()
        };
}
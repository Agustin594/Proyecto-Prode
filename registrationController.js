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
        const register = getFormData();

        // Validaciones

        try 
        { 
            console.log(register);
            const result = await registrationAPI.create(register);
            console.log(result);
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

function getFormData() {
    return {
        name: document.getElementById('user_name').value.trim(),
        mail: document.getElementById('mail').value.trim(),
        password: document.getElementById('user_password').value.trim()
        };
}
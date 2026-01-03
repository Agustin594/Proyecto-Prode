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
        const log = getFormData();

        // Validaciones

        try 
        { 
            console.log(log);
            const result = await loginAPI.create(log);
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
            alert("It couldn't login the user.");
        }
  });
}

function getFormData() {
    return {
        mail: document.getElementById('mail').value.trim(),
        password: document.getElementById('user_password').value.trim()
        };
}
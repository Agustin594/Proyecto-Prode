import { tournamentRegisterAPI } from './tournamentRegisterAPI.js';

let currentTournamentId = null;
const modal = document.getElementById("passwordModal");
const confirmBtn = document.getElementById("confirmBtn");
const cancelBtn = document.getElementById("cancelBtn");

document.addEventListener("click", async (e) => {
    if(e.target.dataset.type === "register") {
        const hasPassword = e.target.dataset.hasPassword === "true";
        currentTournamentId = e.target.dataset.tournamentId;

        if (hasPassword) {
            modal.classList.remove("hidden");
        } else {
            await registerTournament("");
        }
    } else if(e.target.dataset.type === "delete") {
        confirmAction("Are you sure you want to leave the tournament? Your predictions will be lost.",
            async () => {
                const tournamentId = e.target.dataset.tournamentId;

                const register = {tournament_id : tournamentId}

                try { 
                    await tournamentRegisterAPI.remove(register);

                    sessionStorage.setItem("flashMessage", "You were successfully eliminated from the tournament.");
                    sessionStorage.setItem("flashType", "success");

                    window.location.href = "tournament.html?view=general";
                }
                catch (err) {
                    console.log("ERROR: ", err);
                    showToast("You could not be eliminated from the tournament.", "error");
                }
            }
        );
    }
});

cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    const div = document.getElementById("div-user-tournament-password");
    clearPasswordError(div);
});

confirmBtn.addEventListener("click", async () => {
    const password = document.getElementById("userTournamentPassword").value.trim();
    const div = document.getElementById("div-user-tournament-password");

    if(password === ""){
        const p = document.createElement("p");
        p.classList.add("error-message");
        p.textContent = "The password cannot be empty.";
        div.appendChild(p);
    } else {
        try {
            await registerTournament(password);
            clearPasswordError(div);
            modal.classList.add("hidden");
        } catch (err) {
            clearPasswordError(div);

            const p = document.createElement("p");
            p.classList.add("error-message");

            /*
            if (err.status === 401) {
                p.textContent = err.message; // mensaje del backend
            } else {
                p.textContent = "Unexpected error. Try again later.";
            }
            */
            p.textContent = "Incorrect password."

            div.appendChild(p);
        }
    }
});

function clearPasswordError(div) {
    const error = div.querySelector(".error-message");
    if (error) error.remove();
}

async function registerTournament(password) {
    try {
        const register = {
            tournament_id: currentTournamentId,
            password: password
        }

        await tournamentRegisterAPI.create(register);
        
        sessionStorage.setItem("flashMessage", "You were successfully registered for the tournament.");
        sessionStorage.setItem("flashType", "success");

        window.location.href = "tournament.html?view=personal";
    } catch (err) {
        console.log(err);
        showToast("You could not be registered for the tournament.", "error");
    }
}

function confirmAction(message, onConfirm) {
    const modal = document.getElementById("confirmModal");
    const text = document.getElementById("confirmText");
    const ok = document.getElementById("confirmOk");
    const cancel = document.getElementById("confirmCancel");

    text.textContent = message;
    modal.classList.remove("hidden");

    ok.onclick = () => {
        modal.classList.add("hidden");
        onConfirm();
    };

    cancel.onclick = () => {
        modal.classList.add("hidden");
    };
}

function showToast(message, type = "info", duration = 3000) {
  const container = document.getElementById("toastContainer");

  const toast = document.createElement("div");
  toast.className = `toast`;

  const p = document.createElement('p');
  p.textContent = message;

  const i = document.createElement('i');
  i.classList.add("fa-regular");

  if(type === "info") {
    i.classList.add("fa-circle-question");
  } else if(type === "error") {
    i.classList.add("fa-circle-xmark");
  } else if(type === "success") {
    i.classList.add("fa-circle-check");
  }

  toast.appendChild(i);
  toast.appendChild(p);

  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, duration);
}
import { tournamentRegisterAPI } from './tournamentRegisterAPI.js';
import loadTournaments from './tournamentController.js';
import loadOwnTournaments from './tournamentController.js';

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
        const tournamentId = e.target.dataset.tournamentId;

        const register = {tournament_id : tournamentId}

        try { 
            await tournamentRegisterAPI.remove(register);
            loadTournaments();
            loadOwnTournaments();
        }
        catch (err) {
            console.log("ERROR: ", err);
            alert("You can't abandon the torunament.");
        }
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
        loadTournaments();
        loadOwnTournaments();
    } catch (err) {
        console.log(err);
        alert("It couldn't register you into the tournament.");
    }
}
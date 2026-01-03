import { tournamentRegisterAPI } from './tournamentRegisterAPI.js';
import loadTournaments from './tournamentController.js';

document.addEventListener("click", async (e) => {
    if(e.target.dataset.type === "register") {
        const tournamentId = e.target.dataset.tournamentId;

        const register = {tournament_id : tournamentId} 

        try { 
            await tournamentRegisterAPI.create(register);
            loadTournaments();
        }
        catch (err) {
            console.log("ERROR: ", err);
            alert("It couldn't register you into the tournament.");
        }
    }
});
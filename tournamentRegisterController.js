import { tournamentRegisterAPI } from './tournamentRegisterAPI.js';
import loadTournaments from './tournamentController.js';
import loadOwnTournaments from './tournamentController.js';


document.addEventListener("click", async (e) => {
    if(e.target.dataset.type === "register") {
        const tournamentId = e.target.dataset.tournamentId;

        const register = {tournament_id : tournamentId}

        try { 
            await tournamentRegisterAPI.create(register);
            loadTournaments();
            loadOwnTournaments();
        }
        catch (err) {
            console.log("ERROR: ", err);
            alert("It couldn't register you into the tournament.");
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
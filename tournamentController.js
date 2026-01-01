import { tournamentAPI } from './tournamentAPI.js';

document.addEventListener('DOMContentLoaded', () => 
{
    setupTournamentFormHandler();
});

function setupTournamentFormHandler() 
{
  const form = document.getElementById('tournamentForm');
  form.addEventListener('submit', async e => 
  {
        e.preventDefault();
        const tournament = getFormData();

        // Validaciones

        try 
        { 
            console.log(tournament);
            result = await tournamentAPI.create(tournament);
            console.log(result);
            form.reset();
        }
        catch (err)
        {
            alert("It couldn't create the tournament.");
        }
  });
}

function getFormData() {
    return {
        competition_id: document.getElementById('competition').value.trim(),
        open: document.getElementById('open').checked,
        participant_limit: parseInt(document.getElementById('participants').value.trim(), 10),
        entry_price: parseInt(document.getElementById('price').value.trim(), 10),
        public: document.getElementById('public').checked
        };
}
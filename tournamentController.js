import { tournamentAPI } from './tournamentAPI.js';
export default loadTournaments;

document.addEventListener('DOMContentLoaded', () => 
{
    const token = localStorage.getItem("token")

    if (!token) {
        window.location.href = "login.html"
    }

    //initSelect();
    setupTournamentFormHandler();
    loadTournaments();
    loadOwnTournaments();
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
            const result = await tournamentAPI.create(tournament);
            console.log(result);
            form.reset();
            loadTournaments();
            loadOwnTournaments();
        }
        catch (err)
        {
            console.log("ERROR: ", err);
            alert("It couldn't create the tournament.");
        }
  });
}

function getFormData() {
    return {
        competition_id: document.getElementById('competition').value.trim(),
        participant_limit: parseInt(document.getElementById('participants').value.trim(), 10),
        entry_price: parseInt(document.getElementById('price').value.trim(), 10),
        public: document.getElementById('public').checked
        };
}

async function loadTournaments() 
{
    try 
    {
        const tournaments = await tournamentAPI.fetchAll();
        
        /**
         * DEBUG
         */
        //console.log(relations);

        /**
         * En JavaScript: Cualquier string que no esté vacío ("") es considerado truthy.
         * Entonces "0" (que es el valor que llega desde el backend) es truthy,
         * ¡aunque conceptualmente sea falso! por eso: 
         * Se necesita convertir ese string "0" a un número real 
         * o asegurarte de comparar el valor exactamente. 
         * Con el siguiente código se convierten todos los string approved a enteros.
         */
        //relations.forEach(rel => 
        //{
        //    rel.approved = Number(rel.approved);
        //});
        
        renderTournamentList(tournaments, "tournamentList", "register");
    } 
    catch (err) 
    {
        console.error('Tournament charge error:', err.message);
        errormessage();
    }
}

async function loadOwnTournaments() 
{
    try 
    {
        const tournaments = await tournamentAPI.fetchMine();
        
        renderTournamentList(tournaments, "myTournamentList", "delete");
    } 
    catch (err) 
    {
        console.error('Tournament charge error:', err.message);
        errormessage();
    }
}

function renderTournamentList(tournaments, id, type) 
{
    const list = document.getElementById(id);
    list.replaceChildren();

    tournaments.forEach(t => 
    {
        const div = document.createElement('div');

        const p = document.createElement("p");

        const status = t.open ? "Inscripción abierta" : "Inscripción cerrada";
        const visibility = t.public ? "Público" : "Privado";
        const price = t.entry_price === 0 ? "Gratis" : `$${t.entry_price}`;

        p.textContent = `${t.name} — Participantes: ${t.registered_participants}/${t.participant_limit} — ${price} — ${visibility} — ${status}`;

        div.appendChild(p);

        if(type == "register") {
            registerButton(div, t.id);
        } else if(type == "delete") {
            deleteButton(div, t.id);
        }

        list.appendChild(div);
    });
}

function registerButton(container, tournament_id) {
    const btn = document.createElement("button");
    btn.dataset.type = "register";
    btn.textContent = "Register";
    btn.dataset.tournamentId = tournament_id;
    container.appendChild(btn);
}

function deleteButton(container, tournament_id) {
    const btn = document.createElement("button");
    btn.dataset.type = "delete";
    btn.textContent = "Delete";
    btn.dataset.tournamentId = tournament_id;
    container.appendChild(btn);
}

function errormessage(){
    const list = document.getElementById('tournamentList');
    list.replaceChildren();

    const div = document.createElement('div');

    div.appendChild(createErrorCell());

    list.appendChild(div);
}

function createErrorCell(){
    const p = document.createElement('p');
    p.textContent = "Data charge error.";
    return p;
}
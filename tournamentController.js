import { tournamentAPI } from './tournamentAPI.js';
export default loadTournaments;

document.addEventListener('DOMContentLoaded', () => 
{
    const token = localStorage.getItem("token")

    if (!token) {
        window.location.href = "login.html"
    }

    const params = new URLSearchParams(window.location.search);
    const tournamentId = params.get("id");

    if (tournamentId) {
        showTournamentDetail(tournamentId);
        loadTournamentData(tournamentId);
        loadTournamentUserTable(tournamentId);
        loadTournamentMatchTable(tournamentId);
        loadTournamentGoalscorerTable(tournamentId);
    } else {
        showTournamentList();
        //initSelect();
        setupTournamentFormHandler();
        loadTournaments();
        loadOwnTournaments();
        setupTournamentData();
    }
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
        div.classList.add("tournament-card");
        div.dataset.id = t.id;

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

function setupTournamentData(){
    document.addEventListener("click", (e) => {
        const card = e.target.closest(".tournament-card");
        if (!card) return;

        const tournamentId = card.dataset.id;

        // si clickea el botón interno, evitás conflicto
        if (e.target.tagName === "BUTTON") return;

        window.location.href = `tournament.html?id=${tournamentId}`;
    });
}

function showTournamentList() {
  document.getElementById("tournament-list").hidden = false;
  document.getElementById("tournament-detail").hidden = true;
}

function showTournamentDetail(id) {
  document.getElementById("tournament-list").hidden = true;
  document.getElementById("tournament-detail").hidden = false;
}

async function loadTournamentData(tournamentId) 
{
    try 
    {
        const t = await tournamentAPI.fetchById(tournamentId);
        
        const div = document.getElementById('tournament-data');
        div.replaceChildren();

        
        const p = document.createElement('p');

        const status = t.open ? "Inscripción abierta" : "Inscripción cerrada";
        const visibility = t.public ? "Público" : "Privado";
        const price = t.entry_price === 0 ? "Gratis" : `$${t.entry_price}`;

        p.textContent = `${t.name} — Participantes: ${t.registered_participants}/${t.participant_limit} — ${price} — ${visibility} — ${status}`;

        div.appendChild(p);
        
    } 
    catch (err) 
    {
        console.error('Error cargando inscripciones:', err.message);
        errormessage();
    }
}

async function loadTournamentUserTable(tournamentId) 
{
    try 
    {
        const users = await tournamentAPI.fetchByPath(`${tournamentId}/standings`);
        
        renderStandingTable(users);
    } 
    catch (err) 
    {
        console.error('Error cargando posiciones:', err.message);
        errormessage();
    }
}


function renderStandingTable(users) 
{
    const tbody = document.getElementById('user-table');
    tbody.replaceChildren();

    let pos = 1;
    users.forEach(u => 
    {
        const tr = document.createElement('tr');

        tr.appendChild(createCell(pos));
        tr.appendChild(createCell(u.user_name));
        tr.appendChild(createCell(u.points));

        tbody.appendChild(tr);

        pos+=1;
    });
}

function createCell(text) 
{
    const td = document.createElement('td');
    td.textContent = text;
    return td;
}

async function loadTournamentMatchTable(tournamentId) {
    try 
    {
        const matches = await tournamentAPI.fetchByPath(`${tournamentId}/matches`);
        
        renderMatchTable(matches);
    } 
    catch (err) 
    {
        console.error('Error cargando partidos:', err.message);
        errormessage();
    }
}

function renderMatchTable(matches) 
{
    const tbody = document.getElementById('match-table');
    tbody.replaceChildren();

    matches.forEach(m => 
    {
        const tr = document.createElement('tr');

        tr.appendChild(createCell(m.date));
        tr.appendChild(createCell(m.home_team_name));
        tr.appendChild(createCell(m.home_goals));
        tr.appendChild(createCell(m.away_goals));
        tr.appendChild(createCell(m.away_team_name));

        tbody.appendChild(tr);
    });
}

async function loadTournamentGoalscorerTable(tournamentId) {
    try 
    {
        const scorers = await tournamentAPI.fetchByPath(`${tournamentId}/scorers`);
        
        renderScorerTable(scorers);
    } 
    catch (err) 
    {
        console.error('Error cargando goleadores:', err.message);
        errormessage();
    }
}

function renderScorerTable(scorers) 
{
    const tbody = document.getElementById('scorer-table');
    tbody.replaceChildren();

    scorers.forEach(s => 
    {
        const tr = document.createElement('tr');

        tr.appendChild(createCell(s.name));
        tr.appendChild(createCell(s.goals));

        tbody.appendChild(tr);
    });
}
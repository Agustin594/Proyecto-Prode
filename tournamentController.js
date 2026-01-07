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
        showTournamentDetail();
        loadTournamentData(tournamentId);
        loadTournamentUserTable(tournamentId);
        initTournament(tournamentId);
    } else {
        initSelect();
        showTournamentList();
        setupTournamentFormHandler();
        loadTournaments();
        loadOwnTournaments();
        setupTournamentData();
    }
});

async function initTournament(tournamentId) {
    const registered = await isRegistered(tournamentId);

    if (registered) {
        loadSpecialPredictionForm(tournamentId);
        //setupSpecialPredictionForm(tournamentId);
        setupAbandonButton(tournamentId);
        loadTournamentMatchTable(tournamentId);
        loadTournamentGoalscorerTable(tournamentId);
    } else {
        document.getElementById("matches").hidden = true;
        document.getElementById("scorers").hidden = true;
        setupRegisterButton(tournamentId);
    }
}

async function initSelect() 
{
    try 
    {
        const competitions = await tournamentAPI.fetchByPath(`competitions`);
        const competitionSelect = document.getElementById('competitionIdSelect');
        competitions.forEach(c => 
        {
            const option = document.createElement('option');
            option.value = c.id;
            option.textContent = c.name;
            competitionSelect.appendChild(option);
        });
    } 
    catch (err) 
    {
        console.error('Error cargando competiciones:', err.message);
    }
}

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
        competition_id: document.getElementById('competitionIdSelect').value,
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

    if(tournaments.length === 0){
        const p = document.createElement("p");
        p.textContent = "No hay torneos disponibles.";
        list.appendChild(p);
    } else {
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

function showTournamentDetail() {
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

async function isRegistered(tournamentId){
    const register = await tournamentAPI.fetchByPath(`${tournamentId}/inscription`);
    console.log(register);
    return register.length === 1;
}

function loadSpecialPredictionForm(tournamentId){
    document.getElementById("prediction-container").hidden = false;
    //initTeamSelect();
    //initPlayerSelect();
}

function setupSpecialPredictionForm(tournamentId) {
  const form = document.getElementById('predictionForm');
  form.addEventListener('submit', async e => 
  {
        e.preventDefault();
        const prediction = getPredictionFormData(tournamentId);

        // Validaciones

        try 
        { 
            await tournamentAPI.updateWithPath(`${tournamentId}/prediction`, prediction);
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

function getPredictionFormData(tournamentId) {
    return {
        tournament_id: tournamentId,
        champion_id: document.getElementById('championIdSelect').value,
        top_scorer_id: document.getElementById('goalscorerIdSelect').value
        };
}

function setupAbandonButton(tournamentId){
    const container = document.getElementById("prediction-container");
    deleteButton(container, tournamentId);
}

function setupRegisterButton(tournamentId){
    const data = document.getElementById("tournament-data");
    const container = document.createElement("div");
    registerButton(container, tournamentId);
    data.appendChild(container);
}
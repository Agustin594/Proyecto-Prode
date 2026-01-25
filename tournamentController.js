import { tournamentAPI } from './tournamentAPI.js';
export default loadTournaments;

const competitionColors = {
  4: "#fc9802",
  5: "#0230fc",
  6: "#fc1f02",
  7: "#fcce02",
  8: "#7702fc",
  9: "#028bfc",
  10: "#000a92",
  11: "#dd0000",
  14: "#fc02db",
  15: "#02ebfc",
  16: "#02fc23",
  17: "#fcce02"
};

const competitionSecundaryColors = {
  4: "#474747",
  5: "#d8d8d8",
  6: "#d8d8d8",
  7: "#474747",
  8: "#d8d8d8",
  9: "#d8d8d8",
  10: "#d8d8d8",
  11: "#d8d8d8",
  14: "#d8d8d8",
  15: "#474747",
  16: "#474747",
  17: "#474747"
};

const competitionImage = {
  4: "image/EURO.png",
  5: "image/ChampionsLeague.png",
  6: "image/LaLiga.png",
  7: "image/Mundial.png",
  8: "image/PremierLeague.png",
  9: "image/SerieA.png",
  10: "image/Ligue1.png",
  11: "image/Bundesliga.png",
  14: "image/CopaAmerica.png",
  15: "image/LPF2.png",
  16: "image/Brasileirao.png",
  17: "image/Libertadores.png"
};

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
        setupPasswordInput();
        loadTournaments();
        loadOwnTournaments();
        setupTournamentData();
    }
});

async function initTournament(tournamentId) {
    const registered = await isRegistered(tournamentId);

    if (registered) {
        loadSpecialPredictionForm(tournamentId);
        setupSpecialPredictionForm(tournamentId);
        setupAbandonButton(tournamentId);
        loadTournamentMatchTable(tournamentId);
        setupMatchPrediction(tournamentId);
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
        clearPasswordError(form);
        const tournament = getFormData();

        if(!tournament.competition_id || !tournament.participant_limit || !tournament.entry_price || (!tournament.password && !tournament.public)){
            createErrorMessage("tournamentForm", "All fields must be filled in.");
            return;
        }

        if(tournament.competition_id <= 0) {
            createErrorMessage("container-competition-id", "Invalid competition.");
            return;
        }

        if(tournament.participant_limit < 5) {
            createErrorMessage("container-participant-limit", "Invalid participant limit, the minimun limit is 5 participants.");
            return;
        }

        if(tournament.entry_price < 0) {
            createErrorMessage("container-entry-price", "The price cannot be negative.");
            return;
        }

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

function createErrorMessage(containerId, message) {
    const container = document.getElementById(containerId);
    const p = document.createElement("p");
    p.classList.add("error-message");
    p.textContent = message;
    container.appendChild(p);
}

function clearPasswordError(container) {
    const error = container.querySelector(".error-message");
    if (error) error.remove();
}

function getFormData() {
    return {
        competition_id: document.getElementById('competitionIdSelect').value,
        participant_limit: parseInt(document.getElementById('participants').value.trim(), 10),
        entry_price: parseInt(document.getElementById('price').value.trim(), 10),
        public: document.getElementById('public').checked,
        password: document.getElementById('tournament-password').value.trim()
        };
}

function setupPasswordInput() {
    const radios = document.querySelectorAll('input[name="privacity"]');
    const passwordDiv = document.getElementById('password-input');
    const passwordInput = document.getElementById('tournament-password');

    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'private' && radio.checked) {
                passwordDiv.hidden = false;
                passwordInput.required = true;
            } else if (radio.value === 'public' && radio.checked) {
                passwordDiv.hidden = true;
                passwordInput.required = false;
                passwordInput.value = '';
            }
        });
    });
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
        p.textContent = "There are no tournaments available.";
        list.appendChild(p);
    } else {
        tournaments.forEach(t => 
        {
            const container = document.createElement('div');
            container.classList.add("tournament-card");
            container.dataset.id = t.id;
            container.style.setProperty(
                "--competition-color",
                competitionColors[t.competition_id]
            );
            container.style.setProperty(
                "--competition-secundary-color",
                competitionSecundaryColors[t.competition_id]
            );

            const containerImg = document.createElement('div');
            containerImg.classList.add("container-img");

            const img = document.createElement("img");
            img.src = competitionImage[t.competition_id];
            img.alt = `${t.name} logo`;

            containerImg.appendChild(img);

            const competition = document.createElement("h4");
            competition.textContent = t.name;

            const containerData = document.createElement("div");
            containerData.classList.add("container-data");

            container.appendChild(containerImg);
            container.appendChild(competition);
            container.appendChild(containerData);

            const info = document.createElement("div");
            info.classList.add("container-info");

            const containerBtn = document.createElement("div");
            containerBtn.classList.add("container-btn");

            containerData.appendChild(info);
            containerData.appendChild(containerBtn);

            const tInfo = document.createElement("div");

            info.appendChild(tInfo);

            const p1 = document.createElement("p");
            const p2 = document.createElement("p");

            p1.textContent = t.public ? "Público" : "Privado";
            const i = document.createElement("i");
            i.classList.add("fa-solid");
            if(t.public){
                i.classList.add("fa-unlock");
            } else {
                i.classList.add("fa-lock");
            }
            p1.appendChild(i);

            p2.textContent = `Participantes: ${t.registered_participants}/${t.participant_limit}`;

            tInfo.appendChild(p1);
            tInfo.appendChild(p2);

            if(type == "register") {
                if(t.registered_participants < t.participant_limit && t.open){
                    registerButton(containerBtn, t);
                }
            } else if(type == "delete") {
                if(t.open){
                    deleteButton(containerBtn, t.id);
                }
            }

            list.appendChild(container);
        });
    }
}

function registerButton(container, tournament) {
    const btn = document.createElement("button");
    btn.classList.add("tournament-btn");
    btn.id = "registerBtn"
    btn.dataset.type = "register";
    if(tournament.entry_price === 0){
        btn.textContent = "FREE";
        btn.classList.add("free");
    } else {
        btn.textContent = `${tournament.entry_price} FICHAS`;
        btn.classList.add("pay");
    }
    btn.dataset.tournamentId = tournament.id;
    if(tournament.password == null)
        btn.dataset.hasPassword = "false"
    else
        btn.dataset.hasPassword = "true";
    container.appendChild(btn);
}

function deleteButton(container, tournament_id) {
    const btn = document.createElement("button");
    btn.classList.add("tournament-btn");
    btn.classList.add("delete");
    btn.dataset.type = "delete";
    btn.textContent = "Abandon";
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
        
        if(m.status === "finished"){
            tr.appendChild(createCell(m.home_goals));
        } else {
            tr.appendChild(createCell(""));
        }

        createInputCells(tr, m)

        if(m.status === "finished"){
            tr.appendChild(createCell(m.away_goals));
        } else {
            tr.appendChild(createCell(""));
        }
        
        tr.appendChild(createCell(m.away_team_name));

        tr.appendChild(createPredictCell(m));

        tbody.appendChild(tr);
    });
}

function createInputCells(container, match) {
    const matchStart = new Date(match.date);
    const now = new Date();
    const homeTd = document.createElement('td');
    const awayTd = document.createElement('td');
    const homeInput = document.createElement('input');
    const awayInput = document.createElement('input');
    homeInput.type = "number";
    homeInput.min = 0;
    homeInput.id = `home-input-match-${match.id}`;
    awayInput.type = "number";
    awayInput.min = 0;
    awayInput.id = `away-input-match-${match.id}`;
    if(match.prediction) {
        homeInput.value = match.prediction.home_goals;
        awayInput.value = match.prediction.away_goals;
    }
    if (now >= matchStart) {
        homeInput.disabled = true;
        awayInput.disabled = true;
        homeInput.classList.add("locked");
        awayInput.classList.add("locked");
    }
    homeTd.appendChild(homeInput);
    awayTd.appendChild(awayInput);
    container.appendChild(homeTd);
    container.appendChild(awayTd);
}

function createPredictCell(match) {
    const matchStart = new Date(match.date);
    const now = new Date();
    const td = document.createElement("td");
    const btn = document.createElement("button");
    btn.dataset.type = "predict";
    btn.textContent = "Predict";
    btn.dataset.matchId = match.id;
    if (now >= matchStart) {
        btn.disabled = true;
        btn.hidden = true;
    }
    td.appendChild(btn);
    return td;
}

function setupMatchPrediction(tournamentId){
    document.addEventListener("click", async (e) => {
        if(e.target.dataset.type === "predict") {
            const matchId = e.target.dataset.matchId;

            const prediction = getMatchPrediction(matchId);

            if(!prediction.home_goals || !prediction.away_goals){
                return;
            }

            if(prediction.home_goals < 0 && prediction.away_goals < 0){
                return;
            }

            try { 
                await tournamentAPI.updateWithPath(`${tournamentId}/match/${matchId}/prediction`, prediction);
            }
            catch (err) {
                console.log("ERROR: ", err);
                alert("It couldn't register you into the tournament.");
            }
        }
    })
}

function getMatchPrediction(matchId){
    return {
        home_goals: parseInt(document.getElementById(`home-input-match-${matchId}`).value.trim(), 10),
        away_goals: parseInt(document.getElementById(`away-input-match-${matchId}`).value.trim(), 10)
        };
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
    return register.length === 1;
}

function loadSpecialPredictionForm(tournamentId){
    document.getElementById("prediction-container").hidden = false;
    initTeamSelect(tournamentId);
}

async function initTeamSelect(tournamentId) 
{
    try 
    {
        const teams = await tournamentAPI.fetchByPath(`${tournamentId}/teams`);
        const team_prediction = await tournamentAPI.fetchByPath(`${tournamentId}/prediction`);
        const championSelect = document.getElementById('championIdSelect');

        if(!team_prediction.champion_id){
            const option = document.createElement('option');
            option.textContent = "Select champion";
            option.disabled = true;
            option.selected = true;
            championSelect.appendChild(option);
        }

        teams.forEach(t => 
        {
            const option = document.createElement('option');
            option.value = t.id;
            option.textContent = t.name;

            if(t.id === team_prediction.champion_id){
                option.selected = true;
                option.disabled = true;
            }

            championSelect.appendChild(option);
        });
    } 
    catch (err) 
    {
        console.error('Error cargando equipos:', err.message);
    }
}

function setupSpecialPredictionForm(tournamentId) {
  const form = document.getElementById('predictionForm');
  form.addEventListener('submit', async e => 
  {
        e.preventDefault();
        const prediction = getPredictionFormData(tournamentId);

        if(!prediction.champion_id){
            return;
        }

        if(prediction.champion_id <= 0){
            return;
        }

        try 
        { 
            await tournamentAPI.updateWithPath(`${tournamentId}/prediction`, prediction);
            initTeamSelect(tournamentId);
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
        champion_id: document.getElementById('championIdSelect').value
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
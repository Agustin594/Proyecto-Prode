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

document.addEventListener('DOMContentLoaded', () => 
{
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
    }

    const params = new URLSearchParams(window.location.search);
    const view = params.get('view');

    if (view === 'general') {
        document.getElementById('tournamentListContainer').hidden = false;
        document.getElementById('tournamentLink').classList.add("nav-selected");
    }

    if (view === 'personal') {
        document.getElementById('myTournamentListContainer').hidden = false;
        document.getElementById('myTournamentLink').classList.add("nav-selected");
    }

    if (view === 'create-tournament') {
        document.getElementById('createTournamentListContainer').hidden = false;
        document.getElementById('createTournamentLink').classList.add("nav-selected");
    }

    const tournamentId = params.get("id");

    if (tournamentId) {
        hideHeader();
        showTournamentDetail();
        loadTournamentData(tournamentId);
        loadTournamentUserTable(tournamentId);
        initTournament(tournamentId);
    } else {
        loadUserData();
        setupNavBar();
        setupNavButtons();
        initSelect();
        setupPasswordButton();
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
        setupChampionSelect();
        loadSpecialPredictionForm(tournamentId);
        setupSpecialPredictionForm(tournamentId);
        setupAbandonButton(tournamentId);
        loadTournamentMatchTable(tournamentId);
        setupMatchPrediction(tournamentId);
        initChooseTeamEvents();
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
            option.dataset.imageName = c.image_name;
            competitionSelect.appendChild(option);
        });

        const ts = new TomSelect('#competitionIdSelect', {
            placeholder: 'Choose a competition',
            allowEmptyOption: true,
            valueField: 'value',
            labelField: 'text',
            searchField: 'text',

            render: {
                option: (data, escape) => `
                <div style="display:flex;align-items:center;gap:8px">
                    <img src="image/competitions/${data.imageName}.png" style="width:22px;height:22px">
                    <span>${escape(data.text)}</span>
                </div>
                `,
                item: (data, escape) => `
                <div style="display:flex;align-items:center;gap:8px">
                    <img src="image/competitions/${data.imageName}.png" style="width:20px;height:20px">
                    <span>${escape(data.text)}</span>
                </div>
                `
            }
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

        if(tournament.competition_id == null || tournament.participant_limit == null || tournament.entry_price == null || (tournament.password == null && tournament.public == null)){
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
            img.src = `image/competitions/${t.image_name}.png`;
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
  document.getElementById("tournamentDetail").hidden = true;
}

function showTournamentDetail() {
  document.getElementById("tournament-list").hidden = true;
  document.getElementById("tournamentDetail").hidden = false;
}

async function loadTournamentData(tournamentId) 
{
    try 
    {
        const t = await tournamentAPI.fetchById(tournamentId);

        document.getElementById("tournamentDetail").style.setProperty(
            "--competition-color",
            competitionColors[t.competition_id]
        );
        
        const div = document.getElementById('tournamentData');
        div.replaceChildren();

        const dataContainer = document.createElement("div");
        dataContainer.classList.add("tournament-data-detail");

        const competitionImg = document.createElement("img");
        competitionImg.src = `image/competitions/${t.image_name}.png`

        const trophyImg = document.createElement("img");
        trophyImg.src = `image/competitions/${t.image_name}-trophy.png`
        
        const p = document.createElement('p');

        p.textContent = `Participants: ${t.registered_participants}/${t.participant_limit}`;

        const h3 = document.createElement('h3');

        h3.textContent = t.name;

        dataContainer.appendChild(h3);
        dataContainer.appendChild(p);

        div.appendChild(competitionImg);
        div.appendChild(dataContainer);
        div.appendChild(trophyImg);
        
    } 
    catch (err) 
    {
        console.error('Error cargando inscripciones:', err.message);
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
    }
}


function renderStandingTable(users) 
{
    const div = document.getElementById('userTable');
    div.replaceChildren();

    const header = document.createElement("div");
    header.classList.add("user-table-header");

    const p1 = document.createElement('p');
    const p2 = document.createElement('p');
    const p3 = document.createElement('p');

    p1.textContent = "Pos";
    p2.textContent = "Username";
    p3.textContent = "Points";

    header.appendChild(p1);
    header.appendChild(p2);
    header.appendChild(p3);

    div.appendChild(header);

    let pos = 1;
    users.forEach(u => 
    {
        const user = document.createElement('div');
        user.classList.add("user");

        const p1 = document.createElement('p');
        const p2 = document.createElement('p');
        const p3 = document.createElement('p');

        p1.textContent = pos;
        p2.textContent = u.user_name;
        p3.textContent = u.points;

        user.appendChild(p1);
        user.appendChild(p2);
        user.appendChild(p3);

        if (pos === 1) {
            p1.classList.add("first");

            const spanName = document.createElement("span");
            const spanPlace = document.createElement("span");
            const spanPoints = document.createElement("span");

            spanName.classList.add("name");
            spanPlace.classList.add("place");
            spanPoints.classList.add("points");

            spanName.textContent = u.user_name;
            spanPlace.textContent = pos;
            spanPoints.textContent = `${u.points} pts.`

            document.getElementById("podiumFirstPlace").appendChild(spanName);
            document.getElementById("podiumFirstPlace").appendChild(spanPlace);
            document.getElementById("podiumFirstPlace").appendChild(spanPoints);
        } else if (pos === 2) {
            p1.classList.add("second");

            const spanName = document.createElement("span");
            const spanPlace = document.createElement("span");
            const spanPoints = document.createElement("span");

            spanName.classList.add("name");
            spanPlace.classList.add("place");
            spanPoints.classList.add("points");

            spanName.textContent = u.user_name;
            spanPlace.textContent = pos;
            spanPoints.textContent = `${u.points} pts.`

            document.getElementById("podiumSecondPlace").appendChild(spanName);
            document.getElementById("podiumSecondPlace").appendChild(spanPlace);
            document.getElementById("podiumSecondPlace").appendChild(spanPoints);
        } else if (pos === 3) {
            p1.classList.add("third");

            const spanName = document.createElement("span");
            const spanPlace = document.createElement("span");
            const spanPoints = document.createElement("span");

            spanName.classList.add("name");
            spanPlace.classList.add("place");
            spanPoints.classList.add("points");

            spanName.textContent = u.user_name;
            spanPlace.textContent = pos;
            spanPoints.textContent = `${u.points} pts.`

            document.getElementById("podiumThirdPlace").appendChild(spanName);
            document.getElementById("podiumThirdPlace").appendChild(spanPlace);
            document.getElementById("podiumThirdPlace").appendChild(spanPoints);
        }

        div.appendChild(user);

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
    }
}

function renderMatchTable(matches) 
{
    const matchesList = document.getElementById("matches");
    
    const matchTableHeader = document.createElement('div');
    matchTableHeader.classList.add("match-table-header");

    const prevIcon = document.createElement('i');
    prevIcon.classList.add("fa-solid", "fa-chevron-left");

    const title = document.createElement('p');
    if (matches[0]?.round_name != null) {
        title.textContent = matches[0]?.round_name;
    } else {
        title.textContent = `Fecha ${matches[0]?.round}`
    }
    
    title.dataset.orderIndex = matches[0].order_index;

    const nextIcon = document.createElement('i');
    nextIcon.classList.add("fa-solid", "fa-chevron-right");

    matchTableHeader.appendChild(prevIcon);
    matchTableHeader.appendChild(title);
    matchTableHeader.appendChild(nextIcon);

    const matchTable = document.createElement('div');
    matchTable.classList.add("match-table");
    matchTable .replaceChildren();

    matchesList.appendChild(matchTableHeader);
    matchesList.appendChild(matchTable);

    prevIcon.addEventListener("click", () => {
        const match = getPrevOrderIndex(matches, Number(title.dataset.orderIndex));
        if(match != null) {
            if (match.round_name != null) {
                title.textContent = match.round_name;
            } else {
                title.textContent = `Fecha ${match.round}`
            }
            title.dataset.orderIndex = match.order_index;
            createMatchList(matches, matchTable, Number(title.dataset.orderIndex));
        }
    })

    nextIcon.addEventListener("click", () => {
        const match = getNextOrderIndex(matches, Number(title.dataset.orderIndex));
        if(match != null) {
            if (match.round_name != null) {
                title.textContent = match.round_name;
            } else {
                title.textContent = `Fecha ${match.round}`
            }
            title.dataset.orderIndex = match.order_index;
            createMatchList(matches, matchTable, Number(title.dataset.orderIndex));
        }
    })

    createMatchList(matches, matchTable, Number(title.dataset.orderIndex));
}

function getPrevOrderIndex(matches, currentOrderIndex) {
    let prevOrderIndex = 0;
    let prevMatch;
    matches.forEach(m => {
        if(m.order_index < currentOrderIndex && m.order_index > prevOrderIndex){
            prevOrderIndex = m.order_index;
            prevMatch = m;
        }
    })
    if(prevOrderIndex === 0)
        return null
    else 
        return prevMatch;
}

function getNextOrderIndex(matches, currentOrderIndex) {
    let nextOrderIndex = 5000;
    let nextMatch;
    matches.forEach(m => {
        if(m.order_index > currentOrderIndex && m.order_index < nextOrderIndex){
            nextOrderIndex = m.order_index;
            nextMatch = m;
        }
    })
    if(nextOrderIndex === 5000)
        return null
    else 
        return nextMatch;
}

function createMatchList(matches, container, orderIndex) {
    let lastDate = null;
    container.replaceChildren();
    matches.forEach(m => 
    {
        if(m.order_index === orderIndex){
            if(m.date.split("T")[0] !== lastDate){
                lastDate = m.date.split("T")[0];

                const scheduleDate = document.createElement("div");
                scheduleDate.classList.add("schedule-date");

                const dateP = document.createElement("p");
                dateP.textContent = m.date.split("T")[0];

                scheduleDate.appendChild(dateP);
                container.appendChild(scheduleDate);
            }
            
            // ===== Contenedor data =====
            const scheduleData = document.createElement("div");
            scheduleData.classList.add("schedule-data");
            scheduleData.dataset.type = m.match_type;

            // ===== Partido =====
            const scheduleMatchData = document.createElement("div");
            scheduleMatchData.classList.add("schedule-match-data");

            // Hora
            const hourDiv = document.createElement("div");
            hourDiv.classList.add("hour");

            const hourP = document.createElement("p");
            const fecha = new Date(m.date);

            const hora = fecha.toLocaleTimeString("es-AR", {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            });

            hourP.textContent = hora;

            hourDiv.appendChild(hourP);
            scheduleMatchData.appendChild(hourDiv);

            // ===== Resultado =====
            const scheduleDataResult = document.createElement("div");
            scheduleDataResult.classList.add("schedule-data-result");

            // --- Equipo local ---
            const homeTeam = document.createElement("div");
            homeTeam.classList.add("schedule-home-team");

            const homeImg = document.createElement("img");
            homeImg.setAttribute("src", `image/Logos/${m.home_team_image}.png`);
            homeImg.setAttribute("alt", "");

            const homeName = document.createElement("p");
            homeName.textContent = m.home_team_name;

            homeTeam.appendChild(homeImg);
            homeTeam.appendChild(homeName);

            // --- Resultados ---
            const scheduleResults = document.createElement("div");
            scheduleResults.classList.add("schedule-results");

            // Local
            const homeResult = document.createElement("div");
            homeResult.classList.add("schedule-home-result");

            if(m.penalties_home_goals != null) {
                const penaltiesHomeGoals = document.createElement("p");
                penaltiesHomeGoals.textContent = `(${m.penalties_home_goals})`;
                homeResult.appendChild(penaltiesHomeGoals);
            }

            const homeGoals = document.createElement("p");
            if(m.overtime_home_goals != null)
                homeGoals.textContent = m.home_goals + m.overtime_home_goals;
            else
                homeGoals.textContent = m.home_goals;

            homeResult.appendChild(homeGoals);

            // Predicción
            const predictDiv = document.createElement("div");
            predictDiv.classList.add("schedule-predict");

            const inputHome = document.createElement("input");
            const inputAway = document.createElement("input");
            const matchStart = new Date(m.date);
            const now = new Date();

            inputHome.type = "number";
            inputHome.min = 0;
            inputHome.id = `home-input-match-${m.id}`;
            inputHome.classList.add("home-goals");
            inputHome.dataset.teamId = m.home_team_id;
            inputAway.type = "number";
            inputAway.min = 0;
            inputAway.id = `away-input-match-${m.id}`;
            inputAway.classList.add("away-goals");
            inputAway.dataset.teamId = m.away_team_id;

            if(m.match_type === 'secondleg') {
                inputHome.dataset.firstleg = m.referenced?.home_goals ?? null;
                inputAway.dataset.firstleg = m.referenced?.away_goals ?? null;
            }

            if(m.prediction) {
                inputHome.value = m.prediction.home_goals;
                inputAway.value = m.prediction.away_goals;       
            }
            if (now >= matchStart) {
                inputHome.disabled = true;
                inputAway.disabled = true;
                inputHome.classList.add("locked");
                inputAway.classList.add("locked");
            }
            if (m.match_type === 'secondleg' && m.referenced?.status != 'finished') {
                inputHome.disabled = true;
                inputAway.disabled = true;
                inputHome.classList.add("locked");
                inputAway.classList.add("locked");
            }

            predictDiv.appendChild(inputHome);
            predictDiv.appendChild(inputAway);

            // Visitante
            const awayResult = document.createElement("div");
            awayResult.classList.add("schedule-away-result");

            const awayGoals = document.createElement("p");
            if(m.overtime_away_goals != null)
                awayGoals.textContent = m.away_goals + m.overtime_away_goals;
            else
                awayGoals.textContent = m.away_goals;
            awayResult.appendChild(awayGoals);

            if(m.penalties_away_goals != null) {
                const penaltiesAwayGoals = document.createElement("p");
                penaltiesAwayGoals.textContent = `(${m.penalties_away_goals})`;
                awayResult.appendChild(penaltiesAwayGoals);
            }

            // Armar resultados
            scheduleResults.appendChild(homeResult);
            scheduleResults.appendChild(predictDiv);
            scheduleResults.appendChild(awayResult);

            // --- Equipo visitante ---
            const awayTeam = document.createElement("div");
            awayTeam.classList.add("schedule-away-team");

            const awayName = document.createElement("p");
            awayName.textContent = m.away_team_name;

            const awayImg = document.createElement("img");
            awayImg.setAttribute("src", `image/Logos/${m.away_team_image}.png`);
            awayImg.setAttribute("alt", "");

            awayTeam.appendChild(awayName);
            awayTeam.appendChild(awayImg);

            // Armar data result
            scheduleDataResult.appendChild(homeTeam);
            scheduleDataResult.appendChild(scheduleResults);
            scheduleDataResult.appendChild(awayTeam);

            // Confirmar
            const confirmPredict = document.createElement("div");
            confirmPredict.classList.add("confirm-predict");

            const confirmIcon = document.createElement("i");
            confirmIcon.classList.add("fa-solid", "fa-square-check");

            confirmIcon.dataset.type = "predict";
            confirmIcon.dataset.matchId = m.id;
            if (now >= matchStart) {
                confirmPredict.classList.add("hidden");
            }

            confirmPredict.appendChild(confirmIcon);

            // Armar match
            scheduleMatchData.appendChild(scheduleDataResult);
            scheduleMatchData.appendChild(confirmPredict);

            // ===== Playoff =====
            const playoffPredict = document.createElement("div");
            playoffPredict.classList.add("playoff-predict");
            playoffPredict.classList.add("hidden");

            // Texto
            const predictData = document.createElement("div");
            predictData.classList.add("predict-data");

            const predictMessage = document.createElement("div");
            predictMessage.classList.add("predict-message");

            const predictText = document.createElement("p");
            predictText.textContent = "¿Quién avanzará?";

            predictMessage.appendChild(predictText);

            const predictEdit = document.createElement("div");
            predictEdit.classList.add("predict-edit");

            const editIcon = document.createElement("i");
            editIcon.classList.add("fa-regular", "fa-pen-to-square");

            predictEdit.appendChild(editIcon);

            predictData.appendChild(predictMessage);
            predictData.appendChild(predictEdit);

            // Elegir equipo
            const chooseTeam = document.createElement("div");
            chooseTeam.classList.add("choose-team");

            const homeTeamPredict = document.createElement("div");
            homeTeamPredict.classList.add("home-team-predict");
            homeTeamPredict.dataset.teamId = m.home_team_id;

            const homeTeamImg = document.createElement("img");
            homeTeamImg.setAttribute("src", `image/Logos/${m.home_team_image}.png`);
            homeTeamImg.setAttribute("alt", "");

            homeTeamPredict.appendChild(homeTeamImg);

            const awayTeamPredict = document.createElement("div");
            awayTeamPredict.classList.add("away-team-predict");
            awayTeamPredict.dataset.teamId = m.away_team_id;

            const awayTeamImg2 = document.createElement("img");
            awayTeamImg2.setAttribute("src", `image/Logos/${m.away_team_image}.png`);
            awayTeamImg2.setAttribute("alt", "");

            awayTeamPredict.appendChild(awayTeamImg2);

            chooseTeam.appendChild(homeTeamPredict);
            chooseTeam.appendChild(awayTeamPredict);

            // Armar playoff
            playoffPredict.appendChild(predictData);
            playoffPredict.appendChild(chooseTeam);

            // ===== Final =====
            scheduleData.appendChild(scheduleMatchData);
            scheduleData.appendChild(playoffPredict);
            container.appendChild(scheduleData);

            updateAdvanceVisibility(scheduleData);
        }
    });
}

function updateAdvanceVisibility(matchEl) {
    const type = matchEl.dataset.type;

    const homeInput = matchEl.querySelector('.home-goals');
    const awayInput = matchEl.querySelector('.away-goals');
    const advanceBlock = matchEl.querySelector('.playoff-predict');
    const chooseTeam = matchEl.querySelector('.choose-team');

    clearSelectedTeam(chooseTeam);

    let homeGoals = homeInput.value;
    let awayGoals = awayInput.value;

    if (homeGoals === '' || awayGoals === '') {
        advanceBlock.classList.add('hidden');
        return;
    }

    homeGoals = Number(homeGoals);
    awayGoals = Number(awayGoals);

    let isDraw = false;

    if (type === 'single') {
        isDraw = homeGoals === awayGoals;
    }

    if (type === 'secondleg') {
        const firstHome = Number(homeInput.dataset.firstleg ?? 0);
        const firstAway = Number(awayInput.dataset.firstleg ?? 0);

        const totalHome = homeGoals + firstAway;
        const totalAway = awayGoals + firstHome;

        isDraw = totalHome === totalAway;
    }

    if (isDraw && (type === 'single' || type === 'secondleg')) {
        advanceBlock.classList.remove('hidden');
    } else {
        advanceBlock.classList.add('hidden');
    }
}

document.addEventListener('input', e => {
    if (e.target.classList.contains('home-goals') || e.target.classList.contains('away-goals')) {
        const matchEl = e.target.closest('.schedule-data');
        if (matchEl) {
            updateAdvanceVisibility(matchEl);
        }
    }
});

function setupMatchPrediction(tournamentId){
    document.addEventListener("click", async (e) => {
        if(e.target.dataset.type === "predict") {
            const matchId = e.target.dataset.matchId;
            const matchContainer = e.target.closest(".schedule-data");
            const matchType = matchContainer.dataset.type;
            const prediction = getMatchPrediction(matchId);

            if(prediction.home_goals === null || prediction.away_goals === null){
                return;
            }

            if(prediction.home_goals < 0 || prediction.away_goals < 0){
                return;
            }
            
            if (matchType === 'single') {
                if (prediction.home_goals > prediction.away_goals) {
                    prediction.qualified_team_id = document.getElementById(`home-input-match-${matchId}`).dataset.teamId;
                } else if(prediction.home_goals < prediction.away_goals) {
                    prediction.qualified_team_id = document.getElementById(`away-input-match-${matchId}`).dataset.teamId;
                } else { // draw
                    const div = matchContainer.querySelector(".team-selected");

                    if (div != null && div != undefined) {
                        prediction.qualified_team_id = div.dataset.teamId;
                    }
                }
            } else if (matchType === 'secondleg') {
                const totalHome = prediction.home_goals + Number(document.getElementById(`away-input-match-${matchId}`).dataset.firstleg);
                const totalAway = prediction.away_goals + Number(document.getElementById(`home-input-match-${matchId}`).dataset.firstleg);

                if (totalHome > totalAway) {
                    prediction.qualified_team_id = document.getElementById(`home-input-match-${matchId}`).dataset.teamId;
                } else if(totalHome < totalAway) {
                    prediction.qualified_team_id = document.getElementById(`away-input-match-${matchId}`).dataset.teamId;
                } else {
                    const div = matchContainer.querySelector(".team-selected");

                    if (div != null && div != undefined) {
                        prediction.qualified_team_id = div.dataset.teamId;
                    }
                }
            }
            

            try { 
                await tournamentAPI.updateWithPath(`${tournamentId}/match/${matchId}/prediction`, prediction);
            }
            catch (err) {
                console.log("ERROR: ", err);
                alert("It couldn't register your prediction.");
            }
        }
    })
}

function getMatchPrediction(matchId){
    return {
        home_goals: parseInt(document.getElementById(`home-input-match-${matchId}`).value.trim(), 10),
        away_goals: parseInt(document.getElementById(`away-input-match-${matchId}`).value.trim(), 10),
        qualified_team_id: null
        };
}

function initChooseTeamEvents() {
    document.addEventListener("click", (e) => {
        const teamDiv = e.target.closest(".home-team-predict, .away-team-predict");
        if (!teamDiv) return;

        const chooseTeam = teamDiv.closest(".choose-team");
        if (!chooseTeam) return;

        selectTeam(teamDiv);
    });
}

function selectTeam(teamDiv) {
    const chooseTeam = teamDiv.closest(".choose-team");
    if (!chooseTeam) return;

    const allTeams = chooseTeam.querySelectorAll(
        ".home-team-predict, .away-team-predict"
    );

    allTeams.forEach(team => {
        team.classList.remove("team-selected", "team-unselected");
    });

    allTeams.forEach(team => {
        if (team === teamDiv) {
            team.classList.add("team-selected");
        } else {
            team.classList.add("team-unselected");
        }
    });
}

function clearSelectedTeam(chooseTeam) {
    if (!chooseTeam) return;

    const allTeams = chooseTeam.querySelectorAll(
        ".home-team-predict, .away-team-predict"
    );

    allTeams.forEach(team => {
        team.classList.remove("team-selected", "team-unselected");
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
    document.getElementById("predictionContainer").hidden = false;
    initTeamSelect(tournamentId);
}

async function initTeamSelect(tournamentId) 
{
    try 
    {
        const teams = await tournamentAPI.fetchByPath(`${tournamentId}/teams`);
        const team_prediction = await tournamentAPI.fetchByPath(`${tournamentId}/prediction`);
        const championSelect = document.getElementById('championIdSelect');

        /*if(!team_prediction.champion_id){
            const option = document.createElement('option');
            option.value = '';
            option.textContent = "Choose a team";
            option.disabled = true;
            option.selected = true;
            championSelect.appendChild(option);
        }*/

        teams.forEach(t => 
        {
            const option = document.createElement('option');
            option.value = t.id;
            option.textContent = t.name;
            option.dataset.imageName = t.image_name;

            if(t.id === team_prediction.champion_id){
                option.selected = true;
                option.disabled = true;
            }

            championSelect.appendChild(option);
        });

        const ts = new TomSelect('#championIdSelect', {
            placeholder: 'Choose a team',
            allowEmptyOption: true,
            valueField: 'value',
            labelField: 'text',
            searchField: 'text',

            render: {
                option: (data, escape) => `
                <div style="display:flex;align-items:center;gap:8px">
                    <img src="image/Logos/${data.imageName}.png" style="width:22px;height:22px">
                    <span>${escape(data.text)}</span>
                </div>
                `,
                item: (data, escape) => `
                <div style="display:flex;align-items:center;gap:8px">
                    <img src="image/Logos/${data.imageName}.png" style="width:20px;height:20px">
                    <span>${escape(data.text)}</span>
                </div>
                `
            }
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
            showToast("Champion prediction successfully created.", "success");
        }
        catch (err)
        {
            console.log("ERROR: ", err);
            showToast("Champion prediction couldn't be created.", "error");
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
    const container = document.getElementById("predictionContainer");
    deleteButton(container, tournamentId);
}

function setupRegisterButton(tournamentId){
    const data = document.getElementById("tournamentData");
    const container = document.createElement("div");
    registerButton(container, tournamentId);
    data.appendChild(container);
}

function setupChampionSelect() {
    const wrapper = document.querySelector('.select-wrapper');
    const select = wrapper.querySelector('select');

    select.addEventListener('focus', () => {
        wrapper.classList.add('select-open');
    });

    select.addEventListener('blur', () => {
        wrapper.classList.remove('select-open');
    });
}

function setupPasswordButton() {
    const passwordInput = document.getElementById("tournament-password");
    const togglePassword = document.getElementById("togglePassword");

    togglePassword.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePassword.classList.remove("fa-eye-slash");
            togglePassword.classList.add("fa-eye");
        } else {
            passwordInput.type = "password";
            togglePassword.classList.remove("fa-eye");
            togglePassword.classList.add("fa-eye-slash");
        }
    });
}

function setupNavButtons() {
    const matchLink = document.getElementById("matchLink");
    const tournamentLink = document.getElementById("tournamentLink");
    const myTournamentLink = document.getElementById("myTournamentLink");
    const createTournamentLink = document.getElementById("createTournamentLink");
    const shopLink = document.getElementById("shopLink");

    const createT = document.getElementById("createTournamentListContainer");
    const tournaments = document.getElementById("tournamentListContainer");
    const myTournaments = document.getElementById("myTournamentListContainer");

    tournamentLink.addEventListener("click", () => {
        if(!tournamentLink.classList.contains("nav-selected")) {
            myTournamentLink.classList.remove("nav-selected");
            createTournamentLink.classList.remove("nav-selected");
            shopLink.classList.remove("nav-selected");
            tournamentLink.classList.add("nav-selected");

            createT.hidden = true;
            myTournaments.hidden = true;
            tournaments.hidden = false;
        }
    })

    myTournamentLink.addEventListener("click", () => {
        if(!myTournamentLink.classList.contains("nav-selected")) {
            tournamentLink.classList.remove("nav-selected");
            createTournamentLink.classList.remove("nav-selected");
            shopLink.classList.remove("nav-selected");
            myTournamentLink.classList.add("nav-selected");

            createT.hidden = true;
            myTournaments.hidden = false;
            tournaments.hidden = true;
        }
    })

    createTournamentLink.addEventListener("click", () => {
        if(!createTournamentLink.classList.contains("nav-selected")) {
            myTournamentLink.classList.remove("nav-selected");
            tournamentLink.classList.remove("nav-selected");
            shopLink.classList.remove("nav-selected");
            createTournamentLink.classList.add("nav-selected");

            createT.hidden = false;
            myTournaments.hidden = true;
            tournaments.hidden = true;
        }
    })

    matchLink.addEventListener("click", () => {
        window.location.href = "matches.html";
    })
}

async function loadUserData() {
    try 
    {
        const userData = await tournamentAPI.fetchByPath(`userdata`);
        renderUserData(userData[0]);
    } 
    catch (err) 
    {
        console.error('Error cargando datos del usuario:', err.message);
    }
}

function renderUserData(user) {
    const mainOptions = document.getElementById("mainOptions");
    
    const coinsContainer = document.createElement("div");
    const coins = document.createElement('p');
    coins.textContent = user.coins;
    coinsContainer.appendChild(coins);
    mainOptions.prepend(coinsContainer);

    const nameContainer = document.createElement("div");
    const name = document.createElement('p');
    name.textContent = user.name;
    nameContainer.appendChild(name);
    mainOptions.prepend(nameContainer);
}

function hideHeader() {
    document.querySelector("header").hidden = true;
}

function setupNavBar() {
    const menuBtn = document.getElementById('menuOpener');
    const nav = document.getElementById('navBar');

    menuBtn.addEventListener('click', () => {
        nav.classList.toggle('active');
    });
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
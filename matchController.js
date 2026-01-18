import { matchAPI } from './matchAPI.js';

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
  15: "image/LPF.png",
  16: "image/Brasileirao.png",
  17: "image/Libertadores.png"
};

const competitionCountry = {
  4: "Europa",
  5: "Europa",
  6: "España",
  7: "Mundial",
  8: "Inglaterra",
  9: "Italia",
  10: "Francia",
  11: "Alemania",
  14: "América",
  15: "Argentina",
  16: "Brasil",
  17: "América"
};

let currentDate = new Date();     // fecha seleccionada
let calendarDate = new Date();    // mes que se está viendo

document.addEventListener('DOMContentLoaded', () => 
{
    const token = localStorage.getItem("token")

    if (!token) {
        window.location.href = "login.html"
    }

    const params = new URLSearchParams(window.location.search);

    updateDate();
});

async function loadAllMatchList(date) {
    try {
        const matches = await matchAPI.fetchByPath(`?date=${date}`);
        console.log(matches);
        renderMatchList(matches);
    } catch (err) {
        console.log(err);
    }
}

function renderMatchList(matches) {
    const list = document.getElementById("matchList");
    list.replaceChildren();

    if(matches.length === 0){
        const p = document.createElement("p");
        p.textContent = "There are no matches available.";
        list.appendChild(p);
    } else {

        let lastCompetition = null;
        let currentCompetitionDiv = null;
        matches.forEach(m => {

            if(m.competition_id !== lastCompetition){
                lastCompetition = m.competition_id;

                currentCompetitionDiv = document.createElement("div");
                currentCompetitionDiv.classList.add("competition-matches");
                
                list.appendChild(currentCompetitionDiv);

                const info = document.createElement("div");
                info.classList.add("info");

                currentCompetitionDiv.appendChild(info);

                const containerImg = document.createElement("div");
                containerImg.classList.add("container-img");

                info.appendChild(containerImg);

                const img = document.createElement("img");
                img.src = competitionImage[m.competition_id];
                img.alt = `${m.competition_name} logo`;

                containerImg.appendChild(img);

                const competition = document.createElement("div");
                competition.classList.add("competition");

                info.appendChild(competition);

                const p1 = document.createElement("p");
                const p2 = document.createElement("p");

                p1.textContent = competitionCountry[m.competition_id];
                p2.textContent = m.competition_name;

                competition.appendChild(p1);
                competition.appendChild(p2);
            }

            const match = document.createElement("div");
            match.classList.add("match");

            currentCompetitionDiv.appendChild(match);

            const schedule = document.createElement("div");
            schedule.classList.add("schedule");

            match.appendChild(schedule);

            const p3 = document.createElement("p");
            const p4 = document.createElement("p");
            const fecha = new Date(m.date);

            const hora = fecha.toLocaleTimeString("es-AR", {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            });

            p3.textContent = hora;
            if(m.status === "notstarted")
                p4.textContent = "-"
            else if(m.status === "inprogress") {
                p4.textContent = "-";
                p4.classList.add("in-progress");
            } else
                p4.textContent = m.status;

            schedule.appendChild(p3);
            schedule.appendChild(p4);

            const matchData = document.createElement("div");
            matchData.classList.add("match-data");

            match.appendChild(matchData);

            const teams = document.createElement("div");
            teams.classList.add("teams");

            matchData.appendChild(teams);

            const homeTeam = document.createElement("div");
            homeTeam.classList.add("home-team");

            teams.appendChild(homeTeam);

            const p5 = document.createElement("p");
            p5.textContent = m.home_team_name;

            homeTeam.appendChild(p5);

            const awayTeam = document.createElement("div");
            awayTeam.classList.add("away-team");

            teams.appendChild(awayTeam);

            const p6 = document.createElement("p");
            p6.textContent = m.away_team_name;

            awayTeam.appendChild(p6);

            const result = document.createElement("div");
            result.classList.add("result");

            matchData.appendChild(result);

            const homeGoals = document.createElement("div");
            const awayGoals = document.createElement("div");

            result.appendChild(homeGoals);
            result.appendChild(awayGoals);

            const p7 = document.createElement("p");
            p7.textContent = m.home_goals;
            homeGoals.appendChild(p7);

            const p8 = document.createElement("p");
            p8.textContent = m.away_goals;
            awayGoals.appendChild(p8);

            if(m.status === "inprogress") {
                p7.classList.add("in-progress");
                p8.classList.add("in-progress");
            }

            if(m.home_goals > m.away_goals) {
                p5.classList.add("winner");
                p7.classList.add("winner");
            } else if(m.home_goals < m.away_goals) {
                p6.classList.add("winner");
                p8.classList.add("winner");
            }
        })
    }
}

function renderCalendar() {
    const daysContainer = document.getElementById("calendarDays");
    const title = document.getElementById("calendarTitle");

    daysContainer.innerHTML = "";

    const year = calendarDate.getFullYear();
    const month = calendarDate.getMonth();

    title.textContent = calendarDate.toLocaleDateString("es-AR", {
        month: "long",
        year: "numeric"
    });

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();

    // Espacios vacíos
    for (let i = 0; i < firstDay; i++) {
        const span = document.createElement("span");
        span.classList.add("blank");
        daysContainer.appendChild(span);
    }

    // Días
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const span = document.createElement("span");
        span.textContent = day;

        if (isSameDay(date, today)) {
        span.classList.add("today");
        }

        if (isSameDay(date, currentDate)) {
        span.classList.add("selected");
        }

        span.addEventListener("click", () => {
        currentDate = date;
        closeCalendar();
        updateDate();
        });

        daysContainer.appendChild(span);
    }
}

document.getElementById("prevMonth").onclick = () => {
    calendarDate.setMonth(calendarDate.getMonth() - 1);
    renderCalendar();
};

document.getElementById("nextMonth").onclick = () => {
    calendarDate.setMonth(calendarDate.getMonth() + 1);
    renderCalendar();
};

document.getElementById("prevDay").addEventListener("click", () => {
  currentDate.setDate(currentDate.getDate() - 1);
  updateDate();
});

document.getElementById("nextDay").addEventListener("click", () => {
  currentDate.setDate(currentDate.getDate() + 1);
  updateDate();
});

const modal = document.getElementById("calendarModal");

function openCalendar() {
    calendarDate = new Date(currentDate);
    modal.classList.remove("hidden");
    renderCalendar();
}

function closeCalendar() {
    modal.classList.add("hidden");
}

document.getElementById("todayMatch").onclick = () => {
    currentDate = new Date();
    closeCalendar();
    updateDate();
};

document.getElementById("closeCalendar").onclick = () => {
    closeCalendar();
};

document.getElementById("currentDateLabel").addEventListener("click", openCalendar);

function updateDate() {
    const containerDate = document.getElementById("currentDateLabel");

    const today = new Date();
    const normalize = d => new Date(d.getFullYear(), d.getMonth(), d.getDate());

    const diffDays =
    (normalize(currentDate) - normalize(today)) / (1000 * 60 * 60 * 24);

    if (diffDays === -1) {
        containerDate.textContent = "Ayer";
    } else if (diffDays === 0) {
        containerDate.textContent = "Hoy";
    } else if (diffDays === 1) {
        containerDate.textContent = "Mañana";
    } else {
        containerDate.textContent = formatDate(currentDate);
    }
    loadAllMatchList(formatISO(currentDate));
}

function formatISO(date) {
    return date.toISOString().split("T")[0];
}

function formatDate(date) {
  return date.toLocaleDateString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit"
  });
}

function isSameDay(a, b) {
  return a.getDate() === b.getDate() &&
         a.getMonth() === b.getMonth() &&
         a.getFullYear() === b.getFullYear();
}
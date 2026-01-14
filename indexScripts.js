const track = document.querySelector(".cards");
const prev = document.getElementById("prev");
const next = document.getElementById("next");

let cards = Array.from(track.children);
const cardWidth = cards[0].offsetWidth + 20;

// 👀 cuántas cards entran en el viewport
const viewport = document.querySelector(".cards-viewport");
const visibleCards = Math.round(viewport.offsetWidth / cardWidth);

// 🔁 CLONAMOS las necesarias
for (let i = 0; i < visibleCards; i++) {
  const firstClone = cards[i].cloneNode(true);
  const lastClone = cards[cards.length - 1 - i].cloneNode(true);

  firstClone.classList.add("clone");
  lastClone.classList.add("clone");

  track.appendChild(firstClone);
  track.insertBefore(lastClone, track.firstChild);
}

// Actualizamos lista
cards = Array.from(track.children);

let index = visibleCards;

// Posición inicial
track.style.transform = `translateX(-${index * cardWidth}px)`;

// ▶️ NEXT
next.addEventListener("click", () => {
  index++;
  track.style.transition = "transform 0.4s ease";
  track.style.transform = `translateX(-${index * cardWidth}px)`;
});

// ◀️ PREV
prev.addEventListener("click", () => {
  index--;
  track.style.transition = "transform 0.4s ease";
  track.style.transform = `translateX(-${index * cardWidth}px)`;
});

// 🧠 RESET INVISIBLE
track.addEventListener("transitionend", () => {
  if (index >= cards.length - visibleCards) {
    track.style.transition = "none";
    index = visibleCards;
    track.style.transform = `translateX(-${index * cardWidth}px)`;
  }

  if (index < visibleCards) {
    track.style.transition = "none";
    index = cards.length - visibleCards * 2;
    track.style.transform = `translateX(-${index * cardWidth}px)`;
  }
});
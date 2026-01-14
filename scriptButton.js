const buttonUp = document.getElementById("button-up");

let scrollAnimation = null;

buttonUp.addEventListener("click", () => {
    if (!scrollAnimation) {
        scrollUp();
    }
});

function scrollUp() {
    const currentScroll = document.documentElement.scrollTop;

    if (currentScroll > 5) {
        requestAnimationFrame(scrollUp);
        window.scrollTo(0, currentScroll - currentScroll / 10);
    } else {
        window.scrollTo(0, 0);
    }
}

window.addEventListener("scroll", () => {
    const scroll = document.documentElement.scrollTop;

    if (scroll > 200) {
        buttonUp.style.transform = "scale(1)";
    } else {
        buttonUp.style.transform = "scale(0)";
    }
});
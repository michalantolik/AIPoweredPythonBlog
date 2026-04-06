document.addEventListener("DOMContentLoaded", function () {
    const stage = document.querySelector(".intro-stage");
    const overlay = document.getElementById("introOverlay");

    if (!stage || !overlay) {
        return;
    }

    const introEnabled = stage.dataset.introEnabled === "true";
    const duration = Number(stage.dataset.introDuration || 3200);

    if (!introEnabled) {
        return;
    }

    document.body.classList.add("intro-lock");

    requestAnimationFrame(() => {
        stage.classList.add("intro-active");
    });

    const fadeOutStart = Math.max(duration - 1100, 1400);

    window.setTimeout(() => {
        stage.classList.add("intro-fade-out");
    }, fadeOutStart);

    window.setTimeout(() => {
        stage.classList.remove("intro-active");
        stage.classList.add("intro-complete");
        document.body.classList.remove("intro-lock");
        overlay.setAttribute("hidden", "hidden");
    }, duration);
});

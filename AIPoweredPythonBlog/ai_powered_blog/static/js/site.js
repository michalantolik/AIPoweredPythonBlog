(function () {
    const DEFAULT_DURATION = 3200;
    const MIN_DURATION = 1600;
    const IMAGE_WAIT_TIMEOUT_MS = 1200;
    const FADE_OUT_LEAD_MS = 1100;
    const MIN_VISIBLE_BEFORE_FADE_MS = 1400;

    function completeIntro(stage, overlay) {
        stage.classList.remove("intro-active", "intro-fade-out");
        stage.classList.add("intro-complete");
        document.body.classList.remove("intro-lock");
        overlay.setAttribute("hidden", "hidden");
        overlay.setAttribute("aria-hidden", "true");
    }

    function waitForImage(image, onReady) {
        if (!image) {
            onReady();
            return;
        }

        if (image.complete) {
            onReady();
            return;
        }

        let isResolved = false;

        const resolve = function () {
            if (isResolved) {
                return;
            }

            isResolved = true;
            image.removeEventListener("load", resolve);
            image.removeEventListener("error", resolve);
            onReady();
        };

        image.addEventListener("load", resolve, { once: true });
        image.addEventListener("error", resolve, { once: true });
        window.setTimeout(resolve, IMAGE_WAIT_TIMEOUT_MS);
    }

    function initIntro() {
        const stage = document.querySelector("[data-intro-stage='true']");
        const overlay = document.getElementById("introOverlay");

        if (!stage || !overlay) {
            return;
        }

        if (stage.dataset.introInitialized === "true") {
            return;
        }

        stage.dataset.introInitialized = "true";

        const introEnabled = stage.dataset.introEnabled === "true";
        const isHome = stage.dataset.isHome === "true";
        const duration = Math.max(Number(stage.dataset.introDuration || DEFAULT_DURATION), MIN_DURATION);
        const portrait = overlay.querySelector(".intro-overlay__portrait");
        const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        if (!introEnabled || !isHome || prefersReducedMotion) {
            completeIntro(stage, overlay);
            return;
        }

        document.body.classList.add("intro-lock");
        overlay.removeAttribute("hidden");
        overlay.setAttribute("aria-hidden", "false");

        waitForImage(portrait, function () {
            requestAnimationFrame(function () {
                stage.classList.add("intro-active");
            });

            const fadeOutStart = Math.max(duration - FADE_OUT_LEAD_MS, MIN_VISIBLE_BEFORE_FADE_MS);

            window.setTimeout(function () {
                stage.classList.add("intro-fade-out");
            }, fadeOutStart);

            window.setTimeout(function () {
                completeIntro(stage, overlay);
            }, duration);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initIntro, { once: true });
    } else {
        initIntro();
    }
})();

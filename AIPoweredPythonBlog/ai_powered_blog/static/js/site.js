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

    function normalizeText(value) {
        return (value || "")
            .toLowerCase()
            .replace(/\s+/g, " ")
            .trim();
    }

    function getPostWord(value, singular, plural) {
        return value === 1 ? singular : plural;
    }

    function syncArchiveQueryParam(query) {
        const url = new URL(window.location.href);

        if (query) {
            url.searchParams.set("q", query);
        } else {
            url.searchParams.delete("q");
        }

        window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
    }

    function initPostArchiveFilter() {
        const root = document.querySelector("[data-post-filter='true']");

        if (!root) {
            return;
        }

        const input = root.querySelector("[data-post-filter-input='true']");
        const clearButton = root.querySelector("[data-post-filter-clear='true']");
        const countLabel = root.querySelector("[data-post-filter-count='true']");
        const list = document.querySelector("[data-post-filter-list='true']");
        const emptyState = document.querySelector("[data-post-filter-empty='true']");

        if (!input || !list) {
            return;
        }

        const cards = Array.from(list.querySelectorAll("[data-post-card='true']"));
        const totalPosts = cards.length;

        function render() {
            const query = normalizeText(input.value);
            const tokens = query ? query.split(" ") : [];
            let visibleCount = 0;

            cards.forEach(function (card) {
                const haystack = normalizeText(card.dataset.postSearch);

                const isMatch = !tokens.length || tokens.every(function (token) {
                    return haystack.includes(token);
                });

                card.hidden = !isMatch;

                if (isMatch) {
                    visibleCount += 1;
                }
            });

            if (countLabel) {
                if (query) {
                    countLabel.textContent = `${visibleCount} ${getPostWord(visibleCount, "post", "posts")} match “${input.value.trim()}”.`;
                } else {
                    countLabel.textContent = `Showing ${visibleCount} of ${totalPosts} ${getPostWord(totalPosts, "post", "posts")}.`;
                }
            }

            if (clearButton) {
                clearButton.hidden = !query;
                clearButton.disabled = !query;
            }

            if (emptyState) {
                emptyState.hidden = visibleCount !== 0;
            }

            syncArchiveQueryParam(input.value.trim());
        }

        input.addEventListener("input", render);

        if (clearButton) {
            clearButton.addEventListener("click", function () {
                input.value = "";
                input.focus();
                render();
            });
        }

        render();
    }

    function initSite() {
        initIntro();
        initPostArchiveFilter();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSite, { once: true });
    } else {
        initSite();
    }
})();

document.addEventListener("DOMContentLoaded", () => {
    const copyButtons = document.querySelectorAll("[data-copy-code='true']");

    copyButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const frame = button.closest("[data-copy-frame='true']");
            const source = frame?.querySelector("[data-copy-source='true']");

            if (!source) {
                return;
            }

            const rawText = source.innerText;

            try {
                await navigator.clipboard.writeText(rawText);
                const originalText = button.textContent;
                button.textContent = "Copied";
                window.setTimeout(() => {
                    button.textContent = originalText;
                }, 1600);
            } catch (error) {
                console.error("Copy failed", error);
            }
        });
    });

    if (window.mermaid) {
        window.mermaid.initialize({
            startOnLoad: true,
            securityLevel: "loose",
            theme: "dark",
        });
    }
});

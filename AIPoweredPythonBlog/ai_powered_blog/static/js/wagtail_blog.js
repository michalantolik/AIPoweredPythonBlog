document.addEventListener("DOMContentLoaded", () => {
    setupCopyButtons();
    setupMermaid();
});

function setupCopyButtons() {
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
}

function setupMermaid() {
    if (!window.mermaid) {
        console.error("Mermaid was not loaded.");
        return;
    }

    window.mermaid.initialize({
        startOnLoad: true,
        securityLevel: "loose",
        theme: "base",
        fontFamily: "Inter, Segoe UI, Arial, sans-serif",
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: "basis",
            nodeSpacing: 42,
            rankSpacing: 58,
            padding: 24
        },
        sequence: {
            useMaxWidth: true,
            diagramMarginX: 40,
            diagramMarginY: 20,
            actorMargin: 50,
            messageMargin: 36
        },
        gantt: {
            useMaxWidth: true
        },
        themeVariables: {
            background: "#0b1220",
            mainBkg: "#e8eef8",
            secondBkg: "#dce9fb",
            tertiaryBkg: "#eef4ff",

            primaryColor: "#e8eef8",
            primaryTextColor: "#0f172a",
            primaryBorderColor: "#94a3b8",

            secondaryColor: "#dce9fb",
            secondaryTextColor: "#0f172a",
            secondaryBorderColor: "#7aa2d6",

            tertiaryColor: "#eef4ff",
            tertiaryTextColor: "#0f172a",
            tertiaryBorderColor: "#a5b4c7",

            lineColor: "#9fb0c7",
            defaultLinkColor: "#9fb0c7",
            textColor: "#e5e7eb",
            nodeTextColor: "#0f172a",
            edgeLabelBackground: "#111827",

            clusterBkg: "#111827",
            clusterBorder: "#334155",

            noteBkgColor: "#172133",
            noteBorderColor: "#475569",
            noteTextColor: "#e5e7eb",

            actorBkg: "#e8eef8",
            actorBorder: "#94a3b8",
            actorTextColor: "#0f172a",

            labelBoxBkgColor: "#111827",
            labelBoxBorderColor: "#334155",
            labelTextColor: "#e5e7eb",

            activationBkgColor: "#233047",
            activationBorderColor: "#94a3b8",

            signalColor: "#9fb0c7",
            signalTextColor: "#e5e7eb",

            sequenceNumberColor: "#0f172a"
        }
    });
}

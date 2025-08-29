const addUserForm = document.querySelector(".add-user-form");
// Form input field animations
const formInputs = document.querySelectorAll(".form-input-field");

// Helper function to run the animation
function runAnimation(element, isEntering) {
    if (!element.value) {
        element.animate(
            [
                { 
                    color: isEntering ? "var(--text-unhovered)" : "var(--text-hovered)",
                    borderBottomColor: isEntering ? "var(--text-unhovered)" : "var(--text-hovered)"
                },
                { 
                    color: isEntering ? "var(--text-hovered)" : "var(--text-unhovered)",
                    borderBottomColor: isEntering ? "var(--text-hovered)" : "var(--text-unhovered)"
                }
            ],
            {
                duration: 300,
                easing: "ease",
                fill: "forwards"
            }
        );
    }
}

formInputs.forEach(input => {
    // Mouse hover
    input.addEventListener("mouseenter", () => {
        if (!input.value) {
            runAnimation(input, true);
        }
    });

    input.addEventListener("mouseleave", () => {
        if (!input.value && !input.matches(":focus")) {
            runAnimation(input, false);
        }
    });

    // Focus/blur (click in/out)
    input.addEventListener("focus", () => {
        if (!input.value) {
            runAnimation(input, true);
        }
    });

    input.addEventListener("blur", () => {
        if (!input.value) {
            runAnimation(input, false);
        }
    });
});

// Form button animations
const formBtn = document.querySelector(".form-btn");
formBtn.addEventListener("mouseenter", () => {
    formBtn.animate(
        [
            { color: "var(--text-unhovered)" },
            { color: "var(--text-hovered)" }
        ],
        {
            duration: 300,
            easing: "ease",
            fill: "forwards"
        }
    );
});

formBtn.addEventListener("mouseleave", () => {
    formBtn.animate(
        [
            { color: "var(--text-hovered)" },
            { color: "var(--text-unhovered)" }
        ],
        {
            duration: 300,
            easing: "ease",
            fill: "forwards"
        }
    );
});

// Form divider animations
const formDivider = document.querySelector(".form-devider");
formDivider.addEventListener("mouseenter", () => {
    formDivider.animate(
        [
            { borderBottomColor: "var(--text-unhovered)" },
            { borderBottomColor: "var(--text-hovered)" }
        ],
        {
            duration: 300,
            easing: "ease",
            fill: "forwards"
        }
    );
});

formDivider.addEventListener("mouseleave", () => {
    formDivider.animate(
        [
            { borderBottomColor: "var(--text-hovered)" },
            { borderBottomColor: "var(--text-unhovered)" }
        ],
        {
            duration: 300,
            easing: "ease",
            fill: "forwards"
        }
    );
});

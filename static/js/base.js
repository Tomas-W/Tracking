// Load CSS files progressively
function loadCSS(href) {
    return new Promise((resolve) => {
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = href;
        link.onload = () => resolve();
        document.head.appendChild(link);
    });
}

// Progressive loading sequence
document.addEventListener("DOMContentLoaded", async () => {
    // Show body, header and nav immediately
    document.body.classList.add("loaded");
    document.getElementById("site-header").classList.add("loaded");
    document.getElementById("site-nav").classList.add("loaded");

    // Track which CSS files are already loaded via regular link tags
    const loadedStylesheets = Array.from(document.querySelectorAll("link[rel='stylesheet']"))
        .map(link => link.href);
    
    // Load critical CSS files that are still preloaded but not yet applied
    const criticalStyles = [
        "/static/css/settings.css",
        "/static/css/base.css",
        "/static/css/landing/landing.css"
    ];
    
    // Filter out already loaded stylesheets
    const criticalStylesToLoad = criticalStyles.filter(href => 
        !loadedStylesheets.some(loadedHref => loadedHref.endsWith(href)));
    
    // Load critical CSS files first
    if (criticalStylesToLoad.length > 0) {
        await Promise.all(criticalStylesToLoad.map(href => loadCSS(href)));
    }
    
    // Show about section as soon as its styles are loaded
    // const aboutSection = document.getElementById("about-section");
    // if (aboutSection) {
    //     aboutSection.classList.add("loaded");
    // }

    // Find remaining preloaded styles that need to be loaded
    const remainingStyles = Array.from(document.querySelectorAll("link[rel='preload'][as='style']"))
        .filter(link => !criticalStyles.some(href => link.href.includes(href)));
    
    // Load remaining CSS files without delay, but in parallel
    if (remainingStyles.length > 0) {
        Promise.all(remainingStyles.map(link => loadCSS(link.href)))
            .then(() => {
                // Once all styles are loaded, show all remaining sections
                const sections = Array.from(document.querySelectorAll(".content-section"))
                    .filter(section => section.id !== "about-section");
                
                sections.forEach(section => {
                    section.classList.add("loaded");
                });
            });
    } else {
        // If no remaining preloaded styles, show all sections immediately
        const sections = Array.from(document.querySelectorAll(".content-section"))
            .filter(section => section.id !== "about-section");
        
        sections.forEach(section => {
            section.classList.add("loaded");
        });
    }
});

// Nav hover effects
const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(link => {
    link.addEventListener("mouseenter", () => {
        navLinks.forEach(otherLink => {
            const animation = otherLink.animate(
                [
                    { color: getComputedStyle(otherLink).color },
                    { color: otherLink === link ? "var(--text-hovered)" : "var(--text-unhovered)" }
                ],
                {
                    duration: 400,
                    easing: "ease",
                    fill: "forwards"
                }
            );
        });
    });

    link.addEventListener("mouseleave", () => {
        navLinks.forEach(otherLink => {
            const animation = otherLink.animate(
                [
                    { color: getComputedStyle(otherLink).color },
                    { color: "var(--text-white)" }
                ],
                {
                    duration: 1500,
                    easing: "ease",
                    fill: "forwards"
                }
            );
        });
    });
}); 
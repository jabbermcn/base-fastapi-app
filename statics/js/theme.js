function changeTheme(e) {
    e.preventDefault();
    let currentTheme = localStorage.getItem("theme");

    let theme
    if (currentTheme === null || currentTheme === "dark") {
        theme = "light";
    } else {
        theme = "dark";
    }
    localStorage.setItem("theme", theme)

    if (theme === "dark") {
        document.body.setAttribute("data-bs-theme", theme);
    } else {
        document.body.removeAttribute("data-bs-theme")
    }
}

const settingsButton = document.getElementById("settings");
settingsButton.addEventListener("click", () => {
    const modalLayout = document.querySelector(".modal-layout");
    modalLayout.classList.remove("hidden");
});
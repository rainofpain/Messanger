const settingsButton = document.getElementById("settings");
settingsButton.addEventListener("click", () => {
    const modalLayout = document.querySelector(".modal-layout");
    const settingsModal = modalLayout.querySelector(".settings-modal");
    modalLayout.classList.remove("hidden");
    settingsModal.classList.remove("hidden");
});
const createChatBtn = document.querySelector(".create-chat-btn");
if(createChatBtn){
    createChatBtn.addEventListener("click", () => {
        const modalLayout = document.querySelector(".modal-layout");
        const createChatModal = modalLayout.querySelector(".create-chat-modal");
        modalLayout.classList.remove("hidden");
        createChatModal.classList.remove("hidden");
    
    });
}
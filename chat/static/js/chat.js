const deleteChat = document.getElementById('delete-chat');
const blueTrash = document.getElementById("blue-trash");
const addedChatsContainer = document.querySelector(".added-chats-container");
const searchInput = document.querySelector(".search-input");
const userChatContainerContent = document.querySelector(".user-chat-container-content");
const messageInput= document.getElementById("message_input");
const sendMessageBtn = document.getElementById("send_mesage");
let userChatName = "";
const socketApp = io();

socketApp.on("connect", (data) => {
        console.log("Connected");
    });

sendMessageBtn.addEventListener("click", () => {
    let message = messageInput.value.trim();
    
    if (message && message != "")
    socketApp.emit("send_to_chat", {
        chat: "chat_1",
        message: message
    });
    
    socketApp.on("new_message", (data) => {
        console.log(data.message);
    });
})

if (userChatContainerContent){
    userChatName = userChatContainerContent.dataset.userChatName;
}

if (blueTrash){
    blueTrash.addEventListener("click", () => {
        const deleteChatModal = document.querySelector(".delete-chat");
        const modalLayout = document.querySelector(".modal-layout");
        modalLayout.classList.remove("hidden");
        deleteChatModal.classList.remove("hidden");
    });
}

deleteChat.addEventListener("click", () => {
    fetch("/chat",
        {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "delete-chat" })
        })
        .then(()=> {
            window.location.href = "/authorization";
        }
        );
});

if(addedChatsContainer){
    const chats = JSON.parse(addedChatsContainer.dataset.chats);
    const chatNames = chats.map(chat => chat.name);
    
    searchInput.addEventListener('input', (event) =>{
        addedChatsContainer.innerHTML = "";
        const input_value = event.target.value.trim(); 
        if (input_value != ""){
            chatNames.forEach(chatName => {
                if(chatName.includes(input_value) && chatName[0] === input_value[0] && chatName != userChatName){
                    const chat_container = document.createElement("div");
                    chat_container.classList.add("chat-container");
                    chat_container.innerHTML = `<p>${chatName}</p>`;
                    chat_container.addEventListener("click", () => {
                        socketApp.emit("join", { chat: "chat_1" });
                    });
                    addedChatsContainer.appendChild(chat_container);
                }
            });
        }
    });
    
    const chatContainers = document.querySelectorAll(".chat-container");

    if(chatContainers){
        chatContainers.forEach(chat => {
            chat.addEventListener("click", () =>{
                socketApp.emit("join", { chat: "chat_1" });
            });
        });
    }
}


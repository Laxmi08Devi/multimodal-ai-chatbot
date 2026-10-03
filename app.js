const API_URL = "http://127.0.0.1:8000";


let conversationId = null;


function addMessage(
    message,
    role
) {

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    const div =
        document.createElement(
            "div"
        );

    div.className =
        `message ${role}`;

    div.textContent =
        message;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


async function sendMessage() {

    const input =
        document.getElementById(
            "messageInput"
        );

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    addMessage(
        message,
        "user"
    );

    input.value = "";


    try {

        const response =
            await fetch(
                `${API_URL}/api/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message,
                        conversation_id:
                            conversationId
                    })
                }
            );


        const data =
            await response.json();


        conversationId =
            data.conversation_id;


        addMessage(
            data.answer,
            "assistant"
        );


    } catch (error) {

        addMessage(
            "Unable to connect to the backend.",
            "assistant"
        );

        console.error(error);
    }
}


async function uploadDocument() {

    const input =
        document.getElementById(
            "fileInput"
        );

    if (!input.files.length) {

        alert(
            "Please select a document."
        );

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        input.files[0]
    );


    try {

        const response =
            await fetch(
                `${API_URL}/api/documents/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail ||
                "Upload failed."
            );

            return;
        }


        alert(
            "Document uploaded successfully."
        );


        loadDocuments();


    } catch (error) {

        alert(
            "Unable to upload document."
        );

        console.error(error);
    }
}


async function loadDocuments() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/documents`
            );


        const documents =
            await response.json();


        const container =
            document.getElementById(
                "documents"
            );


        container.innerHTML = "";


        documents.forEach(
            document => {

                const div =
                    document.createElement(
                        "div"
                    );

                div.className =
                    "document-item";

                div.textContent =
                    `${document.filename} (${document.file_type})`;

                container.appendChild(
                    div
                );
            }
        );


    } catch (error) {

        console.error(error);
    }
}


loadDocuments();
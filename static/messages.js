const input =
document.getElementById("messageInput");

const chat =
document.getElementById("chatMessages");

const sendButton =
document.getElementById("sendButton");

/* ================= MESSAGE INPUT ================= */

input.addEventListener("input", function () {

```
if (input.value.trim().length > 0) {

    sendButton.innerHTML = "➤";

} else {

    sendButton.innerHTML = "🎤";

}
```

});

/* ================= ENTER TO SEND ================= */

input.addEventListener("keydown", function (event) {

```
if (event.key === "Enter") {

    event.preventDefault();

    sendMessage();

}
```

});

/* ================= SEND MESSAGE ================= */

function sendMessage() {

```
const text =
    input.value.trim();


if (text === "") {

    startVoiceRecording();

    return;

}


const message =
    document.createElement("div");

message.className =
    "message sent";


const time =
    new Date().toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );


message.innerHTML = `

    <div>
        ${escapeHTML(text)}
    </div>

    <span>
        ${time} ✓✓
    </span>

`;


chat.appendChild(message);


input.value = "";

sendButton.innerHTML = "🎤";


chat.scrollTop =
    chat.scrollHeight;
```

}

/* ================= SECURITY ================= */

function escapeHTML(text) {

```
const div =
    document.createElement("div");

div.textContent = text;

return div.innerHTML;
```

}

/* ================= EMOJI ================= */

function toggleEmoji() {

```
document
    .getElementById("emojiPanel")
    .classList.toggle("show");
```

}

function insertEmoji(emoji) {

```
input.value += emoji;

input.focus();
```

}

/* ================= ATTACHMENT ================= */

function openAttachment() {

```
document
    .getElementById("fileInput")
    .click();
```

}

document
.getElementById("fileInput")
.addEventListener("change", function () {

```
    if (this.files.length > 0) {

        alert(
            this.files.length +
            " file(s) selected"
        );

    }

});
```

/* ================= CAMERA ================= */

function openCamera() {

```
document
    .getElementById("cameraInput")
    .click();
```

}

document
.getElementById("cameraInput")
.addEventListener("change", function () {

```
    if (this.files.length > 0) {

        alert("Photo captured.");

    }

});
```

/* ================= PAYMENT ================= */

function sendPayment() {

```
alert(
    "Payment screen will be connected here."
);
```

}

/* ================= VOICE ================= */

function startVoiceRecording() {

```
if (!navigator.mediaDevices ||
    !navigator.mediaDevices.getUserMedia) {

    alert(
        "Microphone is not supported."
    );

    return;

}


navigator.mediaDevices
    .getUserMedia({
        audio: true
    })

    .then(function (stream) {

        alert(
            "Microphone permission granted."
        );


        stream
            .getTracks()
            .forEach(
                track => track.stop()
            );

    })

    .catch(function () {

        alert(
            "Microphone permission denied."
        );

    });
```

}

/* ================= PHONE CALL ================= */

function makeCall() {

```
window.location.href =
    "tel:+919876543210";
```

}

/* ================= VIDEO CALL ================= */

function startVideoCall() {

```
if (!navigator.mediaDevices ||
    !navigator.mediaDevices.getUserMedia) {

    alert(
        "Camera/microphone is not supported."
    );

    return;

}


navigator.mediaDevices
    .getUserMedia({

        video: true,

        audio: true

    })

    .then(function (stream) {

        alert(
            "Camera and microphone are ready for video calling."
        );


        stream
            .getTracks()
            .forEach(
                track => track.stop()
            );

    })

    .catch(function () {

        alert(
            "Camera or microphone permission denied."
        );

    });
```

}

/* ================= MORE MENU ================= */

function toggleMoreMenu() {

```
document
    .getElementById("moreMenu")
    .classList.toggle("show");
```

}

/* ================= CLEAR CHAT ================= */

function clearChat() {

```
if (
    confirm(
        "Clear all chat messages?"
    )
) {

    chat.innerHTML = `

        <div class="date-label">
            Today
        </div>

    `;

}
```

}

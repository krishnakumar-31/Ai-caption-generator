const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const generateBtn = document.getElementById("generateBtn");
const caption = document.getElementById("caption");

const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");
const dropArea = document.getElementById("dropArea");
const browseBtn = document.getElementById("browseBtn");

const imageInfo = document.getElementById("imageInfo");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");
const resolution = document.getElementById("resolution");
const fileType = document.getElementById("fileType");

const shortCaption=document.getElementById("shortCaption");
const socialCaption=document.getElementById("socialCaption");
const hashtags=document.getElementById("hashtags");
let selectedFile = null;

// ---------------- Preview Image ----------------

imageInput.addEventListener("change", function () {

    selectedFile = this.files[0];

    if (selectedFile) {

        updateImageInfo(selectedFile);

    }

});

function updateImageInfo(file) {

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    fileName.innerText = file.name;

    fileSize.innerText =
        (file.size / 1024).toFixed(2) + " KB";

    fileType.innerText = file.type;

    const img = new Image();

    img.onload = function () {
        resolution.innerText =
            this.width + " × " + this.height;
    };

    img.src = URL.createObjectURL(file);

    imageInfo.style.display = "block";

    caption.innerHTML =
        "<span style='color:#94a3b8'>Image uploaded successfully. Click <b>Generate Caption</b>.</span>";
}

// ---------------- Generate Caption ----------------

generateBtn.addEventListener("click", async function () {

    if (!selectedFile) {
        showToast("Please upload an image first.");
        return;
    }

    caption.innerHTML = `
        <div class="loader"></div>
        <br>
        AI is analyzing your image...
    `;

    generateBtn.disabled = true;

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {

    const response = await fetch(
        "https://ai-caption-generator-49v5.onrender.com/generate",
        {
            method: "POST",
            body: formData
        }
    );

    // Read response as text first
    const text = await response.text();

    console.log("Server Response:", text);

    let data;

    try {
        data = JSON.parse(text);
    } catch (e) {
        throw new Error("Server returned HTML instead of JSON.\n\n" + text);
    }

    if (!response.ok) {
        throw new Error(data.message || "Server Error");
    }

    caption.innerHTML = `
        <strong>Caption</strong><br><br>
        ${data.caption}

        <hr style="margin:20px 0;">

        <strong>Image</strong> : ${data.filename}<br>
        <strong>AI Model</strong> : ${data.model}
    `;

    generateCaptionStyles(data.caption);
    saveHistory(data.caption);

} catch (error) {

    caption.innerHTML = `
        <span style="color:red;white-space:pre-wrap">
            ${error.message}
        </span>
    `;

    console.error(error);

} finally {

    generateBtn.disabled = false;

}

});

// ---------------- Copy ----------------

copyBtn.addEventListener("click", () => {

    navigator.clipboard.writeText(caption.innerText);

    showToast("Caption copied.");

});

// ---------------- Download ----------------

downloadBtn.addEventListener("click", () => {

    const text = caption.innerText;

    const blob = new Blob([text], { type: "text/plain" });

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);

    link.download = "caption.txt";

    link.click();

    showToast("Caption downloaded.");

});

// ---------------- Local History ----------------

function saveHistory(text) {

    let history =
        JSON.parse(localStorage.getItem("captionHistory")) || [];

    history.unshift(text);

    if (history.length > 5)
        history.pop();

    localStorage.setItem(
        "captionHistory",
        JSON.stringify(history)
    );

}

// ---------------- Toast ----------------

function showToast(message) {

    const toast = document.createElement("div");

    toast.className = "toast";

    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}

browseBtn.addEventListener("click", () => {

    imageInput.click();

});

dropArea.addEventListener("click", () => {

    imageInput.click();

});

dropArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    dropArea.classList.add("dragover");

});

dropArea.addEventListener("dragleave", () => {

    dropArea.classList.remove("dragover");

});

dropArea.addEventListener("drop", (e) => {

    e.preventDefault();

    dropArea.classList.remove("dragover");

    selectedFile = e.dataTransfer.files[0];

    imageInput.files = e.dataTransfer.files;

    updateImageInfo(selectedFile);

});

function generateCaptionStyles(text){

    // Short Caption
    let words = text.split(" ");

    shortCaption.innerText =
        words.slice(0,5).join(" ") + "...";

    // Social Media Caption
    socialCaption.innerText =
        text + " 📸✨";

    // Hashtags
    let tags = words
        .filter(word => word.length > 3)
        .map(word => "#" + word.replace(/[^a-zA-Z]/g,"").toLowerCase());

    tags = [...new Set(tags)];

    hashtags.innerText = tags.join(" ");
}
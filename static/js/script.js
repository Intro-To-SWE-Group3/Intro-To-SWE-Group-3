const listingForm = document.getElementById("listingForm");
const statusMessage = document.getElementById("statusMessage");
const submitButton = document.getElementById("submitButton");
const imageInput = document.getElementById("imageFile");
const dropZone = document.getElementById("dropZone");
const dropZonePrompt = document.getElementById("dropZonePrompt");
const imagePreview = document.getElementById("imagePreview");
const removeImageButton = document.getElementById("removeImage");
const descriptionInput = document.getElementById("itemDescription");
const descriptionCount = document.getElementById("descriptionCount");
const categoryPicker = document.querySelector(".category-picker");

function setStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = type ? `is-${type}` : "";
}

function updateDescriptionCount() {
    descriptionCount.textContent = `${descriptionInput.value.length} / ${descriptionInput.maxLength}`;
}

function showPreview(file) {
    if (imagePreview.src) {
        URL.revokeObjectURL(imagePreview.src);
    }

    if (!file) {
        imagePreview.removeAttribute("src");
        imagePreview.hidden = true;
        dropZonePrompt.hidden = false;
        removeImageButton.hidden = true;
        return;
    }

    imagePreview.src = URL.createObjectURL(file);
    imagePreview.hidden = false;
    dropZonePrompt.hidden = true;
    removeImageButton.hidden = false;
    dropZone.classList.remove("is-invalid");
}

function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(new Error("Could not read the selected image."));
        reader.readAsDataURL(file);
    });
}

function validateForm() {
    let firstInvalid = null;

    for (const input of listingForm.querySelectorAll("input[type=text], input[type=number], textarea")) {
        const invalid = !input.value.trim() || !input.checkValidity();
        input.classList.toggle("is-invalid", invalid);
        if (invalid && !firstInvalid) firstInvalid = input;
    }

    const category = listingForm.querySelector("input[name=category]:checked");
    categoryPicker.classList.toggle("is-invalid", !category);
    if (!category && !firstInvalid) firstInvalid = categoryPicker.querySelector("input");

    const hasImage = imageInput.files.length > 0;
    dropZone.classList.toggle("is-invalid", !hasImage);
    if (!hasImage && !firstInvalid) firstInvalid = dropZone;

    if (firstInvalid) {
        firstInvalid.focus?.();
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
        return false;
    }
    return true;
}

descriptionInput.addEventListener("input", updateDescriptionCount);

listingForm.addEventListener("input", (event) => {
    event.target.classList?.remove("is-invalid");
    if (event.target.name === "category") {
        categoryPicker.classList.remove("is-invalid");
    }
});

imageInput.addEventListener("change", () => showPreview(imageInput.files[0]));

removeImageButton.addEventListener("click", () => {
    imageInput.value = "";
    showPreview(null);
});

dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("is-dragging");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("is-dragging"));

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("is-dragging");

    const file = event.dataTransfer.files[0];
    if (!file || !file.type.startsWith("image/")) {
        setStatus("Please drop an image file.", "error");
        return;
    }

    imageInput.files = event.dataTransfer.files;
    showPreview(file);
});

listingForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!validateForm()) {
        setStatus("Please fill in the highlighted fields.", "error");
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Posting...";
    setStatus("");

    try {
        const listing = {
            item_name: document.getElementById("itemName").value.trim(),
            item_description: descriptionInput.value.trim(),
            item_price: Number(document.getElementById("itemPrice").value),
            item_type: listingForm.querySelector("input[name=category]:checked").value,
            seller_id: document.getElementById("sellerID").value.trim(),
            image_data: await readFileAsDataURL(imageInput.files[0])
        };

        const response = await fetch(listingForm.action, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(listing)
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.error || "Failed to create listing.");
        }

        setStatus("Listing posted! Taking you to the homepage...", "success");
        listingForm.reset();
        showPreview(null);
        updateDescriptionCount();
        setTimeout(() => { window.location.href = "/"; }, 1200);
    } catch (error) {
        console.error(error);
        setStatus(error.message || "Could not submit listing.", "error");
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Post Listing";
    }
});

updateDescriptionCount();

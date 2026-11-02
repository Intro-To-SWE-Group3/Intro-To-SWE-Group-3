const listingForm = document.getElementById("listingForm");

listingForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const imageFile = document.getElementById("imageFile").files[0];
    const statusMessage = document.getElementById("statusMessage");

    if (!imageFile) {
        statusMessage.textContent = "Please select an image.";
        statusMessage.style.color = "red";
        return;
    }

    try {
        const imageData = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(new Error("Could not read the selected image."));
            reader.readAsDataURL(imageFile);
        });

        const listing = {
            item_name: document.getElementById("itemName").value,
            item_description: document.getElementById("itemDescription").value,
            item_price: Number(document.getElementById("itemPrice").value),
            item_type: document.getElementById("category").value,
            seller_id: document.getElementById("sellerID").value,
            image_data: imageData
        };

        const response = await fetch(listingForm.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(listing)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Failed to create listing.");
        }

        statusMessage.textContent = "Listing created successfully!";
        statusMessage.style.color = "green";

        listingForm.reset();

    } catch (error) {
        statusMessage.textContent = error.message || "Could not submit listing.";
        statusMessage.style.color = "red";
        console.error(error);
    }
});

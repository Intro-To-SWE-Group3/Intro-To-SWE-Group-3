const listingForm = document.getElementById("listingForm");

listingForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const listing = {
        Item_Name: document.getElementById("itemName").value,
        Item_Description: document.getElementById("itemDescription").value,
        Item_Price: parseFloat(document.getElementById("itemPrice").value),
        Category: document.getElementById("category").value,
        Seller_ID: document.getElementById("sellerID").value,
        Image_URL: document.getElementById("imageURL").value
    };

    const statusMessage = document.getElementById("statusMessage");

    try {
        const response = await fetch("YOUR_API_ENDPOINT_HERE", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(listing)
        });

        if (!response.ok) {
            throw new Error("Failed to create listing.");
        }

        statusMessage.textContent = "Listing created successfully!";
        statusMessage.style.color = "green";

        listingForm.reset();

    } catch (error) {
        statusMessage.textContent =
            "Could not submit listing. Check the server connection.";

        statusMessage.style.color = "red";

        console.error(error);
    }
});

const listingGrid = document.getElementById("listing-grid");

function makeImagePlaceholder() {
    const placeholder = document.createElement("div");
    placeholder.className = "listing-card__image-placeholder";
    placeholder.setAttribute("aria-hidden", "true");
    placeholder.textContent = "📦";
    return placeholder;
}

function makeListingCard(listing) {
    const card = document.createElement("article");
    card.className = "listing-card";

    if (listing.Image_URL) {
        const image = document.createElement("img");
        image.className = "listing-card__image";
        image.src = listing.Image_URL;
        image.alt = listing.Item_Name || "Listing image";
        image.addEventListener("error", () => {
            image.replaceWith(makeImagePlaceholder());
        });
        card.append(image);
    } else {
        card.append(makeImagePlaceholder());
    }

    const body = document.createElement("div");
    body.className = "listing-card__body";

    const category = document.createElement("span");
    category.className = "listing-card__category";
    category.textContent = listing.Item_Type || "Other";

    const title = document.createElement("h3");
    title.textContent = listing.Item_Name || "Untitled listing";

    const description = document.createElement("p");
    description.className = "listing-card__description";
    description.textContent = listing.Item_Description || "";

    const seller = document.createElement("p");
    seller.textContent = `Seller ID: ${listing.Seller_ID || "Unknown"}`;

    const price = document.createElement("p");
    price.className = "listing-card__price";
    price.textContent = `$${listing.Item_Price ?? ""}`;

    body.append(category, title, description, seller, price);
    card.append(body);

    return card;
}

async function loadListings() {
    try {
        const response = await fetch("/listings");

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const listings = await response.json();
        listingGrid.replaceChildren();

        if (!Array.isArray(listings) || listings.length === 0) {
            listingGrid.textContent = "No listings available yet.";
            return;
        }

        for (const listing of listings) {
            listingGrid.append(makeListingCard(listing));
        }
    } catch (error) {
        console.error("Could not load listings:", error);
        listingGrid.textContent = "Could not load listings. Please try again.";
    }
}

loadListings();
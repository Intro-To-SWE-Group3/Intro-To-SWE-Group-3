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

const searchInput = document.getElementById("search-input");
const sortSelect = document.getElementById("sort-listings");
const categoryButtons = document.querySelectorAll(".categories button");

let allListings = [];
let selectedCategory = "All";

function getListingTime(listing, index) {
    const created = Date.parse(listing.Created_At || listing.Date_Created || "");
    // Fall back to database order (later rows are newer) when there is no timestamp column.
    return Number.isNaN(created) ? index : created;
}

function renderListings() {
    const query = searchInput.value.trim().toLowerCase();

    const visible = allListings
        .map((listing, index) => ({ listing, index }))
        .filter(({ listing }) => {
            const category = listing.Item_Type || "Other";
            if (selectedCategory !== "All" && category !== selectedCategory) {
                return false;
            }
            if (!query) {
                return true;
            }
            return [listing.Item_Name, listing.Item_Description, category]
                .some((field) => String(field || "").toLowerCase().includes(query));
        });

    const price = ({ listing }) => Number(listing.Item_Price) || 0;
    const sorters = {
        newest: (a, b) => getListingTime(b.listing, b.index) - getListingTime(a.listing, a.index),
        oldest: (a, b) => getListingTime(a.listing, a.index) - getListingTime(b.listing, b.index),
        "price-asc": (a, b) => price(a) - price(b),
        "price-desc": (a, b) => price(b) - price(a),
    };
    visible.sort(sorters[sortSelect.value] || sorters.newest);

    listingGrid.replaceChildren();

    if (allListings.length === 0) {
        listingGrid.textContent = "No listings available yet.";
        return;
    }

    if (visible.length === 0) {
        const empty = document.createElement("p");
        empty.className = "listing-grid__empty";
        empty.textContent = query
            ? `No listings match "${searchInput.value.trim()}"${selectedCategory !== "All" ? ` in ${selectedCategory}` : ""}.`
            : `No listings in ${selectedCategory} yet.`;
        listingGrid.append(empty);
        return;
    }

    for (const { listing } of visible) {
        listingGrid.append(makeListingCard(listing));
    }
}

async function loadListings() {
    try {
        const response = await fetch("/listings");

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const listings = await response.json();
        allListings = Array.isArray(listings) ? listings : [];
        renderListings();
    } catch (error) {
        console.error("Could not load listings:", error);
        listingGrid.textContent = "Could not load listings. Please try again.";
    }
}

for (const button of categoryButtons) {
    button.addEventListener("click", () => {
        selectedCategory = button.dataset.category;
        for (const other of categoryButtons) {
            const isSelected = other === button;
            other.classList.toggle("selected", isSelected);
            other.setAttribute("aria-pressed", String(isSelected));
        }
        renderListings();
    });
}

searchInput.addEventListener("input", renderListings);
sortSelect.addEventListener("change", renderListings);

loadListings();

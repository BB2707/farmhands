document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('product-grid');
    const loader = document.getElementById('loader');
    const endMessage = document.getElementById('end-message');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');

    const API_URL = 'http://127.0.0.1:5001/get_prices';
    

    let isLoading = false;
    let noMoreData = false;
    let allProducts = []; // store all products
    let filteredProducts = []; // filtered list for search

    // --- Fetch Products from API ---
    const fetchProducts = async () => {
        if (isLoading || noMoreData) return;
        isLoading = true;
        loader.style.display = 'flex';

        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Network response was not ok');
            }
            const products = await response.json();

            if (products.length === 0) {
                noMoreData = true;
                endMessage.style.display = 'block';
            } else {
                allProducts = products;
                filteredProducts = products;
                renderProducts(filteredProducts);
            }
        } catch (error) {
            console.error('Failed to fetch products:', error);
            loader.innerHTML = `<p>Error: ${error.message}. Please check if the server is running.</p>`;
        } finally {
            loader.style.display = 'none';
            isLoading = false;
        }
    };

    // --- Render Product Cards ---
    const renderProducts = (products) => {
        productGrid.innerHTML = ''; // clear grid
        if (products.length === 0) {
            productGrid.innerHTML = '<p>No products found.</p>';
            return;
        }

        products.forEach(product => {
            const card = createProductCard(product);
            productGrid.appendChild(card);
        });
    };

    // --- Create Product Card ---
    const createProductCard = (product) => {
        const card = document.createElement('div');
        card.className = 'product-card';

        card.innerHTML = `
            <img src="${product.image_url || 'https://placehold.co/600x400?text=No+Image'}" 
                 alt="${product.commodity}" class="product-image">
            <div class="product-info">
                <h3 class="product-title">${product.commodity || 'Unknown Commodity'}</h3>
                <p class="product-description">${product.state || 'Unknown State'}</p>
                <div class="product-meta">
                    <span class="product-market">📍 ${product.market || 'Unknown Market'}</span>
                    <span class="product-price">${product.modal_price || '₹N/A'}</span>
                </div>
            </div>
        `;
        return card;
    };

    // --- Search Functionality ---
    const handleSearch = () => {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {
            renderProducts(allProducts);
            return;
        }

        filteredProducts = allProducts.filter(p =>
            (p.commodity && p.commodity.toLowerCase().includes(query)) ||
            (p.market && p.market.toLowerCase().includes(query)) ||
            (p.state && p.state.toLowerCase().includes(query))
        );

        renderProducts(filteredProducts);
    };

    // --- Infinite Scroll (optional if you want to keep it) ---
    const handleScroll = () => {
        const mainContent = document.querySelector('.content-scrollable');
        const { scrollTop, scrollHeight, clientHeight } = mainContent;
        if (clientHeight + scrollTop >= scrollHeight - 300) {
            fetchProducts();
        }
    };

    // --- Event Listeners ---
    document.querySelector('.content-scrollable').addEventListener('scroll', handleScroll);
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keyup', e => {
        if (e.key === 'Enter') handleSearch();
    });

    // --- Initial Load ---
    fetchProducts();
});

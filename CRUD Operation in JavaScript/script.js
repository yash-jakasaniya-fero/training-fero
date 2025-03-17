document.addEventListener("DOMContentLoaded", function () {
    let productList = JSON.parse(localStorage.getItem("products")) || [];
    let sortStates = { id: false, price: false, name: false };
    let editIndex = null;

    function generateID() {
        if (productList.length === 0) return 1;
        return Math.max(...productList.map(product => product.id)) + 1;
    }

    function displayProducts(filteredList = null) {
        const tableBody = document.querySelector("#displayTable tbody");
        tableBody.innerHTML = "";

        const productsToDisplay = filteredList || productList;

        productsToDisplay.forEach((product, index) => {
            let row = document.createElement("tr");
            row.setAttribute("data-index", index);
            row.innerHTML = `
                <td>${index + 1}</td>
                <td class="product-name">${product.name}</td>
                <td class="product-description">${product.description}</td>
                <td class="product-price">${product.price}</td>
                <td><img class="product-image" src="${product.image}" alt="Product Image" width="100"></td>
                <td>
                    <button class="btn btn-success btn-sm" onclick="viewProduct(${index})">View</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteProduct(${index})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    document.getElementById("productForm").addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("productName").value;
        const description = document.getElementById("productDescription").value;
        const price = parseFloat(document.getElementById("productPrice").value).toFixed(2);
        const imageFile = document.getElementById("productImage").files[0];

        if (!name || !description || !price) {
            alert("All fields are required!");
            return;
        }

        const reader = new FileReader();
        reader.onload = function () {
            const imageBase64 = reader.result;

            if (editIndex === null) {
                const newProduct = { id: generateID(), name, description, price, image: imageBase64 };
                productList.push(newProduct);
            } else {
                productList[editIndex].name = name;
                productList[editIndex].description = description;
                productList[editIndex].price = price;
                if (imageFile) {
                    productList[editIndex].image = imageBase64;
                }
            }

            localStorage.setItem("products", JSON.stringify(productList));
            displayProducts();
            bootstrap.Modal.getInstance(document.getElementById("productAdd")).hide();
            resetForm();
        };

        if (imageFile) {
            reader.readAsDataURL(imageFile);
        } else {
            localStorage.setItem("products", JSON.stringify(productList));
            displayProducts();
            bootstrap.Modal.getInstance(document.getElementById("productAdd")).hide();
            resetForm();
        }
    });

    function resetForm() {
        document.getElementById("productForm").reset();
        document.getElementById("previewImage").src = "";
        document.getElementById("previewImage").classList.add("d-none");
        editIndex = null;
        document.getElementById("productAddLabel").textContent = "Add Product";
        document.getElementById("saveProductButton").textContent = "Save Product";
    }

    function updateTableRow(index) {
        let row = document.querySelector(`[data-index='${index}']`);
        if (row) {
            row.querySelector(".product-name").textContent = productList[index].name;
            row.querySelector(".product-description").textContent = productList[index].description;
            row.querySelector(".product-price").textContent = productList[index].price;
            row.querySelector(".product-image").src = productList[index].image;
        }
    }

    window.viewProduct = function (index) {
        const product = productList[index];
        editIndex = index;

        document.getElementById("productName").value = product.name;
        document.getElementById("productDescription").value = product.description;
        document.getElementById("productPrice").value = product.price;
        document.getElementById("previewImage").src = product.image;
        document.getElementById("previewImage").classList.remove("d-none");
        document.getElementById("productImage").value = "";

        document.getElementById("productAddLabel").textContent = "Edit Product";
        document.getElementById("saveProductButton").textContent = "Update Product";

        document.getElementById("productName").addEventListener("input", function () {
            productList[editIndex].name = this.value;
            updateTableRow(editIndex);
            localStorage.setItem("products", JSON.stringify(productList));
        });

        document.getElementById("productDescription").addEventListener("input", function () {
            productList[editIndex].description = this.value;
            updateTableRow(editIndex);
            localStorage.setItem("products", JSON.stringify(productList));
        });

        document.getElementById("productPrice").addEventListener("input", function () {
            productList[editIndex].price = parseFloat(this.value).toFixed(2)
            updateTableRow(editIndex);
            localStorage.setItem("products", JSON.stringify(productList));
        });

        new bootstrap.Modal(document.getElementById("productAdd")).show();
    };

    window.deleteProduct = function (index) {
        if (confirm("Are you sure you want to delete this product?")) {
            productList.splice(index, 1);
            localStorage.setItem("products", JSON.stringify(productList));
            displayProducts();
        }
    };

    window.clearList = function () {
        if (confirm("Are you sure you want to delete all products?")) {
            productList = [];
            localStorage.setItem("products", JSON.stringify(productList));
            displayProducts();
        }
    };

    window.searchProduct = function () {
        const searchTerm = document.getElementById("searchInput").value.toLowerCase();
        const filteredProducts = productList.filter(product =>product.name.toLowerCase().includes(searchTerm)
        );

        if (!searchTerm) {
            displayProducts();
        } else {
            displayProducts(filteredProducts);
        }
    };

    window.sortTable = function (column) {
        if (column === "id") {
            productList.sort((a, b) => sortStates.id ? a.id - b.id : b.id - a.id);
            sortStates.id = !sortStates.id;
        } else if (column === "price") {
            productList.sort((a, b) => sortStates.price ? a.price - b.price : b.price - a.price);
            sortStates.price = !sortStates.price;
        } else if (column === "name") {
            productList.sort((a, b) => sortStates.name ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name));
            sortStates.name = !sortStates.name;
        }

        displayProducts();
    };

    displayProducts();
});

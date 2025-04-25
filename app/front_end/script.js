const apiUrl = "http://127.0.0.1:8000";

document.getElementById("shoeForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        nome: document.getElementById("nome").value,
        preco: parseFloat(document.getElementById("preco").value),
        descricao: document.getElementById("descricao").value,
        quantidade: parseInt(document.getElementById("quantidade").value),
    };

    const response = await fetch(`${apiUrl}/insert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert("Tênis cadastrado com sucesso!");
        listarTenis();
    } else {
        alert("Erro ao cadastrar tênis.");
    }
});

async function listarTenis() {
    const response = await fetch(`${apiUrl}/qtd_shoes`);
    const tenis = await response.json();

    const lista = document.getElementById("shoeList");
    lista.innerHTML = "";

    tenis.forEach(shoe => {
        const item = document.createElement("li");
        item.textContent = `${shoe.nome} - R$${shoe.preco} (${shoe.quantidade} unidades)`;
        lista.appendChild(item);
    });
}

// Chama automaticamente ao carregar a página
listarTenis();

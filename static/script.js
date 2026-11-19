const btnBuscar = document.getElementById("btnBuscar");
const textarea = document.getElementById("empresas");
const statusEl = document.getElementById("status");
const resultadosCard = document.getElementById("resultadosCard");
const tabelaBody = document.querySelector("#tabelaResultados tbody");

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.classList.toggle("erro", isError);
}

function limparResultados() {
  tabelaBody.innerHTML = "";
  resultadosCard.hidden = true;
}

function renderResultados(resultados) {
  tabelaBody.innerHTML = "";

  resultados.forEach((r, i) => {
    const tr = document.createElement("tr");

    const tdIdx = document.createElement("td");
    tdIdx.textContent = i + 1;

    const tdEmpresa = document.createElement("td");
    tdEmpresa.textContent = r.empresa;

    const tdCnpj = document.createElement("td");
    if (r.cnpj) {
      tdCnpj.textContent = r.cnpj;
      tdCnpj.classList.add("cnpj-ok");
    } else {
      tdCnpj.textContent = r.erro || "Não encontrado";
      tdCnpj.classList.add("cnpj-erro");
    }

    const tdLink = document.createElement("td");
    if (r.link) {
      const a = document.createElement("a");
      a.href = r.link;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = r.link;
      tdLink.appendChild(a);
    } else {
      tdLink.textContent = "-";
    }

    tr.appendChild(tdIdx);
    tr.appendChild(tdEmpresa);
    tr.appendChild(tdCnpj);
    tr.appendChild(tdLink);
    tabelaBody.appendChild(tr);
  });

  resultadosCard.hidden = resultados.length === 0;
}

async function buscarCnpjs() {
  const linhas = textarea.value
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);

  if (linhas.length === 0) {
    setStatus("Digite ao menos um nome de empresa.", true);
    return;
  }

  btnBuscar.disabled = true;
  limparResultados();
  setStatus(`Buscando ${linhas.length} empresa(s)... isso pode levar alguns segundos.`);

  try {
    const resp = await fetch("/api/buscar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ empresas: linhas }),
    });

    const data = await resp.json();

    if (!resp.ok) {
      setStatus(data.error || "Erro ao buscar.", true);
      return;
    }

    renderResultados(data.resultados);
    setStatus(`Concluído: ${data.resultados.length} empresa(s) processada(s).`);
  } catch (err) {
    setStatus("Erro de conexão com o servidor: " + err.message, true);
  } finally {
    btnBuscar.disabled = false;
  }
}

btnBuscar.addEventListener("click", buscarCnpjs);

document.addEventListener("DOMContentLoaded", () => {
    fetch("../papers.json") // 
        .then(response => {
            if (!response.ok) throw new Error("Failed to load papers.json");
            return response.json();
        })
        .then(papers => {
            const list = document.getElementById("papers-list");
            papers.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
          <b><a href="${p.inspire}" target="_blank">${p.title}</a></b><br>
          [<a href="${p.arxiv}" target="_blank">${p.arxiv.split('/abs/')[1]}</a> /
          <b>${p.journal}</b>]<br>
          ${p.authors}
        `;
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Error loading papers:", err);
            const list = document.getElementById("papers-list");
            list.innerHTML = "<li>Failed to load papers.</li>";
        });
});
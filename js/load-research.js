
// Paper List
document.addEventListener("DOMContentLoaded", () => {
    fetch("../JSON/papers.json") // 
        .then(response => {
            if (!response.ok) throw new Error("Failed to load papers.json");
            return response.json();
        })
        .then(papers => {
            const list = document.getElementById("papers-list");
            papers.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
          <b><a href="https://inspirehep.net/literature/${p.inspire}" target="_blank">${p.title}</a></b><br>
          [<a href="https://arxiv.org/abs/${p.arxiv}" target="_blank">${p.arxiv}</a> /
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


// International Talk
document.addEventListener("DOMContentLoaded", () => {
    fetch("../JSON/pres_int.json")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("pre_int-list");
            data.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
        <font color="teal"><b>${p.conference}</b></font>
        ${p.link ? `<a href="${p.link}" target="_blank"><i class="fas fa-globe-asia"></i></a>` : ""}
        ${p.pdf ? `<a href="${p.pdf}" target="_blank"><i class="far fa-file-pdf"></i></a>` : ""}
        <br>${p.date} @ ${p.place}<br>
        "${p.title}"<br>
      `;
                list.appendChild(li);
            });
        });
});

// Japanese Talk
document.addEventListener("DOMContentLoaded", () => {
    fetch("../JSON/pres_jap.json")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("pre_jap-list");
            data.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
        <font color="teal"><b>${p.conference}</b></font>
        ${p.link ? `<a href="${p.link}" target="_blank"><i class="fas fa-globe-asia"></i></a>` : ""}
        ${p.pdf ? `<a href="${p.pdf}" target="_blank"><i class="far fa-file-pdf"></i></a>` : ""}
        <br>${p.date} @ ${p.place}<br>
        "${p.title}"<br>
      `;
                list.appendChild(li);
            });
        });
});

// Poster Talk
document.addEventListener("DOMContentLoaded", () => {
    fetch("../JSON/pres_pos.json")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("pre_pos-list");
            data.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
        <font color="teal"><b>${p.conference}</b></font>
        ${p.link ? `<a href="${p.link}" target="_blank"><i class="fas fa-globe-asia"></i></a>` : ""}
        ${p.pdf ? `<a href="${p.pdf}" target="_blank"><i class="far fa-file-pdf"></i></a>` : ""}
        <br>${p.date} @ ${p.place}<br>
        "${p.title}"<br>
      `;
                list.appendChild(li);
            });
        });
});

// Seminar Talk
document.addEventListener("DOMContentLoaded", () => {
    fetch("../JSON/seminars.json") // 
        .then(response => {
            if (!response.ok) throw new Error("Failed to load seminars.json");
            return response.json();
        })
        .then(seminars => {
            const list = document.getElementById("seminars-list");
            seminars.forEach(p => {
                const li = document.createElement("li");
                li.innerHTML = `
                <font color="teal"><b>${p.type}</b></font>
                <br>
                ${p.date}, ${p.place}<br>
                "${p.title}"
        `;
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Error loading seminars:", err);
            const list = document.getElementById("seminars-list");
            list.innerHTML = "<li>Failed to load seminars.</li>";
        });
});
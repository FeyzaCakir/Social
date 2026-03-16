// Sayfa yüklendiğinde çalışır
window.addEventListener("DOMContentLoaded", () => {
    checkAuth();
    loadPosts();
});
// -----------------------------------------
// 1) Kullanıcı giriş yapmış mı kontrol et
// -----------------------------------------
function checkAuth() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Lütfen giriş yapın.");
        window.location.href = "/login";
        return;
    }
}
// -----------------------------------------
// 2) Gönderileri API'den çek ve ekranda listele
// -----------------------------------------
async function loadPosts() {
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/posts/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        alert("Gönderiler alınamadı.");
        return;
    }

    const posts = await response.json();
    displayPosts(posts);
    const postContainer = document.getElementById("postContainer");
    postContainer.innerHTML = ""; // Önce temizle
    posts.forEach(post => {
    postContainer.innerHTML += `
      <div class="post">
        <h3>${post.title}</h3>
        <p>${post.content}</p>
        <small><strong>Gönderen:</strong> ${post.owner.username}</small>
        <button onclick="deletePost(${post.id})">Sil</button>
      </div>
    `;
  });  
}
// -----------------------------------------
// 3) Gönderileri HTML'de göster
// -----------------------------------------
function displayPosts(posts) {
    const container = document.getElementById("post-container");
    container.innerHTML = "";

    posts.forEach(post => {
        const card = document.createElement("div");
        card.classList.add("post-card");

        card.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>

            ${post.media_url ? `<img src="${post.media_url}" class="post-image" />` : ""}

            <button class="delete-btn" data-id="${post.id}">Sil</button>
        `;

        container.appendChild(card);
    });

    // Silme butonlarını aktif et
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            await deletePost(id);
        });
    });
}
// -----------------------------------------
// 4) Yeni gönderi ekleme (POST)
// -----------------------------------------
document.getElementById("post-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const media_url = document.getElementById("media_url").value;

    const response = await fetch("http://localhost:8000/posts/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, content, media_url })
    });

    if (response.ok) {
        alert("Gönderi başarıyla paylaşıldı!");
        loadPosts();
        document.getElementById("post-form").reset();
    } else {
        alert("Gönderi eklenemedi.");
    }
});
// -----------------------------------------
// 5) Gönderi silme (DELETE)
// -----------------------------------------
async function deletePost(id) {
    const token = localStorage.getItem("token");

    const response = await fetch(`http://localhost:8000/posts/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert("Gönderi silindi!");
        loadPosts();
    } else {
        alert("Silme işlemi başarısız.");
    }
}
// -----------------------------------------
// 6) Dosya yükleme
// -----------------------------------------
document.getElementById("post-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");

    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const fileInput = document.getElementById("media_file");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);

    if (file) {
        formData.append("media_file", file);  
    }

    const response = await fetch("http://localhost:8000/posts", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
            // ❌ Content-Type EKLEME — FormData kendi belirler
        },
        body: formData
    });

    if (response.ok) {
        alert("Gönderi başarıyla paylaşıldı!");
        loadPosts();
        document.getElementById("post-form").reset();
    } else {
        alert("Gönderi eklenemedi.");
    }
});

let mediaHTML = "";
if (post.media_url) {
    if (post.media_url.endsWith(".mp4") || post.media_url.endsWith(".mov")) {
        mediaHTML = `<video src="${post.media_url}" class="post-video" controls></video>`;
    } else {
        mediaHTML = `<img src="${post.media_url}" class="post-image" />`;
    }
}

card.innerHTML = `
    <h3>${post.title}</h3>
    <p>${post.content}</p>
    ${mediaHTML}
    <button class="delete-btn" data-id="${post.id}">Sil</button>
`;






// -----------------------------------------
// 7) Çıkış yap
// -----------------------------------------
document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
});

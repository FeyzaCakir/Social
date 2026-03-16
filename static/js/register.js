console.log("REGISTER JS ÇALIŞIYOR");
document.getElementById("register-form").addEventListener("submit", async (e)=>{
e.preventDefault(); //sayfanın yenilenmesini engeller

const username= document.getElementById("username").value;
const email= document.getElementById("email").value;
const password= document.getElementById("password").value;

const response= await fetch("/register",{
    method:"POST",
    headers:{"Content-Type": "application/json"},
    body: JSON.stringify({username,email,password}),
});

if (response.ok){
    alert("Kayıt Başarılı! Giriş sayfasına yönlendiriliyorsunuz...");
    window.location.href="/login";
} else{
    alert("Kayıt Başarısız. Lütfen tekrar deneyin.");
}
});
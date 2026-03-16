console.log("LOGIN JS ÇALIŞIYOR");
document.getElementById("login-form").addEventListener("submit",async (e)=>{
    e.preventDefault();

    const email= document.getElementById("email").value;
    const password= document.getElementById("password").value;

    const response= await fetch("/login",{
        method:"POST",
        headers:{"Content-Type":  "application/json"},
        body:JSON.stringify({email,password}),
    });
    
    if (response.ok){
        const data= await response.json();
        localStorage.setItem("token",data.access_token);
        localStorage.setItem("user_id",data.user_id);
        window.location.href= "/dashboard";
    } else{
        alert("Giriş Başarısız.Email veya şifre hatalı.");
    }
});
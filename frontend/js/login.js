const form = document.querySelector("#login-form");

let accessToken = null;

const handleSubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const newPassword = sha256(formData.get("password"));
  formData.set("password", newPassword);

    const res = await fetch("/login", {
        method: "post",
        body: formData,
    });

    const data = await res.json();
    accessToken = data.access_token;

    const infoDiv = document.querySelector("#login-info");
    infoDiv.innerText = "로그인 되었습니다.";

    window.location.pathname = "/";

    // const btn = document.createElement("button");
    // btn.innerText = "상품 가져오기!";
    // btn.addEventListener("click", async () => {
    //   const res = await fetch("http://127.0.0.1:8000/items", {
    //     headers: {
    //       "Authorization": `Bearer ${accessToken}`,
    //       "Content-Type": "application/json"
    //     },
    //   });
    //   const data = await res.json(); 
    //   console.log(data);
    // })
    // infoDiv.appendChild(btn);
};

form.addEventListener("submit", handleSubmit); 

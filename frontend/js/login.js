const form = document.querySelector("#login-form");

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

    const accessToken = data.access_token;
    window.localStorage.setItem('token', accessToken);
    if (res.status === 200) {
      alert("로그인에 성공했습니다!");
      window.location.pathname = "/index.html";
    } else {
        alert("로그인에 실패했습니다!");
    }

};

form.addEventListener("submit", handleSubmit);

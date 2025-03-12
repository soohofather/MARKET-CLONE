const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password = formData.get("password");
  const password2 = formData.get("password2");
  if (password === password2) {
    return true;
  } else {
    return false;
  }
};

const handleSubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const newPassword = sha256(formData.get("password"));
  formData.set("password", newPassword);

  const div = document.querySelector("#password-info");

  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });

    const data = await res.json();

    if (data === "200") {
      //   div.innerText = "회원가입에 성공했습니다!";
      //   div.style.color = "blue";
      alert("회원가입에 성공했습니다!");
      window.location.pathname = "/login.html";
    } else {
      div.innerText = "회원가입에 실패했습니다.";
      div.style.color = "red";
    }
  } else {
    div.innerText = "비밀번호와 비밀번호 확인이 다릅니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);

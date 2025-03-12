const form = document.getElementById("write-form");

const handleSubmitForm = async (e) => {
  e.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());
  try {
    const res = await fetch("http://127.0.0.1:8000/items", {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
      body,
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/index.html";
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);

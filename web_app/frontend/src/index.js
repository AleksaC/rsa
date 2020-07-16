import "../style/index.css";

function prettify(key) {
  return key
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function submitForm(e) {
  e.preventDefault();

  const submitButton = e.target.querySelector("input[type=submit]");
  submitButton.disabled = true;

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData);
  const params = new URLSearchParams(data);

  fetch(`${e.target.action}?${params.toString()}`)
    .then((resp) => {
      if (resp.ok) {
        e.target.reset();
      }
      return resp.json();
    })
    .then((json) => {
      const res = e.target.querySelector(".result");
      res.innerText = "";
      for (const [key, value] of Object.entries(json)) {
        res.innerText += `${res.innerText === "" ? "" : "\n"}${prettify(
          key
        )}: ${value}\n`;
      }
    })
    .catch((err) => {
      alert(err.message);
    })
    .finally(() => (submitButton.disabled = false));
}

for (const form of document.querySelectorAll("form")) {
  form.addEventListener("submit", submitForm);
}

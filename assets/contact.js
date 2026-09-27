// Contact page behavior. Without JavaScript the form still posts straight to Formspree.
(function () {
  // Preselect the topic from links like /contact?topic=starter-kit
  var topic = new URLSearchParams(window.location.search).get("topic");
  var select = document.getElementById("topic");
  if (topic && select) {
    for (var i = 0; i < select.options.length; i++) {
      if (select.options[i].value === topic) { select.selectedIndex = i; break; }
    }
  }

  // Submit in place and show the result on this page
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (!form || !status || !window.fetch) return;
  var button = form.querySelector('button[type="submit"]');

  function show(message, kind) {
    status.textContent = message;
    status.className = "form-status " + kind;
    status.hidden = false;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    button.disabled = true;
    button.textContent = "Sending…";
    status.hidden = true;

    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    })
      .then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          if (response.ok) {
            form.reset();
            show("Thanks, your message was sent. We typically respond within one business day.", "ok");
          } else {
            var detail = data && data.errors && data.errors.length
              ? data.errors.map(function (e) {
                  var m = String(e.message || "").trim();
                  var label = e.field ? e.field.charAt(0).toUpperCase() + e.field.slice(1) + " " : "";
                  m = label ? label + m : m.charAt(0).toUpperCase() + m.slice(1);
                  return /[.!?]$/.test(m) ? m : m + ".";
                }).join(" ")
              : "";
            show("Your message wasn't sent. " + (detail || "Please check the fields and try again.") +
                 " You can also email consultations@vigilantcybersecurity.net.", "err");
          }
        });
      })
      .catch(function () {
        show("Your message wasn't sent because the connection failed. Please try again, or email consultations@vigilantcybersecurity.net.", "err");
      })
      .then(function () {
        button.disabled = false;
        button.textContent = "Send";
      });
  });
})();

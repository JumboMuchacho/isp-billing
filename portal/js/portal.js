async function loadPackages() {
  const select = document.querySelector("#package");
  if (!select) return;
  try {
    const response = await fetch("/packages/");
    const packages = await response.json();
    select.innerHTML = packages
      .map(
        (pkg) =>
          `<option value="${pkg.id}" data-price="${pkg.price}">${pkg.name} - KES ${pkg.price}</option>`
      )
      .join("");
    const amount = document.querySelector("#amount");
    if (amount && packages.length) amount.value = packages[0].price;
    select.addEventListener("change", () => {
      const selected = select.options[select.selectedIndex];
      if (amount) amount.value = selected.dataset.price;
    });
  } catch (error) {
    select.innerHTML = "<option>Unable to load packages</option>";
  }
}

async function submitPayment(event) {
  event.preventDefault();
  const form = event.target;
  const payload = {
    phone: form.phone.value,
    amount: form.amount.value,
    account_ref: form.account.value || form.phone.value,
  };
  const response = await fetch("/payments/mpesa/stk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  window.location.href = `status.html?status=${encodeURIComponent(result.status || "queued")}`;
}

document.addEventListener("DOMContentLoaded", () => {
  loadPackages();
  const form = document.querySelector("#payment-form");
  if (form) form.addEventListener("submit", submitPayment);
});

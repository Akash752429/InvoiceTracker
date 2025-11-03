const companyNameElem = document.getElementById('company_name');
const sharedServersElem = document.getElementById('shared_servers');
const privateServersElem = document.getElementById('private_servers');
const mansanElem = document.getElementById('mansan');
const bdateElem = document.getElementById('bdate');
const amountElem = document.getElementById('amount');
const bfileElem = document.getElementById('bfile');
const billForm = document.getElementById('bill-form');

async function uploadPDF(fileInput) {
  if (!fileInput.files.length) return "";
  let formData = new FormData();
  formData.append('file', fileInput.files[0]);
  let resp = await fetch('/upload_pdf', { method: 'POST', body: formData });
  let res = await resp.json();
  return res.url || "";
}

async function addBill(e) {
  e.preventDefault();
  let company_name = companyNameElem.value.trim();
  let shared_servers = sharedServersElem.value;
  let private_servers = privateServersElem.value;
  let mansan = mansanElem.value.trim();
  let bdate = bdateElem.value;
  let amount = amountElem.value;
  let bfile = bfileElem;
  if(!company_name || !shared_servers || !private_servers || !mansan || !bdate || !amount) {
    alert("All fields required!"); return false;
  }
  let fileURL = "";
  if (bfile.files.length) fileURL = await uploadPDF(bfile);

  let formData = new FormData();
  formData.append('company_name', company_name);
  formData.append('shared_servers', shared_servers);
  formData.append('private_servers', private_servers);
  formData.append('mansan', mansan);
  formData.append('bdate', bdate);
  formData.append('amount', amount);
  formData.append('fileURL', fileURL);

  let resp = await fetch('/add_bill', { method: 'POST', body: formData });
  let res = await resp.json();
  if(res.success) {
    billForm.reset();
    alert("Record Database Mein Save Ho Gaya!");
    loadTable();
  } else {
    alert("Database write error!");
  }
  return false;
}

function formatDate(val) {
  if (!val) return "-";
  const d = new Date(val);
  if (isNaN(d)) return val;
  return d.toLocaleDateString('en-IN');
}

async function loadTable() {
  let resp = await fetch('/get_bills');
  let data = await resp.json();
  let table = document.getElementById('showrows');
  table.innerHTML = "";
  data.forEach((r, i) => {
    let tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${i+1}</td>
      <td>${r.company_name}</td>
      <td>${r.shared_servers}</td>
      <td>${r.private_servers}</td>
      <td>${r.mansan}</td>
      <td>${formatDate(r.bdate)}</td>
      <td>₹${parseInt(r.amount).toLocaleString('en-IN')}</td>
      <td>${r.fileURL
        ? `<a href="${r.fileURL}" target="_blank" download>Download Bill</a>`
        : '-'}</td>
    `;
    table.appendChild(tr);
  });
}

window.onload = function() { loadTable(); }

function printBlockchain() {
  const printWindow = window.open('', '', 'width=800,height=600');
  const content = document.getElementById('chain-output').textContent;
  printWindow.document.write('<pre>' + content + '</pre>');
  printWindow.document.close();
  printWindow.focus();
  printWindow.print();
  printWindow.close();
}

function downloadBlockchain() {
  const content = document.getElementById('chain-output').textContent;
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "blockchain_ledger.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

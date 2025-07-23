let pyodide;
let blockchain;

async function loadPyodideAndBlockchain() {
  pyodide = await loadPyodide();
  await pyodide.loadPackage(['micropip']);
  await pyodide.runPythonAsync(`import micropip; await micropip.install('hashlib')`);

  const response = await fetch('blockchain.py');
  const pythonCode = await response.text();
  await pyodide.runPythonAsync(pythonCode);

  blockchain = pyodide.globals.get('blockchain');
}
loadPyodideAndBlockchain();

async function addCertificate() {
  const name = document.getElementById('name').value;
  const degree = document.getElementById('degree').value;
  const year = document.getElementById('year').value;
  const usn = document.getElementById('usn').value;

  const certData = { name, degree, year, usn };

  const result = await pyodide.runPythonAsync(`result = blockchain.add_block(${JSON.stringify(certData)}); result`);
  alert(result);

  const chainOutput = await pyodide.runPythonAsync('blockchain.display_chain()');
  const invalidOutput = await pyodide.runPythonAsync('blockchain.display_invalid_blocks()');
  const isValid = await pyodide.runPythonAsync('blockchain.is_valid()');

  document.getElementById('chain-output').textContent = chainOutput;
  document.getElementById('invalid-output').textContent = invalidOutput;
  document.getElementById('validity-output').textContent = isValid ? '✅ Valid' : '❌ Invalid';

  if (!document.getElementById('continue').checked) {
    document.getElementById('name').value = '';
    document.getElementById('degree').value = '';
    document.getElementById('year').value = '';
    document.getElementById('usn').value = '';
  }
}
// At the end of blockchain.js
window.addCertificate = addCertificate;

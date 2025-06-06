// api/vectorIndex.js

/**
 * Sendet Dateien an das Backend zur Indizierung in der Vektordatenbank
 * @param {Array} files - Array von Objekten mit { file, name }
 * @returns {Promise<any>}
 */
export async function indexFilesInVectorDB(files) {
  const formData = new FormData();
  files.forEach(f => {
    formData.append('files', f.file, f.name);
  });
  const response = await fetch('/api/index/files', {
    method: 'POST',
    body: formData
  });
  if (!response.ok) {
    throw new Error('Fehler beim Indizieren der Dateien');
  }
  return await response.json();
}

/**
 * Fragt die Liste der indizierten Dateien vom Backend ab
 * @returns {Promise<Array<{title: string, size: number, type: string}>>}
 */
export async function getIndexedFiles() {
  const response = await fetch('/api/index/indexed-files');
  if (!response.ok) {
    throw new Error('Fehler beim Laden der indizierten Dateien');
  }
  const data = await response.json();
  return data.data || [];
}

/**
 * Löscht eine indizierte Datei aus dem Vektorstore
 * @param {string} filename - Der Dateiname, der gelöscht werden soll
 * @returns {Promise<any>}
 */
export async function deleteIndexedFile(filename) {
  const response = await fetch('/api/index/delete-file', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename })
  });
  if (!response.ok) {
    throw new Error('Fehler beim Löschen der Datei');
  }
  return await response.json();
}

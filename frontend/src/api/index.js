// api/vectorIndex.js

/**
 * Sendet Dateien an das Backend zur Indizierung in der Vektordatenbank
 * @param {Array} files - Array von Objekten mit { file, name }
 * @returns {Promise<any>}
 */
export async function indexFilesInVectorDB(files, token) {
  const formData = new FormData();
  files.forEach(f => {
    formData.append('files', f.file, f.name);
  });
  const response = await fetch('/api/index/files', {
    method: 'POST',
    headers: token ? { 'Authorization': `Bearer ${token}` } : undefined,
    body: formData
  });
  if (!response.ok) {
    throw new Error('Fehler beim Indizieren der Dateien');
  }
  return await response.json();
}

/**
 * Sendet Text-Einträge an das Backend zur Indizierung
 * @param {Array<{title: string, text: string}>} texts
 */
export async function indexTextsInVectorDB(texts, token) {
  const response = await fetch('/api/index/texts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(texts)
  });
  if (!response.ok) {
    throw new Error('Fehler beim Indizieren der Texte');
  }
  return await response.json();
}

/**
 * Sendet Q&A-Paare an das Backend zur Indizierung
 * @param {Array<{title: string, question: string, answer: string}>} pairs
 */
export async function indexQAPairsInVectorDB(pairs, token) {
  const response = await fetch('/api/index/qa', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(pairs)
  });
  if (!response.ok) {
    throw new Error('Fehler beim Indizieren der Q&A-Paare');
  }
  return await response.json();
}

/**
 * Fragt die Liste der indizierten Dateien vom Backend ab
 * @returns {Promise<Array<{title: string, size: number, type: string}>>}
 */
export async function getIndexedFiles(token) {
  const response = await fetch('/api/index/indexed-files', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : undefined,
  });
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
export async function deleteIndexedFile(filename, token) {
  const response = await fetch('/api/index/delete-file', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ filename })
  });
  if (!response.ok) {
    throw new Error('Fehler beim Löschen der Datei');
  }
  return await response.json();
}

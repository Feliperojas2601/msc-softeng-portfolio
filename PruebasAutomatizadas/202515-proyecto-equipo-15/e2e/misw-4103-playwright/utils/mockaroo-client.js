// Imports
import fs from 'node:fs';
import path from 'node:path';

export function getAprioriDataPool(filename) {
    
    // Read data from local JSON file
    const filePath = path.join(process.cwd(), 'data', filename);
    
    // Synchronous read
    const raw = fs.readFileSync(filePath, 'utf-8');
    
    // Parse JSON
    const data = JSON.parse(raw);
    
    // Return data
    return data; 
}

export async function getDynamicDataFromMockaroo(count = 1, schema = null) {
    
    // Retrieving API Key
    const apiKey = process.env.MOCKAROO_API_KEY;

    // In case there is no API Key
    if (!apiKey) {
        throw new Error('MOCKAROO_API_KEY no está definido en las variables de entorno');
    }

    // In case there is no schema
    if (!schema) {
        throw new Error('No se definió MOCKAROO_SCHEMA ni se envió schema al método');
    }

    // Generating URL
    const url = `https://api.mockaroo.com/api/${schema}?count=${count}&key=${apiKey}`;

    // Obtaining URL
    const response = await fetch(url);

    // If the response is not 200
    if (!response.ok) {
        throw new Error(
            `Error al obtener datos de Mockaroo: ${response.status} ${response.statusText}`
        );
    }

    // Reading as a .json
    return await response.json();
}


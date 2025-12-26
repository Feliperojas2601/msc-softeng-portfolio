// Imports
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Constant to get current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to get the path of a specific test image
export const getTestImagePath = () => {
    const imagePath = path.join(__dirname, '..', 'tests', 'test-data', 'test-image.png');
    return imagePath;
};

// Function to get a random test image path from the test-data directory
export const getRandomTestImagePath = () => {   
    
    // Path where the test images are stored
    const testDataDir = path.join(__dirname, '..', 'tests', 'test-data');

    // Read all image files from the test-data directory
    const files = fs.readdirSync(testDataDir);

    // Filter image files (assuming common image extensions)
    const images = files
        .filter(file => /\.(png|jpg|jpeg|gif|webp)$/i.test(file))
        .map(file => path.join(testDataDir, file));

    // Ensure there are images available
    if (images.length === 0) {
        throw new Error('No se encontraron imágenes en test-data');
    }

    // RandomIndex to select image
    const randomIndex = Math.floor(Math.random() * images.length);

    // Return selected image path
    return images[randomIndex];
};

export const hashString = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash) % 1000;
}
// features/web/support/utils.js
async function getCurrentPage(driver) {
  
  // Retrieving URL
  const url = await driver.getUrl();
  
  // Returning to the user the signin string
  if (url.includes("/#/signin")) return "signin";
  
  // Returning to the user the signin string
  if (url.includes("/#/setup")) return "setup";

  // Returning to the user the signin string
  if (url.includes("/#/dashboard")) return "dashboard";

  // Anything else would associated to unknown
  return "unknown";
}

async function getPublishedPostsTitles(driver) {
  // Espera a que la lista esté presente
  await driver.$('li.gh-posts-list-item, li.gh-list-row').waitForExist({ timeout: 10000 });

  // Toma todos los títulos visibles
  const titleEls = await driver.$$('h3.gh-content-entry-title');

  // Función interna para limpiar espacios y saltos de línea
  function norm(s) {
    return (s || '').replace(/\s+/g, ' ').trim();
  }

  const texts = [];
  for (const el of titleEls) {
    const t = await el.getText();
    texts.push(norm(t));
  }

  return texts;
}

async function captureFinalScreenshot(world) {
    if (world.screenshotManager) {
        await world.screenshotManager.captureFinalStep();
    }
}

function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash) % 1000;
}

function getAprioriData(name) {
    const fs = require('fs');
    const path = require('path');
    const filePath = path.join(__dirname, '../../../test-data', `${name}_apriori.json`);
    try {
        const rawData = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(rawData);
        return data;
    } catch (error) {
        console.error(`Error loading apriori data for ${name}:`, error.message);
        return [];
    }
}

function getRandomAprioriItem(name) {
    const data = getAprioriData(name);
    if (data.length === 0) {
        return null;
    }
    const randomIndex = Math.floor(Math.random() * data.length);
    return data[randomIndex];
}

module.exports = { getCurrentPage, getPublishedPostsTitles, captureFinalScreenshot, hashString, getAprioriData, getRandomAprioriItem };
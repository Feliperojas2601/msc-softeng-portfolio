// Imports
const fs = require('fs');
const path = require('path');
const expect = require("chai").expect;
const { faker } = require('@faker-js/faker');
const { When, Then } = require("@cucumber/cucumber");
const { captureFinalScreenshot, getPublishedPostsTitles, getRandomAprioriItem } = require('../support/utils');

When ('I click on the posts list', async function () {
  
  // Waiting tag to load
  await this.driver.pause(3000);

  // Expecting element to show up
  let element = await this.driver.$('a[data-test-nav="posts"]');

  // Clicking in button
  return await element.click();

});

When('I modify the header', async function () {
  
    this.generatedNewPostTitle = faker.lorem.sentence(2);
  
    // Waiting site to load
    await this.driver.pause(3000);
    
    // Selects the tag data-test-editor
    const titleField = await this.driver.$('textarea[data-test-editor-title-input]');
    
    // Waiting for the title field to be present and displayed
    await titleField.waitForExist({ timeout: 5000 });

    // Waiting for the title field to be displayed
    await titleField.waitForDisplayed({ timeout: 5000 });

    // Clear content and place header info
    await titleField.click();
    
    // Try catch to clear value
    try {await titleField.clearValue();} catch (_) {};

    // Writing text in the header
    await titleField.setValue(this.generatedNewPostTitle);

    // Verifying if the content has been placed
    await this.driver.waitUntil(async () => (await titleField.getValue()) === this.generatedNewPostTitle,{ timeout: 5000, timeoutMsg: 'The title was not established on time.' });

});

When('I modify the header from apriori data', async function () {
    const aprioriData = getRandomAprioriItem('posts');
    this.generatedNewPostTitle = aprioriData ? aprioriData.new_post_title : faker.lorem.sentence(2);
  
    await this.driver.pause(3000);
    const titleField = await this.driver.$('textarea[data-test-editor-title-input]');
    await titleField.waitForExist({ timeout: 5000 });
    await titleField.waitForDisplayed({ timeout: 5000 });
    await titleField.click();
    try {await titleField.clearValue();} catch (_) {};
    await titleField.setValue(this.generatedNewPostTitle);
    await this.driver.waitUntil(async () => (await titleField.getValue()) === this.generatedNewPostTitle,{ timeout: 5000, timeoutMsg: 'The title was not established on time.' });
});

When('I get the restored post title value', async function () {
  const titleField = await this.driver.$('textarea[data-test-editor-title-input]');
  await titleField.waitForExist({ timeout: 5000 });
  await titleField.waitForDisplayed({ timeout: 5000 });

  const currentValue = await titleField.getValue();
  this.restoredPostTitle = (currentValue || '').trim();

  console.log(`El título actual del post es: "${this.restoredPostTitle}"`);
});


When('I click on new post', async function () {
    await this.driver.pause(3000);
    const postsLink = await this.driver.$('a[data-test-nav="new-story"]');
    await postsLink.waitForExist({ timeout: 3000 })
    await postsLink.click();
});

When('I introduce the post title', async function () {
    this.generatedPostTitle = faker.lorem.sentence(2);
    await this.driver.pause(3000);
    const titleField = await this.driver.$('textarea[data-test-editor-title-input], [data-test-editor-title-input]');
    await titleField.waitForExist({ timeout: 3000 });
    await titleField.waitForDisplayed({ timeout: 3000 });
    await titleField.click();
    try {await titleField.clearValue();} catch (_) {};
    await titleField.setValue(this.generatedPostTitle);
    await this.driver.waitUntil(async () => (await titleField.getValue()) === this.generatedPostTitle, { timeout: 5000, timeoutMsg: 'El título no se estableció a tiempo' });
});

When('I introduce the post title from apriori data', async function () {
    const aprioriData = getRandomAprioriItem('posts');
    this.generatedPostTitle = aprioriData ? aprioriData.post_title : faker.lorem.sentence(2);
    await this.driver.pause(3000);
    const titleField = await this.driver.$('textarea[data-test-editor-title-input], [data-test-editor-title-input]');
    await titleField.waitForExist({ timeout: 3000 });
    await titleField.waitForDisplayed({ timeout: 3000 });
    await titleField.click();
    try {await titleField.clearValue();} catch (_) {};
    await titleField.setValue(this.generatedPostTitle);
    await this.driver.waitUntil(async () => (await titleField.getValue()) === this.generatedPostTitle, { timeout: 5000, timeoutMsg: 'El título no se estableció a tiempo' });
});

When ('I introduce the post content', async function () {
    this.generatedPostContent = faker.lorem.paragraphs();

    await this.driver.pause(3000);
    let editor = await this.driver.$('div[class="kg-prose"]');
    await editor.waitForExist({ timeout: 3000 });
    await editor.click();
    await this.driver.keys(this.generatedPostContent);
});

When('I introduce the post content from apriori data', async function () {
    const aprioriData = getRandomAprioriItem('posts');
    this.generatedPostContent = aprioriData ? aprioriData.post_content : faker.lorem.paragraphs();

    await this.driver.pause(3000);
    let editor = await this.driver.$('div[class="kg-prose"]');
    await editor.waitForExist({ timeout: 3000 });
    await editor.click();
    await this.driver.keys(this.generatedPostContent);
});

When('I introduce the post feature image', async function () {
    const imagePath = path.join(__dirname, '..', '..', '..', 'test-data', 'test-image.png');
    await this.driver.pause(3000);
    await this.driver.$('[data-test-editor-title-input]').waitForExist({ timeout: 3000 });
    if (!fs.existsSync(imagePath)) throw new Error(`Image does not exist in: ${imagePath}`);
    const selectors = [
        'input[type="file"][accept*="image"]',
        'section.gh-editor-feature-image input[type="file"]',
        '.gh-editor-image-uploader input[type="file"]',
        '[data-test-file-input]',
        'input[type="file"]'
    ];
    let fileInput = null;
    for (const sel of selectors) {
        const el = await this.driver.$(sel);
        if (await el.isExisting()) { fileInput = el; break; }
    }
    if (!fileInput) {
        throw new Error('No input tags found under input[type="file"] in the uploader.');
    }
    await this.driver.execute((selector) => {
        const el = document.querySelector(selector);
        if (el) el.style.display = 'block';
    }, selectors[0]);
    await fileInput.setValue(imagePath);
    await this.driver.pause(3000);
});

When('I modify the post image', async function () {
  // --- 1) Capturar src previo si existe
  const img = await this.driver.$('div.gh-editor-feature-image img');
  const hadImage = await img.isExisting();
  this.prevImageSrc = hadImage ? await img.getAttribute('src') : null;

  // --- 2) Si había imagen, hover + borrar
  if (hadImage) {
    // Hover sobre el overlay para mostrar el botón de eliminar
    const overlay = await this.driver.$('div.gh-editor-feature-image-overlay');
    await overlay.moveTo();
    await this.driver.pause(200);

    // Click en el botón borrar
    const deleteBtn = await this.driver.$('button.image-action.image-delete');
    await deleteBtn.waitForExist({ timeout: 5000 });
    await deleteBtn.click();
  }

  // --- 3) Subir nueva imagen aleatoria desde /tests/test-data
  // Si existe el botón "Add feature image", haz click
  const addBtn = await this.driver.$('button.gh-editor-feature-image-add-button');
  if (await addBtn.isExisting()) {
    await this.driver.pause(500);
  }

  // Localizar un input[type=file] válido (Ghost puede variar el contenedor)
  const selectors = [
    'input[type="file"][accept*="image"]',
    'section.gh-editor-feature-image input[type="file"]',
    '.gh-editor-image-uploader input[type="file"]',
    '[data-test-file-input]',
    'input[type="file"]'
  ];

  let fileInput = null;
  for (const sel of selectors) {
    const el = await this.driver.$(sel);
    if (await el.isExisting()) { fileInput = el; break; }
  }
  if (!fileInput) throw new Error('No file input found for feature image');

  // Algunas veces el input está oculto: intenta forzar display si es necesario
  try {
    await this.driver.execute((selector) => {
      const el = document.querySelector(selector);
      if (el) el.style.display = 'block';
    }, selectors[0]);
  } catch (_) {}

  // Obtener ruta aleatoria y subir
  const imagePath = path.join(__dirname, '..', '..', '..', 'test-data', 'test-image-2.png');
  if (!fs.existsSync(imagePath)) throw new Error(`Image not found at: ${imagePath}`);
  await fileInput.setValue(imagePath);

  // --- 4) Confirmar que la nueva imagen apareció y guardar el nuevo src
  const newImg = await this.driver.$('div.gh-editor-feature-image img');
  await this.driver.waitUntil(
    async () => await newImg.isExisting(),
    { timeout: 10000, timeoutMsg: 'New feature image did not appear in time' }
  );
  this.newImageSrc = await newImg.getAttribute('src');

  // Log opcional
  console.log('prevImageSrc:', this.prevImageSrc);
  console.log('newImageSrc:', this.newImageSrc);

  // Pausa breve para estabilidad visual
  await this.driver.pause(3000);
});

When ('I click on the settings sidebar', async function () {
    
    // Waiting tag to load
    await this.driver.pause(3000);

    // Expecting element to show up
    let element = await this.driver.$('button[data-test-psm-trigger]');

    // Clicking in button
    return await element.click();

});

When('I scroll within the settings sidebar', async function () {
  
    // Waiting for tag to show
    const element = await this.driver.$('div[class="settings-menu-content"]');

    // Waiting DOM to exist
    await element.waitForExist({ timeout: 3000 });
    
    // Scrolling up to the end
    await this.driver.execute((el) => {
        el.scrollTop = el.scrollHeight;
    }, element);

    // Providing time for the tag to show
    await this.driver.pause(3000);

});

When ('I click on the post history', async function () {
    
    // Waiting tag to load
    await this.driver.pause(3000);

    // Expecting element to show up
    let element = await this.driver.$('button[data-test-toggle="post-history"]');

    // Clicking in button
    return await element.click();

});

When('I click on the previous version', async function () {
  // Asegúrate de que el panel de historial esté abierto
  // y haya botones de "preview-revision"
  // Waiting tag to load
  await this.driver.pause(3000);

  await this.driver.$('button[data-test-button="preview-revision"]').waitForExist({ timeout: 10000 });

  // Toma todas las versiones listadas
  const items = await this.driver.$$(`button[data-test-button="preview-revision"]`);
  if (!items.length) throw new Error('No preview-revision buttons found');

  // Suele interesar la versión inmediatamente anterior a la actual:
  // usa la última del listado (ajústalo si tu UI ordena distinto)
  const target = items[items.length - 1];

  // Si el historial tiene scroll, asegúrate de llevar el target a la vista
  try {
    await target.scrollIntoView();
  } catch (_) {}

  // Click en la versión
  await target.click();

  // Espera a que se renderice el panel de vista previa
  await this.driver.pause(3000);

  // Espera a que aparezca el botón Restore en panel o en modal
  const appeared = await this.driver.waitUntil(async () => {
    const panelBtn = await this.driver.$('button.gh-post-history-version-restore');
    if (await panelBtn.isExisting()) return true;

    const modal = await this.driver.$('div[data-test-modal="restore-revision"]');
    if (await modal.isExisting()) {
      const confirmBtn = await modal.$('button[data-test-button="restore"]');
      return await confirmBtn.isExisting();
    }
    return false;
  }, { timeout: 8000, timeoutMsg: 'Restore control did not appear after selecting a revision' });

  if (!appeared) throw new Error('Restore did not appear after clicking a revision');
});


When('I click on the restore button', async function () {
  // Espera hasta que aparezca el botón de restore en el panel O el modal con su botón
  const clicked = await this.driver.waitUntil(async () => {
    // Variante A: botón “Restore” en el panel de historial
    const panelBtn = await this.driver.$('button.gh-post-history-version-restore');
    if (await panelBtn.isExisting()) {
      await panelBtn.scrollIntoView();
      await panelBtn.click();
      return true;
    }

    // Variante B: modal de confirmación visible
    const modal = await this.driver.$('div[data-test-modal="restore-revision"]');
    if (await modal.isExisting()) {
      const confirmBtn = await modal.$('button[data-test-button="restore"]');
      if (await confirmBtn.isExisting()) {
        await confirmBtn.scrollIntoView();
        await confirmBtn.click();

        // Espera a que el modal desaparezca para confirmar acción
        await this.driver.waitUntil(async () => !(await modal.isExisting()), {
          timeout: 5000,
          timeoutMsg: 'Restore modal did not close after clicking restore'
        });
        return true;
      }
    }

    return false;
  }, { timeout: 10000, timeoutMsg: 'Restore controls not found (panel or modal)' });

  if (!clicked) throw new Error('Could not click restore (panel or modal control missing)');
});

When ('I click on restore post', async function () {
    
    // Waiting tag to load
    await this.driver.pause(6000);

    // Expecting element to show up
    let element = await this.driver.$('button[data-test-button="restore"]');

    // Clicking in button
    return await element.click();

});

When('I click on return to all posts', async function() {
    
    // Waiting site to load
    await this.driver.pause(3000);
  
    // Selects the tag publish-save
    const posts = await this.driver.$('a[data-test-link="posts"]');

    // Clicking in button
    return await posts.click();
    
});

Then('I may confirm that the post image has been changed', async function () {
  // Asegura que las variables existan
  expect(this.prevImageSrc, 'Previous image src is undefined or empty')
    .to.be.a('string').and.not.empty;
  expect(this.newImageSrc, 'New image src is undefined or empty')
    .to.be.a('string').and.not.empty;

  // Compara las dos rutas
  expect(this.newImageSrc).to.not.equal(
    this.prevImageSrc,
    `Expected the new image src to differ, but both were "${this.newImageSrc}"`
  );

  console.log(`Image successfully changed from:\n${this.prevImageSrc}\nto:\n${this.newImageSrc}`);
  await captureFinalScreenshot(this);
});

When ('I click on publish', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('button[data-test-button="publish-flow"]');
    return await element.click();
});

When ('I click on continue', async function () {
    await this.driver.pause(4000);
    let element = await this.driver.$('button[data-test-button="continue"]');
    return await element.click();
});

When ('I click on publish right now', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('button[data-test-button="confirm-publish"]');
    return await element.click();
});

When ('I close the window', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('button[class="close"]');
    return await element.click();
});

When ('I click on go back to posts', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('a[data-test-nav="posts"]');
    return await element.click();
});

When('I press on update', async function() {
    
    // Waiting site to load
    await this.driver.pause(5000);
  
    // Selects the tag publish-save
    const update = await this.driver.$('button[data-test-button="publish-save"]');

    // Clicking in button
    return await update.click();

});

When('I click on return to posts', async function() {
    
    // Waiting site to load
    await this.driver.pause(5000);
  
    // Selects the tag publish-save
    const posts = await this.driver.$('a[data-test-link="posts"]');

    // Clicking in button
    return await posts.click();
    
});

When('I click the post content to leave it empty', async function () {
    await this.driver.pause(3000);
    let editor = await this.driver.$('div[class="kg-prose"]');
    await editor.waitForExist({ timeout: 3000 });
    await editor.click();
    await this.driver.keys('');
});

When('I click within the created post', async function () {
  // Espera breve por si la lista de posts aún está renderizando
  await this.driver.pause(2000);

  // Normalizamos el título que se creó antes
  const expected = (this.generatedPostTitle || '').trim();
  if (!expected) this.assert.fail('No generatedPostTitle stored in context');

  // Espera a que haya items en la lista
  await this.driver.$('li.gh-list-row, li.gh-posts-list-item').waitForExist({ timeout: 10000 });

  // Busca el título con tu helper (para verificar visibilidad y debugging)
  const titles = await getPublishedPostsTitles(this.driver);
  console.log('Posts encontrados:', titles);

  // Ahora itera directamente sobre las filas
  const rows = await this.driver.$$('li.gh-list-row, li.gh-posts-list-item');

  let found = false;
  for (const row of rows) {
    const h3 = await row.$('h3.gh-content-entry-title');
    if (!h3) continue;

    const text = (await h3.getText() || '').replace(/\s+/g, ' ').trim();
    if (text === expected) {
      console.log(`✅ Found post: "${text}"`);

      // El enlace <a> que realmente abre el post
      const link = await row.$('a.gh-post-list-title');
      if (await link.isExisting()) {
        await link.click();
      } else {
        // Si por alguna razón no existe el <a>, clic directamente en el <h3>
        await h3.click();
      }

      // Espera a que cargue el editor
      await this.driver.pause(2000);
      found = true;
      break;
    }
  }

  if (!found) {
    console.log(`No post found with title: "${expected}"`);
    this.assert.fail(`No post found with title "${expected}"`);
  }
});

When('I click within the modified post', async function () {
  
    // Espera breve por si la lista de posts aún está renderizando
  await this.driver.pause(2000);

  // Normalizamos el título que se creó antes
  const expected = (this.generatedNewPostTitle || '').trim();
  if (!expected) this.assert.fail('No generatedNewPostTitle stored in context');

  // Espera a que haya items en la lista
  await this.driver.$('li.gh-list-row, li.gh-posts-list-item').waitForExist({ timeout: 10000 });

  // Busca el título con tu helper (para verificar visibilidad y debugging)
  const titles = await getPublishedPostsTitles(this.driver);
  console.log('Posts encontrados:', titles);

  // Ahora itera directamente sobre las filas
  const rows = await this.driver.$$('li.gh-list-row, li.gh-posts-list-item');

  let found = false;
  for (const row of rows) {
    const h3 = await row.$('h3.gh-content-entry-title');
    if (!h3) continue;

    const text = (await h3.getText() || '').replace(/\s+/g, ' ').trim();
    if (text === expected) {
      console.log(`✅ Found post: "${text}"`);

      // El enlace <a> que realmente abre el post
      const link = await row.$('a.gh-post-list-title');
      if (await link.isExisting()) {
        await link.click();
      } else {
        // Si por alguna razón no existe el <a>, clic directamente en el <h3>
        await h3.click();
      }

      // Espera a que cargue el editor
      await this.driver.pause(2000);
      found = true;
      break;
    }
  }

  if (!found) {
    console.log(`No post found with title: "${expected}"`);
    this.assert.fail(`No post found with title "${expected}"`);
  }
});

When('I click on the created post', async function () {
    await this.driver.pause(3000);
    const postTitle = this.generatedPostTitle;
    const postElements = await this.driver.$$('h3.gh-content-entry-title');
    for (const element of postElements) {
        const text = await element.getText();
        if (text.trim() === postTitle.trim()) {
            await element.click();
            return;
        }
    }
    throw new Error(`No se encontró el post con título: ${postTitle}`);
});

When('I click on the post settings', async function () {
    await this.driver.pause(3000);
    const settingsButton = await this.driver.$('button[data-test-psm-trigger]');
    await settingsButton.waitForExist({ timeout: 3000 });
    await settingsButton.click();
});

Then('I should see the post title untitled', async function () {
    await this.driver.pause(3000);
    const titleElements = await this.driver.$$('h3.gh-content-entry-title');
    await titleElements[0].waitForExist({ timeout: 10000 });
    const allTitles = await Promise.all(
        titleElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const expectedTitle = "(Untitled)";
    const titleFound = allTitles.some(title => title === expectedTitle);
    expect(titleFound, `El título "${expectedTitle}" no se encontró en la lista de posts. Títulos encontrados: ${allTitles.join(', ')}`).to.be.true;
    await captureFinalScreenshot(this);
});

Then('I should find the new post titled', async function () {
  
  await this.driver.pause(3000);
  
  // Waiting items to load
  await this.driver.$('li.gh-posts-list-item').waitForExist({ timeout: 10000 });

  // Take all the h3 elements in the list
  const titleEls = await this.driver.$$('h3.gh-content-entry-title');

  // Providing log info
  console.log(`Encontré ${titleEls.length} títulos en la lista.`);

  // Function to normalize spaces
  const norm = (s) => s.replace(/\s+/g, ' ').trim();

  // Obtaining all texts
  const texts = [];

  // Getting all texts
  for (const el of titleEls) {
    
    // Getting text
    const t = await el.getText();
    
    // Saving normalized text
    texts.push(norm(t));
  }

  // Log to present
  texts.forEach((t, i) => console.log(`[#${i}] "${t}"`));

  // Does anyone match exactly
  const found = texts.some(t => t === norm(this.generatedNewPostTitle));

  // Expecting to find it
  const expect = require('chai').expect;
  
  // Assertion with detailed message
  expect(found, `No se encontró un post con título exactamente: "${this.generatedNewPostTitle}". Títulos vistos: ${JSON.stringify(texts)}`).to.be.true;
  
  await captureFinalScreenshot(this);
});

Then('I should find a restored post titled', async function () {
  
    // 1) Espera a que aparezcan items en la lista
  await this.driver.$('li.gh-posts-list-item').waitForExist({ timeout: 10000 });

  // 2) Toma todos los h3 que muestran el título
  const titleEls = await this.driver.$$('h3.gh-content-entry-title');

  console.log(`Encontré ${titleEls.length} títulos en la lista.`);

  // Función para normalizar espacios y saltos de línea
  const norm = (s) => s.replace(/\s+/g, ' ').trim();

  // 3) Obtén todos los textos de una
  const texts = [];
  for (const el of titleEls) {
    const t = await el.getText();
    texts.push(norm(t));
  }

  // Log para depurar
  texts.forEach((t, i) => console.log(`[#${i}] "${t}"`));

  // 4) ¿Alguno coincide exactamente con el esperado?
  const found = texts.some(t => t === norm(this.generatedPostTitle));

  const expect = require('chai').expect;
  expect(
    found,
    `No se encontró un post con título exactamente: "${this.generatedPostTitle}". Títulos vistos: ${JSON.stringify(texts)}`
  ).to.be.true;

  await captureFinalScreenshot(this);
});

Then('I should see the new post title', async function () {
    await this.driver.pause(3000);
    const titleElements = await this.driver.$$('h3.gh-content-entry-title');
    await titleElements[0].waitForExist({ timeout: 10000 });
    const allTitles = await Promise.all(
        titleElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const expectedTitle = this.generatedPostTitle.trim();
    const titleFound = allTitles.some(title => title === expectedTitle);
    expect(titleFound, `El título "${expectedTitle}" no se encontró en la lista de posts. Títulos encontrados: ${allTitles.join(', ')}`).to.be.true;

    await captureFinalScreenshot(this);
});

Then('I should see the restored post title', async function () {
  // Normaliza/valida el esperado
  const expectedTitle = (this.restoredPostTitle || '').replace(/\s+/g, ' ').trim();
  if (!expectedTitle) throw new Error('restoredPostTitle no está definido en el contexto');

  // Asegúrate de estar en la lista y que haya items
  await this.driver.$('li.gh-posts-list-item, li.gh-list-row').waitForExist({ timeout: 15000 });

  // Espera a que al menos exista un título
  await this.driver.$('h3.gh-content-entry-title').waitForExist({ timeout: 15000 });

  // Busca el h3 cuyo texto normalizado coincida exactamente
  const h3 = await this.driver.$(`//h3[contains(@class,"gh-content-entry-title") and normalize-space()="${expectedTitle}"]`);
  await h3.waitForExist({
    timeout: 15000,
    timeoutMsg: `No se encontró el título restaurado "${expectedTitle}" en la lista`
  });

  await captureFinalScreenshot(this);
});

When('I click on delete post', async function () {
    await this.driver.pause(3000);
    const postTitle = this.generatedPostTitle.trim();
    const postElements = await this.driver.$$('h3.gh-content-entry-title');
    let postElement = null;
    for (const element of postElements) {
        const text = await element.getText();
        if (text.trim() === postTitle) {
            postElement = element;
            break;
        }
    }
    if (!postElement) {
        throw new Error(`No se encontró el post con título: ${postTitle}`);
    }
    await postElement.click({ button: 'right' });
    await this.driver.pause(1000);
    const deleteButton = await this.driver.$('button[data-test-button="delete"]');
    await deleteButton.waitForExist({ timeout: 3000 });
    await deleteButton.click();
    await this.driver.pause(1000);
    const confirmButton = await this.driver.$('button[data-test-button="confirm"]');
    await confirmButton.waitForExist({ timeout: 3000 });
    await confirmButton.click();
    await this.driver.pause(2000);
});

Then('I should not see the deleted post title', async function () {
    await this.driver.pause(3000);
    const titleElements = await this.driver.$$('h3.gh-content-entry-title');
    if (titleElements.length === 0) {
        return;
    }
    const allTitles = await Promise.all(
        titleElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const deletedTitle = this.generatedPostTitle.trim();
    const titleFound = allTitles.some(title => title === deletedTitle);
    expect(titleFound, `El post "${deletedTitle}" NO debería estar en la lista pero fue encontrado. Títulos encontrados: ${allTitles.join(', ')}`).to.be.false;

    await captureFinalScreenshot(this);
});
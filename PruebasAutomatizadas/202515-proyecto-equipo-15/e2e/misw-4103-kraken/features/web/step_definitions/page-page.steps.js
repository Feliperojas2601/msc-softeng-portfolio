const fs = require('fs');
const path = require('path');
const expect = require("chai").expect;
const { faker } = require('@faker-js/faker');
const { When, Then } = require("@cucumber/cucumber");
const { captureFinalScreenshot, getRandomAprioriItem } = require('../support/utils');

When('I click on new page', async function () {
    await this.driver.pause(3000);
    const pagesLink = await this.driver.$('a[data-test-new-page-button]');
    await pagesLink.waitForExist({ timeout: 3000 })
    await pagesLink.click();
});

When('I introduce the page title', async function () {
    this.generatedPageTitle = faker.lorem.sentence();
    await this.driver.pause(3000);
    const titleField = await this.driver.$('textarea[data-test-editor-title-input], [data-test-editor-title-input]');
    await titleField.waitForExist({ timeout: 3000 });
    await titleField.waitForDisplayed({ timeout: 3000 });
    await titleField.click();
    try {
        await titleField.clearValue();
    } catch (_) {}
    await titleField.setValue(this.generatedPageTitle);
    await this.driver.waitUntil(
        async () => (await titleField.getValue()) === this.generatedPageTitle,
        { timeout: 5000, timeoutMsg: 'El título no se estableció a tiempo' }
    );
});

When ('I introduce the page content', async function () {
    this.generatedPageContent = faker.lorem.paragraphs();
    await this.driver.pause(3000);
    let editor = await this.driver.$('div[class="kg-prose"]');
    await editor.waitForExist({ timeout: 3000 });
    await editor.click();
    await this.driver.keys(this.generatedPageContent);
});

When('I introduce the page title from apriori data', async function () {
    const aprioriData = getRandomAprioriItem('pages');
    this.generatedPageTitle = aprioriData ? aprioriData.page_title : faker.lorem.sentence();
    await this.driver.pause(3000);
    const titleField = await this.driver.$('textarea[data-test-editor-title-input], [data-test-editor-title-input]');
    await titleField.waitForExist({ timeout: 3000 });
    await titleField.waitForDisplayed({ timeout: 3000 });
    await titleField.click();
    try {
        await titleField.clearValue();
    } catch (_) {}
    await titleField.setValue(this.generatedPageTitle);
    await this.driver.waitUntil(
        async () => (await titleField.getValue()) === this.generatedPageTitle,
        { timeout: 5000, timeoutMsg: 'El título no se estableció a tiempo' }
    );
});

When('I introduce the page content from apriori data', async function () {
    const aprioriData = getRandomAprioriItem('pages');
    this.generatedPageContent = aprioriData ? aprioriData.page_content : faker.lorem.paragraphs();
    await this.driver.pause(3000);
    let editor = await this.driver.$('div[class="kg-prose"]');
    await editor.waitForExist({ timeout: 3000 });
    await editor.click();
    await this.driver.keys(this.generatedPageContent);
});

When ('I click on go back to pages', async function () {
    await this.driver.pause(3000);
    let element = await this.driver.$('a[data-test-nav="pages"]');
    return await element.click();
});

Then('I should see the new page title', async function () {
    await this.driver.pause(3000);
    const titleElements = await this.driver.$$('h3.gh-content-entry-title');
    await titleElements[0].waitForExist({ timeout: 10000 });
    const allTitles = await Promise.all(
        titleElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const expectedTitle = this.generatedPageTitle.trim();
    const titleFound = allTitles.some(title => title === expectedTitle);
    expect(titleFound, `El título "${expectedTitle}" no se encontró en la lista de pages. Títulos encontrados: ${allTitles.join(', ')}`).to.be.true;
    await captureFinalScreenshot(this);
});

When('I introduce the page feature image', async function () {
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

When('I click on the created page', async function () {
    await this.driver.pause(3000);
    const pageTitle = this.generatedPageTitle;
    const pageElements = await this.driver.$$('h3.gh-content-entry-title');
    for (const element of pageElements) {
        const text = await element.getText();
        if (text.trim() === pageTitle.trim()) {
            await element.click();
            return;
        }
    }
    throw new Error(`No se encontró la página con título: ${pageTitle}`);
});

When('I click on the page settings', async function () {
    await this.driver.pause(3000);
    const settingsButton = await this.driver.$('button[data-test-psm-trigger]');
    await settingsButton.waitForExist({ timeout: 3000 });
    await settingsButton.click();
});
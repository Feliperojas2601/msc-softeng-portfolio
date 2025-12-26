const expect = require("chai").expect;
const { When, Then } = require("@cucumber/cucumber");
const { faker } = require('@faker-js/faker');
const { captureFinalScreenshot } = require('../support/utils');

When('I click on new tag', async function () {
    await this.driver.pause(3000);
    const tagLink = await this.driver.$('a[href="#/tags/new/"]');
    await tagLink.waitForExist({ timeout: 3000 });
    await tagLink.click();
});

When('I introduce the tag name and slug', async function () {
    this.generatedTagName = faker.word.noun();
    await this.driver.pause(3000);
    const tagNameField = await this.driver.$('input#tag-name');
    await tagNameField.waitForExist({ timeout: 3000 });
    await tagNameField.waitForDisplayed({ timeout: 3000 });
    await tagNameField.click();
    try {
        await tagNameField.clearValue();
    } catch (_) {}
    await tagNameField.setValue(this.generatedTagName);
    await this.driver.pause(500);
    const tagSlugField = await this.driver.$('input#tag-slug');
    await tagSlugField.waitForExist({ timeout: 3000 });
    await tagSlugField.click();
    try {
        await tagSlugField.clearValue();
    } catch (_) {}
    await tagSlugField.setValue(this.generatedTagName);
});

When('I introduce the tag description', async function () {
    this.generatedTagDescription = faker.lorem.sentence();
    await this.driver.pause(3000);
    const tagDescriptionField = await this.driver.$('textarea#tag-description');
    await tagDescriptionField.waitForExist({ timeout: 3000 });
    await tagDescriptionField.click();
    try {
        await tagDescriptionField.clearValue();
    } catch (_) {}
    await tagDescriptionField.setValue(this.generatedTagDescription);
});

When('I click on save tag', async function () {
    await this.driver.pause(3000);
    const saveButton = await this.driver.$('button.gh-btn-primary');
    await saveButton.waitForExist({ timeout: 3000 });
    await saveButton.click();
});

When('I assign the created tag to the post', async function () {
    await this.driver.pause(3000);
    const tagInput = await this.driver.$('input.ember-power-select-trigger-multiple-input');
    await tagInput.waitForExist({ timeout: 3000 });
    await tagInput.click();
    await this.driver.pause(500);
    await this.driver.keys(this.generatedTagName);
    await this.driver.pause(500);
    await this.driver.keys('Enter');
});

Then('I should see the assigned tag in the post', async function () {
    await this.driver.pause(3000);
    const tagElements = await this.driver.$$('li.ember-power-select-multiple-option');
    const allTags = await Promise.all(
        tagElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const expectedTag = this.generatedTagName.trim();
    const tagFound = allTags.some(tag => tag === expectedTag);
    expect(tagFound, `El tag "${expectedTag}" no se encontró en los tags asignados. Tags encontrados: ${allTags.join(', ')}`).to.be.true;

    await captureFinalScreenshot(this);
});

When('I assign the created tag to the page', async function () {
    await this.driver.pause(3000);
    const tagInput = await this.driver.$('input.ember-power-select-trigger-multiple-input');
    await tagInput.waitForExist({ timeout: 3000 });
    await tagInput.click();
    await this.driver.pause(500);
    await this.driver.keys(this.generatedTagName);
    await this.driver.pause(500);
    await this.driver.keys('Enter');
});

Then('I should see the assigned tag in the page', async function () {
    await this.driver.pause(3000);
    const tagElements = await this.driver.$$('li.ember-power-select-multiple-option');
    const allTags = await Promise.all(
        tagElements.map(async (element) => {
            const text = await element.getText();
            return text.trim();
        })
    );
    const expectedTag = this.generatedTagName.trim();
    const tagFound = allTags.some(tag => tag === expectedTag);
    expect(tagFound, `El tag "${expectedTag}" no se encontró en los tags asignados. Tags encontrados: ${allTags.join(', ')}`).to.be.true;

    await captureFinalScreenshot(this);
});